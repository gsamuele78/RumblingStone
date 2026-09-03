"""Il generatore contro i mostri veri.

Il criterio d'accettazione del piano è uno solo e non è negoziabile: *il
risultato supera il collaudo sul GS — e se non passa, il generatore è sbagliato*.

La prima versione non passava: un «GS 7» con 38 punti ferita e CA 12, cioè meno
della metà di quello che ha un mostro di GS 7 nel manuale. Il collaudo l'ha detto
al primo giro (−55%), ed è esattamente il lavoro per cui esiste. Queste sono le
ancore che hanno chiuso quel difetto: mostri del SRD 3.5, con i loro numeri.

Le bande sono larghe di proposito. Un mostro di GS 7 nel SRD sta fra i 76 punti
ferita della Chimera e i 102 dell'Ettin: pretendere che il generatore centri un
numero solo vorrebbe dire pretendere che esista un solo mostro di GS 7.
"""
from __future__ import annotations

import io
import random
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import genera_creatura as G  # noqa: E402
from dmcore import tabelle as T  # noqa: E402

#: Mostri del SRD 3.5, con i numeri del manuale. Sono le ancore: se il
#: generatore si allontana da questi, si è allontanato dal gioco.
#: (nome, GS, tipo, taglia, pf, CA)
ANCORE_SRD = [
    ("Ogre",                   3, "giant",         "large",  29, 16),
    ("Troll",                  5, "giant",         "large",  63, 16),
    ("Ettin",                  6, "giant",         "large",  65, 18),
    ("Chimera",                7, "magical beast", "large",  76, 19),
    ("Gigante delle Colline",  7, "giant",         "large", 102, 20),
    ("Osyluth (diavolo osso)", 9, "outsider",      "large",  95, 25),
]


class ControlDelGS(unittest.TestCase):
    """La creatura generata sta nella fascia dei mostri veri di quel GS."""

    def test_ogni_ancora_del_srd(self):
        for nome, gs, tipo, taglia, pf, ca in ANCORE_SRD:
            with self.subTest(mostro=nome, gs=gs):
                sb, _ = G.genera(gs, tipo=tipo, taglia=taglia, ruolo="bruto",
                                 rng=random.Random(0))
                scarto = abs(int(sb.pf) - pf) / pf
                self.assertLess(scarto, 0.60,
                                f"{nome}: {sb.pf} pf contro i {pf} del manuale")
                self.assertLessEqual(abs(int(sb.ca) - ca), 6,
                                     f"{nome}: CA {sb.ca} contro {ca}")

    def test_nessun_ruolo_e_indifeso(self):
        """Il difetto della prima versione: −55% sui pf, per ogni ruolo."""
        for gs in (1, 3, 5, 7, 10, 13, 16, 20):
            for ruolo in G.RUOLI:
                with self.subTest(gs=gs, ruolo=ruolo):
                    sb, _ = G.genera(gs, ruolo=ruolo, rng=random.Random(0))
                    bersaglio, _ = G.bersaglio_di(gs, ruolo, piu_cattivi=False)
                    scarto = (int(sb.pf) - bersaglio["pf"]) / bersaglio["pf"]
                    self.assertGreater(scarto, -0.25,
                                       f"GS {gs} {ruolo}: {sb.pf} pf contro un "
                                       f"bersaglio di {bersaglio['pf']}")
                    self.assertLess(scarto, 0.25)

    def test_i_punteggi_restano_nella_banda(self):
        """Cos 24 e Des 28 a GS 7 erano il sintomo: numeri giusti, mostro sbagliato."""
        for gs in range(1, 21):
            sb, _ = G.genera(gs, ruolo="bruto", rng=random.Random(0))
            for pezzo in re.findall(r"[A-Z][a-z]{2} (\d+)", sb.attributi):
                with self.subTest(gs=gs, punteggio=pezzo):
                    self.assertLessEqual(int(pezzo), 10 + 2 * G.MOD_MAX)

    def test_il_conto_e_sempre_scritto(self):
        """Un numero senza il suo conto è un numero di cui non ci si fida."""
        sb, conto = G.genera(7, ruolo="bruto", rng=random.Random(0))
        self.assertGreaterEqual(len(conto.righe), 5)
        self.assertTrue(any("bersaglio" in r for r in conto.righe))
        self.assertTrue(any("pf" in r for r in conto.righe))
        self.assertIn("generato-SRD-3.5", sb.fonte)


