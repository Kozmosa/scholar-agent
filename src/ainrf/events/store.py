from __future__ import annotations
from pathlib import Path
from typing import IO

from ainrf.events.models import TaskEvent, TaskEventCategory
from ainrf.state.errors import SerializationError, StateStoreError
from ainrf.state.store import default_state_root


def _lock_file(lock_handle: IO[str]) -> None:
    try:
        import fcntl
    except ImportError:  # pragma: no cover
        return
    fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)


class JsonlTaskEventStore:
    def __init__(self, root_dir: Path | None = None) -> None:
        self._root_dir = root_dir or default_state_root()

    @property
    def root_dir(self) -> Path:
        return self._root_dir

    @property
    def events_dir(self) -> Path:
        return self._root_dir / "events"

    def append_event(
        self,
        *,
        task_id: str,
        category: TaskEventCategory,
        event: str,
        payload: dict[str, object],
    ) -> TaskEvent:
        path = self._event_path(task_id)
        lock_path = path.with_suffix(f"{path.suffix}.lock")
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with lock_path.open("w", encoding="utf-8") as lock_handle:
                _lock_file(lock_handle)
                next_id = self._read_last_event_id(path) + 1
                record = TaskEvent(
                    event_id=next_id,
                    task_id=task_id,
                    category=category,
                    event=event,
                    payload=payload,
                )
                with path.open("a", encoding="utf-8") as handle:
                    handle.write(record.model_dump_json())
                    handle.write("\n")
                return record
        except OSError as exc:
            raise StateStoreError(f"Failed to append event for task {task_id}: {exc}") from exc

    def list_events(
        self,
        task_id: str,
        *,
        after_id: int | None = None,
        categories: set[TaskEventCategory] | None = None,
    ) -> list[TaskEvent]:
        path = self._event_path(task_id)
        if not path.exists():
            return []

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            raise StateStoreError(f"Failed to read event log for task {task_id}: {exc}") from exc

        events: list[TaskEvent] = []
        for line in lines:
            if not line.strip():
                continue
            try:
                event = TaskEvent.model_validate_json(line)
            except Exception as exc:  # pragma: no cover - pydantic aggregates errors
                raise SerializationError(
                    f"Invalid event payload in {path}: {exc}"
                ) from exc
            if after_id is not None and event.event_id <= after_id:
                continue
            if categories is not None and event.category not in categories:
                continue
            events.append(event)
        return events

    def _event_path(self, task_id: str) -> Path:
        return self.events_dir / f"{task_id}.jsonl"

    def _read_last_event_id(self, path: Path) -> int:
        if not path.exists():
            return 0

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            raise StateStoreError(f"Failed to read event log {path}: {exc}") from exc

        for line in reversed(lines):
            if not line.strip():
                continue
            try:
                event = TaskEvent.model_validate_json(line)
            except Exception as exc:  # pragma: no cover - pydantic aggregates errors
                raise SerializationError(f"Invalid event payload in {path}: {exc}") from exc
            return event.event_id
        return 0
