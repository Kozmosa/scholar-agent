from __future__ import annotations

import asyncio
import errno
import json
import os
import shlex
from contextlib import suppress
from functools import partial
from pathlib import Path
from typing import Any

from anyio import create_task_group, to_thread
from fastapi import APIRouter, HTTPException, Query, Request, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from ainrf.api.schemas import (
    TerminalSessionCreateRequest,
    TerminalSessionResponse,
    TerminalSessionStatus,
)
from ainrf.environments import EnvironmentNotFoundError, InMemoryEnvironmentService
from ainrf.environments.models import EnvironmentRegistryEntry
from ainrf.terminal.models import TerminalSessionRecord, TerminalSessionStatus as RuntimeStatus
from ainrf.terminal.pty import (
    TERMINAL_IDLE_TARGET_KIND,
    TERMINAL_LOCAL_TARGET_KIND,
    TERMINAL_SSH_TARGET_KIND,
    TerminalSessionRuntime,
    refresh_terminal_session,
    resize_terminal,
    start_terminal_session,
    stop_terminal_session,
    write_terminal_input,
)

router = APIRouter(prefix="/terminal", tags=["terminal"])
_DEFAULT_PROJECT_ID = "default"
_LOCAL_HOSTS = {"127.0.0.1", "localhost"}


def _serialize_session(
    session: TerminalSessionRecord,
) -> dict[str, str | None | TerminalSessionStatus]:
    return {
        "session_id": session.session_id,
        "provider": session.provider,
        "target_kind": session.target_kind,
        "environment_id": session.environment_id,
        "environment_alias": session.environment_alias,
        "working_directory": session.working_directory,
        "status": session.status,
        "created_at": session.created_at.isoformat() if session.created_at else None,
        "started_at": session.started_at.isoformat() if session.started_at else None,
        "closed_at": session.closed_at.isoformat() if session.closed_at else None,
        "terminal_ws_url": session.terminal_ws_url,
        "detail": session.detail,
    }


def _get_environment_service(request: Request | WebSocket) -> InMemoryEnvironmentService:
    service = getattr(request.app.state, "environment_service", None)
    if service is None:
        raise HTTPException(status_code=500, detail="environment service not initialized")
    return service


def _translate_environment_error(exc: Exception) -> HTTPException:
    if isinstance(exc, EnvironmentNotFoundError):
        return HTTPException(status_code=404, detail="Environment not found")
    return HTTPException(status_code=500, detail="Unexpected terminal environment error")


def _idle_session(
    environment: EnvironmentRegistryEntry | None = None,
    working_directory: str | None = None,
) -> TerminalSessionRecord:
    return TerminalSessionRecord(
        session_id=None,
        provider="pty",
        target_kind=TERMINAL_IDLE_TARGET_KIND,
        environment_id=environment.id if environment is not None else None,
        environment_alias=environment.alias if environment is not None else None,
        working_directory=working_directory,
        status=RuntimeStatus.IDLE,
    )


def get_terminal_runtime(app: Any) -> TerminalSessionRuntime | None:
    return getattr(app.state, "terminal_runtime", None)


def _is_local_environment(environment: EnvironmentRegistryEntry) -> bool:
    return (
        environment.host in _LOCAL_HOSTS
        and environment.proxy_jump is None
        and environment.proxy_command is None
    )


def _resolve_local_spawn_directory(working_directory: str, state_root: Path) -> Path:
    candidate = Path(working_directory).expanduser()
    if candidate.is_absolute():
        return candidate
    return state_root / candidate


def _build_remote_shell_command(working_directory: str | None) -> str:
    if working_directory:
        return f"cd {shlex.quote(working_directory)} && exec ${{SHELL:-/bin/bash}} -l"
    return "exec ${SHELL:-/bin/bash} -l"


