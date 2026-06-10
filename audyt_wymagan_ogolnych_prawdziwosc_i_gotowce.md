# Audyt prawdziwosci wymagan edukacyjnych i research gotowcow

Data weryfikacji: 2026-06-09.

Plik audytowany: `wymagania_ogolne_ZSZ5_2026_2027.html`

Zakres: przedmioty ogolnoksztalcace w technikum, branzowej szkole II stopnia i branzowej szkole I stopnia, ze szczegolnym naciskiem na to, czy tabele `Dopuszczajaca / Dostateczna / Dobra / Bardzo dobra / Celujaca` sa prawdziwe, realne i oparte na zrodlach.

## Wniosek glowny

Obecnej strony nie nalezy traktowac jako gotowych, rzetelnych wymagan edukacyjnych na poszczegolne oceny.

Powody:

1. Oficjalna podstawa programowa potwierdza dzialy i wymagania szczegolowe, ale co do zasady nie przypisuje ich do ocen `dopuszczajaca`, `dostateczna`, `dobra`, `bardzo dobra`, `celujaca`.
2. W wielu tabelach HTML widac mechaniczne rozrzucenie wymagan z podstawy programowej po kolumnach ocen. Nie ma lokalnego zrodla, ktore potwierdza, ze dane wymaganie ma byc akurat na ocene dopuszczajaca albo dobra.
3. Strona ma braki w dzialach oraz bledy strukturalne potwierdzone lokalnymi PDF-ami i oficjalnymi zrodlami.
4. W wielu miejscach wystepuja powtorzenia tej samej tresci w kilku kolumnach ocen, co przeczy idei stopniowania trudnosci. Niezalezny subagent wykryl co najmniej 207 duplikatow tej samej tresci w roznych kolumnach ocen w tym samym dziale; moj lokalny, prostszy skrypt wykryl 178 takich przypadkow.
5. W pliku widac bledy po ekstrakcji PDF: uszkodzone zdania, przestawione fragmenty, puste kolumny i wpisy w niewlasciwych poziomach ocen.

## Podstawa prawna i metodyczna

### Co wynika z przepisow

Rozporzadzenie MEN z 22 lutego 2019 r. w sprawie oceniania, klasyfikowania i promowania uczniow i sluchaczy w szkolach publicznych, tekst jednolity Dz.U. 2023 poz. 2572, potwierdza skale ocen od 1 do 6 oraz wskazuje, ze wymagania edukacyjne dostosowuje sie do indywidualnych potrzeb ucznia. Zrodlo: Dziennik Ustaw, Dz.U. 2023 poz. 2572, plik PDF: https://dziennikustaw.gov.pl/DU/2023/2572/D2023000257201.pdf

Istotne dla strony:

- oceny pozytywne to: celujacy, bardzo dobry, dobry, dostateczny, dopuszczajacy;
- samo rozporzadzenie nie daje gotowych tabel dla kazdego przedmiotu i dzialu;
- przy WF, plastyce, muzyce i technice nalezy szczegolnie brac pod uwage wysilek ucznia, a przy WF takze systematycznosc i aktywnosc.

### Co wynika z podstawy programowej

ORE publikuje podstawe programowa dla liceum, technikum i branzowej szkoly II stopnia z osobnymi PDF-ami dla przedmiotow, m.in. biologii, chemii, EDB, fizyki, geografii, informatyki, jezyka obcego, jezyka polskiego, matematyki, plastyki, WOS, WDZ i WF. Zrodlo: https://ore.edu.pl/2018/03/podstawa-programowa-ksztalcenia-ogolnego-dla-liceum-technikum-i-branzowej-szkoly-ii-stopnia/

Nowelizacja podstawy programowej z 2024 r. zmienia podstawe dla liceum i technikum. Zrodlo: Dz.U. 2024 poz. 1019, PDF: https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU20240001019/O/D20241019.pdf

Dla edukacji obywatelskiej i edukacji zdrowotnej obowiazuja nowe przepisy od roku szkolnego 2025/2026. MEN wskazuje, ze edukacja zdrowotna ma dzialy: Wartosci i postawy, Zdrowie fizyczne, Aktywnosc fizyczna, Odzywianie, Zdrowie psychiczne, Zdrowie spoleczne, Dojrzewanie tylko w SP, Zdrowie seksualne, Zdrowie srodowiskowe, Internet i profilaktyka uzaleznien, System ochrony zdrowia tylko w szkolach ponadpodstawowych. Zrodlo MEN: https://www.gov.pl/web/edukacja/podstawy-programowe-do-przedmiotow-edukacja-obywatelska-i-edukacja-zdrowotna-podpisane-przez-minister-edukacji

