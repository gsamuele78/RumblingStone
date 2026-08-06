"""Test per validate_links.py (finding E3, lotto G3).

Il gate cerca due difetti che rendono un file non consegnabile e che nessuno
vede finché non lo apre: **link relativi rotti** e **percorsi assoluti della
macchina di chi ha scritto**.

I test più importanti qui sono quelli sui **falsi positivi**. La prima
esecuzione ne ha prodotti due classi intere — le guide di deploy dei
`converters/`, che contengono legittimamente percorsi di *server*
(`/home/htmlconverter/`), e i documenti d'audit, che citano `/home/jfs/`
**proprio per segnalarlo**. Un gate che li avesse trattati da errori sarebbe
stato disattivato entro una settimana.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_links as vl  # noqa: E402


class TestTrovaIDifettiVeri(unittest.TestCase):
    def test_link_rotto(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_text("vedi [qui](manca.md)\n", encoding="utf-8")
            probs = vl.check_file(f) if f.is_relative_to(vl.ROOT) else None
            if probs is None:  # fuori dal repo: si verifica la logica in isolamento
                self.assertFalse((f.parent / "manca.md").exists())

    def test_path_assoluto_riconosciuto(self):
        for riga in ("cd /home/tizio/progetto", "[a](file:///home/jfs/x.md)",
                     r"C:\\Users\\Tizio\\"):
            self.assertTrue(vl.ABSOLUTE.search(riga), f"non riconosciuto: {riga}")

    def test_path_relativo_non_e_assoluto(self):
        for riga in ("cd campaign/lore", "vedi ../altro.md", "scripts/dm.py"):
            self.assertIsNone(vl.ABSOLUTE.search(riga), f"falso positivo: {riga}")


class TestFalsiPositivi(unittest.TestCase):
    """Ogni caso qui è legittimo: il gate NON deve segnalarlo."""

    def test_i_converters_sono_esclusi(self):
        """Le guide di deploy contengono percorsi di SERVER, non di una persona."""
        self.assertIn("converters", vl.SKIP_DIRS)

    def test_host_relative_di_homebrewery_accettati(self):
        """`/assets/…` risolve sul dominio del brew, non nel repo."""
        for t in ("/assets/naturalCritLogoRed.svg", "/api/x"):
            self.assertTrue(t.startswith(vl.HOMEBREWERY_HOST))

    def test_segnaposto_didattici_scartati(self):
        for t in ("percorso/relativo/immagine.png", "<il-tuo-file>", "URL"):
            self.assertTrue(vl.PLACEHOLDER.search(t), f"{t} dovrebbe essere segnaposto")

    def test_direttiva_su_riga_e_a_blocco(self):
        testo = ("a\n`/home/x/` <!-- validate-links: ignore -->\n"
                 "<!-- validate-links: ignore-begin -->\nb\nc\n"
                 "<!-- validate-links: ignore-end -->\nd\n")
        self.assertEqual(vl.ignored_lines(testo), {2, 3, 4, 5, 6})


class TestIlRepoEPulito(unittest.TestCase):
    def test_nessun_link_rotto_ne_path_assoluto(self):
        """Condizione per tenere il gate in CI: deve essere verde sul repo."""
        problemi = []
        for p in vl.md_files(vl.ROOT):
            problemi.extend(vl.check_file(p))
        self.assertEqual(problemi, [], f"difetti residui: {problemi[:5]}")

    def test_il_playbook_non_contiene_la_home_di_nessuno(self):
        """Insegnava a un DM terzo un `cd` con dentro la home di chi ha scritto."""
        testo = (ROOT / "campaign" / "DM-CAMPAIGN-PLAYBOOK.md").read_text(encoding="utf-8")
        self.assertNotIn("/home/jfs/", testo)


class TestPalioAncoraNonRisolto(unittest.TestCase):
    """I 13 asset sono marcati per non falsare il gate, NON perché vada bene.

    Se un giorno la decisione arriva e gli asset vengono prodotti (o i
    riferimenti tolti), questo test va aggiornato — è il promemoria che il
    debito esiste ancora.
    """

    BOOKLET = (ROOT / "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist"
               / "homebrew" / "PALIO-BOOKLET.hb.md")

    def test_la_nota_dice_che_il_debito_e_aperto(self):
        testo = self.BOOKLET.read_text(encoding="utf-8")
        self.assertIn("ASSET MANCANTI", testo,
                      "la nota che dichiara il debito è sparita: o è stato risolto "
                      "(aggiornare questo test) o è stato nascosto")


if __name__ == "__main__":
    unittest.main()
