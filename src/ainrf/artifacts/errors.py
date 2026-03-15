from __future__ import annotations


class ArtifactError(RuntimeError):
    """Base error for artifact subsystem failures."""


class InvalidTransitionError(ArtifactError):
    """Raised when an artifact attempts an illegal lifecycle transition."""
