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


def _pdf(pagine: list[str], toc: list[list], cartella: Path) -> Path:
    """Un PDF minimo: una riga per ogni testo, l'indice dato."""
    import pymupdf
    doc = pymupdf.open()
    for testo in pagine:
        pg = doc.new_page(width=420, height=600)
        y = 80
        for riga in testo.splitlines():
            pg.insert_text((40, y), riga, fontsize=9)
            y += 14
    doc.set_toc(toc)
    out = cartella / "prova.pdf"
    doc.save(out)
    return out


try:
    import pymupdf  # noqa: F401
    PYMUPDF = True
except ImportError:
    PYMUPDF = False


@unittest.skipUnless(PYMUPDF, "serve PyMuPDF")
class TestVolume(unittest.TestCase):
    """Lo standard del volume (ADR-0122) su un PDF costruito qui."""

    def setUp(self):
        import tempfile
        self.tmp = Path(tempfile.mkdtemp())
        pagine = [
            "Antefatto\nTutto comincia con una guerra.",
            "I · La valle\n" + "Introduzione al capitolo, con la sintesi.\n" * 20 + "A1. La porta\nTesto.",
            "A2. La sala\nTesto.",
            "B1. La cripta\nTesto.",
            "Appendice: le terre della valle\nLuoghi.",
            "Appendice: i PNG\nSchede.",
        ]
        toc = [[1, "Antefatto", 1], [1, "I · La valle", 2], [2, "A1. La porta", 2],
               [2, "A2. La sala", 3], [2, "B1. La cripta", 4],
               [1, "Appendice: le terre della valle", 5], [1, "Appendice: i PNG", 6]]
        self.pdf = _pdf(pagine, toc, self.tmp)

    def test_s1_conta_l_introduzione_fino_al_primo_sottotitolo(self):
        m = M.misura_volume(self.pdf, None, [])
        self.assertTrue(m["S1"]["intro_volume"])
        self.assertEqual(m["S1"]["capitoli"], 1)
        self.assertGreater(m["S1"]["intro_caratteri"][0], 500)

    def test_s2_e_s3_con_le_mappe_annotate(self):
        annot = {"mappe": [{"pagina": 2, "codici": ["A1", "A2", "A9"]}]}
        m = M.misura_volume(self.pdf, annot, [])
        self.assertEqual(m["S2"]["solo_testo"], ["B1"])
        self.assertEqual(m["S2"]["solo_mappa"], ["A9"])
        self.assertEqual((m["S3"]["n"], m["S3"]["entro_una"]), (2, 1.0))

    def test_s2_le_nostre_mappe_senza_chiavi(self):
        m = M.misura_volume(self.pdf, None, [])
        self.assertEqual((m["S2"]["nel_testo"], m["S2"]["sulla_mappa"]), (3, 0))

    def test_s4_legge_le_appendici_dall_indice(self):
        m = M.misura_volume(self.pdf, None, [])
        self.assertEqual((m["S4"]["regione"], m["S4"]["png"]), (True, True))

    def test_sotto_soglia_dice_che_cosa_manca(self):
        m = M.misura_volume(self.pdf, None, [])
        righe = M.sotto_soglia(m, M.carica_soglie())
        self.assertTrue(any(r.startswith("S2") for r in righe))
        self.assertFalse(any(r.startswith("S4") for r in righe))


class TestSoglie(unittest.TestCase):
    def test_le_soglie_vengono_dai_riferimenti(self):
        import json
        s = json.loads(M.SOGLIE.read_text(encoding="utf-8"))
        rif = s["riferimenti"]
        minimo_intro = min(x for r in rif.values() for x in r["S1_intro_caratteri"])
        self.assertLessEqual(s["soglie"]["S1_intro_min_caratteri"], minimo_intro)
        minimo_s3 = min(r["S3_entro_una"] for r in rif.values())
        self.assertLessEqual(s["soglie"]["S3_quota_entro_una"], minimo_s3)

    def test_le_annotazioni_dei_riferimenti_esistono(self):
        cartella = ROOT / "plans/esperimenti/standard-volume-2026-11-10/riferimenti"
        self.assertEqual(sorted(f.name for f in cartella.glob("*.json")),
                         ["burnt-offerings.json", "red-hand-of-doom-estratto.json"])


if __name__ == "__main__":
    unittest.main()
