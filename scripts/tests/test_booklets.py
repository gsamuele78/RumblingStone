"""Il gate dei booklet e la conversione markdown → Typst.

Perché questi test esistono: in CI **c'è** typst (dal 2026-08-22) e i volumi si
compilano davvero, ma la compilazione dice solo «sì» o «no». Questi test dicono
*cosa* deve uscire — e coprono, uno per uno, i difetti che erano arrivati fino
ai booklet pubblicati:

  * un'immagine stampata come testo (`!Stemma Oca`);
  * grassetto attaccato a una barra che rompeva l'intero volume;
  * una chiave di manifest che una catena legge e l'altra ignora in silenzio.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from export_booklet_typst import dimensioni, inline, md_to_typ  # noqa: E402
from validate_booklets import carica_schema, controlla_manifest, manifest_del_repo  # noqa: E402


class TestImmagini(unittest.TestCase):
    """`![alt](src)` deve diventare una figura, non il testo dell'alt."""

    def setUp(self):
        # La cartella temporanea sta DENTRO il repo: con `--root`, Typst vede
        # solo ciò che sta sotto la radice, e un percorso in /tmp non sarebbe
        # stampabile — il che è la ragione per cui esiste `typ_path`.
        self._tmp = tempfile.TemporaryDirectory(dir=REPO)
        self.base = Path(self._tmp.name)
        # un PNG 4x2 vero: serve la testa IHDR, non il resto
        self.png = self.base / "largo.png"
        self.png.write_bytes(
            b"\x89PNG\r\n\x1a\n" + (13).to_bytes(4, "big") + b"IHDR"
            + (400).to_bytes(4, "big") + (100).to_bytes(4, "big") + b"\x08\x06\x00\x00\x00"
        )
        self.alto = self.base / "alto.png"
        self.alto.write_bytes(
            b"\x89PNG\r\n\x1a\n" + (13).to_bytes(4, "big") + b"IHDR"
            + (100).to_bytes(4, "big") + (400).to_bytes(4, "big") + b"\x08\x06\x00\x00\x00"
        )

    def tearDown(self):
        self._tmp.cleanup()

    def test_dimensioni_png(self):
        self.assertEqual(dimensioni(self.png), (400, 100))

    def test_orizzontale_scavalca_le_colonne(self):
        out = md_to_typ("![Pianta della città](largo.png)", self.base)
        self.assertIn("#figura(", out)
        self.assertIn("larga: true", out)
        self.assertIn("didascalia: [Pianta della città]", out)

    def test_verticale_resta_in_colonna(self):
        out = md_to_typ("![Ritratto](alto.png)", self.base)
        self.assertIn("#figura(", out)
        self.assertNotIn("larga: true", out)

    def test_immagine_mancante_non_e_un_buco_silenzioso(self):
        out = md_to_typ("![Stemma Oca](non-esiste.png)", self.base)
        self.assertNotIn("!Stemma Oca", out)      # il difetto originale
        self.assertIn("immagine mancante", out)

    def test_senza_base_le_immagini_restano_fuori(self):
        """Le schede pregenerate passano dal loro lettore: lì `base` non c'è."""
        self.assertNotIn("#figura(", md_to_typ("![x](y.png)"))

    def test_immagine_in_mezzo_a_una_riga(self):
        out = md_to_typ("Testo prima ![Ritratto](alto.png) testo dopo.", self.base)
        self.assertIn("#figura(", out)
        self.assertIn("Testo prima", out)
        self.assertIn("testo dopo.", out)


class TestEnfasi(unittest.TestCase):
    """I due casi per cui due booklet della campagna non compilavano."""

    def test_grassetto_attaccato_a_una_barra(self):
        self.assertEqual(inline("(il **Seggio**/Deputazione)"),
                         "(il #strong[Seggio]/Deputazione)")

    def test_corsivo_che_contiene_grassetto(self):
        self.assertEqual(inline("*Il peso **(nota.)***"),
                         "#emph[Il peso #strong[(nota.)]]")

    def test_asterisco_che_non_e_enfasi(self):
        self.assertEqual(inline("3 * 4 caselle"), "3 \\* 4 caselle")

    def test_enfasi_mai_chiusa_non_esce_dal_paragrafo(self):
        """Un master con un asterisco dispari non deve mangiarsi il resto."""
        self.assertTrue(inline("**aperto e mai chiuso").endswith("]"))


class TestCapolettera(unittest.TestCase):

    def test_solo_su_un_paragrafo_abbastanza_lungo(self):
        lungo = "Nel mezzo del cammino di nostra vita mi ritrovai per una selva " \
                "oscura, ché la diritta via era smarrita, e non è cosa da dire."
        self.assertIn("#capolettera(\"N\"", md_to_typ(lungo, capolettera=True))

    def test_un_cappello_di_due_righe_resta_com_e(self):
        self.assertNotIn("#capolettera(", md_to_typ("Due righe soltanto.", capolettera=True))


class TestManifestDelRepo(unittest.TestCase):
    """Il gate, sui manifest veri: è il test che tiene onesta la parità."""

    @classmethod
    def setUpClass(cls):
        cls.schema = carica_schema()
        cls.elenco = manifest_del_repo()

    def test_ci_sono_manifest_da_controllare(self):
        self.assertGreaterEqual(len(self.elenco), 5)

    def test_tutti_i_manifest_del_repo_sono_validi(self):
        for m in self.elenco:
            with self.subTest(manifest=m.name):
                errori, _ = controlla_manifest(m, self.schema)
                self.assertEqual(errori, [])

    def test_una_chiave_inventata_viene_rifiutata(self):
        with tempfile.TemporaryDirectory() as d:
            cap = Path(d) / "c.md"
            cap.write_text("# c\n\ntesto\n", encoding="utf-8")
            mp = Path(d) / "X.manifest.json"
            mp.write_text(json.dumps({"title": "x", "chapters": [{"file": "c.md"}],
                                      "cover_imagee": "z.png"}), encoding="utf-8")
            errori, _ = controlla_manifest(mp, self.schema)
            self.assertTrue(any("cover_imagee" in e for e in errori))

    def test_un_master_mancante_viene_rifiutato(self):
        with tempfile.TemporaryDirectory() as d:
            mp = Path(d) / "X.manifest.json"
            mp.write_text(json.dumps({"title": "x", "chapters": [{"file": "manca.md"}]}),
                          encoding="utf-8")
            errori, _ = controlla_manifest(mp, self.schema)
            self.assertTrue(any("master mancante" in e for e in errori))


if __name__ == "__main__":
    unittest.main()
