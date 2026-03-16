from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import httpx
import pytest

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key
from ainrf.artifacts import ArtifactType, GateType, HumanGate, HumanGateStatus, PaperCard, PaperCardStatus
from ainrf.events import JsonlTaskEventStore
from ainrf.state import (
    GateRecord,
    JsonStateStore,
    TaskCheckpoint,
    TaskMode,
    TaskRecord,
    TaskStage,
)


def make_client(tmp_path: Path, **config_overrides: Any) -> httpx.AsyncClient:
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
            gate_sweep_interval_seconds=60,
            **config_overrides,
        )
    )
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    )


def auth_headers() -> dict[str, str]:
    return {"X-API-Key": "secret-key"}


def create_task_payload(*, yolo: bool = False, include_webhook: bool = True) -> dict[str, object]:
    payload: dict[str, object] = {
        "mode": "deep_reproduction",
        "papers": [
            {
                "title": "Attention Is All You Need",
                "pdf_url": "https://arxiv.org/pdf/1706.03762",
                "role": "target",
            }
        ],
        "config": {
            "mode_2": {
                "scope": "core-only",
                "target_tables": ["Table 1"],
                "baseline_first": True,
            }
        },
        "container": {
            "host": "gpu-server-01",
            "port": 22,
            "user": "researcher",
            "ssh_key_path": "/tmp/id_rsa",
            "project_dir": "/workspace/projects/attention-study",
        },
        "budget": {
            "gpu_hours": 24,
            "api_cost_usd": 50,
            "wall_clock_hours": 48,
        },
        "yolo": yolo,
    }
    if include_webhook:
        payload["webhook_url"] = "https://example.com/hooks/ainrf"
        payload["webhook_secret"] = "hmac-shared-secret"
    return payload


def create_plan_gate(task_id: str, index: int, *, status: HumanGateStatus) -> HumanGate:
    now = datetime.now(UTC)
    return HumanGate(
        artifact_id=f"g-plan-{index}",
        source_task_id=task_id,
        status=status,
        gate_type=GateType.PLAN_APPROVAL,
        summary="Review plan",
        payload={"summary": "baseline then full run", "mode": "deep_reproduction"},
        deadline_at=now + timedelta(hours=1) if status is HumanGateStatus.WAITING else None,
        resolved_at=now if status is not HumanGateStatus.WAITING else None,
    )


@pytest.mark.anyio
async def test_create_task_persists_waiting_intake_gate_and_sanitizes_secret(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    webhook_calls: list[dict[str, Any]] = []

    async def fake_send(self: object, *, url: str, secret: str | None, payload: object) -> None:
        webhook_calls.append({"url": url, "secret": secret, "payload": payload})

    monkeypatch.setattr("ainrf.gates.manager.WebhookDispatcher.send", fake_send)

    async with make_client(tmp_path) as client:
        response = await client.post("/tasks", headers=auth_headers(), json=create_task_payload())

    assert response.status_code == 201
    payload = response.json()
    task = JsonStateStore(tmp_path).load_task(payload["task_id"])
    assert task is not None
    assert task.status is TaskStage.GATE_WAITING
    assert task.checkpoint.current_stage is TaskStage.GATE_WAITING
    assert task.config["webhook_url"] == "https://example.com/hooks/ainrf"
    assert "webhook_secret" not in task.config
    assert task.gates[0].gate_type is GateType.INTAKE
    assert task.gates[0].status is HumanGateStatus.WAITING

    active_gate = JsonStateStore(tmp_path).query_artifacts(
        ArtifactType.HUMAN_GATE,
        query=None,
    )[0]
    assert isinstance(active_gate, HumanGate)
    assert active_gate.status is HumanGateStatus.WAITING
    assert active_gate.payload["paper_count"] == 1

    events = JsonlTaskEventStore(tmp_path).list_events(payload["task_id"])
    assert [event.event for event in events] == [
        "artifact.created",
        "gate.waiting",
        "task.stage_changed",
    ]

    assert webhook_calls
    assert webhook_calls[0]["secret"] == "hmac-shared-secret"


@pytest.mark.anyio
async def test_create_task_in_yolo_mode_auto_approves_without_webhook(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def unexpected_send(self: object, *, url: str, secret: str | None, payload: object) -> None:
        raise AssertionError("yolo mode should not send webhook")

    monkeypatch.setattr("ainrf.gates.manager.WebhookDispatcher.send", unexpected_send)

    async with make_client(tmp_path) as client:
        response = await client.post(
            "/tasks",
            headers=auth_headers(),
            json=create_task_payload(yolo=True),
        )

    assert response.status_code == 201
    task = JsonStateStore(tmp_path).load_task(response.json()["task_id"])
    assert task is not None
    assert task.status is TaskStage.PLANNING
    assert task.gates[0].status is HumanGateStatus.APPROVED
    assert task.gates[0].resolved_at is not None
    events = JsonlTaskEventStore(tmp_path).list_events(response.json()["task_id"])
    assert [event.event for event in events] == [
        "artifact.created",
        "gate.resolved",
        "task.stage_changed",
    ]


@pytest.mark.anyio
async def test_create_task_validates_required_pdf_source(tmp_path: Path) -> None:
    payload = create_task_payload()
    payload["papers"] = [{"title": "Invalid", "role": "target"}]

    async with make_client(tmp_path) as client:
        response = await client.post("/tasks", headers=auth_headers(), json=payload)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_list_tasks_filters_by_status(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.SUBMITTED,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.SUBMITTED),
        )
    )
    store.save_task(
        TaskRecord(
            task_id="t-002",
            mode=TaskMode.LITERATURE_EXPLORATION,
            status=TaskStage.CANCELLED,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.CANCELLED),
        )
    )

    async with make_client(tmp_path) as client:
        response = await client.get("/tasks?status=submitted", headers=auth_headers())

    assert response.status_code == 200
    assert [item["task_id"] for item in response.json()["items"]] == ["t-001"]


