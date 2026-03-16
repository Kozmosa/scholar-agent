from __future__ import annotations

import asyncio
import hmac
import logging
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from uuid import uuid4

import httpx

from ainrf.artifacts import ArtifactType, GateType, HumanGate, HumanGateStatus, JsonValue
from ainrf.events import TaskEventCategory, TaskEventService
from ainrf.gates.errors import GateConflictError, GateNotFoundError, GateResolutionError
from ainrf.gates.models import GateWebhookEvent, GateWebhookPayload
from ainrf.runtime import WebhookSecretStore
from ainrf.state import ArtifactQuery, GateRecord, JsonStateStore, TaskRecord, TaskStage

logger = logging.getLogger(__name__)


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class WebhookDispatcher:
    timeout_seconds: float = 10.0
    max_attempts: int = 3

    async def send(
        self,
        *,
        url: str,
        secret: str | None,
        payload: GateWebhookPayload,
    ) -> None:
        body = payload.model_dump_json().encode("utf-8")
        headers = {"content-type": "application/json"}
        if secret is not None:
            digest = hmac.new(secret.encode("utf-8"), body, sha256).hexdigest()
            headers["X-AINRF-Signature"] = f"sha256={digest}"

        last_error: Exception | None = None
        for attempt in range(self.max_attempts):
            try:
                async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                    response = await client.post(url, content=body, headers=headers)
                response.raise_for_status()
                return
            except Exception as exc:  # pragma: no cover - retry branch tested via monkeypatch
                last_error = exc
                if attempt + 1 == self.max_attempts:
                    break
                await asyncio.sleep(float(2**attempt))

        if last_error is not None:
            raise last_error


