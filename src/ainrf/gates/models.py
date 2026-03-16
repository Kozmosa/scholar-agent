from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from ainrf.artifacts import GateType, JsonValue


def utc_now() -> datetime:
    return datetime.now(UTC)


class GateWebhookEvent(StrEnum):
    WAITING = "gate.waiting"
    REMINDER = "gate.reminder"


class IntakeGatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: str
    paper_titles: list[str] = Field(default_factory=list)
    paper_count: int
    yolo: bool = False


class PlanApprovalGatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: str
    summary: str
    milestones: list[str] = Field(default_factory=list)
    estimated_steps: int | None = None


GatePayload = IntakeGatePayload | PlanApprovalGatePayload


class GateWebhookPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event: GateWebhookEvent
    task_id: str
    gate_id: str
    gate_type: GateType
    summary: str
    payload: dict[str, JsonValue] = Field(default_factory=dict)
    approve_endpoint: str
    reject_endpoint: str
    timestamp: datetime = Field(default_factory=utc_now)
    deadline_at: datetime | None = None
