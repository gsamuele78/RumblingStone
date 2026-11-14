#!/usr/bin/env python3
"""
transcribe_session.py — dall'audio della serata alla BOZZA del log (ADR-0135).

Prova misurata, non adozione: la guida e' in
`docs/how-to/GUIDA-TRASCRIZIONE-SERATA.md`, la proposta in
`plans/RICERCA-TOOL-ESTERNI-DM-2026-08.md` §3 e §3.1.

Cosa fa:
  1. controlla il consenso del tavolo (`--consenso`), senza il quale non parte;
  2. converte l'audio in WAV 16 kHz mono con ffmpeg;
  3. lo trascrive in locale con whisper.cpp (`whisper-cli`), in italiano;
  4. scrive, FUORI dal repo, la trascrizione con i tempi e una bozza del log nel
     formato di `campaign/templates/session-template.md`.

Le sezioni pubbliche della bozza (Summary, Key decisions, XP, Loot, World
events, Hooks) restano VUOTE: le scrive il DM. La macchina mette solo, sotto
`## DM notes` (che `session_recap` taglia sempre), i momenti candidati con il
minuto e l'indice dei nomi, per ritrovare un punto dell'audio senza
riascoltarlo tutto. Il campo «Cosa hanno capito male» resta vuoto: richiede di
sapere cosa era vero, e lo scrive il DM a mano (§3.1).

Vincoli (§3, §3.1, ADR-0135):
  - consenso dei giocatori prima di registrare;
  - la bozza non e' mai canone: porta il segno `MARCATORE`, e con quel segno
    `state_apply` la rifiuta e `session_recap` la salta;
  - la trascrizione serve al DM, non sostituisce gli appunti dei giocatori;
  - l'audio, la trascrizione e i nomi dei giocatori non entrano mai nel repo:
    lo script si rifiuta di scrivere dentro il repo e la bozza nomina solo i PG.

Uso:
    python3 scripts/transcribe_session.py trascrivi SERATA.flac --consenso \\
        --out ~/RumblingStone-serate/2026-11-20 --modello ~/whisper.cpp/models/ggml-large-v3-turbo-q8_0.bin
    python3 scripts/transcribe_session.py bozza DIR/trascrizione.json --out DIR
    python3 scripts/transcribe_session.py misura GREZZA.txt CORRETTA.txt   # quanto resta buono
    python3 scripts/transcribe_session.py misura-bozza DIR/bozza-session.md

Degradazione: se `whisper-cli` o ffmpeg mancano, lo script dice come
installarli ed esce con codice 3, senza file a meta'. Solo stdlib; pyyaml
(ADR-0037) serve solo per leggere i nomi da `campaign/state.yaml`.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore.bozza_trascrizione import MARCATORE  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
STATE_YAML = REPO / "campaign" / "state.yaml"

#: Il modello consigliato per l'italiano su 6 GB di VRAM (guida §2).
MODELLO_PREDEFINITO = "ggml-large-v3-turbo-q8_0.bin"

ESCE_SENZA_STRUMENTI = 3

COME_INSTALLARE = """\
Manca {cosa}. Sul PC del DM (Bazzite) si installa in una distrobox:
  distrobox create --nvidia --name whisper --image registry.fedoraproject.org/fedora-toolbox:43
  distrobox enter whisper
  sudo dnf install -y git cmake gcc-c++ ffmpeg-free vulkan-headers vulkan-loader-devel glslc
  git clone https://github.com/ggml-org/whisper.cpp && cd whisper.cpp
  cmake -B build -DGGML_VULKAN=1 && cmake --build build -j --config Release
  sh models/download-ggml-model.sh large-v3-turbo-q8_0
