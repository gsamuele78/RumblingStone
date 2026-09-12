"""La legenda ha una casa sola — `legend/single-source` (ADR-0048, 2026-09-12).

Il difetto non era un errore presente: al momento della migrazione i cinque
posti in cui viveva la legenda — `SYMBOLS` nel renderer e i quattro `set` nei
consumatori — **coincidevano tutti**. Era che niente impediva il prossimo.

🔴 **E il prossimo era gia' arrivato due volte.** `⛺` (tenda) non era in
`WALL_SYMS` e non bloccava la vista in Foundry mentre lo faceva nell'SVG:
ADR-0042. `⛰` (montagne) idem su 2.423 celle: ADR-0043. Due ADR, due giri di
test, due mesi — per due sintomi della **stessa** causa, perche' la fonte unica
stava in una PR chiusa dal 26 luglio.

Questo file e' il cancello che quella decisione dichiarava **assente**:

- `TestNessunConsumatoreHaUnSetProprio` e' `legend/single-source`. Analizza
  l'AST dei cinque consumatori e boccia **qualunque** insieme di emoji
  dichiarato a livello di modulo. E' l'unico dei test qui che impedisce il
  difetto *futuro*; tutti gli altri verificano quello passato.
- `TestLaMigrazioneNonHaCambiatoNiente` e' la prova che il refactor e' stato
  a costo zero sugli artefatti — il criterio d'uscita di ADR-0048 §4.

🔎 **E il gate ha morso al primo uso vero**, come gia' `decisioni_dm.py`: ha
trovato in `render_map_blender.py` **tre tabelle** (`ALTEZZE`, `PIATTI`,
`TEXTURE`) che nessuna misura di questo lotto aveva contato — l'ADR ne
dichiarava quattro, erano sette. Una portava un commento fossile, «edificio,
tenda, dais» accanto a ⬛: il significato di **prima** di ADR-0042, sopravvissuto
otto giorni dopo la decisione che lo aveva abolito.

⚠️ **Il limite, dichiarato.** Il gate vede un set **letterale**. Chi costruisse
il proprio insieme a runtime (`{s for s in ... if ...}`) gli sfuggirebbe. E'
la stessa forma di limite di ADR-0043 — un marcatore dimenticato resta
invisibile — e vale la pena saperlo invece di crederlo chiuso.
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from dmcore import legenda  # noqa: E402

CONSUMATORI = ("render_map_svg.py", "export_uvtt.py", "import_ultraclear.py",
               "compile_map_json.py", "render_map_blender.py")


def _e_emoji(testo: str) -> bool:
    """Un simbolo di legenda: un pittogramma, non una parola accentata."""
    return any(ord(c) >= 0x2190 for c in testo) and len(testo) <= 4


def insiemi_di_emoji_cablati(sorgente: str) -> list[str]:
    """I nomi assegnati, a livello di modulo, a un set/dict/lista di emoji."""
    colpevoli = []
    for nodo in ast.parse(sorgente).body:
        if not isinstance(nodo, (ast.Assign, ast.AnnAssign)):
            continue
        valore = nodo.value
        if isinstance(valore, ast.Set):
            elementi = valore.elts
        elif isinstance(valore, ast.Dict):
            elementi = [k for k in valore.keys if k is not None]
        elif isinstance(valore, (ast.List, ast.Tuple)):
            elementi = valore.elts
        else:
            continue
        stringhe = [e.value for e in elementi
                    if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        if stringhe and all(_e_emoji(s) for s in stringhe):
            bersagli = [nodo.target] if isinstance(nodo, ast.AnnAssign) else nodo.targets
            for t in bersagli:
                if isinstance(t, ast.Name):
                    colpevoli.append(t.id)
    return colpevoli


class TestNessunConsumatoreHaUnSetProprio(unittest.TestCase):
    """`legend/single-source` — il criterio d'accettazione del lotto 1.1."""

    def test_i_cinque_consumatori_sono_puliti(self):
        for nome in CONSUMATORI:
            sorgente = (ROOT / "scripts" / nome).read_text(encoding="utf-8")
            colpevoli = insiemi_di_emoji_cablati(sorgente)
            self.assertEqual(
                colpevoli, [],
                f"{nome} dichiara una legenda propria ({colpevoli}). La fonte e' "
                f"scripts/legend.yaml: si legge da dmcore.legenda. Prima di "
                f"ADR-0048 questo e' costato due ADR (0042, 0043) per due "
                f"sintomi della stessa causa.")

    def test_il_gate_morde(self):
        """Provato a rovescio: senza questo, il test sopra non prova niente."""
        ricaduta = 'WALL_SYMS = {"🏰", "⬛", "⛰"}\n'
        self.assertEqual(insiemi_di_emoji_cablati(ricaduta), ["WALL_SYMS"])
        con_valori = 'LIGHT_SYMS = {"🏮": (6.0, "ffd9a0"), "🔥": (5.0, "ffb37a")}\n'
        self.assertEqual(insiemi_di_emoji_cablati(con_valori), ["LIGHT_SYMS"])

    def test_non_boccia_cio_che_non_e_una_legenda(self):
        """L'altra meta': un gate che boccia troppo verrebbe spento al primo giro."""
        for innocente in (
            'TROOP_WORDS = ("nani", "nano", "cantitrice")\n',
            'SEV_ORDER = {"ERROR": 0, "WARN": 1}\n',
            'Z_ORDER = ["t_grass", "t_veg", "t_wall"]\n',
            'HEAVY_PATS = {"t_wall", "t_struct"}\n',
        ):
            self.assertEqual(insiemi_di_emoji_cablati(innocente), [], innocente)


