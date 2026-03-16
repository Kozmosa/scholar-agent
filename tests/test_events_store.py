from __future__ import annotations

from pathlib import Path

from ainrf.events import JsonlTaskEventStore, TaskEventCategory


def test_event_store_appends_monotonic_ids_and_filters_by_category(tmp_path: Path) -> None:
    store = JsonlTaskEventStore(tmp_path)
    store.append_event(
        task_id="t-001",
        category=TaskEventCategory.TASK,
        event="task.stage_changed",
        payload={"current_stage": "planning"},
    )
    store.append_event(
        task_id="t-001",
        category=TaskEventCategory.GATE,
        event="gate.waiting",
        payload={"gate_id": "g-001"},
    )
    store.append_event(
        task_id="t-001",
        category=TaskEventCategory.TASK,
        event="task.cancelled",
        payload={"current_stage": "cancelled"},
    )

    all_events = store.list_events("t-001")
    assert [event.event_id for event in all_events] == [1, 2, 3]
    assert [event.event for event in all_events] == [
        "task.stage_changed",
        "gate.waiting",
        "task.cancelled",
    ]

    resumed = store.list_events("t-001", after_id=1)
    assert [event.event_id for event in resumed] == [2, 3]

    gate_only = store.list_events("t-001", categories={TaskEventCategory.GATE})
    assert [event.event for event in gate_only] == ["gate.waiting"]
