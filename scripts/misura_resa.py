#!/usr/bin/env python3
"""
misura_resa.py — la resa delle mappe misurata, simbolo per simbolo e terreno
per terreno, prima che una sostituzione entri (R8 di PIANO-RESA-E-ASSET, D23).

Una tessera nuova (un modello CC0 reso, un'immagine generata in locale) prende
il posto di un glifo solo se lo **batte**: si legge meglio sul terreno, non si
confonde con un altro simbolo, sta nello stile del tema, e il DM la preferisce
alla cieca. Questo script fa la parte che si conta. Ogni simbolo è posato su un
banco di prova reso dal renderer vero (`render_map_svg.render_svg`), nei due
temi e su due terreni, rasterizzato con Chrome come fa `export_map_png.py`, e
misurato cella per cella.

Le misure, tutte deterministiche (numpy, scikit-image), con la fonte:

- **contrasto**: rapporto di luminanza fra il decimo più staccato dell'oggetto
  (il contorno, per un glifo) e il terreno intorno, come WCAG 2.1 §1.4.11
  («non-text contrast»: almeno 3:1 per la parte grafica che serve a capire);
  accanto, il contrasto della tinta media;
- **nitidezza del bordo**: gradiente medio della luminanza sul contorno;
- **somiglianza col vicino più prossimo**: SSIM (Wang et al. 2004) fra il
  simbolo e ogni altro, alla risoluzione della cella (28 px); il massimo dice
  con chi si confonde;
- **distanza dalla tavolozza**: ΔE CIEDE2000 medio dei colori dell'oggetto
  dalla tavolozza del set di riferimento (k-means sui glifi della pergamena);
- **inchiostro**: quota del contorno scura (L* < 40), il tratto della casa;
- **colorfulness** di Hasler e Süsstrunk (2003) e **dettaglio** (Sobel medio).

Per i terreni (il tema texture della #227): ΔE fra terreni vicini, visibilità
della griglia, contrasto di un segnalino sul terreno.

Le metriche apprese della community (LPIPS, DISTS, CLIP-IQA di `piq`, Apache-2.0)
vogliono pesi da scaricare: non girano qui né in CI. Si usano sulla macchina del
DM come secondo parere, mai come cancello, perché sono tarate su fotografie e
non su icone da 28 px. Il cancello vero è il confronto a coppie alla cieca del
DM (`coppie`, `voti`), con la misura accanto.

    python3 scripts/misura_resa.py glifi                       # la scheda dei glifi
    python3 scripts/misura_resa.py candidati DIR               # tessere candidate contro i glifi
    python3 scripts/misura_resa.py terreni                     # pergamena contro texture
    python3 scripts/misura_resa.py coppie DIR -o coppie.html   # il confronto alla cieca per il DM
    python3 scripts/misura_resa.py voti voti.json              # registra le preferenze del DM
    python3 scripts/misura_resa.py --aggiorna                  # riscrive la scheda committata
    python3 scripts/misura_resa.py --check                     # la resa non è peggiorata

`--check` ricalcola glifi e terreni e li confronta con `scripts/scheda-resa.json`:
esce 1 se una misura peggiora oltre la tolleranza senza che la scheda sia stata
aggiornata, 0 se tutto regge o se manca un browser (lo dice). Exit 2 senza
numpy o scikit-image.
"""
from __future__ import annotations

import argparse
import html
import json
import random
import subprocess
import sys
import tempfile
from pathlib import Path

RADICE = Path(__file__).resolve().parent
REPO = RADICE.parent
SCHEDA = RADICE / "scheda-resa.json"
sys.path.insert(0, str(RADICE))

import render_map_svg as R  # noqa: E402

SCALA = 3              # px di raster per px di SVG: una cella da 28 diventa 84
TERRENI_BANCO = {"interni": "⬜", "esterno": "🟩"}
TEMI = ("pergamena", "texture")
SOGLIA_WCAG = 3.0      # WCAG 2.1 §1.4.11
TOLLERANZA = 0.05      # relativa, fra due rasterizzazioni di Chrome diverse
COLONNE = 8


def _librerie():
    try:
        import numpy as np
        from skimage import color, filters, metrics
    except ImportError:
        print("✗ misura_resa ha bisogno di numpy e scikit-image: "
              "pip install -r requirements-dev.txt", file=sys.stderr)
        return None
    return np, color, filters, metrics


# --- il banco di prova ----------------------------------------------------------

