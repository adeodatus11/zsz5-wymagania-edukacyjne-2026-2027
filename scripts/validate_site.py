from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "podstawy_programowe.json"
HTML = ROOT / "wymagania_edukacyjne_ZSZ5_2026_2027.html"
INDEX = ROOT / "index.html"


class Parser(HTMLParser):
    pass


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not MANIFEST.exists():
        fail(f"Missing manifest: {MANIFEST}")
    if not HTML.exists():
        fail(f"Missing HTML: {HTML}")
    if not INDEX.exists():
        fail(f"Missing index: {INDEX}")

    items = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not items:
        fail("PDF manifest is empty")

    missing = [item["path"] for item in items if not (ROOT / item["path"]).exists()]
    if missing:
        fail("Missing PDF files from manifest: " + ", ".join(missing[:10]))

    html = HTML.read_text(encoding="utf-8")
    Parser().feed(html)
    Parser().close()

    for item in items:
        if item["path"] not in html:
            fail(f"Manifest PDF not linked in HTML: {item['path']}")

    if html.count('type="search"') < 1:
        fail("Search input not found")
    if "Biblioteka podstaw programowych" not in html and "biblioteka podstaw programowych" not in html.lower():
        fail("PDF library label not found")
    if "<td" in html and re.search(r"<td[^>]*>\s*</td>", html):
        fail("Empty grade table cell found")
    for marker in ["X X X", "Cele 1 2", "Wymagania fakultatywne", "Zakres rozszerzony"]:
        if marker in html:
            fail(f"Forbidden extraction marker found: {marker}")

    general = sum(1 for item in items if item["category"] == "ogolne")
    vocational = sum(1 for item in items if item["category"] == "zawodowe")
    print(f"Manifest PDF files: {len(items)}")
    print(f"General PDFs: {general}")
    print(f"Vocational PDFs: {vocational}")
    print("Site validation OK")


if __name__ == "__main__":
    main()
