from __future__ import annotations


class GateError(Exception):
    """Base error for gate management."""


class GateConflictError(GateError):
    """Raised when a task is not in a gate-manageable state."""


class GateNotFoundError(GateError):
    """Raised when a requested gate does not exist."""


class GateResolutionError(GateError):
    """Raised when a gate cannot be resolved."""
