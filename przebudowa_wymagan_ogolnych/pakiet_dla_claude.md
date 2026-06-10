# Pakiet kontekstowy dla Claude

Cel: kontynuować przebudowę strony `wymagania_ogolne_ZSZ5_2026_2027.html` po audycie jakości i prawdziwości wymagań edukacyjnych.

## Najważniejszy wniosek

Obecny HTML nie jest gotową, wiarygodną stroną wymagań edukacyjnych. Zawiera dużo treści z podstaw programowych, ale:

- ma braki działów;
- ma błędne lub nieaktualne źródła w WF;
- zawiera WDŻwR w technikum, co wymaga potwierdzenia po zmianach z 2025 r.;
- ma liczne duplikaty między kolumnami ocen;
- ma sklejone zdania po ekstrakcji PDF;
- nie ma uzasadnionego modelu przypisywania wymagań do ocen.

## Pliki wejściowe

- `wymagania_ogolne_ZSZ5_2026_2027.html`
- `wymagania_edukacyjne_kierunki_zawodowe_ZSZ5_2026_2027.html`
- `audyt_wymagan_ogolnych_prawdziwosc_i_gotowce.md`
- `audyt_wymagan_ogolnych_research_subagent.md`
- `przedmioty_wg_typu_szkoly/00_wszystkie_przedmioty_wg_typu_szkoly.md`
- `przebudowa_wymagan_ogolnych/model_wymagan_na_oceny_ZSZ5.md`
- `przebudowa_wymagan_ogolnych/macierz_zrodel_wymagan_ogolnych_ZSZ5.md`
- `przebudowa_wymagan_ogolnych/lista_brakow_i_kolejnosc_przebudowy.md`

## Model ocen

Używaj modelu K/P/R/D/W:

- dopuszczająca = wymagania konieczne;
- dostateczna = konieczne + podstawowe;
- dobra = konieczne + podstawowe + rozszerzające;
- bardzo dobra = poprzednie + dopełniające;
- celująca = poprzednie + wykraczające, twórcze, problemowe lub projektowe.

Wymagania są kumulatywne. Nie powtarzaj identycznej treści w każdej kolumnie. Każda wyższa ocena ma dodawać realnie wyższą trudność.

## Priorytety pracy

1. WF technikum i BS I - poprawić źródła.
2. Edukacja zdrowotna - dodać brakujące działy i potraktować osobno wartości/postawy.
3. EDB - dodać brakujące działy II i III.
4. Biologia - dodać brakujące działy.
5. Matematyka technikum i BS II - dodać brakujące działy.
6. Język polski technikum - dodać brakujące działy I i III.
7. Historia - wymaga najostrożniejszej ręcznej przebudowy.

## Polecenie dla Claude: przebudowa jednego przedmiotu

```text
Pracujesz na materiałach ZSZ5 2026/2027. Przebuduj wymagania edukacyjne dla wskazanego przedmiotu zgodnie z audytem.

Użyj plików:
- przebudowa_wymagan_ogolnych/model_wymagan_na_oceny_ZSZ5.md
- przebudowa_wymagan_ogolnych/macierz_zrodel_wymagan_ogolnych_ZSZ5.md
- przebudowa_wymagan_ogolnych/lista_brakow_i_kolejnosc_przebudowy.md
- odpowiedni lokalny PDF podstawy programowej
- wymagania_ogolne_ZSZ5_2026_2027.html jako materiał wejściowy, nie jako źródło prawdy dla ocen

Zadanie:
1. Ustal kompletną listę działów z podstawy programowej.
2. Porównaj ją z HTML-em.
3. Wypisz braki i błędy.
4. Opracuj wymagania na oceny w modelu K/P/R/D/W.
5. Oznacz źródło i status: "opracowanie ZSZ5 na podstawie podstawy programowej".
6. Nie kopiuj 1:1 gotowców internetowych. Używaj ich tylko jako wzorca struktury.
7. Zwróć wynik w Markdown: dział, źródło, tabela ocen, uwagi audytowe.
```

## Polecenie dla Claude: kontrola jakości gotowej tabeli

```text
Sprawdź poniższą tabelę wymagań edukacyjnych.

Kryteria:
1. Czy wszystkie działy są obecne?
2. Czy wymagania są realnie stopniowane od dopuszczającej do celującej?
3. Czy występują duplikaty między kolumnami?
4. Czy tekst nie wygląda jak sklejony z PDF?
5. Czy ocena celująca nie jest tylko losowym wymaganiem z podstawy, ale rzeczywiście poziomem twórczym/problemowym?
6. Czy przy WF, edukacji zdrowotnej i edukacji obywatelskiej zastosowano właściwy typ oceniania?

Zwróć:
- błędy krytyczne;
- błędy merytoryczne;
- poprawioną wersję tabeli;
- listę decyzji do potwierdzenia przez nauczyciela.
```

