# Audyt źródłowości i ryzyka halucynacji wymagań

Data: 2026-06-24.

## Werdykt

Nie można uczciwie powiedzieć, że wszystkie tabele na stronie są gotowymi, w pełni zatwierdzonymi wymaganiami szkolnymi. Można natomiast powiedzieć, że po poprawce z 2026-06-24 usunięto najgroźniejszy typ halucynacji: automatycznie dopisywane zdania zastępcze, które wyglądały jak wymagania, ale nie pochodziły z podstaw programowych.

Aktualny stan:

- 45 pozycji audytowanych: 35 przedmiotów ogólnokształcących i 10 pozycji zawodowych.
- 0 pozycji blokujących po poprawce.
- 0 wygenerowanych fillerów progów ocen typu `samodzielnie wykonuje zadanie problemowe...`.
- 19 pozycji źródłowo śledzalnych.
- 23 pozycje do sprawdzenia, głównie z powodu niedoskonałego dopasowania tekstu po ekstrakcji PDF.
- 3 pozycje do recenzji, bo są ręczną rekonstrukcją działów/pozycji, a nie literalnym ekstraktem.

## Co jest realnie z podstaw programowych

Źródłowe są:

- działy, jednostki efektów kształcenia, kwalifikacje i większość pozycji wymagań/kryteriów wyciągniętych z lokalnych PDF-ów;
- biblioteka PDF podstaw programowych;
- statusy źródeł i ścieżki do plików.

Nie są oficjalną częścią podstawy programowej:

- przypisanie wymagań do ocen `Dopuszczająca`, `Dostateczna`, `Dobra`, `Bardzo dobra`, `Celująca`;
- szkolna interpretacja progów ocen;
- ręczne rekonstrukcje EDB i części WF;
- komunikaty typu `Próg do określenia przez nauczyciela...`, które są celowym oznaczeniem braku automatycznego progu, a nie wymaganiem.

## Co zostało naprawione w trakcie audytu

Usunięto mechanizmy, które tworzyły treści niepochodzące z podstaw:

- `Uczeń omawia najważniejsze zagadnienia działu...`
- `omawia podstawowe zagadnienia jednostki...`
- `samodzielnie wykonuje zadanie problemowe...`
- `łączy wiadomości z działu...`
- `stosuje wiadomości z działu...`
- `opisuje podstawowe pojęcia i przykłady...`
- `rozpoznaje podstawowe pojęcia i przykłady...`

Jeżeli w danej komórce tabeli nie ma pozycji źródłowej, strona pokazuje teraz neutralny komunikat:

`Próg do określenia przez nauczyciela na podstawie programu nauczania.`

To jest bezpieczniejsze niż fałszywa kompletność.

## Źródła oficjalne użyte do kontroli

- Dziennik Ustaw 2019 poz. 991 - podstawa programowa kształcenia w zawodach szkolnictwa branżowego: https://dziennikustaw.gov.pl/DU/2019/991
- Dziennik Ustaw 2025 poz. 1035 - wychowanie fizyczne dla LO, technikum i branżowej szkoły II stopnia: https://dziennikustaw.gov.pl/D2025000103501.pdf
- Dziennik Ustaw 2025 poz. 1052 - wychowanie fizyczne dla szkoły podstawowej i branżowej szkoły I stopnia: https://dziennikustaw.gov.pl/D2025000105201.pdf
- Dziennik Ustaw 2025 poz. 378 - edukacja obywatelska dla branżowej szkoły I stopnia: https://dziennikustaw.gov.pl/D2025000037801.pdf
- Dziennik Ustaw 2025 poz. 382 - edukacja obywatelska dla LO, technikum i branżowej szkoły II stopnia: https://dziennikustaw.gov.pl/du/2025/382
- MEN - materiały dla nauczycieli szkół ponadpodstawowych: https://www.gov.pl/web/edukacja/podstawa-programowa--materialy-dla-nauczycieli-szkol-ponadpodstawowych
- ORE - podstawa programowa z 28 czerwca 2024 r.: https://ore.edu.pl/2024/09/podstawa-programowa-z-28-czerwca-2024-r/
- ORE - podstawa programowa LO, technikum i BS II 2018: https://ore.edu.pl/2018/03/podstawa-programowa-ksztalcenia-ogolnego-dla-liceum-technikum-i-branzowej-szkoly-ii-stopnia/