def _griglia(simboli: list[str], terreno: str, ambiente: str) -> tuple[dict, dict]:
    """Un master con ogni simbolo nella sua cella, un quadretto di terreno
    intorno, e la cella A01 vuota come riferimento del terreno."""
    righe_n = (len(simboli) + COLONNE - 1) // COLONNE
    w, h = COLONNE * 2 + 1, righe_n * 2 + 1
    celle = [[terreno] * w for _ in range(h)]
    pos = {}
    for i, s in enumerate(simboli):
        c, r = 1 + 2 * (i % COLONNE), 1 + 2 * (i // COLONNE)
        celle[r][c] = s
        pos[s] = (c, r)
    pos[""] = (0, 0)
    corpo = ["## BANCO DI PROVA", "", "```",
             "COL →  " + " ".join(R.col_label(i) for i in range(w))]
    corpo += [f"{i:02d}    " + "".join(riga) for i, riga in enumerate(celle, 1)]
    corpo += ["", "@north N", f"@tipo tattica {ambiente}", "```", ""]
    return R.extract_maps("\n".join(corpo))[0], pos


def _browser() -> str | None:
    import export_map_png as E
    try:
        return E.find_browser(None)
    except SystemExit:
        return None


def _raster(svg: str, browser: str, np, trasparente: bool = False):
    """L'SVG in un array RGB (o RGBA con `trasparente`) a SCALA×, con Chrome."""
    from PIL import Image
    import export_map_png as E
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "banco.svg"
        p.write_text(svg, encoding="utf-8")
        w, h = E.svg_size(p)
        out = Path(tmp) / "banco.png"
        cmd = [browser, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
               f"--force-device-scale-factor={SCALA}", f"--screenshot={out}",
               f"--window-size={w},{h}", p.as_uri()]
        if trasparente:
            cmd.insert(1, "--default-background-color=00000000")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not out.exists():
            raise RuntimeError(f"rasterizzazione fallita: {r.stderr.strip()[-300:]}")
        modo = "RGBA" if trasparente else "RGB"
        return np.asarray(Image.open(out).convert(modo), dtype=np.float64) / 255.0


def _solo_figure(svg: str) -> str:
    """Lo stesso SVG con le sole figure degli oggetti (i `<use>` di glifi,
    tessere ed emoji Noto): da qui viene la maschera della figura, che non
    deve contenere il terreno, l'ombra né l'alone."""
    testa = svg[:svg.index(">") + 1]
    defs = svg[svg.index("<defs>"):svg.index("</defs>") + len("</defs>")]
    usi = [riga for riga in svg.split("<use ")[1:]]
    corpo = "".join("<use " + u[:u.index("/>") + 2] for u in usi)
    return testa + defs + corpo + "</svg>"


def _cella(img, c: int, r: int):
    x0 = (R.MARGIN + c * R.CELL) * SCALA
    y0 = (58 + 22 + r * R.CELL) * SCALA
    lato = R.CELL * SCALA
    return img[y0:y0 + lato, x0:x0 + lato]


def banco(simboli: list[str], tema: str, ambiente: str, browser: str, np,
          oggetti: Path | None = None) -> dict:
    """{simbolo: cella RGB}, "" per la cella di solo terreno, e "_fondo" con la
    stessa cella resa senza il simbolo: sul tema texture il terreno cambia da
    una cella all'altra, e solo il gemello allineato dice quali pixel sono
    dell'oggetto."""
    terreno = TERRENI_BANCO[ambiente]
    griglia, pos = _griglia(simboli, terreno, ambiente)
    vuota, _ = _griglia([terreno] * len(simboli), terreno, ambiente)
    vecchio = R.OGGETTI_CC0
    try:
        R.OGGETTI_CC0 = oggetti if oggetti is not None else REPO / "nessuna-tessera"
        svg = R.render_svg(griglia, "banco.md", tema)
        svg_vuoto = R.render_svg(vuota, "banco.md", tema)
    finally:
        R.OGGETTI_CC0 = vecchio
    img, img0 = _raster(svg, browser, np), _raster(svg_vuoto, browser, np)
    fig = _raster(_solo_figure(svg), browser, np, trasparente=True)
    out = {s: _cella(img, c, r) for s, (c, r) in pos.items()}
    out["_fondo"] = {s: _cella(img0, c, r) for s, (c, r) in pos.items()}
    out["_figura"] = {s: _cella(fig, c, r)[..., 3] > 0.5 for s, (c, r) in pos.items()}
    return out


# --- le misure ---------------------------------------------------------------------

def _luminanza(rgb, np):
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    return lin @ np.array([0.2126, 0.7152, 0.0722])


def _maschera(cella, fondo, lib):
    np, color, _, _ = lib
    d = color.deltaE_cie76(color.rgb2lab(cella), color.rgb2lab(fondo))
    return d > 10.0


def misura_cella(cella, fondo, tavolozza, lib, figura=None) -> dict:
    """Le misure di una cella. `figura` è la maschera della figura sola (dal
    render senza terreno, ombra e alone); il suo intorno è la corona di tre
    pixel di cella fuori dalla figura, nell'immagine finale: il contrasto che
    vede l'occhio, alone compreso. Senza `figura` si ripiega sulla differenza
    col gemello, che però include ombra e alone."""
    np, color, filters, _ = lib
    m = figura if figura is not None else _maschera(cella, fondo, lib)
    if m.sum() < 9:
        return {"copertura": 0.0}
    lab = color.rgb2lab(cella)
    L = lab[..., 0]
    bordo = m & ~_erodi(m, np)
    corona = _dilata(m, np, SCALA * 3) & ~m
    lum_o = _luminanza(cella[m], np)
    lf = _luminanza(cella[corona], np).mean() if corona.any() else _luminanza(fondo, np).mean()
    # WCAG 1.4.11 chiede il contrasto della parte che serve a riconoscere
    # l'oggetto: per un glifo è il contorno a inchiostro, non la tinta media.
    # Si prende il decimo più scuro o il più chiaro, quello che si stacca di più.
    rapporti = [(max(v, lf) + 0.05) / (min(v, lf) + 0.05)
                for v in (np.percentile(lum_o, 10), np.percentile(lum_o, 90))]
    lo = lum_o.mean()
    medio = (max(lo, lf) + 0.05) / (min(lo, lf) + 0.05)
    grad = filters.sobel(L / 100.0)
    rgb = cella[m] * 255
    rg, yb = rgb[:, 0] - rgb[:, 1], 0.5 * (rgb[:, 0] + rgb[:, 1]) - rgb[:, 2]
    colorf = (np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean())) / 100.0
    out = {
        "copertura": round(float(m.mean()), 3),
        "contrasto": round(float(max(rapporti)), 2),
        "contrasto_medio": round(float(medio), 2),
        "bordo": round(float(grad[bordo].mean()) if bordo.any() else 0.0, 4),
        "inchiostro": round(float((L[bordo] < 40).mean()) if bordo.any() else 0.0, 3),
        "colorfulness": round(float(colorf), 3),
        "dettaglio": round(float(grad[m].mean()), 4),
    }
    if tavolozza is not None:
        pal = np.asarray(tavolozza, dtype=np.float64)
        pix = lab[m][::4]
        d = np.stack([color.deltaE_ciede2000(pix, np.broadcast_to(p, pix.shape)) for p in pal])
        out["delta_e_tavolozza"] = round(float(d.min(axis=0).mean()), 2)
    return out


