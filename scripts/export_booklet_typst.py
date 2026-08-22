#!/usr/bin/env python3
"""export_booklet_typst.py — l'edizione da stampa: UN volume, segnalibri veri (ADR-0020).

`export_booklet_pdf.py` stampa con Chromium e produce **un PDF per scheda**: va
benissimo per mandare una pagina a un giocatore, ma il browser impagina pagine
web, non libri — niente controllo su vedove e orfane, niente crenatura fine,
niente indice cliccabile degno, e i font restano quelli di sistema.

Questo esportatore affianca quella catena **senza sostituirla**: legge lo stesso
manifest, converte i master markdown in sorgente Typst e produce **un volume
unico** con tipografia embedded (EB Garamond, Cinzel e Inconsolata — OFL, in
`scripts/fonts/`),
due colonne, fregi di capitolo e segnalibri PDF generati dagli heading.

    schermo  →  build_booklet_html.py  →  .html + .hb.md      (invariato)
    stampa   →  export_booklet_typst.py →  un PDF con indice   (questo)

**Le schede pregenerate non sono un capitolo.** Un capitolo di manuale si legge;
una scheda si tiene in mano per tre sessioni. Un capitolo del manifest marcato
`"layout": "schede"` viene quindi impaginato con `typst/scheda-pg.typ`: **una
pagina A4 per personaggio**, fascia alta col ritratto, pannello sinistro con chi
sei, pannello destro con lo statblocco, e in fondo «come si gioca in un minuto».
I dati arrivano dagli stessi master markdown del tavolo (ADR-0003) — nessuna
copia dei numeri da qualche parte, quindi nessuna copia che possa restare
vecchia.

Uso:
    python3 scripts/export_booklet_typst.py MANIFEST.json            # solo pagine ✉ player
    python3 scripts/export_booklet_typst.py MANIFEST.json --all      # tutto, DM incluso
    python3 scripts/export_booklet_typst.py MANIFEST.json --keep-typ # conserva il sorgente .typ
    python3 scripts/export_booklet_typst.py MANIFEST.json --list     # elenca i capitoli
    python3 scripts/export_booklet_typst.py MANIFEST.json --carta bianca  # senza fondo

Dipendenze: stdlib + il binario `typst` (https://github.com/typst/typst,
Apache 2.0). Se manca, lo script **dice come installarlo ed esce pulito**, senza
lasciare file a metà: la catena HTML continua a funzionare da sola.

Rigenera l'esemplare con:
    python3 scripts/export_booklet_typst.py \\
        STANDALONE-Il-Drappo-di-Tarsilia/homebrew/DRAPPO-BOOKLET-DM.manifest.json --all

Exit code: 0 = ok · 1 = binario assente o compilazione fallita · 2 = uso errato.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore.schede import Scheda, SchedaError, leggi_schede  # noqa: E402
from dmcore.statblock import StatblockError, leggi as leggi_statblocco  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMA = ROOT / "scripts" / "typst" / "tema-rumblingstone.typ"
SCHEDA_PG = ROOT / "scripts" / "typst" / "scheda-pg.typ"
FONTS = ROOT / "scripts" / "fonts"

INSTALLA = """\
Il binario «typst» non è nel PATH. È un singolo eseguibile, Apache 2.0:

  Linux/macOS   curl -sSL https://github.com/typst/typst/releases/latest/download/\\
                  typst-x86_64-unknown-linux-musl.tar.xz | tar xJ
                  sudo install typst-*/typst /usr/local/bin/
  Fedora/Bazzite  brew install typst        (oppure il tarball qui sopra)
  Arch            pacman -S typst
  Windows         winget install --id Typst.Typst

