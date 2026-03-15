from __future__ import annotations


class ParsingError(RuntimeError):
    """Base error for parsing subsystem failures."""


class MinerUConfigurationError(ParsingError):
    """Raised when MinerU client configuration is incomplete or invalid."""


class CacheError(ParsingError):
    """Raised when cached parse artifacts cannot be loaded or stored safely."""
