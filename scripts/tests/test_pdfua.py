"""PDF/UA-1 (ISO 14289-1) nell'edizione da stampa (ADR-0129).

Typst verifica da sé, alla compilazione, gli obblighi di PDF/UA-1 che dipendono
dal documento: il primo titolo è di livello 1, nessun titolo salta un livello,
ogni immagine ha un testo alternativo o è un artefatto, lingua e titolo del
documento ci sono. Se uno manca rifiuta di compilare. Questi test sono il
cancello: il tema e il convertitore devono restare in grado di produrre
PDF/UA-1, e un booklet vero (il più piccolo con schede e immagini) lo è.
La conformità piena la misura veraPDF fuori dalla CI
(`plans/esperimenti/pdfua-2026-11-13/`).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import export_booklet_typst as ex  # noqa: E402
import typst_motore as tm  # noqa: E402

TESTA = ('#import "/scripts/typst/tema-rumblingstone.typ": *\n'
         '#show: libro.with(titolo: "Prova", sottotitolo: "", brand: "", banner: "", meta: "",\n'
         '  capitolo: "Prova", apparato: false)\n')


def _compila(corpo: str, pdfua: bool = True) -> tm.Esito:
    with tempfile.TemporaryDirectory(dir=REPO) as d:
        typ = Path(d) / "p.typ"
        typ.write_text(TESTA + corpo, encoding="utf-8")
        return tm.compila(typ, Path(d) / "p.pdf", root=REPO, font=ex.FONTS,
                          pacchetti=ex.PACCHETTI, pdfua=pdfua)


class TestTitoliSenzaSalti(unittest.TestCase):
    def test_un_salto_sale_di_livello_e_ricorda_il_disegno(self):
        src, n = ex.titoli_senza_salti('#capitolo-aperto("I", none)\n=== Chi si incontra\n== Dopo\n')
        self.assertEqual(n, 1)
        self.assertIn("#heading(level: 2)[Chi si incontra] <come-3>", src)
        self.assertIn("\n== Dopo", src)

    def test_sotto_la_profondita_dell_indice_resta_fuori(self):
        src, n = ex.titoli_senza_salti("= A\n== B\n==== C\n")
        self.assertEqual(n, 1)
        self.assertIn("#heading(level: 3, outlined: false)[C] <come-4>", src)

    def test_una_scheda_apre_al_livello_1(self):
        src, n = ex.titoli_senza_salti("== A\n#scheda(\n  nome: [X],\n)\n=== B\n")
        self.assertEqual(n, 1)

    def test_senza_salti_non_cambia_nulla(self):
        testo = "= A\n== B\n=== C\n== D\n= E\n"
        self.assertEqual(ex.titoli_senza_salti(testo), (testo, 0))

    def test_un_titolo_con_etichetta_non_si_tocca(self):
        testo = "= A\n=== B <x>\n"
        self.assertEqual(ex.titoli_senza_salti(testo), (testo, 0))


@unittest.skipUnless(tm.disponibile(), "typst assente")
class TestIlTemaProducePdfUa(unittest.TestCase):
    def test_capitolo_con_titolo_muto_e_salto_riparato(self):
        corpo = ('#capitolo-aperto("I · Apertura", none)\n'
                 '#heading(level: 2)[Chi si incontra] <come-3>\n'
                 'Testo.\n== Sezione\nAltro testo.\n')
        e = _compila(corpo)
        self.assertTrue(e.ok, e.errore)
        self.assertTrue(e.pdfua, e.motivo_pdfua)

    def test_hide_del_titolo_era_il_difetto(self):
        """Il modo di prima: typst lo rifiuta, e l'esito lo dice invece di fallire."""
        e = _compila("#hide(heading(level: 1)[Nascosto])\n== Dopo\nTesto.\n")
        self.assertTrue(e.ok, e.errore)
        self.assertFalse(e.pdfua)
        self.assertIn("first heading", e.motivo_pdfua)

    def test_senza_pdfua_si_compila_come_prima(self):
        e = _compila("= Uno\nTesto.\n", pdfua=False)
        self.assertTrue(e.ok and not e.pdfua and not e.motivo_pdfua)


@unittest.skipUnless(tm.disponibile(), "typst assente")
class TestUnBookletVero(unittest.TestCase):
    """Il fascicolo delle schede del Drappo: schede PG con ritratto, titoli muti."""

    MANIFEST = REPO / "10-stand-alone/Il-Drappo-di-Tarsilia/homebrew/DRAPPO-SCHEDE-PG.manifest.json"

    def test_esce_pdf_ua_1(self):
        pdf = self.MANIFEST.parent / "DRAPPO-SCHEDE-PG-STAMPA.pdf"
        c_era = pdf.exists()
        r = subprocess.run([sys.executable, str(REPO / "scripts/export_booklet_typst.py"),
                            str(self.MANIFEST), "--all"], capture_output=True, text=True, cwd=REPO)
        try:
            self.assertEqual(r.returncode, 0, r.stderr[-2000:])
            self.assertIn("PDF/UA-1", r.stdout)
            self.assertNotIn("non è PDF/UA-1", r.stderr)
        finally:
            if not c_era:
                pdf.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
