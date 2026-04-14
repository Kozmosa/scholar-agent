from __future__ import annotations

from fastapi import APIRouter, Request

from ainrf.api.schemas import CodeServerLifecycleStatus, CodeServerStatusResponse

router = APIRouter(prefix="/code", tags=["code"])


@router.get("/status", response_model=CodeServerStatusResponse)
async def read_code_server_status(request: Request) -> CodeServerStatusResponse:
    supervisor = getattr(request.app.state, "code_server_supervisor", None)
    if supervisor is None:
        return CodeServerStatusResponse(
            status=CodeServerLifecycleStatus.UNAVAILABLE,
            workspace_dir=None,
            detail="code-server supervisor not initialized",
            managed=True,
        )

    state = supervisor.status()
    return CodeServerStatusResponse(
        status=state.status,
        workspace_dir=str(state.workspace_dir) if state.workspace_dir is not None else None,
        detail=state.detail,
        managed=True,
    )
