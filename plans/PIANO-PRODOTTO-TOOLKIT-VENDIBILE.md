# PIANO — DA REPO DI CAMPAGNA A PRODOTTO VENDIBILE

> **Cos'è**: il piano completo per trasformare il toolkit (`scripts/`, renderer,
> legenda, schemi) in un **prodotto professionale, riusabile e vendibile**,
> multi-sistema (D&D 3.5 · Pathfinder 1e · D&D 5e), senza toccare la campagna.
>
> **Decisioni DM del 2026-07-26** che questo piano attua:
> rilicenziare il toolkit · supportare **tre** sistemi di regole · distribuire
> come **wheel + eseguibile autonomo** · vendere **toolkit + map pack neutri +
> il metodo**.
>
> **ADR**: [0014](adr/ADR-0014-legenda-funzionale-fonte-unica.md) legenda fonte
> unica · [0015](adr/ADR-0015-dipendenze-a-livelli-e-pacchettizzazione.md)
> dipendenze e confezionamento · [0016](adr/ADR-0016-profili-regole-multisistema.md)
> profili multi-sistema · [0017](adr/ADR-0017-separazione-prodotto-e-rilicenziamento-toolkit.md)
> separazione e rilicenziamento.
> **Specifica normativa**: [`docs/guides/LEGENDA-FUNZIONALE-SPEC.md`](../docs/guides/LEGENDA-FUNZIONALE-SPEC.md).
> **Misura di partenza**: [`docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md`](../docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md).
>
> **Piano gemello**: [`PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA`](PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md)
> — quello è il *contenuto* (metriche, mappe, inquadratura), questo è il
> *prodotto*. Condividono i lotti fondativi: si eseguono **una volta sola**.
>
> **Stato**: 🟢 **DEFINITIVO — pronto all'esecuzione fase per fase** (2026-07-26)
> · **%**: 0%
>
> **Rev. finale**: aggiunti **P0.0** (rete di sicurezza *prima* di ogni refactor),
> **P0.5** (fetta verticale end-to-end come gate di progetto) e **§5-bis** (regole
> di esecuzione incrementale: un lotto = una PR, «fatto» per fase, migrazione a
> strangolamento, criteri di annullamento, API pubblica e SemVer).
> **Consolidamento**: questo piano è **l'unico proprietario** dell'infrastruttura;
> `PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA` gli ha delegato 12 lotti che erano
> duplicati e conserva il solo contenuto (rami C e D).

---

## 1. Cosa si vende, e cosa no

| | Vendibile | Perché |
|---|---|---|
| ✅ **Il toolkit** | sì | codice originale, arte procedurale in-house, **nessun asset di terzi** |
| ✅ **Map pack neutri** | sì | mappe originali world-neutral prodotte col toolkit |
| ✅ **Il metodo** | sì | schede-mappa, 9 metriche, corpus di calibrazione: nessun concorrente ce l'ha |
| ❌ **La campagna** | **no** | RHoD + Forgotten Realms: blocco WotC assorbente (ADR-0005, invariato) |

**La regola operativa che ne discende, e che vale per ogni lotto**: nessun nome,
luogo, PNG o statblocco della campagna entra mai nel package del toolkit. Il confine si verifica in CI (`arch/no-campaign-leak`, lotto P5.1), non a memoria.

**Il titolo che vende** resta *«scrivi la mappa come testo, ottieni una scena
Foundry con muri e luci»* — risolve un problema che le persone hanno già. Il
linter di level design è la funzione che, una volta dentro, fa dire *«questa cosa
l'ha scritta qualcuno che sa cosa fa»*: è ciò che trasforma un tool utile in un
tool di cui si parla, **ma non è ciò che porta il primo utente.** Non va messo in
copertina.

---

## 2. Il punto di partenza, misurato

Non un'impressione — i numeri dell'audit §6:

| Fatto | Valore | Conseguenza |
|---|---|---|
| Script con `sys.path.insert` | **11** | nulla è installabile o importabile |
| `render_map_svg.py` | **1.530 righe** (legenda + pattern + arte + parser + annotazioni + renderer + CLI) | 4 moduli lo importano *per il parser e la legenda*: il dominio dipende dalla presentazione |
| Validatori JSON Schema a mano | **2** | gli schemi draft-07 sono completi, i validatori no |
| Configurazione lint/format/tipi | **0** | i `# noqa: E402` in 8 file sono il fossile di un flake8 perso |
| Celle `⛰` senza muro nell'export UVTT | **3.689** in 6 mappe | il *Dirupo Mortale* è trasparente in Foundry |
| Copertura dei test | **non misurata** | 70 test verdi, ambito ignoto |

**Coerenza architetturale**: alta e non comune (13 ADR con gate CI, contratto
tool machine-readable bloccante, determinismo verificato per byte-identità,
scritture canone a triplo vincolo). **Il problema non è il progetto: è
l'imballaggio.**

---

## 3. Architettura bersaglio

```
  ┌──────────────────────────────────────────────────────────┐
  │  DOMINIO  (neutro, zero numeri di gioco, zero campagna)  │
  │  legend.yaml · parser griglia · modello mappa · metriche │
  └───────────────┬──────────────────────────────────────────┘
        ┌─────────┼─────────┬──────────────┬─────────────────┐
   ┌────▼────┐ ┌──▼─────┐ ┌─▼──────────┐ ┌─▼────────────┐
   │ render  │ │ export │ │  import    │ │ lint_design  │
   │  SVG    │ │ UVTT…  │ │ watabou…   │ │  (M1-M9)     │
   └─────────┘ └────────┘ └────────────┘ └──────┬───────┘
        └─────────┴─────────┴──────────────┴─────┼──────► CLI · wheel · exe
                                                 │
          ┌──────────────────────────────────────▼──────────────────┐
          │  VERIFICA  `dm.py verify`  — contratto unico dei finding │
          │  design/* · legend/* · map/* · rules/* · framing/*       │
          │  prose/* · arch/* · product/* · tool/* · plans/* · skill/*│
          └──────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────┐
  │  PROFILI DI REGOLE (sostituibili, licenze separate)      │
  │  rules/dnd35.yaml   rules/pf1e.yaml  │  rules/dnd5e.yaml │
  │  ──── OGL 1.0a ─────────────────────  ── CC BY 4.0 ───── │
  └──────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────┐
  │  CAMPAGNA RumblingStone — CONSUMATORE, mai dipendenza    │
  │  resta GPL-3 / privata · ADR-0005 invariato              │
  └──────────────────────────────────────────────────────────┘
```

