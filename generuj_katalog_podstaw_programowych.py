from __future__ import annotations

import re
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent
SOURCE_XLSX = ROOT / "katalog_podstaw_programowych_ZSZ5_2026_2027.xlsx"
OUT = ROOT / "katalog_podstaw_programowych_ZSZ5_2026_2027.html"

NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

SCHOOL_ORDER = ["BS I stopnia", "BS II stopnia", "Technikum"]
AREA_ORDER = ["zawodowe", "ogólne"]


@dataclass(frozen=True)
class CatalogItem:
    school: str
    area: str
    title: str
    document_name: str
    legal_basis: str
    local_path: str
    source_url: str
    status: str

    @property
    def local_exists(self) -> bool:
        return bool(self.local_path) and (ROOT / self.local_path).exists()

    @property
    def qualification(self) -> str:
        found = re.findall(r"[A-Z]{3}\.\d{2}", self.title)
        return ", ".join(found)


def h(value: object) -> str:
    return escape(str(value or ""), quote=True)


def read_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    values: list[str] = []
    for item in root.findall("a:si", NS):
        parts = [node.text or "" for node in item.findall(".//a:t", NS)]
        values.append("".join(parts))
    return values


def sheet_path(zf: zipfile.ZipFile) -> str:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    first_sheet = workbook.find("a:sheets/a:sheet", NS)
    if first_sheet is None:
        raise ValueError("Workbook does not contain sheets")
    rel_id = first_sheet.attrib[f"{{{NS['r']}}}id"]
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    for rel in rels.findall("rel:Relationship", NS):
        if rel.attrib.get("Id") == rel_id:
            target = rel.attrib["Target"]
            return f"xl/{target}" if not target.startswith("/") else target.lstrip("/")
    raise ValueError("Cannot resolve first sheet path")


def cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(".//a:t", NS)).strip()

    value_node = cell.find("a:v", NS)
    if value_node is None or value_node.text is None:
        return ""
    value = value_node.text
    if cell_type == "s":
        try:
            return shared_strings[int(value)].strip()
        except (ValueError, IndexError):
            return ""
    return value.strip()


def column_index(cell_ref: str) -> int:
    letters = re.sub(r"[^A-Z]", "", cell_ref.upper())
    number = 0
    for char in letters:
        number = number * 26 + (ord(char) - ord("A") + 1)
    return max(number - 1, 0)


def read_rows(path: Path) -> list[list[str]]:
    with zipfile.ZipFile(path) as zf:
        shared_strings = read_shared_strings(zf)
        root = ET.fromstring(zf.read(sheet_path(zf)))

    rows: list[list[str]] = []
    for row in root.findall(".//a:sheetData/a:row", NS):
        values: list[str] = []
        for cell in row.findall("a:c", NS):
            idx = column_index(cell.attrib.get("r", "A1"))
            while len(values) <= idx:
                values.append("")
            values[idx] = cell_value(cell, shared_strings)
        rows.append(values)
    return rows


def catalog_items() -> list[CatalogItem]:
    rows = read_rows(SOURCE_XLSX)
    header_idx = next(
        idx for idx, row in enumerate(rows) if row and row[0].strip().lower() == "typ szkoły"
    )
    items: list[CatalogItem] = []
    for row in rows[header_idx + 1 :]:
        padded = row + [""] * 8
        school, area, title, document_name, legal_basis, local_path, source_url, status = [
            value.strip() for value in padded[:8]
        ]
        if not school or not area or (not local_path and not source_url):
            continue
        items.append(
            CatalogItem(
                school=school,
                area=area.lower(),
                title=title,
                document_name=document_name,
                legal_basis=legal_basis,
                local_path=local_path,
                source_url=source_url,
                status=status,
            )
        )
    return items


