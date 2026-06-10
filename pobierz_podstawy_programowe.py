"""
Skrypt do pobierania podstaw programowych MEN - rok szkolny 2026/2027
Szkoła: ZSZ5 (Branżowa Szkoła I st., BS II st., Technikum)

Uruchomienie: python pobierz_podstawy_programowe.py

UWAGA - pliki niedostępne automatycznie (wymagają przeglądarki):
  BS I - przedmioty klasyczne (j.polski, matematyka, biologia, chemia, fizyka,
    geografia, historia, j.angielski, j.niemiecki, WF, EDB):
    → Rozp. MEN 14.02.2017, Dz.U. 2017 poz. 356 (pełny tekst)
    → https://prawo.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20170000356
  Technikum - Historia i teraźniejszość (HiT):
    → Rozp. MEN 1.08.2022, Dz.U. 2022 poz. 1578
    → https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20220001578
  Technikum - Biznes i zarządzanie:
    → nowelizacja Rozp. 2018, 2024 r.
    → https://isap.sejm.gov.pl
"""

import urllib.request
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORE = "https://ore.edu.pl/wp-content/plugins/download-attachments/includes/download.php?id="

PLIKI = [

    # ==========================================
    # BS I STOPNIA - KSZTAŁCENIE ZAWODOWE
    # ==========================================
    {
        "url": "https://infozawodowe.men.gov.pl/image/professionCoreCurriculum/cukiernik_6af131b31de804696ae7f95b52a14780.pdf",
        "sciezka": "01_BSI_stopnia/zawodowe/PP_cukiernik_SPC01.pdf",
        "nazwa": "Cukiernik (SPC.01)"
    },
    {
        "url": "https://infozawodowe.men.gov.pl/image/professionCoreCurriculum/fryzjer_1bd5295abb182cf6bd0379176079d24e.pdf",
        "sciezka": "01_BSI_stopnia/zawodowe/PP_fryzjer_FRK01.pdf",
        "nazwa": "Fryzjer (FRK.01)"
    },
    {
        "url": "https://infozawodowe.men.gov.pl/image/professionCoreCurriculum/kucharz_de43d3fc9c628cd8ca239417d9f966cd.pdf",
        "sciezka": "01_BSI_stopnia/zawodowe/PP_kucharz_HGT02.pdf",
        "nazwa": "Kucharz (HGT.02)"
    },
    {
        "url": "https://infozawodowe.men.gov.pl/image/professionCoreCurriculum/sprzedawca_7897c0e8f14ee4663e235f4de0d5f6ec.pdf",
        "sciezka": "01_BSI_stopnia/zawodowe/PP_sprzedawca_HAN01.pdf",
        "nazwa": "Sprzedawca (HAN.01)"
    },
    {
        "url": "https://infozawodowe.men.gov.pl/image/professionCoreCurriculum/kelner_5e00d777b3998892a27ee645de263f7c.pdf",
        "sciezka": "01_BSI_stopnia/zawodowe/PP_kelner_HGT01.pdf",
        "nazwa": "Kelner (HGT.01)"
    },
    {
        "url": "https://infozawodowe.men.gov.pl/image/professionCoreCurriculum/lakiernik-samochodowy_cefe30de990e4e75bb484b0fed40215c.pdf",
        "sciezka": "01_BSI_stopnia/zawodowe/PP_lakiernik_samochodowy_MOT03.pdf",
        "nazwa": "Lakiernik samochodowy (MOT.03)"
    },
    {
        "url": "https://infozawodowe.men.gov.pl/image/professionCoreCurriculum/mechanik-pojazdow-samochodowych_b8bc2fd71a1f197c3d278fb3da2a583d.pdf",
        "sciezka": "01_BSI_stopnia/zawodowe/PP_mechanik_pojazdow_samochodowych_MOT05.pdf",
        "nazwa": "Mechanik pojazdów samochodowych (MOT.05)"
    },

    # ==========================================
    # BS I STOPNIA - KSZTAŁCENIE OGÓLNE (nowelizacje)
    # Rozp. bazowe: Dz.U. 2017 poz. 356
    # Przedmioty klasyczne NIE mają osobnych PDFów na ORE — są w ww. rozporządzeniu.
    # Poniżej: nowelizacje dostępne na ore.edu.pl
    # ==========================================
    {
        "url": ORE + "70897",
        "sciezka": "01_BSI_stopnia/ogolne/PP_BSI_nowelizacja_28_06_2024_HiT_EdObyw_BizZarz_EdZdrow.pdf",
        "nazwa": "PP BS I - nowelizacja 28.06.2024 (HiT, Ed.obywatelska, Biznes i zarządzanie, Ed.zdrowotna) [Dz.U. 2024 poz. 996]"
    },
    {
        "url": ORE + "89037",
        "sciezka": "01_BSI_stopnia/ogolne/PP_BSI_edukacja_zdrowotna_Rozp_ME_06_03_2025.pdf",
        "nazwa": "PP BS I - Edukacja zdrowotna (Rozp. ME 06.03.2025)"
    },
    {
        "url": ORE + "89116",
        "sciezka": "01_BSI_stopnia/ogolne/PP_edukacja_obywatelska_BSI_Tech_LO_Rozp_ME_06_03_2025.pdf",
        "nazwa": "PP Edukacja obywatelska (BS I + Technikum + LO, Rozp. ME 06.03.2025)"
    },
    {
        "url": ORE + "89106",
        "sciezka": "01_BSI_stopnia/ogolne/PP_BSI_wychowanie_fizyczne_nowe_DzU_2025_poz1035.pdf",
        "nazwa": "PP BS I - Wychowanie fizyczne nowe (Dz.U. 2025 poz. 1035)"
    },

    # ==========================================
    # BS II STOPNIA - KSZTAŁCENIE ZAWODOWE
    # ==========================================
    {
        "url": "https://infozawodowe.men.gov.pl/image/professionCoreCurriculum/technik-uslug-fryzjerskich_7bb3c2170d9008b8229ec5ae782c629b.pdf",
        "sciezka": "02_BSII_stopnia/zawodowe/PP_technik_uslug_fryzjerskich_FRK01_FRK03.pdf",
        "nazwa": "Technik usług fryzjerskich (FRK.01+FRK.03)"
    },

    # ==========================================
    # BS II STOPNIA - KSZTAŁCENIE OGÓLNE
    # Rozp. bazowe: Dz.U. 2018 poz. 467 — indywidualne PDFy z ore.edu.pl
    # BS II realizuje: j.polski, j.angielski, matematykę, informatykę
    # ==========================================
    {
        "url": ORE + "23135",
        "sciezka": "02_BSII_stopnia/ogolne/PP_jezyk_polski.pdf",
        "nazwa": "PP Język polski (BS II/Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23134",
        "sciezka": "02_BSII_stopnia/ogolne/PP_jezyk_obcy_nowozytny.pdf",
        "nazwa": "PP Język obcy nowożytny (BS II/Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23137",
        "sciezka": "02_BSII_stopnia/ogolne/PP_matematyka.pdf",
        "nazwa": "PP Matematyka (BS II/Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23131",
        "sciezka": "02_BSII_stopnia/ogolne/PP_informatyka.pdf",
        "nazwa": "PP Informatyka (BS II/Technikum, Rozp. 2018)"
    },

    # ==========================================
    # TECHNIKUM - KSZTAŁCENIE ZAWODOWE
    # ==========================================
    {
        "url": "https://infozawodowe.men.gov.pl/image/professionCoreCurriculum/technik-uslug-fryzjerskich_7bb3c2170d9008b8229ec5ae782c629b.pdf",
        "sciezka": "03_Technikum/zawodowe/PP_technik_uslug_fryzjerskich_FRK01_FRK03.pdf",
        "nazwa": "Technik usług fryzjerskich (FRK.01+FRK.03)"
    },
    {
        "url": "https://infozawodowe.men.gov.pl/image/professionCoreCurriculum/technik-handlowiec_f7218af640457c9a9b00ae0a24d40de4.pdf",
        "sciezka": "03_Technikum/zawodowe/PP_technik_handlowiec_HAN01_HAN02.pdf",
        "nazwa": "Technik handlowiec (HAN.01+HAN.02)"
    },

    # ==========================================
    # TECHNIKUM - KSZTAŁCENIE OGÓLNE
    # Rozp. bazowe: Dz.U. 2018 poz. 467 — indywidualne PDFy z ore.edu.pl
    # Uwaga: Historia i teraźniejszość (HiT) — brak PDF na ORE, patrz komentarz na górze
    #        Biznes i zarządzanie — brak PDF na ORE (nowelizacja 2024), patrz komentarz na górze
    # ==========================================
    {
        "url": ORE + "23135",
        "sciezka": "03_Technikum/ogolne/PP_jezyk_polski.pdf",
        "nazwa": "PP Język polski (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23134",
        "sciezka": "03_Technikum/ogolne/PP_jezyk_obcy_nowozytny.pdf",
        "nazwa": "PP Język obcy nowożytny – angielski/niemiecki (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "25373",
        "sciezka": "03_Technikum/ogolne/PP_historia.pdf",
        "nazwa": "PP Historia (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23127",
        "sciezka": "03_Technikum/ogolne/PP_geografia.pdf",
        "nazwa": "PP Geografia (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23121",
        "sciezka": "03_Technikum/ogolne/PP_biologia.pdf",
        "nazwa": "PP Biologia (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23122",
        "sciezka": "03_Technikum/ogolne/PP_chemia.pdf",
        "nazwa": "PP Chemia (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23126",
        "sciezka": "03_Technikum/ogolne/PP_fizyka.pdf",
        "nazwa": "PP Fizyka (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23137",
        "sciezka": "03_Technikum/ogolne/PP_matematyka.pdf",
        "nazwa": "PP Matematyka (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23131",
        "sciezka": "03_Technikum/ogolne/PP_informatyka.pdf",
        "nazwa": "PP Informatyka (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23143",
        "sciezka": "03_Technikum/ogolne/PP_wychowanie_fizyczne_Rozp2018.pdf",
        "nazwa": "PP Wychowanie fizyczne (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "89107",
        "sciezka": "03_Technikum/ogolne/PP_wychowanie_fizyczne_nowe_DzU_2025_poz1052.pdf",
        "nazwa": "PP Wychowanie fizyczne nowe (Technikum, Dz.U. 2025 poz. 1052)"
    },
    {
        "url": ORE + "23123",
        "sciezka": "03_Technikum/ogolne/PP_edukacja_dla_bezpieczenstwa.pdf",
        "nazwa": "PP Edukacja dla bezpieczeństwa (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23139",
        "sciezka": "03_Technikum/ogolne/PP_plastyka.pdf",
        "nazwa": "PP Plastyka (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23140",
        "sciezka": "03_Technikum/ogolne/PP_podstawy_przedsiebiorczosci_Rozp2018.pdf",
        "nazwa": "PP Podstawy przedsiębiorczości – stare (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23141",
        "sciezka": "03_Technikum/ogolne/PP_wiedza_o_spoleczenstwie_Rozp2018.pdf",
        "nazwa": "PP Wiedza o społeczeństwie – stare (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "23142",
        "sciezka": "03_Technikum/ogolne/PP_wychowanie_do_zycia_w_rodzinie.pdf",
        "nazwa": "PP Wychowanie do życia w rodzinie (Technikum, Rozp. 2018)"
    },
    {
        "url": ORE + "89038",
        "sciezka": "03_Technikum/ogolne/PP_edukacja_zdrowotna_Rozp_ME_06_03_2025.pdf",
        "nazwa": "PP Edukacja zdrowotna (Technikum, Rozp. ME 06.03.2025)"
    },
    {
        "url": ORE + "89116",
        "sciezka": "03_Technikum/ogolne/PP_edukacja_obywatelska_Rozp_ME_06_03_2025.pdf",
        "nazwa": "PP Edukacja obywatelska (Technikum, Rozp. ME 06.03.2025)"
    },
]

