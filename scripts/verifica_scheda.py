#!/usr/bin/env python3
"""verifica_scheda.py — tutte le verifiche di regola di una scheda, in una chiamata (ADR-0124).

Scopo
  Un agente che scrive o corregge una scheda chiede al server MCP
  (`rumblingstone-tools`) «che cosa non torna?» e riceve, per ogni difetto,
  la **regola**, il valore **atteso**, quello che la scheda **ha**, la
  **fonte** che decide e `file:riga`. Corregge e richiama finché è pulita.
  Sola lettura: non scrive mai il canone.

  Mette insieme i verificatori che esistono, più il controllo dei gradi:
    talenti  prerequisiti dei talenti (`verifica_talenti`: SRD d20 → manuali
             3.5 → PF1e)
    numeri   pf nella fascia dei dadi vita, BAB, tiri salvezza, lotta,
             attacco, iniziativa (`conformita_statblocchi.giudica`)
    abilita  gradi delle abilità: massimo per abilità e punti disponibili
             (capacità `creature.gradi` del plugin; 3.5 e PF1e)
    incantesimi  ogni incantesimo scritto per livello è nella lista della classe
             (o in un dominio) e non sotto il suo livello (capacità
             `creature.liste_incantesimi`; 3.5 dall'SRD, PF1e dal PRD)

  Le regole sono quelle del plugin del sistema della scheda (`sistemi/<id>`).
  Un conto che il plugin non sa fare non compare: `non_verificabili` dice che
  cosa resta fuori e perché.

Uso
  python3 scripts/verifica_scheda.py Bestiario/png/x.md           # una scheda
  python3 scripts/verifica_scheda.py Bestiario/villain --json     # una cartella, per l'agente
  python3 scripts/verifica_scheda.py x.md --check                 # esce 1 se c'è una violazione

Exit  0 = misura fatta (o nessuna violazione con --check)
      1 = violazioni, solo con --check
      2 = errore d'uso

Solo stdlib.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import verifica_talenti as VT  # noqa: E402
from dmcore import lettura_creatura as L  # noqa: E402
from dmcore import bonus as B  # noqa: E402

#: campo di conformita_statblocchi → riga della scheda dove cercarlo
ETICHETTE = {"BAB": ("bab", "base attack"), "lotta": ("lotta", "grapple", "bmc"),
             "Temp": ("temp", "fort"), "Rifl": ("rifl", "ref"), "Vol": ("vol", "will"),
             "pf": ("pf", "hp"), "iniziativa": ("iniz", "init"), "attacco": ("attacc", "attack", "melee", "mischia")}


def _riga(testo: str, campo: str) -> "int | None":
    chiavi = ETICHETTE.get(campo, (campo.lower(),))
    for i, r in enumerate(testo.splitlines(), 1):
        if any(k in r.lower() for k in chiavi):
            return i
    return None


#: Tolleranza zero su tiri salvezza e attacco (DM, 2026-11-12). `--tolleranza`
#: la rimette com'era: TS fino a +4 sopra l'atteso, attacco fra −1 e +2.
SEVERO = True


def numeri(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) dei numeri di una scheda."""
    import conformita_statblocchi as C
    with contextlib.redirect_stdout(io.StringIO()):
        s = L.leggi(p)
        if s is None:
            return [], []
        if not C.del_sistema(p):
            sis = VT.sistema_di(p, s.testo)
            return [], [{"file": VT_rel(p), "riga": None, "verifica": "numeri", "regola": "sistema",
                         "testo": f"i conti di scheda non coprono il sistema {sis}", "fonte": sis}]
        g = C.giudica(s, severo=SEVERO)
    viol, nv = [], []
    dichiarati = B.dichiarati(L.senza_note(s.testo))
    ignote = (VT.leggi(p) or {}).get("classi_ignote") or []
    if not g["verificabile"]:
        nv.append({"file": g["file"], "riga": None, "verifica": "numeri", "regola": "lettura",
                   "testo": "dadi vita o caratteristiche non leggibili: nessun conto parte", "fonte": "srd"})
    for campo, (scritto, atteso, scarto) in g["scarti"].items():
        voce = {"file": g["file"], "riga": _riga(s.testo, campo), "verifica": "numeri",
                "regola": f"numero.{campo}", "atteso": atteso, "ha": scritto,
                "testo": f"{campo} {scritto}, la regola dà {atteso} (scarto {scarto:+d})"
                if isinstance(scarto, int) else f"{campo} {scritto}, la regola dà {atteso}",
                "fonte": "srd"}
        if campo in B.CAMPI_TS or campo == "attacco":
            contate = B.somma(dichiarati.get(campo, []))[1]
            voce["bonus_contati"] = [{"valore": v.valore, "tipo": v.tipo, "sorgente": v.sorgente}
                                     for v in contate]
            voce["testo"] += ("; bonus dichiarati e contati: "
                              + ", ".join(f"+{v.valore} {v.tipo.replace('_', ' ')} ({v.sorgente})"
                                          for v in contate) if contate
                              else "; la scheda non dichiara nessun bonus su questo numero")
        if "-cr" not in p.name:
            # conformita_statblocchi è collaudato sulle schede `*-cr*.md`; nei dossier
            # («BAB/Lotta: +8 / +10») la lettura prende il numero sbagliato
            voce["nota"] = "scheda a dossier: la lettura dei numeri non è collaudata su questo formato"
        elif ignote:
            voce["nota"] = "classi che la lettura non conosce: " + ", ".join(ignote)
        if g["template"]:
            voce["nota"] = f"lo scarto si spiega col template {g['template']}"
        if campo in g["come_la_fonte"]:
            voce["nota"] = "uguale alla fonte trascritta"
        if g["decisione"]:
            voce["nota"] = f"decisione aperta al DM: {g['decisione']}"
        (nv if "nota" in voce else viol).append(voce)
    return viol, nv


