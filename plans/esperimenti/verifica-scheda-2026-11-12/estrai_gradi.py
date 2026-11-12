#!/usr/bin/env python3
"""estrai_gradi.py — le regole dei gradi delle abilità 3.5, dall'SRD in cache.

Scrive `sistemi/dnd35/dati/gradi.toml` e `sistemi/pf1e/dati/gradi.toml`:
  [chiave]   abilità → caratteristica chiave («Climb (Str)» → For)
  [classi]   classe → punti abilità per livello («4 + Int modifier» → 4)
  [tipi]     tipo di creatura → punti per dado vita razziale
  [regole]   massimo dei gradi, moltiplicatore del primo dado vita, minimo per dado

Fonte: olimot/srd-v3.5-md@c7f30a0c (la stessa di talenti.toml), OGL.

Uso
  python3 scripts/riscontro_srd.py scarica                  # riempie la cache
  python3 plans/esperimenti/verifica-scheda-2026-11-12/estrai_gradi.py [--check]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CACHE = Path.home() / ".cache" / "rumblingstone" / "srd" / "srd-v3.5-md-c7f30a0ce11a"
OUT = ROOT / "sistemi" / "dnd35" / "dati" / "gradi.toml"
CAR = {"str": "For", "dex": "Des", "con": "Cos", "int": "Int", "wis": "Sag", "cha": "Car", "none": ""}
FILE_CLASSI = ["basic-rules-and-legal/character-classes-i.md", "basic-rules-and-legal/character-classes-ii.md",
               "basic-rules-and-legal/npc-classes.md", "basic-rules-and-legal/prestige-classes.md",
               "psionics/psionic-classes.md", "epic/epic-prestige-classes.md"]


def _q(s: str) -> str:
    return '"' + s.replace('"', '\\"') + '"'


def chiavi(base: Path) -> "dict[str, str]":
    out = {}
    for f in ("skills-i.md", "skills-ii.md"):
        t = (base / "basic-rules-and-legal" / f).read_text(encoding="utf-8")
        for nome, car in re.findall(r"^#{2,3} ([A-Z][\w' ]+?) <small>\((\w+)", t, flags=re.M):
            if car.lower() in CAR:
                out[nome.strip().lower()] = CAR[car.lower()]
    for f in sorted((base / "psionics").glob("*.md")):
        t = f.read_text(encoding="utf-8")
        for nome, car in re.findall(r"^#{2,3} ([A-Z][\w' ]+?) <small>\((Str|Dex|Con|Int|Wis|Cha)\b", t, flags=re.M):
            out.setdefault(nome.strip().lower(), CAR[car.lower()])
    return dict(sorted(out.items()))


def classi(base: Path) -> "dict[str, int]":
    out = {}
    for rel in FILE_CLASSI:
        f = base / rel
        if not f.is_file():
            continue
        t = f.read_text(encoding="utf-8")
        for blocco in re.split(r"^## ", t, flags=re.M)[1:]:
            nome = blocco.split("\n", 1)[0].strip()
            m = re.search(r"\*\*Skill Points at Each (?:Additional )?Level:?\*\*:?\s*(\d+) \+ Int", blocco)
            if m:
                out[re.sub(r"\s*<small>.*", "", nome).lower()] = int(m.group(1))
    return dict(sorted(out.items()))


def tipi(base: Path) -> "dict[str, int]":
    t = (base / "basic-rules-and-legal" / "types-subtypes-and-special-abilities.md").read_text(encoding="utf-8")
    out = {}
    pezzi = re.split(r"^#{2,4} ([A-Z][\w ]+?) Type\s*$|\*\*([A-Z][\w ]+?) Type:\*\*", t, flags=re.M)
    for i in range(1, len(pezzi) - 2, 3):
        nome = (pezzi[i] or pezzi[i + 1] or "").strip().lower()
        m = re.search(r"Skill points equal to \((\d+) \+ Int modifier", pezzi[i + 2])
        if nome and m:
            out[nome] = int(m.group(1))
    return dict(sorted(out.items()))


PRD = Path.home() / ".cache" / "rumblingstone" / "srd" / "PSRD-Data-76ea47846041"
OUT_PF = ROOT / "sistemi" / "pf1e" / "dati" / "gradi.toml"


def genera_pf1e() -> str:
    """PF1e dal PRD (devonjones/PSRD-Data@76ea4784): `skill_attributes` del Core
    e «Skill points equal to» di ogni tipo nel Bestiary. I punti per livello
    delle classi stanno già in `classi.toml` (`gradi`)."""
    import sqlite3
    core = sqlite3.connect(PRD / "book-cr.db")
    k = {n.lower(): CAR[a.lower()] for n, a in core.execute(
        "select s.name, d.attribute from sections s join skill_attributes d on d.section_id = s.section_id")}
    b1 = sqlite3.connect(PRD / "book-b1.db")
    t = {}
    for nome, corpo in b1.execute("select name, body from sections where body like '%Skill points equal to%'"):
        m = re.search(r"Skill points equal to (\d+) \+ Int modifier", re.sub(r"<[^>]+>", " ", corpo or ""))
        if m and nome:
            t.setdefault(nome.lower(), int(m.group(1)))
    righe = [
        "# sistemi/pf1e/dati/gradi.toml — i gradi delle abilità PF1e (ADR-0124)",
        "# Generato da plans/esperimenti/verifica-scheda-2026-11-12/estrai_gradi.py dal PRD",
        "# (devonjones/PSRD-Data@76ea4784): abilità e caratteristica chiave dal Core,",
        "# «Skill points equal to» di ogni tipo dal Bestiary. I punti per livello delle",
        "# classi sono in classi.toml (`gradi`).",
        "",
        "[regole]",
        "# gradi massimi = dadi vita; un'abilità di classe con almeno 1 grado dà +3;",
        "# nessun moltiplicatore al primo dado; almeno 1 grado per dado; umani +1 per livello",
        "massimo_piu = 0",
        "primo_dado = 1",
        "minimo_per_dado = 1",
        "umano_per_livello = 1",
        "bonus_di_classe = 3",
        "",
        "[chiave]",
        *[f"{_q(a)} = {_q(v)}" for a, v in sorted(k.items())],
        "",
        "[tipi]",
        *[f"{_q(a)} = {v}" for a, v in sorted(t.items())],
        "",
    ]
    return "\n".join(righe)


def genera() -> str:
    k, c, t = chiavi(CACHE), classi(CACHE), tipi(CACHE)
    righe = [
        "# sistemi/dnd35/dati/gradi.toml — i gradi delle abilità 3.5 (ADR-0124)",
        "# Generato da plans/esperimenti/verifica-scheda-2026-11-12/estrai_gradi.py dall'SRD 3.5",
        "# (olimot/srd-v3.5-md@c7f30a0c): «Skills Summary», la riga «Skill Points at Each",
        "# Additional Level» di ogni classe, «Skill points equal to» di ogni tipo.",
        "",
        "[regole]",
        "# gradi massimi in un'abilità di classe = dadi vita + 3; il primo dado vita vale 4 volte;",
        "# almeno 1 punto per dado vita; gli umani hanno 1 punto in più per livello",
        "massimo_piu = 3",
        "primo_dado = 4",
        "minimo_per_dado = 1",
        "umano_per_livello = 1",
        "",
        "[chiave]",
        *[f"{_q(a)} = {_q(v)}" for a, v in k.items()],
        "",
        "[classi]",
        *[f"{_q(a)} = {v}" for a, v in c.items()],
        "",
        "[tipi]",
        *[f"{_q(a)} = {v}" for a, v in t.items()],
        "",
    ]
    return "\n".join(righe)


def main(argv: "list[str]") -> int:
    if not CACHE.is_dir():
        print(f"estrai_gradi: manca la cache {CACHE} (python3 scripts/riscontro_srd.py scarica)", file=sys.stderr)
        return 2
    file = {OUT: genera(), OUT_PF: genera_pf1e()}
    if "--check" in argv:
        vecchi = [f.name for f, t in file.items() if not f.is_file() or f.read_text(encoding="utf-8") != t]
        print("✓ gradi.toml aggiornati" if not vecchi else "✗ da rigenerare: " + ", ".join(vecchi))
        return 1 if vecchi else 0
    for f, t in file.items():
        f.write_text(t, encoding="utf-8")
    print(f"3.5: {len(chiavi(CACHE))} abilità, {len(classi(CACHE))} classi, {len(tipi(CACHE))} tipi; "
          f"PF1e: {OUT_PF.read_text(encoding='utf-8').count(' = ') - 5} voci")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
