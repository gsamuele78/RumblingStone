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
    incantatori  incantesimi al giorno (tabella della classe, incantesimi
             bonus, slot di dominio o di scuola), conosciuti, livello massimo
             lanciabile e CD (capacità `creature.incantatori`; ADR-0126, lotto 3)
    prestigio  i requisiti delle classi di prestigio: bonus di attacco base
             delle altre classi, gradi (massimo prima dell'ingresso e abilità
             scritta), talenti, razza, allineamento, livello d'incantesimo
             (capacità `creature.prestigio`; ADR-0126, lotto 3-bis)
    creatura_base  dadi vita razziali e armatura naturale della creatura base
             che la fonte della scheda dichiara («SRD *Ogre* + …»), e il dado
             dei suoi attacchi naturali nel conto del danno (capacità
             `creature.base`; ADR-0126, lotto 5)
    numero_talenti  quanti talenti: per dadi vita, bonus di classe, umano; fuori
             dal conto quelli concessi dalla classe e quelli dichiarati
             («(B)», «(razziale)», «(dominio)», «(difetto)») (ADR-0126, lotto 4)

  Le regole sono quelle del plugin del sistema della scheda (`sistemi/<id>`).
  Un conto che il plugin non sa fare non compare: `non_verificabili` dice che
  cosa resta fuori e perché.

Uso
  python3 scripts/verifica_scheda.py Bestiario/png/x.md           # una scheda
  python3 scripts/verifica_scheda.py Bestiario/villain --json     # una cartella, per l'agente
  python3 scripts/verifica_scheda.py x.md --check                 # esce 1 se c'è una violazione
  python3 scripts/verifica_scheda.py x.md --fatti                 # non giudica: talenti, incantesimi,
                                                                  # capacità speciali e righe di «Tattiche»
                                                                  # e «Descrizione», in JSON (ADR-0126)

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
#: talenti che danno +2 a due abilità o +3 a una, nominati fuori dalla riga dei talenti:
#: lì non si sa su quale abilità, e il margine vale per tutte
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


def _bonus_dei_talenti(nomi: "list[str]", sistema: str, effetti: dict, chiave: dict,
                       dv: int) -> "tuple[dict[str, int], int]":
    """({abilità: bonus}, bonus su tutte) che i talenti scritti danno alle abilità.

    I numeri sono del plugin (`effetti_talenti`): +2 a due abilità, +3 a una
    scelta. L'abilità scelta sta fra parentesi accanto al talento; se non si
    legge, il bonus vale per tutte (il conto resta una condizione necessaria).
    Dove il bonus cresce coi gradi (PF1e) si prende il più alto che i dadi vita
    permettono. Bonus di talenti diversi sulla stessa abilità si sommano."""
    import lessico_regole as LR
    per: dict[str, int] = {}
    a_tutte = 0
    for nome in nomi:
        r = VT.risolvi(sistema, nome)
        e = effetti.get((r or {}).get("en", "").lower())
        if not e:
            continue
        b = e["bonus_con_gradi"] if dv >= e.get("con_gradi", 10 ** 6) else e["bonus"]
        if e.get("a_scelta"):
            m = re.search(r"[(:]\s*([^)]+)", nome)
            en = _abilita_it().get(LR.norma(m.group(1).strip()), m.group(1).strip().lower()) if m else None
            en = next((k for k in chiave if en and (en == k or en.startswith(k + " "))), None)
            if en is None:
                a_tutte = max(a_tutte, b)
            else:
                per[en] = per.get(en, 0) + b
            continue
        for a in e.get("abilita", []):
            k = next((k for k in chiave if a == k or a.startswith(k + " ")), a)
            per[k] = per.get(k, 0) + b
    return per, a_tutte


def _talenti_d_abilita(nomi: "list[str]", testo: str, sistema: str, regole: dict,
                       dv: int) -> "tuple[dict[str, int], int]":
    """Il bonus dei talenti sulle abilità: dalla riga dei talenti, e se lì non ce
    n'è da dove il testo li nomina («Allerta dal famiglio», una riga dei talenti
    che la lettura non trova): valgono lo stesso, sulle loro abilità."""
    effetti, chiave = regole.get("effetti_talenti", {}), regole["chiave"]
    per, a_tutte = _bonus_dei_talenti(nomi, sistema, effetti, chiave, dv)
    if not per and not a_tutte:
        altrove = [m.group(0) for m in re.finditer(rf"(?:{TALENTI_ABILITA.pattern})(?:\s*\([^)]*\))?", testo, re.I)]
        per, a_tutte = _bonus_dei_talenti(list(dict.fromkeys(altrove)), sistema, effetti, chiave, dv)
    return per, a_tutte


def abilita(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) dei gradi delle abilità.

    La scheda scrive il bonus totale, non i gradi: i gradi **minimi** che un
    bonus chiede sono bonus − modificatore della caratteristica chiave − margine
    (sinergia +2, razza) − il bonus dei talenti su quell'abilità. Due regole, tutte e due condizioni necessarie:
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
    # margine: sinergia o oggetto +2; razza +2 (mostri: +4, o +8 se la scheda parla di bonus razziali).
    # Il bonus dei talenti non è margine: va solo alle abilità che il talento nomina.
    margine = 2 + (8 if re.search(r"razzial|racial", s.testo, re.I) else 4 if razziali else 2)
    chiave = regole["chiave"]
    da_talento, a_tutte = _talenti_d_abilita(f.get("nomi") or [], s.testo, sistema, regole, dv)
    viol, nv, somma, lette = [], [], 0, 0
    for nome, _, bonus in VOCE_ABILITA.findall(re.sub(r"[*_`]", "", riga)):
        nome = nome.strip()
        en = _abilita_it().get(LR.norma(nome), nome.lower())
        en = next((k for k in chiave if en == k or en.startswith(k + " ")), None)
        if en is None:
            continue
        lette += 1
        mod = (car.get(chiave[en], 10) - 10) // 2 if chiave[en] else 0
        talento = max(da_talento.get(en, 0), a_tutte)
        minimi = int(bonus.replace("−", "-")) - mod - margine - talento
        somma += max(0, minimi)
        if minimi > massimo:
            viol.append({**base, "regola": "gradi.massimo", "abilita": en, "atteso": massimo, "ha": minimi,
                         "testo": f"{nome} {bonus}: servono almeno {minimi} gradi "
                                  f"(tolti {mod:+d} di caratteristica, {margine} di margine"
                                  + (f" e {talento} dei talenti" if talento else "") + f"), il massimo è {massimo}"})
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


