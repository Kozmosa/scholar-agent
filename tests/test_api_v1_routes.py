from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key


def make_client(tmp_path: Path) -> httpx.AsyncClient:
    app = create_app(
        ApiConfig(
            api_key_hashes=frozenset({hash_api_key("secret-key")}),
            state_root=tmp_path,
        )
    )
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    )


@pytest.mark.anyio
@pytest.mark.parametrize("path", ["/health", "/v1/health"])
async def test_health_routes_are_public(tmp_path: Path, path: str) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get(path)

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.anyio
async def test_openapi_registers_health_terminal_and_code_routes_and_removes_tasks(tmp_path: Path) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200
    payload = response.json()
    assert "/health" in payload["paths"]
    assert "/v1/health" in payload["paths"]
    assert "/terminal/session" in payload["paths"]
    assert "/v1/terminal/session" in payload["paths"]
    assert "/code/status" in payload["paths"]
    assert "/v1/code/status" in payload["paths"]
    assert "/tasks" not in payload["paths"]
    assert "/v1/tasks" not in payload["paths"]
