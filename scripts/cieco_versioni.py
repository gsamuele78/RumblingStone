#!/usr/bin/env python3
"""cieco_versioni.py — il confronto cieco fra due versioni degli stessi box.

Le misure deterministiche dicono se un testo ha **meno difetti**; nessuna dice
se è **migliore** (ADR-0093). I giudici automatici non concordano con gli
esperti (κ vicino a zero in TTCW, 2024, e in «Measuring AI Slop», 2025), e
ottimizzare un numero peggiora il testo. Resta il lettore: il DM legge ad alta
voce due versioni dello stesso box, senza sapere quale è la nuova, e sceglie.

Tre passi, in quest'ordine, e il primo si fa **prima** di riscrivere:

| Comando | Cosa fa |
|---|---|
| `campione` | sceglie i box da confrontare, con un seme dichiarato, e ne congela il testo |
| `coppie` | trova in una versione successiva il box che corrisponde a ciascuno, mette le due versioni in ordine casuale e scrive la scheda per il DM e la chiave a parte |
| `esito` | legge le scelte del DM, scioglie la chiave e dice se la nuova versione vince |

Il criterio di `esito` è quello scritto prima del rifacimento di ARC-07
(`PROSA-DETERMINISTICA-2026-10-18` §6): la nuova versione deve essere
preferita in **almeno 14 coppie su 20**. Con 20 coppie, 14 dà un intervallo di
Wilson al 95% che parte sopra 0,48: basta per dire «meglio», non «molto
meglio». Il pari conta come non vinto.

⚠️ **L'appaiamento è il punto debole.** Dopo una riscrittura un box può
cambiare posto, nome di sezione o essere spezzato in due. `coppie` sceglie,
nello stesso file, il box più simile (difflib, senza `autojunk`: con il
default due box quasi uguali di 300 caratteri davano 0,08), e preferisce quello sotto la
stessa intestazione; dice la somiglianza di ogni coppia, e segna le coppie
dubbie (sotto 0,2) e quelle identiche, che non si votano.

Uso:

    python3 scripts/cieco_versioni.py campione --ref main --seme 20261018 \\
        --per-file 4 --uscita CAMPIONE.json FILE...
    python3 scripts/cieco_versioni.py coppie --campione CAMPIONE.json \\
        --dopo REF --seme 7 --scheda SCHEDA.md --chiave CHIAVE.json
    python3 scripts/cieco_versioni.py esito --chiave CHIAVE.json --voti VOTI.txt
"""
from __future__ import annotations

import argparse
import difflib
import json
import math
import random
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import misura_craft as mc  # noqa: E402

#: Un box sotto queste parole è una didascalia o una battuta sola: non si vota.
PAROLE_MINIME = 25
#: Sotto questa somiglianza la coppia è dubbia: forse non è lo stesso box.
SOMIGLIANZA_DUBBIA = 0.2
#: Il criterio scritto prima del rifacimento di ARC-07.
VITTORIE_RICHIESTE = 14
COPPIE_ATTESE = 20

_TITOLO = re.compile(r"^#{1,6}\s+(.*\S)")

#: Un box con un numero di regola dentro è una nota per il DM scritta in
#: corsivo citato («Calibrazione rapida: Blast di Artemis ~28/colpo»), non
#: prosa da leggere: `box_read_aloud` la prende, il campione no.
_NOTA_DI_REGOLA = re.compile(r"\b(?:pf|RD|CD|TS|GS|PE|DV|CA)\s*\d|\d+\s*pf\b|~\d")


def testo_a(ref: str, percorso: str) -> str:
    """Il file com'era a `ref`. Con ref vuoto, il file sul disco."""
    if not ref:
        return (ROOT / percorso).read_text(encoding="utf-8")
    return subprocess.run(["git", "show", f"{ref}:{percorso}"], cwd=ROOT,
                          check=True, capture_output=True, text=True).stdout


def box_con_titolo(testo: str) -> "list[dict]":
    """I box di `box_read_aloud`, ognuno con l'intestazione sotto cui sta."""
    righe = testo.splitlines()
    titoli, corrente = {}, ""
    for i, r in enumerate(righe):
        m = _TITOLO.match(r)
        if m:
            corrente = m.group(1)
        titoli[i] = corrente
    uscita, cursore = [], 0
    for b in mc.box_read_aloud(testo):
        # La riga d'inizio del box: la prima occorrenza dopo il box precedente.
        try:
            inizio = righe.index(b[0], cursore)
        except ValueError:
            inizio = cursore
        cursore = inizio + len(b)
        corpo = mc.corpo_del_box(b)
        uscita.append({"titolo": titoli.get(inizio, ""), "testo": corpo,
                       "parole": len(corpo.split())})
    return uscita


def campione(ref: str, files: "list[str]", per_file: int, seme: int) -> dict:
    rng = random.Random(seme)
    voci = []
    for f in files:
        candidati = [(i, b) for i, b in enumerate(box_con_titolo(testo_a(ref, f)))
                     if b["parole"] >= PAROLE_MINIME
                     and not _NOTA_DI_REGOLA.search(b["testo"])]
        scelti = sorted(rng.sample(candidati, min(per_file, len(candidati))),
                        key=lambda x: x[0])
        voci += [{"file": f, "indice": i, **b} for i, b in scelti]
    return {"ref": ref, "seme": seme, "per_file": per_file,
            "parole_minime": PAROLE_MINIME, "voci": voci}


def appaia(voce: dict, dopo: "list[dict]") -> "tuple[int, float]":
    """L'indice del box più simile nella versione dopo, e la somiglianza."""
    if not dopo:
        return -1, 0.0
    def punteggio(b):
        r = difflib.SequenceMatcher(None, voce["testo"], b["testo"],
                                    autojunk=False).ratio()
        return r + (0.1 if b["titolo"] == voce["titolo"] else 0.0), r
    migliore = max(range(len(dopo)), key=lambda i: punteggio(dopo[i])[0])
    return migliore, punteggio(dopo[migliore])[1]


