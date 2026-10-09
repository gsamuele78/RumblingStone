"""La misura della resa (R8 di RESA-ASSET, D23-D26): le parti che decidono
senza un browser, e una misura vera quando Chrome c'è."""

import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import misura_resa as M  # noqa: E402

try:
    import numpy  # noqa: F401
    import skimage  # noqa: F401
    LIB = True
except ImportError:  # pragma: no cover
    LIB = False


def _m(**k):
    base = {"copertura": 0.3, "contrasto": 6.0, "bordo": 0.3, "ssim_vicino": 0.5,
            "vicino": "🧰", "delta_e_tavolozza": 3.0}
    base.update(k)
    return base


class TestCancello(unittest.TestCase):
    def test_una_misura_che_peggiora_oltre_la_tolleranza_e_un_errore(self):
        vecchia = {"glifi": {"texture": {"interni": {"🪨": _m()}}}}
        nuova = {"glifi": {"texture": {"interni": {"🪨": _m(contrasto=5.0)}}}}
        errori = M.regressioni(vecchia, nuova)
        self.assertEqual(len(errori), 1)
        self.assertIn("contrasto da 6.0 a 5.0", errori[0])

    def test_dentro_la_tolleranza_passa(self):
        vecchia = {"glifi": {"texture": {"interni": {"🪨": _m()}}}}
        nuova = {"glifi": {"texture": {"interni": {"🪨": _m(contrasto=5.8, ssim_vicino=0.51)}}}}
        self.assertEqual(M.regressioni(vecchia, nuova), [])

    def test_un_miglioramento_non_e_un_errore(self):
        vecchia = {"glifi": {"texture": {"interni": {"🪨": _m()}}},
                   "terreni": {"texture": {"⬜": {"delta_e_vicino": 4.0}}}}
        nuova = {"glifi": {"texture": {"interni": {"🪨": _m(contrasto=9.0, ssim_vicino=0.3)}}},
                 "terreni": {"texture": {"⬜": {"delta_e_vicino": 9.0}}}}
        self.assertEqual(M.regressioni(vecchia, nuova), [])

    def test_un_terreno_che_si_confonde_di_piu_e_un_errore(self):
        vecchia = {"terreni": {"texture": {"⛰": {"delta_e_vicino": 6.0}}}}
        nuova = {"terreni": {"texture": {"⛰": {"delta_e_vicino": 1.2}}}}
        self.assertTrue(M.regressioni(vecchia, nuova))


class TestConfronto(unittest.TestCase):
    def _scheda(self, m):
        return {"glifi": {"texture": {a: {"🛏": m} for a in M.TERRENI_BANCO}}}

    def test_sotto_tre_a_uno_e_sotto_il_glifo_perde(self):
        esito = M.confronta(self._scheda(_m(contrasto=6.0)), self._scheda(_m(contrasto=2.0)))
        self.assertEqual(esito["🛏"]["interni"]["verdetto"], "perde")

    def test_piu_confondibile_perde(self):
        esito = M.confronta(self._scheda(_m()), self._scheda(_m(ssim_vicino=0.8)))
        self.assertIn("si confonde", esito["🛏"]["interni"]["ragioni"][0])

    def test_meglio_su_contrasto_e_bordo_vince(self):
        esito = M.confronta(self._scheda(_m()), self._scheda(_m(contrasto=8.0, bordo=0.4)))
        self.assertEqual(esito["🛏"]["esterno"]["verdetto"], "vince")

    def test_in_mezzo_resta_al_dm(self):
        esito = M.confronta(self._scheda(_m()), self._scheda(_m(contrasto=7.0, bordo=0.25)))
        self.assertEqual(esito["🛏"]["interni"]["verdetto"], "da giudicare")


class TestVoti(unittest.TestCase):
    def test_il_lato_si_traduce_nella_fonte(self):
        chiave = {"0": {"simbolo": "🛏", "ambiente": "interni", "sinistra": "glifo"},
                  "1": {"simbolo": "🪨", "ambiente": "esterno", "sinistra": "tessera"}}
        pref = M.registra_voti({"voti": {"0": "d", "1": "d"}}, chiave)
        self.assertEqual(pref, {"🛏": {"interni": "tessera"}, "🪨": {"esterno": "glifo"}})


