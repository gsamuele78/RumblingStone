# PIANO — Revisione globale: editoriale/PRD, coerenza narrativa, ingegneria e CI/CD

> **Ambito**: tutto il repo — contenuto di campagna, documentazione di prodotto,
> infrastruttura.
> **Origine**: richiesta DM 2026-08-05 — verificare se RumblingStone segue le
> best practice su (1) PRD editoriale e pubblicazione, con revisione del testo e
> della narrazione; (2) coerenza del flusso, della storia e della narrazione,
> con scioglimento degli `[INFERRED]`; (3) design del software, architettura,
> ADR, testing e CI/CD. Focus dichiarato su **tavolo di adulti**.
> **Decisioni DM (2026-08-05)**: audit prima, esecuzione dopo · ricostruire la
> storia giocata marcando le inferenze · «adulti» = rigore di design **e** temi
> maturi **e** contratto di sicurezza · CI da irrobustire **+** CD reale **+**
> ADR mancanti.

## Stato: 🟡 in esecuzione — G0 e G1 chiusi (2026-08-05)

**Audit (lotto G0) — completato.** Tre documenti in `docs/audit/`:

- [`AUDIT-2026-08-SINTESI.md`](../docs/audit/AUDIT-2026-08-SINTESI.md) — verdetto, 9 misure, 17 finding, roadmap
- [`AUDIT-2026-08-EDITORIALE-E-NARRATIVA.md`](../docs/audit/AUDIT-2026-08-EDITORIALE-E-NARRATIVA.md) — assi E, C, M con le prove
- [`AUDIT-2026-08-INGEGNERIA-ADR-CI-CD.md`](../docs/audit/AUDIT-2026-08-INGEGNERIA-ADR-CI-CD.md) — asse T

**Verdetto in una riga**: il repo è sopra la media di categoria su tutti e tre
gli assi; il difetto trasversale è che la qualità vive nelle *regole scritte* e
non negli *automatismi*, e nel punto peggiore (`state.md` §1) questo ha già
prodotto una contraddizione interna che il DM leggerebbe a inizio sessione.

---

## Lotti

Ordine per **rischio al tavolo**, non per comodità di esecuzione.
G1-G4 non richiedono alcuna decisione del DM e sono eseguibili subito.

- [x] **G0 — Audit read-only** (2026-08-05): 3 documenti, 9 misure riproducibili,
      17 finding con severità. Nessuna modifica a canone, codice o CI.

### Onda 1 — riduce errori al tavolo, nessuna decisione richiesta

- [x] **G1 — Due tempi uniformi in `state.md` + declassamento di `campaign-history.md`** *(finding C1, C2 — 🔴)* — ✅ **eseguito 2026-08-05**
      Nuova **§-1** in testa a `state.md`: legenda dei due tempi (🎬 OGGI AL
      TAVOLO / 📋 PREPARATO) e **confine dichiarato** (giocati Archi 00-06 e
      ARC-07 fino al P4 incluso; da giocare P3B, P5, D16, poi 08-09).
      **§1 Party** portata a due colonne come §6: la colonna «Today» dice che i
      quattro sono nella **Sala della Forgia Eterna** e che **Hella è morta**,
      col template Ibrido Treant **non** attivo. **Banner dei due tempi** in testa
      a **§2, §4, §5**, con l'elenco delle righe da leggere come futuro e la
      conseguenza operativa a verbale: *nessun PNG può ancora riconoscere i PG
      come Custodi Eterni, perché il titolo si conferisce nell'Arco 08*.
      `campaign-history.md` non è più autoproclamato sorgente unica; intestazione
      nuova col confine giocato/preparato e avviso sulla riga di Hella («✅ Alive,
      resurrected as Treant Hybrid»), marcata 📋 in tabella.
      **Nessun contenuto cancellato: solo etichettato.**
      **Due domande lasciate aperte al DM** invece di risolverle d'ufficio, perché
      sono canone e non bonifica editoriale — entrambe marcate `[INFERRED]` nel
      punto in cui vivono e registrate in `state.md` §8:
      1. il **−2 COS permanente di Thorik** è il prezzo della resurrezione di
         Hella (non ancora giocata) o è residuo della sua morte all'Arco 00?
      2. il **Giorno di Marcia**: §2.1 dichiara 19 «Terrelton just fell as
         Hammerfist ended», ma l'orologio Hammerfist in testa al file è a
         **3g 16h** → il giorno reale sarebbe **~15**. Non corretto d'ufficio
         perché alimenta i numeri di §2.4 e la finestra quest di Arco 09.
