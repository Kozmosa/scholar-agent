from __future__ import annotations

import json
import os
import signal
from pathlib import Path
from typing import Any, cast
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key
from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now
from ainrf.terminal.pty import (
    TerminalSessionRuntime,
    build_terminal_ws_url,
    start_terminal_session,
    stop_terminal_session,
)


def make_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[TestClient, FastAPI]:
    monkeypatch.setattr("ainrf.code_server.CodeServerSupervisor.start", lambda self: None)
    monkeypatch.setattr("ainrf.code_server.CodeServerSupervisor.stop", lambda self: None)
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )
    return TestClient(app), app


def test_build_terminal_ws_url_translates_http_base() -> None:
    assert build_terminal_ws_url("http://testserver", "term-1", "token-1") == (
        "ws://testserver/terminal/session/term-1/ws?token=token-1"
    )


def test_start_terminal_session_launches_process_and_returns_ws_url(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict[str, object] = {}

    class DummyProcess:
        pid = 4321

    def fake_popen(*args: object, **kwargs: object) -> DummyProcess:
        captured["args"] = args
        captured["kwargs"] = kwargs
        return DummyProcess()

    monkeypatch.setattr("ainrf.terminal.pty.os.openpty", lambda: (11, 12))
    monkeypatch.setattr("ainrf.terminal.pty.subprocess.Popen", fake_popen)
    monkeypatch.setattr("ainrf.terminal.pty.uuid4", lambda: UUID(int=1))
    monkeypatch.setattr("ainrf.terminal.pty.token_urlsafe", lambda length: "token-1")

    runtime = start_terminal_session(
        api_base_url="http://testserver",
        shell_command=("/bin/sh",),
        working_directory=tmp_path,
    )

    assert captured["args"] == (["/bin/sh"],)
    assert captured["kwargs"] == {
        "stdin": 12,
        "stdout": 12,
        "stderr": 12,
        "cwd": tmp_path.resolve(),
        "start_new_session": True,
        "text": False,
        "close_fds": True,
    }
    assert runtime.record.session_id == "00000000-0000-0000-0000-000000000001"
    assert runtime.record.status is TerminalSessionStatus.RUNNING
    assert runtime.record.terminal_ws_url == (
        "ws://testserver/terminal/session/00000000-0000-0000-0000-000000000001/ws?token=token-1"
    )
    assert runtime.record.terminal_ws_token == "token-1"
    assert runtime.record.pid == 4321


def test_stop_terminal_session_terminates_running_process(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    kill_calls: list[tuple[int, int]] = []

    def fake_killpg(pid: int, signum: int) -> None:
        kill_calls.append((pid, signum))

    class DummyProcess:
        pid = 4321
        returncode: int | None = None

        def poll(self) -> int | None:
            return self.returncode

        def wait(self, timeout: float) -> int:
            self.returncode = 0
            return 0

    monkeypatch.setattr("ainrf.terminal.pty.os.killpg", fake_killpg)
    monkeypatch.setattr("ainrf.terminal.pty.os.close", lambda fd: None)
    runtime = TerminalSessionRuntime(
        record=TerminalSessionRecord(
            session_id="term-1",
            provider="pty",
            target_kind="daemon-host",
            status=TerminalSessionStatus.RUNNING,
            created_at=utc_now(),
            started_at=utc_now(),
            terminal_ws_url="ws://testserver/terminal/session/term-1/ws?token=token-1",
            pid=4321,
            terminal_ws_token="token-1",
        ),
        process=cast(Any, DummyProcess()),
        master_fd=10,
    )

    stopped = stop_terminal_session(runtime)

    assert kill_calls == [(4321, signal.SIGTERM)]
    assert stopped.status is TerminalSessionStatus.IDLE
    assert stopped.session_id is None
    assert stopped.terminal_ws_url is None


def test_terminal_session_routes_and_websocket_bridge(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client, app = make_client(tmp_path, monkeypatch)
    input_calls: list[str] = []
    resize_calls: list[tuple[int, int]] = []

    monkeypatch.setattr(
        "ainrf.api.routes.terminal.write_terminal_input",
        lambda runtime, data: input_calls.append(data),
    )
    monkeypatch.setattr(
        "ainrf.api.routes.terminal.resize_terminal",
        lambda runtime, cols, rows: resize_calls.append((cols, rows)),
    )

    read_fd, write_fd = os.pipe()

    class DummyProcess:
        pid = 4321
        returncode: int | None = None

        def poll(self) -> int | None:
            return self.returncode

        def wait(self, timeout: float) -> int:
            self.returncode = 0
            return 0

    runtime = TerminalSessionRuntime(
        record=TerminalSessionRecord(
            session_id="term-1",
            provider="pty",
            target_kind="daemon-host",
            status=TerminalSessionStatus.RUNNING,
            created_at=utc_now(),
            started_at=utc_now(),
            terminal_ws_url="ws://testserver/terminal/session/term-1/ws?token=token-1",
            pid=4321,
            terminal_ws_token="token-1",
        ),
        process=cast(Any, DummyProcess()),
        master_fd=read_fd,
    )

    app.state.terminal_runtime = runtime

    with client.websocket_connect("/terminal/session/term-1/ws?token=token-1") as ws:
        os.write(write_fd, b"hello from pty\n")
        assert ws.receive_json() == {"type": "output", "data": "hello from pty\n"}

        ws.send_text(json.dumps({"type": "input", "data": "ls\n"}))
        ws.send_text(json.dumps({"type": "resize", "cols": 120, "rows": 40}))

        assert input_calls == ["ls\n"]
        assert resize_calls == [(120, 40)]

    os.close(write_fd)


def test_terminal_session_websocket_rejects_bad_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client, app = make_client(tmp_path, monkeypatch)

    class DummyProcess:
        pid = 4321
        returncode: int | None = None

        def poll(self) -> int | None:
            return self.returncode

        def wait(self, timeout: float) -> int:
            self.returncode = 0
            return 0

    runtime = TerminalSessionRuntime(
        record=TerminalSessionRecord(
            session_id="term-1",
            provider="pty",
            target_kind="daemon-host",
            status=TerminalSessionStatus.RUNNING,
            created_at=utc_now(),
            started_at=utc_now(),
            terminal_ws_url="ws://testserver/terminal/session/term-1/ws?token=token-1",
            pid=4321,
            terminal_ws_token="token-1",
        ),
        process=cast(Any, DummyProcess()),
        master_fd=11,
    )

    app.state.terminal_runtime = runtime

    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/terminal/session/term-1/ws?token=wrong-token") as ws:
            ws.receive_text()
