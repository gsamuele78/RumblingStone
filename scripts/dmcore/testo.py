"""
testo — normalizzazione di stringhe condivisa (Lotto A del piano
QUALITA-DEL-CODICE; ADR-0037 per il vincolo stdlib-only).

Prima di questo modulo il repo aveva **sette** implementazioni di `slug`, e
una si comportava diversamente dalle altre: `build_monster_catalog.py`
saltava la normalizzazione NFKD, quindi una lettera accentata non veniva
traslitterata, veniva buttata via. Nove record veri del catalogo mostri
avevano un id che nessun altro strumento della catena ricalcolava uguale
(``l-myn-redtongue-…`` contro ``lomyn-redtongue-…``).

Qui ce n'è una sola, parametrica sulle due sole cose su cui i sette
chiamanti divergevano davvero: la lunghezza massima e la stringa di
ripiego quando non resta niente.

    >>> slug("Città")
    'citta'
    >>> slug("Lómyn RedTongue")
    'lomyn-redtongue'
    >>> slug("Razorfiend «Blackspawn Alfa» d'élite")
    'razorfiend-blackspawn-alfa-d-elite'
    >>> slug("12–13")          # trattino lungo, non un trattino ASCII
    '12-13'
    >>> slug("«»", ripiego="mappa")
    'mappa'

Solo stdlib.
"""

from __future__ import annotations

import re
import unicodedata

__all__ = ["slug", "piega_ascii"]

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def piega_ascii(s: str) -> str:
    """Riduce `s` ad ASCII, senza far sparire silenziosamente i caratteri.

    Le tre categorie hanno tre destini diversi, e il terzo è il motivo per
    cui questa funzione esiste invece di un ``.encode("ascii", "ignore")``:

    * ASCII: resta com'è;
    * segno combinante (l'accento che NFKD ha staccato dalla lettera): si
      butta, ed è così che ``é`` diventa ``e``;
    * qualsiasi altro carattere non-ASCII: diventa un separatore.

    ``ignore`` metteva tutto e tre nella seconda categoria, e su ``12–13``
    questo produce ``1213``: due numeri diventano uno. Un trattino lungo
    che l'ASCII non sa scrivere separa, non sparisce.
    """
    fuori = []
    for ch in unicodedata.normalize("NFKD", s):
        if ord(ch) < 128:
            fuori.append(ch)
        elif unicodedata.combining(ch):
            continue
        else:
            fuori.append("-")
    return "".join(fuori)


def slug(s: str, *, max_len: int | None = None, ripiego: str = "") -> str:
    """Identificatore stabile derivato da un titolo o da un nome.

    :param max_len: taglia il risultato a questa lunghezza. Il taglio
        avviene prima della ripulitura finale, così un id troncato non
        finisce mai con un trattino penzolante.
    :param ripiego: cosa restituire quando non resta nemmeno un carattere
        utile (un nome fatto di sole virgolette caporali, per dire).
        Vuoto se non specificato.
    """
    s = _NON_ALNUM.sub("-", piega_ascii(s).lower()).strip("-")
    if max_len is not None:
        s = s[:max_len].strip("-")
    return s or ripiego
