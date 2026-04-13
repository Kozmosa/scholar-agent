from __future__ import annotations

import os
import signal
import subprocess
from pathlib import Path
from uuid import uuid4

from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now


class TtydCommand(list[str]):
    def __init__(self, args: list[str], working_directory: Path) -> None:
        super().__init__(args)
        self.working_directory = working_directory.resolve(strict=True)


def build_ttyd_command(
    host: str,
    port: int,
    credential: str,
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
            "--credential",
            credential,
            *shell_command,
        ],
        working_directory=working_directory,
    )


def terminal_url(host: str, port: int) -> str:
    return f"http://{host}:{port}"


def start_ttyd_session(
    host: str,
    port: int,
    credential: str,
    shell_command: tuple[str, ...],
    working_directory: Path,
) -> TerminalSessionRecord:
    command = build_ttyd_command(
        host=host,
        port=port,
        credential=credential,
        shell_command=shell_command,
        working_directory=working_directory,
    )
    process = subprocess.Popen(
        command,
        cwd=working_directory,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        text=False,
    )
    started_at = utc_now()
    return TerminalSessionRecord(
        session_id=str(uuid4()),
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.RUNNING,
        created_at=started_at,
        started_at=started_at,
        terminal_url=terminal_url(host, port),
        pid=process.pid,
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
    )
