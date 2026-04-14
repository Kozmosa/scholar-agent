from __future__ import annotations

from datetime import timedelta
from secrets import compare_digest, token_urlsafe

import anyio
import httpx
from fastapi import APIRouter, HTTPException, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse, StreamingResponse
from starlette.websockets import WebSocketState
import websockets

from ainrf.api.schemas import TerminalSessionResponse, TerminalSessionStatus
from ainrf.terminal.models import TerminalSessionRecord, utc_now
from ainrf.terminal.ttyd import start_ttyd_session, stop_ttyd_session, terminal_url

router = APIRouter(prefix="/terminal", tags=["terminal"])

VIEWER_SESSION_TTL = timedelta(minutes=30)
TTYD_AUTH_HEADER = "X-AINRF-Terminal-Auth"


def _serialize_session(session: TerminalSessionRecord) -> dict[str, str | None | TerminalSessionStatus]:
    return {
        "session_id": session.session_id,
        "provider": session.provider,
        "target_kind": session.target_kind,
        "status": session.status,
        "created_at": session.created_at.isoformat() if session.created_at else None,
        "started_at": session.started_at.isoformat() if session.started_at else None,
        "closed_at": session.closed_at.isoformat() if session.closed_at else None,
        "terminal_url": session.terminal_url,
        "detail": session.detail,
    }


def get_terminal_session(app: object) -> TerminalSessionRecord:
    session = getattr(app.state, "terminal_session", None)
    if session is None:
        return TerminalSessionRecord(
            session_id=None,
            provider="ttyd",
            target_kind="daemon-host",
            status=TerminalSessionStatus.IDLE,
        )
    return session


def _api_base_url(request: Request) -> str:
    return str(request.base_url).rstrip("/")


def _proxy_base_path(session_id: str) -> str:
    return f"/terminal/session/{session_id}/proxy"


def _proxy_target_url(request: Request, session_id: str, suffix: str) -> str:
    config = request.app.state.api_config
    base = terminal_url(config.terminal_host, config.terminal_port)
    normalized_suffix = suffix.lstrip("/")
    if normalized_suffix:
        return f"{base}/{normalized_suffix}"
    return f"{base}/"


def _viewer_cookie_name(session: TerminalSessionRecord) -> str:
    return session.viewer_cookie_name or "ainrf_terminal_viewer"


def _validate_open_request(session: TerminalSessionRecord, session_id: str, token: str) -> None:
    if session.session_id != session_id:
        raise HTTPException(status_code=404, detail="Terminal session not found")
    if session.status != TerminalSessionStatus.RUNNING:
        raise HTTPException(status_code=409, detail="Terminal session is not running")
    if session.browser_open_token is None or session.browser_open_expires_at is None:
        raise HTTPException(status_code=404, detail="Terminal open token is unavailable")
    if not compare_digest(session.browser_open_token, token):
        raise HTTPException(status_code=403, detail="Invalid terminal open token")
    if session.browser_open_consumed_at is not None:
        raise HTTPException(status_code=409, detail="Terminal open token has already been used")
    if session.browser_open_expires_at <= utc_now():
        raise HTTPException(status_code=410, detail="Terminal open token has expired")
    if session.viewer_session_token is not None and session.viewer_session_expires_at is not None:
        if session.viewer_session_expires_at > utc_now():
            raise HTTPException(status_code=409, detail="Terminal viewer session already exists")


def _require_viewer_session(session: TerminalSessionRecord, viewer_token: str | None) -> None:
    if session.session_id is None or session.status != TerminalSessionStatus.RUNNING:
        raise HTTPException(status_code=409, detail="Terminal session is not running")
    if session.viewer_session_token is None or session.viewer_session_expires_at is None:
        raise HTTPException(status_code=401, detail="Terminal viewer session is unavailable")
    if viewer_token is None or not compare_digest(session.viewer_session_token, viewer_token):
        raise HTTPException(status_code=401, detail="Invalid terminal viewer session")
    if session.viewer_session_expires_at <= utc_now():
        raise HTTPException(status_code=401, detail="Terminal viewer session has expired")


def _ttyd_auth_headers() -> dict[str, str]:
    return {TTYD_AUTH_HEADER: "allow"}


@router.get("/session", response_model=TerminalSessionResponse)
async def read_terminal_session(request: Request) -> TerminalSessionResponse:
    session = get_terminal_session(request.app)
    return TerminalSessionResponse.model_validate(_serialize_session(session))


