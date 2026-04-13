from __future__ import annotations

from fastapi import APIRouter, Request

from ainrf.api.schemas import TerminalSessionResponse, TerminalSessionStatus
from ainrf.terminal.models import TerminalSessionRecord
from ainrf.terminal.ttyd import start_ttyd_session, stop_ttyd_session

router = APIRouter(prefix="/terminal", tags=["terminal"])


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


@router.get("/session", response_model=TerminalSessionResponse)
async def read_terminal_session(request: Request) -> TerminalSessionResponse:
    session = get_terminal_session(request.app)
    return TerminalSessionResponse.model_validate(_serialize_session(session))


@router.post("/session", response_model=TerminalSessionResponse)
async def create_terminal_session(request: Request) -> TerminalSessionResponse:
    config = request.app.state.api_config
    api_key = request.headers.get("X-API-Key", "")
    session = start_ttyd_session(
        host=config.terminal_host,
        port=config.terminal_port,
        credential=f"terminal:{api_key}",
        shell_command=config.terminal_command,
        working_directory=config.state_root,
    )
    request.app.state.terminal_session = session
    return TerminalSessionResponse.model_validate(_serialize_session(session))


@router.delete("/session", response_model=TerminalSessionResponse)
async def delete_terminal_session(request: Request) -> TerminalSessionResponse:
    stopped = stop_ttyd_session(getattr(request.app.state, "terminal_session", None))
    request.app.state.terminal_session = stopped
    return TerminalSessionResponse.model_validate(_serialize_session(stopped))
