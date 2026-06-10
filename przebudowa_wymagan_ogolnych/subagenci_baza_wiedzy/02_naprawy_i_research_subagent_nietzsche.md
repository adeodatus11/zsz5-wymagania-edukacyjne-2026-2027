# Subagent: naprawy i research brakujących treści

Agent: `019eb02f-ae50-7ca2-9c08-16c8be5e9ab0`  
Nazwa: Nietzsche  
Rola: wyszukanie i naprawienie braków oraz błędnych ekstrakcji po audycie treści.

## Zakres pracy

Subagent miał:

- wykorzystać wyniki audytu treści,
- znaleźć poprawne podstawy programowe lub właściwe fragmenty lokalnych PDF,
- poprawić generator,
- ponownie wygenerować stronę,
- sprawdzić, czy błędy krytyczne zniknęły.

## Wprowadzone naprawy

- BS I / Edukacja dla bezpieczeństwa:
  - zastąpiono błędne treści WDŻ czterema działami EDB,
  - źródło: lokalny akt `01_BSI_stopnia/ogolne/PP_BSI_nowelizacja_28_06_2024_HiT_EdObyw_BizZarz_EdZdrow.pdf`,
  - oznaczenie: Dz.U. 2024 poz. 996.
- BS I / Wychowanie fizyczne:
  - zastąpiono sklejone fragmenty innymi treściami WF,
  - źródło: `03_Technikum/ogolne/PP_wychowanie_fizyczne_nowe_DzU_2025_poz1052.pdf`,
  - wynik: 9 działów WF.
- Technikum / Edukacja dla bezpieczeństwa:
  - zastąpiono wadliwą ekstrakcję czystymi czterema działami.
- Edukacja obywatelska i Edukacja zdrowotna:
  - dodano czyszczenie bloków `Wymagania fakultatywne`,
  - usunięto artefakty `X X X`, `Cele 1 2`, `Zakres rozszerzony`.
- Generator:
  - dodano cache odczytu PDF,
  - doprecyzowano czyszczenie tytułów i wymagań,
  - zachowano raportowanie końcowe.

## Zmienione pliki

- `../../generuj_kompletne_wymagania_ogolne.py`
- `../../wymagania_ogolne_ZSZ5_2026_2027.html`
- `../raport_generowania_kompletnej_strony.md`
- `../raport_napraw_tresci_wymagan.md`

## Walidacja po naprawach

- Przedmioty: 40.
- Działy: 513.
- Tabele: 513.
- Puste komórki: 0.
- `X X X`: 0.
- `Cele 1 2`: 0.
- `Wymagania fakultatywne`: 0.
- `Zakres rozszerzony`: 0.
- BS I / EDB: 4 właściwe działy EDB, bez WDŻ.

## Prompt do ponownego uruchomienia

```text
Na podstawie audytu treści napraw braki i błędne ekstrakcje w `generuj_kompletne_wymagania_ogolne.py`.

Zakres:
- popraw tylko generator i wygenerowany HTML,
- nie cofaj innych zmian,
- używaj lokalnych PDF-ów jako pierwszego źródła,
- jeśli trzeba, wyszukaj oficjalne źródła internetowe,
- po zmianach uruchom generator i walidację.

Priorytety:
1. BS I / EDB nie może zawierać WDŻ.
2. WF nie może zawierać sklejonych treści z innych przedmiotów.
3. EO/EZ nie mogą zawierać bloków fakultatywnych ani artefaktów tabel.
4. Każda tabela ocen musi mieć komplet pięciu kolumn.

Zwróć listę zmienionych plików, walidację liczbową i ryzyka pozostałe.
```

## Kryteria zakończenia

- Generator przechodzi `python3 -m py_compile`.
- HTML generuje się bez błędu.
- Walidacja liczbowa zgadza się z kryteriami akceptacji.
- Raport napraw opisuje, co zostało zmienione i jakie ryzyka pozostały.