class TestVotiDaScaricati(unittest.TestCase):
    """Il browser salva voti.json in ~/Scaricati, la chiave sta accanto alla pagina."""

    def test_la_chiave_si_ritrova_dal_percorso_scritto_nei_voti(self):
        import tempfile
        pagina_dir, scaricati = Path(tempfile.mkdtemp()), Path(tempfile.mkdtemp())
        chiave = pagina_dir / "coppie-cc0.chiave.json"
        chiave.write_text(json.dumps({"0": {"simbolo": "🛏", "ambiente": "interni",
                                            "sinistra": "glifo"}}), encoding="utf-8")
        voti = scaricati / "voti.json"
        voti.write_text(json.dumps({"seme": 1, "chiave": str(chiave), "voti": {"0": "s"}}),
                        encoding="utf-8")
        scheda = pagina_dir / "scheda.json"
        vecchia, M.SCHEDA = M.SCHEDA, scheda
        vecchio_rep, M.REPO = M.REPO, pagina_dir
        try:
            with redirect_stdout(io.StringIO()):
                self.assertEqual(M.main(["voti", str(voti)]), 0)
        finally:
            M.SCHEDA, M.REPO = vecchia, vecchio_rep
        self.assertEqual(json.loads(scheda.read_text(encoding="utf-8"))["preferenze_dm"],
                         {"🛏": {"interni": "glifo"}})

    def test_senza_voti_un_messaggio_e_non_un_traceback(self):
        err = io.StringIO()
        with redirect_stderr(err), redirect_stdout(io.StringIO()):
            self.assertEqual(M.main(["voti", "/non/esiste/voti.json"]), 1)
        self.assertIn("Scarica voti.json", err.getvalue())


class TestSoloFigure(unittest.TestCase):
    def test_tiene_le_definizioni_e_i_use_e_nient_altro(self):
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><defs><symbol id="a"/>'
               '</defs><rect width="10" height="10"/><circle r="3"/><use href="#a" x="1"/></svg>')
        fig = M._solo_figure(svg)
        self.assertIn('<symbol id="a"/>', fig)
        self.assertIn('<use href="#a" x="1"/>', fig)
        self.assertNotIn("<rect", fig)
        self.assertNotIn("<circle", fig)


class TestAffianca(unittest.TestCase):
    def test_una_revisione_che_non_ha_la_mappa_e_un_errore_chiaro(self):
        mappa = M.REPO / "scripts" / "legend.yaml"
        with self.assertRaisesRegex(RuntimeError, "non esiste in revisione-inesistente"):
            M.affianca(mappa, "revisione-inesistente", "browser-mai-usato", None)


@unittest.skipUnless(LIB and M._browser(), "serve un browser e scikit-image")
class TestMisuraVera(unittest.TestCase):
    def test_un_glifo_della_pergamena_si_stacca_dal_terreno(self):
        lib = M._librerie()
        cel = M.banco(["🗿", "🛏"], "pergamena", "interni", M._browser(), lib[0], M.REPO / "nessuna")
        m = M.misura_cella(cel["🗿"], cel["_fondo"]["🗿"], None, lib, cel["_figura"]["🗿"])
        self.assertGreater(m["copertura"], 0.05)
        self.assertGreater(m["contrasto"], M.SOGLIA_WCAG)

    def test_affianca_una_mappa_identica_a_head_non_cambia_pixel(self):
        mappa = next(M.REPO.glob("**/rendered/*.svg"))
        tela, cambiati = M.affianca(mappa, "HEAD", M._browser(), M._librerie()[0], "0,0,120,120")
        self.assertEqual(cambiati, 0.0)
        self.assertGreater(tela.width, tela.height)


if __name__ == "__main__":
    unittest.main()
