"""Il gate dei booklet e la conversione markdown → Typst.

Perché questi test esistono: in CI **c'è** typst (dal 2026-08-22) e i volumi si
compilano davvero, ma la compilazione dice solo «sì» o «no». Questi test dicono
*cosa* deve uscire — e coprono, uno per uno, i difetti che erano arrivati fino
ai booklet pubblicati:

  * un'immagine stampata come testo (`!Stemma Oca`);
  * grassetto attaccato a una barra che rompeva l'intero volume;
  * una chiave di manifest che una catena legge e l'altra ignora in silenzio.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

from build_booklet_html import colophon_html  # noqa: E402
from export_booklet_typst import (  # noqa: E402
    CELLE_COLONNA, VOCI_COLOPHON, crediti_typ, dimensioni, e_griglia_mappa, e_mappa, inline,
    intestazione,
    larghezza_visiva, md_to_typ,
)
from build_booklet_html import VOCI_COLOPHON as VOCI_HTML  # noqa: E402
from validate_booklets import carica_schema, controlla_manifest, manifest_del_repo  # noqa: E402


class TestImmagini(unittest.TestCase):
    """`![alt](src)` deve diventare una figura, non il testo dell'alt."""

    def setUp(self):
        # La cartella temporanea sta DENTRO il repo: con `--root`, Typst vede
        # solo ciò che sta sotto la radice, e un percorso in /tmp non sarebbe
        # stampabile — il che è la ragione per cui esiste `typ_path`.
        self._tmp = tempfile.TemporaryDirectory(dir=REPO)
        self.base = Path(self._tmp.name)
        # un PNG 4x2 vero: serve la testa IHDR, non il resto
        self.png = self.base / "largo.png"
        self.png.write_bytes(
            b"\x89PNG\r\n\x1a\n" + (13).to_bytes(4, "big") + b"IHDR"
            + (400).to_bytes(4, "big") + (100).to_bytes(4, "big") + b"\x08\x06\x00\x00\x00"
        )
        self.alto = self.base / "alto.png"
        self.alto.write_bytes(
            b"\x89PNG\r\n\x1a\n" + (13).to_bytes(4, "big") + b"IHDR"
            + (100).to_bytes(4, "big") + (400).to_bytes(4, "big") + b"\x08\x06\x00\x00\x00"
        )

    def tearDown(self):
        self._tmp.cleanup()

    def test_dimensioni_png(self):
        self.assertEqual(dimensioni(self.png), (400, 100))

    def test_orizzontale_scavalca_le_colonne(self):
        out = md_to_typ("![Pianta della città](largo.png)", self.base)
        self.assertIn("#figura(", out)
        self.assertIn("larga: true", out)
        self.assertIn("didascalia: [Pianta della città]", out)

    def test_verticale_resta_in_colonna(self):
        out = md_to_typ("![Ritratto](alto.png)", self.base)
        self.assertIn("#figura(", out)
        self.assertNotIn("larga: true", out)

    def test_immagine_mancante_non_e_un_buco_silenzioso(self):
        out = md_to_typ("![Stemma Oca](non-esiste.png)", self.base)
        self.assertNotIn("!Stemma Oca", out)      # il difetto originale
        self.assertIn("immagine mancante", out)

    def test_senza_base_le_immagini_restano_fuori(self):
        """Le schede pregenerate passano dal loro lettore: lì `base` non c'è."""
        self.assertNotIn("#figura(", md_to_typ("![x](y.png)"))

    def test_immagine_in_mezzo_a_una_riga(self):
        out = md_to_typ("Testo prima ![Ritratto](alto.png) testo dopo.", self.base)
        self.assertIn("#figura(", out)
        self.assertIn("Testo prima", out)
        self.assertIn("testo dopo.", out)


