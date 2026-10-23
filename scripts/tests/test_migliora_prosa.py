"""La pipeline migliora_prosa: modello di preferenza, filtro, scheda cieca, esito."""
from __future__ import annotations

import importlib.util
import json
import math
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _mp():
    spec = importlib.util.spec_from_file_location(
        "migliora_prosa", ROOT / "scripts" / "migliora_prosa.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._NLP = False          # senza spaCy: test veloci e uguali ovunque
    return mod


MP = _mp()

ORIGINALE = ("Il vecchio alza la testa e guarda la luce dietro Thorik. Un fabbro con una "
             "gamba sola si tira su contro il muro, e il muro gli si apre sotto la mano come "
             "argilla. Ottocento nani guardano un nano con una corona, e nel cortile c'è solo "
             "il respiro della forgia.")


class TestModello(unittest.TestCase):
    def test_simmetrico(self):
        Z = [[1.0, 0.2], [0.5, -0.3], [2.0, 0.1], [-0.2, 0.4]]
        m = MP.addestra(Z)
        for z in ([0.7, 0.1], [-1.0, 2.0]):
            self.assertAlmostEqual(MP.probabilita(m, z) + MP.probabilita(m, [-v for v in z]), 1.0)

    def test_impara_il_tratto_che_decide(self):
        # il primo tratto è sempre positivo per chi vince, il secondo è rumore
        Z = [[1.0 + i % 3, (-1) ** i * 0.5] for i in range(20)]
        m = MP.addestra(Z)
        self.assertGreater(m["pesi"][0], 0)
        self.assertGreater(abs(m["pesi"][0]), abs(m["pesi"][1]))
        self.assertGreater(MP.probabilita(m, [1.5, 0.0]), 0.5)

    def test_risolvi(self):
        x = MP._risolvi([[2.0, 1.0], [1.0, 3.0]], [3.0, 5.0])
        self.assertAlmostEqual(x[0], 0.8)
        self.assertAlmostEqual(x[1], 1.4)

    def test_test_del_segno(self):
        self.assertEqual(MP.binom_p(0, 0), 1.0)
        self.assertAlmostEqual(MP.binom_p(5, 10), 1.0)
        self.assertLess(MP.binom_p(10, 10), 0.01)

    def test_valida_su_un_dataset_piccolo(self):
        corto, lungo = "Pietra fredda.", "Pietra fredda, nera e silenziosa sotto la luce del fuoco."
        voti = [{"pari": False, "vincente": lungo, "perdente": corto, "originale": corto}
                for _ in range(6)] + [{"pari": True, "vincente": corto, "perdente": lungo,
                                       "originale": corto}]
        r = MP.valida(voti)
        self.assertEqual(r["coppie"], 6)
        self.assertEqual(r["pari_esclusi"], 1)
        self.assertEqual(r["piu_lunga"], 6)
        self.assertFalse(r["supera_soglia"])   # non batte «vince la più lunga»
        self.assertIn("NON superata", MP.rapporto(r))


class TestFiltro(unittest.TestCase):
    def test_passa_una_riscrittura_leggera(self):
        c = ORIGINALE.replace("Il vecchio alza", "Accanto all'incudine il vecchio alza")
        self.assertEqual(MP.filtra(ORIGINALE, c), [])

    def test_numero_cambiato(self):
        o = ORIGINALE.replace("Ottocento", "800")
        c = o.replace("800", "900")
        self.assertTrue(any(m.startswith("fatto cambiato") for m in MP.filtra(o, c)))

    def test_sensi_tolti(self):
        c = ORIGINALE.replace("guarda la luce dietro Thorik", "guarda Thorik") \
                     .replace(" c'è solo il respiro della forgia", " non si muove nessuno")
        motivi = MP.filtra(ORIGINALE, c)
        self.assertTrue(any("sensoriali" in m or "impoverito" in m for m in motivi), motivi)

    def test_frase_finale_tolta(self):
        c = ORIGINALE.rsplit(" Ottocento", 1)[0]
        self.assertTrue(MP.frase_finale_tolta(ORIGINALE, c))
        self.assertIn("regola 3, frase finale tolta", MP.filtra(ORIGINALE, c))

    def test_monologo_spezzato(self):
        o = "«Prendi la gemma, socio. Incastonala nell'Anello e avrai lo sconto a vita.»"
        c = "«Prendi la gemma, socio.»\n\n*La gemma si scalda.*\n\n«Incastonala nell'Anello: sconto a vita.»"
        self.assertTrue(MP.monologo_spezzato(o, c))

    def test_subordinata_spezzata_senza_parser(self):
        o = "Il fabbro si tira su contro il muro che gli si apre sotto la mano."
        c = "Il fabbro si tira su contro il muro. Il muro gli si apre sotto la mano."
        self.assertTrue(MP.subordinata_spezzata(o, c))
        self.assertFalse(MP.subordinata_spezzata(c, o))


class TestCandidate(unittest.TestCase):
    def test_in_chiaro_e_in_box(self):
        testo = ("# P01\n\n## Candidata 1\n\nUna riga\nche continua.\n\n"
                 "## Candidata 2\n\n> *Un box citato*\n> *che continua.*\n\n<!-- nota -->\n")
        self.assertEqual(MP.leggi_candidate(testo), ["Una riga che continua.",
                                                     "Un box citato che continua."])

    def test_migliora_sceglie_fra_le_buone(self):
        buona = ORIGINALE.replace("Il vecchio alza", "Accanto all'incudine il vecchio alza")
        cattiva = ORIGINALE.rsplit(" Ottocento", 1)[0]
        m = MP.addestra([[0.0] * len(MP.TRATTI)])
        r = MP.migliora(ORIGINALE, [cattiva, buona], m)
        self.assertEqual(r["vincitrice"], 2)
        self.assertTrue(r["candidate"][0]["scartata"])


class TestDataset(unittest.TestCase):
    SCHEDA = ("# Scheda\n\n## Parte 1 — 2 coppie\n\n## Coppia 1\n\n*Box B01*\n\n**A**\n\n> uno A\n>\n> due A\n\n"
              "**B**\n\n> uno B\n\n## Coppia 2\n\n*Box B02*\n\n**A**\n\n> x A\n\n**B**\n\n> x B\n\n"
              "## Parte 2 — 1 coppie\n\n## Coppia 1\n\n*Box B01*\n\n**A**\n\n> p2 A\n\n**B**\n\n> p2 B\n")

    def test_scheda_a_piu_parti(self):
        p = MP._voci_scheda(self.SCHEDA)
        self.assertEqual(p[1][1], ("Box B01", "uno A\n\ndue A", "uno B"))
        self.assertEqual(p[2][1][1], "p2 A")

    def test_coppie_con_chiave_voti_ed_etichette(self):
        chiave = {"coppie": [{"n": 1, "nuova": "A", "stato": "valida"},
                             {"n": 2, "nuova": "B", "stato": "valida"}]}
        out = MP.coppie_da_scheda(self.SCHEDA, chiave, "1 B ritmo goffo\n2 =\n", "prova", 1,
                                  {"B01": "orig"}, "V", "N")
        self.assertEqual(out[0]["vincente"], "uno B")
        self.assertEqual(out[0]["ruolo_vincente"], "V")
        self.assertEqual(out[0]["etichette_sulla_perdente"], ["ritmo", "goffo"])
        self.assertEqual(out[0]["originale"], "orig")
        self.assertTrue(out[1]["pari"])

    def test_dataset_del_repo(self):
        coppie = MP.dataset()
        self.assertGreaterEqual(len(coppie), 55)
        for v in coppie:
            for k in ("id", "fonte", "pari", "vincente", "perdente", "originale"):
                self.assertIn(k, v)
        self.assertEqual(len({v["id"] for v in coppie}), len(coppie))


class TestCampioneEdEsito(unittest.TestCase):
    def test_giro_completo(self):
        scelte = {"box": [{"id": "P01", "file": "x.md", "box": 0, "titolo": "Scena",
                           "originale": ORIGINALE, "vincitrice": 1,
                           "candidate": [{"n": 1, "testo": ORIGINALE.replace(
                               "Il vecchio alza", "Accanto all'incudine il vecchio alza")}]}]}
        scheda, chiave = MP.campione(scelte, 3)
        self.assertIn("## Coppia 1", scheda)
        self.assertIn("*Box P01*", scheda)
        self.assertNotIn("_testi-provvisori", scheda)
        self.assertFalse((MP.PIPE / "cieco" / "_testi-provvisori.md").exists())
        voto = chiave["coppie"][0]["nuova"]
        r, nuove = MP.registra_esito(scelte, chiave, f"1 {voto}\n", "2026-10-22")
        self.assertEqual(r["nuova"], 1)
        self.assertEqual(nuove[0]["ruolo_vincente"], "pipeline")
        self.assertEqual(nuove[0]["perdente"], ORIGINALE)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "VOTI.json"
            MP.scrivi_voti(nuove, p)
            self.assertEqual(MP.carica_voti(p)[0]["fonte"], "pipeline-2026-10-22")


if __name__ == "__main__":
    unittest.main()
