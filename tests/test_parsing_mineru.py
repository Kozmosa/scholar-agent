from __future__ import annotations

import asyncio
import io
import json
import zipfile
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


def test_mineru_client_successful_local_upload_batch_parse(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"remote pdf")
    status_calls = 0
    uploaded_payloads: list[bytes] = []
    archive_bytes = _build_result_archive(
        markdown="# Paper\n\n## Abstract\n\nsummary\n\n## Method\n\nm\n\n## Results\n\nr",
        content_list=[
            {
                "type": "image",
                "page_idx": 0,
                "image_caption": ["Figure 1. Overview"],
                "img_path": "images/fig1.png",
            }
        ],
    )

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal status_calls
        if request.method == "POST" and request.url.path == "/api/v4/file-urls/batch":
            assert request.headers["Authorization"] == "Bearer secret"
            return httpx.Response(
                200,
                json={
                    "code": 0,
                    "msg": "ok",
                    "data": {
                        "batch_id": "batch-1",
                        "file_urls": ["https://upload.example.com/object-1"],
                    },
                },
            )
        if request.method == "PUT" and request.url.host == "upload.example.com":
            uploaded_payloads.append(request.content)
            return httpx.Response(200, text="ok")
        if request.method == "GET" and request.url.path == "/api/v4/extract-results/batch/batch-1":
            status_calls += 1
            if status_calls == 1:
                return httpx.Response(
                    200,
                    json={
                        "code": 0,
                        "msg": "ok",
                        "data": {
                            "extract_result": {
                                "state": "running",
                            }
                        },
                    },
                )
            return httpx.Response(
                200,
                json={
                    "code": 0,
                    "msg": "ok",
                    "data": {
                        "extract_result": {
                            "state": "done",
                            "full_zip_url": "https://download.example.com/batch-1.zip",
                        }
                    },
                },
            )
        if request.method == "GET" and request.url.host == "download.example.com":
            return httpx.Response(200, content=archive_bytes)
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
    assert uploaded_payloads == [b"remote pdf"]
    assert result.provider_task_id == "batch-1"
    assert result.metadata.title == "Paper"
    assert result.figures[0].figure_id == "image-p1"
    assert result.figures[0].caption == "Figure 1. Overview"
    assert result.warnings == []