def VT_rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p)


def talenti(p: Path) -> "tuple[list[dict], list[dict], list[dict]]":
    f = VT.leggi(p)
    if f is None:
        return [], [], []
    v, nv = VT.verifica(f)
    for x in v + nv:
        x["verifica"] = "talenti"
    ign = [{"file": f["file"], "riga": f["riga"], "verifica": "talenti", "regola": "nome",
            "testo": f"«{n}» non è un talento di nessuna fonte", "fonte": None} for n in f["ignoti"]]
    return v, nv, ign


#: riga delle abilità: «**Abilità**: Ascoltare +12, …», «Skills: Hide +5, …»
RIGA_ABILITA = re.compile(r"(?:^|[\s*·])(?:Abilit[àa]|Skills)\**:?\**\s+(?=[A-ZÀ-Ý])(.+?)(?=\s·\s|\s\*\*[A-ZÀ-Ý]|$)")
VOCE_ABILITA = re.compile(r"([A-Za-zÀ-ú' ]+?)(?:\s*\(([^)]*)\))?\s*([+\-−]\d+)")
#: talenti che danno +2 a due abilità o +3 a una: margine quando la scheda li ha
TALENTI_ABILITA = re.compile(r"Skill Focus|Abilità Focalizzata|Alertness|Allerta|Acrobatic|Agile|Athletic|Atletico|"
                             r"Deceitful|Deft Hands|Diligent|Investigator|Magical Aptitude|Negotiator|Nimble Fingers|"
                             r"Persuasive|Persuasivo|Self-Sufficient|Stealthy|Furtivo|Animal Affinity", re.I)


@lru_cache(maxsize=None)
def _abilita_it() -> "dict[str, str]":
    import lessico_regole as LR
    return {LR.norma(v["it"]): v["srd35"].lower() for v in LR.tabella_35() if v["tipo"] == "abilità"}


@lru_cache(maxsize=None)
def _classi_it() -> "dict[str, str]":
    import lessico_regole as LR
    return {v["it"].lower(): v["srd35"].lower() for v in LR.tabella_35()
            if v["tipo"] in ("classe", "classe di prestigio")}


