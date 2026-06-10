# Audyt prawdziwości i researchu: `wymagania_ogolne_ZSZ5_2026_2027.html`

Data weryfikacji: 2026-06-09  
Rola: subagent B, audytor prawdziwości i researchu internetowego  
Zakres: przedmioty ogólnokształcące w pliku `wymagania_ogolne_ZSZ5_2026_2027.html`

## Wniosek główny

Strona w obecnej formie w dużej części wygląda jak automatyczne rozdzielenie wymagań szczegółowych z podstaw programowych na kolumny ocen, a nie jak merytorycznie opracowane wymagania edukacyjne na oceny.

Najważniejsze ustalenia:

- Treść wielu komórek faktycznie pochodzi z lokalnych PDF-ów podstaw programowych, więc źródłowo nie jest całkowicie zmyślona.
- Podział na oceny jest słaby merytorycznie: występują duplikaty między ocenami, puste kolumny, losowe przypisania trudności i brak zasady kumulatywnej.
- W pliku wykryto co najmniej 207 duplikatów tej samej treści w różnych kolumnach ocen w tym samym dziale.
- Wykryto liczne błędy sklejania tekstu po ekstrakcji z PDF, np. `przedstawia dializę niewydolności nerek. jako...`, `przez tlenu`, `reakcji; opisuje równania elektrochemiczną`.
- Technikum: `Wychowanie fizyczne` opiera się na starej podstawie 2018, nie na nowej podstawie WF dla LO/technikum/BS II z 2025 r.
- Pliki lokalne WF są myląco nazwane: plik w folderze technikum z `poz1052` jest aktem dla szkoły podstawowej/BS I, a plik w folderze BS I z `poz1035` jest aktem dla LO/technikum/BS II.
- W technikum nadal występuje `WDŻwR`, chociaż rozporządzenie z 6 marca 2025 r. dla LO/technikum/BS II uchyla część `Wychowanie do życia w rodzinie` i dodaje `Edukację zdrowotną`.

Moja rekomendacja: nie publikować obecnego HTML jako finalnych wymagań na oceny. Można go potraktować jako surowy indeks treści podstawy programowej, ale wymagania na oceny trzeba przebudować według modelu `konieczne / podstawowe / rozszerzające / dopełniające / wykraczające` albo według tabel z gotowych planów wynikowych.

## Wykorzystane lokalne skille

Użyłem lokalnych skilli:

- `truth-auditor` - do klasyfikacji ryzyk faktograficznych, aktualności podstaw i wiarygodności źródeł.
- `research-summarizer` - do uporządkowania źródeł internetowych i decyzji, które materiały nadają się do adaptacji.

## Zakres lokalnej strony

HTML zawiera następujące przedmioty:

| Typ szkoły | Przedmiot | Zakres w HTML |
|---|---:|---:|
| Technikum | Biologia | 4 działy, 89 wymagań |
| Technikum | Chemia | 22 działy, 153 wymagania |
| Technikum | EDB | 2 działy, 68 wymagań |
| Technikum | Edukacja obywatelska | 7 działów, 62 wymagania |
| Technikum | Edukacja zdrowotna | 8 działów, 46 wymagań |
| Technikum | Fizyka | 11 działów, 94 wymagania |
| Technikum | Geografia | 39 działów, 258 wymagań |
| Technikum | Historia | 32 działy, 471 wymagań |
| Technikum | Informatyka | 5 działów, 49 wymagań |
| Technikum | Język obcy nowożytny | 44 działy, 423 wymagania |
| Technikum | Język polski | 2 działy, 251 wymagań |
| Technikum | Matematyka | 11 działów, 121 wymagań |
| Technikum | Wiedza o społeczeństwie | 7 działów, 63 wymagania |
| Technikum | WDŻwR | 6 działów, 53 wymagania |
| Technikum | Wychowanie fizyczne | 4 działy, 45 wymagań |
| Branżowa Szkoła II stopnia | Informatyka | 5 działów, 14 wymagań |
| Branżowa Szkoła II stopnia | Język obcy nowożytny | 9 działów, 79 wymagań |
| Branżowa Szkoła II stopnia | Język polski | 4 działy, 103 wymagania |
| Branżowa Szkoła II stopnia | Matematyka | 12 działów, 54 wymagania |
| Branżowa Szkoła I stopnia (nowe) | Biznes i zarządzanie | 6 działów, 30 wymagań |
| Branżowa Szkoła I stopnia (nowe) | Edukacja obywatelska | 7 działów, 62 wymagania |
| Branżowa Szkoła I stopnia (nowe) | Edukacja zdrowotna | 10 działów, 63 wymagania |
| Branżowa Szkoła I stopnia (nowe) | Wychowanie fizyczne (nowe) | 9 działów, 41 wymagań |

