from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
LEGACY_ENTRY = ROOT / "wymagania_edukacyjne_ZSZ5_2026_2027.html"
CATALOG = ROOT / "katalog_podstaw_programowych_ZSZ5_2026_2027.html"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        values = dict(attrs)
        href = values.get("href")
        if href:
            self.hrefs.append(href)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_html(path: Path) -> str:
    if not path.exists():
        fail(f"Missing HTML file: {path.relative_to(ROOT)}")
    html = path.read_text(encoding="utf-8")
    LinkParser().feed(html)
    return html


def local_href_missing(html: str) -> list[str]:
    parser = LinkParser()
    parser.feed(html)
    missing: list[str] = []
    for href in parser.hrefs:
        if href.startswith(("http://", "https://", "#", "mailto:")):
            continue
        path = unquote(href.split("#", 1)[0].split("?", 1)[0])
        if path and not (ROOT / path).exists():
            missing.append(path)
    return missing


def main() -> None:
    index_html = read_html(INDEX)
    legacy_html = read_html(LEGACY_ENTRY)
    catalog_html = read_html(CATALOG)

    required_index_markers = [
        "Przewodnik dla nauczyciela ZSZ5 2026/2027",
        "Od podstawy programowej do wymagań na oceny",
        "Rozkład materiału - po co jest potrzebny",
        "Przykładowy rozkład materiału - szablon i wzór",
        "rozkład materiału - szablon 2026_2027.xlsx",
        "Katalog podstaw programowych ZSZ5",
    ]
    for marker in required_index_markers:
        if marker not in index_html:
            fail(f"Missing current guide marker in index.html: {marker}")

    forbidden_index_markers = [
        "school_technikum",
        "school_bsi",
        "school_bsii",
        "Stan opracowania",
        "35 przedmiotów",
        "10 kierunków zawodowych",
        "Wymagania edukacyjne i biblioteka podstaw programowych",
    ]
    for marker in forbidden_index_markers:
        if marker in index_html:
            fail(f"Legacy visible marker still present in index.html: {marker}")

    if index_html != legacy_html:
        fail("Legacy entry HTML no longer matches index.html")

    if "Cukiernik (SPC.01)" not in catalog_html:
        fail("Catalog does not contain Cukiernik (SPC.01)")
    if "01_BSI_stopnia/zawodowe/PP_cukiernik_SPC01.pdf" not in catalog_html:
        fail("Catalog does not link the local cukiernik PDF")

    for path_name, html in [("index.html", index_html), ("catalog", catalog_html)]:
        missing = local_href_missing(html)
        if missing:
            fail(f"Missing local hrefs in {path_name}: {', '.join(missing[:10])}")

    print("Guide page validation OK")


if __name__ == "__main__":
    main()
