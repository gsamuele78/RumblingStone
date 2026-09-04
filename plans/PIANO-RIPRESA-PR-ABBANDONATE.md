# PIANO — La ripresa delle quattro PR abbandonate

> **Stato**: 🔵 **approvato dal DM, non ancora eseguito** · **Aperto**: 2026-09-04
> **Richiesta-fonte (DM, 2026-09-04)**: *«R8 ok, in un'altra chat; qui fai il
> piano completo con tutte le fasi, che poi si mergia»*.
> **Esecuzione**: in sessioni dedicate, **una fase alla volta**. Questo documento
> è il contratto: chi apre quella sessione legge qui cosa fare e come si verifica.

## Che cos'è, e che cosa non è

Quattro PR aperte contengono lavoro **valido e non superato**: nessuno le ha
riprese, ma il contenuto è ancora l'unico che quei problemi abbia.
`PIANO-RICONCILIAZIONE-PR-APERTE` le ha giudicate una per una, **verificandole
sul codice di oggi** invece di leggerne il corpo. Questo piano dice **in che
ordine** e **con che criterio** si portano dentro.

**Non è** un piano per mergiare quattro branch. Tre di quelle PR hanno una base
vecchia di mesi, e in due casi il valore sta nel **contenuto**, non nei commit.
La domanda operativa non è «si mergia?» ma **«cosa di questo vale, e come lo
porto su `main` in modo verificabile?»** — e la risposta cambia per ognuna.

**Ordine approvato dal DM**: **#63 → #52 → #106 → #99**. Non è cronologico né per
dimensione: è per **rapporto fra ciò che sblocca e ciò che rischia**.

| | PR | Cosa sblocca | Rischio | Costo misurato |
|---|---|---|---|---|
| F0 | — | ✅ **chiusa il 2026-09-04**: `⛰` è un muro, e nessun master esce dal controllo | — | ADR-0043 |
| F1 | **#63** | 14 griglie tattiche che al tavolo mancano | basso | contenuto pronto, SVG **già byte-identici** |
| F2 | **#52** | l'overlay `@` su master scritti a mano | basso | **una rinominazione** |
| F3 | **#106** | catena raster riproducibile + Blender | medio | serve la **GPU del DM** per l'ultimo passo |
| F4 | **#99** | i dati di campagna come dati | **alto** | 88 file, tocca il canone |

---

## FASE 0 — Audit e prerequisiti

Da fare **una volta**, prima di F1, e vale per tutte e quattro.

### 0.1 · Quello che è già misurato, e non va rifatto

| Fatto | Come è stato verificato |
|---|---|
| Gli SVG di #63 si rigenerano **byte-identici** con lo script di oggi | rigenerato il master L3 dalla PR con `render_map_svg.py` corrente e confrontato byte a byte: 5 su 5 uguali, nonostante **222 commit** e un rifacimento del renderer |
| Su `main` i tre master Ultra-Clear hanno **un `map01` ciascuno** | `ls` di `08_…/Mappe/rendered/`: 3 mappe su 17 |
| La **3Y Ponte Sospeso** non ha griglia in tutto il repo | `grep -rn "3Y"`: compare solo nell'atlante e nel `Lotto-3` deprecato |
| #63 cancella 7 SVG di master che **tiene** | i master `Lotto-*` della PR generano ancora 7 mappe: verificato rigenerandoli |
| `validate_maps` **non se ne accorge** | rende solo i markdown con almeno un SVG committato: togliendoli tutti, il master esce dal controllo |
| 2 SVG su 3 di #52 sono **byte-identici**; il terzo cambia **solo di nome** | rigenerati e confrontati: `…grid-6553-scal` → `…grid-65-53-sca`, contenuto identico |
| `comfyui_batch.py` e `render_map_blender.py` **non esistono** su `main` | `ls scripts/` |
| Su `main` non c'è **nessuna** direttiva `@` sulle due mappe di #52, né la scena «Foresta in Fiamme» | `grep -n "@compass\|@path\|@zone\|@mark"` |

### 0.2 · Il prerequisito ✅ CHIUSO il 2026-09-04, insieme al bug di `⛰`

Il DM ha messo `⛰` in cima alla coda — *«aprilo assolutamente come bug da fixare
prima di tutti»* — e i due difetti sono usciti insieme perché sono la stessa
famiglia: **cose che il codice dava per buone senza che nessuno le contasse**.
Entrambi chiusi da
[ADR-0043](adr/ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md).

