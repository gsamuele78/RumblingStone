"""misura_distanza_pagine: la distanza fra la scena e i numeri, letta dal PDF."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_distanza_pagine as M  # noqa: E402


class TestDistanze(unittest.TestCase):
    def test_la_mediana_delle_pagine(self):
        pp = ["zogtar zogtar zogtar entra", "niente", "niente",
              "zogtar ca 26 pf 283", "zogtar zogtar zogtar colpisce"]
        d = M.distanze(pp, "zogtar")
        self.assertEqual((d["pagine_azione"], d["mediana"], d["massima"], d["entro_una"]), (2, 2, 3, 1))

    def test_senza_numeri_non_si_misura(self):
        self.assertIsNone(M.distanze(["zogtar zogtar zogtar"], "zogtar"))

    def test_la_ca_e_i_pf_devono_stare_sulla_stessa_pagina(self):
        pp = ["zogtar zogtar zogtar", "zogtar ca 26", "pf 283"]
        self.assertIsNone(M.distanze(pp, "zogtar"))


if __name__ == "__main__":
    unittest.main()
