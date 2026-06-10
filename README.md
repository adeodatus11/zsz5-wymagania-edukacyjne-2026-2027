# Wymagania edukacyjne ZSZ5 2026/2027

Repozytorium zawiera statyczną stronę z wymaganiami edukacyjnymi ZSZ5 na rok szkolny 2026/2027 oraz bibliotekę PDF podstaw programowych.

## Strona

Plik startowy GitHub Pages:

- `index.html`

Główny plik merytoryczny:

- `wymagania_edukacyjne_ZSZ5_2026_2027.html`

Strona zawiera:

- wymagania edukacyjne z przedmiotów ogólnokształcących,
- wymagania edukacyjne z kształcenia zawodowego,
- bibliotekę PDF podstaw programowych z filtrami według typu szkoły i kategorii.

## Biblioteka PDF

Podstawy programowe są przechowywane w katalogach:

- `01_BSI_stopnia/ogolne`
- `01_BSI_stopnia/zawodowe`
- `02_BSII_stopnia/ogolne`
- `02_BSII_stopnia/zawodowe`
- `03_Technikum/ogolne`
- `03_Technikum/zawodowe`

Manifest biblioteki:

- `data/podstawy_programowe.json`

## Generowanie

```bash
python3 generuj_kompletne_wymagania_ogolne.py
python3 generuj_wymagania_edukacyjne_ZSZ5.py
python3 scripts/validate_site.py
```

## GitHub Pages

Rekomendowana konfiguracja:

- repozytorium publiczne,
- branch: `main`,
- źródło GitHub Pages: root repozytorium,
- plik startowy: `index.html`.

## Ważna informacja

Podział wymagań na oceny jest opracowaniem ZSZ5 przygotowanym na podstawie lokalnych PDF podstaw programowych. Przed publikacją szkolną wymaga końcowej recenzji nauczycieli właściwych przedmiotów i zawodów.