Rozporzadzenie z 6 marca 2025 r. potwierdza m.in. szczegolna strukture dzialu I edukacji zdrowotnej, ktory ma charakter wartosci i postaw, a nie zwyklej listy konkretnych umiejetnosci. Zrodlo: Dz.U. 2025 poz. 378, PDF: https://dziennikustaw.gov.pl/D2025000037801.pdf

Niezalezny subagent wskazal tez na koniecznosc uwzglednienia:

- Dz.U. 2025 poz. 382 dla LO/technikum/BS II: edukacja obywatelska i edukacja zdrowotna oraz uchylenie WDZ w tej podstawie, zrodlo: https://dziennikustaw.gov.pl/du/2025/382
- Dz.U. 2025 poz. 1035 jako nowej podstawy WF dla LO/technikum/BS II, zrodlo: https://dziennikustaw.gov.pl/D2025000103501.pdf
- Dz.U. 2025 poz. 1052 jako nowej podstawy WF m.in. dla szkoly podstawowej i BS I, zrodlo: https://dziennikustaw.gov.pl/D2025000105201.pdf

Wazne: lokalne pliki WF wygladaja na mylaco opisane. Subagent wskazal, ze plik w folderze technikum z `poz1052` dotyczy podstawy dla SP/BS I, a plik w folderze BS I z `poz1035` dotyczy LO/technikum/BS II. Przed generowaniem nowych wymagan trzeba to poprawic albo przynajmniej opisac w katalogu zrodel.

## Audyt obecnej strony

### Krytyczne problemy

| Obszar | Status | Dlaczego to problem | Zalecenie |
|---|---|---|---|
| Podzial wymagan na oceny | Niepotwierdzony | Podstawa programowa daje wymagania, ale nie mowi, ze dane wymaganie jest np. na ocene dobra. | Opracowac model K/P/R/D/W albo podstawowe/ponadpodstawowe i dopiero na nim zbudowac oceny. |
| Komplet dzialow | Niekompletny | Sa przedmioty z brakujacymi dzialami, np. biologia, EDB, edukacja zdrowotna, jezyk polski, matematyka, historia. | Najpierw uzupelnic wszystkie dzialy z podstawy programowej. |
| Powtorzenia w kolumnach ocen | Wysokie ryzyko | Analiza HTML wykazala 178 wierszy, w ktorych identyczna niepusta tresc pojawia sie w kilku kolumnach ocen. | Traktowac obecny podzial jako roboczy, nie jako finalne wymagania. |
| Przedmioty z planow bez pelnego pokrycia | Niekompletne | Czesci przedmiotow z ramowych planow nie ma na stronie albo nie ma dla nich pelnych lokalnych PDF-ow. | Dla kazdego typu szkoly zrobic macierz: przedmiot z planu -> podstawa -> wymagania -> status. |
| WF i edukacja zdrowotna | Wymagaja innego podejscia | WF powinien uwzgledniac wysilek, systematycznosc i aktywnosc. Edukacja zdrowotna ma dzial wartosci/postaw o innej strukturze. | Nie generowac ich tak samo jak matematyki czy chemii. |
| WDZ w technikum | Prawdopodobnie nieaktualne dla 2026/2027 | Nowelizacja dla LO/technikum/BS II z 2025 r. uchyla WDZ i dodaje edukacje zdrowotna. | Usunac z finalnej strony albo przeniesc do sekcji archiwalnej po potwierdzeniu ramowki. |
| Lokalna baza PDF WF | Ryzyko pomylenia podstaw | Pliki `poz1035` i `poz1052` sa najprawdopodobniej przypisane do zlych folderow szkol. | Zweryfikowac nazwy i przypisania przed odbudowa WF. |

### Braki potwierdzone wczesniejszym audytem subagenta

