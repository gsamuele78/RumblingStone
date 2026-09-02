"""`validate_prosa.py`: i calchi, i tic a densità, e i registri da non confondere.

Il test che conta di più è `TestRegistri`. La prima passata produsse **256
rilievi** perché segnalava il progressivo e il possessivo *ovunque*: ma «sta
piovendo» è italiano corretto, e «la sua mano» in terza persona può servire a
disambiguare. Sono calchi **nel read-aloud**, cioè nella prosa che si legge ad
alta voce al tavolo — che è il caso di cui parla `italiano-nativo.md` §1. Con lo
split: 110.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from validate_prosa import (  # noqa: E402
    ANTITESI, controlla, coppie_glossario, e_per_i_giocatori,
)


def _f(s: str, nome: str = "prova.md") -> list[str]:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / nome
        p.write_text(s, encoding="utf-8")
        return controlla(p)


def _read_aloud(*righe: str) -> str:
    return "\n".join(f"> *{r}*" for r in righe)


class TestCalchiSempre(unittest.TestCase):
    """Forme senza nessun uso italiano legittimo: valgono ovunque."""

    def test_realizzare_per_to_realize(self):
        self.assertTrue(_f("Il DM realizza che i PG hanno capito."))

    def test_realizzare_un_progetto_e_italiano(self):
        # Il falso positivo che spegnerebbe il validatore in una settimana.
        self.assertEqual(_f("La contrada realizza il drappo in tre giorni."), [])

    def test_assumere_per_to_assume(self):
        self.assertTrue(_f("Assumi che la porta sia chiusa."))

    def test_eventualmente(self):
        self.assertTrue(_f("Il muro eventualmente cede."))

    def test_nominalizzazione(self):
        self.assertTrue(_f("Provi la sensazione di cadere."))


class TestRegistri(unittest.TestCase):
    """Il progressivo e il possessivo dipendono dal registro: read-aloud sì, prosa no."""

    def test_il_progressivo_in_una_nota_di_regia_non_e_un_calco(self):
        self.assertEqual(_f("Il rituale sta procedendo: il DM annota il round."), [])

    def test_il_progressivo_nel_read_aloud_lo_e(self):
        r = _f(_read_aloud("Stai camminando nel buio."))
        self.assertTrue(any("progressivo" in x for x in r), r)

    def test_il_possessivo_in_prosa_dm_non_e_un_calco(self):
        self.assertEqual(_f("Terros alza la sua mano destra, non la sinistra."), [])

    def test_il_possessivo_nel_read_aloud_lo_e(self):
        r = _f(_read_aloud("La tua mano trema sul pomo della spada."))
        self.assertTrue(any("possessivo" in x for x in r), r)


class TestTicADensita(unittest.TestCase):
    """Non regex ma conteggi: la soglia È il rilievo."""

    def test_una_antitesi_e_uno_strumento(self):
        self.assertEqual(_f(_read_aloud("Non c'è collera: c'è peso.")), [])

    def test_due_antitesi_sono_un_telaio(self):
        r = _f(_read_aloud("Non c'è collera: c'è peso.", "Non è un attacco: è il piano."))
        self.assertTrue(any("antitesi" in x for x in r), r)

    def test_le_quattro_forme_della_norma_si_riconoscono_tutte(self):
        # §9.1 di italiano-nativo.md le elenca: copula, verbo, sostantivo, trattone.
        for e in ("Non c'è collera: c'è PESO.", "Non è un attacco: è il piano.",
                  "Non ruba niente: cataloga.", "Non un burrone — niente."):
            with self.subTest(esempio=e):
                self.assertTrue(ANTITESI.search(e), e)

    def test_una_negazione_normale_non_e_unantitesi(self):
        self.assertIsNone(ANTITESI.search("Il muro non cede. Poi cede."))

    def test_una_maiuscola_di_portento_e_un_effetto(self):
        self.assertEqual(_f(_read_aloud("Senti il PESO nello sterno.")), [])

    def test_due_maiuscole_non_funzionano_piu(self):
        r = _f(_read_aloud("Senti il PESO. Poi il TUMP."))
        self.assertTrue(any("maiuscolo" in x for x in r), r)

    def test_le_sigle_del_repo_non_sono_enfasi(self):
        self.assertEqual(_f(_read_aloud("Prova con CD 22 contro la CA e il TS del PNG.")), [])


class TestCosaSiSalta(unittest.TestCase):

    def test_le_tabelle_non_sono_prosa(self):
        self.assertEqual(_f("| Nome | Nota |\n|---|---|\n| x | assumi che sia così |"), [])

    def test_i_blocchi_di_codice_si_saltano(self):
        self.assertEqual(_f("Testo.\n\n```\nassumi che x == 1\n```\n"), [])

    def test_un_file_senza_read_aloud_prende_solo_i_calchi_sempre(self):
        self.assertEqual(_f("Il rituale sta procedendo e la sua mano si alza."), [])


class TestFilePerIGiocatori(unittest.TestCase):
    """Un hint o un teaser è prosa da leggere per intero, non solo nei box.

    Il buco che questa classe chiude: su `02-HINT-THORIK.md` i controlli sui tic
    coprivano **29 parole su 353** — l'8% — perché guardavano solo dentro
    `> *…*`. I file che il tavolo aveva segnalato tornavano puliti.
    """

    def test_riconosce_i_file_dei_giocatori(self):
        for n in ("02-HINT-THORIK.md", "06-TEASER-GIOCATORI.md", "05-ECHI-HELLA.md",
                  "handout-lettera.md"):
            self.assertTrue(e_per_i_giocatori(Path(n)), n)

    def test_non_scambia_un_file_del_dm_per_uno_dei_giocatori(self):
        for n in ("01-REGIA-SESSIONE.md", "07-GUIDA-DM.md", "ARC07-CASSETTA-DEL-DM.md",
                  "PALIO-STATBLOCCHI.md"):
            self.assertFalse(e_per_i_giocatori(Path(n)), n)

    def test_in_un_file_dei_giocatori_conta_tutta_la_prosa(self):
        testo = "# Hint\n\nSenti il PESO. Poi senti il TUMP.\n"
        self.assertTrue(any("maiuscolo" in x for x in _f(testo, "02-HINT-X.md")))

    def test_nello_stesso_testo_fuori_da_un_file_giocatori_non_conta(self):
        testo = "# Nota\n\nSenti il PESO. Poi senti il TUMP.\n"
        self.assertEqual(_f(testo, "note-dm.md"), [])

    def test_i_titoli_non_sono_prosa_letta(self):
        self.assertEqual(_f("# IL TEMPIO DELLA FORGIA ETERNA\n\nTesto normale.\n",
                            "06-TEASER-X.md"), [])


class TestConvenzioniDelRepo(unittest.TestCase):
    """Ciò che SEMBRA enfasi e non lo è: un validatore che punisce la convenzione
    del repo viene spento, e allora non trova più nemmeno i rilievi veri."""

    def test_letichetta_di_battuta_non_e_una_maiuscola_di_portento(self):
        # `**NOME:**` è il formato che editorial-standards.md §2 IMPONE.
        testo = ("# Hint\n\n> **AEGIS FANG**, con quel tono: *«Vecchia storia.»*\n"
                 "> **LA CORONA**, calore sulla fronte: *«Adesso.»*\n")
        self.assertEqual(_f(testo, "02-HINT-X.md"), [])

    def test_anche_coi_due_punti_dentro_il_grassetto(self):
        testo = "# Hint\n\n> **I BRACIERI:** *«Incudine e Martello.»*\n"
        self.assertEqual(_f(testo, "02-HINT-X.md"), [])

    def test_il_cappello_del_dm_non_e_prosa_di_gioco(self):
        # Sta su piu' righe di blockquote: va tolto il blocco intero.
        testo = ("# Hint\n\n> *Per il giocatore di X. Leggi in privato.\n"
                 "> Sono cose che il TUO personaggio sente, e che gli ALTRI no.*\n\n"
                 "Testo di gioco normale.\n")
        self.assertEqual(_f(testo, "02-HINT-X.md"), [])


class TestGlossario(unittest.TestCase):
    """La forma inglese di un nome che il canone vuole tradotto.

    È il rilievo del tavolo — «prosa inglese» — nella sua forma più letterale.
    """

    def test_il_glossario_del_repo_si_legge(self):
        coppie = coppie_glossario()
        self.assertGreaterEqual(len(coppie), 20, "il glossario non viene letto")
        canonici = {it for it, _ in coppie}
        self.assertIn("Incudine del Mondo", canonici)

    def test_le_voci_dnt_non_diventano_rilievi(self):
        # Aegis Fang e Skullcrusher sono inglesi PER SCELTA: segnalarli sarebbe
        # il falso positivo che spegne il validatore.
        inglesi = {en for _, en in coppie_glossario()}
        for dnt in ("Aegis Fang", "Skullcrusher the Black"):
            self.assertNotIn(dnt, inglesi, dnt)

    def test_le_intestazioni_di_sezione_non_sono_coppie(self):
        for it, en in coppie_glossario():
            self.assertFalse(it.startswith("**"), f"{it} è un'intestazione, non un nome")
            self.assertNotIn(en.lower(), ("italiano", "inglese"), en)

    def test_una_forma_inglese_nel_contenuto_e_un_rilievo(self):
        r = _f("I PG raggiungono l'Anvil of the World e si fermano.")
        self.assertTrue(any("Anvil of the World" in x for x in r), r)

    def test_il_nome_canonico_non_e_un_rilievo(self):
        self.assertEqual(_f("I PG raggiungono l'Incudine del Mondo e si fermano."), [])


if __name__ == "__main__":
    unittest.main()
