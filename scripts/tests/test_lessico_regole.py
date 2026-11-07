"""lessico_regole.py legge i talenti delle schede e li confronta con le fonti giuste.

Il DM, 2026-11-07: vincoli sui termini ufficiali di 3.5 e PF1e «una volta per
tutte», e per i moduli PF1e la tabella diretta italiano → PF1e, mai il passaggio
per la 3.5. Queste prove non usano la rete: l'indice delle fonti è finto.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import lessico_regole as L  # noqa: E402

# Indice finto: tre talenti dell'SRD 3.5 e uno del PRD.
IDX = {
    L.norma("Power Attack"): [{"fonte": "srd35", "tipo": "talento", "nome": "Power Attack"}],
    L.norma("Cleave"): [{"fonte": "srd35", "tipo": "talento", "nome": "Cleave"}],
    L.norma("Weapon Finesse"): [{"fonte": "srd35", "tipo": "talento", "nome": "Weapon Finesse"},
                                {"fonte": "pf1", "tipo": "talento", "nome": "Weapon Finesse"}],
}
ITA = L.mappa_italiana([
    {"it": "Attacco Poderoso", "srd35": "Power Attack", "pf1": "Power Attack"},
    {"it": "Incalzare", "srd35": "Cleave", "pf1": "Cleave", "varianti": "Fendere"},
    {"it": "Arma Accurata", "srd35": "Weapon Finesse", "pf1": "Weapon Finesse",
     "varianti": "Finezza nell'Arma"},
])
PF1 = {L.norma("Arma Accurata"): {"it": "Arma Accurata", "pf1": "Weapon Finesse"},
       L.norma("Attacco Poderoso"): {"it": "Attacco Poderoso", "pf1": "Power Attack"}}


def esiti(testo: str, file: str = "modulo.md") -> list[tuple[str, str]]:
    return [(r["termine"], r["esito"]) for r in L.controlla_testo(testo, IDX, ITA, file, PF1)]


class TestLetturaDelleRighe(unittest.TestCase):
    def test_norma_toglie_tipo_accenti_e_maiuscole(self):
        self.assertEqual(L.norma("Improved Trip <small>[General]</small>"), L.norma("improved trip"))
        self.assertEqual(L.norma("Volontà di Ferro"), L.norma("volonta di ferro"))

    def test_legge_tutti_i_talenti_separati_da_punto_in_mezzo(self):
        self.assertEqual(L.termini_della_riga("Attacco Poderoso · Incalzare · Arma Accurata"),
                         ["Attacco Poderoso", "Incalzare", "Arma Accurata"])

    def test_si_ferma_al_campo_seguente(self):
        self.assertEqual(L.termini_della_riga("Incalzare, Attacco Poderoso **Abilità** Scalare +5"),
                         ["Incalzare", "Attacco Poderoso"])

    def test_segue_l_elenco_che_va_a_capo(self):
        testo = "**Talenti**: Attacco Poderoso · Arma\nAccurata\n**Abilità**: Scalare +4\n"
        self.assertIn(("Attacco Poderoso", "tabella"), esiti(testo))
        self.assertEqual(len(esiti(testo)), 2)


class TestEsiti(unittest.TestCase):
    def test_nome_ufficiale_variante_e_sconosciuto(self):
        e = esiti("**Talenti** Attacco Poderoso, Fendere, Spezzaferro Nanico\n")
        self.assertEqual(e, [("Attacco Poderoso", "tabella"), ("Fendere", "variante"),
                             ("Spezzaferro Nanico", "sconosciuto")])

    def test_nome_inglese_delle_fonti(self):
        self.assertEqual(esiti("**Feats** Power Attack, Cleave\n"),
                         [("Power Attack", "fonte"), ("Cleave", "fonte")])

    def test_marcato_fuori_srd_passa(self):
        e = esiti("**Talenti** Spezzaferro Nanico [Private source — Races of Stone, p. 1]\n")
        self.assertEqual(e[0][1], "marcato")


class TestModuliPF1e(unittest.TestCase):
    """Nei moduli PF1e vale la tabella diretta: un nome 3.5 è un errore."""

    def test_il_percorso_dichiara_il_modulo_pf1e(self):
        self.assertTrue(L.e_pf1("10-stand-alone/Il Giardino PF1e/appendice.md", ""))
        self.assertFalse(L.e_pf1("Bestiario/mostri/ogre.md", "**Talenti** Incalzare"))

    def test_l_intestazione_dichiara_il_modulo_pf1e(self):
        self.assertTrue(L.e_pf1("x.md", "# Modulo\n\n**Sistema**: Pathfinder 1e\n"))

    def test_nome_3_5_in_un_modulo_pf1e(self):
        e = esiti("**Talenti**: Finezza nell'Arma · Arma Accurata\n", "PREGEN-PF1E.md")
        self.assertEqual(e, [("Finezza nell'Arma", "nome 3.5"), ("Arma Accurata", "tabella")])

    def test_lo_stesso_nome_in_un_modulo_3_5_e_una_variante(self):
        self.assertEqual(esiti("**Talenti**: Finezza nell'Arma\n", "STATBLOCCHI.md"),
                         [("Finezza nell'Arma", "variante")])


class TestTabelle(unittest.TestCase):
    def test_la_tabella_italiana_del_repo_si_legge(self):
        voci = L.carica_tabella()
        self.assertGreaterEqual(len(voci), 80)
        self.assertTrue(all(v.get("it") for v in voci))

    def test_tabella_pf1_per_tipo(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "t.tsv"
            p.write_text("# commento\nitaliano\tpf1\ttipo\nArma Accurata\tWeapon Finesse\ttalento\n"
                         "Dardo Incantato\tMagic Missile\tincantesimo\n", encoding="utf-8")
            self.assertEqual(list(L.tabella_pf1(p)), [L.norma("Arma Accurata")])
            self.assertEqual(L.tabella_pf1(p, "incantesimo")[L.norma("Dardo Incantato")]["pf1"],
                             "Magic Missile")

    def test_la_tabella_pf1_del_repo_ha_i_quattro_tipi(self):
        for tipo, minimo in (("talento", 1000), ("incantesimo", 1400), ("abilità", 26), ("condizione", 30)):
            with self.subTest(tipo=tipo):
                self.assertGreaterEqual(len(L.tabella_pf1(tipo=tipo)), minimo)


if __name__ == "__main__":
    unittest.main()
