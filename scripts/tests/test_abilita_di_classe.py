"""Le abilità di classe e il margine vero dei gradi (ADR-0126, lotto 6, prima parte).

Chi ha soltanto livelli di classe, tutti con l'elenco nel plugin, ha il massimo
dimezzato e il costo doppio nelle abilità che non sono di nessuna delle sue
classi; se è di una delle sette razze dell'SRD il margine fisso lascia il posto
a razza e sinergie contate voce per voce."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

SERGENTE = ROOT / "Bestiario" / "mostri" / "hobgoblin-sergente-cr5.md"   # Fighter 5: Intimidate +7, Listen +3, Spot +3


def _prova(nome: str, testo: str) -> "tuple[list[dict], list[dict]]":
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / nome
        p.write_text(testo, encoding="utf-8")
        return V.abilita(p)


def _umano(testo: str) -> str:
    """Il sergente riscritto come umano, senza la parola «razziale» nelle note."""
    t = re.sub(r"(?i)hobgoblin", "Umano", testo)
    t = re.sub(r"(?i)goblinoid[ei]?", "umano", t)
    return re.sub(r"(?i)razzial\w*|racial", "di razza", t)


class TestDati(unittest.TestCase):
    def setUp(self):
        self.r = S.dati("dnd35", "creature.gradi")

    def test_abilita_di_classe_dall_srd(self):
        d = self.r["di_classe"]
        self.assertEqual(d["warrior"], ["climb", "handle animal", "intimidate", "jump", "ride", "swim"])
        self.assertIn("spellcraft", d["wizard"])
        self.assertIn("knowledge", d["wizard"])                  # tutte le Conoscenze
        self.assertIn("knowledge (religion)", d["cleric"])       # solo alcune
        self.assertNotIn("listen", d["fighter"])
        self.assertIn("hide", d["arcane archer"])                # il punto di troppo della fonte non spezza l'elenco
        self.assertNotIn("expert", d)                            # ne sceglie dieci: nessun elenco
        self.assertEqual(self.r["fuori_classe"], {"costo": 2, "massimo_diviso": 2})

    def test_domini_sinergie_e_razze(self):
        self.assertEqual(self.r["di_dominio"]["trickery"], ["bluff", "disguise", "hide"])
        self.assertEqual(self.r["sinergie"]["diplomacy"], ["bluff", "knowledge", "sense motive"])
        self.assertEqual(self.r["sinergie"]["tumble"], ["jump"])
        self.assertEqual(self.r["razze"]["elf"], {"listen": 2, "search": 2, "spot": 2})
        self.assertEqual(self.r["razze"]["human"], {})
        self.assertEqual(set(self.r["razze"]), set(self.r["razze_nomi"]) - {"altre"})

    def test_ogni_abilita_dei_dati_ha_la_sua_chiave(self):
        chiave = self.r["chiave"]
        nomi = [a for v in self.r["di_classe"].values() for a in v]
        nomi += [a for v in self.r["di_dominio"].values() for a in v]
        nomi += list(self.r["sinergie"]) + [a for v in self.r["sinergie"].values() for a in v]
        nomi += [a for v in self.r["razze"].values() for a in v]
        self.assertEqual([a for a in nomi if a.split(" (")[0] not in chiave], [])


class TestRazza(unittest.TestCase):
    def setUp(self):
        self.r = S.dati("dnd35", "creature.gradi")

    def test_le_sette_razze(self):
        for dove, attesa in (("Medium humanoid (human)", "human"), ("umanoide (nano) Guerriero 6", "dwarf"),
                             ("Elfa, Maga 5", "elf"), ("druido mezzelfo", "half-elf"),
                             ("Half-Elf (elf/human) Bard 8", "half-elf"), ("Mezzorco Barbaro 4", "half-orc")):
            with self.subTest(dove=dove):
                self.assertEqual(V._razza_srd(dove, self.r), attesa)

    def test_sottorazze_e_razze_d_altre_pagine_non_si_riconoscono(self):
        for dove in ("umanoide (nano) duergar Ladro 1", "Drow umanoide (elfo) Fighter 3", "Hobgoblin Fighter 5",
                     "umanoide (orco) Barbaro 2", "Aberrazione", "nano ed elfo insieme"):
            with self.subTest(dove=dove):
                self.assertIsNone(V._razza_srd(dove, self.r))


class TestFuoriClasse(unittest.TestCase):
    def setUp(self):
        self.testo = SERGENTE.read_text(encoding="utf-8")

    def test_la_scheda_vera_e_pulita(self):
        self.assertEqual(V.abilita(SERGENTE), ([], []))

    def test_abilita_fuori_classe_sopra_la_meta_del_massimo(self):
        # Ascoltare non è del guerriero: con 5 dadi vita il massimo è (5 + 3) / 2 = 4
        viol, _ = _prova(SERGENTE.name, self.testo.replace("Listen +3", "Listen +15"))
        self.assertEqual([(v["regola"], v["abilita"], v["atteso"], v["ha"]) for v in viol],
                         [("gradi.massimo.fuori_classe", "listen", "4", 5)])

    def test_la_stessa_altezza_in_un_abilita_di_classe_passa(self):
        # Intimidire è del guerriero: gli stessi 5 gradi minimi stanno sotto il massimo di 8
        viol, _ = _prova(SERGENTE.name, self.testo.replace("Intimidate +7", "Intimidate +14"))
        self.assertEqual(viol, [])

    def test_i_gradi_fuori_classe_costano_il_doppio(self):
        # 5 dadi vita, 2 punti per livello, Int 10: 16 punti. Due abilità fuori classe a 4 gradi
        # minimi ne chiedono 16 da sole, più Intimidire: senza il costo doppio ne basterebbero 8
        viol, _ = _prova(SERGENTE.name, self.testo.replace("Listen +3", "Listen +14").replace("Spot +3", "Spot +14")
                         .replace("Intimidate +7", "Intimidate +12"))
        self.assertEqual([v["regola"] for v in viol], ["gradi.punti"])

    def test_classe_senza_elenco_non_giudica_fuori_classe(self):
        viol, _ = _prova(SERGENTE.name, self.testo.replace("Fighter 5", "Expert 5").replace("Listen +3", "Listen +15"))
        self.assertNotIn("gradi.massimo.fuori_classe", {v["regola"] for v in viol})


class TestMargineVero(unittest.TestCase):
    def setUp(self):
        self.testo = SERGENTE.read_text(encoding="utf-8")

    def test_umano_senza_sinergie_ha_il_margine_del_solo_oggetto(self):
        # Intimidire +10 con Carisma 8: 10 + 1 − 2 = 9 gradi, il massimo è 8
        viol, _ = _prova("umano-sergente-cr5.md", _umano(self.testo).replace("Intimidate +7", "Intimidate +10"))
        self.assertEqual([(v["regola"], v["ha"], v["atteso"]) for v in viol], [("gradi.massimo", 9, 8)])
        self.assertEqual(_prova("umano-sergente-cr5.md", _umano(self.testo).replace("Intimidate +7", "Intimidate +9"))[0], [])

    def test_la_sinergia_conta_solo_se_la_fonte_e_scritta(self):
        # Raggirare dà +2 a Intimidire: con Raggirare nella riga il margine sale a 4
        con = _umano(self.testo).replace("Intimidate +7", "Bluff +1, Intimidate +10")
        self.assertEqual(_prova("umano-sergente-cr5.md", con)[0], [])

    def test_chi_non_e_di_una_razza_dell_srd_tiene_il_margine_di_prima(self):
        # lo stesso +10 sull'hobgoblin vero non è una violazione
        self.assertEqual(_prova(SERGENTE.name, self.testo.replace("Intimidate +7", "Intimidate +10"))[0], [])


if __name__ == "__main__":
    unittest.main()
