from __future__ import annotations

import pytest
from pydantic import ValidationError

from ainrf.artifacts import (
    ArtifactRef,
    ArtifactType,
    ExperimentRun,
    ExperimentRunStatus,
    GateType,
    HumanGate,
    HumanGateStatus,
    InvalidTransitionError,
    PaperCard,
    PaperCardStatus,
    ReproductionStrategy,
    ReproductionTask,
    ReproductionTaskStatus,
    ResourceUsage,
    WorkspaceManifest,
)


def test_paper_card_transition_to_structured() -> None:
    paper_card = PaperCard(
        artifact_id="pc-seed-001",
        status=PaperCardStatus.CAPTURED,
        title="Attention Is All You Need",
    )

    transitioned = paper_card.transition_to(PaperCardStatus.STRUCTURED)

    assert transitioned.status is PaperCardStatus.STRUCTURED
    assert transitioned.updated_at >= paper_card.updated_at


def test_paper_card_invalid_transition_raises() -> None:
    paper_card = PaperCard(
        artifact_id="pc-seed-001",
        status=PaperCardStatus.CAPTURED,
        title="Attention Is All You Need",
    )

    with pytest.raises(InvalidTransitionError):
        paper_card.transition_to("completed")


def test_human_gate_terminal_transition_is_rejected() -> None:
    gate = HumanGate(
        artifact_id="gate-001",
        status=HumanGateStatus.WAITING,
        gate_type=GateType.PLAN_APPROVAL,
        summary="Need approval",
        payload={"mode": "deep_reproduction", "summary": "Review plan"},
    ).transition_to(HumanGateStatus.APPROVED)

    with pytest.raises(InvalidTransitionError):
        gate.transition_to(HumanGateStatus.REJECTED)


def test_experiment_run_env_failure_is_formal_terminal_state() -> None:
    run = ExperimentRun(
        artifact_id="run-001",
        status=ExperimentRunStatus.PENDING,
        reproduction_task_id="rt-001",
        run_type="baseline",
    ).transition_to(ExperimentRunStatus.RUNNING)

    failed_run = run.transition_to(ExperimentRunStatus.ENV_FAILURE)

    assert failed_run.status is ExperimentRunStatus.ENV_FAILURE


def test_reproduction_task_supports_related_artifacts_round_trip() -> None:
    task = ReproductionTask(
        artifact_id="rt-001",
        status=ReproductionTaskStatus.PROPOSED,
        strategy=ReproductionStrategy.IMPLEMENT_FROM_PAPER,
        target_paper_id="pc-seed-001",
        objective="Implement baseline from paper",
        related_artifacts=[
            ArtifactRef(
                artifact_type=ArtifactType.PAPER_CARD,
                artifact_id="pc-seed-001",
                path="artifacts/paper-cards/seed-001.json",
            )
        ],
    )

    payload = task.model_dump(mode="json")

    assert payload["related_artifacts"][0]["artifact_type"] == ArtifactType.PAPER_CARD


def test_workspace_manifest_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        WorkspaceManifest.model_validate(
            {
                "artifact_id": "ws-001",
                "project_id": "attention-study",
                "container_host": "gpu-server-01",
                "project_dir": "/workspace/projects/attention",
                "unknown_field": "boom",
            }
        )


def test_resource_usage_defaults_are_optional() -> None:
    manifest = WorkspaceManifest(
        artifact_id="ws-001",
        project_id="attention-study",
        container_host="gpu-server-01",
        project_dir="/workspace/projects/attention",
        budget_limit=ResourceUsage(gpu_hours=24),
    )

    assert manifest.budget_limit.gpu_hours == 24
    assert manifest.budget_used.api_cost_usd is None


def test_human_gate_payload_round_trip() -> None:
    gate = HumanGate(
        artifact_id="gate-002",
        status=HumanGateStatus.WAITING,
        gate_type=GateType.INTAKE,
        summary="Need intake review",
        payload={"paper_count": 1, "paper_titles": ["Attention Is All You Need"], "mode": "deep_reproduction", "yolo": False},
    )

    payload = gate.model_dump(mode="json")

    assert payload["payload"]["paper_count"] == 1