# Pliki dostępne wyłącznie przez przeglądarkę (ISAP)
BRAKUJACE_RECZNE = [
    {
        "sciezka": "01_BSI_stopnia/ogolne/PP_BSI_Rozp2017_poz356_pelny_tekst.pdf",
        "uwaga": "Rozp. MEN 14.02.2017, Dz.U. 2017 poz. 356 — zawiera j.polski, matematykę, biologię,"
                 " chemię, fizykę, geografię, historię, j.angielski, j.niemiecki, WF, EDB dla BS I st.\n"
                 "    Pobierz ręcznie: https://prawo.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20170000356"
    },
    {
        "sciezka": "03_Technikum/ogolne/PP_historia_i_terazniejszosc_DzU_2022_poz1578.pdf",
        "uwaga": "Historia i teraźniejszość, Rozp. MEN 1.08.2022, Dz.U. 2022 poz. 1578\n"
                 "    Pobierz ręcznie: https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20220001578"
    },
    {
        "sciezka": "03_Technikum/ogolne/PP_biznes_i_zarzadzanie_nowelizacja_2024.pdf",
        "uwaga": "Biznes i zarządzanie — nowelizacja Rozp. 2018 z 2024 r.\n"
                 "    Pobierz ręcznie: https://isap.sejm.gov.pl (wyszukaj: podstawa programowa biznes zarządzanie 2024)"
    },
]


