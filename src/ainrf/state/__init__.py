from __future__ import annotations

from pathlib import Path


def default_state_root() -> Path:
    return Path.cwd() / ".ainrf"


__all__ = ["default_state_root"]