_LI = re.compile(r"(?:\bLI|\bCL|incantatore di|livello (?:dell['’]\s*)?incantatore)\s*(\d{1,2})", re.I)
_SPECIALISTA = re.compile(r"specialist|scuol[ae] proibit|prohibited school|\b(?:abiurator|ammaliator|divinator|evocator|"
                          r"illusionist|invocator|necromant|trasmutator)", re.I)
_CAR = {"Sag": r"(?:Sag|Wis)", "Int": r"Int", "Car": r"(?:Car|Cha)"}


def _testa_della_lista(righe: "list[str]", i: int) -> "int | None":
    """L'intestazione degli incantesimi sopra la riga i (come `_classe_che_lancia`)."""
    altro = 0
    for j in range(i, max(-1, i - 20), -1):
        r = righe[j]
        if j == i or RIGA_LIVELLO.match(r):
            continue                 # una riga della lista non è l'intestazione, anche se nomina «incantesimi»
        if TESTA_INCANTESIMI.search(r):
            return j
        if r.strip():
            altro += 1
            if altro > FRA_TESTA_E_LISTA or r.lstrip().startswith("#"):
                return None
    return None


def _livello_scritto(riga: str, classe: str) -> "int | None":
    """Il livello di `classe` scritto nella riga. «conosciuti e al giorno da
    stregone 9» vince su «Stregone 6»: è la scheda che dice con quale riga
    della tabella lancia (un mostro che somma i livelli innati)."""
    nomi = [k for k, v in CLASSI_INCANTATRICI.items() if v == classe]
    for k in nomi:
        m = re.search(r"(?:conosciuti|al giorno)[^;:)]*?\bda\s+" + k + r"[a-z]*\s*(\d{1,2})\b", riga, re.I)
        if m:
            return int(m.group(1))
    for k, v in CLASSI_INCANTATRICI.items():
        if v == classe:
            m = re.search(r"\b" + k + r"[a-z]*\s*(?:di\s*)?\**\s*(\d{1,2})\b", riga, re.I)
            if m:
                return int(m.group(1))
    return None


def _punteggio_che_lancia(righe: "list[str]", testa: int, car: str) -> "int | None":
    """Il punteggio della caratteristica: quello che l'intestazione dichiara
    («con Sag 24»), altrimenti la riga delle caratteristiche più vicina nella
    stessa sezione, sopra e poi sotto. Le righe «era:» sono numeri vecchi."""
    rx = re.compile(r"\b" + _CAR[car] + r"\b\s*\**:?\s*(\d{1,2})\b", re.I)
    pezzo = righe[testa][TESTA_INCANTESIMI.search(righe[testa]).start():]
    m = rx.search(pezzo)
    if m:
        return int(m.group(1))
    intera = re.compile(r"\b(?:For|Str)\b\s*\**:?\s*\d", re.I)
    for passo, limite in ((-1, 80), (1, 40)):
        j = testa
        for _ in range(limite):
            j += passo
            if not 0 <= j < len(righe) or righe[j].lstrip().startswith("#"):
                break
            m = rx.search(righe[j])
            if m and intera.search(righe[j]) and not re.search(r"\bera\b", righe[j][:m.start()]):
                return int(m.group(1))
    return None


