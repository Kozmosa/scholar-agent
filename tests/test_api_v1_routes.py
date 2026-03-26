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
@pytest.mark.parametrize("path", ["/tasks", "/v1/tasks"])
async def test_tasks_routes_require_api_key(tmp_path: Path, path: str) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get(path)

    assert response.status_code == 401


@pytest.mark.anyio
@pytest.mark.parametrize("path", ["/tasks", "/v1/tasks"])
async def test_tasks_routes_accept_valid_api_key(tmp_path: Path, path: str) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get(path, headers={"X-API-Key": "secret-key"})

    assert response.status_code == 200
    assert "items" in response.json()
