"""statblock.py — il blocco statistiche come DATO, non come prosa (ADR-0021).

Il problema che risolve. Nel `Bestiario/` i numeri di 158 schede vivono dentro
frasi italiane: «**hp 34**; **AC 15** (+1 taglia), touch 11 … TS Temp +6». Una
prosa così si legge benissimo al tavolo e non si può usare per niente altro:
il catalogo tiene solo l'indice (id, nome, GS), la stampa non può fare un
riquadro perché non sa quale numero è quale, `suggest_encounter` bilancia sul
GS dichiarato senza poterlo verificare, e un +7 diventato +1 in trascrizione
non lo trova nessuno.

La soluzione, dentro i vincoli del repo (ADR-0003: il markdown è il master):
**un blocco recintato in testa alla scheda**, con i soli campi meccanici. La
prosa resta dov'era, sotto, e resta la cosa che si legge. Nessuna seconda copia
in un file parallelo: il blocco sta nella scheda, e chi corregge il numero lo
corregge una volta sola.

    ```statblocco
    gs: 2
    tipo: Small plant, 4d8+16
    ca: 15
    ca-dettaglio: contatto 11, colto alla sprovvista 15 (+1 taglia, +4 naturale)
    pf: 34
    velocita: 6 m
    ts: Temp +6, Rifl +1, Vol +2
    attacchi:
      - Mischia schianto +5 (1d4+1)
    voci:
      - Talenti: Allerta, Resistenza Fisica
    ```

Il formato è un sottoinsieme di YAML deliberatamente minuscolo — `chiave:
valore` e liste con `- ` — perché il repo è stdlib-only e perché un formato che
sta in venti righe di parser è un formato che si legge a occhio.

Questo modulo fa tre cose e nient'altro:
  * `leggi(testo)` — trova e legge il blocco di una scheda;
  * `estrai(testo)` — **prova** a ricavarlo dalla prosa, dicendo cosa non ha
    trovato: è il ponte per migrare le schede che esistono già;
  * `rendi(sb)` — lo riscrive in forma canonica, per poterlo inserire.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

APERTURA = "```statblocco"
CHIUSURA = "```"

# I campi obbligatori perché una scheda sia utilizzabile al tavolo: senza uno
# di questi il riquadro sarebbe una cornice con dentro dei buchi.
OBBLIGATORI = ("gs", "ca", "pf", "ts")
AMMESSI = (
    "nome", "gs", "tipo", "ca", "ca-dettaglio", "pf", "pf-dado", "ts", "velocita",
    "iniziativa", "sensi", "attributi", "attacchi", "voci", "tattica", "fonte",
)
LISTE = ("attacchi", "voci")


class StatblockError(ValueError):
    """Il blocco c'è ma non si può usare: campo ignoto, obbligatorio mancante."""


@dataclass
class Statblocco:
    nome: str = ""
    gs: str = ""
    tipo: str = ""
    ca: str = ""
    ca_dettaglio: str = ""
    pf: str = ""
    pf_dado: str = ""
    ts: str = ""
    velocita: str = ""
    iniziativa: str = ""
    sensi: str = ""
    attributi: str = ""
    attacchi: list[str] = field(default_factory=list)
    voci: list[str] = field(default_factory=list)
    tattica: str = ""
    fonte: str = ""

    @property
    def completo(self) -> bool:
        return all(getattr(self, c.replace("-", "_")) for c in OBBLIGATORI)

    def mancanti(self) -> list[str]:
        return [c for c in OBBLIGATORI if not getattr(self, c.replace("-", "_"))]


def _campo(chiave: str) -> str:
    return chiave.replace("-", "_")