Tre invarianti verificabili in CI:

1. il **dominio non importa** render, export, CLI né profili;
2. il **package non contiene** stringhe della campagna;
3. `legend.yaml` non contiene **nessun numero di gioco**.

---

## 3-bis. Il modello di verifica unico — «ogni fallimento ha un check»

*(sezione aggiunta il 2026-07-26 su richiesta DM: «il linter deve poter
verificare ogni fallimento».)*

### Perché non basta aggiungere un linter

Il repo ha **già sei verificatori**: `validate_maps`, `validate_modules`,
`validate_bestiario`, `validate_skills`, `tools_manifest --check`,
`check_plans_discipline`. Tutti e sei hanno `--json` — e **tutti e sei emettono
una forma diversa**:

```
validate_maps    → {tool, ok, rendered_dirs, svg, masters, errors[<stringhe>]}
validate_modules → {tool, ok, masters, findings[{file, errors[], warnings[]}]}
validate_skills  → {tool, ok, skills, errors[], warnings[]}
```

C'è una convenzione abbozzata (`tool`, `ok`) e **nessun contratto**: nessun
identificatore stabile di check, nessun modello di severità condiviso, nessuna
àncora `file:riga`, nessun modo per un consumatore di chiedere *«quali
fallimenti ha questa mappa, di qualunque natura?»*.

Aggiungere `lint_map_design` come **settimo silo** peggiorerebbe il problema
invece di risolverlo. La richiesta «verificare ogni fallimento» non si soddisfa
con un tool più grosso: si soddisfa con **un contratto unico e una matrice di
copertura dichiarata**.

### Le tre parti

1. **Un contratto di finding** (`scripts/schemas/findings.schema.json`) che ogni
   check emette:

   ```json
   {
     "check":    "design/M1-cover-reach",
     "severity": "error | warning | info",
     "file":     "08_.../Hammerfist-L1-REVISED-Ultra-Clear.md",
     "map":      1,
     "line":     42,
     "cell":     "K12",
     "message":  "copertura raggiungibile 0.03 (soglia >= 0.60)",
     "expected": 0.60, "actual": 0.03,
     "rule_ref": "LEGENDA-FUNZIONALE-SPEC §3 / audit §3.1",
     "fix":      "aggiungere copertura nel terzo centrale"
   }
   ```

   `check` è un **identificatore stabile**: si può silenziare per riga, contare
   nel tempo, e citare in una deroga motivata.

2. **Un aggregatore**, `dm.py verify`, che esegue i provider e unisce i finding
   in un solo report. Un solo posto dove si decide cosa blocca e cosa avvisa —
   oggi la politica è sparsa fra sei script e il workflow CI.

3. **Una matrice di copertura dichiarata** (§3-ter): ogni classe di fallimento
   dell'audit ha un `check` che la rileva, **oppure** è dichiarata non
   verificabile. Il vuoto dichiarato è informazione; il vuoto implicito no.

**I sei verificatori esistenti non vengono riscritti**: mantengono la loro CLI e
il loro comportamento, e in più emettono il contratto. Il linter di design
diventa **un provider fra gli altri**, non il centro.

---

## 3-ter. Matrice di copertura: ogni fallimento → un check

Legenda stato: ✅ già coperto oggi · 🟡 parziale · ❌ da costruire ·
⛔️ **dichiarato non verificabile a macchina**.

### Mappe — level design (`lint_map_design`)

| Check | Fallimento | Sev. | Stato | Lotto |
|---|---|---|---|---|
| `design/M1-cover-reach` | copertura non raggiungibile (mediana repo **0.30**) | warn | ❌ | P2.1 |
| `design/M2-void` | vuoto connesso massimo (mediana **0.51**) | warn | ❌ | P2.1 |
| `design/M7-symmetry` | mappa a specchio, indescrivibile a parole | info | ❌ | P2.1 |
| `design/M8-landmarks` | nessun riferimento nominabile (mediana **0**) | warn | ❌ | P2.1 |
| `design/M9-engagement` | distanza d'ingaggio fuori banda (**15/15** fuori) | warn | ❌ | P2.1 |
| `design/M3-loops` | topologia ad albero: nessun anello | warn | ❌ | P2.2 |
| `design/chokepoints` | zero strozzature (campo indifferenziato) o troppe (corridoio) | info | ❌ | P2.2 |
| `design/M4-exposure` | tutti vedono tutti (mediana **0.84**) | warn | ❌ | P2.2 |
| `design/M5-sightline` | linea di vista eccessiva al chiuso | info | ❌ | P2.2 |
| `design/M6-elevation` | un solo livello su uno scontro da set-piece | warn | ❌ | P2.2 |
| `design/intent-axis-unrealized` | asse tattico **dichiarato e non realizzato** | warn | ❌ | P2.3 |
| `design/intent-landmark-invalid` | landmark dichiarato su cella `nameable: false` | warn | ❌ | P2.3 |
| `design/intent-role-mismatch` | `combat_role: ambush` con esposizione 0.91 | warn | ❌ | P2.3 |

### Legenda e coerenza fra artefatti

