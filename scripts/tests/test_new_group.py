"""Test del reset per gruppo nuovo (lotto G2-quater).

Il difetto che questi test impediscono di ripetere: `new-campaign-group.sh`
azzerava **solo** `state.md` e `sessions/`. Ogni volta che il repo ha aggiunto
un file di stato — `state.yaml` e `state-changelog.md` il 2026-08-05 — il
gruppo nuovo ha cominciato a **ereditare i dati del precedente**, in silenzio.

Il test decisivo non è «il reset gira»: è **«dopo il reset non resta traccia
del gruppo precedente»**, verificato cercando i nomi dei PG. Così la falla si
riapre solo se qualcuno aggiunge un file di stato *e* ignora un test rosso.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

SCRIPT = ROOT / "scripts" / "new-campaign-group.sh"
TEMPLATES = ROOT / "campaign" / "templates"

# I nomi del primo gruppo: se ricompaiono dopo un reset, il reset perde.
TRACCE = ("Thorik", "Hella", "Tordek", "Artemis", "Ghaurush", "Sonjak")


def _file_azzerati_dallo_script() -> set[str]:
    """I path che lo script copia da template o cancella."""
    testo = SCRIPT.read_text(encoding="utf-8")
    cp = set(re.findall(r"^cp campaign/templates/\S+ (\S+)$", testo, re.M))
    rm = set(re.findall(r"^rm -f ([^\n]+)$", testo, re.M))
    for riga in rm:
        for tok in riga.split():
            if tok.startswith("campaign/"):
                cp.add(tok)
    return cp


class TestCoperturaDelReset(unittest.TestCase):
    def test_ogni_template_di_stato_esiste(self):
        for tpl in ("state-blank.md", "state-blank.yaml",
                    "state-changelog-blank.md", "chronicle-blank.md"):
            self.assertTrue((TEMPLATES / tpl).exists(), f"template mancante: {tpl}")

    def test_tutti_i_file_di_stato_sono_coperti(self):
        """Il test che sarebbe servito il 2026-08-05."""
        coperti = _file_azzerati_dallo_script()
        attesi = {
            "campaign/state.md",
            "campaign/state.yaml",
            "campaign/state-changelog.md",
            "campaign/lore/campaign-chronicle.md",
        }
        mancanti = attesi - coperti
        self.assertEqual(mancanti, set(),
                         f"lo script di reset non azzera: {sorted(mancanti)} — "
                         "un gruppo nuovo erediterebbe i dati del precedente")

    def test_le_sessioni_e_i_recap_si_svuotano(self):
        testo = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("campaign/sessions/*.md", testo)
        self.assertIn("campaign/recaps/", testo)

    def test_la_premessa_condivisa_NON_si_azzera(self):
        """Il prodotto resta: azzerarlo costringerebbe ogni DM a riscriverlo."""
        self.assertNotIn("campaign-premise.md", _file_azzerati_dallo_script())


class TestTemplatePuliti(unittest.TestCase):
    def test_nessuna_traccia_del_primo_gruppo_nei_template(self):
        for tpl in TEMPLATES.glob("*blank*"):
            testo = tpl.read_text(encoding="utf-8")
            for nome in TRACCE:
                self.assertNotIn(nome, testo,
                                 f"{tpl.name} contiene «{nome}»: non è un template vuoto")

    def test_il_template_yaml_e_valido_e_rispetta_il_vincolo(self):
        """Un gruppo nuovo deve partire da uno stato che passa il gate."""
        import json
        import validate_state as vs
        import yaml
        data = yaml.safe_load((TEMPLATES / "state-blank.yaml").read_text(encoding="utf-8"))
        schema = json.loads(
            (ROOT / "scripts" / "schemas" / "campaign_state.schema.json").read_text(encoding="utf-8"))
        errs = vs.validate_schema(data, schema) + vs.coherence_rules(data, schema)
        self.assertEqual(errs, [], f"il template di partenza non è valido: {errs}")

    def test_il_template_markdown_ha_tutte_le_regioni_generate(self):
        """Senza i marcatori, un gruppo nuovo troverebbe la CI rossa al primo push."""
        import render_state as rs
        testo = (TEMPLATES / "state-blank.md").read_text(encoding="utf-8")
        mancanti = [n for n in rs.RENDERERS if f"<!-- gen:state:{n} -->" not in testo]
        self.assertEqual(mancanti, [], f"regioni assenti dal template: {mancanti}")


class TestCronacaSeparataDallaPremessa(unittest.TestCase):
    """La distinzione che rende sensata la separazione: prodotto vs partita."""

    def test_i_due_file_esistono_e_il_vecchio_non_c_e_piu(self):
        lore = ROOT / "campaign" / "lore"
        self.assertTrue((lore / "campaign-premise.md").exists())
        self.assertTrue((lore / "campaign-chronicle.md").exists())
        self.assertFalse((lore / "campaign-history.md").exists(),
                         "campaign-history.md andava spaccato, non duplicato")

    def test_la_premessa_non_afferma_cosa_e_successo_a_questo_party(self):
        """L'invariante vero.

        Non è «la premessa non nomina mai un PG» — sarebbe troppo stretto in un
        repo dove gli artefatti portano il nome del portatore. È **la premessa
        non racconta eventi**: quelli sono partita. È il test che ha fatto
        spostare PART 3 (catena dei dungeon) nella cronaca, perché le sue
        annotazioni dicevano dove Hella è morta e cosa Artemis ha rifiutato.
        """
        testo = (ROOT / "campaign" / "lore" / "campaign-premise.md").read_text(encoding="utf-8")
        eventi = ["Hella Oakenshield DIES", "Thorik passes trial",
                  "Artemis REJECTS", "Hella returns as Treant"]
        trovati = [e for e in eventi if e in testo]
        self.assertEqual(trovati, [],
                         f"la premessa condivisa afferma eventi del gruppo: {trovati}")

    def test_la_cronaca_contiene_il_party(self):
        testo = (ROOT / "campaign" / "lore" / "campaign-chronicle.md").read_text(encoding="utf-8")
        self.assertIn("Thorik", testo)


if __name__ == "__main__":
    unittest.main()