def leggi(testo: str) -> Statblocco | None:
    """Il blocco della scheda, o `None` se non ce n'è uno.

    Un blocco malformato **non** è come un blocco assente: solleva. Una scheda
    che dichiara i suoi numeri e li dichiara male è peggio di una che non li
    dichiara, perché ci si fida.
    """
    righe = testo.split("\n")
    try:
        inizio = next(i for i, r in enumerate(righe) if r.strip() == APERTURA)
    except StopIteration:
        return None
    try:
        fine = next(i for i in range(inizio + 1, len(righe)) if righe[i].strip() == CHIUSURA)
    except StopIteration:
        raise StatblockError("blocco «statblocco» aperto e mai chiuso")

    sb = Statblocco()
    chiave_lista = None
    for r in righe[inizio + 1:fine]:
        if not r.strip():
            continue
        if r.lstrip().startswith("- "):
            if chiave_lista is None:
                raise StatblockError(f"voce di elenco fuori da un campo: {r.strip()!r}")
            getattr(sb, chiave_lista).append(r.lstrip()[2:].strip())
            continue
        if ":" not in r:
            raise StatblockError(f"riga senza «chiave: valore»: {r.strip()!r}")
        chiave, _, valore = r.partition(":")
        chiave = chiave.strip()
        if chiave not in AMMESSI:
            raise StatblockError(f"campo sconosciuto «{chiave}» "
                                 f"(ammessi: {', '.join(AMMESSI)})")
        if chiave in LISTE:
            chiave_lista = _campo(chiave)
            if valore.strip():
                getattr(sb, chiave_lista).append(valore.strip())
        else:
            chiave_lista = None
            setattr(sb, _campo(chiave), valore.strip())
    if sb.mancanti():
        raise StatblockError("campi obbligatori mancanti: " + ", ".join(sb.mancanti()))
    return sb


def rendi(sb: Statblocco) -> str:
    """Il blocco in forma canonica: stesso ordine, sempre, così i diff si leggono."""
    fuori = [APERTURA]
    for chiave in AMMESSI:
        valore = getattr(sb, _campo(chiave))
        if not valore:
            continue
        if chiave in LISTE:
            fuori.append(f"{chiave}:")
            fuori += [f"  - {v}" for v in valore]
        else:
            fuori.append(f"{chiave}: {valore}")
    fuori.append(CHIUSURA)
    return "\n".join(fuori)


# ── il ponte: dalla prosa al blocco ──────────────────────────────────────────
# Queste espressioni descrivono come sono scritte le schede che ESISTONO, non
# come dovrebbero essere scritte. Ogni volta che una scheda non si lascia
# leggere, la scelta è due: allargare qui, o correggere la scheda. Allargare
# qui è quasi sempre la risposta sbagliata — una libreria con quindici dialetti
# è una libreria che nessuno script potrà mai usare davvero.

_RE = {
    # Tre dialetti, tutti presenti nella libreria: «**hp 34**», «(5 HP)»,
    # «**HP**: 84». Si leggono tutti e tre; non se ne inventa un quarto.
    "pf": re.compile(r"\*{0,2}(?:hp|pf|PF|HP)\*{0,2}[:\s]\s*\*{0,2}(\d{1,4})\*{0,2}"
                     r"|\((\d{1,4})\s*(?:HP|hp|PF|pf)\)"),
    # I dadi vita, non i dadi di danno: si cercano nella frase di apertura
    # («Small plant, 4d8+16.») o accanto ai pf, mai in fondo a un attacco.
    "pf_dado": re.compile(r"(?:^|\n)[^\n]{0,80}?\b(\d{1,3}d\d{1,2}(?:\s*[+-]\s*\d+)?)\b"
                          r"(?=[^\n]{0,40}(?:\.|\bhp\b|\bpf\b))", re.I),
    "ca": re.compile(r"\*{0,2}(?:AC|CA)\*{0,2}[:\s]\s*\*{0,2}(\d{1,2})\*{0,2}"),
    "ca_dettaglio": re.compile(
        r"\*{0,2}(?:AC|CA)\*{0,2}[:\s]\s*\*{0,2}\d{1,2}\*{0,2}\s*((?:\([^)]*\)|,)[^.;\n]*)"),
    "ts": re.compile(r"Temp[a-z]*\**\s*\**([+-]\d+)[^.\n]{0,14}?Rifl[a-z]*\**\s*\**([+-]\d+)"
                     r"[^.\n]{0,14}?Vol[a-z]*\**\s*\**([+-]\d+)"),
    # Le schede trascritte dai manuali sono in inglese: stessa cosa, altro nome.
    "ts_en": re.compile(r"Fort[a-z]*\**\s*\**([+-]?\d+)[^.\n]{0,14}?Ref[a-z]*\**\s*\**([+-]?\d+)"
                        r"[^.\n]{0,14}?Will\**\s*\**([+-]?\d+)"),
    "velocita": re.compile(r"\b(?:Vel|Velocità|Speed)\.?\**\s*:?\s*([^.;|\n]+)"),
    "iniziativa": re.compile(r"\bInit(?:iativa|\.)?\**\s*:?\s*\**([+-]\d+)"),
    # «CR 1/2» è mezzo grado, non uno: catturare solo la prima cifra farebbe
    # sembrare un goblin il doppio di quello che è.
    "gs": re.compile(r"\*{0,2}(?:CR|GS)\*{0,2}[:\s]\s*\*{0,2}(\d{1,2}\s*/\s*\d|\d+\.\d+|\d{1,2})"),
    "tipo": re.compile(r"^\s*((?:Tiny|Small|Medium|Large|Huge|Gargantuan|Colossal)\s+[^.]{2,80})\.",
                       re.M | re.I),
    "attacco": re.compile(r"^\*{0,2}(Mischia|Distanza|Melee|Ranged)\*{0,2}\s+([^\n]+)", re.M),
    "voce": re.compile(r"\*{0,2}\b(Talenti|Abilità|Speciali|Capacità|Incantesimi)\*{0,2}\s*:\s*"
                       r"([^.\n]+)"),
}


