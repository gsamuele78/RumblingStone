"""binari.py — le dipendenze binarie del repo, e la regola di degradazione.

Il repo ha deciso due volte di accettare un eseguibile esterno invece di un
toolchain: `typst` per l'edizione da stampa ([ADR-0020]) e `pdfcpu` per
l'imposizione ([ADR-0027]). Sono decisioni buone — un singolo binario statico,
licenza aperta, nessuna installazione di sistema — a **una** condizione, che è
poi la parte che si dimentica di scrivere:

    se il binario manca, lo script dice come installarlo ed ESCE.
    Non fallisce a meta'.

Fallire a metà è il modo in cui una dipendenza opzionale diventa un problema di
fiducia: un PDF di 40 pagine su 96, un file scritto e poi troncato, un errore che
arriva da `subprocess` in inglese e non dice cosa fare. Chi impagina la sera
prima della sessione non ha modo di sapere se il file che ha in mano e' quello
giusto.

La regola sta qui, in un posto solo, perche' con due copie diventano due regole.

Codici d'uscita
---------------
`MANCA` (2) e' distinto da 1. Uno script che esce con 2 sta dicendo *«non ho
nemmeno cominciato: manca uno strumento»*, che non e' la stessa cosa di *«ho
provato e non ci sono riuscito»*. La CI puo' distinguerli, e chi legge anche.

Solo stdlib.
"""
from __future__ import annotations

import shutil
import sys
from typing import NamedTuple

MANCA = 2  # exit code: dipendenza assente. Distinto da 1 = fallimento vero.


class Binario(NamedTuple):
    """Un eseguibile esterno accettato con un ADR, e cosa succede senza."""

    nome: str
    a_cosa_serve: str
    licenza: str
    adr: str
    installa: str
    #: Cosa resta possibile senza. Un ripiego dichiarato e' la differenza fra
    #: una dipendenza opzionale e una dipendenza travestita da opzionale.
    ripiego: str


TYPST = Binario(
    nome="typst",
    a_cosa_serve="l'edizione da stampa: un volume unico con segnalibri veri",
    licenza="Apache-2.0",
    adr="ADR-0020",
    installa="""\
  Linux/macOS   curl -sSL https://github.com/typst/typst/releases/latest/download/\\
                  typst-x86_64-unknown-linux-musl.tar.xz | tar xJ
                  sudo install typst-*/typst /usr/local/bin/
  Fedora/Bazzite  brew install typst        (oppure il tarball qui sopra)
  Arch            pacman -S typst
  Windows         winget install --id Typst.Typst""",
    ripiego="`export_booklet_pdf.py` continua a produrre i PDF per capitolo con "
            "Chromium. Questo esportatore serve al volume da stampa.",
)

PDFCPU = Binario(
    nome="pdfcpu",
    a_cosa_serve="l'imposizione: un libretto da piegare, invece di una risma",
    licenza="Apache-2.0",
    adr="ADR-0027",
    installa="""\
  Con Go (qualsiasi sistema)   go install github.com/pdfcpu/pdfcpu/cmd/pdfcpu@v0.11.0
  Linux/macOS   scarica il binario da https://github.com/pdfcpu/pdfcpu/releases
                e mettilo nel PATH — e' un eseguibile statico, niente altro
  Arch          pacman -S pdfcpu
  Windows       winget install pdfcpu""",
    ripiego="il PDF da stampa resta valido e stampabile pagina per pagina: "
            "l'imposizione e' un di piu' per chi rilega, non un passaggio "
            "obbligato della catena.",
)

TUTTI = (TYPST, PDFCPU)


def messaggio(b: Binario) -> str:
    """Il testo che si stampa quando manca. Dice tre cose: cosa, come, e cosa resta."""
    return (
        f"Il binario «{b.nome}» non è nel PATH. Serve a {b.a_cosa_serve}.\n"
        f"È un singolo eseguibile, {b.licenza} ({b.adr}):\n\n"
        f"{b.installa}\n\n"
        f"Niente panico se non lo installi: {b.ripiego}\n"
    )


def trova(b: Binario) -> str | None:
    """Il percorso dell'eseguibile, o `None`. Nessun effetto collaterale."""
    return shutil.which(b.nome)


def esigi(b: Binario) -> str:
    """Il percorso dell'eseguibile, oppure stampa il modo di installarlo ed **esce**.

    È la regola di degradazione pulita, in una riga di chiamata. Si usa **prima**
    di aprire file di destinazione, non dopo: il punto è non lasciare in giro un
    output a metà.
    """
    percorso = trova(b)
    if percorso is None:
        print(messaggio(b), file=sys.stderr)
        raise SystemExit(MANCA)
    return percorso


def stato() -> list[tuple[Binario, str | None]]:
    """Cosa c'è e cosa manca — per `dm.py doctor`."""
    return [(b, trova(b)) for b in TUTTI]


if __name__ == "__main__":
    mancanti = 0
    for b, p in stato():
        if p:
            print(f"✓ {b.nome:8} {p}")
        else:
            print(f"⚠ {b.nome:8} assente — {b.ripiego}")
            mancanti += 1
    print(f"\n{len(TUTTI) - mancanti}/{len(TUTTI)} dipendenze binarie presenti.")
