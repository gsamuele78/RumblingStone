#!/usr/bin/env python3
"""migliora_prosa.py — una pipeline che sceglie la riscrittura di un box e misura se è migliore.

Il giudice di «migliore» resta il voto cieco del DM (ADR-0093): nessuna misura
automatica lo prevedeva (`RICERCA-QUALITA-MISURABILE-2026-10` §3). Questo script
mette in fila quattro cose, e la generazione delle candidate **non** è fra queste:
le scrive un agente (o una persona), lo script non chiama modelli linguistici.

| Comando | Cosa fa |
|---|---|
| `dataset` | raccoglie tutte le coppie votate alla cieca dal DM in `pipeline/VOTI.json` |
| `modello` | addestra il modello di preferenza e lo valida in leave-one-out, contro il caso e contro «vince la più lunga» |
| `scegli` | sceglie con un seme i box di ARC-07 e ARC-08 da migliorare, esclusi i congelati e quelli già usati |
| `migliora FILE --box N --candidate C.md` | filtra le candidate (fatti, box impoverito, regole 1-4 di §2-ter), le ordina col modello, dice la migliore |
| `campione` | scheda cieca: la vincitrice della pipeline contro l'originale, con `cieco_versioni.coppie` |
| `esito` | registra i voti in `VOTI.json`, rifà il modello, dice quanto vince la pipeline (Wilson) |

**Il modello** è una regressione logistica senza intercetta sulle differenze dei
tratti di due versioni (Bradley-Terry), con penalità L2, in libreria standard.
Modello e soglia sono fissati in `pipeline/SOGLIA.txt`, scritto prima di
addestrarlo: se l'accuratezza in leave-one-out non supera il caso (limite
inferiore di Wilson sopra 0,50) e la regola «vince la più lunga», il modello
ordina le candidate solo come suggerimento, e la pipeline vale come filtro di
non regressione e come raccoglitore di voti.

**Il filtro** scarta una candidata che cambia un fatto (`ciclo_prosa.confronta_fatti`),
che `ciclo_prosa.box_impoveriti` segnala, o che viola una delle regole di
`read-aloud-adulti.md` §2-ter misurabili: (1) meno dettagli sensoriali,
(2) monologo spezzato in battute, (3) frase finale tolta, (4) subordinata
spezzata. La regola 5 (guardare a occhio un rilievo di `misura_sintassi` prima
di riscrivere) riguarda chi scrive e non si misura.

Uso:

    python3 scripts/migliora_prosa.py dataset
    python3 scripts/migliora_prosa.py modello [--scrivi]
    python3 scripts/migliora_prosa.py scegli --seme 20261023 --n 6 --uscita BOX.json
    python3 scripts/migliora_prosa.py migliora FILE --box N --candidate C.md [--scelte S.json --id P01]
    python3 scripts/migliora_prosa.py campione --scelte S.json --seme 7 --scheda SCHEDA.md --chiave CHIAVE.json
    python3 scripts/migliora_prosa.py esito --scelte S.json --chiave CHIAVE.json --voti VOTI.txt

spaCy con `it_core_news_md` è facoltativo: senza, il tratto `livelli_max` vale
zero e la subordinata spezzata si stima dal numero di frasi e di subordinanti.
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import random
import re
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cieco_versioni as cv  # noqa: E402
import ciclo_prosa as cp  # noqa: E402
import misura_craft as mc  # noqa: E402

QUI = ROOT / "plans/esperimenti/qualita-misurabile-2026-10-22"
PIPE = QUI / "pipeline"
VOTI = PIPE / "VOTI.json"
CONGELATI = ROOT / "plans/esperimenti/giro3-arc07-2026-10-19/misure/CONGELATI.json"
CAMPIONE_RISCRITTURA = QUI / "riscrittura/campione/CAMPIONE.json"

ARC07 = [f"07_il Portale Della Forgia Eterna/ARC07-DEF-{i}-{n}.md" for i, n in (
    (1, "PIANO-TERRA-TERROS"), (2, "RITORNO-E-AFFRESCHI"), (3, "RESURREZIONE-HELLA"),
    (4, "VIAGGIO-MILLE-ANNI"), (5, "RITORNO-HAMMERFIST"))]
CARTELLA_ARC08 = "08_La Battaglia Di Hammerfist"

#: Le fonti già votate: le 38 coppie della calibrazione hanno il giro nel campo `set`.
FONTI_38 = {"giro2": "giro2-arc07-2026-10-18", "giro3": "giro3-arc07-2026-10-19",
            "prova": "prova-scrittura-italiana-2026-10-21"}

# ── i parametri fissati in SOGLIA.txt prima di addestrare ────────────────────
LAMBDA = 1.0
TRATTI = ("parole_log", "gulpease", "sensoriali", "gerundi_mente", "possessivi‰",
          "livelli_max", "mattr25", "frase_finale_tolta", "subordinata_spezzata",
          "nomi_tolti", "monologo_spezzato")
#: Il modello decide da solo solo se il limite inferiore di Wilson supera questo.
SOGLIA_WILSON = 0.5

# ── i tratti ─────────────────────────────────────────────────────────────────
_PAROLA = re.compile(r"[A-Za-zÀ-ÿ']+")
_FRASE = re.compile(r"(?<=[.!?…])[»”\"]?\s+")
#: Gli stessi possessivi della calibrazione (calibra_prosa.py, 2026-10-22).
_POSS = re.compile(r"\b(?:il|la|i|le|lo|gli|un|una|del|della|dei|delle|al|alla|nel|nella|sul|sulla)\s+"
                   r"(?:mio|mia|miei|mie|tuo|tua|tuoi|tue|suo|sua|suoi|sue|nostr[oaie]|vostr[oaie]|loro)\b"
                   r"|\b(?:suo|sua|suoi|sue)\b", re.I)
_SUBORDINANTI = re.compile(r"\b(?:che|cui|dove|quando|mentre|perché|finché|poiché|sebbene|benché|"
                           r"affinché|come se|prima che|dopo che)\b", re.I)
_STOP = set("il lo la i gli le un una uno di a da in con su per tra fra e o ma che non si ci vi è sono "
            "era erano ha hanno del della dei delle al alla ai alle dal dalla nel nella nei sul sulla "
            "come più se poi già anche quando dove chi cosa qui lì".split())
_NLP = None


def nlp():
    """Il parser di misura_sintassi, o None se spaCy manca."""
    global _NLP
    if _NLP is None:
        try:
            import misura_sintassi as ms
            _NLP = ms.carica_nlp() or False
        except Exception:
            _NLP = False
    return _NLP or None


def piano(testo: str) -> str:
    """Il testo da leggere: senza marcatura, con i paragrafi."""
    return re.sub(r"[*_`]", "", testo).strip()


def parole(testo: str) -> "list[str]":
    return [w.lower() for w in _PAROLA.findall(testo)]


def frasi(testo: str) -> "list[str]":
    return [f for f in _FRASE.split(piano(testo).replace("\n", " ")) if _PAROLA.search(f)]


def mattr(testo: str, w: int = 25) -> float:
    t = parole(testo)
    if len(t) <= w:
        return len(set(t)) / max(1, len(t))
    return st.mean(len(set(t[i:i + w])) / w for i in range(len(t) - w + 1))


_SINTASSI: dict = {}


def sintassi(testo: str) -> "tuple[int, int] | None":
    """(livelli_max, frasi) di misura_sintassi, o None senza spaCy."""
    if testo not in _SINTASSI:
        n = nlp()
        if n is None:
            _SINTASSI[testo] = None
        else:
            import misura_sintassi as ms
            a = ms.analizza(piano(testo), n)
            _SINTASSI[testo] = (a["livelli_max"], a["frasi"])
    return _SINTASSI[testo]


def _radici(frase: str) -> "set[str]":
    return {w[:5] for w in parole(frase) if w not in _STOP and len(w) > 3}


def frase_finale_tolta(originale: str, testo: str) -> bool:
    """Regola 3 di §2-ter: l'ultima frase dell'originale (almeno tre parole) non
    c'è più: meno della metà delle sue parole piene torna nel testo nuovo."""
    ultime = [f for f in frasi(originale) if len(parole(f)) >= 3]
    if not ultime:
        return False
    chiusa = _radici(ultime[-1])
    if len(chiusa) < 2:
        return False
    return len(chiusa & _radici(testo)) / len(chiusa) < 0.5


