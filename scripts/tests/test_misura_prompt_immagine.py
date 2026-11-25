"""Test del misuratore dei prompt d'immagine (ADR-0150).

Ogni regola si prova in rosso su un caso costruito apposta e in verde sulle
didascalie vere del Drappo: un misuratore che non boccia niente non misura.
"""
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location("misura_prompt_immagine", REPO / "scripts" / "misura_prompt_immagine.py")
mpi = importlib.util.module_from_spec(spec)
sys.modules["misura_prompt_immagine"] = mpi
spec.loader.exec_module(mpi)

PROMPTS = REPO / "10-stand-alone/Il-Drappo-di-Tarsilia/ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md"

BUONA = (
    "Waist-up portrait painting of an old ferryman seen at eye level. He holds a long pole in both hands, "
    "his knuckles swollen and his palms dark with river mud. Behind him the river is grey and wide under "
    "a low sky. A single lantern lights him from the left, warm on his cheek, while cool evening air "
    "outlines his shoulder. His coat is patched wool the colour of wet ochre, fastened with a rope belt. "
    "Style: northern renaissance oil glazing, visible brushwork. Mood: patient, tired."
)


def errori(testo):
    return mpi.misura("x", testo).errori


ROTTE = {
    "manca la sorgente di luce": BUONA.replace(
        "A single lantern lights him from the left, warm on his cheek, "
        "while cool evening air outlines his shoulder.", "Evening falls."),
    "negazione": BUONA.replace("Behind him the river is grey", "Behind him, with no boats, the river is grey"),
    "etichetta di qualità": BUONA.replace("His coat is patched wool", "Masterpiece. His coat is patched wool"),
    "nome di un autore": BUONA.replace("Style: northern renaissance",
                                       "Style: in the style of Someone, northern renaissance"),
    "direzione": BUONA.replace("from the left", "softly"),
}


class TestMisuraPromptImmagine(unittest.TestCase):
    def test_una_didascalia_buona_passa(self):
        self.assertEqual(errori(BUONA), [])

    def test_le_didascalie_del_drappo_passano(self):
        didascalie = mpi.leggi(PROMPTS)
        self.assertEqual(set(didascalie), {"ritratto-vanna", "tavola-la-ruota", "il-drappo"})
        for ident, testo in didascalie.items():
            with self.subTest(ident):
                self.assertEqual(mpi.misura(ident, testo).errori, [])

    def test_il_prompt_a_etichette_di_prima_e_bocciato(self):
        """Il prompt composto della Ruota usato nel collaudo del 21/11."""
        vecchio = ("northern renaissance oil glazing, flemish panel painting light, egg-tempera restraint in the "
                   "flesh tones, epic fantasy matte-painting, high three-quarter aerial view of a medieval river-town "
                   "square, a wide ring of packed earth around a large covered grain market at the centre, eight "
                   "coloured banners on the outer galleries, dense crowd pressed against wooden barriers, eight "
                   "bareback riders mid-turn, dust, late-summer golden hour, atmospheric perspective, no text")
        e = " ".join(errori(vecchio))
        for atteso in ("non è prosa", "Style", "negazione"):
            self.assertIn(atteso, e)

    def test_ogni_regola_morde(self):
        for atteso, rotta in ROTTE.items():
            with self.subTest(atteso):
                self.assertNotEqual(rotta, BUONA)
                self.assertTrue(any(atteso in r for r in errori(rotta)), errori(rotta))

    def test_segnaposto_e_lunghezza(self):
        e = errori("[look comune] + woman, dust. Style: x. Mood: y.")
        self.assertTrue(any("segnaposto" in r for r in e))
        self.assertTrue(any("troppo corta" in r for r in e))

    def test_check_esce_1_su_un_errore(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "p.json"
            f.write_text('{"a": "dust, golden hour, no text"}', encoding="utf-8")
            g = Path(d) / "q.json"
            g.write_text(json.dumps({"a": BUONA}), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(mpi.main([str(f), "--check"]), 1)
                self.assertEqual(mpi.main([str(g), "--check"]), 0)


if __name__ == "__main__":
    unittest.main()
