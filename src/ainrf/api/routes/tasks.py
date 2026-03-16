from __future__ import annotations

import asyncio
from collections import Counter
from collections.abc import AsyncIterator
from datetime import UTC, datetime
import json
import logging
import time
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from starlette.responses import StreamingResponse

from ainrf.api.dependencies import get_api_config, get_event_service, get_gate_manager, get_state_store
from ainrf.api.schemas import (
    ActiveGateResponse,
    ArtifactItemResponse,
    ArtifactSummaryResponse,
    GateRecordResponse,
    TaskActionResponse,
    TaskArtifactsResponse,
    TaskCreateRequest,
    TaskCreateResponse,
    TaskDetailResponse,
    TaskListResponse,
    TaskRejectRequest,
    TaskSummaryResponse,
)
from ainrf.artifacts import ArtifactRecord, ArtifactType, GateType, HumanGate, HumanGateStatus
from ainrf.events import TaskEvent, TaskEventCategory, TaskEventService
from ainrf.gates import GateConflictError, GateNotFoundError, GateResolutionError, IntakeGatePayload
from ainrf.state import ArtifactQuery, JsonStateStore, TaskCheckpoint, TaskRecord, TaskStage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["tasks"])

_TERMINAL_STAGES = {TaskStage.COMPLETED, TaskStage.FAILED, TaskStage.CANCELLED}


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _build_task_id() -> str:
    timestamp = _utc_now().strftime("%Y%m%d%H%M%S")
    return f"t-{timestamp}-{uuid4().hex[:8]}"


def _task_summary(task: TaskRecord) -> TaskSummaryResponse:
    return TaskSummaryResponse(
        task_id=task.task_id,
        mode=task.mode,
        status=task.status,
        created_at=task.created_at,
        updated_at=task.updated_at,
        current_stage=task.checkpoint.current_stage,
        termination_reason=task.termination_reason,
    )


def _artifact_summary(artifacts: list[ArtifactRecord]) -> ArtifactSummaryResponse:
    counts = Counter(artifact.artifact_type.value for artifact in artifacts)
    return ArtifactSummaryResponse(counts=dict(counts), total=sum(counts.values()))


def _artifact_item(artifact: ArtifactRecord) -> ArtifactItemResponse:
    raw_payload = artifact.model_dump(mode="json")
    status_value = raw_payload.get("status")
    return ArtifactItemResponse(
        artifact_id=artifact.artifact_id,
        artifact_type=artifact.artifact_type,
        source_task_id=artifact.source_task_id,
        summary=artifact.summary,
        status=status_value if isinstance(status_value, str) else None,
        payload=raw_payload,
    )


def _active_gate_response(active_gate: HumanGate | None) -> ActiveGateResponse | None:
    if active_gate is None:
        return None
    return ActiveGateResponse(
        gate_id=active_gate.artifact_id,
        gate_type=active_gate.gate_type,
        status=active_gate.status,
        summary=active_gate.summary,
        payload=active_gate.payload,
        deadline_at=active_gate.deadline_at,
        resolved_at=active_gate.resolved_at,
        reminder_sent_at=active_gate.reminder_sent_at,
        feedback=active_gate.feedback,
        auto_approved=active_gate.auto_approved,
    )


def _task_artifacts(store: JsonStateStore, task_id: str) -> list[ArtifactRecord]:
    artifacts: list[ArtifactRecord] = []
    for artifact_type in ArtifactType:
        artifacts.extend(store.query_artifacts(artifact_type, ArtifactQuery(source_task_id=task_id)))
    return artifacts


def _load_task_or_404(store: JsonStateStore, task_id: str) -> TaskRecord:
    task = store.load_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


def _artifact_event_payload(artifact: ArtifactRecord) -> dict[str, object]:
    status_value = getattr(artifact, "status", None)
    return {
        "artifact_id": artifact.artifact_id,
        "artifact_type": artifact.artifact_type.value,
        "status": status_value.value if hasattr(status_value, "value") else status_value,
        "summary": artifact.summary,
    }


def _gate_event_payload(gate: HumanGate) -> dict[str, object]:
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


