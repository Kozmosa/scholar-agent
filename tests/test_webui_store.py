from __future__ import annotations

from pathlib import Path

from ainrf.state import TaskMode, TaskStage
from ainrf.webui.models import (
    ContainerProfileRecord,
    ProjectDefaults,
    ProjectRecord,
    ProjectRunRecord,
)
from ainrf.webui.store import JsonProjectStore


def test_project_store_round_trips_project(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    project = ProjectRecord(
        slug="vision-stack",
        name="Vision Stack",
        description="Local project",
        defaults=ProjectDefaults(
            container_profile_name="gpu-main",
            default_mode=TaskMode.RESEARCH_DISCOVERY,
        ),
    )

    store.save_project(project)
    loaded = store.load_project("vision-stack")

    assert loaded is not None
    assert loaded.name == "Vision Stack"
    assert loaded.defaults.container_profile_name == "gpu-main"
    assert loaded.defaults.default_mode is TaskMode.RESEARCH_DISCOVERY


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
            mode=TaskMode.RESEARCH_DISCOVERY,
            paper_titles=["Paper B"],
            last_known_status=TaskStage.GATE_WAITING,
            last_known_stage=TaskStage.GATE_WAITING,
        )
    )

    runs = store.list_project_runs("vision-stack")

    assert [item.task_id for item in runs] == ["t-002", "t-001"]


def test_project_store_round_trips_container_profile(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    store.save_container_profile(
        "gpu-main",
        ContainerProfileRecord(
            host="gpu-01",
            port=22,
            user="researcher",
            ssh_key_path="/tmp/id_rsa",
            ssh_password="",
            project_dir="/workspace/projects/vision-stack",
        ),
    )

    loaded = store.load_container_profile("gpu-main")
    profiles = store.list_container_profiles()

    assert loaded is not None
    assert loaded.host == "gpu-01"
    assert loaded.user == "researcher"
    assert "gpu-main" in profiles


def test_project_store_sets_default_container_profile(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    store.save_container_profile(
        "gpu-main",
        ContainerProfileRecord(
            host="gpu-01",
            port=22,
            user="researcher",
            ssh_key_path="",
            ssh_password="",
            project_dir="/workspace/projects/vision-stack",
        ),
        set_default=True,
    )

    assert store.default_container_profile_name() == "gpu-main"


def test_project_store_resolves_project_container_profile(tmp_path: Path) -> None:
    store = JsonProjectStore(tmp_path)
    store.save_container_profile(
        "gpu-main",
        ContainerProfileRecord(
            host="gpu-01",
            port=22,
            user="researcher",
            ssh_key_path="",
            ssh_password="",
            project_dir="/workspace/projects/vision-stack",
        ),
    )
    project = ProjectRecord(
        slug="vision-stack",
        name="Vision Stack",
        defaults=ProjectDefaults(container_profile_name="gpu-main"),
    )

    resolved = store.resolve_project_container_profile(project)

    assert resolved is not None
    assert resolved.host == "gpu-01"
