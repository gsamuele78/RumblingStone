#!/usr/bin/env python3
"""eval_componenti.py — un runner solo per le misure di tutti i componenti (lotto E1, ADR-0155).

Legge il registro ``plans/eval/componenti.json``, esegue il comando di ogni
voce, prende le metriche dal JSON che il comando stampa e le confronta con il
tetto. È la forma del registro dei task di lm-eval-harness e di OpenAI evals:
la voce dichiara comando, set, metriche e tetto, il runner è uno. Un componente
nuovo entra con la sua voce, non con un passo CI e un cricchetto suoi.

Una voce ha ``id``, ``componente`` (il file), ``set`` (il percorso del set),
``comando`` (lista argv eseguita senza shell dalla radice del repo, con i
segnaposto ``{python}``, l'interprete di questo runner, e ``{set}``),
``metriche`` (nome → ``{"percorso": "a.b.c", "verso": "alto"|"basso"}``: il
punto nel JSON d'uscita e se più alto o più basso è meglio), ``tetto`` (nome →
valore), ``canale`` (unstable, testing, stable: ADR-0099) e ``adr``.

**Il tetto ha una fonte sola.** Se il set lo scrive già (``agenti-oro.json``
in ``tetto``, ``casi.json`` in ``tetto_omissioni`` e ``tetto_violazioni``), la
voce non lo copia: scrive ``{"dal_set": "tetto.giusti"}`` e il runner lo legge
da lì. Così ``raccogli_casi_agenti.py applica``, che rimette il tetto nel set,
non deve sapere che il registro esiste, e un tetto non può dire due numeri
diversi in due file. Un tetto in chiaro (un intero, o una frazione «a/b» come
stringa) si scrive solo quando il set non lo porta: oggi i conflitti fra le L1,
che ``instradamento_skill.py`` vuole a zero nel codice.

**Confronti esatti.** Valori e tetti sono interi o frazioni «a/b», letti con
``fractions.Fraction``; un float o un booleano è una voce malformata, perché
un cancello non confronta float (come in ``eval_metriche``). Esiti: «al tetto»,
«sopra» (meglio del tetto: si alza a mano nel set), «sotto» (regressione).

**Il cricchetto contro il tetto abbassato a mano.** Con ``--rispetto-a REF``
(default ``origin/main``, se esiste) ogni tetto si confronta con quello che
aveva dove HEAD si stacca da REF (``git merge-base REF HEAD``, poi
``git show``): se è peggiorato esce 1, salvo che la nota del tetto nel set
porti una riga di rimessa di ``raccogli_casi_agenti.py applica`` diversa da
quella su REF (è cambiato il set, non il componente). Se REF o l'antenato
comune non ci sono, come in un clone shallow, lo dice e quel controllo passa.

Codici d'uscita: 0 tutto al tetto o sopra; 1 una metrica sotto il tetto, o un
tetto peggiorato rispetto a REF; 2 un comando fallito, un'uscita che non è JSON
o non ha il percorso, una voce malformata (il 2 vince sull'1).

    python3 scripts/eval_componenti.py                     # tutte le voci, la tabella
    python3 scripts/eval_componenti.py --json              # il rapporto macchina
    python3 scripts/eval_componenti.py --solo instradamento_skill
    python3 scripts/eval_componenti.py --check-registro    # la forma, senza eseguire
    python3 scripts/eval_componenti.py --rispetto-a origin/main

Solo stdlib: le librerie (scikit-learn per ``instradamento_agenti``) le
importano i componenti, nei loro processi. Niente rete, niente modelli.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
REGISTRO = RADICE / "plans" / "eval" / "componenti.json"
CANALI = ("unstable", "testing", "stable")
VERSI = ("alto", "basso")
CAMPI = ("id", "componente", "set", "comando", "metriche", "tetto", "canale", "adr")
REF_DEFAULT = "origin/main"
TIMEOUT = 600
#: La riga che ``raccogli_casi_agenti.py applica`` aggiunge alla nota del tetto
#: quando lo rimette (``_RIMESSA`` là; un test controlla che le due combacino).
MARCA_RIMESSA = "Ultima rimessa (raccogli_casi_agenti.py applica):"


class Malformata(ValueError):
    """Una voce o un'uscita che il runner non sa leggere: esce 2."""


