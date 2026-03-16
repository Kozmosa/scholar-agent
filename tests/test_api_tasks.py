from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key
from ainrf.artifacts import ArtifactType, PaperCard, PaperCardStatus
from ainrf.state import JsonStateStore, TaskCheckpoint, TaskMode, TaskRecord, TaskStage


def make_client(tmp_path: Path) -> httpx.AsyncClient:
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    )


def auth_headers() -> dict[str, str]:
    return {"X-API-Key": "secret-key"}


def create_task_payload() -> dict[str, object]:
    return {
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
        "yolo": False,
    }


@pytest.mark.anyio
async def test_create_task_persists_submitted_record(tmp_path: Path) -> None:
    async with make_client(tmp_path) as client:
        response = await client.post("/tasks", headers=auth_headers(), json=create_task_payload())

    assert response.status_code == 201
    payload = response.json()
    task = JsonStateStore(tmp_path).load_task(payload["task_id"])
    assert task is not None
    assert task.status is TaskStage.SUBMITTED
    assert task.checkpoint.current_stage is TaskStage.SUBMITTED


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
async def test_get_task_returns_artifact_summary(tmp_path: Path) -> None:
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
        response = await client.get("/tasks/t-001", headers=auth_headers())

    assert response.status_code == 200
    assert response.json()["artifact_summary"]["counts"] == {ArtifactType.PAPER_CARD.value: 1}


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
async def test_cancel_task_updates_status(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.EXECUTING,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.EXECUTING),
        )
    )

    async with make_client(tmp_path) as client:
        response = await client.post("/tasks/t-001/cancel", headers=auth_headers())

    assert response.status_code == 200
    task = store.load_task("t-001")
    assert task is not None
    assert task.status is TaskStage.CANCELLED
    assert task.checkpoint.current_stage is TaskStage.CANCELLED


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
async def test_approve_reject_and_events_are_not_implemented_yet(tmp_path: Path) -> None:
    store = JsonStateStore(tmp_path)
    store.save_task(
        TaskRecord(
            task_id="t-001",
            mode=TaskMode.DEEP_REPRODUCTION,
            status=TaskStage.GATE_WAITING,
            checkpoint=TaskCheckpoint(current_stage=TaskStage.GATE_WAITING),
        )
    )

    async with make_client(tmp_path) as client:
        approve = await client.post("/tasks/t-001/approve", headers=auth_headers())
        reject = await client.post(
            "/tasks/t-001/reject",
            headers=auth_headers(),
            json={"feedback": "revise"},
        )
        events = await client.get("/tasks/t-001/events", headers=auth_headers())

    assert approve.status_code == 501
    assert reject.status_code == 501
    assert events.status_code == 501
