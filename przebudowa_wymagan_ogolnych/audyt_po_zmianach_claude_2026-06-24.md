# Audyt strony po zmianach Claude - 2026-06-24

## Zakres

Audyt objął finalną stronę `index.html` i `wymagania_edukacyjne_ZSZ5_2026_2027.html`, manifest `data/podstawy_programowe.json`, generatory Python oraz lokalne foldery PDF podstaw programowych.

## Wynik audytu kompletności podstaw programowych

- Manifest zawiera 38 plików PDF: 28 ogólnokształcących i 10 zawodowych.
- Wszystkie ścieżki z manifestu istnieją lokalnie i są linkowane ze strony.
- Przedmioty ogólnokształcące mają przypisane podstawy programowe jako osobne PDF-y albo jako wspólne akty dla kilku przedmiotów.
- Kształcenie zawodowe jest pokryte przez PDF-y zawodów i kwalifikacji. Strona pokazuje je jako kierunki/zawody, nie jako każdą modułową pozycję z ramówki.
- Pozycje z ramówek takie jak religia, zajęcia z wychowawcą, doradztwo zawodowe i rozwój kompetencji nie mają osobnych podstaw PDF w tej bibliotece i są traktowane jako `nie dotyczy`.

## Ustalenia krytyczne i wdrożone poprawki

| Obszar | Ustalenie | Działanie |
|---|---|---|
| Strona startowa | `index.html` miało home dodane ręcznie, ale generator mógł je nadpisać. | Home przeniesiono do `generuj_wymagania_edukacyjne_ZSZ5.py`; oba pliki HTML są teraz generowane z jednego źródła. |
| Logotyp | Brak logotypu szkoły w finalnym HTML. | Dodano `assets/logo-zsz5.jpg` pobrany z oficjalnej strony szkoły EduPage i osadzono w nagłówku oraz sekcji startowej. |
| Statusy | Etykieta `gotowe` mogła sugerować zatwierdzenie merytoryczne. | Status wymagań ogólnych zmieniono na `projekt do zatwierdzenia`; status PDF w bibliotece to `podstawa dostępna`. |
| Treść home | Wstęp sugerował, że całość opiera się tylko na zmianach z 28.06.2024. | Tekst doprecyzowano: strona korzysta z aktów i materiałów źródłowych z biblioteki PDF, w tym zmian z 2024 i 2025 r. |
| Opracowania ORE | Część linków ORE była kandydatami 404; wracała też pozycja `Plastyka / Historia sztuki`. | Zostawiono tylko linki zweryfikowane jako PDF 200; usunięto plastykę i linki 404. |
| Artefakty PDF | W treści występowały typowe artefakty ekstrakcji: `r eaguje`, `e -mail`, `klim at`, końcówki przypisów i godzin w tytułach. | Dodano dodatkowe czyszczenie tekstu w generatorach. |

## Uwagi merytoryczne

- Wymagania na oceny pozostają projektem roboczym. Przed publikacją dla uczniów i rodziców powinny zostać zatwierdzone przez nauczycieli przedmiotów i zawodów.
- Dla zawodów wymagania są generowane automatycznie z efektów kształcenia i kryteriów weryfikacji. To wymaga recenzji nauczycieli zawodowych.
- WF ma poprawne źródła treściowe, mimo mylących folderów lokalnych: poz. 1035 dotyczy LO/technikum/BS II, a poz. 1052 obejmuje m.in. BS I.

## Walidacja techniczna

- `python3 -m py_compile` dla generatorów i skryptów: OK.
- `python3 scripts/validate_site.py`: OK.
- `node --check` dla skryptu osadzonego w HTML: OK.
- Kontrola zakazanych nazw po wcześniejszym usunięciu przedmiotów: OK.
- Test responsywności strony w widoku telefonu: wykonany po regeneracji strony.
- Screenshoty mobilne:
  - `przebudowa_wymagan_ogolnych/mobile-home-390.png`
  - `przebudowa_wymagan_ogolnych/mobile-pdf-search-390.png`
