from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from ainrf.artifacts import ArtifactRef, GateType, HumanGateStatus, ResourceUsage


def utc_now() -> datetime:
    return datetime.now(UTC)


class TaskStage(StrEnum):
    SUBMITTED = "submitted"
    INGESTING = "ingesting"
    PLANNING = "planning"
    GATE_WAITING = "gate_waiting"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskMode(StrEnum):
    LITERATURE_EXPLORATION = "literature_exploration"
    DEEP_REPRODUCTION = "deep_reproduction"


class GateRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gate_id: str
    gate_type: GateType
    status: HumanGateStatus
    at: datetime = Field(default_factory=utc_now)
    feedback: str | None = None


class AtomicTaskRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step: str
    status: str | None = None
    at: datetime | None = None
    details: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class TaskCheckpoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    current_stage: TaskStage
    completed_steps: list[AtomicTaskRecord] = Field(default_factory=list)
    pending_queue: list[AtomicTaskRecord] = Field(default_factory=list)
    artifact_refs: list[ArtifactRef] = Field(default_factory=list)


class TaskRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    mode: TaskMode
    status: TaskStage
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    config: dict[str, object] = Field(default_factory=dict)
    checkpoint: TaskCheckpoint
    budget_limit: ResourceUsage = Field(default_factory=ResourceUsage)
    budget_used: ResourceUsage = Field(default_factory=ResourceUsage)
    gates: list[GateRecord] = Field(default_factory=list)
    termination_reason: str | None = None


class ArtifactQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str | None = None
    source_task_id: str | None = None
    related_to: str | None = None
    fields: dict[str, str | int | float | bool | None] = Field(default_factory=dict)
