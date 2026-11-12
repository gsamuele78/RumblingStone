"""verifica_talenti.py e la regola strutturata dei prerequisiti (ADR-0124).

Tre cose:
- D1 e D2, i difetti trovati misurando Prolog contro Python: le classi 3.5 in
  italiano contro i prerequisiti in inglese, e il livello del personaggio di
  Leadership che nessuno scriveva;
- la forma dell'uscita che l'agente legge via MCP (regola, atteso, ha, riga);
- il giro di correzione: una scheda segnalata, corretta, torna pulita.
"""
from __future__ import annotations

import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from dmcore import talenti as TL  # noqa: E402
import verifica_talenti as V  # noqa: E402

CAR = {"For": 16, "Des": 13, "Cos": 14, "Int": 13, "Sag": 10, "Car": 10}
KRUSK = REPO / "Bestiario/villain/krusk-sfondacancelli-cr14.md"


class Regola(unittest.TestCase):
    def test_d1_guerriero_in_italiano_prende_specializzazione(self):
        for livelli in ({"guerriero": 4}, {"fighter": 4}):
            s = TL.Stato(car=CAR, bab=4, livelli=livelli, talenti=["Weapon Focus"])
            self.assertEqual(TL.manca("dnd35", "Weapon Specialization", s), [], livelli)

    def test_d1_guerriero_3_non_la_prende(self):
        s = TL.Stato(car=CAR, bab=3, livelli={"guerriero": 3}, talenti=["Weapon Focus"])
        v = TL.violazioni("dnd35", "Weapon Specialization", s)
        self.assertEqual([(x["regola"], x["atteso"], x["ha"]) for x in v], [("classe.fighter", 4, 3)])

    def test_d2_leadership_conta_il_livello_del_personaggio(self):
        self.assertEqual(TL.manca("dnd35", "Leadership", TL.Stato(car=CAR, bab=4, livelli={"guerriero": 6})), [])
        self.assertEqual(TL.manca("dnd35", "Leadership", TL.Stato(car=CAR, bab=4, dv=6)), [])
        v = TL.violazioni("dnd35", "Leadership", TL.Stato(car=CAR, bab=4, livelli={"guerriero": 5}))
        self.assertEqual([(x["regola"], x["atteso"], x["ha"]) for x in v], [("classe.character", 6, 5)])

    def test_manca_e_violazioni_dicono_lo_stesso(self):
        s = TL.Stato(car={**CAR, "For": 12}, bab=2, talenti=[])
        v = TL.violazioni("dnd35", "Great Cleave", s)
        self.assertEqual([x["testo"] for x in v], TL.manca("dnd35", "Great Cleave", s))
        self.assertIn(("car.For", 13, 12), [(x["regola"], x["atteso"], x["ha"]) for x in v])
        self.assertIn(("bab", 4, 2), [(x["regola"], x["atteso"], x["ha"]) for x in v])

    def test_bonus_del_monaco_senza_prerequisiti(self):
        self.assertEqual(TL.bonus_senza_prerequisiti("dnd35", "Improved Trip", {"monk": 6}), "monk")
        self.assertIsNone(TL.bonus_senza_prerequisiti("dnd35", "Improved Trip", {"monk": 5}))
        self.assertIsNone(TL.bonus_senza_prerequisiti("dnd35", "Improved Trip", {"fighter": 6}))


def _r(en: str) -> dict:
    return {"en": en, "sistema": "dnd35", "fonte": "srd", "verificabile": True}