Niente panico se non lo installi: `export_booklet_pdf.py` continua a produrre i
PDF per capitolo con Chromium. Questo esportatore serve al volume da stampa.
"""


def typ_path(p: Path) -> str:
    """Con `--root`, in Typst i percorsi assoluti sono RELATIVI ALLA RADICE.

    Passare il percorso del filesystem fa cercare `/home/...` dentro la radice e
    fallisce: è l'errore che si prende chiunque monti Typst la prima volta.
    """
    return "/" + p.resolve().relative_to(ROOT).as_posix()


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-") or "capitolo"


# ── immagini ─────────────────────────────────────────────────────────────────
# Un'immagine larga dentro una colonna da 8 cm non è un'immagine: è un
# francobollo. La regola è la stessa delle tabelle larghe — se è orizzontale
# scavalca le due colonne — e per applicarla serve sapere quanto è larga
# davvero. Si legge dall'intestazione del file, senza dipendenze.

def dimensioni(f: Path) -> tuple[int, int] | None:
    """(larghezza, altezza) in pixel per PNG/JPEG, in unità utente per SVG."""
    try:
        testa = f.read_bytes()[:4096]
    except OSError:
        return None
    if testa[:8] == b"\x89PNG\r\n\x1a\n" and testa[12:16] == b"IHDR":
        return int.from_bytes(testa[16:20], "big"), int.from_bytes(testa[20:24], "big")
    if testa[:2] == b"\xff\xd8":
        dati = f.read_bytes()
        i = 2
        while i < len(dati) - 9:
            if dati[i] != 0xFF:
                i += 1
                continue
            marcatore = dati[i + 1]
            if 0xC0 <= marcatore <= 0xCF and marcatore not in (0xC4, 0xC8, 0xCC):
                return (int.from_bytes(dati[i + 7:i + 9], "big"),
                        int.from_bytes(dati[i + 5:i + 7], "big"))
            i += 2 + int.from_bytes(dati[i + 2:i + 4], "big")
        return None
    if b"<svg" in testa:
        vb = re.search(rb'viewBox\s*=\s*"([-\d.\s]+)"', testa)
        if vb:
            n = vb.group(1).split()
            if len(n) == 4:
                return int(float(n[2])), int(float(n[3]))
        w = re.search(rb'width\s*=\s*"(\d+)', testa)
        h = re.search(rb'height\s*=\s*"(\d+)', testa)
        if w and h:
            return int(w.group(1)), int(h.group(1))
    return None


def figura(alt: str, src: str, base: Path) -> str:
    """`![alt](src)` → `#figura(...)`, con l'avviso se il file non c'è.

    Prima di questa funzione la sintassi cadeva nella regola dei link e
    l'immagine finiva stampata come **il testo dell'alt preceduto da `!`**:
    nel booklet del Palio erano tredici righe («!Stemma Oca», «!Piazza del
    Palio»…). Un buco silenzioso in un volume da stampa è peggio di un errore.
    """
    if re.match(r"^[a-z]+://", src):
        print(f"  ⚠ immagine remota ignorata (serve un file nel repo): {src}", file=sys.stderr)
        return ""
    f = (base / src).resolve()
    if not f.is_file():
        print(f"  ⚠ immagine mancante: {src}", file=sys.stderr)
        return ("#block(width: 100%, inset: 8pt, stroke: (dash: \"dashed\", paint: rgb(\"#b9a789\")))"
                f"[#align(center)[#text(size: 8pt, fill: rgb(\"#7d2b1f\"))[immagine mancante: {inline(src)}]]]")
    try:
        dentro = typ_path(f)
    except ValueError:
        # Con `--root`, Typst vede SOLO ciò che sta sotto la radice: un master
        # che punta fuori dal repo non è un caso da gestire, è un master da
        # correggere.
        print(f"  ⚠ immagine fuori dalla radice del repo, non stampabile: {src}", file=sys.stderr)
        return ""
    d = dimensioni(f)
    larga = bool(d) and d[0] >= d[1] * 1.25
    voci = [json.dumps(dentro, ensure_ascii=False)]
    if alt.strip():
        voci.append(f"didascalia: [{inline(alt)}]")
        voci.append(f"alt: {json.dumps(alt, ensure_ascii=False)}")
    if larga:
        voci.append("larga: true")
    return "#figura(" + ", ".join(voci) + ")"


# ── markdown → Typst ─────────────────────────────────────────────────────────
# Copre il sottoinsieme che i master del repo usano davvero. Ogni caso in più va
# aggiunto QUI e non nel .typ generato, che è un artefatto.

# `~` in Typst è uno spazio unificatore e `[` `]` delimitano il contenuto: se non
# si scappano, `+ ~200 mo` si stampa «+  200 mo» — il numero resta, la tilde
# sparisce, e nessuno se ne accorge finché non lo legge un giocatore.
_SPECIALI = ("\\", "#", "$", "@", "<", ">", "*", "_", "`", "[", "]", "~")


def _esc(s: str) -> str:
    for ch in _SPECIALI:
        s = s.replace(ch, f"\x00{ord(ch)}\x00")
    return s


def _unesc(s: str) -> str:
    return re.sub(r"\x00(\d+)\x00", lambda m: "\\" + chr(int(m.group(1))), s)


# L'enfasi non si fa con una regex: si fa con una pila.
#
# Due difetti veri, tutti e due trovati compilando i booklet della campagna:
#
#   * `**Seggio**/Deputazione` — grassetto attaccato a una barra — usciva come
#     `*Seggio*/Deputazione` e Typst rispondeva «unclosed delimiter»: la
#     chiusura abbreviata dipende dal carattere che segue. Perciò l'enfasi
#     esce come `#strong[...]` / `#emph[...]`, che non ha delimitatori da
#     indovinare;
#   * `*testo **(nota.)***` — corsivo che contiene un grassetto e chiude tutto
#     insieme — la regex lo spezzava lasciando un asterisco orfano DENTRO il
#     grassetto, e l'errore usciva trecento righe più in basso.
#
# La pila regge la nidificazione perché è la stessa cosa che fa un parser
# markdown: un marcatore chiude se quel tipo è già aperto, altrimenti apre.
# Un asterisco che non può fare né l'uno né l'altro (spazio da entrambi i
# lati, «3 * 4») resta un asterisco.

_APRE = {"strong": "#strong[", "emph": "#emph["}


def _marcatore(n: int, pila: list[str]) -> str:
    voluti = {1: ["emph"], 2: ["strong"], 3: ["strong", "emph"]}[n]
    if all(v in pila for v in voluti):
        limite = min(pila.index(v) for v in voluti)
        quante = len(pila) - limite
        del pila[limite:]
        return "]" * quante
    fuori = []
    for v in voluti:
        if v not in pila:
            pila.append(v)
            fuori.append(_APRE[v])
    return "".join(fuori)


def _inline(s: str) -> str:
    fuori: list[str] = []
    pila: list[str] = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "`":
            j = s.find("`", i + 1)
            if j != -1:
                testo = s[i + 1:j].replace("\\", "\\\\").replace('"', '\\"')
                fuori.append(f'#raw("{testo}")')
                i = j + 1
                continue
        if c == "*":
            n = 0
            while i + n < len(s) and s[i + n] == "*":
                n += 1
            n = min(n, 3)
            voluti = {1: ["emph"], 2: ["strong"], 3: ["strong", "emph"]}[n]
            prec = s[i - 1] if i else " "
            succ = s[i + n] if i + n < len(s) else " "
            if prec not in " \t" and any(v in pila for v in voluti):
                fuori.append(_marcatore(n, pila))
            elif succ not in " \t":
                fuori.append(_marcatore(n, pila))
            else:
                fuori.append(_esc("*" * n))
            i += n
            continue
        fuori.append(_esc(c))
        i += 1
    fuori.append("]" * len(pila))
    return "".join(fuori)


# basename del master → etichetta Typst del suo capitolo. Lo riempie
# `sorgente()` prima di convertire: serve a trasformare un rimando fra due
# capitoli DELLO STESSO volume in un salto cliccabile. In un PDF di sessanta
# pagine un rimando che non si clicca è un rimando che nessuno segue.
RIMANDI: dict[str, str] = {}


def _link(testo: str, bersaglio: str) -> str:
    """Un `[testo](bersaglio)`: link interno se il bersaglio è nel volume."""
    file = bersaglio.split("#")[0].split("/")[-1]
    et = RIMANDI.get(file)
    if et:
        return f"#link(<{et}>)[{_unesc(_inline(testo))}]"
    return _inline(testo)


def inline(s: str) -> str:
    """Grassetto, corsivo, codice e link, nell'ordine che evita le collisioni."""
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: _link(m.group(1), m.group(2)), s)
    return _unesc(_inline(s))


