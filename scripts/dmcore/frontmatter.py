"""frontmatter.py — il blocco dati in testa a un log di sessione (ADR-0017, G2-ter).

Perché esiste
  Fino al 2026-08-05 `state_sync.extract_events` ricavava i delta di fine
  sessione con **regex sulla prosa**: `\\*\\*March Clock\\*\\*: Day (\\d+) → Day (\\d+)`,
  e per i villain una lista di nomi cablata nel sorgente. Funziona finché il DM
  scrive esattamente in quel modo, e finché il villain è fra quelli previsti —
  cioè finché non serve davvero.

  Il front-matter sposta i delta da «prosa da interpretare» a «dati da leggere».
  Il DM non lo scrive a mano: lo emette `session_wizard`, che quelle risposte le
  ha già raccolte in forma strutturata.

Forma
  ---
  sessione: 4
  data: 2026-08-10
  delta:
    march_clock: {da: 19, a: 20}
    villain_clock:
      - {villain: Sonjak, da: "4/8", a: "5/8"}
    xp_a_testa: 3200
  ---
  # Session 4 — … (il log narrativo, invariato)

Compatibilità
  Un log **senza** front-matter resta valido: `extract_events` ricade sulle
  regex di prima. Nessuna sessione già scritta va riscritta.
"""
from __future__ import annotations

import re

FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def split(text: str) -> "tuple[dict | None, str]":
    """(dati, corpo). `dati` è None se il file non ha front-matter.

    Se pyyaml manca, il front-matter viene ignorato e si ricade sul corpo:
    meglio degradare al comportamento precedente che rompere il flusso di
    fine sessione per una dipendenza.
    """
    m = FM_RE.match(text)
    if not m:
        return None, text
    try:
        import yaml
    except ImportError:  # pragma: no cover
        return None, text
    try:
        data = yaml.safe_load(m.group(1))
    except Exception:
        return None, text
    if not isinstance(data, dict):
        return None, text
    return data, text[m.end():]


def deltas(data: "dict | None") -> list[tuple]:
    """Normalizza `delta:` nella forma (nome, raw, groups) usata da extract_events.

    Tenere la stessa forma dei trigger regex è deliberato: `state_apply` non
    deve sapere da dove vengono i delta, e i due percorsi restano confrontabili.
    """
    if not data:
        return []
    d = data.get("delta") or {}
    hits: list[tuple] = []

    mc = d.get("march_clock")
    if isinstance(mc, dict) and mc.get("da") is not None and mc.get("a") is not None:
        hits.append(("march_clock", f"March Clock: Day {mc['da']} → Day {mc['a']}",
                     (str(mc["da"]), str(mc["a"]))))

    rc = d.get("ritual_clock")
    if isinstance(rc, dict) and rc.get("da") is not None and rc.get("a") is not None:
        a, b = str(rc["da"]).split("/")[0], str(rc["a"]).split("/")[0]
        hits.append(("ritual_clock", f"Ritual Clock: {rc['da']} → {rc['a']}", (a, b)))

    for v in d.get("villain_clock") or []:
        if not isinstance(v, dict) or "villain" not in v:
            continue
        hits.append(("villain_clock",
                     f"{v['villain']}: {v.get('da')} → {v.get('a')}",
                     (v["villain"], str(v.get("da", "")), str(v.get("a", "")))))

    return hits
