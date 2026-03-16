from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(UTC)


class AtomicTaskSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_id: str
    kind: str
    title: str
    payload: dict[str, object] = Field(default_factory=dict)
    timeout_seconds: int | None = None


class StepArtifactRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_type: str
    artifact_id: str
    path: str


class TaskPlanResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    milestones: list[str] = Field(default_factory=list)
    estimated_steps: int
    strategy: str
    target_paper_id: str
    success_criteria: list[str] = Field(default_factory=list)
    steps: list[AtomicTaskSpec] = Field(default_factory=list)


class TaskExecutionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str
    summary: str
    messages: list[str] = Field(default_factory=list)
    artifacts: list[StepArtifactRef] = Field(default_factory=list)
    resource_usage: dict[str, float | None] = Field(default_factory=dict)
    step_updates: dict[str, object] = Field(default_factory=dict)
    error: str | None = None
    finished_at: datetime = Field(default_factory=utc_now)