| Check | Fallimento | Sev. | Stato | Lotto |
|---|---|---|---|---|
| `legend/single-source` | un consumatore usa un set di simboli proprio invece della legenda — **la causa della divergenza SVG↔UVTT** | **error** | ❌ | P1.1 |
| `legend/doc-sync` | `legenda-universale.md` diverge da `legend.yaml` | **error** | ❌ | P1.1 |
| `legend/no-game-numbers` | un numero di gioco è finito in `legend.yaml` (violazione ADR-0016) | **error** | ❌ | P1.1 |
| `legend/unknown-symbol` | simbolo usato e non in legenda | warn | 🟡 (regola R3 di `import_ultraclear`) | P2.0 |
| `rules/saturation-undeclared` | un profilo satura un valore senza dichiararlo | warn | ❌ | P1.2 |
| `rules/profile-incomplete` | un valore neutro senza traduzione nel profilo | **error** | ❌ | P1.2 |

### Mappe — struttura e artefatti

| Check | Fallimento | Sev. | Stato | Lotto |
|---|---|---|---|---|
| `map/svg-stale` | SVG fuori sync col master | **error** | ✅ `validate_maps` | — |
| `build/determinism` | render non byte-identico | **error** | ✅ `validate_maps` | — |
| `map/grid-nonuniform` · `map/header-mismatch` | righe di lunghezza diversa · intestazione che mente sulle dimensioni | warn | ✅ `import_ultraclear` R1/R2 | P2.0 |
| `map/kind-missing` | `map_kind` assente → il linter non sa se applicare le metriche (**8 griglie su 29** non sono battlemap) | warn | ❌ | P1.3 |
| `map/elevation-unmodelled` | quota scritta in un callout invece che nel dato (`DARA TOP (+18m)!`) | warn | ❌ | P1.3 |
| `map/companion-missing` | mancano i blocchi Ambiente / Tattiche / Evoluzione | warn | 🟡 (censito **a mano** in `MAPPE-CENSIMENTO.md`) | P2.0 |
| `map/scale-undeclared` | scala non dichiarata in testa | warn | 🟡 | P2.0 |

### Inquadratura e prosa

| Check | Fallimento | Sev. | Stato | Lotto |
|---|---|---|---|---|
| `framing/no-focal` | prompt senza focale (**0/48** oggi la dichiarano) | warn | ❌ | P2.6 |
| `framing/no-camera` | senza altezza/inclinazione camera (**0/48**) | warn | ❌ | P2.6 |
| `framing/no-scale-figure` | senza figura di scala (**0/48**) | warn | ❌ | P2.6 |
| `framing/no-atmospheric` | senza prospettiva atmosferica (**0/48**) | warn | ❌ | P2.6 |
| `framing/no-foreground` | senza primo piano dichiarato | warn | ❌ | P2.6 |
| `framing/ip-reference` | riferimento a IP protetta in un prompt versionato («Doctor Strange», «Lord of the Rings») | **error** in un prodotto venduto | ❌ | P2.6 |
| `prose/no-nonvisual-anchor` | read-aloud che apre su un'immagine invece che su un'ancora non visiva | info · **euristico** | ❌ | P2.6 |
| `prose/scale-by-number-first` | la misura arriva prima del rapporto | info · **euristico** | ❌ | P2.6 |

### Architettura e prodotto

| Check | Fallimento | Sev. | Stato | Lotto |
|---|---|---|---|---|
| `arch/layering` | il dominio importa render/export/CLI/profili | **error** | ❌ | P5.1 |
| `arch/no-campaign-leak` | stringhe della campagna dentro il package venduto | **error** | ❌ | P5.1 |
| `product/license-files` | release senza i file di licenza dei profili inclusi (OGL / CC BY) | **error** | ❌ | P5.1 |
| `product/bundle-smoke` | l'eseguibile non parte su macchina senza Python | **error** | ❌ | P3.2 |
| `tool/manifest-*` | tool senza manifest, o flag divergente da `--help` | **error** | ✅ `tools_manifest --check` | — |
| `plans/changelog-missing` | lotto chiuso senza riga di tracciatura | **error** | ✅ `check_plans_discipline` | — |
| `skill/*` · `module/*` · `bestiary/*` | skill malformata · master DEF fuori standard · statblocco/CR/naming | error/warn | ✅ i tre validator esistenti | P2.0 |

### ⛔️ Dichiarato NON verificabile a macchina

Onestà obbligatoria, altrimenti la matrice mente:

| Cosa | Perché no |
|---|---|
| **Se una mappa è divertente** | il linter misura affordance. Una mappa può passare ogni soglia ed essere noiosa, e un ponte stretto sopra il vuoto viola M1, M2, M3 e M4 **di proposito** |
| **Se un read-aloud funziona al tavolo** | i due check `prose/*` rilevano una *forma*, non la resa. Restano `info` per sempre |
| **Se un'immagine è bella** | la scheda-inquadratura si verifica per **presenza dei campi**, mai per esito |
| **Se una regola 3.5/PF1e/5e è tradotta bene** | lo verifica la suite del profilo contro la fonte, non il linter |
| **Conformità legale (OGL, marchi, licenza)** | `product/license-files` verifica che i file **ci siano**, non che siano **giusti**: quello è l'avvocato IP |

---

## 4. I lotti

Impegno secondo la regola DM 2026-07-22 (engine + livello per fase).

### Fase P0 — Substrato (sblocca tutto il resto)

#### ⬜ P0.0 — La rete di sicurezza, **prima** di toccare qualunque cosa ⭐

*Regola di mestiere*: non si rifattorizza un modulo da 1.530 righe con una rete
parziale. Oggi la rete esiste per gli SVG (byte-identità, forte) e **non** per il
resto: `export_uvtt`, `import_ultraclear` e `compile_map_json` hanno test di
comportamento ma nessun *golden* che congeli l'output corrente.

- **caratterizzazione**: per ogni mappa del corpus, congelare l'output attuale di
  `export_uvtt` e `compile_map_json` come golden file. Non si giudica se è
  giusto — si registra **cos'è oggi**;
- baseline di copertura misurata (oggi ignota) sulle sole aree che P0.4 sposterà;
- ogni golden è etichettato con l'esito atteso: `freeze` (non deve cambiare mai)
  oppure `expected-to-change@P1.1` (cambierà, e si sa perché — le 6 mappe con `⛰`).

