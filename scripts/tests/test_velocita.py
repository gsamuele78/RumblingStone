"""La velocità a terra di una scheda (ADR-0126, lotto 7, prima parte).

Razza, movimento veloce di barbaro e monaco, armatura media o pesante: i numeri
vengono dalla tabella `[movimento]` del plugin 3.5, estratta dall'SRD."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

SCHEDA = """# Prova [INFERRED]
**Faction**: none | **Role**: brute | **Environment**: any | **CR**: 4

```statblocco
gs: 4
tipo: Medium humanoid ({razza}), {classe}, N
ca: 15
ca-dettaglio: contatto 11, colto alla sprovvista 14 ({ca})
pf: 30
pf-dado: {dadi}
ts: Temp +6, Rifl +2, Vol +2
attributi: For 16 Des 12 Cos 14 Int 10 Sag 12 Car 8
velocita: {velocita}
iniziativa: +1
attacchi:
  - Mischia spada lunga +7 (1d8+3/19-20)
voci:
  - Abilità: Scalare +5
  - Talenti: Attacco Poderoso, Incalzare
```
{coda}"""


def giudica(velocita: str, razza: str = "human", classe: str = "Fighter 4", ca: str = "+1 Des",
            dadi: str = "4d10+8", coda: str = "") -> "tuple[list, list]":
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / "prova-cr4.md"
        q.write_text(SCHEDA.format(razza=razza, classe=classe, ca=ca, velocita=velocita, dadi=dadi, coda=coda),
                     encoding="utf-8")
        if V.L.leggi(q) is None:
            raise AssertionError("la scheda di prova non si legge")
        v, n = V.velocita(q)
    return [(x["regola"], x["atteso"], x["ha"]) for x in v], [x["testo"] for x in n]


class TestDati(unittest.TestCase):
    def setUp(self):
        self.m = S.dati("dnd35", "creature.costruzione")["movimento"]

    def test_razze_e_chi_non_rallenta(self):
        self.assertEqual(self.m["razze"], {"human": 30, "dwarf": 20, "elf": 30, "gnome": 20, "half-elf": 30,
                                           "half-orc": 30, "halfling": 20})
        self.assertEqual(self.m["non_rallenta"], ["dwarf"])

    def test_categorie_delle_armature(self):
        a = self.m["armature"]
        self.assertEqual(len(a), 12)
        self.assertEqual(a["chain shirt"]["categoria"], "leggera")
        self.assertEqual(a["breastplate"]["categoria"], "media")
        self.assertEqual(a["full plate"], {"ca": 8, "des_max": 1, "categoria": "pesante"})

    def test_velocita_ridotta_e_classi(self):
        self.assertEqual((self.m["ridotta"]["30"], self.m["ridotta"]["20"], self.m["ridotta"]["40"]), (20, 15, 30))
        self.assertEqual(self.m["classi"]["barbarian"], {"piu": 10, "non_in": ["pesante"]})
        monaco = self.m["classi"]["monk"]["per_livello"]
        self.assertEqual((len(monaco), monaco[1], monaco[2], monaco[8], monaco[19]), (20, 0, 10, 30, 60))

    def test_pf1e_non_ha_la_tabella(self):
        self.assertNotIn("movimento", S.dati("pf1e", "creature.costruzione"))


class TestVelocita(unittest.TestCase):
    def test_umano_senza_armatura(self):
        self.assertEqual(giudica("9 m"), ([], []))
        self.assertEqual(giudica("30 ft"), ([], []))
        self.assertEqual(giudica("6 m")[0], [("numero.velocita", 30, 20)])
        self.assertEqual(giudica("12 m")[0], [("numero.velocita", 30, 40)])

    def test_l_armatura_pesante_e_la_media_rallentano(self):
        self.assertEqual(giudica("6 m", ca="+8 full plate, +1 Des"), ([], []))
        self.assertEqual(giudica("9 m", ca="+8 full plate, +1 Des")[0], [("numero.velocita", 20, 30)])
        self.assertEqual(giudica("9 m", ca="+5 corazza di piastre, +1 Des")[0], [("numero.velocita", 20, 30)])

    def test_l_armatura_leggera_e_lo_scudo_no(self):
        self.assertEqual(giudica("9 m", ca="+4 giaco di maglia, +2 scudo pesante, +1 Des"), ([], []))
        self.assertEqual(giudica("6 m", ca="+4 giaco di maglia, +1 Des")[0], [("numero.velocita", 30, 20)])

    def test_il_nano_non_rallenta(self):
        self.assertEqual(giudica("6 m", razza="dwarf", ca="+8 full plate, +1 Des"), ([], []))
        self.assertEqual(giudica("4,5 m", razza="dwarf", ca="+8 full plate, +1 Des")[0],
                         [("numero.velocita", 20, 15)])

    def test_il_piccolo_in_armatura_scende_a_quattro_metri_e_mezzo(self):
        self.assertEqual(giudica("4,5 m", razza="halfling", ca="+8 full plate, +1 Des"), ([], []))
        self.assertEqual(giudica("6 m", razza="halfling", ca="+8 full plate, +1 Des")[0],
                         [("numero.velocita", 15, 20)])

    def test_il_mithral_conta_una_categoria_piu_leggera(self):
        # corazza di piastre di mithral: da media a leggera, non rallenta
        self.assertEqual(giudica("9 m", ca="+5 breastplate di mithral, +1 Des"), ([], []))
        # armatura completa di mithral: da pesante a media, rallenta ancora
        self.assertEqual(giudica("6 m", ca="+8 full plate di mithral, +1 Des"), ([], []))

    def test_il_barbaro(self):
        b = {"classe": "Barbarian 4", "dadi": "4d12+8"}
        self.assertEqual(giudica("12 m", **b), ([], []))
        self.assertEqual(giudica("9 m", **b)[0], [("numero.velocita", 40, 30)])
        # in armatura media: 40 ridotta a 30; in armatura pesante perde il bonus: 30 ridotta a 20
        self.assertEqual(giudica("9 m", ca="+5 breastplate, +1 Des", **b), ([], []))
        self.assertEqual(giudica("6 m", ca="+8 full plate, +1 Des", **b), ([], []))

    def test_il_monaco(self):
        m = {"classe": "Monk 9", "dadi": "9d8+18"}
        self.assertEqual(giudica("18 m", **m), ([], []))                  # 30 + 30
        self.assertEqual(giudica("9 m", **m)[0], [("numero.velocita", 60, 30)])
        self.assertEqual(giudica("9 m", ca="+4 chain shirt, +1 Des", **m), ([], []))   # in armatura lo perde

    def test_chi_dichiara_una_ragione_e_un_dubbio(self):
        v, n = giudica("12 m (+3 m dagli stivali)")
        self.assertEqual(v, [])
        self.assertEqual(len(n), 1)
        v, n = giudica("12 m", coda="\n*Oggetti*: stivali dell'andatura e del balzo.\n")
        self.assertEqual((v, len(n)), ([], 1))

    def test_chi_non_si_giudica(self):
        # una razza che non è delle sette dell'SRD: la sua velocità il plugin non la sa
        self.assertEqual(giudica("12 m", razza="goblinoid"), ([], []))
        self.assertEqual(giudica("12 m", razza="orc"), ([], []))

    def test_il_bestiario_non_ha_violazioni(self):
        fuori = []
        for p in sorted((ROOT / "Bestiario").rglob("*.md")):
            try:
                v, _ = V.velocita(p)
            except Exception as e:                                        # noqa: BLE001
                self.fail(f"{p.name}: {e}")
            fuori += [f"{x['file']}: {x['testo']}" for x in v]
        self.assertEqual(fuori, [])


if __name__ == "__main__":
    unittest.main()
