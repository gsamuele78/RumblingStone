<!-- Report d'audit 2026-08-05 — documento di analisi. Nessuna modifica al canone. -->
# Audit globale — sintesi

**Data:** 2026-08-05 · **Commit base:** `3b9f3c3` · **Ambito:** tutto il repo
**Mandato DM:** verificare se RumblingStone segue le best practice su tre assi —
(1) **PRD / editoriale / pubblicazione**, revisione del testo e della narrazione;
(2) **coerenza del flusso, della storia e della narrazione**, con scioglimento
degli `[INFERRED]`; (3) **ingegneria del software** — design, architettura, ADR,
testing, CI/CD. Con **focus dichiarato su un tavolo di adulti**.

**Metodo:** lettura diretta delle fonti + misure riproducibili (link relativi
risolti, marcatori contati, date git, test eseguiti). Nessun punteggio «a
sensazione»: ogni numero in questo documento si ricalcola con un comando.

**Documenti di dettaglio:**

- [`AUDIT-2026-08-EDITORIALE-E-NARRATIVA.md`](AUDIT-2026-08-EDITORIALE-E-NARRATIVA.md) — assi E (editoriale), C (coerenza), M (maturità/sicurezza)
- [`AUDIT-2026-08-INGEGNERIA-ADR-CI-CD.md`](AUDIT-2026-08-INGEGNERIA-ADR-CI-CD.md) — asse T (tecnico)
- Piano d'esecuzione: [`plans/PIANO-REVISIONE-GLOBALE-2026-08.md`](../../plans/PIANO-REVISIONE-GLOBALE-2026-08.md)

Companion storico: [`AUDIT-REPORT.md`](AUDIT-REPORT.md) (audit script 2026-07-24,
F1-F9, tutte le fasi eseguite) e [`SCORECARD.md`](SCORECARD.md).

---

## 1. Verdetto

**Il repo è sopra la media di categoria su tutti e tre gli assi.** Non c'è un
solo asse in cui manchi la disciplina: mancano dei *gate* che rendano automatica
la disciplina che già esiste sulla carta.

Cosa è già maturo — e che questo audit **non propone di rifare**:

| Asse | Cosa c'è già |
|---|---|
| Architettura | 17 ADR, libreria condivisa `dmcore/`, orchestratore unico `dm.py` (ADR-0002), contratti JSON Schema, manifest machine-readable dei tool (ADR-0012) |
| Testing | 70 test, **tutti verdi**; `dm.py doctor --ci` pulito; round-trip mappe + determinismo del render in CI |
| CI | 15 step reali, non decorativi: gate manifest, validatori bestiario/moduli/skill/mappe, gate di tracciatura piani (ADR-0009) |
| Editoriale | Standard scritti e **di qualità alta**: `editorial-standards.md`, `italiano-nativo.md`, `read-aloud-adulti.md`, ADR-0016 (italiano lingua sorgente), glossario bloccato |
| Canone | Convenzione `[INFERRED — needs DM confirmation]`, regola «mai inventare» (AGENTS.md §5), Echo Ledger, doppia colonna dei tempi in `state.md` §6 |
| Contenuto | Archi 06-09 a qualità AP verificata da un validatore strutturale (16 sezioni obbligatorie) |

**Il difetto trasversale, unico, è questo:** la qualità del repo vive nelle
*regole scritte* e nella *disciplina del DM*, non negli *automatismi*. Ogni volta
che una regola non ha un gate, la regola si stacca dalla realtà — e le nove
misure di questo audit mostrano esattamente dove si è già staccata.

Il secondo difetto, più grave del primo perché tocca il tavolo: **`state.md`
mescola il tempo giocato e il tempo preparato**, e in un punto si contraddice
con se stesso. Il rimedio non va inventato — **esiste già nello stesso file**
(§6, tabella a due tempi, DM-confermata il 2026-07-04): va solo applicato alle
altre sezioni.

---

## 2. Le nove misure

Ognuna è un numero, non un'impressione. Comandi in appendice ai documenti di dettaglio.

