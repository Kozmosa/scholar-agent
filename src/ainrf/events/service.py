from __future__ import annotations

from ainrf.artifacts import JsonValue
from ainrf.events.models import TaskEvent, TaskEventCategory
from ainrf.events.store import JsonlTaskEventStore


class TaskEventService:
    def __init__(self, store: JsonlTaskEventStore) -> None:
        self._store = store

    def publish(
        self,
        *,
        task_id: str,
        category: TaskEventCategory,
        event: str,
        payload: dict[str, JsonValue],
    ) -> TaskEvent:
        return self._store.append_event(
            task_id=task_id,
            category=category,
            event=event,
            payload=payload,
        )

    def list_events(
        self,
        task_id: str,
        *,
        after_id: int | None = None,
        categories: set[TaskEventCategory] | None = None,
    ) -> list[TaskEvent]:
        return self._store.list_events(task_id, after_id=after_id, categories=categories)
