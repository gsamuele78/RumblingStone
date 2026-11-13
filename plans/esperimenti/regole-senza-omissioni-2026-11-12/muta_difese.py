#!/usr/bin/env python3
"""Banco del lotto 7, seconda parte (ADR-0126): una RI o una RD sbagliata messa apposta.

Per ogni scheda del Bestiario che scrive una resistenza agli incantesimi o una
riduzione del danno N/— fuori dalle righe di storia, si scrivono due copie per
numero: una con un punto in più e una con un punto in meno. Una copia conta
come trovata se compare una violazione `numero.RI` o `numero.RD`. Le schede che
il controllo non giudica (nessuna razza o classe della tabella) non possono
dare violazioni: si contano a parte, è la portata del controllo.

Uso: python3 muta_difese.py  (scrive misure-difese.json accanto)
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402

CAMPI = {"RI": V._SCRITTA_RI, "RD": V._SCRITTA_RD}


def _giudica(testo: str, nome: str):
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / nome
        q.write_text(testo, encoding="utf-8")
        return V.difese(q)


def _prima(testo: str, rx):
    """La prima scrittura fuori dalle righe di storia, come (inizio, fine) del numero nel testo."""
    pos = 0
    for riga in testo.split("\n"):
        if not V._RIGA_DI_STORIA.match(riga):
            m = rx.search(riga)
            if m:
                return pos + m.start(1), pos + m.end(1), int(m.group(1))
        pos += len(riga) + 1
    return None


def main() -> int:
    conto = {c: {"schede che la scrivono": 0, "giudicate": 0, "già fuori regola": 0, "dubbie": 0} for c in CAMPI}
    esiti = {f"{c} {v}": [0, 0] for c in CAMPI for v in ("più 1", "meno 1")}      # trovate, scritte
    perse = []
    for p in sorted((ROOT / "Bestiario").rglob("*.md")):
        testo = p.read_text(encoding="utf-8")
        if V.L.leggi(p) is None:
            continue
        v, nv = V.difese(p)
        for campo, rx in CAMPI.items():
            dove = _prima(testo, rx)
            if dove is None:
                continue
            conto[campo]["schede che la scrivono"] += 1
            regola = f"numero.{campo}"
            if any(x["regola"] == regola for x in v):
                conto[campo]["già fuori regola"] += 1
                continue
            if any(x["regola"] == regola for x in nv):
                conto[campo]["dubbie"] += 1
                continue
            a, b, n = dove
            pv, pn = _giudica(testo[:a] + str(n + 40) + testo[b:], p.name)
            if not any(x["regola"] == regola for x in pv + pn):
                continue                                  # il controllo non la guarda
            conto[campo]["giudicate"] += 1
            for nome, passo in (("più 1", 1), ("meno 1", -1)):
                chiave = f"{campo} {nome}"
                esiti[chiave][1] += 1
                cv, _ = _giudica(testo[:a] + str(n + passo) + testo[b:], p.name)
                if any(x["regola"] == regola for x in cv):
                    esiti[chiave][0] += 1
                else:
                    perse.append(f"{p.relative_to(ROOT)}: {chiave}")
    fuori = {"conto": conto, "esiti": {k: {"trovate": a, "scritte": b} for k, (a, b) in esiti.items()},
             "perse": perse}
    (Path(__file__).parent / "misure-difese.json").write_text(
        json.dumps(fuori, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for c, d in conto.items():
        for k, n in d.items():
            print(f"{c} {k:30} {n}")
    for k, (a, b) in esiti.items():
        print(f"{k:34} {a}/{b}")
    for x in perse:
        print("  persa:", x)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