- Technikum / Biologia: strona ma tylko I, III, V, VII; lokalny PDF potwierdza tez II, IV, VI, VIII, IX, X, XI.
- Technikum / EDB: strona ma I i IV; brakuje II Przygotowanie do dzialan ratowniczych oraz III Podstawy pierwszej pomocy.
- Technikum / Edukacja zdrowotna: brakuje I Wartosci i postawy oraz VIII Zdrowie srodowiskowe.
- Technikum / Jezyk polski: strona ma tylko II i IV; brakuje I Ksztalcenie literackie i kulturowe oraz III Tworzenie wypowiedzi.
- Technikum / Matematyka: brakuje osobnych dzialow VIII Planimetria oraz XIII Optymalizacja i rachunek rozniczkowy.
- Technikum / Wychowanie fizyczne 2018: brakuje V Kompetencje spoleczne.
- Technikum / Wychowanie fizyczne: wiekszym problemem niz brak dzialu V jest aktualnosc; finalna wersja powinna bazowac na Dz.U. 2025 poz. 1035, nie na starej podstawie 2018.
- Technikum / Historia: strona ma 32 dzialy, ale lokalny PDF potwierdza znacznie szerszy uklad, w tym brak czesci dzialow od XIII wzwyz oraz duzego bloku pozniejszej historii.
- BS II / Matematyka: strona ma I-XII; lokalny PDF potwierdza tez XIII Optymalizacja.
- BS I / Edukacja zdrowotna: brakuje I Wartosci i postawy, a dodatkowo wystepuje duplikat dzialu II.
- BS I / Wychowanie fizyczne: trzeba sprawdzic wzgledem Dz.U. 2025 poz. 1052, bo lokalny HTML i nazwy PDF-ow moga bazowac na niewlasciwie przypisanym akcie.

## Ocena realnosci obecnych tabel ocen

Obecne tabele maja pozor konkretu, ale nie sa wystarczajaco wiarygodne.

Wymagania na oceny powinny miec progresje:

- dopuszczajaca: minimum konieczne, proste czynnosci, czesto z pomoca nauczyciela;
- dostateczna: wymagania podstawowe, typowe zadania, rozumienie podstawowych pojec;
- dobra: samodzielne stosowanie wiedzy w typowych sytuacjach;
- bardzo dobra: pelny zakres, sprawne stosowanie, analiza, uzasadnianie, problemy nietypowe;
- celujaca: tworcze zastosowanie, samodzielnosc, zadania wykraczajace, konkursy/projekty lub bardzo wysoki poziom.

Takie podejscie potwierdzaja publiczne opracowania metodyczne i szkolne, np. material ORE z propozycja zaleznosci ocen od poziomow wymagan P/PP oraz szkolne PZO z biologii, fizyki, historii i innych przedmiotow.

## Znalezione gotowce i wzorce

### Zrodla metodyczne ogolne

| Zrodlo | Typ | Co daje | Ocena przydatnosci |
|---|---|---|---|
| ORE / material programowy z poziomami P i PP: https://zasobyip2.ore.edu.pl/pl/publications/download/2644 | material metodyczny | Model: dopuszczajaca 50-74% P, dostateczna 75-100% P, dobra 75-100% P + 50-74% PP, bardzo dobra 75-100% P i PP, celujaca za wymagania wykraczajace. | Bardzo dobry model bazowy do algorytmu oceniania. |
| Edurada, formulowanie wymagan: https://edurada.pl/formulowanie-wymagan-edukacyjnych-jak-to-zrobic/ | opracowanie eksperckie | Model K/P/R/D/W: konieczne, podstawowe, rozszerzajace, dopelniajace, wykraczajace. | Dobre jako model roboczy, ale nie jest zrodlem prawa. |
| ZS8 Szczecin, wymagania technikum: https://zs8.szczecin.pl/wp-content/uploads/2019/09/klasa3-wymagania-na-ocen%C4%99-poz-podst-4-letnie-technikum.pdf | szkolny gotowiec | Jawnie laczy K/P/R/D/W z ocenami 2-6. | Przydatne jako wzorzec struktury tabeli. |

### Przedmioty ogolnoksztalcace

