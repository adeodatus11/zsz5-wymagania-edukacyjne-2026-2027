from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKING_MD = ROOT / "wymagania_edukacyjne_do_opracowania.md"
CURATED = ROOT / "data" / "wymagania_kuratorskie.json"
REPORT = ROOT / "przebudowa_wymagan_ogolnych" / "audyt_opracowan_claude_2026-06-25.md"
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
    "dotyczącą wymagania",
    "dotyczące wymagania",
    "realizuje wymaganie",
    "wykorzystuje wymaganie",
    "wyjaśnia wymaganie:",
    "interpretuje wymaganie:",
    "wymaganiem: «",
    "kryterium: «",
    "wymagania: «",
    "podstawowy element",
    "typowe zadanie komunikacyjne dotyczące",
    "podstawowe słowa lub struktury związane",
]


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", " ", value)).strip().lower()


def repeats_source_requirement(source: str, value: str) -> bool:
    normalized_value = normalize_text(value)
    source = re.sub(r"^\d+\)\s*", "", source)
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


def split_md_row(line: str) -> list[str]:
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in line:
        if char == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
            escaped = False
            continue
        current.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    cells.append("".join(current).strip())
    return cells


def read_rows() -> list[dict]:
    rows = []
    for line in WORKING_MD.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        cells = split_md_row(line)
        if len(cells) != 8:
            continue
        rows.append(
            {
                "key": cells[0].strip("`").replace("\\|", "|"),
                "source": cells[1],
                "status": cells[2],
                "grades": dict(zip(GRADES, cells[3:], strict=True)),
            }
        )
    return rows


def main() -> None:
    rows = read_rows()
    current = json.loads(CURATED.read_text(encoding="utf-8")).get("requirements", {})
    forbidden_counter: Counter[str] = Counter()
    accepted = []
    rejected = []

    for row in rows:
        grades = list(row["grades"].values())
        has_all = all(value and "Do opracowania" not in value for value in grades)
        has_evidence = all("Dowód sprawdzenia:" in value for value in grades)
        found_forbidden = sorted(
            {phrase for phrase in FORBIDDEN for value in grades if phrase.lower() in value.lower()}
        )
        if any(repeats_source_requirement(row["source"], value) for value in grades):
            found_forbidden.append("powtórzenie pełnego wymagania źródłowego")
        for phrase in found_forbidden:
            forbidden_counter[phrase] += sum(
                phrase.lower() in value.lower() for value in grades
            ) or 1
        if has_all and has_evidence and not found_forbidden:
            accepted.append(row)
        else:
            rejected.append((row, has_all, has_evidence, found_forbidden))

    new_accepted = [row for row in accepted if row["key"] not in current]
    accepted_existing = [row for row in accepted if row["key"] in current]

    lines = [
        "# Audyt opracowań Claude - wymagania edukacyjne",
        "",
        "Data audytu: 25 czerwca 2026 r.",
        "",
        "## Wynik",
        "",
        f"- Wiersze w pliku roboczym: {len(rows)}",
        f"- Wiersze kompletne technicznie: {sum(all(value and 'Do opracowania' not in value for value in row['grades'].values()) for row in rows)}",
        f"- Wiersze przechodzące filtr jakości: {len(accepted)}",
        f"- Wiersze już obecne w bazie kuratorskiej: {len(accepted_existing)}",
        f"- Nowe wiersze do bezpiecznego wstrzyknięcia: {len(new_accepted)}",
        "",
        "## Decyzja",
        "",
        "Nie wstrzykiwać hurtowo odrzuconych opracowań Claude zapisanych lokalnie w folderze `przebudowa_wymagan_ogolnych`.",
        "Aktualny plik `wymagania_edukacyjne_do_opracowania.md` ma być bezpieczną bazą roboczo-produkcyjną: status `opracowane roboczo` oznacza kandydat gotowy do importu, a `do opracowania` oznacza brak treści gotowej na stronę.",
        "Do strony można przenosić tylko wpisy, które przejdą importer, nie powtarzają pełnego wymagania w każdej ocenie i opisują konkretne, obserwowalne działania ucznia.",
        "",
        "## Najczęstsze frazy blokujące",
        "",
    ]
    for phrase, count in forbidden_counter.most_common():
        lines.append(f"- `{phrase}`: {count}")
    lines.extend(["", "## Nowe zaakceptowane wpisy", ""])
    if new_accepted:
        for row in new_accepted:
            lines.append(f"- `{row['key']}`")
    else:
        lines.append("Brak nowych wpisów spełniających próg jakości.")
    lines.extend(["", "## Przykłady odrzuconych wpisów", ""])
    for row, _has_all, _has_evidence, found_forbidden in rejected[:20]:
        lines.append(f"- `{row['key']}` - blokujące frazy: {', '.join(found_forbidden) if found_forbidden else 'brak kompletu lub dowodu'}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Rows: {len(rows)}")
    print(f"Accepted: {len(accepted)}")
    print(f"New accepted: {len(new_accepted)}")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