def _dilata(m, np, passi: int):
    d = m.copy()
    for _ in range(passi):
        e = d.copy()
        e[1:, :] |= d[:-1, :]
        e[:-1, :] |= d[1:, :]
        e[:, 1:] |= d[:, :-1]
        e[:, :-1] |= d[:, 1:]
        d = e
    return d


def _erodi(m, np):
    e = m.copy()
    e[1:, :] &= m[:-1, :]
    e[:-1, :] &= m[1:, :]
    e[:, 1:] &= m[:, :-1]
    e[:, :-1] &= m[:, 1:]
    return e


def somiglianze(celle: dict, lib) -> dict[str, tuple[str, float]]:
    """Per ogni simbolo, il più simile fra gli altri e l'SSIM, a 28 px in grigio."""
    np, color, _, metrics = lib
    piccole = {}
    for s, c in celle.items():
        if not s or s.startswith("_"):
            continue
        g = color.rgb2gray(c)
        h = g.shape[0] // SCALA
        piccole[s] = g[:h * SCALA, :h * SCALA].reshape(h, SCALA, h, SCALA).mean(axis=(1, 3))
    out = {}
    for s, a in piccole.items():
        migliore = ("", -1.0)
        for t, b in piccole.items():
            if t == s:
                continue
            v = float(metrics.structural_similarity(a, b, data_range=1.0, win_size=7))
            if v > migliore[1]:
                migliore = (t, v)
        out[s] = (migliore[0], round(migliore[1], 3))
    return out


def tavolozza_dei_glifi(celle: dict, lib, k: int = 16) -> list[list[float]]:
    """La tavolozza della casa: k-means in Lab sui pixel degli oggetti della pergamena."""
    np, color, _, _ = lib
    from scipy.cluster.vq import kmeans2
    pix = [color.rgb2lab(c)[celle["_figura"][s]]
           for s, c in celle.items() if s and not s.startswith("_")]
    tutti = np.concatenate(pix)[::3]
    centri, _ = kmeans2(tutti, k, seed=7, minit="++")
    return [[round(float(x), 2) for x in c] for c in centri]


def simboli_oggetto() -> list[str]:
    return [e for e, s in R.SYMBOLS.items() if s.get("prop")]


def _codice(simbolo: str) -> str:
    return "_".join(f"{ord(c):x}" for c in simbolo if ord(c) != 0xFE0F)


