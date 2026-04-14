from __future__ import annotations

import os
import signal
import subprocess
from datetime import timedelta
from pathlib import Path
from secrets import token_urlsafe
from urllib.parse import urlencode
from uuid import uuid4

from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

BROWSER_OPEN_TOKEN_TTL = timedelta(minutes=5)
VIEWER_COOKIE_NAME = "ainrf_terminal_viewer"
DEFAULT_TTYD_AUTH_HEADER = "X-AINRF-Terminal-Auth"


class TtydCommand(list[str]):
    def __init__(self, args: list[str], working_directory: Path) -> None:
        super().__init__(args)
        self.working_directory = working_directory.resolve(strict=True)


def build_ttyd_command(
    host: str,
    port: int,
    auth_header_name: str,
    shell_command: tuple[str, ...],
    working_directory: Path,
) -> TtydCommand:
    return TtydCommand(
        [
            "ttyd",
            "--port",
            str(port),
            "--interface",
            host,
            "--auth-header",
            auth_header_name,
            *shell_command,
        ],
        working_directory=working_directory,
    )


def terminal_url(host: str, port: int) -> str:
    return f"http://{host}:{port}"


def browser_open_url(api_base_url: str, session_id: str, token: str) -> str:
    query = urlencode({"token": token})
    normalized_base = api_base_url.rstrip("/")
    return f"{normalized_base}/terminal/session/{session_id}/open?{query}"


def start_ttyd_session(
    host: str,
    port: int,
    auth_header_name: str,
    shell_command: tuple[str, ...],
    working_directory: Path,
    api_base_url: str,
) -> TerminalSessionRecord:
    working_directory.mkdir(parents=True, exist_ok=True)
    normalized_working_directory = working_directory.resolve(strict=True)
    command = build_ttyd_command(
        host=host,
        port=port,
        auth_header_name=auth_header_name,
        shell_command=shell_command,
        working_directory=normalized_working_directory,
    )
    process = subprocess.Popen(
        command,
        cwd=normalized_working_directory,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        text=False,
    )
    started_at = utc_now()
    session_id = str(uuid4())
    browser_open_token = token_urlsafe(24)
    return TerminalSessionRecord(
        session_id=session_id,
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=started_at,
        started_at=started_at,
        terminal_url=browser_open_url(api_base_url, session_id, browser_open_token),
        detail=None,
        pid=process.pid,
        browser_open_token=browser_open_token,
        browser_open_expires_at=started_at + BROWSER_OPEN_TOKEN_TTL,
        browser_open_consumed_at=None,
        viewer_session_token=None,
        viewer_session_expires_at=None,
        viewer_cookie_name=VIEWER_COOKIE_NAME,
    )


def stop_ttyd_session(session: TerminalSessionRecord | None) -> TerminalSessionRecord:
    if session is not None and session.pid is not None:
        os.kill(session.pid, signal.SIGTERM)
    return TerminalSessionRecord(
        session_id=None,
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.IDLE,
        closed_at=utc_now(),
        pid=None,
        browser_open_token=None,
        browser_open_expires_at=None,
        browser_open_consumed_at=None,
        viewer_session_token=None,
        viewer_session_expires_at=None,
        viewer_cookie_name=VIEWER_COOKIE_NAME,
    )
