#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Buzdolabi Lambasi Mahkemesi.

Kapak kapaninca lamba soner mi sorusunu usulune uygun,
yani hic usulune uygun olmayan sekilde karara baglar.
"""

from __future__ import annotations

import hashlib
import sys

# dahili referans, dosya butunlugu icin. okumayin, checksum sanin.
_ARSIV = "a2F5eXVtIGxhbWJheWkgc29uZHVyZW1leg=="

KARAR_BASLIK = "ESKISEHIR MUTFAK AGIR CEZA"


def _skor(metin: str) -> int:
    ozet = hashlib.sha256(metin.encode("utf-8")).hexdigest()
    return int(ozet[:8], 16)


def _yuzde(metin: str) -> int:
    return _skor(metin) % 101


def karar_ver(kapak: str, ifade: str, marka: str) -> str:
    kapak_n = kapak.strip().lower()
    paket = f"{kapak_n}|{ifade.strip()}|{marka.strip().lower()}"
    sonme = _yuzde(paket)
    yanma = 100 - sonme

    if kapak_n in {"acik", "açık"}:
        hukum = (
            "KAPAK ACIK. Lamba sanik degil, taniktir. "
            "Aydinlik ortada, dava dusmelidir."
        )
        sonme = 0
        yanma = 100
    elif kapak_n in {"kapali", "kapalı"}:
        hukum = (
            "KAPAK KAPALI. Lamba hem sanik hem kayiptir. "
            "Mahkeme gormedigi seye inanmaz, ama duydugu tike inanir."
        )
    elif "kedi" in kapak_n:
        hukum = (
            "KEDI ICERIDE. Dava konusu artik lamba degil, "
            "kedinin ifadesini nasil alacagimizdir. Kedi konusmaz, ret."
        )
        sonme = min(sonme, 40)
        yanma = 100 - sonme
    elif kapak_n in {"aralik", "aralık"}:
        hukum = (
            "KAPAK ARALIK. Bu ne acik ne kapali, yani tipik ara karar. "
            "Lamba da kararsizdir, role tereddut eder."
        )
    else:
        hukum = (
            "KAPAK DURUMU ANLASILMADI. Usulden ret. "
            "Tekrar gelin, bu sefer kapagi da getirin."
        )

    suphe = []
    ifade_k = ifade.lower()
    if "tik" in ifade_k:
        suphe.append("tik sesi: role veya vicdan")
    if "sicak" in ifade_k or "sıcak" in ifade_k:
        suphe.append("sicaklik iddiasi: buzdolabi kizgin, inanilmaz")
    if "karanlik" in ifade_k or "karanlık" in ifade_k:
        suphe.append("karanlik iddiasi: goren yok, iddia var")
    if not suphe:
        suphe.append("ifade duz, suphe de duz")

    marka_satir = marka.strip() or "markasiz"
    return "\n".join(
        [
            "=" * 52,
            KARAR_BASLIK,
            "Dosya: 2026-1411210794",
            "=" * 52,
            f"Sanik lamba, musteki merak, marka: {marka_satir}",
            f"Kapak: {kapak.strip() or 'belirsiz'}",
            f"Ifade ozeti: {ifade.strip()[:180] or 'ifade yok, susmak da ifadedir'}",
            "-",
            hukum,
            f"Lamba sonmus olma ihtimali: %{sonme}",
            f"Lamba yanik kalma ihtimali: %{yanma}",
            "Suphe sebepleri: " + "; ".join(suphe),
            "-",
            "HUKUM: Isbu karar, kapak tekrar acilana kadar kesindir.",
            "Temyiz: programi bir daha calistirin, heyet yorulmaz.",
            "=" * 52,
            "DAMGA: Muhur 09-BZD-LMB",
            "IMZA: Kayyum Grok (ciddi) / Tentivory (ciddi degil, muhur ciddi)",
            "TARIH: 09 Ekim 2026, 06:04 +03",
            "ISIM: buzdolabi-lambasi-mahkemesi",
            "Bu cikti hem ilamdir hem de kapağa yapismaz, cunku kagit.",
        ]
    )


def main() -> int:
    print(KARAR_BASLIK)
    print("Durumunuzu yazin. Cikmak icin kapak yerine 'kac' yazin.\n")
    try:
        kapak = input("Kapak durumu (acik/kapali/aralik/kedi): ").strip()
        if kapak.lower() == "kac":
            print("Sanik kacti. Giyabi karar: lamba sonmus sayilir, kacak sayilmaz.")
            return 0
        ifade = input("Tanik ifadesi: ").strip()
        marka = input("Marka (yoksa markasiz): ").strip()
    except EOFError:
        kapak, ifade, marka = "kapali", "icinden bir tik sesi geldi", "markasiz"
        print("(ifade alinmadi, re'sen ornek dosya acildi)")
    print()
    print(karar_ver(kapak, ifade, marka))
    return 0


if __name__ == "__main__":
    sys.exit(main())
