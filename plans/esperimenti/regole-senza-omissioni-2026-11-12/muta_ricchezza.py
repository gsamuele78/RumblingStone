#!/usr/bin/env python3
"""Banco del lotto 8 (ADR-0126): un oggetto troppo caro aggiunto apposta.

A ogni scheda del Bestiario che il verificatore legge, con un blocco solo e
coi dadi vita scritti, si aggiunge in fondo una riga «Equipaggiamento» con un
*anello di protezione +5* e un *mantello della resistenza +5* (75.000 mo), che
supera il valore di un PNG fino al 15° livello. La copia conta come trovata se
compare una violazione `equipaggiamento.valore`, come non verificabile se la
razza non ha un modificatore di livello noto o il livello passa il 20°. Le
schede dal 16° livello effettivo in su non si possono giudicare con questa
aggiunta e si contano a parte.

Uso: python3 muta_ricchezza.py  (scrive misure-ricchezza.json accanto)
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402

AGGIUNTA = "\n\n**Equipaggiamento** *anello di protezione +5*, *mantello della resistenza +5*\n"


def main() -> int:
    conto = {"schede lette": 0, "con equipaggiamento dal prezzo certo": 0, "già fuori regola": 0,
             "sopra il 15° livello": 0}
    esito = {"violazione": 0, "non verificabile": 0, "niente": 0}
    perse = []
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        s = V.L.leggi(p)
        if s is None or not sum(g.n for g in s.gruppi):
            continue
        conto["schede lette"] += 1
        v0, n0 = V.ricchezza(p)
        if v0:
            conto["già fuori regola"] += 1
            continue
        from dmcore import sistemi as S
        d = S.dati("dnd35", "creature.costruzione")["oggetti"]
        testo = p.read_text(encoding="utf-8")
        if any(V._oggetti_col_prezzo(r, d, "dnd35") for _, r in V._righe_dell_equipaggiamento(testo)):
            conto["con equipaggiamento dal prezzo certo"] += 1
        with tempfile.TemporaryDirectory() as t:
            q = Path(t) / p.name
            q.write_text(testo + AGGIUNTA, encoding="utf-8")
            v, n = V.ricchezza(q)
        if v:
            esito["violazione"] += 1
        elif len(n) > len(n0) or (n and n != n0):
            esito["non verificabile"] += 1
        elif sum(g.n for g in s.gruppi) > 15:
            conto["sopra il 15° livello"] += 1
        else:
            esito["niente"] += 1
            perse.append(str(p.relative_to(ROOT)))
    fuori = {"conto": conto, "esito": esito, "perse": perse}
    (Path(__file__).parent / "misure-ricchezza.json").write_text(
        json.dumps(fuori, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for k, n in {**conto, **esito}.items():
        print(f"{k:40} {n}")
    for x in perse:
        print("  persa:", x)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
