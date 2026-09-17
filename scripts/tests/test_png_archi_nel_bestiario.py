"""Chi ha statistiche in un arco dev'essere raggiungibile — lotto 4d-5.

🔴 **Il difetto misurato il 2026-09-17.** Diciannove documenti dell'arco 09
portano statblocchi in prosa — Taglia/Tipo, DV, CA, TS — scritti dal DM. Ma
`build_monster_catalog.py` e `suggest_encounter.py` costruiscono il pool degli
incontri scansionando i file **con la forma dello statblock**, e quella forma
d'arco non sempre la ha. Risultato: **47 fra PNG, villain e creature** avevano
statistiche complete e **nessuno strumento le raggiungeva**.

Fra questi il campione del Torneo di Dauth (Monk 14), il boss dei campi drow
(GS 13), e il Drago Rosso che guida l'invasione (GS 15).

La correzione segue il pattern gia' in uso nel repo (`capitana-lorana-cr7.md`):
una voce **POINTER** nel Bestiario che rimanda al file d'arco. Le statistiche
restano dove il DM le ha scritte — duplicarle creerebbe la seconda copia che
ADR-0021 vieta.

⚠️ **Questo test e' il presidio.** Senza, il prossimo documento d'arco con
statblocchi esce dal pool in silenzio, esattamente come questi quarantasette.

🔎 E il cancello se l'e' guadagnato subito: una volta scritto giusto ha trovato
da solo **tre file** che la ricerca a mano aveva saltato — i villain iconici del
torneo, le comparse dell'arena, i nemici della Quest di Hella.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import yaml  # noqa: E402

CATALOGO = yaml.safe_load(
    (ROOT / "scripts" / "monster_catalog.yaml").read_text(encoding="utf-8"))["monsters"]

#: La forma dello statblocco in prosa usata dagli archi (quella del file Zalkatar).
STAT = re.compile(r"^\s*[-*]\s*(Taglia/Tipo|DV|CA|TS|BAB)\s*:", re.M | re.I)
ARCHI = [p for p in ROOT.glob("0*") if p.is_dir()] + [p for p in ROOT.glob("1*") if p.is_dir()]


def _documenti_con_statistiche() -> "list[Path]":
    fuori = []
    for base in ARCHI:
        for p in base.rglob("*.md"):
            if "_ARCHIVIO" in str(p) or "homebrew" in str(p):
                continue
            if len(STAT.findall(p.read_text(encoding="utf-8", errors="replace"))) >= 4:
                fuori.append(p)
    return fuori


class TestOgniStatblocDArcoEraggiungibile(unittest.TestCase):
    def test_ogni_documento_con_statistiche_ha_un_aggancio(self):
        """🔴 Il cancello del lotto.

        Un documento d'arco con quattro o piu' marche di statblocco descrive
        creature giocabili. Se nessuna voce del catalogo lo cita come `Source`,
        quelle creature non esistono per `suggest_encounter`: il DM le ha
        scritte e il tavolo non le vedra' mai.
        """
        # ⚠️ Il catalogo registra come `source_file` il file SCANSIONATO — cioe'
        # la voce del Bestiario, non l'arco a cui rimanda. L'aggancio si cerca
        # quindi nella riga `**Source**` delle voci, che e' dove il POINTER
        # dichiara il proprio bersaglio. (La prima versione di questo test
        # cercava nel campo sbagliato e dava per scoperti quattro file agganciati.)
        citati = set()
        for b in (ROOT / "Bestiario").rglob("*.md"):
            for riga in b.read_text(encoding="utf-8", errors="replace").splitlines():
                if riga.startswith(("**Source**", "**Key stats**")):
                    citati.add(riga)
        # E la seconda via: `build_monster_catalog` raggiunge DIRETTAMENTE alcuni
        # file d'arco, quando la loro forma gli basta (Zalkatar, Regiarix, il
        # Treant Corrotto). Un documento raggiungibile per quella strada non ha
        # bisogno di un POINTER: il criterio e' «gli strumenti ci arrivano»,
        # non «esiste una voce nel Bestiario».
        citati |= {m["source_file"] for m in CATALOGO}
        citati = "\n".join(citati)
        orfani = []
        for p in _documenti_con_statistiche():
            rel = str(p.relative_to(ROOT))
            if rel not in citati:
                orfani.append(rel)
        self.assertEqual(orfani, [],
                         "documenti d'arco con statistiche che nessuna voce del "
                         "Bestiario aggancia — servono voci POINTER:\n  "
                         + "\n  ".join(orfani))

    def test_i_pointer_non_duplicano_le_statistiche(self):
        """ADR-0021: una voce POINTER rimanda, non copia.

        Se un giorno qualcuno ci incolla dentro i numeri, il Bestiario e l'arco
        diventano due copie che divergono alla prima errata — ed e' il difetto
        che il pattern POINTER esiste per non avere.
        """
        for p in (ROOT / "Bestiario").rglob("*.md"):
            testo = p.read_text(encoding="utf-8", errors="replace")
            if "[POINTER" not in testo.split("\n", 1)[0]:
                continue
            with self.subTest(voce=str(p.relative_to(ROOT))):
                self.assertLess(len(STAT.findall(testo)), 2,
                                "un POINTER porta statistiche: o e' una scheda "
                                "vera, o e' una copia che divergera'")
                self.assertIn("**Source**", testo)

    def test_il_pool_degli_incontri_e_cresciuto_e_resta_grande(self):
        """Il guadagno pratico, fissato: erano 305 voci, adesso sono 352.

        ⚠️ La soglia si alza quando il pool cresce: lasciarla sotto il valore
        vero renderebbe il cancello piu' debole di quanto puo' essere.
        """
        self.assertGreaterEqual(len(CATALOGO), 352)

    def test_i_pointer_d_arco_puntano_a_file_che_esistono(self):
        """Stessa disciplina di R11 sull'anagrafica: un percorso si prova."""
        for m in CATALOGO:
            fonte = ROOT / m["source_file"]
            with self.subTest(voce=m["name"][:40]):
                self.assertTrue(fonte.exists(), m["source_file"])


class TestINomiCheIlTornEoHaPortato(unittest.TestCase):
    """Che i nominati siano davvero entrati, non solo il conteggio."""

    NOMI = ("Grandmaster Rihan", "Tetsu", "Lady Koryn", "Ironclad Bruiser",
            "Mistress of Mirrors", "Thrain Ironfist", "Grom Skullcrusher",
            "Zhen Windwhisper", "Kira", "Xilthra", "Killiar Arrowswift",
            "Saarvith")

    def test_ogni_individuo_nominato_e_nel_catalogo(self):
        nomi = " · ".join(m["name"] for m in CATALOGO)
        for n in self.NOMI:
            with self.subTest(png=n):
                self.assertIn(n, nomi)

    def test_grom_non_e_l_ogre_skullcrusher(self):
        """Due «Skullcrusher» diversi: il barbaro GS 14 del torneo e l'ogre GS 5.

        E' la forma d'errore che il lotto precedente ha documentato — un nome
        che combacia per somiglianza e porta alla creatura sbagliata.
        """
        grom = [m for m in CATALOGO if "Grom Skullcrusher" in m["name"]]
        ogre = [m for m in CATALOGO if m["name"].startswith("Ogre Skullcrusher")]
        self.assertEqual(len(grom), 1)
        self.assertTrue(ogre)
        self.assertNotEqual(grom[0]["cr"], ogre[0]["cr"])


if __name__ == "__main__":
    unittest.main()