@pytest.mark.anyio
async def test_get_task_returns_artifact_summary_and_active_gate(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.GATE_WAITING,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.GATE_WAITING),
            gates=[
                GateRecord(
                    gate_id="g-intake-001",
                    gate_type=GateType.INTAKE,
                    status=HumanGateStatus.WAITING,
                )
            ],
        )
    )
    store.save_artifact(
        HumanGate(
            artifact_id="g-intake-001",
            source_task_id="t-001",
            status=HumanGateStatus.WAITING,
            gate_type=GateType.INTAKE,
            summary="Review intake",
            payload={"paper_count": 1, "paper_titles": ["Attention Is All You Need"], "mode": "deep_reproduction", "yolo": False},
            deadline_at=datetime.now(UTC) + timedelta(hours=1),
        )
    )
    store.save_artifact(
        PaperCard(
            artifact_id="pc-001",
            status=PaperCardStatus.CAPTURED,
            title="Attention Is All You Need",
            source_task_id="t-001",
        )
    )

    async with make_client(tmp_path) as client:
        response = await client.get("/tasks/t-001", headers=auth_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["artifact_summary"]["counts"] == {
        ArtifactType.HUMAN_GATE.value: 1,
        ArtifactType.PAPER_CARD.value: 1,
    }
    assert body["active_gate"]["gate_id"] == "g-intake-001"


@pytest.mark.anyio
async def test_get_task_artifacts_returns_linked_artifacts(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.SUBMITTED,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.SUBMITTED),
        )
    )
    store.save_artifact(
        PaperCard(
            artifact_id="pc-001",
            status=PaperCardStatus.CAPTURED,
            title="Attention Is All You Need",
            source_task_id="t-001",
        )
    )

    async with make_client(tmp_path) as client:
        response = await client.get("/tasks/t-001/artifacts", headers=auth_headers())

    assert response.status_code == 200
    assert response.json()["items"][0]["artifact_id"] == "pc-001"


