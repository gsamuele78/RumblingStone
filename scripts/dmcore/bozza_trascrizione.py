"""Il segno della bozza che viene dalla trascrizione (ADR-0135).

La bozza scritta da `transcribe_session.py` non e' mai canone (ADR-0007): il DM
la legge, la riscrive e firma il log con il wizard. Se per sbaglio la bozza
finisce in `campaign/sessions/` cosi' com'e', `state_apply` si rifiuta di
applicarla e `session_recap` la salta: nessuno dei due deve trattare come
storia giocata un testo che nessuno ha ancora letto.
"""
from __future__ import annotations

#: Prima riga di ogni bozza. Il DM la toglie quando il log e' suo.
MARCATORE = "<!-- bozza-trascrizione: non e' canone -->"


def e_bozza(testo: str) -> bool:
    """Vero se il testo porta ancora il segno della bozza."""
    return "<!-- bozza-trascrizione" in testo
