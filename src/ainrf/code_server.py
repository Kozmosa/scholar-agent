from __future__ import annotations

import os
import signal
import subprocess
import time
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import httpx


class CodeServerLifecycleStatus(StrEnum):
    STARTING = "starting"
    READY = "ready"
    UNAVAILABLE = "unavailable"


@dataclass(slots=True)
class CodeServerState:
    status: CodeServerLifecycleStatus
    workspace_dir: Path | None = None
    detail: str | None = None
    pid: int | None = None


def build_code_server_command(host: str, port: int, workspace_dir: Path) -> list[str]:
    return [
        "code-server",
        "--bind-addr",
        f"{host}:{port}",
        "--auth",
        "none",
        str(workspace_dir),
    ]


def _wait_until_ready(host: str, port: int, timeout_seconds: float = 10.0) -> bool:
    deadline = time.monotonic() + timeout_seconds
    url = f"http://{host}:{port}/"
    while time.monotonic() < deadline:
        try:
            response = httpx.get(url, timeout=1.0, follow_redirects=False)
            if response.status_code in {200, 302, 401, 403}:
                return True
        except httpx.HTTPError:
            time.sleep(0.2)
            continue
        time.sleep(0.2)
    return False


def _terminate_process(pid: int) -> None:
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return


class CodeServerSupervisor:
    def __init__(self, host: str, port: int, workspace_dir: Path | None, state_root: Path) -> None:
        self._host = host
        self._port = port
        self._workspace_dir = workspace_dir
        self._state_root = state_root
        self._process: subprocess.Popen[str] | None = None
        self._state = CodeServerState(
            status=CodeServerLifecycleStatus.UNAVAILABLE,
            workspace_dir=workspace_dir,
            detail="code-server not started",
        )

    def start(self) -> None:
        if self._workspace_dir is None:
            self._state = CodeServerState(
                status=CodeServerLifecycleStatus.UNAVAILABLE,
                workspace_dir=None,
                detail="workspace directory is not configured",
            )
            return
        if not self._workspace_dir.exists():
            self._state = CodeServerState(
                status=CodeServerLifecycleStatus.UNAVAILABLE,
                workspace_dir=self._workspace_dir,
                detail=f"workspace directory does not exist: {self._workspace_dir}",
            )
            return
        self._state = CodeServerState(
            status=CodeServerLifecycleStatus.STARTING,
            workspace_dir=self._workspace_dir,
            detail=None,
        )
        runtime_dir = self._state_root / "runtime"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        log_file = runtime_dir / "code-server.log"
        with log_file.open("a", encoding="utf-8") as handle:
            process = subprocess.Popen(
                build_code_server_command(self._host, self._port, self._workspace_dir),
                stdin=subprocess.DEVNULL,
                stdout=handle,
                stderr=handle,
                start_new_session=True,
                text=True,
            )
        self._process = process
        if _wait_until_ready(self._host, self._port):
            self._state = CodeServerState(
                status=CodeServerLifecycleStatus.READY,
                workspace_dir=self._workspace_dir,
                detail=None,
                pid=process.pid,
            )
            return
        _terminate_process(process.pid)
        self._process = None
        self._state = CodeServerState(
            status=CodeServerLifecycleStatus.UNAVAILABLE,
            workspace_dir=self._workspace_dir,
            detail=f"code-server failed to become ready on {self._host}:{self._port}",
        )

    def status(self) -> CodeServerState:
        return self._state

    def stop(self) -> None:
        if self._process is not None:
            _terminate_process(self._process.pid)
            self._process = None
        self._state = CodeServerState(
            status=CodeServerLifecycleStatus.UNAVAILABLE,
            workspace_dir=self._workspace_dir,
            detail="code-server stopped",
        )
