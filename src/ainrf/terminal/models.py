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
    created_at: datetime | None = None
    started_at: datetime | None = None
    closed_at: datetime | None = None
    terminal_url: str | None = None
    detail: str | None = None
    pid: int | None = None
    browser_open_token: str | None = None
    browser_open_expires_at: datetime | None = None
    browser_open_consumed_at: datetime | None = None
    viewer_session_token: str | None = None
    viewer_session_expires_at: datetime | None = None
    viewer_cookie_name: str | None = None


def utc_now() -> datetime:
    return datetime.now(UTC)
