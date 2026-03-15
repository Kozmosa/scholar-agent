from __future__ import annotations

import json
from pathlib import Path

import pytest

from ainrf.parsing import CacheError
from ainrf.parsing import ParseCache, ParseMetadata, ParseResult


def test_parse_cache_round_trip(tmp_path: Path) -> None:
    cache = ParseCache(tmp_path)
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"fake pdf")
    pdf_sha256 = cache.compute_pdf_sha256(pdf_path)

    result = ParseResult(
        markdown="# Title\n\n## Abstract\n\ntext\n\n## Method\n\ntext\n\n## Results\n\ntext",
        metadata=ParseMetadata(
            title="Title",
            authors=["Alice", "Bob"],
            abstract="Summary",
            file_name="paper.pdf",
        ),
        provider_task_id="task-1",
        warnings=["missing_title"],
    )

    cache.save(pdf_sha256, result)
    loaded = cache.load(pdf_sha256)

    assert loaded is not None
    assert loaded.cache_hit is True
    assert loaded.markdown == result.markdown
    assert loaded.metadata.title == "Title"
    assert loaded.metadata.authors == ["Alice", "Bob"]
    assert loaded.provider_task_id == "task-1"


def test_parse_cache_invalidate_removes_record(tmp_path: Path) -> None:
    cache = ParseCache(tmp_path)
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"fake pdf")
    pdf_sha256 = cache.compute_pdf_sha256(pdf_path)

    cache.save(
        pdf_sha256,
        ParseResult(
            markdown="# Title\n\n## Abstract\n\ntext",
            metadata=ParseMetadata(title="Title"),
        ),
    )

    cache.invalidate(pdf_sha256)

    assert cache.load(pdf_sha256) is None


def test_parse_cache_load_invalid_json_raises(tmp_path: Path) -> None:
    cache = ParseCache(tmp_path)
    cache_path = tmp_path / ("a" * 64 + ".json")
    cache_path.write_text("{broken", encoding="utf-8")

    with pytest.raises(CacheError):
        cache.load("a" * 64)


def test_parse_cache_stores_json_record(tmp_path: Path) -> None:
    cache = ParseCache(tmp_path)
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"fake pdf")
    pdf_sha256 = cache.compute_pdf_sha256(pdf_path)

    cache.save(
        pdf_sha256,
        ParseResult(
            markdown="# Title",
            metadata=ParseMetadata(title="Title", file_name="paper.pdf"),
        ),
    )

    payload = json.loads((tmp_path / f"{pdf_sha256}.json").read_text(encoding="utf-8"))

    assert payload["pdf_sha256"] == pdf_sha256
    assert payload["result"]["metadata"]["file_name"] == "paper.pdf"
