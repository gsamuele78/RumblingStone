#!/usr/bin/env python3
"""verifica_scheda.py — tutte le verifiche di regola di una scheda, in una chiamata (ADR-0124).

Scopo
  Un agente che scrive o corregge una scheda chiede al server MCP
  (`rumblingstone-tools`) «che cosa non torna?» e riceve, per ogni difetto,
  la **regola**, il valore **atteso**, quello che la scheda **ha**, la
  **fonte** che decide e `file:riga`. Corregge e richiama finché è pulita.
  Sola lettura: non scrive mai il canone.

  Mette insieme i verificatori che esistono, senza regole nuove:
    talenti  prerequisiti dei talenti (`verifica_talenti`: SRD d20 → manuali
             3.5 → PF1e)
    numeri   pf nella fascia dei dadi vita, BAB, tiri salvezza, lotta,
             attacco, iniziativa (`conformita_statblocchi.giudica`)

  Le regole sono quelle del plugin del sistema della scheda (`sistemi/<id>`).
  Un conto che il plugin non sa fare non compare: `non_verificabili` dice che
  cosa resta fuori e perché.

Uso
  python3 scripts/verifica_scheda.py Bestiario/png/x.md           # una scheda
  python3 scripts/verifica_scheda.py Bestiario/villain --json     # una cartella, per l'agente
  python3 scripts/verifica_scheda.py x.md --check                 # esce 1 se c'è una violazione

Exit  0 = misura fatta (o nessuna violazione con --check)
      1 = violazioni, solo con --check
      2 = errore d'uso

Solo stdlib.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import verifica_talenti as VT  # noqa: E402
from dmcore import lettura_creatura as L  # noqa: E402

#: campo di conformita_statblocchi → riga della scheda dove cercarlo
ETICHETTE = {"BAB": ("bab", "base attack"), "lotta": ("lotta", "grapple", "bmc"),
             "Temp": ("temp", "fort"), "Rifl": ("rifl", "ref"), "Vol": ("vol", "will"),
             "pf": ("pf", "hp"), "iniziativa": ("iniz", "init"), "attacco": ("attacc", "attack", "melee", "mischia")}


def _riga(testo: str, campo: str) -> "int | None":
    chiavi = ETICHETTE.get(campo, (campo.lower(),))
    for i, r in enumerate(testo.splitlines(), 1):
        if any(k in r.lower() for k in chiavi):
            return i
    return None


def numeri(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) dei numeri di una scheda."""
    import conformita_statblocchi as C
    with contextlib.redirect_stdout(io.StringIO()):
        s = L.leggi(p)
        if s is None:
            return [], []
        if not C.del_sistema(p):
            sis = VT.sistema_di(p, s.testo)
            return [], [{"file": VT_rel(p), "riga": None, "verifica": "numeri", "regola": "sistema",
                         "testo": f"i conti di scheda non coprono il sistema {sis}", "fonte": sis}]
        g = C.giudica(s)
    viol, nv = [], []
    ignote = (VT.leggi(p) or {}).get("classi_ignote") or []
    if not g["verificabile"]:
        nv.append({"file": g["file"], "riga": None, "verifica": "numeri", "regola": "lettura",
                   "testo": "dadi vita o caratteristiche non leggibili: nessun conto parte", "fonte": "srd"})
    for campo, (scritto, atteso, scarto) in g["scarti"].items():
        voce = {"file": g["file"], "riga": _riga(s.testo, campo), "verifica": "numeri",
                "regola": f"numero.{campo}", "atteso": atteso, "ha": scritto,
                "testo": f"{campo} {scritto}, la regola dà {atteso} (scarto {scarto:+d})"
                if isinstance(scarto, int) else f"{campo} {scritto}, la regola dà {atteso}",
                "fonte": "srd"}
        if "-cr" not in p.name:
            # conformita_statblocchi è collaudato sulle schede `*-cr*.md`; nei dossier
            # («BAB/Lotta: +8 / +10») la lettura prende il numero sbagliato
            voce["nota"] = "scheda a dossier: la lettura dei numeri non è collaudata su questo formato"
        elif ignote:
            voce["nota"] = "classi che la lettura non conosce: " + ", ".join(ignote)
        if g["template"]:
            voce["nota"] = f"lo scarto si spiega col template {g['template']}"
        if campo in g["come_la_fonte"]:
            voce["nota"] = "uguale alla fonte trascritta"
        if g["decisione"]:
            voce["nota"] = f"decisione aperta al DM: {g['decisione']}"
        (nv if "nota" in voce else viol).append(voce)
    return viol, nv


def VT_rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p)


def talenti(p: Path) -> "tuple[list[dict], list[dict], list[dict]]":
    f = VT.leggi(p)
    if f is None:
        return [], [], []
    v, nv = VT.verifica(f)
    for x in v + nv:
        x["verifica"] = "talenti"
    ign = [{"file": f["file"], "riga": f["riga"], "verifica": "talenti", "regola": "nome",
            "testo": f"«{n}» non è un talento di nessuna fonte", "fonte": None} for n in f["ignoti"]]
    return v, nv, ign


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("percorsi", nargs="+", type=Path, help="schede o cartelle")
    ap.add_argument("--json", action="store_true", help="uscita JSON per l'agente")
    ap.add_argument("--check", action="store_true", help="esce 1 se c'è almeno una violazione")
    a = ap.parse_args(argv)
    percorsi = [p if p.is_absolute() else ROOT / p for p in a.percorsi]
    for p in percorsi:
        if not p.exists():
            print(f"verifica_scheda: {p} non esiste", file=sys.stderr)
            return 2
    viol, nv, lette = [], [], 0
    for p in VT.schede(percorsi):
        tv, tn, ti = talenti(p)
        nvv, nn = numeri(p)
        lette += bool(tv or tn or ti or nvv or nn or L.leggi(p))
        viol += tv + nvv
        nv += tn + ti + nn
    if a.json:
        json.dump({"schede": lette, "violazioni": viol, "non_verificabili": nv}, sys.stdout,
                  ensure_ascii=False, indent=1)
        print()
    else:
        for v in viol:
            dove = f"{v['file']}:{v['riga']}" if v.get("riga") else v["file"]
            nome = f"{v['talento_it']} — manca " if v["verifica"] == "talenti" else ""
            print(f"{dove}: [{v['verifica']}] {nome}{v['testo']}  [regola {v['regola']}, fonte {v['fonte']}]")
        print(f"{'✗' if viol else '✓'} verifica_scheda: {lette} schede, {len(viol)} violazioni in "
              f"{len({v['file'] for v in viol})} schede, {len(nv)} voci non verificabili")
    return 1 if (a.check and viol) else 0


if __name__ == "__main__":
    sys.exit(main())