Passi completi: docs/how-to/GUIDA-TRASCRIZIONE-SERATA.md"""

#: I momenti che la bozza segnala, per sezione del log. Sono un aiuto alla
#: lettura, non un'estrazione: la riga intera va riletta.
CATEGORIE: "dict[str, re.Pattern[str]]" = {
    "Bottino": re.compile(
        r"\bmonet|\bmo\b|\bmonete d'oro|\boro\b|\bargento\b|\bgemm|\bpozion|"
        r"\bpergamen|\bbacchett|\banello|\bmantell|\bamulet|\bbottino|\btesoro|"
        r"\bforziere|\bdividono|\bin parti uguali", re.I),
    "Punti esperienza": re.compile(
        r"\bpunti (?:di )?esperienza|\bpx\b|\bxp\b|\bsal\w* di livello|\blivello\b", re.I),
    "Clock e giorni": re.compile(
        r"\bmarch clock|\bclock\b|\bgiorno \w+|\brituale|\borologio|\balba\b|\bnotte\b", re.I),
    "Decisioni e fine serata": re.compile(
        r"\bdecid|\bscegli|\bscelt|\baccett|\brifiut|\bgiur|\bpromett|\bpatto\b|"
        r"\bci fermiamo|\bla prossima volta|\bprossima sessione|\bsi riparte", re.I),
}

# ------------------------------------------------------------------ percorsi


def dentro_il_repo(p: Path) -> bool:
    """Vero se `p` sta nel repo: audio e trascrizioni non ci entrano mai."""
    try:
        p.resolve().relative_to(REPO)
        return True
    except ValueError:
        return False


def trova_whisper(esplicito: "str | None") -> "str | None":
    if esplicito:
        return esplicito if Path(esplicito).is_file() else None
    for nome in ("whisper-cli", "whisper.cpp"):
        trovato = shutil.which(nome)
        if trovato:
            return trovato
    casa = Path.home() / "whisper.cpp" / "build" / "bin" / "whisper-cli"
    return str(casa) if casa.is_file() else None


def trova_modello(esplicito: "str | None") -> "Path | None":
    if esplicito:
        return Path(esplicito) if Path(esplicito).is_file() else None
    p = Path.home() / "whisper.cpp" / "models" / MODELLO_PREDEFINITO
    return p if p.is_file() else None


# ------------------------------------------------------------------ nomi


def _base(s: str) -> str:
    """minuscolo, senza accenti ne' apostrofi: «Zin'thara» → «zinthara»."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("'", "").replace("’", "")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]", " ", s)).strip()


def nomi_della_campagna(state_yaml: Path = STATE_YAML) -> "list[str]":
    """PG e PNG di `state.yaml`: il nome prima della parentesi, e i soprannomi
    fra «». Solo personaggi del gioco: i giocatori non ci sono."""
    try:
        import yaml  # ADR-0037
    except ImportError:
        print("[trascrivi] ⚠ pyyaml manca: niente nomi della campagna.", file=sys.stderr)
        return []
    if not state_yaml.is_file():
        return []
    dati = yaml.safe_load(state_yaml.read_text(encoding="utf-8")) or {}
    nomi: "list[str]" = []
    for pg in dati.get("party") or []:
        if pg.get("pg"):
            nomi.append(str(pg["pg"]).strip())
    for png in dati.get("png") or []:
        nome = str(png.get("nome") or "")
        nomi.extend(re.findall(r"«([^»]+)»", nome))
        testa = re.split(r"[(«/+]", nome)[0].strip()
        if testa and len(testa) <= 40:
            nomi.append(testa)
    visti: "set[str]" = set()
    unici = []
    for n in nomi:
        if n and _base(n) not in visti:
            visti.add(_base(n))
            unici.append(n)
    return unici


def prompt_dei_nomi(nomi: "list[str]", limite: int = 600) -> str:
    """Il prompt iniziale di whisper: orienta la grafia dei nomi propri.
    whisper ne tiene circa 224 token; oltre si taglia."""
    testo = "Sessione di D&D in Faerûn. Nomi: "
    for n in nomi:
        if len(testo) + len(n) + 2 > limite:
            break
        testo += n + ", "
    return testo.rstrip(", ") + "."


def nomi_nella_riga(riga: str, nomi: "list[str]", soglia: float = 0.8) -> "list[str]":
    """I nomi che la riga contiene, anche storpiati («Gaurush» → Ghaurush).
    Confronta parola per parola, e coppie di parole per i nomi doppi."""
    parole = _base(riga).split()
    trovati = []
    for nome in nomi:
        pezzi = _base(nome).split()
        if not pezzi:
            continue
        n = len(pezzi)
        bersaglio = " ".join(pezzi)
        if len(bersaglio) < 4:
            continue
        for i in range(len(parole) - n + 1):
            candidato = " ".join(parole[i:i + n])
            if difflib.SequenceMatcher(None, candidato, bersaglio).ratio() >= soglia:
                trovati.append(nome)
                break
    return trovati


