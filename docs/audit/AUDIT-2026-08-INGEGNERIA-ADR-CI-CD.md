<!-- Report d'audit 2026-08-05 — dettaglio asse T. Documento di analisi, nessuna modifica al codice. -->
# Audit globale — ingegneria, architettura, ADR, testing, CI/CD

**Data:** 2026-08-05 · **Commit base:** `3b9f3c3`
Sintesi e roadmap: [`AUDIT-2026-08-SINTESI.md`](AUDIT-2026-08-SINTESI.md).
Companion storico: [`AUDIT-REPORT.md`](AUDIT-REPORT.md) (audit `scripts/` del
2026-07-24 — F1-F9 tutte chiuse) e [`SCORECARD.md`](SCORECARD.md).

**Metro:** best practice da senior developer / system engineer / architect.
Quell'audit ha già normalizzato i **singoli tool**. Questo guarda un livello
sopra: il **progetto** come artefatto software — riproducibilità, gate onesti,
distribuzione, e allineamento fra ciò che i documenti dichiarano e ciò che
esiste.

---

## 1. Cosa è già a standard

Va detto per intero, perché condiziona le raccomandazioni: **su questo asse il
repo è messo meglio della maggioranza dei progetti software veri.**

| Pratica | Evidenza |
|---|---|
| Decisioni tracciate | **17 ADR** (0000 template → 0016), citati dal codice e dalle skill, con stato e decisione-fonte |
| Architettura dichiarata | ADR-0002 (CLI unica orchestratrice), libreria condivisa `dmcore/`, tool usabili in isolamento |
| Contratti machine-readable | `scripts/tools.manifest.json` + 3 JSON Schema + `docs/tools/registry.json` + vista MCP, con gate di conformità in CI (ADR-0012) |
| Test | **70 test, 70 verdi**, in 13 moduli; determinismo del render verificato; round-trip mappe M1/M2 |
| Gate di processo | `check_plans_discipline.py` (ADR-0009) blocca una PR strutturale senza riga di CHANGELOG — un gate di *disciplina*, raro e ben concepito |
| Diagnostica | `dm.py doctor --ci` come health check unico, con distinzione fra bloccante (`✓`/`✗`) e informativo (`○`) |
| Documentazione | `docs/INDEX.md` categorizzato, tabelle dei tool **generate** dal manifest (non scritte a mano) |

Le raccomandazioni che seguono **non rifanno niente di questo**.

---

## 2. Findings

### 🔴 T1 — Non esiste CD: la CI valida, nulla pubblica

`.github/workflows/ci.yml` è l'unico workflow del repo. Ha due job:

- `validate` — 15 step, tutti di verifica;
- `build` — costruisce i pacchetti skill e li carica come artifact con
  `retention-days: 14`.

Questo è **CI completa e CD assente**. Le conseguenze sono concrete:

| Cosa manca | Perché conta qui |
|---|---|
| Nessun tag (`git tag` → vuoto) | non esiste il concetto di «versione della campagna». `state.md` §8 è append-only e fa da storia, ma nulla è citabile come «lo stato al momento X» |
| Nessun release | il DM non ha modo di consegnare al gruppo un pacchetto stabile |
| I booklet/PDF non vengono mai costruiti in CI | ADR-0013 definisce lo standard, `GUIDA-BOOKLET-E-PDF.md` documenta la pipeline end-to-end, `build_booklet_html.py`/`export_booklet_pdf.py` esistono — **e nessuno li esegue mai automaticamente**. Il finding E3 (13 asset rotti nel booklet del Palio) è precisamente ciò che una build in CI avrebbe intercettato il giorno stesso |
| L'unico artefatto scade in 14 giorni | e contiene i pacchetti skill, cioè l'output meno prezioso dei tre (skill / booklet / registry) |

**Il caso è forte proprio perché la pipeline esiste già.** Non serve inventare
una distribuzione: servono un tag, un workflow di release e la decisione di cosa
entra nel pacchetto.

**Azione (G9):** `.github/workflows/release.yml` — su tag `v*`: build dei
booklet HTML + PDF, pacchetti skill, `registry.json`, allegati a una GitHub
Release; + ADR «versioning e release» che dichiari cosa versiona il tag (il
*materiale*, non il canone giocato) e cosa entra in ciascuna edizione — con
rimando alla matrice delle edizioni del PRD (G5).

---

### 🟠 T2 — Igiene di progetto Python assente: la build non è riproducibile

| Elemento | Stato |
|---|---|
| `pyproject.toml` / `setup.cfg` | ❌ assenti |
| `requirements.txt` (o lock) | ❌ assente — la CI fa `pip install pyyaml`, **senza versione** |
| Linter / formatter (ruff, black) | ❌ assenti |
| Misura di copertura | ❌ assente |
| `.pre-commit-config.yaml` | ❌ assente (esiste `install-git-hooks.sh`, che installa un `post-merge` e un `pre-push` propri) |
| Versione Python dichiarata per chi contribuisce | ❌ solo in `ci.yml` (`3.11`); `doctor` verifica la versione a runtime |

