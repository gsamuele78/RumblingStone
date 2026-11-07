#!/usr/bin/env python3
"""lessico_regole.py — i termini ufficiali di D&D 3.5 e PF1e, e chi li usa male.

Il problema
  Un agente che scrive «talento *Spezzaferro Nanico*» o «*Arma Specializzata*»
  quando il modulo accanto dice «Specializzazione in un'Arma» non ha modo di
  sapere, senza aprire l'SRD, se il termine esiste e come si chiama. La ricerca
  per nome di ``riscontro_srd.py regola`` non trovava nemmeno i talenti 3.5,
  perché nell'SRD il titolo è «Improved Trip <small>[General]</small>».

Cosa fa
  - ``indice``: genera dall'SRD 3.5 e dal PRD PF1e in cache (quelli di
    ``riscontro_srd.py``, ADR-0103) l'elenco dei termini ufficiali, con il tipo
    e il punto della fonte. L'elenco sta nella cache, non nel repo.
  - ``cerca NOME``: un termine, in inglese o in italiano, nelle due fonti.
  - ``controlla FILE...``: legge le righe dei talenti dei file e segnala ogni
    talento che non è né nella tabella italiana né nelle fonti, e non è
    marcato come fonte privata, non SRD, PF1e o regola della casa sulla
    stessa riga.
  La tabella italiano → SRD 3.5 → PF1e è ``scripts/lessico_it.yaml``.

Uso
  python3 scripts/lessico_regole.py indice
  python3 scripts/lessico_regole.py cerca "Sbilanciare migliorato"
  python3 scripts/lessico_regole.py controlla Bestiario/ PG/ [--json] [--check]

Exit 0 ok · 1 con --check, almeno un termine sconosciuto non marcato · 2 uso
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import riscontro_srd as R  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TABELLA = ROOT / "scripts" / "lessico_it.yaml"
TABELLA_PF1 = ROOT / "scripts" / "lessico_it_pf1.tsv"
# Un modulo è PF1e se lo dice il percorso o l'intestazione: lì vale la tabella
# diretta italiano PF1e → PRD, mai il passaggio per la 3.5 (DM, 2026-11-07).
MODULO_PF1 = re.compile(r"PF1e|Pathfinder", re.I)

# Il tipo di un titolo dell'SRD 3.5 si ricava dal file.
TIPI_SRD = (
    ("feats", "talento"), ("spells/spells-", "incantesimo"), ("epic-spells", "incantesimo"),
    ("skills", "abilità"), ("monsters/", "mostro"), ("epic-monsters", "mostro"),
    ("magic-items", "oggetto"), ("classes", "classe"), ("psionic-powers", "potere"),
)
TIPI_PF1 = {"feat": "talento", "spell": "incantesimo", "skill": "abilità",
            "item": "oggetto", "creature": "mostro", "class": "classe",
            "trap": "trappola", "affliction": "afflizione"}

TITOLO = re.compile(r"^#{2,4}\s+(?P<n>[^\n]+?)\s*$", re.M)
GRASSETTO = re.compile(r"^\*\*(?P<n>[A-Z][^*\n]{1,60}?):?\*\*:?", re.M)
PICCOLO = re.compile(r"<small>.*?</small>", re.S)


def norma(nome: str) -> str:
    """La chiave di confronto: minuscole, senza accenti, senza fregi."""
    s = PICCOLO.sub("", nome)
    s = re.sub(r"\[[^\]]*\]|\([^)]*\)", "", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[’'`*_]", "", s.lower())
    return re.sub(r"[^a-z0-9+]+", " ", s).strip()


def _tipo_srd(rel: str) -> str:
    for pezzo, tipo in TIPI_SRD:
        if pezzo in rel:
            return tipo
    return "regola"


def indice(cache: Path, rete: bool = True) -> dict[str, list[dict]]:
    voci: dict[str, list[dict]] = {}

    def metti(chiave, voce):
        if chiave and len(chiave) > 2:
            voci.setdefault(chiave, []).append(voce)

    base = R.assicura(R.SRD35, cache, rete=rete)
    for rel in sorted(R.SRD35.file):
        testo = (base / rel).read_text(encoding="utf-8")
        tipo = _tipo_srd(rel)
        for rx in (TITOLO, GRASSETTO):
            for m in rx.finditer(testo):
                nome = PICCOLO.sub("", m.group("n")).strip()
                metti(norma(nome), {"fonte": "srd35", "tipo": tipo if rx is TITOLO else "regola",
                                    "nome": nome, "dove": f"{rel}:{R.riga_di(testo, m.start())}"})
    base = R.assicura(R.PF1, cache, rete=rete)
    for db in sorted(R.PF1.file):
        con = sqlite3.connect(f"file:{base / db}?mode=ro", uri=True)
        try:
            righe = con.execute("select name, type, subtype from sections where name is not null").fetchall()
        except sqlite3.Error:
            righe = []
        finally:
            con.close()
        for nome, tipo, sub in righe:
            if tipo in TIPI_PF1 or sub == "condition":
                metti(norma(nome), {"fonte": "pf1", "tipo": TIPI_PF1.get(tipo, "condizione"),
                                    "nome": nome, "dove": db})
    return voci


def carica_indice(cache: Path, rete: bool = True) -> dict[str, list[dict]]:
    file = cache / "lessico-indice.json"
    if file.is_file():
        return json.loads(file.read_text(encoding="utf-8"))
    voci = indice(cache, rete=rete)
    file.write_text(json.dumps(voci, ensure_ascii=False), encoding="utf-8")
    return voci


def carica_tabella(percorso: Path = TABELLA) -> list[dict]:
    """La tabella italiana: YAML semplice, una voce per elemento (senza pyyaml)."""
    voci, voce = [], None
    for riga in percorso.read_text(encoding="utf-8").splitlines():
        if not riga.strip() or riga.lstrip().startswith("#"):
            continue
        m = re.match(r"^\s*(-\s+)?(\w+):\s*(.*?)\s*$", riga)
        if not m:
            continue
        if m.group(1):
            voce = {}
            voci.append(voce)
        valore = m.group(3).strip().strip('"')
        if voce is not None:
            voce[m.group(2)] = None if valore in ("", "null", "~") else valore
    return voci


def tabella_pf1(percorso: Path = TABELLA_PF1, tipo: str = "talento") -> dict[str, dict]:
    """Nome italiano PF1e normalizzato → voce PRD, per un tipo (talento, incantesimo, abilità, condizione)."""
    m = {}
    for riga in percorso.read_text(encoding="utf-8").splitlines():
        if riga.startswith("#") or "\t" not in riga or riga.startswith("italiano\t"):
            continue
        it, en, t = (riga.split("\t") + ["talento"])[:3]
        if t == tipo:
            m.setdefault(norma(it), {"it": it, "pf1": en, "srd35": None, "tipo": t})
    return m


def e_pf1(file: str, testo: str) -> bool:
    return bool(MODULO_PF1.search(file)) or bool(re.search(
        r"^(?:\*\*)?(?:Sistema|Regole|System)(?:\*\*)?\s*:?\s*(?:\*\*)?\s*(?:Pathfinder|PF1e)", testo[:3000], re.I | re.M))


def mappa_italiana(tabella: list[dict]) -> dict[str, dict]:
    m = {}
    for v in tabella:
        for nome in [v.get("it", "")] + [x.strip() for x in (v.get("varianti") or "").split("|") if x.strip()]:
            m[norma(nome)] = v
    return m


# ---------------------------------------------------------------- controllo

RIGA_TALENTI = re.compile(r"(?:\*\*)?\b(?:Talenti|Feats)\b(?:\*\*)?\s*:?\s*(?:\*\*)?\s*(?P<lista>.+)$", re.I)
MARCA_FUORI_SRD = re.compile(
    r"Private source|Non SRD|PF1e|Pathfinder|homebrew|della casa|\[CANONE|Celestial|"
    r"Complete |Races of|Draconomicon|Monster Manual|Manuale dei Mostri|Libro delle", re.I)


# Dove finisce l'elenco dei talenti: il campo seguente dello statblocco, una frase, una cella.
FINE_CAMPO = re.compile(
    r"\*\*[^*]{1,40}\*\*\s*:|\*\*(?:Abilit|Skills|Talenti (?:da|bonus)|Equipaggiamento|Tattiche|Lingu|"
    r"Qualit|SQ|Ambiente|Organizzazione|Tesoro|Allineamento|Avanzamento|Attacc|Difesa|Iniziativa)|"
    r"(?<=[a-z\)])\.\s|\s—\s|\||"
    r"(?:^|(?<=[\s·,;]))(?:Abilità|Skills|Linguaggi|Lingue|Languages|Qualità speciali|Equipaggiamento|SQ|TS)\b")


def termini_della_riga(lista: str) -> list[str]:
    lista = FINE_CAMPO.split(lista)[0]
    lista = re.sub(r"\([^)]*\)", "", lista)
    out = []
    for pezzo in re.split(r"[,;·]", lista):
        t = re.sub(r"\[[^\]]*\]|\*|`|\bB\b|\bx\d+\b|\+\d+", "", pezzo).strip(" .:")
        if 2 < len(t) < 45 and not re.search(r"\d", t) and t[0].isupper():
            out.append(t)
    return out


def controlla_testo(testo: str, idx: dict, ita: dict, file: str = "", pf1: dict | None = None) -> list[dict]:
    rilievi = []
    modulo_pf1 = pf1 is not None and e_pf1(file, testo)
    righe = testo.splitlines()
    for n, riga in enumerate(righe, 1):
        m = RIGA_TALENTI.search(riga)
        if not m:
            continue
        # L'elenco va a capo: si legge anche la riga dopo, se continua lo stesso campo.
        if n < len(righe) and righe[n].strip() and not re.match(r"\s*(?:\*\*|[|#>`-]|\d)", righe[n]) \
                and re.search(r"[·,\w]\s*$", riga) and not FINE_CAMPO.search(m.group("lista")):
            m = RIGA_TALENTI.search(riga.rstrip() + " " + righe[n].strip())
        for t in termini_della_riga(m.group("lista")):
            k = norma(t)
            if modulo_pf1:
                v = pf1.get(k)
                if v:
                    esito = "tabella"
                elif ita.get(k):
                    esito, v = "nome 3.5", ita.get(k)
                elif any(e["fonte"] == "pf1" for e in idx.get(k, [])):
                    esito = "fonte"
                elif MARCA_FUORI_SRD.search(riga.replace("PF1e", "").replace("Pathfinder", "")):
                    esito = "marcato"
                else:
                    esito = "sconosciuto"
                rilievi.append({"file": file, "riga": n, "termine": t, "esito": esito, "sistema": "pf1",
                                "srd35": None, "pf1": (v or {}).get("pf1")})
                continue
            v = ita.get(k)
            if v and k != norma(v.get("it", "")):
                esito = "variante"
            elif v:
                esito = "tabella"
            elif k in idx:
                esito = "fonte"
            elif MARCA_FUORI_SRD.search(riga):
                esito = "marcato"
            else:
                esito = "sconosciuto"
            rilievi.append({"file": file, "riga": n, "termine": t, "esito": esito,
                            "sistema": "3.5", "srd35": (v or {}).get("srd35"), "pf1": (v or {}).get("pf1")})
    return rilievi


def risolvi(termine: str, idx: dict, ita: dict) -> dict:
    """Il termine nelle due fonti: dalla tabella italiana se c'è, se no dall'indice."""
    v = ita.get(norma(termine))
    if v:
        return {"srd35": v.get("srd35"), "pf1": v.get("pf1"), "da": "tabella", "nota": v.get("nota")}
    out = {"srd35": None, "pf1": None, "da": "indice", "nota": None}
    for e in idx.get(norma(termine), []):
        out[e["fonte"]] = out[e["fonte"]] or e["nome"]
    return out


def verifica_tabella(tabella: list[dict], idx: dict) -> list[str]:
    """Ogni nome inglese della tabella deve stare nella sua fonte."""
    errori = []
    for v in tabella:
        for f in ("srd35", "pf1"):
            n = v.get(f)
            if n and not any(e["fonte"] == f for e in idx.get(norma(n), [])):
                errori.append(f"{v.get('it')}: {f} «{n}» non è nella fonte")
    return errori


def misura_casi(casi: list[dict], idx: dict, ita: dict) -> list[dict]:
    out = []
    for c in casi:
        r = risolvi(c["termine"], idx, ita)
        giusto = all(norma(r[f] or "") == norma(c.get(f) or "") for f in ("srd35", "pf1"))
        out.append({**c, "trovato_srd35": r["srd35"], "trovato_pf1": r["pf1"], "giusto": giusto})
    return out


def file_da(percorsi: list[str], volumi: bool = False) -> list[Path]:
    out = []
    for p in map(Path, percorsi):
        p = p if p.is_absolute() else ROOT / p
        out += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    return [f for f in out if f.is_file() and (volumi or ".hb.md" not in f.name)]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", help="cartella della cache dell'SRD (vedi riscontro_srd.py)")
    ap.add_argument("--offline", action="store_true", help="non scaricare: solo cache")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("indice")
    c = sub.add_parser("cerca")
    c.add_argument("nome")
    sub.add_parser("verifica-tabella")
    m = sub.add_parser("casi")
    m.add_argument("file")
    m.add_argument("--check", action="store_true")
    k = sub.add_parser("controlla")
    k.add_argument("percorsi", nargs="+")
    k.add_argument("--json", action="store_true")
    k.add_argument("--check", action="store_true")
    k.add_argument("--volumi", action="store_true", help="legge anche i volumi .hb.md generati (conto prima e dopo dei booklet)")
    a = ap.parse_args(argv)
    cache = R.cartella_cache(a.cache)

    if a.cmd == "indice":
        (cache / "lessico-indice.json").unlink(missing_ok=True)
        idx = carica_indice(cache, rete=not a.offline)
        print(f"lessico: {len(idx)} termini in {cache / 'lessico-indice.json'}")
        return 0
    idx = carica_indice(cache, rete=not a.offline)
    ita = mappa_italiana(carica_tabella())
    if a.cmd == "verifica-tabella":
        errori = verifica_tabella(carica_tabella(), idx)
        print("\n".join(errori) or f"lessico: tabella ok, {len(carica_tabella())} voci tutte nelle fonti")
        return 1 if errori else 0
    if a.cmd == "casi":
        casi = json.loads(Path(a.file).read_text(encoding="utf-8"))["casi"]
        esiti = misura_casi(casi, idx, ita)
        for e in esiti:
            if not e["giusto"]:
                print(f"SBAGLIATO «{e['termine']}»: atteso 3.5 {e.get('srd35')} / PF1e {e.get('pf1')}, "
                      f"trovato {e['trovato_srd35']} / {e['trovato_pf1']}")
        giusti = sum(e["giusto"] for e in esiti)
        print(f"lessico: {giusti} casi giusti su {len(esiti)}")
        return 1 if a.check and giusti < len(esiti) else 0
    if a.cmd == "cerca":
        k_ = norma(a.nome)
        v = ita.get(k_)
        chiavi = [k_] + ([norma(x) for x in (v.get("srd35"), v.get("pf1")) if x] if v else [])
        trovate = [e for ch in dict.fromkeys(chiavi) for e in idx.get(ch, [])]
        if v:
            print(f"tabella: {v.get('it')} → 3.5 {v.get('srd35') or '—'} → PF1e {v.get('pf1') or '—'}"
                  + (f" ({v['nota']})" if v.get("nota") else ""))
        for e in trovate:
            print(f"{e['fonte']:6} {e['tipo']:12} {e['nome']}  [{e['dove']}]")
        return 0 if trovate or v else 1
    pf1 = tabella_pf1()
    rilievi = [r for f in file_da(a.percorsi, a.volumi)
               for r in controlla_testo(f.read_text(encoding="utf-8", errors="ignore"), idx, ita,
                                        str(f.relative_to(ROOT)) if f.is_relative_to(ROOT) else str(f), pf1)]
    ignoti = [r for r in rilievi if r["esito"] in ("sconosciuto", "variante", "nome 3.5")]
    if a.json:
        print(json.dumps(rilievi, ensure_ascii=False, indent=1))
    else:
        for r in ignoti:
            cosa = {"variante": "variante non ufficiale", "nome 3.5": "nome 3.5 in un modulo PF1e"}.get(
                r["esito"], "talento sconosciuto")
            print(f"{r['file']}:{r['riga']}: {cosa} «{r['termine']}»")
        conti = {e: sum(1 for r in rilievi if r["esito"] == e) for e in ("tabella", "fonte", "marcato", "variante", "nome 3.5", "sconosciuto")}
        print(f"lessico: {len(rilievi)} talenti letti · " + " · ".join(f"{k} {v}" for k, v in conti.items()))
    return 1 if a.check and ignoti else 0


if __name__ == "__main__":
    sys.exit(main())
