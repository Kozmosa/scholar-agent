from __future__ import annotations

import json
from pathlib import Path

from ainrf.api.schemas import TaskSummaryResponse
from ainrf.webui.models import ProjectRecord, ProjectRunRecord


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

    @staticmethod
    def _read_json(path: Path) -> object:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _write_json(path: Path, payload: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(f"{path.suffix}.tmp")
        tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp_path.replace(path)
