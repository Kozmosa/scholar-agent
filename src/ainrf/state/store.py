from __future__ import annotations

import json
from pathlib import Path
from typing import IO
from typing import Protocol

from ainrf.artifacts import (
    ArtifactRecord,
    ArtifactRef,
    ArtifactType,
    Claim,
    EvidenceRecord,
    ExperimentRun,
    ExplorationGraph,
    HumanGate,
    PaperCard,
    QualityAssessment,
    ReproductionTask,
    WorkspaceManifest,
)
from ainrf.state.errors import ResumeNotAllowedError, SerializationError, StateStoreError
from ainrf.state.models import ArtifactQuery, TaskRecord, TaskStage

ARTIFACT_MODEL_BY_TYPE: dict[ArtifactType, type[ArtifactRecord]] = {
    ArtifactType.PAPER_CARD: PaperCard,
    ArtifactType.REPRODUCTION_TASK: ReproductionTask,
    ArtifactType.EXPERIMENT_RUN: ExperimentRun,
    ArtifactType.EVIDENCE_RECORD: EvidenceRecord,
    ArtifactType.CLAIM: Claim,
    ArtifactType.EXPLORATION_GRAPH: ExplorationGraph,
    ArtifactType.QUALITY_ASSESSMENT: QualityAssessment,
    ArtifactType.WORKSPACE_MANIFEST: WorkspaceManifest,
    ArtifactType.HUMAN_GATE: HumanGate,
}

ARTIFACT_DIRECTORY_NAMES: dict[ArtifactType, str] = {
    ArtifactType.PAPER_CARD: "paper-cards",
    ArtifactType.REPRODUCTION_TASK: "reproduction-tasks",
    ArtifactType.EXPERIMENT_RUN: "experiment-runs",
    ArtifactType.EVIDENCE_RECORD: "evidence",
    ArtifactType.CLAIM: "claims",
    ArtifactType.EXPLORATION_GRAPH: "exploration-graphs",
    ArtifactType.QUALITY_ASSESSMENT: "quality-assessments",
    ArtifactType.WORKSPACE_MANIFEST: "workspace-manifests",
    ArtifactType.HUMAN_GATE: "human-gates",
}

TERMINAL_TASK_STAGES = {TaskStage.COMPLETED, TaskStage.FAILED, TaskStage.CANCELLED}


def _lock_file(lock_handle: IO[str]) -> None:
    try:
        import fcntl
    except ImportError:  # pragma: no cover
        return
    fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)


def default_state_root() -> Path:
    return Path(".ainrf")


class StateStore(Protocol):
    def save_artifact(self, artifact: ArtifactRecord) -> Path: ...

    def save_task(self, task: TaskRecord) -> Path: ...

    def load_artifact(
        self,
        artifact_type: ArtifactType,
        artifact_id: str,
    ) -> ArtifactRecord | None: ...

    def query_artifacts(
        self,
        artifact_type: ArtifactType,
        query: ArtifactQuery | None = None,
    ) -> list[ArtifactRecord]: ...

    def checkpoint_task(self, task: TaskRecord) -> Path: ...

    def load_task(self, task_id: str) -> TaskRecord | None: ...

    def list_tasks(self, status: TaskStage | None = None) -> list[TaskRecord]: ...

    def resume_task(self, task_id: str) -> TaskRecord | None: ...

    def list_resumable_tasks(self) -> list[TaskRecord]: ...


