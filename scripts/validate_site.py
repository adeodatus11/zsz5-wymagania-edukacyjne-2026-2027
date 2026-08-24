from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "index.html",
    "rozklad_materialu.html",
    "ramowe_plany_nauczania.html",
    "szkolne_zestawy_programow_nauczania.html",
    "adaptacja_programu.html",
    "materialy_i_linki.html",
    "podstawy_prawne.html",
    "wymagania_edukacyjne_ZSZ5_2026_2027.html",
]
CATALOG = ROOT / "katalog_podstaw_programowych_ZSZ5_2026_2027.html"
SCHEDULE_TEMPLATE = "rozkłady materiału przedmiotów/rozkład materiału - szablon 2026_2027.xlsx"
PREVIEW_IMAGES = [
    "assets/rozklad-materialu-wzor.png",
    "assets/rozklad-materialu-szablon.png",
]


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
    page_html = {page: read_html(ROOT / page) for page in PAGES}
    catalog_html = read_html(CATALOG)

    required_by_page = {
        "index.html": [
            "Od podstawy programowej do wymagań na oceny",
            "Ścieżka pracy",
            "Przejdź do rozkładu materiału",
        ],
        "rozklad_materialu.html": [
            "Rozkład materiału",
            SCHEDULE_TEMPLATE,
            "Lekcja organizacyjna. Zapoznanie uczniów z wymaganiami edukacyjnymi i zasadami oceniania",
            "piątku 28 sierpnia 2026 r.",
            "sobotę 29 sierpnia 2026 r.",
            "1 września 2026 r.",
            "assets/rozklad-materialu-wzor.png",
            "assets/rozklad-materialu-szablon.png",
            "Elementy podstawy programowej",
            "Kolekcja po lekcji",
        ],
        "ramowe_plany_nauczania.html": [
            "Ramowe plany nauczania",
            "Wkrótce pojawią się tutaj ramowe plany nauczania",
        ],
        "szkolne_zestawy_programow_nauczania.html": [
            "Szkolne zestawy programów nauczania",
            "Wkrótce pojawią się tutaj szkolne zestawy programów nauczania",
        ],
        "adaptacja_programu.html": ["Adaptacja programu w praktyce"],
        "materialy_i_linki.html": ["Przydatne materiały i linki", "Katalog podstaw programowych"],
        "podstawy_prawne.html": ["Podstawy prawne i źródła"],
    }
    for page, markers in required_by_page.items():
        html = page_html[page]
        for marker in markers:
            if marker not in html:
                fail(f"Missing marker in {page}: {marker}")

    forbidden_markers = [
        "materiał do dalszego opracowania",
        "Robocze tabele",
        "robocze tabele",
        "Na tej stronie zostaje na razie",
        "na tej stronie zostaje na razie",
        "tabele wygenerowane wcześniej przez AI",
        "Nauczyciel robi",
        "Trzeba pilnować",
        "czystą kartą",
        "Co ma być widoczne",
        "Co uzupełnić przed tabelą",
        "Czego unikać",
        "Sztywno trzymamy się",
        "Nie oceniaj",
        "Nie zastępuj",
        "school_technikum",
        "school_bsi",
        "school_bsii",
        "Stan opracowania",
        "35 przedmiotów",
        "10 kierunków zawodowych",
        "Wymagania edukacyjne i biblioteka podstaw programowych",
    ]
    for page, html in page_html.items():
        for marker in forbidden_markers:
            if marker in html:
                fail(f"Forbidden marker in {page}: {marker}")

    for asset in [SCHEDULE_TEMPLATE, *PREVIEW_IMAGES]:
        if not (ROOT / asset).exists():
            fail(f"Missing asset: {asset}")

    for page, html in page_html.items():
        missing = local_href_missing(html)
        if missing:
            fail(f"Missing local hrefs in {page}: {', '.join(missing[:10])}")

    if "Cukiernik (SPC.01)" not in catalog_html:
        fail("Catalog does not contain Cukiernik (SPC.01)")
    if "01_BSI_stopnia/zawodowe/PP_cukiernik_SPC01.pdf" not in catalog_html:
        fail("Catalog does not link the local cukiernik PDF")

    print("Guide page validation OK")


if __name__ == "__main__":
    main()
