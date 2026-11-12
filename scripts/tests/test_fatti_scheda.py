"""`verifica_scheda --fatti`: i fatti di una scheda in JSON (ADR-0126).

Li legge il controllo di coerenza della storia per incrociare la prosa con la
scheda. Qui si prova che ogni fatto porta la riga giusta e che l'uscita non
giudica nulla."""
import json
from pathlib import Path

import verifica_scheda as V

SCHEDA = """# Sacerdote di prova

**Chierico 5** · GS 5

**Talenti:** Volontà di Ferro, Talento Che Non Esiste

**Incantesimi preparati** (LI 5):
- 1° (4+1): *benedizione* ×2, *scudo della fede* (CD 14), *comando*, *anatema*D
- 0 (5): *luce*, *guida*

- *Aura di paura (Sop)*: 9 m, Volontà CD 15.
- **Scacciare non morti (Sop)** 6/giorno.

#### Soffio di cenere (Mag)

**Tattiche** Apre con *benedizione*.
Poi resta dietro lo scudo.

**Bottino** 30 mo.

### Descrizione
Un vecchio magro.
"""


def _fatti(tmp_path: Path, testo: str = SCHEDA) -> dict:
    p = tmp_path / "prova.md"
    p.write_text(testo, encoding="utf-8")
    return V.fatti(p)


def test_talenti_con_canonico_e_riga(tmp_path):
    f = _fatti(tmp_path)
    assert [(t["nome"], t["canonico"], t["riga"]) for t in f["talenti"]] == [
        ("Volontà di Ferro", "Iron Will", 5), ("Talento Che Non Esiste", None, 5)]


def test_incantesimi_con_livello_usi_e_riga(tmp_path):
    f = _fatti(tmp_path)
    inc = {i["nome"]: i for i in f["incantesimi"]}
    assert set(inc) == {"benedizione", "scudo della fede", "comando", "anatema", "luce", "guida"}
    assert inc["benedizione"] == {"nome": "benedizione", "canonico": "Bless", "livello": 1, "usi": "4+1",
                                  "volte": 2, "riga": 8}
    assert inc["scudo della fede"]["canonico"] == "Shield of Faith"
    assert inc["luce"]["livello"] == 0 and inc["luce"]["riga"] == 9


def test_capacita_speciali_nelle_tre_grafie(tmp_path):
    f = _fatti(tmp_path)
    assert [(c["nome"], c["tipo"], c["riga"]) for c in f["capacita_speciali"]] == [
        ("Aura di paura", "Sop", 11), ("Scacciare non morti", "Sop", 12), ("Soffio di cenere", "Mag", 14)]


def test_sezioni_con_inizio_e_fine(tmp_path):
    f = _fatti(tmp_path)
    assert f["tattiche"] == [{"inizio": 16, "fine": 17}]
    assert f["descrizione"] == [{"inizio": 21, "fine": 22}]


def test_piu_sezioni_nello_stesso_file(tmp_path):
    f = _fatti(tmp_path, SCHEDA + "\n**Tattiche** Seconda creatura: carica.\n")
    assert [s["inizio"] for s in f["tattiche"]] == [16, 24]


def test_scheda_senza_nulla(tmp_path):
    f = _fatti(tmp_path, "# Vuota\n\nSolo prosa.\n")
    assert (f["talenti"], f["incantesimi"], f["capacita_speciali"], f["tattiche"], f["descrizione"]) == (
        [], [], [], [], [])


def test_cli_stampa_json_e_non_giudica(tmp_path, capsys):
    p = tmp_path / "prova.md"
    p.write_text(SCHEDA, encoding="utf-8")
    assert V.main([str(p), "--fatti", "--check"]) == 0
    dati = json.loads(capsys.readouterr().out)
    assert len(dati) == 1 and dati[0]["file"].endswith("prova.md")
    assert set(dati[0]) == {"file", "sistema", "talenti", "incantesimi", "capacita_speciali", "tattiche",
                            "descrizione"}
