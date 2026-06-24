# Audyt i naprawa modelu wymagań na oceny - 2026-06-24

## Powód audytu

W trakcie ręcznej kontroli podstawy programowej języka polskiego dla branżowej szkoły II stopnia wykryto, że poprzedni generator przypisywał kolejne punkty podstawy programowej do kolejnych ocen. Był to błąd modelowy: kolejność punktów w podstawie programowej nie oznacza narastającego poziomu trudności ani progu oceniania.

## Ustalenie

Poprzednia funkcja `split_requirements()` dzieliła listę wymagań źródłowych na pięć kolejnych części i wpisywała je do kolumn:

- `Dopuszczająca`,
- `Dostateczna`,
- `Dobra`,
- `Bardzo dobra`,
- `Celująca`.

Ten wzorzec obejmował zarówno przedmioty ogólnokształcące, jak i zawodowe, ponieważ strona zintegrowana korzystała z tej samej funkcji przy generowaniu tabel.

## Decyzja naprawcza

Usunięto mechaniczne dzielenie wymagań źródłowych na oceny. Obecny model jest źródłowo bezpieczniejszy:

1. Każdy wiersz tabeli pokazuje jedno wymaganie lub kryterium z podstawy programowej.
2. Kolumny ocen opisują poziom opanowania tego samego wymagania.
3. Ocena wyższa nie oznacza innego punktu podstawy, tylko wyższy poziom samodzielności, poprawności, złożoności, uzasadnienia i transferu wiedzy lub umiejętności.

## Model dla przedmiotów ogólnokształcących

| Ocena | Znaczenie progu |
|---|---|
| Dopuszczająca | Uczeń z pomocą nauczyciela rozpoznaje wymaganie źródłowe i wykonuje najprostsze zadania odtwórcze dotyczące tego wymagania. |
| Dostateczna | Uczeń samodzielnie odtwarza podstawowe wiadomości i wykonuje typowe zadania bez rozbudowanego uzasadnienia. |
| Dobra | Uczeń poprawnie stosuje wiadomości i umiejętności w typowych sytuacjach oraz wyjaśnia podstawowe zależności. |
| Bardzo dobra | Uczeń sprawnie analizuje, porównuje, dobiera sposób działania i uzasadnia rozwiązania w pełnym zakresie realizowanego materiału. |
| Celująca | Uczeń samodzielnie i twórczo wykorzystuje wymaganie w nowym kontekście, łączy je z innymi treściami i rozwiązuje zadania problemowe. |

## Model dla przedmiotów zawodowych

| Ocena | Znaczenie progu |
|---|---|
| Dopuszczająca | Uczeń z pomocą nauczyciela lub instruktora rozpoznaje kryterium i wykonuje podstawowe czynności zgodnie z instrukcją. |
| Dostateczna | Uczeń wykonuje typowe czynności zawodowe według procedury, z zachowaniem podstawowych zasad jakości i bezpieczeństwa. |
| Dobra | Uczeń samodzielnie stosuje kryterium w typowych zadaniach zawodowych, dobiera narzędzia lub informacje i koryguje proste błędy. |
| Bardzo dobra | Uczeń sprawnie planuje, wykonuje i kontroluje jakość działania, uzasadnia dobór metod oraz reaguje na typowe problemy. |
| Celująca | Uczeń samodzielnie rozwiązuje nietypowe problemy zawodowe, proponuje usprawnienia i łączy kryterium z szerszym procesem pracy. |

## Walidacja po naprawie

Wykonano lokalnie:

```bash
python3 -m py_compile generuj_kompletne_wymagania_ogolne.py generuj_wymagania_edukacyjne_ZSZ5.py scripts/validate_site.py
python3 generuj_kompletne_wymagania_ogolne.py
python3 generuj_wymagania_edukacyjne_ZSZ5.py
python3 scripts/validate_site.py
```

Wynik:

- 35 przedmiotów ogólnokształcących,
- 10 programów zawodowych,
- 38 plików PDF w bibliotece,
- 584 tabele wymagań i kryteriów w finalnym `index.html`,
- 7323 wiersze wymagań/kryteriów,
- 0 wierszy z niepełną liczbą kolumn,
- 0 odwołań do dawnej funkcji `split_requirements()`.

## Ograniczenia

Ta naprawa usuwa błąd polegający na traktowaniu kolejności punktów podstawy jako kolejnych ocen. Nie oznacza jednak, że generator zastępuje recenzję nauczyciela. Finalne wymagania nadal powinny zostać sprawdzone przez nauczycieli przedmiotów i zawodów oraz dostosowane do programu nauczania, rozkładu materiału i realnych warunków pracy z konkretną klasą.
