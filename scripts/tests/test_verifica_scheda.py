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

    def test_gradi_di_abilita_gonfiati(self):
        # un'abilità alzata di 20: i gradi minimi superano il massimo (dadi vita + 3)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / ABISHAI.name
            testo = ABISHAI.read_text(encoding="utf-8")
            self.assertEqual(V.abilita(ABISHAI), ([], []))
            riga = next(r for r in testo.splitlines() if V.RIGA_ABILITA.search(r))
            nuova = re.sub(r"\+(\d+)", lambda m: f"+{int(m.group(1)) + 20}", riga, count=1) \
                if not V.RIGA_ABILITA.search(riga).start(1) else None
            m = V.RIGA_ABILITA.search(riga)
            gonfia = re.sub(r"\+(\d+)", lambda k: f"+{int(k.group(1)) + 20}", m.group(1), count=1)
            p.write_text(testo.replace(riga, riga[:m.start(1)] + gonfia + riga[m.end(1):]), encoding="utf-8")
            del nuova
            viol, _ = V.abilita(p)
        self.assertIn("gradi.massimo", {x["regola"] for x in viol})
        v = next(x for x in viol if x["regola"] == "gradi.massimo")
        self.assertGreater(v["ha"], v["atteso"])

    def test_gradi_classe_fuori_dal_plugin_non_si_giudica(self):
        # Krusk ha il Berserker Furioso, che dal 2026-11-12 il plugin conosce
        # (classi_manuali.toml): la classe ignota qui è inventata.
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / KRUSK.name
            p.write_text(KRUSK.read_text(encoding="utf-8").replace("Berserker Furioso 7", "Spaccatutto di Nessuno 7"),
                         encoding="utf-8")
            viol, nv = V.abilita(p)
        self.assertEqual(viol, [])
        self.assertTrue(any(x["regola"] == "gradi.punti" for x in nv))
        self.assertEqual(V.abilita(KRUSK), ([], []))

    def test_regole_dei_gradi_nei_due_plugin(self):
        from dmcore import sistemi as S
        d35, pf = S.dati("dnd35", "creature.gradi"), S.dati("pf1e", "creature.gradi")
        self.assertEqual((d35["regole"]["massimo_piu"], d35["regole"]["primo_dado"]), (3, 4))
        self.assertEqual((pf["regole"]["massimo_piu"], pf["regole"]["primo_dado"]), (0, 1))
        self.assertEqual((d35["classi"]["rogue"], d35["tipi"]["outsider"], d35["chiave"]["hide"]), (8, 8, "Des"))
        self.assertEqual((pf["classi"]["rogue"]["gradi"], pf["tipi"]["outsider"], pf["chiave"]["stealth"]),
                         (8, 6, "Des"))

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


class ClassiDeiManuali(unittest.TestCase):
    """Le classi 3.5 fuori SRD (classi_manuali.toml, ADR-0124 §8)."""

    def test_classe_dei_manuali_entra_nei_conti(self):
        from dmcore import progressione as P
        assert P.classe("warlock") == (6, ("vol",), 0.75)
        assert P.classe("berserker furioso") == P.classe("frenzied berserker")
        # una classe dell'SRD non viene mai sostituita da un manuale
        assert P.classe("fighter") == (10, ("temp",), 1.0)


    def test_classe_dei_manuali_solo_a_nome_intero(self):
        from dmcore import progressione as P
        # «tempest» (Complete Adventurer) non deve leggere «Cantore delle tempeste 2»
        assert P.CLASSE_LIVELLO.findall("Bardo 12 / Cantore delle tempeste 2") == [("Bardo", "12")]
        assert P.CLASSE_LIVELLO.findall("Umano Warlock 6") == [("Warlock", "6")]
        assert P.CLASSE_LIVELLO.findall("Guerriera 4") == [("Guerrier", "4")]


    def test_classe_su_cui_le_fonti_divergono_resta_sconosciuta(self):
        from dmcore import progressione as P
        from dmcore import sistemi as S
        manuali = S.dati("dnd35", "creature.costruzione")["classi_manuali"]
        divergenti = [n for n, v in manuali.items() if v.get("diverge")]
        assert divergenti and all(P.classe(n) is None for n in divergenti)
        assert all(not P.manuale_affidabile(manuali[n]) for n in divergenti)


    def test_punti_abilita_di_una_classe_dei_manuali(self):
        import verifica_scheda as VS
        from dmcore import sistemi as S
        regole = S.dati("dnd35", "creature.gradi")
        assert VS._punti_di_classe(regole, "scout") == 8
        assert VS._punti_di_classe(regole, "fighter") == 2



class Incantesimi(unittest.TestCase):
    """Gli incantesimi scritti per livello contro le liste del plugin (ADR-0124 §10)."""

    SCHEDA = ("# Prova\n\n```statblocco\ngs: 5\ntipo: Medium humanoid (human), Chierico 5, LN\n```\n\n"
              "**Incantesimi da chierico** (LI 5, CD 13 + livello):\n"
              "- 3° (2+1): *dissolvi magie*, *preghiera*; dominio: *protezione dall'energia*\n"
              "- 2° (3+1): *aiuto*, *blocca persone* (CD 15)\n"
              "- 1° (4+1): *benedizione*, *scudo della fede*\n")

    def _giudica(self, testo):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "prova-cr5.md"
            p.write_text(testo, encoding="utf-8")
            return V.incantesimi(p)

    def test_scheda_pulita(self):
        self.assertEqual(self._giudica(self.SCHEDA), ([], []))

    def test_livello_troppo_basso(self):
        viol, _ = self._giudica(self.SCHEDA.replace("*benedizione*", "*benedizione*, *colpo infuocato*"))
        self.assertEqual([(v["regola"], v["atteso"], v["ha"]) for v in viol], [("incantesimo.livello", 5, 1)])

    def test_fuori_lista(self):
        viol, _ = self._giudica(self.SCHEDA.replace("*aiuto*", "*palla di fuoco*"))
        self.assertEqual([v["regola"] for v in viol], ["incantesimo.lista"])
        self.assertEqual(viol[0]["riga"], 10)

    def test_slot_piu_alto_si_accetta(self):
        self.assertEqual(self._giudica(self.SCHEDA.replace("*preghiera*", "*preghiera*, *benedizione*"))[0], [])

    def test_nome_fuori_dalle_liste_non_si_giudica(self):
        viol, nv = self._giudica(self.SCHEDA.replace("*aiuto*", "*lampo oscuro di Nessuno*"))
        self.assertEqual(viol, [])
        self.assertEqual([x["regola"] for x in nv], ["incantesimo.nome"])

    def test_senza_classe_nell_intestazione_non_si_giudica(self):
        self.assertEqual(self._giudica(self.SCHEDA.replace("Incantesimi da chierico", "Incantesimi")
                                       .replace("*aiuto*", "*palla di fuoco*")), ([], []))

    def test_liste_nei_due_plugin(self):
        from dmcore import sistemi as S
        d35, pf = S.dati("dnd35", "creature.liste_incantesimi"), S.dati("pf1e", "creature.liste_incantesimi")
        self.assertIn("Fireball", d35["liste"]["wizard"]["3"])
        self.assertIn("Flame Strike", d35["domini"]["sun"]["5"])
        self.assertIn("Fireball", pf["liste"]["wizard"]["3"])


if __name__ == "__main__":
    unittest.main()