class TestLaFonteEUnaSola(unittest.TestCase):
    def test_yaml_e_json_sono_in_sincronia(self):
        esito = subprocess.run([sys.executable, "scripts/build_legend.py", "--check"],
                               cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stderr)

    def test_la_pagina_della_skill_e_generata(self):
        esito = subprocess.run(
            [sys.executable, "scripts/build_legenda_skill.py", "--check"],
            cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stderr)

    def test_ogni_simbolo_dichiarato_ha_un_rendering(self):
        for sim, spec in legenda.simboli().items():
            self.assertIn(spec["mode"], ("fill", "unit", "icon"), sim)
            self.assertTrue(spec["fill"].startswith("#"), sim)

    def test_i_set_di_funzione_sono_sottoinsiemi_dei_simboli(self):
        """Un orfano vorrebbe dire che la fonte unica non e' unica."""
        simboli = set(legenda.simboli())
        for nome, insieme in (("muri", legenda.muri()), ("porte", legenda.porte()),
                              ("pericoli", legenda.pericoli()),
                              ("luci", set(legenda.luci()))):
            self.assertEqual(set(insieme) - simboli, set(), nome)

    def test_niente_numeri_di_gioco_nella_legenda(self):
        """ADR-0048 §5: «+4 CA» e «20%» vivono nei profili, non qui.

        ⚠️ Il controllo e' sui **campi funzione**, non sulle etichette: 9
        etichette portano ancora la funzione in prosa («copertura +4 CA»), ed
        e' un debito noto che questo lotto non chiude — la ratifica della spec
        funzionale e' la decisione D1 di PIANO-VENDIBILITA §8.
        """
        dati = json.loads((ROOT / "scripts" / "legend.json").read_text(encoding="utf-8"))
        ammessi = {"wall", "door", "light", "hazard"}
        for sim, voce in dati["symbols"].items():
            self.assertEqual(set(voce.get("function", {})) - ammessi, set(), sim)