## Próbki tabel z HTML

### Technikum, biologia, dział I

| Ocena | Próbka |
|---|---|
| Dopuszczająca | przedstawia znaczenie biologiczne makroelementów, w tym pierwiastków biogennych |
| Dostateczna | przedstawia znaczenie biologiczne makroelementów, w tym pierwiastków biogennych |
| Dobra | przedstawia budowę węglowodanów (...) ale tekst jest sklejony i miejscami nielogiczny |
| Bardzo dobra | pusta |
| Celująca | porównuje chemiczny strukturę |

Ocena: treść pochodzi z biologii, ale poziomowanie jest niewiarygodne. Ta sama treść pojawia się dla `Dopuszczająca` i `Dostateczna`, a `Celująca` jest gramatycznie uszkodzona.

### Technikum, chemia, dział IX

| Ocena | Próbka |
|---|---|
| Dopuszczająca | stosuje pojęcia: półogniwo, anoda, katoda, ogniwo galwaniczne... |
| Dobra | identyczne jak `Dopuszczająca` |
| Celująca | wyjaśnia przebieg korozji elektrochemicznej stali i żeliwa, pisze odpowiednie sposoby ochrony metali przed korozją reakcji; opisuje równania elektrochemiczną |

Ocena: widać zarówno duplikat między ocenami, jak i błędną składnię po ekstrakcji PDF.

### Technikum, matematyka, dział I

| Ocena | Próbka |
|---|---|
| Dopuszczająca | posługuje się pojęciem przedziału liczbowego, zaznacza przedziały na osi liczbowej |
| Dostateczna | przeprowadza proste dowody dotyczące podzielności liczb całkowitych... |
| Dobra | wykonuje działania w zbiorze liczb rzeczywistych |
| Bardzo dobra | wykorzystuje własności potęgowania i pierwiastkowania w sytuacjach praktycznych... |
| Celująca | stosuje związek logarytmowania z potęgowaniem... |

Ocena: to wygląda bliżej realnego stopniowania, ale nadal nie jest opisane jako układ kumulatywny `K/P/R/D/W`, a część wpisów jest sklejona.

### Technikum, edukacja obywatelska, dział I

| Ocena | Próbka |
|---|---|
| Dopuszczająca | wyjaśnia, czym jest patriotyzm... |
| Dostateczna | identyczne jak `Dopuszczająca` |
| Dobra | rozpoznaje przykłady ksenofobii, stereotypów... |
| Bardzo dobra | analizuje wpływ swoich codziennych wyborów... |
| Celująca | wyjaśnia obywatelski obowiązek obrony ojczyzny... |

Ocena: treść jest bliska podstawie 2025, ale samo przypisanie do ocen jest arbitralne i nie uwzględnia praktycznych działań obywatelskich oraz projektu jako integralnej części podstawy.

## Wyniki porównania z lokalnymi PDF-ami

Poniżej podaję odsetek komórek HTML, które dało się znaleźć jako znormalizowane frazy w lokalnym PDF-ie. Wysoki wynik oznacza źródłową zbieżność z podstawą programową, ale nie potwierdza poprawnego podziału na oceny.