def incantatori(p: Path) -> "tuple[list[dict], list[dict]]":
    """Incantesimi al giorno, conosciuti, livello massimo e CD (ADR-0126, lotto 3).

    Regole `numero.incantesimi.al_giorno`, `.conosciuti`, `.livello`, `.cd`. Una
    lista di cui non si legge la classe, il livello o la caratteristica torna fra
    i non verificabili, una volta per lista."""
    from dmcore import magia as M
    from dmcore import sistemi as S
    testo = p.read_text(encoding="utf-8", errors="replace")
    sis = VT.sistema_di(p, testo)
    try:
        M.tabelle(sis)
    except S.ErroreSistemi:
        return [], []
    righe = testo.splitlines()
    viol, nv = [], []
    liste: "dict[int, dict | None]" = {}
    fonte = "srd" if sis == "dnd35" else "prd"

    def nota(riga: int, perche: str) -> None:
        nv.append({"file": VT_rel(p), "riga": riga + 1, "verifica": "incantatori", "regola": "numero.incantesimi",
                   "fonte": fonte, "testo": perche})

    for i, riga in enumerate(righe):
        m = M.RIGA.match(riga)
        if not m or "*" not in m.group("resto") or re.match(r"\d", m.group("resto")):
            continue
        testa = _testa_della_lista(righe, i)
        if testa is None:
            continue
        if testa not in liste:
            liste[testa] = None
            classe = _classe_che_lancia(righe, i, sis)
            if classe is None:
                nota(testa, "non si legge quale classe lancia questa lista")
                continue
            if M.classe(classe, sis) is None:
                nota(testa, f"«{classe}» non ha una tabella degli incantesimi nel plugin {sis}")
                continue
            dati = M.classe(classe, sis)
            t = righe[testa]
            pezzo = t[TESTA_INCANTESIMI.search(t).start():]
            li = _LI.search(pezzo)
            livello = _livello_scritto(pezzo, classe) or (int(li.group(1)) if li else None)
            # una classe di prestigio alza il livello con cui la lista si lancia (ADR-0126, lotto 3-ter)
            pr = _prestigio_nel_tipo(righe, testa, classe, sis)
            if pr and not (livello and _livello_scritto(pezzo, classe) is None and classe in ("paladin", "ranger")):
                base, piu, parti, dubbio = pr
                come = f"{classe} {base} + " + " + ".join(parti) if parti else f"{classe} {base}, nessun livello in più"
                if dubbio:
                    if livello != base + piu:
                        nota(testa, f"livello d'incantatore non giudicabile ({come}): {dubbio}")
                elif livello is None:
                    livello = base + piu
                elif livello != base + piu:
                    viol.append({"file": VT_rel(p), "riga": testa + 1, "verifica": "incantatori", "fonte": fonte,
                                 "regola": "numero.incantesimi.livello_incantatore", "atteso": base + piu, "ha": livello,
                                 "testo": f"la lista si lancia da {classe} {livello}, le classi danno {base + piu} ({come})"})
            if livello is None:
                for j in range(testa - 1, max(-1, testa - 40), -1):
                    if righe[j].lstrip().startswith("#") or re.match(r"\s*(?:---+|\*\*\*+)\s*$", righe[j]):
                        break
                    livello = _livello_scritto(righe[j], classe)
                    if livello:
                        break
            if not livello:
                nota(testa, f"non si legge il livello di {classe}")
                continue
            punti = _punteggio_che_lancia(righe, testa, dati["caratteristica"])
            if punti is None:
                nota(testa, f"non si legge {dati['caratteristica']}, la caratteristica che lancia")
                continue
            intorno = "\n".join(righe[max(0, testa - 60):testa + 60])
            foc = (2 if re.search(r"Focalizzat[oi] Superior|Greater Spell Focus", intorno, re.I)
                   else 1 if re.search(r"Incantesimi Focalizzati|Spell Focus", intorno, re.I) else 0)
            spec = classe == "wizard" and bool(_SPECIALISTA.search(intorno))
            var = dati.get("variante_del_dm")
            liste[testa] = {"classe": classe, "livello": livello, "punti": punti, "foc": foc, "testa": testa,
                            "prove": [(M.al_giorno(classe, livello, punti, x, spec), M.conosciuti(classe, livello, x), [])
                                      for x in ([sis, var] if var else [sis])],
                            "variante": var, "car": dati["caratteristica"]}
            scritti = M.leggi_al_giorno(pezzo)
            if scritti:
                da_zero = dati["al_giorno"]["20"][0] >= 0
                for attesi, _, scarti in liste[testa]["prove"]:
                    scarti += [(testa, {"campo": "incantesimi.al_giorno", "scritto": x["scritto"], "atteso": x["atteso"],
                                        "nota": f"incantesimi al giorno di {x['livello']}°, tabella più incantesimi bonus"})
                               for x in M.giudica_dichiarati(scritti, attesi, da_zero)]
        lista = liste[testa]
        if lista is None:
            continue
        for attesi, noti, scarti in lista["prove"]:
            scarti += [(i, x) for x in M.giudica_riga(int(m.group("liv")), m.group("par") or "", m.group("resto"),
                                                      attesi, noti, lista["punti"], lista["foc"])]
    for lista in filter(None, liste.values()):
        scarti = lista["prove"][0][2]
        chi = f"{lista['classe']} {lista['livello']}, {lista['car']} {lista['punti']}"
        if lista["variante"] and scarti and not [x for _, x in lista["prove"][1][2] if x["campo"] != "incantesimi.cd"]:
            # la scheda segue la tabella che il DM ha scelto per questa classe: è una forma
            # ibrida dichiarata, va nel registro delle regole custom (D-B-ter, lotto 11)
            if any(x["campo"] != "incantesimi.cd" for _, x in scarti):
                nv.append({"file": VT_rel(p), "riga": lista["testa"] + 1, "verifica": "incantatori", "fonte": fonte,
                           "regola": "numero.incantesimi.variante",
                           "testo": f"{chi}: gli slot e i conosciuti seguono la tabella {lista['variante']} scelta dal DM "
                                    f"per questa classe, non quella del {sis}: forma ibrida da registrare"})
            scarti = [(r, x) for r, x in scarti if x["campo"] == "incantesimi.cd"]
        for r, x in scarti:
            viol.append({"file": VT_rel(p), "riga": r + 1, "verifica": "incantatori", "fonte": fonte,
                         "regola": f"numero.{x['campo']}", "atteso": x["atteso"], "ha": x["scritto"],
                         "testo": f"{x['campo']} {x['scritto']}, la regola dà {x['atteso']} ({x['nota']}; {chi})"})
    return viol, nv


def _prestigio_nel_tipo(righe: "list[str]", testa: int, classe: str,
                        sistema: str) -> "tuple[int, int, list[str], str | None] | None":
    """(livelli di `classe`, livelli in più, come, dubbio) dalla riga `tipo:` sopra
    la lista, se nomina `classe` e almeno una classe di prestigio. None altrimenti."""
    from dmcore import prestigio as PR
    tipo = next((righe[j] for j in range(testa, -1, -1) if righe[j].lstrip().lower().startswith("tipo:")), None)
    if tipo is None:
        return None
    base, prestigi, altre = 0, [], []
    for pezzo in re.split(r"[,/]", tipo.split(":", 1)[1]):
        m = re.match(r"\s*([A-Za-zÀ-ú' -]+?)\s+(\d{1,2})\b", pezzo)
        if not m:
            continue
        nome, n = m.group(1).strip(), int(m.group(2))
        en = _prestigio_en(nome, sistema)
        if en:
            prestigi.append((en, n))
            continue
        k = nome.lower()
        lancia = "wizard" if k in VT.SPECIALISTI else next(
            (v for rx, v in CLASSI_INCANTATRICI.items() if re.match(rx, k)), None)
        if lancia == classe:
            base += n
        elif lancia:
            altre.append(lancia)
    if not prestigi or not base:
        return None
    return (base, *PR.avanzamento(classe, prestigi, altre, sistema))


