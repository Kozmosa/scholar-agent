from __future__ import annotations

import json
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
async def test_health_is_public(tmp_path: Path) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.anyio
async def test_protected_route_requires_api_key(tmp_path: Path) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get("/tasks")

    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.anyio
async def test_invalid_api_key_is_rejected(tmp_path: Path) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get("/tasks", headers={"X-API-Key": "wrong"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.anyio
async def test_openapi_is_public(tmp_path: Path) -> None:
    async with make_client(tmp_path) as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200
    payload = response.json()
    assert "/tasks" in payload["paths"]


def test_api_config_loads_default_container_profile_from_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AINRF_API_KEY_HASHES", raising=False)
    monkeypatch.delenv("AINRF_CONTAINER_HOST", raising=False)
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "api_key_hashes": [hash_api_key("secret-key")],
                "container_profiles": {
                    "gpu-main": {
                        "host": "gpu-server-01",
                        "port": 2200,
                        "user": "researcher",
                        "ssh_key_path": "/tmp/id_ed25519",
                        "ssh_password": "secret-pass",
                        "project_dir": "/workspace/project-a",
                        "connect_timeout": 20,
                        "command_timeout": 300,
                    }
                },
                "default_container_profile": "gpu-main",
            }
        ),
        encoding="utf-8",
    )

    config = ApiConfig.from_env(tmp_path)

    assert config.container_config is not None
    assert config.container_config.host == "gpu-server-01"
    assert config.container_config.user == "researcher"
    assert config.container_config.port == 2200
    assert config.container_config.ssh_password == "secret-pass"