def test_mineru_client_uses_remote_url_batch_endpoint(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"remote-url pdf")
    archive_bytes = _build_result_archive(
        markdown="# Remote\n\n## Method\n\nm\n\n## Results\n\nr\n\n## Extra\n\nx",
        content_list=[],
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST" and request.url.path == "/api/v4/extract/task/batch":
            payload = json.loads(request.content.decode("utf-8"))
            assert payload["files"][0]["url"] == "https://example.com/paper.pdf"
            return httpx.Response(
                200,
                json={
                    "code": 0,
                    "msg": "ok",
                    "data": {"batch_id": "batch-remote"},
                },
            )
        if request.method == "GET" and request.url.path == "/api/v4/extract-results/batch/batch-remote":
            return httpx.Response(
                200,
                json={
                    "code": 0,
                    "msg": "ok",
                    "data": {
                        "extract_result": {
                            "state": "done",
                            "full_zip_url": "https://download.example.com/remote.zip",
                        }
                    },
                },
            )
        if request.method == "GET" and request.url.host == "download.example.com":
            return httpx.Response(200, content=archive_bytes)
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

    result = asyncio.run(
        client.parse_pdf(
            ParseRequest(pdf_path=pdf_path, source_url="https://example.com/paper.pdf")
        )
    )

    assert isinstance(result, ParseResult)
    assert result.provider_task_id == "batch-remote"
    assert result.metadata.source_url == "https://example.com/paper.pdf"
    assert "missing_abstract" in result.warnings


def test_mineru_client_returns_provider_failure(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"bad remote pdf")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return httpx.Response(
                200,
                json={
                    "code": 0,
                    "msg": "ok",
                    "data": {"batch_id": "batch-2", "file_urls": ["https://upload.example.com/object"]},
                },
            )
        if request.method == "PUT":
            return httpx.Response(200)
        return httpx.Response(
            200,
            json={
                "code": 0,
                "msg": "ok",
                "data": {
                    "extract_result": {
                        "state": "failed",
                        "err_msg": "PDF corrupted",
                    }
                },
            },
        )

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
    assert result.provider_task_id == "batch-2"


def test_mineru_client_retries_rate_limit_then_succeeds(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"rate limited pdf")
    submit_attempts = 0
    archive_bytes = _build_result_archive(
        markdown="# Paper\n\n## Method\n\nm\n\n## Results\n\nr\n\n## Extra\n\nx",
        content_list=[],
    )

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal submit_attempts
        if request.method == "POST" and request.url.path == "/api/v4/file-urls/batch":
            submit_attempts += 1
            if submit_attempts < 3:
                return httpx.Response(429, json={"msg": "slow down"})
            return httpx.Response(
                200,
                json={
                    "code": 0,
                    "msg": "ok",
                    "data": {"batch_id": "batch-3", "file_urls": ["https://upload.example.com/object"]},
                },
            )
        if request.method == "PUT":
            return httpx.Response(200)
        if request.method == "GET" and request.url.path == "/api/v4/extract-results/batch/batch-3":
            return httpx.Response(
                200,
                json={
                    "code": 0,
                    "msg": "ok",
                    "data": {
                        "extract_result": {
                            "state": "done",
                            "full_zip_url": "https://download.example.com/batch-3.zip",
                        }
                    },
                },
            )
        if request.method == "GET" and request.url.host == "download.example.com":
            return httpx.Response(200, content=archive_bytes)
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
        return httpx.Response(429, json={"msg": "slow down"})

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
    archive_bytes = _build_result_archive(
        markdown="# Paper\n\n## Method\n\nm\n\n## Results\n\nr\n\n## Extra\n\nx",
        content_list=[],
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return httpx.Response(
                200,
                json={
                    "code": 0,
                    "msg": "ok",
                    "data": {"batch_id": "batch-4", "file_urls": ["https://upload.example.com/object"]},
                },
            )
        if request.method == "PUT":
            return httpx.Response(200)
        if request.method == "GET" and request.url.path == "/api/v4/extract-results/batch/batch-4":
            return httpx.Response(
                200,
                json={
                    "code": 0,
                    "msg": "ok",
                    "data": {
                        "extract_result": {
                            "state": "done",
                            "full_zip_url": "https://download.example.com/batch-4.zip",
                        }
                    },
                },
            )
        if request.method == "GET" and request.url.host == "download.example.com":
            return httpx.Response(200, content=archive_bytes)
        raise AssertionError(f"Unexpected request: {request.method} {request.url}")

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


def test_mineru_client_returns_invalid_response_for_bad_archive(tmp_path: Path) -> None:
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"bad archive")

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return httpx.Response(
                200,
                json={
                    "code": 0,
                    "msg": "ok",
                    "data": {"batch_id": "batch-5", "file_urls": ["https://upload.example.com/object"]},
                },
            )
        if request.method == "PUT":
            return httpx.Response(200)
        if request.method == "GET" and request.url.path == "/api/v4/extract-results/batch/batch-5":
            return httpx.Response(
                200,
                json={
                    "code": 0,
                    "msg": "ok",
                    "data": {
                        "extract_result": {
                            "state": "done",
                            "full_zip_url": "https://download.example.com/batch-5.zip",
                        }
                    },
                },
            )
        if request.method == "GET" and request.url.host == "download.example.com":
            return httpx.Response(200, content=b"not-a-zip")
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

    assert isinstance(result, ParseFailure)
    assert result.failure_type is ParseFailureType.INVALID_RESPONSE


def _build_result_archive(markdown: str, content_list: list[dict[str, object]]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("results/full.md", markdown)
        archive.writestr("results/content_list.json", json.dumps(content_list))
    return buffer.getvalue()
