from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import cast
from urllib.request import urlretrieve
from uuid import uuid4

from ainrf.agents import AgentAdapter, AgentExecutionError
from ainrf.artifacts import (
    AssessmentDimension,
    ArtifactRef,
    ArtifactType,
    Claim,
    EvidenceRecord,
    EvidenceType,
    ExperimentRun,
    ExperimentRunStatus,
    ExplorationGraph,
    GateType,
    PaperCard,
    PaperCardStatus,
    QualityAssessment,
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

from ainrf.engine.models import AtomicTaskSpec, TaskExecutionResult, TaskPlanResult


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
    _DEFAULT_MAX_STEP_RETRIES = 3
    _DEFAULT_DEVIATION_THRESHOLD_PERCENT = 5.0

    def __init__(self, context: EngineContext) -> None:
        self._context = context

    async def run_once(self) -> bool:
        task = self._next_task()
        if task is None:
            return False
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
        if self._is_experiment_step(step):
            self._publish_task_event(
                task.task_id,
                "experiment.started",
                {"step": step.kind, "step_id": step.step_id, "title": step.title},
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
            if exc.retryable:
                retry_count_raw = raw_step.details.get("retry_count", 0)
                retry_count = int(retry_count_raw) if isinstance(retry_count_raw, int | float) else 0
                max_retries_raw = raw_step.details.get("max_retries", self._DEFAULT_MAX_STEP_RETRIES)
                max_retries = (
                    int(max_retries_raw)
                    if isinstance(max_retries_raw, int | float)
                    else self._DEFAULT_MAX_STEP_RETRIES
                )
                next_retry_count = retry_count + 1
                if next_retry_count > max_retries:
                    self._fail_task(
                        task,
                        reason="agent_execution_retry_exhausted",
                        detail=f"{step.kind}: {exc}",
                    )
                    return
                retried_step = raw_step.model_copy(
                    update={
                        "details": {
                            **raw_step.details,
                            "retry_count": next_retry_count,
                            "max_retries": max_retries,
                            "last_error": str(exc),
                        }
                    }
                )
                pending_queue = [*task.checkpoint.pending_queue[1:], retried_step]
                updated = task.model_copy(
                    update={
                        "updated_at": utc_now(),
                        "checkpoint": task.checkpoint.model_copy(update={"pending_queue": pending_queue}),
                    }
                )
                self._context.state_store.save_task(updated)
                self._publish_task_event(
                    updated.task_id,
                    "task.progress",
                    {
                        "stage": updated.status.value,
                        "step": step.kind,
                        "detail": f"Retryable agent error: {exc}",
                        "remaining_steps": len(updated.checkpoint.pending_queue),
                        "retry_count": next_retry_count,
                    },
                )
                return
            self._fail_task(task, reason="agent_execution_failed", detail=str(exc))
            return
        experiment_ref = self._record_experiment_run(task, step, result)
        deviation_ref = self._record_deviation_evidence(task, step, result)
        analysis_ref = self._record_analysis_evidence(task, step, result)
        exploration_ref = self._upsert_exploration_graph(task, step, result)
        claim_refs = self._record_mode1_claims(task, step, result)
        pending_queue, mode_termination_reason = self._apply_mode1_termination(
            task,
            task.checkpoint.pending_queue[1:],
            step,
            result,
        )
        updated = task.model_copy(
            update={
                "updated_at": utc_now(),
                "termination_reason": mode_termination_reason,
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
                        "pending_queue": pending_queue,
                        "artifact_refs": self._upsert_artifact_ref_if_needed(
                            task.checkpoint.artifact_refs,
                            experiment_ref,
                        ),
                    }
                ),
                "budget_used": self._merge_budget(task.budget_used, result.resource_usage),
            }
        )
        updated = updated.model_copy(
            update={
                "checkpoint": updated.checkpoint.model_copy(
                    update={
                        "artifact_refs": self._upsert_artifact_ref_if_needed(
                            updated.checkpoint.artifact_refs,
                            deviation_ref,
                        )
                    }
                )
            }
        )
        updated = updated.model_copy(
            update={
                "checkpoint": updated.checkpoint.model_copy(
                    update={
                        "artifact_refs": self._upsert_artifact_ref_if_needed(
                            updated.checkpoint.artifact_refs,
                            analysis_ref,
                        )
                    }
                )
            }
        )
        updated = updated.model_copy(
            update={
                "checkpoint": updated.checkpoint.model_copy(
                    update={
                        "artifact_refs": self._upsert_artifact_ref_if_needed(
                            updated.checkpoint.artifact_refs,
                            exploration_ref,
                        )
                    }
                )
            }
        )
        for claim_ref in claim_refs:
            updated = updated.model_copy(
                update={
                    "checkpoint": updated.checkpoint.model_copy(
                        update={
                            "artifact_refs": self._upsert_artifact_ref(
                                updated.checkpoint.artifact_refs,
                                claim_ref,
                            )
                        }
                    )
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
            self._complete_task(updated, termination_reason=updated.termination_reason)

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
        if task.mode.value == "literature_exploration":
            prompt = "Generate a research discovery plan."
        latest_feedback = self._latest_plan_feedback(task)
        context = {
            "task_id": task.task_id,
            "task_mode": task.mode.value,
            "paper_card": paper_card.model_dump(mode="json"),
            "task_config": task.config,
            "latest_feedback": latest_feedback,
        }
        plan = await self._context.agent_adapter.plan_reproduction(
            container=container,
            prompt=prompt,
            context=context,
        )
        if task.mode.value == "literature_exploration":
            await self._plan_discovery_task(task=task, paper_card=paper_card, plan=plan)
            return
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

    async def _plan_discovery_task(
        self,
        *,
        task: TaskRecord,
        paper_card: PaperCard,
        plan: TaskPlanResult,
    ) -> None:
        existing_graph = self._existing_exploration_graph(task.task_id)
        if existing_graph is None:
            exploration_graph = ExplorationGraph(
                artifact_id=f"eg-{uuid4().hex[:8]}",
                source_task_id=task.task_id,
                summary="Mode 1 exploration graph initialized.",
                seed_paper_ids=[paper_card.artifact_id],
                visited_paper_ids=[paper_card.artifact_id],
                budget_snapshot=task.budget_used,
            )
            graph_event = "artifact.created"
        else:
            exploration_graph = existing_graph.model_copy(
                update={
                    "updated_at": utc_now(),
                    "summary": "Mode 1 exploration graph refreshed with latest plan.",
                    "seed_paper_ids": self._merge_unique_ids(
                        existing_graph.seed_paper_ids,
                        [paper_card.artifact_id],
                    ),
                    "visited_paper_ids": self._merge_unique_ids(
                        existing_graph.visited_paper_ids,
                        [paper_card.artifact_id],
                    ),
                    "budget_snapshot": task.budget_used,
                }
            )
            graph_event = "artifact.updated"
        self._context.state_store.save_artifact(exploration_graph)
        self._publish_artifact_event(graph_event, exploration_graph)
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
                                artifact_type=ArtifactType.EXPLORATION_GRAPH,
                                artifact_id=exploration_graph.artifact_id,
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
        quality_ref = self._upsert_quality_assessment(updated)
        if quality_ref is not None:
            updated = updated.model_copy(
                update={
                    "checkpoint": updated.checkpoint.model_copy(
                        update={
                            "artifact_refs": self._upsert_artifact_ref(
                                updated.checkpoint.artifact_refs,
                                quality_ref,
                            )
                        }
                    )
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

    def _upsert_artifact_ref_if_needed(
        self,
        refs: list[ArtifactRef],
        incoming: ArtifactRef | None,
    ) -> list[ArtifactRef]:
        if incoming is None:
            return refs
        return self._upsert_artifact_ref(refs, incoming)

    def _is_experiment_step(self, step: AtomicTaskSpec) -> bool:
        return step.kind in {"run_baseline", "run_full_experiment"}

    def _run_type_from_step(self, step: AtomicTaskSpec) -> str:
        if step.kind == "run_baseline":
            return "baseline"
        if step.kind == "run_full_experiment":
            return "full_reproduction"
        return "task_step"

    def _record_experiment_run(
        self,
        task: TaskRecord,
        step: AtomicTaskSpec,
        result: TaskExecutionResult,
    ) -> ArtifactRef | None:
        if not self._is_experiment_step(step):
            return None
        reproduction_task = self._existing_reproduction_task(task.task_id)
        reproduction_task_id = (
            reproduction_task.artifact_id if reproduction_task is not None else "rt-unknown"
        )
        raw_metrics = result.step_updates.get("metrics")
        metrics: dict[str, float] = {}
        if isinstance(raw_metrics, dict):
            for key, value in raw_metrics.items():
                if isinstance(key, str) and isinstance(value, int | float):
                    metrics[key] = float(value)
        status = (
            ExperimentRunStatus.COMPLETED
            if result.status in {"completed", "succeeded", "success"}
            else ExperimentRunStatus.FAILED
        )
        run = ExperimentRun(
            artifact_id=f"run-{uuid4().hex[:8]}",
            source_task_id=task.task_id,
            status=status,
            reproduction_task_id=reproduction_task_id,
            run_type=self._run_type_from_step(step),
            metrics=metrics,
            resource_usage=ResourceUsage(**result.resource_usage),
            summary=result.summary,
            failure_reason=result.error,
            related_artifacts=[
                ArtifactRef(
                    artifact_type=ArtifactType.REPRODUCTION_TASK,
                    artifact_id=reproduction_task_id,
                )
            ]
            if reproduction_task is not None
            else [],
        )
        self._context.state_store.save_artifact(run)
        self._publish_artifact_event("artifact.created", run)
        self._publish_task_event(
            task.task_id,
            "experiment.completed",
            {
                "step": step.kind,
                "step_id": step.step_id,
                "run_id": run.artifact_id,
                "run_type": run.run_type,
                "status": run.status.value,
            },
        )
        return ArtifactRef(
            artifact_type=ArtifactType.EXPERIMENT_RUN,
            artifact_id=run.artifact_id,
        )

    def _record_deviation_evidence(
        self,
        task: TaskRecord,
        step: AtomicTaskSpec,
        result: TaskExecutionResult,
    ) -> ArtifactRef | None:
        if not self._is_experiment_step(step):
            return None
        expected_metrics = self._extract_expected_metrics(step.payload)
        actual_metrics = self._extract_actual_metrics(result.step_updates)
        if not expected_metrics or not actual_metrics:
            return None
        threshold_percent = self._extract_threshold_percent(step.payload)
        deviations: list[dict[str, float | str]] = []
        exceeded_count = 0
        for metric, expected_value in expected_metrics.items():
            actual_value = actual_metrics.get(metric)
            if actual_value is None:
                continue
            deviation_percent = abs(actual_value - expected_value) / abs(expected_value) * 100.0
            deviations.append(
                {
                    "metric": metric,
                    "expected": expected_value,
                    "actual": actual_value,
                    "deviation_percent": round(deviation_percent, 4),
                }
            )
            if deviation_percent > threshold_percent:
                exceeded_count += 1
        if not deviations:
            return None
        if exceeded_count == 0:
            return None
        evidence = EvidenceRecord(
            artifact_id=f"ev-{uuid4().hex[:8]}",
            source_task_id=task.task_id,
            evidence_type=EvidenceType.DEVIATION_ANALYSIS,
            statement=(
                f"Detected {exceeded_count} metric deviations above {threshold_percent:.2f}% "
                f"during {step.kind}."
            ),
            content=json.dumps(
                {
                    "step": step.kind,
                    "step_id": step.step_id,
                    "threshold_percent": threshold_percent,
                    "deviations": deviations,
                },
                ensure_ascii=False,
            ),
            summary=f"Deviation detected in {step.kind}",
        )
        self._context.state_store.save_artifact(evidence)
        self._publish_task_event(
            task.task_id,
            "deviation.detected",
            {
                "step": step.kind,
                "step_id": step.step_id,
                "threshold_percent": threshold_percent,
                "count": exceeded_count,
            },
        )
        self._publish_artifact_event("artifact.created", evidence)
        self._publish_task_event(
            task.task_id,
            "diagnosis.completed",
            {
                "evidence_id": evidence.artifact_id,
                "evidence_type": evidence.evidence_type.value,
            },
        )
        return ArtifactRef(
            artifact_type=ArtifactType.EVIDENCE_RECORD,
            artifact_id=evidence.artifact_id,
        )

    def _record_analysis_evidence(
        self,
        task: TaskRecord,
        step: AtomicTaskSpec,
        result: TaskExecutionResult,
    ) -> ArtifactRef | None:
        if step.kind not in {"diagnose_deviation", "compare_tables"}:
            return None
        if step.kind == "diagnose_deviation":
            payload_obj = result.step_updates.get("diagnosis")
            if not isinstance(payload_obj, dict):
                return None
            payload = cast(dict[str, object], payload_obj)
            summary_obj = payload.get("summary")
            summary = summary_obj if isinstance(summary_obj, str) and summary_obj else "Deviation diagnosis generated."
        else:
            payload_obj = result.step_updates.get("table_comparisons")
            if not isinstance(payload_obj, list):
                return None
            payload = payload_obj
            summary = "Table comparisons generated."
        evidence = EvidenceRecord(
            artifact_id=f"ev-{uuid4().hex[:8]}",
            source_task_id=task.task_id,
            evidence_type=EvidenceType.DEVIATION_ANALYSIS,
            statement=summary,
            content=json.dumps(payload, ensure_ascii=False),
            summary=f"{step.kind} output",
        )
        self._context.state_store.save_artifact(evidence)
        self._publish_artifact_event("artifact.created", evidence)
        self._publish_task_event(
            task.task_id,
            "diagnosis.completed",
            {
                "step": step.kind,
                "step_id": step.step_id,
                "evidence_id": evidence.artifact_id,
            },
        )
        return ArtifactRef(
            artifact_type=ArtifactType.EVIDENCE_RECORD,
            artifact_id=evidence.artifact_id,
        )

    def _extract_expected_metrics(self, payload: dict[str, object]) -> dict[str, float]:
        raw_expected = payload.get("expected_metrics")
        if not isinstance(raw_expected, dict):
            return {}
        expected: dict[str, float] = {}
        for key, value in raw_expected.items():
            if isinstance(key, str) and isinstance(value, int | float) and value != 0:
                expected[key] = float(value)
        return expected

    def _extract_actual_metrics(self, step_updates: dict[str, object]) -> dict[str, float]:
        raw_metrics = step_updates.get("metrics")
        if not isinstance(raw_metrics, dict):
            return {}
        actual: dict[str, float] = {}
        for key, value in raw_metrics.items():
            if isinstance(key, str) and isinstance(value, int | float):
                actual[key] = float(value)
        return actual

    def _extract_threshold_percent(self, payload: dict[str, object]) -> float:
        raw_threshold = payload.get("deviation_threshold_percent")
        if isinstance(raw_threshold, int | float) and raw_threshold > 0:
            return float(raw_threshold)
        return self._DEFAULT_DEVIATION_THRESHOLD_PERCENT

    def _existing_quality_assessment(self, task_id: str) -> QualityAssessment | None:
        for artifact in self._context.state_store.query_artifacts(
            ArtifactType.QUALITY_ASSESSMENT,
            ArtifactQuery(source_task_id=task_id),
        ):
            if isinstance(artifact, QualityAssessment) and artifact.source_task_id == task_id:
                return artifact
        return None

    def _upsert_quality_assessment(self, task: TaskRecord) -> ArtifactRef | None:
        if task.mode.value != "deep_reproduction":
            return None
        experiment_runs = [
            artifact
            for artifact in self._context.state_store.query_artifacts(
                ArtifactType.EXPERIMENT_RUN,
                ArtifactQuery(source_task_id=task.task_id),
            )
            if isinstance(artifact, ExperimentRun)
        ]
        total_runs = len(experiment_runs)
        successful_runs = len(
            [run for run in experiment_runs if run.status is ExperimentRunStatus.COMPLETED]
        )
        deviation_records = [
            artifact
            for artifact in self._context.state_store.query_artifacts(
                ArtifactType.EVIDENCE_RECORD,
                ArtifactQuery(source_task_id=task.task_id),
            )
            if isinstance(artifact, EvidenceRecord)
            and artifact.evidence_type is EvidenceType.DEVIATION_ANALYSIS
        ]
        completed_steps = len(task.checkpoint.completed_steps)
        reproducibility_score = 5.0 if total_runs == 0 else 5.0 * (successful_runs / total_runs)
        existing = self._existing_quality_assessment(task.task_id)
        run_ids = [run.artifact_id for run in experiment_runs]
        deviation_ids = [record.artifact_id for record in deviation_records]
        quality_assessment = QualityAssessment(
            artifact_id=existing.artifact_id if existing is not None else f"qa-{uuid4().hex[:8]}",
            source_task_id=task.task_id,
            summary="Automated quality assessment generated after task completion.",
            gold_nugget=AssessmentDimension(
                score=min(5.0, 1.0 + (completed_steps * 0.5)),
                summary="Scored from completed atomic steps.",
                evidence_ids=[step.step for step in task.checkpoint.completed_steps],
            ),
            reproducibility=AssessmentDimension(
                score=round(reproducibility_score, 2),
                summary="Scored from completed vs failed experiment runs and deviation evidence.",
                evidence_ids=[*run_ids, *deviation_ids],
            ),
            scientific_rigor=AssessmentDimension(
                score=max(1.0, min(5.0, 2.0 + (total_runs * 0.5) - (len(deviation_ids) * 0.3))),
                summary="Scored from experiment coverage and deviation diagnostics.",
                evidence_ids=[*run_ids, *deviation_ids],
            ),
            overall_summary=(
                "Completed "
                f"{completed_steps} steps with {successful_runs}/{total_runs} successful runs "
                f"and {len(deviation_ids)} deviation diagnostics."
            ),
            related_artifacts=[
                ArtifactRef(
                    artifact_type=ArtifactType.EXPERIMENT_RUN,
                    artifact_id=run.artifact_id,
                )
                for run in experiment_runs
            ]
            + [
                ArtifactRef(
                    artifact_type=ArtifactType.EVIDENCE_RECORD,
                    artifact_id=record.artifact_id,
                )
                for record in deviation_records
            ],
        )
        self._context.state_store.save_artifact(quality_assessment)
        self._publish_artifact_event(
            "artifact.updated" if existing is not None else "artifact.created",
            quality_assessment,
        )
        return ArtifactRef(
            artifact_type=ArtifactType.QUALITY_ASSESSMENT,
            artifact_id=quality_assessment.artifact_id,
        )

    def _existing_exploration_graph(self, task_id: str) -> ExplorationGraph | None:
        for artifact in self._context.state_store.query_artifacts(
            ArtifactType.EXPLORATION_GRAPH,
            ArtifactQuery(source_task_id=task_id),
        ):
            if isinstance(artifact, ExplorationGraph) and artifact.source_task_id == task_id:
                return artifact
        return None

    def _upsert_exploration_graph(
        self,
        task: TaskRecord,
        step: AtomicTaskSpec,
        result: TaskExecutionResult,
    ) -> ArtifactRef | None:
        if task.mode.value != "literature_exploration":
            return None
        graph = self._existing_exploration_graph(task.task_id)
        if graph is None:
            return None
        exploration_payload = result.step_updates.get("exploration")
        termination_payload = result.step_updates.get("termination")
        updated_graph = graph
        if isinstance(exploration_payload, dict):
            payload = cast(dict[str, object], exploration_payload)
            updated_graph = updated_graph.model_copy(
                update={
                    "updated_at": utc_now(),
                    "visited_paper_ids": self._merge_unique_ids(
                        updated_graph.visited_paper_ids,
                        self._string_list(payload.get("visited_paper_ids")),
                    ),
                    "queued_paper_ids": self._merge_unique_ids(
                        updated_graph.queued_paper_ids,
                        self._string_list(payload.get("queued_paper_ids")),
                    ),
                    "pruned_paper_ids": self._merge_unique_ids(
                        updated_graph.pruned_paper_ids,
                        self._string_list(payload.get("pruned_paper_ids")),
                    ),
                    "current_depth": self._extract_depth(payload.get("current_depth"), updated_graph.current_depth),
                    "budget_snapshot": task.budget_used,
                }
            )
        if isinstance(termination_payload, dict):
            payload = cast(dict[str, object], termination_payload)
            reason = payload.get("reason")
            if isinstance(reason, str) and reason:
                updated_graph = updated_graph.model_copy(update={"termination_reason": reason, "updated_at": utc_now()})
        if step.kind == "generate_discovery_report" and updated_graph.termination_reason is None:
            updated_graph = updated_graph.model_copy(update={"termination_reason": "report_generated", "updated_at": utc_now()})
        if updated_graph == graph:
            return ArtifactRef(
                artifact_type=ArtifactType.EXPLORATION_GRAPH,
                artifact_id=graph.artifact_id,
            )
        self._context.state_store.save_artifact(updated_graph)
        self._publish_artifact_event("artifact.updated", updated_graph)
        return ArtifactRef(
            artifact_type=ArtifactType.EXPLORATION_GRAPH,
            artifact_id=updated_graph.artifact_id,
        )

    def _record_mode1_claims(
        self,
        task: TaskRecord,
        step: AtomicTaskSpec,
        result: TaskExecutionResult,
    ) -> list[ArtifactRef]:
        if task.mode.value != "literature_exploration":
            return []
        claim_candidates: list[dict[str, object]] = []
        exploration_payload = result.step_updates.get("exploration")
        if isinstance(exploration_payload, dict):
            new_claims = cast(dict[str, object], exploration_payload).get("new_claims")
            if isinstance(new_claims, list):
                claim_candidates.extend(
                    [cast(dict[str, object], item) for item in new_claims if isinstance(item, dict)]
                )
        graph_payload = result.step_updates.get("knowledge_graph_update")
        if isinstance(graph_payload, dict):
            raw_claims = cast(dict[str, object], graph_payload).get("claims")
            if isinstance(raw_claims, list):
                claim_candidates.extend(
                    [cast(dict[str, object], item) for item in raw_claims if isinstance(item, dict)]
                )
        refs: list[ArtifactRef] = []
        for candidate in claim_candidates:
            statement = candidate.get("statement")
            if not isinstance(statement, str) or not statement:
                continue
            confidence_value = candidate.get("confidence")
            confidence = float(confidence_value) if isinstance(confidence_value, int | float) else None
            claim = Claim(
                artifact_id=f"cl-{uuid4().hex[:8]}",
                source_task_id=task.task_id,
                statement=statement,
                confidence=confidence,
                summary=f"Claim from {step.kind}",
            )
            self._context.state_store.save_artifact(claim)
            self._publish_artifact_event("artifact.created", claim)
            refs.append(
                ArtifactRef(
                    artifact_type=ArtifactType.CLAIM,
                    artifact_id=claim.artifact_id,
                )
            )
        return refs

    def _apply_mode1_termination(
        self,
        task: TaskRecord,
        pending_queue: list[AtomicTaskRecord],
        step: AtomicTaskSpec,
        result: TaskExecutionResult,
    ) -> tuple[list[AtomicTaskRecord], str | None]:
        if task.mode.value != "literature_exploration" or step.kind != "check_termination":
            return pending_queue, task.termination_reason
        termination_payload = result.step_updates.get("termination")
        if not isinstance(termination_payload, dict):
            return pending_queue, task.termination_reason
        payload = cast(dict[str, object], termination_payload)
        should_terminate = bool(payload.get("should_terminate", False))
        reason = payload.get("reason")
        termination_reason = reason if isinstance(reason, str) and reason else task.termination_reason
        if not should_terminate:
            return pending_queue, termination_reason
        report_step = next(
            (item for item in pending_queue if item.step == "generate_discovery_report"),
            None,
        )
        if report_step is None:
            return [], termination_reason
        return [report_step], termination_reason

    def _merge_unique_ids(self, base: list[str], extra: list[str]) -> list[str]:
        seen = set(base)
        merged = [*base]
        for item in extra:
            if item in seen:
                continue
            merged.append(item)
            seen.add(item)
        return merged

    def _string_list(self, value: object) -> list[str]:
        if not isinstance(value, list):
            return []
        return [item for item in value if isinstance(item, str)]

    def _extract_depth(self, value: object, default: int) -> int:
        if isinstance(value, int) and value >= 0:
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return default

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
