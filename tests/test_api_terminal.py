from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key


@pytest.mark.anyio
async def test_terminal_session_starts_idle(tmp_path: Path) -> None:
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/terminal/session", headers={"X-API-Key": "secret-key"})

    assert response.status_code == 200
    assert response.json()["status"] == "idle"
    assert response.json()["provider"] == "ttyd"
    assert response.json()["target_kind"] == "daemon-host"


@pytest.mark.anyio
async def test_terminal_session_requires_api_key(tmp_path: Path) -> None:
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/terminal/session")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_terminal_session_create_and_delete_round_trip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

    running = TerminalSessionRecord(
        session_id="term-1",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=utc_now(),
        started_at=utc_now(),
        terminal_url="http://127.0.0.1:7681",
    )

    monkeypatch.setattr("ainrf.api.routes.terminal.start_terminal_session", lambda app: running)
    monkeypatch.setattr("ainrf.api.routes.terminal.stop_terminal_session", lambda app: None)

    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        create_response = await client.post("/terminal/session", headers={"X-API-Key": "secret-key"})
        delete_response = await client.delete(
            "/terminal/session", headers={"X-API-Key": "secret-key"}
        )

    assert create_response.status_code == 200
    assert create_response.json()["status"] == "running"
    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "idle"