def _publish_task_stage_events(
    *,
    event_service: TaskEventService,
    previous_stage: TaskStage,
    updated_task: TaskRecord,
) -> None:
    event_service.publish(
        task_id=updated_task.task_id,
        category=TaskEventCategory.TASK,
        event="task.stage_changed",
        payload={
            "previous_stage": previous_stage.value,
            "current_stage": updated_task.status.value,
            "termination_reason": updated_task.termination_reason,
        },
    )
    terminal_event: str | None = None
    if updated_task.status is TaskStage.CANCELLED:
        terminal_event = "task.cancelled"
    elif updated_task.status is TaskStage.FAILED:
        terminal_event = "task.failed"
    elif updated_task.status is TaskStage.COMPLETED:
        terminal_event = "task.completed"
    if terminal_event is not None:
        event_service.publish(
            task_id=updated_task.task_id,
            category=TaskEventCategory.TASK,
            event=terminal_event,
            payload={
                "current_stage": updated_task.status.value,
                "termination_reason": updated_task.termination_reason,
            },
        )


def _parse_event_categories(raw_types: str | None) -> set[TaskEventCategory] | None:
    if raw_types is None or not raw_types.strip():
        return None
    categories: set[TaskEventCategory] = set()
    for value in raw_types.split(","):
        normalized = value.strip()
        if not normalized:
            continue
        try:
            categories.add(TaskEventCategory(normalized))
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Unsupported event type filter: {normalized}",
            ) from exc
    return categories or None


def _parse_last_event_id(raw_value: str | None) -> int | None:
    if raw_value is None:
        return None
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last-Event-ID must be an integer",
        ) from exc
    if value < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last-Event-ID must be non-negative",
        )
    return value


def _encode_sse(event: TaskEvent) -> str:
    return (
        f"id: {event.event_id}\n"
        f"event: {event.event}\n"
        f"data: {json.dumps(event.model_dump(mode='json'), ensure_ascii=False)}\n\n"
    )


@router.post("", response_model=TaskCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_task(request: Request, payload: TaskCreateRequest) -> TaskCreateResponse:
    store = get_state_store(request)
    gate_manager = get_gate_manager(request)
    task_id = _build_task_id()
    now = _utc_now()
    task = TaskRecord(
        task_id=task_id,
        mode=payload.mode,
        status=TaskStage.SUBMITTED,
        created_at=now,
        updated_at=now,
        config=payload.model_dump(mode="json"),
        checkpoint=TaskCheckpoint(current_stage=TaskStage.SUBMITTED),
        budget_limit=payload.budget,
        budget_used=payload.budget.model_copy(
            update={"gpu_hours": 0.0, "api_cost_usd": 0.0, "wall_clock_hours": 0.0}
        ),
    )
    store.save_task(task)
    gate_manager.register_secret(task_id, payload.webhook_secret)

    intake_payload = IntakeGatePayload(
        mode=payload.mode.value,
        paper_titles=[paper.title for paper in payload.papers],
        paper_count=len(payload.papers),
        yolo=payload.yolo,
    )
    updated_task, gate = await gate_manager.trigger_gate(
        task=task,
        gate_type=GateType.INTAKE,
        summary=f"Review intake for {len(payload.papers)} paper(s)",
        payload=intake_payload.model_dump(mode="json"),
        yolo=payload.yolo,
    )
    if not payload.yolo:
        try:
            await gate_manager.send_waiting_webhook(task=updated_task, gate=gate)
        except Exception:
            logger.exception("Failed to deliver intake gate webhook", extra={"task_id": task_id})

    return TaskCreateResponse(task_id=task_id, status=updated_task.status)


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    request: Request,
    status_filter: TaskStage | None = Query(default=None, alias="status"),
) -> TaskListResponse:
    store = get_state_store(request)
    items = [_task_summary(task) for task in store.list_tasks(status_filter)]
    return TaskListResponse(items=items)


@router.get("/{task_id}", response_model=TaskDetailResponse)
async def get_task(request: Request, task_id: str) -> TaskDetailResponse:
    store = get_state_store(request)
    gate_manager = get_gate_manager(request)
    task = _load_task_or_404(store, task_id)
    artifacts = _task_artifacts(store, task_id)
    try:
        active_gate = gate_manager.get_active_gate(task_id)
    except GateConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return TaskDetailResponse(
        **_task_summary(task).model_dump(),
        budget_limit=task.budget_limit,
        budget_used=task.budget_used,
        gates=[GateRecordResponse.model_validate(gate.model_dump(mode="json")) for gate in task.gates],
        active_gate=_active_gate_response(active_gate),
        artifact_summary=_artifact_summary(artifacts),
        config=task.config,
    )