`pip install pyyaml` non pinnato significa che la CI di oggi e quella di fra sei
mesi installano software diverso. Per un repo che ha fatto del **determinismo**
un requisito contrattuale — render SVG byte-identico, output ordinato,
`--seed` — è l'unica incoerenza vistosa: si è reso deterministico l'output degli
script lasciando non deterministico l'ambiente che li esegue.

Nota: l'audit di luglio (F3) aveva già rilevato che il claim «stdlib-only» è
falso per la pipeline skill, e lo ha risolto **al livello giusto per allora**
(il manifest dichiara `stdlib_only` e `external_deps` per tool). Manca il
livello di progetto.

**Azione (G8):** `pyproject.toml` con dipendenze pinnate e `requires-python`,
`ruff` in CI (regole minime, non un rewrite stilistico), copertura misurata e
pubblicata come numero — **senza soglia bloccante al primo giro**, perché una
soglia scelta a caso è peggio di nessuna soglia.

---

### 🟠 T3 — Due gate permanentemente non bloccanti

```yaml
- name: Shell scripts lint (shellcheck) — non-blocking
  continue-on-error: true
  run: shellcheck -S warning scripts/*.sh || true

- name: Bestiario rules check (GS benchmark, flag policy) — non-blocking
  continue-on-error: true
  run: python scripts/validate_bestiario.py --rules
```

Il primo ha **doppia** neutralizzazione (`continue-on-error` *e* `|| true`):
non può fallire nemmeno se shellcheck non è installato. Il secondo verifica il
benchmark di GS e la policy dei flag — cioè **regole di canone**, la cosa che
questo repo prende più sul serio — e il suo esito non ha conseguenze.

Un gate che non blocca produce output che nessuno legge, e col tempo diventa
rumore che maschera i gate veri. La scelta corretta è binaria: **promuovere o
rimuovere**. `plans/INDEX.md` lo sa già e lo elenca fra gli opzionali del piano
audit («opz.: shellcheck bloccante»).

**Azione (G8):** per ciascuno — misurare quanti warning produce oggi, azzerarli,
promuovere a bloccante. Se azzerarli non vale il costo, rimuovere lo step e dirlo
nel piano. Nessuno dei due resta com'è.

---

### 🔴 T4 — Deriva doc↔realtà nel file che ogni agente legge per primo

`AGENTS.md` §«What This Repo Contains» documenta tre cartelle sotto `campaign/`:

```
campaign/
├── npcs/                    # NPC cards (name, stat block, motivation, status)
├── locations/               # Location descriptions and maps metadata
├── encounters/              # Custom encounter files (CR, monsters, tactics)
```

```console
$ ls -d campaign/npcs campaign/locations campaign/encounters
ls: cannot access 'campaign/npcs': No such file or directory
ls: cannot access 'campaign/locations': No such file or directory
ls: cannot access 'campaign/encounters': No such file or directory
```

**Nessuna delle tre esiste.** I PNG vivono in `Bestiario/png/` e
`Bestiario/villain/`, con una struttura diversa e un validatore dedicato
(`validate_bestiario.py`) e una guida dedicata (`GUIDA-BESTIARIO.md`).

Il danno è a cascata, perché lo stesso file poi:

1. definisce tre **formati obbligatori** (NPC file format, Session log format,
   Encounter file format) per file che stanno in quelle cartelle inesistenti —
   il formato PNG reale è quello di `campaign/templates/png-dossier-template.md`
   e della guida bestiario, che è un altro;
2. istruisce nella tabella DO/DON'T: *«Check `campaign/npcs/` before describing
   NPCs»* — un'istruzione che ogni agente eseguirà, trovando il nulla;
3. lascia riferimenti al vecchio path anche altrove: `state.md` §8 cita
   `PNG/Salvatore/Salvatore.md`, `PNG/Azarr_Kul/…` e altri sei, tutti oggi sotto
   `Bestiario/png/`.

È il tipo di deriva che l'audit di luglio ha già combattuto con successo per i
tool (F4: «la tool map esiste solo come prosa scritta a mano e **deriva** dal
codice nel tempo» → risolto generando le tabelle dal manifest). Qui la stessa
malattia è sul documento più importante, e non ha ancora la sua cura.

**Azione (G2):** (a) correggere `AGENTS.md` allineandolo alla struttura reale,
rimuovendo i formati morti e puntando ai template/guide vivi; (b)
`scripts/validate_docs.py` — controlla che ogni percorso citato in blocchi
struttura di `AGENTS.md`, `README.md`, `docs/INDEX.md` esista davvero. È un
validatore da ~80 righe che rende la deriva **impossibile** invece che probabile.

---

### 🟢 T5 — Superficie di contribuzione non documentata a livello GitHub