**Accettazione**: i golden esistono e sono verdi **prima** del primo commit di
refactor; ogni golden dichiara se è `freeze` o `expected-to-change`; un golden che
cambia senza essere marcato **rompe la CI**.
**Engine**: Sonnet · **Impegno**: medio · **Stima**: 5-7 h · **Dip.**: nessuna —
**è il primo lotto in assoluto**.

#### ⬜ P0.1 — `pyproject.toml` e fine dei `sys.path.insert`

Package importabile con entrypoint da console; gli 11 `sys.path.insert`
spariscono. **Il layout attuale resta invocabile identico**: `python3
scripts/dm.py …` continua a funzionare — nessuna rottura per il DM.

- **Accettazione**: `pip install -e .` funziona; i 70 test passano sia dal
  package sia dal layout attuale; SVG **byte-identici**; `tools_manifest --check`
  verde.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: ADR-0015.

#### ⬜ P0.2 — Livelli di dipendenza + `jsonschema` sui gate

Livello 0 core **stdlib puro e offline** · livello 1 `analysis`
(numpy/scipy/networkx/tcod) **opzionale** · livello 2 dev. `jsonschema` valida in
CI gli schemi draft-07 già nel repo; i validatori a mano si riducono ai soli
**controlli semantici** che JSON Schema non può esprimere.

- **Accettazione**: gli esempi validano contro `tactical_map.schema.json` **senza
  modificarlo** (eccetto il caso documentato `units_in: meters`); un test per
  ogni errore che il validatore a mano sapeva già dare — **zero comportamenti
  persi**; il core resta eseguibile senza rete e senza `pip`.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 5-7 h · **Dip.**: P0.1.

#### ⬜ P0.3 — `ruff` + `pytest` + copertura

Un solo tool per lint e formato; `pytest` come runner (esegue i 70 `unittest`
esistenti **senza riscriverli**); baseline di copertura registrata. Non bloccante
al primo giro, bloccante dopo la bonifica.

- **Accettazione**: `ruff check` pulito; `pytest` verde sui test **non
  riscritti**; baseline pubblicata.
- **Engine**: Haiku, con Sonnet sulle correzioni non banali · **Impegno**: basso
  · **Stima**: 4-6 h · **Dip.**: P0.1.

#### ⬜ P0.4 — Cucitura dominio / presentazione

Legenda, parser della griglia e modello della mappa escono da `render_map_svg.py`
e diventano il **dominio**. Renderer, exporter, importer e linter ne dipendono; il
dominio non dipende da nessuno.

- **Accettazione**: `render_map_svg` non è più importato da nessuno per ottenere
  parser o legenda; **grafo delle dipendenze aciclico** con la presentazione
  sulle foglie, verificato da un test; SVG byte-identici; round-trip UVTT verde.
- **Engine**: Opus (confini) → Sonnet (spostamento) · **Impegno**: alto ·
  **Stima**: 10-14 h · **Dip.**: P0.1, P1.1.

#### ⬜ P0.5 — Scheletro deambulante: **una fetta verticale end-to-end** ⭐

*Regola di mestiere*: un piano incrementale prova l'architettura **presto e
sottile**, non tardi e in massa. P0.1-P0.4 sono orizzontali — tutta
infrastruttura, nessuna funzione. Se il confine dominio/presentazione è sbagliato,
lo si scopre dopo aver migrato 62 simboli e 4 script.

Quindi: **prima della migrazione di massa, una fetta sola che attraversi tutta
l'architettura bersaglio**, su **un simbolo** (`🪨` — ha copertura, terreno
difficile, `nameable`, è distruttibile: tocca ogni campo):

```
legend.yaml(🪨) → dominio → ┬→ render SVG   (byte-identico)
                            ├→ export UVTT  (golden invariato)
                            ├→ profilo 3.5 → «+4 CA, movimento ×2»
                            ├→ profilo 5e  → «+2 CA e TS Des, ×2»
                            ├→ una metrica (M1) su una fixture
                            └→ un finding nel contratto unico
```

Tutto il resto resta com'è. Se questa fetta è scomoda da scrivere, **il confine è
sbagliato e si corregge adesso**, quando costa un giorno invece di tre settimane.

**Accettazione**: la fetta gira end-to-end; nessuno degli altri 61 simboli è
stato toccato; il grafo delle dipendenze della fetta è già quello bersaglio;
**decisione go/no-go documentata** prima di aprire P1.1.
**Engine**: Opus (è una verifica di progetto, non codice) · **Impegno**: medio ·
**Stima**: 6-8 h · **Dip.**: P0.1, P0.4 · **È un gate**: P1.1 non parte senza il go.

---

### Fase P1 — La legenda funzionale e i tre sistemi

#### ⬜ P1.1 — `legend.yaml`: fonte unica, funzione neutra

Attua [`LEGENDA-FUNZIONALE-SPEC.md`](../docs/guides/LEGENDA-FUNZIONALE-SPEC.md)
§2 e §4 su tutti e **62** i simboli. `render_map_svg.SYMBOLS` diventa derivato;
`export_uvtt` deriva muri/porte/luci da `function` ed **elimina** `WALL_SYMS`,
`DOOR_SYMS`, `LIGHT_SYMS`; `import_ultraclear.HAZARD_SYMS` idem;
`legenda-universale.md` si **genera** dal YAML.

Chiude la divergenza delle quattro classificazioni (spec §6): `⛰ 🏛 🗼 🗿` sono
tutte **copertura totale**, impenetrabili e opache.

- **Accettazione**: nessun set di simboli cablato resta in `scripts/`; **i 17 SVG
  legacy restano byte-identici** (modo di rendering e funzione sono ortogonali:
  una statua continua a disegnarsi come prop *e* a dichiararsi opaca); l'export
  UVTT delle **6 mappe con `⛰` cambia**, guadagnando **3.689 celle** di muro — è
  il bug, e il diff va verificato a mano una volta; `legend.yaml` **non contiene
  nessun numero di gioco** (test automatico); gate di sync YAML ↔
  `legenda-universale.md`.
