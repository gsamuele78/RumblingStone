#!/usr/bin/env python3
"""verifica_talenti.py — i prerequisiti dei talenti sulle schede che esistono (ADR-0124).

Scopo
  Il generatore sceglie talenti leciti (`dmcore.talenti`), ma nessun cancello
  controllava i talenti delle schede già scritte: il 2026-11-11 erano 30
  violazioni in 19 schede del Bestiario. Questo strumento legge le schede, e per
  ogni talento elencato restituisce il prerequisito che manca con la **regola**,
  il valore **atteso** e quello che la scheda **ha**, più `file:riga`.

  È pensato per essere chiamato da un agente attraverso il server MCP
  (`rumblingstone-tools`): con `--json` l'agente riceve la regola esatta e il
  controesempio, corregge, e richiama finché la scheda è pulita. Sola lettura.

  La regola è una sola, `dmcore.talenti.violazioni`, la stessa del generatore.
  I talenti bonus che una classe concede senza prerequisiti (monaco, stili del
  ranger) non sono violazioni. Un talento che il lessico non riconosce va in
  `ignoti`, e una classe che la scheda non dichiara nel `tipo` o nel titolo non
  si conosce: per questo le violazioni di livello d'incantatore o di classe
  vanno lette con la scheda accanto.

Uso
  python3 scripts/verifica_talenti.py                       # tutto il Bestiario
  python3 scripts/verifica_talenti.py Bestiario/png/x.md    # una scheda o una cartella
  python3 scripts/verifica_talenti.py --json                # uscita per l'agente
  python3 scripts/verifica_talenti.py --check               # esce 1 se c'è una violazione

Exit  0 = misura fatta (o nessuna violazione con --check)
      1 = violazioni, solo con --check
      2 = errore d'uso

Solo stdlib.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import lettura_creatura as L  # noqa: E402
from dmcore import talenti as T  # noqa: E402

#: La riga dei talenti: «**Talenti:** …», «Feats: …», «- Talenti: …».
RIGA = re.compile(r"^\W*(?:Talenti|Feats)\W*?(?:\*\*\s*)?(?::|：|\*\*)\**\s*(.+)$", re.I)
#: Incantatori e la frazione di livello che dà il livello d'incantatore (3.5:
#: paladino e ranger dal 4°, metà livello).
INCANTATORI = {"wizard": 1, "sorcerer": 1, "cleric": 1, "druid": 1, "bard": 1,
               "paladin": 0.5, "ranger": 0.5}
NON_VERIFICABILI = {"gradi", "altro"}
#: Le competenze che una classe base dà da sé (SRD 3.5, «Weapon and Armor
#: Proficiency» di ogni classe; PF1e uguale): non stanno nella riga dei talenti.
COMPETENZE_DI_CLASSE = {
    "Shield Proficiency": {"barbarian", "cleric", "druid", "fighter", "paladin", "ranger"},
    "Armor Proficiency (Light)": {"barbarian", "bard", "cleric", "druid", "fighter", "paladin",
                                  "ranger", "rogue"},
    "Armor Proficiency (Medium)": {"barbarian", "cleric", "druid", "fighter", "paladin", "ranger"},
    "Armor Proficiency (Heavy)": {"cleric", "fighter", "paladin"},
}
#: Regole che senza classi dichiarate non si possono giudicare.
SERVE_LA_CLASSE = ("lic", "capacita", "classe.")


def pezzi(riga: str) -> "list[str]":
    """I nomi dei talenti di una riga: virgole fuori dalle parentesi, senza markup."""
    riga = re.sub(r"`[^`]*`|\*|_", "", riga)
    riga = re.split(r"\s—\s|\.\s+[A-Z]", riga)[0]
    out, prof, buf = [], 0, ""
    for ch in riga:
        prof += (ch == "(") - (ch == ")")
        if ch == "," and prof == 0:
            out.append(buf)
            buf = ""
        else:
            buf += ch
    out.append(buf)
    return [re.sub(r"\s*\(.*?\)\s*", " ", x).strip(" .;") for x in out if x.strip()]


def sistema_di(p: Path, testo: str) -> str:
    """Il sistema che la scheda dichiara, altrimenti quello del suo percorso (sistemi.toml)."""
    from dmcore import sistemi as S
    dichiarato = S.sistema_dichiarato(testo)
    if dichiarato:
        return dichiarato
    return S.sistema_di(p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.name)


def leggi(p: Path) -> "dict | None":
    """I fatti di una scheda che servono ai prerequisiti, o None se non ha talenti."""
    s = L.leggi(p)
    if s is None:
        return None
    righe = s.testo.splitlines()
    n_riga, riga = next(((i + 1, m.group(1)) for i, r in enumerate(righe) if (m := RIGA.match(r))),
                        (None, None))
    if riga is None:
        return None
    sistema = sistema_di(p, s.testo)
    livelli: dict[str, int] = {}
    for n, liv in L.livelli_di_classe(s).items():
        n = T._ALIAS.get(n, n) if n in T.CLASSI_EN_IT.values() else n
        livelli[n] = livelli.get(n, 0) + liv
    dv = sum(g.n for g in s.gruppi)
    lic = int(max([livelli.get(c, 0) * f if livelli.get(c, 0) >= (4 if f < 1 else 1) else 0
                   for c, f in INCANTATORI.items()] or [0]))
    talenti, ignoti = [], []
    for nome in pezzi(riga):
        en = T.nome_inglese(sistema, nome)
        (talenti if en else ignoti).append(en or nome)
    return {"file": p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p),
            "riga": n_riga, "sistema": sistema,
            "car": {k: v for k, v in s.attributi.items() if isinstance(v, int)},
            "bab": s.bab, "livelli": livelli, "dv": dv, "lic": lic,
            "talenti": sorted(set(talenti)), "ignoti": ignoti}


def verifica(f: dict) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) di una scheda letta da `leggi`."""
    dalla_classe = [c for c, classi in COMPETENZE_DI_CLASSE.items() if classi & set(f["livelli"])]
    st = T.Stato(car=f["car"], bab=f["bab"] if f["bab"] is not None else 99,
                 livelli=f["livelli"], lic=f["lic"], talenti=f["talenti"] + dalla_classe, dv=f["dv"])
    viol, nv = [], []
    for en in f["talenti"]:
        if T.bonus_senza_prerequisiti(f["sistema"], en, f["livelli"]):
            continue
        for v in T.violazioni(f["sistema"], en, st):
            if v["regola"] == "bab" and f["bab"] is None:
                continue
            voce = {"file": f["file"], "riga": f["riga"], "talento": en,
                    "talento_it": T.italiano(f["sistema"], en), **v}
            senza_classe = (not f["livelli"] and v["regola"].startswith(SERVE_LA_CLASSE)
                            and v["regola"] != "classe.character")
            if senza_classe:
                voce["nota"] = "la scheda non dichiara le classi nel tipo né nel titolo"
            (nv if v["regola"] in NON_VERIFICABILI or senza_classe else viol).append(voce)
    return viol, nv


