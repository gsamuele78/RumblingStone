#!/usr/bin/env python3
"""memoria_storica.py — la storia del lavoro che esce dalla memoria corta, cercabile.

Il DM, il 2026-11-12: *«evitare sempre la saturazione ed evitare di perdere
informazioni storiche che potrebbero essere importanti per una eventuale
regressione od una rivisitazione di soluzioni già adottate»*, e *«un
meccanismo che se ha necessità legga questo file per recuperare la parte di
memoria storica richiesta»* (ADR-0127).

La memoria del progetto (quella che ogni sessione d'agente legge all'avvio)
ha un limite di dimensione e tiene solo regole, stato aperto e puntatori.
Prima che una riga ne esca, i suoi fatti vanno in `plans/MEMORIA-STORICA.md`,
una voce `MS-NNNN` per riga, con data, PR, ADR e temi. Il file non ha limite
e non si riassume: si aggiunge in coda. Questo script lo **legge**:

    python3 scripts/memoria_storica.py --pr 242          # la storia di una PR
    python3 scripts/memoria_storica.py --adr 93          # di un ADR (0093)
    python3 scripts/memoria_storica.py --tema prosa      # di un tema
    python3 scripts/memoria_storica.py Skullcrusher      # parole nel testo
    python3 scripts/memoria_storica.py --da 2026-10-19 --a 2026-10-20
    python3 scripts/memoria_storica.py --elenco          # id, data e titolo
    python3 scripts/memoria_storica.py --json ...        # per un agente
    python3 scripts/memoria_storica.py --check           # il cancello della CI

I filtri si sommano (tutti devono valere). `--check` controlla la forma
(numeri consecutivi, date valide, campi obbligatori) e che il CHANGELOG dei
piani porti al file: una voce scritta male non si trova più con i filtri.

Solo stdlib, nessuna rete, sola lettura.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
FILE = RADICE / "plans" / "MEMORIA-STORICA.md"
CHANGELOG = RADICE / "plans" / "CHANGELOG.md"
LINK = "MEMORIA-STORICA.md"

TESTA = re.compile(r"^### (MS-(\d{4})) · (\S+) · (.+?)\s*$")
CAMPO = re.compile(r"^- \*\*([^*]+):\*\* ?(.*)$")
OBBLIGATORI = ("Data", "PR", "ADR", "Temi", "Origine", "Testo")


@dataclass
class Voce:
    id: str
    numero: int
    data: str
    titolo: str
    riga: int
    campi: "dict[str, str]" = field(default_factory=dict)
    testo_md: str = ""

    @property
    def pr(self) -> "set[int]":
        return {int(x) for x in re.findall(r"#(\d+)", self.campi.get("PR", ""))}

    @property
    def adr(self) -> "set[int]":
        return {int(x) for x in re.findall(r"ADR-(\d{4})", self.campi.get("ADR", ""))}

    @property
    def temi(self) -> "list[str]":
        return self.campi.get("Temi", "").split()


def leggi(testo: str) -> "list[Voce]":
    """Le voci del file, nell'ordine in cui stanno. Il testo fuori dalle voci è intestazione."""
    voci: "list[Voce]" = []
    corrente: "Voce | None" = None
    righe: "list[str]" = []
    for n, r in enumerate(testo.splitlines(), 1):
        m = TESTA.match(r)
        if m:
            if corrente:
                corrente.testo_md = "\n".join(righe).rstrip()
            corrente = Voce(m.group(1), int(m.group(2)), m.group(3), m.group(4), n)
            voci.append(corrente)
            righe = [r]
            continue
        if corrente is None:
            continue
        if r.startswith("## "):          # una sezione nuova chiude l'ultima voce
            corrente.testo_md = "\n".join(righe).rstrip()
            corrente = None
            continue
        righe.append(r)
        c = CAMPO.match(r)
        if c:
            corrente.campi[c.group(1).strip()] = c.group(2).strip()
    if corrente:
        corrente.testo_md = "\n".join(righe).rstrip()
    return voci


def _piano(s: str) -> str:
    """Minuscole e senza accenti: «città» si trova scrivendo «citta»."""
    s = unicodedata.normalize("NFKD", s.casefold())
    return "".join(c for c in s if not unicodedata.combining(c))