| Typ szkoły | Przedmiot | Dopasowanie do lokalnego PDF | Wniosek |
|---|---:|---:|---|
| Technikum | Biologia | 77/92, 83,7% | Treść w większości z podstawy, ale są uszkodzenia i błędne poziomowanie. |
| Technikum | Chemia | 140/190, 73,7% | Treść częściowo z podstawy, dużo uszkodzeń i duplikatów. |
| Technikum | EDB | 65/70, 92,9% | Źródłowo blisko podstawy, ale wymaga dopracowania poziomów ocen. |
| Technikum | Edukacja obywatelska | 64/67, 95,5% | Źródłowo blisko Dz.U. 2025 poz. 382, ale brakuje sensownego modelu oceniania. |
| Technikum | Edukacja zdrowotna | 55/58, 94,8% | Źródłowo blisko podstawy, lecz wymagania na oceny są arbitralne. |
| Technikum | Fizyka | 81/109, 74,3% | Część treści uszkodzona przez ekstrakcję. |
| Technikum | Geografia | 252/302, 83,4% | Treść głównie źródłowa, ale podział na oceny i składnia wymagają korekty. |
| Technikum | Historia | 173/523, 33,1% | Największy problem: bardzo dużo sklejonych i niedopasowanych wpisów. |
| Technikum | Informatyka | 35/56, 62,5% | Część treści źródłowa, część wymaga ręcznego sprawdzenia. |
| Technikum | Język obcy nowożytny | 433/490, 88,4% | Wysoka zgodność, ale poziomy ocen nie wynikają wprost z podstawy. |
| Technikum | Język polski | 226/252, 89,7% | Treść głównie źródłowa, ale podział na tylko 2 działy jest mało użyteczny dla oceniania. |
| Technikum | Matematyka | 106/141, 75,2% | Częściowo nadaje się jako baza, wymaga przebudowy na poziomy K/P/R/D/W. |
| Technikum | Wiedza o społeczeństwie | 50/70, 71,4% | Trzeba rozstrzygnąć aktualność wobec edukacji obywatelskiej i ramówki. |
| Technikum | WDŻwR | 56/60, 93,3% | Źródłowo zgodne ze starym PDF, ale problem aktualności od 2025/2026. |
| Technikum | Wychowanie fizyczne | 40/50 względem starego PDF 2018; 0/50 względem nowego 2025 | Poważny problem aktualności. |
| BS II | Informatyka | 22/23, 95,7% | Źródłowo blisko PDF. |
| BS II | Język obcy nowożytny | 83/93, 89,2% | Źródłowo blisko PDF. |
| BS II | Język polski | 82/105, 78,1% | Treść częściowo źródłowa, sporo sklejonych fragmentów. |
| BS II | Matematyka | 56/78, 71,8% | Treść częściowo źródłowa, wymaga korekty. |
| BS I | Biznes i zarządzanie | 20/37, 54,1% | Ryzyko: wymagania i plik źródłowy wymagają ręcznego sprawdzenia w ISAP. |
| BS I | Edukacja obywatelska | 64/67, 95,5% | Źródłowo blisko nowej podstawy. |
| BS I | Edukacja zdrowotna | 80/80, 100% | Źródłowo blisko nowej podstawy. |
| BS I | Wychowanie fizyczne (nowe) | 57/57 względem lokalnego pliku `poz1035`, ale ten plik jest aktem dla LO/technikum/BS II | Prawdopodobnie użyto niewłaściwego aktu dla BS I. |

## Ryzyka merytoryczne w logice ocen

1. Brak zasady kumulatywnej.

W sprawdzonych gotowcach najczęściej występuje układ:

- ocena dopuszczająca = wymagania konieczne,
- ocena dostateczna = konieczne + podstawowe,
- ocena dobra = konieczne + podstawowe + rozszerzające,
- ocena bardzo dobra = poprzednie + dopełniające,
- ocena celująca = poprzednie + wykraczające / twórcze / problemowe.

W HTML część wymagań jest po prostu rozsypana po kolumnach, bez tej reguły.

2. Duplikaty między ocenami.

Przykłady:

- Biologia: identyczne wymaganie w `Dopuszczająca` i `Dostateczna`.
- Chemia: identyczne wymaganie w `Dopuszczająca` i `Dobra`.
- Edukacja obywatelska: identyczne wymaganie w `Dopuszczająca` i `Dostateczna`.
- Biznes i zarządzanie: identyczne wymaganie w `Dopuszczająca` i `Dobra`.

