from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version


def get_version() -> str:
    try:
        return version("scholar-agent-notes")
    except PackageNotFoundError:
        return "0.1.0"


__all__ = ["get_version"]
__version__ = get_version()
