"""collaudo_mappe (ADR-0082, PIANO-COLLAUDO-E-GENERAZIONE-MAPPE V1).

Ogni controllo ha un caso che deve mordere e uno che deve tacere: un
controllo che non si e' mai visto rosso non si sa se funziona.
"""

import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import collaudo_mappe as C  # noqa: E402


def _master(cartella: Path, nome: str, righe: list[str], direttive: list[str] = (),
            legenda: str = "") -> Path:
    corpo = ["## MAPPA PROVA", "", "```",
             "COL →  " + " ".join(chr(65 + i) for i in range(len(righe[0])))]
    corpo += [f"{i:02d}    {r}" for i, r in enumerate(righe, 1)]
    if legenda:
        corpo.append("LEGENDA · " + legenda)
    corpo += list(direttive) + ["```", ""]
    p = cartella / nome
    p.write_text("\n".join(corpo), encoding="utf-8")
    return p


def _codici(percorso: Path) -> list[str]:
    testo = percorso.read_text(encoding="utf-8")
    esiti = [C.Collaudo(percorso, i, g, {}).esegui()
             for i, g in enumerate(C.R.extract_maps(testo), 1)]
    return [r["codice"] for e in esiti for r in e.rilievi if not r["deroga"]]


STANZA = [
    "🏰🏰🏰🚪🏰🏰",
    "🏰⬜⬜⬜⬜🏰",
    "🏰⬜🔵⬜⬜🏰",
    "🏰⬜⬜🔴⬜🏰",
    "🏰🏰🏰🏰🏰🏰",
]


