#!/usr/bin/env python3
"""
Pobierz opracowania podstaw programowych z ORE
Seria: "Vademecum nauczyciela. Wdrażanie podstawy programowej w szkole ponadpodstawowej"

Uruchomienie: python3 pobierz_opracowania_ORE.py
"""

import os
import sys
import time
import urllib.request
from urllib.error import URLError, HTTPError

# === FOLDER DOCELOWY ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "opracowania_ORE", "Vademecum_szkola_ponadpodstawowa")

# === LISTA PDF-ÓW ===
# Seria "Vademecum nauczyciela - Wdrażanie podstawy programowej w szkole ponadpodstawowej"
# Dotyczy: Technikum, LO, Branżowa Szkoła II stopnia
BASE = "https://ore.edu.pl/wp-content/uploads"
PFX  = "vademecum-nauczyciela.-wdrazanie-podstawy-programowej-w-szkole-ponadpodstawowej.-"

PDFS = [
    # --- Potwierdzone (znalezione w wynikach wyszukiwania) ---
    ("biologia",              f"{BASE}/2019/07/{PFX}biologia.pdf"),
    ("chemia",                f"{BASE}/2019/07/{PFX}chemia.pdf"),
    ("filozofia-etyka",       f"{BASE}/2019/07/{PFX}filozofia-etyka.pdf"),
    ("fizyka",                f"{BASE}/2019/07/{PFX}fizyka.pdf"),
    ("historia",              f"{BASE}/2019/07/{PFX}historia.pdf"),
    ("jezyk-polski",          f"{BASE}/2019/07/{PFX}jezyk-polski-wyd.elektroniczne.pdf"),
    ("jezyk-lacinski",        f"{BASE}/2019/07/{PFX}jezyk-lacinski.pdf"),
    ("geografia",             f"{BASE}/2019/11/{PFX}geografia.pdf"),
    ("wos",                   f"{BASE}/2019/12/{PFX}wos.pdf"),
    ("wychowanie-fizyczne",   f"{BASE}/2019/12/{PFX}wychowanie-fizyczne.pdf"),
]

# === FUNKCJE ===

def download_file(url: str, dest_path: str) -> bool:
    """Pobierz plik. Zwraca True jeśli sukces."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status != 200:
                return False
            content_type = response.headers.get("Content-Type", "")
            if "pdf" not in content_type.lower() and not url.lower().endswith(".pdf"):
                print(f"  ⚠ Nieoczekiwany Content-Type: {content_type}")
            data = response.read()
            # Sprawdź czy to PDF (magic bytes %PDF)
            if not data.startswith(b"%PDF"):
                print(f"  ⚠ Plik nie wygląda jak PDF (pierwsze bajty: {data[:8]})")
                return False
            with open(dest_path, "wb") as f:
                f.write(data)
            size_kb = len(data) / 1024
            print(f"  ✓ Pobrano ({size_kb:.0f} KB)")
            return True
    except HTTPError as e:
        if e.code == 404:
            print(f"  ✗ Nie znaleziono (404)")
        else:
            print(f"  ✗ Błąd HTTP {e.code}")
        return False
    except URLError as e:
        print(f"  ✗ Błąd połączenia: {e.reason}")
        return False
    except Exception as e:
        print(f"  ✗ Błąd: {e}")
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 65)
    print("Pobieranie opracowań ORE – Vademecum nauczyciela")
    print(f"Folder: {OUTPUT_DIR}")
    print("=" * 65)

    ok, skip, fail = [], [], []

    for name, url in PDFS:
        dest = os.path.join(OUTPUT_DIR, f"vademecum_{name}.pdf")
        print(f"\n[{name}]")
        print(f"  URL: {url}")

        if os.path.exists(dest):
            size_kb = os.path.getsize(dest) / 1024
            print(f"  → Już istnieje ({size_kb:.0f} KB), pomijam")
            skip.append(name)
            continue

        success = download_file(url, dest)
        if success:
            ok.append(name)
        else:
            fail.append(name)

        time.sleep(0.5)  # grzeczne opóźnienie między requestami

    # === PODSUMOWANIE ===
    print("\n" + "=" * 65)
    print("PODSUMOWANIE")
    print("=" * 65)
    print(f"✓ Pobrano:     {len(ok):2d}  → {', '.join(ok) if ok else '-'}")
    print(f"→ Pominięto:   {len(skip):2d}  → {', '.join(skip) if skip else '-'}")
    print(f"✗ Nie znaleziono: {len(fail):2d}  → {', '.join(fail) if fail else '-'}")
    print()
    if fail:
        print("UWAGA: Pliki oznaczone ✗ mogły nie istnieć pod podanym URL.")
        print("Sprawdź ręcznie na: https://ore.edu.pl/2019/12/poradniki-vademecum-nauczyciela-wdrazanie-podstawy-programowej-w-szkole-ponadpodstawowej/")
    print()
    print(f"Folder z plikami: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