- **Engine**: Opus (modello) → Sonnet (migrazione) · **Impegno**: alto ·
  **Stima**: 12-16 h · **Dip.**: P0.1. · **= lotto E1 di `PIANO-EDITOR`: un
  lavoro, tre piani.**

#### ⬜ P1.2 — I tre profili di regole

`rules/dnd35.yaml`, `rules/pf1e.yaml`, `rules/dnd5e.yaml` secondo spec §3 e
ADR-0016. Selettore `--rules`, default per campagna. Regola di **saturazione**:
un valore non esprimibile si riduce al più vicino **e si dichiara nel report**
(caso canonico: `move_cost: 4` non esiste in 5e).

- **Accettazione**: i tre profili passano una suite propria che verifica ogni
  traduzione contro la sua fonte; ⚠️ **`move_cost: 4` per PF1e va confermato sul
  PRD** — è l'unico valore della spec non verificato sul testo; ogni profilo
  dichiara in testa licenza, fonte e revisione; il motore non contiene il nome di
  nessun sistema.
- **Engine**: Opus (traduzioni) → Sonnet (file e test) · **Impegno**: alto ·
  **Stima**: 14-18 h · **Dip.**: P1.1.

#### ⬜ P1.3 — Zone, elevazione, `design_intent`, `map_kind` — schema v1.1

`zones[]` con `name`/`elevation_m`/`connects_to[]` (il grafo su cui si calcola
M3, distinto dal `@zone` attuale che resta un bracket di presentazione);
`design_intent{}`; `map_kind: battle|strategic|schematic|overland` — senza il
quale il linter produrrebbe rumore su **8 griglie su 29**.

- **Accettazione**: lo schema v1.1 valida **invariati** i contratti esistenti; un
  esempio nuovo con 3 bande di elevazione e `design_intent` compila, rende e passa
  `validate_maps`; le 8 griglie non-tattiche del corpus marcate e **saltate** dal
  linter con una riga informativa, non un warning.
- **Engine**: Opus (schema) → Sonnet · **Impegno**: alto · **Stima**: 12-16 h ·
  **Dip.**: P1.1.

---

### Fase P2 — La verifica (integrata, non riscritta)

#### ⬜ P2.0 — Contratto unico dei finding + aggregatore `verify` ⭐

*Attua*: §3-bis. **Precede il linter**, perché il linter deve nascere già dentro
il contratto invece di essere il settimo silo da normalizzare dopo.

- `scripts/schemas/findings.schema.json` — `check` (identificatore stabile),
  `severity`, `file`, `line`/`map`/`cell`, `message`, `expected`/`actual`,
  `rule_ref`, `fix`;
- i **sei verificatori esistenti** emettono il contratto **in aggiunta** al loro
  output attuale: nessuna CLI cambia, nessun comportamento cambia;
- `dm.py verify [--all | --maps | --design | --framing | …] [--json] [--strict]`
  — un solo posto dove si decide cosa blocca e cosa avvisa;
- **silenziamento per deroga**: `<!-- verify: allow design/M1-cover-reach — il
  ponte stretto viola M1 di proposito -->`. Una deroga **senza motivazione è un
  errore**: è ciò che separa una deroga da un warning ignorato;
- promozione dei controlli oggi manuali o impliciti a check con ID:
  `map/companion-missing` (oggi censito a mano in `MAPPE-CENSIMENTO.md`),
  `map/scale-undeclared`, `legend/unknown-symbol` (oggi regola R3 dentro
  `import_ultraclear`).

- **Accettazione**: ogni finding di ogni provider valida contro lo schema; `dm.py
  verify --all --json` produce **un solo documento**; i sei tool mantengono
  output e codici di uscita **invariati** (test di non-regressione); una deroga
  senza motivazione fallisce; il registro dei `check` è generato dal codice, non
  scritto a mano.
- **Engine**: Opus (contratto) → Sonnet (adattatori) · **Impegno**: medio-alto ·
  **Stima**: 10-14 h · **Dip.**: P0.1, P0.2.

#### ⬜ P2.1 — `lint_map_design`: M1, M2, M7, M8, M9

**M1 = `scipy.ndimage.binary_dilation` (5×5), M2 = `ndimage.label` +
`bincount`** — 4 righe, non 18. Nessun BFS a mano.

- **Accettazione**: ADR-0012 pieno; riproduce i valori dell'appendice A
  dell'audit (M1 0.0309 · M2 0.9691 su *Dirupo Mortale*), **già confermati in
  laboratorio**; fixture sintetiche (corridoio, campo aperto, arena ad anello);
  senza le librerie del livello 1 → exit code documentato, **mai** un crash.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: P0.2,
  P1.1, P1.3.

#### ⬜ P2.2 — M3 anelli e strozzature, M4/M5 visibilità, M6 verticalità

`networkx` per μ = E−V+C e `articulation_points` (1 riga ciascuna); **`tcod`
`compute_fov`** (shadowcasting simmetrico) per la visibilità. ⚠️ **Il
campionamento è cancellato**: censimento completo di 1.585 celle su 40×40
misurato in **34 ms**. M4 diventa **esatta**, quindi deterministica per
costruzione — e la stima campionata **sottostimava** (0.88 contro 0.913).

- **Accettazione**: linter completo su 40×40 in **< 1 s**; M3 = 2 sulla fixture
  ad anello, 0 sul corridoio; nessun seme di campionamento da fissare.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: P1.3,
  P2.1.

#### ⬜ P2.3 — Dichiarato contro realizzato

Il linter confronta `design_intent` con le metriche: *«`tactical_axes` include
verticality ma M6 = 1»*, *«landmark dichiarato su cella `nameable: false`»*,
*«`combat_role: ambush` ma M4 = 0.91»*. **Nessuna soglia arbitraria: il metro è
la dichiarazione dell'autore.** È la funzione che nessun altro strumento ha.

- **Accettazione**: i 3 casi riprodotti da fixture; una mappa senza
  `design_intent` non produce warning di questa classe.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 8-10 h · **Dip.**: P1.3,
  P2.2.