def _build_remote_terminal_command(
    environment: EnvironmentRegistryEntry,
    working_directory: str | None,
) -> tuple[str, ...]:
    command: list[str] = ["ssh", "-tt"]
    ssh_config_path = Path.home() / ".ssh" / "config"
    if ssh_config_path.exists():
        command.extend(["-F", str(ssh_config_path)])
    if environment.port:
        command.extend(["-p", str(environment.port)])
    if environment.identity_file:
        command.extend(["-i", environment.identity_file])
    if environment.proxy_jump:
        command.extend(["-o", f"ProxyJump={environment.proxy_jump}"])
    if environment.proxy_command:
        command.extend(["-o", f"ProxyCommand={environment.proxy_command}"])
    for key, value in sorted(environment.ssh_options.items()):
        command.extend(["-o", f"{key}={value}"])
    command.append(f"{environment.user}@{environment.host}")
    command.append(_build_remote_shell_command(working_directory))
    return tuple(command)


def _get_environment_context(
    service: InMemoryEnvironmentService,
    environment_id: str | None,
    state_root: Path,
) -> tuple[EnvironmentRegistryEntry | None, str | None]:
    if environment_id is None:
        return None, None
    environment = service.get_environment(environment_id)
    working_directory = service.resolve_effective_workdir(
        _DEFAULT_PROJECT_ID,
        environment_id,
        state_root,
    )
    return environment, working_directory


def get_terminal_session(
    app: Any,
    environment: EnvironmentRegistryEntry | None = None,
    working_directory: str | None = None,
) -> TerminalSessionRecord:
    runtime = get_terminal_runtime(app)
    if runtime is None:
        return _idle_session(environment, working_directory)
    session = refresh_terminal_session(runtime)
    if environment is not None and session.environment_id != environment.id:
        return _idle_session(environment, working_directory)
    return session


async def _stop_existing_runtime(runtime: TerminalSessionRuntime | None) -> None:
    if runtime is None:
        return
    await to_thread.run_sync(stop_terminal_session, runtime)


@router.get("/session", response_model=TerminalSessionResponse)
async def read_terminal_session(
    request: Request,
    environment_id: str | None = Query(default=None),
) -> TerminalSessionResponse:
    service = _get_environment_service(request)
    try:
        environment, working_directory = _get_environment_context(
            service,
            environment_id,
            request.app.state.api_config.state_root,
        )
    except Exception as exc:
        raise _translate_environment_error(exc) from exc

    session = get_terminal_session(request.app, environment, working_directory)
    return TerminalSessionResponse.model_validate(_serialize_session(session))


@router.post("/session", response_model=TerminalSessionResponse)
async def create_terminal_session(
    payload: TerminalSessionCreateRequest,
    request: Request,
) -> TerminalSessionResponse:
    service = _get_environment_service(request)
    config = request.app.state.api_config
    try:
        environment, working_directory = _get_environment_context(
            service,
            payload.environment_id,
            config.state_root,
        )
    except Exception as exc:
        raise _translate_environment_error(exc) from exc
    assert environment is not None
    assert working_directory is not None

    existing_runtime = get_terminal_runtime(request.app)
    if existing_runtime is not None:
        existing_record = refresh_terminal_session(existing_runtime)
        if (
            existing_record.environment_id == environment.id
            and existing_record.status is RuntimeStatus.RUNNING
        ):
            return TerminalSessionResponse.model_validate(_serialize_session(existing_record))
        await _stop_existing_runtime(existing_runtime)
        request.app.state.terminal_runtime = None

    if _is_local_environment(environment):
        shell_command = config.terminal_command
        spawn_working_directory = _resolve_local_spawn_directory(working_directory, config.state_root)
        target_kind = TERMINAL_LOCAL_TARGET_KIND
    else:
        shell_command = _build_remote_terminal_command(environment, working_directory)
        spawn_working_directory = config.state_root
        target_kind = TERMINAL_SSH_TARGET_KIND

    runtime = await to_thread.run_sync(
        partial(
            start_terminal_session,
            str(request.base_url),
            shell_command,
            spawn_working_directory,
            environment_id=environment.id,
            environment_alias=environment.alias,
            working_directory=working_directory,
            target_kind=target_kind,
        )
    )
    request.app.state.terminal_runtime = runtime
    return TerminalSessionResponse.model_validate(_serialize_session(runtime.record))


def _close_code_for_session_state(status: int) -> int:
    if status == 404:
        return 4404
    if status == 401:
        return 4401
    return 4409


