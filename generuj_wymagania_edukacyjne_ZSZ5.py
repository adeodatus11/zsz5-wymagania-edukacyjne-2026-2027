from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

import generuj_kompletne_wymagania_ogolne as og


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "wymagania_edukacyjne_ZSZ5_2026_2027.html"
INDEX = ROOT / "index.html"
DATA_DIR = ROOT / "data"
PDF_MANIFEST = DATA_DIR / "podstawy_programowe.json"
REPORT_DIR = ROOT / "przebudowa_wymagan_ogolnych"
REPORT = REPORT_DIR / "raport_integracji_wymagan_i_biblioteki_pdf.md"
VOC_AUDIT = REPORT_DIR / "audyt_i_przebudowa_wymagan_zawodowych.md"


SCHOOL_LABELS = {
    "technikum": "Technikum",
    "bsi": "Branżowa Szkoła I stopnia",
    "bsii": "Branżowa Szkoła II stopnia",
}

SCHOOL_SHORT = {
    "technikum": "Technikum",
    "bsi": "BS I",
    "bsii": "BS II",
}

SCHOOL_COLORS = {
    "technikum": "#1e40af",
    "bsi": "#6b21a8",
    "bsii": "#166534",
}

GRADE_ORDER = ["Dopuszczająca", "Dostateczna", "Dobra", "Bardzo dobra", "Celująca"]

ORE_VADEMECUM = [
    {
        "subjects": ["Biologia"],
        "url": "https://ore.edu.pl/wp-content/uploads/2019/07/vademecum-nauczyciela.-wdrazanie-podstawy-programowej-w-szkole-ponadpodstawowej.-biologia.pdf",
        "schools": ["technikum", "bsi"],
    },
    {
        "subjects": ["Chemia"],
        "url": "https://ore.edu.pl/wp-content/uploads/2019/07/vademecum-nauczyciela.-wdrazanie-podstawy-programowej-w-szkole-ponadpodstawowej.-chemia.pdf",
        "schools": ["technikum", "bsi"],
    },
    {
        "subjects": ["Fizyka"],
        "url": "https://ore.edu.pl/wp-content/uploads/2019/07/vademecum-nauczyciela.-wdrazanie-podstawy-programowej-w-szkole-ponadpodstawowej.-fizyka.pdf",
        "schools": ["technikum", "bsi"],
    },
    {
        "subjects": ["Historia"],
        "url": "https://ore.edu.pl/wp-content/uploads/2019/07/vademecum-nauczyciela.-wdrazanie-podstawy-programowej-w-szkole-ponadpodstawowej.-historia.pdf",
        "schools": ["technikum", "bsi"],
    },
    {
        "subjects": ["Język polski"],
        "url": "https://ore.edu.pl/wp-content/uploads/2019/07/vademecum-nauczyciela.-wdrazanie-podstawy-programowej-w-szkole-ponadpodstawowej.-jezyk-polski-wyd.elektroniczne.pdf",
        "schools": ["technikum", "bsi", "bsii"],
    },
    {
        "subjects": ["Geografia"],
        "url": "https://ore.edu.pl/wp-content/uploads/2019/11/vademecum-nauczyciela.-wdrazanie-podstawy-programowej-w-szkole-ponadpodstawowej.-geografia.pdf",
        "schools": ["technikum", "bsi"],
    },
    {
        "subjects": ["Wiedza o społeczeństwie"],
        "url": "https://ore.edu.pl/wp-content/uploads/2019/12/vademecum-nauczyciela.-wdrazanie-podstawy-programowej-w-szkole-ponadpodstawowej.-wos.pdf",
        "schools": ["technikum"],
    },
    {
        "subjects": ["Wychowanie fizyczne"],
        "url": "https://ore.edu.pl/wp-content/uploads/2019/12/vademecum-nauczyciela.-wdrazanie-podstawy-programowej-w-szkole-ponadpodstawowej.-wychowanie-fizyczne.pdf",
        "schools": ["technikum", "bsi"],
    },
]


@dataclass(frozen=True)
class VocationalSpec:
    school: str
    name: str
    path: str
    source_label: str


VOCATIONAL_SPECS = [
    VocationalSpec("bsi", "Cukiernik", "01_BSI_stopnia/zawodowe/PP_cukiernik_SPC01.pdf", "Dz.U. 2019 poz. 991, SPC.01"),
    VocationalSpec("bsi", "Fryzjer", "01_BSI_stopnia/zawodowe/PP_fryzjer_FRK01.pdf", "Dz.U. 2019 poz. 991, FRK.01"),
    VocationalSpec("bsi", "Kelner", "01_BSI_stopnia/zawodowe/PP_kelner_HGT01.pdf", "Dz.U. 2019 poz. 991, HGT.01"),
    VocationalSpec("bsi", "Kucharz", "01_BSI_stopnia/zawodowe/PP_kucharz_HGT02.pdf", "Dz.U. 2019 poz. 991, HGT.02"),
    VocationalSpec("bsi", "Lakiernik samochodowy", "01_BSI_stopnia/zawodowe/PP_lakiernik_samochodowy_MOT03.pdf", "Dz.U. 2019 poz. 991, MOT.03"),
    VocationalSpec("bsi", "Mechanik pojazdów samochodowych", "01_BSI_stopnia/zawodowe/PP_mechanik_pojazdow_samochodowych_MOT05.pdf", "Dz.U. 2019 poz. 991, MOT.05"),
    VocationalSpec("bsi", "Sprzedawca", "01_BSI_stopnia/zawodowe/PP_sprzedawca_HAN01.pdf", "Dz.U. 2019 poz. 991, HAN.01"),
    VocationalSpec("bsii", "Technik usług fryzjerskich", "02_BSII_stopnia/zawodowe/PP_technik_uslug_fryzjerskich_FRK01_FRK03.pdf", "Dz.U. 2019 poz. 991, FRK.01/FRK.03"),
    VocationalSpec("technikum", "Technik handlowiec", "03_Technikum/zawodowe/PP_technik_handlowiec_HAN01_HAN02.pdf", "Dz.U. 2019 poz. 991, HAN.01/HAN.02"),
    VocationalSpec("technikum", "Technik usług fryzjerskich", "03_Technikum/zawodowe/PP_technik_uslug_fryzjerskich_FRK01_FRK03.pdf", "Dz.U. 2019 poz. 991, FRK.01/FRK.03"),
]


def h(value: object) -> str:
    return og.h(str(value))