class Strumento(unittest.TestCase):
    def _esegui(self, *argv) -> "tuple[int, dict]":
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = V.main([*argv, "--json"])
        return rc, json.loads(buf.getvalue())

    def test_uscita_per_l_agente(self):
        rc, d = self._esegui(str(KRUSK))
        self.assertEqual(rc, 0)
        v = d["violazioni"]
        self.assertEqual([(x["talento"], x["regola"], x["atteso"]) for x in v],
                         [("Diehard", "talento", "Endurance")])
        self.assertEqual(v[0]["file"], "Bestiario/villain/krusk-sfondacancelli-cr14.md")
        riga = KRUSK.read_text(encoding="utf-8").splitlines()[v[0]["riga"] - 1]
        self.assertIn("Duro a morire", riga)

    def test_giro_di_correzione(self):
        """Segnalata, corretta come dice la violazione, pulita: --check passa da 1 a 0."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / KRUSK.name
            shutil.copy(KRUSK, p)
            self.assertEqual(self._esegui(str(p), "--check")[0], 1)
            testo = p.read_text(encoding="utf-8").replace("Duro a morire", "Resistenza fisica, Duro a morire", 1)
            p.write_text(testo, encoding="utf-8")
            rc, d = self._esegui(str(p), "--check")
            self.assertEqual((rc, d["violazioni"]), (0, []))

    def test_competenza_della_classe_non_e_una_violazione(self):
        f = {"file": "x.md", "riga": 1, "sistema": "dnd35", "car": CAR, "bab": 8,
             "livelli": {"fighter": 8}, "dv": 8, "lic": 0, "talenti": [_r("Improved Shield Bash")], "senza_regole": [], "ignoti": []}
        self.assertEqual(V.verifica(f), ([], []))
        f["livelli"] = {}
        self.assertEqual([x["regola"] for x in V.verifica(f)[0]], ["talento"])

    def test_senza_classi_il_livello_d_incantatore_non_si_giudica(self):
        f = {"file": "x.md", "riga": 1, "sistema": "dnd35", "car": CAR, "bab": 5,
             "livelli": {}, "dv": 11, "lic": 0, "talenti": [_r("Scribe Scroll")], "senza_regole": [], "ignoti": []}
        viol, nv = V.verifica(f)
        self.assertEqual((viol, [x["regola"] for x in nv]), ([], ["lic"]))

    def test_cascata_srd_poi_manuali_35(self):
        # SRD 3.5, anche i talenti dei mostri; poi i manuali 3.5 (nome sì, prerequisiti no)
        self.assertEqual(V.risolvi("dnd35", "Colpo terrificante")["fonte"], "srd-mostri")
        self.assertEqual(V.risolvi("dnd35", "Incantesimi Focalizzati")["en"], "Spell Focus")
        # manuali 3.5: i prerequisiti vengono dai dati PCGen (talenti_manuali.toml)
        r = V.risolvi("dnd35", "Robustezza Migliorata")
        self.assertEqual((r["en"], r["verificabile"], r["fonte"]),
                         ("Improved Toughness", True, "3.5 Complete Warrior"))
        # un manuale che i dati PCGen non coprono: nome sì, prerequisiti no
        r = V.risolvi("dnd35", "Abjurative Potency")
        self.assertEqual((r["verificabile"], r["fonte"][:3]), (False, "3.5"))
        # l'inglese fra parentesi decide quando l'italiano non è in lessico
        self.assertEqual(V.risolvi("dnd35", "Rune Incise (Inscribe Rune)")["en"], "Inscribe Rune")
        self.assertIsNone(V.risolvi("dnd35", "Virata"))

    def test_cascata_ultima_fonte_pf1e(self):
        # un talento che nessun libro 3.5 ha si verifica col PRD PF1e
        r = V.risolvi("dnd35", "Furious Focus")
        self.assertEqual((r["sistema"], r["verificabile"]), ("pf1e", True))
        self.assertTrue(r["fonte"].startswith("pf1e"))

    def test_talento_di_manuale_non_e_ne_buono_ne_sbagliato(self):
        f = {"file": "x.md", "riga": 1, "sistema": "dnd35", "car": CAR, "bab": 8, "livelli": {"fighter": 8},
             "dv": 8, "lic": 0, "talenti": [], "senza_regole": [V.risolvi("dnd35", "Abjurative Potency")],
             "ignoti": []}
        viol, nv = V.verifica(f)
        self.assertEqual((viol, [(x["regola"], x["talento"]) for x in nv]), ([], [("fonte", "Abjurative Potency")]))

    def test_prerequisiti_dei_manuali_35(self):
        # Critico Poderoso (Complete Warrior): Arma Focalizzata e BAB +4
        st = TL.Stato(car=CAR, bab=3, livelli={"fighter": 3}, talenti=[], dv=3)
        self.assertEqual(sorted(x["regola"] for x in TL.violazioni("dnd35", "Power Critical", st)),
                         ["bab", "talento"])
        # Ira Intimidatoria chiede l'ira: un guerriero no, un barbaro sì
        self.assertEqual([x["regola"] for x in TL.violazioni("dnd35", "Intimidating Rage", st)], ["capacita"])
        st = TL.Stato(car=CAR, bab=3, livelli={"barbarian": 3}, talenti=[], dv=3)
        self.assertEqual(TL.violazioni("dnd35", "Intimidating Rage", st), [])
        # un nome dell'SRD non viene mai sostituito dal manuale
        self.assertEqual(TL.dati("dnd35")["talenti"]["Power Attack"]["libro"], "srd")

    def test_classe_che_la_lettura_non_conosce(self):
        f = {"file": "x.md", "riga": 1, "sistema": "dnd35", "car": CAR, "bab": 5, "livelli": {"paladin": 8},
             "dv": 10, "lic": 4, "talenti": [V.risolvi("dnd35", "Divine Armor")], "senza_regole": [],
             "ignoti": [], "classi_ignote": ["Hammer of Moradin 2"]}
        viol, nv = V.verifica(f)
        self.assertEqual(viol, [])
        self.assertIn("Hammer of Moradin 2", nv[0]["nota"])

    def test_percorso_inesistente(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(V.main(["non/esiste.md"]), 2)



class PrerequisitiFisici(unittest.TestCase):
    """Movimento, taglia, tipo e attacchi naturali letti dalla scheda (ADR-0124 §9)."""

    FATTI = {"movimenti": {"volo": 60}, "taglia": -2, "tipo": "dragon", "attacchi_naturali": 4,
             "attacco_completo": True, "armatura_naturale": True, "soffio": True,
             "ts_base": {"temp": 5, "rifl": 1, "vol": 1}}

    def test_soddisfatti(self):
        import verifica_talenti as VT
        for p in ("Fly speed", "fly speed 20", "Size Huge or larger", "size Large or larger",
                  "Three or more natural attacks", "Natural armor", "breath weapon", "dragon type",
                  "Base Fortitude save bonus +2"):
            self.assertTrue(VT.giudica_altro(p, self.FATTI)[0], p)

    def test_violati_con_il_fatto_che_la_scheda_ha(self):
        import verifica_talenti as VT
        a_terra = {**self.FATTI, "movimenti": {}, "taglia": 0, "attacchi_naturali": 1}
        self.assertEqual(VT.giudica_altro("Fly speed", a_terra), (False, "nessuna velocità di volo"))
        self.assertEqual(VT.giudica_altro("size Large or larger", a_terra), (False, "taglia medium"))
        self.assertFalse(VT.giudica_altro("Three or more natural attacks", a_terra)[0])
        self.assertFalse(VT.giudica_altro("Base Reflex save bonus +2", a_terra)[0])

    def test_senza_la_riga_non_si_giudica(self):
        import verifica_talenti as VT
        vuoti = {"movimenti": None, "taglia": None, "tipo": None, "attacchi_naturali": None,
                 "armatura_naturale": None, "soffio": False, "ts_base": None}
        for p in ("Fly speed", "size Large or larger", "Three or more natural attacks", "Natural armor",
                  "breath weapon", "Base Will save bonus +4", "Member of the Ankheg Tribe"):
            self.assertIsNone(VT.giudica_altro(p, vuoti), p)
        # l'attacco singolo non prova che gli attacchi naturali siano pochi
        solo_singolo = {**self.FATTI, "attacchi_naturali": 1, "attacco_completo": False}
        self.assertIsNone(VT.giudica_altro("Three or more natural attacks", solo_singolo))

    def test_dalla_scheda_vera(self):
        import verifica_talenti as VT
        f = VT.leggi(Path(__file__).resolve().parents[2] / "Bestiario" / "mostri" / "abishai-azzurro-mano-cr11.md")
        self.assertEqual(f["fisici"]["movimenti"], {"volo": 60})
        self.assertEqual(f["fisici"]["attacchi_naturali"], 4)
        viol, nv = VT.verifica(f)
        self.assertFalse([v for v in viol + nv if v["talento"] in ("Flyby Attack", "Multiattack")])

if __name__ == "__main__":
    unittest.main()