| Przedmiot | Przykladowe zrodlo | Czy ma podzial na oceny? | Przydatnosc |
|---|---|---|---|
| Jezyk polski | LO Dabrowa Tarnowska, wymagania kl. 3: https://lo-dabrowa-tarnowska.pl/wp-content/uploads/2025/09/Jezyk-polski-kl3-podstawa-wymagania-edukacyjne.pdf | Tak, opisowo wedlug zakresow podstawy. | Dobre do odbudowy brakujacych dzialow I i III, po dopasowaniu do klas ZSZ5. |
| Jezyk polski | Sobieski Krakow, poziom rozszerzony: https://www.sobieski.krakow.pl/wp-content/uploads/2024/11/Wymagania-edukacyjne-na-poszczegolne-oceny-poziom-rozszerzony-z-zalaczona-podstawa-programowa-2.pdf | Tak, tabela Dopuszczajacy-Celujacy. | Dobre jako wzorzec formatu, ostroznie z zakresem rozszerzonym. |
| Biologia | VI LO Bydgoszcz PZO: https://dokumenty.vilo.bydgoszcz.pl/oszkole/PrzedmiotoweZasadyOceniania/biologia.pdf | Tak, raczej ogolne kryteria, nie kazdy dzial. | Dobre do modelu ocen, niewystarczajace do pelnych dzialow. |
| Chemia | ORE, program `Wszechobecna chemia`: https://ore.edu.pl/wp-content/uploads/phocadownload/EFS/chemia-poziom-podstawowyiv-etap.pdf | Tak, miejscami lekcja/dzial i oceny. | Przydatne jako wzorzec, ale stare i wymaga aktualizacji do obecnej podstawy. |
| Chemia | TL Krakow: https://tl.krakow.pl/semantic.upload/dokumenty_szkoly/CHEMIAwymagania_edukacyjne.pdf | Tak, ogolne wymagania na oceny. | Dobre jako opis kryteriow, nie jako komplet dzialow. |
| Fizyka | Liceum Dubois, kl. 2: https://liceumdubois.pl/wp-content/uploads/2024/09/Fizyka_wymagania-edukacyjne_zakres-podstawowy-kl.2_2024.pdf | Tak, opisuje poziomy trudnosci i konkretne wymagania. | Dobry wzorzec sposobu stopniowania. |
| Geografia | ZSP Piaski, technikum: https://zspiaski.pl/download/2025WE/T/T_WE_Geografia.pdf | Tak, ocena-wymagania. | Bardzo przydatne, bo dotyczy technikum i jest aktualne. |
| EDB | LO Piotrkow, Nowa Era: https://liceum2.piotrkow.pl/content/files/wymagania-edukacyjne-edb-1725617218.pdf | Tak, lekcja i oceny 2-6. | Bardzo przydatne do uzupelnienia EDB, ale trzeba sprawdzic zgodnosc z aktualna podstawa i programem. |
| EDB | ZSMSC: https://zsmsc.edu.pl/wp-content/uploads/Wymagania-edukacyjne-z-edukacji-dla-bezpiecze%C5%84stwa.pdf | Tak, dzialy i kumulacyjny model [1], [1+2] itd. | Bardzo dobry wzorzec kumulacyjny. |
| Informatyka | CKZiU Zory: https://www.ckziuzory.pl/userfiles/upload/files/wymagania__informatyka__d.popek.pdf | Tak, kryteria i progi. | Przydatne jako model ogolny, nie pelna mapa dzialow. |
| Historia | LO Kolbuszowa: https://lokolbuszowa.edupage.org/files/PSO_historia.pdf | Tak, kryteria ogolne dla odpowiedzi. | Przydatne jako model oceny wypowiedzi, nie jako komplet dzialow historii. |
| WOS | ZSB Brzeg: https://zsbbrzeg.pl/files/318/pzo-wostechnikum-1.pdf | Tak, PZO i progi procentowe. | Przydatne do zasad oceniania, nie wystarcza do dzialow. |
| Biznes i zarzadzanie | Elektronik: https://elektronik.edu.pl/images/do_pobrania/przed_sys_ocen/biznes_i_zarz%C4%85dzanie_wymagania_edukacyjne.pdf | Tak, szczegolowe kryteria dla klas I-II. | Bardzo przydatne dla BSI/technikum, wymaga dopasowania do ZSZ5. |
| Edukacja zdrowotna | LO1 Opole: https://lo1.opole.pl/wp-content/uploads/2025/09/Wymagania-edukacyjne_edukacja-zdrowotna.pdf | Sa progi procentowe, mniej konkretow dzialowych. | Przydatne tylko pomocniczo; podzial dzialow brac z MEN/Dz.U. |
| Wychowanie fizyczne | ZSW Sucha, WF 4HT 2025: https://zswsucha.pl/wymagania/pliki/4HT/WF_4HT_gr_1.pdf | Tak, dzial, umiejetnosc i oceny. | Bardzo przydatne jako aktualny wzorzec dla technikum, ale wymaga lokalnego dopasowania. |

### Dodatkowy raport subagenta