@router.post("/session", response_model=TerminalSessionResponse)
async def create_terminal_session(request: Request) -> TerminalSessionResponse:
    config = request.app.state.api_config
    existing_session = getattr(request.app.state, "terminal_session", None)
    if existing_session is not None and existing_session.status == TerminalSessionStatus.RUNNING:
        request.app.state.terminal_session = stop_ttyd_session(existing_session)
    session = start_ttyd_session(
        host=config.terminal_host,
        port=config.terminal_port,
        auth_header_name=TTYD_AUTH_HEADER,
        shell_command=config.terminal_command,
        working_directory=config.state_root,
        api_base_url=_api_base_url(request),
    )
    request.app.state.terminal_session = session
    return TerminalSessionResponse.model_validate(_serialize_session(session))


@router.get("/session/{session_id}/open")
async def open_terminal_session(session_id: str, token: str, request: Request) -> RedirectResponse:
    session = get_terminal_session(request.app)
    _validate_open_request(session, session_id, token)
    now = utc_now()
    session.browser_open_consumed_at = now
    session.viewer_session_token = token_urlsafe(24)
    session.viewer_session_expires_at = now + VIEWER_SESSION_TTL
    redirect = RedirectResponse(url=f"{_proxy_base_path(session_id)}/", status_code=303)
    redirect.set_cookie(
        key=_viewer_cookie_name(session),
        value=session.viewer_session_token,
        httponly=True,
        samesite="lax",
        max_age=int(VIEWER_SESSION_TTL.total_seconds()),
        path=_proxy_base_path(session_id),
    )
    return redirect


@router.get("/session/{session_id}/proxy/{path:path}")
async def proxy_terminal_http(session_id: str, path: str, request: Request) -> Response:
    session = get_terminal_session(request.app)
    _require_viewer_session(session, request.cookies.get(_viewer_cookie_name(session)))
    upstream_url = _proxy_target_url(request, session_id, path)
    upstream_headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in {"host", "cookie", "content-length"}
    }
    upstream_headers.update(_ttyd_auth_headers())
    async with httpx.AsyncClient(follow_redirects=False) as client:
        upstream = await client.request(
            method=request.method,
            url=upstream_url,
            params=request.query_params,
            headers=upstream_headers,
            content=await request.body(),
        )
    response_headers = {
        key: value
        for key, value in upstream.headers.items()
        if key.lower() not in {"content-length", "connection", "transfer-encoding"}
    }
    return StreamingResponse(
        iter([upstream.content]),
        status_code=upstream.status_code,
        headers=response_headers,
        media_type=upstream.headers.get("content-type"),
    )


@router.websocket("/session/{session_id}/proxy/ws")
async def proxy_terminal_websocket(session_id: str, websocket: WebSocket) -> None:
    session = get_terminal_session(websocket.app)
    viewer_token = websocket.cookies.get(_viewer_cookie_name(session))
    try:
        _require_viewer_session(session, viewer_token)
    except HTTPException:
        await websocket.close(code=4401)
        return

    config = websocket.app.state.api_config
    upstream_ws_url = f"ws://{config.terminal_host}:{config.terminal_port}/ws"
    await websocket.accept()

    async with websockets.connect(
        upstream_ws_url,
        additional_headers=_ttyd_auth_headers(),
    ) as upstream:
        async def browser_to_upstream(task_group: anyio.abc.TaskGroup) -> None:
            try:
                while True:
                    message = await websocket.receive()
                    if message.get("type") == "websocket.disconnect":
                        break
                    if "text" in message and message["text"] is not None:
                        await upstream.send(message["text"])
                    if "bytes" in message and message["bytes"] is not None:
                        await upstream.send(message["bytes"])
            except WebSocketDisconnect:
                pass
            finally:
                task_group.cancel_scope.cancel()

        async def upstream_to_browser(task_group: anyio.abc.TaskGroup) -> None:
            try:
                async for message in upstream:
                    if isinstance(message, bytes):
                        await websocket.send_bytes(message)
                    else:
                        await websocket.send_text(message)
            finally:
                task_group.cancel_scope.cancel()

        try:
            async with anyio.create_task_group() as task_group:
                task_group.start_soon(browser_to_upstream, task_group)
                task_group.start_soon(upstream_to_browser, task_group)
        finally:
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await websocket.close()


@router.delete("/session", response_model=TerminalSessionResponse)
async def delete_terminal_session(request: Request) -> TerminalSessionResponse:
    stopped = stop_ttyd_session(getattr(request.app.state, "terminal_session", None))
    request.app.state.terminal_session = stopped
    return TerminalSessionResponse.model_validate(_serialize_session(stopped))