def schede(percorsi: "list[Path]") -> "list[Path]":
    out = []
    for p in percorsi:
        out += sorted(p.rglob("*.md")) if p.is_dir() else [p]
    return out


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("percorsi", nargs="*", type=Path, help="schede o cartelle (difetto: Bestiario/)")
    ap.add_argument("--json", action="store_true", help="uscita JSON per l'agente")
    ap.add_argument("--check", action="store_true", help="esce 1 se c'è almeno una violazione")
    a = ap.parse_args(argv)
    percorsi = [p if p.is_absolute() else ROOT / p for p in (a.percorsi or [Path("Bestiario")])]
    for p in percorsi:
        if not p.exists():
            print(f"verifica_talenti: {p} non esiste", file=sys.stderr)
            return 2
    lette, viol, nv, ignoti = 0, [], [], []
    for p in schede(percorsi):
        f = leggi(p)
        if f is None:
            continue
        lette += 1
        v, n = verifica(f)
        viol += v
        nv += n
        ignoti += [{"file": f["file"], "riga": f["riga"], "nome": x} for x in f["ignoti"]]
    if a.json:
        json.dump({"schede_con_talenti": lette, "violazioni": viol, "non_verificabili": nv,
                   "ignoti": ignoti}, sys.stdout, ensure_ascii=False, indent=1)
        print()
    else:
        for v in viol:
            print(f"{v['file']}:{v['riga']}: {v['talento_it']} ({v['talento']}) — "
                  f"manca {v['testo']}  [regola {v['regola']}]")
        print(f"{'✗' if viol else '✓'} verifica_talenti: {lette} schede con talenti, "
              f"{len(viol)} violazioni in {len({v['file'] for v in viol})} schede, "
              f"{len(nv)} prerequisiti non verificabili, {len(ignoti)} nomi non riconosciuti")
    return 1 if (a.check and viol) else 0


if __name__ == "__main__":
    sys.exit(main())