def subordinata_spezzata(originale: str, testo: str) -> bool:
    """Regola 4 di §2-ter: più frasi e meno livelli di subordinate (spaCy), o,
    senza parser, più frasi e meno subordinanti."""
    if len(frasi(testo)) <= len(frasi(originale)):
        return False
    a, b = sintassi(originale), sintassi(testo)
    if a is not None and b is not None:
        return b[0] < a[0]
    return len(_SUBORDINANTI.findall(testo)) < len(_SUBORDINANTI.findall(originale))


def monologo_spezzato(originale: str, testo: str) -> bool:
    """Regola 2 di §2-ter, con lo stesso criterio di cieco_versioni.verdetto_misurato."""
    pezzi = testo.strip().count("\n\n") + 1
    return pezzi >= 3 and "\n\n" not in originale.strip() and "«" in originale


def nomi_tolti(originale: str, testo: str) -> int:
    return len(mc.nomi_propri(piano(originale)) - mc.nomi_propri(piano(testo)))


def tratti(testo: str, originale: "str | None") -> "dict[str, float]":
    """I tratti di una versione. Quelli delle regole si misurano rispetto
    all'originale, e valgono zero se l'originale non c'è o è il testo stesso."""
    p = piano(testo)
    n = max(1, len(parole(p)))
    s = sintassi(testo)
    rel = originale is not None and originale.strip() != testo.strip()
    return {
        "parole_log": math.log(n),
        "gulpease": mc.gulpease(p),
        "sensoriali": float(mc.dettagli_sensoriali(p)),
        "gerundi_mente": float(len(mc.gerundi_in_coda(p)) + len(mc.avverbi_mente(p))),
        "possessivi‰": 1000 * len(_POSS.findall(p)) / n,
        "livelli_max": float(s[0]) if s else 0.0,
        "mattr25": mattr(p),
        "frase_finale_tolta": float(rel and frase_finale_tolta(originale, testo)),
        "subordinata_spezzata": float(rel and subordinata_spezzata(originale, testo)),
        "nomi_tolti": float(nomi_tolti(originale, testo)) if rel else 0.0,
        "monologo_spezzato": float(rel and monologo_spezzato(originale, testo)),
    }


