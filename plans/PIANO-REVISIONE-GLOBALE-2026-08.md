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

## Stato: 🟡 in esecuzione — 8 lotti chiusi su 17

G0, G1, G2, G2-bis/ter/quater e **G3** chiusi (2026-08-09: la decisione A1 è caduta, era un bug del generatore) + tre correzioni di canone su segnalazione del DM.
**Aperti**: G4-G15. Motore, effort e sequenza consigliata: [§ Come si esegue](#come-si-esegue--motore-effort-sequenza).
**Il percorso critico passa da te**: `G5` (destinatari) è ferma da luglio e blocca cinque lotti.

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
- [x] **G2 — Bonifica deriva doc↔realtà + `validate_docs.py`** *(T4 — 🔴)* — ✅ **eseguito 2026-08-05**
      `AGENTS.md` allineato al filesystem reale: il blocco-struttura di
      `campaign/` non elenca più `npcs/`, `locations/`, `encounters/` (mai
      esistite) ma le cartelle vere (`recaps/`, `templates/`, `ai-media-prompts/`,
      `GLOSSARIO`); il **formato-scheda PNG morto** è sostituito da un puntatore
      alle fonti vive (`campaign/templates/png-dossier-template.md` +
      `GUIDA-BESTIARIO.md`, già applicate in CI da `validate_bestiario.py`); il
      **formato encounter** rimanda a `rumblingstone-module-standard` +
      `validate_modules.py`; la riga DO/DON'T ora manda a `Bestiario/png/` e
      `Bestiario/villain/`; la regola 5 non punta più a
      `campaign/lore/rhod-adaptations.md`, **che non è mai esistito**. `README.md`
      corretto negli stessi due punti.
      **Nuovo gate `scripts/validate_docs.py`** (stdlib-only, deterministico,
      exit 0/1/2, `--json` opt-in): verifica i percorsi citati in blocchi-albero,
      link relativi e path inline di `AGENTS.md`/`README.md`/`docs/INDEX.md`.
      Progettato per **non dare falsi positivi** — accetta l'abbreviazione ADR
      (`plans/adr/ADR-0003` → un solo file; se il prefisso è ambiguo, errore),
      scarta i modelli di nome (`YYYY-MM-DD_session-N.md`) e i mirror generati, e
      offre le direttive `<!-- validate-docs: ignore -->` / `ignore-begin/end`
      per i passaggi che **citano un percorso proprio per dire che non esiste**
      (senza quella via d'uscita il gate impedirebbe di documentare i propri
      errori). Manifest + registry rigenerati (41 tool), **10 test nuovi**
      (80 totali), step **bloccante** in CI + smoke `--help`.
- [x] **G2-bis — `state.yaml`: i fatti come dati validati, la prosa in markdown** *(rinforzo strutturale di C1 — [ADR-0017](adr/ADR-0017-stato-dati-e-prosa.md))* — ✅ **eseguito 2026-08-05**
      *Origine*: domanda del DM — «non sarebbe meglio un formato meno prono alle
      allucinazioni, e i changelog in un file separato?». Misurato prima di
      decidere: `state.md` era **1677 righe, di cui 1150 (68%) di changelog**; del
      contenuto vivo, **215 righe tabellari e 234 di prosa**. Da qui la scelta
      **ibrida** invece della conversione integrale: convertire la prosa in JSON
      avrebbe perso leggibilità **senza guadagnare nulla** contro le allucinazioni.
      **YAML e non JSON**: JSON non ammette commenti, e il file è fatto di
      annotazioni datate; il repo ha già 5 file dati YAML.
      **Il vincolo che chiude C1 alla radice**: nello schema `oggi` è obbligatoria
      e `tempo: giocato|in_corso|preparato` pure — **un fatto senza tempo dichiarato
      non è esprimibile**. G1 l'aveva risolto per convenzione; qui è il file a non
      passare il gate. Limite dichiarato nell'ADR: lo schema vincola la *forma*,
      non la *verità* — impedisce quella classe di errore, non le allucinazioni.
      **Un master, mai due**: le tabelle §0/§1/§6 di `state.md` sono **generate**
      da `render_state.py` dentro regioni marcate. Il lotto è stato eseguito tutto
      insieme proprio per questo: creare `state.yaml` senza il rendering avrebbe
      prodotto una seconda fonte di verità, cioè il finding **C2** appena chiuso.
      **Split dello storico**: `campaign/state-changelog.md`, append-only.
      **`state.md` passa da 1677 a 546 righe.**
      `[INFERRED]` diventa **record tipizzato** (`id`, `dove`, `domanda`, `a_chi`,
      `aperto_dal`): le due domande aperte di G1 sono ora INF-001 e INF-002, con la
      domanda già formulata per il DM. **Questo cambia il progetto di G4**:
      l'inventario si legge dai dati invece di estrarlo dal markdown.
      Migrazione **incrementale**: §3 è il candidato successivo; §2, §4, §5 e §7
      restano prosa. Due gate **bloccanti** nuovi, 13 test nuovi (80 → **93**).

- [x] **G2-ter — una sola via di scrittura: sessione → stato** *(chiude il buco lasciato da G2-bis — [ADR-0017](adr/ADR-0017-stato-dati-e-prosa.md) §4-bis)* — ✅ **eseguito 2026-08-05**
      *Origine*: domanda del DM — «come interagisce lo stato della sessione col
      nuovo campaign state? c'è un metodo automatico che aggiorna puntualmente lo
      stato evitando errori di formattazione?». Verificando invece di rispondere a
      memoria è emersa **una regressione mia**: G2-bis aveva rotto
      `state_apply --migrate` spostando §8 (corretta in un commit separato).
      **Migrate a dati** (decisione DM: «fino a §4 e ai numeri di §2»): **§3**
      clock dei villain, **§4** chi sa cosa, **§2.4** contingenti e scenari di
      Rethmar. `state.yaml` passa da 3 a **7 sezioni**, tutte con `tempo`
      obbligatorio; sette regioni generate in `state.md`.
      **Front-matter dei delta**: il log di sessione resta markdown (è un
      documento) ma porta in testa i delta in forma leggibile dalla macchina,
      **emessi dal wizard** — il DM non scrive YAML. Prima i delta si estraevano
      con regex sulla prosa e i clock villain con una **lista di nomi cablata nel
      sorgente**: Ghaurush, canonizzato il 2026-08-05, non sarebbe stato visto.
      C'è un test che lo dimostra. Retrocompatibile: senza front-matter si ricade
      sulle regex.
      **Il giro si chiude**: `state_apply` scrive i clock in `state.yaml`, poi
      **rigenera la vista** — altrimenti il gate `render_state --check` diventa
      rosso. Scrittura **testuale mirata**, non round-trip YAML, per non perdere
      l'intestazione commentata.
      **Tre domande nuove al DM** (INF-003/004/005), fra cui una incoerenza vera
      trovata dalla classificazione: tre righe canonizzate il 2026-08-05 dicono
      che Ghaurush, Zin'thara e Ushgar sanno dei «Custodi Eterni», **titolo che si
      conferisce nell'Arco 08, non ancora giocato**.
      Regola R2 ora **derivata dallo schema** invece che cablata (si era già
      disallineata al primo lotto). 99 test (da 95).
      **Ci si ferma qui**: §5 e §7 restano prosa — vedi ADR-0017 §4.

- [x] **G2-quater — prodotto e partita: il reset per gruppo nuovo** *([ADR-0017](adr/ADR-0017-stato-dati-e-prosa.md) §7)* — ✅ **eseguito 2026-08-05**
      *Origine*: domanda del DM — «un DM nuovo deve poter partire pulito senza
      sporcare l'originale». Verificando: **il meccanismo perdeva**.
      `new-campaign-group.sh` azzerava solo `state.md` e `sessions/`, quindi un
      gruppo nuovo ereditava `state.yaml` (643 righe), `state-changelog.md`
      (1165), `campaign-history.md` (517) e i recap del gruppo precedente — **le
      prime due falle aperte da me** in G2-bis/ter. E `state-blank.md` non aveva
      i marcatori `gen:state:`: **CI rossa al primo push**.
      **Regola resa esplicita**: *prodotto* (archi, Bestiario, mappe, skill,
      premessa, house rules) **resta**; *partita* (stato, storico, cronaca,
      sessioni, recap) **si azzera da template**.
      **Split di `campaign-history.md`**, che mescolava i due: `campaign-premise.md`
      (AP, ambientazione, grafo villain, riferimenti) è prodotto; `campaign-chronicle.md`
      (party, timeline, catena dei dungeon) è partita. La catena dei dungeon è
      finita nella cronaca **perché l'ha imposto un test**: le sue annotazioni
      dicevano dove Hella è morta e cosa Artemis ha rifiutato.
      Tre template nuovi (`state-blank.yaml`, `state-changelog-blank.md`,
      `chronicle-blank.md`), marcatori nel template markdown, reset che rigenera
      e valida prima di dichiararsi finito.
      **Il presidio è un test, non la disciplina**: `test_new_group.py` verifica
      che **ogni** file di stato sia coperto dal reset e che i template non
      contengano tracce del primo gruppo. 109 test (da 99).
      **Non deciso qui**: branch-per-gruppo vs directory-per-gruppo — dipende da
      **G5**, ed è la seconda decisione che si incaglia lì.

- [x] **G3 — `validate_links.py` + riparazione link e path locali** *(E3 — 🟠)* — ✅ **eseguito 2026-08-06**, **chiuso del tutto il 2026-08-09**
      Nuovo gate **bloccante** su **tutti** i `.md` del repo: link relativi rotti
      **e** percorsi assoluti della macchina di chi scrive. Su 597 file trovava
      **18 link rotti e 25 percorsi assoluti**.
      **Due classi erano falsi positivi**, ed è la parte che decide se un gate
      sopravvive: le guide di deploy dei `converters/` contengono legittimamente
      percorsi di **server** (`/home/htmlconverter/`, `/home/linuxbrew/`) — non è <!-- validate-links: ignore -->
      la macchina di una persona, e `converters/` è già `external-toolchain`
      (ADR-0011), quindi escluso con motivo scritto nel sorgente; e i **documenti
      d'audit** citano `/home/jfs/` **proprio per segnalarlo** — direttiva, non <!-- validate-links: ignore -->
      bonifica.
      **Difetti veri riparati**: i 2 link `file:///home/jfs/…` della scheda Bracieri <!-- validate-links: ignore -->
      ora puntano al master vivo (`ARC07-DEF-1`, quello citato non esiste più); i
      **2 `cd /home/jfs/…` del PLAYBOOK**, che insegnavano a un DM terzo un comando <!-- validate-links: ignore -->
      con dentro la home di un altro; l'immagine dell'Anello, che esisteva come
      `.png` mentre il riferimento diceva `.webp`. Più **un bug mio di G2-quater**:
      il link in `chronicle-blank.md` era relativo alla *destinazione* e non alla
      posizione del template.
      **I 13 asset del Palio: la diagnosi era sbagliata** — errata del
      2026-08-09. Non erano «mai prodotti»: sono tutti in
      `09_…/P2D-Palio-Allegati/`, e ci sono sempre stati. I capitoli vivono in
      `09_…/`, il booklet si genera in `09_…/homebrew/`, e la via `.hb.md`
      copiava i percorsi relativi **senza rebasarli sulla cartella d'uscita**.
      ⚠️ **La toppa era peggio del difetto**: G3 aveva incollato
      `validate-links: ignore` **dentro il `.hb.md` generato** — cioè a mano su
      un artefatto, contro ADR-0003 — zittendo il gate invece di guardare il
      generatore; alla prima rigenerazione le direttive sono sparite e i 13 link
      sono tornati. Corretto in `build_booklet_html.py`
      (`rebase_relative_links()`), 6 test di regressione, decisione A1 **caduta**.
      **Regola che resta**: un gate che dà fastidio si crede prima di metterlo a
      tacere, e un artefatto generato non si tocca mai a mano.
      44 tool a manifest, 15 test nuovi (109 → **125**). <!-- validate-links: ignore -->
- [ ] **G4 — Inventario `[INFERRED]` + ratchet** *(C4 — 🟠)*
      `scripts/inventory_inferred.py` → `docs/audit/INFERRED-INVENTARIO.md`
      raggruppato per file/tema/domanda-al-DM, così che il DM possa smaltirli a
      lotti. `--check` in CI: il conteggio non sale rispetto alla baseline.
      Ratchet, non divieto: aggiungerne uno resta legittimo e aggiorna la baseline.

- [ ] **G14 — Le schede dei PG nel repo, e i costi che nessuno riporta** *(nuovo — trovato il 2026-08-09 — 🟠)*
      Due difetti della stessa famiglia, emersi correggendo il pegno del rito.
      **(a) Manca la scheda di Thorik.** Tordek, Artemis e Hella hanno una
      cartella sotto `PG/Artefatti/Artefatti-Pg/`; **il portatore della Corona
      no**. È esattamente il motivo per cui il suo **−2 DES** ha potuto sparire
      senza che nessuno se ne accorgesse: non esisteva un posto dove *sarebbe
      dovuto stare*, quindi la sua assenza non era osservabile.
      **(b) I consolidamenti tengono i poteri e perdono i costi.** Il blocco
      «Effetti Meccanici Corona» di `PortaleForgia-P1` elenca **−2 DES**, **+4
      CAR**, immunità alla paura, scurovisione 36 m e la **non-rimovibilità**.
      Nessuna delle tre generazioni successive di schede lo riporta: tutte
      elencano **solo i poteri**. È una **classe** di difetto, non un caso —
      va cercata su **tutti** gli artefatti vivi (Aegis Fang, Anello, Bracieri,
      Collana, Cuore di Moradin), non solo sulla Corona.
      **Deliverable**: 4 schede PG minime **come dati** (`PG/schede/<pg>.yaml`:
      caratteristiche, modificatori permanenti con la loro fonte, artefatti
      portati) + `validate_pg.py` che verifica che **ogni modificatore permanente
      dichiarato in un modulo giocato compaia sulla scheda del PG che l'ha
      subito**, con la citazione del file d'origine + passata su tutti gli
      artefatti vivi.
      **Serve al DM**: la scheda di Thorik (ce l'ha al tavolo, non nel repo) e la
      decisione **INF-007** (valgono ancora +4 CAR, immunità paura, scurovisione
      36 m e soprattutto la **non-rimovibilità** della Corona?).
- [ ] **G15 — Echo Ledger: passata di revisione e regola di riscrittura** *(nuovo — 🟡)*
      Gli echi **E-07c** ed **E-07e** hanno richiesto **due** giri di correzione,
      e il secondo solo perché il DM ha insistito: la prima volta erano stati
      **rinominati invece che riscritti**. Un'eco costruita per un monaco
      («una parata che prima gli riusciva») non diventa l'eco di un guerriero
      cambiandole il nome sopra — e un'eco *rovesciata* su chi non ha fatto
      nessuna scelta non è un'eco, è una riga.
      **Deliverable**: (1) passata su **tutti** gli echi armati, con la domanda
      «questo eco regge se cambio l'autore? se sì è scritto male»; (2) regola
      nuova in `consequence-echoes.md`: *un'eco che cambia autore si **riscrive
      da zero** o si **annulla** — mai si rinomina, e l'ID non si riusa*;
      (3) l'Echo Ledger diventa **dati** in `state.yaml` (`echi:` con `id`,
      `autore`, `data`, `stato` ∈ {armato, sparato, annullato}) e la tabella di
      §7.E si genera, come già §0/§1/§6 — così un'eco non può più esistere senza
      autore dichiarato. **Non** tocca il testo dei payoff: quella resta prosa.
      **Serve al DM**: confermare o cassare gli echi rivisti (E-07f in testa).

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

### Onda 5 — multi-gruppo (PR dedicata)

- [ ] **G12 — `groups/<slug>/`: il multi-gruppo diventa una directory** *([ADR-0018](adr/ADR-0018-directory-per-gruppo.md))*
      **Decisione presa il 2026-08-05**, esecuzione in una **PR dedicata** dopo
      G3/G4 — è un diff enorme su file di canone e va rivisto da solo.
      Il gruppo esistente diventa **`groups/rumblingstone/`**; `campaign/` resta
      **solo prodotto**.
      **Risoluzione del gruppo**: `--group` > `RUMBLINGSTONE_GROUP` >
      `.rumblingstone-group` (gitignored, da `.example`) > gruppo unico nel
      registro > errore. `groups/registry.yaml` è **committato**, perché gli
      agenti AI non eseguono il resolver e su un clone fresco il puntatore
      locale non esiste: col registro, «un solo gruppo → usalo» diventa il
      meccanismo che li fa orientare da soli.
      **Slug** `^[a-z0-9][a-z0-9-]{1,30}$`: elimina la classe di problemi che le
      virgolette curerebbero solo come sintomo.
      **Un solo resolver** `dmcore/groups.py`: nessuno script conosce più un
      percorso di stato — oggi `campaign/state.yaml` è cablato in sei punti.
      **Guardia** portata dal branch alla directory: blocca le **scritture di
      canone** con gruppo non risolto o verso un gruppo diverso da quello
      attivo; **non** blocca i commit al prodotto.
      *Gate*: dopo G3/G4.
- [ ] **G13 — `dm.py brief --for-agent`: il context pack** *([ADR-0018](adr/ADR-0018-directory-per-gruppo.md) §6)*
      Pacchetto **generato** dai dati (~200 righe): confine giocato/preparato,
      party di oggi, clock attivi, fili aperti, `[INFERRED]` pendenti, ultime
      sessioni. **Nessun memory store esterno** — sarebbe non versionato, non
      revisionabile e divergente dal repo, cioè il finding C2 in forma invisibile.
      **Vincolo**: è un **indice, non un riassunto** — ogni riga porta il
      puntatore al dato pieno, altrimenti l'agente che deve approfondire finisce
      in un vicolo cieco.

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

## Come si esegue — motore, effort, sequenza

> Perché questa sezione esiste: il piano era *corretto* ma non *completabile*.
> Mancavano tre cose — **quanto costa ogni lotto**, **con che motore conviene
> farlo**, e **in che ordine**, dato che l'effort che conta davvero non è quello
> dell'agente ma **quello del DM**: è l'unica risorsa che non si parallelizza.

**Scala dell'effort agente** (una «sessione» = un turno di lavoro che si chiude
con una PR verde): **XS** ≤ ½ sessione · **S** 1 · **M** 2-3 · **L** 4-6 ·
**XL** 7+.

