from __future__ import annotations

from typing import Protocol

from ainrf.parsing.models import ParseFailure, ParseRequest, ParseResult


class PaperParser(Protocol):
    async def parse_pdf(self, request: ParseRequest) -> ParseResult | ParseFailure:
        """Parse one PDF into normalized markdown and metadata."""