def differenza(a: str, b: str, originale: "str | None") -> "list[float]":
    ta, tb = tratti(a, originale), tratti(b, originale)
    return [ta[k] - tb[k] for k in TRATTI]


# ── il modello: logistica L2 senza intercetta, Newton in libreria standard ──
def _risolvi(A: "list[list[float]]", b: "list[float]") -> "list[float]":
    """Gauss con pivot parziale (le matrici sono 11×11)."""
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        if abs(M[c][c]) < 1e-12:
            continue
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    return [M[i][n] / M[i][i] if abs(M[i][i]) > 1e-12 else 0.0 for i in range(n)]


def _sig(x: float) -> float:
    return 1 / (1 + math.exp(-x)) if x >= 0 else math.exp(x) / (1 + math.exp(x))


def scale(Z: "list[list[float]]") -> "list[float]":
    d = len(Z[0]) if Z else len(TRATTI)
    return [math.sqrt(sum(z[j] ** 2 for z in Z) / len(Z)) or 1.0 if Z else 1.0 for j in range(d)]


def addestra(Z: "list[list[float]]", lam: float = LAMBDA) -> dict:
    """Z: una differenza (vincente − perdente) per coppia. Ogni coppia entra
    nei due versi, quindi il modello è simmetrico e non ha intercetta."""
    s = scale(Z)
    X = [[v / s[j] for j, v in enumerate(z)] for z in Z]
    righe = [(x, 1.0) for x in X] + [([-v for v in x], 0.0) for x in X]
    d = len(s)
    w = [0.0] * d
    for _ in range(50):
        g = [lam * w[j] for j in range(d)]
        H = [[lam if i == j else 0.0 for j in range(d)] for i in range(d)]
        for x, y in righe:
            p = _sig(sum(a * b for a, b in zip(w, x)))
            for i in range(d):
                g[i] += (p - y) * x[i]
                for j in range(d):
                    H[i][j] += p * (1 - p) * x[i] * x[j]
        passo = _risolvi(H, g)
        w = [a - b for a, b in zip(w, passo)]
        if max(abs(v) for v in passo) < 1e-9:
            break
    return {"pesi": w, "scala": s, "tratti": list(TRATTI), "lambda": lam}


def probabilita(modello: dict, z: "list[float]") -> float:
    """P(la prima versione batte la seconda)."""
    return _sig(sum(w * v / s for w, v, s in zip(modello["pesi"], z, modello["scala"])))


def binom_p(k: int, n: int) -> float:
    """p a due code del test del segno contro 0,5."""
    if n == 0:
        return 1.0
    hi = max(k, n - k)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(hi, n + 1)) / 2 ** n)


def valida(voti: "list[dict]") -> dict:
    """Leave-one-out sulle coppie decise, più le due regole di confronto."""
    decise = [v for v in voti if not v["pari"]]
    Z = [differenza(v["vincente"], v["perdente"], v.get("originale")) for v in decise]
    giuste = 0
    for i in range(len(Z)):
        m = addestra(Z[:i] + Z[i + 1:])
        giuste += probabilita(m, Z[i]) > 0.5
    lunga = sum(len(parole(piano(v["vincente"]))) > len(parole(piano(v["perdente"]))) for v in decise)
    pari_lungh = sum(len(parole(piano(v["vincente"]))) == len(parole(piano(v["perdente"]))) for v in decise)
    n = len(Z)
    basso, alto = cv.wilson(giuste, n)
    lb, la = cv.wilson(lunga, n)
    supera = basso > SOGLIA_WILSON and giuste > lunga
    return {"coppie": n, "pari_esclusi": len(voti) - n, "giuste": giuste,
            "accuratezza": giuste / n if n else 0.0, "wilson_95": [round(basso, 3), round(alto, 3)],
            "p_segno": binom_p(giuste, n), "piu_lunga": lunga, "piu_lunga_pari": pari_lungh,
            "piu_lunga_wilson_95": [round(lb, 3), round(la, 3)],
            "supera_soglia": supera, "spacy": nlp() is not None,
            "modello": addestra(Z) if Z else None}