| Lotto | Motore consigliato | Perché quel motore | Agente | DM | Dipende da |
|---|---|---|---|---|---|
| **G4** — inventario `[INFERRED]` + ratchet | **Sonnet 5** | conteggio, raggruppamento, gate: lavoro meccanico e verificabile, zero giudizio editoriale | **S** | — | — |
| **G14** — schede PG + costi persi | **Sonnet 5** (script) + **Opus 5** (passata artefatti) | lo schema e il validatore sono meccanici; capire *quale* costo è stato perso e da dove richiede lettura incrociata di più generazioni di documenti | **M** | scheda di Thorik + **INF-007** (~15 min) | — |
| **G15** — Echo Ledger | **Opus 5** | è narrazione: giudicare se un'eco «regge il cambio d'autore» non è meccanizzabile | **S** | conferma degli echi rivisti (~20 min) | — |
| **G5** — PRD + matrice edizioni | **Opus 5** | è il documento che decide il *significato* di finito per tutto il resto; sbagliarlo propaga su G7 e G9 | **M** | **30-45 min di intervista** — è il collo di bottiglia | ⛔ decisione DM |
| **G6** — contratto di tavolo + ADR contenuto + Adult Design Test | **Opus 5** | temi maturi e sicurezza: nessun automatismo, e il contratto lo **scrive il DM** | **M** | **45-60 min** (session zero) | ⛔ decisione DM |
| **G7** — `validate_prose.py` + bonifica 30 file | **Sonnet 5** (validatore) + **Opus 5** (revisione) | il validatore codifica regole già scritte; la revisione della prosa è giudizio, ed è il lotto dove un motore debole fa danni invisibili | **L** | approvazione a campione | **G5** |
| **G8** — igiene Python + CI hardening | **Sonnet 5** | `pyproject`, `ruff`, test caso-negativo, template: tutto verificabile dalla CI stessa | **M** | — | — |
| **G9** — pipeline CD + ADR release | **Sonnet 5**, ADR rivisto in **Opus 5** | la pipeline è meccanica; *cosa* versiona il tag è una decisione di prodotto | **M** | ~10 min (canale di distribuzione) | **G8**, **G5** |
| **G12** — `groups/<slug>/` | **Opus 5** | diff enorme su file di canone + resolver + guardia: è il lotto con più modi silenziosi di rompere qualcosa | **L** | review della PR | **G4** |
| **G13** — `brief --for-agent` | **Sonnet 5** | generatore deterministico da dati già tipizzati | **S** | — | **G12** |
| **G10** — accensione pipeline ADR-0007 | **Haiku 4.5** o **Sonnet 5** | comandi già scritti e testati: qui serve esecuzione, non progettazione | **XS** | **una sessione reale al tavolo** | ⛔ tavolo |
| **G11** — ricostruzione archi 00-06 | **Opus 5** | è il lotto dove inventare canone è più facile e più grave: serve il motore che sa **fermarsi** e marcare `[INFERRED]` | **XL** | **7 tornate di domande**, una per arco | ⛔ intervista |

