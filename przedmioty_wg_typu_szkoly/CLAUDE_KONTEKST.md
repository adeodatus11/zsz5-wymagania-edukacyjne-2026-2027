# Kontekst do przeniesienia do Claude

Mam trzy pliki PDF z ramowymi / szkolnymi planami nauczania na rok szkolny 2025/2026:

- `ramówki/BSIst2025_2026.pdf` - Branżowa szkoła I stopnia
- `ramówki/BSIIst 2025_2026.pdf` - Branżowa szkoła II stopnia
- `ramówki/Tech2025_2026.pdf` - Technikum

Z tych dokumentow zostala przygotowana kompletna lista unikalnych przedmiotow dla kazdego typu szkoly. Listy sa w plikach:

- `00_wszystkie_przedmioty_wg_typu_szkoly.md` - plik zbiorczy
- `01_branzowa_szkola_i_stopnia.md` - Branżowa szkoła I stopnia
- `02_branzowa_szkola_ii_stopnia.md` - Branżowa szkoła II stopnia
- `03_technikum.md` - Technikum

Zasady ekstrakcji:

- Uwzgledniono pozycje z tabel `Przedmioty`.
- Przedmioty powtarzajace sie w wielu klasach lub zawodach wpisano tylko raz w ramach danego typu szkoly.
- Uwzgledniono przedmioty ogolne, zawodowe, zajecia z wychowawca, religie, edukacje zdrowotna, doradztwo zawodowe oraz pozycje zwiazane z godzinami dyrektorskimi, jezeli wystepowaly jako przedmiot.
- Nie uwzgledniono pozycji technicznych z sekcji `Podsumowanie`, takich jak `Ogolem`, `Minimalna liczba godzin ksztalcenia zawodowego`, `Ksztalcenie zawodowe teoretyczne`, `Ksztalcenie zawodowe praktyczne`, `Praktyka zawodowa (liczba tygodni)`.

Proponowane polecenie dla Claude:

```text
Na podstawie zalaczonych plikow Markdown opracuj uporzadkowana tabele przedmiotow wedlug typu szkoly. Zachowaj oryginalne nazwy przedmiotow. Nie dopisuj przedmiotow spoza listy. Jesli laczysz lub grupujesz przedmioty, wyraznie zaznacz, ze to klasyfikacja robocza, a nie nazwa z ramowego planu nauczania.
```
