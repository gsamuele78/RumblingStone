#!/usr/bin/env python3
"""
state_apply.py — applica a campaign/state.md le proposte meccaniche di
state_sync.py, SOLO dentro le regioni marcate `auto:` (ADR-0007).

Divisione dei ruoli (piano AUTOMAZIONE §3):
  - `state_sync.py`  rileva i trigger nei session log e PROPONE (invariato);
  - questo script APPLICA il sottoinsieme meccanico delle proposte, con
    diff a video e conferma per blocco, dentro le regioni marcate;
  - tutto il resto (prosa, tabelle villain, §1 party) resta proposta da
    applicare a mano: viene stampato, mai toccato.

Regioni gestite (v1):
  march-clock   righe "Current March Day" / "Days remaining" (§2.1)
  changelog     blocco append-only del §8

Uso:
    python3 scripts/state_apply.py --migrate            # inserisce i marker (una tantum, idempotente)
    python3 scripts/state_apply.py --session FILE.md    # proponi+applica dagli eventi di un log
    python3 scripts/state_apply.py --session FILE.md --check   # solo diff, niente scritture
    python3 scripts/state_apply.py --session FILE.md --yes --commit

Sicurezza (ADR-0007): guardia branch (mai su main); rifiuta se state.md ha
modifiche non committate (così `git revert` è sempre pulito); qualsiasi
anomalia di parsing → nessuna scrittura, restano le proposte a video.
`--no-guard` esiste SOLO per i test su repository temporanei.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dmcore import REPO  # noqa: E402
from dmcore import config as cfg  # noqa: E402
from dmcore import gitio  # noqa: E402
from dmcore.regions import RegionError, find_regions, replace_region, wrap  # noqa: E402
from state_sync import extract_events, _suggest  # noqa: E402

STATE_REL = Path("campaign") / "state.md"
# Lo storico è uscito da state.md §8 il 2026-08-05 (ADR-0017): la regione
# `changelog` vive ora nel proprio file, e `state_apply` la segue lì.
CHANGELOG_REL = Path("campaign") / "state-changelog.md"
STATE_YAML_REL = Path("campaign") / "state.yaml"

# Un `clock:` dentro una voce di `villain:` in state.yaml.
_VILLAIN_ENTRY_RE = re.compile(r"^- villain: (.+)$", re.M)


def set_villain_clock(text: str, villain: str, new_clock: str) -> "str | None":
    """Aggiorna `clock:` della voce villain indicata. None se non la trova.

    Modifica **testuale e mirata**, non un round-trip YAML: `yaml.dump`
    riscriverebbe il file perdendo l'intestazione commentata, che in
    `state.yaml` spiega il contratto a chi lo apre. Qui cambia una riga e il
    resto resta byte-identico — stessa filosofia delle regioni marcate.
    """
    entries = list(_VILLAIN_ENTRY_RE.finditer(text))
    for i, m in enumerate(entries):
        nome = m.group(1).strip().strip("'\"")
        if villain.lower() not in nome.lower():
            continue
        end = entries[i + 1].start() if i + 1 < len(entries) else len(text)
        blocco = text[m.start():end]
        nuovo, n = re.subn(r"^(\s*clock:\s*).*$",
                           lambda mm: mm.group(1) + new_clock,
                           blocco, count=1, flags=re.M)
        if n == 0:
            return None
        return text[:m.start()] + nuovo + text[end:]
    return None
SESSIONS_REL = Path("campaign") / "sessions"

#: Day di arrivo dell'orda a Rethmar (waypoint finale §2.1 — canone RHoD adattato).
RETHMAR_DAY = 42

MARCH_DAY_RE = re.compile(r"\*\*Current March Day:\*\*\s*\*\*(\d+)\*\*")
DAYS_LEFT_RE = re.compile(r"\*\*Days remaining to Rethmar:\*\*")
FENCE_RE = re.compile(r"^```", re.M)


# ------------------------------------------------------------------ migrate


def migrate(text: str) -> "tuple[str, list[str]]":
    """Avvolge nei marker le zone gestite. Idempotente: salta le regioni
    già presenti. Ritorna (testo, regioni aggiunte)."""
    added: list[str] = []
    existing = find_regions(text)

    if "march-clock" not in existing:
        m = MARCH_DAY_RE.search(text)
        if not m:
            raise RegionError("riga '**Current March Day:**' non trovata: "
                              "impossibile migrare la regione march-clock")
        start = text.rfind("\n", 0, m.start()) + 1
        # la regione copre la riga del Day e l'eventuale riga Days remaining
        end = text.find("\n", m.end()) + 1
        m2 = DAYS_LEFT_RE.search(text, end)
        if m2 and m2.start() == end:  # riga immediatamente successiva
            end = text.find("\n", m2.end()) + 1
        text = text[:start] + wrap("march-clock", text[start:end]) + "\n" + text[end:]
        added.append("march-clock")

    return text, added


def migrate_changelog(text: str) -> "tuple[str, list[str]]":
    """Avvolge nel marker `changelog` l'ULTIMO blocco fenced di
    `campaign/state-changelog.md`. Idempotente.

    Lo storico è uscito da `state.md` §8 con ADR-0017; la semantica di
    append resta identica, cambia solo il file che la ospita.
    """
    added: list[str] = []
    if "changelog" in find_regions(text):
        return text, added
    fences = list(FENCE_RE.finditer(text))
    if len(fences) < 2:
        raise RegionError("nessun blocco ``` in state-changelog.md: "
                          "impossibile migrare la regione changelog")
    start = fences[-2].start()
    end = text.find("\n", fences[-1].end()) + 1
    text = text[:start] + wrap("changelog", text[start:end]) + "\n" + text[end:]
    added.append("changelog")
    return text, added


# ------------------------------------------------------------------ apply


def apply_march_clock(text: str, new_day: int, session_label: str) -> str:
    content = (
        f"**Current March Day:** **{new_day}** "
        f"(aggiornato da `state_apply` — {session_label}).\n"
        f"**Days remaining to Rethmar:** **{RETHMAR_DAY - new_day}** "
        f"(arrivo dell'orda a Rethmar: Day {RETHMAR_DAY}).\n"
    )
    return replace_region(text, "march-clock", content)


def append_changelog(text: str, line: str) -> str:
    regions = find_regions(text)
    if "changelog" not in regions:
        raise RegionError("regione 'changelog' assente — lancia --migrate")
    content = regions["changelog"].content(text)
    fences = list(FENCE_RE.finditer(content))
    if len(fences) < 2:
        raise RegionError("regione changelog malformata (fence ``` mancanti)")
    close = fences[-1].start()
    new_content = content[:close] + line.rstrip("\n") + "\n" + content[close:]
    return replace_region(text, "changelog", new_content)


def _diff(old: str, new: str, label: str) -> str:
    return "".join(difflib.unified_diff(
        old.splitlines(keepends=True), new.splitlines(keepends=True),
        fromfile=f"a/{label}", tofile=f"b/{label}", n=2))


def _confirm(prompt: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    try:
        return input(f"{prompt} [s/N] ").strip().lower() in ("s", "y", "si", "sì", "yes")
    except EOFError:
        return False


# ------------------------------------------------------------------ main


def run(repo: Path, session_name: "str | None", check: bool, assume_yes: bool,
        do_commit: bool, no_guard: bool) -> int:
    state_path = repo / STATE_REL
    sessions = repo / SESSIONS_REL

    if not no_guard:
        group = cfg.load_group(repo)
        try:
            gitio.guard_canon_branch(
                repo, expected=cfg.group_branch(group) if group else None)
        except gitio.BranchGuardError as exc:
            print(f"[apply] ✗ {exc}", file=sys.stderr)
            return 1
        if not check:
            import subprocess
            dirty = subprocess.run(
                ["git", "-C", str(repo), "status", "--porcelain", "--", str(STATE_REL)],
                capture_output=True, text=True).stdout.strip()
            if dirty:
                print("[apply] ✗ campaign/state.md ha modifiche non committate: "
                      "committa (o scarta) prima, così l'undo resta `git revert` "
                      "(ADR-0007 vincolo 4)", file=sys.stderr)
                return 1

    if session_name:
        spath = sessions / session_name
        if not spath.exists():
            print(f"[apply] ✗ sessione non trovata: {spath}", file=sys.stderr)
            return 2
    else:
        cands = sorted(sessions.glob("????-??-??_session-*.md"))
        if not cands:
            print(f"[apply] ✗ nessun log di sessione in {sessions}", file=sys.stderr)
            return 2
        spath = cands[-1]
    ev = extract_events(spath)
    print(f"[apply] sessione: {ev['file']} ({ev['date']}) — trigger: {len(ev['hits'])}")

    text = state_path.read_text(encoding="utf-8")
    original = text
    clog_path = repo / CHANGELOG_REL
    clog = clog_path.read_text(encoding="utf-8") if clog_path.exists() else None
    clog_original = clog
    syaml_path = repo / STATE_YAML_REL
    syaml = syaml_path.read_text(encoding="utf-8") if syaml_path.exists() else None
    syaml_original = syaml
    applied: list[str] = []
    manual: list[str] = []
    session_label = f"sessione {ev['date']} ({ev['file']})"

    for name, raw, groups in ev["hits"]:
        if name == "march_clock":
            a, b = int(groups[0]), int(groups[1])
            if a == b:
                continue
            try:
                candidate = apply_march_clock(text, b, session_label)
            except RegionError as exc:
                print(f"[apply] ⚠ march_clock non applicabile ({exc}) — resta manuale")
                manual.append(_suggest(name, groups))
                continue
            if candidate == text:
                print(f"[apply] march-clock già a Day {b} — niente da fare (idempotente)")
                continue
            print(f"\n[apply] proposta march-clock: Day {a} → Day {b}")
            print(_diff(text, candidate, str(STATE_REL)) or "  (nessuna differenza)")
            if _confirm("[apply] applico questo blocco?", assume_yes):
                text = candidate
                applied.append(f"March Clock Day {a} → Day {b}")
            else:
                manual.append(_suggest(name, groups))
        elif name == "villain_clock" and len(groups) == 3 and syaml is not None:
            villain, da, a = groups
            if not a or da == a:
                continue
            candidate = set_villain_clock(syaml, villain, a)
            if candidate is None:
                print(f"[apply] ⚠ villain «{villain}» non trovato in {STATE_YAML_REL} — resta manuale")
                manual.append(_suggest(name, groups))
                continue
            if candidate == syaml:
                print(f"[apply] clock di {villain} già a {a} — niente da fare (idempotente)")
                continue
            print(f"\n[apply] proposta clock villain: {villain} {da} → {a}")
            print(_diff(syaml, candidate, str(STATE_YAML_REL)))
            if _confirm("[apply] applico questo blocco?", assume_yes):
                syaml = candidate
                applied.append(f"clock {villain} {da} → {a}")
            else:
                manual.append(_suggest(name, groups))
        elif name == "ritual_clock" and groups[0] == groups[1]:
            continue  # nessun cambiamento: niente rumore
        else:
            manual.append(_suggest(name, groups))

    if applied:
        entry = (f"{date.today().isoformat()}  {session_label}: "
                 + "; ".join(applied) + " (state_apply).")
        if clog is None:
            print(f"[apply] ⚠ {CHANGELOG_REL} assente — annota lo storico a mano")
        else:
            try:
                candidate = append_changelog(clog, entry)
                print(f"\n[apply] proposta storico ({CHANGELOG_REL}):")
                print(_diff(clog, candidate, str(CHANGELOG_REL)))
                if _confirm("[apply] appendo allo storico?", assume_yes):
                    clog = candidate
            except RegionError as exc:
                print(f"[apply] ⚠ storico non applicabile ({exc}) — "
                      f"aggiorna {CHANGELOG_REL} a mano")

    if manual:
        print("\n[apply] proposte NON meccaniche — applicale a mano in state.md:")
        for line in manual:
            print(line)

    if text == original and clog == clog_original and syaml == syaml_original:
        print("\n[apply] ✓ niente da scrivere (già allineato o tutto rifiutato)")
        return 0
    if check:
        print("\n[apply] --check: nessuna scrittura eseguita")
        return 0

    if text != original:
        state_path.write_text(text, encoding="utf-8")
        print(f"\n[apply] ✓ scritto {state_path}")
    if clog is not None and clog != clog_original:
        clog_path.write_text(clog, encoding="utf-8")
        print(f"[apply] ✓ scritto {clog_path}")
    if syaml is not None and syaml != syaml_original:
        syaml_path.write_text(syaml, encoding="utf-8")
        print(f"[apply] ✓ scritto {syaml_path}")
        # la vista markdown va rigenerata, altrimenti state.md resta indietro
        # e il gate render_state --check diventa rosso (ADR-0017).
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            import render_state
            render_state.main([])
        except Exception as exc:  # pragma: no cover
            print(f"[apply] ⚠ rigenera a mano la vista: python3 scripts/render_state.py ({exc})")
    if do_commit:
        sha = gitio.commit_paths(
            repo, [str(STATE_REL)],
            f"state: {'; '.join(applied) or 'sync'} — {session_label} [state_apply]")
        print(f"[apply] ✓ commit {sha}" if sha else "[apply] (nulla da committare)")
    else:
        print("[apply] ricordati il commit: git add campaign/state.md && git commit")
    return 0


def main(argv: "list[str] | None" = None) -> int:
    ap = argparse.ArgumentParser(
        description="Applica le proposte meccaniche a state.md dentro le "
                    "regioni marcate auto: (ADR-0007).")
    ap.add_argument("--migrate", action="store_true",
                    help="inserisce i marker auto: in state.md (idempotente)")
    ap.add_argument("--session", help="file sotto campaign/sessions/ (default: l'ultimo)")
    ap.add_argument("--check", action="store_true", help="solo diff, nessuna scrittura")
    ap.add_argument("--yes", action="store_true", help="applica senza chiedere conferma")
    ap.add_argument("--commit", action="store_true", help="committa state.md dopo l'applicazione")
    ap.add_argument("--no-guard", action="store_true",
                    help="salta guardia branch e check working-tree (SOLO test)")
    ap.add_argument("--repo-root", type=Path, default=REPO, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    repo = args.repo_root.resolve()

    if args.migrate:
        state_path = repo / STATE_REL
        clog_path = repo / CHANGELOG_REL
        text = state_path.read_text(encoding="utf-8")
        clog = clog_path.read_text(encoding="utf-8") if clog_path.exists() else None
        try:
            new_text, added = migrate(text)
            new_clog, added_c = (migrate_changelog(clog) if clog is not None else (None, []))
        except RegionError as exc:
            print(f"[apply] ✗ migrazione fallita: {exc}", file=sys.stderr)
            return 1
        added = added + added_c
        if not added:
            print("[apply] ✓ marker già presenti — niente da fare")
            return 0
        if args.check:
            print(_diff(text, new_text, str(STATE_REL)))
            if new_clog is not None:
                print(_diff(clog, new_clog, str(CHANGELOG_REL)))
            print("[apply] --check: nessuna scrittura eseguita")
            return 0
        if not args.no_guard:
            group = cfg.load_group(repo)
            try:
                gitio.guard_canon_branch(
                    repo, expected=cfg.group_branch(group) if group else None)
            except gitio.BranchGuardError as exc:
                print(f"[apply] ✗ {exc}", file=sys.stderr)
                return 1
        state_path.write_text(new_text, encoding="utf-8")
        if new_clog is not None and added_c:
            clog_path.write_text(new_clog, encoding="utf-8")
        print(f"[apply] ✓ marker inseriti: {', '.join(added)}")
        if args.commit:
            sha = gitio.commit_paths(repo, [str(STATE_REL), str(CHANGELOG_REL)],
                                     "state: migrazione marker auto: (ADR-0007)")
            print(f"[apply] ✓ commit {sha}" if sha else "[apply] (nulla da committare)")
        return 0

    return run(repo, args.session, args.check, args.yes, args.commit, args.no_guard)


if __name__ == "__main__":
    raise SystemExit(main())
