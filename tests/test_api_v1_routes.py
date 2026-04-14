from __future__ import annotations

import threading
from pathlib import Path

import httpx
import pytest

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key


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


@pytest.mark.anyio
@pytest.mark.parametrize("path", ["/health", "/v1/health"])
async def test_health_routes_are_public(tmp_path: Path, path: str) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get(path)

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.anyio
async def test_openapi_registers_health_terminal_and_code_routes_and_removes_tasks(
    tmp_path: Path,
) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200
    payload = response.json()
    assert "/health" in payload["paths"]
    assert "/v1/health" in payload["paths"]
    assert "/terminal/session" in payload["paths"]
    assert "/v1/terminal/session" in payload["paths"]
    assert "/code/status" in payload["paths"]
    assert "/v1/code/status" in payload["paths"]
    assert "/tasks" not in payload["paths"]
    assert "/v1/tasks" not in payload["paths"]


@pytest.mark.anyio
async def test_lifespan_attaches_supervisor_and_runs_sync_hooks_off_event_loop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[tuple[str, int]] = []
    main_thread_id = threading.get_ident()

    class SupervisorSpy:
        def __init__(self, **_: object) -> None:
            self.started = False
            self.stopped = False

        def start(self) -> None:
            self.started = True
            events.append(("start", threading.get_ident()))

        def stop(self) -> None:
            self.stopped = True
            events.append(("stop", threading.get_ident()))

    monkeypatch.setattr("ainrf.api.app.CodeServerSupervisor", SupervisorSpy)
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )

    async with app.router.lifespan_context(app):
        supervisor = app.state.code_server_supervisor
        assert isinstance(supervisor, SupervisorSpy)
        assert supervisor.started is True
        assert supervisor.stopped is False

    assert supervisor.stopped is True
    assert events == [("start", events[0][1]), ("stop", events[1][1])]
    assert events[0][1] != main_thread_id
    assert events[1][1] != main_thread_id
