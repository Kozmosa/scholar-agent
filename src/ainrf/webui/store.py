from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from ainrf.api.schemas import TaskSummaryResponse
from ainrf.state import TaskStage
from ainrf.webui.models import ContainerProfileRecord, ProjectRecord, ProjectRunRecord


class JsonProjectStore:
    def __init__(self, state_root: Path) -> None:
        self._state_root = state_root

    @property
    def webui_root(self) -> Path:
        return self._state_root / "webui"

    @property
    def projects_dir(self) -> Path:
        return self.webui_root / "projects"

    @property
    def project_runs_dir(self) -> Path:
        return self.webui_root / "project-runs"

    @property
    def config_path(self) -> Path:
        return self._state_root / "config.json"

    def save_project(self, project: ProjectRecord) -> Path:
        path = self.projects_dir / f"{project.slug}.json"
        self._write_json(path, project.model_dump(mode="json"))
        return path

    def load_project(self, slug: str) -> ProjectRecord | None:
        path = self.projects_dir / f"{slug}.json"
        if not path.exists():
            return None
        return ProjectRecord.model_validate(self._read_json(path))

    def list_projects(self) -> list[ProjectRecord]:
        if not self.projects_dir.exists():
            return []
        projects = [
            ProjectRecord.model_validate(self._read_json(path))
            for path in sorted(self.projects_dir.glob("*.json"))
        ]
        return sorted(projects, key=lambda item: (item.name.lower(), item.slug))

    def save_project_run(self, project_run: ProjectRunRecord) -> Path:
        path = self.project_runs_dir / f"{project_run.task_id}.json"
        self._write_json(path, project_run.model_dump(mode="json"))
        return path

    def load_project_run(self, task_id: str) -> ProjectRunRecord | None:
        path = self.project_runs_dir / f"{task_id}.json"
        if not path.exists():
            return None
        return ProjectRunRecord.model_validate(self._read_json(path))

    def list_project_runs(self, project_slug: str) -> list[ProjectRunRecord]:
        if not self.project_runs_dir.exists():
            return []
        runs = [
            ProjectRunRecord.model_validate(self._read_json(path))
            for path in sorted(self.project_runs_dir.glob("*.json"))
        ]
        filtered = [item for item in runs if item.project_slug == project_slug]
        return sorted(filtered, key=lambda item: item.created_at, reverse=True)

    def synchronize_task_summaries(self, items: list[TaskSummaryResponse]) -> None:
        if not self.project_runs_dir.exists():
            return
        summaries = {item.task_id: item for item in items}
        for path in sorted(self.project_runs_dir.glob("*.json")):
            payload = self._read_json(path)
            project_run = ProjectRunRecord.model_validate(payload)
            summary = summaries.get(project_run.task_id)
            if summary is None:
                continue
            updated = project_run.model_copy(
                update={
                    "last_known_status": summary.status,
                    "last_known_stage": summary.current_stage,
                    "termination_reason": summary.termination_reason,
                }
            )
            self.save_project_run(updated)

    def update_project_run_status(
        self,
        task_id: str,
        *,
        status: TaskStage,
        stage: TaskStage,
        termination_reason: str | None,
    ) -> None:
        project_run = self.load_project_run(task_id)
        if project_run is None:
            return
        self.save_project_run(
            project_run.model_copy(
                update={
                    "last_known_status": status,
                    "last_known_stage": stage,
                    "termination_reason": termination_reason,
                }
            )
        )

    def list_container_profiles(self) -> dict[str, ContainerProfileRecord]:
        payload = self._read_config_payload()
        container_profiles = payload.get("container_profiles")
        if not isinstance(container_profiles, dict):
            return {}
        profiles: dict[str, ContainerProfileRecord] = {}
        for name, profile_payload in container_profiles.items():
            if not isinstance(name, str):
                continue
            if not isinstance(profile_payload, dict):
                continue
            profiles[name] = ContainerProfileRecord.model_validate(profile_payload)
        return dict(sorted(profiles.items(), key=lambda item: item[0].lower()))

    def save_container_profile(
        self,
        name: str,
        profile: ContainerProfileRecord,
        *,
        set_default: bool = False,
    ) -> None:
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("Container profile name is required.")
        payload = self._read_config_payload()
        container_profiles = payload.get("container_profiles")
        if not isinstance(container_profiles, dict):
            container_profiles = cast(dict[str, object], {})
            payload["container_profiles"] = container_profiles
        typed_profiles = cast(dict[str, object], container_profiles)
        typed_profiles[normalized_name] = profile.model_dump(mode="json")
        if set_default:
            payload["default_container_profile"] = normalized_name
        self._write_json(self.config_path, payload)

    def load_container_profile(self, name: str) -> ContainerProfileRecord | None:
        return self.list_container_profiles().get(name)

    def resolve_project_container_profile(
        self, project: ProjectRecord
    ) -> ContainerProfileRecord | None:
        profile_name = project.defaults.container_profile_name.strip()
        if not profile_name:
            return None
        return self.load_container_profile(profile_name)

    def default_container_profile_name(self) -> str | None:
        payload = self._read_config_payload()
        value = payload.get("default_container_profile")
        if isinstance(value, str) and value.strip():
            return value
        return None

    def _read_config_payload(self) -> dict[str, object]:
        if not self.config_path.exists():
            return {}
        payload = self._read_json(self.config_path)
        if isinstance(payload, dict):
            return cast(dict[str, object], payload)
        return {}

    @staticmethod
    def _read_json(path: Path) -> object:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _write_json(path: Path, payload: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(f"{path.suffix}.tmp")
        tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp_path.replace(path)
