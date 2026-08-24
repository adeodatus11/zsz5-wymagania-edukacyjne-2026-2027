# Przewodnik dla nauczyciela ZSZ5 2026/2027

Repozytorium zawiera statyczną stronę roboczą dla nauczycieli ZSZ5. Obecny widok główny nie publikuje tabel wymagań wygenerowanych przez AI. Na stronie zostaje przewodnik pokazujący drogę od podstawy programowej przez program nauczania i rozkład materiału do wymagań na oceny.

## Strona

Plik startowy GitHub Pages:

- `index.html`

Zapasowy adres wejściowy, obecnie z tą samą treścią:

- `wymagania_edukacyjne_ZSZ5_2026_2027.html`

Klikalny katalog podstaw programowych:

- `katalog_podstaw_programowych_ZSZ5_2026_2027.html`

## Co jest widoczne

- przewodnik od podstawy programowej do wymagań na oceny,
- materiały i linki pomocnicze,
- sekcja o rozkładzie materiału,
- przykładowy rozkład materiału z pliku `rozkłady materiału przedmiotów/rozkład materiału - szablon 2026_2027.xlsx`,
- sekcja o adaptacji programu,
- podstawy prawne,
- link do katalogu podstaw programowych ZSZ5.

## Co zostało schowane

Robocze opracowanie AI z tabelami wymagań dla typów szkół, przedmiotów i zawodów zostało odłożone na branch:

- `codex/opracowanie-ai-podstaw-programowych`

## Generowanie

```bash
python3 generuj_katalog_podstaw_programowych.py
python3 generuj_przewodnik_nauczyciela_ZSZ5.py
python3 scripts/validate_site.py
```

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
