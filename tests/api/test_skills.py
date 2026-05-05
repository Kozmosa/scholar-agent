from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from ainrf.api.app import create_app
from ainrf.api.config import ApiConfig, hash_api_key
from ainrf.skills import SkillsDiscoveryService


def _make_app(tmp_path: Path, scan_roots: list[Path] | None = None) -> tuple:
    api_config = ApiConfig(
        api_key_hashes=frozenset({hash_api_key("secret-key")}),
        state_root=tmp_path,
    )
    app = create_app(api_config)
    if scan_roots is not None:
        app.state.skills_discovery_service = SkillsDiscoveryService(scan_roots=scan_roots)
    return app


def make_client(tmp_path: Path, scan_roots: list[Path] | None = None) -> httpx.AsyncClient:
    app = _make_app(tmp_path, scan_roots=scan_roots)
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
        headers={"X-API-Key": "secret-key"},
    )


def _create_skill_dir(parent: Path, skill_id: str, skill_json: dict, skill_md_content: str) -> Path:
    skill_dir = parent / skill_id
    skill_dir.mkdir(parents=True)
    (skill_dir / "skill.json").write_text(json.dumps(skill_json), encoding="utf-8")
    (skill_dir / "SKILL.md").write_text(skill_md_content, encoding="utf-8")
    return skill_dir


@pytest.mark.anyio
async def test_get_skill_detail_success(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    skill_id = "test-skill"
    skill_json = {
        "skill_id": skill_id,
        "label": "Test Skill",
        "description": "A test skill",
        "version": "1.2.3",
        "author": "tester",
        "dependencies": ["dep-a", "dep-b"],
        "inject_mode": "prompt_only",
        "settings_fragment": {"foo": {"bar": 1}},
        "mcp_servers": ["server1"],
        "hooks": ["hook1"],
        "allowed_agents": ["claude-code", "custom-agent"],
    }
    skill_md = "# Test Skill\n\nThis is the SKILL.md content.\n"
    _create_skill_dir(skills_root, skill_id, skill_json, skill_md)

    async with make_client(tmp_path, scan_roots=[skills_root]) as client:
        response = await client.get(f"/skills/{skill_id}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["skill_id"] == skill_id
    assert payload["label"] == "Test Skill"
    assert payload["description"] == "A test skill"
    assert payload["version"] == "1.2.3"
    assert payload["author"] == "tester"
    assert payload["dependencies"] == ["dep-a", "dep-b"]
    assert payload["inject_mode"] == "prompt_only"
    assert payload["settings_fragment"] == {"foo": {"bar": 1}}
    assert payload["mcp_servers"] == ["server1"]
    assert payload["hooks"] == ["hook1"]
    assert payload["allowed_agents"] == ["claude-code", "custom-agent"]
    assert payload["skill_md"] == skill_md


@pytest.mark.anyio
async def test_get_skill_detail_not_found(tmp_path: Path) -> None:
    async with make_client(tmp_path, scan_roots=[]) as client:
        response = await client.get("/skills/nonexistent")

    assert response.status_code == 404
    assert response.json()["detail"] == "Skill not found"


@pytest.mark.anyio
async def test_preview_skill_settings_success(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    skill_id = "preview-skill"
    skill_json = {
        "skill_id": skill_id,
        "label": "Preview Skill",
        "settings_fragment": {"permissionMode": "restricted", "extra": {"nested": True}},
    }
    _create_skill_dir(skills_root, skill_id, skill_json, "# Preview\n")

    async with make_client(tmp_path, scan_roots=[skills_root]) as client:
        response = await client.get(f"/skills/{skill_id}/preview")

    assert response.status_code == 200
    payload = response.json()
    assert payload["skill_id"] == skill_id
    assert payload["label"] == "Preview Skill"
    assert payload["settings_fragment"] == {
        "permissionMode": "restricted",
        "extra": {"nested": True},
    }
    # merged_preview = deep_merge({"permissionMode": "bypassPermissions"}, settings_fragment)
    assert payload["merged_preview"]["permissionMode"] == "restricted"
    assert payload["merged_preview"]["extra"] == {"nested": True}


@pytest.mark.anyio
async def test_preview_skill_settings_not_found(tmp_path: Path) -> None:
    async with make_client(tmp_path, scan_roots=[]) as client:
        response = await client.get("/skills/nonexistent/preview")

    assert response.status_code == 404
    assert response.json()["detail"] == "Skill not found"