# ------------------------------------------------------------------ trascrizione


def segmenti(json_whisper: Path) -> "list[tuple[str, str]]":
    """(hh:mm:ss, testo) dal JSON di `whisper-cli -oj`."""
    dati = json.loads(json_whisper.read_text(encoding="utf-8"))
    out = []
    for s in dati.get("transcription", []):
        t = s.get("timestamps", {}).get("from", "00:00:00,000").split(",")[0]
        testo = s.get("text", "").strip()
        if testo:
            out.append((t, testo))
    return out


def trascrivi(args) -> int:
    if not args.consenso:
        print("[trascrivi] ✗ Serve --consenso: conferma che TUTTI i giocatori al tavolo "
              "hanno accettato la registrazione prima che partisse (ADR-0135).",
              file=sys.stderr)
        return 2
    audio = Path(args.audio).expanduser()
    out = Path(args.out).expanduser()
    if dentro_il_repo(out) or dentro_il_repo(audio):
        print("[trascrivi] ✗ Audio e trascrizione non entrano mai nel repo: "
              "scegli una cartella fuori (es. ~/RumblingStone-serate/DATA).", file=sys.stderr)
        return 2
    if not audio.is_file():
        print(f"[trascrivi] ✗ {audio} non esiste.", file=sys.stderr)
        return 2
    whisper = trova_whisper(args.whisper)
    ffmpeg = shutil.which("ffmpeg")
    modello = trova_modello(args.modello)
    for manca, cosa in ((not whisper, "whisper-cli (whisper.cpp)"), (not ffmpeg, "ffmpeg"),
                        (not modello, f"il modello ({args.modello or MODELLO_PREDEFINITO})")):
        if manca:
            print(COME_INSTALLARE.format(cosa=cosa), file=sys.stderr)
            return ESCE_SENZA_STRUMENTI

    out.mkdir(parents=True, exist_ok=True)
    wav = out / "audio-16k.wav"
    subprocess.run([ffmpeg, "-v", "error", "-y", "-i", str(audio), "-ar", "16000", "-ac", "1",
                    "-c:a", "pcm_s16le", str(wav)], check=True)
    durata = wav.stat().st_size / (16000 * 2)

    comando = [whisper, "-m", str(modello), "-l", "it", "-f", str(wav),
               "-oj", "-otxt", "-osrt", "-of", str(out / "trascrizione"), "-np"]
    if args.thread:
        comando += ["-t", str(args.thread)]
    nomi = nomi_della_campagna()
    if nomi and args.nomi_nel_prompt:
        # Il prompt vive nel contesto del testo precedente: con `-mc 0` whisper
        # lo ignora (misurato: trascrizioni identiche). Le due cose si escludono.
        comando += ["--prompt", prompt_dei_nomi(nomi)]
        print("[trascrivi] ⚠ nomi nel prompt: il contesto resta acceso, e whisper "
              "puo' saltare frasi ripetute (MISURE.md di ADR-0135).", file=sys.stderr)
    else:
        # Senza il testo precedente come contesto whisper non salta le frasi
        # che somigliano a quelle gia' dette: su FLEURS 16,6% → 5,8% di parole sbagliate.
        comando += ["-mc", "0"]
    if args.vad_modello:
        comando += ["--vad", "-vm", str(Path(args.vad_modello).expanduser())]
    print(f"[trascrivi] whisper.cpp su {durata / 60:.1f} minuti di audio…")
    t0 = time.monotonic()
    esito = subprocess.run(comando)
    secondi = time.monotonic() - t0
    if esito.returncode != 0:
        print(f"[trascrivi] ✗ whisper-cli e' uscito con {esito.returncode}.", file=sys.stderr)
        return esito.returncode
    if not args.tieni_wav:
        wav.unlink(missing_ok=True)

    nel_prompt = bool(nomi and args.nomi_nel_prompt)
    meta = {"data": args.data or date.today().isoformat(), "modello": Path(modello).name,
            "nomi_nel_prompt": nel_prompt, "contesto_precedente": nel_prompt,
            "vad": bool(args.vad_modello),
            "minuti_audio": round(durata / 60, 1), "minuti_trascrizione": round(secondi / 60, 1),
            "volte_il_tempo_reale": round(durata / secondi, 2) if secondi else None}
    (out / "misura.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8")
    scrivi_bozza(out / "trascrizione.json", out, meta["data"], nomi)
    print(f"[trascrivi] ✓ {meta['minuti_audio']} min in {meta['minuti_trascrizione']} min "
          f"({meta['volte_il_tempo_reale']}× il tempo reale). Bozza: {out / 'bozza-session.md'}")
    return 0


