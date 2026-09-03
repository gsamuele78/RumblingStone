"""Le tabelle contro le loro ancore.

Il criterio del piano: *ogni riga cita la sua fonte; un test confronta la tabella
con le righe d'ancora della skill*. Non è una formalità. Le tabelle sono state
battute a mano da un manuale: l'unico modo per accorgersi di una cifra sbagliata
è confrontarla con una copia scritta altrove, in un altro momento, per un altro
scopo. Le skill sono quella copia.

Un test che ricalcolasse la tabella dalla tabella stessa non troverebbe niente —
e questo è il motivo per cui le ancore vengono lette dal markdown delle skill, e
non da una costante Python accanto a quella che dovrebbero controllare.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import tabelle  # noqa: E402

SKILL_35 = ROOT / ".claude/skills/dnd-35-srd/references/classes.md"
SKILL_PF = ROOT / ".claude/skills/pathfinder-1e-srd/references/monster-advancement.md"


def _righe_markdown(testo: str, dopo: str) -> list[list[str]]:
    """Le righe della prima tabella markdown che segue un'intestazione."""
    coda = testo[testo.index(dopo):]
    righe = []
    for riga in coda.splitlines():
        riga = riga.strip()
        if not riga.startswith("|"):
            if righe:
                break
            continue
        celle = [c.strip() for c in riga.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in celle):
            continue
        righe.append(celle)
    return righe[1:]  # senza l'intestazione


def _slot(testo: str) -> tuple[int, ...]:
    """«6/6/6/6/5/3» o «4 | 4 | 3 | - | -» → la tupla degli slot."""
    pezzi = re.split(r"[/|]", testo)
    fuori = []
    for p in pezzi:
        p = p.strip()
        if p in {"-", "—", ""}:
            fuori.append(0)
        elif p.isdigit():
            fuori.append(int(p))
    while fuori and fuori[-1] == 0:
        fuori.pop()
    return tuple(fuori)


class AncoreIncantatori(unittest.TestCase):
    """Le griglie degli incantesimi contro le righe scritte nella skill 3.5."""

    @classmethod
    def setUpClass(cls):
        cls.testo = SKILL_35.read_text(encoding="utf-8")

    def test_stregone_incantesimi_al_giorno(self):
        righe = _righe_markdown(self.testo, "Verified anchor rows (SRD Table: The Sorcerer")
        self.assertTrue(righe, "la skill non ha piu' le righe d'ancora dello stregone")
        for cella in righe:
            liv, al_giorno = int(cella[0]), _slot(cella[1])
            with self.subTest(livello=liv):
                self.assertEqual(tabelle.STREGONE[liv], al_giorno)

    def test_stregone_incantesimi_conosciuti(self):
        righe = _righe_markdown(self.testo, "Verified anchor rows (SRD Table: The Sorcerer")
        for cella in righe:
            liv, conosciuti = int(cella[0]), _slot(cella[2])
            with self.subTest(livello=liv):
                self.assertEqual(tabelle.STREGONE_CONOSCIUTI[liv], conosciuti)

    def test_mago(self):
        righe = _righe_markdown(self.testo, "**Spells /day**:")
        self.assertTrue(righe, "la skill non ha piu' la tabella del mago")
        for cella in righe:
            liv = int(cella[0])
            with self.subTest(livello=liv):
                self.assertEqual(tabelle.MAGO[liv], _slot(" | ".join(cella[1:])))

    def test_chierico_e_druido(self):
        """Il chierico ha un'ancora in repo solo da quando serve al generatore."""
        righe = _righe_markdown(self.testo, "Verified anchor rows (SRD Table: The Cleric")
        self.assertTrue(righe, "la skill non ha le righe d'ancora del chierico")
        for cella in righe:
            liv = int(cella[0])
            with self.subTest(livello=liv):
                self.assertEqual(tabelle.CHIERICO[liv], _slot(cella[1]))
        self.assertIs(tabelle.DRUIDO, tabelle.CHIERICO,
                      "in 3.5 chierico e druido hanno la stessa griglia")

    def test_le_griglie_sono_complete_e_monotone(self):
        """Vent'anni di livelli, e nessuna classe che perde slot salendo."""
        for nome, (griglia, _, _) in tabelle.INCANTATORI.items():
            with self.subTest(classe=nome):
                self.assertEqual(sorted(griglia), list(range(1, 21)))
                for liv in range(2, 21):
                    prima = tabelle.livello_massimo(griglia, liv - 1)
                    dopo = tabelle.livello_massimo(griglia, liv)
                    self.assertGreaterEqual(dopo, prima)

    def test_l_adepto_dichiara_di_non_avere_ancora(self):
        """La riga che non ho potuto controllare deve dirlo lei, non io."""
        self.assertIn("adept", tabelle.INCANTATORI_SENZA_ANCORA)
        self.assertLessEqual(tabelle.livello_massimo(tabelle.ADEPTO, 20), 5,
                             "l'adepto non supera il 5° livello d'incantesimo")