class VariantePiuCattiva(unittest.TestCase):
    """`--piu-cattivi` = template Advanced di PF1e, senza alzare il GS."""

    def test_alza_tutto_quello_che_advanced_alza(self):
        mite, _ = G.genera(7, ruolo="bruto", rng=random.Random(0))
        cattivo, conto = G.genera(7, ruolo="bruto", piu_cattivi=True,
                                  rng=random.Random(0))
        self.assertGreater(int(cattivo.pf), int(mite.pf))
        self.assertGreater(int(cattivo.ca), int(mite.ca))
        self.assertNotEqual(cattivo.attacchi, mite.attacchi)
        self.assertNotEqual(cattivo.ts, mite.ts)

    def test_dichiara_di_valere_un_gs_in_piu(self):
        """La cosa che rende onesta la variante: lo dice la creatura stessa."""
        sb, conto = G.genera(7, ruolo="bruto", piu_cattivi=True,
                             rng=random.Random(0))
        self.assertEqual(sb.gs, "7", "il GS venduto resta quello chiesto")
        self.assertTrue(any("GS 8" in v for v in sb.voci),
                        "deve dire che in realtà picchia come un GS 8")
        self.assertTrue(conto.rincari, "i rincari vanno elencati")
        self.assertIn("piu-cattivi", sb.fonte)

    def test_le_caratteristiche_salgono_di_quattro(self):
        mite, _ = G.genera(9, ruolo="comandante", rng=random.Random(0))
        cattivo, _ = G.genera(9, ruolo="comandante", piu_cattivi=True,
                              rng=random.Random(0))
        prima = [int(n) for n in re.findall(r"\d+", mite.attributi)]
        dopo = [int(n) for n in re.findall(r"\d+", cattivo.attributi)]
        self.assertEqual(dopo, [n + G.ADVANCED["caratteristiche"] for n in prima])


