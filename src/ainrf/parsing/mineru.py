from __future__ import annotations

import asyncio
import io
import json
import os
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx

from ainrf.parsing.cache import ParseCache, default_cache_dir
from ainrf.parsing.contracts import PaperParser
from ainrf.parsing.errors import CacheError, MinerUConfigurationError
from ainrf.parsing.models import (
    ParseFailure,
    ParseFailureType,
    ParseFigure,
    ParseMetadata,
    ParseRequest,
    ParseResult,
)

_TITLE_PATTERN = re.compile(r"^#\s+\S+", re.MULTILINE)
_ABSTRACT_PATTERN = re.compile(r"(?im)^#+\s*abstract\b")
_SECTION_PATTERN = re.compile(r"(?m)^##\s+")
_HEADING_PATTERN = re.compile(r"(?m)^#\s+(?P<title>.+?)\s*$")
_ABSTRACT_BLOCK_PATTERN = re.compile(
    r"(?is)^#+\s*abstract\s*$\n(?P<abstract>.*?)(?:^#+\s+|\Z)",
    re.MULTILINE,
)


@dataclass(slots=True, frozen=True)
class MinerUConfig:
    base_url: str
    api_key: str
    upload_batch_path: str = "/api/v4/file-urls/batch"
    remote_batch_path: str = "/api/v4/extract/task/batch"
    result_path_template: str = "/api/v4/extract-results/batch/{batch_id}"
    model_version: str = "vlm"
    language: str = "en"
    enable_formula: bool = True
    enable_table: bool = True
    is_ocr: bool = True
    timeout_seconds: float = 30.0
    poll_interval_seconds: float = 2.0
    max_retries: int = 3
    cache_dir: Path = field(default_factory=default_cache_dir)

    @classmethod
    def from_env(cls) -> MinerUConfig:
        base_url = os.environ.get("AINRF_MINERU_BASE_URL")
        api_key = os.environ.get("AINRF_MINERU_API_KEY")
        if not base_url or not api_key:
            raise MinerUConfigurationError(
                "AINRF_MINERU_BASE_URL and AINRF_MINERU_API_KEY must both be configured"
            )

        timeout_seconds = float(os.environ.get("AINRF_MINERU_TIMEOUT_SECONDS", "30"))
        poll_interval_seconds = float(os.environ.get("AINRF_MINERU_POLL_INTERVAL_SECONDS", "2"))
        max_retries = int(os.environ.get("AINRF_MINERU_MAX_RETRIES", "3"))
        cache_dir_env = os.environ.get("AINRF_MINERU_CACHE_DIR")
        cache_dir = Path(cache_dir_env) if cache_dir_env else default_cache_dir()
        model_version = os.environ.get("AINRF_MINERU_MODEL_VERSION", "vlm")
        language = os.environ.get("AINRF_MINERU_LANGUAGE", "en")
        enable_formula = _parse_bool_env("AINRF_MINERU_ENABLE_FORMULA", default=True)
        enable_table = _parse_bool_env("AINRF_MINERU_ENABLE_TABLE", default=True)
        is_ocr = _parse_bool_env("AINRF_MINERU_IS_OCR", default=True)

        return cls(
            base_url=base_url,
            api_key=api_key,
            model_version=model_version,
            language=language,
            enable_formula=enable_formula,
            enable_table=enable_table,
            is_ocr=is_ocr,
            timeout_seconds=timeout_seconds,
            poll_interval_seconds=poll_interval_seconds,
            max_retries=max_retries,
            cache_dir=cache_dir,
        )


