"""Test per la coppia state.yaml → state.md (ADR-0017, lotto G2-bis).

Il valore del lotto sta in un'affermazione forte: **un fatto senza tempo
dichiarato non è esprimibile**. Questi test la verificano davvero, invece di
limitarsi a controllare che il file corrente sia valido — e coprono il rischio
opposto, che il rendering perda contenuto di canone.
"""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_state as vs  # noqa: E402
import render_state as rs  # noqa: E402

import yaml  # noqa: E402

STATE = yaml.safe_load((ROOT / "campaign" / "state.yaml").read_text(encoding="utf-8"))
SCHEMA = __import__("json").loads(
    (ROOT / "scripts" / "schemas" / "campaign_state.schema.json").read_text(encoding="utf-8")
)


class TestStatoReale(unittest.TestCase):
    def test_state_yaml_e_valido(self):
        errs = vs.validate_schema(STATE, SCHEMA) + vs.coherence_rules(STATE)
        self.assertEqual(errs, [], f"state.yaml non valido: {errs}")

    def test_state_md_in_sync(self):
        md = (ROOT / "campaign" / "state.md").read_text(encoding="utf-8")
        new, missing = rs.apply_regions(md, STATE)
        self.assertEqual(missing, [], f"regioni assenti: {missing}")
        self.assertEqual(new, md, "state.md fuori sync: rigenerare con render_state.py")

    def test_rendering_deterministico(self):
        """Due esecuzioni identiche danno byte identici (requisito ADR-0012)."""
        for fn in rs.RENDERERS.values():
            self.assertEqual(fn(STATE), fn(copy.deepcopy(STATE)))


class TestIlVincoloCentrale(unittest.TestCase):
    """Un fatto senza tempo dichiarato deve essere RIFIUTATO, non tollerato."""

    def test_arco_senza_tempo_e_rifiutato(self):
        d = copy.deepcopy(STATE)
        del d["archi"][0]["tempo"]
        errs = vs.validate_schema(d, SCHEMA)
        self.assertTrue(any("tempo" in e for e in errs), f"atteso errore su 'tempo', ottenuto {errs}")

    def test_tempo_inventato_e_rifiutato(self):
        d = copy.deepcopy(STATE)
        d["archi"][0]["tempo"] = "forse"
        errs = vs.validate_schema(d, SCHEMA)
        self.assertTrue(any("forse" in e for e in errs))

    def test_pg_senza_oggi_e_rifiutato(self):
        """`oggi` è obbligatorio: è la colonna che si usa in sessione."""
        d = copy.deepcopy(STATE)
        del d["party"][0]["oggi"]
        errs = vs.validate_schema(d, SCHEMA)
        self.assertTrue(any("oggi" in e for e in errs))

    def test_chiave_non_prevista_e_rifiutata(self):
        d = copy.deepcopy(STATE)
        d["party"][0]["posizione"] = "Hammerfist"
        errs = vs.validate_schema(d, SCHEMA)
        self.assertTrue(any("posizione" in e for e in errs),
                        "una chiave fuori contratto deve fallire, non passare in silenzio")


class TestRegoleDiCoerenza(unittest.TestCase):
    def test_R1_id_inferred_duplicati(self):
        d = copy.deepcopy(STATE)
        d["inferred"].append(copy.deepcopy(d["inferred"][0]))
        self.assertTrue(any(e.startswith("R1") for e in vs.coherence_rules(d)))

    def test_R2_dove_verso_sezione_ignota(self):
        d = copy.deepcopy(STATE)
        d["inferred"][0]["dove"] = "sezione_inventata[x]"
        self.assertTrue(any(e.startswith("R2") for e in vs.coherence_rules(d)))

    def test_R4_cruscotto_fuori_ordine(self):
        """Un arco giocato dopo uno preparato è una contraddizione temporale."""
        d = copy.deepcopy(STATE)
        d["archi"][-1]["tempo"] = "giocato"
        self.assertTrue(any(e.startswith("R4") for e in vs.coherence_rules(d)))

    def test_R5_preparato_copia_di_oggi(self):
        d = copy.deepcopy(STATE)
        d["party"][0]["preparato"] = d["party"][0]["oggi"]
        self.assertTrue(any(e.startswith("R5") for e in vs.coherence_rules(d)))


class TestNessunaPerditaDiCanone(unittest.TestCase):
    """Il rischio vero della migrazione: perdere testo passando da tabella a dati."""

    ANCORE = [
        ("party", "Sala della Forgia Eterna"),
        ("party", "MORTA"),
        ("party", "Peso del Mondo"),
        ("artefatti", "Cuore di Moradin"),
        ("artefatti", "Mind Blank"),
        ("archi", "Battaglia di Hammerfist"),
    ]

    def test_le_ancore_di_canone_sopravvivono_al_rendering(self):
        for regione, frase in self.ANCORE:
            reso = rs.RENDERERS[regione](STATE)
            self.assertIn(frase, reso, f"«{frase}» persa nel rendering di {regione}")

    def test_hella_e_morta_oggi_e_viva_solo_nel_preparato(self):
        """La riga che ha originato tutto l'audit: deve restare inequivocabile."""
        hella = next(p for p in STATE["party"] if p["pg"] == "Hella")
        self.assertIn("MORTA", hella["oggi"])
        self.assertIn("Treant", hella["preparato"] or "")


class TestPipelineADR0007SuiFileVeri(unittest.TestCase):
    """Guardia contro la regressione del 2026-08-05.

    Spostando lo storico fuori da `state.md` §8 (G2-bis) si era rotto
    `state_apply --migrate`, che cercava la regione `changelog` dentro
    `state.md`. **La CI non se n'è accorta** perché `test_state_apply.py` gira
    su una fixture in memoria: nessun test toccava i file reali.

    Questi due test chiudono quel buco. Sono in sola lettura — non scrivono
    canone, si limitano a verificare che le regioni siano ancora *migrabili*
    dove ora vivono.
    """

    def test_state_md_resta_migrabile(self):
        import state_apply as sa
        text = (ROOT / "campaign" / "state.md").read_text(encoding="utf-8")
        _, added = sa.migrate(text)
        self.assertIn("march-clock", added,
                      "state.md non espone più l'ancora del March Clock: "
                      "la pipeline ADR-0007 non potrebbe migrarlo")

    def test_lo_storico_resta_migrabile(self):
        import state_apply as sa
        clog = ROOT / "campaign" / "state-changelog.md"
        self.assertTrue(clog.exists(), "campaign/state-changelog.md è sparito")
        _, added = sa.migrate_changelog(clog.read_text(encoding="utf-8"))
        self.assertIn("changelog", added,
                      "lo storico non è più migrabile: state_apply non potrebbe "
                      "appendere le righe di fine sessione")


if __name__ == "__main__":
    unittest.main()
