"""Le misure nate dal giro di lettura del 2026-11-10 (canale di prova):
sigle d'appendice morte, righe d'incontro incomplete, titoli che hanno perso
l'apostrofo, e le pedine delle mappe collegate alle schede."""
import json
import re
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


class TestFoglioDellaSerata(unittest.TestCase):
    """La pagina unica di sessione (le otto voci del «Lazy DM» di M. Shea,
    meno i personaggi, che sono nelle schede dei PG): sta in una pagina solo
    se resta corta, e serve solo se le voci ci sono tutte."""
    VOCI = ("Si comincia così", "Le scene possibili", "Segreti e indizi", "I luoghi", "Chi c'è", "Il tesoro")

    def test_le_voci_ci_sono_e_la_pagina_resta_una(self):
        fogli = sorted(ROOT.glob("**/homebrew/**/00-FOGLIO-DELLA-SERATA.md"))
        self.assertTrue(fogli)
        for f in fogli:
            testo = f.read_text(encoding="utf-8")
            for voce in self.VOCI:
                self.assertIn(f"**{voce}", testo, f"{f.name}: manca «{voce}»")
            # 520 parole: quante ne stanno in una pagina a due colonne col titolo
            self.assertLessEqual(len(testo.split()), 520, f.name)


class TestSchedaDaTavolo(unittest.TestCase):
    """La scheda che apre una scena (prova del 2026-11-12, scelta del DM): le
    voci fisse dei blocchi d'incontro degli AP (creature, sviluppo, tesoro) più
    il rimando al testo intero. Sta nella pagina del titolo solo se resta
    corta, ed esce solo nel booklet di serata."""
    VOCI = ("Chi c'è", "Sviluppo", "Tesoro", "Dove guardare")
    BLOCCO = re.compile(r"<!-- scheda-da-tavolo -->(.*?)<!-- /scheda-da-tavolo -->", re.S)

    def test_le_voci_ci_sono_e_la_scheda_resta_corta(self):
        master = ROOT / "07_il Portale Della Forgia Eterna" / "ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md"
        schede = self.BLOCCO.findall(master.read_text(encoding="utf-8"))
        self.assertEqual(len(schede), 6, "una scheda per ognuna delle Scene 6-11")
        for s in schede:
            for voce in self.VOCI:
                self.assertIn(f"| **{voce}** |", s)
            # 500 parole: la più lunga che sta nella pagina del titolo (Scena 11)
            self.assertLessEqual(len(s.split()), 500, s[:60])

    def test_nel_volume_intero_non_esce(self):
        from dmcore.testo import leggi_per_la_stampa
        master = ROOT / "07_il Portale Della Forgia Eterna" / "ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md"
        self.assertNotIn("La scheda da tavolo**:", leggi_per_la_stampa(master, {}))
        self.assertIn("La scheda da tavolo**:", leggi_per_la_stampa(master, {}, ["SCENA 8"]))


if __name__ == "__main__":
    unittest.main()