**Perché non tutto in Opus.** Su lavoro meccanico e verificabile dalla CI
(G4, G8, G9, G13) il motore più forte non produce un risultato migliore: produce
lo stesso risultato più lentamente. La regola che uso qui è **«chi verifica il
lavoro?»** — se lo verifica un gate, basta Sonnet; se lo verifica solo un lettore
umano (prosa, canone, echi, PRD), serve Opus.

### Sequenza consigliata — cinque tappe

**Tappa 1 — subito, nessuna decisione tua** (agente: ~S+M+S)
`G4` → `G14` → `G15`. Chiudono i tre debiti che questo thread ha portato a
galla e non aspettano niente. Alla fine: gli `[INFERRED]` sono un inventario
smaltibile a lotti, le quattro schede PG esistono e un gate impedisce che un
costo permanente sparisca di nuovo, gli echi sono dati con un autore obbligatorio.

**Tappa 2 — il collo di bottiglia** (tuo: ~1h30 in due sedute)
`G5` (destinatari e ambizione editoriale) e `G6` (confini di contenuto).
⚠️ **Sono ferme da luglio e bloccano cinque lotti**: G7, G9, ADR-0005 e la sorte
della bonifica IP del Palio. Finché non le prendi, la Onda 3 non parte — e
adesso c'è un vincolo in più da valutare: la **serie Golarion degli stemmi**
usa IP Paizo e non è portabile in un'edizione commerciale.

