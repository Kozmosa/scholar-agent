from __future__ import annotations


class StateStoreError(RuntimeError):
    """Base error for state store failures."""


class SerializationError(StateStoreError):
    """Raised when store payloads cannot be serialized or parsed safely."""


class ResumeNotAllowedError(StateStoreError):
    """Raised when a terminal task is asked to resume."""
