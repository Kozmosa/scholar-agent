"""Generate skill.json from SKILL.md frontmatter."""

from __future__ import annotations

import re
from typing import Any

import yaml


_YAML_DELIM_RE = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def parse_skill_md_frontmatter(content: str) -> dict[str, Any]:
    """Parse YAML frontmatter from SKILL.md content.

    Returns empty dict if no frontmatter found or yaml parsing fails.
    """
    # Find the first --- delimiter
    match = _YAML_DELIM_RE.search(content)
    if not match:
        return {}

    start = match.end()
    # Find the closing --- after the opening one
    end_match = _YAML_DELIM_RE.search(content, start)
    if not end_match:
        return {}

    yaml_block = content[start:end_match.start()]
    if not yaml_block.strip():
        return {}

    try:
        parsed = yaml.safe_load(yaml_block)
        if isinstance(parsed, dict):
            return parsed
        return {}
    except yaml.YAMLError:
        return {}


def generate_skill_json(
    skill_dir_name: str,
    frontmatter: dict[str, Any],
    is_core: bool = False,
) -> dict[str, Any]:
    """Generate a skill.json dict from parsed frontmatter.

    Args:
        skill_dir_name: The directory basename (used as fallback for skill_id/label).
        frontmatter: Parsed YAML frontmatter from SKILL.md.
        is_core: Whether this skill is in the core subset (enables inject_mode=auto).

    Returns:
        A dict matching the AINRF skill.json schema.
    """
    skill_id = frontmatter.get("name", skill_dir_name)
    label = frontmatter.get("name", skill_dir_name)
    description = frontmatter.get("description", "")
    inject_mode = "auto" if is_core else "disabled"

    return {
        "skill_id": skill_id,
        "label": label,
        "description": description,
        "version": "0.0.0",
        "author": "ARIS",
        "inject_mode": inject_mode,
        "dependencies": [],
        "settings_fragment": {},
        "mcp_servers": [],
        "hooks": [],
        "allowed_agents": [],
    }
