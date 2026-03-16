from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Query, Request, Response, status

from ainrf.api.dependencies import get_state_store
from ainrf.api.schemas import (
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
from ainrf.artifacts import ArtifactRecord, ArtifactType
from ainrf.state import ArtifactQuery, JsonStateStore, TaskCheckpoint, TaskRecord, TaskStage

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


def _task_artifacts(store: JsonStateStore, task_id: str) -> list[ArtifactRecord]:
    artifacts: list[ArtifactRecord] = []
    for artifact_type in ArtifactType:
        artifacts.extend(store.query_artifacts(artifact_type, ArtifactQuery(source_task_id=task_id)))
    return artifacts


@router.post("", response_model=TaskCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_task(request: Request, payload: TaskCreateRequest) -> TaskCreateResponse:
    store = get_state_store(request)
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
    return TaskCreateResponse(task_id=task_id, status=task.status)


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
    task = store.load_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    artifacts = _task_artifacts(store, task_id)
    return TaskDetailResponse(
        **_task_summary(task).model_dump(),
        budget_limit=task.budget_limit,
        budget_used=task.budget_used,
        gates=[GateRecordResponse.model_validate(gate.model_dump(mode="json")) for gate in task.gates],
        artifact_summary=_artifact_summary(artifacts),
        config=task.config,
    )


@router.post("/{task_id}/cancel", response_model=TaskActionResponse)
async def cancel_task(request: Request, task_id: str) -> TaskActionResponse:
    store = get_state_store(request)
    task = store.load_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.status in _TERMINAL_STAGES:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task is already terminal",
        )

    cancelled = task.model_copy(
        update={
            "status": TaskStage.CANCELLED,
            "updated_at": _utc_now(),
            "checkpoint": task.checkpoint.model_copy(update={"current_stage": TaskStage.CANCELLED}),
        }
    )
    store.save_task(cancelled)
    return TaskActionResponse(
        task_id=task_id,
        status=TaskStage.CANCELLED,
        detail="Task cancelled",
    )


@router.get("/{task_id}/artifacts", response_model=TaskArtifactsResponse)
async def get_task_artifacts(request: Request, task_id: str) -> TaskArtifactsResponse:
    store = get_state_store(request)
    task = store.load_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    artifacts = [_artifact_item(artifact) for artifact in _task_artifacts(store, task_id)]
    return TaskArtifactsResponse(task_id=task_id, items=artifacts)


@router.post("/{task_id}/approve", response_model=TaskActionResponse)
async def approve_task(request: Request, task_id: str) -> TaskActionResponse:
    store = get_state_store(request)
    if store.load_task(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Task approval is planned for P5")


@router.post("/{task_id}/reject", response_model=TaskActionResponse)
async def reject_task(request: Request, task_id: str, payload: TaskRejectRequest) -> TaskActionResponse:
    store = get_state_store(request)
    if store.load_task(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    _ = payload
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Task rejection is planned for P5")


@router.get("/{task_id}/events")
async def task_events(request: Request, task_id: str) -> Response:
    store = get_state_store(request)
    if store.load_task(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Task events are planned for P6")
