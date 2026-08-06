<!-- Report d'audit 2026-08-05 — dettaglio assi E/C/M. Documento di analisi, nessuna modifica al canone. -->
# Audit globale — editoriale, coerenza narrativa, focus adulti

**Data:** 2026-08-05 · **Commit base:** `3b9f3c3`
Sintesi e roadmap: [`AUDIT-2026-08-SINTESI.md`](AUDIT-2026-08-SINTESI.md).

Questo documento contiene le **prove**: per ogni finding, il file e la riga da
cui viene, e il comando con cui il numero si ricalcola.

---

## Asse E — Editoriale, PRD, pubblicazione

### 🔴 E1 — Non esiste un PRD: il repo non dichiara cosa produce, per chi, e quando è finito

Il repo ha una quantità notevole di documentazione **operativa** (come si fa una
cosa) e **decisionale** (perché è fatta così: 17 ADR). Non ha documentazione di
**prodotto**: nessun file risponde alle domande che un PRD esiste per fissare.

| Domanda di prodotto | Dove si risponde oggi |
|---|---|
| Chi è il destinatario? Solo il DM? Il gruppo? Un DM terzo che eredita la campagna? | Nessuna risposta unica. `README.md` dice cosa c'è; `DM-QUICKSTART-NUOVI-DM.md` presuppone un DM terzo; ADR-0005 presuppone una possibile edizione pubblica |
| Quali sono le classi di deliverable e il livello di finitura di ciascuna? | Solo per **una**: `rumblingstone-module-standard` (master DEF). Handout, recap, brief, teaser, booklet, dossier, schede PG, mappe: nessun livello dichiarato |
| Quando un arco è «pubblicabile» invece che «giocabile»? | Non definito. `plans/INDEX.md` traccia il % dei *piani*, non la maturità dei *deliverable* |
| Quali edizioni esistono (tavolo / giocatori / DM terzo / pubblica) e cosa cambia fra loro? | ADR-0016 definisce la **lingua** delle edizioni, non il **contenuto** di ciascuna |

**Perché conta, concretamente.** La domanda «puntiamo a un'edizione
commerciale?» è aperta da luglio e **blocca lavoro reale**: `plans/INDEX.md`
riga «VERIFICA LEGALE-IP (P2D Palio)» ha la bonifica del §7 (rinomina contrade,
riscrittura motti, riambientazione fuori FR) in stato ⬜ *gated* su una decisione
che nessun documento è deputato a prendere. Un PRD è il posto dove quella
decisione vive.