def carica_voti(percorso: Path = VOTI) -> "list[dict]":
    return json.loads(percorso.read_text(encoding="utf-8"))["coppie"] if percorso.exists() else []


def modello_attuale(voti: "list[dict] | None" = None) -> dict:
    voti = carica_voti() if voti is None else voti
    decise = [v for v in voti if not v["pari"]]
    return addestra([differenza(v["vincente"], v["perdente"], v.get("originale")) for v in decise])


def rapporto(r: dict) -> str:
    righe = ["Modello di preferenza sui voti ciechi del DM (migliora_prosa.py modello)", "",
             f"coppie decise: {r['coppie']} (pari esclusi: {r['pari_esclusi']}) · spaCy: "
             + ("sì" if r["spacy"] else "no, livelli_max = 0"),
             f"leave-one-out: {r['giuste']} su {r['coppie']} = {r['accuratezza']:.3f} · "
             f"Wilson 95% {r['wilson_95']} · test del segno p = {r['p_segno']:.3f}",
             f"caso: 0.500 · «vince la più lunga»: {r['piu_lunga']} su {r['coppie']} = "
             f"{r['piu_lunga'] / max(1, r['coppie']):.3f} (pari di lunghezza {r['piu_lunga_pari']}), "
             f"Wilson 95% {r['piu_lunga_wilson_95']}",
             "", "soglia (SOGLIA.txt): Wilson basso > 0.50 e meglio della più lunga → "
             + ("SUPERATA: il modello è misura automatica" if r["supera_soglia"] else
                "NON superata: il modello ordina solo come suggerimento, il giudice resta il cieco"),
             "", "pesi su tutte le coppie (tratti divisi per lo scarto quadratico; + = la versione con più di questo tende a vincere):"]
    m = r["modello"]
    if m:
        for k, w in sorted(zip(m["tratti"], m["pesi"]), key=lambda x: -abs(x[1])):
            righe.append(f"  {k:22} {w:+.3f}")
    righe += ["", "⚠️ Le regole 1-4 di §2-ter vengono da questi stessi voti (giro 2 e riscrittura):",
              "i loro pesi sono letti sui dati che le hanno suggerite, e il leave-one-out non lo corregge."]
    return "\n".join(righe) + "\n"


# ── il dataset ───────────────────────────────────────────────────────────────
def _voci_scheda(testo: str) -> "dict[int, dict[int, tuple[str, str, str]]]":
    """Parte → coppia → (titolo, A, B) da una scheda cieca a più parti."""
    parti: dict = {}
    parte = 1
    for blocco in re.split(r"(?m)^## ", testo)[1:]:
        intest = blocco.split("\n", 1)[0]
        m = re.match(r"Parte (\d+)", intest)
        if m:
            parte = int(m.group(1))
            continue
        m = re.match(r"Coppia (\d+)", intest)
        if not m:
            continue
        titolo = re.search(r"(?m)^\*(.+)\*$", blocco)
        lati = re.split(r"(?m)^\*\*([AB])\*\*\s*$", blocco)
        testi = {lati[i]: lati[i + 1] for i in range(1, len(lati) - 1, 2)}

        def corpo(t):
            righe = [r[1:].strip() if r.startswith(">") else None for r in t.strip().splitlines()]
            out, par = [], []
            for r in righe:
                if r is None:
                    continue
                if r == "":
                    out.append(" ".join(par))
                    par = []
                else:
                    par.append(r)
            out.append(" ".join(par))
            return "\n\n".join(x for x in out if x)
        parti.setdefault(parte, {})[int(m.group(1))] = (
            titolo.group(1) if titolo else "", corpo(testi.get("A", "")), corpo(testi.get("B", "")))
    return parti


def _leggi_voti(testo: str) -> "dict[int, tuple[str, list[str]]]":
    out = {}
    for r in testo.splitlines():
        m = cv._VOTO.match(r)
        if m:
            out[int(m.group(1))] = (m.group(2).upper(), [w.strip(",;.").lower() for w in m.group(3).split() if w])
    return out


