#!/usr/bin/env python3
"""Rifà i contratti JSON di M7-C (la piazza del comando) e M7-H (il quartiere attorno).

Il DM, 2026-10-24: la tenda e il campo devono essere coerenti, «come gli
accampamenti romani o dei barbari», senza tende attaccate a quella di Zog'tar.

- M7-C resta la mappa dello scontro e tiene la tenda dov'era (stesse coordinate
  di tutte le scene), ma la sua cornice diventa lo steccato: la piazza sgombra
  è di 40,5 × 34,5 m, la tenda del turno dopo sta a 9 m nell'angolo nord-est,
  e le file di tende e i ripari degli orchi escono dalla mappa.
- M7-H è nuova: lo stesso steccato con il quartiere attorno, 66 × 60 m, per il
  barile, la fuga dalla tenda in fiamme e i rinforzi che arrivano dalle vie.

Uso (dalla radice del repo):
    python3 plans/esperimenti/barile-zogtar-2026-10-24/genera_mappe.py
    python3 scripts/compile_map_json.py <json> -o <md>   # per ciascuna mappa
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

RADICE = Path(__file__).resolve().parents[3]
MAPPE = RADICE / "07_il Portale Della Forgia Eterna" / "Mappe"
M7C = MAPPE / "ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.json"
M7H = MAPPE / "ARC07-MAPPE-M7H-QUARTIERE-DEL-COMANDO.json"

LARGH, ALT = 27, 23          # M7-C: la piazza dentro lo steccato
DX, DY = 8, 8                # dove sta M7-C dentro M7-H
H_LARGH, H_ALT = 44, 40      # M7-H


def steccato() -> list[dict]:
    """Lo steccato corre sul bordo di M7-C, con quattro varchi sulle vie."""
    s = "Steccato di pali appuntiti, alto 1,5 m: chiude la piazza del comando"
    return [
        {"type": "🧱", "line": [[0, 0], [11, 0]], "label": s},
        {"type": "🧱", "line": [[15, 0], [26, 0]]},
        {"type": "🧱", "line": [[0, 22], [12, 22]]},
        {"type": "🧱", "line": [[16, 22], [26, 22]]},
        {"type": "🧱", "line": [[0, 1], [0, 9]]},
        {"type": "🧱", "line": [[0, 13], [0, 21]]},
        {"type": "🧱", "line": [[26, 1], [26, 9]]},
        {"type": "🧱", "line": [[26, 13], [26, 21]]},
    ]


def rifai_m7c(d: dict) -> dict:
    d = copy.deepcopy(d)
    d["regions"] = [
        {"terrain": "🟫", "rect": [1, 1, 25, 21],
         "label": "La piazza del comando: terra battuta, sgombra, dentro lo steccato"},
        {"terrain": "🟫", "rect": [12, 0, 3, 1], "label": "Il varco nord, sulla via per la fortezza"},
        {"terrain": "🟫", "rect": [13, 22, 3, 1], "label": "Il varco sud, sulla via per le colline"},
        {"terrain": "🟫", "rect": [26, 10, 1, 3], "label": "Il varco est"},
        {"terrain": "🟫", "rect": [0, 10, 1, 3], "label": "Il varco ovest, verso i clan degli orchi"},
        d["regions"][-1],  # l'interno della tenda, invariato
    ]
    tenuti = [s for s in d["structures"]
              if s["type"] != "🧱" and not (s["type"] == "🎪" and "rect" in s
                                             and s["rect"][2:] in ([2, 2], [2, 1], [1, 2])
                                             and s.get("label") != "Telo del glifo")]
    tenuti.append({"type": "🎪", "rect": [23, 3, 2, 2],
                   "label": "Tenda del turno dopo"})
    d["structures"] = steccato() + tenuti
    nuovi_fuochi = {
        "Fuoco del clan": None,
    }
    hz = []
    for h in d["hazards"]:
        if h.get("label") in nuovi_fuochi:
            continue
        hz.append(h)
    luce = "Luce: intensa entro 6 m, fioca fino a 12 m, come una torcia dell'SRD"
    hz.insert(3, {"type": "🔥", "at": [2, 9], "label": "Fuoco del varco ovest",
                  "effect": f"le sentinelle del varco: chi entra nella cella prende 1d6 da fuoco. {luce}"})
    hz.insert(4, {"type": "🔥", "at": [24, 13], "label": "Fuoco del varco est",
                  "effect": f"le sentinelle del varco: chi entra nella cella prende 1d6 da fuoco. {luce}"})
    d["hazards"] = hz
    for m in d["movements"]:
        if m["name"].startswith("Le due guardie del turno dopo"):
            m["path"] = [[23, 5], [20, 16], [14, 15]]
    d["tattiche"] = [t.replace("nella loro tenda, V11–W12", "nella loro tenda, X4–Y5, a 9 m dal telo")
                     for t in d["tattiche"]]
    d["notes"] = [n for n in d["notes"] if not n.startswith("Com'è fatto il campo")]
    d["notes"].append(
        "Com'è fatto il campo qui attorno: la cornice di questa mappa è lo steccato. Dentro c'è "
        "solo la piazza del comando, 40,5 × 34,5 m di terra battuta, con la tenda sola nel mezzo, "
        "come il pretorio di un campo romano; l'unica altra tenda è quella del turno dopo, a 9 m, "
        "nell'angolo nord-est. Fuori dai quattro varchi corre una corsia di 3 m, poi le file di "
        "tende hobgoblin a nord, a est e a sud, e i clan degli orchi a ovest: sono su M7-H, "
        "che serve per il barile e per i rinforzi.")
    d["evoluzione"].append({
        "stato": "I · il barile",
        "trigger": "i PG lasciano cadere dall'alto il barile d'olio con le fiale della fenice",
        "griglia": "dove cade: pozza d'olio di 3 × 3 quadretti attorno all'impatto, schizzi fino a "
                   "2 quadretti, il telo squarciato; se prende il colmo (riga 12) la tenda crolla",
        "effetto": "palle di fuoco da 6d6 (Riflessi CD 14), oggetto in caduta 15d6 su chi sta "
                   "nella casella, olio in fiamme, fumo, crollo: tutte le regole in "
                   "ARC07-BARILE-SULLA-TENDA.md"})
    return d


def sposta(p: list[int]) -> list[int]:
    return [p[0] + DX, p[1] + DY]


def sposta_voce(v: dict) -> dict:
    v = copy.deepcopy(v)
    if "at" in v:
        v["at"] = sposta(v["at"])
    if "rect" in v:
        v["rect"] = sposta(v["rect"][:2]) + v["rect"][2:]
    if "line" in v:
        v["line"] = [sposta(p) for p in v["line"]]
    if "area" in v and "rect" in v["area"]:
        v["area"]["rect"] = sposta(v["area"]["rect"][:2]) + v["area"]["rect"][2:]
    if "path" in v:
        v["path"] = [sposta(p) for p in v["path"]]
    return v


def tende_hobgoblin() -> list[dict]:
    """Contubernium: 3 × 3 m, otto soldati. File diritte, corsie di 1,5 m fra le tende."""
    t = []
    xs_nord = [0, 3, 6, 9, 12, 15, 25, 28, 31, 34, 37, 40]
    for i, x in enumerate(xs_nord):
        if x < 9:
            continue  # l'angolo nord-ovest è dei clan
        for y in (0, 3):
            t.append({"type": "🎪", "rect": [x, y, 2, 2]} | {})
    for y in (9, 12, 15, 22, 25, 28):
        for x in (38, 41):
            t.append({"type": "🎪", "rect": [x, y, 2, 2]})
    for x in (9, 12, 15, 18, 25, 28, 31, 34, 37, 40):
        for y in (34, 37):
            t.append({"type": "🎪", "rect": [x, y, 2, 2]})
    return t


def clan_orchi() -> tuple[list[dict], list[dict]]:
    """Quattro bande d'orchi a ovest: ripari storti attorno al fuoco, vuoto fra un clan e l'altro."""
    ripari, fuochi = [], []
    clan = [
        ("Fuoco della banda della Zanna", (3, 3), [(0, 1, 2, 1), (5, 0, 1, 2), (1, 5, 2, 1), (5, 5, 1, 1)]),
        ("Fuoco della banda del Corvo", (3, 12), [(0, 10, 1, 2), (2, 9, 2, 1), (5, 11, 1, 2), (1, 15, 2, 1)]),
        ("Fuoco della banda dell'Ascia Rotta", (3, 25), [(0, 23, 2, 1), (5, 22, 1, 2), (0, 27, 1, 2), (4, 28, 2, 1)]),
        ("Fuoco della banda dei Teschi", (3, 35), [(0, 33, 2, 1), (5, 34, 1, 2), (1, 38, 2, 1), (4, 37, 1, 2)]),
    ]
    for i, (nome, (fx, fy), rs) in enumerate(clan):
        fuochi.append({"type": "🔥", "at": [fx, fy], "label": nome,
                       "effect": "il fuoco comune di una banda d'orchi: chi entra nella cella prende "
                                 "1d6 da fuoco. Luce: intensa entro 6 m, fioca fino a 12 m. Attorno "
                                 "dormono una ventina d'orchi e lo sciamano della banda"})
        for j, (x, y, w, h) in enumerate(rs):
            v = {"type": "🎪", "rect": [x, y, w, h]}
            ripari.append(v)
    return ripari, fuochi


def costruisci_m7h(c: dict) -> dict:
    h = {
        "schema_version": "1.0",
        "title": "M7-H — Il quartiere del comando: la piazza e le tende attorno (notte, ≈372 DR)",
        "scale_m_per_square": 1.5,
        "map_size": [H_LARGH, H_ALT],
        "base_terrain": "🟩",
        "north": "N",
        "tipo": "tattica",
        "ambiente": "esterno",
        "luogo": c["luogo"],
        "quota": c["quota"],
        "dislivello": c["dislivello"],
    }
    regioni = [
        {"terrain": "🟫", "rect": [6, 6, 31, 2], "label": "La corsia attorno allo steccato, larga 3 m"},
        {"terrain": "🟫", "rect": [6, 31, 31, 2]},
        {"terrain": "🟫", "rect": [6, 8, 2, 23]},
        {"terrain": "🟫", "rect": [35, 8, 2, 23]},
        {"terrain": "🟫", "rect": [20, 0, 3, 6], "label": "La via nord, larga 4,5 m, verso la fortezza"},
        {"terrain": "🟫", "rect": [21, 33, 3, 7], "label": "La via sud, verso le colline"},
        {"terrain": "🟫", "rect": [37, 18, 7, 3], "label": "La via est"},
        {"terrain": "🟫", "rect": [0, 18, 6, 3], "label": "La via ovest, fra i clan degli orchi"},
        {"terrain": "🟫", "rect": [8, 2, 12, 1], "label": "Corsia fra le file di tende"},
        {"terrain": "🟫", "rect": [24, 2, 20, 1]},
        {"terrain": "🟫", "rect": [8, 36, 13, 1]},
        {"terrain": "🟫", "rect": [24, 36, 20, 1]},
        {"terrain": "🟫", "rect": [40, 8, 1, 10]},
        {"terrain": "🟫", "rect": [40, 21, 1, 10]},
    ]
    for r in c["regions"]:
        regioni.append(sposta_voce(r))
    h["regions"] = regioni
    ripari, fuochi = clan_orchi()
    h["structures"] = [sposta_voce(s) for s in c["structures"]] + tende_hobgoblin() + ripari
    h["hazards"] = [sposta_voce(z) for z in c["hazards"] if z["type"] in ("🔥", "🏮", "🟪")] + fuochi + [
        {"type": "🔥", "at": [21, 3], "label": "Fuoco del quartiere nord",
         "effect": "un fuoco in mezzo alla via, lontano dai teli: chi entra nella cella prende 1d6 da fuoco. Luce: intensa entro 6 m, fioca fino a 12 m"},
        {"type": "🔥", "at": [39, 19], "label": "Fuoco del quartiere est",
         "effect": "come il fuoco del quartiere nord"},
        {"type": "🔥", "at": [22, 37], "label": "Fuoco del quartiere sud",
         "effect": "come il fuoco del quartiere nord"},
    ]
    unita = [sposta_voce(u) for u in c["units"] if not u["name"].startswith("I quattro PG")]
    unita.insert(0, {"faction": "PG", "name": "I PG in volo, invisibili, a 48 m sopra la tenda",
                     "token": "🔵", "at": [22, 18], "quantity": 4})
    unita += [
        {"faction": "Orda", "name": "Squadra hobgoblin del quartiere nord, otto per tenda", "token": "🔴",
         "at": [27, 2], "quantity": 8, "cr": "Guerriero 4"},
        {"faction": "Orda", "name": "Squadra hobgoblin del quartiere sud", "token": "🔴",
         "at": [27, 36], "quantity": 8, "cr": "Guerriero 4"},
        {"faction": "Orda", "name": "Banda d'orchi del Corvo, attorno al fuoco", "token": "🔴",
         "at": [2, 13], "quantity": 20, "cr": "GS ½"},
        {"faction": "Orda", "name": "Le sentinelle del varco est", "token": "🔴",
         "at": [37, 20], "quantity": 2, "cr": "Guerriero 4"},
    ]
    h["units"] = unita
    h["movements"] = [
        {"name": "Le ronde di orchi dalla via ovest (1d4+2 round)", "path": [[0, 19], [8, 19]], "color": "#e85d04"},
        {"name": "Gli squadroni hobgoblin dalla via sud (2d4+2 round)", "path": [[22, 39], [22, 31]], "color": "#9d0208"},
        {"name": "Gli squadroni hobgoblin dalla via nord (2d4+2 round)", "path": [[21, 0], [21, 8]], "color": "#9d0208"},
        {"name": "Le sentinelle del varco est", "path": [[37, 19], [34, 19]], "color": "#d62828"},
        {"name": "Le due guardie del turno dopo", "path": [[31, 13], [28, 24], [22, 23]], "color": "#7b2cbf"},
    ]
    h["notes"] = [
        "M7-H è M7-C con il quartiere attorno: la piazza è la stessa e le sue coordinate sono quelle "
        "di M7-C spostate di otto colonne e otto righe (la N12 di M7-C qui è V20).",
        "Le vie sono larghe 4,5 m, le corsie fra le file 1,5 m, la corsia attorno allo steccato 3 m: "
        "le misure del campo di Polibio ridotte a un'orda (plans/esperimenti/mappe-campo-2026-10-21/"
        "RICERCA-ACCAMPAMENTI.md). Le tende hobgoblin sono da otto, 3 × 3 m, in file diritte; i "
        "ripari degli orchi sono storti, attorno al fuoco della banda, con il vuoto fra un clan e l'altro.",
        "Il barile: i PG volano a 48 m, invisibili. Lo sgancio, la deviazione, le fiale della fenice, "
        "l'olio e il fuoco sono in ARC07-BARILE-SULLA-TENDA.md. Una palla di fuoco ha 6 m di raggio, "
        "4 quadretti: dal palo centrale arriva al telo e a Grask solo se il barile devia verso sud.",
        "Le tende hobgoblin più vicine sono a 12 m dal telo del comando, oltre lo steccato e la corsia: "
        "nessuna palla di fuoco nata nella tenda ci arriva, e il fuoco non salta lo spiazzo.",
    ]
    h["tattiche"] = [
        "**Il campo si sveglia** (Scena 8): il boato si sente in tutto il quartiere. Le sentinelle dei "
        "varchi gridano e restano al loro posto; le ronde d'orchi arrivano dalla via ovest in 1d4+2 "
        "round, gli squadroni hobgoblin da nord e da sud in 2d4+2. Finché Zog'tar è in piedi non "
        "entrano nella piazza: fanno quadrato sulla corsia, fuori dallo steccato, e passano secchi e "
        "coperte bagnate oltre i varchi.",
        "**Chi guarda in alto**: nessuno, al primo round. Dal secondo gli sciamani dei clan cercano "
        "chi ha lanciato, e chi ha *vedere invisibilità* guarda il cielo; a 48 m la scurovisione "
        "(18 m) non arriva, e le stelle non bastano per vedere un invisibile che non si muove.",
    ]
    h["evoluzione"] = [
        {"stato": "I · il barile", "trigger": "il barile cade sulla tenda",
         "griglia": "la tenda brucia; lo spiazzo attorno resta sgombro",
         "effetto": "allarme in tutto il quartiere; i rinforzi seguono le vie, non le corsie"},
        {"stato": "J · i secondi barilotti", "trigger": "i PG lasciano cadere uno dei barilotti da 10 litri",
         "griglia": "una pozza di 1 quadretto e schizzi attorno, dove cade",
         "effetto": "sul varco o sulla via dove si ammassano i rinforzi, o sulla tenda del turno dopo: "
                    "regole in ARC07-BARILE-SULLA-TENDA.md"},
    ]
    h["note_dm"] = [
        "**Il quartiere misura 66 × 60 m**: la piazza del comando, 40,5 × 34,5 m dentro lo steccato, "
        "con attorno la corsia di 3 m e la prima fila di tende. Oltre il bordo il campo continua per "
        "mezzo chilometro in ogni direzione (M7-A)."]
    h["taglie"] = [{"at": sposta(t["at"]), "taglia": t["taglia"]} for t in c.get("taglie", [])]
    return h


def main() -> None:
    c = json.loads(M7C.read_text(encoding="utf-8"))
    nuovo = rifai_m7c(c)
    M7C.write_text(json.dumps(nuovo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    M7H.write_text(json.dumps(costruisci_m7h(nuovo), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("scritti", M7C.name, M7H.name)


if __name__ == "__main__":
    main()
