# Plan unifikacji stron wymagań ogólnokształcących i zawodowych

Data: 2026-06-09.

Pliki:

- `../wymagania_ogolne_ZSZ5_2026_2027.html`
- `../wymagania_edukacyjne_kierunki_zawodowe_ZSZ5_2026_2027.html`

## Wniosek audytowy

Strony nie powinny być unifikowane przez proste skopiowanie układu jednej do drugiej. Mają różne struktury:

- strona ogólnokształcąca jest podzielona według typu szkoły i przedmiotu;
- strona zawodowa jest podzielona według zawodu, kwalifikacji i jednostki efektów kształcenia.

Unifikować należy warstwę użytkową i audytową:

- wspólny nagłówek;
- wspólna legenda ocen;
- wspólne ostrzeżenia/statusy;
- wspólny opis źródeł;
- wspólne nazwy kolumn;
- wspólne zasady kolorów i tabel;
- podobny tryb druku.

## Elementy wspólne do wdrożenia

| Element | Strona ogólna | Strona zawodowa | Decyzja |
|---|---|---|---|
| Tytuł strony | `Wymagania edukacyjne – przedmioty ogólnokształcące` | `Wymagania edukacyjne – kształcenie zawodowe` | Utrzymać rozróżnienie, ale ujednolicić podtytuł i format. |
| Nawigacja | Zakładki: Technikum, BS II, BS I | Sticky nav z zawodami | Zostawić różne typy nawigacji, bo odpowiadają strukturze danych. |
| Legenda ocen | Brak pełnej legendy | Jest legenda czasowników ocen | Przenieść wspólną legendę ocen do strony ogólnej i urealnić ją w obu plikach. |
| Status audytu | Dodany banner roboczy | Brak analogicznego statusu | Dodać status źródeł i datę opracowania także do strony zawodowej. |
| Źródła | Ogólny opis w nagłówku | Podstawa zawodowa w podtytule | Dodać przy każdej grupie źródło lub status źródła. |
| Kolumny ocen | Dopuszczająca - Celująca | Dopuszczająca - Celująca | Ujednolicić nazwy i zasadę kumulatywności. |
| Druk | Minimalny | Ma sekcję print | Ujednolicić style print po zakończeniu przebudowy treści. |

## Wspólna legenda ocen

Proponowana legenda do obu stron:

| Ocena | Czasowniki i zakres |
|---|---|
| Dopuszczająca | rozpoznaje, wymienia, wskazuje, wykonuje prostą czynność z pomocą |
| Dostateczna | opisuje, wyjaśnia podstawowe pojęcia, wykonuje typowe zadanie |
| Dobra | stosuje, porównuje, dobiera metodę, wykonuje samodzielnie w typowej sytuacji |
| Bardzo dobra | analizuje, uzasadnia, planuje, weryfikuje, rozwiązuje złożony problem |
| Celująca | projektuje, ocenia, proponuje rozwiązania, działa twórczo lub rozwiązuje zadania nietypowe |

Uwaga: w stronie zawodowej obecna legenda ma dla oceny celującej sformułowanie `przeprowadza dowody`, które pasuje do matematyki, ale nie do większości kwalifikacji zawodowych. Należy zmienić na język zawodowy: `projektuje, optymalizuje, rozwiązuje niestandardowy problem, uzasadnia dobór technologii/procedury`.

## Statusy źródeł

Dodać wspólny blok statusu:

- `wersja robocza`;
- `w trakcie recenzji`;
- `zatwierdzone`;
- `wymaga aktualizacji źródła`;
- `nie publikować`.

## Kolejność unifikacji

1. Dodać ostrzeżenie/status do strony ogólnej.
2. Przygotować wspólną legendę ocen w Markdown.
3. Po zatwierdzeniu modelu przenieść legendę do obu HTML-i.
4. Dodać linki między stronami:
   - z ogólnej do zawodowej;
   - z zawodowej do ogólnej.
5. Ujednolicić nagłówek i podtytuł.
6. Ujednolicić druk i responsywność.
7. Dopiero na końcu ujednolicić wygląd tabel, żeby nie mieszać zmian wizualnych z merytorycznymi.

## Zasada bezpieczeństwa

Najpierw naprawić merytorykę strony ogólnej. Unifikacja wizualna ma sens dopiero wtedy, gdy:

- strona ogólna ma poprawne źródła;
- brakujące działy są uzupełnione;
- model ocen jest zaakceptowany;
- strona zawodowa przejdzie osobny audyt jakości treści.

