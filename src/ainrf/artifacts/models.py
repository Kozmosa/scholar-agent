from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from typing import Self

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(UTC)


JsonValue = Any


class ArtifactType(StrEnum):
    PAPER_CARD = "PaperCard"
    REPRODUCTION_TASK = "ReproductionTask"
    EXPERIMENT_RUN = "ExperimentRun"
    EVIDENCE_RECORD = "EvidenceRecord"
    CLAIM = "Claim"
    EXPLORATION_GRAPH = "ExplorationGraph"
    QUALITY_ASSESSMENT = "QualityAssessment"
    WORKSPACE_MANIFEST = "WorkspaceManifest"
    HUMAN_GATE = "HumanGate"


class PaperCardStatus(StrEnum):
    CAPTURED = "captured"
    STRUCTURED = "structured"


class ReproductionTaskStatus(StrEnum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    BLOCKED = "blocked"
    COMPLETED = "completed"


class ExperimentRunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ENV_FAILURE = "env_failure"
    CANCELLED = "cancelled"


class HumanGateStatus(StrEnum):
    WAITING = "waiting"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class ReproductionStrategy(StrEnum):
    REPRODUCE_FROM_SOURCE = "reproduce-from-source"
    IMPLEMENT_FROM_PAPER = "implement-from-paper"


class EvidenceType(StrEnum):
    PAPER_EXCERPT = "paper_excerpt"
    EXPERIMENT_RESULT = "experiment_result"
    HUMAN_NOTE = "human_note"
    PARSE_FAILURE = "parse_failure"
    DEVIATION_ANALYSIS = "deviation_analysis"
    IMPLEMENTATION_BLOCKER = "implementation_blocker"


class GateType(StrEnum):
    INTAKE = "intake"
    PLAN_APPROVAL = "plan_approval"
    RUNTIME_REVIEW = "runtime_review"


class ArtifactRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_type: ArtifactType
    artifact_id: str
    path: str | None = None


class ResourceUsage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gpu_hours: float | None = None
    api_cost_usd: float | None = None
    wall_clock_hours: float | None = None


class AssessmentDimension(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score: float
    summary: str
    evidence_ids: list[str] = Field(default_factory=list)


class LargeFileRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    size_gb: float


class ArtifactModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str
    artifact_type: ArtifactType
    schema_version: int = 1
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    source_task_id: str | None = None
    related_artifacts: list[ArtifactRef] = Field(default_factory=list)
    summary: str | None = None


class LifecycleArtifactModel(ArtifactModel):
    status: StrEnum

    def transition_to(self, next_status: str | StrEnum) -> Self:
        from ainrf.artifacts.transitions import assert_transition_allowed

        next_status_value = str(next_status)
        assert_transition_allowed(self.artifact_type, str(self.status), next_status_value)
        return self.model_copy(update={"status": next_status, "updated_at": utc_now()})


class PaperCard(LifecycleArtifactModel):
    artifact_type: ArtifactType = ArtifactType.PAPER_CARD
    status: PaperCardStatus
    title: str
    authors: list[str] = Field(default_factory=list)
    abstract: str | None = None
    source_uri: str | None = None
    problem_statement: str | None = None
    method_summary: str | None = None
    key_claims: list[str] = Field(default_factory=list)
    reproduction_value: str | None = None


class ReproductionTask(LifecycleArtifactModel):
    artifact_type: ArtifactType = ArtifactType.REPRODUCTION_TASK
    status: ReproductionTaskStatus
    strategy: ReproductionStrategy
    target_paper_id: str
    objective: str
    entry_points: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    stop_conditions: list[str] = Field(default_factory=list)
    blocking_reason: str | None = None


class ExperimentRun(LifecycleArtifactModel):
    artifact_type: ArtifactType = ArtifactType.EXPERIMENT_RUN
    status: ExperimentRunStatus
    reproduction_task_id: str
    run_type: str
    config_path: str | None = None
    log_path: str | None = None
    metrics: dict[str, float] = Field(default_factory=dict)
    output_paths: list[str] = Field(default_factory=list)
    resource_usage: ResourceUsage = Field(default_factory=ResourceUsage)
    failure_reason: str | None = None


class EvidenceRecord(ArtifactModel):
    artifact_type: ArtifactType = ArtifactType.EVIDENCE_RECORD
    evidence_type: EvidenceType
    statement: str
    source_path: str | None = None
    locator: str | None = None
    content: str | None = None


class Claim(ArtifactModel):
    artifact_type: ArtifactType = ArtifactType.CLAIM
    statement: str
    confidence: float | None = None
    evidence_ids: list[str] = Field(default_factory=list)


class ExplorationGraph(ArtifactModel):
    artifact_type: ArtifactType = ArtifactType.EXPLORATION_GRAPH
    seed_paper_ids: list[str] = Field(default_factory=list)
    visited_paper_ids: list[str] = Field(default_factory=list)
    queued_paper_ids: list[str] = Field(default_factory=list)
    pruned_paper_ids: list[str] = Field(default_factory=list)
    reproduction_task_ids: list[str] = Field(default_factory=list)
    current_depth: int = 0
    budget_snapshot: ResourceUsage = Field(default_factory=ResourceUsage)
    termination_reason: str | None = None


class QualityAssessment(ArtifactModel):
    artifact_type: ArtifactType = ArtifactType.QUALITY_ASSESSMENT
    gold_nugget: AssessmentDimension
    reproducibility: AssessmentDimension
    scientific_rigor: AssessmentDimension
    overall_summary: str


class WorkspaceManifest(ArtifactModel):
    artifact_type: ArtifactType = ArtifactType.WORKSPACE_MANIFEST
    project_id: str
    container_host: str
    project_dir: str
    python_version: str | None = None
    cuda_version: str | None = None
    gpu_models: list[str] = Field(default_factory=list)
    key_packages: list[str] = Field(default_factory=list)
    budget_limit: ResourceUsage = Field(default_factory=ResourceUsage)
    budget_used: ResourceUsage = Field(default_factory=ResourceUsage)
    large_files: list[LargeFileRecord] = Field(default_factory=list)


class HumanGate(LifecycleArtifactModel):
    artifact_type: ArtifactType = ArtifactType.HUMAN_GATE
    status: HumanGateStatus
    gate_type: GateType
    summary: str
    payload: dict[str, JsonValue] = Field(default_factory=dict)
    deadline_at: datetime | None = None
    resolved_at: datetime | None = None
    reminder_sent_at: datetime | None = None
    feedback: str | None = None
    auto_approved: bool = False


ArtifactRecord = (
    PaperCard
    | ReproductionTask
    | ExperimentRun
    | EvidenceRecord
    | Claim
    | ExplorationGraph
    | QualityAssessment
    | WorkspaceManifest
    | HumanGate
)