def read_pdf(path: str) -> str:
    reader = PdfReader(str(ROOT / path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def clean_text(value: str) -> str:
    value = value.replace("\u00ad", "")
    value = re.sub(r"(\w)-\s+(\w)", r"\1\2", value)
    replacements = {
        "e -mail": "e-mail",
        "e -maile": "e-maile",
        "informacyjno - -komunikacyjnych": "informacyjno-komunikacyjnych",
        "klim at": "klimat",
        "za wody": "zawody",
        "r eaguje": "reaguje",
    }
    for bad, good in replacements.items():
        value = value.replace(bad, good)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\s+([,.;:])", r"\1", value)
    return value


def clean_unit_title(value: str) -> str:
    value = clean_text(value)
    value = re.sub(r"\s*\d+\)\s*$", "", value).strip()
    value = re.sub(r"\s+\d{2,4}\s*$", "", value).strip()
    value = re.sub(r"\s+\d+\)\s+\d{2,4}\s*$", "", value).strip()
    return value


def slug(value: str) -> str:
    table = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
    value = value.translate(table).lower()
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return value or "sekcja"


def safe_id(*parts: str) -> str:
    return "_".join(slug(p) for p in parts if p)


def status_class(status: str) -> str:
    return "status-ok" if status in {"podstawa dostępna", "ORE"} else "status-review"


def extract_qualifications(text: str) -> list[str]:
    found = []
    for code, title in re.findall(r"\b([A-Z]{3}\.\d{2})\.\s+([A-ZĄĆĘŁŃÓŚŹŻa-ząćęłńóśźż][^\n]{3,120})", text):
        item = clean_text(f"{code}. {title}")
        if item not in found and "Efekty kształcenia" not in item:
            found.append(item)
    return found[:4]


def extract_goals(text: str) -> list[str]:
    match = re.search(r"CELE KSZTAŁCENIA\s+(.*?)(?:EFEKTY KSZTAŁCENIA|Do wykonywania)", text, re.S)
    if not match:
        return []
    block = match.group(1)
    goals = []
    for item in re.findall(r"(?:^|\s)(?:\d+\)|[a-z]\))\s+(.+?)(?=(?:\s+(?:\d+\)|[a-z]\))\s+)|$)", clean_text(block)):
        item = clean_text(item).rstrip(";.")
        if 15 <= len(item) <= 220 and item not in goals:
            goals.append(item)
    return goals[:8]


def extract_numbered_items(block: str) -> list[str]:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    items: list[str] = []
    current: list[str] = []
    for line in lines:
        if re.match(r"^\d+\)\s+", line):
            if current:
                items.append(clean_text(" ".join(current)))
            current = [line]
        elif current:
            if not re.match(r"^(Dziennik Ustaw|Poz\.|Efekty kształcenia|Kryteria weryfikacji|Uczeń:)", line):
                current.append(line)
    if current:
        items.append(clean_text(" ".join(current)))

    cleaned = []
    seen = set()
    for item in items:
        item = re.sub(r"\s+\d+\s*$", "", item).strip()
        if not 20 <= len(item) <= 700:
            continue
        if re.search(r"\b(godzin|godziny|tygodniowo)\b", item, re.I):
            continue
        key = item.lower()
        if key not in seen:
            seen.add(key)
            cleaned.append(item)
    return cleaned[:45]


def extract_vocational_units(spec: VocationalSpec) -> dict:
    text = read_pdf(spec.path)
    quals = extract_qualifications(text)
    goals = extract_goals(text)
    unit_matches = list(re.finditer(r"(?m)^([A-Z]{3}\.\d{2}\.\d+)\.\s+([^\n]{3,160})\s*$", text))
    units = []
    for idx, match in enumerate(unit_matches):
        code = match.group(1)
        title = clean_unit_title(match.group(2))
        if title.lower().startswith(("efekty", "kryteria")):
            continue
        start = match.end()
        end = unit_matches[idx + 1].start() if idx + 1 < len(unit_matches) else len(text)
        body = text[start:end]
        items = extract_numbered_items(body)
        if not items:
            continue
        units.append(
            {
                "code": code,
                "title": title,
                "items": items,
                "qualification": code.rsplit(".", 1)[0],
            }
        )
    return {
        "school": spec.school,
        "name": spec.name,
        "path": spec.path,
        "source_label": spec.source_label,
        "status": "do recenzji",
        "note": "Sekcja zawodowa została przebudowana automatycznie z lokalnego PDF i wymaga recenzji nauczyciela zawodu przed publikacją.",
        "qualifications": quals,
        "goals": goals,
        "units": units,
    }


def render_table(chunks: dict[str, list[str]]) -> str:
    parts = [
        '<div class="table-wrap" role="region" aria-label="Tabela wymagań na oceny"><table class="req-table">',
        "<thead><tr>",
    ]
    for grade in GRADE_ORDER:
        parts.append(f"<th>{h(grade)}</th>")
    parts.append("</tr></thead><tbody><tr>")
    for grade in GRADE_ORDER:
        parts.append(f'<td data-label="{h(grade)}"><ul>')
        grade_items = chunks.get(grade, [])
        if not grade_items:
            parts.append('<li class="review-note">Próg do określenia przez nauczyciela na podstawie programu nauczania.</li>')
        for item in grade_items:
            parts.append(f"<li>{h(item)}</li>")
        parts.append("</ul></td>")
    parts.append("</tr></tbody></table></div>")
    return "\n".join(parts)


def render_general_card(spec: og.SubjectSpec, idx: int) -> tuple[str, dict]:
    sections = og.extract_sections(spec)
    card_id = f"gen_{spec.school}_{idx}"
    body_id = f"{card_id}_body"
    search = " ".join([spec.name, spec.source_label] + [section["title"] for section in sections])
    parts = [
        f'<article class="content-card general-card" id="{card_id}" data-search="{h(search)}">',
        f'<button class="card-toggle" type="button" onclick="toggleCard(\'{card_id}\')" aria-expanded="false" aria-controls="{body_id}" style="border-left-color:{SCHOOL_COLORS[spec.school]}">',
        '<span class="arrow" aria-hidden="true">▶</span>',
        f'<span class="card-name">{h(spec.name)}</span>',
        f'<span class="card-meta">{og.polish_count(len(sections), "dział", "działy", "działów")} · {og.polish_count(sum(len(s["items"]) for s in sections), "wymaganie źródłowe", "wymagania źródłowe", "wymagań źródłowych")}</span>',
        "</button>",
        f'<div class="card-body" id="{body_id}">',
        '<details class="source-box"><summary>Źródło, status i uwagi</summary>',
        f'<p><span class="status {status_class(spec.status)}">{h(spec.status)}</span><strong>Źródło:</strong> {h(spec.source_label)}</p>',
        f'<code>{h(spec.path)}</code>',
    ]
    if spec.note:
        parts.append(f'<p class="note">{h(spec.note)}</p>')
    parts.extend(
        [
            "</details>",
            '<p class="cumulative">Wymagania są kumulatywne: ocena wyższa obejmuje wymagania na oceny niższe.</p>',
            '<div class="card-actions">',
            f'<button type="button" onclick="expandSections(\'{card_id}\', true)">Rozwiń działy</button>',
            f'<button type="button" onclick="expandSections(\'{card_id}\', false)">Zwiń działy</button>',
            "</div>",
        ]
    )
    for sidx, section in enumerate(sections):
        sec_id = f"{card_id}_{sidx}"
        sec_body_id = f"{sec_id}_body"
        chunks = og.split_requirements(section["items"], section["title"])
        parts.extend(
            [
                f'<section class="unit" id="{sec_id}" data-search="{h(section["number"] + " " + section["title"])}">',
                f'<button class="unit-toggle" type="button" onclick="toggleUnit(\'{sec_id}\')" aria-expanded="false" aria-controls="{sec_body_id}">',
                '<span class="arrow small" aria-hidden="true">▶</span>',
                f'<span class="unit-code">Dział {h(section["number"])}.</span>',
                f'<span class="unit-title">{h(section["title"])}</span>',
                f'<span class="unit-count">{og.polish_count(len(section["items"]), "wymaganie", "wymagania", "wymagań")}</span>',
                "</button>",
                f'<div class="unit-body" id="{sec_body_id}">',
                render_table(chunks),
                "</div></section>",
            ]
        )
    parts.append("</div></article>")
    return "\n".join(parts), {
        "school": spec.school,
        "type": "ogolne",
        "name": spec.name,
        "sections": len(sections),
        "items": sum(len(s["items"]) for s in sections),
        "status": spec.status,
        "id": card_id,
    }


def render_vocational_card(item: dict, idx: int) -> tuple[str, dict]:
    card_id = f"voc_{item['school']}_{idx}"
    body_id = f"{card_id}_body"
    units = item["units"]
    search = " ".join([item["name"], item["source_label"], " ".join(item["qualifications"])] + [u["code"] + " " + u["title"] for u in units])
    parts = [
        f'<article class="content-card vocational-card" id="{card_id}" data-search="{h(search)}">',
        f'<button class="card-toggle" type="button" onclick="toggleCard(\'{card_id}\')" aria-expanded="false" aria-controls="{body_id}" style="border-left-color:{SCHOOL_COLORS[item["school"]]}">',
        '<span class="arrow" aria-hidden="true">▶</span>',
        f'<span class="card-name">{h(item["name"])}</span>',
        f'<span class="card-meta">{og.polish_count(len(units), "jednostka", "jednostki", "jednostek")} · {og.polish_count(sum(len(u["items"]) for u in units), "kryterium", "kryteria", "kryteriów")}</span>',
        "</button>",
        f'<div class="card-body" id="{body_id}">',
        '<details class="source-box" open><summary>Źródło, status i kwalifikacje</summary>',
        f'<p><span class="status status-review">{h(item["status"])}</span><strong>Źródło:</strong> {h(item["source_label"])}</p>',
        f'<code>{h(item["path"])}</code>',
        f'<p class="note">{h(item["note"])}</p>',
        "</details>",
    ]
    if item["qualifications"]:
        parts.append('<div class="chips">' + "".join(f"<span>{h(q)}</span>" for q in item["qualifications"]) + "</div>")
    if item["goals"]:
        parts.append('<details class="goals-box"><summary>Cele kształcenia</summary><ul>')
        for goal in item["goals"]:
            parts.append(f"<li>{h(goal)}</li>")
        parts.append("</ul></details>")
    parts.extend(
        [
            '<p class="cumulative">Wymagania zawodowe są opracowaniem progów ocen na podstawie efektów kształcenia i kryteriów weryfikacji z PDF.</p>',
            '<div class="card-actions">',
            f'<button type="button" onclick="expandSections(\'{card_id}\', true)">Rozwiń jednostki</button>',
            f'<button type="button" onclick="expandSections(\'{card_id}\', false)">Zwiń jednostki</button>',
            "</div>",
        ]
    )
    for uidx, unit in enumerate(units):
        sec_id = f"{card_id}_{uidx}"
        sec_body_id = f"{sec_id}_body"
        chunks = og.split_requirements(unit["items"], f'{unit["code"]} {unit["title"]}')
        parts.extend(
            [
                f'<section class="unit" id="{sec_id}" data-search="{h(unit["code"] + " " + unit["title"])}">',
                f'<button class="unit-toggle" type="button" onclick="toggleUnit(\'{sec_id}\')" aria-expanded="false" aria-controls="{sec_body_id}">',
                '<span class="arrow small" aria-hidden="true">▶</span>',
                f'<span class="unit-code">{h(unit["code"])}</span>',
                f'<span class="unit-title">{h(unit["title"])}</span>',
                f'<span class="unit-count">{og.polish_count(len(unit["items"]), "kryterium", "kryteria", "kryteriów")}</span>',
                "</button>",
                f'<div class="unit-body" id="{sec_body_id}">',
                render_table(chunks),
                "</div></section>",
            ]
        )
    parts.append("</div></article>")
    return "\n".join(parts), {
        "school": item["school"],
        "type": "zawodowe",
        "name": item["name"],
        "sections": len(units),
        "items": sum(len(u["items"]) for u in units),
        "status": item["status"],
        "id": card_id,
    }


def pdf_label_from_path(path: Path, general_specs_by_path: dict[str, list[str]], vocational_specs_by_path: dict[str, VocationalSpec]) -> tuple[str, str, str]:
    rel = path.as_posix()
    if rel in general_specs_by_path:
        return ", ".join(general_specs_by_path[rel]), "", "podstawa dostępna"
    if rel in vocational_specs_by_path:
        spec = vocational_specs_by_path[rel]
        quals = ", ".join(re.findall(r"[A-Z]{3}\.\d{2}", spec.source_label))
        return spec.name, quals, "do recenzji"
    name = path.stem.replace("PP_", "").replace("_", " ")
    return name, "", "do identyfikacji"


def build_pdf_manifest(general_specs: list[og.SubjectSpec]) -> list[dict]:
    general_specs_by_path: dict[str, list[str]] = {}
    for spec in general_specs:
        general_specs_by_path.setdefault(spec.path, [])
        if spec.name not in general_specs_by_path[spec.path]:
            general_specs_by_path[spec.path].append(spec.name)
    vocational_specs_by_path = {spec.path: spec for spec in VOCATIONAL_SPECS}

    items = []
    for path in sorted(ROOT.glob("0*_*/**/*.pdf")):
        rel = path.relative_to(ROOT).as_posix()
        parts = rel.split("/")
        school = {"01_BSI_stopnia": "bsi", "02_BSII_stopnia": "bsii", "03_Technikum": "technikum"}.get(parts[0], "inne")
        category = "ogolne" if len(parts) > 1 and parts[1] == "ogolne" else "zawodowe"
        title, qualification, status = pdf_label_from_path(path.relative_to(ROOT), general_specs_by_path, vocational_specs_by_path)
        items.append(
            {
                "school": school,
                "school_label": SCHOOL_LABELS.get(school, school),
                "category": category,
                "category_label": "Ogólnokształcące" if category == "ogolne" else "Zawodowe",
                "title": title,
                "qualification": qualification,
                "path": rel,
                "file_name": path.name,
                "size_bytes": path.stat().st_size,
                "size_label": f"{path.stat().st_size / 1024 / 1024:.1f} MB",
                "status": status,
            }
        )
    DATA_DIR.mkdir(exist_ok=True)
    PDF_MANIFEST.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return items


def render_pdf_library(items: list[dict], school: str) -> str:
    cards = []
    for idx, item in enumerate(items):
        card_id = f"pdf_{item['school']}_{idx}"
        search = " ".join([item["title"], item["qualification"], item["file_name"], item["category_label"]])
        cards.append(
            f"""
<article class="pdf-card" id="{card_id}" data-category="{h(item['category'])}" data-search="{h(search)}">
  <div>
    <span class="status {status_class(item['status'])}">{h(item['status'])}</span>
    <strong>{h(item['title'])}</strong>
    <p>{h(item['category_label'])}{' · ' + h(item['qualification']) if item['qualification'] else ''}</p>
    <code>{h(item['path'])}</code>
  </div>
  <div class="pdf-actions">
    <span>{h(item['size_label'])}</span>
    <a href="{h(item['path'])}" target="_blank" rel="noopener">Otwórz PDF</a>
    <a href="{h(item['path'])}" download>Pobierz PDF</a>
  </div>
</article>
"""
        )
    return f'<div class="pdf-grid">{"".join(cards)}{render_ore_cards(school)}</div>'


CARD_ID_RE = re.compile(r'id="([^"]+)"')
CARD_NAME_RE = re.compile(r'<span class="card-name">(.*?)</span>')


def render_quick_index(cards: list[str]) -> str:
    links = []
    for card in cards:
        id_match = CARD_ID_RE.search(card)
        name_match = CARD_NAME_RE.search(card)
        if id_match and name_match:
            links.append(f'<a href="#{id_match.group(1)}">{name_match.group(1)}</a>')
    return "".join(links)


def render_ore_cards(school: str) -> str:
    cards = []
    for idx, item in enumerate(entry for entry in ORE_VADEMECUM if school in entry["schools"]):
        title = " / ".join(item["subjects"])
        search = f"{title} Vademecum ORE opracowanie metodyczne podstawa programowa"
        card_id = f"pdf_{school}_ore_{idx}"
        cards.append(
            f"""
<article class="pdf-card" id="{card_id}" data-category="opracowania" data-search="{h(search)}">
  <div>
    <span class="status status-ore">ORE</span>
    <strong>{h(title)} - Vademecum nauczyciela</strong>
    <p>Opracowanie metodyczne ORE do wdrażania podstawy programowej w szkole ponadpodstawowej.</p>
    <code>{h(item['url'])}</code>
  </div>
  <div class="pdf-actions">
    <span>ore.edu.pl</span>
    <a href="{h(item['url'])}" target="_blank" rel="noopener">Otwórz PDF</a>
  </div>
</article>
"""
        )
    if not cards:
        return ""
    intro = """
<div class="ore-note">
  <strong>Opracowania ORE - Vademecum nauczyciela</strong>
  <span>To materiały pomocnicze do wdrażania podstawy programowej. Nie zastępują podstaw programowych ani szkolnej recenzji wymagań.</span>
</div>
"""
    return intro + "".join(cards)


def render_home_page(total_general: int, total_vocational: int, total_tables: int, total_items: int, total_pdf: int) -> str:
    return f"""
<main class="content-page" id="page_home" data-school="home" data-mode="home">
  <section class="home-hero">
    <div class="home-hero-text">
      <p class="eyebrow">Zespół Szkół Zawodowych nr 5 we Wrocławiu</p>
      <h2>Wymagania edukacyjne i biblioteka podstaw programowych 2026/2027</h2>
      <p>Strona porządkuje wymagania dla przedmiotów ogólnokształcących i zawodowych oraz daje szybki dostęp do lokalnych PDF-ów podstaw programowych. Materiał jest roboczym opracowaniem ZSZ5: przed publikacją szkolną wymaga sprawdzenia przez nauczycieli przedmiotów i zawodów.</p>
      <div class="home-nav-hint">
        <a href="#technikum_ogolne" onclick="setSchool('technikum');setMode('ogolne')">Technikum - ogólne</a>
        <a href="#technikum_zawodowe" onclick="setSchool('technikum');setMode('zawodowe')">Technikum - zawodowe</a>
        <a href="#bsi_ogolne" onclick="setSchool('bsi');setMode('ogolne')">BS I - ogólne</a>
        <a href="#bsii_ogolne" onclick="setSchool('bsii');setMode('ogolne')">BS II - ogólne</a>
        <a href="#technikum_pdf" onclick="setSchool('technikum');setMode('pdf')">Biblioteka PDF</a>
      </div>
    </div>
    <div class="home-logo-card">
      <img src="assets/logo-zsz5.jpg" alt="Logotyp ZSZ5 we Wrocławiu">
    </div>
  </section>

  <section class="home-section">
    <h3>Stan opracowania</h3>
    <div class="home-stats">
      <div class="stat-box"><div class="stat-num">{total_general}</div><div class="stat-label">przedmiotów ogólnokształcących</div></div>
      <div class="stat-box"><div class="stat-num">{total_vocational}</div><div class="stat-label">kierunków zawodowych</div></div>
      <div class="stat-box"><div class="stat-num">{total_tables}</div><div class="stat-label">działów i jednostek</div></div>
      <div class="stat-box"><div class="stat-num">{total_items}</div><div class="stat-label">wymagań i kryteriów</div></div>
      <div class="stat-box"><div class="stat-num">{total_pdf}</div><div class="stat-label">plików PDF</div></div>
    </div>
    <p class="home-warning"><strong>Status roboczy:</strong> wymagania na oceny są opracowaniem szkolnym. Podstawy programowe w bibliotece są źródłami, natomiast podział na oceny trzeba zatwierdzić w pracy zespołów przedmiotowych i zawodowych.</p>
  </section>

  <section class="home-section">
    <h3>Od podstawy programowej do wymagań na oceny</h3>
    <p>Podstawa programowa wskazuje obowiązkowe cele i treści kształcenia. Program nauczania porządkuje sposób realizacji tych treści w szkole, a wymagania edukacyjne przekładają je na kryteria oceniania. Dlatego ta strona nie zastępuje decyzji nauczyciela: ma być punktem startowym do recenzji, ujednolicenia i publikacji wymagań.</p>
    <div class="flow-diagram">
      <div class="flow-step">
        <div class="step-num">1</div>
        <h4>Podstawa programowa</h4>
        <p>Źródło prawne dla celów i treści nauczania. W bibliotece PDF można otworzyć lub pobrać dokumenty przypisane do typów szkół i zawodów.</p>
      </div>
      <div class="flow-step">
        <div class="step-num">2</div>
        <h4>Program nauczania</h4>
        <p>Nauczyciel lub zespół nauczycieli dobiera kolejność, metody, materiały i zakres poszerzeń, zachowując wymagania podstawy.</p>
      </div>
      <div class="flow-step">
        <div class="step-num">3</div>
        <h4>Wymagania edukacyjne</h4>
        <p>Kryteria na oceny powinny wynikać z realizowanego programu nauczania i być przedstawione uczniom oraz rodzicom na początku roku.</p>
      </div>
    </div>
  </section>

  <section class="home-section">
    <h3>Podstawy prawne i źródła</h3>
    <div class="home-cards">
      <div class="home-card">
        <h4>Ustawa o systemie oświaty, art. 22a</h4>
        <p>Reguluje przedstawianie i dopuszczanie programów nauczania do użytku w szkole. To podstawa dla szkolnej pracy nad programem, z którego wynikają wymagania.</p>
      </div>
      <div class="home-card">
        <h4>Ustawa o systemie oświaty, art. 44b</h4>
        <p>Łączy ocenianie z wymaganiami edukacyjnymi wynikającymi z realizowanego programu nauczania i nakłada obowiązek poinformowania uczniów oraz rodziców.</p>
      </div>
      <div class="home-card">
        <h4>Rozporządzenie MEN z 22 lutego 2019 r.</h4>
        <p>Określa szczegółowe warunki i sposób oceniania, klasyfikowania i promowania uczniów oraz słuchaczy w szkołach publicznych.</p>
      </div>
      <div class="home-card">
        <h4>Rozporządzenie ME z 28 czerwca 2024 r.</h4>
        <p>Zmienia podstawę programową kształcenia ogólnego dla liceum ogólnokształcącego, technikum oraz branżowej szkoły II stopnia. Nie jest jedynym źródłem dla całej strony: część przedmiotów i kwalifikacji korzysta z innych aktów wskazanych w kartach źródłowych.</p>
      </div>
    </div>
  </section>

  <section class="home-section">
    <h3>Dostosowanie wymagań do uczniów - konkretne przepisy</h3>
    <p>Wymagania edukacyjne nie są jedną sztywną tabelą dla wszystkich uczniów. Prawo rozdziela trzy sprawy: informowanie o wymaganiach, indywidualizowanie pracy oraz dostosowanie wymagań w określonych przypadkach.</p>
    <div class="home-cards">
      <div class="home-card">
        <h4>Co trzeba przekazać uczniom i rodzicom</h4>
        <span class="legal-ref">Ustawa o systemie oświaty, art. 44b ust. 8 pkt 1</span>
        <p>Nauczyciel na początku roku informuje o wymaganiach edukacyjnych niezbędnych do otrzymania poszczególnych śródrocznych i rocznych ocen klasyfikacyjnych, wynikających z realizowanego programu nauczania.</p>
      </div>
      <div class="home-card">
        <h4>Indywidualizacja pracy na lekcji</h4>
        <span class="legal-ref">Ustawa o systemie oświaty, art. 44c ust. 1</span>
        <p>Nauczyciel ma obowiązek indywidualizować pracę z uczniem na zajęciach edukacyjnych odpowiednio do potrzeb rozwojowych i edukacyjnych oraz możliwości psychofizycznych ucznia.</p>
      </div>
      <div class="home-card">
        <h4>Dostosowanie wymagań edukacyjnych</h4>
        <span class="legal-ref">Ustawa o systemie oświaty, art. 44c ust. 2</span>
        <p>Nauczyciel dostosowuje wymagania, o których mowa w art. 44b ust. 8 pkt 1, do indywidualnych potrzeb rozwojowych i edukacyjnych oraz możliwości psychofizycznych ucznia w przypadkach wskazanych w przepisach o ocenianiu.</p>
      </div>
      <div class="home-card">
        <h4>Kiedy dostosowanie jest wymagane</h4>
        <span class="legal-ref">Rozporządzenie MEN z 22.02.2019 r., § 2</span>
        <p>§ 2 rozporządzenia wskazuje, że wymagania dostosowuje się m.in. dla ucznia:</p>
        <ul>
          <li>z orzeczeniem o potrzebie kształcenia specjalnego - na podstawie orzeczenia i IPET,</li>
          <li>z orzeczeniem o potrzebie indywidualnego nauczania,</li>
          <li>z opinią poradni psychologiczno-pedagogicznej, w tym o specyficznych trudnościach w uczeniu się,</li>
          <li>objętego pomocą psychologiczno-pedagogiczną w szkole na podstawie rozpoznania nauczycieli i specjalistów,</li>
          <li>z opinią lekarza o ograniczonych możliwościach wykonywania określonych ćwiczeń fizycznych na WF.</li>
        </ul>
      </div>
    </div>
    <p class="home-warning"><strong>Wniosek dla tej strony:</strong> publikowana tabela może być wspólnym punktem wyjścia, ale nauczyciel musi mieć możliwość dopisania dostosowań dla konkretnego ucznia lub oddziału. Dlatego status materiału pozostaje roboczy do zatwierdzenia przez nauczyciela.</p>
  </section>

  <section class="home-section">
    <h3>Rozkład materiału - po co jest potrzebny</h3>
    <p>Rozkład materiału to praktyczny plan pracy nauczyciela na rok, semestr lub dział. Nie zastępuje podstawy programowej, programu nauczania ani wymagań edukacyjnych. Pokazuje natomiast, jak nauczyciel rozkłada treści programu w czasie i jak łączy je z lekcjami, ćwiczeniami, sprawdzaniem osiągnięć oraz możliwościami konkretnej klasy.</p>
    <div class="home-cards">
      <div class="home-card">
        <h4>Co powinien porządkować</h4>
        <ul>
          <li>kolejność działów i tematów,</li>
          <li>liczbę godzin lub orientacyjny czas realizacji,</li>
          <li>powiązanie tematów z wymaganiami podstawy programowej,</li>
          <li>planowane formy sprawdzania osiągnięć,</li>
          <li>miejsca na powtórzenia, projekty, pracę praktyczną i poprawę.</li>
        </ul>
      </div>
      <div class="home-card">
        <h4>Dlaczego jest potrzebny</h4>
        <p>Bez rozkładu materiału łatwo mieć tabelę wymagań, która wygląda kompletnie, ale nie wynika z realnego tempa pracy klasy. Rozkład pozwala sprawdzić, czy wszystkie treści da się zrealizować w kalendarzu roku szkolnego i czy ocenianie jest zaplanowane w sensownych momentach.</p>
      </div>
      <div class="home-card">
        <h4>Jak łączy się z dostosowaniami</h4>
        <p>Dostosowania wymagań nie polegają wyłącznie na zmianie tabeli ocen. W praktyce wpływają także na tempo, formy pracy, liczbę ćwiczeń, sposób sprawdzania wiedzy i dobór materiałów. To właśnie rozkład materiału pomaga przełożyć dostosowania na codzienną pracę z klasą.</p>
      </div>
    </div>
  </section>

  <section class="home-section">
    <h3>Co znaczy dostosować podstawę w praktyce</h3>
    <p>Nie dostosowuje się samej podstawy programowej jako aktu prawnego: jej wymagania pozostają punktem odniesienia. Dostosowuje się sposób realizacji podstawy w szkolnym programie, rozkładzie materiału, metodach pracy, formach sprawdzania osiągnięć i wymaganiach edukacyjnych dla konkretnych uczniów. W praktyce oznacza to decyzje o tempie, kolejności, przykładach, ćwiczeniach, sposobach odpowiedzi, kryteriach oceniania i wsparciu, przy zachowaniu obowiązkowych celów i treści.</p>
    <div class="home-cards">
      <div class="home-card">
        <h4>1. Od podstawy do programu</h4>
        <p>Najpierw trzeba ustalić, które cele i treści są obowiązkowe. Program nauczania nie jest kopią podstawy: porządkuje jej realizację w konkretnym oddziale i w konkretnych warunkach szkoły.</p>
      </div>
      <div class="home-card">
        <h4>2. Od programu do rozkładu</h4>
        <p>Rozkład materiału przekłada program na kalendarz pracy. To w nim widać, czy tempo jest realne, gdzie są powtórzenia, kiedy uczniowie ćwiczą umiejętności i kiedy nauczyciel sprawdza osiągnięcia.</p>
      </div>
      <div class="home-card">
        <h4>3. Od wymagań do dostosowań</h4>
        <p>Wymagania na oceny powinny być zrozumiałe dla ucznia, ale mogą wymagać dostosowania formy, czasu pracy, sposobu odpowiedzi, liczby przykładów lub poziomu wsparcia, jeżeli wynika to z potrzeb i możliwości ucznia.</p>
      </div>
      <div class="home-card">
        <h4>4. Co nie powinno się wydarzyć</h4>
        <p>Dostosowanie nie może oznaczać przypadkowego usunięcia kluczowych efektów kształcenia ani tabeli ocen oderwanej od programu. Powinno być udokumentowaną decyzją nauczyciela, zespołu lub szkoły, zgodną z podstawą i przepisami o ocenianiu.</p>
      </div>
    </div>
  </section>

  <section class="home-section">
    <h3>Przydatne materiały i linki</h3>
    <p>Poniższe linki prowadzą do materiałów, które warto wykorzystać przy recenzji wymagań, tworzeniu rozkładów materiału i planowaniu dostosowań. Źródła zewnętrzne są pomocnicze: wiążące pozostają aktualne akty prawne oraz szkolne decyzje nauczycieli i zespołów przedmiotowych.</p>
    <div class="home-cards resource-grid">
      <div class="home-card">
        <h4>MEN - materiały dla nauczycieli szkół ponadpodstawowych</h4>
        <p>Pakiet pomocniczy do rozumienia podstawy programowej: preambuła, komentarze, porównania, uzasadnienia i rekomendacje.</p>
        <a class="resource-link" href="https://www.gov.pl/web/edukacja/podstawa-programowa--materialy-dla-nauczycieli-szkol-ponadpodstawowych" target="_blank" rel="noopener">Otwórz materiał</a>
      </div>
      <div class="home-card">
        <h4>ORE - podstawa programowa z 28 czerwca 2024 r.</h4>
        <p>Strona ORE porządkująca materiały związane ze zmianami podstawy programowej, przydatna przy sprawdzaniu aktualnego zakresu treści.</p>
        <a class="resource-link" href="https://ore.edu.pl/2024/09/podstawa-programowa-z-28-czerwca-2024-r/" target="_blank" rel="noopener">Otwórz materiał</a>
      </div>
      <div class="home-card">
        <h4>ORE - programy nauczania do szkoły ponadpodstawowej</h4>
        <p>Przykładowe programy nauczania pokazujące, jak przejść od podstawy programowej do realnej organizacji pracy w szkole.</p>
        <a class="resource-link" href="https://ore.edu.pl/2020/04/programy-nauczania-programy-do-szkoly-ponadpodstawowej/" target="_blank" rel="noopener">Otwórz materiał</a>
      </div>
      <div class="home-card">
        <h4>ORE - dostosowanie wymagań edukacyjnych</h4>
        <p>Praktyczny materiał o dostosowaniu wymagań wobec uczniów ze specyficznymi trudnościami w uczeniu się, z przykładami pracy nauczyciela.</p>
        <a class="resource-link" href="https://ore.edu.pl/wp-content/uploads/2015/03/dostosowanie-wymagan-edukacyjnych-wobec-uczniow-ze-specyficznymi-trudnosciami-w-uczeniu-sie.pdf" target="_blank" rel="noopener">Otwórz PDF</a>
      </div>
      <div class="home-card">
        <h4>ORE - podstawa prawna indywidualizacji nauczania</h4>
        <p>Omówienie przepisów i praktycznych konsekwencji indywidualizacji pracy z uczniem oraz dostosowywania wymagań.</p>
        <a class="resource-link" href="https://ore.edu.pl/2025/10/podstawa-prawna-indywidualizacji-nauczania/" target="_blank" rel="noopener">Otwórz materiał</a>
      </div>
      <div class="home-card">
        <h4>IBE PIB - podstawy programowe i kierunki zmian</h4>
        <p>Miejsce do monitorowania prac nad podstawami programowymi i szerszego kontekstu zmian w edukacji. Do bieżącej publikacji szkolnej trzeba je zestawiać z obowiązującymi aktami prawnymi.</p>
        <a class="resource-link" href="https://ibe.edu.pl/pl/podstawy-programowe" target="_blank" rel="noopener">Otwórz materiał</a>
      </div>
    </div>
    <p class="source-note">Ostatnie sprawdzenie linków źródłowych: 24 czerwca 2026 r.</p>
  </section>

  <section class="home-section">
    <h3>Jak korzystać ze strony</h3>
    <div class="home-cards">
      <div class="home-card">
        <h4>Wybierz typ szkoły</h4>
        <p>Górne zakładki prowadzą do technikum, branżowej szkoły I stopnia i branżowej szkoły II stopnia.</p>
      </div>
      <div class="home-card">
        <h4>Przełącz typ treści</h4>
        <p>Można osobno przeglądać przedmioty ogólnokształcące, zawodowe oraz bibliotekę PDF.</p>
      </div>
      <div class="home-card">
        <h4>Sprawdź źródło</h4>
        <p>Każda karta ma informację o podstawie lub PDF-ie źródłowym. Pozycje zawodowe są oznaczone jako wymagające recenzji nauczycieli zawodu.</p>
      </div>
    </div>
  </section>
</main>
"""


def render_page(general_specs: list[og.SubjectSpec], vocational_data: list[dict], pdf_items: list[dict]) -> tuple[str, list[dict]]:
    grouped_general = {key: [] for key in SCHOOL_LABELS}
    grouped_voc = {key: [] for key in SCHOOL_LABELS}
    stats = []

    for spec in general_specs:
        idx = len(grouped_general[spec.school])
        html_part, stat = render_general_card(spec, idx)
        grouped_general[spec.school].append(html_part)
        stats.append(stat)

    for item in vocational_data:
        idx = len(grouped_voc[item["school"]])
        html_part, stat = render_vocational_card(item, idx)
        grouped_voc[item["school"]].append(html_part)
        stats.append(stat)

    total_tables = sum(stat["sections"] for stat in stats)
    total_items = sum(stat["items"] for stat in stats)
    total_pdf = len(pdf_items)

    school_tabs = '<button class="tab-btn active" type="button" id="school_home" onclick="setHome()" data-color="#f59e0b" aria-selected="true">Start</button>\n' + "\n".join(
        f'<button class="tab-btn" type="button" id="school_{key}" onclick="setSchool(\'{key}\')" data-color="{SCHOOL_COLORS[key]}" aria-selected="false">{SCHOOL_SHORT[key]}</button>'
        for key in ["technikum", "bsi", "bsii"]
    )
    content_tabs = "\n".join(
        f'<button class="mode-btn" type="button" id="mode_{key}" onclick="setMode(\'{key}\')" aria-selected="false">{label}</button>'
        for key, label in [
            ("ogolne", "Ogólnokształcące"),
            ("zawodowe", "Zawodowe"),
            ("pdf", "Biblioteka PDF"),
        ]
    )

    page_sections = [
        render_home_page(
            len([s for s in stats if s["type"] == "ogolne"]),
            len([s for s in stats if s["type"] == "zawodowe"]),
            total_tables,
            total_items,
            total_pdf,
        )
    ]
    for school in ["technikum", "bsi", "bsii"]:
        general_index = render_quick_index(grouped_general[school])
        voc_index = render_quick_index(grouped_voc[school])
        page_sections.append(
            f"""
<main class="content-page" id="page_{school}_ogolne" data-school="{school}" data-mode="ogolne">
  <div class="page-head">
    <h2 style="color:{SCHOOL_COLORS[school]}">{SCHOOL_LABELS[school]} · przedmioty ogólnokształcące</h2>
    <div class="quick-index">{general_index}</div>
  </div>
  <div class="cards-list">{''.join(grouped_general[school])}</div>
</main>
<main class="content-page" id="page_{school}_zawodowe" data-school="{school}" data-mode="zawodowe">
  <div class="page-head">
    <h2 style="color:{SCHOOL_COLORS[school]}">{SCHOOL_LABELS[school]} · kształcenie zawodowe</h2>
    <p>Sekcje zawodowe są przebudowane automatycznie z lokalnych PDF-ów i oznaczone do recenzji nauczycieli zawodów.</p>
    <div class="quick-index">{voc_index or '<span>Brak kierunków zawodowych w tej szkole.</span>'}</div>
  </div>
  <div class="cards-list">{''.join(grouped_voc[school]) or '<p class="empty-page">Brak kierunków zawodowych dla tego typu szkoły.</p>'}</div>
</main>
<main class="content-page" id="page_{school}_pdf" data-school="{school}" data-mode="pdf">
  <div class="page-head">
    <h2 style="color:{SCHOOL_COLORS[school]}">{SCHOOL_LABELS[school]} · biblioteka podstaw programowych</h2>
    <div class="category-filter" role="group" aria-label="Filtr kategorii PDF">
      <button type="button" onclick="setPdfCategory('all')" class="pdf-filter active" data-pdf-filter="all">Wszystkie</button>
      <button type="button" onclick="setPdfCategory('ogolne')" class="pdf-filter" data-pdf-filter="ogolne">Ogólnokształcące</button>
      <button type="button" onclick="setPdfCategory('zawodowe')" class="pdf-filter" data-pdf-filter="zawodowe">Zawodowe</button>
      <button type="button" onclick="setPdfCategory('opracowania')" class="pdf-filter" data-pdf-filter="opracowania">Opracowania ORE</button>
    </div>
  </div>
  {render_pdf_library([item for item in pdf_items if item['school'] == school], school)}
</main>
"""
        )

    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Wymagania edukacyjne ZSZ5 2026/2027</title>
<link rel="icon" href="assets/logo-zsz5.jpg">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;background:#f3f4f6;color:#111827;min-height:100vh}}
a{{color:inherit}}
.skip-link{{position:absolute;left:12px;top:-48px;background:#111827;color:#fff;padding:8px 12px;border-radius:4px;z-index:200;text-decoration:none}}
.skip-link:focus{{top:12px}}
header{{background:#111827;color:#fff;padding:18px 24px}}
.brand{{display:flex;align-items:center;gap:14px;max-width:1180px;margin:0 auto}}
.brand-logo{{width:74px;height:52px;object-fit:contain;background:#fff;border-radius:6px;padding:3px;flex-shrink:0}}
header h1{{font-size:1.25rem}}
header p{{font-size:.86rem;color:#cbd5e1;margin-top:5px;line-height:1.45}}
.summary{{background:#fff7ed;border-bottom:1px solid #fed7aa;color:#7c2d12;padding:12px 24px;font-size:.88rem;line-height:1.45}}
.top-tabs{{position:sticky;top:0;z-index:40;background:#1e293b;color:#fff;box-shadow:0 2px 8px rgba(0,0,0,.2)}}
.tab-row{{display:flex;gap:0;overflow-x:auto;padding:0 16px;border-bottom:1px solid #334155}}
.tab-btn,.mode-btn{{padding:12px 16px;border:none;border-bottom:3px solid transparent;background:transparent;color:#cbd5e1;font-weight:700;white-space:nowrap;cursor:pointer}}
.tab-btn.active{{color:#fff;background:rgba(255,255,255,.08);border-bottom-color:var(--tab-color,#fff)}}
.mode-btn.active{{color:#fff;background:#334155;border-bottom-color:#f59e0b}}
.tools{{display:grid;grid-template-columns:minmax(160px,220px) minmax(260px,1fr) auto;gap:10px;align-items:center;padding:12px 24px;background:#fff;color:#111827;border-bottom:1px solid #e5e7eb}}
.tools label{{font-size:.82rem;font-weight:700;color:#374151}}
.tools input{{width:100%;padding:8px 10px;border:1px solid #cbd5e1;border-radius:6px}}
.tools button,.card-actions button,.category-filter button{{padding:6px 10px;border:1px solid #d1d5db;background:#fff;border-radius:4px;cursor:pointer;font-size:.82rem}}
.filter-status{{font-size:.8rem;color:#6b7280}}
.content-page{{display:none;padding-bottom:42px}}
.page-head{{padding:18px 24px 8px}}
.page-head h2{{font-size:1.2rem;margin-bottom:5px}}
.page-head p{{font-size:.88rem;color:#6b7280;line-height:1.45}}
.quick-index{{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}}
.quick-index a,.quick-index span{{display:inline-flex;align-items:center;min-height:28px;padding:4px 8px;border:1px solid #d1d5db;border-radius:4px;background:#fff;text-decoration:none;font-size:.78rem;color:#374151}}
.cards-list{{padding:12px 16px;display:flex;flex-direction:column;gap:10px}}
.content-card{{background:#fff;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.08);overflow:hidden}}
.card-toggle{{width:100%;display:flex;align-items:center;gap:10px;padding:14px 16px;border:none;border-left:4px solid;background:#fff;text-align:left;cursor:pointer}}
.arrow{{font-size:.75rem;transition:transform .2s;flex-shrink:0}}
.small{{font-size:.65rem;color:#6b7280}}
.card-name{{font-weight:800;flex:1}}
.card-meta{{font-size:.8rem;color:#6b7280;flex-shrink:0}}
.card-body{{display:none;border-top:1px solid #f3f4f6;padding:10px 12px;gap:8px;flex-direction:column}}
.source-box,.goals-box{{background:#f8fafc;border:1px solid #e5e7eb;border-radius:6px;padding:10px 12px;font-size:.82rem;line-height:1.45;color:#374151;margin-bottom:8px}}
.source-box summary,.goals-box summary{{cursor:pointer;font-weight:700}}
.source-box code{{display:block;margin-top:6px;color:#4b5563;word-break:break-all}}
.note{{margin-top:6px;color:#92400e}}
.cumulative{{font-size:.82rem;color:#4b5563;margin:4px 0 8px;line-height:1.45}}
.status{{display:inline-block;margin-right:8px;padding:2px 7px;border-radius:999px;font-size:.72rem;font-weight:800;text-transform:uppercase}}
.status-ok{{background:#dcfce7;color:#166534}}
.status-review{{background:#fef3c7;color:#92400e}}
.status-ore{{background:#e0e7ff;color:#3730a3}}
.home-hero{{display:grid;grid-template-columns:minmax(0,1fr) 180px;gap:24px;align-items:center;padding:30px 24px;background:#1e293b;color:#fff}}
.home-hero h2{{font-size:1.55rem;line-height:1.18;margin:4px 0 10px;max-width:780px}}
.home-hero p{{color:#dbeafe;font-size:.94rem;line-height:1.55;max-width:850px}}
.eyebrow{{font-size:.76rem;text-transform:uppercase;letter-spacing:0;color:#fde68a;font-weight:800}}
.home-logo-card{{display:flex;justify-content:center;align-items:center;background:#fff;border-radius:8px;padding:12px;min-height:130px}}
.home-logo-card img{{width:100%;max-width:160px;height:auto;display:block}}
.home-section{{padding:20px 24px 4px}}
.home-section h3{{font-size:1rem;font-weight:800;color:#1f2937;margin-bottom:10px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}}
.home-section>p{{font-size:.88rem;color:#374151;line-height:1.6;margin-bottom:14px}}
.home-cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-bottom:14px}}
.home-card{{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:14px;box-shadow:0 1px 2px rgba(0,0,0,.05)}}
.home-card h4{{font-size:.9rem;font-weight:800;color:#1e40af;margin-bottom:6px}}
.home-card p{{font-size:.84rem;color:#374151;line-height:1.5}}
.home-card ul{{padding-left:18px;margin-top:8px}}
.home-card li{{font-size:.82rem;color:#374151;line-height:1.45;margin-bottom:5px}}
.legal-ref{{display:inline-block;margin-bottom:7px;padding:3px 7px;border-radius:4px;background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe;font-size:.74rem;font-weight:800}}
.resource-grid .home-card{{display:flex;flex-direction:column;gap:8px}}
.resource-link{{display:inline-flex;align-items:center;justify-content:center;align-self:flex-start;min-height:32px;margin-top:auto;padding:6px 10px;border-radius:4px;border:1px solid #bfdbfe;background:#eff6ff;color:#1e40af;text-decoration:none;font-size:.8rem;font-weight:800}}
.resource-link:hover{{background:#dbeafe;border-color:#93c5fd}}
.source-note{{font-size:.76rem;color:#6b7280;margin-top:-2px}}
.flow-diagram{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:12px 0 14px}}
.flow-step{{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:14px}}
.flow-step .step-num{{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:999px;background:#1e293b;color:#fff;font-size:.78rem;font-weight:800;margin-bottom:8px}}
.flow-step h4{{font-size:.9rem;color:#111827;margin-bottom:6px}}
.flow-step p{{font-size:.82rem;color:#4b5563;line-height:1.5}}
.home-warning{{background:#fef3c7;border:1px solid #fde68a;border-radius:8px;padding:12px 14px;color:#92400e}}
.home-stats{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-bottom:14px}}
.stat-box{{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:14px;text-align:center;box-shadow:0 1px 2px rgba(0,0,0,.05)}}
.stat-num{{font-size:1.55rem;font-weight:800;color:#1e40af;line-height:1}}
.stat-label{{font-size:.72rem;color:#6b7280;margin-top:5px;line-height:1.25}}
.home-nav-hint{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}
.home-nav-hint a{{display:inline-flex;align-items:center;min-height:32px;color:#fff;text-decoration:none;padding:6px 10px;border-radius:4px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.24);font-size:.8rem;font-weight:700}}
.ore-note{{margin:0 0 2px;padding:10px 12px;background:#eef2ff;border:1px solid #c7d2fe;border-radius:8px;font-size:.82rem;color:#3730a3;line-height:1.45}}
.ore-note strong{{display:block;margin-bottom:2px}}
.chips{{display:flex;gap:6px;flex-wrap:wrap;margin:4px 0 8px}}
.chips span{{background:#eef2ff;color:#3730a3;border:1px solid #c7d2fe;border-radius:999px;padding:3px 8px;font-size:.76rem;font-weight:700}}
.unit{{background:#f9fafb;border:1px solid #e5e7eb;border-radius:6px;overflow:hidden;margin-bottom:7px}}
.unit-toggle{{width:100%;display:flex;align-items:center;gap:8px;padding:10px 14px;border:none;background:#f9fafb;text-align:left;cursor:pointer}}
.unit-toggle:hover{{background:#f3f4f6}}
.unit-code{{font-weight:800;color:#374151;font-size:.85rem;flex-shrink:0}}
.unit-title{{font-size:.85rem;color:#374151;flex:1}}
.unit-count{{font-size:.75rem;color:#9ca3af;flex-shrink:0}}
.unit-body{{display:none;padding:8px;border-top:1px solid #e5e7eb;background:#fff}}
.table-wrap{{overflow-x:auto;scrollbar-gutter:stable}}
table{{width:100%;border-collapse:collapse;table-layout:fixed;min-width:980px}}
th{{padding:8px 6px;border:1px solid #d1d5db;background:#f3f4f6;font-size:.78rem;color:#374151;text-align:left}}
td{{vertical-align:top;padding:8px 10px;border:1px solid #e5e7eb;font-size:.78rem;line-height:1.38}}
th:nth-child(1),td:nth-child(1){{background:#fff7ed;border-color:#fed7aa}}
th:nth-child(2),td:nth-child(2){{background:#f0fdf4;border-color:#bbf7d0}}
th:nth-child(3),td:nth-child(3){{background:#eff6ff;border-color:#bfdbfe}}
th:nth-child(4),td:nth-child(4){{background:#faf5ff;border-color:#e9d5ff}}
th:nth-child(5),td:nth-child(5){{background:#fefce8;border-color:#fde68a}}
td ul{{padding-left:16px}}
td li{{margin-bottom:5px}}
.review-note{{color:#92400e;font-style:italic}}
.category-filter{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}}
.category-filter button.active{{background:#1e293b;color:#fff;border-color:#1e293b}}
.pdf-grid{{padding:12px 16px;display:grid;gap:10px}}
.pdf-card{{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;background:#fff;border-radius:8px;border:1px solid #e5e7eb;padding:12px;box-shadow:0 1px 2px rgba(0,0,0,.05)}}
.pdf-card p{{font-size:.82rem;color:#6b7280;margin-top:4px}}
.pdf-card code{{display:block;margin-top:5px;color:#4b5563;font-size:.76rem;word-break:break-all}}
.pdf-actions{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end;min-width:240px}}
.pdf-actions span{{font-size:.78rem;color:#6b7280}}
.pdf-actions a{{padding:6px 9px;border:1px solid #cbd5e1;background:#f8fafc;border-radius:4px;text-decoration:none;font-size:.8rem;color:#111827}}
.empty-page{{padding:20px;background:#fff;border-radius:8px;color:#6b7280}}
[hidden]{{display:none!important}}
button:focus-visible,a:focus-visible,input:focus-visible{{outline:3px solid #f59e0b;outline-offset:2px}}
.back-top{{position:fixed;right:16px;bottom:16px;z-index:50;width:42px;height:42px;border-radius:999px;border:1px solid #cbd5e1;background:#fff;color:#1f2937;box-shadow:0 2px 8px rgba(0,0,0,.16);cursor:pointer;font-size:1.1rem}}
@media (max-width:900px){{.tools{{grid-template-columns:1fr;padding:12px 16px}}.card-toggle,.unit-toggle{{align-items:flex-start}}.card-meta,.unit-count{{display:none}}.pdf-card{{flex-direction:column}}.pdf-actions{{justify-content:flex-start;min-width:0}}table{{min-width:760px}}header,.summary,.page-head{{padding-left:16px;padding-right:16px}}.home-hero{{grid-template-columns:1fr;padding:22px 16px}}.home-logo-card{{justify-content:flex-start;min-height:0;max-width:190px}}.home-section{{padding:16px 16px 4px}}.flow-diagram{{grid-template-columns:1fr}}.home-stats{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (max-width:640px){{.table-wrap{{overflow-x:visible}}table{{min-width:0;table-layout:auto}}thead{{display:none}}tr,td{{display:block;width:100%}}td{{border-width:1px 1px 0}}td:last-child{{border-bottom-width:1px}}td::before{{content:attr(data-label);display:block;font-weight:800;color:#374151;margin-bottom:5px}}}}
@media print{{.skip-link,.top-tabs,.tools,.quick-index,.card-actions,.back-top{{display:none}}.content-page{{display:block!important}}.card-body,.unit-body{{display:block!important}}body{{background:#fff}}.content-card,.unit,.pdf-card{{break-inside:avoid}}.table-wrap{{overflow:visible}}table{{min-width:700px}}}}
</style>
</head>
<body>
<a class="skip-link" href="#main_content">Przejdź do treści</a>
<header>
  <div class="brand">
    <img class="brand-logo" src="assets/logo-zsz5.jpg" alt="Logotyp ZSZ5 we Wrocławiu">
    <div>
      <h1>Wymagania edukacyjne ZSZ5 2026/2027</h1>
      <p>Jedna strona do przeglądania wymagań ogólnokształcących, zawodowych oraz lokalnej biblioteki PDF podstaw programowych.</p>
    </div>
  </div>
</header>
<div class="summary">
  <strong>Status:</strong> {len([s for s in stats if s['type'] == 'ogolne'])} przedmiotów ogólnokształcących, {len([s for s in stats if s['type'] == 'zawodowe'])} kierunków zawodowych, {total_tables} działów/jednostek, {total_items} wymagań/kryteriów, {total_pdf} plików PDF. To robocze opracowanie ZSZ5; przed udostępnieniem uczniom i rodzicom każde wymaganie powinno zostać sprawdzone przez nauczyciela przedmiotu lub zawodu i dostosowane do programu nauczania w danym oddziale.
</div>
<nav class="top-tabs" aria-label="Nawigacja główna">
  <div class="tab-row" role="tablist" aria-label="Typ szkoły">{school_tabs}</div>
  <div class="tab-row" role="tablist" aria-label="Typ treści">{content_tabs}</div>
</nav>
<div class="tools" role="search">
  <label for="global_search">Szukaj</label>
  <input id="global_search" type="search" placeholder="np. matematyka, kucharz, HAN.01, pierwsza pomoc, PDF" oninput="filterCurrentPage()">
  <div class="filter-status" id="filter_status" aria-live="polite"></div>
</div>
<div id="main_content">
{''.join(page_sections)}
</div>
<button class="back-top" type="button" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="Wróć na górę">↑</button>
<script>
let activeSchool='home';
let activeMode='home';
let activePdfCategory='all';
function normalizeText(value){{
  return (value || '').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
}}
function setSchool(school, updateHash=true){{
  activeSchool=school;
  document.querySelectorAll('.tab-btn').forEach(btn=>{{
    btn.classList.toggle('active', btn.id==='school_'+school);
    btn.setAttribute('aria-selected', btn.id==='school_'+school ? 'true' : 'false');
    if(btn.id==='school_'+school) btn.style.setProperty('--tab-color', btn.dataset.color || '#fff');
  }});
  showActivePage();
  if(updateHash) history.replaceState(null,'','#'+activeSchool+'_'+activeMode);
}}
function setHome(updateHash=true){{
  activeSchool='home';
  activeMode='home';
  document.querySelectorAll('.tab-btn').forEach(btn=>{{
    btn.classList.toggle('active', btn.id==='school_home');
    btn.setAttribute('aria-selected', btn.id==='school_home' ? 'true' : 'false');
  }});
  document.querySelectorAll('.mode-btn').forEach(btn=>{{
    btn.classList.remove('active');
    btn.setAttribute('aria-selected','false');
  }});
  showActivePage();
  if(updateHash) history.replaceState(null,'','#home');
}}
function setMode(mode, updateHash=true){{
  if(activeSchool==='home') activeSchool='technikum';
  activeMode=mode;
  document.querySelectorAll('.tab-btn').forEach(btn=>{{
    btn.classList.toggle('active', btn.id==='school_'+activeSchool);
    btn.setAttribute('aria-selected', btn.id==='school_'+activeSchool ? 'true' : 'false');
  }});
  document.querySelectorAll('.mode-btn').forEach(btn=>{{
    btn.classList.toggle('active', btn.id==='mode_'+mode);
    btn.setAttribute('aria-selected', btn.id==='mode_'+mode ? 'true' : 'false');
  }});
  showActivePage();
  if(updateHash) history.replaceState(null,'','#'+activeSchool+'_'+activeMode);
}}
function showActivePage(){{
  document.querySelectorAll('.content-page').forEach(page=>page.style.display='none');
  const pageId=activeSchool==='home' ? 'page_home' : 'page_'+activeSchool+'_'+activeMode;
  const page=document.getElementById(pageId);
  if(page) page.style.display='block';
  filterCurrentPage();
}}
function setCardState(card, open){{
  const body=card.querySelector('.card-body');
  const button=card.querySelector('.card-toggle');
  const arrow=button.querySelector('.arrow');
  body.style.display=open?'flex':'none';
  button.setAttribute('aria-expanded', open ? 'true' : 'false');
  arrow.style.transform=open?'rotate(90deg)':'rotate(0deg)';
}}
function setUnitState(unit, open){{
  const body=unit.querySelector('.unit-body');
  const button=unit.querySelector('.unit-toggle');
  const arrow=button.querySelector('.arrow');
  body.style.display=open?'block':'none';
  button.setAttribute('aria-expanded', open ? 'true' : 'false');
  arrow.style.transform=open?'rotate(90deg)':'rotate(0deg)';
}}
function toggleCard(id){{
  const card=document.getElementById(id);
  if(!card) return;
  setCardState(card, card.querySelector('.card-body').style.display!=='flex');
  history.replaceState(null,'','#'+id);
}}
function toggleUnit(id){{
  const unit=document.getElementById(id);
  if(!unit) return;
  setUnitState(unit, unit.querySelector('.unit-body').style.display!=='block');
  history.replaceState(null,'','#'+id);
}}
function expandSections(cardId, open){{
  const card=document.getElementById(cardId);
  if(!card) return;
  setCardState(card,true);
  card.querySelectorAll('.unit').forEach(unit=>setUnitState(unit,open));
}}
function filterCurrentPage(){{
  const pageId=activeSchool==='home' ? 'page_home' : 'page_'+activeSchool+'_'+activeMode;
  const page=document.getElementById(pageId);
  const input=document.getElementById('global_search');
  const status=document.getElementById('filter_status');
  const query=normalizeText(input ? input.value.trim() : '');
  let visible=0;
  if(!page) return;
  page.querySelectorAll('.content-card').forEach(card=>{{
    const hit=!query || normalizeText(card.dataset.search).includes(query);
    card.hidden=!hit;
    if(hit) visible++;
    if(query && hit) setCardState(card,true);
  }});
  page.querySelectorAll('.pdf-card').forEach(card=>{{
    const categoryHit=activePdfCategory==='all' || card.dataset.category===activePdfCategory;
    const textHit=!query || normalizeText(card.dataset.search).includes(query);
    card.hidden=!(categoryHit && textHit);
    if(categoryHit && textHit) visible++;
  }});
  if(status) status.textContent=query ? `Widoczne wyniki: ${{visible}}.` : '';
}}
function setPdfCategory(category){{
  activePdfCategory=category;
  document.querySelectorAll('.pdf-filter').forEach(btn=>btn.classList.toggle('active', btn.dataset.pdfFilter===category));
  filterCurrentPage();
}}
function openFromHash(){{
  const raw=decodeURIComponent(location.hash || '').replace(/^#/,'');
  if(!raw){{
    setHome(false);
    return;
  }}
  if(raw==='home'){{
    setHome(false);
    return;
  }}
  const pageMatch=raw.match(/^(technikum|bsi|bsii)_(ogolne|zawodowe|pdf)$/);
  if(pageMatch){{
    setSchool(pageMatch[1], false);
    setMode(pageMatch[2], false);
    return;
  }}
  const el=document.getElementById(raw);
  if(!el){{
    setSchool('technikum', false);
    setMode('ogolne', false);
    return;
  }}
  const page=el.closest('.content-page');
  if(page){{
    setSchool(page.dataset.school, false);
    setMode(page.dataset.mode, false);
  }}
  const card=el.classList.contains('content-card') ? el : el.closest('.content-card');
  if(card) setCardState(card,true);
  if(el.classList.contains('unit')) setUnitState(el,true);
  setTimeout(()=>el.scrollIntoView({{behavior:'smooth',block:'start'}}),0);
}}
window.addEventListener('hashchange', openFromHash);
openFromHash();
</script>
</body>
</html>
""", stats


def write_reports(stats: list[dict], vocational_data: list[dict], pdf_items: list[dict]) -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    by_type = {
        "ogolne": [s for s in stats if s["type"] == "ogolne"],
        "zawodowe": [s for s in stats if s["type"] == "zawodowe"],
    }
    lines = [
        "# Raport integracji wymagań i biblioteki PDF",
        "",
        "Data: 2026-06-10.",
        "",
        f"- Plik strony: `{OUT.name}`.",
        f"- Plik startowy GitHub Pages: `{INDEX.name}`.",
        f"- Manifest PDF: `{PDF_MANIFEST.relative_to(ROOT).as_posix()}`.",
        f"- Przedmioty ogólnokształcące: {len(by_type['ogolne'])}.",
        f"- Kierunki zawodowe: {len(by_type['zawodowe'])}.",
        f"- Działy/jednostki: {sum(s['sections'] for s in stats)}.",
        f"- Wymagania/kryteria: {sum(s['items'] for s in stats)}.",
        f"- Pliki PDF w bibliotece: {len(pdf_items)}.",
        "",
        "## Status",
        "",
        "- Część ogólnokształcąca korzysta z naprawionego generatora ogólnego.",
        "- Część zawodowa została przebudowana z lokalnych PDF i oznaczona jako `do recenzji`.",
        "- Biblioteka PDF korzysta z relatywnych ścieżek, gotowych do GitHub Pages.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    audit = [
        "# Audyt i przebudowa wymagań zawodowych",
        "",
        "Data: 2026-06-10.",
        "",
        "Obecny statyczny HTML zawodowy nie został użyty jako źródło prawdy. Wymagania zawodowe zostały ponownie zbudowane z lokalnych PDF-ów podstaw programowych.",
        "",
        "| Typ szkoły | Zawód | Jednostki | Kryteria źródłowe | Status | PDF |",
        "|---|---|---:|---:|---|---|",
    ]
    for item in vocational_data:
        audit.append(
            f"| {SCHOOL_LABELS[item['school']]} | {item['name']} | {len(item['units'])} | {sum(len(u['items']) for u in item['units'])} | {item['status']} | `{item['path']}` |"
        )
    audit.extend(
        [
            "",
            "## Ryzyka",
            "",
            "- Ekstrakcja zawodowa jest automatyczna i wymaga recenzji nauczycieli zawodów.",
            "- Generator usuwa puste komórki przez opracowanie progów ocen z kryteriów weryfikacji, ale nie zastępuje zatwierdzenia merytorycznego.",
            "- Warunki realizacji i tabele godzin nie są traktowane jako wymagania na oceny.",
        ]
    )
    VOC_AUDIT.write_text("\n".join(audit) + "\n", encoding="utf-8")


def main() -> None:
    general_specs = og.specs()
    vocational_data = [extract_vocational_units(spec) for spec in VOCATIONAL_SPECS]
    pdf_items = build_pdf_manifest(general_specs)
    html_page, stats = render_page(general_specs, vocational_data, pdf_items)
    OUT.write_text(html_page, encoding="utf-8")
    shutil.copy2(OUT, INDEX)
    write_reports(stats, vocational_data, pdf_items)
    print(f"Generated {OUT}")
    print(f"Generated {INDEX}")
    print(f"Generated {PDF_MANIFEST}")
    print(f"General subjects: {sum(1 for s in stats if s['type'] == 'ogolne')}")
    print(f"Vocational programmes: {sum(1 for s in stats if s['type'] == 'zawodowe')}")
    print(f"PDF files: {len(pdf_items)}")


if __name__ == "__main__":
    main()