#### ⬜ P2.4 — Calibrazione delle soglie

10-15 mappe **che si sa funzionare al tavolo**, di proprietà o liberamente
licenziate → trascritte → misurate → soglie ai **percentili della distribuzione
reale**. ⚠️ **Mai mappe RHoD** (ADR-0005), e per un prodotto venduto il vincolo è
più stretto: solo materiale di cui si possa **documentare** la licenza.

- **Accettazione**: ogni soglia ha accanto percentile e dimensione del corpus;
  corpus e licenze documentati; le soglie pre-calibrazione **sostituite**, non
  affiancate. Finché non è fatto, il tool **dichiara** che le soglie sono
  euristiche.
- **Engine**: Sonnet (trascrizione) + Opus (percentili) · **Impegno**: medio ·
  **Stima**: 12-16 h · **Dip.**: P2.2 · **Gate**: corpus scelto dal DM.

#### ⬜ P2.5 — Chiusura della matrice: nessun fallimento senza check

*Attua*: §3-ter. Il lotto che rende vera la frase «il linter verifica ogni
fallimento» — e che la **rende falsificabile**.

- ogni riga ❌ o 🟡 della matrice è coperta o **spostata in ⛔️ con motivazione**;
- un **meta-check**, `verify/coverage`, confronta il registro dei `check`
  implementati con la matrice di §3-ter: una riga senza check e senza
  dichiarazione di non-verificabilità **fallisce la CI**. È la matrice che si
  verifica da sola, invece di invecchiare in silenzio;
- baseline registrata: quanti finding per severità produce oggi il corpus. È il
  numero che deve scendere, ed è ciò che permette di dire se il piano funziona.

- **Accettazione**: `dm.py verify --all` copre ogni riga di §3-ter; il
  meta-check è rosso se la matrice e il codice divergono; baseline pubblicata in
  `docs/audit/`.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: P2.0,
  P2.3.

#### ⬜ P2.6 — Check di inquadratura e prosa

L'unico ramo di verifica che oggi non ha **nessun** tool: i prompt e il
read-aloud. Su 48 blocchi prompt, **0** dichiarano focale, altezza camera, figura
di scala o prospettiva atmosferica.

- `framing/*` verifica la **presenza dei campi** della scheda-inquadratura, mai
  l'esito estetico;
- `framing/ip-reference` cerca riferimenti a IP protette nei prompt versionati —
  `warning` per uso privato, **`error` nel prodotto venduto**: la severità
  dipende dal profilo di release, non dal check;
- `prose/*` restano **euristici e `info` per sempre** (§3-ter ⛔️): rilevano una
  forma, non la resa.

- **Accettazione**: il retrofit delle 3 scene pilota di ARC-07 porta i loro
  `framing/*` a zero; nessun `prose/*` è mai promosso a `warning`; la lista dei
  termini IP è un dato versionato, non una regex sepolta nel codice.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 8-10 h · **Dip.**: P2.0,
  e la scheda-inquadratura del piano gemello (lotto D1).

---

### Fase P3 — Confezionamento e distribuzione

#### ⬜ P3.1 — Wheel

Build riproducibile, versionamento semantico, `python -m build`, pubblicazione
su indice.

- **Accettazione**: `pip install <pkg>` su una macchina pulita → la CLI funziona;
  extra `[analysis]` installabile a parte; wheel senza file di campagna.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 5-7 h · **Dip.**: P0.1.

#### ⬜ P3.2 — Eseguibile autonomo (PyInstaller)

Un file da scaricare e lanciare, **tutte le dipendenze incluse**: il DM medio non
deve sapere cosa sia `pip`. Matrice Linux / Windows / macOS in CI.

- **Accettazione**: l'eseguibile parte su una macchina **senza Python**; il
  linter funziona (livello 1 incluso nel bundle); avvisi di licenza delle
  dipendenze bundled inclusi nel pacchetto — **requisito, non cortesia**
  (ADR-0017 §4).
- **Engine**: Sonnet · **Impegno**: alto · **Stima**: 10-14 h · **Dip.**: P3.1.

#### ⬜ P3.3 — Rilicenziamento e provenienza

Verifica **dimostrata** — non assunta — che ogni file del package sia originale;
inventario delle licenze delle dipendenze; cambio di licenza del solo toolkit; la
campagna resta com'è.

- **Accettazione**: inventario di provenienza committato; nessun file del package
  senza attribuzione chiara; `LICENSE` della campagna invariato.
- **Engine**: Opus · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: P0.4.
  **Gate**: ⚠️ **verifica di un avvocato IP prima di qualunque vendita.**

#### ⬜ P3.4 — Conformità OGL / CC BY

Testo OGL 1.0a e catena Section 15 per i profili 3.5 e PF1e; attribuzione CC BY
4.0 per il profilo 5e; dichiarazione di Product Identity e Open Game Content;
formula di compatibilità **verificata testo alla mano** per ciascuno dei tre.
Marchi «D&D» e «Pathfinder» **fuori** da nome e marketing.

- **Accettazione**: un gate CI verifica che ogni release includa i file di
  licenza dovuti per i profili inclusi; nessun marchio nel nome del prodotto.
- **Engine**: Opus · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: P1.2.
  **Gate**: ⚠️ avvocato IP.

---

### Fase P4 — I due prodotti di contenuto

#### ⬜ P4.1 — Map pack neutri

Mappe **originali, world-neutral**, progettate con la scheda-mappa e verificate
dal linter, esportate in SVG/PNG/UVTT. Zero contenuto WotC — **nessuna mappa
RHoD, nemmeno riprogettata**. Etichetta `Contains AI-Generated Content` dove
pertinente.

- **Accettazione**: ogni mappa del pack passa le soglie o porta una **deroga
  scritta**; un gate verifica l'assenza di stringhe della campagna; ogni mappa ha
  la sua scheda-mappa pubblicata.
