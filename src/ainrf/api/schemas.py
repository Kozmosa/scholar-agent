from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class ApiStatus(StrEnum):
    OK = "ok"
    DEGRADED = "degraded"


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: ApiStatus
    state_root: str
    container_configured: bool
    container_health: dict[str, Any] | None = None
    detail: str | None = None
