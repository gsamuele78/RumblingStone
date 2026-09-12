"""
legenda — la legenda dei simboli, letta da una fonte sola (ADR-0048).

Prima di questo modulo la stessa informazione viveva in **cinque** posti:
``SYMBOLS`` in ``render_map_svg.py`` per il rendering, e quattro ``set``
cablati nei consumatori — ``WALL_SYMS``, ``DOOR_SYMS``, ``LIGHT_SYMS`` in
``export_uvtt.py``, ``HAZARD_SYMS`` in ``import_ultraclear.py``.

Al momento della migrazione i cinque **non** erano divergenti in
appartenenza. Il difetto non era un errore presente: era che niente
impediva il prossimo — e il prossimo era già arrivato due volte, ognuna
col suo ADR per rattoppare un sintomo della stessa causa (ADR-0042 sui tre
glifi sotto ``⬛``, ADR-0043 sulle montagne che non erano muri in Foundry).

⚠️ **Perché legge JSON e non YAML.** La fonte scritta a mano è
``scripts/legend.yaml``, che porta i commenti: la memoria di *perché* una
tenda è un muro non sta in un ADR soltanto, sta accanto al dato. Ma
``pyyaml`` è un debito dichiarato (ADR-0037) e non può entrare nel percorso
di rendering, che è ``stdlib_only``. Quindi ``scripts/build_legend.py``
deriva ``scripts/legend.json``, committato e verificato in CI — la forma
che ADR-0048 §2 prescrive, la stessa già in uso per ``docs/tools/``.

Solo stdlib.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

SORGENTE = Path(__file__).resolve().parent.parent / "legend.yaml"
DERIVATO = Path(__file__).resolve().parent.parent / "legend.json"


@lru_cache(maxsize=1)
def _dati() -> dict:
    return json.loads(DERIVATO.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def simboli() -> dict[str, dict]:
    """La tabella di rendering, nella forma storica che i consumatori leggono.

    Le chiavi sono quelle di sempre — ``mode``, ``pat``, ``prop``, ``fill``,
    ``it`` — perché cinque script e sei test le usano: cambiarle sarebbe un
    secondo lotto travestito da primo.
    """
    fuori: dict[str, dict] = {}
    for sim, voce in _dati()["symbols"].items():
        r = voce["render"]
        spec = {"mode": r["mode"]}
        if "pat" in r:
            spec["pat"] = r["pat"]
        if "prop" in r:
            spec["prop"] = r["prop"]
        spec["fill"] = r["fill"]
        spec["it"] = voce.get("label", "")
        fuori[sim] = spec
    return fuori


@lru_cache(maxsize=1)
def pattern_pesanti() -> frozenset[str]:
    """I pattern che ricevono ombra portata e contorno marcato.

    Indicizzati per **pattern** e non per simbolo perché è così che il ciclo
    di pittura del renderer li interroga.
    """
    return frozenset(v["render"]["pat"] for v in _dati()["symbols"].values()
                     if v["render"].get("heavy") and "pat" in v["render"])


def _con(campo: str) -> frozenset[str]:
    return frozenset(s for s, v in _dati()["symbols"].items()
                     if v.get("function", {}).get(campo))


@lru_cache(maxsize=1)
def altezze() -> dict[str, float]:
    """Estrusione 3D in metri per la catena Blender (negativa = scavo).

    ⚠️ Non è ``elevation_m`` di ``LEGENDA-FUNZIONALE-SPEC`` §2, che è la
    **quota del pavimento** della cella. Questa è l'altezza del volume che si
    alza da quel pavimento: la chioma di un albero, la profondità di una
    voragine. Due geometrie diverse, e confonderle sarebbe il difetto che
    ADR-0048 cura.
    """
    return {s: v["render"]["altezza_m"] for s, v in _dati()["symbols"].items()
            if "altezza_m" in v["render"]}


@lru_cache(maxsize=1)
def piatti() -> frozenset[str]:
    """Restano a quota zero: un varco non è un volume."""
    return frozenset(s for s, v in _dati()["symbols"].items()
                     if v["render"].get("piatto"))


@lru_cache(maxsize=1)
def texture() -> dict[str, str]:
    """Cartella di texture per famiglia di superficie.

    Non è uno slug di Poly Haven: è il nome della cartella che il DM riempie
    con l'asset che sceglie, verificando la licenza del singolo file.
    """
    return {s: v["render"]["texture"] for s, v in _dati()["symbols"].items()
            if "texture" in v["render"]}


@lru_cache(maxsize=1)
def muri() -> frozenset[str]:
    """Blocca vista e movimento: diventa segmento di muro nell'export UVTT."""
    return _con("wall")


@lru_cache(maxsize=1)
def porte() -> frozenset[str]:
    return _con("door")


@lru_cache(maxsize=1)
def pericoli() -> frozenset[str]:
    """Classificati come pericolo dall'import, non come struttura."""
    return _con("hazard")


@lru_cache(maxsize=1)
def luci() -> dict[str, tuple[float, str]]:
    """``simbolo -> (raggio in quadretti, colore esadecimale senza cancelletto)``.

    ⚠️ Il raggio è in **quadretti**, non in metri, ed è una divergenza aperta
    con ``LEGENDA-FUNZIONALE-SPEC`` §4.3, che lo dà in metri con quattro
    valori diversi su quattro. Qui vince il codice, perché il criterio
    d'uscita della migrazione era la byte-identità degli artefatti; la scelta
    fra i due è la decisione D1 di ``plans/PIANO-VENDIBILITA.md`` §8.
    """
    fuori = {}
    for sim, voce in _dati()["symbols"].items():
        luce = voce.get("function", {}).get("light")
        if luce:
            fuori[sim] = (float(luce["quadretti"]), luce["colore"])
    return fuori
