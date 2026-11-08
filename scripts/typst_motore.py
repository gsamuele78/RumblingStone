"""typst_motore.py — un solo modo di compilare e interrogare un `.typ` (ADR-0116).

Lo standard è il pacchetto PyPI `typst` (typst-py, Apache-2.0), fissato in
`requirements.txt`. È il compilatore ufficiale dentro un modulo Python: non
passa da GitHub Releases, lo aggiorna Dependabot e va nel bundle insieme alle
altre wheel. Misura: `plans/esperimenti/typst-pip-2026-11-08/MISURE.md`, cioè
19 booklet e 856 pagine con testo e pixel identici alla CLI.

Una CLI `typst` nel PATH resta il **ripiego**: si usa se il modulo manca,
oppure se `RUMBLINGSTONE_TYPST=cli` lo chiede. `RUMBLINGSTONE_TYPST=pypi`
vieta il ripiego. La CLI non e' piu' fissata da nessuna parte (mise e
`strumenti.py` sono usciti con ADR-0116): se la sua versione non e' quella di
`requirements.txt`, i PDF non sono quelli della CI.

Ogni chiamante passa di qui: `export_booklet_typst`, `misura_stampa`,
`varianti_stampa`, `validate_booklets`, `validate_corredo`. Se lo facesse
ognuno per conto suo, le regole diventerebbero due e una invecchierebbe in
silenzio, come dice `binari.py`.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

import binari

try:  # opzionale, con ripiego dichiarato (ADR-0037)
    import typst as _typst
except ImportError:  # pragma: no cover - dipende dall'ambiente
    _typst = None
# Con scripts/ nel sys.path, senza il pacchetto PyPI `import typst` trova la
# cartella scripts/typst/ (tema e pacchetti vendorizzati) come namespace
# package: non è il compilatore, quindi si ripiega.
if _typst is not None and not hasattr(_typst, "compile"):
    _typst = None

VARIABILE = "RUMBLINGSTONE_TYPST"


class Esito(NamedTuple):
    ok: bool
    errore: str
    #: True se ha dovuto ricompilare senza tag PDF (bug di typst 0.15.1
    #: «internal error: parent group» su float annidati: i tag sono
    #: accessibilità, non impaginazione, e il chiamante lo dice).
    senza_tag: bool


def motore() -> str | None:
    """«pypi», «cli», oppure None se non c'è né l'uno né l'altro."""
    scelta = os.environ.get(VARIABILE, "").strip().lower()
    if scelta == "cli":
        return "cli" if binari.trova(binari.TYPST) else None
    if _typst is not None:
        return "pypi"
    if scelta == "pypi":
        return None
    return "cli" if binari.trova(binari.TYPST) else None


def disponibile() -> bool:
    return motore() is not None


MESSAGGIO = """\
✗ typst non c'è: serve per l'edizione da stampa (ADR-0020, ADR-0116).

  Standard       pip install -r requirements.txt     (il pacchetto «typst» di PyPI)
  Ripiego        una CLI typst nel PATH (github.com/typst/typst/releases)

Niente panico se non lo installi: `export_booklet_pdf.py` continua a produrre i
PDF per capitolo con Chromium. Questo esportatore serve al volume da stampa.
"""


def esigi() -> str:
    """Il motore, oppure stampa come installarlo ed esce con `binari.MANCA`."""
    m = motore()
    if m is None:
        print(MESSAGGIO, file=sys.stderr)
        raise SystemExit(binari.MANCA)
    return m


def _opzioni_cli(root: Path, font: Path, pacchetti: Path, solo_font_del_repo: bool,
                 ingressi: dict[str, str] | None) -> list[str]:
    opz = ["--font-path", str(font), "--root", str(root), "--package-path", str(pacchetti)]
    if solo_font_del_repo:
        opz.insert(0, "--ignore-system-fonts")
    for k, v in (ingressi or {}).items():
        opz += ["--input", f"{k}={v}"]
    return opz


def _opzioni_py(root: Path, font: Path, pacchetti: Path, solo_font_del_repo: bool,
                ingressi: dict[str, str] | None) -> dict:
    return dict(root=str(root), font_paths=[str(font)], package_path=str(pacchetti),
                ignore_system_fonts=solo_font_del_repo, sys_inputs=dict(ingressi or {}))


def _data() -> int | None:
    """La data di creazione del PDF: quella di SOURCE_DATE_EPOCH, come fa la CLI."""
    v = os.environ.get("SOURCE_DATE_EPOCH", "").strip()
    return int(v) if v.isdigit() else None


def _e_bug_dei_tag(testo: str) -> bool:
    return "internal error" in testo and "tag" in testo


def compila(typ: Path, pdf: Path, *, root: Path, font: Path, pacchetti: Path,
            solo_font_del_repo: bool = False, ingressi: dict[str, str] | None = None) -> Esito:
    """`typst compile`, col ripiego senza tag PDF quando typst inciampa lì."""
    m = esigi()
    if m == "pypi":
        opz = _opzioni_py(root, font, pacchetti, solo_font_del_repo, ingressi)
        ts = _data()
        if ts is not None:
            opz["timestamp"] = ts
        for tag in (True, False):
            try:
                _typst.compile(str(typ), output=str(pdf), pdf_tags=tag, **opz)
                return Esito(True, "", not tag)
            except _typst.TypstError as e:
                if not (tag and _e_bug_dei_tag(str(e))):
                    return Esito(False, str(e), not tag)
    cmd = [binari.esigi(binari.TYPST), "compile",
           *_opzioni_cli(root, font, pacchetti, solo_font_del_repo, ingressi)]
    r = subprocess.run(cmd + [str(typ), str(pdf)], capture_output=True, text=True)
    if r.returncode != 0 and _e_bug_dei_tag(r.stderr):
        r = subprocess.run(cmd + ["--no-pdf-tags", str(typ), str(pdf)], capture_output=True, text=True)
        return Esito(r.returncode == 0, r.stderr, True)
    return Esito(r.returncode == 0, r.stderr, False)


def valuta(typ: Path, espressione: str, *, root: Path, font: Path, pacchetti: Path,
           solo_font_del_repo: bool = False, ingressi: dict[str, str] | None = None):
    """`typst eval --in typ espressione`, decodificato da JSON. Alza RuntimeError."""
    if esigi() == "pypi":
        try:
            uscita = _typst.eval(str(typ), espressione,
                                 **_opzioni_py(root, font, pacchetti, solo_font_del_repo, ingressi))
        except _typst.TypstError as e:
            raise RuntimeError(f"typst eval: {str(e)[-1000:]}") from e
        if isinstance(uscita, bytes):
            uscita = uscita.decode("utf-8")
        return json.loads(uscita or "[]")
    cmd = [binari.esigi(binari.TYPST), "eval", "--in", str(typ),
           *_opzioni_cli(root, font, pacchetti, solo_font_del_repo, ingressi), espressione]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"typst eval: {r.stderr[-1000:]}")
    return json.loads(r.stdout or "[]")


def versione() -> str:
    """Per `dm.py doctor` e per i rapporti: chi compila, e quale versione."""
    m = motore()
    if m == "pypi":
        from importlib import metadata  # noqa: PLC0415
        return f"pypi typst {metadata.version('typst')}"
    if m == "cli":
        r = subprocess.run([binari.trova(binari.TYPST), "--version"], capture_output=True, text=True)
        return f"cli {r.stdout.strip()}"
    return "assente"


if __name__ == "__main__":
    print(f"typst: {versione()}")
    sys.exit(0 if disponibile() else binari.MANCA)
