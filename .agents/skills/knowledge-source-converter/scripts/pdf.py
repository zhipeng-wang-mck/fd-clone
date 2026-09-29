"""Extract text from PDF into markdown.

PDFs have no native structure for a playbook, so this extracts plain text
per page and joins it with page breaks. Tables in PDFs are not reliably
converted to markdown tables.

Repeated running headers/footers (library name, CONFIDENTIAL, Page N)
are dropped so they do not leak into the knowledge draft. The document
title is kept as a level-1 heading when the source carries one: a running
header that opens page 1, otherwise the PDF metadata title.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

_PAGE_NUM = re.compile(r"^Page\s+\d+$", re.I)
_CONFIDENTIAL = re.compile(r"^CONFIDENTIAL$", re.I)


def _norm(line: str) -> str:
    return " ".join(line.split())


def _page_lines(text: str) -> list[str]:
    return [_norm(line) for line in text.splitlines() if _norm(line)]


def _repeating_chrome(pages: list[list[str]]) -> set[str]:
    if len(pages) < 2:
        return set()
    counts = Counter()
    for page in pages:
        for line in set(page):
            counts[line] += 1
    return {line for line, n in counts.items() if n == len(pages)}


def _is_chrome(line: str, repeating: set[str]) -> bool:
    if line in repeating:
        return True
    if _PAGE_NUM.fullmatch(line) or _CONFIDENTIAL.fullmatch(line):
        return True
    return False


def _source_title(
    pages: list[list[str]], repeating: set[str], metadata_title: str
) -> tuple[str | None, str | None]:
    first = pages[0][0] if pages and pages[0] else None
    banner = first and (_PAGE_NUM.fullmatch(first) or _CONFIDENTIAL.fullmatch(first))
    if first and first in repeating and not banner:
        return first, f"Kept running header '{first}' as the document title"
    if metadata_title and metadata_title != first:
        return metadata_title, f"Used PDF metadata title '{metadata_title}'"
    return None, None


def pdf_to_markdown(path: Path) -> tuple[str, list[str]]:
    try:
        import fitz  # pymupdf
    except ImportError as exc:
        raise ImportError("PyMuPDF is required for PDF conversion. Run setup.py.") from exc

    doc = fitz.open(str(path))
    metadata_title = _norm((doc.metadata or {}).get("title") or "")
    raw_pages = []
    for page in doc:
        text = page.get_text().strip()
        if text:
            raw_pages.append(_page_lines(text))
    doc.close()

    repeating = _repeating_chrome(raw_pages)
    cleaned = []
    dropped = 0
    for page in raw_pages:
        kept = [line for line in page if not _is_chrome(line, repeating)]
        dropped += len(page) - len(kept)
        if kept:
            cleaned.append("\n".join(kept))

    notes = [f"Converted from PDF with PyMuPDF, {len(raw_pages)} page(s)"]
    if dropped:
        notes.append(f"Dropped {dropped} repeated header/footer line(s)")
    title, title_note = _source_title(raw_pages, repeating, metadata_title)
    if title:
        cleaned.insert(0, f"# {title}")
        notes.append(title_note)
    return "\n\n".join(cleaned), notes
