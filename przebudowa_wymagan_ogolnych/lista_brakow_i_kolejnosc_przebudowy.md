# Lista braków i kolejność przebudowy

Data: 2026-06-09.

## Krytyczne decyzje przed publikacją

1. Oznaczyć obecny HTML jako wersję roboczą.
2. Nie publikować obecnego podziału na oceny jako finalnego.
3. Potwierdzić źródła WF:
   - technikum i BS II: Dz.U. 2025 poz. 1035;
   - BS I: Dz.U. 2025 poz. 1052.
4. Potwierdzić, czy WDŻwR ma pozostać na stronie technikum dla roku 2026/2027.
5. Przyjąć jeden model ocen: najlepiej K/P/R/D/W z zasadą kumulatywności.

## Braki działów

| Priorytet | Typ szkoły | Przedmiot | Brak / problem | Działanie |
|---:|---|---|---|---|
| 1 | Technikum | Wychowanie fizyczne | Obecna wersja bazuje na starej podstawie albo błędnym akcie | Odbudować od zera z Dz.U. 2025 poz. 1035. |
| 1 | BS I | Wychowanie fizyczne | Prawdopodobnie użyto aktu dla LO/technikum/BS II | Odbudować z Dz.U. 2025 poz. 1052. |
| 1 | Technikum | WDŻwR | Prawdopodobnie nieaktualne po zmianach 2025 | Usunąć z finalnej strony albo przenieść do archiwum po potwierdzeniu. |
| 1 | Technikum | Historia | Bardzo niska zgodność i ryzyko brakujących działów | Zrobić ręczną mapę działów z PDF, potem przepisać wymagania. |
| 2 | Technikum | Biologia | Brakuje II, IV, VI, VIII, IX, X, XI | Dodać brakujące działy z PDF, potem opracować oceny. |
| 2 | Technikum | EDB | Brakuje II i III | Dodać `Przygotowanie do działań ratowniczych` i `Podstawy pierwszej pomocy`. |
| 2 | Technikum | Edukacja zdrowotna | Brakuje I i VIII | Dodać `Wartości i postawy` i `Zdrowie środowiskowe`. |
| 2 | Technikum | Język polski | Są tylko II i IV | Dodać I `Kształcenie literackie i kulturowe` oraz III `Tworzenie wypowiedzi`. |
| 2 | Technikum | Matematyka | Brakuje VIII i XIII | Dodać `Planimetria` oraz `Optymalizacja i rachunek różniczkowy`. |
| 2 | BS II | Matematyka | Brakuje XIII | Dodać `Optymalizacja`. |
| 2 | BS I | Edukacja zdrowotna | Brakuje I i jest duplikat II | Dodać I, usunąć duplikat II. |
| 3 | Chemia, Fizyka, Geografia, Informatyka, Języki | Duplikaty i sklejone zdania | Przejść przez dział po dziale i przepisać na model ocen. |

## Zalecana kolejność naprawy

### Etap 1 - zabezpieczenie strony

- Dodać ostrzeżenie w HTML, że strona jest wersją roboczą po audycie.
- Podlinkować raporty audytu.
- Nie usuwać jeszcze danych, żeby zachować materiał wejściowy.

### Etap 2 - źródła i działy

1. WF technikum i BS I.
2. Edukacja zdrowotna technikum i BS I.
3. EDB technikum.
4. Biologia technikum.
5. Matematyka technikum i BS II.
6. Język polski technikum.
7. Historia technikum.

### Etap 3 - przebudowa ocen

Najpierw zrobić 2-3 wzorcowe przedmioty:

1. EDB - dobry kandydat, bo zakres jest praktyczny i łatwo ocenić progresję.
2. Matematyka - dobry kandydat do modelu P/PP.
3. Edukacja obywatelska - nowy przedmiot, warto od razu przyjąć właściwy model.

Po zatwierdzeniu wzorca można przepisać pozostałe przedmioty.

## Kontrola jakości każdej tabeli

Przed wpisaniem działu do finalnego HTML sprawdzić:

- czy nazwa działu jest zgodna ze źródłem;
- czy wymagania nie są sklejone z PDF;
- czy nie ma duplikatów między kolumnami ocen;
- czy ocena wyższa rzeczywiście oznacza wyższą trudność;
- czy przy WF i edukacji zdrowotnej nie oceniamy rzeczy, których nie powinno się oceniać wprost;
- czy opis jest możliwy do użycia przez nauczyciela i zrozumiały dla ucznia/rodzica.

## Definicja gotowości

Przedmiot ma status `gotowy do publikacji`, gdy:

1. ma kompletną listę działów;
2. ma wskazane źródło podstawy;
3. ma wymagania przepisane na model ocen;
4. przeszedł kontrolę duplikatów;
5. przeszedł kontrolę językową;
6. został zatwierdzony przez nauczyciela przedmiotu albo osobę merytorycznie odpowiedzialną.

