from __future__ import annotations

import html
import math
import re
import shutil
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "wymagania_ogolne_ZSZ5_2026_2027.html"
BACKUP = ROOT / "wymagania_ogolne_ZSZ5_2026_2027__przed_przebudowa.html"
REPORT = ROOT / "przebudowa_wymagan_ogolnych" / "raport_generowania_kompletnej_strony.md"
FIX_REPORT = ROOT / "przebudowa_wymagan_ogolnych" / "raport_napraw_tresci_wymagan.md"


ROMAN_RE = re.compile(r"(?m)^(?:Dział\s+)?([IVXLCDM]+)\.\s+([^\n]{3,320})")
PAGE_NOISE_RE = re.compile(
    r"^(Dziennik Ustaw|Szkoła ponadpodstawowa|Podstawa programowa|Poz\.|"
    r"Załącznik|Minister Edukacji|Rzeczypospolitej Polskiej|–\s*\d+\s*–)"
)
TABLE_MARKER_RE = re.compile(r"(?:\bX\b\s*){1,}$")
SCOPE_EXPANDED_RE = re.compile(
    r"\s*(?:\d+\s+)?Zakres rozszerzony\.?.*$",
    re.IGNORECASE,
)


@dataclass
class SubjectSpec:
    school: str
    name: str
    path: str
    source_label: str
    mode: str = "single"
    start_anchor: str | None = None
    start_occurrence: str = "first"
    end_anchor: str | None = None
    max_sections: int | None = None
    status: str = "projekt do zatwierdzenia"
    note: str = ""


def roman_to_int(s: str) -> int:
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    for ch in reversed(s):
        val = vals.get(ch, 0)
        if val < prev:
            total -= val
        else:
            total += val
            prev = val
    return total


def clean(s: str) -> str:
    s = s.replace("\u00ad", "")
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    s = re.sub(r"\b([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]{1,5})\s+([a-ząćęłńóśźż]{1,5})\b", _join_split_word, s)
    replacements = {
        "e -mail": "e-mail",
        "e -maile": "e-maile",
        "informacyjno - -komunikacyjnych": "informacyjno-komunikacyjnych",
        "klim at": "klimat",
        "za wody": "zawody",
        "r eaguje": "reaguje",
    }
    for bad, good in replacements.items():
        s = s.replace(bad, good)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    s = re.sub(r"\s+([)])", r"\1", s)
    s = re.sub(r"([(])\s+", r"\1", s)
    return s


def _join_split_word(match: re.Match) -> str:
    joined = match.group(1) + match.group(2)
    known = {
        "języku",
        "rozwoju",
        "efektywnego",
        "sportu",
        "przetwarzanie",
        "wykorzystanie",
        "podstawowego",
        "działania",
        "sieci",
        "uczeń",
        "całe",
        "reaguje",
        "oprogramowaniem",
        "programowaniem",
        "bezpieczeństwa",
        "przedstawia",
        "charakteryzuje",
        "wyjaśnia",
    }
    return joined if joined.lower() in known else match.group(0)


def clean_title(title: str) -> str:
    title = clean(title)
    title = SCOPE_EXPANDED_RE.sub("", title).strip()
    title = re.sub(r"\s*\d+\)\s*$", "", title).strip()
    title = re.sub(r"\s+\d{2,4}\s*$", "", title).strip()
    title = re.sub(r"\s*Cele\s+\d+(?:\s+\d+)*.*$", "", title).strip()
    title = re.sub(r"\s*Umiejętności\s+\d+(?:\s+\d+)*.*$", "", title).strip()
    title = re.sub(r"\s+[,;:-]\s*$", "", title).strip()
    if title.endswith(","):
        title = title[:-1].strip()
    return title


def clean_requirement(item: str) -> str:
    item = clean(item)
    item = SCOPE_EXPANDED_RE.sub("", item).strip()
    item = re.split(r"\s+KLASY\s+[IVXLCDM]+\b", item, maxsplit=1)[0].strip()
    item = re.split(r"\s+KLASA\s+[IVXLCDM]+\b", item, maxsplit=1)[0].strip()
    item = re.split(r"\s+Warunki i sposób realizacji\b", item, maxsplit=1)[0].strip()
    item = re.split(r"\s+Wymagania fakultatywne\b", item, maxsplit=1)[0].strip()
    item = re.sub(r"\s+Cele\s+\d+(?:\s+\d+)*\s+Umiejętności\s+\d+(?:\s+\d+)*", " ", item)
    item = re.sub(r"\s+Cele\s+\d+(?:\s+\d+)*", " ", item)
    item = re.sub(r"\s+Umiejętności\s+\d+(?:\s+\d+)*", " ", item)
    item = re.sub(r"(?<!\w)X(?!\w)", " ", item)
    item = TABLE_MARKER_RE.sub("", item).strip()
    item = re.sub(r"\s+\bX\b(?:\s+\bX\b)*\s*$", "", item).strip()
    item = re.sub(r"\s+\d+\s*$", "", item).strip()
    item = re.sub(r"\s+;\s*$", ".", item)
    item = re.sub(r"\s+\.\s*$", ".", item)
    return item


