from __future__ import annotations


class SSHExecutorError(RuntimeError):
    """Base error for SSH executor failures."""


class SSHConnectionError(SSHExecutorError):
    """Raised when the executor cannot establish or recover an SSH connection."""


class CommandTimeoutError(SSHExecutorError):
    """Raised when a remote command exceeds its timeout."""

    def __init__(self, message: str, stdout: str = "", stderr: str = "") -> None:
        super().__init__(message)
        self.stdout = stdout
        self.stderr = stderr


class TransferError(SSHExecutorError):
    """Raised when a file transfer fails."""


class BootstrapError(SSHExecutorError):
    """Raised when Claude Code bootstrap or validation fails."""


class UnsupportedContainerError(BootstrapError):
    """Raised when the remote container does not match the supported matrix."""
