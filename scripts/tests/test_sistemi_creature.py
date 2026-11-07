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
from dmcore import caratteristiche as C  # noqa: E402
from dmcore import progressione as P  # noqa: E402
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

#: L5b (2026-11-07): impronte delle costanti di main c258a3e, prima dello
#: spostamento in `creature.toml`. `NOMI_DI_CLASSE` non c'è: è ordinato per
#: lunghezza partendo da un `set`, quindi a parità di lunghezza l'ordine cambia
#: con PYTHONHASHSEED già prima di L5b (la regex che lo usa non ne dipende).
IMPRONTE_L5B = {
    "T.MAGO": "52ca98ec50a5de88",
    "T.STREGONE": "d81f1e56ec2c06ed",
    "T.STREGONE_CONOSCIUTI": "288be00dadabf4f1",
    "T.CHIERICO": "b830bf626b47fd2e",
    "T.DRUIDO": "b830bf626b47fd2e",
    "T.ADEPTO": "043b934095eaabbf",
    "T.BARDO": "143fc66e36c447c4",
    "T.BARDO_CONOSCIUTI": "0eba013d243c5289",
    "T.RANGER": "b69e66ddc56f3a4d",
    "T.PALADINO": "b69e66ddc56f3a4d",
    "T.LIVELLO_INCANTATORE_RIDOTTO": "6a9633f885386bc7",
    "T.INCANTATORI": "5dafa79241e64173",
    "T.INCANTATORI_SENZA_ANCORA": "cbad0fe52ade2682",
    "P.PRESTIGIO": "bb65fa3b3e39222b",
    "P.DADO_DI_CLASSE": "7fbf113d03329d21",
    "C.PROFILI": "2abef478722f8731",
    "C.PROFILO_DI_RIPIEGO": "6f6caace7ceb23dc",
    "C.PER_TAGLIA": "08bcc3ca27cf6cb0",
    "C.RAZZE": "7a128d76c0baa3ce",
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



class IncantatoriEProfiliDalPlugin(unittest.TestCase):
    """L5b: incantatori, prestigio, profili, taglie e razze dal plugin."""

    MODULI = {"T": T, "P": P, "C": C}

    def test_stessi_valori_di_prima(self):
        for chiave, attesa in IMPRONTE_L5B.items():
            modulo, nome = chiave.split(".")
            self.assertEqual(impronta(getattr(self.MODULI[modulo], nome)), attesa, chiave)

    def test_nomi_di_classe_stesso_insieme(self):
        self.assertEqual(impronta(frozenset(P.NOMI_DI_CLASSE)), "e5a2db6f0d38a085")

    def test_alias_restano_la_stessa_griglia(self):
        self.assertIs(T.DRUIDO, T.CHIERICO)
        self.assertIs(T.PALADINO, T.RANGER)
        self.assertIs(T.INCANTATORI["paladino"][0], T.RANGER)

    def test_ogni_incantatore_ha_venti_livelli(self):
        for classe, (griglia, car, _) in T.INCANTATORI.items():
            self.assertEqual(sorted(griglia), list(range(1, 21)), classe)
            self.assertIn(car, {"int", "sag", "car"}, classe)

    def test_ordine_delle_razze_conta(self):
        nomi = [n for n, _ in C.RAZZE]
        self.assertLess(nomi.index("hobgoblin"), nomi.index("goblin"))
        self.assertLess(nomi.index("duergar"), nomi.index("nano"))


if __name__ == "__main__":
    unittest.main()
