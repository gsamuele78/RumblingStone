"""Il valore dell'equipaggiamento contro quello di un PNG del suo livello (ADR-0126, lotto 8).

I prezzi vengono dalle tabelle degli oggetti magici dell'SRD; il valore per
livello dalla Tabella 4-23 del DMG 3.5 (solo i numeri)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402
from dmcore import sistemi as S  # noqa: E402


def giudica(coda: str, **kw) -> "tuple[list, list]":
    """(violazioni, non verificabili) della sola verifica `ricchezza` sulla scheda di prova."""
    import tempfile
    from tests.test_difese import SCHEDA
    d = {"titolo": "Prova", "tipo": "Medium humanoid (human)", "classe": "Fighter 3", "dadi": "3d10+6"}
    d.update(kw)
    with tempfile.TemporaryDirectory() as t:
        q = Path(t) / "prova-cr4.md"
        q.write_text(SCHEDA.format(coda=coda, **d), encoding="utf-8")
        if V.L.leggi(q) is None:
            raise AssertionError("la scheda di prova non si legge")
        return V.ricchezza(q)


class TestDati(unittest.TestCase):
    def setUp(self):
        self.d = S.dati("dnd35", "creature.costruzione")["oggetti"]

    def test_tabella_dei_png(self):
        t = self.d["png"]["per_livello"]
        self.assertEqual(len(t), 20)
        self.assertEqual((t[0], t[9], t[19]), (900, 16000, 220000))
        self.assertEqual(t, sorted(t))

    def test_potenziamento(self):
        self.assertEqual(self.d["potenziamento"]["arma"][:5], [2000, 8000, 18000, 32000, 50000])
        self.assertEqual(self.d["potenziamento"]["armatura"], [1000, 4000, 9000, 16000, 25000])

    def test_prezzi_dell_srd(self):
        p = self.d["prezzi"]
        self.assertEqual(p["ring of protection +3"], 18000)
        self.assertEqual(p["cloak of resistance +5"], 25000)
        self.assertEqual(p["amulet of health +6"], 36000)
        self.assertEqual(p["gauntlets of ogre power"], 4000)
        self.assertEqual(p["boots of speed"], 12000)
        self.assertGreater(len(p), 600)

    def test_ogni_nome_ha_un_prezzo(self):
        for v in self.d["nomi"]:
            nomi = [v["nome"].replace("N", str(n)) for n in range(1, 7)] if "N" in v["nome"] else [v["nome"]]
            self.assertTrue(any(n in self.d["prezzi"] for n in nomi), v["nome"])

    def test_pf1e_non_ha_la_tabella(self):
        self.assertNotIn("oggetti", S.dati("pf1e", "creature.costruzione"))


class TestOggetti(unittest.TestCase):
    def setUp(self):
        self.d = S.dati("dnd35", "creature.costruzione")["oggetti"]

    def trova(self, riga: str) -> list:
        return sorted(V._oggetti_col_prezzo(riga, self.d, "dnd35"))

    def test_nomi_italiani_e_inglesi(self):
        self.assertEqual(self.trova("*anello di protezione +2*, *mantello della resistenza +1*"),
                         [("cloak of resistance +1", 1000), ("ring of protection +2", 8000)])
        self.assertEqual(self.trova("Ring of Protection +1, Cloak of Charisma +4"),
                         [("cloak of charisma +4", 16000), ("ring of protection +1", 2000)])

    def test_armature_e_armi_col_solo_potenziamento(self):
        self.assertEqual([mo for _, mo in self.trova("corazza di piastre +1, picca lunga +1")], [1000, 2000])

    def test_capacita_speciali_attaccate_al_nome_o_al_bonus(self):
        # animato +2 e sacrilego +2: (2 + 2)² × 1000 e × 2000; infuocata e affilata: (1 + 2)² × 2000
        self.assertEqual([mo for _, mo in self.trova("**Scudo Pesante +2 animato**")], [16000])
        self.assertEqual([mo for _, mo in self.trova("**Spadone Sacrilego +2**")], [32000])
        self.assertEqual([mo for _, mo in self.trova("spada lunga +1 infuocata e affilata")], [18000])
        self.assertEqual([mo for _, mo in self.trova("longsword +1 flaming")], [8000])
        # limite dichiarato: la capacità scritta prima del nome non si legge, resta il potenziamento
        self.assertEqual([mo for _, mo in self.trova("flaming longsword +1")], [2000])

    def test_una_parola_lontana_non_e_una_capacita(self):
        # «Cerchio Sacro» è un nome proprio: l'arco resta un +1
        self.assertEqual([mo for _, mo in self.trova("Arco lungo composito +1 di tasso del Cerchio Sacro")], [2000])

    def test_oltre_il_piu_dieci_resta_il_potenziamento(self):
        self.assertEqual([mo for _, mo in self.trova("spada lunga +5 vorpal sacrilega")], [50000])

    def test_pozioni_pergamene_e_bacchette(self):
        self.assertEqual(self.trova("3 pozioni di *cura ferite leggere*"),
                         [("3 × potion of cure light wounds (potion)", 150)])
        self.assertEqual(self.trova("due pergamene di palla di fuoco"), [("2 × fireball", 750)])
        self.assertEqual(self.trova("potion of cure moderate wounds x2"),
                         [("2 × potion of cure moderate wounds (potion)", 600)])
        # una bacchetta vale per le cariche scritte; senza cariche non si conta
        self.assertEqual(self.trova("bacchetta di dardo incantato (20 cariche)"), [("wand of magic missile (1st)", 300)])
        self.assertEqual(self.trova("bacchetta di dardo incantato"), [])
        self.assertEqual(self.trova("pozione di un liquido verde"), [])

    def test_nomi_del_lessico(self):
        self.assertEqual(self.trova("Bracciali dell'arciere superiori, Stivali elfici"),
                         [("boots of elvenkind", 2500), ("bracers of archery, greater", 25000)])

    def test_un_nome_italiano_di_una_parola_non_basta(self):
        self.assertEqual(self.trova("un ventaglio di seta, un mantello"), [])
        self.assertEqual(self.trova("Wind fan"), [("wind fan", 5500)])

    def test_tabelle_delle_capacita_e_delle_pergamene(self):
        c = self.d["capacita"]
        self.assertEqual((c["arma"]["keen"], c["arma"]["vorpal"], c["armatura"]["animated"]),
                         ({"bonus": 1}, {"bonus": 5}, {"bonus": 2}))
        self.assertEqual(c["armatura"]["glamered"], {"mo": 2700})
        self.assertEqual((self.d["pergamene"]["fireball"], self.d["pergamene"]["cure light wounds"]), (375, 25))

    def test_senza_bonus_non_ha_prezzo(self):
        self.assertEqual(self.trova("spada lunga perfetta, armatura completa, 2 pozioni"), [])
        self.assertEqual(self.trova("mantello del carisma +3"), [])

    def test_righe_dell_equipaggiamento(self):
        testo = ("**Equipaggiamento** anello di protezione +1\n\n### Equipaggiamento\n- mantello della resistenza +1\n"
                 "| **Anello di Protezione +2** | nota |\n### Tattiche\n- anello di protezione +5\n"
                 "> era: Equipaggiamento anello di protezione +4\n")
        self.assertEqual([n for n, _ in V._righe_dell_equipaggiamento(testo)], [1, 4, 5])


class TestRicchezza(unittest.TestCase):
    def test_sotto_la_tabella(self):
        self.assertEqual(giudica("**Equipaggiamento** spada lunga +1, 2 pozioni"), ([], []))
        self.assertEqual(giudica(""), ([], []))

    def test_sopra_la_tabella(self):
        v, n = giudica("**Equipaggiamento** spada lunga +1, anello di protezione +1")
        self.assertEqual(n, [])
        self.assertEqual(len(v), 1)
        self.assertEqual((v[0]["regola"], v[0]["atteso"], v[0]["ha"]),
                         ("equipaggiamento.valore", "al più 2500 mo", "almeno 4000 mo"))

    def test_il_livello_alza_il_limite(self):
        coda = "**Equipaggiamento** spada lunga +1, anello di protezione +1"
        self.assertEqual(giudica(coda, classe="Fighter 5", dadi="5d10+10"), ([], []))

    def test_razza_fuori_dalle_sette(self):
        v, n = giudica("**Equipaggiamento** anello di protezione +2", tipo="Medium humanoid (goblinoid)")
        self.assertEqual(v, [])
        self.assertEqual(len(n), 1)
        self.assertIn("modificatore di livello", n[0]["testo"])

    def test_razza_senza_dadi_vita_razziali(self):
        # hobgoblin: livello effettivo 3 + 1 = 4, 3300 mo; drow: 3 + 2 = 5, 4300 mo
        coda = "**Equipaggiamento** spada lunga +1, anello di protezione +1"
        v, n = giudica(coda, titolo="Sergente hobgoblin", tipo="Medium humanoid (goblinoid)")
        self.assertEqual(n, [])
        self.assertEqual(v[0]["atteso"], "al più 3300 mo")
        self.assertEqual(giudica(coda, titolo="Esploratrice drow", tipo="Medium humanoid (elf, drow)"), ([], []))
        v, n = giudica(coda, titolo="Predone orco", tipo="Medium humanoid (orc)")
        self.assertEqual(v[0]["atteso"], "al più 2500 mo")

    def test_un_modello_non_si_giudica(self):
        coda = "**Equipaggiamento** spada lunga +1, anello di protezione +1"
        v, n = giudica(coda, titolo="Hobgoblin mezzo-drago", tipo="Medium humanoid (goblinoid)")
        self.assertEqual(v, [])
        self.assertEqual(len(n), 1)

    def test_tabella_dei_modificatori_di_livello(self):
        d = S.dati("dnd35", "creature.costruzione")["mdl"]
        self.assertEqual({k: v["mdl"] for k, v in d["razze"].items()},
                         {"aasimar": 1, "drow": 2, "duergar": 1, "goblin": 0, "hobgoblin": 1, "kobold": 0,
                          "merfolk": 1, "orc": 0, "svirfneblin": 3, "tiefling": 1})
        self.assertEqual(set(d["nomi"]), set(d["razze"]))

    def test_una_riga_di_storia_non_conta(self):
        self.assertEqual(giudica("> era: Equipaggiamento anello di protezione +5"), ([], []))


class Bestiario(unittest.TestCase):
    def test_il_bestiario_non_ha_scarti(self):
        trovate = []
        for p in sorted((ROOT / "Bestiario").rglob("*.md")):
            trovate += [f"{x['file']}:{x['riga']} {x['testo']}" for x in V.ricchezza(p)[0]]
        self.assertEqual(trovate, [])


if __name__ == "__main__":
    unittest.main()