def _prestigio_en(nome: str, sistema: str) -> "str | None":
    """Il nome inglese della classe di prestigio, se il plugin ne ha i requisiti."""
    from dmcore import prestigio as PR
    k = nome.strip().lower()
    return next((c for c in (k, VT.T._ALIAS.get(k, k), _classi_it().get(k, k)) if PR.classe(c, sistema)), None)


def _gradi_che_il_bonus_regge(s: "L.Scheda", sistema: str) -> "tuple[dict[str, int], set[str]] | None":
    """{abilità: bonus scritto − modificatore di caratteristica} e le abilità di
    Forza e Destrezza, dove la penalità di armatura può nascondere dei gradi."""
    import lessico_regole as LR
    from dmcore import sistemi as S
    from dmcore.magia import mod as M_mod
    riga = next((m.group(1) for r in s.testo.splitlines()
                 if (m := RIGA_ABILITA.search(r)) and re.search(r"[+−-]\d", m.group(1))), None)
    if riga is None:
        return None
    chiave = S.dati(sistema, "creature.gradi")["chiave"]
    car = {k: v for k, v in s.attributi.items() if isinstance(v, int)}
    regge: dict[str, int] = {}
    for nome, _, bonus in VOCE_ABILITA.findall(re.sub(r"[*_`]", "", riga)):
        en = _abilita_it().get(LR.norma(nome.strip()), nome.strip().lower())
        en = next((k for k in chiave if en == k or en.startswith(k + " ")), None)
        if en is None:
            continue
        mod = M_mod(car.get(chiave[en], 10)) if chiave[en] else 0
        regge[en] = max(regge.get(en, -99), int(bonus.replace("−", "-")) - mod)
    return regge, {k for k, c in chiave.items() if c in ("For", "Des")}


