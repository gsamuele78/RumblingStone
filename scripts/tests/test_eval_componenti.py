"""Il registro e il runner unici delle misure dei componenti (lotto E1, ADR-0155).

Fissano la forma del registro ``plans/eval/componenti.json``, il confronto
esatto con il tetto (interi e frazioni «a/b» con ``fractions.Fraction``), i
codici d'uscita del runner (0 al tetto, 1 sotto, 2 comando fallito o voce
malformata), il tetto letto dal set invece che duplicato, il cricchetto contro
un tetto peggiorato a mano rispetto a un ref git, e i numeri di oggi dei due
componenti che il registro copre per primi.
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import eval_componenti as E  # noqa: E402

PY = sys.executable


def _voce(**sopra) -> dict:
    """Una voce valida su un set finto, che i test cambiano un campo alla volta."""
    v = {
        "id": "finto",
        "componente": "comp.py",
        "set": "set.json",
        "comando": ["{python}", "comp.py", "{set}"],
        "metriche": {
            "giusti": {"percorso": "test.giusti", "verso": "alto"},
            "f1": {"percorso": "test.f1", "verso": "alto"},
            "errori": {"percorso": "errori", "verso": "basso"},
        },
        "tetto": {
            "giusti": {"dal_set": "tetto.giusti"},
            "f1": {"dal_set": "tetto.f1"},
            "errori": 2,
        },
        "canale": "testing",
        "adr": ["ADR-0099"],
    }
    v.update(sopra)
    return v


class _Radice(unittest.TestCase):
    """Una radice finta: un componente che stampa JSON, il suo set, un ADR."""

    USCITA = {"test": {"giusti": 4, "f1": "58/315"}, "errori": 1}
    SET = {"tetto": {"nota": "si alza a mano", "giusti": 4, "f1": "58/315"}, "casi": []}

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.radice = Path(self._tmp.name)
        (self.radice / "plans" / "adr").mkdir(parents=True)
        (self.radice / "plans" / "adr" / "ADR-0099-tre-canali.md").write_text("x", encoding="utf-8")
        self.scrivi_set(self.SET)
        self.scrivi_componente(self.USCITA)

    def tearDown(self):
        self._tmp.cleanup()

    def scrivi_set(self, dati: dict) -> None:
        (self.radice / "set.json").write_text(json.dumps(dati, ensure_ascii=False), encoding="utf-8")

    def scrivi_componente(self, uscita: dict, codice: int = 0) -> None:
        (self.radice / "comp.py").write_text(
            "import json, sys\n"
            f"print(json.dumps({json.dumps(uscita)}))\n"
            f"sys.exit({codice})\n", encoding="utf-8")

    def registro(self, *voci) -> dict:
        return {"versione": 1, "nota": "prova", "componenti": list(voci) or [_voce()]}


class TestFormaDelRegistro(_Radice):
    def test_una_voce_valida_non_ha_errori(self):
        self.assertEqual(E.controlla_registro(self.registro(), self.radice), [])

    def test_mancano_campi(self):
        v = _voce()
        del v["canale"]
        err = E.controlla_registro(self.registro(v), self.radice)
        self.assertTrue(any("canale" in e for e in err), err)

    def test_canale_fuori_dai_tre_di_adr_0099(self):
        err = E.controlla_registro(self.registro(_voce(canale="beta")), self.radice)
        self.assertTrue(any("canale" in e for e in err), err)

    def test_il_componente_e_il_set_esistono(self):
        err = E.controlla_registro(self.registro(_voce(componente="manca.py", set="manca.json")),
                                   self.radice)
        self.assertTrue(any("manca.py" in e for e in err), err)
        self.assertTrue(any("manca.json" in e for e in err), err)

    def test_il_comando_e_una_lista_argv_senza_shell(self):
        err = E.controlla_registro(self.registro(_voce(comando="python3 comp.py | cat")), self.radice)
        self.assertTrue(any("comando" in e for e in err), err)

    def test_verso_ammesso(self):
        v = _voce()
        v["metriche"]["giusti"]["verso"] = "meglio"
        err = E.controlla_registro(self.registro(v), self.radice)
        self.assertTrue(any("verso" in e for e in err), err)

    def test_ogni_metrica_ha_il_suo_tetto(self):
        v = _voce()
        del v["tetto"]["f1"]
        err = E.controlla_registro(self.registro(v), self.radice)
        self.assertTrue(any("f1" in e for e in err), err)

    def test_il_tetto_dal_set_deve_esistere_nel_set(self):
        v = _voce()
        v["tetto"]["giusti"] = {"dal_set": "tetto.nessuno"}
        err = E.controlla_registro(self.registro(v), self.radice)
        self.assertTrue(any("tetto.nessuno" in e for e in err), err)

    def test_un_tetto_che_non_e_un_numero_ne_una_frazione(self):
        v = _voce()
        v["tetto"]["errori"] = "molti"
        err = E.controlla_registro(self.registro(v), self.radice)
        self.assertTrue(any("errori" in e for e in err), err)

    def test_l_adr_esiste(self):
        err = E.controlla_registro(self.registro(_voce(adr=["ADR-9999"])), self.radice)
        self.assertTrue(any("ADR-9999" in e for e in err), err)

    def test_id_duplicati(self):
        err = E.controlla_registro(self.registro(_voce(), _voce()), self.radice)
        self.assertTrue(any("duplicat" in e for e in err), err)

    def test_check_registro_non_esegue_niente_ed_esce_2_se_malformato(self):
        reg = self.radice / "reg.json"
        reg.write_text(json.dumps(self.registro(_voce(canale="beta"))), encoding="utf-8")
        self.scrivi_componente({}, codice=7)  # se partisse, si vedrebbe
        with redirect_stdout(io.StringIO()):
            self.assertEqual(E.main(["--check-registro", "--registro", str(reg),
                                     "--radice", str(self.radice)]), 2)
        reg.write_text(json.dumps(self.registro()), encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(E.main(["--check-registro", "--registro", str(reg),
                                     "--radice", str(self.radice)]), 0)


class TestConfronto(unittest.TestCase):
    def test_le_frazioni_si_confrontano_esatte(self):
        # 58/315 = 0.18412698...: un decimale arrotondato non è la stessa misura
        self.assertEqual(E.confronta(Fraction(58, 315), Fraction(58, 315), "alto"), "al tetto")
        self.assertEqual(E.confronta(Fraction(57, 315), Fraction(58, 315), "alto"), "sotto")
        self.assertEqual(E.confronta(Fraction(59, 315), Fraction(58, 315), "alto"), "sopra")

    def test_il_verso_basso_rovescia(self):
        self.assertEqual(E.confronta(Fraction(18), Fraction(17), "basso"), "sotto")
        self.assertEqual(E.confronta(Fraction(16), Fraction(17), "basso"), "sopra")

    def test_numero_legge_interi_e_stringhe_a_b(self):
        self.assertEqual(E.numero(4), Fraction(4))
        self.assertEqual(E.numero("58/315"), Fraction(58, 315))
        with self.assertRaises(ValueError):
            E.numero(True)  # un booleano non è una misura
        with self.assertRaises(ValueError):
            E.numero(0.1841)  # un float non si confronta esatto


class TestEsecuzione(_Radice):
    def esegui(self, reg: dict, *argv) -> "tuple[int, str]":
        p = self.radice / "reg.json"
        p.write_text(json.dumps(reg), encoding="utf-8")
        out = io.StringIO()
        with redirect_stdout(out):
            codice = E.main(["--registro", str(p), "--radice", str(self.radice),
                             "--rispetto-a", "nessun-ref-che-esista", *argv])
        return codice, out.getvalue()

    def test_al_tetto_esce_0_e_stampa_la_tabella(self):
        codice, out = self.esegui(self.registro())
        self.assertEqual(codice, 0, out)
        for parola in ("finto", "giusti", "58/315", "al tetto"):
            self.assertIn(parola, out)

    def test_una_metrica_che_scende_esce_1(self):
        self.scrivi_componente({"test": {"giusti": 3, "f1": "58/315"}, "errori": 1})
        codice, out = self.esegui(self.registro())
        self.assertEqual(codice, 1, out)
        self.assertIn("sotto", out)

    def test_una_metrica_basso_che_sale_esce_1(self):
        self.scrivi_componente({"test": {"giusti": 4, "f1": "58/315"}, "errori": 3})
        self.assertEqual(self.esegui(self.registro())[0], 1)

    def test_un_comando_che_fallisce_esce_2(self):
        self.scrivi_componente(self.USCITA, codice=3)
        codice, out = self.esegui(self.registro())
        self.assertEqual(codice, 2, out)

    def test_un_uscita_che_non_e_json_esce_2(self):
        (self.radice / "comp.py").write_text("print('ciao')\n", encoding="utf-8")
        self.assertEqual(self.esegui(self.registro())[0], 2)

    def test_un_percorso_che_manca_nell_uscita_esce_2(self):
        self.scrivi_componente({"test": {"giusti": 4}, "errori": 1})
        self.assertEqual(self.esegui(self.registro())[0], 2)

    def test_una_voce_malformata_esce_2_senza_eseguire(self):
        self.assertEqual(self.esegui(self.registro(_voce(canale="beta")))[0], 2)

    def test_il_2_vince_sull_1(self):
        rotto = _voce(id="rotto", comando=["{python}", "-c", "import sys; sys.exit(5)"])
        self.scrivi_componente({"test": {"giusti": 1, "f1": "1/315"}, "errori": 1})
        self.assertEqual(self.esegui(self.registro(_voce(), rotto))[0], 2)

    def test_solo_esegue_una_voce(self):
        rotto = _voce(id="rotto", comando=["{python}", "-c", "import sys; sys.exit(5)"])
        codice, out = self.esegui(self.registro(_voce(), rotto), "--solo", "finto")
        self.assertEqual(codice, 0, out)
        self.assertNotIn("rotto", out)

    def test_solo_un_id_che_non_c_e_esce_2(self):
        self.assertEqual(self.esegui(self.registro(), "--solo", "nessuno")[0], 2)

    def test_json_e_il_rapporto_macchina(self):
        codice, out = self.esegui(self.registro(), "--json")
        r = json.loads(out)
        self.assertEqual(codice, 0)
        self.assertEqual(r["esito"], 0)
        voce = r["voci"][0]
        self.assertEqual(voce["id"], "finto")
        self.assertEqual(voce["canale"], "testing")
        m = {x["nome"]: x for x in voce["metriche"]}
        self.assertEqual(m["f1"]["valore"], "58/315")
        self.assertEqual(m["f1"]["tetto"], "58/315")
        self.assertEqual(m["errori"]["verso"], "basso")
        self.assertEqual(m["errori"]["esito"], "sopra")
        self.assertIn("secondi", voce)

    def test_il_tetto_si_legge_dal_set_non_dal_registro(self):
        # il set alza il tetto: il registro, che non lo copia, lo segue da solo
        self.scrivi_set({"tetto": {"nota": "x", "giusti": 5, "f1": "58/315"}})
        codice, out = self.esegui(self.registro())
        self.assertEqual(codice, 1, out)

    def test_il_segnaposto_set_diventa_il_percorso_del_set(self):
        argv = E.argv(_voce(), self.radice)
        self.assertEqual(argv[0], PY)
        self.assertEqual(argv[-1], str(self.radice / "set.json"))


class TestCricchetto(_Radice):
    """Un tetto peggiorato a mano rispetto a REF fa uscire 1 (requisito 4)."""

    def setUp(self):
        super().setUp()
        self.reg = self.radice / "reg.json"
        self.reg.write_text(json.dumps(self.registro()), encoding="utf-8")
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "base")

    def git(self, *a):
        subprocess.run(["git", "-C", str(self.radice), *a], check=True, capture_output=True)

    def cricchetto(self, ref="HEAD"):
        return E.cricchetto(json.loads(self.reg.read_text(encoding="utf-8")), self.radice, ref,
                            registro_rel="reg.json")

    def test_tetti_invariati_esce_0(self):
        codice, msg = self.cricchetto()
        self.assertEqual(codice, 0, msg)

    def test_un_tetto_abbassato_a_mano_nel_set_esce_1(self):
        self.scrivi_set({"tetto": {"nota": "si alza a mano", "giusti": 3, "f1": "58/315"}})
        codice, msg = self.cricchetto()
        self.assertEqual(codice, 1, msg)
        self.assertTrue(any("giusti" in m for m in msg), msg)

    def test_una_frazione_abbassata_esce_1(self):
        self.scrivi_set({"tetto": {"nota": "si alza a mano", "giusti": 4, "f1": "41/252"}})
        self.assertEqual(self.cricchetto()[0], 1)

    def test_un_tetto_basso_alzato_nel_registro_esce_1(self):
        v = _voce()
        v["tetto"]["errori"] = 3
        self.reg.write_text(json.dumps(self.registro(v)), encoding="utf-8")
        self.assertEqual(self.cricchetto()[0], 1)

    def test_un_tetto_migliorato_passa(self):
        self.scrivi_set({"tetto": {"nota": "si alza a mano", "giusti": 6, "f1": "60/315"}})
        self.assertEqual(self.cricchetto()[0], 0)

    def test_la_rimessa_di_applica_lascia_passare(self):
        nota = ("si alza a mano " + E.MARCA_RIMESSA +
                " 2026-11-30, entrati 3 casi confermati da Jfs; è cambiato il set, non l'hook.")
        self.scrivi_set({"tetto": {"nota": nota, "giusti": 3, "f1": "41/252"}})
        codice, msg = self.cricchetto()
        self.assertEqual(codice, 0, msg)
        self.assertTrue(any("applica" in m for m in msg), msg)

    def test_una_rimessa_vecchia_non_copre_un_abbassamento_nuovo(self):
        nota = "base " + E.MARCA_RIMESSA + " 2026-11-30, entrati 3 casi."
        self.scrivi_set({"tetto": {"nota": nota, "giusti": 4, "f1": "58/315"}})
        self.git("commit", "-qam", "rimessa")
        self.scrivi_set({"tetto": {"nota": nota, "giusti": 2, "f1": "58/315"}})
        self.assertEqual(self.cricchetto()[0], 1)

    def test_la_marca_e_quella_che_scrive_raccogli_casi_agenti(self):
        import raccogli_casi_agenti as R
        self.assertRegex(" " + E.MARCA_RIMESSA + " 2026-11-30, entrati 1 casi", R._RIMESSA)

    def test_un_ref_che_non_esiste_lo_dice_ed_esce_0(self):
        codice, msg = self.cricchetto("origin/non-esiste")
        self.assertEqual(codice, 0)
        self.assertTrue(any("non esiste" in m for m in msg), msg)

    def test_una_voce_nuova_su_ref_non_si_confronta(self):
        (self.radice / "set2.json").write_text(json.dumps(self.SET), encoding="utf-8")
        v2 = _voce(id="nuova", set="set2.json")
        self.reg.write_text(json.dumps(self.registro(_voce(), v2)), encoding="utf-8")
        codice, msg = self.cricchetto()
        self.assertEqual(codice, 0, msg)

    def _main_avanti(self):
        """REF è andato avanti dopo il ramo e ha alzato il tetto; il ramo non l'ha toccato."""
        self.git("branch", "-M", "ramo")
        self.git("checkout", "-q", "-b", "avanti")
        self.scrivi_set({"tetto": {"nota": "si alza a mano", "giusti": 5, "f1": "58/315"}})
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", "alza")
        self.git("checkout", "-q", "ramo")

    def test_un_ramo_indietro_rispetto_a_ref_non_e_un_abbassamento(self):
        # si confronta col punto in cui il ramo si stacca da REF (REF...HEAD),
        # non con la punta di REF: se no un tetto alzato su main dopo il ramo
        # sembra abbassato a mano sul ramo
        self._main_avanti()
        codice, msg = self.cricchetto("avanti")
        self.assertEqual(codice, 0, msg)

    def test_sul_ramo_indietro_un_abbassamento_vero_esce_ancora_1(self):
        self._main_avanti()
        self.scrivi_set({"tetto": {"nota": "si alza a mano", "giusti": 3, "f1": "58/315"}})
        self.assertEqual(self.cricchetto("avanti")[0], 1)


