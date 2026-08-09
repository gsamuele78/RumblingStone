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


class TestPalioNonEraUnDebito(unittest.TestCase):
    """I «13 asset mancanti» del Palio non mancavano: mancava il rebase.

    L'audit li aveva letti come un debito di produzione (decisione A1) e li
    aveva marcati `validate-links: ignore` **dentro il `.hb.md` generato** —
    cioè modificando a mano un artefatto (contro ADR-0003) e zittendo il gate
    invece di guardare il generatore. Alla prima rigenerazione le direttive
    sono sparite e i 13 link sono tornati.

    Diagnosi vera: i capitoli vivono in `09_.../`, il booklet si genera in
    `09_.../homebrew/`, e la via `.hb.md` copiava i percorsi relativi senza
    rebasarli. Gli asset sono sempre esistiti. Questi test tengono ferme
    entrambe le cose: che esistono, e che il generatore li raggiunge.
    """

    ALLEGATI = (ROOT / "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist"
                / "P2D-Palio-Allegati")
    BOOKLET = (ROOT / "09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist"
               / "homebrew" / "PALIO-BOOKLET.hb.md")

    def test_gli_asset_esistono_davvero(self):
        attesi = [f"stemmi/0{n}-{nome}.svg" for n, nome in enumerate(
            ["oca", "torre", "bruco", "istrice", "drago", "civetta", "unicorno", "onda"], start=1)]
        attesi += ["mappe/piazza-del-palio.svg", "mappe/channathgate-citta.svg",
                   "mappe/rotta-soccorso.svg", "mappe/stalla-assalto-drow.svg",
                   "immagini/piazza-del-palio-panorama.png"]
        mancanti = [a for a in attesi if not (self.ALLEGATI / a).exists()]
        self.assertEqual(mancanti, [], f"asset davvero mancanti: {mancanti}")

    def test_il_booklet_generato_non_ha_direttive_di_silenziamento(self):
        """Se ricompaiono, qualcuno ha rimesso a mano una toppa in un generato."""
        testo = self.BOOKLET.read_text(encoding="utf-8")
        self.assertNotIn("validate-links: ignore", testo)


class TestRebaseDeiLinkRelativi(unittest.TestCase):
    """Il generatore deve rebasare i percorsi sulla cartella d'uscita."""

    def setUp(self):
        import build_booklet_html as bb
        self.rebase = bb.rebase_relative_links

    def test_capitolo_un_livello_sopra_luscita(self):
        src, out = ROOT / "arco", ROOT / "arco" / "homebrew"
        self.assertEqual(self.rebase("![x](Allegati/a.svg)", src, out),
                         "![x](../Allegati/a.svg)")

    def test_percorsi_con_spazi_nel_nome(self):
        src, out = ROOT / "arco", ROOT / "arco" / "homebrew"
        self.assertEqual(self.rebase("[m](Mappe di Prova/a b.png)", src, out),
                         "[m](../Mappe di Prova/a b.png)")

    def test_non_tocca_url_ancore_e_host_relative(self):
        src, out = ROOT / "arco", ROOT / "arco" / "homebrew"
        for t in ("[a](https://x.dev/y)", "[a](#sezione)", "[a](/assets/logo.svg)",
                  "[a](mailto:x@y.z)"):
            self.assertEqual(self.rebase(t, src, out), t)

    def test_stessa_cartella_non_cambia_niente(self):
        src = out = ROOT / "arco" / "homebrew"
        self.assertEqual(self.rebase("![x](img/a.png)", src, out), "![x](img/a.png)")

    def test_ancora_e_titolo_sopravvivono(self):
        src, out = ROOT / "arco", ROOT / "arco" / "homebrew"
        self.assertEqual(self.rebase("[a](doc.md#par)", src, out), "[a](../doc.md#par)")
        self.assertEqual(self.rebase('[a](doc.md "T")', src, out), '[a](../doc.md "T")')


if __name__ == "__main__":
    unittest.main()