def render_item(item: CatalogItem, index: int) -> str:
    missing_class = " is-missing" if not item.local_exists and not item.source_url else ""
    search = " ".join(
        [
            item.school,
            item.area,
            item.title,
            item.document_name,
            item.legal_basis,
            item.local_path,
            item.source_url,
            item.status,
            item.qualification,
        ]
    )
    local_action = ""
    if item.local_exists:
        local_action = f'<a class="btn" href="{h(item.local_path)}" target="_blank" rel="noopener">Otwórz plik lokalny</a>'
    source_action = (
        f'<a class="btn primary" href="{h(item.source_url)}" target="_blank" rel="noopener">Otwórz w ZPE</a>'
        if item.source_url
        else ""
    )
    download_action = (
        f'<a class="btn" href="{h(item.local_path)}" download>Pobierz</a>' if item.local_exists else ""
    )
    no_action = '<span class="btn disabled">Brak linku</span>' if not local_action and not source_action else ""
    local_path_row = (
        f'<div><dt>Plik lokalny</dt><dd><code>{h(item.local_path)}</code></dd></div>'
        if item.local_path
        else '<div><dt>Plik lokalny</dt><dd>nie jest przechowywany</dd></div>'
    )
    return f"""
<article class="catalog-card{missing_class}" data-search="{h(search)}" id="pozycja_{index}">
  <div class="catalog-main">
    <div class="card-topline">
      <span class="pill area">{h(item.area)}</span>
      {f'<span class="pill qualification">{h(item.qualification)}</span>' if item.qualification else ''}
      <span class="pill status">{h(item.status)}</span>
      {'' if item.local_exists or item.source_url else '<span class="pill warning">brak linku</span>'}
    </div>
    <h3>{h(item.title)}</h3>
    <p>{h(item.document_name)}</p>
    <dl>
      <div><dt>Podstawa prawna</dt><dd>{h(item.legal_basis).replace(chr(10), '<br>')}</dd></div>
      {local_path_row}
    </dl>
  </div>
  <div class="catalog-actions">
    {source_action}
    {local_action}
    {download_action}
    {no_action}
  </div>
</article>
"""


def render_section(school: str, area: str, items: list[CatalogItem], start_index: int) -> tuple[str, int]:
    section_items = [item for item in items if item.school == school and item.area == area]
    if not section_items:
        return "", start_index
    cards: list[str] = []
    idx = start_index
    for item in section_items:
        cards.append(render_item(item, idx))
        idx += 1
    return f"""
<section class="school-section" id="{h(slug(school + '-' + area))}">
  <div class="section-head">
    <h2>{h(school)} · {h(area)}</h2>
    <span>{len(section_items)} pozycji</span>
  </div>
  <div class="catalog-grid">
    {''.join(cards)}
  </div>
</section>
""", idx


def slug(value: str) -> str:
    table = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
    return re.sub(r"[^a-z0-9]+", "-", value.translate(table).lower()).strip("-")


def render_page(items: list[CatalogItem]) -> str:
    grouped = defaultdict(int)
    for item in items:
        grouped[item.school] += 1
    local_count = sum(1 for item in items if item.local_exists)
    zpe_count = sum(1 for item in items if "zpe.gov.pl" in item.source_url)
    missing_count = sum(1 for item in items if not item.local_exists and not item.source_url)
    nav = "\n".join(
        f'<a href="#{h(slug(school))}">{h(school)} <span>{grouped[school]}</span></a>'
        for school in SCHOOL_ORDER
        if grouped[school]
    )

    sections: list[str] = []
    index = 1
    for school in SCHOOL_ORDER:
        school_sections: list[str] = []
        for area in AREA_ORDER:
            section, index = render_section(school, area, items, index)
            if section:
                school_sections.append(section)
        if school_sections:
            sections.append(
                f"""
<div class="school-block" id="{h(slug(school))}">
  {''.join(school_sections)}
</div>
"""
            )

    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Katalog podstaw programowych ZSZ5 2026/2027</title>
