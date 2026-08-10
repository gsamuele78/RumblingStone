"""Test per inventory_inferred.py (finding C4, lotto G4).

Il test che conta è quello sulla **classificazione**. Un ratchet che conta
insieme i marcatori dei documenti vivi e quelli dei changelog produce un numero
che non può scendere — si smaltisce un debito, si scrive nel changelog che l'hai
smaltito, e il totale resta uguale. Un gate così viene disattivato entro una
settimana, ed è la stessa dinamica del finding T3.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import inventory_inferred as inv  # noqa: E402


class TestClassificazione(unittest.TestCase):
    """La distinzione che rende il ratchet capace di scendere."""

    def test_i_documenti_vivi_sono_debito_aperto(self):
        for rel in ("campaign/state.yaml",
                    "07_il Portale/ARC07-DEF-1.md",
                    "Bestiario/png/Lorana/Lorana.md",
                    "PG/Artefatti/x.md"):
            self.assertEqual(inv.classe(rel), "aperti", rel)

    def test_i_piani_e_i_changelog_sono_storici(self):
        """Raccontano un debito, non lo aprono."""
        for rel in ("plans/PIANO-X.md", "plans/CHANGELOG.md",
                    "campaign/state-changelog.md"):
            self.assertEqual(inv.classe(rel), "storici", rel)

    def test_i_documenti_di_audit_sono_meta(self):
        """Citano il marcatore per misurarlo."""
        self.assertEqual(inv.classe("docs/audit/AUDIT-2026-08-SINTESI.md"), "meta")

    def test_la_documentazione_normale_non_e_meta(self):
        """Solo `docs/audit/`: una guida che marca un'inferenza ha un debito vero."""
        self.assertEqual(inv.classe("docs/guides/GUIDA-IMMAGINI.md"), "aperti")


class TestScansione(unittest.TestCase):
    def test_riconosce_nudi_e_parlanti(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.md"
            f.write_text("a `[INFERRED]` b\n"
                         "c `[INFERRED — needs DM confirmation]` d\n"
                         "e `[INFERRED: durata 3 round]` f\n", encoding="utf-8")
            voci = inv.scansiona(Path(d))
            self.assertEqual(len(voci), 3)
            note = [v["nota"] for v in voci]
            self.assertEqual(note[0], "", "il marcatore nudo non ha nota")
            self.assertEqual(note[1], "needs DM confirmation")
            self.assertEqual(note[2], "durata 3 round")

    def test_piu_marcatori_sulla_stessa_riga_contano_tutti(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "x.md").write_text("[INFERRED] e [INFERRED]\n", encoding="utf-8")
            self.assertEqual(len(inv.scansiona(Path(d))), 2)

    def test_ignora_le_cartelle_generate(self):
        with tempfile.TemporaryDirectory() as d:
            gen = Path(d) / "build"
            gen.mkdir()
            (gen / "x.md").write_text("[INFERRED]\n", encoding="utf-8")
            self.assertEqual(inv.scansiona(Path(d)), [])


class TestRatchet(unittest.TestCase):
    def test_la_baseline_esiste_ed_e_allineata(self):
        """Se salta l'allineamento, la CI lo dice al primo push — non a caso."""
        self.assertTrue(inv.BASELINE.exists(), "baseline assente: eseguire --update-baseline")
        atteso = json.loads(inv.BASELINE.read_text(encoding="utf-8"))["aperti"]
        aperti = sum(1 for v in inv.scansiona(inv.ROOT) if v["classe"] == "aperti")
        self.assertLessEqual(
            aperti, atteso,
            f"il debito aperto è salito ({aperti} > {atteso}). Se è voluto, "
            "aggiornare la baseline nello stesso commit.")

    def test_check_fallisce_se_sale(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "vivo.md").write_text("[INFERRED]\n" * 5, encoding="utf-8")
            vecchia = inv.BASELINE.read_text(encoding="utf-8")
            try:
                inv.BASELINE.write_text(json.dumps({"aperti": 0}) + "\n", encoding="utf-8")
                self.assertEqual(inv.main(["--check", "--path", d]), 1)
            finally:
                inv.BASELINE.write_text(vecchia, encoding="utf-8")


class TestInventarioGenerato(unittest.TestCase):
    def test_e_in_sync_col_repo(self):
        """L'inventario è generato: se qualcuno lo modifica a mano, si vede."""
        atteso = inv.scrivi_inventario(inv.scansiona(inv.ROOT), inv.record_tipizzati())
        self.assertEqual(
            inv.INVENTARIO.read_text(encoding="utf-8"), atteso,
            "INFERRED-INVENTARIO.md non è allineato: rigenerare con "
            "`python3 scripts/inventory_inferred.py`")

    def test_dichiara_di_essere_generato(self):
        testa = inv.INVENTARIO.read_text(encoding="utf-8").splitlines()[0]
        self.assertIn("GENERATO", testa)


if __name__ == "__main__":
    unittest.main()
