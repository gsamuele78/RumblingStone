#!/usr/bin/env python3
"""Il barile sulla tenda di Zog'tar: simulazione Monte Carlo del round di sorpresa.

Simula lo sgancio del barile da 48 m sulla tenda del comando (M7-C), con le
regole di ARC07-BARILE-SULLA-TENDA.md, versione del 2026-10-26 (SRD 3.5 con le
variazioni segnate): niente tiro per colpire, deviazione 1d8 per la direzione
e 1d4−1 quadretti; il barile e le fiale si rompono sempre (prendono anche loro
il danno della caduta); due palle di fuoco da 6d6 (Riflessi CD 14) dall'angolo
della casella d'impatto; oggetto in caduta 15d6 (SRD 3.5); l'olio come arma a
spargimento e come pinta versata (SRD 3.5); danno massiccio (SRD 3.5). Poi la
fine del primo round: l'olio che brucia, chi prende fuoco.

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
    dado_deviazione: int = 4     # 1d4−1 quadretti: chi sgancia sta fermo in aria
    in_volo: bool = False         # chi sgancia si muove: +6 quadretti in avanti (verso est)
    dadi_caduta: int = 15        # 15d6 sopra i 200 libbre, 7d6 sotto (SRD 3.5)
    cd_fiala: int = 14
    massiccio_unico: bool = True  # le fiale contano come un'esplosione sola per i 50 danni
    inzuppato_brucia: bool = True  # chi è nel cuore prende fuoco senza TS (variazione)


RAGGIO_FUOCO = 6.0   # palla di fuoco: 20 piedi
RAGGIO_OLIO = 6.0    # l'olio della botte copre i quadretti entro 6 m dall'origine


def prova(par: Parametri, rng: random.Random) -> dict:
    crs = disposizione()
    for cr in crs:
        cr.pf_ora = cr.pf
    esito: dict = {"colmo": False}

    # 1. Lo sgancio non è un attacco: niente tiro per colpire, l'invisibilità resta.
    #    Deviazione come le armi a spargimento che mancano (SRD): 1d8 la direzione,
    #    e la distanza 1d4−1 quadretti (variazione: 1 quadretto ogni 15 m di caduta).
    p = MIRE[par.mira]
    passi = rng.randint(1, par.dado_deviazione) - 1
    if passi:
        p = devia(p, passi, rng)
    if par.in_volo:
        p = (p[0] + 6, p[1])
    punto = casella(p)
    esito["punto"] = punto
    esito["deviazione"] = passi
    # L'origine delle palle di fuoco è un angolo della casella d'impatto (SRD: le
    # aree partono da un incrocio della griglia).
    origine = (punto[0] + rng.randint(0, 1), punto[1] + rng.randint(0, 1))

    # 2. Il colpo diretto: una creatura sola, quella nella casella. Niente TS.
    colpito = next((cr for cr in crs if punto in cr.caselle), None)
    danno_per: dict[str, list[int]] = {cr.nome: [] for cr in crs}
    if colpito:
        dn = max(0, d(par.dadi_caduta, 6, rng) - colpito.rd)
        danno_per[colpito.nome].append(dn)
        esito["colpito"] = colpito.nome

    # 3. Il colmo: sulla riga del colmo, 2 su 6 il barile prende la trave.
    if punto in COLMO and rng.randint(1, 6) <= 2:
        esito["colmo"] = True

    # 4. Le fiale si rompono tutte all'impatto: una palla di fuoco ciascuna.
    fuoco_per: dict[str, int] = {cr.nome: 0 for cr in crs}
    for _ in range(par.fiale):
        for cr in crs:
            if nell_area(cr, origine, RAGGIO_FUOCO):
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

    # 5. L'olio: chi è nel cuore (la casella d'impatto e le otto attorno) è colpito
    #    in pieno come da un'ampolla d'olio (SRD, fuoco dell'alchimista: 1d6 ora,
    #    1d6 il round dopo); chi è nel resto dell'area prende lo spruzzo, 1 danno.
    cuore = {(punto[0] + i, punto[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1)}
    for cr in crs:
        if any(q in cuore for q in cr.caselle):
            cr.inzuppato = True
            danno_per[cr.nome].append(d(1, 6, rng))
        elif nell_area(cr, origine, RAGGIO_OLIO):
            danno_per[cr.nome].append(1)

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

    # 7. Fine del primo round. La palla di fuoco accende l'olio (SRD: incendia i
    #    combustibili). Chi è nell'olio che brucia prende 1d3 (SRD, la pinta versata)
    #    e tira Riflessi CD 15 per non prendere fuoco (SRD); chi è inzuppato prende
    #    il secondo 1d6 dell'ampolla e, con la variazione, brucia senza TS.
    for cr in crs:
        if cr.morto:
            continue
        nell_olio = cr.inzuppato or nell_area(cr, origine, RAGGIO_OLIO)
        if not nell_olio or not cr.dentro and not cr.inzuppato and rng.random() < 0.5:
            # chi è fuori dal telo e ai margini dell'olio ha già fatto un passo via
            continue
        cr.pf_ora -= d(1, 3, rng)
        if cr.inzuppato:
            cr.pf_ora -= d(1, 6, rng)
        if (cr.inzuppato and par.inzuppato_brucia) or rng.randint(1, 20) + cr.rifl < 15:
            cr.in_fiamme = True
            cr.pf_ora -= d(1, 6, rng)
        if cr.pf_ora <= -10:
            cr.morto = True

    esito["creature"] = {cr.nome: (cr.pf_ora, cr.morto, cr.in_fiamme) for cr in crs}
    return esito


def conta_olio() -> tuple[int, int]:
    """Quadretti coperti dall'olio della botte: il cuore e il resto (origine su un incrocio)."""
    o = (10.0, 10.0)
    area = [(x, y) for x in range(4, 16) for y in range(4, 16)
            if distanza_m((x + 0.5, y + 0.5), o) <= RAGGIO_OLIO]
    return 9, len(area) - 9