Niezalezny research subagenta B zostal zapisany w pliku:

`audyt_wymagan_ogolnych_research_subagent.md`

Ten plik zawiera szersza tabele gotowcow, m.in. dla edukacji obywatelskiej, biznesu i zarzadzania, matematyki, chemii, geografii, fizyki, informatyki, WF, EDB, jezyka angielskiego, historii i WOS. Wskazuje tez dopasowanie tresci HTML do lokalnych PDF-ow dla poszczegolnych przedmiotow.

## Ryzyka prawne i praktyczne przy korzystaniu z gotowcow

1. Gotowce ze stron szkol sa materialami publicznie dostepnymi, ale nie oznacza to automatycznie prawa do kopiowania calych tabel 1:1.
2. Bezpieczne podejscie: wykorzystac je jako wzorzec struktury, jezyk czynnosci ucznia i poziomowanie trudnosci, a finalne wymagania opracowac lokalnie dla ZSZ5.
3. Najbardziej obronne zrodla do merytoryki to: Dziennik Ustaw, ISAP, MEN, ORE i lokalne PDF-y podstaw programowych.
4. Gotowce szkolne i wydawnicze powinny miec status `material pomocniczy`, nie `zrodlo podstawy programowej`.

## Rekomendowany model naprawy strony

### Krok 1: macierz zrodel

Dla kazdego przedmiotu i typu szkoly utworzyc rekord:

| Typ szkoly | Przedmiot | Czy jest w planie | Zrodlo podstawy | Czy jest na stronie | Status dzialow | Status ocen |
|---|---|---|---|---|---|---|

### Krok 2: komplet dzialow

Najpierw uzupelnic wszystkie dzialy z podstawy programowej. Bez tego nie ma sensu dopracowywac ocen.

### Krok 3: wybrac model ocen

Najbezpieczniejszy model:

- Dopuszczajaca = wymagania konieczne / minimum niezbedne do dalszej nauki.
- Dostateczna = wymagania podstawowe.
- Dobra = wymagania rozszerzajace / samodzielne zastosowanie w typowych sytuacjach.
- Bardzo dobra = wymagania dopelniajace / pelny zakres, analiza, uzasadnienie, nietypowe sytuacje.
- Celujaca = wymagania wykraczajace lub tworcze zastosowanie, projekty, konkursy, samodzielne rozwiazania.

Alternatywnie dla przedmiotow scislych mozna stosowac model P/PP:

- dopuszczajaca: czesc wymagan podstawowych;
- dostateczna: pelne wymagania podstawowe;
- dobra: podstawowe + czesc ponadpodstawowych;
- bardzo dobra: podstawowe + pelne ponadpodstawowe;
- celujaca: ponadprogramowe/tworcze/konkursowe.

### Krok 4: odbudowac tabele

Dla kazdego dzialu tabela powinna zawierac:

- nazwe dzialu z podstawy;
- zrodlo: lokalny PDF / Dz.U. / ORE;
- wymagania na oceny napisane jako czynnosci ucznia;
- znacznik: `opracowanie ZSZ5 na podstawie podstawy programowej`, nie `cytat z podstawy`.

### Krok 5: recenzja nauczycielska

Automatyczne wygenerowanie tabel moze dac szkic, ale finalna wersja powinna byc zatwierdzona przez nauczyciela przedmiotu, bo przypisanie wymagan do ocen jest decyzja dydaktyczna w ramach oceniania wewnatrzszkolnego.

## Decyzja audytowa

Obecny HTML:

- moze sluzyc jako baza techniczna UI;
- nie powinien byc publikowany jako finalne wymagania edukacyjne;
- wymaga przebudowy merytorycznej przed uzupelnianiem brakujacych dzialow;
- wymaga oznaczenia zrodel przy kazdym przedmiocie;
- wymaga osobnego traktowania WF, edukacji zdrowotnej, jezykow obcych i historii.

## Kolejny praktyczny krok

Najrozsadniej przygotowac teraz plik roboczy `model_wymagan_na_oceny_ZSZ5.md` oraz osobne pliki z tabelami dla przedmiotow, zaczynajac od tych, dla ktorych sa najlepsze gotowce:

1. EDB
2. WF
3. Geografia
4. Biznes i zarzadzanie
5. Jezyk polski
6. Matematyka
7. Biologia / Chemia / Fizyka

Po zatwierdzeniu modelu mozna dopiero wygenerowac nowa wersje HTML.
