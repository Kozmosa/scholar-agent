from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class ApiStatus(StrEnum):
    OK = "ok"
    DEGRADED = "degraded"


class TerminalSessionStatus(StrEnum):
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    FAILED = "failed"


class CodeServerLifecycleStatus(StrEnum):
    STARTING = "starting"
    READY = "ready"
    UNAVAILABLE = "unavailable"


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: ApiStatus
    state_root: str
    container_configured: bool
    container_health: dict[str, Any] | None = None
    detail: str | None = None


class TerminalSessionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str | None = None
    provider: str = "pty"
    target_kind: str = "daemon-host"
    status: TerminalSessionStatus
    created_at: str | None = None
    started_at: str | None = None
    closed_at: str | None = None
    terminal_ws_url: str | None = None
    detail: str | None = None


class CodeServerStatusResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: CodeServerLifecycleStatus
    workspace_dir: str | None = None
    detail: str | None = None
    managed: bool = True
