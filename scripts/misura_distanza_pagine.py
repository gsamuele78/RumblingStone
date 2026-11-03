#!/usr/bin/env python3
r"""misura_distanza_pagine.py — quante pagine sfoglia il DM per trovare i numeri di chi ha davanti?

## Perché esiste

La prova di ADR-0107 (2026-11-03) ha misurato la distanza fra la scena e lo
statblocco **a mano**: un DM e un playtester hanno letto i due PDF e contato
le pagine («numeri di Zog'tar a +31, mappa a +37»). È la misura che conta al
tavolo, ma una lettura a mano non si ripete a ogni commit.

Questo strumento la rifà sul **PDF stampato**, con PyMuPDF (AGPL, già nella
dotazione di sviluppo per `validate_booklets --stampa`). È una tecnica di
*document AI* nella sua forma più semplice e deterministica: si legge il testo
di ogni pagina, non si indovina niente.

Per ogni persona che ha un riquadro nel repo (`dmcore.chi_si_incontra`):

* **pagine d'azione**: le pagine che la nominano almeno 3 volte;
* **pagine dei numeri**: le pagine che la nominano e hanno sia «CA N» sia «pf N»;
* per ogni pagina d'azione, la distanza dalla pagina dei numeri più vicina.

Il numero che riassume è la **mediana** delle distanze. Il 2026-11-03, sui due
PDF della prova (157 e 172 pagine): Zog'tar 23,5 → 5, Skullcrusher 21 → 4,
Balvar 28,5 → 5,5, Durin 53 → 4,5. Durik peggiora (102,5 → 112): i suoi numeri
stanno solo in appendice, e le pagine in più li allontanano. La misura lo dice.

## Cosa NON misura, dichiarato

* una pagina che nomina la persona senza parlarne (un elenco) conta come
  pagina d'azione se la nomina 3 volte;
* uno statblocco spezzato su due pagine, con CA e pf su pagine diverse, non
  conta come pagina dei numeri;
* le mappe: le piante non hanno testo affidabile da cui riconoscerle.

È un **indicatore**, come `misura_standard_tavolo`: esce sempre 0.

## Uso

    python3 scripts/misura_distanza_pagine.py VOLUME.pdf [ALTRO.pdf ...]
    python3 scripts/misura_distanza_pagine.py --json A.pdf B.pdf
    python3 scripts/misura_distanza_pagine.py --nomi "Zog'tar,Skullcrusher" A.pdf
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from misura_standard_tavolo import chiave, conta_nome, piega  # noqa: E402

AZIONE = 3
CA = re.compile(r"\bca\s+\d+")
PF = re.compile(r"\bpf\s+\d+")


def pagine(pdf: Path) -> list[str]:
    import pymupdf  # noqa: PLC0415
    with pymupdf.open(pdf) as doc:
        # l'apostrofo tipografico del PDF («Zog’tar») si piega in «-»: va tolto prima
        return [piega(re.sub(r"[’ʼ‘]", "", p.get_text())) for p in doc]


def distanze(pp: list[str], k: str) -> "dict | None":
    """Le distanze di una persona, o `None` se non ha pagine d'azione o di numeri."""
    numeri = [i for i, t in enumerate(pp) if conta_nome(t, k) and CA.search(t) and PF.search(t)]
    azione = [i for i, t in enumerate(pp) if conta_nome(t, k) >= AZIONE]
    if not numeri or not azione:
        return None
    d = [min(abs(i - j) for j in numeri) for i in azione]
    return {"pagine_azione": len(azione), "pagine_numeri": len(numeri),
            "mediana": statistics.median(d), "massima": max(d),
            "entro_una": sum(x <= 1 for x in d)}


def chiavi_del_repo() -> list[str]:
    from dmcore import chi_si_incontra  # noqa: PLC0415
    idx = chi_si_incontra.indice_del_repo()
    return sorted({chiave(p.nome) or k for k, p in idx.riquadri.items()} - {""})


def misura(pdf: Path, chiavi: list[str]) -> dict:
    pp = pagine(pdf)
    out = {}
    for k in chiavi:
        d = distanze(pp, k)
        if d:
            out[k] = d
    return {"pagine": len(pp), "persone": out}


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pdf", nargs="+", type=Path)
    ap.add_argument("--nomi", help="nomi separati da virgola (default: chi ha un riquadro nel repo)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    chiavi = [chiave(n) for n in a.nomi.split(",")] if a.nomi else chiavi_del_repo()
    dati = {str(p): misura(p, chiavi) for p in a.pdf}
    if a.json:
        print(json.dumps(dati, ensure_ascii=False, indent=1))
        return 0
    tutte = sorted({k for v in dati.values() for k in v["persone"]})
    print(f"{'persona':<16}" + "".join(f"{Path(p).name[:22]:>24}" for p in dati))
    for k in tutte:
        celle = []
        for v in dati.values():
            d = v["persone"].get(k)
            celle.append(f"{d['mediana']:>6} (max {d['massima']:>3})" if d else "—")
        print(f"{k:<16}" + "".join(f"{c:>24}" for c in celle))
    print("mediana delle pagine fra dove la persona agisce e dove stanno CA e pf "
          "(indicatore, non cancello)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