class AncorePerGS(unittest.TestCase):
    """La tabella PF1e per GS contro Table 1–1 come sta nella skill."""

    def test_le_righe_verificate_coincidono_con_la_skill(self):
        righe = _righe_markdown(SKILL_PF.read_text(encoding="utf-8"),
                                "| CR | AC | hp | High attack |")
        visti = set()
        for cella in righe:
            gs = int(cella[0])
            visti.add(gs)
            atteso = tabelle.PER_GS[gs]
            with self.subTest(gs=gs):
                self.assertEqual(atteso[0], int(cella[1]), "CA")
                self.assertEqual(atteso[1], int(cella[2]), "pf")
                self.assertEqual(atteso[2], int(cella[3]), "attacco")
                self.assertEqual(atteso[4], int(cella[5]), "CD primaria")
        self.assertEqual(visti, set(tabelle.PER_GS_VERIFICATE),
                         "le righe verificate devono essere ESATTAMENTE quelle "
                         "che la skill scrive: ne' meno (perderemmo un controllo) "
                         "ne' di piu' (ci fideremmo di una riga non vista)")

    def test_riga_gs_dice_se_e_verificata(self):
        riga, verificata = tabelle.riga_gs(13)
        self.assertTrue(verificata)
        self.assertEqual(riga["pf"], 180)
        _, verificata = tabelle.riga_gs(3)
        self.assertFalse(verificata, "GS 3 e' estrapolato e deve dichiararlo")

    def test_la_tabella_cresce(self):
        """Nessun GS che costa meno del precedente: sarebbe un errore di battitura."""
        for gs in range(2, 21):
            for campo in ("ca", "pf", "attacco", "cd"):
                with self.subTest(gs=gs, campo=campo):
                    self.assertGreaterEqual(tabelle.riga_gs(gs)[0][campo],
                                            tabelle.riga_gs(gs - 1)[0][campo])


class Provenienza(unittest.TestCase):
    def test_ogni_tabella_dichiara_la_fonte(self):
        for nome in ("TIPI", "CLASSI", "TAGLIE", "ARMATURE", "ELITE", "BASIC",
                     "INCANTESIMI", "PER_GS", "PASSI_GS"):
            with self.subTest(tabella=nome):
                self.assertIn(nome, tabelle.PROVENIENZA)
                self.assertTrue(tabelle.PROVENIENZA[nome].strip())

    def test_la_fonte_dice_quale_sistema(self):
        """Il punto della gerarchia: si vede a colpo d'occhio cosa viene da dove."""
        for nome, fonte in tabelle.PROVENIENZA.items():
            with self.subTest(tabella=nome):
                self.assertTrue("SRD" in fonte or "PF1e" in fonte, fonte)

    def test_derive_statblocks_usa_le_stesse_tabelle(self):
        """Due copie divergono. E' successo al manifest dei tool."""
        import derive_statblocks as d
        self.assertIs(d.TIPI, tabelle.TIPI)
        self.assertIs(d.CLASSI, tabelle.CLASSI)
        self.assertIs(d.PER_GS_VERIFICATE, tabelle.PER_GS_VERIFICATE)


if __name__ == "__main__":
    unittest.main()
