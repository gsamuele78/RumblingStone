#!/usr/bin/env python3
"""render_state.py — genera le tabelle di canone di state.md da state.yaml (ADR-0017).

Scopo
  `campaign/state.yaml` è il master dei fatti di §0 (cruscotto archi), §1 (party)
  e §6 (artefatti). Questo tool ne genera la **vista markdown** dentro le regioni
  marcate di `campaign/state.md`, così che il DM continui a leggere un documento
  e non uno YAML.

  È la ragione per cui il lotto esiste: senza rendering, `state.yaml` sarebbe una
  **seconda fonte di verità** — cioè esattamente il difetto C2 che l'audit ha
  appena chiuso (`state.md` e `campaign-history.md` che si dichiaravano entrambi
  sorgente unica). Un master e una vista generata; mai due master.

  Le sezioni di **prosa** (§5 promesse, §7 fili narrativi, i banner dei due tempi)
  NON sono toccate: restano scritte a mano, perché sono narrazione e non dati.

Regioni gestite
  <!-- gen:state:archi -->      … <!-- /gen:state:archi -->
  <!-- gen:state:party -->      … <!-- /gen:state:party -->
  <!-- gen:state:artefatti -->  … <!-- /gen:state:artefatti -->

  Tutto ciò che sta fra i marcatori è **rigenerato**: non modificarlo a mano,
  la modifica va fatta in `state.yaml`.

Uso
  python3 scripts/render_state.py            # rigenera le regioni
  python3 scripts/render_state.py --check    # gate CI: segnala drift, non scrive
  python3 scripts/render_state.py --stdout   # stampa senza toccare i file

Input   campaign/state.yaml
Output  campaign/state.md (regioni marcate) — deterministico, idempotente
Exit    0 = ok / in sync · 1 = drift (--check) o errore di dominio · 2 = errore d'uso
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_YAML = ROOT / "campaign" / "state.yaml"
STATE_MD = ROOT / "campaign" / "state.md"

try:
    import yaml
except ImportError:  # pragma: no cover
    print("✗ render_state: serve pyyaml (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

FASE = {"giocato": "✅", "in_corso": "🟡", "preparato": "⬜"}

BANNER = ("<!-- GENERATO da scripts/render_state.py a partire da campaign/state.yaml — "
          "non modificare a mano (ADR-0017) -->")


def _cell(v) -> str:
    """Una cella markdown: None diventa em-dash, le pipe interne sono neutralizzate."""
    if v is None or (isinstance(v, str) and not v.strip()):
        return "—"
    return str(v).replace("|", "\\|").replace("\n", " ").strip()


def render_archi(d: dict) -> str:
    out = [BANNER, "", "| Arc | Fase | Stato | March Clock | PG Lv | Note |", "|---|---|---|---|---|---|"]
    for a in d["archi"]:
        out.append("| {} | {} | {} | {} | {} | {} |".format(
            _cell(a["arco"]), FASE[a["tempo"]], _cell(a["stato"]),
            _cell(a.get("march_clock")), _cell(a.get("pg_livello")), _cell(a.get("note"))))
    out += ["", "**Legenda**: ✅ giocato · 🟡 in corso · ⬜ preparato (non giocato) · "
                "❌ fallito · ⏸ sospeso"]
    return "\n".join(out)


def render_party(d: dict) -> str:
    c = d["confine"]
    out = [BANNER, "",
           f"| PC | Class | **Oggi al tavolo** ({c['giocato_fino_a'].split('—')[0].strip()}) "
           f"| **Preparato** (non ancora vero) | Open personal threads |",
           "|---|---|---|---|---|"]
    for p in d["party"]:
        out.append("| {} | {} | {} | {} | {} |".format(
            _cell(p["pg"]), _cell(p["classe"]), _cell(p["oggi"]),
            _cell(p.get("preparato")), _cell(p.get("filoni"))))
    return "\n".join(out)


def render_artefatti(d: dict) -> str:
    out = [BANNER, "",
           "| Artifact | Holder | **Oggi al tavolo** | **Preparato** (non ancora vero) |",
           "|---|---|---|---|"]
    for a in d["artefatti"]:
        out.append("| {} | {} | {} | {} |".format(
            _cell(a["artefatto"]), _cell(a["portatore"]),
            _cell(a["oggi"]), _cell(a.get("preparato"))))
    return "\n".join(out)


RENDERERS = {"archi": render_archi, "party": render_party, "artefatti": render_artefatti}


def region_re(name: str) -> re.Pattern:
    return re.compile(
        rf"(<!-- gen:state:{name} -->\n)(.*?)(\n<!-- /gen:state:{name} -->)",
        re.DOTALL,
    )


def apply_regions(md: str, data: dict) -> tuple[str, list[str]]:
    """Sostituisce il contenuto delle regioni. Ritorna (testo, regioni mancanti)."""
    missing = []
    for name, fn in RENDERERS.items():
        rx = region_re(name)
        if not rx.search(md):
            missing.append(name)
            continue
        md = rx.sub(lambda m: m.group(1) + fn(data) + m.group(3), md)
    return md, missing


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="render_state.py",
        description="Genera le tabelle di canone di state.md da state.yaml (ADR-0017).",
    )
    ap.add_argument("--check", action="store_true",
                    help="Verifica che le regioni siano allineate; non scrive nulla.")
    ap.add_argument("--stdout", action="store_true",
                    help="Stampa le regioni generate senza toccare i file.")
    args = ap.parse_args(argv)

    if not STATE_YAML.exists():
        print(f"✗ render_state: {STATE_YAML} non esiste", file=sys.stderr)
        return 2
    data = yaml.safe_load(STATE_YAML.read_text(encoding="utf-8"))

    if args.stdout:
        for name, fn in RENDERERS.items():
            print(f"--- {name} ---\n{fn(data)}\n")
        return 0

    md = STATE_MD.read_text(encoding="utf-8")
    new, missing = apply_regions(md, data)

    if missing:
        print("✗ render_state: regioni assenti in state.md: " + ", ".join(missing),
              file=sys.stderr)
        print("  Inserire i marcatori <!-- gen:state:NOME --> … <!-- /gen:state:NOME -->",
              file=sys.stderr)
        return 1

    if args.check:
        if new != md:
            print("✗ render_state: state.md è fuori sync con state.yaml", file=sys.stderr)
            print("  Rigenerare con: python3 scripts/render_state.py", file=sys.stderr)
            return 1
        print("✓ render_state: state.md allineato a state.yaml")
        return 0

    if new == md:
        print("✓ render_state: già allineato — nessuna scrittura")
        return 0
    STATE_MD.write_text(new, encoding="utf-8")
    print(f"✓ render_state: rigenerate {len(RENDERERS)} regioni in campaign/state.md")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
