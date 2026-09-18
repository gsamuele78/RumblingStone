"""Il metro del mestiere, e le cinque volte che al primo giro diceva il falso.

Il DM il 2026-09-18: *«c'e' un modo di misurare che il nuovo stile a 9 pilastri
e le altre cose inserite sono presenti in quella parte, in che percentuale»*.

🔴 **La prima tabella invertiva la verita'.** Non per un bug di sintassi: per il
difetto di ADR-0053 — *un matcher largo traveste l'ignoranza*. Ogni classe di
test qui sotto fissa **una** di quelle cinque bugie, e la fissa **dal lato che
morde**: un rilevatore che tornasse largo torna rosso qui.

⚠️ Il sesto difetto non era nei rilevatori ma nei **bersagli**: misuravo 6 file
del Palio su 15 e 1 di ARC-08 su 23, e la tabella non lo diceva. Gli zeri
sembravano assenze di mestiere ed erano assenze di misura.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _mc():
    spec = importlib.util.spec_from_file_location(
        "misura_craft", ROOT / "scripts" / "misura_craft.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MC = _mc()
RX = {nome: rx for nome, rx, _ in MC.CONGEGNI}


def conta(congegno: str, testo: str) -> int:
    return len(RX[congegno].findall(testo))


class TestReadAloudNonEUnaNotaEditoriale(unittest.TestCase):
    """🐛 `^>` prendeva QUALSIASI citazione. DEF-1 segnava 183 read-aloud e
    sono `> **Sistema: D&D 3.5 SRD**`; l'Abbazia ne segnava 11 ed erano tutti
    prosa vera. Il numero diceva il contrario del vero."""

    NOTA = "> **Sistema: D&D 3.5 SRD** (al massimo Pathfinder 1e)\n"
    PROSA = "> *La mattina sulla soglia dell'osteria c'e' del sale grosso.*\n"

    def test_la_nota_editoriale_non_conta(self):
        self.assertEqual(conta("read-aloud narrativo", self.NOTA), 0)

    def test_la_prosa_in_corsivo_conta(self):
        """Il lato che morde: stringere non deve aver spento il rilevatore."""
        self.assertEqual(conta("read-aloud narrativo", self.PROSA), 1)

    def test_sul_documento_vero_il_banco_resta_intero(self):
        """L'Abbazia perde **zero** read-aloud passando al metro stretto: e'
        la prova che i suoi 11 erano tutti veri e i 183 di DEF-1 no."""
        testo, _, _ = MC.carica(MC.BERSAGLI["★ Abbazia (stand-alone)"])
        largo = len(__import__("re").findall(r"^>\s*[*_]*[A-ZÀ-Ù«\"]", testo,
                                            __import__("re").M))
        self.assertEqual(conta("read-aloud narrativo", testo), 11)
        self.assertEqual(largo, 11, "il banco e' il caso in cui i due metri "
                                    "coincidono: se diverge, la prova non vale piu'")


class TestLoSpotlightNonELaFormattazione(unittest.TestCase):
    """🐛 Pretendeva il **grassetto**. Il Palio nomina tutti e quattro i PG e
    non li scrive mai in grassetto: segnava 0. Misurava il markdown."""

    def test_il_PG_conta_anche_senza_grassetto(self):
        self.assertEqual(conta("spotlight per PG", "Tordek si fa avanti."), 1)

    def test_il_PG_in_grassetto_conta_ancora(self):
        self.assertEqual(conta("spotlight per PG", "**Hella** tace."), 1)


class TestEcoConosceIlPlurale(unittest.TestCase):
    """🐛 Il Palio ha un **file intero** chiamato `PALIO-CONSEGUENZE-ECHI.md`
    e segnava **zero echi**: il rilevatore non conosceva il plurale."""

    def test_echi_al_plurale_conta(self):
        self.assertGreaterEqual(conta("eco / conseguenze a distanza",
                                      "Echi (stile BG3) e echi RP"), 2)

    def test_il_palio_non_e_piu_a_zero_echi(self):
        testo, _, _ = MC.carica(MC.BERSAGLI["★ Palio di Channathgate"])
        self.assertGreater(conta("eco / conseguenze a distanza", testo), 0,
                           "il banco degli echi torna a dichiarare zero echi")


class TestIlDialogoHaDueConvenzioni(unittest.TestCase):
    """🐛 Il rilevatore pretendeva `Nome: «…»`: **zero in tutti i 12 bersagli**.
    Una forma inventata, che nessun documento del repo usa.

    ⚠️ E le virgolette dritte non sono automaticamente dialogo: nel Palio
    `"…"` da' **128 hit** e sono **titoli di canzoni**. Il discrimine e'
    >=3 parole **e** punteggiatura di frase."""

    def test_le_guillemette_contano(self):
        self.assertEqual(conta("battute di dialogo", "«Il Signore aspetta.»"), 1)

    def test_la_battuta_fra_virgolette_dritte_conta(self):
        self.assertEqual(
            conta("battute di dialogo", '"Ci pensate. Il banco resta qui."'), 1)

    def test_il_titolo_di_canzone_NON_conta(self):
        """Il lato che morde, ed e' quello che ha ucciso 106 falsi positivi."""
        for titolo in ('"L\'Aria dei Conti"', '"Il Lamento del Traghetto"',
                       '"Bastone-di-Serpente"', '"Disguise Self psionico"'):
            with self.subTest(titolo=titolo):
                self.assertEqual(conta("battute di dialogo", titolo), 0)

    def test_nessun_bersaglio_e_piu_a_zero_per_forma_inventata(self):
        """La Torre resta a zero — ma per un fatto, non per il metro: non ha
        **nessun** dialogo, ne' `«…»` ne' dritto. Gli altri devono averne."""
        vivi = 0
        for nome in MC.BERSAGLI:
            testo, _, _ = MC.carica(MC.BERSAGLI[nome])
            if conta("battute di dialogo", testo):
                vivi += 1
        self.assertGreaterEqual(vivi, 8, "il rilevatore e' tornato a non "
                                         "riconoscere nessuna convenzione")


