from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import httpx
import pytest
from fastapi import FastAPI

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key
from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now
from ainrf.terminal.pty import TerminalSessionRuntime


def _make_app(tmp_path: Path) -> FastAPI:
    return create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )


def test_terminal_session_record_uses_pty_fields() -> None:
    session = TerminalSessionRecord(
        session_id="term-1",
        provider="pty",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        terminal_ws_url="ws://testserver/terminal/session/term-1/ws?token=token-1",
        terminal_ws_token="token-1",
    )

    assert session.provider == "pty"
    assert session.terminal_ws_url == "ws://testserver/terminal/session/term-1/ws?token=token-1"
    assert session.terminal_ws_token == "token-1"


@pytest.mark.anyio
async def test_terminal_session_starts_idle(tmp_path: Path) -> None:
    app = _make_app(tmp_path)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/terminal/session", headers={"X-API-Key": "secret-key"})

    assert response.status_code == 200
    assert response.json()["status"] == "idle"
    assert response.json()["provider"] == "pty"
    assert response.json()["target_kind"] == "daemon-host"


@pytest.mark.anyio
async def test_terminal_session_requires_api_key(tmp_path: Path) -> None:
    app = _make_app(tmp_path)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/terminal/session")

    assert response.status_code == 401


@pytest.mark.anyio
async def test_terminal_session_create_uses_api_config_for_lifecycle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, object] = {}
    running = TerminalSessionRuntime(
        record=TerminalSessionRecord(
            session_id="term-1",
            provider="pty",
            target_kind="daemon-host",
            status=TerminalSessionStatus.RUNNING,
            created_at=utc_now(),
            started_at=utc_now(),
            terminal_ws_url="ws://testserver/terminal/session/term-1/ws?token=ws-token",
            pid=4321,
            terminal_ws_token="ws-token",
        ),
        process=cast(Any, object()),
        master_fd=11,
    )

    def fake_start_terminal_session(
        api_base_url: str,
        shell_command: tuple[str, ...],
        working_directory: Path,
    ) -> TerminalSessionRecord:
        captured["api_base_url"] = api_base_url
        captured["shell_command"] = shell_command
        captured["working_directory"] = working_directory
        return running

    monkeypatch.setattr(
        "ainrf.api.routes.terminal.start_terminal_session", fake_start_terminal_session
    )

    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
            terminal_command=("/bin/bash", "-lc", "pwd"),
        )
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.post("/terminal/session", headers={"X-API-Key": "secret-key"})

    assert response.status_code == 200
    assert captured == {
        "api_base_url": "http://testserver/",
        "shell_command": ("/bin/bash", "-lc", "pwd"),
        "working_directory": tmp_path,
    }
    assert app.state.terminal_runtime is not None
    assert (
        response.json()["terminal_ws_url"]
        == "ws://testserver/terminal/session/term-1/ws?token=ws-token"
    )


@pytest.mark.anyio
async def test_terminal_session_delete_stops_active_session(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    stopped = TerminalSessionRecord(
        session_id=None,
        provider="pty",
        target_kind="daemon-host",
        status=TerminalSessionStatus.IDLE,
        closed_at=utc_now(),
    )
    captured: dict[str, object] = {}

    runtime = object()

    def fake_stop_terminal_session(session: object) -> TerminalSessionRecord:
        captured["session"] = session
        return stopped

    monkeypatch.setattr(
        "ainrf.api.routes.terminal.stop_terminal_session", fake_stop_terminal_session
    )

    app = _make_app(tmp_path)
    app.state.terminal_runtime = runtime

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.delete("/terminal/session", headers={"X-API-Key": "secret-key"})

    assert response.status_code == 200
    assert captured["session"] is runtime
    assert app.state.terminal_runtime is None
    assert response.json()["status"] == "idle"
