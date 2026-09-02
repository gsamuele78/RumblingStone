"""derive_statblocks.py — la derivazione dalle tabelle, e perché PROPONE e non scrive.

ADR-0033, che emenda ADR-0021.

`extract_statblocks.py` **trascrive**: legge i numeri dalla prosa. Questo script
doveva fare l'altra metà — **derivarli** dalle tabelle, con la gerarchia di fonti
scelta dal DM: **SRD 3.5 prima**, contenuto libero Pathfinder 1e solo dove il SRD
non ha un equivalente.

    dai DV e dal tipo di creatura   →  dado dei DV, BAB, TS buoni e cattivi   [SRD]
    dai livelli di classe           →  TS base per classe, dado dei DV        [SRD]
    dalla matrice elite/standard    →  le caratteristiche (15,14,13,12,10,8)  [SRD]
    dalla taglia                    →  armatura naturale, modificatore di CA  [SRD]
    dall'equipaggiamento nominato   →  bonus d'armatura e scudo               [SRD]
    dal GS                          →  il COLLAUDO                       [PF1e T.1–1]

⚠️ **Non esiste un `--apply`, ed è il risultato del lotto H, non una mancanza.**

Provato: con quelle tabelle e quel collaudo, **nessuna** delle schede rimaste
produce numeri che superino il proprio controllo di sanità. Le schede sono
documenti in prosa, non dati: una espressione regolare ci trova sempre qualcosa
di plausibile, e il modo in cui sbaglia non è rumoroso — è «CA 11 per un mostro
di GS 9», che ha l'aria di un conto e non di un errore. Un numero così entra nel
canone e ci resta fino al tavolo.

Perciò lo strumento **propone**, mostrando il conto per esteso, e la mano che
scrive resta quella del DM. È la stessa disciplina di `import_ultraclear.py` per
le mappe — bozza più rapporto — e la stessa ragione: **una scheda con un numero
dedotto in silenzio è peggio di una scheda non migrata** (ADR-0021 §3).

La tabella per GS di Pathfinder è usata **come guardia, non come fonte**: non
fornisce valori, rifiuta i nostri quando sono assurdi. È il ruolo per cui serve
davvero, ed è anche il motivo per cui non ne prendiamo i numeri: sono tarati su
PF1e, che a parità di GS è più duro del 3.5 su cui questa campagna gira.

Uso:

    python3 scripts/derive_statblocks.py                 # il rapporto
    python3 scripts/derive_statblocks.py --json          # machine-readable
    python3 scripts/derive_statblocks.py <file>...       # solo queste schede

Solo stdlib.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BESTIARIO = ROOT / "Bestiario"
sys.path.insert(0, str(ROOT / "scripts"))
from dmcore.statblock import Statblocco, rendi  # noqa: E402
from dmcore.statblock import estrai  # noqa: E402
from extract_statblocks import APERTURA, e_non_creatura, inserisci, schede  # noqa: E402

# ===========================================================================
# Le tabelle. SRD 3.5 salvo dove dichiarato.
# ===========================================================================

#: SRD, «Table: Creature Improvement by Type» — dado dei DV, BAB, TS buoni.
TIPI = {
    "aberration":         (8,  0.75, ("vol",)),
    "animal":             (8,  0.75, ("temp", "rifl")),
    "construct":          (10, 0.75, ()),
    "dragon":             (12, 1.0,  ("temp", "rifl", "vol")),
    "elemental":          (8,  0.75, ("rifl",)),
    "fey":                (6,  0.5,  ("rifl", "vol")),
    "giant":              (8,  0.75, ("temp",)),
    "humanoid":           (8,  0.75, ("temp",)),
    "magical beast":      (10, 1.0,  ("temp", "rifl")),
    "monstrous humanoid": (8,  1.0,  ("rifl", "vol")),
    "ooze":               (10, 0.75, ()),
    "outsider":           (8,  1.0,  ("temp", "rifl", "vol")),
    "plant":              (8,  0.75, ("temp",)),
    "undead":             (12, 0.5,  ("vol",)),
    "vermin":             (8,  0.75, ("temp",)),
}
#: Come il tipo si scrive nelle schede (italiano e inglese).
ALIAS_TIPO = {
    "aberrazione": "aberration", "animale": "animal", "costrutto": "construct",
    "drago": "dragon", "elementale": "elemental", "folletto": "fey",
    "gigante": "giant", "umanoide": "humanoid", "bestia magica": "magical beast",
    "umanoide mostruoso": "monstrous humanoid", "melma": "ooze",
    "esterno": "outsider", "pianta": "plant", "non-morto": "undead",
    "nonmorto": "undead", "parassita": "vermin", "immondo": "outsider",
    "tiefling": "outsider", "mezzodrago": "dragon",
}

#: SRD — dado dei DV e TS buoni per classe. Le classi PNG (warrior, adept,
#: expert, aristocrat, commoner) stanno nel SRD come le altre.
CLASSI = {
    "barbarian": (12, ("temp",)),   "barbaro":   (12, ("temp",)),
    "bard":      (6,  ("rifl", "vol")), "bardo":  (6,  ("rifl", "vol")),
    "cleric":    (8,  ("temp", "vol")), "chierico": (8, ("temp", "vol")),
    "druid":     (8,  ("temp", "vol")), "druido": (8,  ("temp", "vol")),
    "fighter":   (10, ("temp",)),   "guerriero": (10, ("temp",)),
    "monk":      (8,  ("temp", "rifl", "vol")), "monaco": (8, ("temp", "rifl", "vol")),
    "paladin":   (10, ("temp",)),   "paladino":  (10, ("temp",)),
    "ranger":    (8,  ("temp", "rifl")),
    "rogue":     (6,  ("rifl",)),   "ladro":     (6,  ("rifl",)),
    "sorcerer":  (4,  ("vol",)),    "stregone":  (4,  ("vol",)),
    "wizard":    (4,  ("vol",)),    "mago":      (4,  ("vol",)),
    # classi PNG (SRD)
    "warrior":   (8,  ("temp",)),   "adept":     (6,  ("vol",)),
    "expert":    (6,  ("vol",)),    "aristocrat": (8, ("vol",)),
    "commoner":  (4,  ()),          "esperto":   (6,  ("vol",)),
    "adepto":    (6,  ("vol",)),    "popolano":  (4,  ()),
}

#: SRD — armatura naturale e modificatore di CA per taglia.
TAGLIE = {
    "fine": (0, +8), "diminutive": (0, +4), "tiny": (0, +2), "minuscola": (0, +2),
    "small": (0, +1), "piccola": (0, +1),
    "medium": (0, 0), "media": (0, 0),
    "large": (2, -1), "grande": (2, -1),
    "huge": (5, -2), "enorme": (5, -2),
    "gargantuan": (9, -4), "mastodontica": (9, -4),
    "colossal": (14, -8), "colossale": (14, -8),
}

#: SRD «Table: Armor and Shields» — solo le voci che le schede nominano.
ARMATURE = {
    "full plate": (8, 1), "piastre": (8, 1), "fullplate": (8, 1),
    "half-plate": (7, 0), "mezza piastra": (7, 0),
    "breastplate": (5, 3), "corazza": (5, 3),
    "chainmail": (5, 2), "cotta di maglia": (5, 2), "maglia": (4, 4),
    "chain shirt": (4, 4), "camicia di maglia": (4, 4),
    "scale mail": (4, 3), "scaglie": (4, 3),
    "studded leather": (3, 5), "cuoio borchiato": (3, 5),
    "leather": (2, 6), "cuoio": (2, 6),
    "padded": (1, 8), "imbottita": (1, 8),
}
SCUDI = {"heavy shield": 2, "scudo pesante": 2, "tower": 4, "torre": 4,
         "light shield": 1, "scudo leggero": 1, "buckler": 1, "brocchiere": 1,
         "shield": 2, "scudo": 2}

#: SRD — matrice elite (15,14,13,12,10,8) e standard (13,12,11,10,9,8).
#: PF1e le chiama «heroic» e «basic» e sono gli stessi numeri: una matrice sola
#: per tutti e due i sistemi.
ELITE = (15, 14, 13, 12, 10, 8)
BASIC = (13, 12, 11, 10, 9, 8)
#: I ruoli che meritano la matrice elite: chi ha un nome, chi comanda, chi e' un
#: boss. Il fondale prende quella standard — ed e' il punto: un mook non deve
#: avere le caratteristiche di un luogotenente.
RUOLI_ELITE = ("boss", "elite", "villain", "commander", "captain", "lieutenant",
               "alfa", "leader", "mastermind", "officer", "ally", "caster")

#: PF1e Bestiary Table 1–1 — il collaudo finale. **Qui il SRD 3.5 non ha un
#: equivalente**: non esiste una tabella «statistiche per GS» nel SRD, e questa
#: e' contenuto libero OGL. Serve solo a DIRE se il risultato e' fuori bersaglio,
#: mai a sostituire il conto.
PER_GS = {1: (12, 15), 2: (14, 20), 3: (15, 30), 4: (17, 40), 5: (18, 50),
          6: (19, 65), 7: (20, 85), 8: (21, 100), 9: (23, 115), 10: (24, 130),
          11: (25, 145), 12: (27, 160), 13: (28, 180), 14: (29, 200),
          15: (30, 220), 16: (31, 240), 17: (32, 265), 18: (33, 290),
          19: (34, 320), 20: (35, 350)}


def mod(punteggio: int) -> int:
    return (punteggio - 10) // 2


def ts_buono(dv: int) -> int:
    return 2 + dv // 2


def ts_cattivo(dv: int) -> int:
    return dv // 3


def media_dado(faccia: int) -> float:
    """La media di un dado, come la usa il SRD per i PNG: (faccia/2) + 0,5."""
    return faccia / 2 + 0.5


# ===========================================================================
# Leggere la scheda
# ===========================================================================
_CLASSI_RE = re.compile(r"\b(" + "|".join(sorted(CLASSI, key=len, reverse=True))
                        + r")\s*(\d{1,2})\b", re.I)
_DV_RE = re.compile(r"\b(\d{1,2})\s*d\s*(4|6|8|10|12)\b", re.I)
_GS_RE = re.compile(r"\*\*CR\*\*:\s*(\d{1,2})|\bGS\s*(\d{1,2})\b|-cr(\d{1,2})\b", re.I)
_RUOLO_RE = re.compile(r"\*\*Role\*\*:\s*([^|\n]+)", re.I)


@dataclass
class Lettura:
    """Quello che la scheda dice davvero, senza inventare niente."""
    nome: str
    gs: int | None = None
    dv: int | None = None
    dado: int | None = None
    tipo: str | None = None
    taglia: str = "medium"
    classi: list[tuple[str, int]] = field(default_factory=list)
    armatura: tuple[int, int] | None = None
    scudo: int = 0
    elite: bool = False
    manca: list[str] = field(default_factory=list)


def leggi_scheda(f: Path) -> Lettura:
    t = f.read_text(encoding="utf-8")
    testa = t[:4000]
    L = Lettura(nome=f.stem)

    m = _GS_RE.search(testa) or _GS_RE.search(f.name)
    if m:
        L.gs = int(next(g for g in m.groups() if g))

    ruolo = _RUOLO_RE.search(testa)
    testo_ruolo = (ruolo.group(1) if ruolo else "") + " " + f.stem
    L.elite = any(r in testo_ruolo.lower() for r in RUOLI_ELITE)

    # ⚠️ Deduplicare, e per (classe, livello). «Orco Regular (Warrior 4)» nel
    # titolo e «Warrior 4» nella prosa sono LA STESSA cosa detta due volte: la
    # prima versione contava 8 DV invece di 4, e poi ci sommava i «4d8» della
    # frase dei pf — dodici DV per un orco di GS 3, e 48 pf.
    visti = set()
    for nome, liv in _CLASSI_RE.findall(testa):
        chiave = (nome.lower(), int(liv))
        if chiave not in visti:
            visti.add(chiave)
            L.classi.append(chiave)

    m = _DV_RE.search(testa)
    if m:
        n, d = int(m.group(1)), int(m.group(2))
        # I DV razziali si sommano ai livelli di classe SOLO se non sono gli
        # stessi: «Warrior 4 … 4d8+8» e' un modo di scrivere lo stesso numero.
        if not any(liv == n for _, liv in L.classi):
            L.dv, L.dado = n, d

    basso = testa.lower()
    for alias, tipo in list(ALIAS_TIPO.items()) + [(k, k) for k in TIPI]:
        if alias in basso:
            L.tipo = tipo
            break
    for taglia in TAGLIE:
        if re.search(rf"\b{taglia}\b", basso):
            L.taglia = taglia
            break
    for nome, val in ARMATURE.items():
        if nome in basso:
            L.armatura = val
            break
    for nome, val in SCUDI.items():
        if nome in basso:
            L.scudo = val
            break
    return L


# ===========================================================================
# Derivare
# ===========================================================================
def deriva(L: Lettura) -> tuple[Statblocco | None, list[str], list[str]]:
    """(blocco, conti, cosa manca). Se manca qualcosa, il blocco e' None."""
    manca, conti = [], []
    arr = ELITE if L.elite else BASIC
    matrice = "elite" if L.elite else "standard"

    dv_tot = sum(n for _, n in L.classi)
    if L.dv:
        dv_tot += L.dv
    if not dv_tot:
        manca.append("DV o livelli di classe")
        return None, conti, manca
    # ⚠️ Il tipo o una classe devono essere DETTI. Senza, il dado dei DV e i TS
    # buoni sarebbero una scelta nostra, non una lettura — e da li' in poi ogni
    # numero sarebbe inventato con l'aria di essere calcolato.
    if not L.classi and not L.tipo:
        manca.append("tipo di creatura (senza, dado dei DV e TS buoni sono una scelta)")
        return None, conti, manca

    # --- caratteristiche: la matrice, assegnata per priorita' di ruolo -----
    # Ordine SRD per un combattente: For, Cos, Des, Sag, Car, Int. Non e' un
    # giudizio: e' l'ordine che il SRD usa per i PNG guerrieri, ed e' scritto
    # qui perche' chiunque lo possa rifare uguale.
    forza, cos, des = arr[0], arr[1], arr[2]
    # +1 a una caratteristica ogni 4 DV (SRD)
    bonus = dv_tot // 4
    cos += bonus // 2
    forza += bonus - bonus // 2
    conti.append(f"caratteristiche: matrice {matrice} {arr} + {bonus} da DV/4 "
                 f"→ For {forza}, Cos {cos}, Des {des}")

    # --- pf ---------------------------------------------------------------
    if L.classi:
        pezzi = [(c, n, CLASSI[c][0]) for c, n in L.classi]
        somma = sum(media_dado(d) * n for _, n, d in pezzi)
        det = " + ".join(f"{n}d{d}" for _, n, d in pezzi)
    elif L.dado or L.tipo:
        d = L.dado or TIPI[L.tipo][0]
        somma = media_dado(d) * dv_tot
        det = f"{dv_tot}d{d}"
    else:
        manca.append("pf (né classe né tipo: il dado dei DV è ignoto)")
        return None, conti, manca
    pf = int(somma + mod(cos) * dv_tot)
    conti.append(f"pf: {det} media {somma:.1f} + Cos {mod(cos):+d}×{dv_tot} = {pf}")

    # --- TS ---------------------------------------------------------------
    base = {"temp": 0, "rifl": 0, "vol": 0}
    if L.classi:
        for c, n in L.classi:
            buoni = CLASSI[c][1]
            for k in base:
                base[k] += ts_buono(n) if k in buoni else ts_cattivo(n)
        det_ts = "somma dei TS base di ogni classe (SRD: multiclasse si sommano)"
    else:
        buoni = TIPI[L.tipo][2] if L.tipo else ()
        for k in base:
            base[k] = ts_buono(dv_tot) if k in buoni else ts_cattivo(dv_tot)
        det_ts = f"tipo «{L.tipo}», TS buoni {buoni or '—'}"
    temp = base["temp"] + mod(cos)
    rifl = base["rifl"] + mod(des)
    vol = base["vol"] + mod(arr[3])          # Sag dalla matrice
    conti.append(f"TS: {det_ts} → Temp {temp:+d}, Rifl {rifl:+d}, Vol {vol:+d}")

    # --- CA ---------------------------------------------------------------
    nat, size_mod = TAGLIE[L.taglia]
    pezzi_ca = [f"10", f"taglia {size_mod:+d}", f"Des {mod(des):+d}"]
    ca = 10 + size_mod + mod(des)
    if nat:
        ca += nat
        pezzi_ca.append(f"naturale +{nat} ({L.taglia})")
    if L.armatura:
        bonus_arm, max_des = L.armatura
        # il massimo Des dell'armatura puo' tagliare il bonus
        taglio = min(mod(des), max_des) - mod(des)
        ca += bonus_arm + taglio
        pezzi_ca.append(f"armatura +{bonus_arm}"
                        + (f" (max Des {max_des}: {taglio:+d})" if taglio else ""))
    if L.scudo:
        ca += L.scudo
        pezzi_ca.append(f"scudo +{L.scudo}")
    if not L.armatura and not nat:
        manca.append("ca (nessuna armatura nominata e nessuna armatura naturale "
                     "dalla taglia: il numero sarebbe inventato)")
        return None, conti, manca
    conti.append(f"CA: {' + '.join(pezzi_ca)} = {ca}")

    # --- collaudo sul GS --------------------------------------------------
    # La tabella per GS e' una **guardia**, non una fonte: non fornisce numeri,
    # rifiuta i nostri quando sono assurdi. E' cio' che serve davvero, perche' il
    # modo in cui questa derivazione sbaglia non e' rumoroso — e' «CA 80 per un
    # PNG di GS 8», che ha l'aria di un conto e non di un errore.
    if L.gs in PER_GS:
        ca_att, pf_att = PER_GS[L.gs]
        dca, dpf = ca - ca_att, pf - pf_att
        if abs(dca) > 6 or abs(dpf) > max(15, pf_att * 0.5):
            manca.append(
                f"collaudo fallito: per GS {L.gs} la tabella attende CA {ca_att} e "
                f"pf {pf_att}, il conto dà CA {ca} e pf {pf} ({dca:+d} / {dpf:+d}). "
                f"La lettura della scheda è troppo incerta: serve la mano del DM")
            return None, conti, manca
        conti.append(f"collaudo GS {L.gs} [PF1e Tab. 1–1]: atteso CA {ca_att}, "
                     f"pf {pf_att} → {dca:+d} CA, {dpf:+d} pf, dentro tolleranza")
    else:
        manca.append("GS assente: senza non c'è collaudo, e senza collaudo non si scrive")
        return None, conti, manca
    collaudo = ""

    sb = Statblocco(
        gs=str(L.gs) if L.gs is not None else "",
        ca=str(ca),
        pf=str(pf),
        ts=f"Temp {temp:+d}, Rifl {rifl:+d}, Vol {vol:+d}",
        fonte=("derivato-SRD — " + " · ".join(conti)
               + ("" if not collaudo else collaudo)),
    )
    return sb, conti, manca


