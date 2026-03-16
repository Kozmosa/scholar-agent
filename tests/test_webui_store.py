from __future__ import annotations

from pathlib import Path

from ainrf.state import TaskMode, TaskStage
from ainrf.webui.models import ProjectDefaults, ProjectRecord, ProjectRunRecord
from ainrf.webui.store import JsonProjectStore


def test_project_store_round_trips_project(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    project = ProjectRecord(
        slug="vision-stack",
        name="Vision Stack",
        description="Local project",
        defaults=ProjectDefaults(container_host="gpu-01", container_user="researcher"),
    )

    store.save_project(project)
    loaded = store.load_project("vision-stack")

    assert loaded is not None
    assert loaded.name == "Vision Stack"
    assert loaded.defaults.container_host == "gpu-01"


def test_project_store_lists_runs_for_project_in_reverse_time_order(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    store.save_project_run(
        ProjectRunRecord(
            task_id="t-001",
            project_slug="vision-stack",
            mode=TaskMode.DEEP_REPRODUCTION,
            paper_titles=["Paper A"],
            last_known_status=TaskStage.PLANNING,
            last_known_stage=TaskStage.PLANNING,
        )
    )
    store.save_project_run(
        ProjectRunRecord(
            task_id="t-002",
            project_slug="vision-stack",
            mode=TaskMode.LITERATURE_EXPLORATION,
            paper_titles=["Paper B"],
            last_known_status=TaskStage.GATE_WAITING,
            last_known_stage=TaskStage.GATE_WAITING,
        )
    )

    runs = store.list_project_runs("vision-stack")

    assert [item.task_id for item in runs] == ["t-002", "t-001"]

