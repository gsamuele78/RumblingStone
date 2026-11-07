"""dmcore.sistemi — i sistemi di gioco come plugin di dati (ADR-0111).

Il caricatore unico di `sistemi.toml` e dei plugin in `sistemi/<id>/sistema.toml`.
Risponde a tre domande e non ne fa altre:

    sistema_di(percorso)          quale sistema usa questo file
    attivi() / plugin(id)         quali sistemi ci sono e cosa dichiarano
    capacita(id, nome)            come un sistema copre una capacità, seguendo
                                  l'eredità fino in fondo

Una capacità si dichiara in quattro modi (`sistemi/catalogo.toml`): `dati`,
`codice` (ancora cablata, con il lotto che la migra), `eredita` (con il
motivo) o `non_supportato` (con il motivo). **Nessuna eredità implicita**: una
capacità non dichiarata è un buco, e `problemi()` lo dice.

Solo libreria standard (`tomllib`, Python 3.11+). Nessuna scrittura, nessuna
rete: stesso albero, stesso risultato.
"""
from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = "sistemi.toml"
CARTELLA = "sistemi"
CATALOGO = "sistemi/catalogo.toml"
MODI = ("dati", "codice", "eredita", "non_supportato")
CAMPI_PLUGIN = ("id", "nome", "tipo", "licenza", "fonti", "skill", "capacita")
TIPI_PLUGIN = ("sistema", "famiglia")


class ErroreSistemi(RuntimeError):
    """Configurazione o plugin illeggibile: lo strumento non deve indovinare."""


@dataclass(frozen=True)
class Copertura:
    """Come un sistema copre una capacità, dopo l'eredità."""

    sistema: str          # il sistema chiesto
    capacita: str
    modo: str             # dati · codice · non_supportato · mancante
    da: str               # il plugin che la dichiara davvero
    catena: tuple         # i plugin attraversati, compreso `sistema`
    voci: tuple           # i file o i file:NOME
    nota: str             # motivo o lotto

    @property
    def utilizzabile(self) -> bool:
        return self.modo in ("dati", "codice")