| # | Misura | Valore | Lettura |
|---|---|---|---|
| 1 | Test unitari eseguiti / verdi | **70 / 70** | ✅ nessun debito di test *esistenti* |
| 2 | File di contenuto `.md` toccati l'ultima volta **prima** dello standard editoriale (2026-07-31) | **446 / 477 (93%)** | 🟠 il corpus precede le sue regole |
| 3 | Marcatori `[INFERRED]` | **379 in 151 file** (27 in `state.md`) | 🟠 nessun inventario, nessun ratchet |
| 4 | Log di sessione reali in `campaign/sessions/` | **1** (+1 ricostruzione con 13 `[INFERRED]`) | 🔴 ~7 archi giocati, memoria non scritta |
| 5 | Archi giocati senza alcun `.md` (01, 02, 03, 05) | **4 archi su 6** | 🔴 solo `.txt`/`.webp`/`.ods`/`.pdf` grezzi |
| 6 | Link relativi rotti (esclusi host-relative Homebrewery) | **18 / 241** | 🟠 nessun gate sui link |
| 7 | File con path assoluti della macchina del DM committati | **4** (`/home/jfs/...`) | 🟠 non portabile, non pubblicabile |
| 8 | Calchi dall'inglese (§1 `italiano-nativo.md`), misura proxy | **48 in 30 file** | 🟢 debito piccolo → gate conveniente |
| 9 | Cartelle documentate in `AGENTS.md` che non esistono | **3 su 3** (`campaign/npcs/`, `locations/`, `encounters/`) | 🔴 il file che istruisce gli agenti indica percorsi inesistenti |

---

## 3. Findings — quadro completo

Severità: 🔴 alta (blocca qualità o induce errori al tavolo) · 🟠 media · 🟢 bassa.

### Asse E — Editoriale, PRD, pubblicazione

| # | Finding | Sev |
|---|---|---|
| **E1** | **Non esiste un PRD.** Il repo non dichiara per chi produce, quali sono le classi di deliverable, e quando un deliverable è «finito». `rumblingstone-module-standard` è l'unica definizione-di-fatto e copre una sola classe (i master DEF) | 🔴 |
| **E2** | Lo standard editoriale nasce **dopo** il 93% del corpus e **nessun gate lo verifica**: `validate_modules.py` controlla la struttura (16 sezioni), non la prosa | 🟠 |
| **E3** | Un deliverable di pubblicazione è **rotto in produzione**: `PALIO-BOOKLET.hb.md` referenzia 13 asset inesistenti; 4 file contengono path assoluti `/home/jfs/...` | 🟠 |
| **E4** | Il glossario bloccato è un contratto **senza applicazione**: nessun controllo confronta i nomi nuovi con `GLOSSARIO-E-LOCALIZZAZIONE.md` | 🟢 |

### Asse C — Coerenza, flusso, storia

| # | Finding | Sev |
|---|---|---|
| **C1** | **`state.md` mescola due tempi e §1 contraddice §0**: il cruscotto dice «ARC-07 in corso, Hella morta, resurrezione = prossima»; la tabella Party colloca i 4 PG **dopo Hammerfist**, in viaggio verso mete ARC-09, con Hella «Treant Hybrid attivo post-resurrezione» e Thorik che ha già pagato −2 COS per una resurrezione non ancora avvenuta. **Il rimedio esiste già in §6** | 🔴 |
| **C2** | **Due file si dichiarano entrambi «single source of truth»**: `state.md` e `campaign-history.md`. Il secondo afferma come passato ciò che non è stato giocato | 🔴 |
| **C3** | **La storia giocata non esiste come documento** (misure 4-5): la memoria del tavolo è ricostruita, non registrata | 🔴 |
| **C4** | **379 `[INFERRED]` senza inventario né ratchet**: la convenzione è giusta, il processo di smaltimento non c'è, e nulla impedisce al numero di salire | 🟠 |
| **C5** | **La pipeline ADR-0007 è costruita, testata e mai attivata**: `doctor` segnala `campaign/group.yaml` assente e marker `auto:` assenti. L'automazione che avrebbe prevenuto C1 e C3 esiste e non è in uso | 🟠 |

### Asse M — Focus adulti e contratto di tavolo

| # | Finding | Sev |
|---|---|---|
| **M1** | Il focus «adulti» è dichiarato **in una riga di un solo file** (`campaign-dm-strategy.md`) e non è verificabile per beat: nessun test dice se una scena offre davvero scelta con costo reale | 🟠 |
| **M2** | **Non esiste un contratto di contenuto e sicurezza**: il corpus tratta morte con costo permanente, corruzione dell'anima a prezzo di livelli negativi, guerra con 210 caduti nominati, sfruttamento di minori — senza confine dichiarato, senza note di contenuto per arco, senza strumento di stop condiviso (session zero / lines & veils / X-card). Per un tavolo di adulti non è censura: è **avere il confine deciso prima, non durante** | 🔴 |

### Asse T — Ingegneria, ADR, testing, CI/CD

