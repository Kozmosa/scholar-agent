from __future__ import annotations

import asyncio
import os
import re
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


@dataclass(slots=True, frozen=True)
class MinerUConfig:
    base_url: str
    api_key: str
    submit_path: str = "/v1/tasks"
    status_path_template: str = "/v1/tasks/{task_id}"
    result_path_template: str = "/v1/tasks/{task_id}/result"
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

        return cls(
            base_url=base_url,
            api_key=api_key,
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

        if isinstance(result, ParseResult):
            self._cache.save(pdf_sha256, result)

        return result

    async def _parse_via_provider(self, request: ParseRequest) -> ParseResult:
        submit_payload = await self._submit_pdf(request)
        task_id = self._extract_required_str(
            submit_payload,
            ("task_id", "data.task_id", "id", "data.id"),
        )

        terminal_payload = await self._poll_until_terminal(task_id)
        status = self._extract_required_str(
            terminal_payload,
            ("status", "data.status", "state", "data.state"),
        ).lower()

        if status in {"failed", "error", "rejected", "cancelled"}:
            reason = self._extract_optional_str(
                terminal_payload,
                (
                    "message",
                    "error.message",
                    "data.message",
                    "data.error.message",
                    "reason",
                    "data.reason",
                ),
            )
            raise ProviderRejectedError(
                task_id=task_id,
                message=reason or f"MinerU task {task_id} finished with status {status}",
                retryable=status not in {"rejected", "cancelled"},
            )

        result_payload = self._extract_optional_mapping(
            terminal_payload,
            ("result", "data.result", "output", "data.output"),
        )
        if result_payload is None:
            result_payload = await self._fetch_result(task_id)

        return self._normalize_result(result_payload, request, task_id)

    async def _submit_pdf(self, request: ParseRequest) -> dict[str, Any]:
        file_bytes = request.pdf_path.read_bytes()
        files = {"file": (request.pdf_path.name, file_bytes, "application/pdf")}
        data = {}
        if request.source_url is not None:
            data["source_url"] = request.source_url
        if request.role is not None:
            data["role"] = request.role
        return await self._request_json("POST", self._config.submit_path, data=data, files=files)

    async def _poll_until_terminal(self, task_id: str) -> dict[str, Any]:
        deadline = asyncio.get_running_loop().time() + self._config.timeout_seconds
        while True:
            payload = await self._request_json(
                "GET",
                self._config.status_path_template.format(task_id=task_id),
                task_id=task_id,
            )
            status = self._extract_required_str(
                payload,
                ("status", "data.status", "state", "data.state"),
                task_id=task_id,
            ).lower()
            if status in {"completed", "succeeded", "success", "failed", "error", "rejected"}:
                return payload
            if asyncio.get_running_loop().time() >= deadline:
                raise httpx.ReadTimeout(f"MinerU polling timed out for task {task_id}")
            await asyncio.sleep(self._config.poll_interval_seconds)

    async def _fetch_result(self, task_id: str) -> dict[str, Any]:
        return await self._request_json(
            "GET",
            self._config.result_path_template.format(task_id=task_id),
            task_id=task_id,
        )

    async def _request_json(
        self,
        method: str,
        path: str,
        *,
        task_id: str | None = None,
        data: dict[str, str] | None = None,
        files: dict[str, tuple[str, bytes, str]] | None = None,
    ) -> dict[str, Any]:
        attempts = self._config.max_retries + 1
        last_rate_limit_error: RateLimitExhaustedError | None = None

        for attempt in range(1, attempts + 1):
            try:
                response = await self._get_client().request(
                    method,
                    path,
                    headers=self._headers(),
                    data=data,
                    files=files,
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

    def _normalize_result(
        self,
        payload: dict[str, Any],
        request: ParseRequest,
        task_id: str,
    ) -> ParseResult:
        markdown = self._extract_required_str(
            payload,
            ("markdown", "data.markdown", "content.markdown", "result.markdown"),
            task_id=task_id,
        )
        metadata_payload = self._extract_optional_mapping(
            payload,
            ("metadata", "data.metadata", "content.metadata", "result.metadata"),
        )
        figures_payload = self._extract_optional_list(
            payload,
            ("figures", "data.figures", "content.figures", "result.figures"),
        )

        metadata = ParseMetadata(
            title=self._extract_optional_str_from_mapping(metadata_payload, ("title",)),
            authors=self._extract_str_list_from_mapping(metadata_payload, ("authors",)),
            abstract=self._extract_optional_str_from_mapping(metadata_payload, ("abstract",)),
            source_url=request.source_url
            or self._extract_optional_str_from_mapping(metadata_payload, ("source_url",)),
            file_name=request.pdf_path.name,
        )
        figures = self._parse_figures(figures_payload)
        warnings = self._validate_markdown(markdown, metadata)

        return ParseResult(
            markdown=markdown,
            metadata=metadata,
            figures=figures,
            provider_task_id=task_id,
            warnings=warnings,
        )

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

    def _parse_figures(self, payload: list[Any] | None) -> list[ParseFigure]:
        if payload is None:
            return []

        figures: list[ParseFigure] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            figures.append(
                ParseFigure(
                    figure_id=self._optional_str(item.get("figure_id") or item.get("id")),
                    caption=self._optional_str(item.get("caption")),
                    uri=self._optional_str(item.get("uri") or item.get("url")),
                )
            )
        return figures

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

    def _extract_required_str(
        self,
        payload: dict[str, Any],
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
        payload: dict[str, Any],
        candidates: tuple[str, ...],
    ) -> str | None:
        value = self._extract_optional_value(payload, candidates)
        return self._optional_str(value)

    def _extract_optional_mapping(
        self,
        payload: dict[str, Any],
        candidates: tuple[str, ...],
    ) -> dict[str, Any] | None:
        value = self._extract_optional_value(payload, candidates)
        if isinstance(value, dict):
            return value
        return None

    def _extract_optional_list(
        self,
        payload: dict[str, Any],
        candidates: tuple[str, ...],
    ) -> list[Any] | None:
        value = self._extract_optional_value(payload, candidates)
        if isinstance(value, list):
            return value
        return None

    def _extract_optional_value(
        self,
        payload: dict[str, Any] | None,
        candidates: tuple[str, ...],
    ) -> Any | None:
        if payload is None:
            return None

        for candidate in candidates:
            current: Any = payload
            found = True
            for segment in candidate.split("."):
                if isinstance(current, dict) and segment in current:
                    current = current[segment]
                else:
                    found = False
                    break
            if found:
                return current
        return None

    def _extract_optional_str_from_mapping(
        self,
        payload: dict[str, Any] | None,
        candidates: tuple[str, ...],
    ) -> str | None:
        if payload is None:
            return None
        value = self._extract_optional_value(payload, candidates)
        return self._optional_str(value)

    def _extract_str_list_from_mapping(
        self,
        payload: dict[str, Any] | None,
        candidates: tuple[str, ...],
    ) -> list[str]:
        if payload is None:
            return []
        value = self._extract_optional_value(payload, candidates)
        if not isinstance(value, list):
            return []
        return [str(item) for item in value]

    def _optional_str(self, value: object) -> str | None:
        if value is None:
            return None
        return str(value)


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