class TestEnfasi(unittest.TestCase):
    """I due casi per cui due booklet della campagna non compilavano."""

    def test_grassetto_attaccato_a_una_barra(self):
        self.assertEqual(inline("(il **Seggio**/Deputazione)"),
                         "(il #strong[Seggio]/Deputazione)")

    def test_corsivo_che_contiene_grassetto(self):
        self.assertEqual(inline("*Il peso **(nota.)***"),
                         "#emph[Il peso #strong[(nota.)]]")

    def test_asterisco_che_non_e_enfasi(self):
        self.assertEqual(inline("3 * 4 caselle"), "3 \\* 4 caselle")

    def test_segno_di_struttura_a_inizio_cella_resta_testo(self):
        """«= suo nipote» in una cella di DEF-4 diventava un titolo in Typst."""
        self.assertEqual(inline("= suo nipote"), "\\= suo nipote")
        self.assertEqual(inline("/ 8"), "\\/ 8")
        self.assertEqual(inline("- nota"), "\\- nota")
        # ma un segno attaccato a un numero non è struttura, e resta com'è
        self.assertEqual(inline("+2 alla CA"), "+2 alla CA")
        self.assertEqual(inline("-5 pf"), "-5 pf")

    def test_enfasi_mai_chiusa_non_esce_dal_paragrafo(self):
        """Un master con un asterisco dispari non deve mangiarsi il resto."""
        self.assertTrue(inline("**aperto e mai chiuso").endswith("]"))