def coppie_da_scheda(scheda: str, chiave: dict, voti: str, fonte: str, parte: int,
                     originali: "dict[str, str]", vecchia: str, nuova: str) -> "list[dict]":
    """Le coppie votate di una parte di scheda, con la chiave di cieco_versioni."""
    testi = _voci_scheda(scheda).get(parte, {})
    vv = _leggi_voti(voti)
    out = []
    for c in chiave["coppie"]:
        if c["stato"] == "identica" or c["n"] not in vv or c["n"] not in testi:
            continue
        titolo, a, b = testi[c["n"]]
        voto, etichette = vv[c["n"]]
        t_nuova, t_vecchia = (a, b) if c["nuova"] == "A" else (b, a)
        if voto == "=":
            vinc, perd, rv, rp = t_nuova, t_vecchia, nuova, vecchia
        elif voto == c["nuova"]:
            vinc, perd, rv, rp = t_nuova, t_vecchia, nuova, vecchia
        else:
            vinc, perd, rv, rp = t_vecchia, t_nuova, vecchia, nuova
        bid = titolo.replace("Box ", "")
        out.append({"id": f"{fonte}-{parte}-{c['n']}", "fonte": fonte, "coppia": c["n"],
                    "titolo": titolo, "pari": voto == "=", "vincente": vinc, "perdente": perd,
                    "ruolo_vincente": rv, "ruolo_perdente": rp,
                    "etichette_sulla_perdente": [] if voto == "=" else etichette,
                    "originale": originali.get(bid)})
    return out


def dataset() -> "list[dict]":
    """Tutte le coppie votate alla cieca dal DM che il repo conserva."""
    coppie = []
    for r in json.loads((QUI / "COPPIE-VOTATE.json").read_text(encoding="utf-8")):
        coppie.append({"id": f"{r['set']}-{r['n']}", "fonte": FONTI_38[r["set"]], "coppia": r["n"],
                       "titolo": "", "pari": False, "vincente": r["win"], "perdente": r["lose"],
                       "ruolo_vincente": "nuova" if r["nuova_vince"] else "vecchia",
                       "ruolo_perdente": "vecchia" if r["nuova_vince"] else "nuova",
                       "etichette_sulla_perdente": [],
                       "originale": r["lose"] if r["nuova_vince"] else r["win"]})
    ris = QUI / "riscrittura"
    incr = json.loads((ris / "misure/INCROCIATA.json").read_text(encoding="utf-8"))
    originali = {b["id"]: mc.corpo_del_box(b["versioni"]["O"]["righe"]) for b in incr["box"]}
    scheda = (ris / "cieco/SCHEDA-CIECA.md").read_text(encoding="utf-8")
    for parte, nome, vecchia, nuova in ((1, "V-N", "V (catena vecchia)", "N (catena nuova)"),
                                        (2, "F-O", "O (originale)", "F (fusione)")):
        chiave = json.loads((ris / f"chiave/CHIAVE-{nome}.json").read_text(encoding="utf-8"))
        voti = (ris / f"cieco/VOTI-{parte}.txt").read_text(encoding="utf-8")
        coppie += coppie_da_scheda(scheda, chiave, voti, "riscrittura-2026-10-22", parte,
                                   originali, vecchia, nuova)
    # i voti della pipeline, se ce ne sono, restano
    coppie += [v for v in carica_voti() if v["fonte"].startswith("pipeline")]
    return coppie


def scrivi_voti(coppie: "list[dict]", percorso: Path = VOTI) -> None:
    percorso.parent.mkdir(parents=True, exist_ok=True)
    dati = {"_nota": "Le coppie votate alla cieca dal DM (ADR-0093). «vincente» e «perdente» "
                     "sono i testi; con «pari» vero sono solo le due versioni. «originale» è il "
                     "testo da cui partivano le riscritture, quando si conosce: le regole di "
                     "§2-ter si misurano rispetto a quello. Rigenera: migliora_prosa.py dataset.",
            "coppie": coppie}
    percorso.write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# ── il filtro di non regressione ─────────────────────────────────────────────
def _come_box(testo: str, titolo: str = "Box") -> str:
    righe = [f"## {titolo}", ""]
    for i, par in enumerate(testo.strip().split("\n\n")):
        if i:
            righe.append(">")
        righe.append(f"> *{par.strip()}*")
    return "\n".join(righe) + "\n"


def filtra(originale: str, candidata: str) -> "list[str]":
    """Perché la candidata è scartata: vuoto vuol dire che passa."""
    motivi = [f"fatto cambiato, {x}" for x in cp.confronta_fatti(originale, candidata)]
    motivi += [f"box impoverito, {x}" for x in cp.box_impoveriti(_come_box(originale), _come_box(candidata))]
    d = mc.dettagli_sensoriali(piano(candidata)) - mc.dettagli_sensoriali(piano(originale))
    if d < 0 and not any(m.startswith("box impoverito") for m in motivi):
        motivi.append(f"regola 1, {-d} dettagli sensoriali in meno")
    if monologo_spezzato(originale, candidata):
        motivi.append("regola 2, monologo spezzato in battute")
    if frase_finale_tolta(originale, candidata):
        motivi.append("regola 3, frase finale tolta")
    if subordinata_spezzata(originale, candidata):
        motivi.append("regola 4, subordinata spezzata")
    return motivi