class TestIlPilastroDichiarato(unittest.TestCase):
    """🔎 La risposta vera alla domanda del DM.

    La *fusion rule* dice «UN pilastro guida, al piu' due di supporto». I
    documenti che la applicano **la scrivono**: `(Casa di Davide lead)`,
    `(BG3 lead)`, `(Mercer support)`. Si conta quella marca."""

    def test_la_marca_del_pilastro_conta(self):
        self.assertEqual(
            conta("PILASTRO dichiarato (lead/support)",
                  "### 🌙 HELLA — la seconda vita alla prova (BG3 lead)"), 1)

    def test_il_support_tattico_NON_conta(self):
        """🔴 Il lato che morde: nel repo «support» e' quasi sempre un ruolo di
        combattimento. Senza il nome del pilastro dentro la parentesi, il
        rilevatore ripescherebbe «healing support» e direbbe una bugia."""
        for falso in ("un chierico da healing support", "ranged support",
                      "Kitor full support", "blaster e support"):
            with self.subTest(falso=falso):
                self.assertEqual(
                    conta("PILASTRO dichiarato (lead/support)", falso), 0)

    def test_solo_DEF_2_5_dichiarano_i_pilastri(self):
        """Il fatto misurato, e vale come non-regressione del canone: la marca
        esiste **solo** in DEF-2..DEF-5. Se un giorno comparisse altrove, e'
        perche' qualcuno ha portato lo stile — e questo test va aggiornato
        **di proposito**, non per caso."""
        con, senza = [], []
        for nome in MC.BERSAGLI:
            testo, _, _ = MC.carica(MC.BERSAGLI[nome])
            (con if conta("PILASTRO dichiarato (lead/support)", testo) else senza
             ).append(nome)
        self.assertEqual(sorted(con), ["DEF-2 Ritorno e affreschi",
                                       "DEF-3 Resurrezione Hella",
                                       "DEF-4 Viaggio 1.000 anni",
                                       "DEF-5 Ritorno Hammerfist"])
        self.assertIn("★ Abbazia (stand-alone)", senza)
        self.assertIn("DEF-1 Piano della Terra", senza)


class TestIBersagliNonSiCampionanoInSilenzio(unittest.TestCase):
    """🔴 Il difetto che non era in nessun rilevatore.

    Misuravo **6 file del Palio su 15**, **1 di ARC-08 su 23**, **4 del Torneo
    su 22** — e la tabella stampava zeri che sembravano assenze di mestiere.
    E' la stessa forma del censimento tarato sul campione."""

    def test_un_modello_che_non_pesca_niente_e_un_errore(self):
        """Il lato che morde: prima un percorso sbagliato spariva in silenzio."""
        with self.assertRaises(SystemExit):
            MC.espandi(["07_il Portale Della Forgia Eterna/QUESTO-NON-ESISTE-*.md"])

    def test_ogni_bersaglio_pesca_i_file_che_dice(self):
        atteso = {"★ Palio di Channathgate": 15, "ARC-09 Torneo di Dauth": 22,
                  "ARC-09 Torre di Zalkatar": 12, "ARC-09 Battaglia Finale": 16,
                  "ARC-08 Hammerfist": 13}
        for nome, n in atteso.items():
            with self.subTest(bersaglio=nome):
                self.assertEqual(len(MC.espandi(MC.BERSAGLI[nome])), n)

    def test_le_versioni_superate_restano_fuori(self):
        """Un `DEPRECATO` o una `ERRATA-` non dicono niente sul documento vivo,
        e ARC-08 ne ha **quattro** che gonfierebbero ogni conteggio."""
        presi = {f.name for f in MC.espandi(MC.BERSAGLI["ARC-08 Hammerfist"])}
        self.assertTrue(presi, "nessun file: il modello si e' rotto")
        for nome in presi:
            self.assertNotIn("DEPRECATO", nome)
            self.assertNotIn("ERRATA-", nome)


if __name__ == "__main__":
    unittest.main()
