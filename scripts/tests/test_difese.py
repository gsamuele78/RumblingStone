"""Resistenza agli incantesimi e riduzione del danno di una scheda (ADR-0126, lotto 7, seconda parte).

La razza dà N + i livelli di classe, il monaco livello + 10, il barbaro N/— per
livello: i numeri vengono dalla tabella `[difese]` del plugin 3.5, estratta dall'SRD."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import verifica_scheda as V  # noqa: E402
from dmcore import sistemi as S  # noqa: E402

SCHEDA = """# {titolo} [INFERRED]
**Faction**: none | **Role**: brute | **Environment**: any | **CR**: 4

```statblocco
gs: 4
tipo: {tipo}, {classe}, N
ca: 11
ca-dettaglio: contatto 11, colto alla sprovvista 10 (+1 Des)
pf: 30
pf-dado: {dadi}
ts: Temp +6, Rifl +2, Vol +2
attributi: For 16 Des 12 Cos 14 Int 10 Sag 12 Car 8
velocita: 9 m
iniziativa: +1
attacchi:
  - Mischia spada lunga +7 (1d8+3/19-20)
voci:
  - Abilità: Scalare +5
  - Talenti: Attacco Poderoso, Incalzare
```
{coda}
"""


def giudica(coda: str = "", titolo: str = "Prova", tipo: str = "Medium humanoid (human)",
            classe: str = "Fighter 3", dadi: str = "3d10+6", sistema: str = "") -> "tuple[list, list]":
    with tempfile.TemporaryDirectory() as d:
        q = Path(d) / "prova-cr4.md"
        testo = SCHEDA.format(titolo=titolo, tipo=tipo, classe=classe, dadi=dadi, coda=coda)
        if sistema:
            testo = testo.replace("**CR**: 4", f"**CR**: 4 | **Sistema**: {sistema}")
        q.write_text(testo, encoding="utf-8")
        if V.L.leggi(q) is None:
            raise AssertionError("la scheda di prova non si legge")
        v, n = V.difese(q)
    return [(x["regola"], x["atteso"], x["ha"]) for x in v], [x["testo"] for x in n]


DROW = {"titolo": "Drow della casata", "tipo": "Medium humanoid (elf)"}


class TestDati(unittest.TestCase):
    def setUp(self):
        self.d = S.dati("dnd35", "creature.costruzione")["difese"]

    def test_razze_con_la_resistenza_agli_incantesimi(self):
        self.assertEqual(self.d["ri"]["razze"], {"azer": 13, "drow": 11, "hound archon": 16, "pixie": 15,
                                                 "rakshasa": 27, "svirfneblin": 11})
        self.assertEqual(set(self.d["ri"]["nomi"]), set(self.d["ri"]["razze"]))

    def test_monaco_e_barbaro(self):
        self.assertEqual(self.d["ri"]["classi"]["monk"], {"dal": 13, "piu": 10})
        self.assertEqual(self.d["rd"]["classi"]["barbarian"]["per_livello"],
                         [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5])

    def test_pf1e_non_ha_la_tabella(self):
        self.assertNotIn("difese", S.dati("pf1e", "creature.costruzione"))


class TestResistenzaAgliIncantesimi(unittest.TestCase):
    def test_drow_con_tre_livelli(self):
        self.assertEqual(giudica("**SR**: 14 | **SLA**: as drow", **DROW), ([], []))
        self.assertEqual(giudica("**TS** Temp +6. **RI 14**.", **DROW), ([], []))

    def test_un_punto_di_troppo_o_di_meno(self):
        self.assertEqual(giudica("**SR**: 15", **DROW)[0], [("numero.RI", 14, 15)])
        self.assertEqual(giudica("**RI 13**.", **DROW)[0], [("numero.RI", 14, 13)])

    def test_chi_non_la_scrive(self):
        v, n = giudica("", **DROW)
        self.assertEqual(v, [("numero.RI", 14, None)])
        self.assertEqual(n, [])

    def test_una_nota_accanto_al_numero_e_un_dubbio(self):
        v, n = giudica("**SR**: 18 (drow noble +4 over std)", **DROW)
        self.assertEqual(v, [])
        self.assertEqual(len(n), 1)
        self.assertIn("la regola dà 14", n[0])

    def test_un_oggetto_che_la_da_e_un_dubbio(self):
        v, n = giudica("**RI 21**.\n**Oggetti** mantello della resistenza agli incantesimi", **DROW)
        self.assertEqual(v, [])
        self.assertEqual(len(n), 1)

    def test_due_numeri_diversi(self):
        v, n = giudica("**RI 14**.\n**In forma di ragno** RI 18", **DROW)
        self.assertEqual(v, [])
        self.assertIn("più d'una", n[0])

    def test_le_righe_di_storia_non_contano(self):
        self.assertEqual(giudica("**RI 14**.\n> era: RI 12\nBoost log: RI 12 → 14", **DROW), ([], []))

    def test_un_umano_non_la_deve_avere(self):
        self.assertEqual(giudica(""), ([], []))
        self.assertEqual(giudica("**RI 15** (anello)"), ([], []))

    def test_il_cultista_del_rakshasa_non_e_un_rakshasa(self):
        self.assertEqual(giudica("", titolo="Cultista Rakshasa", classe="Rogue 3", dadi="3d6+6"), ([], []))

    def test_rakshasa_con_livelli_di_classe(self):
        r = {"titolo": "Il mercante", "tipo": "Medium outsider (native), rakshasa", "classe": "Sorcerer 2",
             "dadi": "7d8+2d4+27"}
        self.assertEqual(giudica("**RI 29**", **r), ([], []))
        self.assertEqual(giudica("**RI 27**", **r)[0], [("numero.RI", 29, 27)])

    def test_monaco_dal_tredicesimo(self):
        m13 = {"classe": "Monk 13", "dadi": "13d8+26"}
        self.assertEqual(giudica("**RI 23**", **m13), ([], []))
        self.assertEqual(giudica("**RI 22**", **m13)[0], [("numero.RI", 23, 22)])
        self.assertEqual(giudica("", **m13)[0], [("numero.RI", 23, None)])
        self.assertEqual(giudica("", classe="Monk 12", dadi="12d8+24"), ([], []))


class TestRiduzioneDelDanno(unittest.TestCase):
    B7 = {"classe": "Barbarian 7", "dadi": "7d12+14"}
    B10 = {"classe": "Barbarian 10", "dadi": "10d12+20"}

    def test_barbaro_in_regola(self):
        self.assertEqual(giudica("**Difesa** RD 1/—; schivare prodigioso", **self.B7), ([], []))
        self.assertEqual(giudica("DR 1/- uncanny dodge", **self.B7), ([], []))
        self.assertEqual(giudica("RD 2/—", **self.B10), ([], []))

    def test_barbaro_fuori_regola(self):
        self.assertEqual(giudica("RD 1/—", **self.B10)[0], [("numero.RD", 2, 1)])
        self.assertEqual(giudica("RD 3/—", **self.B10)[0], [("numero.RD", 2, 3)])

    def test_barbaro_che_non_la_scrive(self):
        self.assertEqual(giudica("", **self.B7)[0], [("numero.RD", 1, None)])
        self.assertEqual(giudica("RD 5/magia", **self.B7)[0], [("numero.RD", 1, None)])

    def test_sotto_il_settimo_non_ne_ha(self):
        self.assertEqual(giudica("", classe="Barbarian 6", dadi="6d12+12"), ([], []))
        self.assertEqual(giudica("RD 1/—", classe="Barbarian 6", dadi="6d12+12")[0], [("numero.RD", 0, 1)])

    def test_la_storia_non_conta_e_due_numeri_sono_un_dubbio(self):
        self.assertEqual(giudica("RD 2/—\n- era: RD 1/—", **self.B10), ([], []))
        v, n = giudica("RD 2/—\n**Variante** RD 3/—", **self.B10)
        self.assertEqual(v, [])
        self.assertIn("più d'una", n[0])

    def test_chi_non_e_barbaro(self):
        self.assertEqual(giudica("RD 10/adamantio"), ([], []))
        self.assertEqual(giudica("RD 3/—"), ([], []))


class Bestiario(unittest.TestCase):
    #: scarti veri in attesa della decisione del DM (card del thread delle regole)
    IN_ATTESA = {"Il_Collezionista_Rakshasa.md"}

    def test_il_bestiario_non_ha_altri_scarti(self):
        trovate, attese = [], set()
        for p in sorted((ROOT / "Bestiario").rglob("*.md")):
            v = V.difese(p)[0]
            if p.name in self.IN_ATTESA:
                attese |= {p.name} if v else set()
            else:
                trovate += [f"{x['file']}:{x['riga']} {x['testo']}" for x in v]
        self.assertEqual(trovate, [])
        self.assertEqual(attese, self.IN_ATTESA, "una scheda in attesa è stata corretta: toglierla dall'elenco")


if __name__ == "__main__":
    unittest.main()
