# Przewodnik dla nauczyciela ZSZ5 2026/2027

Repozytorium zawiera statyczny przewodnik dla nauczycieli ZSZ5: od podstawy programowej przez rozkład materiału do wymagań edukacyjnych i zasad oceniania.

## Struktura strony

- `index.html` - ścieżka pracy od podstawy programowej do wymagań na oceny.
- `rozklad_materialu.html` - rozkład materiału, terminy, szablon XLSX i opis kolumn.
- `adaptacja_programu.html` - jak adaptować program nauczania w praktyce.
- `materialy_i_linki.html` - katalog podstaw programowych, szablon rozkładu i materiały zewnętrzne.
- `podstawy_prawne.html` - podstawy prawne i źródła.
- `wymagania_edukacyjne_ZSZ5_2026_2027.html` - kompatybilny adres wejściowy z treścią strony startowej.
- `katalog_podstaw_programowych_ZSZ5_2026_2027.html` - klikalny katalog podstaw programowych ZSZ5.

## Rozkład materiału

Widoczny na stronie szablon pochodzi z pliku:

- `rozkłady materiału przedmiotów/rozkład materiału - szablon 2026_2027.xlsx`

Podglądy arkuszy są zapisane jako:

- `assets/rozklad-materialu-wzor.png`
- `assets/rozklad-materialu-szablon.png`

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
