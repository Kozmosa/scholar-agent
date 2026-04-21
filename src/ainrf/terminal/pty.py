from __future__ import annotations

import errno
import os
import signal
import struct
import subprocess
import termios
from dataclasses import dataclass, replace
from datetime import timedelta
from pathlib import Path
from secrets import token_urlsafe
from uuid import uuid4
from typing import Any

from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus, utc_now

TERMINAL_PROVIDER = "pty"
TERMINAL_TARGET_KIND = "daemon-host"
TERMINAL_WS_TOKEN_TTL = timedelta(minutes=30)
_TERMINAL_READ_SIZE = 4096
_TERMINAL_CLOSE_TIMEOUT_SECONDS = 5.0


@dataclass(slots=True)
class TerminalSessionRuntime:
    record: TerminalSessionRecord
    process: subprocess.Popen[Any]
    master_fd: int | None


def _to_websocket_base(api_base_url: str) -> str:
    normalized = api_base_url.rstrip("/")
    if normalized.startswith("https://"):
        return "wss://" + normalized.removeprefix("https://")
    if normalized.startswith("http://"):
        return "ws://" + normalized.removeprefix("http://")
    return normalized


def build_terminal_ws_url(api_base_url: str, session_id: str, token: str) -> str:
    websocket_base = _to_websocket_base(api_base_url)
    return f"{websocket_base}/terminal/session/{session_id}/ws?token={token}"


def _close_master_fd(master_fd: int | None) -> None:
    if master_fd is None:
        return
    try:
        os.close(master_fd)
    except OSError:
        pass


def _spawn_terminal_process(
    shell_command: tuple[str, ...],
    working_directory: Path,
) -> tuple[subprocess.Popen[Any], int]:
    master_fd, slave_fd = os.openpty()
    try:
        process = subprocess.Popen(
            list(shell_command),
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            cwd=working_directory,
            start_new_session=True,
            text=False,
            close_fds=True,
        )
    except Exception:
        _close_master_fd(master_fd)
        _close_master_fd(slave_fd)
        raise
    finally:
        _close_master_fd(slave_fd)

    os.set_blocking(master_fd, False)
    return process, master_fd


def start_terminal_session(
    api_base_url: str,
    shell_command: tuple[str, ...],
    working_directory: Path,
) -> TerminalSessionRuntime:
    working_directory.mkdir(parents=True, exist_ok=True)
    normalized_working_directory = working_directory.resolve(strict=True)
    process, master_fd = _spawn_terminal_process(shell_command, normalized_working_directory)
    started_at = utc_now()
    session_id = str(uuid4())
    ws_token = token_urlsafe(24)
    record = TerminalSessionRecord(
        session_id=session_id,
        provider=TERMINAL_PROVIDER,
        target_kind=TERMINAL_TARGET_KIND,
        status=TerminalSessionStatus.RUNNING,
        created_at=started_at,
        started_at=started_at,
        terminal_ws_url=build_terminal_ws_url(api_base_url, session_id, ws_token),
        detail=None,
        pid=process.pid,
        terminal_ws_token=ws_token,
    )
    return TerminalSessionRuntime(record=record, process=process, master_fd=master_fd)


def _mark_failed(runtime: TerminalSessionRuntime, close_fd: bool) -> TerminalSessionRecord:
    if runtime.record.status is TerminalSessionStatus.FAILED:
        return runtime.record

    return_code = runtime.process.returncode
    detail = (
        f"Terminal session exited with code {return_code}"
        if return_code is not None
        else "Terminal session exited unexpectedly"
    )
    if close_fd:
        _close_master_fd(runtime.master_fd)
        runtime.master_fd = None

    runtime.record = replace(
        runtime.record,
        status=TerminalSessionStatus.FAILED,
        closed_at=utc_now(),
        terminal_ws_url=None,
        detail=detail,
    )
    return runtime.record


def refresh_terminal_session(
    runtime: TerminalSessionRuntime,
    *,
    close_fd: bool = True,
) -> TerminalSessionRecord:
    if runtime.process.poll() is None:
        return runtime.record
    return _mark_failed(runtime, close_fd=close_fd)


def stop_terminal_session(runtime: TerminalSessionRuntime | None) -> TerminalSessionRecord:
    if runtime is None:
        return TerminalSessionRecord(
            session_id=None,
            provider=TERMINAL_PROVIDER,
            target_kind=TERMINAL_TARGET_KIND,
            status=TerminalSessionStatus.IDLE,
            closed_at=utc_now(),
        )

    _close_master_fd(runtime.master_fd)
    runtime.master_fd = None

    if runtime.process.poll() is None:
        try:
            os.killpg(runtime.process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            runtime.process.wait(timeout=_TERMINAL_CLOSE_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(runtime.process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            runtime.process.wait(timeout=_TERMINAL_CLOSE_TIMEOUT_SECONDS)

    runtime.record = TerminalSessionRecord(
        session_id=None,
        provider=TERMINAL_PROVIDER,
        target_kind=TERMINAL_TARGET_KIND,
        status=TerminalSessionStatus.IDLE,
        closed_at=utc_now(),
    )
    return runtime.record


def write_terminal_input(runtime: TerminalSessionRuntime, data: str) -> None:
    if runtime.master_fd is None:
        return
    os.write(runtime.master_fd, data.encode("utf-8"))


def resize_terminal(runtime: TerminalSessionRuntime, cols: int, rows: int) -> None:
    if runtime.master_fd is None:
        return
    packed = struct.pack("HHHH", rows, cols, 0, 0)
    try:
        import fcntl

        fcntl.ioctl(runtime.master_fd, termios.TIOCSWINSZ, packed)
    except OSError as exc:
        if exc.errno not in {errno.EIO, errno.EBADF}:
            raise