def scheda_glifi(browser: str, lib, oggetti: Path | None = None,
                 tavolozza=None, celle_dir: Path | None = None, fonte: str = "glifo") -> dict:
    """{tema: {ambiente: {simbolo: misure}}}, più la tavolozza usata. Con
    `celle_dir` scrive anche ogni cella in PNG, per il livello B
    (`misura_resa_appresa.py`): <tema>-<ambiente>-<codice>-<fonte>.png."""
    simboli = simboli_oggetto()
    out: dict = {}
    for tema in TEMI:
        for amb in TERRENI_BANCO:
            celle = banco(simboli, tema, amb, browser, lib[0], oggetti)
            if celle_dir is not None:
                from PIL import Image
                celle_dir.mkdir(parents=True, exist_ok=True)
                for s in simboli:
                    Image.fromarray((celle[s] * 255).round().astype("uint8")).save(
                        celle_dir / f"{tema}-{amb}-{_codice(s)}-{fonte}.png")
            if tavolozza is None and tema == "pergamena" and amb == "interni":
                tavolozza = tavolozza_dei_glifi(celle, lib)
            vicini = somiglianze(celle, lib)
            righe = {}
            for s in simboli:
                m = misura_cella(celle[s], celle["_fondo"][s], tavolozza, lib, celle["_figura"][s])
                m["vicino"], m["ssim_vicino"] = vicini[s]
                righe[s] = m
            out.setdefault(tema, {})[amb] = righe
    return {"tavolozza": tavolozza, "glifi": out}


def scheda_terreni(browser: str, lib) -> dict:
    """Ogni terreno con una texture CC0, nei due temi: colore medio, ΔE dal
    terreno più vicino, visibilità della griglia, contrasto di un segnalino."""
    np, color, _, _ = lib
    tex = R._texture_cc0()
    if not tex:
        return {}
    terreni = sorted({k.split("@")[0] for k in tex[0]})
    out = {}
    for tema in TEMI:
        medie, righe = {}, {}
        for t in terreni:
            corpo = ["## T", "", "```", "COL →  A B C D E F"]
            corpo += [f"{i:02d}    " + t * 6 for i in range(1, 7)]
            corpo[5] = "03    " + t * 2 + "🔴" + t * 3
            corpo += ["", "@north N", "@tipo tattica interni", "```", ""]
            g = R.extract_maps("\n".join(corpo))[0]
            img = _raster(R.render_svg(g, "t.md", tema), browser, np)
            fondo = _cella(img, 4, 3)
            segn = _cella(img, 2, 2)
            lab = color.rgb2lab(fondo)
            medie[t] = lab.reshape(-1, 3).mean(axis=0)
            # la griglia: la colonna di pixel sulla linea fra C e D, contro il centro delle celle
            x = (R.MARGIN + 4 * R.CELL) * SCALA
            y0, y1 = (80 + 3 * R.CELL) * SCALA, (80 + 5 * R.CELL) * SCALA
            linea = img[y0:y1, x - 1:x + 2]
            dentro = img[y0:y1, x + 8:x + 11]
            ls, ld = _luminanza(linea, np).mean(), _luminanza(dentro, np).mean()
            # il segnalino è un cerchio di raggio 0,37 cella: dentro contro la corona fuori
            lato = segn.shape[0]
            yy, xx = np.mgrid[:lato, :lato]
            rr = np.hypot(yy - lato / 2, xx - lato / 2) / lato
            dentro_s, fuori_s = rr < 0.30, rr > 0.44
            ls_, lf_ = _luminanza(segn[dentro_s], np).mean(), _luminanza(segn[fuori_s], np).mean()
            righe[t] = {
                "griglia": round(float((max(ls, ld) + 0.05) / (min(ls, ld) + 0.05)), 3),
                "segnalino": round(float((max(ls_, lf_) + 0.05) / (min(ls_, lf_) + 0.05)), 2),
                "dettaglio": round(float(np.abs(np.diff(lab[..., 0], axis=1)).mean()), 3),
            }
        for t in terreni:
            altri = [(u, float(color.deltaE_ciede2000(medie[t], medie[u]))) for u in terreni if u != t]
            u, d = min(altri, key=lambda x: x[1])
            righe[t]["vicino"], righe[t]["delta_e_vicino"] = u, round(d, 2)
        out[tema] = righe
    return out


# --- la taratura automatica del tema texture (D24) -----------------------------------

ALONI = (0.0, 0.35, 0.55, 0.65, 0.75, 0.85, 0.95)
VELATURE_PROVA = tuple(round(0.30 + 0.05 * i, 2) for i in range(11))   # 0,30-0,80