- [ ] **G2 — Bonifica deriva doc↔realtà + `validate_docs.py`** *(T4 — 🔴)*
      Allineare `AGENTS.md` alla struttura reale (le tre cartelle inesistenti, i
      tre formati morti, la riga DO/DON'T che manda a `campaign/npcs/`);
      aggiornare i path `PNG/…` → `Bestiario/png/…` nei riferimenti superstiti.
      Nuovo validatore: ogni percorso citato nei blocchi-struttura di
      `AGENTS.md`/`README.md`/`docs/INDEX.md` deve esistere. Gate CI.
- [ ] **G3 — `validate_links.py` + riparazione link e path locali** *(E3 — 🟠)*
      Validatore link relativi + path assoluti, con allowlist per gli
      host-relative Homebrewery (`/assets/…`) e i placeholder didattici.
      Riparare i 17 rotti reali (13 asset del `PALIO-BOOKLET` — produrre o
      rimuovere i riferimenti, decisione contenutistica da porre al DM),
      sostituire i 4 path `/home/jfs/…` con path relativi. Gate CI.
- [ ] **G4 — Inventario `[INFERRED]` + ratchet** *(C4 — 🟠)*
      `scripts/inventory_inferred.py` → `docs/audit/INFERRED-INVENTARIO.md`
      raggruppato per file/tema/domanda-al-DM, così che il DM possa smaltirli a
      lotti. `--check` in CI: il conteggio non sale rispetto alla baseline.
      Ratchet, non divieto: aggiungerne uno resta legittimo e aggiorna la baseline.

### Onda 2 — richiede una decisione del DM

- [ ] **G5 — PRD + ADR «matrice delle edizioni»** *(E1 — 🔴)*
      `docs/PRD.md`: destinatari, classi di deliverable, definizione di «finito»
      per classe, matrice delle edizioni (tavolo / giocatori / DM terzo /
      pubblica). Scritto **estendendo** il modello di
      `rumblingstone-module-standard`, che è già un PRD per una classe.
      Sblocca la decisione ferma da luglio su ADR-0005 (bonifica §7 Palio).
      **Serve al DM**: destinatari e ambizione editoriale.
- [ ] **G6 — Contratto di tavolo + ADR contenuto/sicurezza + Adult Design Test** *(M1, M2 — 🔴/🟠)*
      1. `campaign/CONTRATTO-DI-TAVOLO.md` — session zero, confini dichiarati,
         strumento di stop, rinegoziazione. **Compilato dal DM**: è l'unico
         documento del repo il cui contenuto non è deducibile dai file.
      2. ADR «contenuto maturo e sicurezza al tavolo», con la conseguenza per le
         edizioni derivate (un DM terzo eredita il materiale senza il contesto
         del tavolo che l'ha accettato).
      3. **Adult Design Test** in `rumblingstone-module-standard`, sul modello
         del PC Protagonism Test già esistente: scelta reale, costo visibile
         prima di scegliere, fallimento che produce storia. Sezione dichiarativa
         nei master DEF + riga in `validate_modules.py`.
      4. Campo `content-notes:` per arco.

### Onda 3 — editoriale e infrastruttura

- [ ] **G7 — `validate_prose.py` + passata di revisione** *(E2, E4 — 🟠/🟢)*
      Validatore deterministico **senza LLM** che codifica le regole
      meccanizzabili di `italiano-nativo.md` §1 (calchi) e §9 (tic ripetitivi);
      warning per i nomi propri nuovi assenti dal glossario. Poi bonifica dei
      **30 file** con calchi misurati. Le regole non meccanizzabili (ritmo,
      respiro, voce) restano giudizio umano e **non** entrano nel gate.
      *Dipende da G5* (il livello di finitura per classe decide quanto è severo).
- [ ] **G8 — Igiene Python + CI hardening** *(T2, T3, T5, T6 — 🟠/🟢)*
      `pyproject.toml` con dipendenze **pinnate** e `requires-python`; `ruff` in
      CI (regole minime); copertura misurata e pubblicata **senza soglia
      bloccante al primo giro**. Promuovere o rimuovere i due gate
      `continue-on-error` (shellcheck, `validate_bestiario --rules`): nessuno
      dei due resta com'è. Test caso-negativo per i 4 validatori. PR template
      con la checklist della regola d'oro, `CONTRIBUTING.md`, rimozione di
      `.pr-body.md`. Decisione esplicita sui 4 test dei `converters/` mai eseguiti.
- [ ] **G9 — Pipeline CD + ADR release/versioning** *(T1 — 🔴)*
      `.github/workflows/release.yml`: su tag `v*` → booklet HTML+PDF, pacchetti
      skill, `registry.json`, allegati a una GitHub Release. ADR su cosa versiona
      il tag (il **materiale**, non il canone giocato) e cosa entra in ciascuna
      edizione. *Dipende da G8* (build riproducibile) e da G5 (matrice edizioni).
      Effetto collaterale utile: costruire i booklet in CI avrebbe intercettato
      E3 il giorno stesso.

### Onda 4 — gated sul tavolo e sull'intervista al DM

- [ ] **G10 — Attivazione della pipeline ADR-0007** *(C5 — 🟠)*
      `dm.py session branch --group …`, `state_apply.py --migrate` per creare le
      regioni `auto:`, primo `dm.py session end` reale. Lotto **piccolo** con
      effetto sproporzionato: è l'unico che rende automatica la prevenzione di
      C1 e C3 per il futuro. *Gate*: prima sessione reale al tavolo.
- [ ] **G11 — Ricostruzione della storia giocata (archi 00-06)** *(C3 — 🔴)*
      Arco per arco, dal materiale grezzo (`.txt`, `.ods`, `.pdf`), in **batch di
      domande al DM** — una tornata per arco: date, presenti, XP, bottino, tre
      decisioni chiave. Output nel formato log di `AGENTS.md`. Ogni buco non
      colmato resta `[INFERRED]`, mai riempito d'invenzione (AGENTS.md §5).
      Modello già collaudato: `campaign/sessions/RETROATTIVI-ARC07-INFERRED.md`.
      *Gate*: intervista al DM — è la stessa ragione per cui il task B1 di ARC-07
      è fermo da luglio, e nessun agente può sbloccarla da solo.

---

## Gate / decisioni che servono al DM

| # | Domanda | Blocca |
|---|---|---|
| 1 | Destinatari e ambizione editoriale: solo tavolo? anche DM terzi? edizione pubblica? | G5 → e a cascata G7, G9 |
| 2 | Confini di contenuto del tavolo e strumento di stop condiviso | G6 |
| 3 | I 13 asset del `PALIO-BOOKLET`: produrli o rimuovere i riferimenti? | chiusura di G3 |
| 4 | Intervista di ricostruzione, arco per arco | G11 |
| 5 | Prima sessione reale col flusso `dm.py session end` | G10 |

---

## Invarianti da rispettare

- **Nessuna invenzione di canone.** G11 in particolare è il lotto dove sarebbe
  più tentante violare AGENTS.md §5: ogni buco resta `[INFERRED]`.
- **Nessun contenuto preparato viene cancellato** da G1: viene *etichettato*.
- **Non uniformare i nomi esistenti** (divieto esplicito del glossario): i gate
  di G7 guardano solo i file e i nomi nuovi.
- **Renderer/parser mappe e semantica `state_apply` non si toccano**: G10 attiva,
  non modifica.
- **Nessun gate nuovo nasce non bloccante**: se non è pronto a bloccare, non entra
  in CI (è la lezione di T3).
- Regola d'oro dei piani: ogni lotto chiuso aggiorna, nello stesso commit, la
  checklist qui sopra + `plans/INDEX.md` + `plans/CHANGELOG.md`.