def prestigio(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) dei requisiti delle classi di prestigio
    (ADR-0126, lotto 3-bis). Regole `prestigio.bab`, `.gradi.massimo`, `.gradi`,
    `.talenti`, `.razza`, `.allineamento`, `.incantesimi`; i requisiti che non
    si riducono a un numero vanno fra i non verificabili (`prestigio.speciali`)."""
    import lessico_regole as LR
    from dmcore import prestigio as PR
    from dmcore import sistemi as S
    s = L.leggi(p)
    if s is None:
        return [], []
    f = VT.leggi(p) or {}
    sistema = VT.sistema_di(p, s.testo)
    livelli = dict(f.get("livelli") or L.livelli_di_classe(s))
    ignote = []
    for voce in f.get("classi_ignote") or []:
        nome, _, n = voce.rpartition(" ")
        livelli[nome.lower()] = livelli.get(nome.lower(), 0) + int(n)
        ignote.append(nome.lower())
    righe = s.testo.splitlines()
    n_riga = next((i + 1 for i, r in enumerate(righe) if r.lower().startswith("tipo:")), 1)
    base = {"file": VT_rel(p), "riga": n_riga, "verifica": "prestigio"}
    try:
        dati = PR.requisiti(sistema)
    except S.ErroreSistemi:
        dati = None
    costruzione = S.dati(sistema, "creature.costruzione")
    di_prestigio = {**costruzione.get("prestigio", {}),
                    **{k: v for k, v in costruzione.get("classi_manuali", {}).items() if v.get("prestigio")}}
    viol, nv = [], []
    for nome, n in livelli.items():
        k = nome.lower()
        en = _prestigio_en(nome, sistema) if dati else None
        if en is None:
            if any(c in di_prestigio for c in (k, VT.T._ALIAS.get(k, k), _classi_it().get(k, k))):
                nv.append({**base, "regola": "prestigio", "fonte": sistema,
                           "testo": f"{nome} {n}: classe di prestigio senza requisiti nel plugin {sistema}"})
            continue
        req = PR.classe(en, sistema)
        tot = max(sum(g.n for g in s.gruppi), sum(livelli.values()))
        altri = [g for g in s.gruppi if g.nome.lower() != k]
        bab_prima = None
        if s.composizione_nota and len(altri) == len(s.gruppi) - 1 and sum(g.n for g in s.gruppi) == tot <= 20:
            bab_prima = PR.bab_di(altri)
        gradi = _gradi_che_il_bonus_regge(s, sistema)
        scritti = (f.get("talenti") or []) + (f.get("senza_regole") or [])
        fatti = {
            "bab_prima": bab_prima,
            "gradi_massimi": tot - n + S.dati(sistema, "creature.gradi")["regole"]["massimo_piu"],
            "abilita": gradi[0] if gradi else None, "incerte": gradi[1] if gradi else (),
            "talenti": {PR.senza_parentesi(x["en"]) for x in scritti}
                       | {PR.senza_parentesi(x) for x in VT.talenti_concessi({c: v for c, v in livelli.items() if c != nome})},
            "talenti_ignoti": bool(f.get("ignoti")) or not f,
            "razza": s.tipo or "",
            "razze_it": {v["srd35"].lower(): (v["it"].lower(),) for v in LR.tabella_35() if v["tipo"] == "razza"},
            "allineamento": (f.get("fisici") or VT.fatti_fisici(s))["allineamento"],
            "classi": {x: v for c, v in livelli.items() if c != nome for x in (c, VT.T._ALIAS.get(c, c))},
            "car": {k: v for k, v in s.attributi.items() if isinstance(v, int)},
            "classi_ignote": any(c in ignote or c in di_prestigio or _classi_it().get(c, c) in di_prestigio
                                 for c in livelli if c != nome),
        }
        scarti, incerti = PR.giudica(req, fatti, sistema)
        chi = f"{nome} {n}"
        if req.get("diverge"):      # più libri danno requisiti diversi: lo scarto è un dubbio
            incerti = [{**x, "nota": x["nota"] + " (la classe ha requisiti diversi in più manuali)"}
                       for x in scarti] + incerti
            scarti = []
        for x in scarti:
            viol.append({**base, "fonte": req["fonte"], "regola": f"prestigio.{x['campo']}",
                         "atteso": x["atteso"], "ha": x["scritto"], "testo": f"{chi}: {x['nota']}"})
        for x in incerti:
            nv.append({**base, "fonte": req["fonte"], "regola": f"prestigio.{x['campo']}",
                       "testo": f"{chi}: {x['nota']}"})
    return viol, nv


#: un talento che la scheda dichiara fuori dal conto per livello: «(B)» del mostro,
#: «(razziale)», «[dominio]», «(difetto)», «(tratto)»
_FUORI_CONTO = re.compile(r"\(B\)|razzial|racial|domini|domain|difett|flaw|tratt[oi]\b|\btrait", re.I)


def numero_talenti(p: Path) -> "tuple[list[dict], list[dict]]":
    """(violazioni, non verificabili) del numero dei talenti (ADR-0126, lotto 4).

    I talenti scritti, tolti quelli che la classe concede per nome e quelli che
    la scheda dichiara fuori dal conto, devono essere quanti ne danno i dadi
    vita e i talenti bonus delle classi (`dmcore.talenti`), più quello
    dell'umano. Regola `numero.talenti`: di più è una violazione, di meno pure
    (uno slot non speso). Con una classe di cui il plugin non conosce i talenti
    bonus il conto resta un dubbio."""
    from dmcore import sistemi as S
    f = VT.leggi(p)
    s = L.leggi(p)
    if f is None or s is None:
        return [], []
    sistema, T = f["sistema"], VT.T
    costruzione = S.dati(sistema, "creature.costruzione")
    in_piu = costruzione.get("talenti_in_piu", {})
    bonus = T.dati(sistema)["bonus"]
    livelli: dict[str, int] = {}
    for k, v in f["livelli"].items():
        k = k if k in bonus else T._ALIAS.get(k, k) if T._ALIAS.get(k, k) in bonus else k
        livelli[k] = livelli.get(k, 0) + v
    note = set(costruzione.get("classi", {})) | set(bonus)
    ignote = list(f["classi_ignote"]) + [k for k in livelli if k not in note and T._ALIAS.get(k, k) not in note]
    tot = max(f["dv"], L.dv_totali(s.testo) or 0, sum(livelli.values()))
    # la composizione dei dadi vita non letta, o un umanoide con più di tre dadi «razziali» e
    # nessuna classe: sono livelli di una classe che la lettura non ha visto
    if not s.composizione_nota or any(g.nome == "classe non dichiarata" for g in s.gruppi) or (
            not livelli and any(g.nome == "humanoid" and g.n > 3 for g in s.gruppi)):
        ignote.append("una classe non letta")
    en_di = {c: (c if c in T.CLASSI_EN_IT else T._ALIAS.get(c, c)) for c in livelli}
    concessi = {PR_senza(t) for _, t in T.concessi(sistema, livelli)} | {PR_senza(t) for t in VT.talenti_concessi(livelli)}
    for d in in_piu.get("domini", {}).values():
        if any(livelli.get(c) or livelli.get(T._ALIAS.get(c, c)) for c in d["classi"]) and re.search(
                rf"(?:domin\w+|domains?)\b[^\n]*\b(?:{'|'.join(d['nomi'])})\b", s.testo, re.I):
            concessi |= {PR_senza(t) for t in d["talenti"]}
    contati, fuori, ignoti = 0, 0, 0
    for nome in f["nomi"]:
        r = VT.risolvi(sistema, nome)
        if _FUORI_CONTO.search(nome):
            fuori += 1
        elif r and PR_senza(r["en"]) in concessi:
            fuori += 1
        elif r is None and (len(nome.split()) > 6 or re.search(r"[.:;«»]|\b(?:era|sono|non|che)\b", nome)):
            ignoti += 1          # prosa finita nella riga, non un nome: il conto resta un dubbio
        else:
            contati += 1         # anche un nome che la lettura non conosce è un talento scritto
    minimo = T.generali(sistema, tot) + len(T.bonus_di_classe(sistema, livelli))
    umano = bool(re.search(rf"\b(?:{'|'.join(in_piu.get('razza_umana', ['human']))})\b", s.tipo or "", re.I))
    minimo += in_piu.get("umano", 0) if umano else 0
    massimo = minimo + sum(1 for c, n in livelli.items()
                           for lv in in_piu.get("capacita_o_talento", {}).get(en_di[c], ()) if lv <= n)
    base = {"file": f["file"], "riga": f["riga"], "verifica": "numero_talenti", "regola": "numero.talenti",
            "fonte": "srd" if sistema == "dnd35" else f"{sistema} prd"}
    atteso = str(minimo) if minimo == massimo else f"{minimo}-{massimo}"
    come = (f"{T.generali(sistema, tot)} per {tot} dadi vita, {len(T.bonus_di_classe(sistema, livelli))} bonus di classe"
            + (", 1 da umano" if umano and in_piu.get("umano") else "")
            + (f"; {fuori} fuori dal conto (concessi dalla classe o dichiarati)" if fuori else ""))
    if minimo <= contati <= massimo:
        return [], []
    testo = (f"la scheda conta {contati} talenti, la regola ne dà {atteso} ({come})")
    if ignote:
        return [], [{**base, "testo": testo + f"; i talenti bonus di {', '.join(ignote)} non sono nel plugin"}]
    if ignoti:
        return [], [{**base, "testo": testo + f"; la riga ha {ignoti} voci di prosa che non si contano"}]
    if contati > massimo:
        testo += "; un talento fuori dal conto va dichiarato accanto al nome: (B), (razziale), (dominio), (difetto)"
    return [{**base, "atteso": atteso, "ha": contati, "testo": testo}], []


def PR_senza(nome: str) -> str:
    return re.sub(r"\s*\(.*$", "", nome).strip().lower()


def classe_armatura(p: Path) -> "tuple[list[dict], list[dict]]":
    """La CA dei recinti della scheda, ricostruita dalle sue voci (ADR-0126, lotto 1-bis)."""
    import conformita_statblocchi as C
    from dmcore import classe_armatura as CA
    testo = p.read_text(encoding="utf-8")
    sis = VT.sistema_di(p, testo)
    if sis != "dnd35":
        return [], []          # il PF1e ha già contatto, sprovvista e DMC nel cancello dei moduli
    viol, nv = [], []
    with contextlib.redirect_stderr(io.StringIO()):
        blocchi = list(C._recinti_del_master(testo))
    righe = testo.split("\n")
    for b in blocchi:
        sb = b["sb"]
        riga = next((i + 1 for i in range(b["riga"] - 1, min(len(righe), b["riga"] + 40))
                     if righe[i].startswith("ca:")), b["riga"])
        scarti, non = CA.giudica(C._int(sb.ca), sb.ca_dettaglio or "",
                                 C._mod_caratteristica(sb.attributi or "", "Des"), testo, sis)
        base = {"file": VT_rel(p), "riga": riga, "verifica": "numeri", "fonte": "srd"}
        for x in scarti:
            viol.append(dict(base, regola=f"numero.{x['campo']}", atteso=x["atteso"], ha=x["scritto"],
                             testo=f"{x['campo']} {x['scritto']}, la regola dà {x['atteso']} ({x['nota']})"))
        for x in non:
            nv.append(dict(base, regola="numero.CA", testo=x["nota"]))
        # sensi e CD: gli stessi conti che il cancello dei moduli fa sui recinti dei master
        for x in C.conti_del_recinto(b, {}, sis):
            if x["campo"] == "sensi" or x["campo"].startswith("CD"):
                campo = x["campo"].replace(" ", "_")
                viol.append(dict(base, riga=b["riga"], regola=f"numero.{campo}", atteso=x["atteso"],
                                 ha=x["scritto"],
                                 testo=f"{x['campo']} {x['scritto']}, la regola dà {x['atteso']} ({x['nota']})"))
    return viol, nv


_FONTE_SCHEDA = re.compile(r"\*\*(?:Source|Fonte)\*\*\s*:?\s*([^|\n]*)", re.I)
_TAGLIE_IT = {"minuscola": "Fine", "minuta": "Diminutive", "piccolissima": "Tiny", "piccola": "Small",
              "media": "Medium", "grande": "Large", "enorme": "Huge", "mastodontica": "Gargantuan",
              "colossale": "Colossal"}
_TIPI_IT = {"gigante": "giant", "umanoide mostruoso": "monstrous humanoid", "umanoide": "humanoid",
            "bestia magica": "magical beast", "animale": "animal", "aberrazione": "aberration",
            "esterno": "outsider", "non morto": "undead", "costrutto": "construct", "drago": "dragon",
            "elementale": "elemental", "folletto": "fey", "melma": "ooze", "vegetale": "plant",
            "parassita": "vermin"}


def _base_del_blocco(testo: str, sb, un_blocco: bool, sistema: str) -> "tuple[str, dict, bool] | None":
    """(nome, voce, stessa taglia) della creatura base che la scheda dichiara, o None.

    La dichiara la riga della fonte («SRD *Ogre* + …», solo se il file ha un
    blocco solo). Il sottotipo non basta: un flind è «umanoide (gnoll)» e non è
    uno gnoll. Un drago vero (col colore scritto) ha per base la sua taglia.
    Vale solo se il tipo della base è quello del blocco: «MM Rakshasa + Rogue 3»
    su un umanoide è il cultista di un rakshasa, non un rakshasa."""
    from dmcore import creature_base as CB
    tipo_ = (sb.tipo or "").lower()
    for it, en in _TIPI_IT.items():
        tipo_ = tipo_.replace(it, en)
    dove = (sb.taglia or "").lower() + " " + tipo_
    taglia = next((en for it, en in _TAGLIE_IT.items() if re.search(rf"\b{it}\b", dove)), None) or next(
        (t for t in _TAGLIE_IT.values() if re.search(rf"\b{t.lower()}\b", dove)), None)
    trovata = None
    if un_blocco:
        m = _FONTE_SCHEDA.search(testo)
        trovata = CB.dichiarata(m.group(1), sistema) if m else None
    if trovata is None and ("dragon" in tipo_ or (not tipo_ and un_blocco)):
        # un drago vero: il colore sta nel tipo o, con un blocco solo, nel titolo della scheda
        trovata = CB.drago((sb.tipo or "") + (" " + testo.split("\n", 1)[0] if un_blocco else ""), taglia, sistema)
        if trovata:
            return trovata[0], trovata[1], True
    if trovata is None or trovata[1]["tipo"] not in tipo_:
        return None
    return trovata[0], trovata[1], taglia == trovata[1]["taglia"]


def creatura_base(p: Path) -> "tuple[list[dict], list[dict]]":
    """Dadi vita razziali e armatura naturale della creatura base dichiarata (ADR-0126, lotto 5)."""
    import conformita_statblocchi as C
    testo = p.read_text(encoding="utf-8")
    sis = VT.sistema_di(p, testo)
    viol, nv = [], []
    with contextlib.redirect_stderr(io.StringIO()):
        blocchi = list(C._recinti_del_master(testo))
    for b in blocchi:
        sb = b["sb"]
        trovata = _base_del_blocco(testo, sb, len(blocchi) == 1, sis)
        if trovata is None:
            continue
        nome, voce, stessa = trovata
        if "dv" not in voce:
            continue               # un drago vero: dalla taglia vengono solo gli attacchi
        base = {"file": VT_rel(p), "riga": b["riga"], "verifica": "creatura_base", "fonte": "srd"}
        # dadi vita razziali: «4d8» dell'ogre deve stare nei dadi scritti
        dadi = " ".join(x for x in (sb.pf_dado or "", sb.tipo or "") if x)
        scritti = re.findall(r"(\d+)d(\d+)", dadi)
        if scritti and isinstance(voce["dv"], int):
            if (str(voce["dv"]), str(voce["dado"])) not in scritti:
                viol.append(dict(base, regola="numero.dv.razziali", atteso=f"{voce['dv']}d{voce['dado']}",
                                 ha="+".join(f"{n}d{f}" for n, f in scritti),
                                 testo=f"dadi vita {'+'.join(f'{n}d{f}' for n, f in scritti)}: la creatura base "
                                       f"{nome} porta {voce['dv']}d{voce['dado']} razziali"))
        elif not scritti:
            nv.append(dict(base, regola="numero.dv.razziali",
                           testo=f"la scheda non scrive i dadi vita: i {voce['dv']}d{voce['dado']} di {nome} non si riscontrano"))
        # armatura naturale: la base, se la taglia è la stessa
        nat = re.search(r"([+-]?\d+)\s*(?:naturale|natural|nat\b)", (sb.ca_dettaglio or "").replace("−", "-"), re.I)
        if nat and stessa:
            ha = int(nat.group(1))
            if ha != voce["naturale"]:
                viol.append(dict(base, regola="numero.CA.naturale", atteso=voce["naturale"], ha=ha,
                                 testo=f"armatura naturale {ha:+d}: la creatura base {nome} ha {voce['naturale']:+d} "
                                       f"(un bonus in più va dichiarato con la sua sorgente)"))
        elif nat and not stessa:
            nv.append(dict(base, regola="numero.CA.naturale",
                           testo=f"taglia diversa da quella di {nome} ({voce['taglia']}): l'armatura naturale non si riscontra"))
    return viol, nv


def danno(p: Path) -> "tuple[list[dict], list[dict]]":
    """Dado, bonus e critico delle armi della tabella (ADR-0126, lotto 2)."""
    import conformita_statblocchi as C
    from dmcore import danno as D
    testo = p.read_text(encoding="utf-8")
    sis = VT.sistema_di(p, testo)
    if sis != "dnd35":
        return [], []          # le armi del PF1e fuori dal manuale base arrivano col lotto 10
    viol, nv = [], []
    with contextlib.redirect_stderr(io.StringIO()):
        blocchi = list(C._recinti_del_master(testo))
    righe = testo.split("\n")
    for i, b in enumerate(blocchi):
        sb = b["sb"]
        # i talenti stanno nel recinto o nella prosa che lo segue: fino al recinto dopo
        fine = blocchi[i + 1]["riga"] - 1 if i + 1 < len(blocchi) else len(righe)
        intorno = testo if len(blocchi) == 1 else "\n".join(righe[b["riga"] - 1:fine])
        scudo = bool(re.search(r"scudo|shield|buckler|brocchiere", sb.ca_dettaglio or "", re.I))
        mod_for = C._mod_caratteristica(sb.attributi or "", "For")
        for att in sb.attacchi:
            riga = next((n + 1 for n in range(b["riga"] - 1, min(len(righe), b["riga"] + 60))
                         if att.strip()[:40] in righe[n]), b["riga"])
            base = {"file": VT_rel(p), "riga": riga, "verifica": "numeri", "fonte": "srd"}
            trovata = _base_del_blocco(testo, sb, len(blocchi) == 1, sis)
            scarti, non = D.giudica(att, mod_for, sb.tipo or "", intorno, scudo, sb.ca_dettaglio or "", sis,
                                    creatura=trovata[:2] if trovata and trovata[2] else None)
            for x in scarti:
                viol.append(dict(base, regola=f"numero.{x['campo']}", atteso=x["atteso"], ha=x["scritto"],
                                 testo=f"{x['campo']} {x['scritto']}, la regola dà {x['atteso']} ({x['nota']})"))
            for x in non:
                nv.append(dict(base, regola="numero.danno", testo=x["nota"]))
    return viol, nv


#: «**Vista cieca (Str)**», «- **Aura di paura (Sop)**:», «Spell Resistance (Su)»
_CAPACITA = re.compile(r"(?:\*{1,2}|_{1,2})\s*([^*_()]{2,70}?)\s*\((Str|Sop|Mag|Ex|Su|Sp)\)\s*(?:\*{1,2}|_{1,2})|"
                       r"(?:\*{1,2}|_{1,2})\s*([^*_()]{2,70}?)\s*(?:\*{1,2}|_{1,2})\s*\((Str|Sop|Mag|Ex|Su|Sp)\)|"
                       r"^#{1,6}\s*([^*_()#]{2,70}?)\s*\((Str|Sop|Mag|Ex|Su|Sp)\)")
#: l'etichetta di una sezione di prosa: titolo («### Tattiche») o grassetto a inizio riga («**Tattiche**:»)
_SEZIONE = re.compile(r"^\s*(?:[-*•]\s+)?(?:#{1,6}\s*|\*\*\s*)(Tattiche|Tactics|Descrizione|Description)\b", re.I)
_TITOLO = re.compile(r"^\s*(?:#{1,6}\s|---+\s*$)")
_ALTRA_SEZIONE = re.compile(r"^\s*(?:#{1,6}\s|\*\*[A-ZÀ-Ý][^*]{1,40}\*\*|---+\s*$)")


def fatti(p: Path) -> dict:
    """I fatti di una scheda che un controllo di coerenza può incrociare con la
    prosa (ADR-0126; chiesti dal controllo di coerenza della storia, regola S8):
    talenti, incantesimi e capacità speciali con il nome canonico e la riga, e
    le righe di inizio e fine di ogni «Tattiche» e «Descrizione» del file (un
    booklet ne ha più d'una). Sola lettura: non giudica nulla. Un nome che il
    plugin non conosce ha `canonico` nullo. I talenti sono quelli della prima
    riga «Talenti» del file, come nel resto dello strumento."""
    import lessico_regole as LR
    from dmcore import magia as M
    from dmcore import sistemi as S
    testo = p.read_text(encoding="utf-8", errors="replace")
    righe = testo.splitlines()
    sistema = VT.sistema_di(p, testo)
    f = VT.leggi(p)
    scheda = L.leggi(p) is not None
    if f is None:    # un file che la lettura delle schede non riconosce: resta la riga «Talenti»
        n, riga = next(((i + 1, m.group(1)) for i, r in enumerate(righe) if (m := VT.RIGA.match(r))), (None, ""))
        f = {"riga": n, "nomi": list(VT.pezzi(riga)) if n else []}
    talenti_ = [{"nome": n, "canonico": (VT.risolvi(sistema, n) or {}).get("en"), "riga": f.get("riga")}
                for n in f.get("nomi") or []]
    try:
        nomi = _liste(sistema)[2]
    except S.ErroreSistemi:
        nomi = {}
    it = _incantesimi_it() if sistema == "dnd35" else {}
    incantesimi_, capacita, sezioni = [], [], {}
    for i, riga in enumerate(righe):
        m = M.RIGA.match(riga)
        if m and "*" in m.group("resto") and not re.match(r"\d", m.group("resto")):
            della_riga = []
            for pezzo in re.split(r"[,;]", re.sub(r"\([^()]*\)|\[[^\]]*\]|[(\[].*$", "", m.group("resto"))):
                volte = re.search(r"[×x]\s*(\d+)\b", pezzo)
                nome = re.sub(r"\b(?:domini[oa]|domain)\s*:?|\([^)]*\)|[×x]\s*\d+\b|\bD\s*$", "", pezzo).strip(" *_.·")
                k = LR.norma(nome)
                if not k or len(k) < 3 or re.fullmatch(r"[\d+ /]+", k):
                    continue
                k = LR.norma(it[k]) if k in it else k
                della_riga.append({"nome": nome, "canonico": nomi.get(k), "livello": int(m.group("liv")),
                                   "usi": m.group("par") or None, "volte": int(volte.group(1)) if volte else 1,
                                   "riga": i + 1})
            # Fuori da una scheda riconosciuta «1° …» è spesso un elenco di prosa: la riga
            # conta solo se almeno un nome è un incantesimo che il plugin conosce.
            if scheda or any(x["canonico"] for x in della_riga):
                incantesimi_ += della_riga
        for c in _CAPACITA.finditer(riga):
            capacita.append({"nome": (c.group(1) or c.group(3) or c.group(5)).strip(" -:·"),
                             "tipo": c.group(2) or c.group(4) or c.group(6), "riga": i + 1})
        s = _SEZIONE.match(riga)
        if s:
            chiave = "tattiche" if s.group(1).lower().startswith("ta") else "descrizione"
            if not any(v["inizio"] <= i + 1 <= v["fine"] for v in sezioni.get(chiave, [])):
                # Un titolo si chiude al titolo dopo (dentro ha i suoi grassetti: «**Round 1**»);
                # un'etichetta in grassetto si chiude all'etichetta dopo.
                ferma = _TITOLO if riga.lstrip().startswith("#") else _ALTRA_SEZIONE
                fine = i
                for j in range(i + 1, len(righe)):
                    if ferma.match(righe[j]):
                        break
                    if righe[j].strip():
                        fine = j
                sezioni.setdefault(chiave, []).append({"inizio": i + 1, "fine": fine + 1})
    return {"file": VT_rel(p), "sistema": sistema, "talenti": talenti_, "incantesimi": incantesimi_,
            "capacita_speciali": capacita, "tattiche": sezioni.get("tattiche", []),
            "descrizione": sezioni.get("descrizione", [])}


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("percorsi", nargs="+", type=Path, help="schede o cartelle")
    ap.add_argument("--json", action="store_true", help="uscita JSON per l'agente")
    ap.add_argument("--check", action="store_true", help="esce 1 se c'è almeno una violazione")
    ap.add_argument("--fatti", action="store_true",
                    help="non giudica: stampa in JSON, per scheda, talenti, incantesimi, capacità speciali "
                         "e le righe di «Tattiche» e «Descrizione»")
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
    if a.fatti:
        tutti = [fatti(p) for p in VT.schede(percorsi)]
        json.dump([f for f in tutti if any(f[k] for k in f if k not in ("file", "sistema"))], sys.stdout,
                  ensure_ascii=False, indent=1)
        print()
        return 0
    viol, nv, lette = [], [], 0
    for p in VT.schede(percorsi):
        tv, tn, ti = talenti(p)
        nvv, nn = numeri(p)
        av, an = abilita(p)
        iv, inn = incantesimi(p)
        cv, cn = classe_armatura(p)
        dv, dn = danno(p)
        mv, mn = incantatori(p)
        pv, pn = prestigio(p)
        qv, qn = numero_talenti(p)
        bv, bn = creatura_base(p)
        lette += bool(tv or tn or ti or nvv or nn or av or an or iv or inn or cv or cn or dv or dn or mv or mn
                      or pv or pn or L.leggi(p))
        viol += tv + nvv + cv + dv + av + iv + mv + pv + qv + bv
        nv += tn + ti + nn + cn + dn + an + inn + mn + pn + qn + bn
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
