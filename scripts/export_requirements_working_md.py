from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import generuj_kompletne_wymagania_ogolne as og
import generuj_wymagania_edukacyjne_ZSZ5 as site

OUT = ROOT / "wymagania_edukacyjne_do_opracowania.md"


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def grade_value(
    school: str,
    subject: str,
    section: str,
    requirement: str,
    vocational: bool = False,
) -> dict[str, str]:
    curated = og.curated_grade_requirements(school, subject, section, requirement)
    if curated:
        return curated
    prefix = "Do opracowania"
    if vocational:
        prefix = "Do opracowania przez nauczyciela zawodu"
    return {grade: prefix for grade in og.GRADE_ORDER}


def append_table_header(parts: list[str]) -> None:
    parts.append("| Klucz | Wymaganie źródłowe | Status | Dopuszczająca | Dostateczna | Dobra | Bardzo dobra | Celująca |")
    parts.append("|---|---|---|---|---|---|---|---|")


def append_requirement_row(
    parts: list[str],
    school: str,
    subject: str,
    section: str,
    requirement: str,
    vocational: bool = False,
) -> None:
    key = og.curated_key(school, subject, section, requirement)
    grades = grade_value(school, subject, section, requirement, vocational=vocational)
    status = "opracowane roboczo" if "Do opracowania" not in grades["Dopuszczająca"] else "do opracowania"
    parts.append(
        "| "
        + " | ".join(
            [
                f"`{md_escape(key)}`",
                md_escape(requirement),
                status,
                md_escape(grades["Dopuszczająca"]),
                md_escape(grades["Dostateczna"]),
                md_escape(grades["Dobra"]),
                md_escape(grades["Bardzo dobra"]),
                md_escape(grades["Celująca"]),
            ]
        )
        + " |"
    )


def export_general(parts: list[str]) -> tuple[int, int, int]:
    subjects = sections = requirements = 0
    for spec in og.specs():
        subjects += 1
        spec_sections = og.extract_sections(spec)
        parts.extend(
            [
                "",
                f"## {site.SCHOOL_LABELS[spec.school]} / Ogólnokształcące / {spec.name}",
                "",
                f"- `school`: `{spec.school}`",
                f"- `subject`: `{spec.name}`",
                f"- `source`: `{spec.source_label}`",
                f"- `path`: `{spec.path}`",
                f"- `status`: `{spec.status}`",
            ]
        )
        if spec.note:
            parts.append(f"- `note`: {spec.note}")
        for section in spec_sections:
            sections += 1
            requirements += len(section["items"])
            parts.extend(["", f"### Dział {section['number']}. {section['title']}", ""])
            append_table_header(parts)
            for requirement in section["items"]:
                append_requirement_row(
                    parts,
                    spec.school,
                    spec.name,
                    section["number"],
                    requirement,
                )
    return subjects, sections, requirements


def export_vocational(parts: list[str]) -> tuple[int, int, int]:
    programmes = units = requirements = 0
    for spec in site.VOCATIONAL_SPECS:
        programmes += 1
        item = site.extract_vocational_units(spec)
        item_units = item["units"]
        parts.extend(
            [
                "",
                f"## {site.SCHOOL_LABELS[item['school']]} / Zawodowe / {item['name']}",
                "",
                f"- `school`: `{item['school']}`",
                f"- `subject`: `{item['name']}`",
                f"- `source`: `{item['source_label']}`",
                f"- `path`: `{item['path']}`",
                f"- `status`: `{item['status']}`",
                f"- `qualifications`: {', '.join(item['qualifications']) if item['qualifications'] else 'brak'}",
            ]
        )
        if item["goals"]:
            parts.extend(["", "**Cele kształcenia:**"])
            for goal in item["goals"]:
                parts.append(f"- {goal}")
        for unit in item_units:
            units += 1
            requirements += len(unit["items"])
            parts.extend(["", f"### Jednostka {unit['code']}. {unit['title']}", ""])
            append_table_header(parts)
            for requirement in unit["items"]:
                append_requirement_row(
                    parts,
                    item["school"],
                    item["name"],
                    unit["code"],
                    requirement,
                    vocational=True,
                )
    return programmes, units, requirements


def main() -> None:
    parts = [
        "# Wymagania edukacyjne do opracowania",
        "",
        "Ten plik jest roboczą bazą wszystkich przedmiotów, działów i wymagań źródłowych wyciągniętych z lokalnych podstaw programowych ZSZ5.",
        "",
        "Jak używać:",
        "- każda tabela ma klucz zgodny z `data/wymagania_kuratorskie.json`,",
        "- wiersze oznaczone `opracowane roboczo` mają już konkretne wymagania w bazie kuratorskiej,",
        "- wiersze `do opracowania` trzeba uzupełnić konkretnymi wymaganiami na oceny,",
        "- nie dopisuj autorów, lektur, epok ani przykładów, jeśli nie wynikają z programu nauczania albo rozkładu materiału,",
        "- każda ocena powinna opisywać obserwowalne działanie ucznia i najlepiej zawierać dowód sprawdzenia.",
    ]
    general_subjects, general_sections, general_requirements = export_general(parts)
    vocational_programmes, vocational_units, vocational_requirements = export_vocational(parts)

    summary = [
        "# Wymagania edukacyjne do opracowania",
        "",
        "Ten plik jest roboczą bazą wszystkich przedmiotów, działów i wymagań źródłowych wyciągniętych z lokalnych podstaw programowych ZSZ5.",
        "",
        "## Podsumowanie",
        "",
        f"- przedmioty ogólnokształcące: {general_subjects}",
        f"- działy ogólnokształcące: {general_sections}",
        f"- wymagania ogólnokształcące: {general_requirements}",
        f"- programy zawodowe: {vocational_programmes}",
        f"- jednostki zawodowe: {vocational_units}",
        f"- kryteria zawodowe: {vocational_requirements}",
        f"- razem wierszy do opracowania lub recenzji: {general_requirements + vocational_requirements}",
        "",
    ]
    final_parts = summary + parts[2:]
    OUT.write_text("\n".join(final_parts) + "\n", encoding="utf-8")
    print(f"Generated {OUT}")
    print(f"Rows: {general_requirements + vocational_requirements}")


if __name__ == "__main__":
    main()