class TestDirettiveDiPagina(unittest.TestCase):
    """Appendici e mappe su pagine A4 a una colonna (richiesta DM 2026-09-25)."""

    def test_un_commento_qualsiasi_non_finisce_nel_pdf(self):
        typ = md_to_typ("Testo.\n\n<!-- nota privata\nsu due righe -->\n\nAltro.")
        self.assertNotIn("<!--", typ)
        self.assertNotIn("nota privata", typ)

    def test_pagina_a_una_colonna_si_apre_e_si_chiude(self):
        typ = md_to_typ("<!-- pagina: una-colonna -->\n\n## Appendice\n\nDati.\n\n<!-- /pagina -->\n")
        self.assertIn("#page(columns: 1)[", typ)
        self.assertEqual(typ.count("#page(columns: 1)["), typ.count("\n]"))

    def test_pagina_lasciata_aperta_si_chiude_col_capitolo(self):
        typ = md_to_typ("<!-- pagina: una-colonna -->\n\nDati.")
        self.assertTrue(typ.rstrip().endswith("]"))

    def test_una_mappa_su_pagina_a_una_colonna_non_supera_il_foglio(self):
        """M7-C, verticale, a tutta larghezza usciva dal bordo alto del foglio."""
        with tempfile.TemporaryDirectory(dir=REPO) as d:   # dentro il repo: --root
            (Path(d) / "m.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" width="820" height="1261"/>')
            dentro = md_to_typ("<!-- pagina: una-colonna -->\n\n![M](m.svg)\n\n<!-- /pagina -->", base=Path(d))
            fuori = md_to_typ("![M](m.svg)", base=Path(d))
        self.assertIn("pagina: true", dentro)
        self.assertNotIn("pagina: true", fuori)

    def test_nuova_pagina_non_viene_assorbita_dal_paragrafo(self):
        typ = md_to_typ("Una riga.\n<!-- nuova-pagina -->\nUn'altra.")
        self.assertIn("#pagebreak(weak: true)", typ.split("\n"))


class TestMappeCheNonEntranoInColonna(unittest.TestCase):
    """Una mappa o sta in colonna o va su una pagina A4 (richiesta DM 2026-09-25).

    Nel volume della serata le due mappe della Sala di `DEF-2`, larghe 72
    celle, erano stampate nel corpo a due colonne e andavano a capo a brandelli.
    """

    LARGA = "```\n" + "═" * 72 + "\n NORD ▼ [P1 → Stanza della Corona]\n```"
    STRETTA = "```\nA B C\n⬛ ⬛ ⬛\n```"

    def test_un_emoji_vale_due_celle_e_mezza(self):
        self.assertEqual(larghezza_visiva("ab"), 2)
        self.assertEqual(larghezza_visiva("⬛"), 2.5)
        self.assertEqual(larghezza_visiva("🗿\ufe0f"), 2.5)   # il selettore di variante non occupa

    def test_la_griglia_stretta_resta_in_colonna(self):
        typ = md_to_typ("### Mappa\n\n" + self.STRETTA)
        self.assertNotIn("#page(", typ)
        self.assertIn("#griglia(", typ)

    def test_la_griglia_larga_va_su_a4_col_suo_titolo(self):
        typ = md_to_typ("Prima.\n\n### Mappa S-1\n\n> Nota.\n\n" + self.LARGA + "\n\nDopo.")
        righe = typ.split("\n")
        pagina = righe.index("#page(columns: 1)[")
        titolo = next(i for i, r in enumerate(righe) if r.startswith("=== Mappa"))
        griglia = next(i for i, r in enumerate(righe) if r.startswith("#griglia("))
        self.assertLess(pagina, titolo, "il titolo non resta in fondo alla colonna")
        self.assertLess(titolo, griglia)
        self.assertLess(righe.index("Prima."), pagina)

    def test_la_pagina_automatica_si_chiude_alla_sezione_dopo(self):
        typ = md_to_typ("## Mappe\n\n" + self.LARGA + "\n\n### S-2\n\n" + self.LARGA
                        + "\n\n## Altro\n\nTesto.")
        righe = typ.split("\n")
        self.assertEqual(typ.count("#page(columns: 1)["), 1, "le due mappe della sezione stanno insieme")
        self.assertLess(righe.index("]"), next(i for i, r in enumerate(righe) if r.startswith("== Altro")))

    def test_dentro_una_pagina_esplicita_non_se_ne_apre_un_altra(self):
        typ = md_to_typ("<!-- pagina: una-colonna -->\n\n" + self.LARGA + "\n\n<!-- /pagina -->")
        self.assertEqual(typ.count("#page(columns: 1)["), 1)

    def test_la_griglia_non_va_mai_a_capo_nel_tema(self):
        """Il corpo scende finché la riga più larga ci sta; mai il raw nudo."""
        tema = (REPO / "scripts" / "typst" / "tema-rumblingstone.typ").read_text(encoding="utf-8")
        self.assertIn("#let griglia(", tema)
        self.assertNotIn("#raw(", md_to_typ(self.LARGA))

    def test_una_mappa_immagine_fuori_pagina_va_su_a4(self):
        with tempfile.TemporaryDirectory(dir=REPO) as d:
            (Path(d) / "x_map01_sala.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" width="820" height="1261"/>')
            typ = md_to_typ("### Sala\n\n![La Sala](x_map01_sala.svg)", base=Path(d))
        self.assertIn("#page(columns: 1)[", typ)
        self.assertIn("pagina: true", typ)

    def test_riconosce_le_mappe(self):
        self.assertTrue(e_mappa("", "Mappe/rendered/M7C_map01_tenda.svg"))
        self.assertTrue(e_mappa("La mappa della Sala", "x.svg"))
        self.assertFalse(e_mappa("Hella", "PG/Immagini/web/Hella.jpg"))

    def test_un_comando_largo_non_apre_una_pagina(self):
        """Una riga di `bash` in un elenco del Drappo apriva una pagina A4 intera."""
        cmd = "```bash\npython3 scripts/export_booklet_typst.py STANDALONE/homebrew/X.json\n```"
        typ = md_to_typ("### Cosa stampare\n\n" + cmd)
        self.assertNotIn("#page(", typ)
        self.assertNotIn("larga: true", typ)

    def test_uno_schema_larghissimo_scavalca_le_colonne(self):
        schema = "```\n" + "─" * 90 + "\n```"
        typ = md_to_typ("### Struttura\n\n" + schema)
        self.assertNotIn("#page(", typ)
        self.assertIn("larga: true", typ)

    def test_riconosce_una_griglia_dalla_forma(self):
        self.assertTrue(e_griglia_mappa(["@north S", "01 ⬛ ⬛"]))
        self.assertTrue(e_griglia_mappa(["⬛ ⬛ ⬛ ⬛ ⬛"] * 3))
        self.assertTrue(e_griglia_mappa(["x"], "MAPPA T-1 — Piano della Terra"))
        self.assertFalse(e_griglia_mappa(["python3 scripts/dm.py volume"], "Rigenerare"))

    def test_ogni_capitolo_si_apre_su_una_pagina_sua(self):
        """Il titolo è un float: senza salto di pagina saliva sopra la coda del
        capitolo di prima. Nel fascicolo dei giocatori gli echi privati di
        Thorik e di Tordek finivano sullo stesso foglio (2026-09-25)."""
        tema = (REPO / "scripts" / "typst" / "tema-rumblingstone.typ").read_text(encoding="utf-8")
        apertura = tema.split("#let capitolo-aperto(", 1)[1].split("\n}\n", 1)[0]
        self.assertIn("pagebreak(weak: true)", apertura)
        self.assertLess(apertura.index("pagebreak("), apertura.index("place("))

    def test_un_ritratto_verticale_non_supera_i_16_cm(self):
        tema = (REPO / "scripts" / "typst" / "tema-rumblingstone.typ").read_text(encoding="utf-8")
        figura = tema.split("#let figura(percorso, didascalia:", 1)[1].split("\n}\n", 1)[0]
        self.assertIn("alta > 16cm", figura)

    def test_la_soglia_e_quella_misurata(self):
        """217,7 pt di colonna / 4,5 pt di cella Inconsolata a 9 pt."""
        self.assertEqual(CELLE_COLONNA, 48)


class TestCapolettera(unittest.TestCase):

    def test_solo_su_un_paragrafo_abbastanza_lungo(self):
        lungo = "Nel mezzo del cammino di nostra vita mi ritrovai per una selva " \
                "oscura, ché la diritta via era smarrita, e non è cosa da dire."
        self.assertIn("#capolettera(\"N\"", md_to_typ(lungo, capolettera=True))

    def test_un_cappello_di_due_righe_resta_com_e(self):
        self.assertNotIn("#capolettera(", md_to_typ("Due righe soltanto.", capolettera=True))


class TestFormato(unittest.TestCase):
    """A5 è il libretto: una colonna, corpo 9.6 pt.

    Sta accanto all'imposizione (ADR-0027), non al posto suo: `pdfcpu booklet`
    su un volume A4 mette due pagine per foglio e scala tutto al 71%, cioè
    10.2 pt diventano ~7.2. Comporre in A5 e poi imporre tiene il corpo dove si
    legge.
    """

    def test_a4_non_dichiara_niente(self):
        """Il default non finisce nel sorgente: un artefatto pulito si legge."""
        self.assertNotIn("formato:", "\n".join(intestazione({"title": "x"})))

    def test_a5_dichiarato_al_tema(self):
        self.assertIn('formato: "a5"',
                      "\n".join(intestazione({"title": "x"}, formato="a5")))

    def test_il_tema_conosce_il_parametro(self):
        """Anti-drift: se qualcuno rinomina `formato` nel tema, qui si vede."""
        tema = (REPO / "scripts" / "typst" / "tema-rumblingstone.typ").read_text(encoding="utf-8")
        self.assertIn('formato: "a4"', tema)
        self.assertIn('formato == "a5"', tema)


class TestManifestDelRepo(unittest.TestCase):
    """Il gate, sui manifest veri: è il test che tiene onesta la parità."""

    @classmethod
    def setUpClass(cls):
        cls.schema = carica_schema()
        cls.elenco = manifest_del_repo()

    def test_ci_sono_manifest_da_controllare(self):
        self.assertGreaterEqual(len(self.elenco), 5)

    def test_tutti_i_manifest_del_repo_sono_validi(self):
        for m in self.elenco:
            with self.subTest(manifest=m.name):
                errori, _ = controlla_manifest(m, self.schema)
                self.assertEqual(errori, [])

    def test_una_chiave_inventata_viene_rifiutata(self):
        with tempfile.TemporaryDirectory() as d:
            cap = Path(d) / "c.md"
            cap.write_text("# c\n\ntesto\n", encoding="utf-8")
            mp = Path(d) / "X.manifest.json"
            mp.write_text(json.dumps({"title": "x", "chapters": [{"file": "c.md"}],
                                      "cover_imagee": "z.png"}), encoding="utf-8")
            errori, _ = controlla_manifest(mp, self.schema)
            self.assertTrue(any("cover_imagee" in e for e in errori))

    def test_un_master_mancante_viene_rifiutato(self):
        with tempfile.TemporaryDirectory() as d:
            mp = Path(d) / "X.manifest.json"
            mp.write_text(json.dumps({"title": "x", "chapters": [{"file": "manca.md"}]}),
                          encoding="utf-8")
            errori, _ = controlla_manifest(mp, self.schema)
            self.assertTrue(any("master mancante" in e for e in errori))


COLOPHON_PIENO = {
    "edizione": "Edizione da tavolo",
    "versione": "v3",
    "data": "2026-09-02",
    "autori": "Il DM",
    "basato_su": "SRD 3.5 · OGL 1.0a",
    "licenza": "Materiale del DM, uso privato.",
    "nota": "Grazie al tavolo.",
}


class TestColophon(unittest.TestCase):
    """La pagina dei crediti: prima del 2026-09-02 i volumi uscivano anonimi."""

    def test_senza_la_chiave_il_volume_esce_come_prima(self):
        # Retrocompatibilità: i dieci manifest che non dichiarano un colophon
        # non devono cambiare di una virgola.
        self.assertIsNone(crediti_typ({"title": "x"}))
        self.assertEqual(colophon_html({"title": "x"}, "piede"), "")

    def test_un_colophon_vuoto_non_produce_una_pagina_bianca(self):
        self.assertIsNone(crediti_typ({"colophon": {}}))
        self.assertEqual(colophon_html({"colophon": {}}, "piede"), "")

    def test_le_voci_dichiarate_finiscono_nel_typst(self):
        typ = crediti_typ({"colophon": COLOPHON_PIENO})
        self.assertTrue(typ.startswith("colophon(voci: ("))
        for valore in ("Edizione da tavolo", "v3", "2026-09-02", "Il DM", "SRD 3.5"):
            self.assertIn(valore, typ)
        self.assertIn('licenza: "Materiale del DM, uso privato."', typ)

    def test_una_voce_sola_resta_una_tupla_valida(self):
        # `(("a", "b"))` in Typst non è un array di uno: è una parentesi.
        # Senza la virgola finale il volume non compila.
        typ = crediti_typ({"colophon": {"versione": "v1"}})
        self.assertIn('(("Versione", "v1"),)', typ)

    def test_le_voci_assenti_non_lasciano_righe_vuote(self):
        typ = crediti_typ({"colophon": {"versione": "v1", "data": "2026-01-01"}})
        self.assertNotIn('""', typ.split("licenza:")[0])

    def test_la_data_non_viene_mai_dedotta(self):
        # Un PDF che prende la data dall'orologio cambia a ogni compilazione e
        # smette di essere byte-identico: il gate di stampa verifica il contrario.
        typ = crediti_typ({"colophon": {"versione": "v1"}})
        self.assertNotIn("Data", typ)

    def test_le_due_catene_ordinano_le_voci_allo_stesso_modo(self):
        # È il test che conta: due catene che ordinano diversamente i crediti
        # producono due edizioni diverse dello stesso volume.
        self.assertEqual(VOCI_COLOPHON, VOCI_HTML)

    def test_la_catena_html_emette_le_stesse_voci(self):
        out = colophon_html({"colophon": COLOPHON_PIENO}, "piede")
        for valore in ("Edizione da tavolo", "v3", "2026-09-02", "Il DM", "SRD 3.5"):
            self.assertIn(valore, out)
        self.assertIn("Materiale del DM, uso privato.", out)
        self.assertIn("Grazie al tavolo.", out)

    def test_il_testo_del_colophon_viene_escapato(self):
        out = colophon_html({"colophon": {"nota": "<script>x</script>"}}, "p")
        self.assertNotIn("<script>", out)

    def test_una_chiave_inventata_dentro_il_colophon_viene_rifiutata(self):
        # Senza la ricorsione sugli oggetti annidati questo refuso passerebbe
        # in silenzio — cioè il difetto che lo schema esiste per impedire.
        schema = carica_schema()
        with tempfile.TemporaryDirectory() as d:
            cap = Path(d) / "c.md"
            cap.write_text("# c\n\ntesto\n", encoding="utf-8")
            mp = Path(d) / "X.manifest.json"
            mp.write_text(json.dumps({"title": "x", "chapters": [{"file": "c.md"}],
                                      "colophon": {"versionee": "v1"}}), encoding="utf-8")
            errori, _ = controlla_manifest(mp, schema)
            self.assertTrue(any("versionee" in e for e in errori), errori)

    def test_un_colophon_valido_passa_il_gate(self):
        schema = carica_schema()
        with tempfile.TemporaryDirectory() as d:
            cap = Path(d) / "c.md"
            cap.write_text("# c\n\ntesto\n", encoding="utf-8")
            mp = Path(d) / "X.manifest.json"
            mp.write_text(json.dumps({"title": "x", "chapters": [{"file": "c.md"}],
                                      "colophon": COLOPHON_PIENO}), encoding="utf-8")
            errori, _ = controlla_manifest(mp, schema)
            self.assertEqual(errori, [])


if __name__ == "__main__":
    unittest.main()
