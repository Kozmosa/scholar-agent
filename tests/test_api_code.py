from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key
from ainrf.code_server import CodeServerLifecycleStatus, CodeServerState


@pytest.mark.anyio
@pytest.mark.parametrize("path", ["/code/status", "/v1/code/status"])
async def test_code_status_reports_unavailable_without_supervisor(tmp_path: Path, path: str) -> None:
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get(path, headers={"X-API-Key": "secret-key"})

    assert response.status_code == 200
    assert response.json() == {
        "status": "unavailable",
        "workspace_dir": None,
        "detail": "code-server supervisor not initialized",
        "managed": True,
    }


@pytest.mark.anyio
@pytest.mark.parametrize("path", ["/code/", "/v1/code/"])
async def test_code_proxy_returns_503_when_code_server_is_unavailable(tmp_path: Path, path: str) -> None:
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get(path, headers={"X-API-Key": "secret-key"})

    assert response.status_code == 503
    assert response.json() == {"detail": "code-server is unavailable"}


class ReadySupervisor:
    base_url = "http://127.0.0.1:18080"

    def status(self) -> CodeServerState:
        return CodeServerState(status=CodeServerLifecycleStatus.READY)


@pytest.mark.anyio
@pytest.mark.parametrize("path", ["/code/", "/v1/code/"])
async def test_code_proxy_forwards_ready_requests(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, path: str) -> None:
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )
    app.state.code_server_supervisor = ReadySupervisor()

    original_request = httpx.AsyncClient.request

    async def fake_request(
        self: httpx.AsyncClient,
        method: str,
        url: str,
        **kwargs: object,
    ) -> httpx.Response:
        if str(url).startswith("/") or str(url).startswith("http://testserver"):
            return await original_request(self, method, url, **kwargs)

        headers = kwargs["headers"]
        content = kwargs.get("content", b"")
        follow_redirects = kwargs["follow_redirects"]

        assert method == "GET"
        assert url == "http://127.0.0.1:18080/"
        assert headers["accept"] == "text/html"
        assert "x-api-key" not in headers
        assert content == b""
        assert follow_redirects is False
        return httpx.Response(
            status_code=200,
            headers={"content-type": "text/html; charset=utf-8", "x-upstream": "code-server"},
            text="<html>ok</html>",
        )

    monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get(
            path,
            headers={"X-API-Key": "secret-key", "Accept": "text/html"},
        )

    assert response.status_code == 200
    assert response.text == "<html>ok</html>"
    assert response.headers["content-type"].startswith("text/html")
    assert response.headers["x-upstream"] == "code-server"
