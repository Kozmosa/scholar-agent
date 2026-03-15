from __future__ import annotations

import asyncio
from pathlib import Path

import httpx

from ainrf.parsing import (
    MinerUClient,
    MinerUConfig,
    ParseCache,
    ParseFailure,
    ParseFailureType,
    ParseMetadata,
    ParseRequest,
    ParseResult,
)


def test_mineru_client_returns_cached_result_without_remote_call(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"cached pdf")
    cache = ParseCache(tmp_path / "cache")
    pdf_sha256 = cache.compute_pdf_sha256(pdf_path)
    cache.save(
        pdf_sha256,
        ParseResult(
            markdown="# Cached\n\n## Abstract\n\ntext\n\n## Method\n\ntext\n\n## Results\n\ntext",
            metadata=ParseMetadata(title="Cached"),
        ),
    )

    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError(f"Unexpected remote request: {request.method} {request.url}")

    client = MinerUClient(
        MinerUConfig(base_url="https://mineru.example", api_key="secret", cache_dir=cache.cache_dir),
        cache=cache,
        http_client=httpx.AsyncClient(
            base_url="https://mineru.example",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = asyncio.run(client.parse_pdf(ParseRequest(pdf_path=pdf_path)))

    assert isinstance(result, ParseResult)
    assert result.cache_hit is True
    assert result.markdown.startswith("# Cached")


def test_mineru_client_successful_parse_round_trip(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"remote pdf")
    status_calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal status_calls
        if request.method == "POST" and request.url.path == "/v1/tasks":
            return httpx.Response(200, json={"task_id": "task-1"})
        if request.method == "GET" and request.url.path == "/v1/tasks/task-1":
            status_calls += 1
            if status_calls == 1:
                return httpx.Response(200, json={"status": "processing"})
            return httpx.Response(
                200,
                json={
                    "status": "completed",
                    "result": {
                        "markdown": (
                            "# Paper\n\n## Abstract\n\nsummary\n\n## Method\n\nm\n\n## Results\n\nr"
                        ),
                        "metadata": {
                            "title": "Paper",
                            "authors": ["Alice"],
                            "abstract": "summary",
                        },
                        "figures": [{"id": "fig-1", "caption": "Overview", "url": "s3://fig"}],
                    },
                },
            )
        raise AssertionError(f"Unexpected request: {request.method} {request.url}")

    client = MinerUClient(
        MinerUConfig(
            base_url="https://mineru.example",
            api_key="secret",
            poll_interval_seconds=0,
            cache_dir=tmp_path / "cache",
        ),
        http_client=httpx.AsyncClient(
            base_url="https://mineru.example",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = asyncio.run(client.parse_pdf(ParseRequest(pdf_path=pdf_path)))

    assert isinstance(result, ParseResult)
    assert result.provider_task_id == "task-1"
    assert result.metadata.title == "Paper"
    assert result.figures[0].figure_id == "fig-1"
    assert result.warnings == []


def test_mineru_client_returns_provider_failure(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"bad remote pdf")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return httpx.Response(200, json={"task_id": "task-2"})
        return httpx.Response(200, json={"status": "failed", "message": "PDF corrupted"})

    client = MinerUClient(
        MinerUConfig(
            base_url="https://mineru.example",
            api_key="secret",
            poll_interval_seconds=0,
            cache_dir=tmp_path / "cache",
        ),
        http_client=httpx.AsyncClient(
            base_url="https://mineru.example",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = asyncio.run(client.parse_pdf(ParseRequest(pdf_path=pdf_path)))

    assert isinstance(result, ParseFailure)
    assert result.failure_type is ParseFailureType.PROVIDER_REJECTED
    assert result.provider_task_id == "task-2"


def test_mineru_client_retries_rate_limit_then_succeeds(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"rate limited pdf")
    submit_attempts = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal submit_attempts
        if request.method == "POST":
            submit_attempts += 1
            if submit_attempts < 3:
                return httpx.Response(429, json={"message": "slow down"})
            return httpx.Response(200, json={"task_id": "task-3"})
        if request.url.path == "/v1/tasks/task-3":
            return httpx.Response(
                200,
                json={
                    "status": "completed",
                    "result": {
                        "markdown": "# Paper\n\n## Method\n\nm\n\n## Results\n\nr\n\n## Extra\n\nx",
                        "metadata": {"title": "Paper"},
                    },
                },
            )
        raise AssertionError(f"Unexpected request: {request.method} {request.url}")

    client = MinerUClient(
        MinerUConfig(
            base_url="https://mineru.example",
            api_key="secret",
            max_retries=2,
            poll_interval_seconds=0,
            cache_dir=tmp_path / "cache",
        ),
        http_client=httpx.AsyncClient(
            base_url="https://mineru.example",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = asyncio.run(client.parse_pdf(ParseRequest(pdf_path=pdf_path)))

    assert isinstance(result, ParseResult)
    assert submit_attempts == 3
    assert "missing_abstract" in result.warnings


def test_mineru_client_returns_rate_limit_exhausted(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"rate limited forever")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"message": "slow down"})

    client = MinerUClient(
        MinerUConfig(
            base_url="https://mineru.example",
            api_key="secret",
            max_retries=1,
            cache_dir=tmp_path / "cache",
        ),
        http_client=httpx.AsyncClient(
            base_url="https://mineru.example",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = asyncio.run(client.parse_pdf(ParseRequest(pdf_path=pdf_path)))

    assert isinstance(result, ParseFailure)
    assert result.failure_type is ParseFailureType.RATE_LIMIT_EXHAUSTED


def test_mineru_client_maps_timeout_to_failure(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"timeout pdf")

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("boom", request=request)

    client = MinerUClient(
        MinerUConfig(
            base_url="https://mineru.example",
            api_key="secret",
            max_retries=0,
            cache_dir=tmp_path / "cache",
        ),
        http_client=httpx.AsyncClient(
            base_url="https://mineru.example",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = asyncio.run(client.parse_pdf(ParseRequest(pdf_path=pdf_path)))

    assert isinstance(result, ParseFailure)
    assert result.failure_type is ParseFailureType.TIMEOUT


def test_mineru_client_invalid_cache_is_rebuilt(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"rebuild cache")
    cache = ParseCache(tmp_path / "cache")
    pdf_sha256 = cache.compute_pdf_sha256(pdf_path)
    cache.cache_dir.mkdir(parents=True, exist_ok=True)
    (cache.cache_dir / f"{pdf_sha256}.json").write_text("{broken", encoding="utf-8")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return httpx.Response(200, json={"task_id": "task-4"})
        return httpx.Response(
            200,
            json={
                "status": "completed",
                "result": {
                    "markdown": "# Paper\n\n## Method\n\nm\n\n## Results\n\nr\n\n## Extra\n\nx",
                    "metadata": {"title": "Paper"},
                },
            },
        )

    client = MinerUClient(
        MinerUConfig(
            base_url="https://mineru.example",
            api_key="secret",
            poll_interval_seconds=0,
            cache_dir=cache.cache_dir,
        ),
        cache=cache,
        http_client=httpx.AsyncClient(
            base_url="https://mineru.example",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = asyncio.run(client.parse_pdf(ParseRequest(pdf_path=pdf_path)))

    assert isinstance(result, ParseResult)
    rebuilt = cache.load(pdf_sha256)
    assert rebuilt is not None
    assert rebuilt.cache_hit is True


def test_mineru_client_returns_invalid_response_for_empty_markdown(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"empty markdown")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return httpx.Response(200, json={"task_id": "task-5"})
        return httpx.Response(200, json={"status": "completed", "result": {"markdown": " "}})

    client = MinerUClient(
        MinerUConfig(
            base_url="https://mineru.example",
            api_key="secret",
            poll_interval_seconds=0,
            cache_dir=tmp_path / "cache",
        ),
        http_client=httpx.AsyncClient(
            base_url="https://mineru.example",
            transport=httpx.MockTransport(handler),
        ),
    )

    result = asyncio.run(client.parse_pdf(ParseRequest(pdf_path=pdf_path)))

    assert isinstance(result, ParseFailure)
    assert result.failure_type is ParseFailureType.INVALID_RESPONSE
