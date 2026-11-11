"""Le misure nate dal giro di lettura del 2026-11-10 (canale di prova):
sigle d'appendice morte, righe d'incontro incomplete, titoli che hanno perso
l'apostrofo, e le pedine delle mappe collegate alle schede."""
import json
import unittest
from pathlib import Path

import misura_mappe_schede as M
import misura_stampa as MS

ROOT = Path(__file__).resolve().parents[2]


class _Pagina:
    def __init__(self, testo):
        self.testo = testo

    def get_text(self, come="text"):
        if come == "blocks":
            return [(0, 0, 0, 0, b) for b in self.testo.split("\n\n")]
        return self.testo


class TestLettura(unittest.TestCase):
    def test_sigla_morta_e_sigla_viva(self):
        doc = [_Pagina("Vedi Appendice A.3 e Appendice B.\n"), _Pagina("A.3 Durin\nscheda\n")]
        self.assertEqual([s for _, s in MS.sigle_morte(doc)], ["Appendice B"])

    def test_riga_breve_senza_attacchi(self):
        doc = [_Pagina("Worg GS 2 scheda a pagina 9 CA 14 · pf 30\n\n"
                       "Wyvern GS 6 scheda a pagina 9 CA 18 · Iniz +1 · TS Temp +8 · Mischia pungiglione +10 (1d6+4)")]
        manca = MS.righe_brevi_incomplete(doc)
        self.assertEqual(len(manca), 1)
        self.assertIn("iniziativa", manca[0][2])

    def test_titolo_senza_apostrofo(self):
        doc = [_Pagina("ATTO III · LALBA\nAll'alba le mura tacciono. La lama resta nel fodero: LAMA.")]
        self.assertEqual([t for _, t in MS.titoli_rovinati(doc)], ["LALBA"])


class TestMappeESchede(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.indice = M.indice_schede()
        cls.misure = {m: M.misura(m, cls.indice) for m in M.mappe()}

    def test_nessun_collegamento_rotto(self):
        rotte = [(m.name, r) for m, v in self.misure.items() for r in v["dettaglio"]["rotte"]]
        self.assertEqual(rotte, [])

    def test_la_taglia_sulla_pianta_e_quella_della_scheda(self):
        discordi = [(m.name, r) for m, v in self.misure.items() for r in v["dettaglio"]["taglie_discordi"]]
        self.assertEqual(discordi, [])

    def test_il_registro_e_aggiornato(self):
        registro = json.loads(M.REGISTRO.read_text(encoding="utf-8"))["totale"]
        totale = {k: sum(v[k] for v in self.misure.values()) for k in M.MISURE}
        self.assertEqual(registro, totale, "python3 scripts/misura_mappe_schede.py --aggiorna")

    def test_la_proposta_non_attraversa_i_moduli(self):
        m = next(x for x in M.mappe() if x.name == "GSC-3-QUOTA-MEDIA-E-FONDO.json")
        p = M.proposta({"name": "Chuul avanzato"}, m, self.indice)
        self.assertTrue(p is None or "PF1e" not in p, p)


if __name__ == "__main__":
    unittest.main()