@router.post("/{task_id}/cancel", response_model=TaskActionResponse)
async def cancel_task(request: Request, task_id: str) -> TaskActionResponse:
    store = get_state_store(request)
    gate_manager = get_gate_manager(request)
    event_service = get_event_service(request)
    task = _load_task_or_404(store, task_id)
    if task.status in _TERMINAL_STAGES:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task is already terminal",
        )

    now = _utc_now()
    try:
        active_gate = gate_manager.get_active_gate(task_id)
    except GateConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    if active_gate is not None:
        cancelled_gate = active_gate.transition_to(HumanGateStatus.CANCELLED).model_copy(
            update={"resolved_at": now, "updated_at": now}
        )
        store.save_artifact(cancelled_gate)
        event_service.publish(
            task_id=task_id,
            category=TaskEventCategory.ARTIFACT,
            event="artifact.updated",
            payload=_artifact_event_payload(cancelled_gate),
        )
        event_service.publish(
            task_id=task_id,
            category=TaskEventCategory.GATE,
            event="gate.resolved",
            payload=_gate_event_payload(cancelled_gate),
        )
        task_gates = [
            gate.model_copy(
                update={
                    "status": HumanGateStatus.CANCELLED,
                    "resolved_at": now,
                }
            )
            if gate.gate_id == active_gate.artifact_id
            else gate
            for gate in task.gates
        ]
    else:
        task_gates = task.gates

    cancelled = task.model_copy(
        update={
            "status": TaskStage.CANCELLED,
            "updated_at": now,
            "checkpoint": task.checkpoint.model_copy(update={"current_stage": TaskStage.CANCELLED}),
            "gates": task_gates,
        }
    )
    store.save_task(cancelled)
    _publish_task_stage_events(
        event_service=event_service,
        previous_stage=task.status,
        updated_task=cancelled,
    )
    return TaskActionResponse(
        task_id=task_id,
        status=TaskStage.CANCELLED,
        detail="Task cancelled",
    )


@router.get("/{task_id}/artifacts", response_model=TaskArtifactsResponse)
async def get_task_artifacts(request: Request, task_id: str) -> TaskArtifactsResponse:
    store = get_state_store(request)
    _load_task_or_404(store, task_id)
    artifacts = [_artifact_item(artifact) for artifact in _task_artifacts(store, task_id)]
    return TaskArtifactsResponse(task_id=task_id, items=artifacts)


@router.post("/{task_id}/approve", response_model=TaskActionResponse)
async def approve_task(request: Request, task_id: str) -> TaskActionResponse:
    store = get_state_store(request)
    gate_manager = get_gate_manager(request)
    task = _load_task_or_404(store, task_id)
    try:
        updated_task, gate = await gate_manager.resolve_current_gate(
            task=task,
            approved=True,
            feedback=None,
        )
    except GateNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except (GateConflictError, GateResolutionError) as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return TaskActionResponse(
        task_id=task_id,
        status=updated_task.status,
        detail=f"{gate.gate_type.value} gate approved",
    )


@router.post("/{task_id}/reject", response_model=TaskActionResponse)
async def reject_task(request: Request, task_id: str, payload: TaskRejectRequest) -> TaskActionResponse:
    store = get_state_store(request)
    gate_manager = get_gate_manager(request)
    task = _load_task_or_404(store, task_id)
    try:
        updated_task, gate = await gate_manager.resolve_current_gate(
            task=task,
            approved=False,
            feedback=payload.feedback,
        )
    except GateNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except (GateConflictError, GateResolutionError) as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return TaskActionResponse(
        task_id=task_id,
        status=updated_task.status,
        detail=f"{gate.gate_type.value} gate rejected",
    )


@router.get("/{task_id}/events")
async def task_events(
    request: Request,
    task_id: str,
    types: str | None = Query(default=None),
) -> Response:
    store = get_state_store(request)
    api_config = get_api_config(request)
    event_service = get_event_service(request)
    _load_task_or_404(store, task_id)
    categories = _parse_event_categories(types)
    last_event_id = _parse_last_event_id(request.headers.get("Last-Event-ID"))

    async def stream() -> AsyncIterator[str]:
        current_event_id = last_event_id
        last_keepalive = time.monotonic()
        while True:
            if await request.is_disconnected():
                break

            events = event_service.list_events(
                task_id,
                after_id=current_event_id,
                categories=categories,
            )
            if events:
                for event in events:
                    current_event_id = event.event_id
                    yield _encode_sse(event)
                last_keepalive = time.monotonic()
                continue

            task = store.load_task(task_id)
            if task is None or task.status in _TERMINAL_STAGES:
                break

            if time.monotonic() - last_keepalive >= api_config.sse_keepalive_seconds:
                yield ": keepalive\n\n"
                last_keepalive = time.monotonic()

            await asyncio.sleep(api_config.sse_poll_interval_seconds)

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
