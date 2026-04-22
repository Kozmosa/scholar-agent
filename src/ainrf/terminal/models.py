from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class TerminalSessionStatus(StrEnum):
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    FAILED = "failed"


@dataclass(slots=True)
class TerminalSessionRecord:
    session_id: str | None
    provider: str
    target_kind: str
    status: TerminalSessionStatus
    environment_id: str | None = None
    environment_alias: str | None = None
    working_directory: str | None = None
    created_at: datetime | None = None
    started_at: datetime | None = None
    closed_at: datetime | None = None
    terminal_ws_url: str | None = None
    detail: str | None = None
    pid: int | None = None
    terminal_ws_token: str | None = None


def utc_now() -> datetime:
    return datetime.now(UTC)