## Metoda audytu

Audyt wykonano skryptem `scripts/audit_source_traceability.py`.

Skrypt:

- importuje aktualne generatory strony;
- przechodzi po wszystkich specyfikacjach przedmiotów i zawodów;
- sprawdza, czy lokalny PDF istnieje;
- wykrywa ręcznie rekonstruowane sekcje;
- wykrywa wygenerowane zdania zastępcze;
- porównuje oczyszczone pozycje z oczyszczonym tekstem lokalnego PDF;
- oddziela treści źródłowe od szkolnego przypisania do ocen.

## Rejestr ryzyka

| Typ szkoły | Typ | Pozycja | Działy/jednostki | Pozycje źródłowe | Status | Ryzyko |
|---|---|---|---:|---:|---|---|
| Branżowa Szkoła I stopnia | ogólne | Edukacja dla bezpieczeństwa | 4 | 30 | do recenzji | ręczna rekonstrukcja działów/pozycji z podstawy, nie ekstrakt literalny |
| Branżowa Szkoła I stopnia | ogólne | Wychowanie fizyczne | 9 | 33 | do recenzji | ręczna rekonstrukcja działów/pozycji z podstawy, nie ekstrakt literalny |
| Technikum | ogólne | Edukacja dla bezpieczeństwa | 4 | 41 | do recenzji | ręczna rekonstrukcja działów/pozycji z podstawy, nie ekstrakt literalny |
| Branżowa Szkoła I stopnia | ogólne | Biologia | 2 | 15 | do sprawdzenia | 1 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła I stopnia | ogólne | Fizyka | 3 | 29 | do sprawdzenia | 1 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła I stopnia | ogólne | Geografia | 3 | 27 | do sprawdzenia | 1 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła I stopnia | ogólne | Język angielski | 26 | 151 | do sprawdzenia | 4 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła I stopnia | ogólne | Język niemiecki | 26 | 151 | do sprawdzenia | 4 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła I stopnia | ogólne | Język polski | 3 | 28 | do sprawdzenia | 1 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła I stopnia | ogólne | Matematyka | 7 | 34 | do sprawdzenia | 2 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła I stopnia | zawodowe | Cukiernik | 8 | 267 | do sprawdzenia | 2 kryteriów nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła I stopnia | zawodowe | Fryzjer | 10 | 376 | do sprawdzenia | 1 kryteriów nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła I stopnia | zawodowe | Kelner | 9 | 310 | do sprawdzenia | 9 kryteriów nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła I stopnia | zawodowe | Lakiernik samochodowy | 10 | 285 | do sprawdzenia | 2 kryteriów nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła II stopnia | ogólne | Język polski | 4 | 26 | do sprawdzenia | 1 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła II stopnia | ogólne | Matematyka | 13 | 121 | do sprawdzenia | 14 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła II stopnia | zawodowe | Technik usług fryzjerskich | 17 | 608 | do sprawdzenia | 2 kryteriów nie dopasowano literalnie po czyszczeniu ekstraktu |
| Technikum | ogólne | Chemia | 22 | 153 | do sprawdzenia | 2 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Technikum | ogólne | Historia | 59 | 484 | do sprawdzenia | 187 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Technikum | ogólne | Historia i teraźniejszość | 6 | 108 | do sprawdzenia | 4 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Technikum | ogólne | Język polski | 4 | 26 | do sprawdzenia | 1 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Technikum | ogólne | Matematyka | 13 | 121 | do sprawdzenia | 14 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Technikum | ogólne | Wiedza o społeczeństwie | 7 | 64 | do sprawdzenia | 1 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Technikum | ogólne | Wychowanie fizyczne | 9 | 49 | do sprawdzenia | 1 pozycji nie dopasowano literalnie po czyszczeniu ekstraktu |
| Technikum | zawodowe | Technik handlowiec | 17 | 566 | do sprawdzenia | 3 kryteriów nie dopasowano literalnie po czyszczeniu ekstraktu |
| Technikum | zawodowe | Technik usług fryzjerskich | 17 | 608 | do sprawdzenia | 2 kryteriów nie dopasowano literalnie po czyszczeniu ekstraktu |
| Branżowa Szkoła I stopnia | ogólne | Biznes i zarządzanie | 6 | 64 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Branżowa Szkoła I stopnia | ogólne | Chemia | 6 | 30 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Branżowa Szkoła I stopnia | ogólne | Edukacja obywatelska | 7 | 31 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Branżowa Szkoła I stopnia | ogólne | Historia | 18 | 95 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Branżowa Szkoła I stopnia | ogólne | Historia i teraźniejszość | 7 | 46 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Branżowa Szkoła I stopnia | ogólne | Informatyka | 7 | 28 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Branżowa Szkoła I stopnia | zawodowe | Kucharz | 3 | 83 | źródłowo śledzalne | jednostki i kryteria pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Branżowa Szkoła I stopnia | zawodowe | Mechanik pojazdów samochodowych | 7 | 266 | źródłowo śledzalne | jednostki i kryteria pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Branżowa Szkoła I stopnia | zawodowe | Sprzedawca | 7 | 243 | źródłowo śledzalne | jednostki i kryteria pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Branżowa Szkoła II stopnia | ogólne | Informatyka | 5 | 45 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Branżowa Szkoła II stopnia | ogólne | Język angielski | 39 | 337 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Technikum | ogólne | Biologia | 11 | 154 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Technikum | ogólne | Biznes i zarządzanie | 6 | 64 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Technikum | ogólne | Edukacja obywatelska | 7 | 31 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Technikum | ogólne | Fizyka | 11 | 94 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Technikum | ogólne | Geografia | 42 | 282 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Technikum | ogólne | Informatyka | 5 | 45 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Technikum | ogólne | Język angielski | 39 | 337 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |
| Technikum | ogólne | Język niemiecki | 39 | 337 | źródłowo śledzalne | działy i pozycje pochodzą z lokalnego PDF; progi ocen są opracowaniem |

