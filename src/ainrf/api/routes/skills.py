from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from ainrf.api.schemas import (
    SkillDetailResponse,
    SkillItemResponse,
    SkillListResponse,
    SkillPreviewResponse,
)
from ainrf.skills import SkillsDiscoveryService
from ainrf.skills.merge import deep_merge_settings

router = APIRouter(prefix="/skills", tags=["skills"])


def _get_skills_discovery_service(request: Request) -> SkillsDiscoveryService:
    service = getattr(request.app.state, "skills_discovery_service", None)
    if service is None:
        raise HTTPException(status_code=500, detail="skills discovery service not initialized")
    return service


@router.get("", response_model=SkillListResponse)
async def list_skills(request: Request) -> SkillListResponse:
    service = _get_skills_discovery_service(request)
    skills = service.discover()
    return SkillListResponse(
        items=[
            SkillItemResponse(
                skill_id=s.skill_id,
                label=s.label,
                description=s.description,
            )
            for s in skills
        ]
    )


@router.get("/{skill_id}", response_model=SkillDetailResponse)
async def get_skill_detail(request: Request, skill_id: str) -> SkillDetailResponse:
    """Return full skill metadata plus SKILL.md content."""
    service = _get_skills_discovery_service(request)
    skills = service.discover_full()
    skill = next((s for s in skills if s.skill_id == skill_id), None)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    skill_md = None
    for root in service._scan_roots:
        md_path = root / skill_id / "SKILL.md"
        if md_path.is_file():
            skill_md = md_path.read_text(encoding="utf-8")
            break

    return SkillDetailResponse(
        skill_id=skill.skill_id,
        label=skill.label,
        description=skill.description,
        version=skill.version,
        author=skill.author,
        dependencies=list(skill.dependencies),
        inject_mode=skill.inject_mode.value,
        settings_fragment=dict(skill.settings_fragment),
        mcp_servers=list(skill.mcp_servers),
        hooks=list(skill.hooks),
        allowed_agents=list(skill.allowed_agents),
        skill_md=skill_md,
    )


@router.get("/{skill_id}/preview", response_model=SkillPreviewResponse)
async def preview_skill_settings(request: Request, skill_id: str) -> SkillPreviewResponse:
    """Return the skill's settings fragment and a merged preview."""
    service = _get_skills_discovery_service(request)
    skills = service.discover_full()
    skill = next((s for s in skills if s.skill_id == skill_id), None)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    merged_preview = deep_merge_settings(
        {"permissionMode": "bypassPermissions"},
        skill.settings_fragment,
    )

    return SkillPreviewResponse(
        skill_id=skill.skill_id,
        label=skill.label,
        settings_fragment=dict(skill.settings_fragment),
        merged_preview=merged_preview,
    )
