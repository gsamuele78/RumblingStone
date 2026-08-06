#!/usr/bin/env python3
"""validate_links.py — gate sui collegamenti e sui percorsi assoluti (finding E3).

Scopo
  Due difetti che rendono un deliverable non consegnabile, entrambi invisibili
  finché qualcuno non apre il file:

  1. **link relativi rotti** — il caso peggiore trovato dall'audit è
     `PALIO-BOOKLET.hb.md`, che referenzia 13 fra stemmi e mappe mai prodotti:
     il booklet si genera, ma esce con 13 immagini rotte;
  2. **percorsi assoluti della macchina di chi ha scritto** (`/home/<utente>/…`,
     `C:\\Users\\…`, `file:///…`). Un playbook che insegna a un DM terzo un
     comando con dentro la home di qualcun altro non è un documento: è un
     appunto privato.

  `validate_docs.py` copre gli stessi difetti sui **tre documenti d'ingresso**;
  questo li copre su **tutto il repo**. I due gate non si sovrappongono per caso:
  quello è un contratto sulla struttura dichiarata, questo è igiene diffusa.

Falsi positivi, esclusi per costruzione
  - URL, ancore, `mailto:`;
  - host-relative di Homebrewery (`/assets/…`): risolvono sul dominio del brew;
  - segnaposto didattici (`percorso/relativo/immagine.png`, `<...>`, `[...]`);
  - mirror per-agente gitignored (`.claude/`, `.cursor/`, …);
  - le direttive `<!-- validate-links: ignore -->` e `ignore-begin/end`, per i
    passaggi che citano un percorso **proprio per dire che è rotto**.

Uso
  python3 scripts/validate_links.py [--path DIR] [--json] [--verbose]

Input   tutti i `.md` del repo (escluse le cartelle generate)
Output  stdout testuale, oppure JSON con --json
Exit    0 = pulito · 1 = link rotti o percorsi assoluti · 2 = errore d'uso
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Cartelle generate o storiche: non sono deliverable e non si bonificano.
SKIP_DIRS = {".git", "build", ".claude", ".cursor", ".gemini", ".chatgpt",
             ".windsurf", ".kilo", ".agents", ".github", "_ARCHIVIO", "Old",
             # `converters/` è dichiarato `external-toolchain` (ADR-0011) e le sue
             # guide di deploy contengono legittimamente percorsi di SERVER
             # (`/home/htmlconverter/`, `/home/linuxbrew/`): sono utenti di
             # servizio, non la macchina di chi scrive. Il difetto che questo gate
             # cerca è un altro, e includerli lo annegherebbe nel rumore.
             "converters"}

LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
IMG_HTML = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)

# Percorsi assoluti di una macchina: il difetto più insidioso, perché il file
# funziona benissimo per chi l'ha scritto.
ABSOLUTE = re.compile(r"(?:file://)?/(?:home|Users)/[A-Za-z0-9_.-]+/|[A-Z]:\\\\Users\\\\")

PLACEHOLDER = re.compile(r"[<>{}]|\.\.\.|^percorso/|^path/|^URL$|^#", re.I)
HOMEBREWERY_HOST = ("/assets/", "/api/", "/homebrew/")

IGNORE_LINE = "<!-- validate-links: ignore -->"
IGNORE_BEGIN = "<!-- validate-links: ignore-begin -->"
IGNORE_END = "<!-- validate-links: ignore-end -->"


def ignored_lines(text: str) -> set[int]:
    out: set[int] = set()
    in_block = False
    for lineno, raw in enumerate(text.splitlines(), start=1):
        if IGNORE_BEGIN in raw:
            in_block = True
            out.add(lineno)
        elif IGNORE_END in raw:
            in_block = False
            out.add(lineno)
        elif in_block or IGNORE_LINE in raw:
            out.add(lineno)
    return out


def md_files(base: Path):
    for p in sorted(base.rglob("*.md")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def check_file(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    skip = ignored_lines(text)
    rel = str(path.relative_to(ROOT))
    problems: list[dict] = []

    for lineno, raw in enumerate(text.splitlines(), start=1):
        if lineno in skip:
            continue

        # 1) percorsi assoluti — si segnalano ovunque compaiano
        if ABSOLUTE.search(raw):
            frammento = ABSOLUTE.search(raw).group(0)
            problems.append({"file": rel, "line": lineno, "kind": "path-assoluto",
                             "target": frammento,
                             "reason": "percorso della macchina di chi ha scritto: "
                                       "non funziona per nessun altro"})

        # 2) link relativi rotti
        targets = [t for _, t in LINK.findall(raw)] + IMG_HTML.findall(raw)
        for tgt in targets:
            t = tgt.strip()
            if t.startswith(("http://", "https://", "#", "mailto:", "data:")):
                continue
            if t.startswith(HOMEBREWERY_HOST):
                continue
            if PLACEHOLDER.search(t):
                continue
            clean = urllib.parse.unquote(t.split("#", 1)[0].strip())
            if not clean or clean.startswith("/"):
                continue
            if not (path.parent / clean).exists():
                problems.append({"file": rel, "line": lineno, "kind": "link-rotto",
                                 "target": clean,
                                 "reason": "il file referenziato non esiste"})
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="validate_links.py",
        description="Verifica link relativi e percorsi assoluti in tutti i .md del repo.",
    )
    ap.add_argument("--path", type=Path, default=ROOT,
                    help="Sottoalbero da controllare (default: tutto il repo).")
    ap.add_argument("--json", action="store_true", help="Report in JSON (opt-in).")
    ap.add_argument("--verbose", action="store_true", help="Stampa il numero di file esaminati.")
    args = ap.parse_args(argv)

    base = args.path.resolve()
    if not base.exists():
        print(f"✗ validate_links: {base} non esiste", file=sys.stderr)
        return 2

    problems: list[dict] = []
    n = 0
    for p in md_files(base):
        n += 1
        problems.extend(check_file(p))

    if args.json:
        print(json.dumps({"report_version": 1, "files": n, "problems": problems},
                         indent=2, ensure_ascii=False))
        return 1 if problems else 0

    if not problems:
        print(f"✓ validate_links: {n} file, nessun link rotto e nessun percorso assoluto")
        return 0

    rotti = [p for p in problems if p["kind"] == "link-rotto"]
    assoluti = [p for p in problems if p["kind"] == "path-assoluto"]
    print(f"✗ validate_links: {len(rotti)} link rotti, {len(assoluti)} percorsi assoluti "
          f"(su {n} file)\n", file=sys.stderr)
    for p in problems:
        print(f"  {p['file']}:{p['line']}  [{p['kind']}]  {p['target']}", file=sys.stderr)
    print("\nUn link rotto o un path assoluto rendono il file non consegnabile.",
          file=sys.stderr)
    print("Se un passaggio cita un percorso rotto di proposito, usare "
          "<!-- validate-links: ignore -->. Finding E3, audit 2026-08.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