@pytest.mark.anyio
async def test_cancel_task_updates_status_and_cancels_waiting_gate(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    now = datetime.now(UTC)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.GATE_WAITING,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.GATE_WAITING),
            gates=[
                GateRecord(
                    gate_id="g-intake-001",
                    gate_type=GateType.INTAKE,
                    status=HumanGateStatus.WAITING,
                    at=now,
                )
            ],
        )
    )
    store.save_artifact(
        HumanGate(
            artifact_id="g-intake-001",
            source_task_id="t-001",
            status=HumanGateStatus.WAITING,
            gate_type=GateType.INTAKE,
            summary="Review intake",
            payload={"paper_count": 1, "paper_titles": ["Attention Is All You Need"], "mode": "deep_reproduction", "yolo": False},
            deadline_at=now + timedelta(hours=1),
        )
    )

    async with make_client(tmp_path) as client:
        response = await client.post("/tasks/t-001/cancel", headers=auth_headers())

    assert response.status_code == 200
    task = store.load_task("t-001")
    assert task is not None
    assert task.status is TaskStage.CANCELLED
    gate = store.load_artifact(ArtifactType.HUMAN_GATE, "g-intake-001")
    assert isinstance(gate, HumanGate)
    assert gate.status is HumanGateStatus.CANCELLED
    events = JsonlTaskEventStore(tmp_path).list_events("t-001")
    assert [event.event for event in events] == [
        "artifact.updated",
        "gate.resolved",
        "task.stage_changed",
        "task.cancelled",
    ]


@pytest.mark.anyio
async def test_cancel_task_rejects_terminal_task(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.COMPLETED,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.COMPLETED),
        )
    )

    async with make_client(tmp_path) as client:
        response = await client.post("/tasks/t-001/cancel", headers=auth_headers())

    assert response.status_code == 409


@pytest.mark.anyio
async def test_approve_intake_gate_advances_task_to_planning(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    now = datetime.now(UTC)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.GATE_WAITING,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.GATE_WAITING),
            gates=[
                GateRecord(
                    gate_id="g-intake-001",
                    gate_type=GateType.INTAKE,
                    status=HumanGateStatus.WAITING,
                    at=now,
                )
            ],
        )
    )
    store.save_artifact(
        HumanGate(
            artifact_id="g-intake-001",
            source_task_id="t-001",
            status=HumanGateStatus.WAITING,
            gate_type=GateType.INTAKE,
            summary="Review intake",
            payload={"paper_count": 1, "paper_titles": ["Attention Is All You Need"], "mode": "deep_reproduction", "yolo": False},
            deadline_at=now + timedelta(hours=1),
        )
    )

    async with make_client(tmp_path) as client:
        response = await client.post("/tasks/t-001/approve", headers=auth_headers())

    assert response.status_code == 200
    task = store.load_task("t-001")
    assert task is not None
    assert task.status is TaskStage.PLANNING
    assert task.gates[0].status is HumanGateStatus.APPROVED


@pytest.mark.anyio
async def test_reject_intake_gate_cancels_task(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    now = datetime.now(UTC)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.GATE_WAITING,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.GATE_WAITING),
            gates=[
                GateRecord(
                    gate_id="g-intake-001",
                    gate_type=GateType.INTAKE,
                    status=HumanGateStatus.WAITING,
                    at=now,
                )
            ],
        )
    )
    store.save_artifact(
        HumanGate(
            artifact_id="g-intake-001",
            source_task_id="t-001",
            status=HumanGateStatus.WAITING,
            gate_type=GateType.INTAKE,
            summary="Review intake",
            payload={"paper_count": 1, "paper_titles": ["Attention Is All You Need"], "mode": "deep_reproduction", "yolo": False},
            deadline_at=now + timedelta(hours=1),
        )
    )

    async with make_client(tmp_path) as client:
        response = await client.post(
            "/tasks/t-001/reject",
            headers=auth_headers(),
            json={"feedback": "out of scope"},
        )

    assert response.status_code == 200
    task = store.load_task("t-001")
    assert task is not None
    assert task.status is TaskStage.CANCELLED
    assert task.termination_reason == "intake_rejected"


