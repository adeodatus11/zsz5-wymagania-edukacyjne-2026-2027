# Baza wiedzy subagentów - wymagania ogólnokształcące ZSZ5

Data utrwalenia: 2026-06-10.

Cel: zachować efekty pracy subagentów tak, aby w przyszłości można było ponownie uruchomić podobny proces bez odtwarzania kontekstu od zera.

## Pliki bazowe

- `01_audyt_tresci_subagent_mill.md` - audyt kompletności i błędów treści wymagań.
- `02_naprawy_i_research_subagent_nietzsche.md` - naprawy braków, błędnych ekstrakcji i walidacja po researchu.
- `03_audyt_ui_subagent_aristotle.md` - audyt czytelności, dostępności i działania strony przy dużej liczbie treści.

## Finalne pliki projektu

- `../../wymagania_ogolne_ZSZ5_2026_2027.html` - finalna strona wymagań ogólnokształcących.
- `../../generuj_kompletne_wymagania_ogolne.py` - generator finalnej strony.
- `../raport_generowania_kompletnej_strony.md` - raport liczbowy po generowaniu.
- `../raport_napraw_tresci_wymagan.md` - raport napraw treści.
- `../audyt_wizualny_i_poprawki_ui_2026-06-10.md` - raport audytu UI i wdrożonych poprawek.

## Zalecana kolejność ponownego uruchomienia

1. Uruchomić subagenta audytu treści na podstawie `01_audyt_tresci_subagent_mill.md`.
2. Po jego wynikach uruchomić subagenta napraw/researchu na podstawie `02_naprawy_i_research_subagent_nietzsche.md`.
3. Po regeneracji HTML uruchomić subagenta UI na podstawie `03_audyt_ui_subagent_aristotle.md`.
4. Na końcu uruchomić walidację lokalną:

```bash
python3 -m py_compile generuj_kompletne_wymagania_ogolne.py
python3 generuj_kompletne_wymagania_ogolne.py
node --check <(python3 - <<'PY'
from pathlib import Path
import re
html=Path('wymagania_ogolne_ZSZ5_2026_2027.html').read_text(encoding='utf-8')
m=re.search(r'<script>([\s\S]*)</script>', html)
print(m.group(1) if m else '')
PY
)
```

## Kryteria akceptacji

- 40 przedmiotów.
- 513 działów.
- 513 tabel wymagań.
- 0 pustych komórek ocen.
- 0 znaczników `X X X`.
- 0 znaczników `Cele 1 2`.
- 0 doklejonych bloków `Wymagania fakultatywne`.
- 0 doklejonych bloków `Zakres rozszerzony`.
- BS I / Edukacja dla bezpieczeństwa bez działów WDŻ.
- Strona ma wyszukiwarkę, indeks przedmiotów, hash-linki, poprawne `aria-*`, czytelny mobile layout i bezpieczne rozwijanie treści.

