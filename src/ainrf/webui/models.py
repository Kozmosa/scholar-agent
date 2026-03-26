from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ainrf.api.schemas import ApiStatus, ArtifactItemResponse, ModeTwoScope, TaskDetailResponse
from ainrf.events import TaskEventCategory
from ainrf.state import TaskMode, TaskStage


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class WebUiConfig:
    host: str = "127.0.0.1"
    port: int = 7860
    api_base_url: str = "http://127.0.0.1:8000"
    state_root: Path = Path(".ainrf")


@dataclass(slots=True)
class TaskStageSummary:
    stage: TaskStage
    count: int


@dataclass(slots=True)
class RunTimelineItem:
    event_id: int
    event: str
    category: TaskEventCategory
    created_at: datetime
    payload: dict[str, Any]


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
    selected_project_slug: str | None = None
    selected_run_task_id: str | None = None
    selected_run_detail: TaskDetailResponse | None = None
    selected_run_artifacts: tuple[ArtifactItemResponse, ...] = ()
    run_timeline_items: tuple[RunTimelineItem, ...] = ()
    last_event_id_by_task: dict[str, int] = field(default_factory=dict)
    run_event_mode: str | None = None
    run_refresh_error: str | None = None
    last_error: str | None = None


class ModeOneDefaults(BaseModel):
    model_config = ConfigDict(extra="forbid")

    domain_context: str = ""
    max_depth: int = 3
    focus_directions: list[str] = Field(default_factory=list)
    ignore_directions: list[str] = Field(default_factory=list)


class ModeTwoDefaults(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scope: ModeTwoScope = ModeTwoScope.CORE_ONLY
    target_tables: list[str] = Field(default_factory=list)
    baseline_first: bool = True


class ProjectDefaults(BaseModel):
    model_config = ConfigDict(extra="forbid")

    container_host: str = ""
    container_port: int = 22
    container_user: str = ""
    container_ssh_key_path: str = ""
    container_project_dir: str = ""
    budget_gpu_hours: float | None = None
    budget_api_cost_usd: float | None = None
    budget_wall_clock_hours: float | None = None
    webhook_url: str = ""
    yolo: bool = False
    mode_1: ModeOneDefaults = Field(default_factory=ModeOneDefaults)
    mode_2: ModeTwoDefaults = Field(default_factory=ModeTwoDefaults)


class ContainerProfileRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    host: str
    port: int = 22
    user: str
    ssh_key_path: str = ""
    ssh_password: str = ""
    project_dir: str = ""


class ProjectRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    slug: str
    name: str
    description: str = ""
    defaults: ProjectDefaults = Field(default_factory=ProjectDefaults)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class ProjectRunRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    project_slug: str
    mode: TaskMode
    paper_titles: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    last_known_status: TaskStage
    last_known_stage: TaskStage
    termination_reason: str | None = None


class RunCreateFormState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: TaskMode = TaskMode.DEEP_REPRODUCTION
    webhook_secret: str = ""
    mode_1_seed_rows: list[list[str]] = Field(default_factory=list)
    mode_2_title: str = ""
    mode_2_pdf_url: str = ""
    mode_2_pdf_path: str = ""