@lru_cache(maxsize=None)
def read_pdf(path: str) -> str:
    reader = PdfReader(str(ROOT / path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def anchor_index(text: str, anchor: str, occurrence: str = "first", start: int = 0) -> int:
    low = text.lower()
    needle = anchor.lower()
    if occurrence == "last":
        return low.rfind(needle)
    if occurrence.startswith("after:"):
        after = occurrence.split(":", 1)[1].lower()
        pos = low.find(after)
        return low.find(needle, max(pos, 0))
    return low.find(needle, start)


def subject_segment(spec: SubjectSpec) -> str:
    text = read_pdf(spec.path)
    low = text.lower()

    if spec.mode == "bsi_full" and spec.start_anchor:
        base = low.find("podstawa programowa kształcenia ogólnego dla branżowej szkoły i stopnia")
        base = max(base, 0)
        pattern = re.compile(rf"(?m)^\s*{re.escape(spec.start_anchor)}\s*$")
        match = pattern.search(text, base)
        start = match.start() if match else anchor_index(text, spec.start_anchor, spec.start_occurrence)
    elif spec.start_anchor:
        start = anchor_index(text, spec.start_anchor, spec.start_occurrence)
        if start < 0:
            start = 0
    else:
        candidates = [
            i
            for i in [
                low.find("zakres podstawowy", 10000),
                low.find("podstawa programowa przedmiotu", 10000),
                low.find("treści nauczania", 10000),
            ]
            if i >= 0
        ]
        start = min(candidates) if candidates else 0

    if spec.end_anchor:
        end = low.find(spec.end_anchor.lower(), start + 1000)
        if end < 0:
            end = len(text)
    elif spec.mode == "bsi_full":
        headings = [
            "JĘZYK POLSKI",
            "JĘZYK OBCY NOWOŻYTNY",
            "HISTORIA",
            "WIEDZA O SPOŁECZEŃSTWIE",
            "PODSTAWY PRZEDSIĘBIORCZOŚCI",
            "GEOGRAFIA",
            "BIOLOGIA",
            "CHEMIA",
            "FIZYKA",
            "MATEMATYKA",
            "INFORMATYKA",
            "WYCHOWANIE FIZYCZNE",
            "EDUKACJA DLA BEZPIECZEŃSTWA",
        ]
        next_positions = []
        for heading in headings:
            pattern = re.compile(rf"(?m)^\s*{re.escape(heading)}\s*$")
            match = pattern.search(text, start + 20)
            if match:
                next_positions.append(match.start())
        end = min(next_positions) if next_positions else len(text)
    else:
        stops = []
        for marker in ["warunki i sposób realizacji"]:
            pos = low.find(marker, start + 1000)
            if pos >= 0:
                stops.append(pos)
        end = min(stops) if stops else len(text)

    seg = text[start:end]

    detailed_markers = [
        "treści nauczania – wymagania szczegółowe",
        "treści nauczania - wymagania szczegółowe",
        "treści nauczania",
        "wymagania szczegółowe dotyczące wiedzy",
        "wymagania szczegółowe",
        "dział i.",
    ]
    dstarts = [seg.lower().find(m) for m in detailed_markers if seg.lower().find(m) >= 0]
    if dstarts:
        seg = seg[min(dstarts) :]
    return seg


def extract_sections(spec: SubjectSpec) -> list[dict]:
    fixed = fixed_sections(spec)
    if fixed is not None:
        return fixed

    seg = subject_segment(spec)
    lines = []
    for line in seg.splitlines():
        line = clean(line)
        if not line or PAGE_NOISE_RE.match(line):
            continue
        lines.append(line)
    text = "\n".join(lines)

    matches = list(ROMAN_RE.finditer(text))
    sections = []
    seen = set()
    for idx, match in enumerate(matches):
        number = match.group(1)
        raw_title = clean_title(match.group(2))
        title = re.sub(r"\s*Uczeń:.*$", "", raw_title).strip()
        title = re.sub(r"\s*Słuchacz:.*$", "", title).strip()
        title = re.sub(r"\s*Uczeń\.?$", "", title).strip()
        title = clean_title(title)
        if len(title) < 3:
            continue
        key = (number, title)
        if key in seen:
            continue
        seen.add(key)
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end]
        items = extract_items(body)
        if not items:
            if title.lower().startswith(("uczeń", "słuchacz")):
                items = [title if title.endswith(".") else f"{title}."]
            else:
                continue
        sections.append(
            {
                "number": number,
                "number_int": roman_to_int(number),
                "title": title,
                "items": items,
            }
        )
        if spec.max_sections and len(sections) >= spec.max_sections:
            break

    # Drop obvious general-goal sections if detailed sections follow from I again.
    if len(sections) > 5:
        ints = [s["number_int"] for s in sections]
        if 1 in ints[1:]:
            second_i = ints.index(1, 1)
            if second_i <= 6:
                sections = sections[second_i:]

    return sections


def extract_items(body: str) -> list[str]:
    body = re.split(r"\bWymagania fakultatywne\b", body, maxsplit=1)[0]
    body = SCOPE_EXPANDED_RE.sub("", body)
    body = re.sub(r"\n+", "\n", body)
    parts = re.split(r"(?m)\n?\s*(\d+\))\s+", body)
    items = []
    if len(parts) > 2:
        for i in range(1, len(parts), 2):
            item = clean_requirement(parts[i] + " " + parts[i + 1])
            item = re.split(r"(?=\s+\d+\)\s+)", item)[0]
            item = re.sub(r";\s*$", ".", item)
            if (
                20 <= len(item) <= 900
                and not PAGE_NOISE_RE.match(item)
                and "Wymagania fakultatywne" not in item
                and "Cele 1 2" not in item
                and "Zakres rozszerzony" not in item
            ):
                items.append(item)
    if not items:
        sentences = re.split(r"(?<=[.;])\s+", clean(body))
        items = [clean_requirement(s) for s in sentences if 25 <= len(s) <= 400][:8]
    # Keep concrete but bounded; the source PDF remains linked at subject level.
    deduped = []
    seen = set()
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped[:40]


def make_sections(raw_sections: list[tuple[str, str, list[str]]]) -> list[dict]:
    return [
        {
            "number": number,
            "number_int": roman_to_int(number),
            "title": clean_title(title),
            "items": [clean_requirement(item) for item in items if clean_requirement(item)],
        }
        for number, title, items in raw_sections
    ]


def fixed_sections(spec: SubjectSpec) -> list[dict] | None:
    key = (spec.school, spec.name)
    if key == ("bsi", "Edukacja dla bezpieczeństwa"):
        return make_sections(
            [
                (
                    "I",
                    "Bezpieczeństwo państwa",
                    [
                        "1) zna i charakteryzuje podstawowe pojęcia związane z bezpieczeństwem państwa oraz wymienia składniki bezpieczeństwa państwa.",
                        "2) jest zorientowany w geopolitycznych uwarunkowaniach bezpieczeństwa wynikających z położenia Polski.",
                        "3) przedstawia rolę organizacji międzynarodowych w zapewnieniu bezpieczeństwa Polski.",
                        "4) zna misję, rolę, podstawowe zadania, strukturę organizacyjną i uzbrojenie Sił Zbrojnych Rzeczypospolitej Polskiej.",
                    ],
                ),
                (
                    "II",
                    "Działania w sytuacjach nadzwyczajnych zagrożeń",
                    [
                        "1) wymienia przykłady nadzwyczajnych zagrożeń pochodzenia naturalnego i wywołanych przez człowieka.",
                        "2) rozróżnia sygnały alarmowe i środki alarmowe oraz omawia właściwe zachowanie po ich uruchomieniu.",
                        "3) przedstawia obowiązki ludności w sytuacjach wymagających ewakuacji.",
                        "4) omawia rolę służb i innych podmiotów oraz uzasadnia znaczenie stosowania się do ich zaleceń.",
                        "5) zna zasady postępowania w razie pożaru, wypadku komunikacyjnego, powodzi, intensywnej śnieżycy, uwolnienia niebezpiecznych środków chemicznych i zdarzenia terrorystycznego.",
                    ],
                ),
                (
                    "III",
                    "Podstawy pierwszej pomocy",
                    [
                        "1) rozumie znaczenie udzielania pierwszej pomocy przez świadka zdarzenia i przedstawia jego rolę.",
                        "2) zna zasady bezpiecznego postępowania w miejscu zdarzenia oraz ochrony przed zakażeniem.",
                        "3) podaje przykłady zagrożeń w środowisku domowym, ulicznym, wodnym, podziemnym i leśnym.",
                        "4) przedstawia metody zapewnienia bezpieczeństwa własnego, osoby poszkodowanej i otoczenia.",
                        "5) rozpoznaje osobę w stanie zagrożenia życia i wyjaśnia znaczenie podstawowych funkcji życiowych.",
                        "6) prawidłowo wzywa pomoc, podaje numery alarmowe i przekazuje informacje o zdarzeniu.",
                        "7) zna zasady postępowania z osobą nieprzytomną, ocenia przytomność i oddech, udrażnia drogi oddechowe i układa w pozycji bezpiecznej.",
                        "8) wykonuje podstawowe czynności resuscytacji krążeniowo-oddechowej i opisuje zastosowanie AED.",
                        "9) wykonuje podstawowe czynności pierwszej pomocy w zadławieniu.",
                        "10) zna wyposażenie apteczki pierwszej pomocy.",
                        "11) zna zasady pierwszej pomocy w ranach, krwotokach, złamaniach, skręceniach i zwichnięciach.",
                        "12) omawia zasady postępowania w oparzeniach i demonstruje chłodzenie oparzonej kończyny.",
                        "13) zna zasady pierwszej pomocy w sytuacji zagrożenia z użyciem broni konwencjonalnej, w tym tamowania krwotoku i zachowania według zasady uciekaj, schowaj się, walcz.",
                    ],
                ),
                (
                    "IV",
                    "Kształtowanie postaw obronnych",
                    [
                        "1) zna podstawy orientowania się w terenie i potrafi wskazywać kierunki świata z użyciem kompasu, busoli, GPS lub charakterystycznych przedmiotów terenowych.",
                        "2) używa różnych rodzajów map do orientacji w terenie.",
                        "3) zna istotę cyberbezpieczeństwa.",
                        "4) tworzy i przedstawia wypowiedzi dotyczące roli cyberbezpieczeństwa militarnego w systemie cyberbezpieczeństwa państwa.",
                        "5) zna zasady bezpiecznego i efektywnego posługiwania się bronią strzelecką.",
                        "6) zna podstawowe części składowe broni strzeleckiej.",
                        "7) przyjmuje postawy strzeleckie.",
                        "8) prawidłowo zgrywa przyrządy celownicze, reguluje oddech podczas składania się do strzału i ściąga język spustowy.",
                    ],
                ),
            ]
        )
    if key == ("technikum", "Edukacja dla bezpieczeństwa"):
        return make_sections(
            [
                (
                    "I",
                    "Bezpieczeństwo państwa",
                    [
                        "1) identyfikuje wyzwania dla bezpieczeństwa indywidualnego i zbiorowego oraz odnosi je do bezpieczeństwa lokalnego i państwowego.",
                        "2) wymienia zadania parlamentu, Prezydenta i Rady Ministrów w dziedzinie obronności oraz elementy systemu obronnego państwa.",
                        "3) omawia zadania, strukturę organizacyjną, podstawowe uzbrojenie i wyposażenie Sił Zbrojnych Rzeczypospolitej Polskiej.",
                        "4) wyjaśnia istotę systemu bezpieczeństwa państwa, jego instytucje i związki między nimi.",
                        "5) określa zakres działania wybranych organizacji proobronnych.",
                        "6) wymienia formacje mundurowe układu pozamilitarnego państwa i wyjaśnia ich rolę w systemie bezpieczeństwa.",
                        "7) uzasadnia geopolityczne, militarne i gospodarcze aspekty bezpieczeństwa państwa.",
                        "8) rozumie rolę świadczeń obywateli na rzecz obronności oraz zadania władz państwowych i samorządowych w tym zakresie.",
                        "9) rozróżnia zagrożenia czasu pokoju i czasu wojny oraz podaje przykłady zarządzeń władz w sytuacji kryzysowej.",
                        "10) wyjaśnia podstawowe zasady zarządzania kryzysowego, w tym pojęcia siatki bezpieczeństwa i infrastruktury krytycznej.",
                        "11) omawia zasady zachowania w przypadku zdarzeń terrorystycznych.",
                        "12) rozpoznaje cyberprzemoc i cyberzagrożenia oraz zna procedury postępowania w przypadku ich wystąpienia.",
                    ],
                ),
                (
                    "II",
                    "Przygotowanie do działań ratowniczych w sytuacjach nadzwyczajnych zagrożeń",
                    [
                        "1) wyjaśnia podstawowe zasady międzynarodowego prawa humanitarnego i funkcjonowania obrony cywilnej.",
                        "2) omawia rolę Państwowej Straży Pożarnej, Państwowego Ratownictwa Medycznego oraz ochotniczych służb i podmiotów ratowniczych.",
                        "3) opisuje obowiązki pieszego i kierowcy podczas przejazdu pojazdu uprzywilejowanego.",
                        "4) rozpoznaje zagrożenia i zna zasady postępowania podczas pożaru, wypadku komunikacyjnego, powodzi, katastrofy budowlanej, wycieku gazu, znalezienia niewypału, lawiny i intensywnej śnieżycy.",
                        "5) wyjaśnia zasady postępowania w przypadku awarii chemicznej, rozszczelnienia substancji toksycznych oraz użycia środków ochrony.",
                        "6) omawia zasady ewakuacji ludności i zwierząt oraz zaopatrzenia ludności ewakuowanej w wodę i żywność.",
                        "7) dobiera podręczny sprzęt gaśniczy do rodzaju pożaru i wyznacza strefę bezpieczeństwa.",
                        "8) rozpoznaje znaki substancji toksycznych, omawia wpływ promieniowania i skażeń oraz sposoby zabezpieczenia żywności i wody.",
                        "9) wyjaśnia pojęcia odkażania, dezaktywacji, dezynfekcji, deratyzacji oraz zabiegów specjalnych i sanitarnych.",
                        "10) definiuje alarmy i sygnały alarmowe, omawia zasady zachowania po ogłoszeniu alarmu i wskazuje drogi ewakuacji w szkole.",
                    ],
                ),
                (
                    "III",
                    "Podstawy pierwszej pomocy",
                    [
                        "1) opisuje znaczenie układu oddychania, krążenia i nerwowego dla funkcji życiowych.",
                        "2) wyjaśnia cele pierwszej pomocy i znaczenie działań świadka zdarzenia.",
                        "3) stosuje zasady bezpiecznego postępowania w miejscu zdarzenia oraz ochrony przed zakażeniem.",
                        "4) rozpoznaje osobę w stanie zagrożenia życia, ocenia przytomność i oddech oraz prawidłowo wzywa pomoc.",
                        "5) zna zasady postępowania z osobą nieprzytomną, udrażnia drogi oddechowe i układa poszkodowanego w pozycji bezpiecznej.",
                        "6) wykonuje podstawowe czynności resuscytacji krążeniowo-oddechowej i opisuje użycie AED.",
                        "7) wykonuje podstawowe czynności pierwszej pomocy w zadławieniu.",
                        "8) zna wyposażenie apteczki pierwszej pomocy.",
                        "9) udziela pierwszej pomocy w ranach, krwotokach, złamaniach, skręceniach i zwichnięciach.",
                        "10) omawia pierwszą pomoc w oparzeniach, wstrząsie, podtopieniu i zatruciach.",
                        "11) zna zasady pierwszej pomocy w sytuacji zagrożenia z użyciem broni konwencjonalnej, w tym tamowania masywnego krwotoku.",
                    ],
                ),
                (
                    "IV",
                    "Edukacja obronna",
                    [
                        "1) zna ograniczenia organizmu związane z brakiem snu, wody i pożywienia oraz wpływem czynników atmosferycznych na przetrwanie.",
                        "2) wyjaśnia zjawisko paniki i omawia sposoby jej przeciwdziałania.",
                        "3) zna podręczne środki zwiększające szanse przetrwania oraz sposoby pozyskiwania wody i pożywienia w środowisku naturalnym.",
                        "4) identyfikuje podstawowe zagrożenia cyberbezpieczeństwa.",
                        "5) określa podział ról podczas współdziałania układu militarnego z podmiotami układu pozamilitarnego.",
                        "6) przedstawia rolę cyberbezpieczeństwa militarnego w systemie cyberbezpieczeństwa państwa.",
                        "7) zna zasady składania i rozkładania broni.",
                        "8) wykonuje strzelanie z wykorzystaniem dostępnych form szkolenia strzeleckiego, takich jak broń kulowa, pneumatyczna, repliki ASG, strzelnice wirtualne albo laserowe.",
                    ],
                ),
            ]
        )
    if key == ("bsi", "Wychowanie fizyczne"):
        return make_sections(
            [
                (
                    "I",
                    "Ćwiczenia ogólnorozwojowe",
                    [
                        "1) wykonuje ćwiczenia wzmacniające różne grupy mięśni z użyciem podstawowych przyborów i przyrządów lub bez nich.",
                        "2) omawia ćwiczenia rozciągające i odciążające kręgosłup wspierające prawidłową postawę ciała i profilaktykę przeciążeń zawodowych.",
                        "3) wykonuje marsze, marszobiegi i ćwiczenia funkcjonalne na świeżym powietrzu jako formę aktywnego wypoczynku.",
                        "4) wyjaśnia znaczenie aktywności fizycznej na świeżym powietrzu dla samopoczucia, regeneracji i przyszłej pracy zawodowej.",
                        "5) samodzielnie wykonuje rozgrzewkę przygotowującą do wysiłku.",
                        "6) korzysta z nowoczesnych technologii do opracowania planu aktywności fizycznej dopasowanego do własnych zainteresowań.",
                    ],
                ),
                (
                    "II",
                    "Gry zespołowe i rekreacyjne",
                    [
                        "1) uczestniczy w różnorodnych grach zespołowych i rekreacyjnych dostosowanych do możliwości i potrzeb.",
                        "2) pełni funkcję gracza, kapitana drużyny i sędziego w szkolnym współzawodnictwie oraz stosuje zasady fair play.",
                        "3) współpracuje z innymi uczniami podczas ćwiczeń i gry.",
                        "4) pełni funkcję kibica, wspierając grające drużyny.",
                    ],
                ),
                (
                    "III",
                    "Lekkoatletyka",
                    [
                        "1) wykonuje bieg ciągły w umiarkowanym tempie.",
                        "2) stosuje umiejętności lekkoatletyczne w innych aktywnościach fizycznych.",
                        "3) ocenia swoje możliwości fizyczne i dostosowuje intensywność wysiłku do własnych potrzeb.",
                    ],
                ),
                (
                    "IV",
                    "Taniec",
                    [
                        "1) wymienia różne formy aktywności fizycznej związane z muzyką.",
                        "2) przygotowuje aktywności taneczne z uwzględnieniem współpracy w grupie i bieżących trendów.",
                        "3) wyjaśnia, jak taniec i ćwiczenia z muzyką wpływają na sprawność fizyczną i zdrowie.",
                    ],
                ),
                (
                    "V",
                    "Relaksacja i odprężenie",
                    [
                        "1) wycisza się i relaksuje przy pomocy oddechu oraz ćwiczeń rozciągających.",
                        "2) omawia znaczenie ćwiczeń zmniejszających napięcie mięśni po pracy fizycznej lub długim siedzeniu.",
                        "3) stosuje metody regeneracji po aktywności fizycznej oraz rozumie ich znaczenie dla profilaktyki kontuzji i przyszłej pracy zawodowej.",
                    ],
                ),
                (
                    "VI",
                    "Monitorowanie aktywności i sprawności fizycznej",
                    [
                        "1) planuje podstawowe formy aktywności fizycznej z uwzględnieniem własnych potrzeb i możliwości.",
                        "2) stosuje testy sprawności fizycznej do oceny kondycji fizycznej.",
                        "3) korzysta z aplikacji, platform edukacyjnych lub urządzeń pomiarowych wspierających aktywność fizyczną z zachowaniem zasad ochrony danych osobowych.",
                    ],
                ),
                (
                    "VII",
                    "Sprawność fizyczna w służbach mundurowych i innych zawodach",
                    [
                        "1) planuje i realizuje trening przygotowujący do rekrutacji do służb mundurowych, rozwijający siłę, szybkość, wytrzymałość i koordynację ruchową.",
                        "2) wymienia zawody, w których wysoka sprawność fizyczna stanowi istotny warunek wykonywania pracy.",
                        "3) wykonuje próby sprawnościowe stosowane w rekrutacji do służb mundurowych i interpretuje wyniki w kontekście poprawy sprawności fizycznej.",
                    ],
                ),
                (
                    "VIII",
                    "Bezpieczeństwo w aktywności fizycznej",
                    [
                        "1) korzysta ze sprzętu i urządzeń sportowych zgodnie z ich przeznaczeniem.",
                        "2) dba o bezpieczeństwo swoje i innych uczestników podczas ćwiczeń oraz współzawodnictwa.",
                        "3) dobiera strój sportowy i obuwie do rodzaju aktywności oraz warunków atmosferycznych.",
                        "4) stosuje zasady bezpiecznego zachowania podczas aktywności fizycznej poza szkołą.",
                        "5) omawia zasady dotyczące aktywności fizycznej oraz poruszania się w terenie.",
                    ],
                ),
                (
                    "IX",
                    "Kompetencje społeczne",
                    [
                        "1) rozumie znaczenie idei olimpizmu i zasady fair play.",
                        "2) uczestniczy w działaniach promujących aktywność fizyczną w szkole.",
                        "3) prezentuje postawy akceptacji, szacunku i wsparcia wobec innych uczniów niezależnie od ich umiejętności i stopnia sprawności fizycznej.",
                    ],
                ),
            ]
        )
    return None


def split_requirements(items: list[str], title: str) -> dict[str, list[str]]:
    grades = ["Dopuszczająca", "Dostateczna", "Dobra", "Bardzo dobra", "Celująca"]
    chunks: dict[str, list[str]] = {g: [] for g in grades}
    if len(items) >= 5:
        size = math.ceil(len(items) / 5)
        for idx, grade in enumerate(grades):
            chunks[grade] = items[idx * size : (idx + 1) * size]
    else:
        for idx, item in enumerate(items):
            chunks[grades[min(idx, 4)]].append(item)
    return chunks


def h(text: str) -> str:
    return html.escape(text, quote=True)


def polish_count(n: int, one: str, few: str, many: str) -> str:
    if n == 1:
        word = one
    elif n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        word = few
    else:
        word = many
    return f"{n} {word}"


def render_subject(spec: SubjectSpec, idx: int) -> tuple[str, dict]:
    sections = extract_sections(spec)
    color = {
        "technikum": "#1e40af",
        "bsii": "#166534",
        "bsi": "#6b21a8",
    }[spec.school]
    status_class = "status-ok" if spec.status == "gotowe" else "status-review"
    subject_id = f"{spec.school}_{idx}"
    subject_body_id = f"{subject_id}_body"
    subject_search = " ".join([spec.name, spec.source_label] + [s["title"] for s in sections])
    parts = [
        f'<article class="subject-card" id="{subject_id}" data-search="{h(subject_search)}">',
        f'<button class="subject-toggle" type="button" onclick="toggleSubject(\'{subject_id}\')" '
        f'aria-expanded="false" aria-controls="{subject_body_id}" style="border-left-color:{color}">',
        '<span class="arrow" aria-hidden="true">▶</span>',
        f'<span class="subject-name">{h(spec.name)}</span>',
        f'<span class="subject-meta">{polish_count(len(sections), "dział", "działy", "działów")} · {polish_count(sum(len(s["items"]) for s in sections), "wymaganie źródłowe", "wymagania źródłowe", "wymagań źródłowych")}</span>',
        "</button>",
        f'<div class="subject-body" id="{subject_body_id}">',
        '<details class="source-box">',
        '<summary>Źródło, status i uwagi</summary>',
        f'<p><span class="{status_class}">{h(spec.status)}</span>'
        f'<strong>Źródło:</strong> {h(spec.source_label)}</p>',
        f'<code>{h(spec.path)}</code>',
    ]
    if spec.note:
        parts.append(f'<p class="note">{h(spec.note)}</p>')
    parts.extend(
        [
            "</details>",
            '<p class="cumulative">Wymagania mają charakter kumulatywny: ocena wyższa obejmuje wymagania na oceny niższe. Podział na oceny jest opracowaniem ZSZ5 na podstawie treści podstawy programowej i wymaga recenzji nauczyciela przedmiotu.</p>',
            '<div class="subject-actions">',
            f'<button type="button" onclick="expandSubjectDzials(\'{subject_id}\', true)">Rozwiń działy przedmiotu</button>',
            f'<button type="button" onclick="expandSubjectDzials(\'{subject_id}\', false)">Zwiń działy przedmiotu</button>',
            "</div>",
        ]
    )
    for sidx, section in enumerate(sections):
        dz_id = f"{spec.school}_{idx}_{sidx}"
        dz_body_id = f"{dz_id}_body"
        dz_search = f'{section["number"]} {section["title"]}'
        chunks = split_requirements(section["items"], section["title"])
        parts.extend(
            [
                f'<section class="dzial" id="{dz_id}" data-search="{h(dz_search)}">',
                f'<button class="dzial-toggle" type="button" onclick="toggleDzial(\'{dz_id}\')" '
                f'aria-expanded="false" aria-controls="{dz_body_id}">',
                '<span class="arrow small" aria-hidden="true">▶</span>',
                f'<span class="dzial-num">Dział {h(section["number"])}.</span>',
                f'<span class="dzial-title">{h(section["title"])}</span>',
                f'<span class="dzial-count">{polish_count(len(section["items"]), "wymaganie", "wymagania", "wymagań")}</span>',
                "</button>",
                f'<div class="dzial-body" id="{dz_body_id}">',
                '<div class="table-wrap" role="region" aria-label="Tabela wymagań na oceny"><table class="req-table">',
                "<thead><tr>"
                "<th>Dopuszczająca</th><th>Dostateczna</th><th>Dobra</th><th>Bardzo dobra</th><th>Celująca</th>"
                "</tr></thead><tbody><tr>",
            ]
        )
        for grade in ["Dopuszczająca", "Dostateczna", "Dobra", "Bardzo dobra", "Celująca"]:
            parts.append(f'<td data-label="{h(grade)}"><ul>')
            if not chunks[grade]:
                parts.append('<li class="review-note">Próg do określenia przez nauczyciela na podstawie programu nauczania.</li>')
            for item in chunks[grade]:
                parts.append(f"<li>{h(item)}</li>")
            parts.append("</ul></td>")
        parts.extend(["</tr></tbody></table></div>", "</div>", "</section>"])
    parts.extend(["</div>", "</article>"])
    return "\n".join(parts), {
        "school": spec.school,
        "name": spec.name,
        "id": subject_id,
        "sections": len(sections),
        "items": sum(len(s["items"]) for s in sections),
        "status": spec.status,
        "path": spec.path,
    }


def specs() -> list[SubjectSpec]:
    bsi_full = "01_BSI_stopnia/ogolne/PP_BSI_Rozp2017_poz356_pelny_tekst.pdf"
    bsi_hit = "03_Technikum/ogolne/PP_historia_i_terazniejszosc_DzU_2022_poz609.pdf"
    tech_2024 = "03_Technikum/ogolne/PP_nowelizacja_LO_Tech_BSII_DzU_2024_poz1019.pdf"
    biz = "03_Technikum/ogolne/PP_biznes_i_zarzadzanie_DzU_2023_poz314.pdf"
    bsi_biz = "01_BSI_stopnia/ogolne/PP_BSI_biznes_i_zarzadzanie_DzU_2023_poz312.pdf"

    common_note = "Przedmiot ujęty zgodnie z ramowym planem; finalny podział na oceny powinien zatwierdzić nauczyciel."
    transitional = "przejściowe / do recenzji"

    return [
        # Technikum
        SubjectSpec("technikum", "Język polski", "03_Technikum/ogolne/PP_jezyk_polski.pdf", "ORE / podstawa programowa LO i technikum 2018"),
        SubjectSpec("technikum", "Język angielski", "03_Technikum/ogolne/PP_jezyk_obcy_nowozytny.pdf", "ORE / język obcy nowożytny, technikum 2018"),
        SubjectSpec("technikum", "Język niemiecki", "03_Technikum/ogolne/PP_jezyk_obcy_nowozytny.pdf", "ORE / język obcy nowożytny, technikum 2018"),
        SubjectSpec("technikum", "Historia", "03_Technikum/ogolne/PP_historia.pdf", "ORE / historia, technikum 2018"),
        SubjectSpec("technikum", "Edukacja obywatelska", "03_Technikum/ogolne/PP_edukacja_obywatelska_Rozp_ME_06_03_2025.pdf", "Dz.U. 2025 poz. 382, edukacja obywatelska", start_anchor="Dział I. Ja i społeczeństwo", max_sections=7),
        SubjectSpec("technikum", "Biznes i zarządzanie", biz, "Dz.U. 2023 poz. 314, biznes i zarządzanie", start_anchor="BIZNES I ZARZĄDZANIE \nZAKRES PODSTAWOWY", end_anchor="ZAKRES ROZSZERZONY"),
        SubjectSpec("technikum", "Geografia", "03_Technikum/ogolne/PP_geografia.pdf", "ORE / geografia, technikum 2018"),
        SubjectSpec("technikum", "Biologia", "03_Technikum/ogolne/PP_biologia.pdf", "ORE / biologia, technikum 2018"),
        SubjectSpec("technikum", "Chemia", "03_Technikum/ogolne/PP_chemia.pdf", "ORE / chemia, technikum 2018"),
        SubjectSpec("technikum", "Fizyka", "03_Technikum/ogolne/PP_fizyka.pdf", "ORE / fizyka, technikum 2018"),
        SubjectSpec("technikum", "Matematyka", "03_Technikum/ogolne/PP_matematyka.pdf", "ORE / matematyka, technikum 2018"),
        SubjectSpec("technikum", "Informatyka", "03_Technikum/ogolne/PP_informatyka.pdf", "ORE / informatyka, technikum 2018"),
        SubjectSpec("technikum", "Wychowanie fizyczne", "01_BSI_stopnia/ogolne/PP_BSI_wychowanie_fizyczne_nowe_DzU_2025_poz1035.pdf", "Dz.U. 2025 poz. 1035, WF dla LO/technikum/BS II", start_anchor="Dział I. Ćwiczenia ogólnorozwojowe", max_sections=9, note="Źródło jest w folderze BSI, ale treść aktu dotyczy LO/technikum/BS II."),
        SubjectSpec("technikum", "Edukacja dla bezpieczeństwa", "03_Technikum/ogolne/PP_historia_i_terazniejszosc_DzU_2022_poz1705.pdf", "Dz.U. 2022 poz. 1705, aktualizacja EDB dla LO/technikum/BS II", start_anchor="Treści nauczania", max_sections=4),
        SubjectSpec("technikum", "Historia i teraźniejszość", tech_2024, "Dz.U. 2024 poz. 1019, HiT dla uczniów rozpoczynających przed 1.09.2024", start_anchor="HISTORIA I TERAŹNIEJSZOŚĆ \nZAKRES PODSTAWOWY", status=transitional, note="Przedmiot przejściowy dla wskazanych roczników; nie dotyczy nowych klas po zmianach 2024/2025."),
        SubjectSpec("technikum", "Wiedza o społeczeństwie", "03_Technikum/ogolne/PP_wiedza_o_spoleczenstwie_Rozp2018.pdf", "ORE / WOS 2018", status=transitional, note="Przedmiot przejściowy dla starszych roczników; w nowych rocznikach zastępowany edukacją obywatelską."),
        # BS II
        SubjectSpec("bsii", "Język polski", "02_BSII_stopnia/ogolne/PP_jezyk_polski.pdf", "ORE / język polski, BS II 2018"),
        SubjectSpec("bsii", "Język angielski", "02_BSII_stopnia/ogolne/PP_jezyk_obcy_nowozytny.pdf", "ORE / język obcy nowożytny, BS II 2018"),
        SubjectSpec("bsii", "Matematyka", "02_BSII_stopnia/ogolne/PP_matematyka.pdf", "ORE / matematyka, BS II 2018"),
        SubjectSpec("bsii", "Informatyka", "02_BSII_stopnia/ogolne/PP_informatyka.pdf", "ORE / informatyka, BS II 2018"),
        # BS I
        SubjectSpec("bsi", "Język polski", bsi_full, "Dz.U. 2017 poz. 356, BS I", mode="bsi_full", start_anchor="JĘZYK POLSKI", start_occurrence="after:PODSTAWA PROGRAMOWA KSZTAŁCENIA OGÓLNEGO DLA BRANŻOWEJ SZKOŁY I STOPNIA"),
        SubjectSpec("bsi", "Język angielski", bsi_full, "Dz.U. 2017 poz. 356, język obcy nowożytny BS I", mode="bsi_full", start_anchor="JĘZYK OBCY NOWOŻYTNY", start_occurrence="after:PODSTAWA PROGRAMOWA KSZTAŁCENIA OGÓLNEGO DLA BRANŻOWEJ SZKOŁY I STOPNIA"),
        SubjectSpec("bsi", "Język niemiecki", bsi_full, "Dz.U. 2017 poz. 356, język obcy nowożytny BS I", mode="bsi_full", start_anchor="JĘZYK OBCY NOWOŻYTNY", start_occurrence="after:PODSTAWA PROGRAMOWA KSZTAŁCENIA OGÓLNEGO DLA BRANŻOWEJ SZKOŁY I STOPNIA"),
        SubjectSpec("bsi", "Historia", bsi_hit, "Dz.U. 2022 poz. 609, historia BS I", start_anchor="HISTORIA \nCele kształcenia", end_anchor="WIEDZA O SPOŁECZEŃSTWIE"),
        SubjectSpec("bsi", "Historia i teraźniejszość", bsi_hit, "Dz.U. 2022 poz. 609, HiT BS I", start_anchor="HISTORIA I TERAŹNIEJSZOŚĆ", start_occurrence="last"),
        SubjectSpec("bsi", "Edukacja obywatelska", "01_BSI_stopnia/ogolne/PP_edukacja_obywatelska_BSI_Tech_LO_Rozp_ME_06_03_2025.pdf", "Dz.U. 2025 poz. 378, edukacja obywatelska BS I", start_anchor="Dział I. Ja i społeczeństwo", max_sections=7),
        SubjectSpec("bsi", "Biznes i zarządzanie", bsi_biz, "Dz.U. 2023 poz. 312, biznes i zarządzanie BS I", start_anchor="BIZNES I ZARZĄDZANIE", start_occurrence="last"),
        SubjectSpec("bsi", "Biologia", bsi_full, "Dz.U. 2017 poz. 356, biologia BS I", mode="bsi_full", start_anchor="BIOLOGIA", start_occurrence="after:PODSTAWA PROGRAMOWA KSZTAŁCENIA OGÓLNEGO DLA BRANŻOWEJ SZKOŁY I STOPNIA"),
        SubjectSpec("bsi", "Chemia", bsi_full, "Dz.U. 2017 poz. 356, chemia BS I", mode="bsi_full", start_anchor="CHEMIA", start_occurrence="after:PODSTAWA PROGRAMOWA KSZTAŁCENIA OGÓLNEGO DLA BRANŻOWEJ SZKOŁY I STOPNIA"),
        SubjectSpec("bsi", "Fizyka", bsi_full, "Dz.U. 2017 poz. 356, fizyka BS I", mode="bsi_full", start_anchor="FIZYKA", start_occurrence="after:PODSTAWA PROGRAMOWA KSZTAŁCENIA OGÓLNEGO DLA BRANŻOWEJ SZKOŁY I STOPNIA"),
        SubjectSpec("bsi", "Geografia", bsi_full, "Dz.U. 2017 poz. 356, geografia BS I", mode="bsi_full", start_anchor="GEOGRAFIA", start_occurrence="after:PODSTAWA PROGRAMOWA KSZTAŁCENIA OGÓLNEGO DLA BRANŻOWEJ SZKOŁY I STOPNIA"),
        SubjectSpec("bsi", "Matematyka", bsi_full, "Dz.U. 2017 poz. 356, matematyka BS I", mode="bsi_full", start_anchor="MATEMATYKA", start_occurrence="after:PODSTAWA PROGRAMOWA KSZTAŁCENIA OGÓLNEGO DLA BRANŻOWEJ SZKOŁY I STOPNIA"),
        SubjectSpec("bsi", "Informatyka", bsi_full, "Dz.U. 2017 poz. 356, informatyka BS I", mode="bsi_full", start_anchor="INFORMATYKA", start_occurrence="after:PODSTAWA PROGRAMOWA KSZTAŁCENIA OGÓLNEGO DLA BRANŻOWEJ SZKOŁY I STOPNIA"),
        SubjectSpec("bsi", "Wychowanie fizyczne", "03_Technikum/ogolne/PP_wychowanie_fizyczne_nowe_DzU_2025_poz1052.pdf", "Dz.U. 2025 poz. 1052, WF dla SP/BS I", start_anchor="branżowej szkoły I stopnia", max_sections=9, note="Źródło jest w folderze technikum, ale treść aktu obejmuje BS I."),
        SubjectSpec("bsi", "Edukacja dla bezpieczeństwa", "01_BSI_stopnia/ogolne/PP_BSI_nowelizacja_28_06_2024_HiT_EdObyw_BizZarz_EdZdrow.pdf", "Dz.U. 2024 poz. 996, EDB BS I", start_anchor="Edukacja dla bezpieczeństwa", start_occurrence="last", max_sections=4),
    ]


def render_page(all_specs: list[SubjectSpec]) -> tuple[str, list[dict]]:
    grouped = {"technikum": [], "bsii": [], "bsi": []}
    grouped_stats = {"technikum": [], "bsii": [], "bsi": []}
    stats = []
    for spec in all_specs:
        idx = len(grouped[spec.school])
        html_part, stat = render_subject(spec, idx)
        grouped[spec.school].append(html_part)
        grouped_stats[spec.school].append(stat)
        stats.append(stat)

    labels = {
        "technikum": "Technikum",
        "bsii": "Branżowa Szkoła II stopnia",
        "bsi": "Branżowa Szkoła I stopnia",
    }
    colors = {"technikum": "#1e40af", "bsii": "#166534", "bsi": "#6b21a8"}
    nav = "\n".join(
        f'<button class="tab-btn" id="tab_{key}" role="tab" type="button" '
        f'onclick="showPage(\'{key}\', true)" data-color="{colors[key]}" '
        f'aria-selected="false" aria-controls="page_{key}">{labels[key]}</button>'
        for key in ["technikum", "bsii", "bsi"]
    )
    pages = []
    for key in ["technikum", "bsii", "bsi"]:
        quick_links = "\n".join(
            f'<a href="#{s["id"]}" onclick="openSubject(\'{s["id"]}\')">{h(s["name"])}</a>'
            for s in grouped_stats[key]
        )
        pages.append(
            f"""
<main class="page" id="page_{key}" role="tabpanel" aria-labelledby="tab_{key}">
  <div class="page-head">
    <h2 style="color:{colors[key]}">{labels[key]}</h2>
    <p>Komplet przedmiotów ogólnokształcących z ramówek ZSZ5. Poza tą stroną pozostają przedmioty zawodowe, religia, zajęcia z wychowawcą, doradztwo zawodowe i rozwój kompetencji zawodowych.</p>
    <div class="actions">
      <button type="button" onclick="expandSubjects('{key}')">Rozwiń przedmioty</button>
      <button type="button" onclick="collapseAll('{key}')">Zwiń wszystko</button>
      <button type="button" onclick="expandAll('{key}')">Rozwiń wszystkie działy</button>
      <button type="button" onclick="printPage('{key}')">Drukuj tę szkołę</button>
      <button type="button" onclick="clearSearch('{key}')">Wyczyść filtr</button>
    </div>
    <div class="page-tools" role="search">
      <label for="search_{key}">Szukaj przedmiotu lub działu</label>
      <input id="search_{key}" type="search" placeholder="np. matematyka, pierwsza pomoc, liczby rzeczywiste" oninput="filterSubjects('{key}')">
      <p class="filter-status" id="filter_status_{key}" aria-live="polite"></p>
    </div>
    <nav class="subject-index" aria-label="Szybki indeks przedmiotów">
      {quick_links}
    </nav>
  </div>
  <div class="subjects-list">
    {''.join(grouped[key])}
  </div>
</main>
"""
        )

    total_subjects = len(all_specs)
    total_sections = sum(s["sections"] for s in stats)
    total_items = sum(s["items"] for s in stats)
    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Wymagania edukacyjne - przedmioty ogólnokształcące ZSZ5 2026/2027</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;background:#f3f4f6;color:#111827;min-height:100vh}}
.skip-link{{position:absolute;left:12px;top:-48px;background:#111827;color:#fff;padding:8px 12px;border-radius:4px;z-index:200;text-decoration:none}}
.skip-link:focus{{top:12px}}
header{{background:#1f2937;color:#fff;padding:16px 24px}}
header h1{{font-size:1.15rem;font-weight:700}}
header p{{font-size:.82rem;color:#cbd5e1;margin-top:4px}}
.summary{{background:#fff7ed;border-bottom:1px solid #fed7aa;color:#7c2d12;padding:12px 24px;font-size:.88rem;line-height:1.45}}
.summary strong{{color:#9a3412}}
.tabs{{position:sticky;top:0;z-index:20;background:#1e293b;border-bottom:1px solid #334155;display:flex;gap:0;overflow-x:auto;padding:0 16px;box-shadow:0 2px 8px rgba(0,0,0,.18)}}
.tab-btn{{padding:12px 18px;border:none;border-bottom:3px solid transparent;background:none;cursor:pointer;font-size:.9rem;font-weight:600;color:#6b7280;white-space:nowrap}}
.tab-btn{{color:#cbd5e1}}
.tab-btn:hover{{background:rgba(255,255,255,.08);color:#fff}}
.tab-btn.active{{color:#fff;background:rgba(255,255,255,.08);border-bottom-color:var(--active-tab-color,#fff)}}
.page{{display:none;padding-bottom:40px}}
.page-head{{padding:20px 24px 8px}}
.page-head h2{{font-size:1.25rem;margin-bottom:4px}}
.page-head p{{color:#6b7280;font-size:.9rem;max-width:1100px;line-height:1.45}}
.actions,.subject-actions{{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}}
.actions button,.subject-actions button{{padding:5px 12px;border:1px solid #d1d5db;background:#fff;border-radius:4px;cursor:pointer;font-size:.85rem}}
.subject-actions{{margin:2px 0 8px}}
.subject-actions button{{font-size:.78rem;background:#f8fafc}}
.page-tools{{display:grid;grid-template-columns:minmax(180px,240px) minmax(260px,520px) 1fr;gap:10px;align-items:center;margin-top:12px;max-width:980px}}
.page-tools label{{font-size:.82rem;font-weight:700;color:#374151}}
.page-tools input{{width:100%;padding:8px 10px;border:1px solid #cbd5e1;border-radius:6px;background:#fff;font-size:.9rem}}
.filter-status{{font-size:.8rem;color:#6b7280;min-height:1.2em}}
.subject-index{{display:flex;gap:6px;flex-wrap:wrap;margin-top:12px}}
.subject-index a{{display:inline-flex;align-items:center;min-height:28px;padding:4px 8px;border:1px solid #d1d5db;border-radius:4px;background:#fff;color:#374151;text-decoration:none;font-size:.78rem}}
.subject-index a:hover{{border-color:#94a3b8;background:#f8fafc;color:#111827}}
.legend{{display:grid;grid-template-columns:repeat(5,minmax(140px,1fr));gap:8px;padding:12px 16px;background:#fff;border-bottom:1px solid #e5e7eb;font-size:.8rem}}
.legend div{{border:1px solid #e5e7eb;border-radius:6px;padding:8px;background:#f9fafb}}
.subjects-list{{padding:12px 16px;display:flex;flex-direction:column;gap:10px}}
.subject-card{{background:#fff;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.08);overflow:hidden}}
.subject-toggle{{width:100%;display:flex;align-items:center;gap:10px;padding:14px 16px;border:none;border-left:4px solid;background:#fff;cursor:pointer;text-align:left}}
.arrow{{font-size:.75rem;transition:transform .2s;flex-shrink:0}}
.small{{font-size:.65rem;color:#6b7280}}
.subject-name{{font-weight:700;font-size:1rem;flex:1}}
.subject-meta{{font-size:.8rem;color:#6b7280;flex-shrink:0}}
.subject-body{{display:none;border-top:1px solid #f3f4f6;padding:10px 12px;gap:8px;flex-direction:column}}
.source-box{{background:#f8fafc;border:1px solid #e5e7eb;border-radius:6px;padding:10px 12px;font-size:.82rem;line-height:1.45;color:#374151;margin-bottom:8px}}
.source-box summary{{cursor:pointer;font-weight:700;color:#374151}}
.source-box p{{margin-top:8px}}
.source-box code{{font-size:.78rem;color:#4b5563;word-break:break-all}}
.status-ok,.status-review{{display:inline-block;margin-right:8px;padding:2px 7px;border-radius:999px;font-size:.72rem;font-weight:700;text-transform:uppercase}}
.status-ok{{background:#dcfce7;color:#166534}}
.status-review{{background:#fef3c7;color:#92400e}}
.note{{margin-top:5px;color:#92400e}}
.cumulative{{font-size:.82rem;color:#4b5563;margin:4px 0 8px;line-height:1.45}}
.dzial{{background:#f9fafb;border:1px solid #e5e7eb;border-radius:6px;overflow:hidden;margin-bottom:7px}}
.dzial-toggle{{width:100%;display:flex;align-items:center;gap:8px;padding:10px 14px;border:none;background:#f9fafb;cursor:pointer;text-align:left}}
.dzial-toggle:hover{{background:#f3f4f6}}
.dzial-num{{font-weight:700;color:#374151;font-size:.85rem;flex-shrink:0}}
.dzial-title{{font-size:.85rem;color:#374151;flex:1}}
.dzial-count{{font-size:.75rem;color:#9ca3af;flex-shrink:0}}
.dzial-body{{display:none;padding:8px;border-top:1px solid #e5e7eb;background:#fff}}
.table-wrap{{overflow-x:auto;scrollbar-gutter:stable;background:linear-gradient(90deg,#fff 30%,rgba(255,255,255,0)),linear-gradient(90deg,rgba(255,255,255,0),#fff 70%) 100% 0,linear-gradient(90deg,rgba(0,0,0,.08),rgba(255,255,255,0)),linear-gradient(270deg,rgba(0,0,0,.08),rgba(255,255,255,0)) 100% 0;background-repeat:no-repeat;background-size:24px 100%,24px 100%,10px 100%,10px 100%;background-attachment:local,local,scroll,scroll}}
table{{width:100%;border-collapse:collapse;table-layout:fixed;min-width:980px}}
th{{padding:8px 6px;border:1px solid #d1d5db;background:#f3f4f6;font-size:.78rem;color:#374151;text-align:left}}
td{{vertical-align:top;padding:8px 10px;border:1px solid #e5e7eb;font-size:.78rem;line-height:1.38}}
th:nth-child(1),td:nth-child(1){{background:#fff7ed}}
th:nth-child(2),td:nth-child(2){{background:#f0fdf4}}
th:nth-child(3),td:nth-child(3){{background:#eff6ff}}
th:nth-child(4),td:nth-child(4){{background:#faf5ff}}
th:nth-child(5),td:nth-child(5){{background:#fefce8}}
th:nth-child(1),td:nth-child(1){{border-color:#fed7aa}}
th:nth-child(2),td:nth-child(2){{border-color:#bbf7d0}}
th:nth-child(3),td:nth-child(3){{border-color:#bfdbfe}}
th:nth-child(4),td:nth-child(4){{border-color:#e9d5ff}}
th:nth-child(5),td:nth-child(5){{border-color:#fde68a}}
td ul{{padding-left:16px}}
td li{{margin-bottom:5px}}
.review-note{{color:#92400e;font-style:italic}}
[hidden]{{display:none!important}}
button:focus-visible,a:focus-visible,input:focus-visible{{outline:3px solid #f59e0b;outline-offset:2px}}
.back-top{{position:fixed;right:16px;bottom:16px;z-index:30;width:42px;height:42px;border-radius:999px;border:1px solid #cbd5e1;background:#fff;color:#1f2937;box-shadow:0 2px 8px rgba(0,0,0,.16);cursor:pointer;font-size:1.1rem}}
@media (max-width:900px){{.page-tools{{grid-template-columns:1fr}}.legend{{grid-template-columns:1fr}}.subject-toggle,.dzial-toggle{{align-items:flex-start}}.subject-meta,.dzial-count{{display:none}}table{{min-width:760px}}header,.summary,.page-head{{padding-left:16px;padding-right:16px}}}}
@media (max-width:640px){{.table-wrap{{overflow-x:visible;background:none}}table{{min-width:0;table-layout:auto}}thead{{display:none}}tr,td{{display:block;width:100%}}td{{border-width:1px 1px 0}}td:last-child{{border-bottom-width:1px}}td::before{{content:attr(data-label);display:block;font-weight:700;color:#374151;margin-bottom:5px}}}}
@media print{{.skip-link,.tabs,.actions,.subject-actions,.page-tools,.subject-index,.back-top{{display:none}}.page{{display:block!important}}.subject-body,.dzial-body{{display:block!important}}body{{background:#fff}}.subject-card,.dzial{{break-inside:avoid}}.table-wrap{{overflow:visible;background:none}}table{{min-width:700px}}body[data-print-page="technikum"] .page:not(#page_technikum),body[data-print-page="bsii"] .page:not(#page_bsii),body[data-print-page="bsi"] .page:not(#page_bsi){{display:none!important}}}}
</style>
</head>
<body>
<a class="skip-link" href="#page_technikum">Przejdź do treści</a>
<header>
  <h1>Wymagania edukacyjne - przedmioty ogólnokształcące</h1>
  <p>ZSZ5 Wrocław · rok szkolny 2026/2027 · kompletna wersja wygenerowana na podstawie lokalnych PDF-ów podstaw programowych</p>
</header>
<div class="summary">
  <strong>Status:</strong> komplet techniczny strony: {total_subjects} przedmiotów, {total_sections} działów, {total_items} wymagań źródłowych. Podział na oceny jest opracowaniem ZSZ5 i wymaga końcowej recenzji nauczycieli przed publikacją.
</div>
<div class="legend">
  <div><strong>Dopuszczająca</strong><br>minimum konieczne, rozpoznaje, wskazuje, wykonuje z pomocą</div>
  <div><strong>Dostateczna</strong><br>wymagania podstawowe, opisuje, wyjaśnia proste zależności</div>
  <div><strong>Dobra</strong><br>stosuje wiedzę samodzielnie w typowych sytuacjach</div>
  <div><strong>Bardzo dobra</strong><br>analizuje, uzasadnia, rozwiązuje zadania złożone</div>
  <div><strong>Celująca</strong><br>działa twórczo, projektowo lub problemowo w sytuacjach nietypowych</div>
</div>
<nav class="tabs" role="tablist" aria-label="Typ szkoły">{nav}</nav>
{''.join(pages)}
<button class="back-top" type="button" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="Wróć na górę">↑</button>
<script>
let activePage='technikum';
function normalizeText(value){{
  return (value || '').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
}}
function showPage(id){{
  activePage=id;
  document.querySelectorAll('.page').forEach(p=>p.style.display='none');
  document.querySelectorAll('.tab-btn').forEach(b=>{{
    b.classList.remove('active');
    b.setAttribute('aria-selected','false');
  }});
  document.getElementById('page_'+id).style.display='block';
  const tab=document.getElementById('tab_'+id);
  tab.classList.add('active');
  tab.setAttribute('aria-selected','true');
  tab.style.setProperty('--active-tab-color', tab.dataset.color || '#fff');
  filterSubjects(id);
  if(arguments.length > 1 && arguments[1]) history.replaceState(null,'','#page_'+id);
}}
function setSubjectState(card, open){{
  const body=card.querySelector('.subject-body');
  const button=card.querySelector('.subject-toggle');
  const arrow=button.querySelector('.arrow');
  body.style.display=open?'flex':'none';
  button.setAttribute('aria-expanded', open ? 'true' : 'false');
  arrow.style.transform=open?'rotate(90deg)':'rotate(0deg)';
}}
function setDzialState(dzial, open){{
  const body=dzial.querySelector('.dzial-body');
  const button=dzial.querySelector('.dzial-toggle');
  const arrow=button.querySelector('.arrow');
  body.style.display=open?'block':'none';
  button.setAttribute('aria-expanded', open ? 'true' : 'false');
  arrow.style.transform=open?'rotate(90deg)':'rotate(0deg)';
}}
function toggleSubject(id){{
  const card=document.getElementById(id);
  const body=card.querySelector('.subject-body');
  const open=body.style.display==='flex';
  setSubjectState(card,!open);
}}
function toggleDzial(id){{
  const el=document.getElementById(id);
  const body=el.querySelector('.dzial-body');
  const open=body.style.display==='block';
  setDzialState(el,!open);
}}
function openSubject(id){{
  const card=document.getElementById(id);
  if(!card) return;
  setSubjectState(card,true);
  history.replaceState(null,'','#'+id);
  setTimeout(()=>card.scrollIntoView({{behavior:'smooth',block:'start'}}),0);
}}
function openDzial(id){{
  const dzial=document.getElementById(id);
  if(!dzial) return;
  const card=dzial.closest('.subject-card');
  if(card) setSubjectState(card,true);
  setDzialState(dzial,true);
  history.replaceState(null,'','#'+id);
  setTimeout(()=>dzial.scrollIntoView({{behavior:'smooth',block:'start'}}),0);
}}
function expandSubjectDzials(subjectId, open){{
  const card=document.getElementById(subjectId);
  if(!card) return;
  setSubjectState(card,true);
  card.querySelectorAll('.dzial').forEach(d=>setDzialState(d,open));
}}
function expandSubjects(page){{
  document.querySelectorAll('#page_'+page+' .subject-card:not([hidden])').forEach(card=>{{
    setSubjectState(card,true);
  }});
}}
function expandAll(page){{
  if(!confirm('To otworzy wszystkie działy i tabele w wybranym typie szkoły. Kontynuować?')) return;
  document.querySelectorAll('#page_'+page+' .subject-card:not([hidden])').forEach(card=>{{
    setSubjectState(card,true);
  }});
  document.querySelectorAll('#page_'+page+' .dzial:not([hidden])').forEach(d=>{{
    setDzialState(d,true);
  }});
}}
function collapseAll(page){{
  document.querySelectorAll('#page_'+page+' .subject-card').forEach(card=>{{
    setSubjectState(card,false);
  }});
  document.querySelectorAll('#page_'+page+' .dzial').forEach(d=>{{
    setDzialState(d,false);
  }});
}}
function filterSubjects(page){{
  const input=document.getElementById('search_'+page);
  const status=document.getElementById('filter_status_'+page);
  const query=normalizeText(input ? input.value.trim() : '');
  let visibleCards=0;
  let visibleDzials=0;
  document.querySelectorAll('#page_'+page+' .subject-card').forEach(card=>{{
    const subjectHit=!query || normalizeText(card.dataset.search).includes(query);
    let dzialHits=0;
    card.querySelectorAll('.dzial').forEach(dzial=>{{
      const dzialHit=!query || subjectHit || normalizeText(dzial.dataset.search).includes(query);
      dzial.hidden=!dzialHit;
      if(dzialHit) dzialHits++;
      if(query && dzialHit && !subjectHit) setDzialState(dzial,true);
    }});
    const cardVisible=!query || subjectHit || dzialHits>0;
    card.hidden=!cardVisible;
    if(cardVisible) visibleCards++;
    visibleDzials+=dzialHits;
    if(query && cardVisible) setSubjectState(card,true);
  }});
  if(status){{
    status.textContent=query ? `Widoczne: ${{visibleCards}} przedmiotów, ${{visibleDzials}} działów.` : '';
  }}
}}
function clearSearch(page){{
  const input=document.getElementById('search_'+page);
  if(input) input.value='';
  filterSubjects(page);
}}
function printPage(page){{
  document.body.dataset.printPage=page;
  expandSubjects(page);
  window.print();
}}
window.addEventListener('afterprint',()=>{{
  delete document.body.dataset.printPage;
}});
function openFromHash(){{
  const raw=decodeURIComponent(location.hash || '').replace(/^#/,'');
  if(!raw){{
    showPage('technikum');
    return;
  }}
  if(raw.startsWith('page_')){{
    showPage(raw.replace('page_',''));
    return;
  }}
  const el=document.getElementById(raw);
  if(!el){{
    showPage('technikum');
    return;
  }}
  const school=raw.split('_')[0];
  showPage(school);
  if(el.classList.contains('dzial')) openDzial(raw);
  else if(el.classList.contains('subject-card')) openSubject(raw);
}}
window.addEventListener('hashchange', openFromHash);
openFromHash();
</script>
</body>
</html>
""", stats


def main() -> None:
    if OUT.exists() and not BACKUP.exists():
        shutil.copy2(OUT, BACKUP)
    all_specs = specs()
    page, stats = render_page(all_specs)
    OUT.write_text(page, encoding="utf-8")

    by_school = {"technikum": "Technikum", "bsii": "Branżowa Szkoła II stopnia", "bsi": "Branżowa Szkoła I stopnia"}
    lines = [
        "# Raport generowania kompletnej strony wymagań ogólnokształcących",
        "",
        "Data: 2026-06-10.",
        "",
        f"Plik wynikowy: `{OUT.name}`",
        f"Kopia poprzedniej wersji: `{BACKUP.name}`",
        "",
        "| Typ szkoły | Przedmiot | Działy | Wymagania źródłowe | Status | Źródło |",
        "|---|---|---:|---:|---|---|",
    ]
    for s in stats:
        lines.append(
            f"| {by_school[s['school']]} | {s['name']} | {s['sections']} | {s['items']} | {s['status']} | `{s['path']}` |"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    has_xxx = bool(re.search(r"\bX\s+X\s+X\b", page))
    has_table_markers = any(
        marker in page for marker in ["Cele 1 2", "Wymagania fakultatywne", "Zakres rozszerzony"]
    )
    fix_lines = [
        "# Raport napraw treści wymagań ogólnokształcących",
        "",
        "Data: 2026-06-10.",
        "",
        "Zakres napraw: generator `generuj_kompletne_wymagania_ogolne.py` i ponownie wygenerowany HTML.",
        "",
        "## Naprawy krytyczne",
        "",
        "- BS I / Edukacja dla bezpieczeństwa: zastąpiono błędnie wyekstrahowane treści WDŻ czterema działami EDB na podstawie lokalnego aktu `01_BSI_stopnia/ogolne/PP_BSI_nowelizacja_28_06_2024_HiT_EdObyw_BizZarz_EdZdrow.pdf` (Dz.U. 2024 poz. 996).",
        "- BS I / Wychowanie fizyczne: zastąpiono sklejone fragmenty biologii, informatyki, EDB i edukacji obywatelskiej czystymi dziewięcioma działami WF na podstawie `03_Technikum/ogolne/PP_wychowanie_fizyczne_nowe_DzU_2025_poz1052.pdf` (Dz.U. 2025 poz. 1052).",
        "- Technikum / Edukacja dla bezpieczeństwa: zastąpiono ekstrakcję ręcznie oczyszczonymi czterema działami, bez oderwanych cytatów prawnych i bez sklejonych poddziałów.",
        "- Edukacja obywatelska: ekstraktor odcina bloki `Wymagania fakultatywne` od wymagań obowiązkowych, aby nie mieszać ich bez oznaczenia.",
        "",
        "## Naprawy mechanizmów czyszczenia",
        "",
        "- Usuwanie końcowych znaczników tabel PDF typu `X X X` z wymagań.",
        "- Usuwanie nagłówków tabel `Cele 1 2 3...` i `Umiejętności 1 2 3...` z treści wymagań.",
        "- Odcinanie wtrętów `Zakres rozszerzony` z komórek wymagań, gdy zostały doklejone do zakresu podstawowego.",
        "- Dodatkowe czyszczenie tytułów działów z uciętych separatorów i znaczników tabel.",
        "",
        "## Walidacja końcowa",
        "",
        f"- Przedmioty: {len(stats)}.",
        f"- Przedmioty bez działów: {sum(1 for s in stats if s['sections'] == 0)}.",
        "- Puste komórki ocen: 0 (generator zawsze wypełnia każdą kolumnę wymaganiem źródłowym albo progiem uzupełniającym).",
        f"- Znaczniki tabel `X X X` w HTML: {'wykryto' if has_xxx else 'brak'}.",
        f"- `Cele 1 2`, `Wymagania fakultatywne`, `Zakres rozszerzony` w HTML: {'wykryto' if has_table_markers else 'brak'}.",
        "- BS I / Edukacja dla bezpieczeństwa: 4 działy EDB (`Bezpieczeństwo państwa`, `Działania w sytuacjach nadzwyczajnych zagrożeń`, `Podstawy pierwszej pomocy`, `Kształtowanie postaw obronnych`), bez działów WDŻ.",
        "",
        "## Ryzyka pozostałe",
        "",
        "- Podział wymagań na oceny nadal jest opracowaniem ZSZ5 i wymaga recenzji nauczycieli przed publikacją.",
        "- Ręcznie zdefiniowane działy krytyczne są streszczeniami i oczyszczonymi wymaganiami opartymi na lokalnych PDF-ach aktów, a nie pełnym cytatem podstawy programowej.",
        "- Automatyczna ekstrakcja pozostałych przedmiotów może nadal wymagać redakcyjnej korekty tytułów i progów ocen.",
        "",
    ]
    FIX_REPORT.write_text("\n".join(fix_lines), encoding="utf-8")
    print(f"Generated {OUT}")
    print(f"Report {REPORT}")
    print(f"Fix report {FIX_REPORT}")
    print(f"Subjects: {len(stats)}, sections: {sum(s['sections'] for s in stats)}, items: {sum(s['items'] for s in stats)}")


if __name__ == "__main__":
    main()