3. Kolumny są nierównomiernie wypełnione.

Przykłady skrajne:

- Historia, technikum: `Dostateczna` ma 367 wpisów, `Dobra` tylko 2.
- Język polski, technikum: `Dostateczna` ma 197 wpisów, `Celująca` tylko 2.
- Biologia, technikum: `Dostateczna` ma 60 wpisów, `Dobra` tylko 6.

To nie wygląda jak realny przedmiotowy system oceniania.

4. Część komórek to tekst źle przetworzony z PDF.

Przykłady:

- `przedstawia proces wchłaniania poszczególnych produktów składników pokarmowych...`
- `opisuje wymianę gazową... oraz i ułatwiające dyfuzję gazów przez tlenu...`
- `charakteryzuje cywilizacje europejskich w podziale Nowego Świata prekolumbijskie`
- `analizuje równania i nierówności ... liniowe z parametrami oraz` na końcu lub w środku zdania.

## Oficjalne źródła do dalszego porządkowania

| Źródło | Link | Co potwierdza | Wykorzystanie |
|---|---|---|---|
| ORE, podstawa programowa dla LO/technikum/BS II 2018 | https://ore.edu.pl/2018/03/podstawa-programowa-ksztalcenia-ogolnego-dla-liceum-technikum-i-branzowej-szkoly-ii-stopnia/ | ORE udostępnia PDF-y dla przedmiotów LO/technikum/BS II: m.in. geografia, historia, informatyka, język obcy, język polski, matematyka, WOS, WF. | Źródło bazowe do treści wymagań, nie do podziału na oceny. |
| Dziennik Ustaw 2018 poz. 467 | https://dziennikustaw.gov.pl/du/2018/467 | Rozporządzenie MEN z 30.01.2018 dla LO, technikum i BS II. | Źródło prawne nadrzędne dla podstaw 2018. |
| Dziennik Ustaw 2025 poz. 382 | https://dziennikustaw.gov.pl/du/2025/382 oraz PDF https://dziennikustaw.gov.pl/D2025000038201.pdf | Nowelizacja dla LO/technikum/BS II: dodaje edukację obywatelską i edukację zdrowotną, uchyla WDŻwR. | Konieczne do aktualizacji technikum i BS II. |
| Dziennik Ustaw 2025 poz. 378 | https://dziennikustaw.gov.pl/D2025000037801.pdf | Nowelizacja dla szkoły podstawowej i BS I: edukacja obywatelska i edukacja zdrowotna. | Konieczne do BS I. |
| Dziennik Ustaw 2025 poz. 1035 | https://dziennikustaw.gov.pl/D2025000103501.pdf | Nowa podstawa WF dla LO/technikum/BS II. | Konieczne do technikum i BS II WF. |
| Dziennik Ustaw 2025 poz. 1052 | https://dziennikustaw.gov.pl/D2025000105201.pdf | Nowa podstawa WF m.in. dla szkoły podstawowej i BS I. | Konieczne do BS I WF. |
| MEN, program nauczania edukacji zdrowotnej | https://www.gov.pl/web/edukacja/przykladowy-program-nauczania-edukacji-zdrowotnej | MEN udostępnia program dla BS I, LO i technikum. | Dobre jako wzorzec kolejności i metodyki, nie jako gotowa tabela ocen. |
| ORE, materiały edukacji obywatelskiej | https://ore.edu.pl/2025/02/edukacja-obywatelska-materialy-do-pobrania/ | Podstawa EO, komentarz metodyczny, materiały IBE. | Dobre do ustalenia specyfiki EO: wiedza, działania obywatelskie, projekt. |
| Ustawa o systemie oświaty, art. 44b | https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19910950425/U/D19910425Lj.pdf | Nauczyciele informują o wymaganiach niezbędnych do poszczególnych ocen, wynikających z programu nauczania; wymagania trzeba dostosowywać do potrzeb ucznia. | Podstawa prawna dla formy wymagań edukacyjnych. |

## Gotowce i przykłady do adaptacji

Legenda użyteczności:

