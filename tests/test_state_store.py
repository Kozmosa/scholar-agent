from __future__ import annotations

import json
from pathlib import Path

import pytest

from ainrf.artifacts import (
    ArtifactRef,
    ArtifactType,
    GateType,
    HumanGateStatus,
    PaperCard,
    PaperCardStatus,
    ReproductionStrategy,
    ReproductionTask,
    ReproductionTaskStatus,
)
from ainrf.state import (
    ArtifactQuery,
    AtomicTaskRecord,
    GateRecord,
    JsonStateStore,
    ResumeNotAllowedError,
    SerializationError,
    TaskCheckpoint,
    TaskMode,
    TaskRecord,
    TaskStage,
)


def test_json_state_store_round_trip_artifact(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    artifact = PaperCard(
        artifact_id="pc-seed-001",
        status=PaperCardStatus.CAPTURED,
        title="Attention Is All You Need",
        authors=["Alice", "Bob"],
        source_task_id="t-001",
    )

    artifact_path = store.save_artifact(artifact)
    loaded = store.load_artifact(ArtifactType.PAPER_CARD, artifact.artifact_id)

    assert artifact_path == tmp_path / "artifacts" / "paper-cards" / "pc-seed-001.json"
    assert loaded is not None
    assert isinstance(loaded, PaperCard)
    assert loaded.model_dump(mode="json") == artifact.model_dump(mode="json")


def test_query_related_artifacts_returns_downstream_match(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    paper_card = PaperCard(
        artifact_id="pc-seed-001",
        status=PaperCardStatus.STRUCTURED,
        title="Attention Is All You Need",
    )
    store.save_artifact(paper_card)
    reproduction_task = ReproductionTask(
        artifact_id="rt-001",
        status=ReproductionTaskStatus.PROPOSED,
        strategy=ReproductionStrategy.IMPLEMENT_FROM_PAPER,
        target_paper_id=paper_card.artifact_id,
        objective="Implement from scratch",
        related_artifacts=[
            ArtifactRef(
                artifact_type=ArtifactType.PAPER_CARD,
                artifact_id=paper_card.artifact_id,
            )
        ],
    )
    store.save_artifact(reproduction_task)

    matches = store.query_artifacts(
        ArtifactType.REPRODUCTION_TASK,
        ArtifactQuery(related_to=paper_card.artifact_id),
    )

    assert len(matches) == 1
    assert isinstance(matches[0], ReproductionTask)
    assert matches[0].artifact_id == "rt-001"


def test_query_filters_by_status_and_fields(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    proposed = ReproductionTask(
        artifact_id="rt-001",
        status=ReproductionTaskStatus.PROPOSED,
        strategy=ReproductionStrategy.REPRODUCE_FROM_SOURCE,
        target_paper_id="pc-001",
        objective="Reproduce open-source baseline",
    )
    active = ReproductionTask(
        artifact_id="rt-002",
        status=ReproductionTaskStatus.ACTIVE,
        strategy=ReproductionStrategy.REPRODUCE_FROM_SOURCE,
        target_paper_id="pc-001",
        objective="Reproduce open-source baseline",
    )
    store.save_artifact(proposed)
    store.save_artifact(active)

    matches = store.query_artifacts(
        ArtifactType.REPRODUCTION_TASK,
        ArtifactQuery(
            status="active",
            fields={"strategy": ReproductionStrategy.REPRODUCE_FROM_SOURCE.value},
        ),
    )

    assert [match.artifact_id for match in matches] == ["rt-002"]


def test_load_artifact_invalid_json_raises(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    artifact_path = tmp_path / "artifacts" / "paper-cards" / "pc-001.json"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text("{broken", encoding="utf-8")

    with pytest.raises(SerializationError):
        store.load_artifact(ArtifactType.PAPER_CARD, "pc-001")


def test_checkpoint_and_resume_task_round_trip(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    task = TaskRecord(
        task_id="t-001",
        mode=TaskMode.DEEP_REPRODUCTION,
        status=TaskStage.EXECUTING,
        checkpoint=TaskCheckpoint(
            current_stage=TaskStage.EXECUTING,
            completed_steps=[
                AtomicTaskRecord(
                    step="analyze_method",
                    status="success",
                    details={"paper": "pc-seed-001"},
                )
            ],
            pending_queue=[
                AtomicTaskRecord(
                    step="implement_module",
                    details={"module": "attention"},
                )
            ],
            artifact_refs=[
                ArtifactRef(
                    artifact_type=ArtifactType.PAPER_CARD,
                    artifact_id="pc-seed-001",
                    path="artifacts/paper-cards/pc-seed-001.json",
                )
            ],
        ),
        gates=[
            GateRecord(
                gate_id="g-001",
                gate_type=GateType.PLAN_APPROVAL,
                status=HumanGateStatus.APPROVED,
            )
        ],
        termination_reason=None,
    )

    task_path = store.checkpoint_task(task)
    resumed = store.resume_task(task.task_id)

    assert task_path == tmp_path / "tasks" / "t-001.json"
    assert resumed is not None
    assert resumed.model_dump(mode="json") == task.model_dump(mode="json")


def test_list_tasks_filters_by_status(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    submitted_task = TaskRecord(
        task_id="t-001",
        mode=TaskMode.DEEP_REPRODUCTION,
        status=TaskStage.SUBMITTED,
        checkpoint=TaskCheckpoint(current_stage=TaskStage.SUBMITTED),
    )
    cancelled_task = TaskRecord(
        task_id="t-002",
        mode=TaskMode.DEEP_REPRODUCTION,
        status=TaskStage.CANCELLED,
        checkpoint=TaskCheckpoint(current_stage=TaskStage.CANCELLED),
    )
    store.save_task(submitted_task)
    store.save_task(cancelled_task)

    tasks = store.list_tasks(TaskStage.SUBMITTED)

    assert [task.task_id for task in tasks] == ["t-001"]


def test_resume_task_rejects_terminal_status(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    task = TaskRecord(
        task_id="t-001",
        mode=TaskMode.LITERATURE_EXPLORATION,
        status=TaskStage.COMPLETED,
        checkpoint=TaskCheckpoint(current_stage=TaskStage.COMPLETED),
        termination_reason="diminishing_returns",
    )
    store.checkpoint_task(task)

    with pytest.raises(ResumeNotAllowedError):
        store.resume_task(task.task_id)


def test_list_resumable_tasks_filters_terminal_records(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    active_task = TaskRecord(
        task_id="t-001",
        mode=TaskMode.DEEP_REPRODUCTION,
        status=TaskStage.EXECUTING,
        checkpoint=TaskCheckpoint(current_stage=TaskStage.EXECUTING),
    )
    done_task = TaskRecord(
        task_id="t-002",
        mode=TaskMode.LITERATURE_EXPLORATION,
        status=TaskStage.COMPLETED,
        checkpoint=TaskCheckpoint(current_stage=TaskStage.COMPLETED),
    )
    store.checkpoint_task(active_task)
    store.checkpoint_task(done_task)

    resumable = store.list_resumable_tasks()

    assert [task.task_id for task in resumable] == ["t-001"]


def test_save_task_sanitizes_webhook_secret_from_persisted_config(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    task = TaskRecord(
        task_id="t-001",
        mode=TaskMode.DEEP_REPRODUCTION,
        status=TaskStage.SUBMITTED,
        checkpoint=TaskCheckpoint(current_stage=TaskStage.SUBMITTED),
        config={"webhook_url": "https://example.com/hooks/ainrf", "webhook_secret": "secret"},
    )

    store.save_task(task)

    payload = json.loads((tmp_path / "tasks" / "t-001.json").read_text(encoding="utf-8"))
    assert payload["config"]["webhook_url"] == "https://example.com/hooks/ainrf"
    assert "webhook_secret" not in payload["config"]


def test_relation_index_tracks_saved_artifacts(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    paper_card = PaperCard(
        artifact_id="pc-seed-001",
        status=PaperCardStatus.STRUCTURED,
        title="Attention Is All You Need",
    )
    store.save_artifact(paper_card)
    reproduction_task = ReproductionTask(
        artifact_id="rt-001",
        status=ReproductionTaskStatus.PROPOSED,
        strategy=ReproductionStrategy.IMPLEMENT_FROM_PAPER,
        target_paper_id=paper_card.artifact_id,
        objective="Implement from scratch",
        related_artifacts=[
            ArtifactRef(
                artifact_type=ArtifactType.PAPER_CARD,
                artifact_id=paper_card.artifact_id,
                path="artifacts/paper-cards/pc-seed-001.json",
            )
        ],
    )
    store.save_artifact(reproduction_task)

    index_payload = json.loads(
        (tmp_path / "indexes" / "artifact-links.json").read_text(encoding="utf-8")
    )

    assert index_payload["pc-seed-001"][0]["artifact_id"] == "rt-001"
