from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "index.html"
LEGACY_ENTRY = ROOT / "wymagania_edukacyjne_ZSZ5_2026_2027.html"


HTML = """<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Przewodnik dla nauczyciela ZSZ5 2026/2027</title>
<link rel="icon" href="assets/logo-zsz5-black.png">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#f3f0e9;--paper:#fffdf8;--ink:#172033;--muted:#647084;--line:#d9d5cc;--navy:#172a46;--blue:#2b67d1;--teal:#245e58;--gold:#d99b2b;--shadow:0 12px 30px rgba(23,32,51,.08);--soft-shadow:0 8px 20px rgba(23,32,51,.06)}
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
.nav-link.primary,.btn.primary{background:#eef4fb;color:#1d4f9a;border:1px solid #b9d4f7}
main{padding-bottom:44px}
.hero{max-width:1120px;margin:22px auto 0;padding:28px 22px;background:var(--navy);color:#fff;border-radius:8px;box-shadow:var(--shadow)}
.eyebrow{font-size:.74rem;text-transform:uppercase;letter-spacing:.12em;color:#8fd4dd;font-weight:850}
.hero h2{font-size:clamp(1.45rem,3vw,2.25rem);line-height:1.1;margin-top:6px;max-width:860px}
.hero p{color:#c8d1df;font-size:.96rem;margin-top:12px;max-width:900px}
.hero-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
.hero-actions a{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.26);color:#fff}
.section{max-width:1120px;margin:0 auto;padding:24px 22px 0}
.section h3{font-size:1.08rem;color:var(--ink);margin-bottom:10px}
.section>p{font-size:.9rem;color:#374151;line-height:1.65;margin-bottom:14px;max-width:940px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.card{background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;padding:16px;box-shadow:var(--soft-shadow)}
.card h4{font-size:.94rem;color:var(--navy);margin-bottom:7px}
.card p,.card li{font-size:.85rem;color:#374151;line-height:1.55}
.card ul{padding-left:18px;margin-top:8px}
.resource-grid .card{display:flex;flex-direction:column;gap:8px}
.btn{align-self:flex-start;margin-top:auto;border:1px solid var(--line);background:#fff;color:var(--ink)}
.source-note{font-size:.76rem;color:var(--muted);margin-top:8px}
.table-wrap{overflow-x:auto;scrollbar-gutter:stable;background:var(--paper);border:1px solid rgba(23,32,51,.08);border-radius:8px;box-shadow:var(--soft-shadow)}
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
.callout{background:#e8f6f4;border:1px solid #b8ddd7;border-radius:8px;padding:15px;margin-top:14px;color:var(--teal)}
.callout h4{font-size:.92rem;margin-bottom:6px}
.callout p{font-size:.86rem;line-height:1.55}
.legal-ref{display:inline-block;margin-bottom:7px;padding:4px 8px;border-radius:999px;background:#eef4fb;color:#345070;border:1px solid #dce9f7;font-size:.74rem;font-weight:850}
button:focus-visible,a:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
@media (max-width:860px){body{font-size:14px}.brand{align-items:flex-start}.brand-logo{width:68px;height:48px}.hero{margin:14px 12px 0;padding:20px 16px}.section{padding-left:12px;padding-right:12px}.topbar-inner{padding-left:12px;padding-right:12px}.process-lab{grid-template-columns:1fr}}
@media (max-width:560px){header{padding:10px 14px}.brand-logo{width:58px;height:42px}header h1{font-size:1.04rem}header p{display:none}.hero h2{font-size:1.42rem}.hero p{font-size:.88rem}.card,.process-step,.process-panel{padding:12px}.process-step{grid-template-columns:30px 1fr;min-height:58px}}
@media print{.skip-link,.topbar,.hero-actions{display:none}body{background:#fff}.card,.process-panel,.process-step{break-inside:avoid}}
</style>
</head>
<body>
<a class="skip-link" href="#main_content">Przejdź do treści</a>
<header>
  <div class="brand">
    <img class="brand-logo" src="assets/logo-zsz5-black.png" alt="Logotyp ZSZ5 we Wrocławiu">
    <div>
      <h1>Przewodnik dla nauczyciela ZSZ5 2026/2027</h1>
      <p>Materiały robocze do przejścia od podstawy programowej przez program i rozkład materiału do wymagań na oceny.</p>
    </div>
  </div>
</header>
<nav class="topbar" aria-label="Nawigacja">
  <div class="topbar-inner">
    <a class="nav-link primary" href="katalog_podstaw_programowych_ZSZ5_2026_2027.html">Katalog podstaw programowych ZSZ5</a>
    <a class="nav-link" href="#sciezka">Ścieżka pracy</a>
    <a class="nav-link" href="#materialy">Materiały</a>
    <a class="nav-link" href="#rozklad">Rozkład materiału</a>
    <a class="nav-link" href="#przyklad-rozkladu">Wzór rozkładu</a>
    <a class="nav-link" href="#podstawy-prawne">Podstawy prawne</a>
  </div>
</nav>
<main id="main_content">
  <section class="hero">
    <p class="eyebrow">materiał do dalszego opracowania</p>
    <h2>Od podstawy programowej do wymagań na oceny</h2>
    <p>Na tej stronie zostaje na razie przewodnik dla nauczyciela: jak uporządkować pracę od podstawy programowej, przez program nauczania i rozkład materiału, do jasnych wymagań edukacyjnych. Robocze tabele wygenerowane wcześniej przez AI zostały zdjęte z widoku głównego.</p>
    <div class="hero-actions">
      <a class="nav-link" href="katalog_podstaw_programowych_ZSZ5_2026_2027.html">Otwórz katalog podstaw programowych</a>
      <a class="nav-link" href="#sciezka">Zobacz ścieżkę pracy</a>
      <a class="nav-link" href="#przyklad-rozkladu">Zobacz wzór rozkładu</a>
    </div>
  </section>

  <section class="section" id="sciezka">
    <h3>Od podstawy programowej do wymagań na oceny</h3>
    <p>Droga od podstawy programowej do oceny ucznia powinna być czytelna i możliwa do sprawdzenia. Sama podstawa nie jest jeszcze wymaganiami na ocenę: najpierw trzeba wybrać lub opracować program nauczania, rozpisać go na rozkład materiału, jasno określić wymagania edukacyjne, zaplanować sprawdzanie wiedzy i umiejętności, a dopiero potem wystawić ocenę ucznia.</p>
    <div class="process-lab" aria-label="Ścieżka od podstawy programowej do oceny ucznia">
      <div class="process-track" role="list">
        <button class="process-step active" type="button" role="listitem" aria-pressed="true" data-step="1" data-title="Podstawa programowa" data-teacher="Sprawdza obowiązkowe cele, treści, efekty kształcenia i kryteria wskazane w przepisach." data-output="Lista tego, czego nie można pominąć w danym przedmiocie lub kwalifikacji." data-check="Nie zastępuj podstawy propozycją z podręcznika ani tabelą z wydawnictwa." onclick="setProcessStep(this)">
          <span class="step-num">1</span><span><strong>Podstawa programowa</strong><small>Co jest obowiązkowe</small></span>
        </button>
        <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="2" data-title="Program nauczania" data-teacher="Wybiera program z wydawnictwa, modyfikuje go albo opracowuje własny, ale nadal pilnuje zgodności z podstawą." data-output="Program, który pokazuje sposób realizacji podstawy w danym oddziale." data-check="Program może być adaptowany, jeżeli tempo, kolejność albo dobór ćwiczeń nie pasują do klasy." onclick="setProcessStep(this)">
          <span class="step-num">2</span><span><strong>Program nauczania</strong><small>Jak realizujemy podstawę</small></span>
        </button>
        <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="3" data-title="Rozkład materiału" data-teacher="Przekłada program na działy, tematy, ćwiczenia, powtórzenia, projekty i orientacyjny czas pracy." data-output="Plan pracy na rok lub semestr, który da się realnie wykonać z konkretną klasą." data-check="Rozkład ma pomagać kontrolować realizację, a nie blokować sensowną korektę tempa." onclick="setProcessStep(this)">
          <span class="step-num">3</span><span><strong>Rozkład materiału</strong><small>Kolejność i tempo pracy</small></span>
        </button>
        <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="4" data-title="Wymagania edukacyjne" data-teacher="Opisuje, co uczeń powinien wiedzieć i umieć na poszczególne oceny." data-output="Jasne wymagania na dopuszczającą, dostateczną, dobrą, bardzo dobrą i celującą." data-check="Wymagania mają wynikać z realizowanego programu i podstawy, a nie z ogólnych haseł typu zna, rozumie, potrafi." onclick="setProcessStep(this)">
          <span class="step-num">4</span><span><strong>Wymagania edukacyjne</strong><small>Poziomy na oceny</small></span>
        </button>
        <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="5" data-title="Sprawdzanie wiedzy i umiejętności" data-teacher="Dobiera sprawdziany, odpowiedzi, zadania praktyczne, projekty i obserwację pracy ucznia do wcześniej podanych wymagań." data-output="Dowody uczenia się: prace, wypowiedzi, działania praktyczne, wyniki zadań i projekty." data-check="Nie oceniaj tego, czego wcześniej nie było w wymaganiach albo czego nie dało się przećwiczyć w danym trybie pracy." onclick="setProcessStep(this)">
          <span class="step-num">5</span><span><strong>Sprawdzanie</strong><small>Dowody wiedzy i umiejętności</small></span>
        </button>
        <button class="process-step" type="button" role="listitem" aria-pressed="false" data-step="6" data-title="Ocena ucznia" data-teacher="Porównuje osiągnięcia ucznia z wymaganiami edukacyjnymi i zasadami oceniania." data-output="Ocena bieżąca, śródroczna lub roczna, którą da się uzasadnić konkretnymi wymaganiami." data-check="Ocena powinna wynikać z rozpoznanych osiągnięć ucznia, a nie z samego faktu przerobienia tematów." onclick="setProcessStep(this)">
          <span class="step-num">6</span><span><strong>Ocena ucznia</strong><small>Uzasadniony wynik</small></span>
        </button>
      </div>
      <div class="process-panel" aria-live="polite">
        <div class="process-panel-head">
          <span class="eyebrow">aktywny etap</span>
          <h4><span id="process_step_num">1</span>. <span id="process_title">Podstawa programowa</span></h4>
        </div>
        <div class="process-panel-grid">
          <div><strong>Nauczyciel robi</strong><p id="process_teacher">Sprawdza obowiązkowe cele, treści, efekty kształcenia i kryteria wskazane w przepisach.</p></div>
          <div><strong>Powstaje</strong><p id="process_output">Lista tego, czego nie można pominąć w danym przedmiocie lub kwalifikacji.</p></div>
          <div><strong>Trzeba pilnować</strong><p id="process_check">Nie zastępuj podstawy propozycją z podręcznika ani tabelą z wydawnictwa.</p></div>
        </div>
      </div>
    </div>
    <div class="callout">
      <h4>Co to oznacza w praktyce</h4>
      <p><strong>Sztywno trzymamy się podstawy programowej</strong>: obowiązkowych celów, treści, efektów kształcenia i kryteriów wskazanych w przepisach. <strong>Nie musimy natomiast mechanicznie realizować propozycji wydawnictwa</strong>, jeżeli w konkretnej klasie nie działa tempo, kolejność, dobór ćwiczeń albo sposób sprawdzania.</p>
    </div>
  </section>

  <section class="section" id="materialy">
    <h3>Przydatne materiały i linki</h3>
    <p>Poniższe linki prowadzą do materiałów, które warto wykorzystać przy recenzji wymagań, tworzeniu rozkładów materiału i adaptowaniu programu do realnej pracy z klasą. Źródła zewnętrzne są pomocnicze: wiążące pozostają aktualne akty prawne oraz szkolne decyzje nauczycieli i zespołów przedmiotowych.</p>
    <div class="cards resource-grid">
      <div class="card">
        <h4>Katalog podstaw programowych ZSZ5</h4>
        <p>Osobna strona z bezpośrednimi linkami do PDF-ów podstaw programowych, uporządkowana według typu szkoły, obszaru, przedmiotu i zawodu.</p>
        <a class="btn primary" href="katalog_podstaw_programowych_ZSZ5_2026_2027.html">Otwórz katalog</a>
      </div>
      <div class="card">
        <h4>MEN - materiały dla nauczycieli szkół ponadpodstawowych</h4>
        <p>Pakiet pomocniczy do rozumienia podstawy programowej: preambuła, komentarze, porównania, uzasadnienia i rekomendacje.</p>
        <a class="btn" href="https://www.gov.pl/web/edukacja/podstawa-programowa--materialy-dla-nauczycieli-szkol-ponadpodstawowych" target="_blank" rel="noopener">Otwórz materiał</a>
      </div>
      <div class="card">
        <h4>ORE - podstawa programowa z 28 czerwca 2024 r.</h4>
        <p>Strona ORE porządkująca materiały związane ze zmianami podstawy programowej, przydatna przy sprawdzaniu aktualnego zakresu treści.</p>
        <a class="btn" href="https://ore.edu.pl/2024/09/podstawa-programowa-z-28-czerwca-2024-r/" target="_blank" rel="noopener">Otwórz materiał</a>
      </div>
      <div class="card">
        <h4>ORE - programy nauczania do szkoły ponadpodstawowej</h4>
        <p>Przykładowe programy nauczania pokazujące, jak przejść od podstawy programowej do realnej organizacji pracy w szkole.</p>
        <a class="btn" href="https://ore.edu.pl/2020/04/programy-nauczania-programy-do-szkoly-ponadpodstawowej/" target="_blank" rel="noopener">Otwórz materiał</a>
      </div>
      <div class="card">
        <h4>IBE PIB - podstawy programowe i kierunki zmian</h4>
        <p>Miejsce do monitorowania prac nad podstawami programowymi i szerszego kontekstu zmian w edukacji. Do bieżącej publikacji szkolnej trzeba je zestawiać z obowiązującymi aktami prawnymi.</p>
        <a class="btn" href="https://ibe.edu.pl/pl/podstawy-programowe" target="_blank" rel="noopener">Otwórz materiał</a>
      </div>
    </div>
    <p class="source-note">Ostatnie sprawdzenie linków źródłowych: 24 czerwca 2026 r.</p>
  </section>

  <section class="section" id="rozklad">
    <h3>Rozkład materiału - po co jest potrzebny</h3>
    <p>Rozkład materiału to praktyczny plan pracy nauczyciela na rok, semestr lub dział. Nie zastępuje podstawy programowej, programu nauczania ani wymagań edukacyjnych. Pokazuje natomiast, jak nauczyciel rozkłada treści programu w czasie i jak łączy je z lekcjami, ćwiczeniami, sprawdzaniem osiągnięć oraz możliwościami konkretnej klasy.</p>
    <div class="cards">
      <div class="card">
        <h4>Co powinien porządkować</h4>
        <ul>
          <li>kolejność działów i tematów,</li>
          <li>liczbę godzin lub orientacyjny czas realizacji,</li>
          <li>powiązanie tematów z wymaganiami podstawy programowej,</li>
          <li>planowane formy sprawdzania osiągnięć,</li>
          <li>miejsca na powtórzenia, projekty, pracę praktyczną i poprawę.</li>
        </ul>
      </div>
      <div class="card">
        <h4>Dlaczego jest potrzebny</h4>
        <p>Bez rozkładu materiału łatwo mieć tabelę wymagań, która wygląda kompletnie, ale nie wynika z realnego tempa pracy klasy. Rozkład pozwala sprawdzić, czy wszystkie treści da się zrealizować w kalendarzu roku szkolnego i czy ocenianie jest zaplanowane w sensownych momentach.</p>
      </div>
      <div class="card">
        <h4>Jak łączy się z adaptacją programu</h4>
        <p>Adaptacja programu wpływa na tempo, formy pracy, liczbę ćwiczeń, sposób sprawdzania wiedzy i dobór materiałów. To właśnie rozkład materiału pomaga przełożyć decyzje nauczyciela na codzienną pracę z klasą.</p>
      </div>
    </div>
  </section>

  <section class="section" id="przyklad-rozkladu">
    <h3>Przykładowy rozkład materiału - szablon i wzór</h3>
    <p>Plik zawiera dwa arkusze: <strong>wzór</strong> z przykładem wypełnienia oraz <strong>szablon</strong> do pracy nauczyciela. W górnej części arkusza wpisuje się informacje ogólne o rozkładzie, a od wiersza z nagłówkami uzupełnia się kolejne lekcje, tematy lub bloki pracy.</p>
    <div class="cards resource-grid">
      <div class="card">
        <h4>Plik do pobrania</h4>
        <p>Szablon rozkładu materiału na rok szkolny 2026/2027 z przykładowym arkuszem wzorcowym.</p>
        <a class="btn primary" href="rozkłady materiału przedmiotów/rozkład materiału - szablon 2026_2027.xlsx">Otwórz szablon XLSX</a>
      </div>
      <div class="card">
        <h4>Co uzupełnić przed tabelą</h4>
        <p>Przed listą tematów trzeba wpisać przedmiot i nauczyciela, nazwę rozkładu, typ szkoły i poziom klasy, podstawę programową, krótki opis rozkładu oraz numer szkolnego zestawu programów nauczania.</p>
      </div>
    </div>
    <div class="table-wrap" aria-label="Podgląd przykładowego rozkładu materiału">
      <table class="sample-table">
        <thead>
          <tr>
            <th>L.p.</th>
            <th>Temat</th>
            <th>Dział</th>
            <th>Liczba godzin</th>
            <th>Elementy podstawy programowej</th>
            <th>Rozszerzenie</th>
            <th>Aktywna</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td>
            <td>Sieci komputerowe</td>
            <td>Temat A1. Sieci komputerowe</td>
            <td>1</td>
            <td>III.4</td>
            <td>Nie</td>
            <td>Tak</td>
          </tr>
          <tr>
            <td>2</td>
            <td>Bezpieczeństwo i ochrona danych w komputerach i sieciach komputerowych</td>
            <td>Temat A2. Bezpieczeństwo i ochrona danych w komputerach i sieciach komputerowych</td>
            <td>1</td>
            <td>V.1, V.3, V.4</td>
            <td>Nie</td>
            <td>Tak</td>
          </tr>
          <tr>
            <td>3</td>
            <td>Sprawdzian (tematy A1-A2)</td>
            <td>-</td>
            <td>1</td>
            <td></td>
            <td>Nie</td>
            <td>Tak</td>
          </tr>
          <tr>
            <td>4</td>
            <td>Tworzenie formuł, formaty danych i formatowanie tabeli arkusza kalkulacyjnego</td>
            <td>Temat B1. Formuły, funkcje i wykresy w arkuszu kalkulacyjnym</td>
            <td>1</td>
            <td>II.2, II.3.c</td>
            <td>Nie</td>
            <td>Tak</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="column-guide">
      <div class="column-item"><strong>L.p.</strong><p>Kolejny numer pozycji w rozkładzie. Ułatwia sprawdzanie kompletności i rozmowę o konkretnym temacie.</p></div>
      <div class="column-item"><strong>Temat</strong><p>Temat lekcji, bloku zajęć, sprawdzianu, powtórzenia albo zadania praktycznego. Powinien być zrozumiały dla nauczyciela i możliwy do przeniesienia do planu pracy.</p></div>
      <div class="column-item"><strong>Dział</strong><p>Nazwa działu, modułu lub większego obszaru programu. Pomaga grupować tematy i kontrolować kolejność pracy.</p></div>
      <div class="column-item"><strong>Liczba godzin</strong><p>Planowana liczba godzin przeznaczona na temat lub blok. Wpis powinien pomagać sprawdzić, czy cały rozkład mieści się w realnej liczbie godzin.</p></div>
      <div class="column-item"><strong>Elementy podstawy programowej</strong><p>Numery punktów, efekty kształcenia albo kryteria z podstawy programowej, które są realizowane w tej pozycji.</p></div>
      <div class="column-item"><strong>Podstawa programowa</strong><p>Nazwa podstawy, dokumentu lub kwalifikacji, z której pochodzą wskazane elementy. Przy kilku podstawach warto podać dokładne źródło.</p></div>
      <div class="column-item"><strong>Komentarz</strong><p>Miejsce na krótkie uwagi organizacyjne: warunki realizacji, potrzebne pracownie, zakres powtórzenia, wariant dla słabszej lub mocniejszej klasy.</p></div>
      <div class="column-item"><strong>Zasoby prywatne</strong><p>Materiały nauczyciela niedostępne publicznie, np. własne karty pracy, pliki w chmurze szkolnej, sprawdziany lub notatki.</p></div>
      <div class="column-item"><strong>Zasoby publiczne</strong><p>Linki do publicznych materiałów, stron, filmów, dokumentów albo otwartych zasobów edukacyjnych.</p></div>
      <div class="column-item"><strong>Rozszerzenie</strong><p>Informacja, czy temat wykracza poza podstawowy zakres albo jest traktowany jako poszerzenie dla danej klasy. W szablonie przykładowo wpisano „Tak” albo „Nie”.</p></div>
      <div class="column-item"><strong>Smartlinki</strong><p>Miejsce na krótkie odnośniki lub identyfikatory prowadzące do powiązanych materiałów w systemie, repozytorium albo bibliotece nauczyciela.</p></div>
      <div class="column-item"><strong>Materiały dydaktyczne</strong><p>Podręcznik, ćwiczenia, prezentacje, karty pracy, sprzęt, oprogramowanie albo inne materiały potrzebne do realizacji tematu.</p></div>
      <div class="column-item"><strong>Kolekcja po lekcji</strong><p>Miejsce na materiały powstałe po zajęciach: notatki, linki, prace uczniów, zdjęcia efektów, zadania do poprawy lub materiały do archiwum.</p></div>
      <div class="column-item"><strong>Aktywna</strong><p>Informacja, czy pozycja ma być brana pod uwagę w aktualnym rozkładzie. Przydatne, gdy nauczyciel trzyma w pliku tematy rezerwowe albo wyłączone.</p></div>
    </div>
  </section>

  <section class="section">
    <h3>Co znaczy adaptować program w praktyce</h3>
    <p>Nie zmienia się samej podstawy programowej jako aktu prawnego: jej wymagania pozostają punktem odniesienia. Adaptuje się sposób realizacji programu: kolejność tematów, tempo, przykłady, ćwiczenia, materiały, formy pracy i sposoby sprawdzania wiedzy.</p>
    <div class="cards">
      <div class="card">
        <h4>1. Od podstawy do programu</h4>
        <p>Najpierw trzeba ustalić, które cele i treści są obowiązkowe. Program nauczania nie jest kopią podstawy: porządkuje jej realizację w konkretnym oddziale i w konkretnych warunkach szkoły.</p>
      </div>
      <div class="card">
        <h4>2. Od programu do rozkładu</h4>
        <p>Rozkład materiału przekłada program na kalendarz pracy. To w nim widać, czy tempo jest realne, gdzie są powtórzenia, kiedy uczniowie ćwiczą umiejętności i kiedy nauczyciel sprawdza osiągnięcia.</p>
      </div>
      <div class="card">
        <h4>3. Od wymagań do pracy na lekcji</h4>
        <p>Wymagania na oceny powinny być zrozumiałe dla ucznia, a sposób dochodzenia do tych wymagań może być różny: przez więcej przykładów, inne ćwiczenia, pracę praktyczną, projekty, rozmowę albo zadania stopniowane trudnością.</p>
      </div>
      <div class="card">
        <h4>4. Co nie powinno się wydarzyć</h4>
        <p>Adaptacja nie może oznaczać przypadkowego usunięcia kluczowych efektów kształcenia ani tabeli ocen oderwanej od programu. Powinna być świadomą decyzją nauczyciela, zespołu lub szkoły, zgodną z podstawą i realnym planem pracy.</p>
      </div>
    </div>
  </section>

  <section class="section" id="podstawy-prawne">
    <h3>Podstawy prawne i źródła</h3>
    <div class="cards">
      <div class="card">
        <h4>Ustawa o systemie oświaty, art. 22a</h4>
        <span class="legal-ref">program nauczania</span>
        <p>Reguluje przedstawianie i dopuszczanie programów nauczania do użytku w szkole. To podstawa dla szkolnej pracy nad programem, z którego wynikają wymagania.</p>
      </div>
      <div class="card">
        <h4>Ustawa o systemie oświaty, art. 44b</h4>
        <span class="legal-ref">ocenianie</span>
        <p>Łączy ocenianie z wymaganiami edukacyjnymi wynikającymi z realizowanego programu nauczania i nakłada obowiązek poinformowania uczniów oraz rodziców.</p>
      </div>
      <div class="card">
        <h4>Rozporządzenie MEN z 22 lutego 2019 r.</h4>
        <span class="legal-ref">klasyfikowanie i promowanie</span>
        <p>Określa szczegółowe warunki i sposób oceniania, klasyfikowania i promowania uczniów oraz słuchaczy w szkołach publicznych.</p>
      </div>
      <div class="card">
        <h4>Rozporządzenie ME z 28 czerwca 2024 r.</h4>
        <span class="legal-ref">zmiany podstawy programowej</span>
        <p>Zmienia podstawę programową kształcenia ogólnego dla liceum ogólnokształcącego, technikum oraz branżowej szkoły II stopnia.</p>
      </div>
    </div>
  </section>
</main>
<script>
function setProcessStep(button){
  document.querySelectorAll('.process-step').forEach(item=>{
    const active=item===button;
    item.classList.toggle('active', active);
    item.setAttribute('aria-pressed', active ? 'true' : 'false');
  });
  document.getElementById('process_step_num').textContent=button.dataset.step;
  document.getElementById('process_title').textContent=button.dataset.title;
  document.getElementById('process_teacher').textContent=button.dataset.teacher;
  document.getElementById('process_output').textContent=button.dataset.output;
  document.getElementById('process_check').textContent=button.dataset.check;
}
</script>
</body>
</html>
"""


def main() -> None:
    OUT.write_text(HTML, encoding="utf-8")
    shutil.copy2(OUT, LEGACY_ENTRY)
    print(f"Generated {OUT}")
    print(f"Generated {LEGACY_ENTRY}")


if __name__ == "__main__":
    main()