# ---------------------------------------------------------------- tabella


def riassumi(par: Parametri, n: int, seme: int) -> list[str]:
    rng = random.Random(seme)
    nomi = [cr.nome for cr in disposizione()]
    morti = {k: 0 for k in nomi}
    fuori = {k: 0 for k in nomi}  # a 0 pf o meno
    pf_zog = []
    colmo = 0
    devs = [0, 0, 0, 0]
    colpiti: dict[str, int] = {}
    for _ in range(n):
        e = prova(par, rng)
        colmo += e["colmo"]
        devs[e["deviazione"]] += 1
        if "colpito" in e:
            colpiti[e["colpito"]] = colpiti.get(e["colpito"], 0) + 1
        for k, (pf, morto, _) in e["creature"].items():
            morti[k] += morto
            fuori[k] += (pf <= 0)
        pf_zog.append(e["creature"]["Zog'tar"][0])
    pf_zog.sort()
    pct = lambda x: f"{100 * x / n:.0f}%"  # noqa: E731
    righe = [
        f"### Mira: {par.mira} · fiale sul barile: {par.fiale} · caduta {par.dadi_caduta}d6"
        + (" · chi sgancia è in volo" if par.in_volo else ""),
        "",
        f"- colmo spezzato all'impatto: {pct(colmo)}; deviazione 0/1/2/3 quadretti: "
        + " / ".join(pct(v) for v in devs),
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
                    help="ogni fiala è un attacco a sé per il danno massiccio, e chi è "
                         "inzuppato tira il TS per non prendere fuoco (lettura RAW)")
    a = ap.parse_args()
    cuore, resto = conta_olio()
    out = [f"<!-- generato da simula_barile.py --prove {a.prove} --seme {a.seme} "
           f"--caduta {a.caduta}{' --regole-srd' if a.regole_srd else ''} -->", "",
           f"L'olio della botte copre {cuore + resto} quadretti: il cuore di {cuore} "
           f"(5 pinte a quadretto) e {resto} attorno (1 pinta a quadretto), "
           f"{cuore * 5 + resto} pinte su 105.", ""]
    for mira in ("centro", "seggio"):
        for fiale in (1, 2, 3):
            par = Parametri(mira=mira, fiale=fiale, dadi_caduta=a.caduta,
                            massiccio_unico=not a.regole_srd, inzuppato_brucia=not a.regole_srd)
            out += riassumi(par, a.prove, a.seme)
    out += riassumi(Parametri(mira="seggio", in_volo=True, dadi_caduta=a.caduta,
                              massiccio_unico=not a.regole_srd,
                              inzuppato_brucia=not a.regole_srd), a.prove, a.seme)
    print("\n".join(out))


if __name__ == "__main__":
    main()