def _fino_al_punto(s: str) -> str:
    """La prima frase, tenendo insieme le parentesi: «+5 (1d4+1). Altro» → «+5 (1d4+1)»."""
    fuori = []
    livello = 0
    for i, c in enumerate(s):
        if c == "(":
            livello += 1
        elif c == ")":
            livello = max(0, livello - 1)
        elif c == "." and livello == 0 and (i + 1 >= len(s) or s[i + 1] in " \n"):
            break
        fuori.append(c)
    return "".join(fuori).strip()


def estrai(testo: str) -> tuple[Statblocco, list[str]]:
    """Prova a ricavare il blocco dalla prosa. Ritorna (blocco, campi non trovati).

    Non indovina: se un numero non c'è nel testo, resta vuoto e finisce
    nell'elenco dei mancanti. Una scheda inventata a metà sarebbe peggio di una
    scheda non migrata.
    """
    sb = Statblocco()
    for chiave in ("pf", "ca", "velocita", "iniziativa", "gs", "tipo", "pf_dado"):
        m = _RE[chiave].search(testo)
        if m:
            # `pf` ha due rami alternativi: vale il gruppo che ha catturato.
            valore = next((g for g in m.groups() if g), "")
            setattr(sb, chiave, valore.strip().rstrip(",;"))
    m = _RE["ca_dettaglio"].search(testo)
    if m:
        # La barra verticale separa i CAMPI nelle schede a coppie chiave/valore:
        # oltre quella non c'è più il dettaglio della CA, c'è un altro campo.
        sb.ca_dettaglio = m.group(1).split("|")[0].strip().lstrip(",").strip()
    m = _RE["ts"].search(testo) or _RE["ts_en"].search(testo)
    if m:
        def segno(v: str) -> str:
            return v if v[0] in "+-" else "+" + v
        sb.ts = (f"Temp {segno(m.group(1))}, Rifl {segno(m.group(2))}, "
                 f"Vol {segno(m.group(3))}")
    # L'attacco finisce dove finisce la frase: nel formato compatto del repo
    # dopo il danno segue spesso tutt'altro («… (1d4+1). Scurovisione 18 m»).
    sb.attacchi = [f"{a} {_fino_al_punto(b)}" for a, b in _RE["attacco"].findall(testo)][:4]
    sb.voci = [f"{a}: {b.strip()}" for a, b in _RE["voce"].findall(testo)][:4]
    # Il markdown residuo non serve dentro un campo che verrà impaginato a parte.
    for chiave in ("tipo", "ca_dettaglio", "velocita"):
        setattr(sb, chiave, getattr(sb, chiave).replace("**", "").strip())
    sb.attacchi = [a.replace("**", "").strip() for a in sb.attacchi]
    sb.voci = [v.replace("**", "").strip() for v in sb.voci]
    return sb, sb.mancanti()


def togli_blocco(testo: str) -> str:
    """Il testo senza il blocco: serve a chi impagina la prosa a parte."""
    righe = testo.split("\n")
    try:
        inizio = next(i for i, r in enumerate(righe) if r.strip() == APERTURA)
        fine = next(i for i in range(inizio + 1, len(righe)) if righe[i].strip() == CHIUSURA)
    except StopIteration:
        return testo
    return "\n".join(righe[:inizio] + righe[fine + 1:]).lstrip("\n")