def leggi_candidate(testo: str) -> "list[str]":
    """Le candidate di un file: una per sezione `## …`, in box (`> *…*`) o in chiaro."""
    testo = re.sub(r"<!--.*?-->", "", testo, flags=re.S)
    out = []
    for blocco in re.split(r"(?m)^##\s+.*$", testo)[1:]:
        righe = [r for r in blocco.strip().splitlines()]
        if not any(r.strip() for r in righe):
            continue
        if all(r.startswith(">") or not r.strip() for r in righe):
            pars, cur = [], []
            for r in righe:
                r2 = r.lstrip(">").strip()
                if r2:
                    cur.append(r2)
                elif cur:
                    pars.append(cur)
                    cur = []
            if cur:
                pars.append(cur)
            out.append("\n\n".join(mc.corpo_del_box(["> " + x for x in p]) for p in pars))
        else:
            out.append("\n\n".join(re.sub(r"\s+", " ", p).strip()
                                   for p in "\n".join(righe).strip().split("\n\n")))
    return out


def migliora(originale: str, candidate: "list[str]", modello: dict) -> dict:
    voci = []
    for i, c in enumerate(candidate, 1):
        motivi = filtra(originale, c)
        z = differenza(c, originale, originale)
        voci.append({"n": i, "testo": c, "scartata": motivi,
                     "punteggio": round(probabilita(modello, z), 3)})
    buone = [v for v in voci if not v["scartata"]]
    migliore = max(buone, key=lambda v: (v["punteggio"], -v["n"])) if buone else None
    return {"originale": originale, "candidate": voci,
            "vincitrice": migliore["n"] if migliore else None,
            "punteggio": migliore["punteggio"] if migliore else None}


# ── scegli: i box da migliorare ──────────────────────────────────────────────
def _chiave_testo(t: str) -> str:
    return re.sub(r"\s+", " ", piano(t)).strip()[:120]


def file_arc() -> "list[str]":
    arc08 = sorted(str(p.relative_to(ROOT)) for p in (ROOT / CARTELLA_ARC08).glob("*.md")
                   if not p.name.startswith("ERRATA-"))
    return ARC07 + arc08


def gia_usati() -> "set[str]":
    usati = set()
    if CONGELATI.exists():
        usati |= {_chiave_testo(c["testo"]) for c in json.loads(CONGELATI.read_text(encoding="utf-8"))}
    incr = QUI / "riscrittura/misure/INCROCIATA.json"
    if incr.exists():
        usati |= {_chiave_testo(mc.corpo_del_box(b["versioni"]["O"]["righe"]))
                  for b in json.loads(incr.read_text(encoding="utf-8"))["box"]}
    for v in carica_voti():
        usati |= {_chiave_testo(v["vincente"]), _chiave_testo(v["perdente"])}
    return usati


#: Una nota di regola che `_NOTA_DI_REGOLA` di cieco_versioni non vede: dadi,
#: punti ferita, caratteristiche («25d12+175», «I pf tornano», «For 31»).
_NOTA_DI_REGOLA_IN_PIU = re.compile(r"\d+d\d+|\bpf\b|\b(?:For|Des|Cos|Int|Sag|Car)\s+\d")


def scegli(seme: int, n: int) -> "list[dict]":
    usati = gia_usati()
    cand = []
    for f in file_arc():
        for i, b in enumerate(cv.box_con_titolo((ROOT / f).read_text(encoding="utf-8"))):
            if b["parole"] < cv.PAROLE_MINIME or cv._NOTA_DI_REGOLA.search(b["testo"]) \
                    or _NOTA_DI_REGOLA_IN_PIU.search(b["testo"]):
                continue
            if _chiave_testo(b["testo"]) in usati:
                continue
            cand.append({"file": f, "box": i, "titolo": b["titolo"], "parole": b["parole"],
                         "testo": b["testo"]})
    rng = random.Random(seme)
    return sorted(rng.sample(cand, min(n, len(cand))), key=lambda c: (c["file"], c["box"]))


# ── campione ed esito ────────────────────────────────────────────────────────
TESTA_SCHEDA = [
    "# Scheda cieca — la pipeline migliora_prosa contro l'originale", "",
    "Per ogni coppia leggi ad alta voce **A** e poi **B**, e scrivi una riga nel file dei voti",
    "(`VOTI.txt`): `N A`, `N B` o `N =`. Dopo la lettera, se vuoi, le etichette di ciò che",
    "non andava nella versione scartata (anche più d'una):", ""]