class Incantatori(unittest.TestCase):
    """La parte che il DM ha chiesto per nome."""

    def test_gli_slot_vengono_dalla_tabella_di_classe(self):
        sb, _ = G.genera(9, ruolo="artigliere", classe=("mago", 9),
                         rng=random.Random(0))
        atteso = "/".join(str(n) for n in T.MAGO[9])
        self.assertTrue(any(atteso in v for v in sb.voci),
                        f"gli slot devono essere quelli del SRD: {atteso}")

    def test_la_cd_massima_sta_sulla_riga_del_gs(self):
        """Il controllo che chiude il cerchio: la CD di un incantatore di GS n
        deve stare sulla CD primaria della riga di GS n."""
        for gs, livelli in ((5, 5), (9, 9), (13, 13), (16, 16)):
            for classe in ("mago", "chierico", "stregone"):
                with self.subTest(gs=gs, classe=classe):
                    sb, _ = G.genera(gs, ruolo="controllore",
                                     classe=(classe, livelli), rng=random.Random(0))
                    cd = int(re.search(r"CD (\d+)\)", " ".join(sb.voci)).group(1))
                    atteso = T.riga_gs(gs)[0]["cd"]
                    self.assertLessEqual(abs(cd - atteso), 3,
                                         f"CD {cd} contro una riga da {atteso}")

    def test_lo_stregone_porta_gli_incantesimi_conosciuti(self):
        sb, _ = G.genera(11, ruolo="artigliere", classe=("stregone", 11),
                         rng=random.Random(0))
        self.assertTrue(any("conosciuti" in v for v in sb.voci))

    def test_il_chierico_ricorda_i_domini(self):
        sb, _ = G.genera(7, ruolo="comandante", classe=("chierico", 7),
                         rng=random.Random(0))
        self.assertTrue(any("domini" in v for v in sb.voci))

    def test_gli_incantesimi_sono_scelti_dalla_lista_del_ruolo(self):
        """Il criterio del lotto D: nessun incantesimo fuori lista di livello.

        Estrarre a sorte da tutto il SRD produce un incantatore che al tavolo non
        si sa giocare — un mago con «individuazione del veleno» preparato e
        niente per il round in cui i PG gli arrivano addosso.
        """
        for ruolo in ("controllore", "artigliere", "comandante"):
            for livelli in (5, 9, 13, 17):
                with self.subTest(ruolo=ruolo, livelli=livelli):
                    sb, _ = G.genera(livelli, ruolo=ruolo, classe=("mago", livelli),
                                     rng=random.Random(4))
                    riga = next((v for v in sb.voci if v.startswith("Preparati")), "")
                    self.assertTrue(riga, "un incantatore senza incantesimi scelti")
                    lista = G.INCANTESIMI[ruolo]
                    for pezzo in riga.removeprefix("Preparati — ").split(" · "):
                        liv = int(pezzo.split("°")[0])
                        for nome in pezzo.split(": ", 1)[1].split(", "):
                            self.assertIn(nome, lista[liv],
                                          f"{nome} non è nella lista di {ruolo} "
                                          f"al {liv}° livello")

    def test_nessun_incantesimo_sopra_il_livello_lanciabile(self):
        sb, _ = G.genera(5, ruolo="artigliere", classe=("mago", 5),
                         rng=random.Random(1))
        riga = next(v for v in sb.voci if v.startswith("Preparati"))
        massimo = max(int(p.split("°")[0]) for p in
                      riga.removeprefix("Preparati — ").split(" · "))
        self.assertEqual(massimo, T.livello_massimo(T.MAGO, 5))

    def test_ogni_ruolo_incantatore_ha_la_sua_lista(self):
        for ruolo in G.RUOLI:
            with self.subTest(ruolo=ruolo):
                self.assertTrue(ruolo in G.INCANTESIMI or ruolo in G.LISTA_DI_RIPIEGO,
                                "un ruolo senza lista né ripiego resta senza "
                                "incantesimi, e un vuoto è peggio di una lista "
                                "sbagliata di ruolo")

    def test_una_classe_senza_lista_non_prende_quella_di_un_altra(self):
        """Il difetto trovato costruendo il Bestiario, e il piu' insidioso di
        tutti: un druido usciva con *armatura magica* e *dito della morte* (mago)
        o con *benedizione* e *santuario* (chierico). Il blocco sembrava
        completo, e al tavolo il druido annunciava un incantesimo che non ha.

        Meglio un vuoto dichiarato che una lista di un'altra classe."""
        for classe in ("druido", "adepto"):
            for ruolo in ("controllore", "artigliere", "comandante", "bruto"):
                with self.subTest(classe=classe, ruolo=ruolo):
                    sb, _ = G.genera(12, ruolo=ruolo, classe=(classe, 12),
                                     rng=random.Random(0))
                    self.assertFalse(any(v.startswith("Preparati") for v in sb.voci),
                                     f"{classe} non deve ricevere la lista di {ruolo}")
                    self.assertTrue(any("da scegliere a mano" in v for v in sb.voci),
                                    "il vuoto va dichiarato, non lasciato in silenzio")

    def test_le_classi_coperte_gli_incantesimi_li_prendono(self):
        """Il rifiuto vale per le classi scoperte, non per tutte."""
        for classe in ("mago", "stregone", "chierico"):
            with self.subTest(classe=classe):
                sb, _ = G.genera(9, ruolo="controllore", classe=(classe, 9),
                                 rng=random.Random(0))
                self.assertTrue(any(v.startswith("Preparati") for v in sb.voci))

    def test_le_liste_coprono_tutti_i_livelli(self):
        for ruolo, lista in G.INCANTESIMI.items():
            with self.subTest(ruolo=ruolo):
                self.assertEqual(sorted(lista), list(range(0, 10)))
                for liv, voci in lista.items():
                    self.assertGreaterEqual(len(voci), 2, f"{ruolo} {liv}°")

    def test_gli_aumenti_ogni_quattro_livelli(self):
        """Senza, un mago di 9° usciva con Intelligenza 15."""
        sb, _ = G.genera(9, ruolo="artigliere", classe=("mago", 9),
                         rng=random.Random(0))
        intelligenza = int(re.search(r"Int (\d+)", sb.attributi).group(1))
        self.assertEqual(intelligenza, T.ELITE[0] + 9 // 4)


class IlConfine(unittest.TestCase):
    """ADR-0033: lo strumento propone, nel canone scrive il DM."""

    def test_si_rifiuta_di_scrivere_nel_bestiario(self):
        for dove in ("Bestiario", "Bestiario/mostri", "Bestiario/villain/x"):
            with self.subTest(cartella=dove):
                with self.assertRaises(SystemExit) as e:
                    G._rifiuta_bestiario(ROOT / dove)
                self.assertIn("Bestiario", str(e.exception))

    def test_una_cartella_di_lavoro_va_bene(self):
        with tempfile.TemporaryDirectory() as d:
            G._rifiuta_bestiario(Path(d))   # non solleva

    def test_scrive_dove_gli_si_dice(self):
        with tempfile.TemporaryDirectory() as d:
            with redirect_stdout(io.StringIO()):
                G.main(["--gs", "5", "--ruolo", "bruto", "--in", d, "--seed", "1"])
            prodotti = list(Path(d).glob("*.md"))
            self.assertEqual(len(prodotti), 1)
            self.assertIn("```statblocco", prodotti[0].read_text(encoding="utf-8"))


class LaRigaDiComando(unittest.TestCase):
    def test_niente_abbreviazioni(self):
        """Nel lotto H `--apply` passava come abbreviazione di `--apply-ts`.
        `--piu-cattivi` non deve poter essere invocato per sbaglio."""
        p = G.costruisci_parser()
        with self.assertRaises(SystemExit):
            p.parse_args(["--gs", "5", "--piu"])

    def test_il_gs_sta_fra_uno_e_venti(self):
        with self.assertRaises(SystemExit):
            G.main(["--gs", "0"])
        with self.assertRaises(SystemExit):
            G.main(["--gs", "21"])

    def test_lo_stesso_seed_da_la_stessa_creatura(self):
        a, _ = G.genera(7, ruolo="bruto", rng=random.Random(99))
        b, _ = G.genera(7, ruolo="bruto", rng=random.Random(99))
        self.assertEqual(a, b)

    def test_il_json_e_leggibile(self):
        import json
        f = io.StringIO()
        with redirect_stdout(f):
            G.main(["--gs", "7", "--json", "--quanti", "2", "--seed", "3"])
        dati = json.loads(f.getvalue())
        self.assertEqual(len(dati), 2)
        self.assertIn("blocco", dati[0])
        self.assertIn("conto", dati[0])

    def test_i_tipi_e_le_classi_ignote_si_rifiutano(self):
        import argparse
        with self.assertRaises(argparse.ArgumentTypeError):
            G._tipo("draghetto")
        with self.assertRaises(argparse.ArgumentTypeError):
            G._classe("negromante:5")
        with self.assertRaises(argparse.ArgumentTypeError):
            G._classe("mago")


class IlCarattere(unittest.TestCase):
    """Lotto E del piano: senza, escono mostri intercambiabili."""

    def test_ogni_ruolo_ha_le_sue_voci(self):
        for ruolo in G.RUOLI:
            with self.subTest(ruolo=ruolo):
                self.assertIn(ruolo, G.CARATTERE)
                self.assertGreaterEqual(len(G.CARATTERE[ruolo]), 3)
                for talento, tattica, debolezza in G.CARATTERE[ruolo]:
                    self.assertTrue(talento and tattica and debolezza)

    def test_la_creatura_esce_con_una_cosa_sua(self):
        sb, _ = G.genera(7, ruolo="bruto", rng=random.Random(0))
        self.assertTrue(sb.tattica, "senza tattica è un mucchio di numeri")
        self.assertTrue(any("Debolezza" in v for v in sb.voci),
                        "senza debolezza i PG non hanno niente da trovare")

    def test_due_creature_dello_stesso_ruolo_non_sono_identiche(self):
        visti = {G.genera(7, ruolo="bruto", rng=random.Random(s))[0].tattica
                 for s in range(20)}
        self.assertGreater(len(visti), 1)


if __name__ == "__main__":
    unittest.main()