def carica_registro(percorso: Path = REGISTRO) -> dict:
    return json.loads(Path(percorso).read_text(encoding="utf-8"))


def numero(v) -> Fraction:
    """Un intero o una frazione «a/b» (anche «4»): mai un float o un booleano."""
    if isinstance(v, bool) or isinstance(v, float):
        raise ValueError(f"{v!r} non si confronta esatto: scrivilo intero o «a/b»")
    if isinstance(v, int):
        return Fraction(v)
    if isinstance(v, str):
        try:
            return Fraction(v.strip())
        except (ValueError, ZeroDivisionError) as e:
            raise ValueError(f"{v!r} non è un intero né una frazione «a/b»") from e
    raise ValueError(f"{v!r} non è un intero né una frazione «a/b»")


def confronta(valore: Fraction, tetto: Fraction, verso: str) -> str:
    """«al tetto», «sopra» (meglio) o «sotto» (regressione), secondo il verso."""
    if valore == tetto:
        return "al tetto"
    meglio = valore > tetto if verso == "alto" else valore < tetto
    return "sopra" if meglio else "sotto"


def _punto(dati, percorso: str):
    nodo = dati
    for chiave in percorso.split("."):
        if not isinstance(nodo, dict) or chiave not in nodo:
            raise KeyError(percorso)
        nodo = nodo[chiave]
    return nodo


def _leggi_json(testo: str, dove: str) -> dict:
    try:
        return json.loads(testo)
    except json.JSONDecodeError as e:
        raise Malformata(f"{dove}: non è JSON ({e})") from e


def _tetto_da(spec, set_dati: "dict | None", dove: str) -> Fraction:
    if isinstance(spec, dict):
        if set(spec) != {"dal_set"} or not isinstance(spec["dal_set"], str):
            raise Malformata(f"{dove}: un tetto oggetto è solo {{\"dal_set\": \"percorso\"}}")
        if set_dati is None:
            raise Malformata(f"{dove}: il set non si legge")
        try:
            return numero(_punto(set_dati, spec["dal_set"]))
        except KeyError:
            raise Malformata(f"{dove}: {spec['dal_set']} non c'è nel set") from None
        except ValueError as e:
            raise Malformata(f"{dove}: {e}") from None
    try:
        return numero(spec)
    except ValueError as e:
        raise Malformata(f"{dove}: {e}") from None


def tetti(voce: dict, radice: Path = RADICE) -> "dict[str, Fraction]":
    """I tetti della voce risolti: quelli ``dal_set`` letti dal set su disco."""
    set_dati = _leggi_set(voce, radice)
    return {nome: _tetto_da(spec, set_dati, f"{voce['id']}: tetto {nome}")
            for nome, spec in voce["tetto"].items()}


