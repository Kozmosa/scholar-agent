from __future__ import annotations

from fastapi import APIRouter, Request

from ainrf.api.schemas import TerminalSessionResponse, TerminalSessionStatus
from ainrf.terminal.models import TerminalSessionRecord

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


def start_terminal_session(app: object) -> TerminalSessionRecord:
    return get_terminal_session(app)


def stop_terminal_session(app: object) -> None:
    app.state.terminal_session = None


@router.get("/session", response_model=TerminalSessionResponse)
async def read_terminal_session(request: Request) -> TerminalSessionResponse:
    session = get_terminal_session(request.app)
    return TerminalSessionResponse.model_validate(_serialize_session(session))


@router.post("/session", response_model=TerminalSessionResponse)
async def create_terminal_session(request: Request) -> TerminalSessionResponse:
    session = start_terminal_session(request.app)
    request.app.state.terminal_session = session
    return TerminalSessionResponse.model_validate(_serialize_session(session))


@router.delete("/session", response_model=TerminalSessionResponse)
async def delete_terminal_session(request: Request) -> TerminalSessionResponse:
    stop_terminal_session(request.app)
    return TerminalSessionResponse(
        provider="ttyd",
        target_kind="daemon-host",
        status=TerminalSessionStatus.IDLE,
    )
