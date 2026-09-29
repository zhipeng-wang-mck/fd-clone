#!/usr/bin/env python3
"""Convert a document to markdown.

Pandoc handles most formats. PDF and Excel use custom extractors because
pandoc cannot read them reliably.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import pypandoc
except ImportError:
    print("ERROR: pypandoc not installed. Run scripts/setup.py first.", file=sys.stderr)
    sys.exit(1)

PANDOC_READERS = {
    ".docx": "docx",
    ".pptx": "pptx",
    ".odt": "odt",
    ".rtf": "rtf",
    ".epub": "epub",
    ".rst": "rst",
    ".org": "org",
    ".tex": "latex",
    ".adoc": "asciidoc",
    ".asciidoc": "asciidoc",
    ".ipynb": "ipynb",
    ".csv": "csv",
    ".tsv": "tsv",
    ".jira": "jira",
    ".textile": "textile",
    ".mediawiki": "mediawiki",
    ".typ": "typst",
    ".txt": "markdown",
    ".text": "markdown",
}

PASSTHROUGH = {".md", ".markdown"}
CUSTOM = {".pdf", ".xlsx", ".xlsm"}
PANDOC_ARGS = ["--wrap=none", "--markdown-headings=atx"]


def supported_suffixes():
    return sorted(PASSTHROUGH | PANDOC_READERS.keys() | CUSTOM)


def to_markdown(path: Path) -> tuple[str, list[str]]:
    """Return (markdown, notes)."""
    suffix = path.suffix.casefold()

    if suffix in PASSTHROUGH:
        return path.read_text(encoding="utf-8"), []

    if suffix == ".pdf":
        try:
            from .pdf import pdf_to_markdown
        except ImportError:
            from pdf import pdf_to_markdown
        return pdf_to_markdown(path)

    if suffix in {".xlsx", ".xlsm"}:
        try:
            from .xlsx import xlsx_to_markdown
        except ImportError:
            from xlsx import xlsx_to_markdown
        return xlsx_to_markdown(path)

    reader = PANDOC_READERS.get(suffix)
    if reader is None:
        raise ValueError(
            f"No converter for '{suffix}'. Supported: {', '.join(supported_suffixes())}"
        )

    return pypandoc.convert_file(
        str(path), to="gfm", format=reader, extra_args=PANDOC_ARGS
    ), [f"Converted from {reader} via pandoc"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Source document path")
    parser.add_argument("--out", type=Path, help="Output markdown file path")
    parser.add_argument("--stdout", action="store_true", help="Print to stdout")
    args = parser.parse_args()

    if not args.source.exists():
        print(f"ERROR: source not found: {args.source}", file=sys.stderr)
        sys.exit(1)

    markdown, notes = to_markdown(args.source)
    if args.stdout:
        print(markdown)
    else:
        out = args.out or args.source.with_suffix(".md")
        out.write_text(markdown, encoding="utf-8")
        print(out)
    for note in notes:
        print(f"note: {note}", file=sys.stderr)


if __name__ == "__main__":
    main()
