from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LEGACY_ENTRY = "wymagania_edukacyjne_ZSZ5_2026_2027.html"
SCHEDULE_TEMPLATE = "rozkłady materiału przedmiotów/rozkład materiału - szablon 2026_2027.xlsx"


@dataclass(frozen=True)
class Page:
    file_name: str
    nav_label: str
    title: str
    lead: str
    body: str


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#f3f0e9;--paper:#fffdf8;--ink:#172033;--muted:#647084;--line:#d9d5cc;--navy:#172a46;--blue:#2b67d1;--teal:#245e58;--gold:#d99b2b;--green:#2e8b68;--red:#c94c4c;--shadow:0 12px 30px rgba(23,32,51,.08);--soft-shadow:0 8px 20px rgba(23,32,51,.06)}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;background:var(--bg);color:var(--ink);min-height:100vh;font-size:15px;line-height:1.55}
a{color:inherit}
.skip-link{position:absolute;left:12px;top:-48px;background:var(--navy);color:#fff;padding:8px 12px;border-radius:999px;z-index:20;text-decoration:none}
.skip-link:focus{top:12px}
header{background:var(--paper);border-bottom:1px solid rgba(23,32,51,.08);padding:14px 24px}
.brand{display:flex;align-items:center;gap:16px;max-width:1120px;margin:0 auto}
.brand-logo{width:82px;height:58px;object-fit:contain;flex-shrink:0}
header h1{font-size:1.18rem;line-height:1.2}
header p{font-size:.86rem;color:var(--muted);margin-top:5px;max-width:820px}
.topbar{position:sticky;top:0;z-index:10;background:rgba(243,240,233,.95);border-bottom:1px solid var(--line);backdrop-filter:blur(12px)}
.topbar-inner{max-width:1120px;margin:0 auto;padding:9px 18px;display:flex;gap:8px;flex-wrap:wrap}
.nav-link,.btn{display:inline-flex;align-items:center;justify-content:center;min-height:32px;padding:6px 11px;border-radius:999px;text-decoration:none;font-size:.82rem;font-weight:850}
.nav-link{background:#fff;border:1px solid var(--line);color:#345070}
.nav-link.active,.nav-link.primary,.btn.primary{background:#eef4fb;color:#1d4f9a;border:1px solid #b9d4f7}
main{padding-bottom:46px}
.hero{max-width:1120px;margin:22px auto 0;padding:28px 22px;background:var(--navy);color:#fff;border-radius:8px;box-shadow:var(--shadow)}
.eyebrow{font-size:.74rem;text-transform:uppercase;letter-spacing:.12em;color:#8fd4dd;font-weight:850}
.hero h2{font-size:clamp(1.45rem,3vw,2.25rem);line-height:1.1;margin-top:6px;max-width:900px}
.hero p{color:#c8d1df;font-size:.96rem;margin-top:12px;max-width:920px}
.hero-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
.hero-actions a{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.26);color:#fff}
.section{max-width:1120px;margin:0 auto;padding:24px 22px 0}
.section h3{font-size:1.08rem;color:var(--ink);margin-bottom:10px}
.section h4{font-size:.95rem;color:var(--navy);margin-bottom:7px}
.section>p{font-size:.9rem;color:#374151;line-height:1.65;margin-bottom:14px;max-width:960px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.card{background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;padding:16px;box-shadow:var(--soft-shadow)}
.card p,.card li{font-size:.85rem;color:#374151;line-height:1.55}
.card ul,.number-list{padding-left:18px;margin-top:8px}
.card li,.number-list li{margin-bottom:5px}
.resource-grid .card{display:flex;flex-direction:column;gap:8px}
.btn{align-self:flex-start;margin-top:auto;border:1px solid var(--line);background:#fff;color:var(--ink)}
.source-note{font-size:.76rem;color:var(--muted);margin-top:8px}
.callout{background:#e8f6f4;border:1px solid #b8ddd7;border-radius:8px;padding:15px;margin-top:14px;color:var(--teal)}
.callout.warning{background:#fff7df;border-color:#ecd6a4;color:#6d5828}
.callout h4{font-size:.92rem;margin-bottom:6px;color:inherit}
.callout p,.callout li{font-size:.86rem;line-height:1.55}
.callout ul{padding-left:18px;margin-top:6px}
.process-lab{display:grid;grid-template-columns:minmax(280px,.95fr) minmax(320px,1.05fr);gap:14px;margin-top:14px}
.process-track{display:grid;gap:8px}
.process-step{display:grid;grid-template-columns:34px 1fr;gap:10px;align-items:center;width:100%;min-height:64px;text-align:left;background:var(--paper);border:1px solid rgba(23,32,51,.1);border-radius:8px;padding:10px 12px;color:var(--ink);box-shadow:0 6px 16px rgba(23,32,51,.04);cursor:pointer}
.process-step:hover{border-color:#b9d4f7;background:#fff}
.process-step.active{background:#eef4fb;border-color:var(--blue);box-shadow:0 10px 24px rgba(43,103,209,.13)}
.step-num{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:999px;background:var(--navy);color:#fff;font-size:.8rem;font-weight:850}
.process-step.active .step-num{background:var(--blue)}
.process-step strong{display:block;font-size:.88rem;line-height:1.2}
.process-step small{display:block;margin-top:3px;color:var(--muted);font-size:.74rem;line-height:1.25}
.process-panel{background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;padding:18px;box-shadow:var(--shadow);align-self:stretch}
.process-panel-head{margin-bottom:12px}
.process-panel-head .eyebrow{color:var(--blue)}
.process-panel h4{font-size:1.18rem;line-height:1.2;margin-top:5px}
.process-panel-grid{display:grid;gap:10px}
.process-panel-grid div{background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px}
.process-panel-grid strong{display:block;color:var(--navy);font-size:.82rem;margin-bottom:5px;text-transform:uppercase;letter-spacing:.05em}
.process-panel-grid p{font-size:.88rem;color:#374151;line-height:1.55}
.preview-grid{display:grid;grid-template-columns:1fr;gap:14px;margin-top:14px}
.preview-card{background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;box-shadow:var(--soft-shadow);overflow:hidden}
.preview-card h4{padding:13px 14px 0}
.preview-card p{padding:4px 14px 12px;font-size:.84rem;color:#374151}
.preview-card img{display:block;width:100%;height:auto;border-top:1px solid var(--line);background:#fff}
.table-wrap{overflow-x:auto;scrollbar-gutter:stable;background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;box-shadow:var(--soft-shadow);margin-top:14px}
.sample-table{width:100%;border-collapse:collapse;min-width:900px}
.sample-table th,.sample-table td{border-bottom:1px solid var(--line);border-right:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;font-size:.8rem;line-height:1.4}
.sample-table th{background:#eef4fb;color:#1d4f9a;font-weight:850}
.sample-table td{background:#fff}
.sample-table tr:last-child td{border-bottom:none}
.sample-table th:last-child,.sample-table td:last-child{border-right:none}
.column-guide{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-top:14px}
.column-item{background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;padding:12px;box-shadow:0 6px 16px rgba(23,32,51,.04)}
.column-item strong{display:block;color:var(--navy);font-size:.86rem;margin-bottom:4px}
.column-item p{font-size:.82rem;color:#374151;line-height:1.5}
.legal-ref{display:inline-block;margin-bottom:7px;padding:4px 8px;border-radius:999px;background:#eef4fb;color:#345070;border:1px solid #dce9f7;font-size:.74rem;font-weight:850}
button:focus-visible,a:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
@media (max-width:860px){body{font-size:14px}.brand{align-items:flex-start}.brand-logo{width:68px;height:48px}.hero{margin:14px 12px 0;padding:20px 16px}.section{padding-left:12px;padding-right:12px}.topbar-inner{padding-left:12px;padding-right:12px}.process-lab{grid-template-columns:1fr}}
@media (max-width:560px){header{padding:10px 14px}.brand-logo{width:58px;height:42px}header h1{font-size:1.04rem}header p{display:none}.hero h2{font-size:1.42rem}.hero p{font-size:.88rem}.card,.process-step,.process-panel,.column-item{padding:12px}.process-step{grid-template-columns:30px 1fr;min-height:58px}}
@media print{.skip-link,.topbar,.hero-actions{display:none}body{background:#fff}.card,.process-panel,.process-step,.column-item,.preview-card{break-inside:avoid}}
"""


def page_shell(page: Page, pages: list[Page]) -> str:
    nav = "\n".join(
        f'<a class="nav-link{" active" if item.file_name == page.file_name else ""}" href="{item.file_name}">{item.nav_label}</a>'
        for item in pages
    )
    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{page.title} | ZSZ5 2026/2027</title>
<link rel="icon" href="assets/logo-zsz5-black.png">
<style>{CSS}</style>
</head>
<body>
<a class="skip-link" href="#main_content">Przejdź do treści</a>
<header>
  <div class="brand">
    <img class="brand-logo" src="assets/logo-zsz5-black.png" alt="Logotyp ZSZ5 we Wrocławiu">
    <div>
      <h1>Przewodnik dla nauczyciela ZSZ5 2026/2027</h1>
      <p>Od podstawy programowej przez rozkład materiału do wymagań edukacyjnych i zasad oceniania.</p>
    </div>
  </div>
</header>
<nav class="topbar" aria-label="Nawigacja">
  <div class="topbar-inner">
    {nav}
    <a class="nav-link primary" href="katalog_podstaw_programowych_ZSZ5_2026_2027.html">Katalog podstaw programowych</a>
  </div>
</nav>
<main id="main_content">
  <section class="hero">
    <p class="eyebrow">ZSZ5 · rok szkolny 2026/2027</p>
    <h2>{page.title}</h2>
    <p>{page.lead}</p>
    <div class="hero-actions">
      <a class="nav-link" href="rozklad_materialu.html">Przejdź do rozkładu materiału</a>
      <a class="nav-link" href="{SCHEDULE_TEMPLATE}">Otwórz szablon XLSX</a>
    </div>
  </section>
{page.body}
</main>
<script>
function setProcessStep(button){{
  document.querySelectorAll('.process-step').forEach(item=>{{
    const active=item===button;
    item.classList.toggle('active', active);
    item.setAttribute('aria-pressed', active ? 'true' : 'false');
  }});
  document.getElementById('process_step_num').textContent=button.dataset.step;
  document.getElementById('process_title').textContent=button.dataset.title;
  document.getElementById('process_teacher').textContent=button.dataset.teacher;
  document.getElementById('process_output').textContent=button.dataset.output;
  document.getElementById('process_check').textContent=button.dataset.check;
}}
</script>
</body>
</html>
"""


START_BODY = """
<section class="section">
  <h3>Ścieżka pracy</h3>
  <p>Praca nauczyciela rozpoczyna się od analizy podstawy programowej. Następnie jej zapisy należy przełożyć na program nauczania, rozkład materiału, wymagania edukacyjne oraz sposoby sprawdzania osiągnięć uczniów.</p>
  <div class="process-lab" aria-label="Ścieżka od podstawy programowej do oceny ucznia">
    <div class="process-track" role="list">
      <button class="process-step active" type="button" role="listitem" aria-pressed="true" data-step="1" data-title="Podstawa programowa" data-teacher="Analizę obowiązkowych celów, treści, efektów kształcenia i kryteriów wskazanych w przepisach." data-output="Zestawienie elementów obowiązkowych w danym przedmiocie lub kwalifikacji." data-check="Podstawa programowa pozostaje nadrzędna wobec propozycji z podręcznika lub tabeli wydawnictwa." onclick="setProcessStep(this)">
        <span class="step-num">1</span><span><strong>Podstawa programowa</strong><small>Co jest obowiązkowe</small></span>
      </button>
      <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="2" data-title="Program nauczania" data-teacher="Program nauczania wybrany z oferty wydawnictwa, zmodyfikowany albo opracowany samodzielnie z zachowaniem zgodności z podstawą." data-output="Program pokazujący sposób realizacji podstawy programowej w danym oddziale." data-check="Adaptacja programu może obejmować tempo, kolejność treści i dobór ćwiczeń dostosowanych do potrzeb klasy." onclick="setProcessStep(this)">
        <span class="step-num">2</span><span><strong>Program nauczania</strong><small>Jak realizujemy podstawę</small></span>
      </button>
      <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="3" data-title="Rozkład materiału" data-teacher="Układ działów, tematów, ćwiczeń, powtórzeń, projektów oraz orientacyjny czas pracy." data-output="Realny plan pracy na rok lub semestr dla konkretnej klasy." data-check="Rozkład powinien pokazywać realizację podstawy, tempo pracy i momenty sprawdzania osiągnięć." onclick="setProcessStep(this)">
        <span class="step-num">3</span><span><strong>Rozkład materiału</strong><small>Kolejność i tempo pracy</small></span>
      </button>
      <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="4" data-title="Wymagania edukacyjne" data-teacher="Opis wymagań wskazujący, co uczeń powinien wiedzieć i umieć na poszczególne oceny." data-output="Zestaw wymagań na ocenę dopuszczającą, dostateczną, dobrą, bardzo dobrą i celującą." data-check="Wymagania powinny wynikać z realizowanego programu i podstawy programowej, a nie z ogólnych haseł." onclick="setProcessStep(this)">
        <span class="step-num">4</span><span><strong>Wymagania edukacyjne</strong><small>Poziomy na oceny</small></span>
      </button>
      <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="5" data-title="Sprawdzanie" data-teacher="Dobór sprawdzianów, odpowiedzi, zadań praktycznych, projektów i obserwacji pracy ucznia do wcześniej przedstawionych wymagań." data-output="Dowody uczenia się: prace, wypowiedzi, działania praktyczne, wyniki zadań i projekty." data-check="Sprawdzanie osiągnięć powinno obejmować treści i umiejętności wcześniej wskazane w wymaganiach oraz przećwiczone podczas zajęć." onclick="setProcessStep(this)">
        <span class="step-num">5</span><span><strong>Sprawdzanie</strong><small>Dowody wiedzy i umiejętności</small></span>
      </button>
      <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="6" data-title="Ocena ucznia" data-teacher="Zestawienie osiągnięć ucznia z wymaganiami edukacyjnymi i zasadami oceniania." data-output="Ocena bieżąca, śródroczna lub roczna uzasadniona konkretnymi wymaganiami." data-check="Ocena powinna wynikać z rozpoznanych osiągnięć ucznia, a nie wyłącznie z realizacji kolejnych tematów." onclick="setProcessStep(this)">
        <span class="step-num">6</span><span><strong>Ocena ucznia</strong><small>Uzasadniony wynik</small></span>
      </button>
    </div>
    <div class="process-panel" aria-live="polite">
      <div class="process-panel-head">
        <span class="eyebrow">aktywny etap</span>
        <h4><span id="process_step_num">1</span>. <span id="process_title">Podstawa programowa</span></h4>
      </div>
      <div class="process-panel-grid">
        <div><strong>Nauczyciel przygotowuje</strong><p id="process_teacher">Analizę obowiązkowych celów, treści, efektów kształcenia i kryteriów wskazanych w przepisach.</p></div>
        <div><strong>Efekt pracy</strong><p id="process_output">Zestawienie elementów obowiązkowych w danym przedmiocie lub kwalifikacji.</p></div>
        <div><strong>Warto zwrócić uwagę</strong><p id="process_check">Podstawa programowa pozostaje nadrzędna wobec propozycji z podręcznika lub tabeli wydawnictwa.</p></div>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <h3>Najważniejsze kroki przed 1 września</h3>
  <div class="cards">
    <div class="card"><h4>1. Analiza podstawy</h4><p>Należy ustalić, które elementy podstawy programowej dotyczą danego przedmiotu, klasy, zawodu lub kwalifikacji.</p></div>
    <div class="card"><h4>2. Przygotowanie rozkładu</h4><p>Rozkład materiału powinien pokazywać tematy, liczbę godzin i elementy podstawy realizowane przy każdym temacie.</p></div>
    <div class="card"><h4>3. Powiązanie wymagań</h4><p>Wymagania edukacyjne i zasady oceniania muszą być jasne dla uczniów oraz uwzględnione w pracy nauczyciela od początku roku.</p></div>
  </div>
</section>
"""


SCHEDULE_BODY = f"""
<section class="section">
  <h3>Dlaczego rozkład materiału jest potrzebny</h3>
  <p>Każdy nauczyciel powinien mieć przygotowany rozkład materiału. To dokument, który przekłada podstawę programową i program nauczania na konkretne tematy, kolejność pracy, liczbę godzin oraz wymagania realizowane w czasie lekcji.</p>
  <div class="cards">
    <div class="card">
      <h4>Zakres informacji w rozkładzie</h4>
      <ul>
        <li>jakie tematy lub działy są realizowane,</li>
        <li>ile godzin zaplanowano na poszczególne części,</li>
        <li>które elementy podstawy programowej są realizowane przy konkretnym temacie,</li>
        <li>czy cała podstawa programowa została zaplanowana,</li>
        <li>gdzie pojawiają się wymagania edukacyjne i sprawdzanie osiągnięć.</li>
      </ul>
    </div>
    <div class="card">
      <h4>Struktura arkusza</h4>
      <p>Jeżeli przedmiot jest nauczany przez wiele lat, rozkład może być prowadzony w jednym arkuszu, np. język polski na pięć lat albo informatyka na dwa lata. Dopuszczalne jest także prowadzenie osobnych arkuszy lub plików dla pojedynczych lat szkolnych.</p>
    </div>
    <div class="card">
      <h4>Materiały wydawnictw</h4>
      <p>Wiele wydawnictw publikuje gotowe rozkłady materiału oraz plany wynikowe. Często wystarczające jest połączenie tych dwóch źródeł, sprawdzenie zgodności z podstawą programową i dostosowanie materiału do realnej pracy z klasą.</p>
    </div>
  </div>
  <div class="callout warning">
    <h4>Termin przygotowania</h4>
    <p>Rozkład materiału należy przygotować przed 1 września 2026 r. Istniejące rozkłady, które nauczyciele przygotowali w dzienniku elektronicznym, są jeszcze dostępne, ale w sobotę 29 sierpnia 2026 r. zostaną usunięte. Rozkłady należy przygotować do piątku 28 sierpnia 2026 r., aby od 1 września rozpocząć pracę w uporządkowanym dzienniku.</p>
  </div>
</section>
<section class="section">
  <h3>Pierwsza lekcja w roku szkolnym</h3>
  <p>Na początku każdego roku szkolnego pierwszym tematem w rozkładzie i w dzienniku powinien być: <strong>Lekcja organizacyjna. Zapoznanie uczniów z wymaganiami edukacyjnymi i zasadami oceniania</strong>.</p>
  <div class="cards">
    <div class="card"><h4>Zapis w dzienniku</h4><p>Temat musi zostać wpisany do dziennika elektronicznego. Jeżeli zapis w dzienniku jest prawidłowy, od tego roku szkolnego nie zbiera się dodatkowych papierowych potwierdzeń od nauczycieli uczących w oddziale.</p></div>
    <div class="card"><h4>Przypominanie wymagań</h4><p>Wymagania edukacyjne warto przypominać także na początku działów lub większych partii materiału, zwłaszcza przed sprawdzaniem osiągnięć.</p></div>
    <div class="card"><h4>Zastępstwa i nieobecności</h4><p>Dobrze przygotowany rozkład pomaga nauczycielowi zastępującemu kontynuować materiał w razie choroby lub nieprzewidzianej nieobecności nauczyciela prowadzącego.</p></div>
  </div>
</section>
<section class="section">
  <h3>Szablon rozkładu materiału</h3>
  <p>Plik zawiera dwa arkusze: <strong>wzór</strong> z przykładem wypełnienia oraz <strong>szablon</strong> do pracy nauczyciela. W górnej części arkusza wpisuje się informacje ogólne o rozkładzie, a od wiersza z nagłówkami uzupełnia się kolejne lekcje, tematy lub bloki pracy.</p>
  <div class="cards resource-grid">
    <div class="card">
      <h4>Plik do pobrania</h4>
      <p>Szablon rozkładu materiału na rok szkolny 2026/2027 z przykładowym arkuszem wzorcowym.</p>
      <a class="btn primary" href="{SCHEDULE_TEMPLATE}">Otwórz szablon XLSX</a>
    </div>
    <div class="card">
      <h4>Informacje do uzupełnienia przed tabelą</h4>
      <p>Przed listą tematów należy wpisać przedmiot i nauczyciela, nazwę rozkładu, typ szkoły i poziom klasy, podstawę programową, krótki opis rozkładu oraz numer szkolnego zestawu programów nauczania.</p>
    </div>
  </div>
  <div class="preview-grid">
    <div class="preview-card">
      <h4>Podgląd arkusza „wzór”</h4>
      <p>Przykładowe wiersze pokazują, jak łączyć temat, dział, liczbę godzin i elementy podstawy programowej.</p>
      <img src="assets/rozklad-materialu-wzor.png" alt="Podgląd przykładowego wypełnienia rozkładu materiału">
    </div>
    <div class="preview-card">
      <h4>Podgląd arkusza „szablon”</h4>
      <p>Pusty układ do wypełnienia przez nauczyciela.</p>
      <img src="assets/rozklad-materialu-szablon.png" alt="Podgląd pustego szablonu rozkładu materiału">
    </div>
  </div>
</section>
<section class="section">
  <h3>Opis kolumn w szablonie</h3>
  <div class="column-guide">
    <div class="column-item"><strong>L.p.</strong><p>Kolejny numer pozycji w rozkładzie. Ułatwia sprawdzanie kompletności i odwoływanie się do konkretnego tematu.</p></div>
    <div class="column-item"><strong>Temat</strong><p>Temat lekcji, bloku zajęć, sprawdzianu, powtórzenia albo zadania praktycznego.</p></div>
    <div class="column-item"><strong>Dział</strong><p>Nazwa działu, modułu lub większego obszaru programu. Pomaga grupować tematy i kontrolować kolejność pracy.</p></div>
    <div class="column-item"><strong>Liczba godzin</strong><p>Planowana liczba godzin przeznaczona na temat lub blok.</p></div>
    <div class="column-item"><strong>Elementy podstawy programowej</strong><p>Numery punktów, efekty kształcenia albo kryteria z podstawy programowej, które są realizowane w tej pozycji.</p></div>
    <div class="column-item"><strong>Podstawa programowa</strong><p>Nazwa podstawy, dokumentu lub kwalifikacji, z której pochodzą wskazane elementy.</p></div>
    <div class="column-item"><strong>Komentarz</strong><p>Krótkie uwagi organizacyjne: warunki realizacji, pracownia, zakres powtórzenia lub wariant dla klasy.</p></div>
    <div class="column-item"><strong>Zasoby prywatne</strong><p>Materiały nauczyciela niedostępne publicznie, np. własne karty pracy, sprawdziany lub notatki.</p></div>
    <div class="column-item"><strong>Zasoby publiczne</strong><p>Linki do publicznych materiałów, stron, filmów, dokumentów albo otwartych zasobów edukacyjnych.</p></div>
    <div class="column-item"><strong>Rozszerzenie</strong><p>Informacja, czy temat wykracza poza podstawowy zakres albo jest traktowany jako poszerzenie.</p></div>
    <div class="column-item"><strong>Smartlinki</strong><p>Krótkie odnośniki lub identyfikatory prowadzące do powiązanych materiałów.</p></div>
    <div class="column-item"><strong>Materiały dydaktyczne</strong><p>Podręcznik, ćwiczenia, prezentacje, karty pracy, sprzęt, oprogramowanie albo inne materiały potrzebne do lekcji.</p></div>
    <div class="column-item"><strong>Kolekcja po lekcji</strong><p>Materiały powstałe po zajęciach: notatki, linki, prace uczniów lub zadania do poprawy.</p></div>
    <div class="column-item"><strong>Aktywna</strong><p>Informacja, czy pozycja ma być brana pod uwagę w aktualnym rozkładzie.</p></div>
  </div>
</section>
"""


ADAPTATION_BODY = """
<section class="section">
  <h3>Na czym polega adaptacja programu w praktyce</h3>
  <p>Podstawa programowa jako akt prawny nie podlega zmianie: jej wymagania pozostają punktem odniesienia. Adaptacji podlega sposób realizacji programu: kolejność tematów, tempo, przykłady, ćwiczenia, materiały, formy pracy i sposoby sprawdzania wiedzy.</p>
  <div class="cards">
    <div class="card"><h4>1. Od podstawy do programu</h4><p>W pierwszej kolejności należy ustalić, które cele i treści są obowiązkowe. Program nauczania porządkuje ich realizację w konkretnym oddziale i w konkretnych warunkach szkoły.</p></div>
    <div class="card"><h4>2. Od programu do rozkładu</h4><p>Rozkład materiału przekłada program na kalendarz pracy. Widać w nim tempo, powtórzenia, ćwiczenia umiejętności i momenty sprawdzania osiągnięć.</p></div>
    <div class="card"><h4>3. Od wymagań do pracy na lekcji</h4><p>Wymagania na oceny powinny być zrozumiałe dla ucznia, a sposób dochodzenia do nich może obejmować różne ćwiczenia, projekty, rozmowy i zadania praktyczne.</p></div>
    <div class="card"><h4>4. Warto zwrócić uwagę</h4><p>Adaptacja nie może oznaczać przypadkowego usunięcia kluczowych efektów kształcenia ani tabeli ocen oderwanej od programu.</p></div>
  </div>
  <div class="callout">
    <h4>Praktyczna zasada</h4>
    <p>Punktem odniesienia pozostaje podstawa programowa: obowiązkowe cele, treści, efekty kształcenia i kryteria wskazane w przepisach. Propozycje wydawnictwa nie muszą być realizowane mechanicznie, jeżeli inna kolejność, tempo lub forma pracy lepiej odpowiada potrzebom klasy.</p>
  </div>
</section>
"""


FRAMEWORK_PLANS_BODY = """
<section class="section">
  <h3>Ramowe plany nauczania</h3>
  <p>Ta sekcja zostanie uzupełniona. Wkrótce pojawią się tutaj ramowe plany nauczania.</p>
  <div class="callout">
    <h4>W przygotowaniu</h4>
    <p>Po dodaniu materiałów ta podstrona będzie miejscem do sprawdzania ramowych planów nauczania dla typów szkół i kierunków prowadzonych w ZSZ5.</p>
  </div>
</section>
"""


SCHOOL_PROGRAM_SETS_BODY = """
<section class="section">
  <h3>Szkolne zestawy programów nauczania</h3>
  <p>Ta sekcja zostanie uzupełniona. Wkrótce pojawią się tutaj szkolne zestawy programów nauczania.</p>
  <div class="callout">
    <h4>W przygotowaniu</h4>
    <p>Po uzupełnieniu danych ta podstrona będzie porządkowała szkolne zestawy programów nauczania obowiązujące w roku szkolnym 2026/2027.</p>
  </div>
</section>
"""


MATERIALS_BODY = """
<section class="section">
  <h3>Przydatne materiały i linki</h3>
  <p>Te materiały warto wykorzystać przy recenzji wymagań, tworzeniu rozkładów materiału i adaptowaniu programu do realnej pracy z klasą. Źródła zewnętrzne są pomocnicze: wiążące pozostają aktualne akty prawne oraz szkolne decyzje nauczycieli i zespołów przedmiotowych.</p>
  <div class="cards resource-grid">
    <div class="card"><h4>Katalog podstaw programowych ZSZ5</h4><p>Bezpośrednie linki do PDF-ów podstaw programowych uporządkowane według typu szkoły, obszaru, przedmiotu i zawodu.</p><a class="btn primary" href="katalog_podstaw_programowych_ZSZ5_2026_2027.html">Otwórz katalog</a></div>
    <div class="card"><h4>Szablon rozkładu materiału</h4><p>Plik XLSX z arkuszem wzorcowym i pustym szablonem do pracy nauczyciela.</p><a class="btn" href="rozkłady materiału przedmiotów/rozkład materiału - szablon 2026_2027.xlsx">Otwórz szablon</a></div>
    <div class="card"><h4>MEN - materiały dla nauczycieli szkół ponadpodstawowych</h4><p>Pakiet pomocniczy do rozumienia podstawy programowej: preambuła, komentarze, porównania, uzasadnienia i rekomendacje.</p><a class="btn" href="https://www.gov.pl/web/edukacja/podstawa-programowa--materialy-dla-nauczycieli-szkol-ponadpodstawowych" target="_blank" rel="noopener">Otwórz materiał</a></div>
    <div class="card"><h4>ORE - podstawa programowa z 28 czerwca 2024 r.</h4><p>Strona ORE porządkująca materiały związane ze zmianami podstawy programowej.</p><a class="btn" href="https://ore.edu.pl/2024/09/podstawa-programowa-z-28-czerwca-2024-r/" target="_blank" rel="noopener">Otwórz materiał</a></div>
    <div class="card"><h4>ORE - programy nauczania do szkoły ponadpodstawowej</h4><p>Przykładowe programy nauczania pokazujące przejście od podstawy programowej do organizacji pracy w szkole.</p><a class="btn" href="https://ore.edu.pl/2020/04/programy-nauczania-programy-do-szkoly-ponadpodstawowej/" target="_blank" rel="noopener">Otwórz materiał</a></div>
    <div class="card"><h4>IBE PIB - podstawy programowe i kierunki zmian</h4><p>Miejsce do monitorowania prac nad podstawami programowymi i szerszego kontekstu zmian w edukacji.</p><a class="btn" href="https://ibe.edu.pl/pl/podstawy-programowe" target="_blank" rel="noopener">Otwórz materiał</a></div>
  </div>
  <p class="source-note">Ostatnie sprawdzenie linków źródłowych: 24 czerwca 2026 r.</p>
</section>
"""


LEGAL_BODY = """
<section class="section">
  <h3>Podstawy prawne i źródła</h3>
  <div class="cards">
    <div class="card"><h4>Ustawa o systemie oświaty, art. 22a</h4><span class="legal-ref">program nauczania</span><p>Reguluje przedstawianie i dopuszczanie programów nauczania do użytku w szkole. To podstawa dla szkolnej pracy nad programem, z którego wynikają wymagania.</p></div>
    <div class="card"><h4>Ustawa o systemie oświaty, art. 44b</h4><span class="legal-ref">ocenianie</span><p>Łączy ocenianie z wymaganiami edukacyjnymi wynikającymi z realizowanego programu nauczania i nakłada obowiązek poinformowania uczniów oraz rodziców.</p></div>
    <div class="card"><h4>Rozporządzenie MEN z 22 lutego 2019 r.</h4><span class="legal-ref">klasyfikowanie i promowanie</span><p>Określa szczegółowe warunki i sposób oceniania, klasyfikowania i promowania uczniów oraz słuchaczy w szkołach publicznych.</p></div>
    <div class="card"><h4>Rozporządzenie ME z 28 czerwca 2024 r.</h4><span class="legal-ref">zmiany podstawy programowej</span><p>Zmienia podstawę programową kształcenia ogólnego dla liceum ogólnokształcącego, technikum oraz branżowej szkoły II stopnia.</p></div>
  </div>
</section>
"""


def pages() -> list[Page]:
    return [
        Page(
            "index.html",
            "Ścieżka pracy",
            "Od podstawy programowej do wymagań na oceny",
            "Przewodnik porządkuje pracę nauczyciela: od obowiązkowych treści podstawy programowej, przez program nauczania i rozkład materiału, po wymagania edukacyjne, sposoby sprawdzania osiągnięć i ocenę ucznia.",
            START_BODY,
        ),
        Page(
            "rozklad_materialu.html",
            "Rozkład materiału",
            "Rozkład materiału",
            "Rozkład materiału pokazuje, jak nauczyciel planuje realizację podstawy programowej w konkretnym oddziale, roku szkolnym i kalendarzu pracy.",
            SCHEDULE_BODY,
        ),
        Page(
            "ramowe_plany_nauczania.html",
            "Ramowe plany",
            "Ramowe plany nauczania",
            "Miejsce na ramowe plany nauczania dla typów szkół i kierunków prowadzonych w ZSZ5.",
            FRAMEWORK_PLANS_BODY,
        ),
        Page(
            "szkolne_zestawy_programow_nauczania.html",
            "Szkolne zestawy",
            "Szkolne zestawy programów nauczania",
            "Miejsce na szkolne zestawy programów nauczania obowiązujące w roku szkolnym 2026/2027.",
            SCHOOL_PROGRAM_SETS_BODY,
        ),
        Page(
            "adaptacja_programu.html",
            "Adaptacja programu",
            "Adaptacja programu w praktyce",
            "Program nauczania można dostosować do warunków klasy, zachowując pełną zgodność z podstawą programową.",
            ADAPTATION_BODY,
        ),
        Page(
            "materialy_i_linki.html",
            "Materiały i linki",
            "Przydatne materiały i linki",
            "Zebrane źródła pomagają sprawdzić podstawy programowe, przygotować rozkład materiału i uporządkować wymagania edukacyjne.",
            MATERIALS_BODY,
        ),
        Page(
            "podstawy_prawne.html",
            "Podstawy prawne",
            "Podstawy prawne i źródła",
            "Najważniejsze akty i odniesienia potrzebne przy pracy nad programem nauczania, wymaganiami edukacyjnymi i ocenianiem.",
            LEGAL_BODY,
        ),
    ]


def main() -> None:
    generated_pages = pages()
    for page in generated_pages:
        (ROOT / page.file_name).write_text(page_shell(page, generated_pages), encoding="utf-8")
        print(f"Generated {ROOT / page.file_name}")
    (ROOT / LEGACY_ENTRY).write_text(page_shell(generated_pages[0], generated_pages), encoding="utf-8")
    print(f"Generated {ROOT / LEGACY_ENTRY}")


if __name__ == "__main__":
    main()
