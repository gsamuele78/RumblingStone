#!/usr/bin/env python3
"""Scrive `sistemi/dnd35/dati/linguaggi.toml`: i linguaggi che razza e classe danno da soli (ADR-0126, lotto 7).

Uso: python3 estrai_linguaggi.py [<cartella srd-v3.5-md>]            # scrive il file
     python3 estrai_linguaggi.py --check [<cartella srd-v3.5-md>]    # 1 se il file non è aggiornato

Dall'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c, OGL), solo nomi:
  razze   «Automatic Language(s): …» di ognuna delle sette razze
  classi  il druido: «A druid also knows Druidic»
I nomi italiani dei linguaggi sono scritti qui a mano, non vengono dall'SRD.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / "sistemi" / "dnd35" / "dati" / "linguaggi.toml"
CACHE = Path.home() / ".cache" / "rumblingstone" / "srd" / "srd-v3.5-md-c7f30a0ce11a"
RAZZE = {"Humans": "human", "Dwarves": "dwarf", "Elves": "elf", "Gnomes": "gnome", "Half-Elves": "half-elf",
         "Half-Orcs": "half-orc", "Halflings": "halfling"}
#: come una scheda scrive ogni linguaggio (espressioni regolari)
NOMI = {"Common": "comune|common", "Dwarven": "nanico|dwarven", "Elven": "elfico|elven", "Gnome": "gnomesco|gnome",
        "Orc": "orchesco|orc", "Halfling": "halfling", "Druidic": "druidico|druidic"}


def razze(base: Path) -> "dict[str, list[str]]":
    t = (base / "basic-rules-and-legal" / "races.md").read_text(encoding="utf-8")
    out, razza = {}, None
    for riga in t.split("\n"):
        m = re.match(r"## (.+)$", riga)
        if m:
            razza = RAZZE.get(m.group(1).strip())
        m = re.match(r"- Automatic Languages?: ([^.]+)\.", riga)
        if m and razza:
            out[razza] = [x.strip() for x in re.split(r",| and ", m.group(1)) if x.strip()]
    return out


def druido(base: Path) -> str:
    t = (base / "basic-rules-and-legal" / "character-classes-i.md").read_text(encoding="utf-8")
    return re.search(r"A druid also knows (\w+), a secret language", t).group(1)


def genera(base: Path) -> str:
    r, d = razze(base), druido(base)
    assert set(r) == set(RAZZE.values()) and all(x in NOMI for v in r.values() for x in v) and d in NOMI, (r, d)
    q = lambda s: '"' + s + '"'  # noqa: E731
    return "\n".join([
        "# sistemi/dnd35/dati/linguaggi.toml — i linguaggi che razza e classe danno da soli (ADR-0126, lotto 7)",
        "#",
        "# GENERATO da plans/esperimenti/regole-senza-omissioni-2026-11-12/estrai_linguaggi.py",
        "# dall'SRD 3.5 (olimot/srd-v3.5-md@c7f30a0c, OGL). Non si corregge a mano.",
        "",
        "[linguaggi.razze]",
        "# SRD, razze: «Automatic Languages»",
        *[f"{q(n)} = [{', '.join(q(x) for x in v)}]" for n, v in sorted(r.items())],
        "",
        "[linguaggi.classi]",
        "# SRD, druido: «A druid also knows Druidic»",
        f"druid = [{q(d)}]",
        "",
        "[linguaggi.nomi]",
        "# come una scheda scrive ogni linguaggio (espressioni regolari; non vengono dall'SRD)",
        *[f"{q(n)} = {q(v)}" for n, v in NOMI.items()],
        "",
    ])


def main(argv: "list[str]") -> int:
    check = "--check" in argv
    resto = [a for a in argv if a != "--check"]
    testo = genera(Path(resto[0]) if resto else CACHE)
    if check:
        if not DEST.exists() or DEST.read_text(encoding="utf-8") != testo:
            print("✗ linguaggi.toml non è aggiornato: rilanciare estrai_linguaggi.py", file=sys.stderr)
            return 1
        print("✓ linguaggi.toml aggiornato")
        return 0
    DEST.write_text(testo, encoding="utf-8")
    print(f"scritto {DEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