**`⛰` non è un muro nell'export** — 2.423 celle in 21 file. La `Hammerfist-L1`
ha 338 celle di montagna e produceva **8 segmenti**: tutta la catena invisibile
al VTT. Adesso **20**.

**Il punto cieco di `validate_maps`** — rendeva solo i markdown con almeno un SVG
committato, quindi cancellarli tutti faceva **sparire il master dal controllo**.
Adesso un master che genera mappe e non ha nessun SVG è un **errore**, salvo che
si dichiari nel proprio testo con
`<!-- validate_maps: non-renderizzato — motivo -->`.

🔎 **Il gate ha trovato due casi già in `main`** appena acceso: due master di
ARC-09 con quattro mappe mai renderizzate. Renderizzate: **31 SVG / 17 master**
(erano 27 e 15).

⚠️ **Cosa cambia per F1.** La #63 **non può più** cancellare i sette SVG dei
master `Lotto-*` in silenzio: o si rigenerano, o quei master si archiviano, o si
dichiarano. La decisione D1 resta, ma adesso è **forzata dalla CI** invece che
affidata a chi legge il diff.

### 0.3 · Il vincolo che si applica a tutte

- **Nessuna PR si mergia per il numero.** Se il contenuto vale, entra; se non
  vale, la PR si chiude con la motivazione scritta. Il conteggio delle PR aperte
  non è un obiettivo.
