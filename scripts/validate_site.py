from __future__ import annotations

import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET
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
EXPECTED_SCHEDULE_HEADERS = [
    "nr tematu",
    "poziom klasy",
    "Temat",
    "Dział",
    "Liczba godzin",
    "Elementy podstawy programowej",
    "cele podstawowe: uczeń:",
    "cele ponadpodstawowe: uczeń:",
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


def read_xlsx_strings(path: Path) -> list[str]:
    ns = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    strings: list[str] = []
    with zipfile.ZipFile(path) as archive:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in root.findall("main:si", ns):
                parts = [node.text or "" for node in item.findall(".//main:t", ns)]
                shared.append("".join(parts))
        for name in archive.namelist():
            if not name.startswith("xl/worksheets/sheet") or not name.endswith(".xml"):
                continue
            root = ET.fromstring(archive.read(name))
            for cell in root.findall(".//main:c", ns):
                value = cell.find("main:v", ns)
                if value is None:
                    inline = cell.find("main:is", ns)
                    if inline is not None:
                        parts = [node.text or "" for node in inline.findall(".//main:t", ns)]
                        if parts:
                            strings.append("".join(parts))
                    continue
                text = value.text or ""
                if cell.attrib.get("t") == "s":
                    index = int(text)
                    if index < len(shared):
                        strings.append(shared[index])
                else:
                    strings.append(text)
    return strings


def main() -> None:
    page_html = {page: read_html(ROOT / page) for page in PAGES}
    catalog_html = read_html(CATALOG)

    required_by_page = {
        "index.html": [
            "Od podstawy programowej do wymagań na oceny",
            "Ścieżka pracy",
            "1. Ścieżka pracy",
            "2. Adaptacja programu",
            "3. Przygotowanie rozkładu",
            "Przejdź do kroku 2",
        ],
        "rozklad_materialu.html": [
            "Rozkład materiału",
            "3. Rozkład materiału",
            SCHEDULE_TEMPLATE,
            "Zastępstwa i nieobecności",
            "Lekcja organizacyjna. Zapoznanie uczniów z wymaganiami edukacyjnymi i zasadami oceniania",
            "piątku 28 sierpnia 2026 r.",
            "sobotę 29 sierpnia 2026 r.",
            "przed 30 sierpnia 2026 r.",
            "1 września 2026 r.",
            "po 30 sierpnia wprowadzić go do uporządkowanego dziennika",
            "assets/rozklad-materialu-wzor.png",
            "assets/rozklad-materialu-szablon.png",
            "nr tematu",
            "poziom klasy",
            "Elementy podstawy programowej",
            "cele podstawowe: uczeń:",
            "cele ponadpodstawowe: uczeń:",
        ],
        "ramowe_plany_nauczania.html": [
            "Ramowe plany nauczania",
            "Ramowe plany nauczania zostaną opublikowane po uporządkowaniu i zatwierdzeniu materiałów",
        ],
        "szkolne_zestawy_programow_nauczania.html": [
            "Szkolne zestawy programów nauczania",
            "Szkolne zestawy programów nauczania zostaną opublikowane po uporządkowaniu i zatwierdzeniu materiałów",
        ],
        "adaptacja_programu.html": [
            "2. Adaptacja programu",
            "Adaptacja programu w praktyce",
            "Otwórz katalog podstaw programowych",
            "katalog_podstaw_programowych_ZSZ5_2026_2027.html",
        ],
        "materialy_i_linki.html": ["Przydatne materiały i linki", "Katalog podstaw programowych", "ZPE - podstawa programowa"],
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
        "Ta sekcja zostanie uzupełniona",
        "Wkrótce pojawią się tutaj",
        "czystą kartą",
        "Co ma być widoczne",
        "Co uzupełnić przed tabelą",
        "Czego unikać",
        "Sztywno trzymamy się",
        "Nie oceniaj",
        "Nie zastępuj",
        "L.p.",
        "Zasoby prywatne",
        "Zasoby publiczne",
        "Rozszerzenie",
        "Smartlinki",
        "Materiały dydaktyczne",
        "Kolekcja po lekcji",
        "Aktywna",
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

    workbook_strings = read_xlsx_strings(ROOT / SCHEDULE_TEMPLATE)
    missing_headers = [header for header in EXPECTED_SCHEDULE_HEADERS if header not in workbook_strings]
    if missing_headers:
        fail(f"Missing schedule XLSX headers: {', '.join(missing_headers)}")
    obsolete_headers = [
        "L.p.",
        "Zasoby prywatne",
        "Zasoby publiczne",
        "Rozszerzenie",
        "Smartlinki",
        "Materiały dydaktyczne",
        "Kolekcja po lekcji",
        "Aktywna",
    ]
    present_obsolete_headers = [header for header in obsolete_headers if header in workbook_strings]
    if present_obsolete_headers:
        fail(f"Obsolete schedule XLSX headers: {', '.join(present_obsolete_headers)}")

    for page, html in page_html.items():
        missing = local_href_missing(html)
        if missing:
            fail(f"Missing local hrefs in {page}: {', '.join(missing[:10])}")
    catalog_missing = local_href_missing(catalog_html)
    if catalog_missing:
        fail(f"Missing local hrefs in catalog: {', '.join(catalog_missing[:10])}")

    if "Cukiernik (SPC.01)" not in catalog_html:
        fail("Catalog does not contain Cukiernik (SPC.01)")
    if "https://zpe.gov.pl/podstawa-programowa/ksztalcenie-zawodowe/branza-spozywcza" not in catalog_html:
        fail("Catalog does not link Cukiernik (SPC.01) to the ZPE vocational branch")
    if "ore.edu.pl" in catalog_html or "ore.edu.pl" in page_html["materialy_i_linki.html"]:
        fail("ORE link remains in catalog or materials page")

    print("Guide page validation OK")


if __name__ == "__main__":
    main()