class TestCollaudo(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_una_stanza_pulita_non_ha_errori(self):
        p = _master(self.tmp, "ok.md", STANZA, ["@north N"])
        self.assertEqual([c for c in _codici(p) if C.CLASSE[c] == "E"], [])

    def test_il_nord_e_obbligatorio_nelle_tattiche(self):
        p = _master(self.tmp, "n.md", STANZA)
        self.assertIn("nord/mancante", _codici(p))

    def test_una_strategica_non_riceve_i_controlli_tattici(self):
        p = _master(self.tmp, "s.md", STANZA, ["@tipo strategica"])
        self.assertNotIn("nord/mancante", _codici(p))

    def test_simbolo_ignoto(self):
        righe = [r for r in STANZA]
        righe[1] = "🏰⬜🦄⬜⬜🏰"
        p = _master(self.tmp, "i.md", righe, ["@north N"])
        self.assertIn("simbolo/ignoto", _codici(p))

    def test_un_simbolo_locale_dichiarato_non_e_ignoto(self):
        righe = [r for r in STANZA]
        righe[1] = "🏰⬜🦄⬜⬜🏰"
        p = _master(self.tmp, "l.md", righe, ["@north N"], legenda="🦄 statua del cavallo")
        self.assertNotIn("simbolo/ignoto", _codici(p))

    def test_la_legenda_locale_non_rovescia_un_universale(self):
        """Il difetto del Cuore della Montagna: ⬛ muratura usato come pavimento."""
        p = _master(self.tmp, "f.md", STANZA, ["@north N"], legenda="⬛ pavimento di caverna")
        self.assertIn("legenda/funzione-opposta", _codici(p))

    def test_porta_sospesa(self):
        righe = [r for r in STANZA]
        righe[2] = "🏰⬜🔵🚪⬜🏰"
        p = _master(self.tmp, "p.md", righe, ["@north N"])
        self.assertIn("posa/nel-muro", _codici(p))

    def test_una_fila_di_porte_e_un_varco_solo(self):
        righe = ["🏰🚪🚪🚪🏰🏰"] + STANZA[1:]
        p = _master(self.tmp, "r.md", righe, ["@north N"])
        self.assertEqual(_codici(p).count("posa/nel-muro"), 0)

    def test_unita_irraggiungibile(self):
        righe = ["🏰🏰🏰🏰🏰🏰",
                 "🏰⬜🔵🏰⬜🏰",
                 "🏰⬜⬜🏰🔴🏰",
                 "🏰🏰🏰🏰🏰🏰"]
        p = _master(self.tmp, "u.md", righe, ["@north N"])
        self.assertIn("raggiungibile/unita", _codici(p))

    def test_la_diagonale_non_passa_l_angolo_di_un_muro(self):
        """SRD: niente diagonale oltre l'angolo di un muro."""
        righe = ["🏰🏰🏰🏰🏰",
                 "🏰🔵🏰🏰🏰",
                 "🏰🏰🔴⬜🏰",
                 "🏰🏰🏰🏰🏰"]
        p = _master(self.tmp, "d.md", righe, ["@north N"])
        self.assertIn("raggiungibile/unita", _codici(p))

    def test_la_diagonale_passa_una_fossa(self):
        """SRD: la diagonale passa oltre una fossa, che non e' un muro."""
        righe = ["🏰🏰🏰🏰🏰",
                 "🏰🔵🕳🏰🏰",
                 "🏰🕳🔴⬜🏰",
                 "🏰🏰🏰🏰🏰"]
        p = _master(self.tmp, "f2.md", righe, ["@north N"])
        self.assertNotIn("raggiungibile/unita", _codici(p))

    def test_la_scala_senza_gemella_morde(self):
        righe = [r for r in STANZA]
        righe[1] = "🏰🔽⬜⬜⬜🏰"
        p = _master(self.tmp, "sc.md", righe, ["@north N"])
        self.assertIn("posa/fra-livelli", _codici(p))

    def test_la_scala_con_la_gemella_giusta_tace(self):
        sotto = _master(self.tmp, "sotto.md", [r.replace("🚪", "🏰") for r in STANZA[:1]] +
                        ["🏰🔼⬜⬜⬜🏰"] + STANZA[2:], ["@north N", "@collega B02 ; sopra.md C02"])
        sopra = [r for r in STANZA]
        sopra[1] = "🏰⬜🔽⬜⬜🏰"
        su = _master(self.tmp, "sopra.md", sopra, ["@north N", f"@collega C02 ; {sotto.name} B02"])
        self.assertNotIn("posa/fra-livelli", _codici(su))
        self.assertNotIn("posa/fra-livelli", _codici(sotto))

    def test_due_scale_nello_stesso_verso_mordono(self):
        a = [r for r in STANZA]
        a[1] = "🏰🔽⬜⬜⬜🏰"
        _master(self.tmp, "b.md", a, ["@north N"])
        p = _master(self.tmp, "a.md", a, ["@north N", "@collega B02 ; b.md B02"])
        self.assertIn("posa/fra-livelli", _codici(p))

    def test_la_porta_segreta_non_va_ai_giocatori(self):
        righe = ["🏰🏰🏰❔🏰🏰"] + STANZA[1:]
        master = _master(self.tmp, "m.md", righe, ["@north N"])
        giocatori = _master(self.tmp, "g.md", righe, ["@north N", "@vista giocatori"])
        self.assertNotIn("posa/solo-master", _codici(master))
        self.assertIn("posa/solo-master", _codici(giocatori))

    def test_una_deroga_motivata_sospende_il_codice(self):
        p = _master(self.tmp, "dr.md", STANZA,
                    ["@deroga nord/mancante ; la mappa e' un dettaglio senza orientamento"])
        self.assertNotIn("nord/mancante", _codici(p))

    def test_una_deroga_senza_motivo_non_vale(self):
        p = _master(self.tmp, "dv.md", STANZA, ["@deroga nord/mancante ; boh"])
        self.assertIn("nord/mancante", _codici(p))

    def test_un_grande_non_passa_un_corridoio_largo_uno(self):
        righe = ["🏰🏰🏰🏰🏰🏰🏰🏰",
                 "🏰⬜⬜🏰🏰🏰🔵🏰",
                 "🏰⬜🔴⬜⬜⬜⬜🏰",
                 "🏰🏰🏰🏰🏰🏰🏰🏰"]
        p = _master(self.tmp, "g2.md", righe, ["@north N", "@taglia C03 ; Grande"])
        self.assertIn("ingombro/grande", _codici(p))

    def test_un_grande_passa_dove_c_e_spazio(self):
        righe = ["🏰🏰🏰🏰🏰🏰",
                 "🏰⬜⬜⬜⬜🏰",
                 "🏰⬜🔴⬜🔵🏰",
                 "🏰⬜⬜⬜⬜🏰",
                 "🏰🏰🏰🏰🏰🏰"]
        p = _master(self.tmp, "g3.md", righe, ["@north N", "@taglia C03 ; Grande"])
        self.assertNotIn("ingombro/grande", _codici(p))

    def test_il_json_e_la_cli(self):
        p = _master(self.tmp, "j.md", STANZA)
        out = self.tmp / "r.json"
        self.assertEqual(C.main([str(p), "--json", str(out)]), 0)
        dati = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(dati["schema"], "map_findings/1")
        self.assertEqual(dati["mappe"][0]["distanza_giocabilita"], C.PESI["nord/mancante"])
        self.assertEqual(C.main([str(p), "--strict"]), 1)
        self.assertEqual(C.main([str(self.tmp / "non-esiste.md")]), 2)


if __name__ == "__main__":
    unittest.main()
