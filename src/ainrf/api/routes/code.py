from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

import httpx
from fastapi import APIRouter, HTTPException, Request, Response

from ainrf.api.schemas import CodeServerLifecycleStatus, CodeServerStatusResponse

router = APIRouter(prefix="/code", tags=["code"])
_HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}


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


def _filter_request_headers(headers: httpx.Headers) -> dict[str, str]:
    return {
        key: value
        for key, value in headers.items()
        if key.lower() not in _HOP_BY_HOP_HEADERS and key.lower() != "x-api-key"
    }


def _filter_response_headers(headers: httpx.Headers) -> dict[str, str]:
    return {
        key: value
        for key, value in headers.items()
        if key.lower() not in _HOP_BY_HOP_HEADERS
    }


def _build_upstream_url(base_url: str, request: Request, path: str) -> str:
    base = base_url.rstrip("/")
    upstream_path = f"/{path}" if path else "/"
    split = urlsplit(str(request.url))
    return urlunsplit(("http", urlsplit(base).netloc, upstream_path, split.query, ""))


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
async def proxy_code_server(request: Request, path: str) -> Response:
    supervisor = getattr(request.app.state, "code_server_supervisor", None)
    if supervisor is None or supervisor.status().status != CodeServerLifecycleStatus.READY:
        raise HTTPException(status_code=503, detail="code-server is unavailable")

    upstream_url = _build_upstream_url(supervisor.base_url, request, path)
    request_headers = _filter_request_headers(request.headers)
    request_body = await request.body()

    try:
        async with httpx.AsyncClient() as client:
            upstream_response = await client.request(
                request.method,
                upstream_url,
                headers=request_headers,
                content=request_body,
                follow_redirects=False,
            )
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=503, detail="code-server upstream timed out") from exc
    except (httpx.RequestError, httpx.TransportError) as exc:
        raise HTTPException(status_code=502, detail="code-server upstream request failed") from exc

    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=_filter_response_headers(upstream_response.headers),
        media_type=upstream_response.headers.get("content-type"),
    )
