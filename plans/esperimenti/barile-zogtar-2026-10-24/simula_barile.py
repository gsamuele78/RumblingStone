#!/usr/bin/env python3
"""Il barile sulla tenda di Zog'tar: simulazione Monte Carlo del round di sorpresa.

Simula lo sgancio del barile da 48 m sulla tenda del comando (M7-C), con le
regole proposte in ARC07-BARILE-SULLA-TENDA.md: tiro di sgancio, deviazione,
tenuta del barile, fiale della fenice che si rompono o no, palle di fuoco da
6d6 (Riflessi CD 14), oggetto in caduta (SRD 3.5) e danno massiccio (SRD 3.5).
Poi il primo round: pozza d'olio in fiamme, chi prende fuoco, il crollo.

Le posizioni sono quelle della disposizione A di M7-C. Le colonne partono da
A = 0 e le righe da 01 = 0; ogni casella è 1,5 m.

Uso:
    python3 simula_barile.py              # tabella completa, 20.000 prove
    python3 simula_barile.py --prove 2000 --seme 7
"""
from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass, field

# ---------------------------------------------------------------- creature


@dataclass
class Creatura:
    nome: str
    caselle: list[tuple[int, int]]
    pf: int
    rifl: int
    temp: int
    rd: int = 0
    dentro: bool = True  # sotto il telo
    pf_ora: int = 0
    morto: bool = False
    in_fiamme: bool = False
    inzuppato: bool = False
    note: list[str] = field(default_factory=list)

    def centro(self) -> tuple[float, float]:
        xs = [c for c, _ in self.caselle]
        ys = [r for _, r in self.caselle]
        return (min(xs) + max(xs) + 1) / 2, (min(ys) + max(ys) + 1) / 2


def c(col: str, riga: int) -> tuple[int, int]:
    """'O', 13 -> (14, 12)."""
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n - 1, riga - 1


def disposizione() -> list[Creatura]:
    """Disposizione A di M7-C (Scena 7): tutti svegli tranne il sacerdote."""
    return [
        Creatura("Zog'tar", [c("O", 13), c("P", 13), c("O", 14), c("P", 14)],
                 pf=283, rifl=9, temp=18, rd=3),
        Creatura("Guardia M13", [c("M", 13)], pf=60, rifl=3, temp=8),
        Creatura("Guardia N13", [c("N", 13)], pf=60, rifl=3, temp=8),
        Creatura("Guardia Q14", [c("Q", 14)], pf=60, rifl=3, temp=8),
        Creatura("Guardia M14", [c("M", 14)], pf=60, rifl=3, temp=8),
        Creatura("Sacerdote", [c("N", 14)], pf=38, rifl=4, temp=4),
        Creatura("Balvar", [c("R", 14)], pf=101, rifl=8, temp=13),
        Creatura("Grask", [c("P", 16)], pf=6, rifl=1, temp=3, dentro=False),
    ]


# Interno della tenda: J10-R14; telo: I9-S15; colmo sulla riga 12, da J a R.
INTERNO = {(x, y) for x in range(9, 18) for y in range(9, 14)}
TELO = {(x, y) for x in range(8, 19) for y in range(8, 15)}
COLMO = {(x, 11) for x in range(9, 18)}
BRACIERI = {c("L", 10), c("K", 14)}

MIRE = {
    "centro": (13.5, 11.5),   # il palo centrale, N12: il punto più alto del telo
    "seggio": (15.0, 13.0),   # l'incrocio al centro del seggio di Zog'tar
}

# ---------------------------------------------------------------- dadi


def d(n: int, f: int, rng: random.Random) -> int:
    return sum(rng.randint(1, f) for _ in range(n))


DIREZIONI = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]


def devia(p: tuple[float, float], caselle: int, rng: random.Random) -> tuple[float, float]:
    dx, dy = rng.choice(DIREZIONI)
    return p[0] + dx * caselle, p[1] + dy * caselle


def casella(p: tuple[float, float]) -> tuple[int, int]:
    return int(math.floor(p[0])), int(math.floor(p[1]))


def distanza_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1]) * 1.5


def nell_area(cr: Creatura, centro: tuple[float, float], raggio_m: float) -> bool:
    """La creatura è nell'area se il centro di una sua casella è nel raggio."""
    return any(distanza_m((x + 0.5, y + 0.5), centro) <= raggio_m for x, y in cr.caselle)


