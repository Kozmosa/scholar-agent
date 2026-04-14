from __future__ import annotations

from datetime import timedelta
from pathlib import Path
import signal

from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now
from ainrf.terminal.ttyd import (
    BROWSER_OPEN_TOKEN_TTL,
    VIEWER_COOKIE_NAME,
    browser_open_url,
    build_ttyd_command,
    start_ttyd_session,
    stop_ttyd_session,
    terminal_url,
)


def test_build_ttyd_command_uses_auth_header_mode(tmp_path: Path) -> None:
    command = build_ttyd_command(
        host="127.0.0.1",
        port=7681,
        auth_header_name="X-AINRF-Terminal-Auth",
        shell_command=("/bin/sh",),
        working_directory=tmp_path,
    )

    assert command == [
        "ttyd",
        "--port",
        "7681",
        "--interface",
        "127.0.0.1",
        "--auth-header",
        "X-AINRF-Terminal-Auth",
        "/bin/sh",
    ]
    assert getattr(command, "working_directory") == tmp_path.resolve()


def test_terminal_url_returns_local_http_address() -> None:
    assert terminal_url("127.0.0.1", 7681) == "http://127.0.0.1:7681"


def test_browser_open_url_points_to_backend_open_route() -> None:
    assert browser_open_url("http://testserver", "term-1", "open-token") == (
        "http://testserver/terminal/session/term-1/open?token=open-token"
    )


def test_start_ttyd_session_launches_process_and_returns_mediated_record(
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
    monkeypatch.setattr("ainrf.terminal.ttyd.token_urlsafe", lambda length: "open-token")

    session = start_ttyd_session(
        host="127.0.0.1",
        port=7681,
        auth_header_name="X-AINRF-Terminal-Auth",
        shell_command=("/bin/sh",),
        working_directory=tmp_path,
        api_base_url="http://testserver",
    )

    assert popen_calls["args"] == (
        [
            "ttyd",
            "--port",
            "7681",
            "--interface",
            "127.0.0.1",
            "--auth-header",
            "X-AINRF-Terminal-Auth",
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
    assert session.status is TerminalSessionStatus.RUNNING
    assert session.terminal_url == "http://testserver/terminal/session/session-1234/open?token=open-token"
    assert session.browser_open_token == "open-token"
    assert session.viewer_session_token is None
    assert session.viewer_cookie_name == VIEWER_COOKIE_NAME
    assert session.browser_open_expires_at == session.started_at + BROWSER_OPEN_TOKEN_TTL


def test_start_ttyd_session_creates_missing_working_directory(tmp_path: Path, monkeypatch) -> None:
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
    monkeypatch.setattr("ainrf.terminal.ttyd.token_urlsafe", lambda length: "open-token")

    session = start_ttyd_session(
        host="127.0.0.1",
        port=7681,
        auth_header_name="X-AINRF-Terminal-Auth",
        shell_command=("/bin/sh",),
        working_directory=working_directory,
        api_base_url="http://testserver",
    )

    assert working_directory.is_dir()
    assert getattr(popen_calls["args"][0], "working_directory") == working_directory.resolve()
    assert popen_calls["kwargs"]["cwd"] == working_directory.resolve()
    assert session.session_id == "session-1234"
    assert session.browser_open_token == "open-token"


def test_stop_ttyd_session_terminates_pid_and_clears_browser_state(monkeypatch) -> None:
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
        terminal_url="http://testserver/terminal/session/session-1234/open?token=open-token",
        pid=4321,
        browser_open_token="open-token",
        browser_open_expires_at=utc_now() + timedelta(minutes=5),
        viewer_session_token="viewer-token",
        viewer_session_expires_at=utc_now() + timedelta(minutes=30),
        viewer_cookie_name=VIEWER_COOKIE_NAME,
    )

    stopped = stop_ttyd_session(running)

    assert kill_calls == [(4321, signal.SIGTERM)]
    assert stopped.session_id is None
    assert stopped.status is TerminalSessionStatus.IDLE
    assert stopped.terminal_url is None
    assert stopped.browser_open_token is None
    assert stopped.viewer_session_token is None
    assert stopped.viewer_cookie_name == VIEWER_COOKIE_NAME
