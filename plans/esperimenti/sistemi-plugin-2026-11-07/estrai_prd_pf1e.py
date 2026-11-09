#!/usr/bin/env python3
"""estrai_prd_pf1e.py — le tabelle numeriche PF1e dei plugin, dal PRD in cache.

Scrive i dati del plugin `sistemi/pf1e/dati/` leggendo il PRD di Pathfinder 1e
(`devonjones/PSRD-Data@76ea4784`, scaricato con `riscontro_srd.py scarica`).
Niente numeri a mano: ogni valore viene da una tabella del PRD, citata per
libro, id della sezione e nome. Rilanciato sulla stessa cache, riscrive gli
stessi byte (con `--check` esce 1 se i file sul disco sono diversi).

    python3 plans/esperimenti/sistemi-plugin-2026-11-07/estrai_prd_pf1e.py           # scrive
    python3 plans/esperimenti/sistemi-plugin-2026-11-07/estrai_prd_pf1e.py --check   # confronta

Tabelle (Open Game Content, OGL 1.0a; il testo della licenza è in OGL.txt):
    book-cr 2743  Character Advancement and Level-Dependent Bonuses  → pe.toml
    book-cr 3655  Experience Point Awards                            → incontri.toml
    book-cr 3653  Encounter Design                                   → incontri.toml
    book-cr 3661  Treasure Values per Encounter                      → tesoro.toml
    book-b1 116   Creature Statistics by Type                        → creature.toml
    book-b1 160   Size Bonuses and Penalties                         → creature.toml
    book-cr/apg/acg/uc/um  le tabelle delle classi (BAB e TS)       → conformita_prd.toml
    book-b1 361-385, 405-423  sensi dei tipi e dei sottotipi        → conformita_prd.toml
    book-b1…b4  i sensi degli umanoidi del Bestiario                → conformita_prd.toml
    book-b1 1112  Corrupt Water (drago nero)                        → conformita_prd.toml
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sqlite3
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / "sistemi" / "pf1e" / "dati"
COMMIT = "76ea47846041"
PRD = f"PSRD-Data-{COMMIT}"


def cache() -> Path:
    for c in (os.environ.get("RUMBLINGSTONE_SRD_CACHE"),
              os.path.join(os.environ.get("XDG_CACHE_HOME", ""), "rumblingstone", "srd")
              if os.environ.get("XDG_CACHE_HOME") else None,
              str(Path.home() / ".cache" / "rumblingstone" / "srd")):
        if c and (Path(c) / PRD).is_dir():
            return Path(c) / PRD
    sys.exit("manca il PRD in cache: python3 scripts/riscontro_srd.py scarica")


class _Righe(HTMLParser):
    def __init__(self):
        super().__init__()
        self.righe, self._riga, self._cella = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._riga = []
        elif tag in ("td", "th") and self._riga is not None:
            self._cella = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cella is not None:
            self._riga.append(re.sub(r"\s+", " ", "".join(self._cella)).strip())
            self._cella = None
        elif tag == "tr" and self._riga is not None:
            self.righe.append(self._riga)
            self._riga = None

    def handle_data(self, data):
        if self._cella is not None:
            self._cella.append(data)


def tabella(base: Path, libro: str, sid: int, nome: str) -> "list[list[str]]":
    c = sqlite3.connect(base / f"book-{libro}.db")
    r = c.execute("select name, body from sections where section_id=?", (sid,)).fetchone()
    if not r or r[0] != nome:
        sys.exit(f"book-{libro} {sid}: atteso «{nome}», trovato «{r and r[0]}»")
    p = _Righe()
    p.feed(html.unescape(r[1]))
    return [x for x in p.righe if x]


def numero(s: str) -> int:
    s = s.replace(",", "").replace("gp", "").replace("–", "-").replace("–", "-").strip()
    return int(s)


def fonte(libro: str, sid: int, nome: str) -> str:
    return f'fonte = "PRD PF1e, devonjones/PSRD-Data@{COMMIT[:8]}, book-{libro}.db sezione {sid} «{nome}»"'


def pe(base: Path) -> str:
    nome = "Table: Character Advancement and Level-Dependent Bonuses"
    righe = tabella(base, "cr", 2743, nome)
    tracce = {"lenta": {}, "media": {}, "veloce": {}}
    for r in righe:
        m = re.match(r"^(\d+)(st|nd|rd|th)$", r[0])
        if not m:
            continue
        liv = int(m.group(1))
        for k, v in zip(("lenta", "media", "veloce"), r[1:4]):
            tracce[k][liv] = 0 if liv == 1 else numero(v)
    out = ["# sistemi/pf1e/dati/pe.toml — i PE per livello, tre tracce (generato da estrai_prd_pf1e.py)",
           fonte("cr", 2743, nome), ""]
    for k in ("lenta", "media", "veloce"):
        out.append(f"[soglie.{k}]")
        out += [f'"{liv}" = {v}' for liv, v in sorted(tracce[k].items())]
        out.append("")
    assert all(len(t) == 20 for t in tracce.values())
    return "\n".join(out)


def incontri(base: Path) -> str:
    n1 = "Table: Experience Point Awards"
    righe = tabella(base, "cr", 3655, n1)
    px = {}
    for r in righe:
        if re.fullmatch(r"\d+(/\d+)?", r[0]) and len(r) >= 2:
            px[r[0]] = numero(r[1])
    n2 = "Table: Encounter Design"
    diff = {}
    for r in tabella(base, "cr", 3653, n2):
        if len(r) == 2 and r[1].startswith("APL"):
            d = r[1].replace("APL", "").replace("–", "-").replace("–", "-").strip() or "0"
            diff[r[0]] = int(d)
    out = ["# sistemi/pf1e/dati/incontri.toml — PE per GS e difficoltà (generato da estrai_prd_pf1e.py)",
           "# Un incontro PF1e vale la somma dei PE delle creature; il suo GS è il più alto",
           "# il cui valore in PE non supera la somma («Designing Encounters», book-cr 3652).",
           fonte("cr", 3655, n1), f'fonte_difficolta = "book-cr.db sezione 3653 «{n2}»"',
           'metodo = "somma_px"  # letto da suggest_encounter (ADR-0111, L4)', "", "[px_per_gs]"]
    def chiave(g):
        a, _, b = g.partition("/")
        return int(a) / int(b) if b else int(a)
    out += [f'"{g}" = {v}' for g, v in sorted(px.items(), key=lambda kv: chiave(kv[0]))]
    out += ["", "[difficolta]  # GS dell'incontro = APL + scarto"]
    out += [f'"{k.lower()}" = {v}' for k, v in diff.items()]
    assert len(px) == 30 and diff
    return "\n".join(out) + "\n"


def tesoro(base: Path) -> str:
    nome = "Table: Treasure Values per Encounter"
    out = ["# sistemi/pf1e/dati/tesoro.toml — mo per incontro per APL (generato da estrai_prd_pf1e.py)",
           fonte("cr", 3661, nome), ""]
    tr = {"lenta": {}, "media": {}, "veloce": {}}
    for r in tabella(base, "cr", 3661, nome):
        if re.fullmatch(r"\d+", r[0]) and len(r) >= 4:
            for k, v in zip(("lenta", "media", "veloce"), r[1:4]):
                tr[k][int(r[0])] = numero(v)
    for k in ("lenta", "media", "veloce"):
        out.append(f"[mo_per_incontro.{k}]")
        out += [f'"{a}" = {v}' for a, v in sorted(tr[k].items())]
        out.append("")
    assert all(len(t) == 20 for t in tr.values())
    return "\n".join(out)


def creature(base: Path) -> str:
    n1 = "Table: Creature Statistics by Type"
    bab = {"HD × 3/4 (Medium BAB)": 0.75, "HD (Fast BAB)": 1.0, "HD × 1/2 (Slow BAB)": 0.5}
    ts = {"Fort": "temp", "Ref": "rifl", "Will": "vol"}
    tipi = []
    for r in tabella(base, "b1", 116, n1):
        if len(r) == 5 and r[1].startswith("d"):
            buoni = [ts[x.strip()] for x in r[3].split(",") if x.strip() in ts]
            var = re.search(r"any (one|two)", r[3])
            tipi.append((r[0].lower(), int(r[1][1:]), bab[r[2]], buoni,
                         {"one": 1, "two": 2}[var.group(1)] if var else 0,
                         int(re.match(r"(\d+)", r[4]).group(1))))
    n2 = "Table: Size Bonuses and Penalties"
    taglie = []
    for r in tabella(base, "b1", 160, n2):
        if len(r) == 5 and r[0] in ("Fine", "Diminutive", "Tiny", "Small", "Medium", "Large",
                                    "Huge", "Gargantuan", "Colossal"):
            taglie.append((r[0].lower(), numero(r[1]), numero(r[2])))
    out = ["# sistemi/pf1e/dati/creature.toml — tipi e taglie PF1e (generato da estrai_prd_pf1e.py)",
           fonte("b1", 116, n1), f'fonte_taglie = "book-b1.db sezione 160 «{n2}»"', "",
           "# tipo = { dv = faccia del dado, bab = per DV, ts_buoni, ts_a_scelta (umanoide 1, esterno 2), gradi = per DV + Int }",
           "[tipi]"]
    for nome, dv, b, buoni, scelta, gradi in tipi:
        lista = ", ".join(f'"{x}"' for x in buoni)
        out.append(f'"{nome}" = {{ dv = {dv}, bab = {b}, ts_buoni = [{lista}], ts_a_scelta = {scelta}, gradi = {gradi} }}')
    out += ["", "# taglia = { ca_attacco, bmc_dmc }", "[taglie]"]
    out += [f'"{n}" = {{ ca_attacco = {a}, bmc_dmc = {c} }}' for n, a, c in taglie]
    assert len(tipi) == 13 and len(taglie) == 9
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# conformita_prd.toml: le regole PF1e che conformita_statblocchi controlla
# sulle schede (BAB e TS per classe, sensi per tipo, sottotipo e razza).
# ---------------------------------------------------------------------------
LIBRI_CLASSI = ("cr", "apg", "acg", "uc", "um")
#: Le progressioni PF1e: si verifica livello per livello che la tabella del PRD
#: sia una di queste, altrimenti la classe non entra (e il generatore lo dice).
BAB = {1.0: lambda L: L, 0.75: lambda L: 3 * L // 4, 0.5: lambda L: L // 2}
TS = {"buono": lambda L: 2 + L // 2, "scarso": lambda L: L // 3,
      "buono_prestigio": lambda L: (L + 1) // 2, "scarso_prestigio": lambda L: (L + 1) // 3}
#: piedi → metri, alla scala del progetto (1,5 m per 5 piedi)
METRI = {30: 9, 60: 18, 90: 27, 120: 36}


def _ordinale(s: str) -> "int | None":
    m = re.match(r"(\d+)(st|nd|rd|th)$", s)
    return int(m.group(1)) if m else None


def _lessico(*categorie: str) -> "dict[str, str]":
    """{inglese: italiano} dal lessico PF1e del repo (prima voce vince)."""
    import csv
    out: "dict[str, str]" = {}
    for f in ("lessico_it_pf1.tsv", "lessico_it_35.tsv"):
        with open(ROOT / "scripts" / f, encoding="utf-8") as fh:
            for r in csv.reader(fh, delimiter="\t"):
                if len(r) >= 3 and r[2] in categorie:
                    out.setdefault(r[1], r[0])
    return out


def _classi(base: Path):
    fuori, scartate = [], []
    for libro in LIBRI_CLASSI:
        c = sqlite3.connect(base / f"book-{libro}.db")
        q = ("select s.section_id, s.name, s.subtype, s.lft, s.rgt from sections s "
             "join class_details cd on cd.section_id = s.section_id order by s.section_id")
        for sid, nome, tipo, lft, rgt in c.execute(q).fetchall():
            # la prima tabella della classe con «Level» in testa; lo Swashbuckler
            # (book-acg 1145) ha le teste «Bonus, Save, Save, Save»: l'ordine è
            # quello di tutte le altre (BAB, Tempra, Riflessi, Volontà)
            t, col = None, None
            for tid, corpo in c.execute("select section_id, body from sections where type = 'table' "
                                        "and lft > ? and rgt < ? order by lft", (lft, rgt)).fetchall():
                p = _Righe()
                p.feed(html.unescape(corpo or ""))
                testa = next((r for r in p.righe if r and r[0] == "Level"), None)
                if not testa:
                    continue
                if any(h.startswith("Base Attack") for h in testa):
                    col = [next(i for i, h in enumerate(testa) if h.startswith(k))
                           for k in ("Base Attack", "Fort", "Ref", "Will")]
                elif testa[1:5] == ["Bonus", "Save", "Save", "Save"]:
                    col = [1, 2, 3, 4]
                else:
                    continue
                t = (tid, corpo)
                break
            if not t:
                scartate.append(f"{nome} (book-{libro} {sid}: nessuna tabella)")
                continue
            righe = set()
            for r in p.righe:
                if r and _ordinale(r[0]) and len(r) > max(col):
                    try:
                        righe.add((_ordinale(r[0]),) + tuple(int(r[i].split("/")[0]) for i in col))
                    except ValueError:
                        pass
            righe = sorted(righe)
            bab = next((k for k, f in BAB.items() if all(x[1] == f(x[0]) for x in righe)), None)
            ts = [next((k for k, f in TS.items() if all(x[i] == f(x[0]) for x in righe)), None)
                  for i in (2, 3, 4)]
            if bab is None or None in ts or len(righe) not in (10, 20):
                scartate.append(f"{nome} (book-{libro} {t[0]}: progressione fuori formula)")
                continue
            fuori.append((nome.lower(), bab, ts, tipo, libro, t[0]))
    return fuori, scartate


def _sensi_di(testo: str) -> "tuple[int, bool]":
    dv = re.search(r"[Dd]arkvision (\d+) feet", testo)
    return (METRI[int(dv.group(1))] if dv else 0), bool(re.search(r"[Ll]ow-light vision", testo))


def _sensi_regole(base: Path, primo: int, ultimo: int):
    c = sqlite3.connect(base / "book-b1.db")
    fuori = []
    for sid, nome in c.execute("select section_id, name from sections where section_id between ? and ? "
                               "and type = 'section' and url like 'pfsrd://Bestiary/Rules/Creature Types/%' "
                               "order by section_id", (primo, ultimo)).fetchall():
        corpi = [c.execute("select body from sections where section_id = ?", (sid,)).fetchone()[0] or ""]
        corpi += [b or "" for (b,) in c.execute("select body from sections where parent_id = ?", (sid,))]
        testo = re.sub(r"<[^>]+>", " ", " ".join(corpi))
        dv, ll = _sensi_di(testo)
        if dv or ll:
            fuori.append((nome.replace(" Subtype", "").lower(), dv, ll, sid))
    return fuori


def _sensi_razze(base: Path):
    it = _lessico("mostro", "razza")
    fuori = {}
    for libro in ("b1", "b2", "b3", "b4"):
        c = sqlite3.connect(base / f"book-{libro}.db")
        q = ("select s.section_id, s.name, cd.senses from sections s join creature_details cd "
             "on cd.section_id = s.section_id where cd.creature_type = 'Humanoid' order by s.section_id")
        for sid, nome, sensi in c.execute(q):
            dv = re.search(r"darkvision (\d+) ft", sensi or "")
            ll = "low-light vision" in (sensi or "")
            ita = it.get(nome)
            if not (dv or ll) or not ita or "(" in nome or ita.startswith("Archetipo") or ita in fuori:
                continue
            fuori[ita] = (nome, METRI[int(dv.group(1))] if dv else 0, ll, libro, sid)
    return fuori


def conformita_prd(base: Path) -> str:
    classi, scartate = _classi(base)
    it = {k.lower(): v for k, v in _lessico("classe", "classe di prestigio").items()}
    out = ["# sistemi/pf1e/dati/conformita_prd.toml — le regole PF1e che conformita_statblocchi",
           "# controlla sulle schede (generato da estrai_prd_pf1e.py, non si scrive a mano).",
           f'fonte = "PRD PF1e, devonjones/PSRD-Data@{COMMIT[:8]}: tabelle delle classi, '
           'Bestiary «Creature Types», creature del Bestiario 1-4"', "",
           "# classe = { bab per livello, ts = [Tempra, Riflessi, Volontà], tabella del PRD }",
           "# buono = 2 + L/2, scarso = L/3; *_prestigio = (L+1)/2 e (L+1)/3 (classi di prestigio)",
           "[classi]"]
    for nome, bab, ts, tipo, libro, tid in classi:
        lista = ", ".join(f'"{x}"' for x in ts)
        out.append(f'"{nome}" = {{ bab = {bab}, ts = [{lista}], tipo = "{tipo}", tabella = "book-{libro} {tid}" }}')
    out += ["", "# nome italiano (lessico_it_pf1.tsv, classi PNG da lessico_it_35.tsv) = classe del PRD",
            "[alias_classi]"]
    alias = {}
    for nome, *_ in classi:
        if nome in it:
            alias[it[nome].lower()] = nome
    out += [f'"{k}" = "{v}"' for k, v in sorted(alias.items())]
    if scartate:
        out += ["", "# fuori: " + " · ".join(scartate)]
    out += ["", "# scurovisione in metri (0 = no), visione crepuscolare; book-b1 «Creature Types»",
            "[sensi.tipi]"]
    for nome, dv, ll, sid in _sensi_regole(base, 361, 386):
        out.append(f'"{nome}" = {{ scurovisione = {dv}, crepuscolare = {str(ll).lower()}, sezione = {sid} }}')
    out += ["", "[sensi.sottotipi]"]
    for nome, dv, ll, sid in _sensi_regole(base, 388, 433):
        out.append(f'"{nome}" = {{ scurovisione = {dv}, crepuscolare = {str(ll).lower()}, sezione = {sid} }}')
    out += ["", "# umanoidi del Bestiario 1-4 con sensi propri, per nome italiano (lessico_it_pf1.tsv)",
            "[sensi.razze]"]
    for ita, (nome, dv, ll, libro, sid) in sorted(_sensi_razze(base).items()):
        out.append(f'"{ita.lower()}" = {{ scurovisione = {dv}, crepuscolare = {str(ll).lower()}, '
                   f'prd = "{nome}", fonte = "book-{libro} {sid}" }}')
    c = sqlite3.connect(base / "book-b1.db")
    testo = c.execute("select body from sections where section_id = 1112").fetchone()[0]
    assert "DC equal to the dragon's frightful presence" in testo, "Corrupt Water cambiato"
    out += ["", "[corrompere_acqua]",
            '# «Liquid-based magic items … must succeed on a Will save (DC equal to the dragon\'s',
            "# frightful presence) or become ruined» — la stessa regola dell'SRD 3.5",
            'cd = "presenza_terrificante"', 'fonte = "book-b1 1112 «Corrupt Water»"']
    assert len(classi) >= 40 and "fighter" in alias.values()
    return "\n".join(out) + "\n"


FILE = {"pe.toml": pe, "incontri.toml": incontri, "tesoro.toml": tesoro, "creature.toml": creature,
        "conformita_prd.toml": conformita_prd}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    base = cache()
    diversi = []
    for nome, f in FILE.items():
        testo = f(base)
        dest = DEST / nome
        if a.check:
            if not dest.is_file() or dest.read_text(encoding="utf-8") != testo:
                diversi.append(nome)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(testo, encoding="utf-8")
            print(f"scritto {dest.relative_to(ROOT)}")
    for d in diversi:
        print(f"🔴 {d} diverso dal PRD")
    return 1 if diversi else 0


if __name__ == "__main__":
    sys.exit(main())