| File | Stato |
|---|---|
| `CODEOWNERS` | ❌ |
| `.github/PULL_REQUEST_TEMPLATE.md` | ❌ |
| `.github/ISSUE_TEMPLATE/` | ❌ |
| `CONTRIBUTING.md` | ❌ |
| `SECURITY.md` | ❌ (marginale per questo repo) |
| `.pr-body.md` in root | ⚠️ **residuo**: corpo di una PR passata («Alliance System + Standalone Loot Generator v2»), lasciato in root |

Curiosamente il repo ha la parte **difficile** (un gate automatico che impone la
disciplina dei piani su ogni PR strutturale) e non la parte facile (un template
che spieghi al contributore cosa quel gate si aspetta). Chi apre la prima PR
scopre la regola d'oro dei piani quando la CI diventa rossa.

**Azione (G8):** PR template che riproduca la checklist della regola d'oro
(piano + INDEX + CHANGELOG nello stesso commit) e chieda esplicitamente «serve
un ADR?»; `CONTRIBUTING.md` breve che punti a `docs/INDEX.md` e a
`TOOL-AUTHORING-STANDARD.md`; rimozione di `.pr-body.md`.

---

### 🟢 T6 — I validatori che fanno da gate al contenuto non sono testati

I 70 test coprono `dmcore`, `state_apply`, `next_session`, `session_wizard`,
`campaign_branch`, `import_ultraclear`, `compile_meters`, `regions`,
`visibility`, `determinism`, `session_recap_pg`, `tools_manifest`.

Senza test:

| Script | Ruolo |
|---|---|
| `validate_bestiario.py` | **gate CI** su naming, header, CR, sync catalogo |
| `validate_modules.py` | **gate CI** sui 16 requisiti dei master DEF |
| `validate_skills.py` | **gate CI** su frontmatter, link, YAML delle skill |
| `validate_maps.py` | **gate CI** su SVG allineati |
| `build_monster_catalog.py` | genera il catalogo su cui `validate_bestiario` verifica il sync |
| `hype_homebrew.py`, `dm_dossier.py`, `build_booklet_html.py` | producono i deliverable di pubblicazione |

L'asimmetria è netta: la parte **testata** è quella che scrive canone (giusto,
è la più pericolosa), la parte **non testata** è quella che decide se il canone
è valido. Un falso negativo in un validatore è silenzioso per definizione —
la CI resta verde e nessuno lo scopre.

Da notare anche che `converters/pdf-to-md-engine/` contiene **4 file di test**
(`test_layout_extraction.py`, `test_pdf_analyzer.py`, `test_enhanced_*`) che la
CI **non esegue mai**: `unittest discover` punta solo a `scripts/tests`, e sui
converters gira solo `compileall`.

**Azione (G8):** test caso-negativo per i quattro validatori (un fixture
malformato per regola principale: deve fallire, e con l'exit code giusto);
valutare se agganciare i test dei converters o dichiararli esplicitamente
fuori CI in `tools.manifest.json` (`stability: external-toolchain` è già la
categoria giusta).

---

## 3. Osservazione architetturale: dove sta davvero il rischio

Il repo ha due sottosistemi con maturità molto diversa, e vale la pena dirlo
esplicitamente perché orienta dove mettere lo sforzo:

| Sottosistema | Maturità | Rischio residuo |
|---|---|---|
| **Automazione DM** (`scripts/`, `dmcore/`) | alta — manifest, test, determinismo, ADR | basso. Il rischio non è la qualità: è la **non adozione** (C5 — la pipeline ADR-0007 non è mai stata accesa) |
| **Contenuto di campagna** (archi, `campaign/`, `Bestiario/`, `PG/`) | alta sul contenuto recente, disomogenea sul resto | **alto** — è dove vivono tutti i finding rossi: due tempi mescolati, storia non scritta, 379 `[INFERRED]`, deliverable rotti |

La conclusione operativa è controintuitiva ma solida: **la prossima unità di
lavoro ingegneristico rende di più se applicata al contenuto, non al codice.**
I validatori proposti (`validate_links`, `validate_prose`, `validate_docs`,
`inventory_inferred`) sono tutti piccoli, tutti deterministici, tutti senza LLM
— e tutti puntati sull'unico sottosistema che oggi non ha gate proporzionati al
suo valore. Il codice, invece, ha già i suoi.

---

## 4. Cosa NON toccare

- **`render_map_svg`, `compile_map_json`, `import_ultraclear`** — byte-deterministici, testati, delicati.
- **`state_apply` / `session_wizard`** — semantica governata da ADR-0007 con 31 test. G10 li **attiva**; non li modifica.
- **Il gate `check_plans_discipline.py`** — è la cosa migliore del processo. Va esteso, semmai, non toccato.
- **La struttura del manifest e degli schema** — nuova, coerente, con generatore. Aggiungere campi se serve; non riorganizzare.
- **I converters** — funzionali, isolati, con toolchain esterna e stabilità dichiarata. Fuori scope, tranne la decisione esplicita sui loro test.