def coppie(camp: dict, ref_dopo: str, seme: int) -> "tuple[str, dict]":
    rng = random.Random(seme)
    cache: dict = {}
    scheda = ["# Confronto cieco fra due versioni", "",
              "Leggi ad alta voce **A** e poi **B**. Scrivi nel file dei voti una "
              "riga per coppia, `N A`, `N B` o `N =`. Non aprire la chiave.", ""]
    chiave = {"campione_ref": camp["ref"], "dopo": ref_dopo, "seme": seme, "coppie": []}
    n = 0
    for voce in camp["voci"]:
        if voce["file"] not in cache:
            try:
                cache[voce["file"]] = box_con_titolo(testo_a(ref_dopo, voce["file"]))
            except subprocess.CalledProcessError:
                cache[voce["file"]] = []
        dopo = cache[voce["file"]]
        i, somiglianza = appaia(voce, dopo)
        nuovo = dopo[i]["testo"] if i >= 0 else ""
        stato = ("identica" if nuovo == voce["testo"] else
                 "dubbia" if somiglianza < SOMIGLIANZA_DUBBIA else "valida")
        n += 1
        nuova_e_a = rng.random() < 0.5
        chiave["coppie"].append({"n": n, "file": voce["file"], "titolo": voce["titolo"],
                                 "nuova": "A" if nuova_e_a else "B",
                                 "somiglianza": round(somiglianza, 3), "stato": stato})
        if stato == "identica":
            continue
        a, b = (nuovo, voce["testo"]) if nuova_e_a else (voce["testo"], nuovo)
        scheda += [f"## Coppia {n}", "", f"*{Path(voce['file']).name} · {voce['titolo']}*",
                   "", "**A**", "", f"> {a}", "", "**B**", "", f"> {b}", ""]
    return "\n".join(scheda), chiave


def wilson(k: int, n: int, z: float = 1.96) -> "tuple[float, float]":
    if n == 0:
        return 0.0, 0.0
    p = k / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    margine = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centro - margine), min(1.0, centro + margine)


_VOTO = re.compile(r"^\s*(\d+)\s*[:.)-]?\s*([AaBb=])\s*$")


def esito(chiave: dict, voti_testo: str) -> dict:
    voti = {}
    for r in voti_testo.splitlines():
        m = _VOTO.match(r)
        if m:
            voti[int(m.group(1))] = m.group(2).upper()
    nuova = vecchia = pari = 0
    for c in chiave["coppie"]:
        if c["stato"] == "identica" or c["n"] not in voti:
            continue
        v = voti[c["n"]]
        if v == "=":
            pari += 1
        elif v == c["nuova"]:
            nuova += 1
        else:
            vecchia += 1
    n = nuova + vecchia + pari
    basso, alto = wilson(nuova, n)
    if n < COPPIE_ATTESE:
        verdetto = f"incompleto: {n} coppie votate su {COPPIE_ATTESE}"
    elif nuova >= VITTORIE_RICHIESTE:
        verdetto = "meglio: la nuova versione vince in modo dimostrabile"
    else:
        verdetto = "non dimostrato: la nuova versione non vince abbastanza coppie"
    return {"nuova": nuova, "vecchia": vecchia, "pari": pari, "votate": n,
            "wilson_95": [round(basso, 3), round(alto, 3)], "verdetto": verdetto}


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("campione", help="sceglie e congela i box, prima di riscrivere")
    c.add_argument("--ref", default="", help="la versione di partenza (vuoto: il disco)")
    c.add_argument("--seme", type=int, required=True)
    c.add_argument("--per-file", type=int, default=4)
    c.add_argument("--uscita", required=True)
    c.add_argument("files", nargs="+")
    p = sub.add_parser("coppie", help="scheda per il DM e chiave a parte")
    p.add_argument("--campione", required=True)
    p.add_argument("--dopo", default="", help="la versione nuova (vuoto: il disco)")
    p.add_argument("--seme", type=int, required=True)
    p.add_argument("--scheda", required=True)
    p.add_argument("--chiave", required=True)
    e = sub.add_parser("esito", help="scioglie la chiave e applica il criterio")
    e.add_argument("--chiave", required=True)
    e.add_argument("--voti", required=True)
    a = ap.parse_args(argv)

    if a.cmd == "campione":
        dati = campione(a.ref, a.files, a.per_file, a.seme)
        Path(a.uscita).write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n",
                                  encoding="utf-8")
        print(f"{len(dati['voci'])} box congelati in {a.uscita} (seme {a.seme})")
    elif a.cmd == "coppie":
        camp = json.loads(Path(a.campione).read_text(encoding="utf-8"))
        scheda, chiave = coppie(camp, a.dopo, a.seme)
        Path(a.scheda).write_text(scheda + "\n", encoding="utf-8")
        Path(a.chiave).write_text(json.dumps(chiave, ensure_ascii=False, indent=1) + "\n",
                                  encoding="utf-8")
        stati = [c["stato"] for c in chiave["coppie"]]
        print(f"{stati.count('valida')} coppie valide, {stati.count('dubbia')} dubbie, "
              f"{stati.count('identica')} identiche (non si votano)")
    else:
        chiave = json.loads(Path(a.chiave).read_text(encoding="utf-8"))
        r = esito(chiave, Path(a.voti).read_text(encoding="utf-8"))
        print(f"nuova {r['nuova']} · vecchia {r['vecchia']} · pari {r['pari']} "
              f"su {r['votate']} · Wilson 95% {r['wilson_95']}")
        print(r["verdetto"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