- **Ogni fase è un commit che passa tutti i gate**, con piano + `INDEX` +
  `CHANGELOG` nello stesso commit (regola d'oro).
- **La base è vecchia: si porta il contenuto, non i commit**, salvo dove il
  branch si rebasa pulito. In entrambi i casi il criterio di accettazione è che
  gli artefatti si **rigenerino** dal sorgente, non che il diff applichi.

---

## FASE 1 — #63: le 14 griglie tattiche di Hammerfist

**Perché per prima.** È l'unica delle quattro che si sente **al tavolo**: oggi
un DM che gioca ARC-08 ha tre mappe su diciassette, e l'incontro del Ponte
Sospeso non ha una griglia da nessuna parte. Il contenuto è pronto e verificato,
e il costo è quasi zero.

### 1.1 · Cosa entra

| Artefatto | Cosa |
|---|---|
| `Hammerfist-L1-REVISED-Ultra-Clear.md` | da 1 a **3** mappe (torrione di vedetta, sentiero nascosto, campo della Mano Rossa) |
| `Hammerfist-L2-REVISED-Ultra-Clear.md` | da 1 a **3** (fortezza top-down, disposizione Giorno 1, attacco del drago) |
| `Hammerfist-L3-REVISED-Ultra-Clear.md` | da 1 a **5** (cortile sfondato, **3Y ponte sospeso**, 3Z incrocio silenzioso, cuore della montagna, battaglia finale terrestre) |
| `ARC08-00-INDICE`, `ARC08-01-GUIDA-DM`, `ARC08-04-MARCIA`, `Atlante` | puntamenti riallineati alle mappe nuove |

### 1.2 · Cosa NON entra così com'è

🐛 **La cancellazione dei 7 SVG dei master `Lotto-*` deprecati.** Con il
controllo di 0.2 attivo, quella cancellazione **fa rossa la CI** — ed è giusto
così. Due strade, e la scelta è del DM:

- **(a)** si tengono i 7 SVG. I master deprecati restano rigenerabili e
  tracciabili; costo: 7 file che nessuno guarda;
- **(b)** i tre master `Lotto-*` finiscono in `_ARCHIVIO/` con la stessa
  procedura già usata per i 16 sorgenti assorbiti di ARC-07 (`git mv` +
  riscrittura controllata dei riferimenti + `README.md` che documenta la
  politica). Allora la cancellazione degli SVG è **conseguente**, non silenziosa.

📌 **Proposta**: la **(b)**. Il repo ha già la procedura, i `Lotto-*` sono
sorgenti assorbiti esattamente come quelli di ARC-07, e lasciare in `Mappe/` tre
master deprecati accanto ai tre definitivi è la condizione che genera il prossimo
errore di puntamento.

### 1.3 · Come si porta dentro

Il branch ha **222 commit** di distanza dalla base. Non si rebasa: si **porta il
contenuto**, e lo si riverifica.

1. Estrarre dal branch i **tre master markdown** e i quattro file di puntamento.
2. Applicarli su un branch nuovo da `main`, risolvendo a mano i conflitti sui
   quattro file di puntamento (che nel frattempo sono cambiati: `ARC08-01-GUIDA-DM`
   ha avuto tre commit, fra cui la reintegrazione dell'Incontro 2F).
3. **Rigenerare gli SVG da zero** con `render_map_svg.py`. Non copiare quelli
   della PR: si rigenerano, e devono venire identici — è già stato provato su L3.
4. Eseguire la scelta 1.2 (archiviazione o mantenimento).

### 1.4 · Validazione

- `validate_maps` verde **col controllo nuovo di 0.2 attivo**
- `validate_modules` sui master ARC-08
- ogni link relativo nei quattro file di puntamento risolve
- **conteggio**: 17 mappe tattiche presenti, la **3Y** fra queste
- `pytest`, `dm.py doctor --ci`, `check_plans_discipline`

**Definizione di fatto**: un DM che apre `ARC08-01-GUIDA-DM` e cerca un incontro
qualsiasi trova la griglia, e nessun link punta a un master archiviato.

---

## FASE 2 — #52: l'overlay professionale sulle mappe degli incendi drow

**Perché per seconda.** Costa **una rinominazione** e chiude una dimostrazione
che serve al metodo, non solo a quella scena.

### 2.1 · Cosa entra, e perché il valore non è il disegno

Il pezzo che conta è la **prova che le direttive `@` di
[ADR-0006](adr/ADR-0006-annotazioni-mappa-overlay-professionale.md) funzionano
sui master scritti a mano**, non solo su quelli compilati da JSON — e **in
place**, senza ricostruire la griglia, quindi senza perdere il disegno
esistente. Oggi i 14 master che usano le direttive sono tutti generati.

| Artefatto | Cosa |
|---|---|
| `SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md` | direttive `@` su **Campo Drow 2**: bussola, rotte di pattuglia/assalto/squadre incendiarie, zone etichettate, landmark (Wyrmlord, tesoro, prigioni) |
| `…P1B-Cerchio-Treant-COMPLETO-maps.md` | direttive `@` sul **Cerchio Sacro** + **primo SVG committato** per quella mappa |
| `…P1B-Foresta-In-Fiamme` (`.json` + master + SVG) | scena nuova: piromanti drow, **fronte del fuoco** (vento da est), avanzata PG, treant alleato di Hella, ritirata drow, e gli **stati di propagazione** nel blocco EVOLUZIONE |

### 2.2 · L'unico intoppo, ed è meccanico

Il terzo SVG cambia nome: `…grid-6553-scal.svg` → `…grid-65-53-sca.svg`.
Non è marciume: è la **`slug` corretta** dal lotto A di
`PIANO-QUALITA-DEL-CODICE`, che aveva trovato sette implementazioni diverse e
**tutte e sette** incollavano `65×53` in `6553`. Si rigenera e il nome giusto
esce da solo.

### 2.3 · Come si porta dentro, e la verifica

Come F1: contenuto, non commit. Estrarre i master e il JSON, applicarli su
`main`, **rigenerare tutti gli SVG**.

- `validate_maps` verde (attesi **+3** SVG, di cui uno rinominato)
- gli SVG rigenerati coincidono con quelli della PR **tranne** il nome del terzo
- la scena nuova passa `validate_modules`
- la scala della campagna è rispettata: **1,5 m/quadretto**

**Definizione di fatto**: `grep` delle direttive `@` trova i due master scritti
a mano fra quelli che le usano, e la scena «Foresta in Fiamme» ha un SVG.

---

## FASE 3 — #106: la catena dei raster e Blender come geometria

**Perché per terza.** Vale molto e non è urgente al tavolo: nessuna sessione si
blocca perché mancano i diciotto raster del Drappo. E l'ultimo passo **non si può
fare qui**: serve la macchina del DM.

### 3.1 · Cosa entra

**`comfyui_batch.py`** (567 righe, 216 di test). Il markdown resta il master
(ADR-0003) e diventa **eseguibile**: un commento HTML sopra ogni blocco di
prompt porta `id`, `size`, `stile`, `serie`, `seed`. Il prompt si corregge **nel
documento, mai nello script**.

**`render_map_blender.py`** (381 righe + 346 nello script Blender, 202 di test).
Risolve la geometria con la **stessa `paint()`** che alimenta l'SVG: non è una
comodità, è la garanzia che le due catene **non possano** divergere.

### 3.2 · Misurato contro la pratica dell'illustrazione AI-aided: cinque su sei

| Requisito | #106 |
|---|---|
| Prompt, seed, modello e risoluzione **fuori dal codice** | ✅ annotazione in commento HTML, invisibile nel rendering |
| **Determinismo prima della scelta** | ✅ seed derivato dall'`id` con SHA-256, non sorteggiato: due macchine partono dalle stesse diciotto immagini. `--reroll N` cambia tentativo in modo altrettanto ripetibile |
| **Provenienza scritta** | ✅ `PROVENIENZA.txt` con file · modello e versione · **licenza dei pesi** · seed · data · chi — e **nasce prima** delle immagini |
| **Igiene di licenza sui pesi** | ✅ **exit 1 nel codice**, non un avvertimento, se il checkpoint contiene `flux1-dev` e varianti — e *prima* di ogni scrittura e di ogni chiamata di rete (ADR-0019: la licenza è dei pesi, non del software) |
| **Condizionamento da geometria reale** | ✅ `--profondita`: il pass Z alimenta ControlNet depth, coi due passi scritti nel codice perché non li salti — **normalizza** (il pass Z è in metri, un PNG no) e **inverti** (ControlNet vuole il vicino chiaro): saltare l'inversione dà un'immagine che *sembra* giusta e guida il modello al contrario |
| **Il giudizio umano nel ciclo** | ⚠️ **manca** |

### 3.3 · Il sesto requisito, e il deliverable che F3 aggiunge

`--fissa-seed` registra **la scelta**, ma non c'è dove scrivere **cosa è stato
scartato e perché**. `rumblingstone-art-direction` dice che un'immagine **si
butta** invece di tenerla perché «è già venuta» — e quel giudizio, che è il
lavoro vero, oggi non lascia traccia.

**Deliverable 3.3**: un `SCARTI.txt` accanto a `PROVENIENZA.txt`, con la stessa
forma — `id · seed · reroll · motivo`. Il motivo è **testo libero e obbligatorio**:
serve a chi rifà la serie fra un anno per non ripercorrere gli stessi vicoli
ciechi. È il file che trasforma diciotto immagini scelte in **una serie
motivata**.

### 3.4 · Le tre decisioni di `render_map_blender.py` che si vedono solo nel risultato

1. **Nessun piano di appoggio** — ogni cella è un solido, terreno compreso: con
   un piano sotto, una voragine resterebbe coperta e il passo di profondità la
   leggerebbe **piatta**, cioè proprio l'informazione per cui il passo esiste.
2. **Le celle uguali si fondono in rettangoli** — la Ruota passa da **2.944 cubi
   a 38 solidi**.
3. **L'asse Y si ribalta** — quello di Blender sale, quello della griglia scende:
   senza il ribaltamento la mappa esce **speculare**, l'errore che non si nota
   finché qualcuno non cerca la curva nord a sud.

### 3.5 · Il taglio: cosa si fa qui e cosa sulla macchina del DM

| | Dove |
|---|---|
| Gli **script**, i test, i gate, `SCARTI.txt`, la documentazione | ✅ **qui** |
| I **diciotto raster** | 🖥 **macchina del DM** — questo ambiente non ha GPU (`nvidia-smi` assente) e ComfyUI non è in ascolto |
| Il **render Blender** | 🖥 **macchina del DM** — il binario non c'è |

⚠️ **Il collo di bottiglia è il giudizio, non la GPU**: ~1,5-2 ore, e quasi tutte
sono scegliere quale delle quattro varianti tenere.

### 3.6 · Validazione

- `pytest` sui due file di test (218 test fra i due, già scritti)
- smoke in CI: `--help`, `--lista`, `--dry-run`, più il **controllo di
  determinismo** del piano di scena 3D
- `test_serie_base_e_diciotto` — il capitolato dice diciotto, i prompt sono
  venti: le due tavole in più sono `serie=extra` e la CI si fa rossa al
  diciannovesimo. **Non è un divieto: è un modo di obbligare a decidere**
- `tools_manifest --check` con i due tool nuovi
- verifica esplicita del divieto: un checkpoint `flux1-dev` **esce 1 prima** di
  scrivere qualsiasi cosa

---

## FASE 4 — #99: i dati di campagna come dati

**Perché per ultima.** È la più grossa (88 file, +14.078 / −4.931) e tocca la
parte più delicata del repo — **il canone**. E il suo corpo lo dice da sé:
*«è nata read-only, la riga originale non vale più»*.

### 4.1 · Il vincolo che governa tutta la fase

🔴 **Non si mergia in blocco.** La PR ha già i lotti separati nel corpo, e si
prendono **uno alla volta**, ciascuno col suo commit e i suoi gate.

⚠️ **La correzione del Peso è già uscita** e non va riportata: è il lotto R1 di
`PIANO-RICONCILIAZIONE-PR-APERTE`, già su `main`.

### 4.2 · L'ordine dei lotti, dal meno al più invasivo

| # | Lotto | Cosa porta | Perché in questa posizione |
|---|---|---|---|
| 4a | **G2** — `validate_docs.py` | gate bloccante sulla deriva doc↔realtà | **Indipendente da tutto.** Chiude un difetto reale: `AGENTS.md` documentava `campaign/npcs/`, `locations/`, `encounters/` — **nessuna delle tre è mai esistita**. Ed è progettato attorno ai falsi positivi: alla prima esecuzione **9 hit di cui 4 falsi**, corretti nel validatore e non nei documenti |
| 4b | **G3** — link e path locali | 18 link relativi rotti su 241 · 4 file con path assoluti `/home/jfs/…` | igiene pura, nessuna decisione |
| 4c | **G1** — i due tempi di `state.md` | §1 collocava i PG **dopo Hammerfist** mentre §0 marca l'arco 08 `⬜ NON giocato` | ⚠️ tocca il canone, ma **non cancella niente: etichetta**. Estende la tabella a due tempi che §6 aveva già, DM-confermata. Porta con sé **due domande al DM** (il −2 COS di Thorik, il Giorno di Marcia 19 vs ~15) |
| 4d | **G2-bis** — ADR-0017, `state.yaml` | i fatti come dati, `state.md` **generato** | il pezzo grosso. Vedi 4.3 |
| 4e | **G2-ter** — una sola via di scrittura | clock villain, «chi sa cosa», numeri di Rethmar migrati a dati; il log di sessione prende un front-matter coi delta | dipende da 4d |
| 4f | **G2-quater** — prodotto e partita | il reset per gruppo nuovo **perdeva**: azzerava `state.md` e `sessions/` e lasciava `state.yaml`, `state-changelog.md`, `campaign-history.md` e i recap al gruppo dopo | dipende da 4d/4e |
| 4g | schede PG a dati | `PG/schede/*.yaml` + `.md` generati | oggi le schede PG **non esistono come dato** da nessuna parte |
| 4h | ADR-0018 — `groups/<slug>/` | multi-gruppo per directory invece che per branch | **PR dedicata**, come dice la #99 stessa |

### 4.3 · Il lotto 4d, e perché vale la pena

Misurato **prima** di decidere: `state.md` era **1.677 righe, di cui 1.150 (68%)
di changelog**; delle 527 vive, 215 tabellari e 234 di prosa. Da lì l'**ibrido**
invece della conversione integrale — e **YAML invece di JSON**, perché JSON non
ammette commenti e un file di canone senza commenti è un file che nessuno
correggerà mai.

**Il vincolo che chiude alla radice il difetto dei due tempi**: `oggi` e `tempo`
**obbligatori** nello schema. Un fatto senza tempo dichiarato **non è
esprimibile**.

**Un master, mai due**: le tabelle di `state.md` diventano generate. Il file
passa da 1.677 a **546 righe**; lo storico esce in `state-changelog.md`.

⚠️ **Il limite, dichiarato dall'ADR stesso e da tenere in vista**: lo schema
vincola la **forma**, non la **verità**. Un fatto sbagliato con un tempo giusto
passa.

### 4.4 · La regressione da non ripetere

🔁 La #99 racconta una sua regressione: lo split dello storico aveva rotto
`state_apply --migrate`, e **la CI non l'aveva vista** perché quei test girano su
fixture. Ha aggiunto due test **sui file veri**.

**Vincolo per 4d/4e**: ogni lotto che tocca `state_apply` o `render_state`
aggiunge almeno un test **sul file vero**, non solo su fixture. È il punto in cui
questo piano può fallire più silenziosamente.

### 4.5 · La misura da guardare in faccia

La #99 la scrive nel suo audit, ed è il motivo per cui questa fase esiste:

> *«La pipeline che avrebbe prevenuto questi difetti è costruita, ha 31 test, è
> al ~98% — e non è mai stata accesa.»*

Il difetto trasversale che l'audit trova è uno solo: **la qualità vive nelle
regole scritte e non negli automatismi**, e ogni regola senza gate si è già
staccata dalla realtà di qualche misura.

### 4.6 · Validazione

Oltre ai gate soliti, per ogni lotto di F4:

- `validate_state` · `render_state --check` · `validate_pg` (dove pertinente)
- **`state.md` rigenerato dev'essere identico a quello committato** — è il
  controllo che tiene in piedi «un master, mai due»
- per 4c e 4f: **nessun contenuto preparato cancellato**, solo etichettato
- per 4f: un test che dimostri che il reset per gruppo nuovo **non eredita
  niente** — è la falla che quel lotto chiude, e due delle sue perdite le aveva
  aperte l'agente stesso

---

## Piano di validazione trasversale

Vale per **ogni** commit di **ogni** fase.

| Gate | Comando |
|---|---|
| test | `python3 -m pytest scripts/tests/ -q` |
| skill e instradamento (ADR-0041) | `python3 scripts/validate_skills.py` |
| mappe | `python3 scripts/validate_maps.py` |
| moduli | `python3 scripts/validate_modules.py` |
| bestiario | `python3 scripts/validate_bestiario.py` |
| manifest dei tool | `python3 scripts/tools_manifest.py --check` |
| ambiente | `python3 scripts/dm.py doctor --ci` |
| disciplina dei piani | `python3 scripts/check_plans_discipline.py` |

**Invarianti che nessuna fase può violare** (ereditate dalla #99 e da ADR-0041):

- nessuna invenzione di canone — quello che non è attestato si marca
  `[INFERRED — needs DM confirmation]`
- nessun contenuto preparato cancellato: **si etichetta**
- i nomi esistenti non si uniformano
- **nessun gate nuovo nasce non bloccante**
- ogni lotto chiuso aggiorna checklist + `INDEX` + `CHANGELOG` **nello stesso
  commit**

---

## Le decisioni che restano al DM

| # | Fase | Domanda |
|---|---|---|
| D1 | F1 | I tre master `Hammerfist-Lotto-*` deprecati: **si archiviano** in `_ARCHIVIO/` (proposta) o **si tengono coi loro SVG**? |
| D2 | F3 | I diciotto raster si generano **sulla tua macchina** — quando? La fase si chiude senza, ma la catena resta non collaudata sul risultato vero |
| D3 | F4 · 4c | Le due domande di G1: il **−2 COS di Thorik** e il **Giorno di Marcia 19 vs ~15** |
| D4 | F4 | I **13 stemmi e mappe** del `PALIO-BOOKLET` che la #99 lascia in sospeso: si producono o si tolgono i riferimenti? |
| ~~D5~~ | ~~fuori piano~~ | ✅ **deciso e fatto il 2026-09-04**: il DM l'ha messo in cima alla coda, ed è chiuso insieme al punto cieco di `validate_maps` (ADR-0043) |
| D6 | F1 | `…P1C-Rituale-COMPLETO-SCALE` mappa 3 dichiara **40×40** e ha **26×29** celle: il renderer avvisa e disegna lo stesso. La griglia è contenuto — la ridisegno o la lascio con l'avviso? |

---

## Come si misura che il piano è finito

Non «quattro PR chiuse». Queste:

1. Un DM che gioca **ARC-08** trova la griglia di ogni incontro, **3Y compresa**.
2. Le direttive `@` funzionano su master scritti a mano, e c'è **una mappa che lo
   dimostra** oltre a quelle generate.
3. La serie dei diciotto raster si **rifà da capo** su un'altra macchina, e si sa
   **cosa era stato scartato e perché**.
4. Un fatto di canone **senza tempo dichiarato non è esprimibile**, e `state.md`
   si rigenera identico dal suo `state.yaml`.

⚠️ E una cosa che il piano **non** promette: che il canone sia vero. I gate
verificano forma, copertura e coerenza fra artefatti. La verità di quello che è
successo al tavolo la sa solo il DM.