def _leggi(f: Path) -> dict:
    try:
        return tomllib.loads(f.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise ErroreSistemi(f"manca {f}") from e
    except tomllib.TOMLDecodeError as e:
        raise ErroreSistemi(f"{f}: TOML non valido ({e})") from e


@lru_cache(maxsize=8)
def _carica(root: Path) -> "tuple[dict, dict, dict]":
    """(configurazione, catalogo, {id: plugin}). Messo in cache per radice."""
    cfg = _leggi(root / CONFIG)
    cat = _leggi(root / CATALOGO).get("capacita", {})
    plug = {}
    for f in sorted((root / CARTELLA).glob("*/sistema.toml")):
        p = _leggi(f)
        p["_cartella"] = f.parent.name
        plug[p.get("id", f.parent.name)] = p
    return cfg, cat, plug


def carica(root: "Path | None" = None) -> "tuple[dict, dict, dict]":
    return _carica((root or ROOT).resolve())


def progetto(root: "Path | None" = None) -> dict:
    return carica(root)[0].get("progetto", {})


def attivi(root: "Path | None" = None) -> "list[str]":
    return list(progetto(root).get("attivi", []))


def predefinito(root: "Path | None" = None) -> str:
    p = progetto(root).get("predefinito")
    if not p:
        raise ErroreSistemi(f"{CONFIG}: manca [progetto] predefinito")
    return p


def plugin(id_: str, root: "Path | None" = None) -> dict:
    plug = carica(root)[2]
    if id_ not in plug:
        raise ErroreSistemi(f"nessun plugin «{id_}» in {CARTELLA}/")
    return plug[id_]


def sistema_di(percorso: "str | Path", root: "Path | None" = None) -> str:
    """Il sistema di un file: il percorso più lungo di [moduli] che lo contiene."""
    r = (root or ROOT).resolve()
    p = Path(percorso)
    if p.is_absolute():
        try:
            p = p.resolve().relative_to(r)
        except ValueError:
            pass
    parti = p.parts
    migliore, lung = None, -1
    for chiave, sis in carica(r)[0].get("moduli", {}).items():
        pezzi = Path(chiave).parts
        if parti[:len(pezzi)] == pezzi and len(pezzi) > lung:
            migliore, lung = sis, len(pezzi)
    return migliore or predefinito(r)


def capacita(id_: str, nome: str, root: "Path | None" = None) -> Copertura:
    """Come `id_` copre `nome`, seguendo `eredita`. Un ciclo è un errore."""
    _, _, plug = carica(root)
    catena, corrente = [], id_
    while True:
        if corrente in catena:
            raise ErroreSistemi(f"eredità circolare per «{nome}»: {' → '.join(catena + [corrente])}")
        catena.append(corrente)
        voce = plug.get(corrente, {}).get("capacita", {}).get(nome)
        if voce is None:
            return Copertura(id_, nome, "mancante", corrente, tuple(catena), (), "")
        modo = next((m for m in MODI if m in voce), None)
        if modo == "eredita":
            corrente = voce["eredita"]
            continue
        if modo == "dati":
            return Copertura(id_, nome, "dati", corrente, tuple(catena), tuple(voce["dati"]), voce.get("nota", ""))
        if modo == "codice":
            return Copertura(id_, nome, "codice", corrente, tuple(catena), tuple(voce["codice"]), voce.get("lotto", ""))
        if modo == "non_supportato":
            return Copertura(id_, nome, "non_supportato", corrente, tuple(catena), (), voce["non_supportato"])
        return Copertura(id_, nome, "mancante", corrente, tuple(catena), (), "modo sconosciuto")


#: La riga con cui un modulo dichiara il proprio sistema: «**Sistema:** …»,
#: «**Regole**: …», anche in un elenco o in una citazione, nelle prime righe.
DICHIARAZIONE = re.compile(
    r"^\s*(?:[-*>]\s*)?\*\*(?:Sistema|Regole|System)(?:\*\*\s*:|:\*\*)\s*(.+)$", re.I | re.M)
TESTA = 3000


def sistema_dichiarato(testo: str, root: "Path | None" = None) -> "str | None":
    """Il sistema che il testo dichiara nella riga «**Sistema:**», o None.

    Ogni plugin dice con `riconosci` come si scrive il suo nome; vince quello
    che compare per primo nella riga («D&D 3.5 (max PF1e)» è 3.5)."""
    m = DICHIARAZIONE.search(testo[:TESTA])
    if not m:
        return None
    valore, migliore = m.group(1), None
    for i, p in carica(root)[2].items():
        for pat in p.get("riconosci", []):
            t = re.search(pat, valore, re.I)
            if t and (migliore is None or t.start() < migliore[0]):
                migliore = (t.start(), i)
    return migliore[1] if migliore else None


def dichiarazioni_divergenti(root: "Path | None" = None) -> "list[tuple[str, str, str]]":
    """(file, sistema dichiarato, sistema di sistemi.toml) dove i due non coincidono.

    Si leggono i markdown delle cartelle d'arco e degli stand-alone (`0*`, `1*`),
    fuori da `homebrew/` (booklet generati) e `_ARCHIVIO/` (copie)."""
    r = (root or ROOT).resolve()
    fuori = []
    for base in sorted(list(r.glob("0*")) + list(r.glob("1*"))):
        if not base.is_dir():
            continue
        for f in sorted(base.rglob("*.md")):
            rel = f.relative_to(r)
            if "homebrew" in rel.parts or "_ARCHIVIO" in rel.parts:
                continue
            d = sistema_dichiarato(f.read_text(encoding="utf-8", errors="replace"), r)
            if d is not None:
                c = sistema_di(rel, r)
                if d != c:
                    fuori.append((str(rel), d, c))
    return fuori


def dati(id_: str, nome: str, root: "Path | None" = None) -> dict:
    """I dati TOML con cui `id_` copre `nome`, dopo l'eredità.

    Fonde i file `.toml` elencati in `dati = [...]`, nell'ordine. Se la
    capacità non è in modo «dati» è un errore: lo strumento deve usare il
    suo codice (modo «codice») o dire che il sistema non è supportato."""
    r = (root or ROOT).resolve()
    c = capacita(id_, nome, r)
    if c.modo != "dati":
        raise ErroreSistemi(f"{id_}: «{nome}» è {c.modo}" + (f" ({c.nota})" if c.nota else ""))
    out: dict = {}
    for v in c.voci:
        if v.endswith(".toml"):
            out.update(_leggi(r / v))
    return out


def termini_vietati(id_: str | None = None, root: "Path | None" = None) -> "list[tuple[str, str]]":
    """(regex, perché) dei termini vietati in un sistema (capacità termini.vietati).

    Senza `id_` vale il predefinito. È la lista sola che validate_modules e
    validate_standalone leggono (ADR-0111, L3)."""
    voci = dati(id_ or predefinito(root), "termini.vietati", root).get("vietato", [])
    return [(v["regex"], v["perche"]) for v in voci]


def abilita(id_: str | None = None, root: "Path | None" = None) -> dict:
    """{"nomi": [...], "estranee": [...]} di un sistema (capacità lessico.abilita).

    I file `.toml` danno le liste; un `.tsv` del lessico (italiano, inglese,
    tipo) aggiunge ai `nomi` le righe di tipo «abilità», in minuscolo."""
    r = (root or ROOT).resolve()
    id_ = id_ or predefinito(r)
    c = capacita(id_, "lessico.abilita", r)
    if c.modo != "dati":
        raise ErroreSistemi(f"{id_}: «lessico.abilita» è {c.modo}")
    out = {"nomi": [], "estranee": []}
    for v in c.voci:
        if v.endswith(".toml"):
            d = _leggi(r / v)
            for k in out:
                out[k] += [x for x in d.get(k, []) if x not in out[k]]
        elif v.endswith(".tsv"):
            for riga in (r / v).read_text(encoding="utf-8").splitlines():
                campi = riga.split("\t")
                if len(campi) >= 3 and campi[2] == "abilità" and not riga.startswith("#"):
                    nome = campi[0].lower()
                    if nome not in out["nomi"]:
                        out["nomi"].append(nome)
    return out


def opzione(id_: str, chiave: str, default=None, root: "Path | None" = None):
    """Un'opzione di campagna del sistema, da `[opzioni.<id>]` in sistemi.toml."""
    return carica(root)[0].get("opzioni", {}).get(id_, {}).get(chiave, default)


def skill_da_installare(root: "Path | None" = None) -> "list[str]":
    """Le skill dei sistemi attivi e di quelli di rinforzo, e delle loro famiglie (D5)."""
    pr = progetto(root)
    _, _, plug = carica(root)
    ids = list(dict.fromkeys(list(pr.get("attivi", [])) + list(pr.get("rinforzo", []))))
    fuori: "list[str]" = []
    for i in ids:
        for j in (i, plug.get(i, {}).get("famiglia")):
            for s in plug.get(j, {}).get("skill", []) if j else []:
                if s not in fuori:
                    fuori.append(s)
    return fuori


_NOME_IN_CODICE = r"^(?:def\s+{n}\b|class\s+{n}\b|{n}\s*(?::[^=\n]+)?=)"


def problemi(root: "Path | None" = None, strumenti: "dict[str, list[str]] | None" = None) -> "list[str]":
    """Tutto quello che rende la configurazione inaffidabile. Vuoto = verde.

    `strumenti` è {id strumento: [capacità chieste]}, dal manifest dei tool.
    """
    r = (root or ROOT).resolve()
    try:
        cfg, cat, plug = carica(r)
    except ErroreSistemi as e:
        return [str(e)]
    fuori = []
    pr = cfg.get("progetto", {})
    att = list(pr.get("attivi", []))
    if not att:
        fuori.append(f"{CONFIG}: [progetto] attivi è vuoto")
    if pr.get("predefinito") not in att:
        fuori.append(f"{CONFIG}: il predefinito «{pr.get('predefinito')}» non è fra gli attivi")
    for i in att + list(pr.get("rinforzo", [])):
        if i not in plug:
            fuori.append(f"{CONFIG}: «{i}» non ha un plugin in {CARTELLA}/{i}/sistema.toml")
        elif plug[i].get("tipo") != "sistema":
            fuori.append(f"{CONFIG}: «{i}» è una {plug[i].get('tipo')}, non un sistema attivabile")
    for chiave, sis in cfg.get("moduli", {}).items():
        if not (r / chiave).exists():
            fuori.append(f"{CONFIG} [moduli]: la cartella «{chiave}» non esiste")
        if sis not in att:
            fuori.append(f"{CONFIG} [moduli]: «{chiave}» usa «{sis}», che non è attivo")
    for i, p in sorted(plug.items()):
        dove = f"{CARTELLA}/{p['_cartella']}/sistema.toml"
        for campo in CAMPI_PLUGIN:
            if campo not in p:
                fuori.append(f"{dove}: manca «{campo}»")
        if p.get("id") != p["_cartella"]:
            fuori.append(f"{dove}: id «{p.get('id')}» diverso dalla cartella")
        if p.get("tipo") not in TIPI_PLUGIN:
            fuori.append(f"{dove}: tipo «{p.get('tipo')}» non è uno di {TIPI_PLUGIN}")
        fam = p.get("famiglia")
        if fam and plug.get(fam, {}).get("tipo") != "famiglia":
            fuori.append(f"{dove}: la famiglia «{fam}» non è un plugin di tipo famiglia")
        for s in p.get("skill", []):
            if not (r / "skills" / s / "SKILL.md").is_file():
                fuori.append(f"{dove}: la skill «{s}» non esiste in skills/")
        for nome, voce in p.get("capacita", {}).items():
            if nome not in cat:
                fuori.append(f"{dove}: capacità «{nome}» non è nel catalogo")
            modi = [m for m in MODI if m in voce] if isinstance(voce, dict) else []
            if len(modi) != 1:
                fuori.append(f"{dove}: «{nome}» deve avere uno e un solo modo fra {MODI}")
                continue
            m = modi[0]
            if m == "eredita":
                if voce["eredita"] not in plug:
                    fuori.append(f"{dove}: «{nome}» eredita da «{voce['eredita']}», che non esiste")
                if not voce.get("motivo"):
                    fuori.append(f"{dove}: «{nome}» eredita senza motivo")
            elif m == "dati":
                for f in voce["dati"]:
                    if not (r / f).is_file():
                        fuori.append(f"{dove}: «{nome}»: il file «{f}» non esiste")
            elif m == "codice":
                if not voce.get("lotto"):
                    fuori.append(f"{dove}: «{nome}» è nel codice senza il lotto che lo migra")
                for v in voce["codice"]:
                    f, _, n = v.partition(":")
                    if not (r / f).is_file():
                        fuori.append(f"{dove}: «{nome}»: il file «{f}» non esiste")
                    elif not n or not re.search(_NOME_IN_CODICE.format(n=re.escape(n)),
                                                (r / f).read_text(encoding="utf-8"), re.M):
                        fuori.append(f"{dove}: «{nome}»: «{n}» non è definito in {f}")
            elif not voce.get("non_supportato"):
                fuori.append(f"{dove}: «{nome}» non supportato senza motivo")
    for i in sorted(plug):
        for nome in cat:
            try:
                capacita(i, nome, r)
            except ErroreSistemi as e:
                fuori.append(str(e))
    for sid, chieste in sorted((strumenti or {}).items()):
        for nome in chieste:
            if nome not in cat:
                fuori.append(f"tools.manifest.json «{sid}»: capacità «{nome}» non è nel catalogo")
                continue
            for i in att:
                c = capacita(i, nome, r)
                if c.modo == "mancante":
                    fuori.append(f"«{sid}» chiede «{nome}», che «{i}» non dichiara: "
                                 "dichiararla (dati, codice, eredita o non_supportato)")
    for f, d, c in dichiarazioni_divergenti(r):
        fuori.append(f"{f}: la riga «Sistema» dice «{d}», {CONFIG} [moduli] dice «{c}»: "
                     "correggere la riga o aggiungere la cartella a [moduli]")
    return fuori