def campione(scelte: dict, seme: int) -> "tuple[str, dict]":
    """La vincitrice di ogni box contro l'originale, con cieco_versioni.coppie.
    Tutte le coppie vanno al DM: la misura non ne decide nessuna."""
    rel = "plans/esperimenti/qualita-misurabile-2026-10-22/pipeline/cieco/_testi-provvisori.md"
    tmp = ROOT / rel
    tmp.parent.mkdir(parents=True, exist_ok=True)
    voci, md = [], ["# testi", ""]
    for s in scelte["box"]:
        if s.get("vincitrice") is None:
            continue
        titolo = f"Box {s['id']}"
        nuovo = next(c["testo"] for c in s["candidate"] if c["n"] == s["vincitrice"])
        voci.append({"file": rel, "indice": len(voci), "titolo": titolo,
                     "testo": s["originale"], "parole": len(s["originale"].split())})
        md += [_come_box(nuovo, titolo)]
    tmp.write_text("\n".join(md) + "\n", encoding="utf-8")
    vecchio = cv.CONTROLLI
    cv.CONTROLLI = 10 ** 6
    try:
        scheda, chiave = cv.coppie({"ref": "", "seme": seme, "per_file": len(voci),
                                    "parole_minime": cv.PAROLE_MINIME, "voci": voci}, "", seme)
    finally:
        cv.CONTROLLI = vecchio
        tmp.unlink()
    chiave["confronto"] = {"vecchia": "originale", "nuova": "vincitrice della pipeline"}
    corpo = [r for r in scheda.splitlines()
             if not r.startswith(("# Confronto cieco", "Leggi ad alta voce", "Se vuoi, dopo la lettera"))]
    corpo = [re.sub(r"^\*_testi-provvisori\.md · (Box \S+)\*$", r"*\1*", r) for r in corpo]
    testa = TESTA_SCHEDA + [f"- `{k}`: {v}" for k, v in cv.ETICHETTE.items()] + [
        "", "Esempio: `3 B goffo ritmo`. Non aprire la cartella `chiave/` prima di aver votato.", ""]
    testo = "\n".join(testa + corpo)
    return re.sub(r"\n{3,}", "\n\n", testo).strip() + "\n", chiave


def registra_esito(scelte: dict, chiave: dict, voti_testo: str, data: str) -> "tuple[dict, list[dict]]":
    r = cv.esito(chiave, voti_testo)
    vv = _leggi_voti(voti_testo)
    per_titolo = {f"Box {s['id']}": s for s in scelte["box"]}
    nuove = []
    for c in chiave["coppie"]:
        if c["stato"] == "identica" or c["n"] not in vv:
            continue
        s = per_titolo[c["titolo"]]
        voto, etichette = vv[c["n"]]
        nuovo = next(x["testo"] for x in s["candidate"] if x["n"] == s["vincitrice"])
        vince_nuova = voto == c["nuova"]
        vinc, perd = (nuovo, s["originale"]) if voto == "=" or vince_nuova else (s["originale"], nuovo)
        nuove.append({"id": f"pipeline-{data}-{chiave['seme']}-{c['n']}",
                      "fonte": f"pipeline-{data}", "coppia": c["n"], "titolo": f"{s['file']} · {s['titolo']}",
                      "pari": voto == "=", "vincente": vinc, "perdente": perd,
                      "ruolo_vincente": "pipeline" if voto == "=" or vince_nuova else "originale",
                      "ruolo_perdente": "originale" if voto == "=" or vince_nuova else "pipeline",
                      "etichette_sulla_perdente": [] if voto == "=" else etichette,
                      "originale": s["originale"]})
    return r, nuove