<link rel="icon" href="assets/logo-zsz5-black.png">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f3f0e9;--paper:#fffdf8;--ink:#172033;--muted:#647084;--line:#d9d5cc;--navy:#172a46;--blue:#2b67d1;--gold:#d99b2b;--green:#2e8b68;--red:#c94c4c;--shadow:0 10px 24px rgba(23,32,51,.08)}}
html{{scroll-behavior:smooth}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;background:var(--bg);color:var(--ink);font-size:15px;line-height:1.5}}
a{{color:inherit}}
header{{background:var(--paper);border-bottom:1px solid rgba(23,32,51,.08);padding:14px 22px}}
.brand{{display:flex;align-items:center;gap:16px;max-width:1236px;margin:0 auto}}
.brand img{{width:82px;height:58px;object-fit:contain;flex-shrink:0}}
h1{{font-size:1.25rem;line-height:1.2}}
header p{{margin-top:5px;color:var(--muted);font-size:.88rem;max-width:880px}}
.hero{{max-width:1236px;margin:20px auto 0;padding:24px 22px;background:var(--navy);color:#fff;border-radius:8px;box-shadow:var(--shadow)}}
.hero h2{{font-size:clamp(1.45rem,3vw,2.25rem);line-height:1.1;max-width:860px}}
.hero p{{margin-top:10px;color:#c8d1df;max-width:920px}}
.hero-actions,.quick-nav{{display:flex;gap:8px;flex-wrap:wrap;margin-top:15px}}
.hero-actions a,.quick-nav a{{display:inline-flex;align-items:center;min-height:32px;padding:6px 11px;border-radius:999px;text-decoration:none;font-size:.82rem;font-weight:800}}
.hero-actions a{{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.26);color:#fff}}
.quick-nav{{max-width:1236px;margin:14px auto 0;padding:0 22px}}
.quick-nav a{{background:#fff;border:1px solid var(--line);color:#345070}}
.quick-nav span{{margin-left:6px;color:var(--muted);font-weight:850}}
.tools{{position:sticky;top:0;z-index:20;background:rgba(243,240,233,.95);border-bottom:1px solid var(--line);backdrop-filter:blur(12px);margin-top:14px}}
.tools-inner{{max-width:1236px;margin:0 auto;padding:10px 22px;display:grid;grid-template-columns:minmax(200px,1fr) auto;gap:10px;align-items:center}}
label{{font-size:.78rem;font-weight:850;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}}
input{{width:100%;padding:10px 14px;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink);box-shadow:0 8px 18px rgba(23,32,51,.04)}}
#result_status{{font-size:.82rem;color:var(--muted);white-space:nowrap}}
.stats{{max-width:1236px;margin:14px auto 0;padding:0 22px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}}
.stat{{background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;padding:14px;text-align:center;box-shadow:0 8px 20px rgba(23,32,51,.06)}}
.stat strong{{display:block;font-size:1.55rem;color:var(--blue);line-height:1}}
.stat span{{display:block;margin-top:4px;font-size:.76rem;color:var(--muted);line-height:1.25}}
.school-section{{max-width:1236px;margin:22px auto 0;padding:0 22px}}
.section-head{{display:flex;align-items:end;justify-content:space-between;gap:12px;margin-bottom:10px}}
.section-head h2{{font-size:1.08rem;color:var(--navy)}}
.section-head span{{font-size:.78rem;color:var(--muted);font-weight:800}}
.catalog-grid{{display:grid;gap:10px}}
.catalog-card{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px;align-items:start;background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;padding:14px;box-shadow:0 8px 20px rgba(23,32,51,.05)}}
.catalog-card.is-missing{{border-left:4px solid var(--gold)}}
.card-topline{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:7px}}
.pill{{display:inline-flex;align-items:center;min-height:22px;padding:2px 7px;border-radius:999px;font-size:.7rem;font-weight:850;text-transform:uppercase}}
.area{{background:#eef4fb;color:#1d4f9a;border:1px solid #cfe2fb}}
.qualification{{background:#eef2ff;color:#3730a3;border:1px solid #c7d2fe}}
.status{{background:#dcfce7;color:#166534;border:1px solid #bbf7d0}}
.warning{{background:#fef3c7;color:#92400e;border:1px solid #fde68a}}
.catalog-card h3{{font-size:1rem;line-height:1.25}}
.catalog-card p{{margin-top:4px;color:#374151;font-size:.86rem}}
dl{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}}
dt{{font-size:.7rem;font-weight:850;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}}
dd{{font-size:.8rem;color:#374151;margin-top:2px}}
code{{font-size:.76rem;color:#4b5563;word-break:break-all}}
.catalog-actions{{display:flex;gap:8px;align-items:flex-start;justify-content:flex-end;flex-wrap:wrap;min-width:260px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:32px;padding:6px 10px;border:1px solid var(--line);background:#fff;border-radius:999px;text-decoration:none;font-size:.8rem;color:var(--ink);font-weight:800}}
.btn.primary{{background:#eef4fb;color:#1d4f9a;border-color:#b9d4f7}}
.btn.disabled{{color:#92400e;background:#fff7df;border-color:#ecd6a4}}
[hidden]{{display:none!important}}
a:focus-visible,input:focus-visible{{outline:3px solid var(--gold);outline-offset:2px}}
@media (max-width:820px){{.brand{{align-items:flex-start}}.brand img{{width:62px;height:44px}}.hero{{margin:14px 12px 0;padding:18px 16px}}.quick-nav,.stats,.school-section{{padding-left:12px;padding-right:12px}}.tools-inner{{grid-template-columns:1fr;padding-left:12px;padding-right:12px}}#result_status{{white-space:normal}}.stats{{grid-template-columns:1fr 1fr}}.catalog-card{{grid-template-columns:1fr}}.catalog-actions{{justify-content:flex-start;min-width:0}}dl{{grid-template-columns:1fr}}}}
@media (max-width:560px){{header p{{display:none}}h1{{font-size:1.04rem}}.hero h2{{font-size:1.42rem}}.stats{{grid-template-columns:1fr}}}}
@media print{{.tools,.hero-actions,.quick-nav{{display:none}}body{{background:#fff}}.catalog-card{{break-inside:avoid}}}}
</style>
</head>
<body>
<header>
  <div class="brand">
    <img src="assets/logo-zsz5-black.png" alt="Logotyp ZSZ5 we Wrocławiu">
    <div>
      <h1>Katalog podstaw programowych ZSZ5 2026/2027</h1>
      <p>Prosty indeks wygenerowany z arkusza „katalog_podstaw_programowych_ZSZ5_2026_2027.xlsx”.</p>
    </div>
  </div>
</header>
<main>
  <section class="hero">
    <h2>Bezpośrednie linki do podstaw programowych</h2>
    <p>Wybierz typ szkoły, znajdź zawód albo przedmiot i otwórz aktualną podstawę programową w Zintegrowanej Platformie Edukacyjnej. Lokalne kopie PDF nie są wymagane do pracy z katalogiem.</p>
    <div class="hero-actions">
      <a href="wymagania_edukacyjne_ZSZ5_2026_2027.html">Wróć do wymagań edukacyjnych</a>
      <a href="index.html">Strona startowa</a>
      <a href="{h(SOURCE_XLSX.name)}">Otwórz arkusz katalogu</a>
    </div>
  </section>
  <nav class="quick-nav" aria-label="Szybka nawigacja">{nav}</nav>
  <section class="stats" aria-label="Podsumowanie katalogu">
    <div class="stat"><strong>{len(items)}</strong><span>pozycji z arkusza</span></div>
    <div class="stat"><strong>{zpe_count}</strong><span>linków do ZPE</span></div>
    <div class="stat"><strong>{missing_count}</strong><span>pozycji bez linku lub pliku</span></div>
  </section>
  <div class="tools">
    <div class="tools-inner">
      <div>
        <label for="catalog_search">Szukaj w katalogu</label>
        <input id="catalog_search" type="search" placeholder="np. cukiernik, SPC.01, technikum, matematyka" oninput="filterCatalog()">
      </div>
      <div id="result_status" aria-live="polite"></div>
    </div>
  </div>
  {''.join(sections)}
</main>
<script>
function normalizeText(value){{
  return (value || '').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
}}
function filterCatalog(){{
  const query=normalizeText(document.getElementById('catalog_search').value.trim());
  let visible=0;
  document.querySelectorAll('.catalog-card').forEach(card=>{{
    const match=!query || normalizeText(card.dataset.search).includes(query);
    card.hidden=!match;
    if(match) visible++;
  }});
  document.querySelectorAll('.school-section').forEach(section=>{{
    const any=[...section.querySelectorAll('.catalog-card')].some(card=>!card.hidden);
    section.hidden=!any;
  }});
  document.querySelectorAll('.school-block').forEach(block=>{{
    const any=[...block.querySelectorAll('.school-section')].some(section=>!section.hidden);
    block.hidden=!any;
  }});
  document.getElementById('result_status').textContent=query ? `Widoczne pozycje: ${{visible}}` : '';
}}
</script>
</body>
</html>
"""


def generate_catalog_page() -> list[CatalogItem]:
    items = catalog_items()
    OUT.write_text(render_page(items), encoding="utf-8")
    return items


def main() -> None:
    items = generate_catalog_page()
    print(f"Generated {OUT}")
    print(f"Catalog items: {len(items)}")
    print(f"Local files: {sum(1 for item in items if item.local_exists)}")


if __name__ == "__main__":
    main()