- **Engine**: Opus (design) → Sonnet (griglie) · **Impegno**: alto · **Stima**:
  6-8 h a mappa · **Dip.**: P2.1, e la scheda-mappa del piano gemello.

#### ⬜ P4.2 — Il metodo, come guida vendibile

Schede-mappa, le 9 metriche, il corpus di calibrazione, la disciplina di
progettazione — e la parte di inquadratura (blockout, ordine percettivo). È la
parte **senza concorrenti**, e utile anche a chi non compra il software.

- **Accettazione**: la guida sta in piedi **senza** il toolkit installato; ogni
  metrica ha un esempio prima/dopo su una mappa che il lettore può vedere.
- **Engine**: Opus · **Impegno**: alto · **Stima**: 20-25 h · **Dip.**: P2.4.

---

### Fase P5 — Gate di prodotto in CI

#### ⬜ P5.1 — Le tre invarianti dell'architettura, verificate

```
□ il dominio non importa render/export/CLI/profili   (grafo aciclico)
□ il package non contiene stringhe della campagna    (lista di termini vietati)
□ legend.yaml non contiene numeri di gioco           (nessun +N, %, CD)
□ ogni release include le licenze dei profili inclusi
□ l'eseguibile parte su macchina senza Python        (smoke su matrice OS)
```

- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: P0.4,
  P3.2.

---

## 5. Sequenza

| # | Lotti | Ore | Cosa hai in mano alla fine |
|---|---|---|---|
| 0 | **P0.0** rete di sicurezza | 5-7 | golden congelati **prima** di toccare qualunque cosa |
| 1 | P0.1 → P0.3 → **P0.5** | 21-29 | il toolkit è **installabile**, con lint e test veri, e **la fetta verticale ha dato il go** |
| 2 | **P1.1 + P0.4** | 22-30 | legenda funzionale + dominio separato. **La divergenza SVG↔UVTT è chiusa**: 3.689 celle di muro recuperate |
| 3 | P1.2 | 14-18 | **tre sistemi supportati** — il mercato passa da «i DM di 3.5» a 3.5+PF1e+5e |
| 4 | P3.1 + P3.3 | 11-15 | wheel pubblicabile, provenienza dimostrata |
| 5 | **P2.0** → P1.3 → P2.1 → P2.2 | 34-46 | contratto unico dei finding + il linter completo e veloce, **già dentro il contratto** |
| 6 | P3.2 + P3.4 + P5.1 | 22-30 | **eseguibile per DM non tecnici**, conformità, gate |
| 7 | P2.3 + **P2.5** + **P2.6** + P2.4 | 34-44 | dichiarato-vs-realizzato · **matrice chiusa e auto-verificata** · check di inquadratura · soglie calibrate |
| 8 | P4.1 + P4.2 | 40+ | i due prodotti di contenuto |

**Totale**: ~206-259 h al netto di P4 (che scala con quante mappe si vendono).

**Il primo punto di rilascio possibile è dopo il passo 4**: un toolkit
installabile, multi-sistema, con la legenda corretta e la provenienza pulita —
**senza** il linter. Il linter è ciò di cui si parla, non ciò che porta il primo
utente: rilasciare prima e aggiungerlo dopo è la sequenza giusta, non un
compromesso.

---

## 5-bis. Regole di esecuzione incrementale

*(sezione aggiunta con la revisione finale — è ciò che rende il piano
**eseguibile fase per fase** invece che solo leggibile.)*

### 1. Un lotto = una PR

Ogni lotto è una PR autonoma che **arriva verde da sola**. Mai una PR che
«funzionerà quando arriva la prossima». Ogni PR chiude applicando la regola d'oro
dei piani: checklist del piano + riga in `plans/INDEX.md` + riga in
`plans/CHANGELOG.md`, **nello stesso commit** (ADR-0009, già enforced).

### 2. Definizione di «fatto» a livello di **fase**

Un lotto ha criteri di accettazione propri (§4). Una **fase** è chiusa solo se:

| Fase | La fase è chiusa quando… |
|---|---|
| **P0** | `pip install -e .` funziona · zero `sys.path.insert` · `ruff` e `pytest` verdi · golden verdi · **la fetta verticale ha dato go** · `python3 scripts/dm.py` funziona ancora identico |
| **P1** | un simbolo qualunque risponde a «blocchi la vista? quanto copri, in 3.5 / PF1e / 5e?» · zero set cablati · **3.689 celle di muro recuperate** e diff UVTT verificato · SVG byte-identici |
| **P2** | `dm.py verify --all --json` è **un solo documento** · ogni riga di §3-ter ha un check o una ⛔️ · meta-check verde · baseline registrata |
| **P3** | il wheel si installa su macchina pulita · l'eseguibile parte su macchina **senza Python** · provenienza dimostrata · file di licenza presenti |
| **P4** | ogni mappa del pack passa o ha deroga scritta · la guida sta in piedi senza il software |
| **P5** | le tre invarianti sono rosse se violate — verificato **introducendo di proposito** una violazione |

### 3. Migrazione a strangolamento (*strangler*), non big-bang

Il vecchio percorso resta vivo mentre il nuovo cresce accanto. Concretamente:
`scripts/*.py` resta invocabile **identico** per tutta la durata del piano; il
package cresce accanto; un percorso si rimuove **solo** quando il suo sostituto è
verde da una fase intera. **Nessun lotto contiene una rimozione e la sua
sostituzione insieme.**

### 4. Criteri di annullamento (dichiarati prima, non dopo)

| Lotto | Si ferma e si ripensa se… |
|---|---|
| P0.4 | la fetta verticale di P0.5 risulta scomoda → il confine è sbagliato: si ridisegna prima di migrare |
| P1.1 | un SVG cambia senza spiegazione, o un golden `freeze` si muove |
| P1.2 | un sistema richiede un campo neutro nuovo → si riapre ADR-0016 invece di aggiungere un campo di sistema alla legenda |
| P2.x | la baseline dei finding **sale** invece di scendere: il linter sta producendo rumore |
| P3.3 | la provenienza di un file non è dimostrabile → non entra nel package, punto |

