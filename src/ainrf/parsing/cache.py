from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path

from ainrf.parsing.errors import CacheError
from ainrf.parsing.models import (
    CachedParseRecord,
    ParseFigure,
    ParseMetadata,
    ParseResult,
)


def default_cache_dir() -> Path:
    return Path(".ainrf/cache/mineru")


class ParseCache:
    def __init__(self, cache_dir: Path | None = None) -> None:
        self._cache_dir = cache_dir or default_cache_dir()

    @property
    def cache_dir(self) -> Path:
        return self._cache_dir

    def compute_pdf_sha256(self, pdf_path: Path) -> str:
        digest = hashlib.sha256()
        try:
            with pdf_path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
        except OSError as exc:
            raise CacheError(f"Failed to hash PDF file {pdf_path}: {exc}") from exc
        return digest.hexdigest()

    def load(self, pdf_sha256: str) -> ParseResult | None:
        cache_path = self._record_path(pdf_sha256)
        if not cache_path.exists():
            return None

        try:
            payload = json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CacheError(f"Failed to load parse cache {cache_path}: {exc}") from exc

        try:
            record = CachedParseRecord(
                pdf_sha256=str(payload["pdf_sha256"]),
                result=self._parse_result_from_dict(payload["result"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise CacheError(f"Invalid parse cache schema in {cache_path}: {exc}") from exc

        if record.pdf_sha256 != pdf_sha256:
            raise CacheError(f"Parse cache key mismatch for {cache_path}")

        return replace(record.result, cache_hit=True)

    def save(self, pdf_sha256: str, result: ParseResult) -> None:
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        record = CachedParseRecord(
            pdf_sha256=pdf_sha256,
            result=replace(result, cache_hit=False),
        )
        cache_path = self._record_path(pdf_sha256)
        temp_path = cache_path.with_suffix(".tmp")

        try:
            temp_path.write_text(
                json.dumps(asdict(record), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            temp_path.replace(cache_path)
        except OSError as exc:
            raise CacheError(f"Failed to write parse cache {cache_path}: {exc}") from exc

    def invalidate(self, pdf_sha256: str) -> None:
        cache_path = self._record_path(pdf_sha256)
        try:
            cache_path.unlink(missing_ok=True)
        except OSError as exc:
            raise CacheError(f"Failed to remove parse cache {cache_path}: {exc}") from exc

    def _record_path(self, pdf_sha256: str) -> Path:
        return self._cache_dir / f"{pdf_sha256}.json"

    def _parse_result_from_dict(self, payload: object) -> ParseResult:
        payload_mapping = self._expect_mapping(payload, "result payload")
        metadata_payload = self._expect_mapping(
            self._mapping_required(payload_mapping, "metadata"),
            "metadata payload",
        )
        figures_payload_raw = self._mapping_optional(payload_mapping, "figures", [])
        if not isinstance(figures_payload_raw, list):
            raise TypeError("figures payload must be a list")
        figures_payload: list[object] = [item for item in figures_payload_raw]

        return ParseResult(
            markdown=str(self._mapping_required(payload_mapping, "markdown")),
            metadata=ParseMetadata(
                title=self._optional_str(self._mapping_optional(metadata_payload, "title")),
                authors=self._string_list(self._mapping_optional(metadata_payload, "authors")),
                abstract=self._optional_str(self._mapping_optional(metadata_payload, "abstract")),
                source_url=self._optional_str(
                    self._mapping_optional(metadata_payload, "source_url")
                ),
                file_name=self._optional_str(self._mapping_optional(metadata_payload, "file_name")),
            ),
            figures=self._parse_figures(figures_payload),
            provider_task_id=self._optional_str(
                self._mapping_optional(payload_mapping, "provider_task_id")
            ),
            cache_hit=bool(self._mapping_optional(payload_mapping, "cache_hit", False)),
            warnings=self._string_list(self._mapping_optional(payload_mapping, "warnings")),
        )

    def _optional_str(self, value: object) -> str | None:
        if value is None:
            return None
        return str(value)

    def _string_list(self, value: object) -> list[str]:
        if value is None:
            return []
        if not isinstance(value, list):
            raise TypeError("expected a list")
        return [str(item) for item in value]

    def _expect_mapping(self, value: object, label: str) -> dict[str, object]:
        if not isinstance(value, dict):
            raise TypeError(f"{label} must be a dict")
        return {str(key): item for key, item in value.items()}

    def _mapping_required(self, mapping: dict[str, object], key: str) -> object:
        if key not in mapping:
            raise KeyError(key)
        return mapping[key]

    def _mapping_optional(
        self,
        mapping: dict[str, object],
        key: str,
        default: object | None = None,
    ) -> object | None:
        if key in mapping:
            return mapping[key]
        return default

    def _parse_figures(self, value: list[object]) -> list[ParseFigure]:
        figures: list[ParseFigure] = []
        for item in value:
            if not isinstance(item, dict):
                continue
            item_mapping = self._expect_mapping(item, "figure payload")
            figures.append(
                ParseFigure(
                    figure_id=self._optional_str(self._mapping_optional(item_mapping, "figure_id")),
                    caption=self._optional_str(self._mapping_optional(item_mapping, "caption")),
                    uri=self._optional_str(self._mapping_optional(item_mapping, "uri")),
                )
            )
        return figures