def pobierz(url, sciezka_wzgledna, nazwa):
    sciezka = os.path.join(BASE_DIR, sciezka_wzgledna)
    os.makedirs(os.path.dirname(sciezka), exist_ok=True)
    if os.path.exists(sciezka):
        print(f"  [SKIP] Już istnieje: {os.path.basename(sciezka)}")
        return "skip"
    print(f"  Pobieranie: {nazwa} ...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r, open(sciezka, "wb") as f:
            f.write(r.read())
        print("OK")
        return "ok"
    except Exception as e:
        print(f"BŁĄD: {e}")
        return "err"


def main():
    print("=" * 65)
    print("Pobieranie podstaw programowych MEN – ZSZ5 – rok szk. 2026/2027")
    print(f"Folder docelowy: {BASE_DIR}")
    print("=" * 65)

    ok = err = skip = 0
    for p in PLIKI:
        wynik = pobierz(p["url"], p["sciezka"], p["nazwa"])
        if wynik == "ok":
            ok += 1
        elif wynik == "skip":
            skip += 1
        else:
            err += 1

    print()
    print(f"Gotowe. Pobrane: {ok}, Pominięte (już istnieją): {skip}, Błędy: {err}")
    if err:
        print("Sprawdź dostęp do internetu i spróbuj ponownie.")

    print()
    print("=" * 65)
    print("PLIKI WYMAGAJĄCE RĘCZNEGO POBRANIA (strony z JS – brak auto-pobierania):")
    print("=" * 65)
    for b in BRAKUJACE_RECZNE:
        print(f"  Plik docelowy: {b['sciezka']}")
        print(f"  {b['uwaga']}")
        print()


if __name__ == "__main__":
    main()
