from __future__ import annotations

import argparse
import json
from pathlib import Path

from audit_requirements_working_md import FORBIDDEN, GRADES, read_rows, repeats_source_requirement


ROOT = Path(__file__).resolve().parents[1]
CURATED = ROOT / "data" / "wymagania_kuratorskie.json"


def row_is_importable(row: dict) -> tuple[bool, list[str]]:
    problems = []
    grades = row["grades"]
    if row.get("status") != "opracowane roboczo":
        problems.append("status nie jest `opracowane roboczo`")
    for grade in GRADES:
        value = str(grades.get(grade, "")).strip()
        if not value or "Do opracowania" in value:
            problems.append(f"brak gotowej treści: {grade}")
        if "Dowód sprawdzenia:" not in value:
            problems.append(f"brak `Dowód sprawdzenia:`: {grade}")
        for phrase in FORBIDDEN:
            if phrase.lower() in value.lower():
                problems.append(f"fraza szablonowa `{phrase}`: {grade}")
        if repeats_source_requirement(row["source"], value):
            problems.append(f"powtórzenie pełnego wymagania źródłowego: {grade}")
    return not problems, problems


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importuje gotowe wymagania z Markdowna do data/wymagania_kuratorskie.json."
    )
    parser.add_argument("--apply", action="store_true", help="Zapisz zaakceptowane wpisy do JSON.")
    parser.add_argument("--include-existing", action="store_true", help="Nadpisz także istniejące wpisy.")
    args = parser.parse_args()

    data = json.loads(CURATED.read_text(encoding="utf-8"))
    requirements = data.setdefault("requirements", {})
    rows = read_rows()

    accepted = []
    rejected = []
    for row in rows:
        ok, problems = row_is_importable(row)
        if ok:
            if row["key"] in requirements and not args.include_existing:
                continue
            accepted.append(row)
        else:
            rejected.append((row, problems))

    print(f"Rows in Markdown: {len(rows)}")
    print(f"Importable rows: {len(accepted)}")
    print(f"Rejected rows: {len(rejected)}")
    if not args.apply:
        print("Dry run only. Add --apply to write data/wymagania_kuratorskie.json.")
        return

    for row in accepted:
        requirements[row["key"]] = {grade: row["grades"][grade].strip() for grade in GRADES}
    CURATED.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported rows: {len(accepted)}")
    print(f"Total curated rows: {len(requirements)}")


if __name__ == "__main__":
    main()