# ------------------------------------------------------------------ bozza


def componi_bozza(segs: "list[tuple[str, str]]", data: str, nomi: "list[str]") -> str:
    righe = [
        MARCATORE,
        f"> ⚠️ **BOZZA dalla trascrizione automatica del {data}. Non è canone** "
        "(ADR-0007, ADR-0135). Il DM la legge, scrive le sezioni e firma il log con "
        "`python3 scripts/dm.py session end`; questa riga e quella sopra si tolgono solo allora.",
        "> La trascrizione serve al DM: non sostituisce gli appunti dei giocatori.",
        "",
        f"# Session N — [Titolo] ({data})",
        "",
        "**Players present**: [solo i nomi dei PG, mai quelli dei giocatori]",
        "**Location**: [da scrivere: DM]",
        "**In-world dates**: [da scrivere: DM]",
        "**Session XP budget**: [da scrivere: DM]",
        "",
    ]
    for sez in ("Summary", "Key decisions", "XP awarded", "Loot distributed",
                "World events triggered", "Next session hooks"):
        righe += [f"## {sez}", "", "[da scrivere: DM]", ""]
    righe += [
        "## DM notes (private — optional)",
        "",
        "### Cosa hanno capito male",
        "",
        "> A mano: la trascrizione non sa cosa era vero (RICERCA-TOOL-ESTERNI §3.1).",
        "> Sono i ganci regalati dal tavolo, non errori da correggere.",
        "",
        "- ",
        "",
        "### Momenti candidati dalla trascrizione",
        "",
        "> Spunta `[x]` le righe che ti sono servite per scrivere il log: è la misura "
        "(`transcribe_session.py misura-bozza`).",
        "",
    ]
    for cat, regex in CATEGORIE.items():
        trovati = [(t, s) for t, s in segs if regex.search(s)]
        righe += [f"#### {cat}", ""]
        righe += [f"- [ ] `{t}` {s}" for t, s in trovati] or ["- (nessuna riga)"]
        righe.append("")
    indice: "dict[str, list[str]]" = {}
    for t, s in segs:
        for n in nomi_nella_riga(s, nomi):
            indice.setdefault(n, []).append(t)
    righe += ["### Indice dei nomi", ""]
    righe += [f"- **{n}**: " + ", ".join(f"`{t}`" for t in ts)
              for n, ts in sorted(indice.items())] or ["- (nessun nome riconosciuto)"]
    return "\n".join(righe).rstrip() + "\n"


def scrivi_bozza(json_whisper: Path, out: Path, data: str,
                 nomi: "list[str] | None" = None) -> Path:
    if nomi is None:
        nomi = nomi_della_campagna()
    testo = componi_bozza(segmenti(json_whisper), data, nomi)
    dest = out / "bozza-session.md"
    tmp = dest.with_suffix(".tmp")
    tmp.write_text(testo, encoding="utf-8")
    os.replace(tmp, dest)
    return dest


