"""L5 (ADR-0111): le tabelle base delle creature 3.5 lette dal plugin dnd35.

Il difetto che questo test esiste per impedire: un numero che cambia
spostandolo da `dmcore/tabelle.py` a `sistemi/dnd35/dati/creature.toml`. Le
impronte sono quelle delle costanti scritte nel codice fino al 2026-11-07
(main b0a74ae), calcolate su `repr` delle voci ordinate: se un valore cambia
nei dati, l'impronta cambia e il test lo dice. Per cambiare una tabella di
proposito si aggiorna l'impronta qui, nello stesso diff, con il motivo.

Solo `unittest`.
"""
from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore import sistemi as S  # noqa: E402
from dmcore import tabelle as T  # noqa: E402

IMPRONTE_PRIMA = {
    "TIPI": "f314442313fc6eb1",
    "CLASSI": "ba993374d9283a09",
    "CLASSI_PNG": "b9acd679e2fa5931",
    "BAB_CLASSE": "e806f841362f1085",
    "TAGLIE": "e0f832356e31615e",
    "ARMATURE": "8caf8f137870a208",
    "SCUDI": "9cfe333a9826ed8f",
    "ELITE": "f3bbb911592fbc0a",
    "BASIC": "09397ca2fbf7a68e",
}


def impronta(x) -> str:
    if isinstance(x, dict):
        x = sorted(x.items())
    elif isinstance(x, frozenset):
        x = sorted(x)
    return hashlib.sha256(repr(x).encode()).hexdigest()[:16]


class TabelleDalPlugin(unittest.TestCase):
    def test_stessi_valori_di_prima(self):
        for nome, attesa in IMPRONTE_PRIMA.items():
            self.assertEqual(impronta(getattr(T, nome)), attesa, nome)

    def test_la_fonte_e_il_plugin(self):
        self.assertEqual(S.capacita("dnd35", "creature.costruzione").modo, "dati")
        dati = S.dati("dnd35", "creature.costruzione")
        self.assertEqual(set(dati["tipi"]), set(T.TIPI))
        self.assertEqual(T.TIPI["undead"], (12, 0.5, ("vol",)))

    def test_ogni_classe_ha_dado_ts_e_bab(self):
        self.assertEqual(set(T.BAB_CLASSE), set(T.CLASSI))
        self.assertTrue(T.CLASSI_PNG <= set(T.CLASSI))


if __name__ == "__main__":
    unittest.main()