def _leggi_set(voce: dict, radice: Path) -> "dict | None":
    p = radice / voce["set"]
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def controlla_registro(dati: dict, radice: Path = RADICE) -> "list[str]":
    """Gli errori di forma del registro, senza eseguire niente. Vuota se è valido."""
    if not isinstance(dati, dict) or not isinstance(dati.get("componenti"), list):
        return ["il registro vuole un oggetto con la lista «componenti»"]
    err: list[str] = []
    visti: set[str] = set()
    for i, v in enumerate(dati["componenti"]):
        if not isinstance(v, dict):
            err.append(f"voce #{i}: non è un oggetto")
            continue
        vid = v.get("id", f"#{i}")
        mancano = [c for c in CAMPI if c not in v]
        if mancano:
            err.append(f"{vid}: mancano i campi {', '.join(mancano)}")
            continue
        if vid in visti:
            err.append(f"{vid}: id duplicato")
        visti.add(vid)
        if v["canale"] not in CANALI:
            err.append(f"{vid}: canale «{v['canale']}» non è fra {', '.join(CANALI)} (ADR-0099)")
        for campo in ("componente", "set"):
            if not isinstance(v[campo], str) or not (radice / v[campo]).is_file():
                err.append(f"{vid}: {campo} {v[campo]} non esiste")
        cmd = v["comando"]
        if not isinstance(cmd, list) or not cmd or not all(isinstance(a, str) for a in cmd):
            err.append(f"{vid}: comando dev'essere una lista argv di stringhe, senza shell")
        adr = v["adr"] if isinstance(v["adr"], list) else [v["adr"]]
        for a in adr:
            if not isinstance(a, str) or not list((radice / "plans" / "adr").glob(f"{a}-*.md")):
                err.append(f"{vid}: {a} non è un ADR in plans/adr/")
        metriche, tetto = v["metriche"], v["tetto"]
        if not isinstance(metriche, dict) or not metriche or not isinstance(tetto, dict):
            err.append(f"{vid}: metriche e tetto sono oggetti nome → valore, non vuoti")
            continue
        for nome, m in metriche.items():
            if not isinstance(m, dict) or not isinstance(m.get("percorso"), str):
                err.append(f"{vid}: metrica {nome} senza «percorso»")
            elif m.get("verso") not in VERSI:
                err.append(f"{vid}: metrica {nome}, verso «{m.get('verso')}» non è «alto» o «basso»")
            if nome not in tetto:
                err.append(f"{vid}: metrica {nome} senza tetto")
        for nome in tetto:
            if nome not in metriche:
                err.append(f"{vid}: tetto {nome} senza metrica")
        set_dati = _leggi_set(v, radice) if isinstance(v["set"], str) else None
        for nome, spec in tetto.items():
            try:
                _tetto_da(spec, set_dati, f"{vid}: tetto {nome}")
            except Malformata as e:
                err.append(str(e))
    return err


def argv(voce: dict, radice: Path = RADICE) -> "list[str]":
    sost = {"{python}": sys.executable, "{set}": str(radice / voce["set"])}
    return [sost.get(a, a) for a in voce["comando"]]


def esegui_voce(voce: dict, radice: Path = RADICE) -> dict:
    """Esegue una voce: le metriche col loro esito, o l'errore che vale un 2."""
    out: dict = {"id": voce["id"], "componente": voce["componente"], "canale": voce["canale"],
                 "comando": voce["comando"], "metriche": [], "errore": None}
    t0 = time.monotonic()
    try:
        limiti = tetti(voce, radice)
        p = subprocess.run(argv(voce, radice), cwd=radice, capture_output=True, text=True,
                           timeout=TIMEOUT)
        if p.returncode != 0:
            coda = (p.stderr or p.stdout).strip().splitlines()[-3:]
            raise Malformata(f"il comando è uscito {p.returncode}: {' / '.join(coda)}")
        uscita = _leggi_json(p.stdout, "l'uscita del comando")
        for nome, m in voce["metriche"].items():
            try:
                valore = numero(_punto(uscita, m["percorso"]))
            except KeyError:
                raise Malformata(f"{m['percorso']} non c'è nell'uscita del comando") from None
            except ValueError as e:
                raise Malformata(f"metrica {nome}: {e}") from None
            out["metriche"].append({"nome": nome, "valore": str(valore), "tetto": str(limiti[nome]),
                                    "verso": m["verso"],
                                    "esito": confronta(valore, limiti[nome], m["verso"])})
    except (Malformata, OSError, subprocess.TimeoutExpired) as e:
        out["errore"] = str(e)
    out["secondi"] = round(time.monotonic() - t0, 2)
    return out


def esegui(dati: dict, radice: Path = RADICE, solo: "str | None" = None) -> dict:
    """Il rapporto di tutte le voci (o di una); ``esito`` è il codice d'uscita."""
    t0 = time.monotonic()
    err = controlla_registro(dati, radice)
    if err:
        return {"esito": 2, "errori_registro": err, "voci": [], "secondi": 0.0}
    voci = [v for v in dati["componenti"] if solo is None or v["id"] == solo]
    if not voci:
        return {"esito": 2, "errori_registro": [f"nessuna voce con id «{solo}»"], "voci": [],
                "secondi": 0.0}
    righe = [esegui_voce(v, radice) for v in voci]
    esito = 2 if any(r["errore"] for r in righe) else (
        1 if any(m["esito"] == "sotto" for r in righe for m in r["metriche"]) else 0)
    return {"esito": esito, "errori_registro": [], "voci": righe,
            "secondi": round(time.monotonic() - t0, 2)}


