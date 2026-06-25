from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURATED = ROOT / "data" / "wymagania_kuratorskie.json"
GRADES = ["Dopuszczająca", "Dostateczna", "Dobra", "Bardzo dobra", "Celująca"]
FORBIDDEN = [
    "…",
    "korzystając z instrukcji, schematu lub pokazu",
    "dla jednego wskazanego przypadku, pod nadzorem",
    "samodzielnie zgodnie z obowiązującymi przepisami i normami",
    "właściwie dobierając narzędzia, materiały i metodę pracy",
    "w złożonej sytuacji zawodowej",
    "uzasadniając dobór techniki i oceniając jakość efektu",
    "planując pracę, weryfikując jakość i wskazując możliwości doskonalenia",
    "karta pracy z odnotowaną obserwacją lub uproszczonym protokołem",
    "protokół wykonania zadania z podpisem oceniającego",
    "zadanie praktyczne z kartą oceny i komentarzem",
    "projekt technologiczny lub sprawozdanie z oceną jakości",
    "samodzielny projekt z planem pracy i oceną końcową",
    "korzystając z osi czasu lub mapy z oznaczeniami",
    "podając datę, miejsce lub nazwę",
    "podając przyczynę i skutek w kilku zdaniach",
    "porównuje z innym wydarzeniem lub zjawiskiem",
    "z wielu perspektyw, oceniając znaczenie",
    "formułując tezę interpretacyjną",
    "notatka z osią czasu lub mapą",
    "krótka odpowiedź z przyczyną i skutkiem",
    "akapit porównawczy z argumentami",
    "esej historyczny z oceną",
    "praca pisemna z tezą i źródłami",
    "karta pracy z uzupełnionymi lukami",
    "kartkówka z krótką odpowiedzią",
    "sprawdzian z zadaniami opisowymi",
    "praca pisemna z wnioskami",
    "projekt samodzielny z prezentacją",
    "jeden przykład ilustrujący:",
    "obszaru tematycznego:",
    "słownictwo z obszaru:",
    "krótkich, standardowych wypowiedziach komunikacyjnych",
    "w dłuższej wypowiedzi pisemnej lub ustnej z nielicznymi błędami",
    "swobodnie stosuje bogate słownictwo",
    "twórczo operuje słownictwem",
    "wyjaśnia podstawowy aspekt zagadnienia:",
    "analizuje zagadnienie:",
    "interpretuje zagadnienie:",
    "samodzielnie omawia zagadnienie:",
    "zagadnienie:",
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


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", " ", value)).strip().lower()


def repeats_source_requirement(source: str, value: str) -> bool:
    normalized_value = normalize_text(value)
    source = re.split(
        r"SZKOŁA PONADPODSTAWOWA|PODSTAWA PROGRAMOWA|spełnia wymagania określone",
        source,
        flags=re.IGNORECASE,
    )[0]
    candidates = [source]
    candidates.extend(part for part in re.split(r";|\boraz\b", source, flags=re.IGNORECASE) if part.strip())
    for candidate in candidates:
        normalized_source = normalize_text(candidate)
        if len(normalized_source) >= 18 and normalized_source in normalized_value:
            return True
    return False


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
        source_requirement = parts[3].strip()
        for grade in GRADES:
            value = str(grades.get(grade, "")).strip()
            if not value:
                fail(f"Missing {grade} in {key}")
            if "Dowód sprawdzenia:" not in value:
                fail(f"Missing evidence phrase in {key} / {grade}")
            for phrase in FORBIDDEN:
                if phrase.lower() in value.lower():
                    fail(f"Forbidden generic phrase in {key} / {grade}: {phrase}")
            if repeats_source_requirement(source_requirement, value):
                fail(f"Curated row repeats source requirement in {key} / {grade}")

    print(f"Curated requirements OK: {len(requirements)} rows")


if __name__ == "__main__":
    main()