**Tappa 3 — infrastruttura, in parallelo alla 2** (agente: ~M+M)
`G8` → `G9`. Non dipendono da te salvo dieci minuti su G9. Effetto collaterale
che vale da solo: **costruire i booklet in CI** avrebbe intercettato il giorno
stesso sia il finding E3 sia il bug del rebase.

**Tappa 4 — la PR grossa, da sola** (agente: ~L+S)
`G12` → `G13`. Decisione già presa (ADR-0018), esecuzione in PR dedicata perché
è un diff enorme su file di canone e va rivisto senza altro rumore intorno.

**Tappa 5 — gated su di te e sul tavolo** (agente: ~XS+XL)
`G10` alla prima sessione reale; `G11` quando accetti l'intervista, un arco per
tornata. `G7` si incastra qui, dopo G5.

**Percorso critico**: `G5` → `G7` → `G9`. Tutto il resto è parallelizzabile.
Se hai un'ora sola da dare a questo piano, spendila sulla **Tappa 2**.

---

## Gate / decisioni che servono al DM

| # | Domanda | Blocca |
|---|---|---|
| 1 | Destinatari e ambizione editoriale: solo tavolo? anche DM terzi? edizione pubblica? | G5 → e a cascata G7, G9 |
| 2 | Confini di contenuto del tavolo e strumento di stop condiviso | G6 |
| ~~3~~ | ~~I 13 asset del `PALIO-BOOKLET`~~ — ✅ **caduta il 2026-08-09**: gli asset esistevano, non li raggiungeva il generatore | — |
| 4 | Intervista di ricostruzione, arco per arco | G11 |
| 5 | Prima sessione reale col flusso `dm.py session end` | G10 |
| 6 | **INF-007** — valgono ancora +4 CAR, immunità alla paura, scurovisione 36 m e la **non-rimovibilità** della Corona, che stanno nello stesso blocco del −2 DES reintegrato? | G14 |
| 7 | La **scheda di Thorik**: la porti nel repo? È l'unico PG che non c'è, ed è il motivo per cui un suo malus permanente è potuto sparire | G14 |
| 8 | Gli **echi rivisti** (E-07c riscritta, E-07e annullata, **E-07f** nuova): confermi o cassi? | G15 |

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
