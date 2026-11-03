#!/usr/bin/env python3
r"""misura_box_telecomando.py — i box che decidono per il gruppo cosa capisce, sa o prova.

## Perché esiste

Un box read-aloud descrive; non dice ai giocatori cosa pensano («capite che
qualunque cosa facciate, lui ne guadagnerà»). Il 2026-11-03 (RICERCA-GUARDRAIL)
due configurazioni a confronto sui 569 box del repo:

* prima: 40 verbi di pensiero e sentimento in seconda persona, singolare e
  plurale: 15 colpi fuori dalle battute, **2 veri** (13%). Il singolare era
  quasi sempre un'eco personale voluta per un PG («la ricordi»), un sogno o un
  effetto magico;
* **rigorosa**: solo la seconda persona **plurale**, cioè il gruppo intero,
  fuori dalle battute, e non quando il verbo è seguito da «voi» («quello che
  decidete voi» dà la scelta, non la toglie): 4 colpi, **2 veri** (50%).

Si adotta la seconda, come indicatore: un elenco breve da leggere, non un
cancello. Deterministico, nessuna dipendenza.

## Uso

    python3 scripts/misura_box_telecomando.py [FILE.md ...]   # default: i file vivi
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

#: Seconda persona plurale di capire, sapere, ricordare, decidere, credere,
#: pensare, temere, rendersi conto, accorgersi, sentirsi: il gruppo intero.
VERBI = re.compile(
    r"\b(capite|sapete|ricordate|decidete|credete|pensate|temete|"
    r"vi rendete conto|vi accorgete|vi sentite)\b(?!\s+voi\b(?!\s+che))", re.I)
BATTUTA = re.compile(r"«[^»]*»|\"[^\"]*\"|“[^”]*”")


def colpi(testo: str) -> list[str]:
    """Le frasi dei box col verbo, tolte le battute dei PNG.

    >>> colpi("> *Sorride, e capite che qualunque cosa facciate, lui ne guadagnerà.*")
    ['capite']
    >>> colpi("> *Le loro mani fanno quello che decidete voi.*")
    []
    >>> colpi("> *Capite anche voi che è finita.*")
    ['capite']
    >>> colpi('> *«Lo sapete anche voi» dice il re.*')
    []
    """
    import misura_craft as mc
    out = []
    for b in mc.box_read_aloud(testo):
        corpo = BATTUTA.sub(" ", mc.corpo_del_box(b))
        out += [m.group(1).lower() for m in VERBI.finditer(corpo)]
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="*", type=Path, help="file markdown (default: i file vivi)")
    a = ap.parse_args(argv)
    import misura_craft as mc
    if a.file:
        fs = a.file
    else:
        import misura_craft as mc
        fs = [p for p in sorted(ROOT.glob("0[0-9]_*/**/*.md")) + sorted((ROOT / "10-stand-alone").glob("**/*.md"))
              if not any(x in str(p) for x in mc.ESCLUSI) and not any(x in p.name for x in mc.ESCLUSI_NOME)]
    import misura_craft as mc
    tot, trovati = 0, []
    for p in fs:
        t = p.read_text(errors="replace")
        tot += len(mc.box_read_aloud(t))
        for b in mc.box_read_aloud(t):
            corpo = BATTUTA.sub(" ", mc.corpo_del_box(b))
            for m in VERBI.finditer(corpo):
                trovati.append((p, corpo[max(0, m.start() - 90):m.end() + 70].strip()))
    print(f"BOX TELECOMANDO — {tot} box, {len(trovati)} da leggere (indicatore, non cancello)")
    for p, f in trovati:
        rel = p.resolve().relative_to(ROOT) if p.resolve().is_relative_to(ROOT) else p
        print(f"  {rel}: …{f}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
