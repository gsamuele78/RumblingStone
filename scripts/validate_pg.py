#!/usr/bin/env python3
"""validate_pg.py — gate sulle schede PG: i costi permanenti non spariscono più.

Il difetto che questo gate esiste per impedire
  Il 2026-08-09 il DM ha chiesto di verificare un **−2 DES** che ricordava e che
  nessun documento gli riconosceva più. Era vero, ed era scritto nel modulo
  giocato — `PortaleForgia-P1`, fra le «Limitazioni» della Corona indossata, col
  ricalcolo per esteso *DES 10 → 8*. Non compariva in **nessuna** delle tre
  generazioni di schede successive: tutte elencavano **solo i poteri**.
  I consolidamenti tenevano i bonus e perdevano i costi.

  Nessun gate poteva accorgersene, perché Thorik non aveva una scheda: non
  esisteva un posto dove quel dato *sarebbe dovuto stare*, quindi la sua assenza
  non era osservabile. Prima si crea il posto (`PG/schede/*.yaml`), poi si può
  sorvegliarlo.

Le tre verifiche
  1. **Schema** — ogni modificatore permanente porta una `fonte`, e la fonte
     **esiste su disco**. Un modificatore senza fonte apribile è indistinguibile
     da un'invenzione.
  2. **Aritmetica** — `base` + somma dei delta = `attuale`, caratteristica per
     caratteristica. È il controllo che rende impossibile scrivere «DES 6» senza
     dire da dove vengono i quattro punti persi.
  3. **Deriva** (il cuore) — scansione di tutti i `.md` alla ricerca di
     affermazioni del tipo «*<PG> … −2 DES … permanenti*». Ogni tripla trovata
     dev'essere **o** presente sulla scheda di quel PG, **o** dismessa
     esplicitamente in `scripts/data/pg_modificatori_ignorati.yaml` **con una
     ragione scritta**. Non c'è una terza via: è lo stesso schema del ratchet dei
     `[INFERRED]` — non si vieta, si obbliga a dichiarare.
  4. **Fonti primarie** — il controllo 3 confronta *tipi* di modificatore
     (`−2 DES`), e da solo non distingue **due** modificatori uguali: Thorik ne
     ha due, −2 DES dalla Corona indossata e −2 DES dal rito, e togliendone uno
     il tipo resterebbe coperto dall'altro. Quindi i file elencati come
     `fonti_primarie` — quelli in cui un costo **nasce**, non quelli che lo
     ricitano — devono avere **ogni** loro affermazione registrata sulla scheda
     **con quel file come `fonte`**. È il controllo che avrebbe visto sparire il
     −2 DES della Corona il giorno stesso.

Uso
  python3 scripts/validate_pg.py [--json] [--verbose]

Exit  0 = tutto coerente · 1 = incoerenze · 2 = errore d'uso
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEDE = ROOT / "PG" / "schede"
SCHEMA = ROOT / "scripts" / "schemas" / "pg_scheda.schema.json"
IGNORATI = ROOT / "scripts" / "data" / "pg_modificatori_ignorati.yaml"

SKIP_DIRS = {".git", "build", ".claude", ".cursor", ".gemini", ".chatgpt",
             ".windsurf", ".kilo", ".agents", ".github", "Old", "converters"}

SIGLE = {"FOR": "for", "DES": "des", "COS": "cos", "INT": "int", "SAG": "sag", "CAR": "car"}
NOMI_LUNGHI = {"FORZA": "FOR", "DESTREZZA": "DES", "COSTITUZIONE": "COS",
               "INTELLIGENZA": "INT", "SAGGEZZA": "SAG", "CARISMA": "CAR"}

CARATT = r"(?:FOR|DES|COS|INT|SAG|CAR|Forza|Destrezza|Costituzione|Intelligenza|Saggezza|Carisma)"
DELTA = re.compile(rf"([+−-]\s?\d+)\s*(?:punti\s+)?({CARATT})\b", re.I)
PERMANENTE = re.compile(r"permanent", re.I)


def carica_yaml(p: Path):
    import yaml
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def normalizza(sigla: str) -> str:
    s = sigla.upper()
    return NOMI_LUNGHI.get(s, s[:3])


def schede() -> dict[str, dict]:
    return {p.stem: carica_yaml(p) for p in sorted(SCHEDE.glob("*.yaml"))}


def valida_schema(dati: dict, nome: str) -> list[str]:
    """Validazione mirata: le regole che contano, senza dipendere da jsonschema."""
    problemi: list[str] = []
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for chiave in schema["required"]:
        if chiave not in dati:
            problemi.append(f"{nome}: manca la chiave obbligatoria `{chiave}`")
    for i, mod in enumerate(dati.get("modificatori_permanenti") or []):
        for chiave in ("caratteristica", "delta", "causa", "fonte"):
            if not mod.get(chiave):
                problemi.append(f"{nome}: modificatore #{i + 1} senza `{chiave}`")
        fonte = mod.get("fonte")
        if fonte and not (ROOT / fonte).exists():
            problemi.append(
                f"{nome}: modificatore «{mod.get('causa', '')[:40]}…» cita una fonte "
                f"che non esiste: `{fonte}` — una fonte che non si può aprire non è una fonte")
    for i, v in enumerate(dati.get("vincoli") or []):
        fonte = v.get("fonte")
        if fonte and not (ROOT / fonte).exists():
            problemi.append(f"{nome}: vincolo #{i + 1} cita una fonte inesistente: `{fonte}`")
    return problemi


def valida_aritmetica(dati: dict, nome: str) -> list[str]:
    problemi: list[str] = []
    somme: dict[str, int] = {}
    for mod in dati.get("modificatori_permanenti") or []:
        c = normalizza(str(mod.get("caratteristica", "")))
        somme[c] = somme.get(c, 0) + int(mod.get("delta", 0))
    for sigla, chiave in SIGLE.items():
        car = (dati.get("caratteristiche") or {}).get(chiave) or {}
        base, attuale = car.get("base"), car.get("attuale")
        atteso = somme.get(sigla, 0)
        if base is None and attuale is None:
            # Delta noto, valori no: legittimo e frequente: il modulo scrive
            # «+2 COS permanenti» senza dire da quale COS si parte. Inventare la
            # base per far tornare il conto sarebbe il male peggiore — resta
            # [INFERRED] e lo si conta, non lo si segnala come errore.
            continue
        if base is None or attuale is None:
            manca = "base" if base is None else "attuale"
            problemi.append(
                f"{nome}: {sigla} dichiara metà del conto ({manca} è null) — o si dichiarano "
                "entrambi i valori o nessuno: una metà sola non è verificabile e sembra un dato")
            continue
        if base + atteso != attuale:
            problemi.append(
                f"{nome}: {sigla} non torna — base {base} {atteso:+d} = {base + atteso}, "
                f"ma la scheda dichiara attuale {attuale}")
    return problemi


def md_files():
    for p in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def scansiona_deriva(pgs: list[str]) -> dict[tuple, list[str]]:
    """Triple (PG, delta, caratteristica) affermate come permanenti nei documenti."""
    trovate: dict[tuple, list[str]] = {}
    minuscoli = {p.lower(): p for p in pgs}
    for p in md_files():
        for i, riga in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if not PERMANENTE.search(riga):
                continue
            citati = [nome for low, nome in minuscoli.items() if low in riga.lower()]
            if len(citati) != 1:
                continue  # riga ambigua: due PG o nessuno — non si indovina
            for m in DELTA.finditer(riga):
                segno = m.group(1).replace(" ", "").replace("−", "-")
                chiave = (citati[0], int(segno), normalizza(m.group(2)))
                trovate.setdefault(chiave, []).append(f"{p.relative_to(ROOT)}:{i}")
    return trovate


def dismissioni() -> dict[tuple, str]:
    if not IGNORATI.exists():
        return {}
    dati = carica_yaml(IGNORATI) or {}
    out: dict[tuple, str] = {}
    for v in dati.get("ignorati") or []:
        out[(v["pg"], int(v["delta"]), normalizza(v["caratteristica"]))] = v.get("ragione", "")
    return out


def fonti_primarie() -> list[dict]:
    """I file in cui un costo NASCE, con che cosa ciascuno stabilisce."""
    if not IGNORATI.exists():
        return []
    return list((carica_yaml(IGNORATI) or {}).get("fonti_primarie") or [])


def scansiona_file(path: Path, pgs: list[str]) -> set[tuple]:
    """Triple (PG, delta, caratteristica) affermate come permanenti in UN file."""
    minuscoli = {p.lower(): p for p in pgs}
    trovate: set[tuple] = set()
    for riga in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not PERMANENTE.search(riga):
            continue
        citati = [nome for low, nome in minuscoli.items() if low in riga.lower()]
        if len(citati) != 1:
            continue
        for m in DELTA.finditer(riga):
            segno = m.group(1).replace(" ", "").replace("−", "-")
            trovate.add((citati[0], int(segno), normalizza(m.group(2))))
    return trovate


def verifica_fonti_primarie(tutte: dict[str, dict], pgs: list[str]) -> list[str]:
    """Due controlli che il confronto per *tipo* non può fare.

    **(a) Nessuna fonte primaria orfana.** Un file dichiarato primario è un file
    in cui un costo *nasce*: se nessun modificatore di nessuna scheda lo cita più
    come `fonte`, quel costo è stato cancellato da una scheda e non se ne sarebbe
    accorto nessuno. È letteralmente ciò che è successo alla Corona — e il
    confronto per tipo non lo vede, perché Thorik ha **due** −2 DES e l'altro
    copriva il buco.

    **(b) Citazione letterale.** Ogni modificatore può portare `cita:`, una
    stringa che deve comparire nel file citato. Serve al caso opposto: la fonte
    resta, ma smette di dire quello che la scheda le fa dire. Senza questo, una
    riscrittura del modulo lascerebbe in piedi una scheda che cita il vuoto.

    Perché non si scansiona il testo della fonte primaria in cerca dei delta: nel
    modulo il costo è scritto come `- **-2 Destrezza** (peso e restrizione
    movimenti testa)`, su una riga che **non nomina Thorik e non dice
    «permanente»**. Una scansione a riga non lo troverebbe — è la ragione per cui
    era invisibile in partenza, e imitarla qui riprodurrebbe il difetto.
    """
    problemi: list[str] = []
    citate: set[str] = set()
    for dati in tutte.values():
        nome = dati.get("pg", "?")
        for m in dati.get("modificatori_permanenti") or []:
            rel = str(m.get("fonte", ""))
            citate.add(rel)
            frammento = m.get("cita")
            f = ROOT / rel
            if frammento and f.exists():
                if frammento not in f.read_text(encoding="utf-8", errors="ignore"):
                    problemi.append(
                        f"{nome}: il modificatore «{str(m.get('causa'))[:40]}…» cita "
                        f"`{rel}`, ma in quel file la frase «{frammento}» non c'è più. "
                        "O la fonte è cambiata, o la scheda le fa dire una cosa che non dice")
    registrati: set[tuple] = set()
    for dati in tutte.values():
        for m in dati.get("modificatori_permanenti") or []:
            registrati.add((dati.get("pg"), normalizza(str(m["caratteristica"])),
                            int(m["delta"]), str(m.get("fonte", ""))))
    for voce in fonti_primarie():
        rel = voce["file"]
        if not (ROOT / rel).exists():
            problemi.append(f"fonte primaria inesistente: `{rel}`")
            continue
        for att in voce.get("attesta") or []:
            chiave = (att["pg"], normalizza(str(att["caratteristica"])), int(att["delta"]), rel)
            if chiave not in registrati:
                problemi.append(
                    f"{att['pg']}: la fonte primaria `{rel}` stabilisce "
                    f"**{int(att['delta']):+d} {normalizza(str(att['caratteristica']))} "
                    "permanenti**, ma sulla sua scheda non c'è nessun modificatore con quel "
                    "valore E quel file come `fonte`. Le due colonne non quadrano: o il costo "
                    "è stato cancellato dalla scheda, o il modulo non lo stabilisce più")
    return problemi


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--json", action="store_true", help="Report in JSON (opt-in).")
    ap.add_argument("--verbose", action="store_true", help="Elenca anche ciò che è coerente.")
    args = ap.parse_args(argv)

    if not SCHEDE.is_dir():
        print(f"ERRORE: manca {SCHEDE.relative_to(ROOT)}", file=sys.stderr)
        return 2
    try:
        tutte = schede()
    except Exception as e:  # YAML rotto: è un errore d'uso, non un'incoerenza
        print(f"ERRORE: scheda illeggibile — {e}", file=sys.stderr)
        return 2
    if not tutte:
        print(f"ERRORE: nessuna scheda in {SCHEDE.relative_to(ROOT)}", file=sys.stderr)
        return 2

    problemi: list[str] = []
    for nome, dati in tutte.items():
        problemi += valida_schema(dati, nome)
        problemi += valida_aritmetica(dati, nome)

    pgs = [d.get("pg", n) for n, d in tutte.items()]
    per_pg: dict[str, set] = {}
    for nome, dati in tutte.items():
        pg = dati.get("pg", nome)
        per_pg[pg] = {(normalizza(str(m["caratteristica"])), int(m["delta"]))
                      for m in (dati.get("modificatori_permanenti") or [])}

    problemi += verifica_fonti_primarie(tutte, pgs)

    ignorati = dismissioni()
    derive: list[str] = []
    for (pg, delta, car), dove in sorted(scansiona_deriva(pgs).items()):
        if (car, delta) in per_pg.get(pg, set()):
            continue
        if (pg, delta, car) in ignorati:
            continue
        derive.append(
            f"{pg}: i documenti affermano **{delta:+d} {car} permanenti** ma la sua scheda non lo "
            f"registra, e non è dismesso in {IGNORATI.relative_to(ROOT)}.\n"
            f"    Prime occorrenze: {', '.join(dove[:3])}")

    inferred = sum(1 for d in tutte.values()
                   for c in (d.get("caratteristiche") or {}).values()
                   if c.get("attuale") is None)

    if args.json:
        print(json.dumps({"schede": len(tutte), "problemi": problemi, "derive": derive,
                          "caselle_inferred": inferred}, ensure_ascii=False, indent=2))
        return 1 if (problemi or derive) else 0

    if problemi or derive:
        for x in problemi:
            print(f"  ✗ {x}")
        for x in derive:
            print(f"  ⚠ {x}")
        print(f"\n✗ validate_pg: {len(problemi)} incoerenze, {len(derive)} possibili derive.")
        print("  Una deriva si chiude in due modi: la si registra sulla scheda del PG, oppure")
        print(f"  la si dismette in {IGNORATI.relative_to(ROOT)} **con una ragione scritta**.")
        return 1

    print(f"✓ validate_pg: {len(tutte)} schede coerenti, nessuna deriva "
          f"({inferred} caselle ancora [INFERRED])")
    if args.verbose:
        for nome, dati in tutte.items():
            mods = dati.get("modificatori_permanenti") or []
            print(f"  · {dati.get('pg', nome)}: {len(mods)} modificatori permanenti")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
