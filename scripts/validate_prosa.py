#!/usr/bin/env python3
"""validate_prosa.py — il traduttese e i tic dell'IA, misurati invece che ricordati.

Perché esiste, in tre date.

  * **2026-07-31** — i giocatori al tavolo: *«la prosa sembra tradotta
    dall'inglese»*. Nasce `references/italiano-nativo.md` (274 righe: §1 i dieci
    calchi, §9 i tic dell'IA).
  * **2026-08-01** — [ADR-0016] decide che l'italiano è la lingua sorgente e
    scrive la condizione: *«Banco di prova: i prossimi handout. Se i giocatori
    diranno ancora che sembra tradotto… questa ADR va riaperta»*.
  * **2026-09-02** — i giocatori lo dicono di nuovo, **echi compresi**.

Fra la prima data e la terza c'è un motore di stile da 2047 righe. Quindi il
problema non è che manchi la norma: è che **nessuno misura se il testo la
rispetta**, e una norma che nessuno misura è un'intenzione.

## Le due famiglie di rilievo, che sono problemi diversi

**I calchi** (§1) sono errori: *realizzare* per *to realize* è sbagliato in
italiano, punto. Qui si segnalano solo le forme con **firma inequivocabile** —
`realizzi CHE`, non ogni `realizzare`, perché *realizzare un progetto* è
italiano corretto e un validatore che lo segnala viene spento.

**I tic** (§9) non sono errori: sono **abitudini**. L'antitesi «non X: è Y»
funziona benissimo *una volta*; alla terza il tavolo sente il telaio. Non si
verificano con una regex ma con un **conteggio**, ed è esattamente la cosa che
un revisore umano non fa mai — perché dovrebbe contare — e che una macchina fa
gratis.

I tic si contano **solo nella prosa rivolta ai giocatori** (read-aloud, handout,
echi): in una tabella di CD o in una nota di regia le maiuscole e i trattini
sono legittimi, e contarli lì sarebbe rumore.

Uso:
    python3 scripts/validate_prosa.py                 # tutto il contenuto
    python3 scripts/validate_prosa.py FILE…           # solo questi
    python3 scripts/validate_prosa.py --strict        # i rilievi diventano errori
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENUTO = ("00_", "01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_",
             "10-stand-alone", "STANDALONE-", "campaign", "PG")

PARTI_DEL_CORPO = (r"man[oi]|braccia?|test[ae]|occhi?|respiro|cuore|petto|schien[ae]|"
                   r"voce|sguardo|gamb[ae]|piedi?|dita|vis[oi]|volt[oi]|spall[ae]|labbra|ginocchia")

# §1 — i calchi, in DUE famiglie, perché non sono la stessa cosa.
#
# SEMPRE: forme che non hanno nessun uso italiano legittimo. «realizzi che» è
# sbagliato in una nota di regia come in un read-aloud.
CALCHI_SEMPRE: list[tuple[str, str]] = [
    (rf"\brealizz(?:o|i|a|iamo|ate|ano|ato|ata)\s+(?:subito\s+|che\b)",
     "«realizzi che» → capisci / ti rendi conto (realizzare = portare a compimento)"),
    (r"\bassum(?:o|i|e|iamo|ete|ono)\s+che\b",
     "«assumi che» → dai per scontato / immagini (to assume ≠ assumere)"),
    (r"\b(?:la\s+sensazione|un\s+senso|il\s+senso)\s+di\s+\w+",
     "nominalizzazione all'inglese: l'italiano verbalizza («cadi», non «la sensazione di cadere»)"),
    (r"\beventualmente\b",
     "«eventualmente» = casomai, NON eventually → «prima o poi», «alla fine»"),
]

# SOLO NEL READ-ALOUD: calchi che dipendono dal REGISTRO. «Sta piovendo» è
# italiano corretto, e «la sua mano» in terza persona può servire a disambiguare.
# Diventano un difetto nella prosa che si legge ad alta voce al tavolo, che è
# il caso di cui parla `italiano-nativo.md` §1 («stai camminando» → «cammini»).
# Segnalarli ovunque produrrebbe centinaia di rilievi corretti in teoria e
# inutili in pratica — misurato: 256 alla prima passata, per lo più questi.
CALCHI_READ_ALOUD: list[tuple[str, str]] = [
    (rf"\b(?:l[aeoi]|il|gli)\s+(?:su[aoei]|tu[aoei]|mi[aoei]|loro)\s+(?:{PARTI_DEL_CORPO})\b",
     "possessivo su una parte del corpo: in italiano è già implicito («alzò la mano»)"),
    (r"\b(?:sto|stai|sta|stiamo|stat[ei]|stanno)\s+\w+(?:ando|endo)\b",
     "progressivo all'inglese: nel read-aloud basta il presente («cammini nel buio»)"),
]

# §9 — i tic. Non regex ma CONTEGGI: la soglia è il rilievo.
# L'antitesi si riconosce dalla FORMA, non dal verbo: frase che apre con «non»,
# breve, spezzata da due punti o da un trattone. La seconda metà può essere una
# copula («c'è PESO»), un verbo («cataloga») o un sostantivo («niente») — tutti
# e tre gli esempi di `italiano-nativo.md` §9.1, e vanno presi tutti.
ANTITESI = re.compile(
    r"(?:^|[.!?»]\s+|\*\s*)Non\s+[^.;:!?\n]{2,50}?\s*[:—–]\s*\S", re.M)
MAIUSCOLE = re.compile(r"\b[A-ZÀÈÉÌÒÙ]{3,}\b")
TRATTINO = re.compile(r"[—–]")
# Sigle e acronimi del repo: maiuscoli per necessità, non per enfasi.
SIGLE = {
    "CD", "GS", "PG", "PGS", "DM", "PNG", "SRD", "OGL", "XP", "PX", "TS", "CA", "BAB",
    "EL", "RD", "RI", "TPK", "ADR", "CI", "PDF", "HTML", "SVG", "JSON", "VTT", "AP",
    "DR", "PF1E", "RHOD", "NPC", "HP", "DV", "MO", "PP", "MA", "CR", "UVTT", "YAML",
    "CSS", "URL", "API", "MIT", "GPL", "IP", "FR", "SW", "NE", "NO", "SE", "II", "III",
    "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "XIII", "XIV", "XV", "XX",
}
SOGLIE = {"antitesi": 1, "maiuscole": 1}

GLOSSARIO = ROOT / "campaign" / "GLOSSARIO-E-LOCALIZZAZIONE.md"


def coppie_glossario() -> list[tuple[str, str]]:
    """(canonico italiano, forma inglese) per le voci che vanno TRADOTTE.

    Le righe marcate `DNT` (do-not-translate) si saltano: *Aegis Fang* e
    *Skullcrusher* sono inglesi per scelta e restano tali. Si saltano anche le
    righe di intestazione di sezione (colonna 1 in grassetto) e i casi in cui la
    forma inglese compare già dentro il nome canonico (`Valle di Channath /
    Cannath Vale`): lì l'inglese è una delle due forme accettate, non un calco.
    """
    if not GLOSSARIO.is_file():
        return []
    fuori: list[tuple[str, str]] = []
    for riga in GLOSSARIO.read_text(encoding="utf-8").splitlines():
        if not riga.strip().startswith("|"):
            continue
        celle = [c.strip() for c in riga.strip().strip("|").split("|")]
        if len(celle) < 3:
            continue
        it, en, nota = celle[0], celle[1], celle[2]
        if (it.startswith(("Italiano", "---", ":--", "**")) or "DNT" in nota
                or "invariat" in en.lower() or it == en or "·" in en or len(en) < 5
                or en.lower() in it.lower()):
            continue
        fuori.append((it, en))
    return fuori


PG = ("Thorik", "Tordek", "Hella", "Artemis", "Durik")

# Le forme brevi che il canone usa in prosa e che il glossario NON puo' dare,
# perche' li' i nomi stanno per esteso (o in inglese). Si estende a mano quando
# un artefatto prende un soprannome al tavolo: e' l'unico pezzo di questo file
# che sa qualcosa della campagna, ed e' voluto che si veda.
ALIAS = ("Anello", "Ascia", "Corona", "Bracieri", "Guanti", "Collana", "Cuore",
         "Sentinella", "Topazio", "Smeraldo", "Rubino", "Forgia", "Incudine")

# Parole che in un nome proprio non identificano niente da sole.
VUOTE = {"della", "delle", "degli", "dello", "dei", "del", "di", "da", "il", "la",
         "lo", "le", "gli", "of", "the", "and", "una", "uno", "in", "e"}


def nomi_canonici() -> list[str]:
    """Nomi del canone, **forme brevi comprese**.

    Un giocatore non scrive «Corona di Adamantio» in un eco: scrive «la Corona».
    Un controllo che pretende il nome per esteso da' il risultato rovesciato — e
    l'ha dato: segnalava l'hint di Artemis, che le ancore ha («l'Anello», «la
    Sentinella»), e lasciava passare quello di Hella, che non ne ha nessuna.
    Da qui: ogni voce del glossario contribuisce anche le sue **parole piene**.
    """
    fuori = set(PG) | set(ALIAS)
    if GLOSSARIO.is_file():
        for riga in GLOSSARIO.read_text(encoding="utf-8").splitlines():
            if not riga.strip().startswith("|"):
                continue
            celle = [c.strip() for c in riga.strip().strip("|").split("|")]
            if len(celle) < 2 or celle[0].startswith(("Italiano", "---", ":--", "**")):
                continue
            for pezzo in re.split(r"\s*[/·(«»]\s*", celle[0]):
                for parola in re.findall(r"[A-Za-zÀ-ÿ'’]{4,}", pezzo):
                    if parola.lower() not in VUOTE:
                        fuori.add(parola)
    return sorted(fuori)


_NOMI: list[str] | None = None


def check_ancore(f: Path, righe: list[tuple[int, str]], rel) -> list[str]:
    """Un testo per i giocatori senza un solo nome che loro riconoscano.

    Il caso: gli echi di Hella prima dello scontro con Terros. La giocatrice ha
    detto di **non capirci niente**, e `validate_prosa` sul resto era pulito —
    non era prosa, era progetto. Contate le ancore nella prosa dei quattro testi
    per-PG della stessa sessione: Tordek 8, Thorik 5, Artemis 4, **Hella 0**.
    Riceve «una testa grande, ossuta» (e' Durik) e «spalle larghe, oneste» (e'
    Thorik) senza nominarli mai.

    Quattro immagini non attribuite di fila non sono mistero: sono rumore. Un
    frammento evocativo si regge se chi legge puo' attaccarne **uno** a qualcosa
    che conosce. `module-standard` §5 vuole che un PG assente percepisca «solo
    echi»: li vuole **oscuri**, non **senza appigli**.
    """
    # Il controllo vale dove il glossario E' il canone. I moduli autoconclusivi
    # hanno il loro (il Drappo e' a Tarsilia, su Golarion: Vesca e Salle non
    # stanno in GLOSSARIO-E-LOCALIZZAZIONE.md, e non devono starci). Segnalarli
    # vorrebbe dire chiedere loro di citare un canone che non e' il loro.
    if any(x.startswith(("STANDALONE-", "10-stand-alone")) for x in f.parts):
        return []
    if f.name.upper().startswith("README"):
        return []
    global _NOMI
    if _NOMI is None:
        _NOMI = nomi_canonici()
    prosa = "\n".join(r for _, r in righe if not r.lstrip().startswith("#"))
    prosa = CONGEDO_DM.sub(" ", CAPPELLO_DM.sub(" ", prosa))
    if len(prosa.split()) < 90:
        return []
    # ⚠ Confronto CASE-SENSITIVE, e non e' un dettaglio: meta' delle forme brevi
    # del canone sono anche nomi comuni italiani. «batteva il cuore» non e' il
    # Cuore di Moradin, «voci di cristallo» non e' un artefatto. La maiuscola e'
    # cio' che distingue un nome proprio da una parola — ed e' l'unico segnale
    # affidabile che il testo offre. Senza, il controllo dava Hella per ancorata.
    if any(re.search(rf"\b{re.escape(n)}\b", prosa) for n in _NOMI):
        return []
    return [f"{rel}: testo per i giocatori **senza una sola ancora nominata** — "
            f"niente che chi legge riconosca. Un frammento evocativo si regge su "
            f"almeno un nome noto: senza, non e' mistero, e' rumore"]


_COPPIE: list[tuple[str, str]] | None = None


def check_glossario(f: Path, testo: str, rel) -> list[str]:
    """La forma inglese di un nome che il glossario vuole tradotto.

    È il rilievo che il tavolo ha fatto per primo — «prosa inglese» — nella sua
    forma più letterale e più facile da correggere: *Anvil of the World* dove il
    canone dice *Incudine del Mondo*.
    """
    global _COPPIE
    if _COPPIE is None:
        _COPPIE = coppie_glossario()
    if "GLOSSARIO" in f.name:
        return []
    fuori = []
    for it, en in _COPPIE:
        m = re.search(rf"\b{re.escape(en)}\b", testo)
        if m:
            n = testo[: m.start()].count("\n") + 1
            fuori.append(f"{rel}:{n}: forma inglese «{en}» — il canone è «{it}» (glossario §)")
    return fuori


# La prosa rivolta ai giocatori, in DUE forme.
#
# 1. Il **read-aloud** dentro un file qualunque: blockquote in corsivo.
# 2. Il **file intero**, quando il file *è* per i giocatori — un hint, un teaser,
#    un handout, una lettera, un eco. Lì non c'è un blockquote che marca la
#    prosa: la prosa è tutta la pagina.
#
# ⚠ Senza il secondo caso il controllo copriva **l'8-13%** di un file come
# `02-HINT-THORIK.md` (misurato: 29 parole su 353 dentro `> *…*`), ed è il
# motivo per cui i file che il tavolo aveva segnalato tornavano puliti.
READ_ALOUD = re.compile(r"^>\s*\*[^*].*$", re.M)

PER_I_GIOCATORI = re.compile(
    r"HINT-|TEASER|ECHI-|GIOCATORI|HANDOUT|LETTERA|PROFEZIA|AVVISO|PROP|^pg-",
    re.I)
# Anche dentro un file per i giocatori, questi sono per il DM: non si contano.
PER_IL_DM = re.compile(r"REGIA|GUIDA-DM|CASSETTA|DM-MASTER|STATBLOCCHI", re.I)

# Due cose che SEMBRANO enfasi e non lo sono, e che vanno tolte prima di contare.
#
# 1. L'etichetta di battuta: `**AEGIS FANG**, con quel tono…` — è il formato che
#    `editorial-standards.md` §2 IMPONE per i dialoghi (`**NOME (registro):**`).
#    Contarla come «maiuscola di portento» significa punire la convenzione del
#    repo, e un validatore che punisce la convenzione viene spento.
# 2. Il cappello per il giocatore: *«Per il giocatore di X. Leggi in privato…»* —
#    è un'istruzione del DM, non prosa di gioco.
# I due punti possono stare DENTRO il grassetto (`**I BRACIERI:**`) o fuori
# (`**AEGIS FANG**,`): il repo usa entrambe le forme, e sono la stessa cosa.
ETICHETTA_BATTUTA = re.compile(
    r"^>?\s*\*\*[A-ZÀ-Ù][A-ZÀ-Ù'’ \-]{1,30}[:：]?\*\*\s*[,(:]?", re.M)
# Il cappello sta su PIÙ righe di blockquote: si toglie il blocco intero, non la
# riga che contiene la frase-spia — altrimenti restano dentro le altre.
# Il congedo in coda — `> *(Niente meccanica, stanotte. …)*` — sta su piu' righe
# di blockquote: si toglie il BLOCCO, non la riga che apre la parentesi. Togliendo
# solo la prima restavano dentro le altre, e con loro i nomi che ci sono citati:
# un testo senza appigli risultava ancorato.
CONGEDO_DM = re.compile(r"(?:^>\s*\*?\(.*\n)(?:^>.*\n)*", re.M)
CAPPELLO_DM = re.compile(
    r"(?:^>.*\n)*?^>.*(?:per il giocatore|per la giocatrice|leggi in privato|non ci sono istruzioni"
    r"|affar tuo|ripasso lampo).*\n(?:^>.*\n)*",
    re.I | re.M)


def e_per_i_giocatori(f: Path) -> bool:
    """Vero se il file, per intero, è testo che i giocatori leggono."""
    if PER_IL_DM.search(f.name):
        return False
    return bool(PER_I_GIOCATORI.search(f.name)
                or "handout" in str(f).lower()
                or "templates/homebrew" in str(f).replace("\\", "/").lower())
CODE_FENCE = re.compile(r"^\s*```")
INLINE = re.compile(r"`[^`]*`|https?://\S+|\[[^\]]*\]\([^)]*\)|[\w./-]+\.(?:md|py|json|svg|html|typ)")


def prosa_e_readaloud(testo: str) -> tuple[list[tuple[int, str]], str]:
    """(righe di prosa numerate, testo dei soli read-aloud).

    Le tabelle si saltano: una riga `| CD 22 | ... |` non è prosa, e i tic
    contati lì sarebbero rumore.
    """
    righe: list[tuple[int, str]] = []
    fence = False
    for n, riga in enumerate(testo.splitlines(), 1):
        if CODE_FENCE.match(riga):
            fence = not fence
            continue
        if fence or riga.lstrip().startswith("|") or riga.startswith(("    ", "\t")):
            continue
        righe.append((n, INLINE.sub(lambda m: "x" * len(m.group(0)), riga)))
    return righe, "\n".join(READ_ALOUD.findall(testo))


def controlla(f: Path) -> list[str]:
    testo = f.read_text(encoding="utf-8", errors="ignore")
    rel = f.relative_to(ROOT) if ROOT in f.parents else f
    righe, readaloud = prosa_e_readaloud(testo)
    if e_per_i_giocatori(f):
        # Il file è per i giocatori: la prosa è tutta la pagina, non solo i box.
        # Restano fuori i titoli, che non sono prosa letta.
        readaloud = "\n".join(r for _, r in righe if not r.lstrip().startswith("#"))
    fuori: list[str] = check_glossario(f, testo, rel)
    if e_per_i_giocatori(f):
        fuori += check_ancore(f, righe, rel)

    for n, riga in righe:
        for pattern, perche in CALCHI_SEMPRE:
            m = re.search(pattern, riga, re.I)
            if m:
                fuori.append(f"{rel}:{n}: calco — {perche}  «…{m.group(0)}…»")

    if not readaloud.strip():
        return fuori

    for pattern, perche in CALCHI_READ_ALOUD:
        for m in re.finditer(pattern, readaloud, re.I):
            fuori.append(f"{rel}: read-aloud — {perche}  «…{m.group(0)}…»")

    n_ant = len(ANTITESI.findall(readaloud))
    if n_ant > SOGLIE["antitesi"]:
        fuori.append(
            f"{rel}: l'antitesi «non X: è Y» compare {n_ant} volte nei read-aloud "
            f"(massimo {SOGLIE['antitesi']} per documento): alla terza il tavolo sente il telaio"
        )
    ripulito = ETICHETTA_BATTUTA.sub(" ", CAPPELLO_DM.sub(" ", readaloud))
    portento = Counter(w for w in MAIUSCOLE.findall(ripulito) if w.upper() not in SIGLE)
    if len(portento) > SOGLIE["maiuscole"]:
        elenco = ", ".join(sorted(portento)[:6])
        fuori.append(
            f"{rel}: {len(portento)} parole in maiuscolo di enfasi nei read-aloud "
            f"({elenco}) — massimo {SOGLIE['maiuscole']}: se sono due, non funzionano più"
        )
    parole = len(readaloud.split())
    if parole >= 80:
        densita = TRATTINO.findall(readaloud)
        if len(densita) / parole > 0.03:
            fuori.append(
                f"{rel}: {len(densita)} trattini lunghi in {parole} parole di read-aloud "
                f"— il trattino come respiro è un tic: punto e virgola, due punti, o niente"
            )
    return fuori


def file_di_contenuto() -> list[Path]:
    out: list[Path] = []
    for d in ROOT.iterdir():
        if d.is_dir() and d.name.startswith(CONTENUTO):
            out.extend(p for p in d.rglob("*.md") if not p.name.endswith(".hb.md"))
    return sorted(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--strict", action="store_true",
                    help="i rilievi diventano errori (exit 1)")
    args = ap.parse_args(argv)

    bersagli = [Path(f).resolve() for f in args.files] if args.files else file_di_contenuto()
    rilievi: list[str] = []
    for f in bersagli:
        if f.is_file():
            rilievi += controlla(f)

    if not rilievi:
        print(f"✓ validate_prosa: {len(bersagli)} file — nessun calco, nessun tic oltre soglia")
        return 0
    testa = "✗" if args.strict else "  ⚠"
    print(f"{testa} validate_prosa: {len(rilievi)} rilievi in {len(bersagli)} file")
    for r in rilievi[:60]:
        print(f"  - {r}")
    if len(rilievi) > 60:
        print(f"  … e altri {len(rilievi) - 60}")
    if not args.strict:
        print("  (non bloccante: la norma è `italiano-nativo.md`, questo la misura)")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