def cmd_bozza(args) -> int:
    out = Path(args.out).expanduser()
    if dentro_il_repo(out):
        print("[bozza] ✗ la bozza si scrive fuori dal repo.", file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    dest = scrivi_bozza(Path(args.json).expanduser(), out, args.data or date.today().isoformat())
    print(f"[bozza] ✓ {dest}")
    return 0


# ------------------------------------------------------------------ misura


def _parole(testo: str) -> "list[str]":
    return _base(testo).split()


def distanza(rif: "list[str]", ipo: "list[str]") -> int:
    """Distanza di Levenshtein fra le due sequenze di parole."""
    prec = list(range(len(ipo) + 1))
    for i, r in enumerate(rif, 1):
        cur = [i] + [0] * len(ipo)
        for j, h in enumerate(ipo, 1):
            cur[j] = min(prec[j] + 1, cur[j - 1] + 1, prec[j - 1] + (r != h))
        prec = cur
    return prec[-1]


def misura_testi(grezza: str, corretta: str, nomi: "list[str]") -> dict:
    """Quanto della trascrizione grezza resta dopo la correzione del DM.

    - `wer`: errori di parola (sostituzioni+cancellazioni+inserzioni) / parole corrette;
    - `parole_buone`: 1 - wer, la parte che il DM non ha dovuto toccare;
    - `nomi`: per ogni nome della campagna presente nella versione corretta,
      quante volte la grezza lo scrive giusto (stessa grafia, senza accenti).
    """
    rif, ipo = _parole(corretta), _parole(grezza)
    d = distanza(rif, ipo)
    wer = d / len(rif) if rif else 0.0
    giusti = attesi = inventati = 0
    dettaglio = {}
    for nome in nomi:
        b = _base(nome)
        if len(b) < 4:
            continue
        pat = re.compile(rf"\b{re.escape(b)}\b")
        nr, ng = len(pat.findall(" ".join(rif))), len(pat.findall(" ".join(ipo)))
        if nr or ng:
            dettaglio[nome] = {"corretta": nr, "grezza": ng}
            attesi += nr
            giusti += min(nr, ng)
            inventati += max(0, ng - nr)
    return {"parole_corrette": len(rif), "errori": d, "wer": round(wer, 3),
            "parole_buone": round(max(0.0, 1 - wer), 3),
            "nomi_attesi": attesi, "nomi_giusti": giusti, "nomi_inventati": inventati,
            "nomi": dettaglio}


def cmd_misura(args) -> int:
    nomi = nomi_della_campagna()
    if args.nomi:
        nomi += [n.strip() for n in Path(args.nomi).read_text(encoding="utf-8").splitlines()
                 if n.strip()]
    m = misura_testi(Path(args.grezza).read_text(encoding="utf-8"),
                     Path(args.corretta).read_text(encoding="utf-8"), nomi)
    print(json.dumps(m, ensure_ascii=False, indent=2))
    return 0


def misura_bozza(testo: str) -> dict:
    spuntate = len(re.findall(r"^- \[[xX]\] ", testo, re.M))
    tutte = spuntate + len(re.findall(r"^- \[ \] ", testo, re.M))
    return {"righe_candidate": tutte, "spuntate": spuntate,
            "quota_utile": round(spuntate / tutte, 3) if tutte else None}


def cmd_misura_bozza(args) -> int:
    print(json.dumps(misura_bozza(Path(args.bozza).read_text(encoding="utf-8")), indent=2))
    return 0


# ------------------------------------------------------------------ cli


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("trascrivi", help="audio → trascrizione + bozza, fuori dal repo")
    t.add_argument("audio")
    t.add_argument("--out", required=True, help="cartella FUORI dal repo")
    t.add_argument("--consenso", action="store_true",
                   help="tutti i giocatori hanno accettato la registrazione prima che partisse")
    t.add_argument("--data", help="data della serata (default: oggi)")
    t.add_argument("--whisper", help="percorso di whisper-cli")
    t.add_argument("--modello", help=f"modello ggml (default ~/whisper.cpp/models/{MODELLO_PREDEFINITO})")
    t.add_argument("--vad-modello", help="modello Silero VAD ggml: salta i silenzi")
    t.add_argument("--nomi-nel-prompt", action="store_true",
                   help="passa a whisper i nomi di state.yaml; riaccende il contesto (prova A/B: guida §4)")
    t.add_argument("--thread", type=int)
    t.add_argument("--tieni-wav", action="store_true")
    t.set_defaults(func=trascrivi)

    b = sub.add_parser("bozza", help="rifà la bozza da una trascrizione JSON già fatta")
    b.add_argument("json")
    b.add_argument("--out", required=True)
    b.add_argument("--data")
    b.set_defaults(func=cmd_bozza)

    m = sub.add_parser("misura", help="trascrizione grezza contro quella corretta dal DM")
    m.add_argument("grezza")
    m.add_argument("corretta")
    m.add_argument("--nomi", help="file con altri nomi da contare, uno per riga")
    m.set_defaults(func=cmd_misura)

    mb = sub.add_parser("misura-bozza", help="quante righe candidate il DM ha usato")
    mb.add_argument("bozza")
    mb.set_defaults(func=cmd_misura_bozza)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
