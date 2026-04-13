from __future__ import annotations

from pathlib import Path
import signal

from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now
from ainrf.terminal.ttyd import (
    build_ttyd_command,
    start_ttyd_session,
    stop_ttyd_session,
    terminal_url,
)


def test_build_ttyd_command_uses_expected_flags(tmp_path: Path) -> None:
    command = build_ttyd_command(
        host="127.0.0.1",
        port=7681,
        credential="token:secret",
        shell_command=("/bin/sh",),
        working_directory=tmp_path,
    )

    assert command == [
        "ttyd",
        "--port",
        "7681",
        "--interface",
        "127.0.0.1",
        "--credential",
        "token:secret",
        "/bin/sh",
    ]
    assert getattr(command, "working_directory") == tmp_path.resolve()


def test_terminal_url_returns_local_http_address() -> None:
    assert terminal_url("127.0.0.1", 7681) == "http://127.0.0.1:7681"


def test_start_ttyd_session_launches_process_and_returns_running_record(
    tmp_path: Path, monkeypatch
) -> None:
    popen_calls: dict[str, object] = {}

    class DummyProcess:
        pid = 4321

    def fake_popen(*args, **kwargs):
        popen_calls["args"] = args
        popen_calls["kwargs"] = kwargs
        return DummyProcess()

    monkeypatch.setattr("ainrf.terminal.ttyd.subprocess.Popen", fake_popen)
    monkeypatch.setattr("ainrf.terminal.ttyd.uuid4", lambda: "session-1234")

    session = start_ttyd_session(
        host="127.0.0.1",
        port=7681,
        credential="token:secret",
        shell_command=("/bin/sh",),
        working_directory=tmp_path,
    )

    assert popen_calls["args"] == (
        [
            "ttyd",
            "--port",
            "7681",
            "--interface",
            "127.0.0.1",
            "--credential",
            "token:secret",
            "/bin/sh",
        ],
    )
    assert popen_calls["kwargs"] == {
        "cwd": tmp_path,
        "stdin": -3,
        "stdout": -3,
        "stderr": -3,
        "start_new_session": True,
        "text": False,
    }
    assert session.session_id == "session-1234"
    assert session.provider == "ttyd"
    assert session.target_kind == "daemon-host"
    assert session.status is TerminalSessionStatus.RUNNING
    assert session.created_at is not None
    assert session.started_at == session.created_at
    assert session.closed_at is None
    assert session.terminal_url == "http://127.0.0.1:7681"
    assert session.pid == 4321


def test_start_ttyd_session_creates_missing_working_directory(
    tmp_path: Path, monkeypatch
) -> None:
    popen_calls: dict[str, object] = {}
    working_directory = tmp_path / ".ainrf"

    class DummyProcess:
        pid = 4321

    def fake_popen(*args, **kwargs):
        popen_calls["args"] = args
        popen_calls["kwargs"] = kwargs
        return DummyProcess()

    monkeypatch.setattr("ainrf.terminal.ttyd.subprocess.Popen", fake_popen)
    monkeypatch.setattr("ainrf.terminal.ttyd.uuid4", lambda: "session-1234")

    assert working_directory.exists() is False

    session = start_ttyd_session(
        host="127.0.0.1",
        port=7681,
        credential="token:secret",
        shell_command=("/bin/sh",),
        working_directory=working_directory,
    )

    assert working_directory.is_dir()
    assert getattr(popen_calls["args"][0], "working_directory") == working_directory.resolve()
    assert popen_calls["kwargs"]["cwd"] == working_directory.resolve()
    assert session.session_id == "session-1234"
    assert session.status is TerminalSessionStatus.RUNNING


def test_stop_ttyd_session_terminates_pid_and_returns_idle_record(monkeypatch) -> None:
    kill_calls: list[tuple[int, int]] = []

    def fake_kill(pid: int, signal_value: int) -> None:
        kill_calls.append((pid, signal_value))

    monkeypatch.setattr("ainrf.terminal.ttyd.os.kill", fake_kill)

    running = TerminalSessionRecord(
        session_id="session-1234",
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=utc_now(),
        started_at=utc_now(),
        terminal_url="http://127.0.0.1:7681",
        pid=4321,
    )

    stopped = stop_ttyd_session(running)

    assert kill_calls == [(4321, signal.SIGTERM)]
    assert stopped.session_id is None
    assert stopped.provider == "ttyd"
    assert stopped.target_kind == "daemon-host"
    assert stopped.status is TerminalSessionStatus.IDLE
    assert stopped.closed_at is not None
    assert stopped.pid is None
    assert stopped.terminal_url is None