| # | Finding | Sev |
|---|---|---|
| **T1** | **Non esiste CD.** La CI valida, nulla pubblica: nessun release, nessun tag, nessun artefatto versionato per il gruppo. L'unico output è `build/` con retention 14 giorni, e contiene solo i pacchetti skill | 🔴 |
| **T2** | **Igiene di progetto Python assente**: nessun `pyproject.toml`/`requirements.txt` (la CI fa `pip install pyyaml` **non pinnato** → build non riproducibile), nessun linter/formatter, nessuna misura di copertura, nessun `.pre-commit-config.yaml` | 🟠 |
| **T3** | **Due gate CI permanentemente non bloccanti** (`shellcheck`, `validate_bestiario --rules`): warning che nessuno legge. Un gate che non blocca va promosso o rimosso, non lasciato verde per sempre | 🟠 |
| **T4** | **Deriva doc↔realtà in `AGENTS.md`**: documenta tre cartelle inesistenti e tre formati-file che nessuno usa; i PNG vivono in `Bestiario/png/`. È il file che ogni agente legge per primo | 🔴 |
| **T5** | Superficie di contribuzione non documentata a livello GitHub: nessun `CODEOWNERS`, PR/issue template, `CONTRIBUTING`. Residuo `.pr-body.md` in root | 🟢 |
| **T6** | **I validatori che fanno da gate al contenuto non sono testati**: nessun test per `validate_bestiario`, `validate_modules`, `build_monster_catalog`, `hype_homebrew`, `dm_dossier`, `build_booklet_html` | 🟢 |

---

## 4. Roadmap — findings → lotti

Ordine scelto su due criteri: **prima ciò che riduce errori al tavolo**, poi ciò
che richiede una decisione del DM o un'intervista.

| Lotto | Copre | Sblocca | Dipende da | Taglia |
|---|---|---|---|---|
| **G1** — Due tempi uniformi in `state.md` + declassamento `campaign-history.md` | C1, C2 | il tavolo smette di leggere fatti non ancora giocati | — | M |
| **G2** — Bonifica deriva doc↔realtà + gate `validate_docs.py` | T4 | gli agenti smettono di cercare cartelle inesistenti | — | S |
| **G3** — `validate_links.py` + riparazione dei 18 link + purga dei path locali | E3, misure 6-7 | i booklet tornano pubblicabili | — | S |
| **G4** — Inventario `[INFERRED]` + gate ratchet | C4 | il debito smette di crescere | — | S |
| **G5** — PRD + ADR matrice delle edizioni | E1 | ogni lotto successivo ha un «finito» dichiarato | decisione DM | M |
| **G6** — Contratto di tavolo + ADR contenuto/sicurezza + Adult Design Test | M1, M2 | il focus adulti diventa verificabile | decisione DM | M |
| **G7** — `validate_prose.py` + passata di revisione sui 30 file | E2, E4 | lo standard editoriale entra in vigore davvero | G5 | L |
| **G8** — Igiene Python + CI hardening | T2, T3, T5, T6 | build riproducibile, gate onesti | — | M |
| **G9** — Pipeline CD + ADR di release/versioning | T1 | il gruppo riceve PDF versionati | G8 | M |
| **G10** — Attivazione ADR-0007 (branch gruppo, marker `auto:`, primo `session end` reale) | C5 | la memoria del tavolo si scrive da sola | collaudo al tavolo | S |
| **G11** — Ricostruzione della storia giocata (archi 00-06) | C3, misure 4-5 | la campagna ha una memoria | intervista DM + G10 | L |

**G1, G2, G3, G4 sono eseguibili subito e senza alcuna decisione del DM.**
G5 e G6 sono le due decisioni che il DM deve prendere perché tutto il resto
dell'asse editoriale abbia un metro. G11 è il lotto più grande ed è **gated
sull'intervista al DM**: nessun agente può ricostruire da solo date, giocatori
presenti, XP e bottino reali — quelli non stanno nei file (è la stessa ragione
per cui il task B1 di ARC-07 è fermo da luglio).

---

## 5. Cosa questo audit NON propone di toccare

Per la stessa prudenza dell'audit di luglio:

- **Renderer e parser delle mappe** (`render_map_svg`, `compile_map_json`,
  `import_ultraclear`): logica delicata, byte-deterministica, coperta da test.
- **Il contenuto degli archi 06-09**: è il materiale migliore del repo e ha già
  passato tre piani di revisione dedicati. L'asse E lo tocca solo dove i
  *deliverable generati* sono rotti (E3), mai la sostanza narrativa.
- **La semantica di `state_apply`/`session_wizard`** (ADR-0007): governata da ADR
  e da 70 test. G10 la **attiva**, non la modifica.
- **I nomi già in uso**: il glossario lo vieta esplicitamente («non uniformare i
  nomi esistenti: sono in centinaia di file»). E4 controlla i nomi *nuovi*.
- **Le decisioni di canone del DM**: questo audit non scioglie un solo
  `[INFERRED]`. Li conta, li inventaria e prepara le domande.