class JsonStateStore:
    def __init__(self, root_dir: Path | None = None) -> None:
        self._root_dir = root_dir or default_state_root()

    @property
    def root_dir(self) -> Path:
        return self._root_dir

    @property
    def artifacts_dir(self) -> Path:
        return self._root_dir / "artifacts"

    @property
    def indexes_dir(self) -> Path:
        return self._root_dir / "indexes"

    @property
    def tasks_dir(self) -> Path:
        return self._root_dir / "tasks"

    def save_artifact(self, artifact: ArtifactRecord) -> Path:
        existing = self.load_artifact(artifact.artifact_type, artifact.artifact_id)
        artifact_path = self._artifact_path(artifact.artifact_type, artifact.artifact_id)
        self._write_json(
            artifact_path,
            artifact.model_dump(mode="json"),
        )
        self._update_relation_index(existing, artifact, artifact_path)
        return artifact_path

    def load_artifact(
        self,
        artifact_type: ArtifactType,
        artifact_id: str,
    ) -> ArtifactRecord | None:
        artifact_path = self._artifact_path(artifact_type, artifact_id)
        if not artifact_path.exists():
            return None
        payload = self._read_json(artifact_path)
        return self._validate_artifact_payload(artifact_type, payload)

    def query_artifacts(
        self,
        artifact_type: ArtifactType,
        query: ArtifactQuery | None = None,
    ) -> list[ArtifactRecord]:
        normalized_query = query or ArtifactQuery()
        if normalized_query.related_to is not None:
            refs = self._load_relation_index().get(normalized_query.related_to, [])
            candidates = [
                self.load_artifact(artifact_type, ref.artifact_id)
                for ref in refs
                if ref.artifact_type is artifact_type
            ]
            artifacts = [artifact for artifact in candidates if artifact is not None]
        else:
            artifact_dir = self.artifacts_dir / ARTIFACT_DIRECTORY_NAMES[artifact_type]
            if not artifact_dir.exists():
                return []
            artifacts = []
            for artifact_path in sorted(artifact_dir.glob("*.json")):
                payload = self._read_json(artifact_path)
                artifacts.append(self._validate_artifact_payload(artifact_type, payload))

        return [
            artifact for artifact in artifacts if self._matches_query(artifact, normalized_query)
        ]

    def checkpoint_task(self, task: TaskRecord) -> Path:
        return self.save_task(task)

    def save_task(self, task: TaskRecord) -> Path:
        task_path = self._task_path(task.task_id)
        self._write_json(task_path, task.model_dump(mode="json"))
        return task_path

    def load_task(self, task_id: str) -> TaskRecord | None:
        task_path = self._task_path(task_id)
        if not task_path.exists():
            return None
        payload = self._read_json(task_path)
        try:
            return TaskRecord.model_validate(payload)
        except Exception as exc:  # pragma: no cover - pydantic bundles multiple error types
            raise SerializationError(f"Invalid task payload in {task_path}: {exc}") from exc

    def list_tasks(self, status: TaskStage | None = None) -> list[TaskRecord]:
        if not self.tasks_dir.exists():
            return []
        tasks: list[TaskRecord] = []
        for task_path in sorted(self.tasks_dir.glob("*.json")):
            task = self.load_task(task_path.stem)
            if task is None:
                continue
            if status is not None and task.status is not status:
                continue
            tasks.append(task)
        return tasks

    def resume_task(self, task_id: str) -> TaskRecord | None:
        task = self.load_task(task_id)
        if task is None:
            return None
        if task.status in TERMINAL_TASK_STAGES:
            raise ResumeNotAllowedError(f"Task {task_id} is terminal and cannot be resumed")
        return task

    def list_resumable_tasks(self) -> list[TaskRecord]:
        return [task for task in self.list_tasks() if task.status not in TERMINAL_TASK_STAGES]

    def _artifact_path(self, artifact_type: ArtifactType, artifact_id: str) -> Path:
        directory = self.artifacts_dir / ARTIFACT_DIRECTORY_NAMES[artifact_type]
        return directory / f"{artifact_id}.json"

    def _task_path(self, task_id: str) -> Path:
        return self.tasks_dir / f"{task_id}.json"

    def _index_path(self) -> Path:
        return self.indexes_dir / "artifact-links.json"

    def _validate_artifact_payload(
        self,
        artifact_type: ArtifactType,
        payload: object,
    ) -> ArtifactRecord:
        model_cls = ARTIFACT_MODEL_BY_TYPE[artifact_type]
        try:
            return model_cls.model_validate(payload)
        except Exception as exc:  # pragma: no cover - pydantic bundles multiple error types
            raise SerializationError(
                f"Invalid {artifact_type.value} payload in state store: {exc}"
            ) from exc

    def _update_relation_index(
        self,
        previous_artifact: ArtifactRecord | None,
        current_artifact: ArtifactRecord,
        current_path: Path,
    ) -> None:
        index = self._load_relation_index()
        if previous_artifact is not None:
            self._remove_from_index(index, previous_artifact.artifact_id)
        current_ref = ArtifactRef(
            artifact_type=current_artifact.artifact_type,
            artifact_id=current_artifact.artifact_id,
            path=self._relative_path(current_path),
        )
        for upstream_ref in current_artifact.related_artifacts:
            downstream_refs = index.setdefault(upstream_ref.artifact_id, [])
            if all(ref.artifact_id != current_ref.artifact_id for ref in downstream_refs):
                downstream_refs.append(current_ref)
        self._write_relation_index(index)

    def _load_relation_index(self) -> dict[str, list[ArtifactRef]]:
        index_path = self._index_path()
        if not index_path.exists():
            return {}
        payload = self._read_json(index_path)
        if not isinstance(payload, dict):
            raise SerializationError(f"Invalid relation index payload in {index_path}")

        index: dict[str, list[ArtifactRef]] = {}
        for artifact_id, refs_payload in payload.items():
            if not isinstance(artifact_id, str) or not isinstance(refs_payload, list):
                raise SerializationError(f"Invalid relation index payload in {index_path}")
            refs: list[ArtifactRef] = []
            for ref_payload in refs_payload:
                refs.append(ArtifactRef.model_validate(ref_payload))
            index[artifact_id] = refs
        return index

    def _write_relation_index(self, index: dict[str, list[ArtifactRef]]) -> None:
        payload = {
            artifact_id: [ref.model_dump(mode="json") for ref in refs]
            for artifact_id, refs in sorted(index.items())
        }
        self._write_json(self._index_path(), payload)

    def _remove_from_index(
        self,
        index: dict[str, list[ArtifactRef]],
        downstream_artifact_id: str,
    ) -> None:
        empty_keys: list[str] = []
        for upstream_id, refs in index.items():
            filtered_refs = [ref for ref in refs if ref.artifact_id != downstream_artifact_id]
            if filtered_refs:
                index[upstream_id] = filtered_refs
            else:
                empty_keys.append(upstream_id)
        for empty_key in empty_keys:
            index.pop(empty_key, None)

    def _matches_query(self, artifact: ArtifactRecord, query: ArtifactQuery) -> bool:
        if query.status is not None and getattr(artifact, "status", None) != query.status:
            return False
        if query.source_task_id is not None and artifact.source_task_id != query.source_task_id:
            return False
        for key, expected in query.fields.items():
            if not self._field_matches(getattr(artifact, key, None), expected):
                return False
        return True

    def _field_matches(
        self,
        actual: object,
        expected: str | int | float | bool | None,
    ) -> bool:
        if hasattr(actual, "value"):
            return getattr(actual, "value") == expected
        return actual == expected

    def _read_json(self, path: Path) -> object:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise SerializationError(f"Failed to load state payload {path}: {exc}") from exc

    def _write_json(self, path: Path, payload: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = path.with_suffix(f"{path.suffix}.lock")
        temp_path = path.with_suffix(f"{path.suffix}.tmp")

        try:
            with lock_path.open("w", encoding="utf-8") as lock_handle:
                _lock_file(lock_handle)
                temp_path.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                temp_path.replace(path)
        except OSError as exc:
            raise StateStoreError(f"Failed to write state payload {path}: {exc}") from exc

    def _relative_path(self, path: Path) -> str:
        return path.relative_to(self.root_dir).as_posix()