- `Gotowe do adaptacji` - można wykorzystać strukturę i logikę po sprawdzeniu licencji/statutu szkoły i aktualności podstawy.
- `Tylko inspiracja` - przydatne jako wzorzec języka albo progów, ale nie do kopiowania treści.
- `Nieużyteczne dla treści` - może potwierdzać ogólne zasady, ale nie daje konkretnych wymagań na oceny.

| Źródło | Przedmiot | Typ szkoły | Ma podział na oceny? | Co można wykorzystać | Ryzyka | Ocena |
|---|---|---|---|---|---|---|
| Nowa Era / Gov.pl, `Rozkład materiału i plan wynikowy do edukacji obywatelskiej` https://www.gov.pl/attachment/284e1fbc-eeae-4521-85ca-b673fde929ee | Edukacja obywatelska | LO/technikum | Tak, plan wynikowy z poziomami ocen | Bardzo dobry wzorzec układu: wymagania podstawowe/fakultatywne, DZO, projekt, rekomendacje oceniania. | Copyright Nowa Era; nie kopiować hurtowo bez uprawnienia. | Gotowe do adaptacji strukturalnej |
| ZSMSC, edukacja obywatelska 2025 https://zsmsc.edu.pl/wp-content/uploads/Wymagania-edukacyjne-na-poszczegolne-oceny-do-przedmiotu-edukacja-obywatelska-dla-liceum-ogolnoksztalcacego-i-technikum.pdf | Edukacja obywatelska | LO/technikum | Tak: konieczne, podstawowe, rozszerzające, dopełniające, wykraczające | Dobry wzorzec tabeli ocen dla nowego przedmiotu. | Publiczny PDF szkoły, brak jasnej licencji. Używać jako inspiracji, nie kopiować 1:1. | Gotowe do adaptacji po przepisaniu |
| MEN, program nauczania edukacji zdrowotnej https://www.gov.pl/web/edukacja/przykladowy-program-nauczania-edukacji-zdrowotnej | Edukacja zdrowotna | BS I, LO, technikum | Nie jako tabela ocen | Kolejność działów, cele, metodyka, przykładowy program. | Nie zastępuje wymagań na oceny. | Tylko inspiracja metodyczna |
| LO1 Opole, edukacja zdrowotna https://lo1.opole.pl/wp-content/uploads/2025/09/Wymagania-edukacyjne_edukacja-zdrowotna.pdf | Edukacja zdrowotna | LO | Częściowo, ma progi i zasady | Progi ocen, formy aktywności, ocenianie projektu/aktywności. | Nie wystarczy do szczegółowych tabel działowych; brak jasnej licencji. | Tylko inspiracja |
| Nowa Era, biznes i zarządzanie kl. 1 https://dlanauczyciela.nowaera.pl/zasob/281992%2Cwymagania-edukacyjne-biznes-i-zarzadzanie-klasa-1.docx | Biznes i zarządzanie | prawdopodobnie szkoła ponadpodstawowa / BS I zależnie od zasobu | Tak, dokument `wymagania edukacyjne` | Potencjalnie najlepszy materiał wydawniczy do BiZ. | Copyright i dostęp nauczycielski; używać tylko zgodnie z licencją. | Gotowe do adaptacji, jeśli szkoła ma prawo użycia |
| Powiat Szczycieński, BiZ BS I https://m.powiatszczycienski.pl/2025/09/biz-wymagania-edukacyjne-bs-i-stopnia-86073.pdf | Biznes i zarządzanie | BS I | Tak: kolumny 1-5, oceny dopuszczająca-celująca | Bardzo dobry wzorzec dla BS I: skala kumulatywna kolumn. | Publiczny PDF, brak jasnej licencji; sprawdzić zgodność z programem używanym w ZSZ5. | Gotowe do adaptacji po przepisaniu |
| ZSM1 Kraków, BiZ BS I https://www.zsm1krakow.pl/images/Biznes_i_Zarz%C4%85dzanie-klasa-1-Es.pdf | Biznes i zarządzanie | BS I | Tak: konieczne-podstawowe-rozszerzające-dopełniające-wykraczające | Dobry model do przebudowy BiZ. | Publiczny materiał szkoły, nie kopiować bez zgody. | Gotowe do adaptacji strukturalnej |
| PZS1 Pszczyna, matematyka technikum https://pzs1.pszczyna.edu.pl/wp-content/uploads/2022/10/matematyka-PP-kl-2T.pdf | Matematyka | technikum | Tak: K/P/R/D/W | Wzorcowy model kumulatywny dla matematyki. | Materiał 2022; sprawdzić aktualność i podręcznik/program. | Gotowe do adaptacji strukturalnej |
| 4 LO Tarnów, matematyka https://4lo-tarnow.edu.pl/wp-content/uploads/2022/11/Wymagania_mat_kl3_podstawa_po_SP_zmiana.pdf | Matematyka | LO, zakres podstawowy | Tak | Jasny opis, że dopuszczająca = K, dostateczna = K+P itd. | LO, nie technikum/BS; treści klasowe mogą się różnić. | Tylko inspiracja |
| Technikuminformatyczne.edu.pl, chemia kl. 1 PP https://technikuminformatyczne.edu.pl/wp-content/uploads/2024/11/9_1_wymagania-edukacyjne-chemia-%E2%80%94-kl1PP.pdf | Chemia | technikum | Tak: oceny w tabeli działowej | Dobry wzorzec szczegółowej tabeli na oceny. | Materiał może być oparty na podręczniku/wydawnictwie; prawa autorskie. | Gotowe do adaptacji po przepisaniu |
| Maczek Katowice, chemia https://maczek.edu.pl/static/upload/store/2025_26_wice/wymagania_edukacyjne/Wymagania_edukacyjne_i_PSO_chemia_-_poprawiony_%281%29.pdf | Chemia | LO | Ma progi i ogólne wymagania | Dobre progi i ogólny PSO. | Nie daje pełnej tabeli działowej dla ZSZ5; LO. | Tylko inspiracja |
| 4 LO Tarnów, biologia https://4lo-tarnow.edu.pl/wp-content/uploads/2024/09/Biologia-1DA-zakres-rozszerzony.pdf | Biologia | LO/technikum, rozszerzenie | Tak | Dobry przykład, jak opisać wymagania z hierarchią Blooma. | Zakres rozszerzony i LO; nie kopiować treści. | Tylko inspiracja |
| Slowacki.edu.pl, geografia kl. 1 https://slowacki.edu.pl/wp-content/uploads/2024/09/Wymagania-edukacyjne-oblicza-geografii-1-zakres-podstawowy.pdf | Geografia | LO/technikum, zakres podstawowy | Tak: konieczne-podstawowe-rozszerzające-dopełniające-wykraczające | Bardzo dobry wzorzec tabelaryczny. | Związane z podręcznikiem Nowa Era; prawa autorskie. | Gotowe do adaptacji strukturalnej |
| 4 LO Tarnów, geografia ZP https://4lo-tarnow.edu.pl/wp-content/uploads/2024/10/WYMAGANIA-EDUKACYJNE-1-3-ZP.pdf | Geografia | LO, zakres podstawowy | Tak | Przykład agregacji klas 1-3 i tabel ocen. | LO; nie kopiować dosłownie. | Tylko inspiracja |
| Technikuminformatyczne.edu.pl, fizyka https://technikuminformatyczne.edu.pl/wp-content/uploads/2024/11/11_Wymagania-edukacyjne-FIZYKA-dla-kl.-2.pdf | Fizyka | technikum | Tak | Przykład wymagań na oceny i opisu celującej jako ponad bardzo dobrą/problemową. | Materiał prawdopodobnie wydawniczy; sprawdzić podstawę i program. | Gotowe do adaptacji strukturalnej |
| Plater.edu.pl, informatyka kl. 1 https://plater.edu.pl/liceum/wp-content/uploads/2024/09/Wymagania_informatyka_Klasa_1.pdf | Informatyka | LO/technikum, zakres podstawowy | Tak: pięć kolumn ocen | Dobry wzorzec na działowe poziomowanie umiejętności praktycznych. | Publiczny PDF, brak jasnej licencji. | Gotowe do adaptacji po przepisaniu |
| ZSMSC, informatyka https://zsmsc.edu.pl/wp-content/uploads/Wymagania-edukacyjne-na-poszczeg%C3%B3lne-oceny-dla-liceum-i-technikum.-Informatyka-na-czasie.-Zakres-podstawowy.-Cz%C4%99%C5%9B%C4%87-1.pdf | Informatyka | LO/technikum | Tak | Przydatny wzór działowy dla informatyki. | Zależne od podręcznika `Informatyka na czasie`; prawa autorskie. | Gotowe do adaptacji strukturalnej |
| ZSTiB Brzesko, WF technikum https://zstib.edu.pl/upload/files/d9487/wymagania-edukacyjne-technikum-3.pdf | Wychowanie fizyczne | technikum | Tak: wymaganie z podstawy + oceny | Bardzo dobry model dla WF, bo rozbija wymaganie źródłowe na poziomy wykonania. | Materiał na starej podstawie; trzeba dostosować do WF 2025. | Tylko inspiracja |
| ZSTiB Brzesko, WF BS I https://zstib.edu.pl/upload/files/d10125/wymagania-edukacyjne-branzowa-1.pdf | Wychowanie fizyczne | BS I | Tak | Model dla BS I: wymaganie z podstawy + stopniowanie. | Materiał stary; dopasować do Dz.U. 2025 poz. 1052. | Tylko inspiracja |
| PZS1 Pszczyna, EDB https://pzs1.pszczyna.edu.pl/wp-content/uploads/2022/10/edb.pdf | Edukacja dla bezpieczeństwa | szkoła ponadpodstawowa | Tak | Dobry przykład ogólnych wymagań i celującej jako ponad bardzo dobrą. | Stara wersja; sprawdzić program i aktualność. | Tylko inspiracja |
| ZSTiB Brzesko, język angielski https://zstib.edu.pl/upload/files/d21710/jezyk-angielski.pdf | Język obcy | technikum/BS | Tak | Dobre szczegółowe kryteria dla sprawności językowych: mówienie, pisanie, słuchanie, czytanie. | Trzeba dostosować do poziomów ESOKJ i języka nauczanego w ZSZ5. | Gotowe do adaptacji strukturalnej |
| Energetyk, język angielski technikum https://energetyk.edu.pl/wp-content/uploads/2022/10/PZO-Jezyk-angielski-TE-20222023.pdf | Język angielski | technikum | Tak | Przydatne opisy poziomów ocen w sprawnościach językowych. | Stare, szkolne, brak jasnej licencji. | Tylko inspiracja |
| ZSMK, historia technikum https://zsmk.edu.pl/images/PZO/PZO_historia_poziom_podstawowy__Liceum_Og%C3%B3lnokszta%C5%82c%C4%85ce_i_Technikum.pdf | Historia | LO/technikum | Częściowo: progi i PZO | Przydatne progi, zasady, ogólne kryteria. | Nie zastąpi szczegółowych wymagań działowych. | Tylko inspiracja |
| Mościcki, WOS kl. 5 https://moscicki.edu.pl/wp-content/uploads/2024/06/WOS-klasy-5.pdf | WOS | technikum/LO | Tak | Przykład tabeli temat - oceny dla WOS. | WOS wygaszany/zastępowany w części przez edukację obywatelską; sprawdzić ramówkę ZSZ5. | Tylko inspiracja |