class MinerUClient(PaperParser):
    def __init__(
        self,
        config: MinerUConfig,
        *,
        cache: ParseCache | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._config = config
        self._cache = cache or ParseCache(config.cache_dir)
        self._http_client = http_client

    async def parse_pdf(self, request: ParseRequest) -> ParseResult | ParseFailure:
        if not request.pdf_path.exists():
            return ParseFailure(
                failure_type=ParseFailureType.FILE_NOT_FOUND,
                message=f"PDF file does not exist: {request.pdf_path}",
                retryable=False,
            )

        try:
            pdf_sha256 = self._cache.compute_pdf_sha256(request.pdf_path)
        except CacheError as exc:
            return ParseFailure(
                failure_type=ParseFailureType.INVALID_RESPONSE,
                message=str(exc),
                retryable=False,
            )

        try:
            cached_result = self._cache.load(pdf_sha256)
        except CacheError:
            self._cache.invalidate(pdf_sha256)
            cached_result = None

        if cached_result is not None:
            return cached_result

        try:
            result = await self._parse_via_provider(request)
        except httpx.TimeoutException as exc:
            return ParseFailure(
                failure_type=ParseFailureType.TIMEOUT,
                message=f"MinerU request timed out: {exc}",
                retryable=True,
            )
        except httpx.HTTPError as exc:
            return ParseFailure(
                failure_type=ParseFailureType.NETWORK_ERROR,
                message=f"MinerU request failed: {exc}",
                retryable=True,
            )
        except RateLimitExhaustedError as exc:
            return ParseFailure(
                failure_type=ParseFailureType.RATE_LIMIT_EXHAUSTED,
                message=str(exc),
                retryable=True,
                provider_task_id=exc.task_id,
            )
        except InvalidProviderResponseError as exc:
            return ParseFailure(
                failure_type=ParseFailureType.INVALID_RESPONSE,
                message=str(exc),
                retryable=False,
                provider_task_id=exc.task_id,
            )
        except ProviderRejectedError as exc:
            return ParseFailure(
                failure_type=ParseFailureType.PROVIDER_REJECTED,
                message=str(exc),
                retryable=exc.retryable,
                provider_task_id=exc.task_id,
            )

        self._cache.save(pdf_sha256, result)
        return result

    async def _parse_via_provider(self, request: ParseRequest) -> ParseResult:
        if request.source_url is not None:
            batch_id = await self._submit_remote_url(request)
        else:
            batch_id = await self._submit_local_file(request)

        terminal_result = await self._poll_until_terminal(batch_id)
        state = self._extract_required_str(
            terminal_result,
            ("state",),
            task_id=batch_id,
        ).lower()
        if state == "failed":
            raise ProviderRejectedError(
                task_id=batch_id,
                message=self._extract_optional_str(terminal_result, ("err_msg",))
                or f"MinerU batch {batch_id} failed",
                retryable=False,
            )

        full_zip_url = self._extract_required_str(
            terminal_result,
            ("full_zip_url",),
            task_id=batch_id,
        )
        archive_bytes = await self._download_result_archive(full_zip_url, batch_id)
        markdown, figures, metadata = self._extract_archive_payload(archive_bytes, request)
        warnings = self._validate_markdown(markdown, metadata)

        return ParseResult(
            markdown=markdown,
            metadata=metadata,
            figures=figures,
            provider_task_id=batch_id,
            warnings=warnings,
        )

    async def _submit_local_file(self, request: ParseRequest) -> str:
        envelope = await self._request_enveloped_json(
            "POST",
            self._config.upload_batch_path,
            json=self._build_upload_request_body(request),
        )
        batch_id = self._extract_required_str(envelope, ("batch_id",))
        file_urls = self._extract_required_list(envelope, ("file_urls",), task_id=batch_id)
        if len(file_urls) != 1:
            raise InvalidProviderResponseError(
                f"Expected exactly one upload URL for batch {batch_id}",
                task_id=batch_id,
            )

        upload_url = str(file_urls[0])
        await self._upload_file(upload_url, request.pdf_path, batch_id)
        return batch_id

    async def _submit_remote_url(self, request: ParseRequest) -> str:
        envelope = await self._request_enveloped_json(
            "POST",
            self._config.remote_batch_path,
            json=self._build_remote_request_body(request),
        )
        return self._extract_required_str(envelope, ("batch_id",))

    async def _poll_until_terminal(self, batch_id: str) -> dict[str, object]:
        deadline = asyncio.get_running_loop().time() + self._config.timeout_seconds
        while True:
            envelope = await self._request_enveloped_json(
                "GET",
                self._config.result_path_template.format(batch_id=batch_id),
                task_id=batch_id,
            )
            extract_result = self._extract_required_mapping(
                envelope,
                ("extract_result",),
                task_id=batch_id,
            )
            state = self._extract_required_str(
                extract_result,
                ("state",),
                task_id=batch_id,
            ).lower()
            if state in {"done", "failed"}:
                return extract_result
            if asyncio.get_running_loop().time() >= deadline:
                raise httpx.ReadTimeout(f"MinerU polling timed out for batch {batch_id}")
            await asyncio.sleep(self._config.poll_interval_seconds)

    async def _download_result_archive(self, archive_url: str, batch_id: str) -> bytes:
        attempts = self._config.max_retries + 1
        last_rate_limit_error: RateLimitExhaustedError | None = None
        for attempt in range(1, attempts + 1):
            try:
                response = await self._get_client().get(archive_url)
            except httpx.TimeoutException:
                if attempt == attempts:
                    raise
                continue
            except httpx.HTTPError:
                if attempt == attempts:
                    raise
                continue

            if response.status_code == 429:
                last_rate_limit_error = RateLimitExhaustedError(
                    f"MinerU result archive rate limit exhausted after {attempt} attempts",
                    task_id=batch_id,
                )
                if attempt == attempts:
                    break
                continue

            if response.status_code >= 500:
                if attempt == attempts:
                    response.raise_for_status()
                continue

            response.raise_for_status()
            return response.content

        if last_rate_limit_error is not None:
            raise last_rate_limit_error

        raise InvalidProviderResponseError(
            "MinerU result archive exhausted retries without a valid response",
            task_id=batch_id,
        )

    def _extract_archive_payload(
        self,
        archive_bytes: bytes,
        request: ParseRequest,
    ) -> tuple[str, list[ParseFigure], ParseMetadata]:
        try:
            with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
                markdown = archive.read(self._find_archive_member(archive, "full.md")).decode("utf-8")
                content_list_name = self._find_optional_archive_member(
                    archive,
                    ("content_list.json", "_content_list.json"),
                )
                content_list_payload = (
                    json.loads(archive.read(content_list_name).decode("utf-8"))
                    if content_list_name is not None
                    else None
                )
        except (OSError, zipfile.BadZipFile, KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise InvalidProviderResponseError(
                f"Failed to unpack MinerU result archive: {exc}"
            ) from exc

        metadata = self._build_metadata(markdown, request, content_list_payload)
        figures = self._parse_figures_from_content_list(content_list_payload)
        return markdown, figures, metadata

    def _build_metadata(
        self,
        markdown: str,
        request: ParseRequest,
        content_list_payload: object,
    ) -> ParseMetadata:
        title = self._extract_title(markdown, content_list_payload)
        abstract = self._extract_abstract(markdown)
        return ParseMetadata(
            title=title,
            authors=[],
            abstract=abstract,
            source_url=request.source_url,
            file_name=request.pdf_path.name,
        )

    def _extract_title(self, markdown: str, content_list_payload: object) -> str | None:
        heading_match = _HEADING_PATTERN.search(markdown)
        if heading_match is not None:
            return heading_match.group("title").strip()

        if isinstance(content_list_payload, list):
            for item in content_list_payload:
                if not isinstance(item, dict):
                    continue
                item_mapping = self._mapping_from_object(item)
                item_type = self._mapping_optional(item_mapping, "type")
                text_level = self._mapping_optional(item_mapping, "text_level")
                if item_type == "text" and text_level == 1:
                    text = self._mapping_optional(item_mapping, "text")
                    if isinstance(text, str) and text.strip():
                        return text.strip()
        return None

    def _extract_abstract(self, markdown: str) -> str | None:
        match = _ABSTRACT_BLOCK_PATTERN.search(markdown)
        if match is None:
            return None
        abstract = match.group("abstract").strip()
        if abstract.endswith("\n#"):
            abstract = abstract[:-2].rstrip()
        return abstract or None

    def _parse_figures_from_content_list(self, payload: object) -> list[ParseFigure]:
        if not isinstance(payload, list):
            return []

        figures: list[ParseFigure] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            item_mapping = self._mapping_from_object(item)
            item_type = self._mapping_optional(item_mapping, "type")
            if item_type not in {"image", "table"}:
                continue

            caption_field = "image_caption" if item_type == "image" else "table_caption"
            caption = self._join_caption(self._mapping_optional(item_mapping, caption_field))
            uri = self._mapping_optional(item_mapping, "img_path")
            figure_id = str(item_type)
            page_idx = self._mapping_optional(item_mapping, "page_idx")
            if isinstance(page_idx, int):
                figure_id = f"{item_type}-p{page_idx + 1}"

            figures.append(
                ParseFigure(
                    figure_id=figure_id,
                    caption=caption,
                    uri=str(uri) if isinstance(uri, str) else None,
                )
            )
        return figures

    def _join_caption(self, value: object) -> str | None:
        if isinstance(value, list):
            parts = [str(item).strip() for item in value if str(item).strip()]
            return " ".join(parts) if parts else None
        if isinstance(value, str) and value.strip():
            return value.strip()
        return None

    def _validate_markdown(self, markdown: str, metadata: ParseMetadata) -> list[str]:
        normalized = markdown.strip()
        if not normalized:
            raise InvalidProviderResponseError("MinerU returned empty markdown")
        if len(normalized) < 40 and "##" not in normalized:
            raise InvalidProviderResponseError("MinerU markdown is too short to be useful")

        warnings: list[str] = []
        if metadata.title is None and _TITLE_PATTERN.search(markdown) is None:
            warnings.append("missing_title")
        if metadata.abstract is None and _ABSTRACT_PATTERN.search(markdown) is None:
            warnings.append("missing_abstract")
        if len(_SECTION_PATTERN.findall(markdown)) < 3:
            warnings.append("insufficient_sections")
        return warnings

    def _build_upload_request_body(self, request: ParseRequest) -> dict[str, object]:
        return {
            "enable_formula": self._config.enable_formula,
            "language": self._config.language,
            "enable_table": self._config.enable_table,
            "model_version": self._config.model_version,
            "files": [
                {
                    "name": request.pdf_path.name,
                    "is_ocr": self._config.is_ocr,
                    "data_id": request.pdf_path.stem,
                }
            ],
        }

    def _build_remote_request_body(self, request: ParseRequest) -> dict[str, object]:
        assert request.source_url is not None
        return {
            "enable_formula": self._config.enable_formula,
            "language": self._config.language,
            "enable_table": self._config.enable_table,
            "model_version": self._config.model_version,
            "files": [
                {
                    "url": request.source_url,
                    "is_ocr": self._config.is_ocr,
                    "data_id": request.pdf_path.stem,
                }
            ],
        }

    async def _upload_file(self, upload_url: str, pdf_path: Path, batch_id: str) -> None:
        attempts = self._config.max_retries + 1
        body = pdf_path.read_bytes()
        last_rate_limit_error: RateLimitExhaustedError | None = None

        for attempt in range(1, attempts + 1):
            try:
                response = await self._get_client().put(upload_url, content=body, headers={})
            except httpx.TimeoutException:
                if attempt == attempts:
                    raise
                continue
            except httpx.HTTPError:
                if attempt == attempts:
                    raise
                continue

            if response.status_code == 429:
                last_rate_limit_error = RateLimitExhaustedError(
                    f"MinerU upload rate limit exhausted after {attempt} attempts",
                    task_id=batch_id,
                )
                if attempt == attempts:
                    break
                continue

            if response.status_code >= 500:
                if attempt == attempts:
                    response.raise_for_status()
                continue

            response.raise_for_status()
            return

        if last_rate_limit_error is not None:
            raise last_rate_limit_error

        raise InvalidProviderResponseError(
            "MinerU upload exhausted retries without a valid response",
            task_id=batch_id,
        )

    async def _request_enveloped_json(
        self,
        method: str,
        path: str,
        *,
        task_id: str | None = None,
        json: dict[str, object] | None = None,
    ) -> dict[str, object]:
        payload = await self._request_json(method, path, task_id=task_id, json=json)
        code = payload.get("code")
        if code != 0:
            msg = payload.get("msg")
            raise ProviderRejectedError(
                task_id=task_id or "unknown",
                message=f"MinerU API returned non-zero code {code}: {msg}",
                retryable=False,
            )

        data = payload.get("data")
        if not isinstance(data, dict):
            raise InvalidProviderResponseError(
                "MinerU response data must be a JSON object",
                task_id=task_id,
            )
        return {str(key): value for key, value in data.items()}

    async def _request_json(
        self,
        method: str,
        path: str,
        *,
        task_id: str | None = None,
        json: dict[str, object] | None = None,
    ) -> dict[str, Any]:
        attempts = self._config.max_retries + 1
        last_rate_limit_error: RateLimitExhaustedError | None = None

        for attempt in range(1, attempts + 1):
            try:
                response = await self._get_client().request(
                    method,
                    path,
                    headers=self._headers(),
                    json=json,
                )
            except httpx.TimeoutException:
                if attempt == attempts:
                    raise
                continue
            except httpx.HTTPError:
                if attempt == attempts:
                    raise
                continue

            if response.status_code == 429:
                last_rate_limit_error = RateLimitExhaustedError(
                    f"MinerU rate limit exhausted after {attempt} attempts",
                    task_id=task_id,
                )
                if attempt == attempts:
                    break
                continue

            if response.status_code >= 500:
                if attempt == attempts:
                    response.raise_for_status()
                continue

            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise InvalidProviderResponseError(
                    "MinerU response must be a JSON object",
                    task_id=task_id,
                )
            return payload

        if last_rate_limit_error is not None:
            raise last_rate_limit_error

        raise InvalidProviderResponseError(
            "MinerU request exhausted retries without a valid response",
            task_id=task_id,
        )

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._config.api_key}"}

    def _get_client(self) -> httpx.AsyncClient:
        if self._http_client is not None:
            return self._http_client
        self._http_client = httpx.AsyncClient(
            base_url=self._config.base_url,
            timeout=self._config.timeout_seconds,
        )
        return self._http_client

    def _find_archive_member(self, archive: zipfile.ZipFile, suffix: str) -> str:
        member = self._find_optional_archive_member(archive, (suffix,))
        if member is None:
            raise KeyError(suffix)
        return member

    def _find_optional_archive_member(
        self,
        archive: zipfile.ZipFile,
        suffixes: tuple[str, ...],
    ) -> str | None:
        for name in archive.namelist():
            lowered = name.lower()
            if any(lowered.endswith(suffix.lower()) for suffix in suffixes):
                return name
        return None

    def _extract_required_mapping(
        self,
        payload: dict[str, object],
        candidates: tuple[str, ...],
        *,
        task_id: str | None = None,
    ) -> dict[str, object]:
        value = self._extract_optional_value(payload, candidates)
        if not isinstance(value, dict):
            joined = ", ".join(candidates)
            raise InvalidProviderResponseError(
                f"MinerU response is missing required object field: {joined}",
                task_id=task_id,
            )
        return {str(key): item for key, item in value.items()}

    def _extract_required_list(
        self,
        payload: dict[str, object],
        candidates: tuple[str, ...],
        *,
        task_id: str | None = None,
    ) -> list[object]:
        value = self._extract_optional_value(payload, candidates)
        if not isinstance(value, list):
            joined = ", ".join(candidates)
            raise InvalidProviderResponseError(
                f"MinerU response is missing required list field: {joined}",
                task_id=task_id,
            )
        return [item for item in value]

    def _extract_required_str(
        self,
        payload: dict[str, object],
        candidates: tuple[str, ...],
        *,
        task_id: str | None = None,
    ) -> str:
        value = self._extract_optional_value(payload, candidates)
        if value is None or str(value).strip() == "":
            joined = ", ".join(candidates)
            raise InvalidProviderResponseError(
                f"MinerU response is missing required string field: {joined}",
                task_id=task_id,
            )
        return str(value)

    def _extract_optional_str(
        self,
        payload: dict[str, object],
        candidates: tuple[str, ...],
    ) -> str | None:
        value = self._extract_optional_value(payload, candidates)
        if value is None:
            return None
        return str(value)

    def _extract_optional_value(
        self,
        payload: dict[str, object] | None,
        candidates: tuple[str, ...],
    ) -> object | None:
        if payload is None:
            return None

        for candidate in candidates:
            current: object = payload
            found = True
            for segment in candidate.split("."):
                if not isinstance(current, dict):
                    found = False
                    break
                current_mapping = self._mapping_from_object(current)
                if segment not in current_mapping:
                    found = False
                    break
                current = current_mapping[segment]
            if found:
                return current
        return None

    def _mapping_from_object(self, value: object) -> dict[str, object]:
        if not isinstance(value, dict):
            raise InvalidProviderResponseError("Expected a JSON object in MinerU payload")
        return {str(key): item for key, item in value.items()}

    def _mapping_optional(self, mapping: dict[str, object], key: str) -> object | None:
        if key in mapping:
            return mapping[key]
        return None


class InvalidProviderResponseError(RuntimeError):
    def __init__(self, message: str, *, task_id: str | None = None) -> None:
        super().__init__(message)
        self.task_id = task_id


class RateLimitExhaustedError(RuntimeError):
    def __init__(self, message: str, *, task_id: str | None = None) -> None:
        super().__init__(message)
        self.task_id = task_id


class ProviderRejectedError(RuntimeError):
    def __init__(self, *, task_id: str, message: str, retryable: bool) -> None:
        super().__init__(message)
        self.task_id = task_id
        self.retryable = retryable


def _parse_bool_env(name: str, *, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise MinerUConfigurationError(f"Invalid boolean value for {name}: {value}")
