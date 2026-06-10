# Raport napraw treści wymagań ogólnokształcących

Data: 2026-06-10.

Zakres napraw: generator `generuj_kompletne_wymagania_ogolne.py` i ponownie wygenerowany HTML.

## Naprawy krytyczne

- BS I / Edukacja dla bezpieczeństwa: zastąpiono błędnie wyekstrahowane treści WDŻ czterema działami EDB na podstawie lokalnego aktu `01_BSI_stopnia/ogolne/PP_BSI_nowelizacja_28_06_2024_HiT_EdObyw_BizZarz_EdZdrow.pdf` (Dz.U. 2024 poz. 996).
- BS I / Wychowanie fizyczne: zastąpiono sklejone fragmenty biologii, informatyki, EDB i edukacji obywatelskiej czystymi dziewięcioma działami WF na podstawie `03_Technikum/ogolne/PP_wychowanie_fizyczne_nowe_DzU_2025_poz1052.pdf` (Dz.U. 2025 poz. 1052).
- Technikum / Edukacja dla bezpieczeństwa: zastąpiono ekstrakcję ręcznie oczyszczonymi czterema działami, bez oderwanych cytatów prawnych i bez sklejonych poddziałów.
- Edukacja obywatelska: ekstraktor odcina bloki `Wymagania fakultatywne` od wymagań obowiązkowych, aby nie mieszać ich bez oznaczenia.

## Naprawy mechanizmów czyszczenia

- Usuwanie końcowych znaczników tabel PDF typu `X X X` z wymagań.
- Usuwanie nagłówków tabel `Cele 1 2 3...` i `Umiejętności 1 2 3...` z treści wymagań.
- Odcinanie wtrętów `Zakres rozszerzony` z komórek wymagań, gdy zostały doklejone do zakresu podstawowego.
- Dodatkowe czyszczenie tytułów działów z uciętych separatorów i znaczników tabel.

## Walidacja końcowa

- Przedmioty: 35.
- Przedmioty bez działów: 0.
- Puste komórki ocen: 0 (generator zawsze wypełnia każdą kolumnę wymaganiem źródłowym albo progiem uzupełniającym).
- Znaczniki tabel `X X X` w HTML: brak.
- `Cele 1 2`, `Wymagania fakultatywne`, `Zakres rozszerzony` w HTML: brak.
- BS I / Edukacja dla bezpieczeństwa: 4 działy EDB (`Bezpieczeństwo państwa`, `Działania w sytuacjach nadzwyczajnych zagrożeń`, `Podstawy pierwszej pomocy`, `Kształtowanie postaw obronnych`), bez działów WDŻ.

## Ryzyka pozostałe

- Podział wymagań na oceny nadal jest opracowaniem ZSZ5 i wymaga recenzji nauczycieli przed publikacją.
- Ręcznie zdefiniowane działy krytyczne są streszczeniami i oczyszczonymi wymaganiami opartymi na lokalnych PDF-ach aktów, a nie pełnym cytatem podstawy programowej.
- Automatyczna ekstrakcja pozostałych przedmiotów może nadal wymagać redakcyjnej korekty tytułów i progów ocen.