@pytest.mark.anyio
async def test_plan_gate_rejection_advances_back_to_planning_until_limit(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    now = datetime.now(UTC)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.GATE_WAITING,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.GATE_WAITING),
            gates=[
                GateRecord(
                    gate_id="g-plan-1",
                    gate_type=GateType.PLAN_APPROVAL,
                    status=HumanGateStatus.REJECTED,
                    at=now - timedelta(minutes=3),
                    resolved_at=now - timedelta(minutes=3),
                ),
                GateRecord(
                    gate_id="g-plan-2",
                    gate_type=GateType.PLAN_APPROVAL,
                    status=HumanGateStatus.REJECTED,
                    at=now - timedelta(minutes=2),
                    resolved_at=now - timedelta(minutes=2),
                ),
                GateRecord(
                    gate_id="g-plan-3",
                    gate_type=GateType.PLAN_APPROVAL,
                    status=HumanGateStatus.WAITING,
                    at=now - timedelta(minutes=1),
                ),
            ],
        )
    )
    store.save_artifact(create_plan_gate("t-001", 1, status=HumanGateStatus.REJECTED))
    store.save_artifact(create_plan_gate("t-001", 2, status=HumanGateStatus.REJECTED))
    store.save_artifact(create_plan_gate("t-001", 3, status=HumanGateStatus.WAITING))

    async with make_client(tmp_path) as client:
        response = await client.post(
            "/tasks/t-001/reject",
            headers=auth_headers(),
            json={"feedback": "tighten plan"},
        )

    assert response.status_code == 200
    task = store.load_task("t-001")
    assert task is not None
    assert task.status is TaskStage.FAILED
    assert task.termination_reason == "plan_rejected_limit"


@pytest.mark.anyio
async def test_plan_gate_approval_advances_to_executing(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    now = datetime.now(UTC)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.GATE_WAITING,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.GATE_WAITING),
            gates=[
                GateRecord(
                    gate_id="g-plan-1",
                    gate_type=GateType.PLAN_APPROVAL,
                    status=HumanGateStatus.WAITING,
                    at=now,
                )
            ],
        )
    )
    store.save_artifact(create_plan_gate("t-001", 1, status=HumanGateStatus.WAITING))

    async with make_client(tmp_path) as client:
        response = await client.post("/tasks/t-001/approve", headers=auth_headers())

    assert response.status_code == 200
    task = store.load_task("t-001")
    assert task is not None
    assert task.status is TaskStage.EXECUTING


@pytest.mark.anyio
async def test_approve_reject_require_waiting_gate(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.PLANNING,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.PLANNING),
        )
    )

    async with make_client(tmp_path) as client:
        approve = await client.post("/tasks/t-001/approve", headers=auth_headers())
        reject = await client.post(
            "/tasks/t-001/reject",
            headers=auth_headers(),
            json={"feedback": "revise"},
        )

    assert approve.status_code == 409
    assert reject.status_code == 409


@pytest.mark.anyio
async def test_gate_reminder_marks_gate_once_and_sends_webhook(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = JsonStateStore(tmp_path)
    past = datetime.now(UTC) - timedelta(minutes=5)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.GATE_WAITING,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.GATE_WAITING),
            config={"webhook_url": "https://example.com/hooks/ainrf"},
            gates=[
                GateRecord(
                    gate_id="g-intake-001",
                    gate_type=GateType.INTAKE,
                    status=HumanGateStatus.WAITING,
                    at=past,
                )
            ],
        )
    )
    store.save_artifact(
        HumanGate(
            artifact_id="g-intake-001",
            source_task_id="t-001",
            status=HumanGateStatus.WAITING,
            gate_type=GateType.INTAKE,
            summary="Review intake",
            payload={"paper_count": 1, "paper_titles": ["Attention Is All You Need"], "mode": "deep_reproduction", "yolo": False},
            deadline_at=past,
        )
    )
    webhook_calls: list[str | None] = []

    async def fake_send(self: object, *, url: str, secret: str | None, payload: object) -> None:
        webhook_calls.append(secret)

    monkeypatch.setattr("ainrf.gates.manager.WebhookDispatcher.send", fake_send)
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
            gate_sweep_interval_seconds=60,
        )
    )
    app.state.gate_manager.register_secret("t-001", "runtime-secret")

    await app.state.gate_manager.sweep_overdue_gates()
    await app.state.gate_manager.sweep_overdue_gates()

    gate = store.load_artifact(ArtifactType.HUMAN_GATE, "g-intake-001")
    assert isinstance(gate, HumanGate)
    assert gate.reminder_sent_at is not None
    assert webhook_calls == ["runtime-secret"]
