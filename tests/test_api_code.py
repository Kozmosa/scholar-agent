from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key


@pytest.mark.anyio
async def test_code_status_reports_unavailable_without_supervisor(tmp_path: Path) -> None:
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
        response = await client.get("/code/status", headers={"X-API-Key": "secret-key"})

    assert response.status_code == 200
    assert response.json() == {
        "status": "unavailable",
        "workspace_dir": None,
        "detail": "code-server supervisor not initialized",
        "managed": True,
    }