def filtra(voci: "list[Voce]", parole: "list[str]" = (), pr: "int | None" = None,
           adr: "int | None" = None, tema: "str | None" = None, da: "str | None" = None,
           a: "str | None" = None, ident: "str | None" = None) -> "list[Voce]":
    fuori = []
    for v in voci:
        corpo = _piano(v.testo_md)
        if ident and v.id != ident.upper():
            continue
        if pr is not None and pr not in v.pr and not re.search(rf"#{pr}(?!\d)", v.testo_md):
            continue
        if adr is not None and adr not in v.adr and f"ADR-{adr:04d}" not in v.testo_md:
            continue
        if tema and _piano(tema) not in {_piano(t) for t in v.temi}:
            continue
        if da and v.data < da:
            continue
        if a and v.data > a:
            continue
        if any(_piano(p) not in corpo for p in parole):
            continue
        fuori.append(v)
    return fuori


def controlla(testo: str, changelog: "str | None") -> "list[str]":
    """I difetti di forma. Lista vuota = il file si può cercare con i filtri."""
    errori = []
    voci = leggi(testo)
    if not voci:
        errori.append("nessuna voce MS-NNNN nel file")
    for atteso, v in enumerate(voci, 1):
        dove = f"{v.id} (riga {v.riga})"
        if v.numero != atteso:
            errori.append(f"{dove}: numero fuori sequenza, atteso MS-{atteso:04d}")
        try:
            date.fromisoformat(v.data)
        except ValueError:
            errori.append(f"{dove}: data «{v.data}» non è AAAA-MM-GG")
        for c in OBBLIGATORI:
            if c not in v.campi:
                errori.append(f"{dove}: manca il campo «{c}»")
        if v.campi.get("Data") and v.campi["Data"] != v.data:
            errori.append(f"{dove}: il campo Data ({v.campi['Data']}) non è la data del titolo")
        if not v.campi.get("Testo"):
            errori.append(f"{dove}: Testo vuoto")
        if v.campi.get("PR", "—") != "—" and not v.pr:
            errori.append(f"{dove}: PR senza numeri #NNN (o «—»)")
        if v.campi.get("ADR", "—") != "—" and not v.adr:
            errori.append(f"{dove}: ADR senza numeri ADR-NNNN (o «—»)")
    if changelog is not None and LINK not in changelog:
        errori.append(f"plans/CHANGELOG.md non porta a {LINK}: la storia va collegata al changelog")
    return errori


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("parole", nargs="*", help="Parole che devono comparire tutte nella voce "
                    "(senza badare a maiuscole e accenti).")
    ap.add_argument("--pr", type=int, help="Numero della PR, senza #.")
    ap.add_argument("--adr", type=int, help="Numero dell'ADR, anche senza zeri (93 = ADR-0093).")
    ap.add_argument("--tema", help="Un tema della voce (campo Temi), per esempio prosa, regole, arc07.")
    ap.add_argument("--da", help="Prima data, AAAA-MM-GG compresa.")
    ap.add_argument("--a", help="Ultima data, AAAA-MM-GG compresa.")
    ap.add_argument("--id", dest="ident", help="Una voce sola, per esempio MS-0042.")
    ap.add_argument("--elenco", action="store_true", help="Solo id, data e titolo delle voci trovate.")
    ap.add_argument("--json", action="store_true", help="Uscita per un agente: le voci coi loro campi.")
    ap.add_argument("--check", action="store_true", help="Il cancello: esce 1 se il file è "
                    "scritto male o il CHANGELOG dei piani non lo collega.")
    ap.add_argument("--file", type=Path, default=FILE, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)

    for d in (a.da, a.a):
        if d:
            try:
                date.fromisoformat(d)
            except ValueError:
                print(f"data non valida: {d} (serve AAAA-MM-GG)", file=sys.stderr)
                return 2
    if not a.file.is_file():
        print(f"manca {a.file}", file=sys.stderr)
        return 2
    testo = a.file.read_text(encoding="utf-8")

    if a.check:
        cl = CHANGELOG.read_text(encoding="utf-8") if a.file == FILE else None
        errori = controlla(testo, cl)
        for e in errori:
            print(f"✗ {e}")
        if errori:
            return 1
        print(f"✓ memoria storica: {len(leggi(testo))} voci in forma, collegata al changelog")
        return 0

    trovate = filtra(leggi(testo), a.parole, a.pr, a.adr, a.tema, a.da, a.a, a.ident)
    if a.json:
        print(json.dumps([{k: v for k, v in asdict(x).items() if k != "numero"} for x in trovate],
                         ensure_ascii=False, indent=1))
    elif a.elenco:
        for v in trovate:
            print(f"{v.id}  {v.data}  {v.titolo}")
    else:
        print("\n\n".join(v.testo_md for v in trovate) if trovate else "Nessuna voce trovata.")
        if trovate:
            print(f"\n— {len(trovate)} voci (plans/MEMORIA-STORICA.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
