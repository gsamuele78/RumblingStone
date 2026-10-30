"""Il tema stampa delle mappe (ADR-0105, M7-H, 2026-10-30).

Una mappa larga 44 colonne, messa nel booklet A4, scendeva a scala 0,3: le
scritte uscivano a 3-3,8 pt e i filtri della pergamena (grana, ombre sfumate)
diventavano strati raster a 288 dpi. Il tema stampa scrive ogni corpo in
punti per una mappa larga quanto la gabbia (17,5 cm), sposta indicazioni e
legenda in un secondo SVG e non usa filtri. Il test fissa queste tre cose
sulla mappa vera che l'ha fatto nascere.
"""

import re
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import render_map_svg as R  # noqa: E402

M7H = SCRIPTS.parent / "07_il Portale Della Forgia Eterna" / "Mappe" / \
    "ARC07-MAPPE-M7H-QUARTIERE-DEL-COMANDO.md"
ALTEZZA_MAX_PT = 595  # il tetto delle figure su pagina dedicata (21 cm)


def _misure(svg: str) -> tuple[float, float, float]:
    """(larghezza, altezza, scala del gruppo) dell'SVG."""
    w, h = (float(x) for x in re.search(r'width="([\d.]+)" height="([\d.]+)"', svg).groups())
    k = re.search(r'<g transform="scale\(([\d.]+)\)">', svg)
    return w, h, float(k.group(1)) if k else 1.0


def _corpi_pt(svg: str) -> list[float]:
    """I corpi delle scritte una volta stampato l'SVG nella gabbia."""
    w, h, k = _misure(svg)
    pt_per_px = min(R.LARGHEZZA_STAMPA_PT / w, ALTEZZA_MAX_PT / h)
    return [float(c) * k * pt_per_px for c in re.findall(r'font-size="([\d.]+)"', svg)]


class TestTemaStampa(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        g = R.extract_maps(M7H.read_text(encoding="utf-8"))[0]
        cls.mappa = R.render_svg(g, M7H.name, "stampa")
        cls.legenda = R.render_svg(g, M7H.name, "stampa", "legenda")
        cls.pergamena = R.render_svg(g, M7H.name)

    def test_nessuna_scritta_sotto_i_7_pt(self):
        for nome, svg in (("mappa", self.mappa), ("legenda", self.legenda)):
            # le emoji della griglia sono disegni, non scritte: qui non ce ne sono
            self.assertGreaterEqual(min(_corpi_pt(svg)), 7.0, nome)

    def test_la_pergamena_invece_scende_a_3_pt(self):
        self.assertLess(min(_corpi_pt(self.pergamena)), 4.0)

    def test_niente_filtri_ne_vignettatura(self):
        for svg in (self.mappa, self.legenda):
            self.assertNotIn('filter="url(', svg)
            self.assertNotIn("url(#vign)", svg)

    def test_la_mappa_non_porta_la_legenda_e_viceversa(self):
        self.assertNotIn("LEGENDA", self.mappa)
        self.assertNotIn("INDICAZIONI", self.mappa)
        self.assertIn("LEGENDA", self.legenda)
        self.assertIn("INDICAZIONI", self.legenda)
        self.assertNotIn("quadretti · scala", self.legenda)

    def test_le_zone_sono_lettere_spiegate_in_legenda(self):
        self.assertNotIn("Telo del glifo", self.mappa)
        self.assertIn("Telo del glifo", self.legenda)
        self.assertRegex(self.mappa, r'font-style="italic" text-anchor="middle" fill="#2c2313">b<')

    def test_a_capo_tiene_le_parole(self):
        righe = R._a_capo("uno due tre quattro cinque", 9)
        self.assertEqual(righe, ["uno due", "tre", "quattro", "cinque"])
        self.assertEqual(" ".join(righe), "uno due tre quattro cinque")


if __name__ == "__main__":
    unittest.main()
