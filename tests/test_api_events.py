from __future__ import annotations

import asyncio
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any, cast

import httpx
import pytest
from fastapi import FastAPI

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key
from ainrf.events import TaskEventCategory
from ainrf.state import TaskCheckpoint, TaskMode, TaskRecord, TaskStage


def make_client(tmp_path: Path) -> tuple[FastAPI, httpx.AsyncClient]:
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
            gate_sweep_interval_seconds=60,
            sse_keepalive_seconds=0.05,
            sse_poll_interval_seconds=0.01,
        )
    )
    client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    )
    return app, client


def auth_headers(**extra: str) -> dict[str, str]:
    return {"X-API-Key": "secret-key", **extra}


def seed_task(app: FastAPI, *, status: TaskStage) -> TaskRecord:
    task = TaskRecord(
        task_id="t-001",
        mode=TaskMode.DEEP_REPRODUCTION,
        status=status,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        checkpoint=TaskCheckpoint(current_stage=status),
        termination_reason="user_requested" if status is TaskStage.CANCELLED else None,
    )
    app.state.state_store.save_task(task)
    return task


def extract_sse_events(raw_lines: list[str]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    current: dict[str, Any] = {}
    for line in raw_lines:
        if not line:
            if current:
                events.append(current)
                current = {}
            continue
        if line.startswith("id: "):
            current["id"] = int(line[4:])
        elif line.startswith("event: "):
            current["event"] = line[7:]
        elif line.startswith("data: "):
            current["data"] = json.loads(line[6:])
    if current:
        events.append(current)
    return events


@pytest.mark.anyio
async def test_task_events_replay_history_for_terminal_task(tmp_path: Path) -> None:
    app, client = make_client(tmp_path)
    seed_task(app, status=TaskStage.CANCELLED)
    app.state.event_service.publish(
        task_id="t-001",
        category=TaskEventCategory.TASK,
        event="task.stage_changed",
        payload={"previous_stage": "planning", "current_stage": "cancelled"},
    )
    app.state.event_service.publish(
        task_id="t-001",
        category=TaskEventCategory.TASK,
        event="task.cancelled",
        payload={"current_stage": "cancelled", "termination_reason": "user_requested"},
    )

    async with client:
        async with client.stream("GET", "/tasks/t-001/events", headers=auth_headers()) as response:
            assert response.status_code == 200
            lines = [line async for line in response.aiter_lines()]

    events = extract_sse_events(lines)
    assert [event["event"] for event in events] == ["task.stage_changed", "task.cancelled"]
    payload = cast(dict[str, Any], events[-1]["data"])
    payload_data = cast(dict[str, Any], payload["payload"])
    assert payload_data["termination_reason"] == "user_requested"


@pytest.mark.anyio
async def test_task_events_support_last_event_id_and_category_filter(tmp_path: Path) -> None:
    app, client = make_client(tmp_path)
    seed_task(app, status=TaskStage.CANCELLED)
    app.state.event_service.publish(
        task_id="t-001",
        category=TaskEventCategory.TASK,
        event="task.stage_changed",
        payload={"previous_stage": "submitted", "current_stage": "gate_waiting"},
    )
    app.state.event_service.publish(
        task_id="t-001",
        category=TaskEventCategory.GATE,
        event="gate.waiting",
        payload={"gate_id": "g-001"},
    )
    app.state.event_service.publish(
        task_id="t-001",
        category=TaskEventCategory.GATE,
        event="gate.resolved",
        payload={"gate_id": "g-001", "status": "approved"},
    )

    async with client:
        async with client.stream(
            "GET",
            "/tasks/t-001/events?types=gate",
            headers=auth_headers(**{"Last-Event-ID": "1"}),
        ) as response:
            assert response.status_code == 200
            lines = [line async for line in response.aiter_lines()]

    events = extract_sse_events(lines)
    assert [event["id"] for event in events] == [2, 3]
    assert [event["event"] for event in events] == ["gate.waiting", "gate.resolved"]


@pytest.mark.anyio
async def test_task_events_stream_new_events_for_nonterminal_task(tmp_path: Path) -> None:
    app, client = make_client(tmp_path)
    task = TaskRecord(
        task_id="t-001",
        mode=TaskMode.DEEP_REPRODUCTION,
        status=TaskStage.PLANNING,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
        checkpoint=TaskCheckpoint(current_stage=TaskStage.PLANNING),
    )
    app.state.state_store.save_task(task)

    async def publish_later() -> None:
        await asyncio.sleep(0.02)
        app.state.event_service.publish(
            task_id="t-001",
            category=TaskEventCategory.GATE,
            event="gate.waiting",
            payload={"gate_id": "g-001"},
        )
        updated = task.model_copy(
            update={
                "status": TaskStage.CANCELLED,
                "updated_at": datetime.now(UTC),
                "checkpoint": task.checkpoint.model_copy(update={"current_stage": TaskStage.CANCELLED}),
                "termination_reason": "user_requested",
            }
        )
        app.state.state_store.save_task(updated)
        app.state.event_service.publish(
            task_id="t-001",
            category=TaskEventCategory.TASK,
            event="task.cancelled",
            payload={"current_stage": "cancelled", "termination_reason": "user_requested"},
        )

    async with client:
        publisher = asyncio.create_task(publish_later())
        async with client.stream("GET", "/tasks/t-001/events", headers=auth_headers()) as response:
            assert response.status_code == 200
            lines = [line async for line in response.aiter_lines()]
        await publisher

    events = extract_sse_events(lines)
    assert [event["event"] for event in events] == ["gate.waiting", "task.cancelled"]


@pytest.mark.anyio
async def test_task_events_reject_invalid_last_event_id(tmp_path: Path) -> None:
    app, client = make_client(tmp_path)
    seed_task(app, status=TaskStage.CANCELLED)

    async with client:
        response = await client.get(
            "/tasks/t-001/events",
            headers=auth_headers(**{"Last-Event-ID": "abc"}),
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Last-Event-ID must be an integer"
