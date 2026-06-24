from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import generuj_kompletne_wymagania_ogolne as og  # noqa: E402
import generuj_wymagania_edukacyjne_ZSZ5 as site  # noqa: E402


MANUAL_GENERAL_KEYS = {
    ("bsi", "Edukacja dla bezpieczeństwa"),
    ("technikum", "Edukacja dla bezpieczeństwa"),
    ("bsi", "Wychowanie fizyczne"),
}

GENERATED_PHRASES = (
    "samodzielnie wykonuje zadanie problemowe",
    "łączy wiadomości z działu",
    "stosuje wiadomości z działu",
    "opisuje podstawowe pojęcia i przykłady z działu",
    "rozpoznaje podstawowe pojęcia i przykłady z działu",
    "omawia podstawowe zagadnienia jednostki",
    "Uczeń omawia najważniejsze zagadnienia działu",
)


def norm(value: str) -> str:
    value = value.lower()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[^a-ząćęłńóśźż0-9 ]+", "", value)
    return value.strip()


def is_generated(item: str) -> bool:
    item_norm = item.lower()
    return any(phrase.lower() in item_norm for phrase in GENERATED_PHRASES)


def audit_general() -> list[dict]:
    rows: list[dict] = []
    for spec in og.specs():
        source_path = ROOT / spec.path
        sections = og.extract_sections(spec)
        manual = (spec.school, spec.name) in MANUAL_GENERAL_KEYS
        generated_fallbacks = 0
        grade_generated = 0
        item_count = 0
        source_text = ""
        if source_path.exists() and not manual:
            source_text = norm(og.subject_segment(spec))
        unmatched = 0
        for section in sections:
            for item in section["items"]:
                item_count += 1
                if is_generated(item):
                    generated_fallbacks += 1
                if source_text and norm(item)[:80] and norm(item)[:80] not in source_text:
                    unmatched += 1
            chunks = og.split_requirements(section["items"], section["title"])
            for grade_items in chunks.values():
                for item in grade_items:
                    if is_generated(item) and item not in section["items"]:
                        grade_generated += 1
        if not source_path.exists():
            status = "blokujące"
            risk = "brak lokalnego PDF"
        elif manual:
            status = "do recenzji"
            risk = "ręczna rekonstrukcja działów/pozycji z podstawy, nie ekstrakt literalny"
        elif generated_fallbacks:
            status = "blokujące"
            risk = "fallback zamiast treści źródłowej"
        elif unmatched:
            status = "do sprawdzenia"
            risk = f"{unmatched} pozycji nie dopasowano literalnie po czyszczeniu ekstraktu"
        else:
            status = "źródłowo śledzalne"
            risk = "działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem"
        rows.append(
            {
                "school": spec.school,
                "type": "ogólne",
                "name": spec.name,
                "sections": len(sections),
                "items": item_count,
                "source": spec.path,
                "status": status,
                "risk": risk,
                "grade_generated": grade_generated,
                "manual": manual,
            }
        )
    return rows


def audit_vocational() -> list[dict]:
    rows: list[dict] = []
    for spec in site.VOCATIONAL_SPECS:
        source_path = ROOT / spec.path
        data = site.extract_vocational_units(spec)
        fallback_items = 0
        item_count = 0
        source_text = ""
        if source_path.exists():
            source_text = norm(site.read_pdf(spec.path))
        unmatched = 0
        for unit in data["units"]:
            for item in unit["items"]:
                item_count += 1
                if is_generated(item):
                    fallback_items += 1
                if source_text and norm(item)[:80] and norm(item)[:80] not in source_text:
                    unmatched += 1
        if not source_path.exists():
            status = "blokujące"
            risk = "brak lokalnego PDF"
        elif fallback_items:
            status = "blokujące"
            risk = "fallback zamiast kryterium weryfikacji z PDF"
        elif not data["units"]:
            status = "blokujące"
            risk = "nie wyodrębniono jednostek efektów kształcenia"
        elif unmatched:
            status = "do sprawdzenia"
            risk = f"{unmatched} kryteriów nie dopasowano literalnie po czyszczeniu ekstraktu"
        else:
            status = "źródłowo śledzalne"
            risk = "jednostki i kryteria pochodzą z lokalnego PDF; progi ocen są opracowaniem"
        rows.append(
            {
                "school": spec.school,
                "type": "zawodowe",
                "name": spec.name,
                "sections": len(data["units"]),
                "items": item_count,
                "source": spec.path,
                "status": status,
                "risk": risk,
                "grade_generated": 0,
                "manual": False,
            }
        )
    return rows


def main() -> None:
    rows = audit_general() + audit_vocational()
    status_order = {"blokujące": 0, "do recenzji": 1, "do sprawdzenia": 2, "źródłowo śledzalne": 3}
    rows.sort(key=lambda row: (status_order.get(row["status"], 9), row["school"], row["type"], row["name"]))

    total = len(rows)
    print(f"Audited records: {total}")
    for status in ["blokujące", "do recenzji", "do sprawdzenia", "źródłowo śledzalne"]:
        print(f"{status}: {sum(1 for row in rows if row['status'] == status)}")
    print(f"Generated grade fillers: {sum(row['grade_generated'] for row in rows)}")
    print()
    print("| Typ szkoły | Typ | Pozycja | Działy/jednostki | Pozycje źródłowe | Status | Ryzyko |")
    print("|---|---|---|---:|---:|---|---|")
    for row in rows:
        school = site.SCHOOL_LABELS.get(row["school"], row["school"])
        print(
            f"| {school} | {row['type']} | {row['name']} | {row['sections']} | {row['items']} | "
            f"{row['status']} | {row['risk']} |"
        )


if __name__ == "__main__":
    main()
