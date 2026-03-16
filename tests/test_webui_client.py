from __future__ import annotations

import httpx
import pytest

from ainrf.api.config import hash_api_key
from ainrf.api.schemas import ApiStatus, TaskCreateRequest
from ainrf.artifacts import ResourceUsage
from ainrf.state import TaskMode
from ainrf.state import TaskStage
from ainrf.webui.client import (
    AinrfApiClient,
    ApiAuthenticationError,
    ApiConnectionError,
    ApiProtocolError,
)


def test_get_health_accepts_degraded_response() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            503,
            json={
                "status": "degraded",
                "state_root": ".ainrf",
                "container_configured": True,
                "container_health": {"ssh_ok": False},
                "detail": "Container connectivity degraded",
            },
        )
    )
    client = AinrfApiClient("http://ainrf.local", transport=transport)

    health = client.get_health()

    assert health.status is ApiStatus.DEGRADED
    assert health.detail == "Container connectivity degraded"


def test_list_tasks_requires_valid_api_key() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(401, json={"detail": "Unauthorized"}))
    client = AinrfApiClient("http://ainrf.local", api_key="wrong", transport=transport)

    with pytest.raises(ApiAuthenticationError):
        client.list_tasks()


def test_list_tasks_maps_request_errors_to_connection_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    client = AinrfApiClient("http://ainrf.local", api_key="secret", transport=httpx.MockTransport(handler))

    with pytest.raises(ApiConnectionError):
        client.list_tasks()


def test_list_tasks_validates_payload_shape() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"items": [{}]}))
    client = AinrfApiClient("http://ainrf.local", api_key="secret", transport=transport)

    with pytest.raises(ApiProtocolError):
        client.list_tasks()


def test_list_tasks_parses_response_and_passes_api_key() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["X-API-Key"] == "secret-key"
        assert request.url.params["status"] == TaskStage.PLANNING.value
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "task_id": "t-001",
                        "mode": "deep_reproduction",
                        "status": "planning",
                        "created_at": "2026-03-16T00:00:00Z",
                        "updated_at": "2026-03-16T00:00:00Z",
                        "current_stage": "planning",
                        "termination_reason": None,
                    }
                ]
            },
        )

    client = AinrfApiClient(
        "http://ainrf.local",
        api_key="secret-key",
        transport=httpx.MockTransport(handler),
    )

    task_list = client.list_tasks(TaskStage.PLANNING)

    assert len(task_list.items) == 1
    assert task_list.items[0].status is TaskStage.PLANNING


def test_get_task_parses_detail_payload() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            json={
                "task_id": "t-001",
                "mode": "deep_reproduction",
                "status": "gate_waiting",
                "created_at": "2026-03-16T00:00:00Z",
                "updated_at": "2026-03-16T00:00:00Z",
                "current_stage": "gate_waiting",
                "termination_reason": None,
                "budget_limit": {"gpu_hours": 1.0, "api_cost_usd": 2.0, "wall_clock_hours": 3.0},
                "budget_used": {"gpu_hours": 0.0, "api_cost_usd": 0.0, "wall_clock_hours": 0.0},
                "gates": [],
                "active_gate": None,
                "artifact_summary": {"counts": {}, "total": 0},
                "config": {},
            },
        )
    )
    client = AinrfApiClient("http://ainrf.local", api_key=hash_api_key("unused"), transport=transport)

    detail = client.get_task("t-001")

    assert detail.task_id == "t-001"
    assert detail.status is TaskStage.GATE_WAITING


def test_create_task_posts_validated_payload() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        payload = request.read().decode("utf-8")
        assert request.headers["X-API-Key"] == "secret-key"
        assert '"mode":"deep_reproduction"' in payload
        return httpx.Response(201, json={"task_id": "t-123", "status": "gate_waiting"})

    client = AinrfApiClient(
        "http://ainrf.local",
        api_key="secret-key",
        transport=httpx.MockTransport(handler),
    )
    request = TaskCreateRequest.model_validate(
        {
            "mode": TaskMode.DEEP_REPRODUCTION.value,
            "papers": [
                {
                    "title": "Paper",
                    "pdf_url": "https://example.com/paper.pdf",
                    "role": "target",
                }
            ],
            "config": {"mode_2": {"scope": "core-only", "baseline_first": True, "target_tables": []}},
            "container": {
                "host": "gpu-01",
                "port": 22,
                "user": "researcher",
                "project_dir": "/workspace/projects/demo",
            },
            "budget": ResourceUsage().model_dump(mode="json"),
            "yolo": False,
        }
    )

    response = client.create_task(request)

    assert response.task_id == "t-123"
    assert response.status is TaskStage.GATE_WAITING