def _sintesi_glifi(tema: str, browser: str, lib) -> dict:
    """Mediane di contrasto e bordo, e quanti glifi stanno sotto 3:1, per ambiente."""
    import statistics as st
    sim = simboli_oggetto()
    out = {}
    for amb in TERRENI_BANCO:
        cel = banco(sim, tema, amb, browser, lib[0], REPO / "nessuna-tessera")
        ms = [misura_cella(cel[s], cel["_fondo"][s], None, lib, cel["_figura"][s]) for s in sim]
        out[amb] = {"contrasto": round(st.median(m["contrasto"] for m in ms), 2),
                    "bordo": round(st.median(m["bordo"] for m in ms), 4),
                    "sotto_3": sum(m["contrasto"] < SOGLIA_WCAG for m in ms)}
    return out


def _media_terreno(t: str, tema: str, browser: str, lib):
    np, color, _, _ = lib
    corpo = ["## T", "", "```", "COL →  A B C D E F"]
    corpo += [f"{i:02d}    " + t * 6 for i in range(1, 7)]
    corpo += ["", "@north N", "@tipo tattica interni", "```", ""]
    img = _raster(R.render_svg(R.extract_maps("\n".join(corpo))[0], "t.md", tema), browser, np)
    # due celle accanto: una tessera di texture ne copre due, la media le prende entrambe
    centro = np.concatenate([_cella(img, 2, 2), _cella(img, 3, 2)])
    return color.rgb2lab(centro).reshape(-1, 3).mean(axis=0)


def tara(browser: str, lib) -> dict:
    """Cerca l'alone più leggero che porta i glifi del tema texture almeno al
    livello della pergamena, e la velatura più bassa, terreno per terreno, che
    tiene ogni terreno distinto dal più vicino almeno quanto in pergamena (e mai
    sotto ΔE 5, ben sopra la soglia percettiva di 2,3). Il minimo, non il
    massimo: più alone e più velatura avvicinano il tema texture alla pergamena,
    e la foto è la ragione per cui il tema esiste."""
    np, color, _, _ = lib
    vecchia = {"alone": R._alone, "velatura": R._velatura}
    try:
        # 1. le velature: le medie di colore non dipendono dagli altri terreni
        tex = R._texture_cc0()
        terreni = sorted({k.split("@")[0] for k in tex[0]}) if tex else []
        R._alone = lambda: 0.0
        perg = {t: _media_terreno(t, "pergamena", browser, lib) for t in terreni}

        def de(a, b):
            return float(color.deltaE_ciede2000(a, b))
        bersaglio = {t: max(5.0, min(de(perg[t], perg[u]) for u in terreni if u != t)) for t in terreni}
        medie: dict = {}
        for v in VELATURE_PROVA:
            R._velatura = lambda s, v=v: v
            for t in terreni:
                medie[(t, v)] = _media_terreno(t, "texture", browser, lib)
        scelta = {t: VELATURE_PROVA[0] for t in terreni}
        irrisolte: set = set()

        def vicino(t):
            return min(((u, de(medie[(t, scelta[t])], medie[(u, scelta[u])])) for u in terreni
                        if u != t), key=lambda x: x[1])
        for _ in range(len(terreni) * len(VELATURE_PROVA)):
            difetti = []
            for t in terreni:
                u, d = vicino(t)
                if d < bersaglio[t] - 1e-6 and frozenset((t, u)) not in irrisolte:
                    difetti.append((bersaglio[t] - d, t, u, d))
            if not difetti:
                break
            _, t, u, d = max(difetti)
            # si alza la velatura di uno dei due solo se la distanza cresce davvero:
            # velare una foto senza separarla dal vicino la cancella e basta
            mossa = None
            for chi in sorted((t, u), key=lambda x: scelta[x]):
                i = VELATURE_PROVA.index(scelta[chi])
                if i + 1 == len(VELATURE_PROVA):
                    continue
                prova = dict(scelta)
                prova[chi] = VELATURE_PROVA[i + 1]
                altro = u if chi == t else t
                nuova = de(medie[(chi, prova[chi])], medie[(altro, prova[altro])])
                if nuova > d + 0.3:
                    mossa = (chi, prova[chi])
                    break
            if mossa is None:
                irrisolte.add(frozenset((t, u)))
                continue
            scelta[mossa[0]] = mossa[1]
        per_terreno = {t: v for t, v in scelta.items() if v != R.VELATURA}
        R._velatura = lambda s: per_terreno.get(s, R.VELATURA)
        # 2. l'alone, sopra le velature appena scelte
        rif = _sintesi_glifi("pergamena", browser, lib)
        alone, sintesi = ALONI[-1], None
        for a in ALONI:
            R._alone = lambda a=a: a
            sint = _sintesi_glifi("texture", browser, lib)
            if all(sint[amb]["contrasto"] >= rif[amb]["contrasto"] * (1 - TOLLERANZA / 2)
                   and sint[amb]["bordo"] >= rif[amb]["bordo"] * (1 - TOLLERANZA / 2)
                   and sint[amb]["sotto_3"] <= rif[amb]["sotto_3"] + 1 for amb in rif):
                alone, sintesi = a, sint
                break
            sintesi = sint
        distanze = {t: round(min(de(medie[(t, scelta[t])], medie[(u, scelta[u])]) for u in terreni if u != t), 2)
                    for t in terreni}
        da_cambiare = sorted("".join(sorted(c)) for c in irrisolte)
        return {"alone": alone, "velatura_per_terreno": per_terreno,
                "texture_da_cambiare": da_cambiare,
                "misurato": {"pergamena": rif, "texture": sintesi,
                             "delta_e_vicino": distanze,
                             "bersaglio_delta_e": {t: round(v, 2) for t, v in bersaglio.items()}},
                "scritto_da": "misura_resa.py tara (D24 di RESA-ASSET)"}
    finally:
        R._alone, R._velatura = vecchia["alone"], vecchia["velatura"]