# --------------------------------------------------------------------------- #
# Il cricchetto contro REF
# --------------------------------------------------------------------------- #
def _git_show(radice: Path, ref: str, percorso: str) -> "str | None":
    p = subprocess.run(["git", "-C", str(radice), "show", f"{ref}:{percorso}"],
                       capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def _ref_esiste(radice: Path, ref: str) -> bool:
    p = subprocess.run(["git", "-C", str(radice), "rev-parse", "--verify", "--quiet",
                        f"{ref}^{{commit}}"], capture_output=True, text=True)
    return p.returncode == 0


def _merge_base(radice: Path, ref: str) -> "str | None":
    p = subprocess.run(["git", "-C", str(radice), "merge-base", ref, "HEAD"],
                       capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 and p.stdout.strip() else None


def _nota_rimessa(set_dati: "dict | None", spec) -> str:
    """La riga di rimessa nella nota accanto al tetto (``tetto.nota`` per ``tetto.giusti``)."""
    if not isinstance(spec, dict) or not isinstance(set_dati, dict):
        return ""
    padre = spec["dal_set"].rsplit(".", 1)[0] if "." in spec["dal_set"] else ""
    try:
        nota = _punto(set_dati, f"{padre}.nota" if padre else "nota")
    except KeyError:
        return ""
    if not isinstance(nota, str) or MARCA_RIMESSA not in nota:
        return ""
    return nota[nota.index(MARCA_RIMESSA):]


def cricchetto(dati: dict, radice: Path, ref: str,
               registro_rel: str = "plans/eval/componenti.json",
               solo: "str | None" = None) -> "tuple[int, list[str]]":
    """1 se un tetto è peggiorato rispetto a REF senza la rimessa di ``applica``."""
    if not _ref_esiste(radice, ref):
        return 0, [f"○ cricchetto dei tetti: il ref {ref} non esiste qui (clone shallow?), "
                   "controllo saltato"]
    # Il confronto è col punto in cui HEAD si stacca da REF (``REF...HEAD``, come
    # documentazione_allineata): un tetto alzato su REF dopo il ramo non è un
    # abbassamento del ramo.
    base = _merge_base(radice, ref)
    if base is None:
        return 0, [f"○ cricchetto dei tetti: nessun antenato comune fra {ref} e HEAD "
                   "(clone shallow?), controllo saltato"]
    testo = _git_show(radice, base, registro_rel)
    vecchio = {v.get("id"): v for v in (json.loads(testo).get("componenti", []) if testo else [])}
    peggiori: list[str] = []
    note: list[str] = []
    for v in dati["componenti"]:
        if solo is not None and v["id"] != solo:
            continue
        set_ora = _leggi_set(v, radice)
        set_rif_testo = _git_show(radice, base, v["set"])
        set_rif = json.loads(set_rif_testo) if set_rif_testo else None
        prima_voce = vecchio.get(v["id"], v)
        for nome, spec in v["tetto"].items():
            spec_rif = prima_voce.get("tetto", {}).get(nome, spec)
            if isinstance(spec_rif, dict) and set_rif is None:
                continue  # il set non c'era su REF: niente da confrontare
            if not isinstance(spec_rif, dict) and v["id"] not in vecchio:
                continue  # voce nuova, tetto in chiaro: su REF non c'era
            try:
                ora = _tetto_da(spec, set_ora, nome)
                prima = _tetto_da(spec_rif, set_rif, nome)
            except Malformata:
                continue  # su REF quel tetto non c'era ancora
            verso = v["metriche"][nome]["verso"]
            if confronta(ora, prima, verso) != "sotto":
                continue
            rimessa = _nota_rimessa(set_ora, spec)
            if rimessa and rimessa != _nota_rimessa(set_rif, spec_rif):
                note.append(f"○ {v['id']}: tetto {nome} da {prima} a {ora}, rimesso da "
                            "raccogli_casi_agenti.py applica (è cambiato il set)")
                continue
            peggiori.append(f"{v['id']}: tetto {nome} da {prima} a {ora}")
    if peggiori:
        return 1, [f"✗ cricchetto dei tetti rispetto a {ref}: peggiorato a mano "
                   f"({'; '.join(peggiori)}). Un tetto si alza quando la misura sale e non "
                   "si abbassa; lo rimette solo raccogli_casi_agenti.py applica"] + note
    return 0, [f"✓ cricchetto dei tetti rispetto a {ref}: nessun tetto peggiorato"] + note


# --------------------------------------------------------------------------- #
# Uscita
# --------------------------------------------------------------------------- #
def _tabella(r: dict) -> str:
    righe = [("componente", "metrica", "valore", "tetto", "esito")]
    for v in r["voci"]:
        if v["errore"]:
            righe.append((v["id"], "—", "—", "—", f"errore: {v['errore']}"))
        for m in v["metriche"]:
            segno = "<=" if m["verso"] == "basso" else ">="
            righe.append((v["id"], m["nome"], m["valore"], f"{segno} {m['tetto']}", m["esito"]))
    larg = [max(len(x[i]) for x in righe) for i in range(4)]
    out = ["  ".join(c.ljust(larg[i]) if i < 4 else c for i, c in enumerate(x)) for x in righe]
    out.insert(1, "  ".join("-" * w for w in larg) + "  -----")
    return "\n".join(out)


def main(argv_: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--registro", type=Path, default=REGISTRO,
                    help="il registro (default: plans/eval/componenti.json)")
    ap.add_argument("--radice", type=Path, default=RADICE, help=argparse.SUPPRESS)
    ap.add_argument("--solo", metavar="ID", help="esegue una voce sola")
    ap.add_argument("--json", action="store_true", help="il rapporto macchina")
    ap.add_argument("--check-registro", action="store_true",
                    help="valida la forma del registro senza eseguire niente")
    ap.add_argument("--rispetto-a", metavar="REF", default=None,
                    help="il ref dei tetti di confronto (default: origin/main, se esiste)")
    a = ap.parse_args(argv_)
    radice = a.radice.resolve()
    try:
        dati = carica_registro(a.registro)
    except (OSError, json.JSONDecodeError) as e:
        print(f"✗ eval_componenti: il registro {a.registro} non si legge ({e})")
        return 2
    if a.check_registro:
        err = controlla_registro(dati, radice)
        print("\n".join(f"✗ {e}" for e in err) if err else
              f"✓ eval_componenti: registro valido, {len(dati['componenti'])} voci")
        return 2 if err else 0
    r = esegui(dati, radice, a.solo)
    try:
        rel = str(a.registro.resolve().relative_to(radice))
    except ValueError:
        rel = str(a.registro)
    ref = a.rispetto_a or REF_DEFAULT
    codice_c, msg_c = (0, [])
    if not r["errori_registro"]:
        codice_c, msg_c = cricchetto(dati, radice, ref, rel, a.solo)
    r["cricchetto"] = {"rif": ref, "esito": codice_c,
                       "messaggi": msg_c}
    codice = max(r["esito"], codice_c)
    r["esito"] = codice
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return codice
    if r["errori_registro"]:
        print("\n".join(f"✗ {e}" for e in r["errori_registro"]))
        return codice
    print(_tabella(r))
    for v in r["voci"]:
        sopra = [m["nome"] for m in v["metriche"] if m["esito"] == "sopra"]
        if sopra:
            print(f"⚠ {v['id']}: {', '.join(sopra)} meglio del tetto: il tetto si stringe a mano nel set")
    print("\n".join(msg_c))
    print(f"esito {codice} in {r['secondi']} s ({len(r['voci'])} voci)")
    return codice


if __name__ == "__main__":
    sys.exit(main())