## Ocena legalna wykorzystania gotowców

Nie jest to porada prawna, ale praktyczna ocena ryzyka:

1. Oficjalne akty prawne i strony MEN/ORE można wykorzystywać jako źródło podstawy programowej i linkować. Przy cytowaniu dużych fragmentów lepiej zachować umiar i podać źródło.
2. Materiały wydawnictw, np. Nowa Era, są zwykle chronione prawem autorskim. Można korzystać z nich zgodnie z licencją szkoły/nauczyciela, ale nie należy publikować hurtowo przerobionych lub skopiowanych tabel bez sprawdzenia uprawnień.
3. Publiczne PDF-y innych szkół są dobre jako benchmark i inspiracja. Brak wyraźnej licencji oznacza, że bezpieczniej przepisać logikę własnymi słowami, dostosować do programu ZSZ5 i nie kopiować pełnych tabel.
4. Najbezpieczniejsza ścieżka: użyć oficjalnej podstawy programowej jako źródła treści, a gotowców jako wzorca struktury oceniania i języka operacyjnego.

## Rekomendowany model przebudowy

1. Najpierw uporządkować podstawy:

- technikum i BS II: sprawdzić aktualność wobec Dz.U. 2018 poz. 467 z późniejszymi zmianami, Dz.U. 2025 poz. 382 i Dz.U. 2025 poz. 1035,
- BS I: sprawdzić Dz.U. 2017 poz. 356 z późniejszymi zmianami, Dz.U. 2025 poz. 378 i Dz.U. 2025 poz. 1052,
- usunąć lub oznaczyć historycznie `WDŻwR` w technikum, jeśli strona ma obowiązywać w roku 2026/2027,
- poprawić lokalne pliki WF lub co najmniej ich nazwy/opisy.

