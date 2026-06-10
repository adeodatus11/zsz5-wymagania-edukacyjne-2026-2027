# Audyt wizualny i poprawki UI strony wymagań ogólnokształcących

Data: 2026-06-10.

Plik audytowany i poprawiony: `wymagania_ogolne_ZSZ5_2026_2027.html`

## Wynik audytu subagenta

Subagent wykonał statyczny audyt czytelności, dostępności i ergonomii strony z dużą liczbą treści. Renderowania przez `file://` nie wykonywano, ponieważ wcześniejsze próby były blokowane przez środowisko i nie obchodzono tego ograniczenia.

Najważniejsze problemy wskazane przez audyt:

- brak wyszukiwarki i bezpośrednich linków do przedmiotów lub działów,
- zbyt ciężka akcja `Rozwiń wszystko`, otwierająca setki tabel naraz,
- brak statycznych stanów dostępności dla akordeonów i zakładek,
- słaba ergonomia tabel na urządzeniach mobilnych,
- brak szybkiego powrotu na górę i spisu przedmiotów,
- brak głębokich linków URL/hash,
- niespójność wizualna ze stroną zawodową w zakresie kolorowania kolumn ocen,
- widoczne techniczne ścieżki źródeł PDF w każdym przedmiocie.

## Wdrożone poprawki

- Dodano wyszukiwarkę w każdej zakładce typu szkoły. Filtr działa po nazwie przedmiotu, źródle i tytułach działów.
- Dodano szybki indeks przedmiotów pod nagłówkiem każdej szkoły.
- Dodano głębokie linki `#technikum_10`, `#technikum_10_0` itd. Link otwiera właściwą szkołę, przedmiot i dział.
- Zmieniono akcję globalną na bezpieczniejsze `Rozwiń przedmioty`; pełne rozwinięcie wszystkich działów wymaga potwierdzenia.
- Dodano przyciski `Rozwiń działy przedmiotu` i `Zwiń działy przedmiotu` w każdym przedmiocie.
- Dodano statyczne i dynamiczne `aria-expanded`, `aria-controls`, `aria-selected`, `role="tablist"`, `role="tab"` i `role="tabpanel"`.
- Dodano wyraźny `:focus-visible` dla obsługi klawiaturą.
- Dodano przycisk powrotu na górę.
- Zmieniono źródła PDF na zwijane `<details>`, aby nie dominowały nad treścią.
- Ujednolicono tabele ze stroną zawodową przez kolorowe kolumny ocen.
- Dodano mobilny układ tabel: na małych ekranach każda ocena jest osobnym blokiem z nazwą oceny.
- Dodano etykiety `data-label` do wszystkich komórek ocen.
- Dodano tryb druku bieżącej szkoły.
- Dodano polską odmianę liczników: `1 wymaganie`, `2 wymagania`, `5 wymagań`.
- Dodano drobne czyszczenie typowych rozbić wyrazów z ekstrakcji PDF.

## Walidacja końcowa

- Przedmioty: 40.
- Działy: 513.
- Tabele wymagań: 513.
- Komórki ocen z etykietami mobilnymi: 2565.
- Puste komórki ocen: 0.
- Polskie błędy liczników typu `1 wymagań`: 0.
- `X X X` w HTML: 0.
- `Cele 1 2` w HTML: 0.
- `Wymagania fakultatywne` w HTML: 0.
- `Zakres rozszerzony` w HTML: 0.
- Parser HTML: bez błędów.
- `node --check` dla skryptu strony: bez błędów.

## Ryzyka pozostałe

- Nie wykonano wizualnego testu w przeglądarce przez ograniczenie `file://`; audyt UI opierał się na analizie HTML/CSS/JS i walidatorach.
- Podział wymagań na oceny jest opracowaniem ZSZ5 i nadal wymaga końcowej recenzji nauczycieli przed publikacją.
- Część treści pochodzi z automatycznej ekstrakcji PDF, więc mogą pozostać pojedyncze redakcyjne artefakty spacji lub łamania wyrazów.
