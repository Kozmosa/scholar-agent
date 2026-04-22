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


class DummyProcess:
    def __init__(self, returncode: int | None = None) -> None:
        self.pid = 4321
        self.returncode = returncode

    def poll(self) -> int | None:
        return self.returncode

    def wait(self, timeout: float) -> int:
        _ = timeout
        self.returncode = 0
        return 0


def _make_app(tmp_path: Path) -> FastAPI:
    return create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
            terminal_command=("/bin/bash", "-l"),
        )
    )


def _runtime_for(environment_id: str, environment_alias: str, target_kind: str) -> TerminalSessionRuntime:
    return TerminalSessionRuntime(
        record=TerminalSessionRecord(
            session_id=f"term-{environment_id}",
            provider="pty",
            target_kind=target_kind,
            status=TerminalSessionStatus.RUNNING,
            environment_id=environment_id,
            environment_alias=environment_alias,
            working_directory="/workspace/project",
            created_at=utc_now(),
            started_at=utc_now(),
            terminal_ws_url=f"ws://testserver/terminal/session/term-{environment_id}/ws?token=token",
            terminal_ws_token="token",
            pid=4321,
        ),
        process=cast(Any, DummyProcess()),
        master_fd=11,
    )


@pytest.mark.anyio
async def test_terminal_session_get_returns_idle_for_selected_environment(tmp_path: Path) -> None:
    app = _make_app(tmp_path)
    environment = app.state.environment_service.create_environment(
        alias="gpu-lab",
        display_name="GPU Lab",
        host="gpu.example.com",
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get(
            f"/terminal/session?environment_id={environment.id}",
            headers={"X-API-Key": "secret-key"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "session_id": None,
        "provider": "pty",
        "target_kind": "daemon-host",
        "environment_id": environment.id,
        "environment_alias": "gpu-lab",
        "working_directory": str(tmp_path),
        "status": "idle",
        "created_at": None,
        "started_at": None,
        "closed_at": None,
        "terminal_ws_url": None,
        "detail": None,
    }


@pytest.mark.anyio
async def test_terminal_session_post_uses_project_override_for_local_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, object] = {}
    running = _runtime_for("env-1", "gpu-lab", "environment-local")

    def fake_start_terminal_session(
        api_base_url: str,
        shell_command: tuple[str, ...],
        spawn_working_directory: Path,
        *,
        environment_id: str,
        environment_alias: str,
        working_directory: str | None,
        target_kind: str,
    ) -> TerminalSessionRuntime:
        captured["api_base_url"] = api_base_url
        captured["shell_command"] = shell_command
        captured["spawn_working_directory"] = spawn_working_directory
        captured["environment_id"] = environment_id
        captured["environment_alias"] = environment_alias
        captured["working_directory"] = working_directory
        captured["target_kind"] = target_kind
        return running

    monkeypatch.setattr("ainrf.api.routes.terminal.start_terminal_session", fake_start_terminal_session)

    app = _make_app(tmp_path)
    environment = app.state.environment_service.create_environment(
        alias="localhost-2",
        display_name="Localhost 2",
        host="127.0.0.1",
        default_workdir="/workspace/default",
    )
    app.state.environment_service.create_project_reference(
        project_id="default",
        environment_id=environment.id,
        override_workdir="/workspace/override",
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.post(
            "/terminal/session",
            headers={"X-API-Key": "secret-key"},
            json={"environment_id": environment.id},
        )

    assert response.status_code == 200
    assert captured == {
        "api_base_url": "http://testserver/",
        "shell_command": ("/bin/bash", "-l"),
        "spawn_working_directory": Path("/workspace/override"),
        "environment_id": environment.id,
        "environment_alias": "localhost-2",
        "working_directory": "/workspace/override",
        "target_kind": "environment-local",
    }


@pytest.mark.anyio
async def test_terminal_session_post_reuses_existing_session_for_same_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    app = _make_app(tmp_path)
    environment = app.state.environment_service.create_environment(
        alias="gpu-lab",
        display_name="GPU Lab",
        host="gpu.example.com",
    )
    app.state.terminal_runtime = _runtime_for(environment.id, environment.alias, "environment-ssh")

    monkeypatch.setattr(
        "ainrf.api.routes.terminal.start_terminal_session",
        lambda *args, **kwargs: pytest.fail("start_terminal_session should not be called"),
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.post(
            "/terminal/session",
            headers={"X-API-Key": "secret-key"},
            json={"environment_id": environment.id},
        )

    assert response.status_code == 200
    assert response.json()["status"] == "running"
    assert response.json()["environment_id"] == environment.id


@pytest.mark.anyio
async def test_terminal_session_post_replaces_existing_session_for_different_environment_and_builds_ssh_command(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, object] = {}
    stopped_runtime: list[object] = []
    running = _runtime_for("env-new", "remote-lab", "environment-ssh")

    def fake_start_terminal_session(
        api_base_url: str,
        shell_command: tuple[str, ...],
        spawn_working_directory: Path,
        *,
        environment_id: str,
        environment_alias: str,
        working_directory: str | None,
        target_kind: str,
    ) -> TerminalSessionRuntime:
        captured["api_base_url"] = api_base_url
        captured["shell_command"] = shell_command
        captured["spawn_working_directory"] = spawn_working_directory
        captured["environment_id"] = environment_id
        captured["environment_alias"] = environment_alias
        captured["working_directory"] = working_directory
        captured["target_kind"] = target_kind
        return running

    def fake_stop_terminal_session(runtime: object) -> TerminalSessionRecord:
        stopped_runtime.append(runtime)
        return TerminalSessionRecord(
            session_id=None,
            provider="pty",
            target_kind="daemon-host",
            status=TerminalSessionStatus.IDLE,
        )

    home_dir = tmp_path / "home"
    (home_dir / ".ssh").mkdir(parents=True)
    (home_dir / ".ssh" / "config").write_text("Host *\n", encoding="utf-8")
    monkeypatch.setattr("ainrf.api.routes.terminal.Path.home", lambda: home_dir)
    monkeypatch.setattr("ainrf.api.routes.terminal.start_terminal_session", fake_start_terminal_session)
    monkeypatch.setattr("ainrf.api.routes.terminal.stop_terminal_session", fake_stop_terminal_session)

    app = _make_app(tmp_path)
    old_environment = app.state.environment_service.create_environment(
        alias="old-lab",
        display_name="Old Lab",
        host="old.example.com",
    )
    old_runtime = _runtime_for(old_environment.id, old_environment.alias, "environment-ssh")
    app.state.terminal_runtime = old_runtime
    environment = app.state.environment_service.create_environment(
        alias="remote-lab",
        display_name="Remote Lab",
        host="gpu.example.com",
        port=2222,
        user="researcher",
        identity_file="/keys/id_ed25519",
        proxy_jump="bastion",
        proxy_command="ssh -W %h:%p bastion",
        ssh_options={"StrictHostKeyChecking": "no", "ServerAliveInterval": "30"},
        default_workdir="/workspace/project",
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.post(
            "/terminal/session",
            headers={"X-API-Key": "secret-key"},
            json={"environment_id": environment.id},
        )

    assert response.status_code == 200
    assert stopped_runtime == [old_runtime]
    assert captured["api_base_url"] == "http://testserver/"
    assert captured["spawn_working_directory"] == tmp_path
    assert captured["environment_id"] == environment.id
    assert captured["environment_alias"] == "remote-lab"
    assert captured["working_directory"] == "/workspace/project"
    assert captured["target_kind"] == "environment-ssh"
    assert captured["shell_command"] == (
        "ssh",
        "-tt",
        "-F",
        str(home_dir / ".ssh" / "config"),
        "-p",
        "2222",
        "-i",
        "/keys/id_ed25519",
        "-o",
        "ProxyJump=bastion",
        "-o",
        "ProxyCommand=ssh -W %h:%p bastion",
        "-o",
        "ServerAliveInterval=30",
        "-o",
        "StrictHostKeyChecking=no",
        "researcher@gpu.example.com",
        "cd /workspace/project && exec ${SHELL:-/bin/bash} -l",
    )


@pytest.mark.anyio
async def test_terminal_session_post_returns_404_for_missing_environment(tmp_path: Path) -> None:
    app = _make_app(tmp_path)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.post(
            "/terminal/session",
            headers={"X-API-Key": "secret-key"},
            json={"environment_id": "missing"},
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Environment not found"}
