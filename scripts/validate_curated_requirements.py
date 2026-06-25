from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURATED = ROOT / "data" / "wymagania_kuratorskie.json"
GRADES = ["Dopuszczająca", "Dostateczna", "Dobra", "Bardzo dobra", "Celująca"]
FORBIDDEN = [
    "związany z wymaganiem",
    "związane z wymaganiem",
    "opisuje wymaganie:",
    "realizuje wymaganie:",
    "wykorzystuje wymaganie",
    "wyjaśnia wymaganie:",
    "interpretuje wymaganie:",
    "wymaganiem: «",
    "kryterium: «",
    "wymagania: «",
    "podstawowy element",
    "typowe zadanie komunikacyjne dotyczące",
    "podstawowe słowa lub struktury związane",
    "Uczeń samodzielnie realizuje",
    "Uczeń wykonuje typową czynność lub wyjaśnia typową procedurę",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not CURATED.exists():
        fail(f"Missing curated requirements file: {CURATED}")
    data = json.loads(CURATED.read_text(encoding="utf-8"))
    requirements = data.get("requirements")
    if not isinstance(requirements, dict) or not requirements:
        fail("Curated requirements list is empty")
    if len(requirements) < 26:
        fail(f"Expected at least 26 curated requirement rows, got {len(requirements)}")

    for key, grades in requirements.items():
        parts = key.split("||")
        if len(parts) != 4 or not all(part.strip() for part in parts):
            fail(f"Invalid curated key: {key}")
        if not isinstance(grades, dict):
            fail(f"Curated row is not an object: {key}")
        for grade in GRADES:
            value = str(grades.get(grade, "")).strip()
            if not value:
                fail(f"Missing {grade} in {key}")
            if "Dowód sprawdzenia:" not in value:
                fail(f"Missing evidence phrase in {key} / {grade}")
            for phrase in FORBIDDEN:
                if phrase in value:
                    fail(f"Forbidden generic phrase in {key} / {grade}: {phrase}")

    print(f"Curated requirements OK: {len(requirements)} rows")


if __name__ == "__main__":
    main()
