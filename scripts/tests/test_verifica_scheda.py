"""verifica_scheda.py: talenti e numeri di una scheda in una chiamata (ADR-0124)."""
from __future__ import annotations

import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import verifica_scheda as V  # noqa: E402

ABISHAI = ROOT / "Bestiario" / "mostri" / "abishai-azzurro-mano-cr11.md"
KRUSK = ROOT / "Bestiario" / "villain" / "krusk-sfondacancelli-cr14.md"


class Scheda(unittest.TestCase):
    def _esegui(self, *argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = V.main([*argv, "--json"])
        return rc, json.loads(buf.getvalue())

    def test_scheda_pulita(self):
        rc, d = self._esegui(str(ABISHAI), "--check")
        self.assertEqual((rc, d["violazioni"]), (0, []))

    def test_talenti_e_numeri_nella_stessa_uscita(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / KRUSK.name
            testo = KRUSK.read_text(encoding="utf-8")
            # un BAB sbagliato in più, oltre al talento che già manca
            testo = re.sub(r"(BAB \+)(\d+)", lambda m: m.group(1) + str(int(m.group(2)) + 3), testo)
            p.write_text(testo, encoding="utf-8")
            rc, d = self._esegui(str(p), "--check")
        self.assertEqual(rc, 1)
        voci = d["violazioni"] + d["non_verificabili"]
        self.assertIn(("talenti", "talento"), {(x["verifica"], x["regola"]) for x in voci})
        for x in d["violazioni"]:
            self.assertTrue({"file", "riga", "verifica", "regola", "atteso", "ha", "fonte"} <= set(x), x)

    def test_un_numero_sbagliato_si_vede_e_corretto_sparisce(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / ABISHAI.name
            giusto = ABISHAI.read_text(encoding="utf-8")
            p.write_text(giusto.replace("BAB +14", "BAB +16"), encoding="utf-8")
            rc, d = self._esegui(str(p), "--check")
            v = [x for x in d["violazioni"] if x["regola"] == "numero.BAB"]
            self.assertEqual((rc, [(x["ha"], x["atteso"]) for x in v]), (1, [(16, 14)]))
            self.assertIsNotNone(v[0]["riga"])
            # l'agente corregge col valore atteso e richiama
            p.write_text(p.read_text(encoding="utf-8").replace("BAB +16", f"BAB +{v[0]['atteso']}"),
                         encoding="utf-8")
            self.assertEqual(self._esegui(str(p), "--check")[0], 0)

    def test_dossier_i_numeri_non_si_giudicano(self):
        p = ROOT / "Bestiario" / "png" / "Lythiel" / "Lythiel.md"
        _, d = self._esegui(str(p))
        self.assertFalse([x for x in d["violazioni"] if x["verifica"] == "numeri"])

    def test_sola_lettura(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / KRUSK.name
            shutil.copy(KRUSK, p)
            prima = p.read_bytes()
            self._esegui(str(p))
            self.assertEqual(p.read_bytes(), prima)

    def test_percorso_inesistente(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(V.main(["non/esiste.md"]), 2)


if __name__ == "__main__":
    unittest.main()