def _celle(riga: str) -> list[str]:
    return [c.strip() for c in riga.strip().strip("|").split("|")]


_BLOCCO = re.compile(r"^(#{1,4}\s|>|---+\s*$|\s*[-*]\s+|\s*\d+\.\s+|\s*\||```|!\[)")


_IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def md_to_typ(md: str, base: Path | None = None, capolettera: bool = False) -> str:
    """Il sottoinsieme di markdown che i master usano davvero → sorgente Typst.

    `base` accende le immagini (senza, restano testo: è il caso delle schede,
    dove il ritratto arriva per un'altra strada). `capolettera` mette il
    versale d'apertura sul primo paragrafo vero del capitolo.
    """
    # Un'immagine in mezzo a una riga di testo diventa una riga sua: il resto
    # del convertitore lavora per blocchi, e una figura non è un blocco inline.
    if base is not None:
        md = "\n".join(
            _IMG.sub(lambda m: "\n" + m.group(0) + "\n", ln) if _IMG.search(ln) else ln
            for ln in md.split("\n")
        )
    righe = md.split("\n")
    primo_paragrafo = None
    ultimo_titolo = ""
    out: list[str] = []
    i = 0
    while i < len(righe):
        ln = righe[i]

        if ln.strip().startswith("```"):               # blocco di codice
            recinto = ln.strip()
            i += 1
            blocco = []
            while i < len(righe) and not righe[i].strip().startswith("```"):
                blocco.append(righe[i])
                i += 1
            i += 1
            if recinto == "```statblocco":
                # Il blocco statistiche non è codice: è un riquadro (ADR-0021).
                # Stamparlo come `raw` vorrebbe dire mettere in un manuale la
                # forma-dato invece del mostro.
                out.append(statblocco_typ("\n".join(blocco), ultimo_titolo))
                continue
            testo = "\n".join(blocco).replace("`", "\u0060")
            out.append("#block(breakable: true)[#raw(\"" + testo.replace('"', '\\"').replace("\n", "\\n") + "\", block: true)]")
            continue

        if ln.strip().startswith("|") and i + 1 < len(righe) and re.match(
            r"^\s*\|[\s:|-]+\|\s*$", righe[i + 1]
        ):
            testa = _celle(ln)
            i += 2
            corpo = []
            while i < len(righe) and righe[i].strip().startswith("|"):
                corpo.append(_celle(righe[i]))
                i += 1
            n = len(testa)
            out.append(f"#tabella({n},")
            out += [f"  [*{inline(h)}*]," if h.strip() else "  []," for h in testa]
            for r in corpo:
                out += [f"  [{inline(c)}]," for c in (r + [""] * n)[:n]]
            out.append(")")
            continue

        if ln.startswith(">"):                         # read-aloud o nota di regia
            blocco, aloud = [], False
            while i < len(righe) and righe[i].startswith(">"):
                t = righe[i].lstrip(">").strip()
                if t.startswith("*") and not t.startswith("**"):
                    aloud = True
                blocco.append(t)
                i += 1
            testo = " ".join(x for x in blocco if x)
            out.append(("#leggi[" if aloud else "#nota[") + inline(testo) + "]")
            continue

        m_img = _IMG.fullmatch(ln.strip())
        if m_img is not None and base is not None:
            fig = figura(m_img.group(1), m_img.group(2), base)
            if fig:
                out.append(fig)
            i += 1
            continue

        if re.match(r"^#{1,4}\s", ln):
            lvl = len(ln) - len(ln.lstrip("#"))
            ultimo_titolo = re.sub(r"\s*\[[^\]]*\]\s*$", "", ln[lvl:].strip())
            out.append("=" * lvl + " " + inline(ln[lvl:].strip()))
        elif re.match(r"^---+\s*$", ln):
            out.append("#fregio()")
        elif re.match(r"^\s*[-*]\s+", ln) or re.match(r"^\s*\d+\.\s+", ln):
            # Anche la voce di elenco assorbe le righe di continuazione: nei
            # master vanno spesso a capo, e trattarle come paragrafi a sé
            # staccava la coda della frase dal suo punto elenco.
            segno = "-" if re.match(r"^\s*[-*]\s+", ln) else "+"
            voce = [re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", ln)]
            while i + 1 < len(righe) and righe[i + 1].strip() and not _BLOCCO.match(righe[i + 1]):
                i += 1
                voce.append(righe[i].strip())
            out.append(f"{segno} " + inline(" ".join(voce)))
        elif ln.strip() == "":
            out.append("")
        else:
            # Il paragrafo si accorpa PRIMA dell'inline: nei master il grassetto
            # va spesso a capo, e riga per riga risulterebbe sbilanciato — il
            # difetto si vede come `**testo**` stampato letterale.
            para = [ln]
            while i + 1 < len(righe) and righe[i + 1].strip() and not _BLOCCO.match(righe[i + 1]):
                i += 1
                para.append(righe[i])
            if primo_paragrafo is None:
                primo_paragrafo = len(out)
            out.append(inline(" ".join(x.strip() for x in para)))
        i += 1

    # Il versale d'apertura va sul primo paragrafo VERO del capitolo, e solo se
    # è abbastanza lungo da reggerlo: su due righe di cappello starebbe storto.
    if capolettera and primo_paragrafo is not None:
        testo = out[primo_paragrafo]
        if len(testo) >= 120 and testo[:1].isalpha():
            out[primo_paragrafo] = (
                "#capolettera(" + json.dumps(testo[0], ensure_ascii=False)
                + ", [" + testo[1:] + "])"
            )
    return "\n".join(out)


def statblocco_typ(corpo: str, titolo_corrente: str = "") -> str:
    """Un blocco ```statblocco → una chiamata a `#statblocco()` del tema.

    Se il blocco non si legge, il volume NON si costruisce a metà: si dice
    quale scheda è rotta. Un riquadro con dentro dei buchi al tavolo è peggio
    di un errore in compilazione.
    """
    try:
        sb = leggi_statblocco("```statblocco\n" + corpo + "\n```")
    except StatblockError as e:
        raise SchedaError(f"blocco statistiche non valido: {e}") from e
    if sb is None:
        return ""
    nome = sb.nome or titolo_corrente
    voci = [f"nome: {json.dumps(nome, ensure_ascii=False)}"]
    for chiave, valore in (
        ("tipo", sb.tipo), ("gs", sb.gs), ("iniziativa", sb.iniziativa),
        ("sensi", sb.sensi), ("pf", (sb.pf + (f" ({sb.pf_dado})" if sb.pf_dado else "")).strip()),
        ("velocita", sb.velocita), ("tattica", sb.tattica), ("fonte", sb.fonte),
    ):
        if valore:
            voci.append(f"{chiave}: [{inline(valore)}]")
    ca = sb.ca + (f", {sb.ca_dettaglio}" if sb.ca_dettaglio else "")
    if ca.strip():
        voci.append(f"ca: [{inline(ca)}]")
    if sb.ts:
        voci.append(f"ts: [{inline(sb.ts)}]")
    if sb.attributi:
        coppie = [c.strip().split(None, 1) for c in sb.attributi.split(",") if c.strip()]
        voci.append("attributi: (" + "".join(
            f"({json.dumps(k, ensure_ascii=False)}, {json.dumps(v, ensure_ascii=False)}), "
            for k, v in (c for c in coppie if len(c) == 2)) + ")")
    if sb.attacchi:
        voci.append("attacchi: (" + "".join(
            "(" + json.dumps(a.split(None, 1)[0], ensure_ascii=False) + ", ["
            + inline(a.split(None, 1)[1] if len(a.split(None, 1)) > 1 else "") + "]), "
            for a in sb.attacchi) + ")")
    if sb.voci:
        voci.append("voci: (" + "".join(
            "(" + json.dumps(v.split(":", 1)[0].strip(), ensure_ascii=False) + ", ["
            + inline(v.split(":", 1)[1].strip() if ":" in v else "") + "]), "
            for v in sb.voci) + ")")
    return "#statblocco(\n  " + ",\n  ".join(voci) + ",\n)"


# ── le schede pregenerate ────────────────────────────────────────────────────
# Qui il convertitore generico non basta. Per mettere la CA in un riquadro, i sei
# attributi in una griglia e i legami in una colonna a parte bisogna sapere
# **quale numero è quale**: lo sa `dmcore.schede`, che legge i master. Questo
# pezzo traduce il risultato in una chiamata a `#scheda()` e nient'altro — la
# forma sta tutta in `typst/scheda-pg.typ`.

def _riga(md: str) -> str:
    """Un campo di prosa (anche andato a capo nel master) → contenuto Typst."""
    return "[" + inline(" ".join(md.split())) + "]"


def _blocco(md: str) -> str:
    """Un campo con struttura (gli slot degli incantesimi) → contenuto Typst."""
    return "[" + md_to_typ(md).strip() + "]"


def _str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def _tuple_str(righe) -> str:
    """Array Typst di tuple di stringhe, con la virgola finale che serve a 1 solo elemento."""
    return "(" + "".join("(" + ", ".join(_str(x) for x in r) + "), " for r in righe) + ")"


def _tuple_corpo(righe, come=_riga) -> str:
    """Array Typst di tuple `(etichetta, contenuto)`."""
    return "(" + "".join(f"({_str(e)}, {come(c)}), " for e, c in righe) + ")"


def _scheda_typ(s: Scheda, indice: int, totale: int, piede: str) -> str:
    # L'equipaggiamento sta col background — è la roba che il personaggio ha
    # addosso, non un numero da consultare in combattimento. Tutto il resto
    # (talenti, abilità, incantesimi, capacità di classe) va nello statblocco.
    equip = s.voce("equipaggiamento")
    destra = [(v.etichetta, v.corpo) for v in s.voci if v is not equip]

    campi: list[str] = [
        f"nome: {_str(s.nome)}",
        f"ruolo: {_str(s.ruolo)}",
        f"numero: {_str(s.numero or str(indice))}",
        f"totale: {_str(str(totale))}",
        f"classe: {_str(s.classe)}",
        f"rapide: {_tuple_str(s.rapide)}",
        f"ca: {_str(s.ca)}",
        f"pf: {_str(s.pf)}",
        f"pf-dado: {_str(s.pf_dado)}",
        f"ts: {_tuple_str(s.ts)}",
        f"attributi: {_tuple_str(s.attributi)}",
        f"manovre: {_tuple_str(s.manovre)}",
        "attacchi: (" + "".join(
            f"({_riga(riga)}, {'true' if rientro else 'false'}), " for riga, rientro in s.attacchi
        ) + ")",
        f"destra: {_tuple_corpo(destra, _blocco)}",
        f"retro: {_tuple_corpo([(v.etichetta, v.corpo) for v in s.voci_retro])}",
        f"legami: {_tuple_corpo(s.legami)}",
        f"piede: {_str(piede)}",
    ]
    for chiave, valore, come in (
        ("occhiello", s.occhiello, _riga),
        ("ca-dettaglio", s.ca_dettaglio, _riga),
        ("ts-nota", s.ts_nota, _riga),
        ("ad-alta-voce", s.ad_alta_voce, _riga),
        ("equipaggiamento", equip.corpo if equip else "", _blocco),
        ("problema", s.problema, _riga),
        ("minuto", s.minuto, _riga),
    ):
        if valore.strip():
            campi.append(f"{chiave}: {come(valore)}")
    if s.ritratto is not None:
        campi.append(f"ritratto: {_str(typ_path(s.ritratto))}")

    return "#scheda(\n  " + ",\n  ".join(campi) + ",\n)"


def schede_di(cap: dict, base: Path, f: Path) -> list[tuple[str, str]]:
    """Le schede di un capitolo `"layout": "schede"`, una per elemento.

    Tenerle separate serve a `--per-scheda`: un PDF per giocatore si ottiene
    compilando **un sorgente che contiene solo quella scheda**, non ritagliando
    la pagina N dal volume. Il ritaglio per numero regge finché ogni scheda sta
    in una pagina sola — cioè finché qualcuno non allunga un equipaggiamento.
    """
    retro = cap.get("retro")
    ritratti = cap.get("ritratti") or []
    if isinstance(ritratti, str):
        ritratti = [ritratti]
    elenco = leggi_schede(
        f,
        (base / retro).resolve() if retro else None,
        [(base / d).resolve() for d in ritratti],
    )
    mancanti = [s.nome for s in elenco if s.ritratto is None]
    if mancanti:
        print(f"  ⚠ schede senza ritratto: {', '.join(mancanti)}", file=sys.stderr)
    piede = cap.get("footer", "")
    return [
        (f"{s.numero or i}-{slug(s.nome)}", _scheda_typ(s, i, len(elenco), piede))
        for i, s in enumerate(elenco, 1)
    ]


def schede(cap: dict, base: Path, f: Path) -> str:
    """Il sorgente Typst di tutte le schede del capitolo, in fila."""
    return "\n\n".join(corpo for _, corpo in schede_di(cap, base, f))


# ── assemblaggio ─────────────────────────────────────────────────────────────

def capitoli(man: dict, base: Path, tutti: bool) -> list[tuple[dict, str, Path]]:
    fuori = []
    for c in man.get("chapters", []):
        if not tutti and c.get("tag") != "player":
            continue
        f = (base / c["file"]).resolve()
        if f.exists():
            fuori.append((c, c.get("title") or f.stem, f))
        else:
            print(f"  ⚠ capitolo mancante, saltato: {c['file']}", file=sys.stderr)
    return fuori


def fregio_per(titolo: str, file: Path, base: Path) -> str | None:
    """Il fregio del capitolo, se la sua cartella ne ha uno con un nome affine."""
    for d in (base.parent / "ALLEGATI" / "tavole" / "fregi", ROOT / "docs" / "assets" / "fregi"):
        if not d.is_dir():
            continue
        chiave = slug(file.stem)
        for svg in sorted(d.glob("fregio-*.svg")):
            nome = svg.stem[len("fregio-"):]
            if nome and (nome in chiave or chiave.startswith(nome)):
                return typ_path(svg)
    return None


# Le chiavi che questa catena consuma davvero. Tutto ciò che sta in un
# manifest e non è qui viene DICHIARATO a video invece che ignorato in
# silenzio: era la promessa di ADR-0020 («la divergenza diventa un controllo
# automatico, non una promessa») rimasta tale.
CHIAVI_NOTE = {
    "title", "subtitle", "brand", "banner", "meta", "footer", "header",
    "player_footer", "front_matter", "cover_image", "cover_tag", "intro_md",
    "out", "chapters", "carta", "capolettera",
}
CHIAVI_SOLO_HTML = {"player_footer", "header", "cover_tag", "out"}


def avvisa_chiavi(man: dict) -> None:
    ignote = sorted(set(man) - CHIAVI_NOTE)
    if ignote:
        print(f"  ⚠ chiavi di manifest sconosciute a entrambe le catene: {', '.join(ignote)}",
              file=sys.stderr)
    solo_html = sorted(set(man) & CHIAVI_SOLO_HTML)
    if solo_html:
        print(f"  · chiavi che valgono solo per la catena HTML, qui inattive: "
              f"{', '.join(solo_html)}", file=sys.stderr)


def intestazione(man: dict, apparato: bool | None = None, base: Path | None = None,
                 carta: str = "avorio") -> list[str]:
    """Import e `#show: libro.with(...)`: la testa di ogni sorgente generato."""
    if apparato is None:
        apparato = bool(man.get("front_matter", True))
    extra: list[str] = []
    if apparato and base is not None:
        # `cover_image` e `intro_md` sono relative al MANIFEST, come nella
        # catena HTML: due catene che risolvono lo stesso percorso in due modi
        # diversi sono un bug che si scopre in stampa.
        cop = man.get("cover_image")
        if cop:
            f = (base / cop).resolve()
            if f.is_file():
                extra.append(f'  copertina: {json.dumps(typ_path(f), ensure_ascii=False)},')
            else:
                print(f"  ⚠ cover_image mancante: {cop}", file=sys.stderr)
        intro = man.get("intro_md")
        if intro:
            f = (base / intro).resolve()
            if f.is_file():
                extra.append("  intro: [\n"
                             + md_to_typ(f.read_text(encoding="utf-8"), f.parent)
                             + "\n  ],")
            else:
                print(f"  ⚠ intro_md mancante: {intro}", file=sys.stderr)
    if carta != "avorio":
        extra.append(f'  carta: {json.dumps(carta, ensure_ascii=False)},')
    return [
        f'#import "{typ_path(TEMA)}": *',
        f'#import "{typ_path(SCHEDA_PG)}": scheda',
        "#show: libro.with(",
        f'  titolo: {json.dumps(man.get("title", ""), ensure_ascii=False)},',
        f'  sottotitolo: {json.dumps(man.get("subtitle", ""), ensure_ascii=False)},',
        f'  brand: {json.dumps(man.get("brand", ""), ensure_ascii=False)},',
        f'  banner: {json.dumps(man.get("banner", ""), ensure_ascii=False)},',
        f'  meta: {json.dumps(man.get("meta", ""), ensure_ascii=False)},',
        f'  capitolo: {json.dumps(man.get("footer", ""), ensure_ascii=False)},',
        f'  apparato: {"true" if apparato else "false"},',
        *extra,
        ")",
        "",
    ]


def sorgente(man: dict, base: Path, tutti: bool, carta: str = "avorio") -> str:
    elenco = capitoli(man, base, tutti)

    # Prima le etichette di TUTTI i capitoli, poi la conversione: un rimando in
    # avanti («vedi il capitolo 12») deve trovare il suo bersaglio anche se il
    # capitolo 12 non è ancora stato convertito.
    RIMANDI.clear()
    for cap, titolo, f in elenco:
        RIMANDI[f.name] = "cap-" + slug(f.stem)

    avvisa_chiavi(man)
    parti = intestazione(man, base=base, carta=carta)
    predefinito = bool(man.get("capolettera", True))
    for cap, titolo, f in elenco:
        if cap.get("layout") == "schede":
            parti.append(schede(cap, base, f))
            parti.append("")
            continue
        fr = fregio_per(titolo, f, base)
        parti.append(f"#capitolo-aperto({json.dumps(titolo, ensure_ascii=False)}, "
                     f"{'none' if not fr else json.dumps(fr, ensure_ascii=False)})")
        parti.append(f"#metadata(\"capitolo\") <{RIMANDI[f.name]}>")
        corpo = md_to_typ(f.read_text(encoding="utf-8"), f.parent,
                          capolettera=bool(cap.get("capolettera", predefinito)))
        corpo = re.sub(r"\A\s*=\s[^\n]*\n", "", corpo)   # il titolo lo dà il manifest
        parti.append(corpo)
        parti.append("")
    return "\n".join(parti)


def compila(binario: str, typ: Path, pdf: Path) -> tuple[subprocess.CompletedProcess, bool]:
    """Un `typst compile`, col ripiego sui tag PDF dichiarato dal chiamante.

    Typst 0.15.1 ha un bug interno nella costruzione dell'albero dei tag PDF
    («internal error: parent group») su documenti con float dentro strutture
    annidate. I tag sono accessibilità, non impaginazione: se inciampa lì si
    riprova senza — e lo si DICE, invece di consegnare un PDF diverso da quello
    che il comando promette.
    """
    cmd = [binario, "compile", "--font-path", str(FONTS), "--root", str(ROOT)]
    esito = subprocess.run(cmd + [str(typ), str(pdf)], capture_output=True, text=True)
    if esito.returncode != 0 and "internal error" in esito.stderr and "tags" in esito.stderr:
        return subprocess.run(cmd + ["--no-pdf-tags", str(typ), str(pdf)],
                              capture_output=True, text=True), True
    return esito, False


def per_scheda(man: dict, base: Path, tutti: bool, binario: str, nome: str,
               tieni_typ: bool, carta: str = "avorio") -> int:
    """Un PDF per scheda in `<manifest>/schede/`, da mandare a un giocatore solo.

    Non è una comodità: sulla scheda c'è «la cosa che non dici». Girare il
    volume intero nel gruppo brucia i sei segreti prima della prima serata —
    il fascicolo completo è per il DM e per la stampante, i singoli per i
    giocatori. Perciò qui l'apparato è **sempre** spento: una copertina e un
    indice su un foglio solo non hanno senso.
    """
    fuori = base / "schede"
    trovate: list[tuple[str, str]] = []
    for cap, _, f in capitoli(man, base, tutti):
        if cap.get("layout") == "schede":
            trovate += schede_di(cap, base, f)
    if not trovate:
        print("✗ --per-scheda: nessun capitolo «\"layout\": \"schede\"» nel manifest.\n"
              "  È la chiave che accende l'impaginazione a scheda — vedi "
              "docs/guides/GUIDA-BOOKLET-E-PDF.md §1.2.", file=sys.stderr)
        return 2

    fuori.mkdir(exist_ok=True)
    testa = intestazione(man, apparato=False, base=base, carta=carta)
    for etichetta, corpo in trovate:
        typ = fuori / f"{nome}-{etichetta}.typ"
        pdf = typ.with_suffix(".pdf")
        typ.write_text("\n".join(testa + [corpo, ""]), encoding="utf-8")
        esito, _ = compila(binario, typ, pdf)
        if not tieni_typ:
            typ.unlink(missing_ok=True)
        if esito.returncode != 0:
            print(esito.stderr.strip()[:2000], file=sys.stderr)
            print(f"✗ --per-scheda: compilazione fallita su {etichetta}", file=sys.stderr)
            return 1
    print(f"✓ --per-scheda: {len(trovate)} schede → {fuori.relative_to(ROOT)}/ "
          f"(una a testa, senza frontespizio)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("manifest", help="il manifest del booklet (lo stesso dell'HTML)")
    ap.add_argument("--all", action="store_true", help="tutti i capitoli, ⚠ DM inclusi")
    ap.add_argument("--keep-typ", action="store_true", help="conserva il sorgente .typ generato")
    ap.add_argument("--list", action="store_true", help="elenca i capitoli e esci")
    ap.add_argument("--carta", choices=("avorio", "bianca"), default="avorio",
                    help="«bianca» toglie il fondo avorio: sessanta pagine di fondo pieno "
                         "su una stampante di casa sono una cartuccia")
    ap.add_argument("--per-scheda", action="store_true",
                    help="in più, un PDF per ogni scheda in schede/ (da mandare a un giocatore solo)")
    args = ap.parse_args()

    mp = Path(args.manifest).resolve()
    if not mp.is_file():
        print(f"✗ manifest non trovato: {mp}", file=sys.stderr)
        return 2
    man = json.loads(mp.read_text(encoding="utf-8"))
    base = mp.parent

    if args.list:
        for cap, t, f in capitoli(man, base, True):
            marchio = "  [schede]" if cap.get("layout") == "schede" else ""
            print(f"  {t}{marchio}  ←  {f.relative_to(ROOT) if ROOT in f.parents else f}")
        return 0

    binario = shutil.which("typst")
    if not binario:
        print(INSTALLA, file=sys.stderr)
        return 1

    typ = base / f"{mp.stem.replace('.manifest', '')}.typ"
    pdf = base / f"{mp.stem.replace('.manifest', '')}-STAMPA.pdf"
    try:
        src = sorgente(man, base, args.all, args.carta)
    except SchedaError as e:
        print(f"✗ export_booklet_typst: {e}", file=sys.stderr)
        return 1
    typ.write_text(src, encoding="utf-8")

    esito, degradato = compila(binario, typ, pdf)

    if not args.keep_typ:
        typ.unlink(missing_ok=True)
    if esito.returncode != 0:
        print(esito.stderr.strip()[:4000], file=sys.stderr)
        print("✗ export_booklet_typst: compilazione fallita", file=sys.stderr)
        return 1
    if degradato:
        print("  ⚠ tag PDF disattivati: bug interno di typst sull'albero dei tag.\n"
              "    Il volume è completo e i segnalibri ci sono; manca il livello di\n"
              "    accessibilità per i lettori di schermo. Riprovare a ogni aggiornamento\n"
              "    di typst — la riga di fallback si toglie il giorno che compila.",
              file=sys.stderr)

    n = len(capitoli(man, base, args.all))
    print(f"✓ export_booklet_typst: {n} capitoli → {pdf.relative_to(ROOT)} "
          f"({pdf.stat().st_size // 1024} KB, un volume con segnalibri)")

    if args.per_scheda:
        return per_scheda(man, base, args.all, binario,
                          mp.stem.replace(".manifest", ""), args.keep_typ, args.carta)
    return 0


if __name__ == "__main__":
    sys.exit(main())