def _get_active_runtime(session_id: str, token: str, app: object) -> TerminalSessionRuntime:
    runtime = get_terminal_runtime(app)
    if runtime is None or runtime.record.session_id != session_id:
        raise HTTPException(status_code=404, detail="Terminal session not found")
    refresh_terminal_session(runtime)
    if runtime.record.terminal_ws_token is None or runtime.record.terminal_ws_token != token:
        raise HTTPException(status_code=401, detail="Invalid terminal session token")
    if runtime.record.status != RuntimeStatus.RUNNING:
        raise HTTPException(status_code=409, detail="Terminal session is not running")
    if runtime.master_fd is None:
        raise HTTPException(status_code=409, detail="Terminal session is unavailable")
    return runtime


@router.websocket("/session/{session_id}/ws")
async def terminal_session_ws(session_id: str, token: str, websocket: WebSocket) -> None:
    try:
        runtime = _get_active_runtime(session_id, token, websocket.app)
    except HTTPException as exc:
        await websocket.close(code=_close_code_for_session_state(exc.status_code))
        return

    await websocket.accept()
    loop = asyncio.get_running_loop()
    output_queue: asyncio.Queue[str | None] = asyncio.Queue()
    master_fd = runtime.master_fd
    if master_fd is None:
        await websocket.close(code=4409)
        return

    def on_master_ready() -> None:
        if runtime.master_fd is None:
            return
        try:
            raw_chunk = os.read(runtime.master_fd, 4096)
        except OSError as exc:
            if exc.errno not in {errno.EIO, errno.EBADF}:
                output_queue.put_nowait(None)
                return
            raw_chunk = b""
        if raw_chunk:
            output_queue.put_nowait(raw_chunk.decode("utf-8", errors="replace"))
            return
        output_queue.put_nowait(None)

    loop.add_reader(master_fd, on_master_ready)

    async def forward_input() -> None:
        try:
            while True:
                message = await websocket.receive_text()
                payload = json.loads(message)
                message_type = payload.get("type")
                if message_type == "input":
                    data = payload.get("data")
                    if not isinstance(data, str):
                        raise ValueError("input payload must include string data")
                    write_terminal_input(runtime, data)
                    continue
                if message_type == "resize":
                    cols = payload.get("cols")
                    rows = payload.get("rows")
                    if not isinstance(cols, int) or not isinstance(rows, int):
                        raise ValueError("resize payload must include integer cols and rows")
                    resize_terminal(runtime, cols, rows)
                    continue
                raise ValueError(f"Unsupported terminal message type: {message_type!r}")
        except WebSocketDisconnect:
            return
        finally:
            task_group.cancel_scope.cancel()

    async def forward_output() -> None:
        try:
            while True:
                chunk = await output_queue.get()
                if chunk is None:
                    return
                await websocket.send_json({"type": "output", "data": chunk})
        finally:
            task_group.cancel_scope.cancel()

    async def watch_process() -> None:
        try:
            while True:
                returncode = runtime.process.poll()
                if returncode is not None:
                    refresh_terminal_session(runtime, close_fd=False)
                    output_queue.put_nowait(None)
                    if websocket.client_state == WebSocketState.CONNECTED:
                        with suppress(Exception):
                            await websocket.send_json(
                                {
                                    "type": "status",
                                    "status": "exited",
                                    "return_code": returncode,
                                }
                            )
                    return
                await asyncio.sleep(0.25)
        finally:
            task_group.cancel_scope.cancel()

    try:
        async with create_task_group() as task_group:
            task_group.start_soon(forward_input)
            task_group.start_soon(forward_output)
            task_group.start_soon(watch_process)
    finally:
        loop.remove_reader(master_fd)
        if runtime.process.poll() is not None and runtime.master_fd is not None:
            with suppress(OSError):
                os.close(runtime.master_fd)
            runtime.master_fd = None
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()


@router.delete("/session", response_model=TerminalSessionResponse)
async def delete_terminal_session(request: Request) -> TerminalSessionResponse:
    runtime = get_terminal_runtime(request.app)
    stopped = await to_thread.run_sync(stop_terminal_session, runtime)
    request.app.state.terminal_runtime = None
    return TerminalSessionResponse.model_validate(_serialize_session(stopped))