class TestRegistroVero(unittest.TestCase):
    """Il registro del repo: le prime due voci e i numeri di oggi (requisito 1)."""

    @classmethod
    def setUpClass(cls):
        cls.reg = E.carica_registro(E.REGISTRO)
        cls.voci = {v["id"]: v for v in cls.reg["componenti"]}

    def test_la_forma_e_valida(self):
        self.assertEqual(E.controlla_registro(self.reg, E.RADICE), [])

    def test_le_prime_due_voci(self):
        self.assertLessEqual({"instradamento_agenti", "instradamento_skill"}, set(self.voci))
        self.assertEqual(self.voci["instradamento_agenti"]["canale"], "testing")
        self.assertEqual(self.voci["instradamento_skill"]["canale"], "stable")

    def test_i_tetti_coincidono_con_quelli_dei_set(self):
        oro = json.loads((E.RADICE / "plans/instradamento/agenti-oro.json").read_text(encoding="utf-8"))
        casi = json.loads((E.RADICE / "plans/instradamento/casi.json").read_text(encoding="utf-8"))
        ta = E.tetti(self.voci["instradamento_agenti"], E.RADICE)
        self.assertEqual(ta["giusti"], Fraction(oro["tetto"]["giusti"]))
        self.assertEqual(ta["giusti_indulgenti"], Fraction(oro["tetto"]["giusti_indulgenti"]))
        self.assertEqual(ta["macro_f1"], Fraction(oro["tetto"]["macro_f1"]))
        ts = E.tetti(self.voci["instradamento_skill"], E.RADICE)
        self.assertEqual(ts["omissioni"], Fraction(casi["tetto_omissioni"]))
        self.assertEqual(ts["violazioni"], Fraction(casi["tetto_violazioni"]))
        self.assertEqual(ts["conflitti_l1"], 0)

    def test_nessun_tetto_dei_set_e_duplicato_nel_registro(self):
        for vid in ("instradamento_agenti", "instradamento_skill"):
            for nome, spec in self.voci[vid]["tetto"].items():
                if nome != "conflitti_l1":  # vive nel codice di instradamento_skill, non nel set
                    with self.subTest(vid=vid, nome=nome):
                        self.assertIsInstance(spec, dict)
                        self.assertIn("dal_set", spec)

    def test_i_numeri_di_oggi(self):
        r = E.esegui(self.reg, E.RADICE)
        self.assertEqual(r["esito"], 0, r)
        val = {(v["id"], m["nome"]): m["valore"] for v in r["voci"] for m in v["metriche"]}
        self.assertEqual(val[("instradamento_agenti", "giusti")], "4")
        self.assertEqual(val[("instradamento_agenti", "giusti_indulgenti")], "4")
        self.assertEqual(val[("instradamento_agenti", "macro_f1")], "58/315")
        self.assertEqual(val[("instradamento_skill", "omissioni")], "17")
        self.assertEqual(val[("instradamento_skill", "violazioni")], "1")
        self.assertEqual(val[("instradamento_skill", "conflitti_l1")], "0")


if __name__ == "__main__":
    unittest.main()
