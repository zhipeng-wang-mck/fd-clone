"""Strip page chrome from HTML before pandoc converts it.

Wiki and intranet exports wrap the document in navigation, headers, footers
and sidebars. Pandoc keeps that text, and keeps layout <div>/<span> wrappers
as raw HTML in GFM output. This removes chrome elements up front and has
pandoc unwrap the remaining divs and spans, so only the document body is left.
"""
from __future__ import annotations

import re
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

import pypandoc

CHROME_TAGS = {"header", "nav", "footer", "aside", "script", "style", "noscript", "template"}
CHROME_TOKENS = {
    "header", "site-header", "page-header", "masthead",
    "footer", "site-footer", "page-footer",
    "nav", "navbar", "navigation", "menu",
    "breadcrumb", "breadcrumbs",
    "sidebar", "toolbar", "cookie-banner",
}
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "source", "track", "wbr",
}
PANDOC_FORMAT = "html-native_divs-native_spans"
PANDOC_ARGS = ["--wrap=none", "--markdown-headings=atx"]
_TOKEN_SPLIT = re.compile(r"\s+")


def _is_chrome(tag: str, attrs: list[tuple[str, str | None]]) -> bool:
    if tag in CHROME_TAGS:
        return True
    tokens: set[str] = set()
    for name, value in attrs:
        if name in {"class", "id", "role"} and value:
            tokens.update(t.casefold() for t in _TOKEN_SPLIT.split(value) if t)
    if "navigation" in tokens or "contentinfo" in tokens or "banner" in tokens:
        return True
    return bool(tokens & CHROME_TOKENS)


class _ChromeStripper(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.out: list[str] = []
        self.dropped: list[str] = []
        self._skip_tag: str | None = None
        self._skip_depth = 0
        self._skip_text: list[str] = []

    def _emit(self, text: str) -> None:
        if self._skip_tag is None:
            self.out.append(text)
        else:
            self._skip_text.append(text)

    def handle_starttag(self, tag, attrs):
        if self._skip_tag is not None:
            if tag == self._skip_tag:
                self._skip_depth += 1
            return
        if tag not in VOID_TAGS and _is_chrome(tag, attrs):
            self._skip_tag = tag
            self._skip_depth = 1
            self._skip_text = []
            return
        self.out.append(self.get_starttag_text() or "")

    def handle_startendtag(self, tag, attrs):
        if self._skip_tag is None:
            self.out.append(self.get_starttag_text() or "")

    def handle_endtag(self, tag):
        if self._skip_tag is not None:
            if tag == self._skip_tag:
                self._skip_depth -= 1
                if self._skip_depth == 0:
                    text = " ".join(unescape("".join(self._skip_text)).split())
                    self.dropped.append(f"<{tag}>" + (f": {text[:80]}" if text else ""))
                    self._skip_tag = None
            return
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        self._emit(data)

    def handle_entityref(self, name):
        self._emit(f"&{name};")

    def handle_charref(self, name):
        self._emit(f"&#{name};")

    def handle_decl(self, decl):
        self._emit(f"<!{decl}>")

    def handle_comment(self, data):
        pass


def strip_chrome(html: str) -> tuple[str, list[str]]:
    """Return (html without chrome elements, description of each dropped element)."""
    parser = _ChromeStripper()
    parser.feed(html)
    parser.close()
    return "".join(parser.out), parser.dropped


def html_to_markdown(path: Path) -> tuple[str, list[str]]:
    html = path.read_text(encoding="utf-8", errors="replace")
    cleaned, dropped = strip_chrome(html)
    markdown = pypandoc.convert_text(
        cleaned, to="gfm", format=PANDOC_FORMAT, extra_args=PANDOC_ARGS
    )
    notes = ["Converted from html via pandoc"]
    notes.extend(f"Dropped page chrome {item}" for item in dropped)
    return markdown, notes