# --- il confronto dei candidati ----------------------------------------------------

def confronta(glifi: dict, candidati: dict) -> dict:
    """Per ogni simbolo con una tessera: le misure nel tema texture, glifo
    contro tessera, e il verdetto del livello A. «Vince» solo dove la misura lo
    dice; «da giudicare» resta al DM, «perde» non entra senza una sua ragione."""
    out = {}
    for amb in TERRENI_BANCO:
        g = glifi["glifi"]["texture"][amb]
        c = candidati["glifi"]["texture"][amb]
        for s in c:
            if c[s] == g.get(s):
                continue
            a, b = g[s], c[s]
            if not b.get("copertura"):
                continue
            ragioni = []
            if b["contrasto"] < SOGLIA_WCAG and b["contrasto"] < a.get("contrasto", 0) * 0.9:
                ragioni.append(f"contrasto {b['contrasto']} sotto 3:1 e sotto il glifo ({a.get('contrasto')})")
            if b["ssim_vicino"] > a["ssim_vicino"] + 0.05:
                ragioni.append(f"si confonde con {b['vicino']} (SSIM {b['ssim_vicino']} contro {a['ssim_vicino']})")
            if b.get("delta_e_tavolozza", 0) > a.get("delta_e_tavolozza", 0) * 1.5 + 2:
                ragioni.append(f"fuori tavolozza (ΔE {b.get('delta_e_tavolozza')} contro {a.get('delta_e_tavolozza')})")
            meglio = (b["contrasto"] >= a.get("contrasto", 0) and b["bordo"] >= a.get("bordo", 0))
            verdetto = "perde" if ragioni else ("vince" if meglio else "da giudicare")
            out.setdefault(s, {})[amb] = {"glifo": a, "tessera": b, "verdetto": verdetto,
                                         "ragioni": ragioni}
    return out


# --- il confronto alla cieca del DM ------------------------------------------------

PAGINA = """<!doctype html><meta charset="utf-8"><title>Confronto alla cieca</title>
<style>body{{font-family:sans-serif;background:#efe4c9;margin:16px}}.c{{display:flex;gap:24px;
align-items:center;margin:18px 0}}img{{width:252px;image-rendering:auto;border:1px solid #3b2e1e;cursor:pointer}}
img.s{{outline:5px solid #2b7a3d}}</style>
<h1>Quale si legge e sta meglio sulla mappa?</h1>
<p>Clicca l'immagine che preferisci in ogni coppia. Non è detto quale sia il glifo.
Alla fine scarica i voti e dalli a <code>misura_resa.py voti</code>.</p>{righe}
<button onclick="salva()">Scarica voti.json</button>
<script>const v={{}};function sc(i,l,el){{v[i]=l;document.querySelectorAll('[data-i="'+i+'"]')
.forEach(e=>e.classList.remove('s'));el.classList.add('s')}}
function salva(){{const b=new Blob([JSON.stringify({{seme:{seme},voti:v}},null,1)],{{type:'application/json'}});
const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='voti.json';a.click()}}</script>"""


def coppie(glifi_celle: dict, cand_celle: dict, seme: int) -> tuple[str, dict]:
    """La pagina con le coppie in ordine e lato casuali (seme scritto), e la chiave."""
    import base64
    import io
    from PIL import Image
    import numpy as np
    rnd = random.Random(seme)
    chiave, righe = {}, []
    voci = [(s, amb) for amb in cand_celle for s in cand_celle[amb]]
    rnd.shuffle(voci)
    for i, (s, amb) in enumerate(voci):
        lati = [("glifo", glifi_celle[amb][s]), ("tessera", cand_celle[amb][s])]
        rnd.shuffle(lati)
        chiave[str(i)] = {"simbolo": s, "ambiente": amb, "sinistra": lati[0][0]}
        imgs = []
        for lato, (nome, cella) in zip(("s", "d"), lati):
            buf = io.BytesIO()
            Image.fromarray((cella * 255).astype(np.uint8)).save(buf, "PNG")
            b64 = base64.b64encode(buf.getvalue()).decode()
            imgs.append(f'<img data-i="{i}" onclick="sc(\'{i}\',\'{lato}\',this)" '
                        f'src="data:image/png;base64,{b64}" alt="">')
        righe.append(f'<div class="c"><b>{i + 1}</b>{"".join(imgs)}</div>')
    return PAGINA.format(righe="".join(righe), seme=seme), chiave


