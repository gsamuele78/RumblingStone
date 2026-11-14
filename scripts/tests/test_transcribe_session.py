"""transcribe_session (ADR-0135): la bozza della trascrizione non e' canone.

La CI non ha whisper.cpp: qui si prova tutto cio' che sta attorno, su un JSON
nel formato di `whisper-cli -oj`. Consenso, niente scritture nel repo, uscita
pulita senza binario, sezioni pubbliche vuote, segno di bozza rispettato da
`state_apply` e `session_recap`, misure.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import session_recap  # noqa: E402
import state_apply  # noqa: E402
import transcribe_session as ts  # noqa: E402
from dmcore.bozza_trascrizione import MARCATORE, e_bozza  # noqa: E402

NOMI = ["Thorik", "Tordek", "Hella", "Artemis", "Ghaurush", "Cenerevento",
        "Zin'thara Vel'Ryn", "Hammerfist"]

SEGMENTI = [
    ("00:00:00,000", "Bene, riprendiamo davanti a Hammerist."),
    ("00:00:41,000", "Lo stregone Gaurush ride e sparisce verso il fiume."),
    ("00:01:10,000", "Trovate 300 monete d'oro e due pozioni."),
    ("00:01:30,000", "Ognuno guadagna 1200 punti esperienza."),
    ("00:01:45,000", "Il March Clock passa dal giorno 19 al giorno 20."),
    ("00:02:00,000", "Va bene, ci fermiamo qui."),
]


def json_whisper(cartella: Path) -> Path:
    dati = {"transcription": [{"timestamps": {"from": t, "to": t}, "text": " " + s}
                              for t, s in SEGMENTI]}
    p = cartella / "trascrizione.json"
    p.write_text(json.dumps(dati), encoding="utf-8")
    return p


class TestTrascrivi(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.audio = self.dir / "serata.flac"
        self.audio.write_bytes(b"non e' audio")

    def tearDown(self):
        self._tmp.cleanup()

    def test_senza_consenso_non_parte(self):
        rc = ts.main(["trascrivi", str(self.audio), "--out", str(self.dir / "o")])
        self.assertEqual(rc, 2)
        self.assertFalse((self.dir / "o").exists())

    def test_non_scrive_dentro_il_repo(self):
        dentro = ts.REPO / "campaign" / "sessions" / "prova-trascrizione"
        rc = ts.main(["trascrivi", str(self.audio), "--consenso", "--out", str(dentro)])
        self.assertEqual(rc, 2)
        self.assertFalse(dentro.exists())
        rc = ts.main(["bozza", str(json_whisper(self.dir)), "--out", str(dentro)])
        self.assertEqual(rc, 2)
        self.assertFalse(dentro.exists())

    def test_senza_whisper_esce_pulito(self):
        out = self.dir / "o"
        with mock.patch.object(ts, "trova_whisper", return_value=None):
            rc = ts.main(["trascrivi", str(self.audio), "--consenso", "--out", str(out)])
        self.assertEqual(rc, ts.ESCE_SENZA_STRUMENTI)
        self.assertFalse(out.exists())  # niente file a meta'


class TestBozza(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.bozza = ts.scrivi_bozza(json_whisper(self.dir), self.dir, "2026-11-20",
                                     NOMI).read_text(encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_porta_il_segno(self):
        self.assertTrue(self.bozza.startswith(MARCATORE))
        self.assertTrue(e_bozza(self.bozza))

    def test_sezioni_pubbliche_vuote(self):
        pubblico = session_recap.strip_private(self.bozza)
        for frase in ("monete", "Gaurush", "punti esperienza", "ci fermiamo"):
            self.assertNotIn(frase, pubblico)
        self.assertIn("## Summary\n\n[da scrivere: DM]", pubblico)

    def test_campo_capito_male_vuoto_e_privato(self):
        privato = self.bozza.split("## DM notes", 1)[1]
        self.assertIn("### Cosa hanno capito male", privato)
        sezione = privato.split("### Cosa hanno capito male", 1)[1].split("###", 1)[0]
        self.assertIn("\n- \n", sezione)

    def test_momenti_e_nomi(self):
        self.assertIn("- [ ] `00:01:10` Trovate 300 monete d'oro", self.bozza)
        self.assertIn("- [ ] `00:01:30` Ognuno guadagna 1200 punti esperienza.", self.bozza)
        self.assertIn("- [ ] `00:02:00` Va bene, ci fermiamo qui.", self.bozza)
        self.assertIn("- **Ghaurush**: `00:00:41`", self.bozza)   # «Gaurush»
        self.assertIn("- **Hammerfist**: `00:00:00`", self.bozza)  # «Hammerist»

    def test_nessun_nome_di_giocatore(self):
        self.assertIn("mai quelli dei giocatori", self.bozza)
        self.assertNotRegex(self.bozza, r"\*\*Players present\*\*: [A-Z][a-z]+ \(")


class TestSegnoRispettato(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        sessions = self.root / "campaign" / "sessions"
        sessions.mkdir(parents=True)
        bozza = ts.componi_bozza([(t[:8], s) for t, s in SEGMENTI], "2026-11-20", NOMI)
        (sessions / "2026-11-20_session-9.md").write_text(bozza, encoding="utf-8")
        self.sessions = sessions

    def tearDown(self):
        self._tmp.cleanup()

    def test_state_apply_rifiuta_la_bozza(self):
        rc = state_apply.run(self.root, "2026-11-20_session-9.md", check=True,
                             assume_yes=True, do_commit=False, no_guard=True)
        self.assertEqual(rc, 2)

    def test_session_recap_salta_la_bozza(self):
        salvato = session_recap.SESSIONS_DIR
        session_recap.SESSIONS_DIR = self.sessions
        try:
            self.assertEqual(session_recap.find_session_files(3), [])
        finally:
            session_recap.SESSIONS_DIR = salvato


class TestMisura(unittest.TestCase):
    def test_testi_uguali(self):
        m = ts.misura_testi("Thorik carica.", "Thorik carica.", NOMI)
        self.assertEqual(m["wer"], 0.0)
        self.assertEqual((m["nomi_attesi"], m["nomi_giusti"]), (1, 1))

    def test_nome_sbagliato_e_nome_inventato(self):
        m = ts.misura_testi("Thorik chiede: e Thorik risponde",
                            "Tordek chiede: e Thorik risponde", NOMI)
        self.assertEqual(m["errori"], 1)
        self.assertAlmostEqual(m["wer"], 0.2)
        self.assertEqual(m["nomi_attesi"], 2)
        self.assertEqual(m["nomi_giusti"], 1)
        self.assertEqual(m["nomi_inventati"], 1)

    def test_accenti_e_apostrofi_non_contano(self):
        m = ts.misura_testi("la voce di Zin'thara Vel'Ryn", "La voce di Zinthara VelRyn.", NOMI)
        self.assertEqual(m["wer"], 0.0)

    def test_misura_bozza(self):
        testo = "- [x] `00:01` a\n- [ ] `00:02` b\n- [X] `00:03` c\n- [ ] `00:04` d\n"
        self.assertEqual(ts.misura_bozza(testo),
                         {"righe_candidate": 4, "spuntate": 2, "quota_utile": 0.5})


class TestNomi(unittest.TestCase):
    def test_nomi_da_state_yaml(self):
        nomi = ts.nomi_della_campagna()
        if not nomi:
            self.skipTest("pyyaml assente")
        for atteso in ("Thorik", "Ghaurush", "Cenerevento", "Re Thorek Hammerfist"):
            self.assertIn(atteso, nomi)

    def test_prompt_resta_corto(self):
        self.assertLessEqual(len(ts.prompt_dei_nomi(["Nome%d" % i for i in range(500)])), 600)


if __name__ == "__main__":
    unittest.main()