## Najważniejsze ryzyka

1. Historia w technikum wymaga osobnej kontroli ręcznej. Skrypt wskazał 187 pozycji niedopasowanych literalnie po czyszczeniu ekstraktu. To może być efekt rozbudowanej struktury PDF, ale nie należy tego traktować jako gotowe bez recenzji nauczyciela historii.
2. Matematyka w technikum i BS II wymaga kontroli granicy zakresu podstawowego i rozszerzonego. Skrypt wskazuje po 14 pozycji niedopasowanych.
3. EDB w technikum i BS I oraz WF w BS I są ręcznie rekonstruowane. Treść może być merytorycznie zgodna z podstawą, ale nie jest literalnym ekstraktem z PDF.
4. W zawodowych pozycjach największe ryzyko po czyszczeniu ma Kelner: 9 kryteriów niedopasowanych literalnie. Pozostałe ryzyka zawodowe są punktowe.
5. Przypisanie pozycji do ocen pozostaje opracowaniem ZSZ5. Nie istnieje w podstawie programowej gotowy podział na oceny.

## Rekomendacja publikacyjna

Strona może pozostać jako robocza biblioteka i punkt startowy do pracy nauczycieli, ale nie powinna być opisana jako finalny, w pełni zatwierdzony zestaw wymagań. Bezpieczny opis to:

`Działy i pozycje zostały zbudowane na podstawie lokalnych PDF-ów podstaw programowych. Podział na oceny jest opracowaniem roboczym ZSZ5 i wymaga zatwierdzenia przez nauczycieli przed publikacją dla uczniów i rodziców.`
