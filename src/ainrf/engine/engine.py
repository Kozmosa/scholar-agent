from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import cast
from urllib.request import urlretrieve
from uuid import uuid4

from ainrf.agents import AgentAdapter, AgentExecutionError
from ainrf.artifacts import (
    ArtifactRef,
    ArtifactType,
    EvidenceRecord,
    EvidenceType,
    GateType,
    PaperCard,
    PaperCardStatus,
    ReproductionStrategy,
    ReproductionTask,
    ReproductionTaskStatus,
    ResourceUsage,
)
from ainrf.events import TaskEventCategory, TaskEventService
from ainrf.execution import ContainerConfig
from ainrf.gates import HumanGateManager, PlanApprovalGatePayload
from ainrf.parsing import PaperParser, ParseFailure, ParseRequest
from ainrf.state import ArtifactQuery, AtomicTaskRecord, JsonStateStore, TaskRecord, TaskStage

from ainrf.engine.models import AtomicTaskSpec


def utc_now() -> datetime:
    return datetime.now().astimezone()


@dataclass(slots=True)
class EngineContext:
    state_store: JsonStateStore
    event_service: TaskEventService
    gate_manager: HumanGateManager
    parser: PaperParser
    agent_adapter: AgentAdapter
    runtime_root: Path


class TaskEngine:
    def __init__(self, context: EngineContext) -> None:
        self._context = context

    async def run_once(self) -> bool:
        task = self._next_task()
        if task is None:
            return False
        if task.mode.value != "deep_reproduction":
            self._fail_task(task, reason="mode_not_implemented", detail="Mode is not implemented in P7")
            return True
        if task.status is TaskStage.PLANNING:
            await self._advance_planning_task(task)
            return True
        if task.status is TaskStage.EXECUTING:
            await self._advance_executing_task(task)
            return True
        return False

    async def run_forever(self, poll_interval_seconds: float) -> None:
        while True:
            ran = await self.run_once()
            if not ran:
                await asyncio.sleep(poll_interval_seconds)

    def _next_task(self) -> TaskRecord | None:
        candidates = [
            task
            for task in self._context.state_store.list_resumable_tasks()
            if task.status in {TaskStage.PLANNING, TaskStage.EXECUTING}
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda item: item.created_at)
        for task in candidates:
            if self._context.gate_manager.get_active_gate(task.task_id) is None:
                return task
        return None

    async def _advance_planning_task(self, task: TaskRecord) -> None:
        self._publish_task_event(task.task_id, "task.started", {"current_stage": task.status.value})
        paper_card = self._find_structured_paper_card(task.task_id)
        if paper_card is None:
            await self._ingest_task(task)
            task = self._context.state_store.load_task(task.task_id) or task
        if self._context.gate_manager.get_active_gate(task.task_id) is not None:
            return
        if self._has_waiting_plan_gate(task):
            return
        await self._plan_task(task)

    async def _advance_executing_task(self, task: TaskRecord) -> None:
        if not task.checkpoint.pending_queue:
            self._complete_task(task, termination_reason=None)
            return
        raw_step = task.checkpoint.pending_queue[0]
        step = AtomicTaskSpec(
            step_id=str(raw_step.details.get("step_id", raw_step.step)),
            kind=raw_step.step,
            title=str(raw_step.details.get("title", raw_step.step)),
            payload=dict(raw_step.details.get("payload", {}))
            if isinstance(raw_step.details.get("payload"), dict)
            else {},
        )
        container = self._container_from_task(task)
        try:
            await self._context.agent_adapter.bootstrap(container)
            result = await self._context.agent_adapter.execute_step(
                container=container,
                step=step,
                context={"task_id": task.task_id, "config": task.config},
            )
        except AgentExecutionError as exc:
            self._fail_task(task, reason="agent_execution_failed", detail=str(exc))
            return
        updated = task.model_copy(
            update={
                "updated_at": utc_now(),
                "checkpoint": task.checkpoint.model_copy(
                    update={
                        "completed_steps": [
                            *task.checkpoint.completed_steps,
                            AtomicTaskRecord(
                                step=step.kind,
                                status=result.status,
                                at=result.finished_at,
                                details={
                                    "step_id": step.step_id,
                                    "title": step.title,
                                    "summary": result.summary,
                                },
                            ),
                        ],
                        "pending_queue": task.checkpoint.pending_queue[1:],
                    }
                ),
                "budget_used": self._merge_budget(task.budget_used, result.resource_usage),
            }
        )
        if self._budget_exhausted(updated):
            updated = updated.model_copy(update={"termination_reason": "budget_exhausted"})
        self._context.state_store.save_task(updated)
        self._publish_task_event(
            updated.task_id,
            "task.progress",
            {
                "stage": updated.status.value,
                "step": step.kind,
                "detail": result.summary,
                "remaining_steps": len(updated.checkpoint.pending_queue),
            },
        )
        if updated.termination_reason == "budget_exhausted":
            self._complete_task(updated, termination_reason="budget_exhausted")
            return
        if not updated.checkpoint.pending_queue:
            self._complete_task(updated, termination_reason=None)

    async def _ingest_task(self, task: TaskRecord) -> None:
        papers = task.config.get("papers")
        if not isinstance(papers, list) or not papers:
            self._fail_task(task, reason="invalid_task_config", detail="Task config is missing papers")
            return
        if not isinstance(papers[0], dict):
            self._fail_task(
                task,
                reason="invalid_task_config",
                detail="Task paper source must be an object",
            )
            return
        source = cast(dict[str, object], papers[0])
        request = await self._build_parse_request(task.task_id, source)
        parse_result = await self._context.parser.parse_pdf(request)
        if isinstance(parse_result, ParseFailure):
            evidence = EvidenceRecord(
                artifact_id=f"ev-{uuid4().hex[:8]}",
                source_task_id=task.task_id,
                evidence_type=EvidenceType.PARSE_FAILURE,
                statement=parse_result.message,
                content=parse_result.message,
                summary=parse_result.failure_type.value,
            )
            self._context.state_store.save_artifact(evidence)
            self._publish_artifact_event("artifact.created", evidence)
            self._fail_task(task, reason="parse_failed", detail=parse_result.message)
            return

        paper_card = PaperCard(
            artifact_id=f"pc-{uuid4().hex[:8]}",
            source_task_id=task.task_id,
            status=PaperCardStatus.STRUCTURED,
            title=parse_result.metadata.title or str(source["title"]),
            authors=parse_result.metadata.authors,
            abstract=parse_result.metadata.abstract,
            source_uri=str(source.get("pdf_url") or source.get("pdf_path")),
            method_summary="Parsed paper markdown available for planning.",
            summary="Structured paper card from MinerU ingestion.",
        )
        self._context.state_store.save_artifact(paper_card)
        self._publish_artifact_event("artifact.created", paper_card)
        updated = task.model_copy(
            update={
                "updated_at": utc_now(),
                "checkpoint": task.checkpoint.model_copy(
                    update={
                        "artifact_refs": [
                            *task.checkpoint.artifact_refs,
                            ArtifactRef(
                                artifact_type=ArtifactType.PAPER_CARD,
                                artifact_id=paper_card.artifact_id,
                            ),
                        ],
                    }
                ),
            }
        )
        self._context.state_store.save_task(updated)

    async def _plan_task(self, task: TaskRecord) -> None:
        paper_card = self._find_structured_paper_card(task.task_id)
        if paper_card is None:
            self._fail_task(task, reason="missing_paper_card", detail="Planning requires a structured paper card")
            return
        container = self._container_from_task(task)
        await self._context.agent_adapter.bootstrap(container)
        prompt = "Generate a deep reproduction plan."
        latest_feedback = self._latest_plan_feedback(task)
        context = {
            "task_id": task.task_id,
            "paper_card": paper_card.model_dump(mode="json"),
            "task_config": task.config,
            "latest_feedback": latest_feedback,
        }
        plan = await self._context.agent_adapter.plan_reproduction(
            container=container,
            prompt=prompt,
            context=context,
        )
        reproduction_task = self._existing_reproduction_task(task.task_id)
        if reproduction_task is None:
            reproduction_task = ReproductionTask(
                artifact_id=f"rt-{uuid4().hex[:8]}",
                source_task_id=task.task_id,
                status=ReproductionTaskStatus.PROPOSED,
                strategy=ReproductionStrategy(plan.strategy),
                target_paper_id=plan.target_paper_id,
                objective=plan.summary,
                success_criteria=plan.success_criteria,
                related_artifacts=[
                    ArtifactRef(
                        artifact_type=ArtifactType.PAPER_CARD,
                        artifact_id=paper_card.artifact_id,
                    )
                ],
                summary=plan.summary,
            )
            event_name = "artifact.created"
        else:
            reproduction_task = reproduction_task.model_copy(
                update={
                    "updated_at": utc_now(),
                    "status": ReproductionTaskStatus.PROPOSED,
                    "strategy": ReproductionStrategy(plan.strategy),
                    "target_paper_id": plan.target_paper_id,
                    "objective": plan.summary,
                    "success_criteria": plan.success_criteria,
                    "summary": plan.summary,
                }
            )
            event_name = "artifact.updated"
        self._context.state_store.save_artifact(reproduction_task)
        self._publish_artifact_event(event_name, reproduction_task)
        updated = task.model_copy(
            update={
                "updated_at": utc_now(),
                "checkpoint": task.checkpoint.model_copy(
                    update={
                        "pending_queue": [
                            AtomicTaskRecord(
                                step=item.kind,
                                details={
                                    "step_id": item.step_id,
                                    "title": item.title,
                                    "payload": item.payload,
                                },
                            )
                            for item in plan.steps
                        ],
                        "artifact_refs": self._upsert_artifact_ref(
                            task.checkpoint.artifact_refs,
                            ArtifactRef(
                                artifact_type=ArtifactType.REPRODUCTION_TASK,
                                artifact_id=reproduction_task.artifact_id,
                            ),
                        ),
                    }
                ),
            }
        )
        self._context.state_store.save_task(updated)
        gate_payload = PlanApprovalGatePayload(
            mode=task.mode.value,
            summary=plan.summary,
            milestones=plan.milestones,
            estimated_steps=plan.estimated_steps,
            strategy=plan.strategy,
            target_paper_id=plan.target_paper_id,
            success_criteria=plan.success_criteria,
        )
        next_task, gate = await self._context.gate_manager.trigger_gate(
            task=updated,
            gate_type=GateType.PLAN_APPROVAL,
            summary=plan.summary,
            payload=gate_payload.model_dump(mode="json"),
            yolo=bool(task.config.get("yolo", False)),
        )
        if not bool(task.config.get("yolo", False)):
            await self._context.gate_manager.send_waiting_webhook(task=next_task, gate=gate)

    async def _build_parse_request(self, task_id: str, source_mapping: dict[str, object]) -> ParseRequest:
        pdf_path = source_mapping.get("pdf_path")
        if isinstance(pdf_path, str) and pdf_path:
            return ParseRequest(
                pdf_path=Path(pdf_path),
                source_url=None,
                role=self._optional_str(source_mapping, "role"),
            )
        pdf_url = source_mapping.get("pdf_url")
        if not isinstance(pdf_url, str) or not pdf_url:
            raise ValueError("Task paper source requires pdf_path or pdf_url")
        runtime_dir = self._context.runtime_root / "runtime" / "pdfs"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        target_path = runtime_dir / f"{task_id}-{uuid4().hex[:8]}.pdf"
        urlretrieve(pdf_url, target_path)
        return ParseRequest(
            pdf_path=target_path,
            source_url=pdf_url,
            role=self._optional_str(source_mapping, "role"),
        )

    def _find_structured_paper_card(self, task_id: str) -> PaperCard | None:
        for artifact in self._context.state_store.query_artifacts(
            ArtifactType.PAPER_CARD,
            ArtifactQuery(source_task_id=task_id),
        ):
            if isinstance(artifact, PaperCard) and artifact.source_task_id == task_id:
                return artifact
        return None

    def _existing_reproduction_task(self, task_id: str) -> ReproductionTask | None:
        for artifact in self._context.state_store.query_artifacts(
            ArtifactType.REPRODUCTION_TASK,
            ArtifactQuery(source_task_id=task_id),
        ):
            if isinstance(artifact, ReproductionTask) and artifact.source_task_id == task_id:
                return artifact
        return None

    def _has_waiting_plan_gate(self, task: TaskRecord) -> bool:
        active_gate = self._context.gate_manager.get_active_gate(task.task_id)
        return active_gate is not None and active_gate.gate_type is GateType.PLAN_APPROVAL

    def _latest_plan_feedback(self, task: TaskRecord) -> str | None:
        for gate in reversed(task.gates):
            if gate.gate_type is GateType.PLAN_APPROVAL and gate.feedback:
                return gate.feedback
        return None

    def _container_from_task(self, task: TaskRecord) -> ContainerConfig:
        container = task.config.get("container")
        if not isinstance(container, dict):
            raise ValueError("Task config is missing container settings")
        container_mapping = cast(dict[str, object], container)
        return ContainerConfig(
            host=self._required_str(container_mapping, "host"),
            port=self._optional_int(container_mapping, "port", default=22),
            user=self._required_str(container_mapping, "user"),
            ssh_key_path=self._optional_str(container_mapping, "ssh_key_path"),
            project_dir=self._required_str(container_mapping, "project_dir"),
        )

    def _merge_budget(
        self,
        budget: ResourceUsage,
        usage_delta: dict[str, float | None],
    ) -> ResourceUsage:
        return ResourceUsage(
            gpu_hours=(budget.gpu_hours or 0.0) + float(usage_delta.get("gpu_hours") or 0.0),
            api_cost_usd=(budget.api_cost_usd or 0.0) + float(usage_delta.get("api_cost_usd") or 0.0),
            wall_clock_hours=(budget.wall_clock_hours or 0.0)
            + float(usage_delta.get("wall_clock_hours") or 0.0),
        )

    def _budget_exhausted(self, task: TaskRecord) -> bool:
        checks = (
            (task.budget_limit.gpu_hours, task.budget_used.gpu_hours),
            (task.budget_limit.api_cost_usd, task.budget_used.api_cost_usd),
            (task.budget_limit.wall_clock_hours, task.budget_used.wall_clock_hours),
        )
        return any(limit is not None and used is not None and used >= limit for limit, used in checks)

    def _complete_task(self, task: TaskRecord, termination_reason: str | None) -> None:
        updated = task.model_copy(
            update={
                "status": TaskStage.COMPLETED,
                "updated_at": utc_now(),
                "termination_reason": termination_reason,
                "checkpoint": task.checkpoint.model_copy(update={"current_stage": TaskStage.COMPLETED}),
            }
        )
        self._context.state_store.save_task(updated)
        self._publish_task_event(
            updated.task_id,
            "task.completed",
            {"current_stage": updated.status.value, "termination_reason": updated.termination_reason},
        )
        self._context.gate_manager.clear_secret(updated.task_id)

    def _fail_task(self, task: TaskRecord, *, reason: str, detail: str) -> None:
        updated = task.model_copy(
            update={
                "status": TaskStage.FAILED,
                "updated_at": utc_now(),
                "termination_reason": reason,
                "checkpoint": task.checkpoint.model_copy(update={"current_stage": TaskStage.FAILED}),
            }
        )
        self._context.state_store.save_task(updated)
        self._publish_task_event(
            updated.task_id,
            "task.failed",
            {"current_stage": updated.status.value, "termination_reason": reason, "detail": detail},
        )
        self._context.gate_manager.clear_secret(updated.task_id)

    def _publish_task_event(self, task_id: str, event: str, payload: dict[str, object]) -> None:
        self._context.event_service.publish(
            task_id=task_id,
            category=TaskEventCategory.TASK,
            event=event,
            payload=payload,
        )

    def _publish_artifact_event(self, event: str, artifact: object) -> None:
        self._context.event_service.publish(
            task_id=getattr(artifact, "source_task_id"),
            category=TaskEventCategory.ARTIFACT,
            event=event,
            payload={
                "artifact_id": getattr(artifact, "artifact_id"),
                "artifact_type": getattr(getattr(artifact, "artifact_type"), "value", None),
                "summary": getattr(artifact, "summary"),
            },
        )

    def _upsert_artifact_ref(
        self,
        refs: list[ArtifactRef],
        incoming: ArtifactRef,
    ) -> list[ArtifactRef]:
        remaining = [item for item in refs if item.artifact_id != incoming.artifact_id]
        return [*remaining, incoming]

    def _required_str(self, payload: dict[str, object], key: str) -> str:
        value = payload.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"Missing required string field: {key}")
        return value

    def _optional_str(self, payload: dict[str, object], key: str) -> str | None:
        value = payload.get(key)
        return value if isinstance(value, str) and value else None

    def _optional_int(self, payload: dict[str, object], key: str, *, default: int) -> int:
        value = payload.get(key)
        if value is None:
            return default
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            return int(value)
        raise ValueError(f"Field {key} must be an integer")
