from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from ainrf.artifacts import JsonValue


def utc_now() -> datetime:
    return datetime.now(UTC)


class TaskEventCategory(StrEnum):
    TASK = "task"
    ARTIFACT = "artifact"
    GATE = "gate"
    EXPERIMENT = "experiment"
    LOG = "log"


class TaskEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: int
    task_id: str
    category: TaskEventCategory
    event: str
    timestamp: datetime = Field(default_factory=utc_now)
    payload: dict[str, JsonValue] = Field(default_factory=dict)
