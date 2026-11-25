#!/usr/bin/env python3
"""Misura un prompt d'immagine contro la guida ufficiale di FLUX (ADR-0150).

Il repo scrive i prompt nella scheda di ADR-0015 e li esegue con
`comfyui_batch.py`. Un modello senza riscrittura del prompt (FLUX.2 [klein]
non ne ha: «quello che scrivi è esattamente quello che il modello riceve»)
vuole una **didascalia completa in prosa**, non una lista di etichette. I
servizi come Gemini il prompt corto lo espandono da soli, ed è per questo che
le loro immagini venivano più ricche a parità di testo.

Ogni regola qui sotto viene dalla guida di Black Forest Labs (pagine
«Building a good prompt», «Technical parameters», «Prompt reference»,
lette il 2026-11-25) o da una regola del repo già scritta (ADR-0005,
ADR-0015). Le soglie numeriche sono nostre e lo dicono.

Uso:
    python3 scripts/misura_prompt_immagine.py FILE [FILE ...]
    python3 scripts/misura_prompt_immagine.py FILE --check     # esce 1 se c'è un errore
    python3 scripts/misura_prompt_immagine.py FILE --json

FILE è un markdown con blocchi `<!-- didascalia id=... -->` (le didascalie
per i modelli senza riscrittura) oppure un JSON {id: testo}.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DIDASCALIA = re.compile(
    r"<!--\s*didascalia\s+(?P<campi>[^>]*?)\s*-->\s*\n```\n(?P<corpo>.*?)\n```",
    re.DOTALL,
)
CAMPO = re.compile(r"(\w+)=([^\s]+)")

# Soglie nostre, non della guida: la guida dice «parti da una frase e aggiungi
# dettaglio» e che la struttura conta più della lunghezza. Per un modello senza
# riscrittura la didascalia deve fare il lavoro dell'upsampler (le didascalie
# d'esempio della guida stanno fra 30 e 190 parole); il codificatore di
# FLUX.2 legge al massimo 512 token, circa 380 parole inglesi.
PAROLE_MIN = 60
PAROLE_MAX = 350
FRASI_MIN = 3

# «Image type and medium: one opening sentence that sets the look.»
TIPO_IMMAGINE = re.compile(
    r"\b(portrait|panorama|painting|illustration|view|scene|banner|landscape|"
    r"close-up|interior|still life|study|drawing|engraving|map|cover)\b",
    re.IGNORECASE,
)
# «Describe the light source, direction, and softness.» (FLUX.2 [klein])
LUCE = re.compile(r"\b(light|lit|lighting|sunlight|daylight|torchlight|lantern|candle|glow|torch)\w*\b", re.IGNORECASE)
DIREZIONE = re.compile(
    r"\bfrom (the )?(upper |lower |far )?(left|right|above|below|behind|front)\b"
    r"|\b(low|high) from the (left|right)\b|\bbacklit\b|\brim (of )?light\b",
    re.IGNORECASE,
)
# «Add `Style: [style]. Mood: [mood].` at the end for consistent aesthetics.»
STILE_UMORE = re.compile(r"Style:\s*[^.]+\..*Mood:\s*[^.]+\.?\s*$", re.DOTALL)
# «FLUX has no negative prompt»: «an empty promenade» invece di «no crowds».
NEGAZIONE = re.compile(r"\b(no|without|not|never|avoid|don't|nothing)\b", re.IGNORECASE)
# «omit quality tags such as "masterpiece"»; «highly detailed adds little».
ETICHETTE_QUALITA = re.compile(
    r"\b(masterpiece|best quality|high quality|highly detailed|ultra[- ]?detailed|"
    r"ultra[- ]?realistic|8k|4k|hdr|trending on \w+|award[- ]winning)\b",
    re.IGNORECASE,
)
# ADR-0005: mai il nome di un artista, mai «in the style of».
STILE_DI = re.compile(r"\b[Ii]n the style of\b|\bby (?!the\b)[A-Z][a-z]+")
SEGNAPOSTO = re.compile(r"\[[^\]]+\]")


@dataclass
class Esito:
    ident: str
    parole: int
    frasi: int
    errori: list[str] = field(default_factory=list)
    avvisi: list[str] = field(default_factory=list)


def _frasi(testo: str) -> list[str]:
    return [f for f in re.split(r"(?<=[.;:!?])\s+", testo.strip()) if f]


def _quota_etichette(testo: str) -> float:
    """Quanto del testo è fatto di frammenti corti separati da virgole.

    Una lista di etichette («dust, golden hour, no text») ha quasi tutti i
    pezzi fra le virgole sotto le quattro parole; la prosa no.
    """
    pezzi = [p.strip() for p in re.split(r"[,.;:]", testo) if p.strip()]
    if not pezzi:
        return 0.0
    corti = sum(1 for p in pezzi if len(p.split()) <= 3)
    return corti / len(pezzi)


def misura(ident: str, testo: str) -> Esito:
    testo = " ".join(testo.split())
    parole = len(testo.split())
    frasi = _frasi(testo)
    e = Esito(ident, parole, len(frasi))

    if SEGNAPOSTO.search(testo):
        e.errori.append(f"segnaposto non espanso: {SEGNAPOSTO.search(testo).group(0)}")
    if parole < PAROLE_MIN:
        e.errori.append(f"troppo corta per un modello senza riscrittura: {parole} parole (min {PAROLE_MIN})")
    if parole > PAROLE_MAX:
        e.errori.append(f"oltre il limite del codificatore: {parole} parole (max {PAROLE_MAX})")
    if len(frasi) < FRASI_MIN:
        e.errori.append(f"non è prosa: {len(frasi)} frasi (min {FRASI_MIN})")
    quota = _quota_etichette(testo)
    if quota > 0.5:
        e.errori.append(f"lista di etichette: {quota:.0%} dei frammenti sotto le quattro parole")
    if frasi and not TIPO_IMMAGINE.search(frasi[0]):
        e.errori.append("la prima frase non dice che immagine è (ritratto, veduta, dipinto…)")
    if not LUCE.search(testo):
        e.errori.append("manca la sorgente di luce")
    elif not DIREZIONE.search(testo):
        e.errori.append("la luce non ha una direzione (from the left, from above…)")
    if not STILE_UMORE.search(testo):
        e.errori.append("manca la chiusa «Style: … Mood: …»")
    for m in NEGAZIONE.finditer(testo):
        e.errori.append(f"negazione «{m.group(0)}»: FLUX non ha il prompt negativo, descrivi cosa c'è")
    for m in ETICHETTE_QUALITA.finditer(testo):
        e.errori.append(f"etichetta di qualità «{m.group(0)}»: non descrive niente di visibile")
    if STILE_DI.search(testo):
        e.errori.append(f"nome di un autore o «in the style of» (ADR-0005): «{STILE_DI.search(testo).group(0)}»")
    return e


def leggi(percorso: Path) -> dict[str, str]:
    testo = percorso.read_text(encoding="utf-8")
    if percorso.suffix == ".json":
        dati = json.loads(testo)
        return {k: v for k, v in dati.items() if isinstance(v, str) and not k.startswith("_")}
    fuori = {}
    for m in DIDASCALIA.finditer(testo):
        campi = dict(CAMPO.findall(m.group("campi")))
        if "id" in campi:
            fuori[campi["id"]] = m.group("corpo")
    return fuori


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", nargs="+", type=Path)
    ap.add_argument("--check", action="store_true", help="esce 1 se una didascalia ha un errore")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    esiti: list[tuple[Path, Esito]] = []
    for f in a.file:
        didascalie = leggi(f)
        if not didascalie:
            print(f"{f}: nessuna didascalia trovata", file=sys.stderr)
            if a.check:
                return 1
        esiti += [(f, misura(i, t)) for i, t in didascalie.items()]

    if a.json:
        print(json.dumps([{"file": str(f), **e.__dict__} for f, e in esiti], ensure_ascii=False, indent=2))
    else:
        for f, e in esiti:
            stato = "ok" if not e.errori else f"{len(e.errori)} errori"
            print(f"{f.name} · {e.ident}: {e.parole} parole, {e.frasi} frasi · {stato}")
            for r in e.errori:
                print(f"  ✗ {r}")
        n = sum(1 for _, e in esiti if not e.errori)
        print(f"— {n}/{len(esiti)} didascalie senza errori")
    return 1 if a.check and any(e.errori for _, e in esiti) else 0


if __name__ == "__main__":
    sys.exit(main())
