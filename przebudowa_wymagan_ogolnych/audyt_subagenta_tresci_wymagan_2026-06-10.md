# Audyt subagenta: treści wymagań i oceny

Data: 2026-06-10.

Zakres: `wymagania_ogolne_ZSZ5_2026_2027.html` oraz `przebudowa_wymagan_ogolnych/raport_generowania_kompletnej_strony.md`.

## Wniosek

Strukturalnie strona ma komplet przedmiotów i działów: 40 przedmiotów i 512 działów. Nie wykryto przedmiotów z zerem działów ani pustych kolumn. Problemem jest jakość ekstrakcji i obronność części wymagań na oceny.

## Krytyczne

1. BSI / Edukacja dla bezpieczeństwa ma treść z innego przedmiotu.
   - W HTML znajdują się działy typu `Rodzina`, `Dojrzewanie`, `Seksualność człowieka`, `Życie jako fundamentalna wartość`.
   - Wygląda to jak WDŻ, nie EDB.
   - Naprawa: ponownie wyciągnąć właściwy zakres EDB BS I.

2. BSI / Wychowanie fizyczne jest sklejone z innymi podstawami.
   - W dziale I i kolejnych występują wtrącenia z biologii, informatyki, EDB i edukacji obywatelskiej.
   - Naprawa: zregenerować WF BSI z właściwego aktu Dz.U. 2025 poz. 1052.

3. Edukacja obywatelska i edukacja zdrowotna zawierają znaczniki tabel PDF jako treść.
   - Wymagania zawierają m.in. `X X X`, `Wymagania fakultatywne`, `Cele 1 2 3`.
   - Dotyczy technikum i BSI.
   - Naprawa: usunąć znaczniki tabel i oddzielić wymagania obowiązkowe od fakultatywnych.

4. Technikum / EDB ma sklejone poddziały i ucięte akty prawne.
   - Dział II miesza źródła promieniowania, ostrzeganie ludności i inne poddziały.
   - Dział IV zawiera oderwane fragmenty typu `655)`.
   - Naprawa: rozbić i oczyścić treść EDB, bez cytatów prawnych jako wymagań.

## Ważne

1. Podział na oceny jest w wielu miejscach nieobronny.
   - Algorytm rozdziela kolejne punkty podstawy między oceny, zamiast budować progi trudności.
   - Naprawa: dla problematycznych przedmiotów zastosować rubryki ocen: rozpoznaje / opisuje / stosuje / analizuje / projektuje.

2. Dużo generycznych kolumn ocen.
   - Szczególnie języki obce, geografia, historia i WF.
   - Naprawa: oznaczyć jako wymagające recenzji albo poprawić przed publikacją.

3. 134 tytuły działów wyglądają na ucięte.
   - Dotyczy głównie języków obcych, geografii, biznesu i zarządzania, plastyki, EDB.
   - Naprawa: odtworzyć tytuły z PDF albo skrócić redakcyjnie bez urywania składni.

4. Raport zbyt łatwo oznacza problemy jako `gotowe`.
   - Naprawa: zmienić statusy na `do recenzji` tam, gdzie treść wymaga czyszczenia.

## Drobne

- Artefakty spacji po ekstrakcji PDF, np. `języ ku`, `rozw oju`, `efek tywnego`, `spo rtu`.
- Numery stron w treści.
- Gramatyka liczników, np. `1 wymagań`.
- Mylące ścieżki źródeł dla WF.

## Priorytet napraw

1. BSI / EDB.
2. BSI / WF.
3. Edukacja obywatelska i edukacja zdrowotna.
4. Technikum / EDB.
5. Tytuły działów i generyczne kolumny ocen.

