from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class ParseFailureType(StrEnum):
    FILE_NOT_FOUND = "file_not_found"
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"
    RATE_LIMIT_EXHAUSTED = "rate_limit_exhausted"
    PROVIDER_REJECTED = "provider_rejected"
    INVALID_RESPONSE = "invalid_response"
    INVALID_STRUCTURE = "invalid_structure"


@dataclass(slots=True, frozen=True)
class ParseRequest:
    pdf_path: Path
    source_url: str | None = None
    role: str | None = None


@dataclass(slots=True, frozen=True)
class ParseMetadata:
    title: str | None = None
    authors: list[str] = field(default_factory=list)
    abstract: str | None = None
    source_url: str | None = None
    file_name: str | None = None


@dataclass(slots=True, frozen=True)
class ParseFigure:
    figure_id: str | None = None
    caption: str | None = None
    uri: str | None = None


@dataclass(slots=True, frozen=True)
class ParseResult:
    markdown: str
    metadata: ParseMetadata
    figures: list[ParseFigure] = field(default_factory=list)
    provider_task_id: str | None = None
    cache_hit: bool = False
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True, frozen=True)
class ParseFailure:
    failure_type: ParseFailureType
    message: str
    retryable: bool
    provider_task_id: str | None = None


@dataclass(slots=True, frozen=True)
class CachedParseRecord:
    pdf_sha256: str
    result: ParseResult
