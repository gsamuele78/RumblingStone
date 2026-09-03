"""`validate_prosa --prima-dopo`: la riscrittura è migliorata o no?

Scritto **prima** dell'implementazione, e il caso di prova non è inventato: è
`05-ECHI-HELLA.md`, riscritto il 2026-09-02 e giudicato migliore dal DM. Tre
versioni in git, un giudizio umano su quale sia la buona. È l'unico metro vero
che questo repo abbia per la qualità della prosa.

## Perché una soglia assoluta non funziona, e un confronto sì

Tutte le misure assolute provate su questo corpus hanno fallito, e vale la pena
che restino scritte perché non tornino:

- **burstiness** (varianza della lunghezza delle frasi, la proposta più citata
  in letteratura): sulla riscrittura approvata **peggiora** — CV 0.55 → 0.47 —
  perché la riscrittura ha tolto i frammenti brevi, e togliere frammenti riduce
  la varianza. La metrica premia esattamente il tic che §9 vieta;
- **densità di frasi corte** come soglia di repo: il file peggiore (75%) è fatto
  di grida (*«PORTATORE MALEDETTO!»*) e note telegrafiche di regia (*«Treant lo
  lancia»*), non di frammenti narrativi;
- **aperture ripetute**: tre occorrenze in tutto il corpus. Troppo rare.

Le stesse misure **dentro un solo testo, fra due versioni**, non hanno il
problema: grida e note di regia ci sono prima e dopo, quindi si annullano. Quello
che resta è ciò che la riscrittura ha cambiato.
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import validate_prosa as P  # noqa: E402

#: Le tre versioni dell'eco di Hella, dalla più vecchia alla riscrittura
#: approvata dal DM il 2026-09-02.
ECHI = "07_il Portale Della Forgia Eterna/homebrew/sessione-terros/05-ECHI-HELLA.md"
ORIGINALE = "e7ed6b8"
INTERMEDIA = "f14f1b8"
APPROVATA = "67a6d21"


def _versione(sha: str) -> str | None:
    fuori = subprocess.run(["git", "show", f"{sha}:{ECHI}"],
                           cwd=REPO, capture_output=True, text=True)
    return fuori.stdout if fuori.returncode == 0 else None


class ImisuriChiTracciaLaQualita(unittest.TestCase):
    """Il criterio: la versione approvata deve misurare meglio della sua."""

    @classmethod
    def setUpClass(cls):
        cls.prima = _versione(INTERMEDIA)
        cls.dopo = _versione(APPROVATA)
        if cls.prima is None or cls.dopo is None:
            raise unittest.SkipTest("storia git non disponibile in questo checkout")

    def test_i_frammenti_brevi_calano(self):
        """Il tic che la riscrittura ha davvero tolto: *«Sono tuoi.»*,
        *«Non sai se lui ha sentito.»*"""
        self.assertLess(P.conta_tic(self.dopo)["frammenti"],
                        P.conta_tic(self.prima)["frammenti"])

    def test_le_aperture_ripetute_calano(self):
        """*«Nessuno va spiegato. Nessuno va interpretato ad alta voce.»*"""
        self.assertLessEqual(P.conta_tic(self.dopo)["aperture_ripetute"],
                             P.conta_tic(self.prima)["aperture_ripetute"])

    def test_il_verdetto_complessivo_e_migliorata(self):
        verdetto = P.confronta(self.prima, self.dopo)
        self.assertGreater(verdetto["migliorati"], verdetto["peggiorati"],
                           f"la riscrittura approvata dal DM deve misurare "
                           f"meglio: {verdetto}")

    def test_il_confronto_e_antisimmetrico(self):
        """Invertendo le due versioni il verdetto si capovolge. Senza questo,
        un confronto che dice sempre «migliorata» passerebbe il test sopra."""
        dritto = P.confronta(self.prima, self.dopo)
        rovescio = P.confronta(self.dopo, self.prima)
        self.assertEqual(dritto["migliorati"], rovescio["peggiorati"])
        self.assertEqual(dritto["peggiorati"], rovescio["migliorati"])

    def test_un_testo_con_se_stesso_non_cambia(self):
        v = P.confronta(self.dopo, self.dopo)
        self.assertEqual((v["migliorati"], v["peggiorati"]), (0, 0))


class LaBurstinessNonEUnObiettivo(unittest.TestCase):
    """⚠️ Questo test esiste per impedire una regressione di *progetto*.

    La varianza della lunghezza delle frasi è la misura più citata in
    letteratura e sembra la scelta ovvia. Su questo corpus va nella direzione
    sbagliata, e la prova è la riscrittura che il DM ha approvato. Se qualcuno
    fra sei mesi la propone di nuovo, questo test è il controesempio già
    scritto.
    """

    @classmethod
    def setUpClass(cls):
        cls.prima = _versione(INTERMEDIA)
        cls.dopo = _versione(APPROVATA)
        if cls.prima is None or cls.dopo is None:
            raise unittest.SkipTest("storia git non disponibile in questo checkout")

    def test_la_riscrittura_approvata_ha_burstiness_PEGGIORE(self):
        self.assertLess(P.burstiness(self.dopo), P.burstiness(self.prima),
                        "se questo test cade, la burstiness ha smesso di "
                        "contraddire il giudizio del tavolo e la decisione di "
                        "non usarla come soglia va riesaminata")

    def test_non_e_fra_i_tic_contati(self):
        self.assertNotIn("burstiness", P.conta_tic(self.dopo),
                         "misurabile sì, obiettivo no")


class ContaTic(unittest.TestCase):
    def test_i_frammenti_sono_le_frasi_corte(self):
        self.assertEqual(P.conta_tic("Uno due tre quattro cinque sei sette otto. "
                                     "Ed ecco.")["frammenti"], 1)

    def test_le_frasi_di_una_parola_sola_NON_contano(self):
        """⚠️ Scritto dopo aver misurato, e contro la mia prima versione.

        Il test originale usava «Corta.» e pretendeva che contasse: una frase di
        una parola è il frammento per eccellenza. Misurando il corpus, le frasi
        di una parola nei read-aloud sono **279 e quasi tutte artefatti**: «È…»,
        «Solo…», «Ma…», cioè la prima metà di una frase spezzata dai puntini di
        sospensione. Contarle vorrebbe dire inventare 279 tic che non ci sono.

        Il caso vero — la riscrittura di Hella — toglieva «Sono tuoi.» e «Non
        sai se lui ha sentito.», due e sei parole: il filtro non lo perde."""
        self.assertEqual(P.conta_tic("È... Solo... Ma...")["frammenti"], 0)
        self.assertEqual(P.conta_tic("Sono tuoi.")["frammenti"], 1)

    def test_le_aperture_ripetute_sono_consecutive(self):
        tre = "Nessuno va spiegato. Nessuno va detto. Nessuno va scritto."
        self.assertEqual(P.conta_tic(tre)["aperture_ripetute"], 2)
        sparse = "Nessuno va spiegato. Il sole scende. Nessuno va detto."
        self.assertEqual(P.conta_tic(sparse)["aperture_ripetute"], 0)

    def test_l_antitesi_e_contata(self):
        self.assertEqual(
            P.conta_tic("Non è collera: è peso.")["antitesi"], 1)

    def test_su_testo_vuoto_non_esplode(self):
        for vuoto in ("", "   ", "\n\n"):
            with self.subTest(testo=repr(vuoto)):
                self.assertEqual(P.conta_tic(vuoto)["frammenti"], 0)
                self.assertIsNone(P.burstiness(vuoto))


class LaRigaDiComando(unittest.TestCase):
    def test_prima_dopo_su_un_file_tracciato(self):
        if _versione(APPROVATA) is None:
            self.skipTest("storia git non disponibile")
        self.assertEqual(P.main(["--prima-dopo", "--rispetto-a", INTERMEDIA, ECHI]), 0)

    def test_un_file_non_tracciato_non_fa_esplodere(self):
        self.assertEqual(P.main(["--prima-dopo", "--rispetto-a", "HEAD",
                                 "file-che-non-esiste.md"]), 0)


if __name__ == "__main__":
    unittest.main()