# ===========================================================================
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file", nargs="*", type=Path)
    # ⚠️ NON esiste un `--apply`, ed e' il risultato del lotto H, non una
    # mancanza. Provato: con le tabelle SRD, le matrici e il collaudo sul GS,
    # **nessuna** delle 60 schede produce numeri che superino il proprio
    # controllo di sanita'. Il modo in cui questa derivazione sbaglia non e'
    # rumoroso — e' «CA 11 per un mostro di GS 9», che ha l'aria di un conto.
    # Quindi propone, e la mano che scrive resta quella del DM.
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    elenco = [f if f.is_absolute() else ROOT / f for f in a.file] or schede()
    fatti, fermi, saltate = [], {}, 0
    for f in elenco:
        t = f.read_text(encoding="utf-8")
        if APERTURA in t or e_non_creatura(t):
            saltate += 1
            continue
        # ⚠️ Il principio: **la prosa vince sempre.** Si legge prima cosa la
        # scheda dice gia', si deriva solo il buco, e un numero scritto non si
        # tocca mai. Derivare sopra un valore del DM vorrebbe dire sostituire
        # un numero vero con uno calcolato — il danno esatto che ADR-0021 teme.
        letto, _ = estrai(t)
        sb, conti, manca = deriva(leggi_scheda(f))
        rel = str(f.relative_to(ROOT))
        if sb is None:
            fermi[rel] = manca
            continue
        derivati = []
        for campo in ("ca", "pf", "ts", "gs"):
            if getattr(letto, campo):
                setattr(sb, campo, getattr(letto, campo))
            elif getattr(sb, campo):
                derivati.append(campo)
        if not derivati:
            continue                      # non c'era niente da derivare
        for campo in ("tipo", "ca_dettaglio", "velocita", "iniziativa"):
            if getattr(letto, campo):
                setattr(sb, campo, getattr(letto, campo))
        sb.fonte = (f"derivati dalle tabelle: {', '.join(derivati)} "
                    f"(il resto è letto dalla prosa) — " + " · ".join(conti))
        fatti.append((f, sb, conti))

    if a.json:
        print(json.dumps({
            "derivabili": {str(f.relative_to(ROOT)): {"ca": sb.ca, "pf": sb.pf, "ts": sb.ts}
                           for f, sb, _ in fatti},
            "fermi": fermi,
        }, ensure_ascii=False, indent=2))
        return 0

    print(f"  {len(fatti)} proposte che superano il collaudo sul GS "
          f"(questo strumento NON scrive: propone)")
    for f, sb, _ in fatti[:8]:
        print(f"      · {f.name:48} CA {sb.ca}  pf {sb.pf}  {sb.ts}")
    if len(fatti) > 8:
        print(f"      … e altre {len(fatti) - 8}")
    print(f"  {len(fermi)} schede su cui NON si deriva (il numero sarebbe inventato):")
    perche: dict[str, int] = {}
    for m in fermi.values():
        for x in m:
            k = x.split("(")[0].strip()
            perche[k] = perche.get(k, 0) + 1
    for k, n in sorted(perche.items(), key=lambda x: -x[1]):
        print(f"      {n:3}× {k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
