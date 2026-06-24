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


def render_table(
    items: list[str],
    subject_name: str = "",
    vocational: bool = False,
    school: str = "",
    section_number: str = "",
) -> str:
    return og.render_requirement_matrix(
        items,
        subject_name=subject_name,
        vocational=vocational,
        school=school,
        section_number=section_number,
    )


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
            '<p class="cumulative"><strong>Model bezpieczny źródłowo:</strong> każdy wiersz pokazuje jedno wymaganie z podstawy programowej, a kolumny ocen opisują poziom opanowania tego samego wymagania. Nie przypisujemy kolejnych punktów podstawy do kolejnych ocen.</p>',
            '<div class="card-actions">',
            f'<button type="button" onclick="expandSections(\'{card_id}\', true)">Rozwiń działy</button>',
            f'<button type="button" onclick="expandSections(\'{card_id}\', false)">Zwiń działy</button>',
            "</div>",
        ]
    )
    for sidx, section in enumerate(sections):
        sec_id = f"{card_id}_{sidx}"
        sec_body_id = f"{sec_id}_body"
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
                render_table(
                    section["items"],
                    subject_name=spec.name,
                    school=spec.school,
                    section_number=section["number"],
                ),
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
            '<p class="cumulative"><strong>Model bezpieczny źródłowo:</strong> każdy wiersz pokazuje jedno kryterium lub efekt z podstawy programowej zawodu, a kolumny ocen opisują poziom samodzielności, poprawności, jakości i złożoności wykonania tego samego kryterium.</p>',
            '<div class="card-actions">',
            f'<button type="button" onclick="expandSections(\'{card_id}\', true)">Rozwiń jednostki</button>',
            f'<button type="button" onclick="expandSections(\'{card_id}\', false)">Zwiń jednostki</button>',
            "</div>",
        ]
    )
    for uidx, unit in enumerate(units):
        sec_id = f"{card_id}_{uidx}"
        sec_body_id = f"{sec_id}_body"
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
                render_table(
                    unit["items"],
                    subject_name=item["name"],
                    vocational=True,
                    school=item["school"],
                    section_number=unit["code"],
                ),
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
      <img src="assets/logo-zsz5-black.png" alt="Logotyp ZSZ5 we Wrocławiu">
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
    <p class="home-warning"><strong>Status roboczy:</strong> wymagania na oceny są opracowaniem szkolnym. Podstawy programowe w bibliotece są źródłami, a oceny opisują poziom opanowania tych samych wymagań; całość trzeba zatwierdzić w pracy zespołów przedmiotowych i zawodowych.</p>
  </section>

  <section class="home-section">
    <h3>Przydatne materiały i linki</h3>
    <p>Poniższe linki prowadzą do materiałów, które warto wykorzystać przy recenzji wymagań, tworzeniu rozkładów materiału i adaptowaniu programu do realnej pracy z klasą. Źródła zewnętrzne są pomocnicze: wiążące pozostają aktualne akty prawne oraz szkolne decyzje nauczycieli i zespołów przedmiotowych.</p>
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
        <h4>IBE PIB - podstawy programowe i kierunki zmian</h4>
        <p>Miejsce do monitorowania prac nad podstawami programowymi i szerszego kontekstu zmian w edukacji. Do bieżącej publikacji szkolnej trzeba je zestawiać z obowiązującymi aktami prawnymi.</p>
        <a class="resource-link" href="https://ibe.edu.pl/pl/podstawy-programowe" target="_blank" rel="noopener">Otwórz materiał</a>
      </div>
    </div>
    <p class="source-note">Ostatnie sprawdzenie linków źródłowych: 24 czerwca 2026 r.</p>
  </section>

  <section class="home-section">
    <h3>Od podstawy programowej do wymagań na oceny</h3>
    <p>Droga od podstawy programowej do oceny ucznia powinna być czytelna i możliwa do sprawdzenia. Sama podstawa nie jest jeszcze wymaganiami na ocenę: najpierw trzeba wybrać lub opracować program nauczania, rozpisać go na rozkład materiału, jasno określić wymagania edukacyjne, zaplanować sprawdzanie wiedzy i umiejętności, a dopiero potem wystawić ocenę ucznia.</p>
    <div class="process-lab" aria-label="Ścieżka od podstawy programowej do oceny ucznia">
      <div class="process-track" role="list">
        <button class="process-step active" type="button" role="listitem" aria-pressed="true" data-step="1" data-title="Podstawa programowa" data-teacher="Sprawdza obowiązkowe cele, treści, efekty kształcenia i kryteria wskazane w przepisach." data-output="Lista tego, czego nie można pominąć w danym przedmiocie lub kwalifikacji." data-check="Nie zastępuj podstawy propozycją z podręcznika ani tabelą z wydawnictwa." onclick="setProcessStep(this)">
          <span class="step-num">1</span><span><strong>Podstawa programowa</strong><small>Co jest obowiązkowe</small></span>
        </button>
        <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="2" data-title="Program nauczania" data-teacher="Wybiera program z wydawnictwa, modyfikuje go albo opracowuje własny, ale nadal pilnuje zgodności z podstawą." data-output="Program, który pokazuje sposób realizacji podstawy w danym oddziale." data-check="Program może być adaptowany, jeżeli tempo, kolejność albo dobór ćwiczeń nie pasują do klasy." onclick="setProcessStep(this)">
          <span class="step-num">2</span><span><strong>Program nauczania</strong><small>Jak realizujemy podstawę</small></span>
        </button>
        <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="3" data-title="Rozkład materiału" data-teacher="Przekłada program na działy, tematy, ćwiczenia, powtórzenia, projekty i orientacyjny czas pracy." data-output="Plan pracy na rok lub semestr, który da się realnie wykonać z konkretną klasą." data-check="Rozkład nie jest świętym harmonogramem. Ma pomagać kontrolować realizację, a nie blokować sensowną korektę tempa." onclick="setProcessStep(this)">
          <span class="step-num">3</span><span><strong>Rozkład materiału</strong><small>Kolejność i tempo pracy</small></span>
        </button>
        <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="4" data-title="Wymagania edukacyjne" data-teacher="Opisuje, co uczeń powinien wiedzieć i umieć na poszczególne oceny." data-output="Jasne wymagania na dopuszczającą, dostateczną, dobrą, bardzo dobrą i celującą." data-check="Wymagania mają wynikać z realizowanego programu i podstawy, a nie z ogólnych haseł typu zna, rozumie, potrafi." onclick="setProcessStep(this)">
          <span class="step-num">4</span><span><strong>Wymagania edukacyjne</strong><small>Poziomy na oceny</small></span>
        </button>
        <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="5" data-title="Sprawdzanie wiedzy i umiejętności" data-teacher="Dobiera sprawdziany, odpowiedzi, zadania praktyczne, projekty i obserwację pracy ucznia do wcześniej podanych wymagań." data-output="Dowody uczenia się: prace, wypowiedzi, działania praktyczne, wyniki zadań i projekty." data-check="Nie oceniaj tego, czego wcześniej nie było w wymaganiach albo czego nie dało się przećwiczyć w danym trybie pracy." onclick="setProcessStep(this)">
          <span class="step-num">5</span><span><strong>Sprawdzanie</strong><small>Dowody wiedzy i umiejętności</small></span>
        </button>
        <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="6" data-title="Ocena ucznia" data-teacher="Porównuje osiągnięcia ucznia z wymaganiami edukacyjnymi i zasadami oceniania." data-output="Ocena bieżąca, śródroczna lub roczna, którą da się uzasadnić konkretnymi wymaganiami." data-check="Ocena powinna wynikać z rozpoznanych osiągnięć ucznia, a nie z samego faktu przerobienia tematów." onclick="setProcessStep(this)">
          <span class="step-num">6</span><span><strong>Ocena ucznia</strong><small>Uzasadniony wynik</small></span>
        </button>
      </div>
      <div class="process-panel" aria-live="polite">
        <div class="process-panel-head">
          <span class="eyebrow">aktywny etap</span>
          <h4><span id="process_step_num">1</span>. <span id="process_title">Podstawa programowa</span></h4>
        </div>
        <div class="process-panel-grid">
          <div><strong>Nauczyciel robi</strong><p id="process_teacher">Sprawdza obowiązkowe cele, treści, efekty kształcenia i kryteria wskazane w przepisach.</p></div>
          <div><strong>Powstaje</strong><p id="process_output">Lista tego, czego nie można pominąć w danym przedmiocie lub kwalifikacji.</p></div>
          <div><strong>Trzeba pilnować</strong><p id="process_check">Nie zastępuj podstawy propozycją z podręcznika ani tabelą z wydawnictwa.</p></div>
        </div>
      </div>
    </div>
    <div class="law-callout">
      <h4>Co to oznacza w praktyce</h4>
      <p><strong>Sztywno trzymamy się podstawy programowej</strong>: obowiązkowych celów, treści, efektów kształcenia i kryteriów wskazanych w przepisach. <strong>Nie musimy natomiast mechanicznie realizować propozycji wydawnictwa</strong>, jeżeli w konkretnej klasie nie działa tempo, kolejność, dobór ćwiczeń albo sposób sprawdzania. Program nauczania, rozkład materiału, metody pracy i wymagania edukacyjne mają służyć realizacji podstawy w realnych warunkach szkoły.</p>
    </div>
    <div class="home-cards legal-grid">
      <div class="home-card">
        <h4>Program nie jest nadrzędny wobec podstawy</h4>
        <span class="legal-ref">Ustawa o systemie oświaty, art. 22a ust. 1, 3 i 5</span>
        <p>Nauczyciel albo zespół nauczycieli przedstawia dyrektorowi program nauczania. Przepis mówi też wprost, że programy nauczania powinny być dostosowane do potrzeb i możliwości uczniów, dla których są przeznaczone.</p>
        <a class="resource-link" href="https://dziennikustaw.gov.pl/D2025000088101.pdf" target="_blank" rel="noopener">Otwórz Dz.U. 2025 poz. 881</a>
      </div>
      <div class="home-card">
        <h4>Cała podstawa musi być objęta szkolnym zestawem</h4>
        <span class="legal-ref">Ustawa o systemie oświaty, art. 22a ust. 7</span>
        <p>Dyrektor odpowiada za to, aby szkolny zestaw programów nauczania uwzględniał całość podstawy programowej dla danego etapu, a w kształceniu zawodowym także właściwe podstawy programowe zawodów.</p>
        <a class="resource-link" href="https://dziennikustaw.gov.pl/D2025000088101.pdf" target="_blank" rel="noopener">Otwórz Dz.U. 2025 poz. 881</a>
      </div>
      <div class="home-card">
        <h4>Ocena odnosi się do podstawy i programu</h4>
        <span class="legal-ref">Ustawa o systemie oświaty, art. 44b ust. 3</span>
        <p>Ocenianie polega na rozpoznawaniu poziomu i postępów ucznia w stosunku do wymagań z podstawy programowej oraz wymagań edukacyjnych wynikających z realizowanych w szkole programów nauczania.</p>
        <a class="resource-link" href="https://dziennikustaw.gov.pl/D2025000088101.pdf" target="_blank" rel="noopener">Otwórz Dz.U. 2025 poz. 881</a>
      </div>
      <div class="home-card">
        <h4>Uczeń i rodzic mają znać wymagania i sposoby sprawdzania</h4>
        <span class="legal-ref">Ustawa o systemie oświaty, art. 44b ust. 8 pkt 1-2</span>
        <p>Na początku roku nauczyciel informuje o wymaganiach edukacyjnych potrzebnych do uzyskania poszczególnych ocen oraz o sposobach sprawdzania osiągnięć edukacyjnych uczniów.</p>
        <a class="resource-link" href="https://dziennikustaw.gov.pl/D2025000088101.pdf" target="_blank" rel="noopener">Otwórz Dz.U. 2025 poz. 881</a>
      </div>
    </div>
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
        <h4>Jak łączy się z adaptacją programu</h4>
        <p>Adaptacja programu nie polega wyłącznie na zmianie tabeli ocen. W praktyce wpływa na tempo, formy pracy, liczbę ćwiczeń, sposób sprawdzania wiedzy i dobór materiałów. To właśnie rozkład materiału pomaga przełożyć decyzje nauczyciela na codzienną pracę z klasą.</p>
      </div>
    </div>
  </section>

  <section class="home-section">
    <h3>Co znaczy adaptować program w praktyce</h3>
    <p>Nie zmienia się samej podstawy programowej jako aktu prawnego: jej wymagania pozostają punktem odniesienia. Adaptuje się sposób realizacji programu: kolejność tematów, tempo, przykłady, ćwiczenia, materiały, formy pracy i sposoby sprawdzania wiedzy. W praktyce oznacza to, że nauczyciel może odejść od gotowej propozycji wydawnictwa, jeśli widzi, że w danej klasie lepiej zadziała inna kolejność, więcej ćwiczeń, wolniejsze tempo albo inny sposób sprawdzenia umiejętności.</p>
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
        <h4>3. Od wymagań do pracy na lekcji</h4>
        <p>Wymagania na oceny powinny być zrozumiałe dla ucznia, a sposób dochodzenia do tych wymagań może być różny: przez więcej przykładów, inne ćwiczenia, pracę praktyczną, projekty, rozmowę albo zadania stopniowane trudnością.</p>
      </div>
      <div class="home-card">
        <h4>4. Co nie powinno się wydarzyć</h4>
        <p>Adaptacja nie może oznaczać przypadkowego usunięcia kluczowych efektów kształcenia ani tabeli ocen oderwanej od programu. Powinna być świadomą decyzją nauczyciela, zespołu lub szkoły, zgodną z podstawą i realnym planem pracy.</p>
      </div>
    </div>
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
<link rel="icon" href="assets/logo-zsz5-black.png">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#f3f0e9;--paper:#fffdf8;--ink:#172033;--muted:#647084;--line:#d9d5cc;--navy:#172a46;--blue:#2b67d1;--cyan:#28a8b8;--gold:#d99b2b;--green:#2e8b68;--red:#c94c4c;--shadow:0 12px 30px rgba(23,32,51,.08);--soft-shadow:0 8px 20px rgba(23,32,51,.06)}}
html{{scroll-behavior:smooth}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;background:var(--bg);color:var(--ink);min-height:100vh;font-size:15px;line-height:1.5}}
a{{color:inherit}}
.skip-link{{position:absolute;left:12px;top:-48px;background:var(--navy);color:#fff;padding:8px 12px;border-radius:999px;z-index:200;text-decoration:none}}
.skip-link:focus{{top:12px}}
header{{background:var(--paper);color:var(--ink);padding:14px 24px;border-bottom:1px solid rgba(23,32,51,.08)}}
.brand{{display:flex;align-items:center;gap:16px;max-width:1236px;margin:0 auto}}
.brand-logo{{width:82px;height:58px;object-fit:contain;background:transparent;border-radius:0;padding:0;flex-shrink:0}}
header h1{{font-size:1.22rem;line-height:1.18;letter-spacing:0}}
header p{{font-size:.86rem;color:var(--muted);margin-top:5px;line-height:1.45;max-width:860px}}
.summary{{background:#fff7df;border-bottom:1px solid #ecd6a4;color:#6d5828;padding:12px max(18px,calc((100vw - 1236px)/2));font-size:.88rem;line-height:1.45}}
.top-tabs{{position:sticky;top:0;z-index:40;background:rgba(243,240,233,.94);color:var(--ink);border-bottom:1px solid var(--line);box-shadow:0 8px 24px rgba(23,32,51,.06);backdrop-filter:blur(14px)}}
.tab-row{{display:flex;gap:6px;overflow-x:auto;max-width:1236px;margin:0 auto;padding:8px 18px 0;border-bottom:0;scrollbar-width:none}}
.tab-row::-webkit-scrollbar{{display:none}}
.tab-btn,.mode-btn{{padding:9px 13px;border:none;border-radius:999px;background:transparent;color:var(--muted);font-weight:800;white-space:nowrap;cursor:pointer}}
.tab-btn.active{{color:#fff;background:var(--tab-color,var(--navy));box-shadow:0 8px 18px rgba(23,32,51,.12)}}
.mode-btn.active{{color:#fff;background:var(--navy)}}
.tools{{display:grid;grid-template-columns:minmax(140px,190px) minmax(260px,1fr) auto;gap:10px;align-items:center;max-width:1236px;margin:0 auto;padding:10px 18px 12px;background:transparent;color:var(--ink);border-bottom:0}}
.tools label{{font-size:.78rem;font-weight:850;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}}
.tools input{{width:100%;padding:10px 14px;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--ink);box-shadow:0 8px 18px rgba(23,32,51,.04)}}
.tools button,.card-actions button,.category-filter button{{padding:7px 11px;border:1px solid var(--line);background:#fff;border-radius:999px;cursor:pointer;font-size:.82rem;color:var(--ink);font-weight:750}}
.tools button:hover,.card-actions button:hover,.category-filter button:hover{{border-color:var(--blue);box-shadow:0 8px 18px rgba(43,103,209,.10)}}
.filter-status{{font-size:.8rem;color:var(--muted)}}
.content-page{{display:none;padding-bottom:42px}}
.page-head{{max-width:1236px;margin:0 auto;padding:24px 22px 8px}}
.page-head h2{{font-size:1.28rem;margin-bottom:5px;color:var(--ink)}}
.page-head p{{font-size:.9rem;color:var(--muted);line-height:1.5;max-width:900px}}
.quick-index{{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}}
.quick-index a,.quick-index span{{display:inline-flex;align-items:center;min-height:30px;padding:5px 10px;border:1px solid var(--line);border-radius:999px;background:#fff;text-decoration:none;font-size:.78rem;color:#345070;font-weight:750}}
.quick-index a:hover{{border-color:var(--blue);background:#eef4fb}}
.cards-list{{max-width:1236px;margin:0 auto;padding:12px 22px;display:flex;flex-direction:column;gap:12px}}
.content-card{{background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;box-shadow:var(--soft-shadow);overflow:hidden}}
.card-toggle{{width:100%;display:flex;align-items:center;gap:10px;padding:15px 16px;border:none;border-left:5px solid;background:var(--paper);text-align:left;cursor:pointer}}
.card-toggle:hover{{background:#fff}}
.arrow{{font-size:.75rem;transition:transform .2s;flex-shrink:0}}
.small{{font-size:.65rem;color:var(--muted)}}
.card-name{{font-weight:800;flex:1}}
.card-meta{{font-size:.8rem;color:var(--muted);flex-shrink:0}}
.card-body{{display:none;border-top:1px solid rgba(23,32,51,.08);padding:12px;gap:8px;flex-direction:column;background:#fff}}
.source-box,.goals-box{{background:#f7fbff;border:1px solid #dce9f7;border-radius:8px;padding:10px 12px;font-size:.82rem;line-height:1.45;color:#374151;margin-bottom:8px}}
.source-box summary,.goals-box summary{{cursor:pointer;font-weight:700}}
.source-box code{{display:block;margin-top:6px;color:#4b5563;word-break:break-all}}
.note{{margin-top:6px;color:#92400e}}
.cumulative{{font-size:.82rem;color:#4b5563;margin:4px 0 8px;line-height:1.45}}
.draft-note{{font-size:.8rem;line-height:1.45;color:#6d5828;background:#fff7df;border:1px solid #ecd6a4;border-radius:6px;padding:8px 10px;margin:4px 0 8px}}
.source-requirement.curated-row{{background:#f0fdf4!important;border-left:4px solid #16a34a!important}}
.source-requirement.curated-row::before{{content:"Opracowane roboczo";display:inline-block;margin:0 0 6px;padding:2px 6px;border-radius:999px;background:#dcfce7;color:#166534;font-size:.68rem;font-weight:850;text-transform:uppercase}}
.source-requirement.unreviewed-row{{background:#fffbeb!important;border-left:4px solid #f59e0b!important}}
.source-requirement.unreviewed-row::before{{content:"Do opracowania";display:inline-block;margin:0 0 6px;padding:2px 6px;border-radius:999px;background:#fef3c7;color:#92400e;font-size:.68rem;font-weight:850;text-transform:uppercase}}
.status{{display:inline-block;margin-right:8px;padding:2px 7px;border-radius:999px;font-size:.72rem;font-weight:800;text-transform:uppercase}}
.status-ok{{background:#dcfce7;color:#166534}}
.status-review{{background:#fef3c7;color:#92400e}}
.status-ore{{background:#e0e7ff;color:#3730a3}}
.home-hero{{display:grid;grid-template-columns:minmax(0,1fr) 210px;gap:28px;align-items:center;max-width:1236px;margin:24px auto 0;padding:28px;background:var(--navy);color:#fff;border-radius:8px;box-shadow:var(--shadow);position:relative;overflow:hidden}}
.home-hero h2{{font-size:clamp(1.55rem,3vw,2.35rem);line-height:1.08;margin:6px 0 12px;max-width:860px}}
.home-hero p{{color:#c8d1df;font-size:.98rem;line-height:1.58;max-width:900px}}
.eyebrow{{font-size:.74rem;text-transform:uppercase;letter-spacing:.12em;color:#8fd4dd;font-weight:850}}
.home-logo-card{{display:flex;justify-content:center;align-items:center;background:#fffdf8;border:1px solid rgba(255,255,255,.5);border-radius:8px;padding:16px;min-height:150px}}
.home-logo-card img{{width:100%;max-width:172px;height:auto;display:block}}
.home-section{{max-width:1236px;margin:0 auto;padding:22px 22px 4px}}
.home-section h3{{font-size:1.04rem;font-weight:850;color:var(--ink);margin-bottom:12px;padding-bottom:0;border-bottom:0}}
.home-section>p{{font-size:.9rem;color:#374151;line-height:1.65;margin-bottom:14px;max-width:920px}}
.home-cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;margin-bottom:14px}}
.home-card{{background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;padding:16px;box-shadow:var(--soft-shadow)}}
.home-card h4{{font-size:.92rem;font-weight:850;color:var(--navy);margin-bottom:7px}}
.home-card p{{font-size:.85rem;color:#374151;line-height:1.55}}
.home-card ul{{padding-left:18px;margin-top:8px}}
.home-card li{{font-size:.82rem;color:#374151;line-height:1.45;margin-bottom:5px}}
.legal-ref{{display:inline-block;margin-bottom:7px;padding:4px 8px;border-radius:999px;background:#eef4fb;color:#345070;border:1px solid #dce9f7;font-size:.74rem;font-weight:850}}
.resource-grid .home-card{{display:flex;flex-direction:column;gap:8px}}
.resource-link{{display:inline-flex;align-items:center;justify-content:center;align-self:flex-start;min-height:32px;margin-top:auto;padding:6px 11px;border-radius:999px;border:1px solid #b9d4f7;background:#eef4fb;color:#1d4f9a;text-decoration:none;font-size:.8rem;font-weight:850}}
.resource-link:hover{{background:#dcecff;border-color:#8ebcf2}}
.source-note{{font-size:.76rem;color:var(--muted);margin-top:-2px}}
.process-lab{{display:grid;grid-template-columns:minmax(280px,0.95fr) minmax(320px,1.05fr);gap:14px;margin:14px 0}}
.process-track{{display:grid;grid-template-columns:1fr;gap:8px}}
.process-step{{display:grid;grid-template-columns:34px 1fr;gap:10px;align-items:center;width:100%;min-height:64px;text-align:left;background:var(--paper);border:1px solid rgba(23,32,51,.1);border-radius:8px;padding:10px 12px;color:var(--ink);box-shadow:0 6px 16px rgba(23,32,51,.04);cursor:pointer}}
.process-step:hover{{border-color:#b9d4f7;background:#fff}}
.process-step.active{{background:#eef4fb;border-color:var(--blue);box-shadow:0 10px 24px rgba(43,103,209,.13)}}
.process-step .step-num{{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:999px;background:var(--navy);color:#fff;font-size:.8rem;font-weight:850}}
.process-step.active .step-num{{background:var(--blue)}}
.process-step strong{{display:block;font-size:.88rem;line-height:1.2}}
.process-step small{{display:block;margin-top:3px;color:var(--muted);font-size:.74rem;line-height:1.25}}
.process-panel{{background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;padding:18px;box-shadow:var(--shadow);align-self:stretch}}
.process-panel-head{{margin-bottom:12px}}
.process-panel-head .eyebrow{{color:var(--blue)}}
.process-panel h4{{font-size:1.2rem;line-height:1.2;margin-top:5px;color:var(--ink)}}
.process-panel-grid{{display:grid;grid-template-columns:1fr;gap:10px}}
.process-panel-grid div{{background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px}}
.process-panel-grid strong{{display:block;color:var(--navy);font-size:.82rem;margin-bottom:5px;text-transform:uppercase;letter-spacing:.05em}}
.process-panel-grid p{{font-size:.88rem;color:#374151;line-height:1.55}}
.law-callout{{background:#e8f6f4;border:1px solid #b8ddd7;border-radius:8px;padding:15px;margin:12px 0 14px;color:#245e58}}
.law-callout h4{{font-size:.92rem;color:#245e58;margin-bottom:6px}}
.law-callout p{{font-size:.86rem;color:#245e58;line-height:1.55}}
.legal-grid{{margin-top:10px}}
.home-warning{{background:#fff7df;border:1px solid #ecd6a4;border-radius:8px;padding:12px 14px;color:#6d5828}}
.home-stats{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-bottom:14px}}
.stat-box{{background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;padding:14px;text-align:center;box-shadow:var(--soft-shadow)}}
.stat-num{{font-size:1.55rem;font-weight:850;color:var(--blue);line-height:1}}
.stat-label{{font-size:.72rem;color:var(--muted);margin-top:5px;line-height:1.25}}
.home-nav-hint{{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}}
.home-nav-hint a{{display:inline-flex;align-items:center;min-height:32px;color:#fff;text-decoration:none;padding:6px 11px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.24);font-size:.8rem;font-weight:800}}
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
table{{width:100%;border-collapse:collapse;table-layout:fixed;min-width:1120px}}
th:first-child,td:first-child{{width:28%}}
th{{padding:8px 6px;border:1px solid #d1d5db;background:#f3f4f6;font-size:.78rem;color:#374151;text-align:left}}
td{{vertical-align:top;padding:8px 10px;border:1px solid #e5e7eb;font-size:.78rem;line-height:1.38}}
th:nth-child(1),td:nth-child(1){{background:#fff;border-color:#d1d5db;font-weight:650}}
th:nth-child(2),td:nth-child(2){{background:#fff7ed;border-color:#fed7aa}}
th:nth-child(3),td:nth-child(3){{background:#f0fdf4;border-color:#bbf7d0}}
th:nth-child(4),td:nth-child(4){{background:#eff6ff;border-color:#bfdbfe}}
th:nth-child(5),td:nth-child(5){{background:#faf5ff;border-color:#e9d5ff}}
th:nth-child(6),td:nth-child(6){{background:#fefce8;border-color:#fde68a}}
.category-filter{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}}
.category-filter button.active{{background:var(--navy);color:#fff;border-color:var(--navy)}}
.pdf-grid{{max-width:1236px;margin:0 auto;padding:12px 22px;display:grid;gap:12px}}
.pdf-card{{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;background:var(--paper);border-radius:8px;border:1px solid rgba(23,32,51,.08);padding:14px;box-shadow:var(--soft-shadow)}}
.pdf-card p{{font-size:.82rem;color:#6b7280;margin-top:4px}}
.pdf-card code{{display:block;margin-top:5px;color:#4b5563;font-size:.76rem;word-break:break-all}}
.pdf-actions{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end;min-width:240px}}
.pdf-actions span{{font-size:.78rem;color:#6b7280}}
.pdf-actions a{{padding:6px 10px;border:1px solid var(--line);background:#fff;border-radius:999px;text-decoration:none;font-size:.8rem;color:var(--ink);font-weight:750}}
.empty-page{{padding:20px;background:#fff;border-radius:8px;color:#6b7280}}
[hidden]{{display:none!important}}
button:focus-visible,a:focus-visible,input:focus-visible{{outline:3px solid var(--gold);outline-offset:2px}}
.back-top{{position:fixed;right:16px;bottom:16px;z-index:50;width:42px;height:42px;border-radius:999px;border:1px solid #cbd5e1;background:#fff;color:#1f2937;box-shadow:0 2px 8px rgba(0,0,0,.16);cursor:pointer;font-size:1.1rem}}
@media (max-width:900px){{body{{font-size:14px}}.brand{{align-items:flex-start}}.brand-logo{{width:74px;height:52px}}.tools{{grid-template-columns:1fr;padding:10px 12px 12px}}.tab-row{{padding-left:10px;padding-right:10px}}.card-toggle,.unit-toggle{{align-items:flex-start}}.card-meta,.unit-count{{display:none}}.pdf-card{{flex-direction:column}}.pdf-actions{{justify-content:flex-start;min-width:0}}table{{min-width:760px}}header,.summary,.page-head{{padding-left:14px;padding-right:14px}}.cards-list,.pdf-grid{{padding-left:12px;padding-right:12px}}.home-hero{{grid-template-columns:1fr;margin:14px 12px 0;padding:20px 16px}}.home-logo-card{{justify-content:flex-start;min-height:0;max-width:210px}}.home-section{{padding:18px 12px 4px}}.process-lab{{grid-template-columns:1fr}}.home-stats{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (max-width:640px){{header{{padding-top:10px;padding-bottom:10px}}header h1{{font-size:1.04rem}}header p{{display:none}}.brand-logo{{width:58px;height:42px}}.summary{{display:none}}.tab-btn,.mode-btn{{padding:7px 10px;font-size:.82rem}}.tools{{padding:8px 12px}}.tools label{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}.tools input{{padding:9px 12px}}.filter-status:empty{{display:none}}.home-hero{{display:block}}.home-hero h2{{font-size:1.45rem}}.home-hero p{{font-size:.88rem}}.home-hero-text>p:not(.eyebrow){{display:none}}.home-logo-card{{display:none}}.home-nav-hint{{gap:6px;margin-top:12px}}.home-nav-hint a{{min-height:28px;padding:5px 8px;font-size:.76rem}}.home-stats{{gap:8px}}.home-card,.process-step,.process-panel,.process-panel-grid div,.pdf-card{{padding:12px}}.process-step{{grid-template-columns:30px 1fr;min-height:58px}}.process-panel h4{{font-size:1.05rem}}.table-wrap{{overflow-x:visible}}table{{min-width:0;table-layout:auto}}th:first-child,td:first-child{{width:100%}}thead{{display:none}}tr,td{{display:block;width:100%}}td{{border-width:1px 1px 0}}td:last-child{{border-bottom-width:1px}}td::before{{content:attr(data-label);display:block;font-weight:800;color:#374151;margin-bottom:5px}}}}
@media print{{.skip-link,.top-tabs,.tools,.quick-index,.card-actions,.back-top{{display:none}}.content-page{{display:block!important}}.card-body,.unit-body{{display:block!important}}body{{background:#fff}}.content-card,.unit,.pdf-card{{break-inside:avoid}}.table-wrap{{overflow:visible}}table{{min-width:700px}}}}
</style>
</head>
<body>
<a class="skip-link" href="#main_content">Przejdź do treści</a>
<header>
  <div class="brand">
    <img class="brand-logo" src="assets/logo-zsz5-black.png" alt="Logotyp ZSZ5 we Wrocławiu">
    <div>
      <h1>Wymagania edukacyjne ZSZ5 2026/2027</h1>
      <p>Jedna strona do przeglądania wymagań ogólnokształcących, zawodowych oraz lokalnej biblioteki PDF podstaw programowych.</p>
    </div>
  </div>
</header>
<div class="summary">
  <strong>Status:</strong> {len([s for s in stats if s['type'] == 'ogolne'])} przedmiotów ogólnokształcących, {len([s for s in stats if s['type'] == 'zawodowe'])} kierunków zawodowych, {total_tables} działów/jednostek, {total_items} wymagań/kryteriów, {total_pdf} plików PDF. Każdy punkt podstawy jest pokazywany jako źródło wymagania, a oceny opisują poziom jego opanowania; przed udostępnieniem uczniom i rodzicom materiał powinien zostać sprawdzony przez nauczyciela przedmiotu lub zawodu i dostosowany do programu nauczania w danym oddziale.
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
function setProcessStep(button){{
  if(!button) return;
  document.querySelectorAll('.process-step').forEach(step=>{{
    const active=step===button;
    step.classList.toggle('active', active);
    step.setAttribute('aria-pressed', active ? 'true' : 'false');
  }});
  const fields={{
    process_step_num: button.dataset.step,
    process_title: button.dataset.title,
    process_teacher: button.dataset.teacher,
    process_output: button.dataset.output,
    process_check: button.dataset.check
  }};
  Object.entries(fields).forEach(([id,value])=>{{
    const el=document.getElementById(id);
    if(el) el.textContent=value || '';
  }});
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
