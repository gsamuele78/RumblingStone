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
             "livelli": {"fighter": 8}, "dv": 8, "lic": 0, "talenti": ["Improved Shield Bash"], "ignoti": []}
        self.assertEqual(V.verifica(f), ([], []))
        f["livelli"] = {}
        self.assertEqual([x["regola"] for x in V.verifica(f)[0]], ["talento"])

    def test_senza_classi_il_livello_d_incantatore_non_si_giudica(self):
        f = {"file": "x.md", "riga": 1, "sistema": "dnd35", "car": CAR, "bab": 5,
             "livelli": {}, "dv": 11, "lic": 0, "talenti": ["Scribe Scroll"], "ignoti": []}
        viol, nv = V.verifica(f)
        self.assertEqual((viol, [x["regola"] for x in nv]), ([], ["lic"]))

    def test_percorso_inesistente(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(V.main(["non/esiste.md"]), 2)


if __name__ == "__main__":
    unittest.main()
