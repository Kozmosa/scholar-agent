from __future__ import annotations

from dataclasses import dataclass

from ainrf.api.schemas import ApiStatus
from ainrf.state import TaskStage


@dataclass(slots=True)
class WebUiConfig:
    host: str = "127.0.0.1"
    port: int = 7860
    api_base_url: str = "http://127.0.0.1:8000"


@dataclass(slots=True)
class TaskStageSummary:
    stage: TaskStage
    count: int


@dataclass(slots=True)
class ConnectionSession:
    api_base_url: str = "http://127.0.0.1:8000"
    api_key: str = ""
    reachable: bool = False
    authenticated: bool = False
    health_status: ApiStatus | None = None
    state_root: str | None = None
    container_configured: bool = False
    container_detail: str | None = None
    total_tasks: int = 0
    task_summaries: tuple[TaskStageSummary, ...] = ()
    last_error: str | None = None