class HumanGateManager:
    def __init__(
        self,
        *,
        store: JsonStateStore,
        event_service: TaskEventService,
        webhook_dispatcher: WebhookDispatcher,
        secret_registry: WebhookSecretStore,
        gate_timeout_seconds: int,
    ) -> None:
        self._store = store
        self._event_service = event_service
        self._webhook_dispatcher = webhook_dispatcher
        self._secret_registry = secret_registry
        self._gate_timeout_seconds = gate_timeout_seconds

    def get_active_gate(self, task_id: str) -> HumanGate | None:
        gates = self._store.query_artifacts(
            ArtifactType.HUMAN_GATE,
            ArtifactQuery(status=HumanGateStatus.WAITING.value, source_task_id=task_id),
        )
        if not gates:
            return None
        if len(gates) > 1:
            raise GateConflictError(f"Task {task_id} has multiple waiting gates")
        gate = gates[0]
        if not isinstance(gate, HumanGate):
            raise GateConflictError(f"Task {task_id} active gate payload is invalid")
        return gate

    async def trigger_gate(
        self,
        *,
        task: TaskRecord,
        gate_type: GateType,
        summary: str,
        payload: dict[str, JsonValue],
        yolo: bool,
    ) -> tuple[TaskRecord, HumanGate]:
        if self.get_active_gate(task.task_id) is not None:
            raise GateConflictError(f"Task {task.task_id} already has a waiting gate")

        now = utc_now()
        approved = yolo
        gate_status = HumanGateStatus.APPROVED if approved else HumanGateStatus.WAITING
        gate = HumanGate(
            artifact_id=self._build_gate_id(),
            status=gate_status,
            gate_type=gate_type,
            summary=summary,
            payload=payload,
            source_task_id=task.task_id,
            deadline_at=None if approved else now + timedelta(seconds=self._gate_timeout_seconds),
            resolved_at=now if approved else None,
            auto_approved=approved,
        )
        self._store.save_artifact(gate)
        updated_task = task.model_copy(
            update={
                "status": self._post_trigger_task_stage(gate_type, approved),
                "updated_at": now,
                "checkpoint": task.checkpoint.model_copy(
                    update={
                        "current_stage": self._post_trigger_task_stage(gate_type, approved),
                    }
                ),
                "gates": [
                    *task.gates,
                    GateRecord(
                        gate_id=gate.artifact_id,
                        gate_type=gate.gate_type,
                        status=gate.status,
                        at=now,
                        resolved_at=gate.resolved_at,
                    ),
                ],
            }
        )
        self._store.save_task(updated_task)
        self._publish_gate_trigger_events(previous_task=task, updated_task=updated_task, gate=gate)
        return updated_task, gate

    async def resolve_current_gate(
        self,
        *,
        task: TaskRecord,
        approved: bool,
        feedback: str | None,
    ) -> tuple[TaskRecord, HumanGate]:
        gate = self.get_active_gate(task.task_id)
        if gate is None:
            raise GateNotFoundError(f"Task {task.task_id} has no waiting gate")
        if gate.status is not HumanGateStatus.WAITING:
            raise GateResolutionError(f"Gate {gate.artifact_id} is not waiting")

        now = utc_now()
        next_status = HumanGateStatus.APPROVED if approved else HumanGateStatus.REJECTED
        resolved_gate = gate.transition_to(next_status).model_copy(
            update={
                "feedback": feedback,
                "resolved_at": now,
                "updated_at": now,
            }
        )
        self._store.save_artifact(resolved_gate)

        updated_gates = []
        for gate_record in task.gates:
            if gate_record.gate_id == gate.artifact_id:
                updated_gates.append(
                    gate_record.model_copy(
                        update={
                            "status": next_status,
                            "feedback": feedback,
                            "resolved_at": now,
                        }
                    )
                )
            else:
                updated_gates.append(gate_record)

        next_task = task.model_copy(
            update={
                "status": self._post_resolution_task_stage(
                    task=task.model_copy(update={"gates": updated_gates}),
                    gate=resolved_gate,
                    approved=approved,
                ),
                "updated_at": now,
                "checkpoint": task.checkpoint.model_copy(
                    update={
                        "current_stage": self._post_resolution_task_stage(
                            task=task.model_copy(update={"gates": updated_gates}),
                            gate=resolved_gate,
                            approved=approved,
                        )
                    }
                ),
                "gates": updated_gates,
                "termination_reason": self._termination_reason(
                    task=task.model_copy(update={"gates": updated_gates}),
                    gate=resolved_gate,
                    approved=approved,
                ),
            }
        )
        self._store.save_task(next_task)
        self._publish_gate_resolution_events(previous_task=task, updated_task=next_task, gate=resolved_gate)
        return next_task, resolved_gate

    async def sweep_overdue_gates(self) -> None:
        now = utc_now()
        tasks = self._store.list_tasks(TaskStage.GATE_WAITING)
        for task in tasks:
            gate = self.get_active_gate(task.task_id)
            if gate is None or gate.deadline_at is None or gate.reminder_sent_at is not None:
                continue
            if gate.deadline_at > now:
                continue

            reminded_gate = gate.model_copy(update={"reminder_sent_at": now, "updated_at": now})
            self._store.save_artifact(reminded_gate)
            self._event_service.publish(
                task_id=task.task_id,
                category=TaskEventCategory.ARTIFACT,
                event="artifact.updated",
                payload=self._artifact_payload(reminded_gate),
            )
            self._event_service.publish(
                task_id=task.task_id,
                category=TaskEventCategory.GATE,
                event="gate.reminder",
                payload=self._gate_payload(reminded_gate),
            )

            webhook_url = task.config.get("webhook_url")
            if not isinstance(webhook_url, str) or not webhook_url:
                continue

            secret = self._secret_registry.get(task.task_id)
            if secret is None:
                logger.warning("Skipping webhook reminder without registered secret", extra={"task_id": task.task_id})
                continue

            payload = self._webhook_payload(
                event=GateWebhookEvent.REMINDER,
                task_id=task.task_id,
                gate=reminded_gate,
            )
            try:
                await self._webhook_dispatcher.send(url=webhook_url, secret=secret, payload=payload)
            except Exception:
                logger.exception("Failed to deliver gate reminder webhook", extra={"task_id": task.task_id})

    async def send_waiting_webhook(self, *, task: TaskRecord, gate: HumanGate) -> None:
        webhook_url = task.config.get("webhook_url")
        if not isinstance(webhook_url, str) or not webhook_url:
            return
        secret = self._secret_registry.get(task.task_id)
        payload = self._webhook_payload(event=GateWebhookEvent.WAITING, task_id=task.task_id, gate=gate)
        await self._webhook_dispatcher.send(url=webhook_url, secret=secret, payload=payload)

    def register_secret(self, task_id: str, secret: str | None) -> None:
        self._secret_registry.set(task_id, secret)

    def clear_secret(self, task_id: str) -> None:
        self._secret_registry.drop(task_id)

    def _webhook_payload(
        self,
        *,
        event: GateWebhookEvent,
        task_id: str,
        gate: HumanGate,
    ) -> GateWebhookPayload:
        return GateWebhookPayload(
            event=event,
            task_id=task_id,
            gate_id=gate.artifact_id,
            gate_type=gate.gate_type,
            summary=gate.summary,
            payload=gate.payload,
            approve_endpoint=f"/tasks/{task_id}/approve",
            reject_endpoint=f"/tasks/{task_id}/reject",
            deadline_at=gate.deadline_at,
        )

    def _build_gate_id(self) -> str:
        timestamp = utc_now().strftime("%Y%m%d%H%M%S")
        return f"g-{timestamp}-{uuid4().hex[:8]}"

    def _artifact_payload(self, gate: HumanGate) -> dict[str, JsonValue]:
        return {
            "artifact_id": gate.artifact_id,
            "artifact_type": gate.artifact_type.value,
            "status": gate.status.value,
            "summary": gate.summary,
        }

    def _gate_payload(self, gate: HumanGate) -> dict[str, JsonValue]:
        return {
            "gate_id": gate.artifact_id,
            "gate_type": gate.gate_type.value,
            "status": gate.status.value,
            "summary": gate.summary,
            "payload": gate.payload,
            "deadline_at": gate.deadline_at.isoformat() if gate.deadline_at is not None else None,
            "resolved_at": gate.resolved_at.isoformat() if gate.resolved_at is not None else None,
            "reminder_sent_at": gate.reminder_sent_at.isoformat()
            if gate.reminder_sent_at is not None
            else None,
            "feedback": gate.feedback,
            "auto_approved": gate.auto_approved,
        }

    def _publish_gate_trigger_events(
        self,
        *,
        previous_task: TaskRecord,
        updated_task: TaskRecord,
        gate: HumanGate,
    ) -> None:
        self._event_service.publish(
            task_id=updated_task.task_id,
            category=TaskEventCategory.ARTIFACT,
            event="artifact.created",
            payload=self._artifact_payload(gate),
        )
        self._event_service.publish(
            task_id=updated_task.task_id,
            category=TaskEventCategory.GATE,
            event="gate.resolved" if gate.status is HumanGateStatus.APPROVED else "gate.waiting",
            payload=self._gate_payload(gate),
        )
        self._publish_task_stage_events(previous_task=previous_task, updated_task=updated_task)

    def _publish_gate_resolution_events(
        self,
        *,
        previous_task: TaskRecord,
        updated_task: TaskRecord,
        gate: HumanGate,
    ) -> None:
        self._event_service.publish(
            task_id=updated_task.task_id,
            category=TaskEventCategory.ARTIFACT,
            event="artifact.updated",
            payload=self._artifact_payload(gate),
        )
        self._event_service.publish(
            task_id=updated_task.task_id,
            category=TaskEventCategory.GATE,
            event="gate.resolved",
            payload=self._gate_payload(gate),
        )
        self._publish_task_stage_events(previous_task=previous_task, updated_task=updated_task)

    def _publish_task_stage_events(
        self,
        *,
        previous_task: TaskRecord,
        updated_task: TaskRecord,
    ) -> None:
        self._event_service.publish(
            task_id=updated_task.task_id,
            category=TaskEventCategory.TASK,
            event="task.stage_changed",
            payload={
                "previous_stage": previous_task.status.value,
                "current_stage": updated_task.status.value,
                "termination_reason": updated_task.termination_reason,
            },
        )
        terminal_event = self._terminal_event_name(updated_task.status)
        if terminal_event is None:
            return
        self._event_service.publish(
            task_id=updated_task.task_id,
            category=TaskEventCategory.TASK,
            event=terminal_event,
            payload={
                "current_stage": updated_task.status.value,
                "termination_reason": updated_task.termination_reason,
            },
        )

    def _terminal_event_name(self, stage: TaskStage) -> str | None:
        if stage is TaskStage.CANCELLED:
            return "task.cancelled"
        if stage is TaskStage.FAILED:
            return "task.failed"
        if stage is TaskStage.COMPLETED:
            return "task.completed"
        return None

    def _post_trigger_task_stage(self, gate_type: GateType, approved: bool) -> TaskStage:
        if not approved:
            return TaskStage.GATE_WAITING
        if gate_type is GateType.INTAKE:
            return TaskStage.PLANNING
        if gate_type is GateType.PLAN_APPROVAL:
            return TaskStage.EXECUTING
        raise GateConflictError(f"Unsupported gate type {gate_type.value}")

    def _post_resolution_task_stage(
        self,
        *,
        task: TaskRecord,
        gate: HumanGate,
        approved: bool,
    ) -> TaskStage:
        if approved:
            return self._post_trigger_task_stage(gate.gate_type, True)
        if gate.gate_type is GateType.INTAKE:
            return TaskStage.CANCELLED
        if gate.gate_type is GateType.PLAN_APPROVAL:
            if self._consecutive_plan_rejections(task) >= 3:
                return TaskStage.FAILED
            return TaskStage.PLANNING
        raise GateConflictError(f"Unsupported gate type {gate.gate_type.value}")

    def _termination_reason(
        self,
        *,
        task: TaskRecord,
        gate: HumanGate,
        approved: bool,
    ) -> str | None:
        if approved:
            return None
        if gate.gate_type is GateType.INTAKE:
            return "intake_rejected"
        if gate.gate_type is GateType.PLAN_APPROVAL and self._consecutive_plan_rejections(task) >= 3:
            return "plan_rejected_limit"
        return None

    def _consecutive_plan_rejections(self, task: TaskRecord) -> int:
        count = 0
        for gate in reversed(task.gates):
            if gate.gate_type is not GateType.PLAN_APPROVAL:
                if count == 0:
                    continue
                break
            if gate.status is HumanGateStatus.REJECTED:
                count += 1
                continue
            break
        return count
