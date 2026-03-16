from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ainrf.artifacts import ArtifactType, GateType, HumanGateStatus, ResourceUsage
from ainrf.state import TaskMode, TaskStage


class PaperRole(StrEnum):
    SEED = "seed"
    TARGET = "target"


class ModeTwoScope(StrEnum):
    CORE_ONLY = "core-only"
    FULL_SUITE = "full-suite"


class ApiStatus(StrEnum):
    OK = "ok"
    DEGRADED = "degraded"


class PaperInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    pdf_url: str | None = None
    pdf_path: str | None = None
    role: PaperRole

    @model_validator(mode="after")
    def validate_pdf_source(self) -> PaperInput:
        if not self.pdf_url and not self.pdf_path:
            raise ValueError("Either pdf_url or pdf_path must be provided")
        return self


class ModeOneConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    domain_context: str | None = None
    max_depth: int = 3
    focus_directions: list[str] = Field(default_factory=list)
    ignore_directions: list[str] = Field(default_factory=list)


class ModeTwoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scope: ModeTwoScope = ModeTwoScope.CORE_ONLY
    target_tables: list[str] = Field(default_factory=list)
    baseline_first: bool = True


class TaskConfigInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode_1: ModeOneConfig | None = None
    mode_2: ModeTwoConfig | None = None


class ContainerInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    host: str
    port: int = 22
    user: str
    ssh_key_path: str | None = None
    project_dir: str


class TaskCreateRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "mode": "deep_reproduction",
                "papers": [
                    {
                        "title": "Attention Is All You Need",
                        "pdf_url": "https://arxiv.org/pdf/1706.03762",
                        "role": "target",
                    }
                ],
                "config": {
                    "mode_2": {
                        "scope": "core-only",
                        "target_tables": ["Table 1"],
                        "baseline_first": True,
                    }
                },
                "container": {
                    "host": "gpu-server-01",
                    "port": 22,
                    "user": "researcher",
                    "ssh_key_path": "/path/to/id_rsa",
                    "project_dir": "/workspace/projects/attention-study",
                },
                "budget": {
                    "gpu_hours": 24,
                    "api_cost_usd": 50,
                    "wall_clock_hours": 48,
                },
                "yolo": False,
                "webhook_url": "https://example.com/hooks/ainrf",
                "webhook_secret": "hmac-shared-secret",
            }
        },
    )

    mode: TaskMode
    papers: list[PaperInput] = Field(min_length=1)
    config: TaskConfigInput = Field(default_factory=TaskConfigInput)
    container: ContainerInput
    budget: ResourceUsage
    yolo: bool = False
    webhook_url: str | None = None
    webhook_secret: str | None = None


class GateRecordResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gate_id: str
    gate_type: GateType
    status: HumanGateStatus
    at: datetime
    resolved_at: datetime | None = None
    feedback: str | None = None


class ActiveGateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gate_id: str
    gate_type: GateType
    status: HumanGateStatus
    summary: str
    payload: dict[str, Any] = Field(default_factory=dict)
    deadline_at: datetime | None = None
    resolved_at: datetime | None = None
    reminder_sent_at: datetime | None = None
    feedback: str | None = None
    auto_approved: bool = False


class ArtifactSummaryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    counts: dict[str, int] = Field(default_factory=dict)
    total: int = 0


class TaskSummaryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    mode: TaskMode
    status: TaskStage
    created_at: datetime
    updated_at: datetime
    current_stage: TaskStage
    termination_reason: str | None = None


class TaskDetailResponse(TaskSummaryResponse):
    budget_limit: ResourceUsage
    budget_used: ResourceUsage
    gates: list[GateRecordResponse] = Field(default_factory=list)
    active_gate: ActiveGateResponse | None = None
    artifact_summary: ArtifactSummaryResponse
    config: dict[str, Any] = Field(default_factory=dict)


class TaskListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[TaskSummaryResponse]


class TaskCreateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    status: TaskStage


class TaskActionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    status: TaskStage
    detail: str


class TaskRejectRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    feedback: str | None = None


class ArtifactItemResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str
    artifact_type: ArtifactType
    source_task_id: str | None = None
    summary: str | None = None
    status: str | None = None
    payload: dict[str, Any]


class TaskArtifactsResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    items: list[ArtifactItemResponse]


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: ApiStatus
    state_root: str
    container_configured: bool
    container_health: dict[str, Any] | None = None
    detail: str | None = None
