"""Le cinque capacità PF1e prima «non supportate» (ADR-0111): PE, incontri,
tesoro, classi e razze, costruzione delle creature.

I difetti che questi test esistono per impedire:

- un numero PF1e scritto a mano che non è quello del PRD (i dati li scrive
  estrai_prd_pf1e.py; qui si controllano i punti che il PRD stesso dà come
  esempio, e il --check quando il PRD è in cache);
- un incontro PF1e combinato con la formula 3.5 (tre GS 10 fanno GS 13 in
  PF1e, 13,17 in 3.5);
- un blocco portato in PF1e che perde i pf del suo GS cambiando dado vita;
- uno strumento che con --sistema pf1e cambia anche l'uscita 3.5 (quella la
  tiene il banco d'invarianza, qui si prova solo che il predefinito resta 3.5).

Solo `unittest`.
"""
from __future__ import annotations

import os
import random
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore import sistemi as S  # noqa: E402
from dmcore import creature_pf1e as CP  # noqa: E402
import coerenza_campagna as C  # noqa: E402
import genera_creatura as G  # noqa: E402
import suggest_encounter as E  # noqa: E402
import suggest_loot as L  # noqa: E402
import update_xp as X  # noqa: E402

ESTRATTORE = REPO / "plans/esperimenti/sistemi-plugin-2026-11-07/estrai_prd_pf1e.py"
CACHE = Path(os.environ.get("RUMBLINGSTONE_SRD_CACHE",
                            Path.home() / ".cache/rumblingstone/srd")) / "PSRD-Data-76ea47846041"


