#!/usr/bin/env python3
"""
build_texture_cc0.py — le texture CC0 dei terreni per il tema «texture» delle
mappe (R4-bis di PIANO-RESA-E-ASSET-DELLE-MAPPE, D13-D15).

Il tema texture è la seconda resa di ogni mappa, accanto alla pergamena: gli
stessi terreni, gli stessi contorni e gli stessi glifi, ma il riempimento è una
fotografia del materiale (lastricato, terra, roccia, erba) velata del colore
della pergamena, così il colore di un terreno si legge come prima. Le texture
vengono da Poly Haven, CC0 1.0 (pagina «License», letta il 2026-10-09): uso
anche commerciale, ridistribuzione permessa, nessun credito obbligatorio.
Possono stare nel repo e uscirne.

Lo script scarica la diffusa 1k di ogni texture fissata qui sotto, ne
controlla l'MD5 contro quello che dichiara l'API di Poly Haven, la riduce a una
tessera webp di LATO px e la scrive in `scripts/texture-cc0/`, con l'indice
(`indice.json`: fonte, URL, MD5, impronta della tessera). Il renderer resta in
libreria standard: legge solo i webp e l'indice.

    python3 scripts/build_texture_cc0.py                  # scarica e costruisce (rete, Pillow)
    python3 scripts/build_texture_cc0.py --da-cartella D  # costruisce da jpg già scaricati in D
    python3 scripts/build_texture_cc0.py --check          # niente rete: le tessere combaciano con l'indice

`--check` esce 0 anche se le texture non sono ancora state scaricate (lo dice);
esce 1 se una tessera manca o non combacia con l'indice. Exit 2 senza Pillow.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import urllib.request
from pathlib import Path

RADICE = Path(__file__).resolve().parent
USCITA = RADICE / "texture-cc0"
INDICE = USCITA / "indice.json"
API = "https://api.polyhaven.com/files/{id}"
PAGINA = "https://polyhaven.com/a/{id}"
LATO = 256        # px della tessera: copre CELLE_PER_TESSERA quadretti nel renderer
QUALITA = 60      # webp: misurato il 2026-10-09, circa 15 KB in base64 a tessera

#: (chiave, id Poly Haven). La chiave è il simbolo del terreno, oppure
#: «simbolo@ambiente» quando un ambiente di `@tipo` vuole un altro materiale:
#: il muro 🏰 è roccia in caverna e all'aperto, muratura negli interni.
#: Restano vettoriali, per scelta: 🌲 (dall'alto è una chioma, non foglie a
#: terra), l'acqua (🟦 🌊 💧), la lava 🟧, la fogna 🫧, il vuoto 🌫, la zona
#: letale 🟥 e il pilastro 🟪. Poly Haven non ha acqua né lava.
TEXTURE: tuple[tuple[str, str], ...] = (
    ("⬜", "stone_tiles_02"),
    ("🏰", "rock_wall_10"),
    ("🏰@interni", "castle_brick_07"),
    ("🏰@abitato", "castle_brick_07"),
    ("🟫", "dirt_floor"),
    ("⬛", "roof_slates_02"),
    ("🟩", "leafy_grass"),
    ("🌿", "forest_ground_04"),
    ("🟨", "sand_01"),
    ("⛰", "rock_face_03"),
    ("🟤", "rocks_ground_02"),
    ("🔳", "monastery_stone_floor"),
)


#: D27 di RESA-ASSET: ⛰ 🔳 ⬛ si confondevano nel tema texture (ΔE dal vicino
#: 1,5-2,3, misura_resa.py) e la velatura non li separa. Questi candidati CC0
#: di Poly Haven si scaricano con --candidati in asset-esterni/, fuori da git;
#: `misura_resa.py tara --candidati` sceglie quello che separa di più, e solo
#: allora entra in TEXTURE.
CANDIDATI: dict[str, tuple[str, ...]] = {
    "⛰": ("aerial_rocks_02", "lichen_rock", "tiger_rock"),
    "🔳": ("medieval_wood", "plank_flooring", "marble_01"),
    "⬛": ("clay_roof_tiles", "red_slate_roof_tiles_01", "thatch_roof_angled"),
}
CARTELLA_CANDIDATI = RADICE.parent / "asset-esterni" / "texture-candidate"


def _ids() -> list[str]:
    return sorted({i for _, i in TEXTURE})


def _pillow():
    try:
        from PIL import Image
    except ImportError:
        print("✗ build_texture_cc0 ha bisogno di Pillow: pip install -r requirements.txt",
              file=sys.stderr)
        return None
    return Image


def _scarica(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "RumblingStone build_texture_cc0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def _sorgente_rete(tid: str) -> tuple[bytes, dict]:
    files = json.loads(_scarica(API.format(id=tid)))
    voce = files["Diffuse"]["1k"]["jpg"]
    dati = _scarica(voce["url"])
    md5 = hashlib.md5(dati).hexdigest()
    if md5 != voce["md5"]:
        raise ValueError(f"{tid}: MD5 {md5} diverso da quello dell'API ({voce['md5']})")
    return dati, {"url": voce["url"], "md5": md5}


def _sorgente_cartella(cartella: Path, tid: str) -> tuple[bytes, dict]:
    p = cartella / f"{tid}_diff_1k.jpg"
    dati = p.read_bytes()
    return dati, {"url": f"https://dl.polyhaven.org/file/ph-assets/Textures/jpg/1k/{tid}/{p.name}",
                  "md5": hashlib.md5(dati).hexdigest()}


def tessera(Image, dati: bytes) -> bytes:
    """La diffusa ridotta a LATO×LATO, webp. Una texture di Poly Haven si ripete
    senza giunte, e la riduzione intera la lascia ripetibile."""
    im = Image.open(io.BytesIO(dati)).convert("RGB").resize((LATO, LATO), Image.LANCZOS)
    out = io.BytesIO()
    im.save(out, "WEBP", quality=QUALITA, method=6)
    return out.getvalue()


def costruisci(cartella: Path | None) -> int:
    Image = _pillow()
    if Image is None:
        return 2
    USCITA.mkdir(exist_ok=True)
    voci = {}
    for tid in _ids():
        try:
            dati, fonte = (_sorgente_cartella(cartella, tid) if cartella
                           else _sorgente_rete(tid))
        except (OSError, ValueError, KeyError) as e:
            print(f"✗ {tid}: {e}", file=sys.stderr)
            return 1
        webp = tessera(Image, dati)
        (USCITA / f"{tid}.webp").write_bytes(webp)
        voci[tid] = {"fonte": "Poly Haven", "pagina": PAGINA.format(id=tid), **fonte,
                     "licenza": "CC0 1.0", "byte": len(webp),
                     "sha256": hashlib.sha256(webp).hexdigest()}
        print(f"✓ {tid}: {len(webp)} byte")
    indice = {"lato": LATO, "qualita": QUALITA,
              "terreni": {k: i for k, i in TEXTURE}, "texture": voci}
    INDICE.write_text(json.dumps(indice, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


def scarica_candidati(cartella: Path | None) -> int:
    """I candidati di CANDIDATI in tessere, con l'indice, fuori da git: la
    stessa strada delle texture vere (MD5 contro l'API, o --da-cartella)."""
    Image = _pillow()
    if Image is None:
        return 2
    CARTELLA_CANDIDATI.mkdir(parents=True, exist_ok=True)
    voci = {}
    for simbolo, ids in CANDIDATI.items():
        for tid in ids:
            try:
                dati, fonte = (_sorgente_cartella(cartella, tid) if cartella else _sorgente_rete(tid))
            except (OSError, ValueError, KeyError) as e:
                print(f"✗ {tid}: {e}", file=sys.stderr)
                return 1
            webp = tessera(Image, dati)
            (CARTELLA_CANDIDATI / f"{tid}.webp").write_bytes(webp)
            voci[tid] = {"fonte": "Poly Haven", "pagina": PAGINA.format(id=tid), **fonte,
                         "licenza": "CC0 1.0", "per": simbolo, "byte": len(webp),
                         "sha256": hashlib.sha256(webp).hexdigest()}
            print(f"✓ candidato {tid} per {simbolo}: {len(webp)} byte")
    (CARTELLA_CANDIDATI / "indice.json").write_text(json.dumps(
        {"candidati": {k: list(v) for k, v in CANDIDATI.items()}, "texture": voci},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("Poi: python3 scripts/misura_resa.py tara --candidati asset-esterni/texture-candidate")
    return 0


def controlla() -> int:
    if not INDICE.exists():
        print("○ build_texture_cc0: texture non ancora scaricate (scripts/texture-cc0/). "
              "Il tema texture non c'è, la pergamena sì: python3 scripts/build_texture_cc0.py")
        return 0
    indice = json.loads(INDICE.read_text(encoding="utf-8"))
    errori = []
    if indice.get("terreni") != {k: i for k, i in TEXTURE}:
        errori.append("l'indice non elenca i terreni di TEXTURE: rigenera")
    for tid in _ids():
        voce = indice.get("texture", {}).get(tid)
        p = USCITA / f"{tid}.webp"
        if not voce or not p.exists():
            errori.append(f"{tid}: manca la tessera o la sua voce")
        elif hashlib.sha256(p.read_bytes()).hexdigest() != voce["sha256"]:
            errori.append(f"{tid}: la tessera non combacia con l'indice")
        elif voce.get("licenza") != "CC0 1.0":
            errori.append(f"{tid}: licenza «{voce.get('licenza')}», ammessa solo CC0 1.0")
    for e in errori:
        print(f"✗ build_texture_cc0: {e}")
    if not errori:
        print(f"✓ build_texture_cc0: {len(_ids())} texture CC0, "
              f"{sum(v['byte'] for v in indice['texture'].values())} byte")
    return 1 if errori else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="niente rete: le tessere combaciano con l'indice")
    g.add_argument("--da-cartella", type=Path,
                   help="costruisce dai <id>_diff_1k.jpg già scaricati in questa cartella")
    ap.add_argument("--candidati", action="store_true",
                    help="scarica le texture candidate di CANDIDATI in asset-esterni/texture-candidate/ (D27)")
    args = ap.parse_args(argv)
    if args.candidati:
        return scarica_candidati(args.da_cartella)
    return controlla() if args.check else costruisci(args.da_cartella)


if __name__ == "__main__":
    sys.exit(main())