# ---------------------------------------------------------------- una prova


@dataclass
class Parametri:
    mira: str = "centro"
    fiale: int = 2
    bonus_sgancio: int = 15
    cd_sgancio: int = 25
    dadi_caduta: int = 15        # 15d6 sopra i 91 kg, 7d6 sotto (SRD 3.5)
    cd_fiala: int = 14
    massiccio_unico: bool = True  # le fiale rotte all'impatto contano come un'esplosione sola


def prova(par: Parametri, rng: random.Random) -> dict:
    crs = disposizione()
    for cr in crs:
        cr.pf_ora = cr.pf
    esito: dict = {"colmo": False, "fiamme": False, "fuoco_ritardato": False}

    # 1. Sgancio: non è un attacco, quindi l'invisibilità resta (SRD, invisibilità).
    tiro = rng.randint(1, 20) + par.bonus_sgancio
    manca = par.cd_sgancio - tiro
    p = MIRE[par.mira]
    if manca > 0:
        passi = 1 if manca <= 4 else 2 if manca <= 9 else rng.randint(1, 4) + 2
        p = devia(p, passi, rng)
    punto = casella(p)
    esito["punto"] = punto
    centro_impatto = (punto[0] + 0.5, punto[1] + 0.5)

    # 2. Il colpo diretto: una creatura sola, quella nella casella.
    colpito = next((cr for cr in crs if punto in cr.caselle), None)
    danno_per: dict[str, list[int]] = {cr.nome: [] for cr in crs}
    if colpito:
        dn = max(0, d(par.dadi_caduta, 6, rng) - colpito.rd)
        danno_per[colpito.nome].append(dn)
        esito["colpito"] = colpito.nome

    # 3. Il colmo: sulla riga del colmo, 2 su 6 il barile prende la trave.
    if punto in COLMO and rng.randint(1, 6) <= 2:
        esito["colmo"] = True

    # 4. Il barile: 1-16 scoppia, 17-19 si crepa e rotola, 20 regge.
    t = rng.randint(1, 20)
    barile = "scoppia" if t <= 16 else "rotola" if t <= 19 else "intero"
    if barile == "rotola":
        centro_olio = devia(centro_impatto, rng.randint(1, 3), rng)
    else:
        centro_olio = centro_impatto
    esito["barile"] = barile

    # 5. Le fiale: 1-3 intatta (nel fuoco si rompe dopo 1d4 round),
    #    4-6 si rompe a 1d2 caselle, 7-20 si rompe all'impatto.
    scoppi = []
    ritardate = 0
    for _ in range(par.fiale):
        f = rng.randint(1, 20)
        if f <= 3:
            ritardate += 1
        elif f <= 6:
            scoppi.append(devia(centro_impatto, rng.randint(1, 2), rng))
        else:
            scoppi.append(centro_impatto)
    esito["scoppi"] = len(scoppi)

    fuoco_per: dict[str, int] = {cr.nome: 0 for cr in crs}
    for s in scoppi:
        for cr in crs:
            if nell_area(cr, s, 6.0):
                dn = d(6, 6, rng)
                if rng.randint(1, 20) + cr.rifl >= par.cd_fiala:
                    dn //= 2
                fuoco_per[cr.nome] += dn
                if not par.massiccio_unico:
                    danno_per[cr.nome].append(dn)
    if par.massiccio_unico:
        for cr in crs:
            if fuoco_per[cr.nome]:
                danno_per[cr.nome].append(fuoco_per[cr.nome])

    # Senza scoppi, l'olio prende fuoco solo se arriva a un braciere (raggio 2).
    olio_vicino = barile != "intero"
    tocca_braciere = olio_vicino and any(
        distanza_m((bx + 0.5, by + 0.5), centro_olio) <= 3.0 for bx, by in BRACIERI)
    esito["fiamme"] = bool(scoppi) or tocca_braciere
    esito["fuoco_ritardato"] = (not scoppi) and ritardate > 0 and not tocca_braciere

    # 6. Danni del round di sorpresa e danno massiccio (SRD 3.5: 50 da un solo attacco).
    for cr in crs:
        for dn in danno_per[cr.nome]:
            cr.pf_ora -= dn
            if dn >= 50 and cr.pf_ora > -10:
                if rng.randint(1, 20) == 1 or rng.randint(1, 20) + cr.temp < 15:
                    cr.morto = True
                    cr.note.append("danno massiccio")
        if cr.pf_ora <= -10:
            cr.morto = True

    # 7. Primo round: pozza 3x3 attorno al centro dell'olio, corona fino a 2 caselle.
    if esito["fiamme"] and barile != "intero":
        for cr in crs:
            if cr.morto:
                continue
            dist = min(max(abs(x + 0.5 - centro_olio[0]), abs(y + 0.5 - centro_olio[1]))
                       for x, y in cr.caselle)
            if dist <= 1.0:
                cr.inzuppato = True
                cr.in_fiamme = True          # inzuppato: prende fuoco senza TS
                cr.pf_ora -= d(2, 6, rng) + d(1, 6, rng)
            elif dist <= 2.0 and rng.randint(1, 20) + cr.rifl < 15:
                cr.in_fiamme = True
                cr.pf_ora -= d(1, 6, rng)
            if cr.pf_ora <= -10:
                cr.morto = True

    esito["creature"] = {cr.nome: (cr.pf_ora, cr.morto, cr.in_fiamme) for cr in crs}
    return esito


