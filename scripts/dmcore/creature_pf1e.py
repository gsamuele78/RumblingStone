"""dmcore/creature_pf1e.py — una creatura costruita in 3.5, portata in PF1e (ADR-0111).

`genera_creatura.py --sistema pf1e` costruisce come sempre sul bersaglio per
GS, poi passa di qui: i numeri che in Pathfinder 1e cambiano si ricalcolano
dai dati del plugin (`sistemi/pf1e/dati/creature.toml`, estratti dal PRD).

Cosa si ricalcola, e con quale regola del PRD (Creature Statistics by Type,
Size Bonuses and Penalties, Combat Maneuvers):

- dado vita del tipo, e la caratteristica dei pf risolta di nuovo sui pf del
  blocco 3.5 (i non morti usano il Carisma, PRD Undead Traits);
- BAB del tipo, quindi gli attacchi spostati della differenza;
- TS buoni del tipo: buono = 2 + DV/2, scarso = DV/3;
- BMC = BAB + For + taglia; DMC = 10 + BAB + For + Des + taglia;
- gradi di abilità = (gradi del tipo + Int) × DV, almeno 1 per DV.

Cosa no, e si dice nel conto: i pf bonus dei costrutti per taglia (la tabella
non c'è nel PRD in cache), le abilità
fuse di PF1e, i livelli di classe (rifiutati: la conversione vale per i DV
razziali). Gigante ed elementale non sono tipi PF1e: diventano umanoide
(sottotipo gigante) ed esterno (sottotipo elementale).
"""
from __future__ import annotations

import re
from dataclasses import replace

from . import sistemi as S
from .formule import formula
from . import tabelle as T

#: Tipi 3.5 che in PF1e sono sottotipi di un altro tipo (PRD, Creature Types).
DIVENTA = {"giant": "humanoid", "elemental": "outsider"}
ORDINE_TS = ("temp", "rifl", "vol")
NOMI_TS = {"temp": "Temp", "rifl": "Rifl", "vol": "Vol"}
#: Il tetto della caratteristica dei pf, lo stesso di genera_creatura (COS_MAX).
COS_MAX = 6


def _mod(x: int) -> int:
    """Il modificatore di caratteristica: formula `modificatore` del plugin (F3 di ADR-0112)."""
    return formula("modificatore", "pf1e")(punteggio=x)


def _attributi(testo: str) -> dict[str, int]:
    return {k: int(v) for k, v in re.findall(r"(For|Des|Cos|Int|Sag|Car)\s+(\d+)", testo)}


def taglia_inglese(taglia: str, taglie_pf1e: dict) -> str:
    """La taglia come la scrive il PRD (le alias italiane di tabelle.TAGLIE)."""
    t = taglia.lower()
    if t in taglie_pf1e:
        return t
    valore = T.TAGLIE.get(t)
    for nome in taglie_pf1e:
        if T.TAGLIE.get(nome) == valore:
            return nome
    raise ValueError(f"taglia ignota per PF1e: {taglia}")


def ts_buoni(tipo35: str, voce: dict) -> tuple[str, ...]:
    """I TS buoni PF1e. Per umanoide (uno a scelta) ed esterno (due a scelta) la
    scelta è deterministica: prima i TS buoni che il tipo 3.5 aveva, poi
    nell'ordine Temp, Rifl, Vol."""
    if not voce["ts_a_scelta"]:
        return tuple(voce["ts_buoni"])
    prima = [k for k in T.TIPI[tipo35][2] if k in ORDINE_TS]
    resto = [k for k in ORDINE_TS if k not in prima]
    return tuple((prima + resto)[:voce["ts_a_scelta"]])