### 5. Superficie pubblica e versionamento

Dal momento in cui esiste un wheel (P3.1) c'è un contratto con chi lo installa:

- **API pubblica dichiarata esplicitamente** (`__all__` + documentata). Tutto il
  resto è privato e può cambiare senza preavviso;
- **SemVer**: rottura dell'API pubblica, del contratto JSON o del formato dei
  finding → *major*. Il repo ha già i pezzi giusti (`schema_version` nel contratto,
  `report_version` nei report): vanno **collegati** al versionamento del package;
- ogni schema porta la sua versione e una nota di migrazione. Un contratto che
  cambia in silenzio è il modo più veloce di perdere gli utenti che si sono appena
  pagati.

### 6. Ordine dei mattoni: sempre dato → strumento → contenuto

Regola trasversale, già rispettata dalla sequenza di §5: nessuna metrica prima
del dato che la rende calcolabile; nessun contenuto di massa prima dello strumento
che lo verifica. Le violazioni di quest'ordine sono la ragione per cui M3 e M6 non
si potevano calcolare oggi.

---

## 6. Rischi

| Rischio | Mitigazione |
|---|---|
| P0/P1 rompono ciò che oggi funziona (11 import, modulo da 1.530 righe) | la rete c'è già: 70 test, byte-identità SVG, round-trip UVTT. Il layout `scripts/*.py` **resta invocabile identico** |
| L'export UVTT cambia su 6 mappe | **è il bug**, non una regressione: diff verificato a mano una volta e documentato |
| Tre profili = tre fonti da riseguire a ogni errata | suite di verifica per profilo; ogni profilo dichiara fonte e revisione; un profilo si può **ritirare** senza toccare il prodotto |
| `move_cost: 4` per PF1e non verificato | bloccante per il rilascio di **quel** profilo, non degli altri due |
| Conformità OGL sbagliata | gate CI sui file di licenza **+ avvocato IP prima della vendita**. Non autocertificabile |
| Le dipendenze bundled non sono ridistribuibili | gate di licenza permissiva già in ADR-0015, promosso a **requisito di prodotto** |
| Contenuto di campagna finisce nel package | gate automatico (P5.1), non disciplina a memoria |
| Il prodotto non trova compratori | i tre prodotti sono indipendenti: il metodo (P4.2) vende anche senza il software, e i map pack hanno il pubblico più largo |
| Il piano non chiude mai | il primo rilascio è al passo 4 di 8. Tutto il resto è incrementale su un prodotto **già uscito** |
| **La verifica diventa rumore e viene spenta** | severità a tre livelli con default advisory; `map_kind` **prima** del linter; deroghe silenziabili **con motivazione obbligatoria**; baseline registrata, così si vede se il rumore sale |
| **La matrice di §3-ter invecchia in silenzio** | il meta-check `verify/coverage` (P2.5) è rosso se matrice e codice divergono: la matrice si verifica da sola |
| Il contratto unico rompe i sei verificatori esistenti | emettono il contratto **in aggiunta**, CLI e codici d'uscita invariati, con test di non-regressione |

---

## 7. Cosa questo piano NON risolve

- **Non rende la campagna vendibile.** ADR-0005 resta intatto: il blocco WotC è
  assorbente e non si aggira separando i prodotti.
- **Non è consulenza legale.** OGL, CC BY, marchi e rilicenziamento richiedono un
  avvocato IP prima della vendita.
- **Non garantisce un mercato.** Un linter di design non esiste — ma novità non
  significa domanda: è uno strumento **da progettista**, non da DM, e il pubblico
  è più piccolo e più tecnico di quello dell'export UVTT.
- **Non copre l'editor visuale**, che resta un piano separato — al quale però
  questo piano finalmente dà **qualcosa da importare**.

---

## Checklist

```
P0 substrato
□ P0.0 ⭐ rete di sicurezza: golden export_uvtt/compile_map_json + baseline
□ P0.1 pyproject + fine degli 11 sys.path.insert
□ P0.2 livelli di dipendenza + jsonschema sui gate
□ P0.3 ruff + pytest + baseline copertura
□ P0.4 cucitura dominio/presentazione (grafo aciclico verificato)
□ P0.5 ⭐ fetta verticale end-to-end su UN simbolo → GO/NO-GO prima di P1.1

P1 legenda e sistemi
□ P1.1 legend.yaml — 62 simboli, funzione neutra, 4 correzioni ⛰🏛🗼🗿
□ P1.2 rules/dnd35 · rules/pf1e · rules/dnd5e (+ verificare PF1e move_cost 4)
□ P1.3 zones/elevation/design_intent/map_kind — schema v1.1

P2 verifica  (contratto unico: ogni fallimento ha un check — §3-bis/§3-ter)
□ P2.0 ⭐ findings.schema.json + `dm.py verify` + i 6 validator nel contratto
□ P2.1 M1 M2 M7 M8 M9 (scipy)
□ P2.2 M3+strozzature (networkx) · M4/M5 ESATTE (tcod) · M6
□ P2.3 dichiarato vs realizzato
□ P2.5 chiusura matrice + meta-check verify/coverage + baseline
□ P2.6 framing/* e prose/* (l'unico ramo oggi senza alcun tool)
□ P2.4 calibrazione su corpus documentato

P3 prodotto
□ P3.1 wheel
□ P3.2 eseguibile autonomo (matrice Linux/Win/macOS)
□ P3.3 rilicenziamento + provenienza dimostrata   [gate: avvocato IP]
□ P3.4 conformità OGL 1.0a / CC BY 4.0 + marchi   [gate: avvocato IP]

P4 contenuto
□ P4.1 map pack neutri
□ P4.2 il metodo come guida

P5 gate
□ P5.1 le tre invarianti verificate in CI
```

> **Regola d'oro dei piani**: chi chiude un lotto aggiorna — nello stesso commit
> — questa checklist, la riga in `plans/INDEX.md` e una riga in
> `plans/CHANGELOG.md`.
