#!/usr/bin/env python3
"""estrai_prd_pf1e.py — le tabelle numeriche PF1e dei plugin, dal PRD in cache.

Scrive i dati del plugin `sistemi/pf1e/dati/` leggendo il PRD di Pathfinder 1e
(`devonjones/PSRD-Data@76ea4784`, scaricato con `riscontro_srd.py scarica`).
Niente numeri a mano: ogni valore viene da una tabella del PRD, citata per
libro, id della sezione e nome. Rilanciato sulla stessa cache, riscrive gli
stessi byte (con `--check` esce 1 se i file sul disco sono diversi).

    python3 plans/esperimenti/sistemi-plugin-2026-11-07/estrai_prd_pf1e.py           # scrive
    python3 plans/esperimenti/sistemi-plugin-2026-11-07/estrai_prd_pf1e.py --check   # confronta

Tabelle (Open Game Content, OGL 1.0a; il testo della licenza è in OGL.txt):
    book-cr 2743  Character Advancement and Level-Dependent Bonuses  → pe.toml
    book-cr 3655  Experience Point Awards                            → incontri.toml
    book-cr 3653  Encounter Design                                   → incontri.toml
    book-cr 3661  Treasure Values per Encounter                      → tesoro.toml
    book-b1 116   Creature Statistics by Type                        → creature.toml
    book-b1 160   Size Bonuses and Penalties                         → creature.toml
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sqlite3
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / "sistemi" / "pf1e" / "dati"
COMMIT = "76ea47846041"
PRD = f"PSRD-Data-{COMMIT}"


def cache() -> Path:
    for c in (os.environ.get("RUMBLINGSTONE_SRD_CACHE"),
              os.path.join(os.environ.get("XDG_CACHE_HOME", ""), "rumblingstone", "srd")
              if os.environ.get("XDG_CACHE_HOME") else None,
              str(Path.home() / ".cache" / "rumblingstone" / "srd")):
        if c and (Path(c) / PRD).is_dir():
            return Path(c) / PRD
    sys.exit("manca il PRD in cache: python3 scripts/riscontro_srd.py scarica")


class _Righe(HTMLParser):
    def __init__(self):
        super().__init__()
        self.righe, self._riga, self._cella = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._riga = []
        elif tag in ("td", "th") and self._riga is not None:
            self._cella = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cella is not None:
            self._riga.append(re.sub(r"\s+", " ", "".join(self._cella)).strip())
            self._cella = None
        elif tag == "tr" and self._riga is not None:
            self.righe.append(self._riga)
            self._riga = None

    def handle_data(self, data):
        if self._cella is not None:
            self._cella.append(data)


def tabella(base: Path, libro: str, sid: int, nome: str) -> "list[list[str]]":
    c = sqlite3.connect(base / f"book-{libro}.db")
    r = c.execute("select name, body from sections where section_id=?", (sid,)).fetchone()
    if not r or r[0] != nome:
        sys.exit(f"book-{libro} {sid}: atteso «{nome}», trovato «{r and r[0]}»")
    p = _Righe()
    p.feed(html.unescape(r[1]))
    return [x for x in p.righe if x]


def numero(s: str) -> int:
    s = s.replace(",", "").replace("gp", "").replace("–", "-").replace("–", "-").strip()
    return int(s)


def fonte(libro: str, sid: int, nome: str) -> str:
    return f'fonte = "PRD PF1e, devonjones/PSRD-Data@{COMMIT[:8]}, book-{libro}.db sezione {sid} «{nome}»"'


def pe(base: Path) -> str:
    nome = "Table: Character Advancement and Level-Dependent Bonuses"
    righe = tabella(base, "cr", 2743, nome)
    tracce = {"lenta": {}, "media": {}, "veloce": {}}
    for r in righe:
        m = re.match(r"^(\d+)(st|nd|rd|th)$", r[0])
        if not m:
            continue
        liv = int(m.group(1))
        for k, v in zip(("lenta", "media", "veloce"), r[1:4]):
            tracce[k][liv] = 0 if liv == 1 else numero(v)
    out = ["# sistemi/pf1e/dati/pe.toml — i PE per livello, tre tracce (generato da estrai_prd_pf1e.py)",
           fonte("cr", 2743, nome), ""]
    for k in ("lenta", "media", "veloce"):
        out.append(f"[soglie.{k}]")
        out += [f'"{liv}" = {v}' for liv, v in sorted(tracce[k].items())]
        out.append("")
    assert all(len(t) == 20 for t in tracce.values())
    return "\n".join(out)


def incontri(base: Path) -> str:
    n1 = "Table: Experience Point Awards"
    righe = tabella(base, "cr", 3655, n1)
    px = {}
    for r in righe:
        if re.fullmatch(r"\d+(/\d+)?", r[0]) and len(r) >= 2:
            px[r[0]] = numero(r[1])
    n2 = "Table: Encounter Design"
    diff = {}
    for r in tabella(base, "cr", 3653, n2):
        if len(r) == 2 and r[1].startswith("APL"):
            d = r[1].replace("APL", "").replace("–", "-").replace("–", "-").strip() or "0"
            diff[r[0]] = int(d)
    out = ["# sistemi/pf1e/dati/incontri.toml — PE per GS e difficoltà (generato da estrai_prd_pf1e.py)",
           "# Un incontro PF1e vale la somma dei PE delle creature; il suo GS è il più alto",
           "# il cui valore in PE non supera la somma («Designing Encounters», book-cr 3652).",
           fonte("cr", 3655, n1), f'fonte_difficolta = "book-cr.db sezione 3653 «{n2}»"',
           'metodo = "somma_px"  # letto da suggest_encounter (ADR-0111, L4)', "", "[px_per_gs]"]
    def chiave(g):
        a, _, b = g.partition("/")
        return int(a) / int(b) if b else int(a)
    out += [f'"{g}" = {v}' for g, v in sorted(px.items(), key=lambda kv: chiave(kv[0]))]
    out += ["", "[difficolta]  # GS dell'incontro = APL + scarto"]
    out += [f'"{k.lower()}" = {v}' for k, v in diff.items()]
    assert len(px) == 30 and diff
    return "\n".join(out) + "\n"


def tesoro(base: Path) -> str:
    nome = "Table: Treasure Values per Encounter"
    out = ["# sistemi/pf1e/dati/tesoro.toml — mo per incontro per APL (generato da estrai_prd_pf1e.py)",
           fonte("cr", 3661, nome), ""]
    tr = {"lenta": {}, "media": {}, "veloce": {}}
    for r in tabella(base, "cr", 3661, nome):
        if re.fullmatch(r"\d+", r[0]) and len(r) >= 4:
            for k, v in zip(("lenta", "media", "veloce"), r[1:4]):
                tr[k][int(r[0])] = numero(v)
    for k in ("lenta", "media", "veloce"):
        out.append(f"[mo_per_incontro.{k}]")
        out += [f'"{a}" = {v}' for a, v in sorted(tr[k].items())]
        out.append("")
    assert all(len(t) == 20 for t in tr.values())
    return "\n".join(out)


def creature(base: Path) -> str:
    n1 = "Table: Creature Statistics by Type"
    bab = {"HD × 3/4 (Medium BAB)": 0.75, "HD (Fast BAB)": 1.0, "HD × 1/2 (Slow BAB)": 0.5}
    ts = {"Fort": "temp", "Ref": "rifl", "Will": "vol"}
    tipi = []
    for r in tabella(base, "b1", 116, n1):
        if len(r) == 5 and r[1].startswith("d"):
            buoni = [ts[x.strip()] for x in r[3].split(",") if x.strip() in ts]
            var = re.search(r"any (one|two)", r[3])
            tipi.append((r[0].lower(), int(r[1][1:]), bab[r[2]], buoni,
                         {"one": 1, "two": 2}[var.group(1)] if var else 0,
                         int(re.match(r"(\d+)", r[4]).group(1))))
    n2 = "Table: Size Bonuses and Penalties"
    taglie = []
    for r in tabella(base, "b1", 160, n2):
        if len(r) == 5 and r[0] in ("Fine", "Diminutive", "Tiny", "Small", "Medium", "Large",
                                    "Huge", "Gargantuan", "Colossal"):
            taglie.append((r[0].lower(), numero(r[1]), numero(r[2])))
    out = ["# sistemi/pf1e/dati/creature.toml — tipi e taglie PF1e (generato da estrai_prd_pf1e.py)",
           fonte("b1", 116, n1), f'fonte_taglie = "book-b1.db sezione 160 «{n2}»"', "",
           "# tipo = { dv = faccia del dado, bab = per DV, ts_buoni, ts_a_scelta (umanoide 1, esterno 2), gradi = per DV + Int }",
           "[tipi]"]
    for nome, dv, b, buoni, scelta, gradi in tipi:
        lista = ", ".join(f'"{x}"' for x in buoni)
        out.append(f'"{nome}" = {{ dv = {dv}, bab = {b}, ts_buoni = [{lista}], ts_a_scelta = {scelta}, gradi = {gradi} }}')
    out += ["", "# taglia = { ca_attacco, bmc_dmc }", "[taglie]"]
    out += [f'"{n}" = {{ ca_attacco = {a}, bmc_dmc = {c} }}' for n, a, c in taglie]
    assert len(tipi) == 13 and len(taglie) == 9
    return "\n".join(out) + "\n"


FILE = {"pe.toml": pe, "incontri.toml": incontri, "tesoro.toml": tesoro, "creature.toml": creature}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    base = cache()
    diversi = []
    for nome, f in FILE.items():
        testo = f(base)
        dest = DEST / nome
        if a.check:
            if not dest.is_file() or dest.read_text(encoding="utf-8") != testo:
                diversi.append(nome)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(testo, encoding="utf-8")
            print(f"scritto {dest.relative_to(ROOT)}")
    for d in diversi:
        print(f"🔴 {d} diverso dal PRD")
    return 1 if diversi else 0


if __name__ == "__main__":
    sys.exit(main())