class TestLaMigrazioneNonHaCambiatoNiente(unittest.TestCase):
    """Il criterio d'uscita di ADR-0048 §4: nessuna regressione visiva."""

    CONGELATI = {
        "muri": {"🏰", "⬛", "⛺", "⛰", "🟪", "🗼", "🏛", "🗿"},
        "porte": {"🚪"},
        "pericoli": {"🔥", "💥", "💀", "🕳", "⚡", "❄", "🕸"},
        "pesanti": {"t_wall", "t_struct", "t_pillar", "t_mountain"},
        "piatti": {"🚪", "⬇", "🎯", "⭐", "✨", "⚔", "🖼"},
    }

    def test_i_set_valgono_esattamente_quel_che_valevano(self):
        self.assertEqual(set(legenda.muri()), self.CONGELATI["muri"])
        self.assertEqual(set(legenda.porte()), self.CONGELATI["porte"])
        self.assertEqual(set(legenda.pericoli()), self.CONGELATI["pericoli"])
        self.assertEqual(set(legenda.pattern_pesanti()), self.CONGELATI["pesanti"])

    def test_le_tre_tabelle_del_blender_valgono_quel_che_valevano(self):
        """Le ha trovate il gate, non l'inventario: non erano in nessuna misura."""
        self.assertEqual(set(legenda.piatti()), self.CONGELATI["piatti"])
        self.assertEqual(len(legenda.altezze()), 29)
        self.assertEqual(len(legenda.texture()), 15)
        self.assertEqual(legenda.altezze()["🗼"], 9.0, "la torre")
        self.assertEqual(legenda.altezze()["🕳"], -2.5, "la voragine e' uno scavo")

    def test_il_buco_di_adr_0042_nel_blender_resta_dichiarato(self):
        """⛺ e 🔳 non hanno un'altezza propria: si estrudono al default.

        🐛 Terzo sintomo della causa che ADR-0048 chiude, e il primo trovato
        **da un gate** invece che da un bug al tavolo. Non si corregge qui
        perche' l'altezza di una tenda e' contenuto, non refactoring:
        decisione D2 di PIANO-VENDIBILITA §8. Questo test esiste perche' il
        giorno in cui qualcuno la decide, sia lui a togliere il test — non il
        buco a sopravvivere in silenzio.
        """
        for sim in ("⛺", "🔳"):
            self.assertNotIn(sim, legenda.altezze(), sim)

    def test_i_63_simboli_ci_sono_tutti(self):
        """62 era il numero della spec di luglio; 🔳 e' entrato con ADR-0042."""
        self.assertEqual(len(legenda.simboli()), 63)

    def test_i_consumatori_vedono_gli_stessi_valori(self):
        import export_uvtt as eu
        import import_ultraclear as iu
        import render_map_svg as rms
        self.assertEqual(rms.SYMBOLS, legenda.simboli())
        self.assertEqual(rms.HEAVY_PATS, set(legenda.pattern_pesanti()))
        self.assertEqual(eu.WALL_SYMS, set(legenda.muri()))
        self.assertEqual(iu.HAZARD_SYMS, set(legenda.pericoli()))
        import render_map_blender as rmb
        self.assertEqual(rmb.ALTEZZE, legenda.altezze())
        self.assertEqual(rmb.PIATTI, set(legenda.piatti()))
        self.assertEqual(rmb.TEXTURE, legenda.texture())

    def test_la_voragine_non_e_una_sorgente_di_luce(self):
        """🕳 stava fra le luci con raggio 0.0, e l'export lo scartava.

        Toglierlo dalla fonte non cambia un byte d'uscita, e la guardia
        `if rng <= 0` resta al suo posto per chi dichiarasse una luce spenta.
        """
        self.assertNotIn("🕳", legenda.luci())
        self.assertIn("if rng <= 0", (ROOT / "scripts" / "export_uvtt.py")
                      .read_text(encoding="utf-8"))
        self.assertIn("🕳", legenda.pericoli(), "resta un pericolo, ed e' quel che e'")


if __name__ == "__main__":
    unittest.main()