def converti(sb, tipo: str, taglia: str, root=None):
    """(statblocco PF1e, righe del conto). `sb` è il blocco 3.5 di genera()."""
    dati = S.dati("pf1e", "creature.costruzione", root)
    tipo_pf = DIVENTA.get(tipo, tipo)
    if tipo_pf not in dati["tipi"]:
        raise ValueError(f"tipo {tipo} senza riga PF1e in creature.toml")
    voce = dati["tipi"][tipo_pf]
    tg = taglia_inglese(taglia, dati["taglie"])
    mt = dati["taglie"][tg]["bmc_dmc"]
    car = _attributi(sb.attributi)
    dv = int(sb.pf_dado.split("d")[0])
    conto = [f"PF1e: tipo {tipo_pf}" + (f" (in 3.5 era {tipo}, ora sottotipo)" if tipo_pf != tipo else "")
             + f", d{voce['dv']}, BAB ×{voce['bab']:g}, taglia {tg} (BMC/DMC {mt:+d}) — PRD, "
             "Creature Statistics by Type e Size Bonuses"]

    # pf: dado del tipo, e la caratteristica dei pf risolta di nuovo sui pf del
    # blocco 3.5 (che è già sul bersaglio del GS), come fa genera() con la Cos:
    # cambiare dado senza risolvere spostava il blocco di 70 pf a GS 7.
    # I non morti usano il Carisma, i costrutti non hanno Costituzione.
    media = dv * (voce["dv"] / 2 + 0.5)
    attributi = sb.attributi
    obiettivo = int(sb.pf)
    if tipo_pf == "construct":
        m_pf, chiave_pf = 0, None
        attributi = re.sub(r"Cos\s+\d+", "Cos —", attributi)
        conto.append("⚠ i pf bonus dei costrutti per taglia (PRD, Construct Traits) "
                     "non ci sono: la tabella manca nel PRD in cache, il blocco resta sotto il bersaglio")
    else:
        chiave_pf = "Car" if tipo_pf == "undead" else "Cos"
        m_pf = min(COS_MAX, round((obiettivo - media) / dv))
        car[chiave_pf] = 10 + 2 * m_pf
        attributi = re.sub(chiave_pf + r"\s+\d+", f"{chiave_pf} {car[chiave_pf]}", attributi)
        if tipo_pf == "undead":
            attributi = re.sub(r"Cos\s+\d+", "Cos —", attributi)
    pf = max(1, int(media + m_pf * dv))
    conto.append(f"pf = {dv}d{voce['dv']} ({media:g})"
                 + (f" {m_pf:+d}×{dv} {chiave_pf} {car[chiave_pf]}" if chiave_pf else "")
                 + f" = {pf} (3.5: {sb.pf})"
                 + (f"; {chiave_pf} al tetto +{COS_MAX}, mancano {obiettivo - pf} pf" if chiave_pf and m_pf == COS_MAX and pf < obiettivo else ""))

    # BAB e attacchi.
    bab = int(voce["bab"] * dv)
    bab35 = int(T.TIPI[tipo][1] * dv)
    delta = bab - bab35
    attacchi = list(sb.attacchi)
    if delta:
        attacchi = [re.sub(r"([+-]\d+)", lambda m: f"{int(m.group(1)) + delta:+d}", a, count=1) for a in attacchi]
        conto.append(f"BAB +{bab} (3.5: +{bab35}): attacchi spostati di {delta:+d}"
                     + (" — sopra il bersaglio del GS, è la regola del tipo in PF1e" if delta > 0 else ""))
    else:
        conto.append(f"BAB +{bab}, come in 3.5")

    # TS.
    buoni = ts_buoni(tipo, voce)
    car_ts = {"temp": "Car" if tipo_pf == "undead" else "Cos", "rifl": "Des", "vol": "Sag"}
    ts = {}
    for k in ORDINE_TS:
        base = 2 + dv // 2 if k in buoni else dv // 3
        m = 0 if (k == "temp" and tipo_pf == "construct") else _mod(car.get(car_ts[k], 10))
        ts[k] = base + m
    ts_testo = ", ".join(f"{NOMI_TS[k]} {ts[k]:+d}" for k in ORDINE_TS)
    conto.append(f"TS buoni {', '.join(NOMI_TS[k] for k in buoni) or 'nessuno'} → {ts_testo}")

    # Manovre e abilità.
    m_for, m_des = _mod(car.get("For", 10)), _mod(car.get("Des", 10))
    bmc = bab + m_for + mt
    dmc = 10 + bab + m_for + m_des + mt
    gradi = max(1, voce["gradi"] + _mod(car.get("Int", 10))) * dv
    conto.append(f"BMC = {bab} BAB {m_for:+d} For {mt:+d} taglia = {bmc:+d}; "
                 f"DMC = 10 + {bab} {m_for:+d} {m_des:+d} Des {mt:+d} = {dmc}")
    conto.append(f"gradi di abilità = ({voce['gradi']} + Int) × {dv} DV = {gradi}")

    bonus = pf - int(media)
    nuovo = replace(
        sb,
        tipo=re.sub(r"\d+d\d+([+-]\d+)?", f"{dv}d{voce['dv']}" + (f"{bonus:+d}" if bonus else ""), sb.tipo, count=1)
        .replace(tipo, tipo_pf) if tipo_pf != tipo else
        re.sub(r"\d+d\d+([+-]\d+)?", f"{dv}d{voce['dv']}" + (f"{bonus:+d}" if bonus else ""), sb.tipo, count=1),
        pf=str(pf),
        pf_dado=f"{dv}d{voce['dv']}",
        ts=ts_testo,
        attacchi=attacchi,
        attributi=attributi,
        voci=list(sb.voci) + [f"Manovre: BMC {bmc:+d}, DMC {dmc}", f"Gradi di abilità: {gradi}"],
        fonte=sb.fonte.replace("generato-SRD-3.5", "generato-PRD-PF1e (base 3.5)"),
    )
    return nuovo, conto
