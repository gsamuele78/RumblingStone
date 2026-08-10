"""Test per validate_pg.py e le schede PG (lotto G14).

Il test che vale tutti gli altri è `test_riprodurrebbe_il_difetto_originale`:
toglie dalla scheda di Thorik il −2 DES della Corona e pretende che il gate se
ne accorga. Se un giorno smette di accorgersene, il gate è decorativo — ed è
esattamente il difetto che è rimasto invisibile per tre generazioni di schede.
"""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_pg as vp  # noqa: E402


class TestIlRepoEPulito(unittest.TestCase):
    def test_il_gate_passa(self):
        self.assertEqual(vp.main([]), 0)

    def test_ci_sono_tutti_e_quattro_i_pg(self):
        nomi = {d["pg"] for d in vp.schede().values()}
        self.assertEqual(nomi, {"Thorik", "Tordek", "Hella", "Artemis"},
                         "un PG senza scheda è un PG i cui costi possono sparire")


class TestFontiEAritmetica(unittest.TestCase):
    def test_ogni_modificatore_ha_una_fonte_apribile(self):
        for nome, dati in vp.schede().items():
            for mod in dati.get("modificatori_permanenti") or []:
                self.assertTrue(
                    (ROOT / mod["fonte"]).exists(),
                    f"{nome}: fonte inesistente {mod['fonte']}")

    def test_la_catena_della_des_di_thorik_torna(self):
        """10 base → 8 (Corona indossata) → 6 (rito dello Smeraldo)."""
        t = vp.schede()["thorik"]
        des = t["caratteristiche"]["des"]
        self.assertEqual((des["base"], des["attuale"]), (10, 6))
        delta = sum(m["delta"] for m in t["modificatori_permanenti"]
                    if m["caratteristica"] == "DES")
        self.assertEqual(delta, -4)
        self.assertEqual(vp.valida_aritmetica(t, "thorik"), [])

    def test_aritmetica_sbagliata_viene_vista(self):
        t = copy.deepcopy(vp.schede()["thorik"])
        t["caratteristiche"]["des"]["attuale"] = 8
        self.assertTrue(vp.valida_aritmetica(t, "x"))

    def test_meta_conto_e_un_errore(self):
        """base senza attuale sembra un dato e non lo è."""
        t = copy.deepcopy(vp.schede()["thorik"])
        t["caratteristiche"]["des"]["attuale"] = None
        self.assertTrue(vp.valida_aritmetica(t, "x"))

    def test_delta_noto_senza_valori_e_lecito(self):
        """Il modulo scrive «+2 COS permanenti» senza dire da quale COS si parte.

        Inventare la base per far tornare il conto sarebbe peggio del buco.
        """
        t = vp.schede()["thorik"]
        cos = t["caratteristiche"]["cos"]
        self.assertIsNone(cos["base"])
        self.assertNotIn("COS", " ".join(vp.valida_aritmetica(t, "thorik")))


class TestDeriva(unittest.TestCase):
    """Il gate deve trovare i costi affermati nei documenti e assenti dalle schede."""

    def test_riprodurrebbe_il_difetto_originale(self):
        """Tolto il −2 DES della **Corona**, il gate deve accorgersene.

        È il caso difficile, ed è il vero motivo per cui esiste il controllo
        sulle fonti primarie: Thorik ha DUE −2 DES (Corona indossata e rito), e
        il confronto per *tipo* resterebbe soddisfatto dall'altro. Solo la fonte
        distingue i due — ed è la Corona quella che era sparita davvero.
        """
        tutte = copy.deepcopy(vp.schede())
        tutte["thorik"]["modificatori_permanenti"] = [
            m for m in tutte["thorik"]["modificatori_permanenti"]
            if not (m["caratteristica"] == "DES" and "Corona" in m["causa"])]
        problemi = vp.verifica_fonti_primarie(tutte, ["Thorik", "Tordek", "Hella", "Artemis"])
        self.assertTrue(
            any("Thorik" in x and "DES" in x for x in problemi),
            "il gate NON si accorgerebbe della sparizione del −2 DES della Corona: "
            f"è decorativo. Problemi visti: {problemi}")

    def test_sparizione_totale_vista_anche_dal_controllo_per_tipo(self):
        """Il difetto storico era l'assenza TOTALE: nessuna scheda, nessun −2 DES."""
        registrati: set = set()
        trovate = vp.scansiona_deriva(["Thorik", "Tordek", "Hella", "Artemis"])
        ignorati = vp.dismissioni()
        derive = [k for k in trovate
                  if k[0] == "Thorik" and (k[2], k[1]) not in registrati and k not in ignorati]
        self.assertTrue(any(k[1] == -2 and k[2] == "DES" for k in derive))

    def test_le_fonti_primarie_esistono_e_dicono_cosa_stabiliscono(self):
        for voce in vp.fonti_primarie():
            self.assertTrue((ROOT / voce["file"]).exists(), f"inesistente: {voce['file']}")
            self.assertTrue(voce.get("attesta"), f"{voce['file']} non dice cosa stabilisce")
            self.assertTrue(voce.get("cosa"), f"{voce['file']} senza spiegazione")

    def test_oggi_nessuna_deriva_scoperta(self):
        registrati = {d["pg"]: {(m["caratteristica"], m["delta"])
                                for m in (d.get("modificatori_permanenti") or [])}
                      for d in vp.schede().values()}
        ignorati = vp.dismissioni()
        scoperte = [k for k in vp.scansiona_deriva(list(registrati))
                    if (k[2], k[1]) not in registrati.get(k[0], set()) and k not in ignorati]
        self.assertEqual(scoperte, [], f"derive non dichiarate: {scoperte}")

    def test_ogni_dismissione_porta_una_ragione(self):
        """Dismettere in silenzio sarebbe il difetto originale con un file in più."""
        for chiave, ragione in vp.dismissioni().items():
            self.assertGreater(len(ragione.strip()), 40,
                               f"dismissione {chiave} senza una ragione vera")

    def test_le_righe_ambigue_non_si_indovinano(self):
        """Due PG sulla stessa riga: il gate tace invece di attribuire a caso."""
        self.assertIn("len(citati) != 1",
                      (ROOT / "scripts" / "validate_pg.py").read_text(encoding="utf-8"))


class TestCanoneRegistrato(unittest.TestCase):
    def test_tordek_non_ha_malus_dal_rito(self):
        """Il refuso 2026-07-31→08-06: il Peso l'ha preso Thorik."""
        self.assertEqual(vp.schede()["tordek"]["modificatori_permanenti"], [])

    def test_hella_e_morta_oggi(self):
        """Quasi tutti i documenti la descrivono viva: raccontano il DOPO."""
        self.assertIn("MORTA", vp.schede()["hella"]["stato"].upper())

    def test_la_corona_non_e_rimovibile(self):
        vincoli = " ".join(v["vincolo"] for v in vp.schede()["thorik"]["vincoli"])
        self.assertIn("NON è rimovibile", vincoli)


if __name__ == "__main__":
    unittest.main()