def registra_voti(voti: dict, chiave: dict) -> dict:
    """{simbolo: {ambiente: «glifo» o «tessera»}}: chi ha preferito il DM."""
    out = {}
    for i, lato in voti.get("voti", {}).items():
        k = chiave[i]
        scelto = k["sinistra"] if lato == "s" else ("tessera" if k["sinistra"] == "glifo" else "glifo")
        out.setdefault(k["simbolo"], {})[k["ambiente"]] = scelto
    return out


# --- la scheda committata e il cancello -------------------------------------------

def _peggiora(vecchio: float, nuovo: float, piu_e_meglio: bool) -> bool:
    if piu_e_meglio:
        return nuovo < vecchio * (1 - TOLLERANZA) - 1e-9
    return nuovo > vecchio * (1 + TOLLERANZA) + 1e-9


#: Per ogni misura, se più alto è meglio. ΔE dalla tavolozza: meno è meglio.
VERSO = {"contrasto": True, "bordo": True, "ssim_vicino": False,
         "delta_e_tavolozza": False, "griglia": True, "segnalino": True, "delta_e_vicino": True}


def regressioni(vecchia: dict, nuova: dict) -> list[str]:
    errori = []
    for tema, ambs in vecchia.get("glifi", {}).items():
        for amb, righe in ambs.items():
            for s, m in righe.items():
                n = nuova.get("glifi", {}).get(tema, {}).get(amb, {}).get(s)
                if n is None:
                    errori.append(f"{s} ({tema}, {amb}): manca nella misura nuova")
                    continue
                for k, piu in VERSO.items():
                    if k in m and k in n and _peggiora(m[k], n[k], piu):
                        errori.append(f"{s} ({tema}, {amb}): {k} da {m[k]} a {n[k]}")
    for tema, righe in vecchia.get("terreni", {}).items():
        for t, m in righe.items():
            n = nuova.get("terreni", {}).get(tema, {}).get(t, {})
            for k, piu in VERSO.items():
                if k in m and k in n and _peggiora(m[k], n[k], piu):
                    errori.append(f"terreno {t} ({tema}): {k} da {m[k]} a {n[k]}")
    return errori