**Nota di merito**: `rumblingstone-module-standard/SKILL.md` è, di fatto, un PRD
per una classe di deliverable — ed è ben fatto (nasce da una checklist approvata
dal DM, PR #61, con un'implementazione di riferimento citata). Il lotto G5 va
scritto **estendendo quel modello** alle altre classi, non inventandone un altro.

**Azione (G5):** `docs/PRD.md` + ADR «matrice delle edizioni e definizione di
finito per classe di deliverable».

---

### 🟠 E2 — Lo standard editoriale nasce dopo il 93% del corpus, e nessun gate lo verifica

Lo standard **esiste ed è di qualità alta**. Tre riferimenti nella skill
`rumblingstone-narrative-style`:

| File | Cosa fissa | Data git |
|---|---|---|
| `references/editorial-standards.md` | impaginazione | 2026-07-30 |
| `references/italiano-nativo.md` | la lingua: 10 calchi tipici + §9 «tic dell'IA» | 2026-08-01 |
| `references/read-aloud-adulti.md` | registro del read-aloud per adulti | 2026-08-01 |
| `plans/adr/ADR-0016` | italiano lingua sorgente, inglese edizione derivata | 2026-08-01 |

`italiano-nativo.md` nasce da un rilievo dei giocatori del 2026-07-31 — gli
handout *«sembrano traduzioni maldestre dall'inglese»* — ed è esattamente la
lamentela che ha originato questo audit. **La regola è giusta e recente. Il
corpus è vecchio.**

```
# file di contenuto .md e ultima modifica rispetto allo standard
totale: 477   scritti/toccati prima del 2026-07-31: 446   (93%)
```

Due conseguenze distinte:

1. **Nessuna passata retroattiva è mai avvenuta.** Lo standard vale per ciò che
   si genera da agosto in poi; i 446 file precedenti non sono stati riletti.
2. **Nessun gate misura la prosa.** `validate_modules.py` è un ottimo validatore
   *strutturale* — verifica la presenza di 16 sezioni obbligatorie (INDICE,
   QUICKSTART, Tattiche round-per-round, Contingenze, ramo sconfitta, Echo
   Ledger, budget PX, scala 1,5 m…) — ma per costruzione non guarda **come è
   scritta** una frase. Il commento nel sorgente lo dice: *«review automatica e
   SENZA token (niente LLM)»*.

**Il debito reale è però piccolo**, ed è la parte buona della misura. Proxy su
due delle dieci regole di `italiano-nativo.md` §1:

```
possessivo su parti del corpo («la sua mano», «il suo respiro»):  48 occorrenze
soggetto esplicito ridondante («Lui si voltò»):                    2 occorrenze
file toccati da almeno un calco:                                  30 file
```

30 file su 477. **Un gate deterministico è quindi conveniente**: costa poco,
blocca la regressione, e la bonifica dell'arretrato è un lavoro finito, non
infinito. È il caso classico in cui conviene automatizzare *prima* di bonificare.

**Azione (G7):** `scripts/validate_prose.py` — stesso stile degli altri
validatori (exit 1 bloccante, warning non bloccanti, nessun LLM), che codifica
le regole meccanicamente verificabili di `italiano-nativo.md` §1 e §9; poi
passata sui 30 file. Le regole **non** meccanizzabili (ritmo, respiro, voce)
restano giudizio umano e non entrano nel gate.

---

### 🟠 E3 — Un deliverable di pubblicazione è rotto, e 4 file contengono path della macchina del DM

Misura su 241 link relativi in file `.md` (esclusi gli host-relative di
Homebrewery `/assets/…`, che risolvono sul dominio Homebrewery e non sono un
difetto, e i placeholder letterali):

```
link relativi controllati: 241
rotti (reali):              18
```

Ripartizione:

| Quanti | Dove | Natura |
|---|---|---|
| 13 | `09_…/homebrew/PALIO-BOOKLET.hb.md` | stemmi delle contrade (8 `.svg`), mappe (`piazza-del-palio`, `channathgate-citta`, `rotta-soccorso`, `stalla-assalto-drow`), panorama `.png` — **asset mai prodotti**. Il booklet si genera, ma esce con 13 immagini rotte |
| 3 | `PG/Artefatti/…/Tordek/03_Risveglio_Completo_Bracieri_Terra.md` (×2), `07_…/_ARCHIVIO/…-alternative.md` | `file:///home/jfs/Scrivania/00-Giochi_di_ruolo/…` — **path assoluti della macchina del DM**, committati nel canone | <!-- validate-links: ignore -->
| 1 | `PG/Artefatti/…/ringOfChaoticIllumination/00_Ring…Revised.md` | `ring-chaotic-illumination-evolved.webp` assente |
| 1 | `docs/guides/GUIDA-IMMAGINI.md` | `percorso/relativo/immagine.png` — placeholder didattico, **falso positivo accettabile** (da mettere in allowlist) |

Path locali della macchina, cercati su tutto il repo:

```
campaign/DM-CAMPAIGN-PLAYBOOK.md:214   cd /home/jfs/00_Antigravity_workspace/RumblingStone <!-- validate-links: ignore -->
campaign/DM-CAMPAIGN-PLAYBOOK.md:476   cd /home/jfs/00_Antigravity_workspace/RumblingStone <!-- validate-links: ignore -->
PG/Artefatti/…/Tordek/03_Risveglio_Completo_Bracieri_Terra.md:5, :174
07_…/_ARCHIVIO/PortaleForgia-P4-PianoTerra-COMPLETO-alternative.md:770
```

Due li conosce già il repo: `PG/Artefatti/…/Tordek/README-tooling-locale.md`
avverte che quei file *«non sono eseguibili così come sono in un'altra
macchina»* — l'awareness c'è, la bonifica no. Il playbook, invece, insegna a un
**DM terzo** un comando che contiene la home del DM originale.

**Perché è un finding editoriale e non solo tecnico:** questi file sono
*deliverable*. Il booklet del Palio è materiale destinato al tavolo o alla
condivisione; un PDF con 13 immagini mancanti e un playbook con la home di
qualcun altro sono difetti di **pubblicazione**, non di codice.

**Azione (G3):** `scripts/validate_links.py` (link relativi + path assoluti +
allowlist per gli host-relative Homebrewery), riparazione dei 17 rotti reali,
sostituzione dei path locali con path relativi al repo.

---

### 🟢 E4 — Il glossario bloccato è un contratto senza applicazione

`campaign/GLOSSARIO-E-LOCALIZZAZIONE.md` è il *loc kit* previsto da ADR-0016 e
dichiara la propria regola d'uso: *«se un nome è in questa tabella, si scrive
così in ogni file nuovo. Se non c'è, aggiungilo tu la prima volta che lo
inventi.»* Nessun controllo verifica né la prima né la seconda metà della regola.

Il file è anche esplicito su ciò che **non** va fatto — *«non uniformare i nomi
esistenti: sono già in centinaia di file, nelle mappe, nelle immagini e nelle
schede dei giocatori»* — e questo audit lo rispetta: il gate proposto guarda
solo i **file nuovi** e i **nomi nuovi**.

**Azione (G7, appendice):** controllo che i nomi propri introdotti da un file
nuovo compaiano in glossario (warning, non bloccante — inventare un nome è
legittimo, dimenticarsi di registrarlo no).

---

## Asse C — Coerenza, flusso, storia

### 🔴 C1 — `state.md` mescola due tempi, e §1 contraddice §0

**È il finding più importante dell'audit**, perché è l'unico che produce errori
*durante* la sessione.

Il file dichiara la propria autorità in testa (righe 3-9): *«single source of
truth per ciò che è attualmente vero… se questo file è in disaccordo con
`campaign-history.md`, questo file vince»*. Poi, al suo interno, dice due cose
diverse.

**Cosa dice l'intestazione + §0** (righe 15-31, 44-46):

> ARC-07 **in corso** al tavolo. ✅ Piano della Terra (P4) completato 2026-07-31.
> **Prossimo: resurrezione di Hella (P3B).** Restano da giocare: resurrezione
> fisica di Hella (P3B), viaggio ai 1.000 anni fa (P5), raccordo al 1372 (D16)
> — **poi** l'Arco 08. **Tutto ciò che questo file dice dell'Arco 08 e
> dell'Arco 09 è canone preparato (design), non ancora giocato al tavolo.**

E la riga di cruscotto: `| 08 Battaglia di Hammerfist | ⬜ | pianificato — canone preparato, NON giocato |`.

**Cosa dice §1 — Party** (righe 74-79), presentata senza alcuna qualificazione
temporale, sotto il titolo *«Current Position & Condition»*:

| PC | Location dichiarata | Stato dichiarato |
|---|---|---|
| Thorik | **Hammerfist Holds, war council chamber** | «−2 perm CON **sacrificed for Hella's resurrection** (NEVER restored)» |
| Tordek | **Hammerfist → traveling to Dauth Tournament** | Bracieri Earth phase complete |
| Hella | **Hammerfist → traveling to Sacred Forest** | «**Treant Hybrid template active post-resurrection**» |
| Artemis | **Hammerfist → traveling to Invisible Tower** | Ring attivo |

Cioè: §0 dice che la resurrezione di Hella è **la prossima cosa da giocare**, e
§1 dice che Hella **è già risorta**, che Thorik **ha già pagato** il prezzo, e
che i quattro sono **già oltre** la Battaglia di Hammerfist — un arco che §0
marca `⬜ NON giocato`.

**La causa è ricostruibile e non è negligenza.** La prima riga del changelog §8
la spiega:

> `2026-05-01  Initial state.md created … Baseline = end of Hammerfist battle,`
> `            party at Hammerfist Holds, Custodi Eterni granted.`

`state.md` **nacque** dal materiale post-Hammerfist, quando si pensava di essere
più avanti. Il 2026-07-02 (piano ARC-08, task A0, «REGOLA ZERO applicata:
state.md al giocato reale») l'intestazione e §0 furono riportate al giocato
reale — **ma §1 non fu riportata indietro con loro**. È una bonifica parziale,
non un errore di concezione.

**Il rimedio esiste già nello stesso file.** §6 (Artifact State) risolve
*esattamente* questo problema, e lo risolve bene:

> **Two-times table (T6c, DM-confirmed 2026-07-04)**: le due colonne di stato
> sono etichettate. **«Today at the table»** = la posizione reale del tavolo per
> §0. **«Prepared (ARC-09 entry)»** = lo stato scritto in avanti, che diventa
> vero solo dopo P4 → P3B → P5. Per la sessione di stasera usare SEMPRE la
> colonna "Today".

E §6 è **coerente**: la riga Collana dice «Hella (dead — resurrection pending)»,
la riga Cuore di Moradin dice «Intact — will be expended… in the P3B ritual».
§6 sa che Hella è morta. §1, tre pagine sopra, dice che è viva.

**Sezioni da verificare e portare al pattern a due tempi:**

| Sezione | Stato | Nota |
|---|---|---|
| §0 cruscotto | ✅ corretta | è il riferimento |
| §1 Party | 🔴 **scritta in avanti senza etichetta** | il caso peggiore: è la prima tabella che un DM legge a inizio sessione |
| §2 Active Forces | 🟡 da verificare | ha già una separazione «Dual Clock» propria — verificare che i due orologi non siano confusi con i due *tempi* |
| §4 NPC Knowledge | 🟡 da verificare | «cosa sa un PNG» dipende da cosa è successo: rischio alto |
| §5 Promesse/debiti | 🟡 da verificare | idem |
| §6 Artefatti | ✅ corretta | **modello da replicare** |
| §7 Thread aperti | 🟡 misto | contiene sia domande su ARC-09 preparato sia esiti giocati marcati `[ESITO GIOCATO 2026-07-31]` — la marcatura c'è ma non è sistematica |

**Azione (G1):** estendere le due colonne etichettate di §6 a §1, e verificare
§2/§4/§5/§7. Nessun contenuto va cancellato: il materiale «preparato» è lavoro
buono e va conservato — va solo **etichettato come futuro**.

---

### 🔴 C2 — Due file si dichiarano entrambi «single source of truth»

| File | Riga | Autoproclamazione |
|---|---|---|
| `campaign/state.md` | 3-9 | *«single source of truth for what is currently true… if this file disagrees with `campaign-history.md`… this file wins»* |
| `campaign/lore/campaign-history.md` | 5 | *«This file is the **single source of truth** for the RumblingStone campaign narrative.»* |

La gerarchia **è** dichiarata (state.md vince), quindi non è un conflitto
irrisolvibile — ma `campaign-history.md` non lo sa e non lo dice, e afferma come
**passato** ciò che non è stato giocato:

- riga 26: `| Hella Oakenshield | … | 13 (post-resurrection) | … | ✅ Alive (died in arc 06, resurrected as Treant Hybrid) |`
- riga 153: `Hella returns as Treant Hybrid (-1 level → restored by story XP)`
- riga 176: «After Hella's resurrection, she goes deeper underground…» — detto
  di un PNG, al passato/futuro-certo

Chi apre `campaign-history.md` per primo — ed è il file il cui titolo promette
*«Complete History & Narrative Reference»* — esce con lo stato di campagna
sbagliato. La stessa asimmetria di C1, fra file invece che dentro un file.

**Azione (G1):** intestazione esplicita su `campaign-history.md` («storia
**giocata** fino a *X*; tutto ciò che segue è design preparato»), rinuncia
all'autoproclamazione di sorgente unica, puntatore a `state.md`, e marcatura dei
blocchi scritti in avanti.

---

### 🔴 C3 — La storia giocata non esiste come documento

```
campaign/sessions/  →  2026-05-03_session-3.md          (1 log reale)
                       RETROATTIVI-ARC07-INFERRED.md     (ricostruzione, 13 [INFERRED])
```

Contro un cruscotto §0 che dichiara **sette archi completati** (00→06) e il
settimo in corso. E il materiale grezzo di quegli archi non è in forma
editoriale:

| Arco | `.md` | Cosa c'è davvero |
|---|---|---|
| 00 Red Hand of Doom | 4 | fogli armate `.ods`, `campagna_flusso.txt`, calcoli XP |
| 01 La Miniera | **0** | `Miniera-ita.txt`, `Miniera.txt`, `grell necromante.txt` |
| 02 Scaladossa/funghi | **0** | 4 `.txt` + 4 `.webp` |
| 03 La Cittadella | **0** | `.txt`, `.pdf`, `.webp`, sottocartelle |
| 04 Tomba di Belkram | 2 | `.txt`, `.html`, `.webp` |
| 05 Stanza Runica | **0** | 2 `.pdf`, 2 `.webp` |
| 06 Corona di Adamantio | 25 | primo arco in forma editoriale |

Il file `RETROATTIVI-ARC07-INFERRED.md` è la prova che il problema è **già noto
e già affrontato correttamente**: è una ricostruzione dichiarata tale, con
disclaimer in testa, che dice esplicitamente *«L'intervista al DM (task B1) non è
ancora avvenuta: date, giocatori presenti e dettagli di tavolo sono da
confermare»*. Il metodo è giusto. È fermo da luglio perché **manca l'input
umano**, non perché manchi lo strumento.

Questo è il vero motore dei `[INFERRED]`: **quando la memoria del tavolo non è
scritta, ogni documento che vi si appoggia deve dedurre.**

**Azione (G11, gated):** ricostruzione arco per arco a partire dal grezzo, in
batch di domande al DM (una tornata per arco: date, presenti, XP, bottino, tre
decisioni chiave), output nel formato log di AGENTS.md, ogni buco non colmato
resta `[INFERRED]`. **Nessuna invenzione**: è la regola 5 di AGENTS.md e questo
lotto è precisamente il posto dove sarebbe più tentante violarla.

---

### 🟠 C4 — 379 `[INFERRED]` senza inventario né freno

```
occorrenze totali: 379      file coinvolti: 151
```

Top file:

| File | Occorrenze | Perché conta |
|---|---|---|
| `campaign/state.md` | **27** | è la sorgente di verità: 27 punti di verità dichiarata incerta |
| `plans/PIANO-REVISIONE-ARC07-…` | 23 | debito noto e tracciato ✅ |
| `plans/CHANGELOG.md` | 17 | in gran parte *scioglimenti* registrati ✅ |
| `campaign/sessions/RETROATTIVI-ARC07-INFERRED.md` | 13 | ricostruzione dichiarata ✅ |
| `Bestiario/png/Witchwood_Tiri_Kitor/…` | 12 | contenuto preparato |
| `PG/Artefatti/…/Hella/01_Collana_dei_Semi_Eterni.md` | 9 | **artefatto di un PG**: incertezza su poteri in mano al giocatore |

La convenzione è **giusta** ed è la cosa migliore che il repo fa sul canone:
AGENTS.md regola 5 impone di marcare invece di inventare, e il repo la rispetta.
Mancano le due metà successive del ciclo:

1. **Nessun inventario**: non esiste un elenco dei 379, raggruppato per
   destinatario della domanda, che il DM possa smaltire a lotti. Oggi
   scioglierne uno richiede di trovarlo.
2. **Nessun ratchet**: nulla impedisce che una PR ne aggiunga 20 senza che se ne
   accorga nessuno. Il numero può solo salire per inerzia.

**Azione (G4):** `scripts/inventory_inferred.py --check` — genera
`docs/audit/INFERRED-INVENTARIO.md` (raggruppato per file/tema/domanda) e in CI
verifica che il conteggio **non salga** rispetto alla baseline registrata. Un
ratchet, non un divieto: aggiungere un `[INFERRED]` resta legittimo, ma diventa
una scelta esplicita che aggiorna la baseline.

---

### 🟠 C5 — La pipeline che avrebbe prevenuto C1 e C3 è costruita, testata, e mai attivata

`python3 scripts/dm.py doctor --ci`, eseguito su questo commit:

```
✓ python 3.11.15          ✓ campaign/state.md       ✓ campaign/sessions
✓ campaign/templates      ✓ plans/INDEX.md          ✓ monster_catalog.yaml fresco
○ campaign/group.yaml assente — `dm.py session branch --group <nome>` per attivare il flusso ADR-0007
○ marker auto: assenti in state.md — `state_apply.py --migrate` sul branch gruppo
```

I due `○` sono la diagnosi di C1 e C3 in due righe. La pipeline ADR-0007 —
wizard di fine sessione, apply engine sulle regioni marcate, recap per-PG,
brief della prossima sessione, branch per gruppo — **esiste**, ha **31 dei 70
test** del repo, è documentata in una skill dedicata, ed è al ~98% secondo
`plans/INDEX.md`. Non è mai stata accesa: manca il collaudo al tavolo, tracciato
come tale nell'INDEX dal 2026-07.

Conseguenza diretta: `state.md` si aggiorna a mano (→ la bonifica parziale di
C1), i log di sessione si scrivono a mano o non si scrivono (→ C3).

**Azione (G10):** attivazione — `dm.py session branch --group …`,
`state_apply.py --migrate` per creare le regioni `auto:`, e il primo
`dm.py session end` reale. È un lotto **piccolo** con un effetto sproporzionato:
è l'unico che rende *automatica* la prevenzione di C1 e C3 per il futuro.

---

## Asse M — Focus adulti e contratto di tavolo

Il mandato chiede il focus «adult role player» su tutti e tre i significati che
il DM ha confermato: **rigore di design per adulti**, **temi maturi**, e un
**contratto di sicurezza** che li tenga insieme.

### 🟠 M1 — Il focus adulti è dichiarato in una riga e non è verificabile per beat

La definizione esiste, è buona, e sta in un posto solo —
`skills/rumblingstone-campaign/references/campaign-dm-strategy.md`, riga 3:

> *«Questa analisi è strutturata su misura per un gruppo di giocatori adulti,
> professionisti affermati, che investono ore di viaggio per giocare. Per un
> gruppo simile l'esperienza deve essere **Premium**: meno railroading, meno
> combattimenti "vuoti", maggiore "agency" e trame che stimolino l'intelletto,
> la morale e il problem-solving.»*

Quella riga è un **requisito di prodotto** travestito da nota di strategia: dice
cosa il materiale deve garantire. Nessuno verifica che lo garantisca.

Il repo ha già l'infrastruttura per farlo, in due pezzi:

- `validate_modules.py` impone 16 sezioni, e **quattro di queste sono proxy del
  requisito adulti**: `Contingenze «Se i PG fanno X»`, `ramo sconfitta/fallimento
  (mai punizione gratuita)`, `Sviluppi`, `ECHI / Echo Ledger`. Sono presenza di
  sezione, non qualità di scelta.
- La skill `rumblingstone-narrative-style` ha già un test di questa famiglia — il
  **PC Protagonism Test** — con `pc-protagonism.md` come riferimento. Esiste il
  precedente di «un test narrativo scritto come test».

Manca il pezzo centrale: un **Adult Design Test** che chieda, per beat, le tre
cose che la riga 3 promette — *c'è una scelta reale? ha un costo che il
giocatore può vedere prima di scegliere? il fallimento produce una storia invece
di una punizione?* — e una riga nel validatore che verifichi che il beat
**dichiari** la risposta.

**Azione (G6):** Adult Design Test in `rumblingstone-module-standard`, sul
modello del PC Protagonism Test; sezione dichiarativa obbligatoria nei master
DEF; riga corrispondente in `validate_modules.py`.

---

### 🔴 M2 — Non esiste un contratto di contenuto e sicurezza

Il materiale della campagna, letto dai file di canone, contiene:

| Tema | Dove (esempio dal canone) |
|---|---|
| Morte di un PG con costo permanente su un altro PG | Hella morta in ARC-06; Thorik −2 COS permanenti «NEVER restored»; Tordek −2 DES/+2 COS permanenti per il Peso del Mondo |
| Corruzione dell'anima a prezzo esplicito | Sigillo di Ossidiana: *«ogni uso divora un'anima (1 livello negativo a una creatura toccata); se non disponibile, consuma il portatore»* (`state.md` §7) |
| Guerra con caduti nominati uno per uno | Cerimonia delle 100 Asce: 210 morti, *«pronuncia tutti i 210 nomi»* |
| Tortura/esperimento su esseri senzienti | Zalkatar, ex chierico divenuto Mind Flayer **per scelta**, movente «lettura sperimentale»; 75 esperimenti fungini nei campi drow |
| Sfruttamento di minori | Lirien, «mulino dei bambini» del quartiere basso di Rethmar (`state.md` §1) |
| Manipolazione affettiva e lutto | Mira Serani si muove fra i profughi **con la faccia della figlia morta di Lorana** |

Questo è materiale da tavolo adulto ed è **scritto bene**: nessuno di questi
elementi è gratuito, ognuno paga in trama. Il finding non riguarda il contenuto.

Riguarda il fatto che **non esiste un documento che dichiari il confine**.
Cercando in `campaign/`, `skills/`, `docs/`, `plans/adr/` non compare nulla su:

- cosa la campagna **rappresenta e cosa lascia fuori campo** (rating dichiarato);
- **note di contenuto per arco**, per sapere cosa arriva prima che arrivi;
- uno **strumento di stop condiviso** (session zero, lines & veils, X-card o
  equivalente) — cioè: cosa fa un giocatore, in quel momento, se una scena tocca
  qualcosa che non aveva previsto di incontrare;
- chi decide, e come si rinegozia fra una sessione e l'altra.

`read-aloud-adulti.md` regola il **registro** del testo letto ad alta voce, che
è cosa diversa: è come si dice, non cosa si sceglie di dire.

**Per un tavolo di quattro adulti che si conoscono, questo non è un adempimento
formale — è utilità pratica per il DM.** Il confine deciso prima è quello che
permette di spingere *più forte*, non meno: sapere dove il tavolo sta comodo è
la condizione per portarlo, consapevolmente, appena oltre. È lo stesso principio
per cui il repo scrive un ADR invece di ricordarsi una decisione.

E c'è una ragione strutturale in più: il repo è scritto per essere **ereditato**
da un DM terzo (`DM-QUICKSTART-NUOVI-DM.md`, `new-campaign-group.sh`,
`state-blank.md`). Un DM terzo riceve il Sigillo di Ossidiana e il mulino dei
bambini **senza il contesto del tavolo che li ha accettati**.

**Azione (G6):**
1. `campaign/CONTRATTO-DI-TAVOLO.md` — session zero, confini dichiarati, strumento
   di stop, procedura di rinegoziazione. Compilato **dal DM**, non da un agente:
   è l'unico documento del repo il cui contenuto non può essere dedotto dai file.
2. ADR «contenuto maturo e sicurezza al tavolo» — il *perché* della scelta, con la
   sua conseguenza per le edizioni derivate (un'edizione condivisa eredita il
   contratto).
3. Campo `content-notes:` per arco nei master DEF, verificato da `validate_modules.py`.

---

## Appendice — comandi delle misure

```bash
# misura 2 — corpus precedente allo standard editoriale
while IFS= read -r f; do d=$(git log -1 --format=%ad --date=short -- "$f"); \
  [ "$d" \< "2026-07-31" ] && echo "$f"; done \
  < <(find campaign PG Bestiario 0* -name '*.md') | wc -l

# misura 3 — marcatori [INFERRED]
grep -ro "INFERRED" --include=*.md . | wc -l
grep -rc "INFERRED" --include=*.md . | sort -t: -k2 -rn | head

# misura 6-7 — link rotti e path locali
grep -rn "file:///home\|/home/jfs" --include=*.md . <!-- validate-links: ignore -->

# misura 8 — calchi (proxy italiano-nativo §1)
grep -rEoi "\b(la|il|le|i) su[ao]i? (mano|mani|occhi|respiro|testa|spalle|voce|sguardo|volto)\b" \
  --include=*.md campaign PG Bestiario 0* | wc -l

# C5 — stato della pipeline ADR-0007
python3 scripts/dm.py doctor --ci
```
