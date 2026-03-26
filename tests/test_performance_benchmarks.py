from __future__ import annotations

import asyncio
import time
from pathlib import Path

import pytest

from ainrf.events import JsonlTaskEventStore, TaskEventCategory, TaskEventService
from ainrf.state import JsonStateStore, TaskCheckpoint, TaskMode, TaskRecord, TaskStage


def _task(task_id: str) -> TaskRecord:
    return TaskRecord(
        task_id=task_id,
        mode=TaskMode.DEEP_REPRODUCTION,
        status=TaskStage.PLANNING,
        checkpoint=TaskCheckpoint(current_stage=TaskStage.PLANNING),
    )


@pytest.mark.anyio
async def test_event_service_concurrent_publish_smoke(tmp_path: Path) -> None:
    """Lightweight concurrency benchmark to catch obvious event write bottlenecks."""
    store = JsonlTaskEventStore(tmp_path)
    service = TaskEventService(store)

    task_id = "t-perf"
    workers = 8
    events_per_worker = 20

    async def publish_batch(worker_index: int) -> None:
        for event_index in range(events_per_worker):
            await asyncio.to_thread(
                service.publish,
                task_id=task_id,
                category=TaskEventCategory.LOG,
                event="perf.event",
                payload={"worker": worker_index, "index": event_index},
            )

    start = time.perf_counter()
    await asyncio.gather(*(publish_batch(worker) for worker in range(workers)))
    elapsed = time.perf_counter() - start

    events = store.list_events(task_id)
    assert len(events) == workers * events_per_worker
    # Keep this intentionally loose to avoid flaky CI while still surfacing regressions.
    assert elapsed < 10.0


def test_state_store_task_roundtrip_smoke(tmp_path: Path) -> None:
    """Measure coarse task read/write latency with a conservative threshold."""
    store = JsonStateStore(tmp_path)
    total = 80

    write_start = time.perf_counter()
    for index in range(total):
        store.save_task(_task(f"t-{index:03d}"))
    write_elapsed = time.perf_counter() - write_start

    read_start = time.perf_counter()
    loaded = [store.load_task(f"t-{index:03d}") for index in range(total)]
    read_elapsed = time.perf_counter() - read_start

    assert all(item is not None for item in loaded)
    assert write_elapsed < 10.0
    assert read_elapsed < 5.0