def _punti_di_classe(regole: dict, classe: str) -> "int | None":
    v = regole.get("classi", {}).get(classe)
    if v is None:   # le classi dei manuali 3.5 fuori SRD (classi_manuali.toml)
        m = regole.get("classi_manuali", {}).get(classe) or {}
        return None if "punti" in (m.get("diverge") or ()) else m.get("punti")
    return v.get("gradi") if isinstance(v, dict) else v


def abilita(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) dei gradi delle abilità.

    La scheda scrive il bonus totale, non i gradi: i gradi **minimi** che un
    bonus chiede sono bonus − modificatore della caratteristica chiave − margine
    (sinergia +2, razza, talenti). Due regole, tutte e due condizioni necessarie:
      gradi.massimo  i gradi minimi di un'abilità non superano il massimo
                     (3.5: dadi vita + 3; PF1e: dadi vita, più 3 d'abilità di classe)
      gradi.punti    la somma dei gradi minimi non supera i punti abilità che
                     classi e dadi vita razziali danno
    Con margini larghi vede gli errori grossi, non quelli di un punto."""
    import lessico_regole as LR
    from dmcore import sistemi as S
    f = VT.leggi(p) or {}
    s = L.leggi(p)
    if s is None:
        return [], []
    n_riga, riga = next(((i + 1, m.group(1)) for i, r in enumerate(s.testo.splitlines())
                         if (m := RIGA_ABILITA.search(r)) and re.search(r"[+−-]\d", m.group(1))), (None, None))
    if riga is None:
        return [], []
    sistema = VT.sistema_di(p, s.testo)
    rel = VT_rel(p)
    try:
        regole = S.dati(sistema, "creature.gradi")
    except S.ErroreSistemi as e:
        return [], [{"file": rel, "riga": n_riga, "verifica": "abilita", "regola": "sistema",
                     "testo": str(e), "fonte": sistema}]
    car = {k: v for k, v in s.attributi.items() if isinstance(v, int)}
    dv = sum(g.n for g in s.gruppi)
    livelli = f.get("livelli") or {k: v for k, v in L.livelli_di_classe(s).items()}
    ignote = f.get("classi_ignote") or []
    base = {"file": rel, "riga": n_riga, "verifica": "abilita",
            "fonte": "srd" if sistema == "dnd35" else f"{sistema} prd"}
    if not dv or "Int" not in car:
        return [], [{**base, "regola": "lettura", "testo": "dadi vita o Intelligenza non leggibili"}]
    r = regole["regole"]
    intel = (car["Int"] - 10) // 2
    # il tipo sta nella riga `tipo:` (o «Type»); il più lungo che combacia, perché
    # «monstrous humanoid» contiene «humanoid»
    riga_tipo = next((x for x in s.testo.splitlines() if re.match(r"\W*(?:tipo|type)\b", x, re.I)), s.testo[:400])
    alias = S.dati(sistema, "creature.costruzione").get("alias_tipo", {})
    nomi_tipo = {**{t: t for t in regole["tipi"]}, **{it: en for it, en in alias.items() if en in regole["tipi"]}}
    tipo = next((nomi_tipo[t] for t in sorted(nomi_tipo, key=len, reverse=True)
                 if re.search(rf"\b{re.escape(t)}\b", riga_tipo, re.I)), None)
    # le classi che la lettura dei livelli non conosce ma il plugin dei gradi sì («Druid 9»)
    livelli = dict(livelli)
    for voce in ignote:
        nome, _, n = voce.rpartition(" ")
        livelli[nome] = livelli.get(nome, 0) + int(n)
    razziali = max(0, dv - sum(livelli.values()))
    quote, sconosciute = [], []
    for classe, n in livelli.items():
        k = classe.lower()
        pt = next((x for x in (_punti_di_classe(regole, c) for c in (k, VT.T._ALIAS.get(k, k), _classi_it().get(k, k)))
                   if x is not None), None)
        if pt is None:
            sconosciute.append(f"{classe} {n}")
        else:
            quote.append((n, pt))
    if razziali:
        if tipo is None:
            sconosciute.append("tipo della creatura")
        else:
            quote.append((razziali, regole["tipi"][tipo]))
    per_dado = [max(r["minimo_per_dado"], pt + intel) for _, pt in quote]
    punti = sum(n * q for (n, _), q in zip(quote, per_dado)) + (r["primo_dado"] - 1) * max(per_dado, default=0)
    umano = bool(re.search(r"\b(?:human|umano|umana)\b", s.testo[:1500], re.I))
    punti += (dv + r["primo_dado"] - 1) * r["umano_per_livello"] if umano else 0
    massimo = dv + r["massimo_piu"] + r.get("bonus_di_classe", 0)
    # margine: sinergia o oggetto +2; razza +2 (mostri: +4, o +8 se la scheda parla di bonus razziali);
    # +3 se la scheda ha un talento che alza le abilità
    margine = 2 + (8 if re.search(r"razzial|racial", s.testo, re.I) else 4 if razziali else 2)
    margine += 3 if TALENTI_ABILITA.search(s.testo) else 0
    chiave = regole["chiave"]
    viol, nv, somma, lette = [], [], 0, 0
    for nome, _, bonus in VOCE_ABILITA.findall(re.sub(r"[*_`]", "", riga)):
        nome = nome.strip()
        en = _abilita_it().get(LR.norma(nome), nome.lower())
        en = next((k for k in chiave if en == k or en.startswith(k + " ")), None)
        if en is None:
            continue
        lette += 1
        mod = (car.get(chiave[en], 10) - 10) // 2 if chiave[en] else 0
        minimi = int(bonus.replace("−", "-")) - mod - margine
        somma += max(0, minimi)
        if minimi > massimo:
            viol.append({**base, "regola": "gradi.massimo", "abilita": en, "atteso": massimo, "ha": minimi,
                         "testo": f"{nome} {bonus}: servono almeno {minimi} gradi "
                                  f"(tolti {mod:+d} di caratteristica e {margine} di margine), il massimo è {massimo}"})
    if sconosciute:
        nv.append({**base, "regola": "gradi.punti", "testo": "punti abilità non calcolabili: "
                   + ", ".join(sconosciute) + " fuori dalle regole del plugin"})
        nv += [{**v, "nota": "classi che la lettura non conosce: il massimo può essere più alto"} for v in viol]
        return [], nv
    if lette and somma > punti:
        viol.append({**base, "regola": "gradi.punti", "atteso": punti, "ha": somma,
                     "testo": f"le abilità scritte chiedono almeno {somma} gradi, "
                              f"classi e dadi vita ne danno {punti}"})
    return viol, nv


# --- incantesimi: sono nella lista della classe, al livello scritto? (ADR-0124 §10) ---

#: «- 5° (3+1): *colpo infuocato* (CD 19), …», «Level 3: Dispel Magic, …», «**2°** — *aiuto*»
RIGA_LIVELLO = re.compile(r"^\s*(?:[-*•]\s*)?\**(?:Level\s+|Livello\s+)?(\d)(?:°|º|st|nd|rd|th)?\**\s*"
                          r"(?:\([^)]*\))?\s*\**\s*[:—–-]\s*(\S.*)$", re.I)
#: come una scheda nomina la classe che lancia
CLASSI_INCANTATRICI = {"chieric": "cleric", "cleric": "cleric", "clr": "cleric", "mag[oa]\\b": "wizard", "wizard": "wizard",
                       "wiz": "wizard", "stregon": "sorcerer", "sorcerer": "sorcerer", "sor\\b": "sorcerer",
                       "bard": "bard", "brd": "bard", "druid": "druid", "drd": "druid", "paladin": "paladin",
                       "pal\\b": "paladin", "ranger": "ranger", "rgr": "ranger"}
TESTA_INCANTESIMI = re.compile(r"incantesimi|spells", re.I)


@lru_cache(maxsize=None)
def _incantesimi_it() -> "dict[str, str]":
    import lessico_regole as LR
    return {LR.norma(v["it"]): v["srd35"] for v in LR.tabella_35() if v["tipo"] == "incantesimo"}


@lru_cache(maxsize=None)
def _liste(sistema: str) -> "tuple[dict, dict, dict, dict]":
    """(classe → {nome normalizzato: livello}, dominio → idem, nome normalizzato →
    nome della fonte, classe → nomi che vengono dai manuali).

    Ordine delle fonti (DM, 2026-11-12): prima la lista dell'SRD, poi quella dei
    manuali 3.5 (`liste_manuali`, da PCGen: solo nomi e livelli). Una classe che
    pesca dalle liste altrui (`liste_prese`: anima prescelta → chierico, accordo
    sublime → bardo, stregone, mago) eredita quelle liste."""
    import lessico_regole as LR
    from dmcore import sistemi as S
    d = S.dati(sistema, "creature.liste_incantesimi")
    nomi: dict = {}

    def piatta(gruppo: dict) -> dict:
        out: dict = {}
        for chiave, livelli in gruppo.items():
            for liv, voci in livelli.items():
                for n in voci:
                    k = LR.norma(n)
                    nomi.setdefault(k, n)
                    out.setdefault(chiave, {})[k] = min(int(liv), out.get(chiave, {}).get(k, 9))
        return out
    liste, domini = piatta(d.get("liste", {})), piatta(d.get("domini", {}))
    dai_manuali: dict = {}
    for chiave, voci in piatta(d.get("liste_manuali", {})).items():
        for k, liv in voci.items():
            if k not in liste.setdefault(chiave, {}):
                liste[chiave][k] = liv
                dai_manuali.setdefault(chiave, set()).add(k)
    # I domini dei manuali hanno un prefisso: valgono solo dove la scheda segna
    # l'incantesimo come di dominio. Senza il segno, un chierico prenderebbe per
    # buono qualunque incantesimo che uno dei 102 domini dei manuali concede.
    for chiave, voci in piatta(d.get("domini_manuali", {})).items():
        for k, liv in voci.items():
            domini.setdefault("manuali:" + chiave, {}).setdefault(k, liv)
    for chiave, altre in d.get("liste_prese", {}).items():
        if chiave in liste and chiave not in altre:
            continue          # ha una lista sua
        for altra in altre:
            for k, liv in liste.get(altra, {}).items():
                if altra == chiave:
                    continue
                mia = liste.setdefault(chiave, {})
                mia[k] = min(liv, mia.get(k, 9))
                if k in dai_manuali.get(altra, ()):
                    dai_manuali.setdefault(chiave, set()).add(k)
    return liste, domini, nomi, dai_manuali


@lru_cache(maxsize=None)
def _classi_dei_manuali(sistema: str) -> "list[tuple[re.Pattern, str]]":
    """Le classi con una lista che l'SRD non ha, come le nomina una scheda: il nome
    inglese e, dove il lessico lo dà, quello italiano. Le più lunghe per prime
    («savage bard» prima di «bard»)."""
    from dmcore import sistemi as S
    try:
        liste = _liste(sistema)[0]
    except S.ErroreSistemi:
        return []
    srd = set(CLASSI_INCANTATRICI.values())
    it = {k: v.get("it") for k, v in (L.T._DATI.get("classi_manuali") or {}).items()} if sistema == "dnd35" else {}
    out = []
    for nome in sorted(liste, key=len, reverse=True):
        if nome in srd or len(nome) < 5 or not re.fullmatch(r"[a-z' -]+", nome):
            continue
        for forma in filter(None, (nome, it.get(nome))):
            # una parola sola («adept», «innato») è anche una parola comune: vale
            # solo con il livello dopo («Adept 5») o come «Healer Spells»
            coda = r"(?!\w)" if " " in forma else r"(?=\s*\**\s*\d|\s+spells\b)"
            out.append((re.compile(r"(?<!\w)" + re.escape(forma) + coda, re.I), nome))
    return out


def _classi_nella_riga(riga: str, sistema: str) -> "set[str]":
    trovate = {v for k, v in CLASSI_INCANTATRICI.items() if re.search(r"\b" + k, riga, re.I)}
    for rx, nome in _classi_dei_manuali(sistema):
        m = rx.search(riga)
        if m:
            # «savage bard» non è anche «bard»
            trovate -= {v for v in trovate if v in m.group(0).lower()}
            return trovate | {nome}
    return trovate


#: quante righe non vuote possono stare fra l'intestazione e la lista («Livello
#: incantatore 14…», «Esempio di preparazione:»)
FRA_TESTA_E_LISTA = 4
CLASSE_CON_LIVELLO = r"\s*\**\s*\d{1,2}\b"


def _classe_che_lancia(righe: "list[str]", i: int, sistema: str = "dnd35") -> "str | None":
    """La classe che lancia la riga i: quella nominata dall'intestazione degli
    incantesimi più vicina sopra; se l'intestazione non la nomina («Prepared
    Spells:»), l'unica classe incantatrice scritta con il suo livello più sopra
    nello stesso blocco («Chierico 12»)."""
    testa = None
    altro = 0
    for j in range(i, max(-1, i - 20), -1):
        r = righe[j]
        if j != i and RIGA_LIVELLO.match(r):
            continue                                   # un'altra riga della lista
        if TESTA_INCANTESIMI.search(r):
            testa = j
            break
        if j != i and r.strip():
            altro += 1
            if altro > FRA_TESTA_E_LISTA or r.lstrip().startswith("#"):
                return None                            # fra la lista e l'intestazione c'è dell'altro
    if testa is None:
        return None
    riga = righe[testa] if testa != i else righe[testa].split("—")[0]
    trovate = _classi_nella_riga(riga, sistema)
    if trovate:
        # «Bardo 8 + Accordo Sublime 1»: la lista è l'unione delle due
        return "+".join(sorted(trovate))
    for j in range(testa - 1, max(-1, testa - 40), -1):
        r = righe[j]
        if re.match(r"\s*(?:---+|\*\*\*+)\s*$", r):
            return None                                # finisce il blocco della creatura
        con_livello = {c for c in _classi_nella_riga(r, sistema)
                       if any(re.search(rx.pattern + CLASSE_CON_LIVELLO, r, re.I)
                              for rx, n in _classi_dei_manuali(sistema) if n == c)
                       or any(re.search(r"\b" + k + r"[a-z]*" + CLASSE_CON_LIVELLO, r, re.I)
                              for k, v in CLASSI_INCANTATRICI.items() if v == c)}
        if con_livello:
            return "+".join(sorted(con_livello))
        if r.lstrip().startswith("#") and j < testa - 1:
            return None
    return None


def incantesimi(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) degli incantesimi scritti per livello.

    Regole: `incantesimo.lista` (l'incantesimo non è nella lista della classe né
    in un dominio), `incantesimo.livello` (è scritto a un livello più basso del
    suo; più alto si accetta, è uno slot superiore o un talento di metamagia).
    Un nome che le liste non hanno (manuali, nomi propri) non è verificabile."""
    testo = p.read_text(encoding="utf-8", errors="replace")
    sistema = VT.sistema_di(p, testo)
    from dmcore import sistemi as S
    try:
        liste, domini, nomi, dai_manuali = _liste(sistema)
    except S.ErroreSistemi:   # il sistema non ha liste di classe
        return [], []
    import lessico_regole as LR
    it = _incantesimi_it() if sistema == "dnd35" else {}
    righe = testo.splitlines()
    viol, nv = [], []
    for i, riga in enumerate(righe):
        m = RIGA_LIVELLO.match(riga)
        if not m or "*" not in m.group(2) and not re.search(r"\bLevel\b", riga):
            continue
        if re.match(r"\d", m.group(2)):      # «1–4: cura, …» è un intervallo, non un livello
            continue
        classe = _classe_che_lancia(righe, i, sistema)
        if classe is None or not all(c in liste for c in classe.split("+")):
            continue
        sua: dict = {}
        for c in classe.split("+"):
            for nome_k, liv in liste[c].items():
                sua[nome_k] = min(liv, sua.get(nome_k, 9))
        manuale = set().union(*(dai_manuali.get(c, set()) for c in classe.split("+")))
        scritto = int(m.group(1))
        di_dominio = False
        for pezzo in re.split(r"[,;]", re.sub(r"\((?:CD|DC)[^)]*\)", "", m.group(2))):
            if re.search(r"\bdomini[oa]\b|\bdomain\b", pezzo, re.I):
                di_dominio = True
            dominio = di_dominio or bool(re.search(r"\((?:D|d)\)|\bD\b\s*$", pezzo))
            nome = re.sub(r"\b(?:domini[oa]|domain)\s*:?|\([^)]*\)|[×x]\s*\d+\b|\bD\s*$", "", pezzo).strip(" *_.·")
            k = LR.norma(nome)
            if not k or len(k) < 3 or re.fullmatch(r"[\d+ /]+", k):
                continue
            k = LR.norma(it[k]) if k in it else k
            base = {"file": VT_rel(p), "riga": i + 1, "verifica": "incantesimi", "incantesimo": nome,
                    "fonte": "prd" if sistema != "dnd35" else
                    "3.5 manuali (PCGen)" if k in manuale else "srd"}
            if k not in nomi:
                nv.append({**base, "regola": "incantesimo.nome", "atteso": None, "ha": None,
                           "testo": f"«{nome}» non è nelle liste del plugin {sistema}"})
                continue
            suo = sua.get(k)
            da_dominio = min((d[k] for n_d, d in domini.items()
                              if k in d and (dominio or not n_d.startswith("manuali:"))), default=None)
            if suo is None and da_dominio is not None and "cleric" in classe.split("+"):
                suo = da_dominio
            elif suo is not None and dominio and da_dominio is not None:
                suo = min(suo, da_dominio)
            if suo is None:
                viol.append({**base, "regola": "incantesimo.lista", "atteso": f"lista {classe}", "ha": "fuori lista",
                             "testo": f"{nomi[k]} non è nella lista {classe}"})
            elif scritto < suo:
                viol.append({**base, "regola": "incantesimo.livello", "atteso": suo, "ha": scritto,
                             "testo": f"{nomi[k]} è di {suo}° livello per {classe}, la scheda lo scrive al {scritto}°"})
    return viol, nv


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("percorsi", nargs="+", type=Path, help="schede o cartelle")
    ap.add_argument("--json", action="store_true", help="uscita JSON per l'agente")
    ap.add_argument("--check", action="store_true", help="esce 1 se c'è almeno una violazione")
    ap.add_argument("--tolleranza", action="store_true",
                    help="rimette la tolleranza di prima su tiri salvezza (+4) e attacco (−1…+2)")
    a = ap.parse_args(argv)
    global SEVERO
    SEVERO = not a.tolleranza
    percorsi = [p if p.is_absolute() else ROOT / p for p in a.percorsi]
    for p in percorsi:
        if not p.exists():
            print(f"verifica_scheda: {p} non esiste", file=sys.stderr)
            return 2
    viol, nv, lette = [], [], 0
    for p in VT.schede(percorsi):
        tv, tn, ti = talenti(p)
        nvv, nn = numeri(p)
        av, an = abilita(p)
        iv, inn = incantesimi(p)
        lette += bool(tv or tn or ti or nvv or nn or av or an or iv or inn or L.leggi(p))
        viol += tv + nvv + av + iv
        nv += tn + ti + nn + an + inn
    if a.json:
        json.dump({"schede": lette, "violazioni": viol, "non_verificabili": nv}, sys.stdout,
                  ensure_ascii=False, indent=1)
        print()
    else:
        for v in viol:
            dove = f"{v['file']}:{v['riga']}" if v.get("riga") else v["file"]
            nome = f"{v['talento_it']} — manca " if v["verifica"] == "talenti" else ""
            print(f"{dove}: [{v['verifica']}] {nome}{v['testo']}  [regola {v['regola']}, fonte {v['fonte']}]")
        print(f"{'✗' if viol else '✓'} verifica_scheda: {lette} schede, {len(viol)} violazioni in "
              f"{len({v['file'] for v in viol})} schede, {len(nv)} voci non verificabili")
    return 1 if (a.check and viol) else 0


if __name__ == "__main__":
    sys.exit(main())
