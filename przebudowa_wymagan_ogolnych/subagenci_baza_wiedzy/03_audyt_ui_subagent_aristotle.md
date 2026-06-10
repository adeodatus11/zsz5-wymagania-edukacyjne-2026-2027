# Subagent: audyt czytelności, UI i dostępności

Agent: `019eb03b-954d-73d2-af49-e28345edd77a`  
Nazwa: Aristotle  
Rola: audyt wizualny i funkcjonalny strony przy dużej liczbie treści.

## Zakres pracy

Subagent miał statycznie sprawdzić:

- ergonomię nawigacji przy 40 przedmiotach i 513 tabelach,
- zachowanie akordeonów,
- dostępność klawiaturą i przez czytniki ekranu,
- użyteczność na mobile,
- drukowanie,
- spójność ze stroną zawodową,
- ryzyka czytelności.

Renderowania przez `file://` nie wykonywano, ponieważ wcześniejsze próby były blokowane przez środowisko. Ograniczenia nie obchodzono.

## Najważniejsze ustalenia

- Brak wyszukiwarki i bezpośrednich linków do przedmiotów/działów był krytyczny.
- `Rozwiń wszystko` było zbyt ciężkie dla Technikum, ponieważ mogło otworzyć ponad 300 tabel naraz.
- Akordeony wymagały `aria-expanded`, `aria-controls` i lepszego powiązania przycisków z panelami.
- Mobile wymagał alternatywy dla szerokich tabel.
- Brakowało przycisku powrotu na górę i indeksu przedmiotów.
- Zakładki szkół wymagały wyraźniejszego stanu aktywnego.
- Strona ogólna i zawodowa miały różne modele tabel; wskazano potrzebę wspólnego kolorowania kolumn ocen.
- Źródła PDF w każdym przedmiocie były zbyt techniczne i powinny być zwijane.

## Wdrożone poprawki po audycie

Szczegółowy raport wdrożenia zapisano w:

`../audyt_wizualny_i_poprawki_ui_2026-06-10.md`

Najważniejsze wdrożenia:

- wyszukiwarka przedmiotów i działów,
- indeks przedmiotów,
- hash-linki do szkoły, przedmiotu i działu,
- `aria-expanded`, `aria-controls`, `aria-selected`, role tabów i paneli,
- wyraźny `:focus-visible`,
- bezpieczniejsze rozwijanie treści,
- rozwijanie działów tylko w pojedynczym przedmiocie,
- przycisk powrotu na górę,
- mobilny układ tabel z etykietami ocen,
- kolorowe kolumny ocen spójniejsze ze stroną zawodową,
- źródła PDF zwinięte w `<details>`,
- druk bieżącej szkoły.

## Walidacja po wdrożeniu

- Przedmioty: 40.
- Działy: 513.
- Tabele: 513.
- Komórki ocen z etykietami mobilnymi: 2565.
- Puste komórki: 0.
- Parser HTML: OK.
- `node --check` dla skryptu strony: OK.

## Prompt do ponownego uruchomienia

```text
Wykonaj audyt czytelności, UI i dostępności strony `wymagania_ogolne_ZSZ5_2026_2027.html`.

Nie edytuj plików. Sprawdź:
- czy wyszukiwarka działa logicznie przy dużej liczbie treści,
- czy indeks przedmiotów i hash-linki prowadzą do właściwych miejsc,
- czy akordeony mają poprawne `aria-*`,
- czy obsługa klawiaturą jest czytelna,
- czy mobile layout tabel jest zrozumiały,
- czy druk bieżącej szkoły jest sensowny,
- czy strona jest spójna ze stroną zawodową,
- czy są pozostałe problemy czytelności przy bardzo dużej liczbie tabel.

Zwróć raport po polsku w tabeli: priorytet, miejsce w pliku, problem, konsekwencja, rekomendowana poprawka. Nie wprowadzaj zmian.
```

## Kryteria zakończenia

- Raport oddziela problemy krytyczne, ważne i kosmetyczne.
- Każda rekomendacja jest wdrażalna w generatorze.
- Audyt jasno wskazuje, czy był oparty na renderowaniu, czy na analizie statycznej.