2. Dla każdego przedmiotu przyjąć jedną tabelę poziomów:

- `Dopuszczająca`: wymagania konieczne, proste, odtwórcze, z pomocą nauczyciela.
- `Dostateczna`: konieczne + podstawowe, typowe zadania, podstawowe pojęcia.
- `Dobra`: samodzielne stosowanie wiedzy w typowych i częściowo problemowych sytuacjach.
- `Bardzo dobra`: analiza, uzasadnianie, łączenie informacji, samodzielność.
- `Celująca`: wymagania wykraczające albo twórcze/problemowe, projektowe, konkursowe, pogłębione; nie jako losowy trudniejszy punkt z podstawy.

3. Dla nowych przedmiotów:

- Edukacja obywatelska: uwzględnić projekt edukacyjny i cztery działania obywatelskie, bo wynika to z podstawy 2025.
- Edukacja zdrowotna: nie robić wyłącznie testowej tabeli wiedzy; uwzględnić analizę źródeł, decyzje zdrowotne, postawy i działania prozdrowotne.
- WF: oceniać przede wszystkim postęp, aktywność, wiedzę o zdrowiu i umiejętność planowania aktywności, nie tylko wyniki testów sprawnościowych.

## Priorytet napraw

| Priorytet | Co poprawić | Dlaczego |
|---|---|---|
| P0 | WF: rozdzielić właściwe akty `1035` i `1052`; poprawić technikum i BS I | Obecnie jest ryzyko użycia niewłaściwej podstawy. |
| P0 | Technikum: rozstrzygnąć `WDŻwR` vs `Edukacja zdrowotna` | Dz.U. 2025 poz. 382 uchyla WDŻwR i dodaje EZ dla LO/technikum/BS II. |
| P1 | Usunąć automatyczne duplikaty między ocenami | Duplikaty unieważniają sens tabel ocen. |
| P1 | Naprawić uszkodzone zdania po ekstrakcji PDF | Obecne teksty są miejscami nieczytelne dla ucznia i rodzica. |
| P1 | Historia, język polski, język obcy: przebudować układ działów | Obecny rozkład kolumn jest szczególnie nierówny. |
| P2 | Dodać źródło/podstawę przy każdym przedmiocie | Ułatwi audyt i obronę dokumentu. |
| P2 | Dodać informację o programie nauczania/podręczniku | Wymagania edukacyjne powinny wynikać z programu realizowanego przez nauczyciela, nie tylko z podstawy. |

## Decyzja końcowa

Obecny HTML jest przydatny jako surowa baza treści podstaw programowych, ale nie jest jeszcze wiarygodnym dokumentem wymagań edukacyjnych na oceny. Do dopracowania strony można legalnie i merytorycznie wykorzystać:

- oficjalne podstawy MEN/ORE/ISAP jako źródło treści,
- gotowce szkół i wydawnictw jako wzorzec struktury,
- szczególnie modele `K/P/R/D/W` i tabele działowe z pięcioma kolumnami ocen.

Nie rekomenduję kopiowania gotowych tabel z innych szkół lub wydawnictw 1:1. Najbezpieczniejszy wariant to własna adaptacja: ta sama logika stopniowania, własny opis, aktualna podstawa, program nauczania ZSZ5 i krótkie źródło przy każdym przedmiocie.
