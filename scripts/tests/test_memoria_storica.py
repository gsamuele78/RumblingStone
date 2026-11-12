"""Test di memoria_storica.py (ADR-0127): la storia che esce dalla memoria corta."""
from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import memoria_storica as ms  # noqa: E402

TESTO = """# Memoria storica

Intestazione con un esempio che non è una voce: ### MS-9999 · finto

## Voci

### MS-0001 · 2026-10-19 · Duello con Skullcrusher

- **Data:** 2026-10-19
- **PR:** #257 #242
- **ADR:** —
- **Temi:** arc07 skullcrusher
- **Origine:** memoria del progetto
- **Testo:** Virata al posto di Ghermire; la presa in bocca è di Fauci (PR #242).

### MS-0002 · 2026-10-23 · Città della valle

- **Data:** 2026-10-23
- **PR:** —
- **ADR:** ADR-0102
- **Temi:** mappe citta
- **Origine:** memoria del progetto
- **Testo:** Rethmar capitale, Channathgate la più popolosa.
"""


class TestLettura(unittest.TestCase):
    def setUp(self):
        self.voci = ms.leggi(TESTO)

    def test_legge_le_voci_e_i_campi(self):
        self.assertEqual([v.id for v in self.voci], ["MS-0001", "MS-0002"])
        self.assertEqual(self.voci[0].pr, {257, 242})
        self.assertEqual(self.voci[1].adr, {102})
        self.assertEqual(self.voci[1].temi, ["mappe", "citta"])

    def test_filtri(self):
        self.assertEqual([v.id for v in ms.filtra(self.voci, pr=242)], ["MS-0001"])
        self.assertEqual([v.id for v in ms.filtra(self.voci, adr=102)], ["MS-0002"])
        self.assertEqual([v.id for v in ms.filtra(self.voci, tema="ARC07")], ["MS-0001"])
        self.assertEqual([v.id for v in ms.filtra(self.voci, da="2026-10-20")], ["MS-0002"])
        self.assertEqual([v.id for v in ms.filtra(self.voci, a="2026-10-20")], ["MS-0001"])

    def test_le_parole_non_badano_ad_accenti_e_maiuscole(self):
        self.assertEqual([v.id for v in ms.filtra(self.voci, ["citta", "CHANNATHGATE"])], ["MS-0002"])
        self.assertEqual(ms.filtra(self.voci, ["citta", "Fauci"]), [])

    def test_il_numero_della_pr_non_prende_un_prefisso(self):
        self.assertEqual(ms.filtra(self.voci, pr=24), [])


class TestCancello(unittest.TestCase):
    def test_file_in_forma_passa(self):
        self.assertEqual(ms.controlla(TESTO, "vedi MEMORIA-STORICA.md"), [])

    def test_numeri_fuori_sequenza(self):
        e = ms.controlla(TESTO.replace("MS-0002", "MS-0003"), None)
        self.assertTrue(any("fuori sequenza" in x for x in e), e)

    def test_campo_mancante_e_data_sbagliata(self):
        rotto = TESTO.replace("- **Temi:** mappe citta\n", "").replace("2026-10-23 · Città", "23/10 · Città")
        e = ms.controlla(rotto, None)
        self.assertTrue(any("Temi" in x for x in e), e)
        self.assertTrue(any("AAAA-MM-GG" in x for x in e), e)

    def test_il_changelog_deve_portare_al_file(self):
        e = ms.controlla(TESTO, "nessun collegamento")
        self.assertTrue(any("CHANGELOG" in x for x in e), e)

    def test_il_file_vero_e_in_forma(self):
        self.assertEqual(ms.main(["--check"]), 0)


class TestRiga(unittest.TestCase):
    def test_json_e_data_non_valida(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "M.md"
            f.write_text(TESTO, encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(ms.main(["--file", str(f), "--json", "--pr", "257"]), 0)
            self.assertIn('"id": "MS-0001"', out.getvalue())
            self.assertEqual(ms.main(["--file", str(f), "--da", "19/10"]), 2)


if __name__ == "__main__":
    unittest.main()
