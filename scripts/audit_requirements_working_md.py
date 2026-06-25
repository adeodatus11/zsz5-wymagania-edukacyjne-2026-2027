from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKING_MD = ROOT / "wymagania_edukacyjne_do_opracowania.md"
CURATED = ROOT / "data" / "wymagania_kuratorskie.json"
REPORT = ROOT / "przebudowa_wymagan_ogolnych" / "audyt_opracowan_claude_2026-06-25.md"
GRADES = ["Dopuszczająca", "Dostateczna", "Dobra", "Bardzo dobra", "Celująca"]
FORBIDDEN = [
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
        found_forbidden = sorted({phrase for phrase in FORBIDDEN for value in grades if phrase in value})
        for phrase in found_forbidden:
            forbidden_counter[phrase] += sum(phrase in value for value in grades)
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
        "Nie wstrzykiwać hurtowo opracowań z aktualnego pliku `wymagania_edukacyjne_do_opracowania.md`.",
        "Claude oznaczył wszystkie wiersze jako `opracowane roboczo`, ale większość treści nadal jest automatyczną parafrazą wymagania źródłowego.",
        "Do strony można przenosić tylko wpisy, które nie powtarzają pełnego wymagania w każdej ocenie i opisują konkretne, obserwowalne działania ucznia.",
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
