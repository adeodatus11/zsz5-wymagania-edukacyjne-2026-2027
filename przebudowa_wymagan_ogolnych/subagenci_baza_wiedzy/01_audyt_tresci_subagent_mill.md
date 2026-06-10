# Subagent: audyt treści wymagań

Agent: `019eb006-3b01-7be2-a2d0-0e1e10e8be9a`  
Nazwa: Mill  
Rola: audyt kompletności i poprawności treści wymagań ogólnokształcących.

## Zakres pracy

Subagent miał sprawdzić, czy finalna strona wymagań ogólnokształcących nie zawiera:

- przedmiotów bez działów,
- działów bez tabel,
- pustych komórek ocen,
- treści doklejonych z niewłaściwych przedmiotów,
- artefaktów ekstrakcji PDF,
- niepełnych albo błędnych bloków wymagań.

## Najważniejsze ustalenia

- Strona nie miała przedmiotów z zerową liczbą działów.
- Strona nie miała pustych kolumn ocen.
- Wykryto jednak krytyczne błędne ekstrakcje:
  - BS I / Edukacja dla bezpieczeństwa zawierała treści WDŻ.
  - BS I / Wychowanie fizyczne zawierało sklejone fragmenty z innych przedmiotów.
  - Edukacja obywatelska i edukacja zdrowotna miały artefakty tabel PDF, m.in. `X X X`, `Cele 1 2`, bloki fakultatywne i zakres rozszerzony.
  - Technikum / Edukacja dla bezpieczeństwa miało sklejone poddziały i fragmenty prawne.
- Wskazano także ryzyko zbyt optymistycznych statusów oraz generycznych progów ocen.

## Plik raportu wynikowego

Szczegółowy raport zapisano w:

`../audyt_subagenta_tresci_wymagan_2026-06-10.md`

## Prompt do ponownego uruchomienia

```text
Wykonaj audyt treści strony `wymagania_ogolne_ZSZ5_2026_2027.html`.

Nie edytuj plików. Sprawdź:
- czy każdy przedmiot ma działy,
- czy każdy dział ma tabelę ocen,
- czy żadna komórka ocen nie jest pusta,
- czy przedmioty nie mają treści z innych przedmiotów,
- czy nie ma artefaktów PDF typu `X X X`, `Cele 1 2`, `Zakres rozszerzony`, `Wymagania fakultatywne`,
- czy BS I / Edukacja dla bezpieczeństwa nie zawiera WDŻ,
- czy WF, EDB, Edukacja obywatelska i Edukacja zdrowotna nie są sklejone z innymi podstawami.

Zwróć raport po polsku: priorytet, miejsce w pliku, problem, konsekwencja, rekomendacja. Nie wprowadzaj zmian.
```

## Kryteria zakończenia

- Wszystkie braki i błędy są spisane z konkretnym miejscem w pliku.
- Raport oddziela problemy krytyczne od redakcyjnych.
- Raport wskazuje, które błędy wymagają subagenta naprawczego.