# ── la riga di comando ───────────────────────────────────────────────────────
def _scrivi_json(percorso: str, dati) -> None:
    p = Path(percorso)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("dataset", help="raccoglie le coppie votate in pipeline/VOTI.json")
    m = sub.add_parser("modello", help="leave-one-out, caso e «vince la più lunga»")
    m.add_argument("--scrivi", action="store_true", help="scrive anche pipeline/MODELLO.txt")
    s = sub.add_parser("scegli", help="sceglie con un seme i box da migliorare")
    s.add_argument("--seme", type=int, required=True)
    s.add_argument("--n", type=int, default=6)
    s.add_argument("--uscita", required=True)
    g = sub.add_parser("migliora", help="filtra e ordina le candidate di un box")
    g.add_argument("file")
    g.add_argument("--box", type=int, help="l'indice del box (senza: li elenca)")
    g.add_argument("--candidate", help="file con una candidata per sezione `## …`")
    g.add_argument("--scelte", help="registra il risultato in questo JSON")
    g.add_argument("--id", help="l'identificativo del box nelle scelte (P01…)")
    c = sub.add_parser("campione", help="scheda cieca: vincitrice contro originale")
    c.add_argument("--scelte", required=True)
    c.add_argument("--seme", type=int, required=True)
    c.add_argument("--scheda", required=True)
    c.add_argument("--chiave", required=True)
    e = sub.add_parser("esito", help="registra i voti, rifà il modello, dice quanto vince la pipeline")
    e.add_argument("--scelte", required=True)
    e.add_argument("--chiave", required=True)
    e.add_argument("--voti", required=True)
    e.add_argument("--data", default=datetime.date.today().isoformat())
    a = ap.parse_args(argv)

    if a.cmd == "dataset":
        coppie = dataset()
        scrivi_voti(coppie)
        per_fonte: dict = {}
        for v in coppie:
            per_fonte[v["fonte"]] = per_fonte.get(v["fonte"], 0) + 1
        print(f"{len(coppie)} coppie in {VOTI.relative_to(ROOT)} "
              f"({sum(v['pari'] for v in coppie)} pari): "
              + ", ".join(f"{k} {n}" for k, n in per_fonte.items()))
    elif a.cmd == "modello":
        testo = rapporto(valida(carica_voti()))
        print(testo, end="")
        if a.scrivi:
            (PIPE / "MODELLO.txt").write_text(testo, encoding="utf-8")
    elif a.cmd == "scegli":
        scelti = scegli(a.seme, a.n)
        _scrivi_json(a.uscita, {"seme": a.seme, "criterio": "box di ARC-07 e ARC-08 con almeno "
                                f"{cv.PAROLE_MINIME} parole, non note di regola (né dadi, pf, caratteristiche), non congelati, non nel "
                                "campione della riscrittura, non già votati", "box": [
                                    {"id": f"P{i:02d}", **b} for i, b in enumerate(scelti, 1)]})
        for i, b in enumerate(scelti, 1):
            print(f"P{i:02d} {b['file']} box {b['box']} ({b['parole']} parole) · {b['titolo'][:50]}")
    elif a.cmd == "migliora":
        testo = Path(a.file).read_text(encoding="utf-8")
        boxes = cv.box_con_titolo(testo)
        if a.box is None:
            for i, b in enumerate(boxes):
                print(f"{i:3} {b['parole']:4} parole · {b['titolo'][:60]}")
            return 0
        if not a.candidate:
            ap.error("migliora --box vuole --candidate")
        originale = boxes[a.box]["testo"]
        candidate = leggi_candidate(Path(a.candidate).read_text(encoding="utf-8"))
        r = migliora(originale, candidate, modello_attuale())
        for v in r["candidate"]:
            stato = "scartata: " + "; ".join(v["scartata"]) if v["scartata"] else "passa"
            print(f"candidata {v['n']} · P(batte l'originale) {v['punteggio']:.3f} · {stato}")
        if r["vincitrice"] is None:
            print("nessuna candidata passa il filtro: resta l'originale")
        else:
            print(f"migliore: candidata {r['vincitrice']} (punteggio {r['punteggio']:.3f})")
            print(next(v["testo"] for v in r["candidate"] if v["n"] == r["vincitrice"]))
        if a.scelte:
            p = Path(a.scelte)
            dati = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"box": []}
            voce = {"id": a.id or f"P{len(dati['box']) + 1:02d}", "file": str(Path(a.file).resolve().relative_to(ROOT))
                    if Path(a.file).resolve().is_relative_to(ROOT) else a.file,
                    "box": a.box, "titolo": boxes[a.box]["titolo"], **r}
            dati["box"] = [b for b in dati["box"] if b["id"] != voce["id"]] + [voce]
            dati["box"].sort(key=lambda b: b["id"])
            _scrivi_json(a.scelte, dati)
    elif a.cmd == "campione":
        scelte = json.loads(Path(a.scelte).read_text(encoding="utf-8"))
        scheda, chiave = campione(scelte, a.seme)
        Path(a.scheda).parent.mkdir(parents=True, exist_ok=True)
        Path(a.scheda).write_text(scheda, encoding="utf-8")
        _scrivi_json(a.chiave, chiave)
        print(f"{len(chiave['coppie'])} coppie in {a.scheda}; chiave in {a.chiave} (fuori dal repo fino al voto)")
    else:
        scelte = json.loads(Path(a.scelte).read_text(encoding="utf-8"))
        chiave = json.loads(Path(a.chiave).read_text(encoding="utf-8"))
        r, nuove = registra_esito(scelte, chiave, Path(a.voti).read_text(encoding="utf-8"), a.data)
        ids = {v["id"] for v in nuove}
        tutte = [v for v in carica_voti() if v["id"] not in ids] + nuove
        scrivi_voti(tutte)
        print(f"{len(nuove)} coppie aggiunte a {VOTI.relative_to(ROOT)} ({len(tutte)} in tutto)")
        print(f"la pipeline vince {r['nuova']} · l'originale {r['vecchia']} · pari {r['pari']} "
              f"su {r['votate']} · Wilson 95% {r['wilson_95']} · soglia di cieco_versioni "
              f"{r['soglia']} su {r['votabili']}")
        print(r["verdetto"].replace("la nuova versione", "la pipeline"))
        print(rapporto(valida(tutte)), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