# ---------------------------------------------------------------- tabella


def riassumi(par: Parametri, n: int, seme: int) -> list[str]:
    rng = random.Random(seme)
    nomi = [cr.nome for cr in disposizione()]
    morti = {k: 0 for k in nomi}
    fuori = {k: 0 for k in nomi}  # a 0 pf o meno
    pf_zog = []
    colmo = fiamme = ritardato = 0
    colpiti: dict[str, int] = {}
    for _ in range(n):
        e = prova(par, rng)
        colmo += e["colmo"]
        fiamme += e["fiamme"]
        ritardato += e["fuoco_ritardato"]
        if "colpito" in e:
            colpiti[e["colpito"]] = colpiti.get(e["colpito"], 0) + 1
        for k, (pf, morto, _) in e["creature"].items():
            morti[k] += morto
            fuori[k] += (pf <= 0)
        pf_zog.append(e["creature"]["Zog'tar"][0])
    pf_zog.sort()
    pct = lambda x: f"{100 * x / n:.0f}%"  # noqa: E731
    righe = [
        f"### Mira: {par.mira} · fiale sul barile: {par.fiale} · caduta {par.dadi_caduta}d6",
        "",
        f"- colmo spezzato all'impatto: {pct(colmo)}; fuoco subito: {pct(fiamme)}; "
        f"solo fuoco ritardato (fiala intatta nell'olio): {pct(ritardato)}",
        "- colpo diretto del barile: " + (", ".join(
            f"{k} {pct(v)}" for k, v in sorted(colpiti.items(), key=lambda kv: -kv[1])) or "nessuno"),
        f"- Zog'tar alla fine del round 1: mediana {pf_zog[n // 2]} pf su 283 "
        f"(10° percentile {pf_zog[n // 10]})",
        "",
        "| Chi | a 0 pf o meno | morto |",
        "|---|---:|---:|",
    ]
    for k in nomi:
        righe.append(f"| {k} | {pct(fuori[k])} | {pct(morti[k])} |")
    righe.append("")
    return righe


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--prove", type=int, default=20000)
    ap.add_argument("--seme", type=int, default=24)
    ap.add_argument("--caduta", type=int, default=15, help="dadi dell'oggetto in caduta (15 o 7)")
    ap.add_argument("--regole-srd", action="store_true",
                    help="ogni fiala è un attacco a sé per il danno massiccio (lettura RAW)")
    a = ap.parse_args()
    out = [f"<!-- generato da simula_barile.py --prove {a.prove} --seme {a.seme} "
           f"--caduta {a.caduta}{' --regole-srd' if a.regole_srd else ''} -->", ""]
    for mira in ("centro", "seggio"):
        for fiale in (1, 2, 3):
            par = Parametri(mira=mira, fiale=fiale, dadi_caduta=a.caduta,
                            massiccio_unico=not a.regole_srd)
            out += riassumi(par, a.prove, a.seme)
    print("\n".join(out))


if __name__ == "__main__":
    main()