class Dati(unittest.TestCase):
    def test_nessuna_capacita_pf1e_resta_non_supportata(self):
        cat = S.carica()[1]
        modi = {n: S.capacita("pf1e", n).modo for n in cat}
        self.assertEqual([n for n, m in modi.items() if m not in ("dati", "codice")], [])

    def test_dati_rifiuta_una_capacita_in_codice(self):
        with self.assertRaises(S.ErroreSistemi):
            S.dati("dnd35", "pe.soglie")

    def test_opzioni_di_campagna(self):
        self.assertEqual(S.opzione("pf1e", "traccia_pe"), "media")
        self.assertIsNone(S.opzione("pf1e", "inesistente"))

    @unittest.skipUnless(CACHE.is_dir(), "PRD PF1e non in cache (riscontro_srd.py scarica)")
    def test_i_dati_sono_quelli_del_prd(self):
        r = subprocess.run([sys.executable, str(ESTRATTORE), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class PE(unittest.TestCase):
    def test_tre_tracce_del_prd(self):
        for traccia, liv2, liv20 in (("lenta", 3000, 5350000), ("media", 2000, 3600000),
                                     ("veloce", 1300, 2400000)):
            soglie, _ = X.soglie_di("pf1e", traccia)
            self.assertEqual((soglie[1], soglie[2], soglie[20]), (0, liv2, liv20))

    def test_predefinito_resta_3_5(self):
        soglie, etichetta = X.soglie_di()
        self.assertIs(soglie, X.THRESHOLDS)
        self.assertEqual(etichetta, "3.5")

    def test_livello_e_mancanti(self):
        soglie, _ = X.soglie_di("pf1e", "media")
        self.assertEqual(X.next_threshold(1025, soglie), (1, 975))
        self.assertEqual(X.next_threshold(1025), (2, 1975))  # 3.5, come prima

    def test_sistema_spento_rifiutato(self):
        with self.assertRaises(SystemExit):
            X.soglie_di("pf2e")


class Incontri(unittest.TestCase):
    def test_somma_dei_pe(self):
        f = E.combina_gs_pf1e
        self.assertEqual(f([10, 10]), 12)
        self.assertEqual(f([10, 10, 10]), 13)       # 3.5: 13,17
        self.assertEqual(f([0.5, 0.5]), 1)          # 400 PE = GS 1
        self.assertEqual(f([25, 25]), 27)           # oltre la tabella si raddoppia ogni 2 GS
        self.assertEqual(f([]), 0)

    def test_predefinito_resta_3_5(self):
        self.assertIs(E.COMBINA, E.combine_el)


class Tesoro(unittest.TestCase):
    def test_valori_per_incontro(self):
        tab, etichetta = L.tesoro_di("pf1e", "media")
        self.assertEqual((tab[1], tab[13], tab[20]), (260, 11600, 67000))
        self.assertIn("velocità media", etichetta)
        self.assertEqual(L.tesoro_di("pf1e", "veloce")[0][20], 100000)

    def test_predefinito_resta_3_5(self):
        self.assertIsNone(L.TESORO_SISTEMA)


class ClassiERazze(unittest.TestCase):
    DRAPPO = "10-stand-alone/Il-Drappo-di-Tarsilia/x.md"

    def test_classi_pf1e_solo_nei_moduli_pf1e(self):
        paren = "Umano Inquisitore 9/Fattucchiere 3, GS 11"
        self.assertEqual(C.classi_da_paren(paren, self.DRAPPO), "fattucchiere 3/inquisitore 9")
        self.assertIsNone(C.classi_da_paren(paren, "07_x/a.md"))
        self.assertIsNone(C.classi_da_paren(paren))

    def test_il_3_5_resta_quello_di_prima(self):
        classi, razze = C.entita_di("dnd35")
        self.assertEqual(classi, frozenset(C.CLASSI))
        self.assertEqual(razze, frozenset(C.RAZZE))

    def test_pf1e_contiene_il_3_5(self):
        classi, razze = C.entita_di("pf1e")
        self.assertTrue(frozenset(C.CLASSI) <= classi)
        self.assertTrue(frozenset(C.RAZZE) <= razze)


class Creature(unittest.TestCase):
    def blocco(self, tipo, taglia="medium", gs=7, seed=42):
        sb, _ = G.genera(gs, tipo=tipo, taglia=taglia, rng=random.Random(seed))
        return sb, CP.converti(sb, tipo, taglia)

    def test_non_morto_tiene_i_pf_col_carisma(self):
        sb, (pf, conto) = self.blocco("undead")
        self.assertEqual(pf.pf_dado.split("d")[1], "8")       # 3.5 d12, PF1e d8
        self.assertEqual(pf.pf, sb.pf)
        self.assertIn("Car 22", pf.attributi)
        self.assertIn("Cos —", pf.attributi)

    def test_costrutto_bab_pieno(self):
        sb, (pf, conto) = self.blocco("construct")
        self.assertTrue(any("BAB +9 (3.5: +6)" in r for r in conto), conto)
        self.assertTrue(any("⚠" in r for r in conto))           # pf bonus per taglia: lo dice

    def test_bmc_dmc_con_la_taglia(self):
        sb, (pf, conto) = self.blocco("dragon", taglia="huge", gs=14, seed=7)
        voce = next(v for v in pf.voci if v.startswith("Manovre"))
        self.assertEqual(voce, "Manovre: BMC +27, DMC 37")      # 19 BAB +6 For +2 taglia

    def test_gigante_diventa_umanoide(self):
        sb, (pf, conto) = self.blocco("giant")
        self.assertIn("humanoid", pf.tipo)
        self.assertIn("generato-PRD-PF1e", pf.fonte)

    def test_esterno_due_ts_a_scelta_deterministici(self):
        self.assertEqual(CP.ts_buoni("outsider", S.dati("pf1e", "creature.costruzione")["tipi"]["outsider"]),
                         ("temp", "rifl"))

    def test_classi_rifiutate(self):
        with self.assertRaises(SystemExit) as e:
            G.main(["--gs", "7", "--sistema", "pf1e", "--classe", "guerriero:3"])
        self.assertIn("livelli di classe", str(e.exception))


if __name__ == "__main__":
    unittest.main()