def misura_tutto(browser: str, lib) -> dict:
    vecchia = json.loads(SCHEDA.read_text(encoding="utf-8")) if SCHEDA.exists() else {}
    g = scheda_glifi(browser, lib, R.OGGETTI_CC0, vecchia.get("tavolozza"))
    return {"versione": 1, "scala": SCALA, "tavolozza": g["tavolozza"], "glifi": g["glifi"],
            "terreni": scheda_terreni(browser, lib),
            "preferenze_dm": vecchia.get("preferenze_dm", {}),
            "candidati": vecchia.get("candidati", {}),
            **({"livello_b": vecchia["livello_b"]} if "livello_b" in vecchia else {})}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("azione", nargs="?",
                    choices=["glifi", "candidati", "terreni", "coppie", "voti", "appresa", "tara"])
    ap.add_argument("percorso", nargs="?", type=Path,
                    help="candidati e coppie: la cartella con indice.json e i webp; voti: voti.json")
    ap.add_argument("-o", "--uscita", type=Path, help="dove scrivere il JSON o la pagina")
    ap.add_argument("--seme", type=int, default=2026, help="l'ordine delle coppie (coppie)")
    ap.add_argument("--celle", type=Path, help="glifi, candidati: scrive anche le celle in PNG per il livello B")
    ap.add_argument("--registra", action="store_true",
                    help="candidati: scrive i verdetti nella scheda, dove li legge build_oggetti_cc0 --check")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="la resa non è peggiorata rispetto alla scheda")
    g.add_argument("--aggiorna", action="store_true", help="riscrive scripts/scheda-resa.json")
    args = ap.parse_args(argv)
    lib = _librerie()
    if lib is None:
        return 2
    browser = _browser()
    if browser is None:
        print("○ misura_resa: nessun browser per rasterizzare (Chrome o Chromium): "
              "la misura non gira, export_map_png.py dice come installarlo")
        return 0
    if args.check:
        if not SCHEDA.exists():
            print("○ misura_resa: scheda non ancora scritta: python3 scripts/misura_resa.py --aggiorna")
            return 0
        vecchia = json.loads(SCHEDA.read_text(encoding="utf-8"))
        errori = regressioni(vecchia, misura_tutto(browser, lib))
        for e in errori:
            print(f"✗ misura_resa: {e}")
        if not errori:
            n = sum(len(r) for a in vecchia["glifi"].values() for r in a.values())
            print(f"✓ misura_resa: {n} misure di simboli e {sum(len(r) for r in vecchia['terreni'].values())} "
                  f"di terreni, nessuna peggiorata oltre il {int(TOLLERANZA * 100)}%")
        return 1 if errori else 0
    if args.aggiorna:
        scheda = misura_tutto(browser, lib)
        SCHEDA.write_text(json.dumps(scheda, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"✓ scritta {SCHEDA.relative_to(REPO)}")
        return 0
    if args.azione == "glifi":
        out = scheda_glifi(browser, lib, REPO / "nessuna-tessera", celle_dir=args.celle)
    elif args.azione == "terreni":
        out = scheda_terreni(browser, lib)
    elif args.azione in ("candidati", "coppie"):
        if not args.percorso or not (args.percorso / "indice.json").exists():
            print("✗ serve la cartella delle tessere candidate, con indice.json", file=sys.stderr)
            return 2
        base = json.loads(SCHEDA.read_text(encoding="utf-8")).get("tavolozza") if SCHEDA.exists() else None
        if args.azione == "candidati":
            glifi = scheda_glifi(browser, lib, REPO / "nessuna-tessera", base)
            cand = scheda_glifi(browser, lib, args.percorso, glifi["tavolozza"],
                                celle_dir=args.celle, fonte="tessera")
            out = confronta(glifi, cand)
            if args.registra:
                scheda = json.loads(SCHEDA.read_text(encoding="utf-8")) if SCHEDA.exists() else {}
                scheda.setdefault("candidati", {}).update(
                    {s: {a: v["verdetto"] for a, v in amb.items()} for s, amb in out.items()})
                SCHEDA.write_text(json.dumps(scheda, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        else:
            sim = simboli_oggetto()
            gc = {a: banco(sim, "texture", a, browser, lib[0], REPO / "nessuna-tessera") for a in TERRENI_BANCO}
            cc = {a: banco(sim, "texture", a, browser, lib[0], args.percorso) for a in TERRENI_BANCO}
            ind = json.loads((args.percorso / "indice.json").read_text(encoding="utf-8"))
            cand = {a: {s: cc[a][s] for s in ind.get("simboli", {}) if s in cc[a]} for a in cc}
            pagina, chiave = coppie(gc, cand, args.seme)
            dest = args.uscita or Path("coppie.html")
            dest.write_text(pagina, encoding="utf-8")
            dest.with_suffix(".chiave.json").write_text(json.dumps(chiave, ensure_ascii=False, indent=1),
                                                        encoding="utf-8")
            print(f"✓ {dest} ({len(chiave)} coppie) e la chiave in {dest.with_suffix('.chiave.json')}")
            return 0
    elif args.azione == "tara":
        t = tara(browser, lib)
        dest = args.uscita or R.TARATURA
        dest.write_text(json.dumps(t, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"✓ alone {t['alone']}, velature {t['velatura_per_terreno'] or 'tutte ' + str(R.VELATURA)} "
              f"→ {dest}; poi: python3 scripts/dm.py maps texture e misura_resa.py --aggiorna")
        return 0
    elif args.azione == "appresa":
        if not args.percorso:
            print("✗ serve il JSON di misura_resa_appresa.py", file=sys.stderr)
            return 2
        b = json.loads(args.percorso.read_text(encoding="utf-8"))
        scheda = json.loads(SCHEDA.read_text(encoding="utf-8")) if SCHEDA.exists() else {}
        scheda["livello_b"] = b   # secondo parere: --check non lo legge (D26)
        SCHEDA.write_text(json.dumps(scheda, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"✓ {len(b.get('misure', {}))} misure del livello B nella scheda, come secondo parere")
        return 0
    elif args.azione == "voti":
        if not args.percorso:
            print("✗ serve voti.json", file=sys.stderr)
            return 2
        chiave_p = args.percorso.with_name("coppie.chiave.json")
        voti = json.loads(args.percorso.read_text(encoding="utf-8"))
        pref = registra_voti(voti, json.loads(chiave_p.read_text(encoding="utf-8")))
        scheda = json.loads(SCHEDA.read_text(encoding="utf-8")) if SCHEDA.exists() else {}
        scheda.setdefault("preferenze_dm", {}).update(pref)
        SCHEDA.write_text(json.dumps(scheda, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"✓ {len(pref)} simboli con la preferenza del DM in {SCHEDA.relative_to(REPO)}")
        return 0
    else:
        ap.error("indica un'azione, oppure --check o --aggiorna")
    testo = json.dumps(out, ensure_ascii=False, indent=1)
    if args.uscita:
        args.uscita.write_text(testo + "\n", encoding="utf-8")
        print(f"✓ {args.uscita}")
    else:
        print(testo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
