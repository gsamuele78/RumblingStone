# PIANO — Proposta commerciale e sfide: cosa si vende, quanto vale, cosa lo blocca

> **Stato**: 🔵 **proposta, non autorizzata** · **Aperto**: 2026-09-04
> **Richiesta-fonte (DM, 2026-09-04)**: *«crea un piano dettagliato di proposta
> commerciale e sfide che elenca questa discussione e i punti sollevati, o
> comunque dia chiaramente il problema e la direzione da prendere. Per gli
> strumenti, quanti di questi sono vincolati alla campagna o possono essere
> venduti separatamente, e che valore onesto potrebbero avere così o con una
> interfaccia UI più usabile mantenendo il core? Ma gli strumenti si può usare
> l'applicazione come base per fini commerciali futuri, o siamo bloccati col MIT?»*
> **Precede**: [PIANO-AUDIT-PROVENIENZA-E-VENDIBILITA](PIANO-AUDIT-PROVENIENZA-E-VENDIBILITA.md),
> che stabilisce **cosa è vendibile** sul piano dei diritti. Questo piano parte da
> lì e chiede **quanto vale e cosa serve per venderlo**.
> **Fonti in repo**: `scripts/tools.manifest.json` (54 voci) · `LICENSES.md` ·
> `scripts/LICENSE` (MIT) · ADR-0029 · ADR-0012 (manifest) · ADR-0030 (MCP)

> ⚠️ Valutazione di ingegneria e di prodotto, **non un parere legale né una
> perizia di valutazione**. Le cifre di §3 sono ordini di grandezza con le
> ipotesi dichiarate, non una stima peritale.

---

## §0 · «Siamo bloccati col MIT?» — No, e la risposta va data per prima

**Non sei bloccato.** La confusione è comune e vale la pena scioglierla per bene,
perché condiziona ogni decisione a valle.

Una licenza è una **concessione che fai agli altri**. Non vincola te. Tu detieni
il copyright del codice in `scripts/`: il MIT è ciò che hai dato al pubblico, non
ciò che ti sei tolto.

Cosa puoi fare, oggi, senza chiedere niente a nessuno:

| Puoi | Nota |
|---|---|
| **Vendere il software così com'è** | il MIT non lo vieta. Nessuna licenza open source vieta di vendere |
| **Fare doppia licenza** | lo stesso codice sotto MIT *e* sotto una licenza commerciale, a scelta del cliente |
| **Cambiare licenza per le versioni future** | da domani `scripts/` può uscire sotto qualunque altra licenza tu voglia |
| **Costruirci sopra un prodotto proprietario** | UI, servizio ospitato, pacchetti di contenuto: niente di tutto ciò deve essere MIT |

L'unica cosa che **non** puoi fare è **ritirare il MIT da quello che è già
uscito**. Chi ha ricevuto una copia sotto MIT conserva per sempre, *su quel
codice*, il diritto di usarlo, modificarlo, ridistribuirlo e venderlo. Un
concorrente potrebbe partire dall'ultima versione MIT e farsi la sua.

Quindi la formulazione giusta non è «il MIT ci blocca», è: **il MIT non blocca e
non protegge**. E la seconda metà conta più della prima, perché porta alla
domanda vera.

### La domanda vera: cosa protegge davvero un prodotto software qui

Non la licenza. In questo mercato il codice non è il fossato. Lo sono:

- **il contenuto** — i moduli, le tabelle, il canone: è quello che il cliente
  compra e che non può forkare da GitHub;
- **il servizio** — se gira ospitato, il valore è l'esecuzione, non i sorgenti;
- **l'aggiornamento continuo** — chi forka prende una fotografia, non il flusso;
- **il nome** — un marchio si difende dove una licenza permissiva non arriva.

### La forma consigliata: **open core**

È esattamente ciò che il DM ha intuito con *«mantenendo il core»*, e ha un nome
in letteratura. Il core resta MIT — è già pubblico, e l'apertura aiuta
l'adozione — mentre UI, servizio e contenuti stanno sopra, proprietari.

⚠️ E qui c'è una cosa che va detta in positivo, perché è un vantaggio reale e
raro: **questo core è già fatto come si deve per reggerci sopra un prodotto**.
Non è un complimento di cortesia, sono proprietà misurabili:

- **54 strumenti con un manifest machine-readable** (`tools.manifest.json`,
  ADR-0012): argomenti, input, output, codici d'uscita, determinismo, effetti
  collaterali. Una UI si genera in gran parte da lì;
- **un server MCP che espone il catalogo dallo stesso manifest** (ADR-0030), con
  allowlist: la superficie d'integrazione esiste già;
- **i codici d'uscita sono il contratto**, e ci sono test che li chiamano per
  processo;
- **21.000 righe di Python, 563 test, 2.070 sotto-test**, CI verde;
- **output deterministici con `--seed`** dove la casualità c'entra.

La maggior parte dei progetti che vogliono diventare prodotto deve *prima*
costruire questo. Qui c'è.

---

## §1 · Quanto degli strumenti è legato alla campagna — misurato, non stimato

Metodo: per ognuna delle 54 voci del manifest, conteggio dei riferimenti testuali
al canone (`campaign/`, `Bestiario`, `state.md`, nomi propri della campagna) più
il campo `writes_canon` del manifest.

⚠️ **La misura è un limite superiore, non la verità.** Conta le occorrenze
*testuali*: un percorso di default, un esempio nella docstring e un vincolo vero
pesano uguale. Diversi strumenti in fondo alla tabella sono **motori generici
puntati sui dati della campagna**, non motori che la contengono.

| Fascia | Quanti | Che cosa sono |
|---|---:|---|
| **Generici** — zero legami | **12** | funzionano su qualunque dato, oggi, senza toccarli |
| **Quasi generici** — 1-6 legami | **20** | il legame è un default o una citazione, non una dipendenza |
| **Legati alla campagna** — >6 o scrivono canone | **22** | qui sta la vera specificità |

### I dodici già generici

`render_map_svg` · `export_uvtt` · `import_ultraclear` · `validate_maps` ·
`suggest_map` · `export_booklet_pdf` · `validate_booklets` ·
`build_image_derivatives` · `extract_scene_prompts` · `html-to-markdown` ·
`image-to-webp` · `install-git-hooks`

Sette dei dodici sono **la pipeline delle mappe e dei materiali**. Torna in §3, e
non per caso.

### I «legati» che in realtà non lo sono

Due esempi controllati a mano, perché la misura da sola ingannerebbe:

- **`genera_creatura`** (12 legami) è un generatore SRD 3.5/PF1e puro. I legami
  sono il *rifiuto* di scrivere dentro `Bestiario/` e le citazioni nelle
  docstring. Scorporarlo è una questione di configurazione, non di riscrittura;
- **`suggest_encounter`** (23 legami) legge il catalogo mostri costruito da
  `Bestiario/`. È accoppiamento **ai dati**, non al codice: puntato su un'altra
  cartella funziona.

### Dove sta la specificità vera

Nel **pipeline dello stato di sessione**: `state_apply`, `state_sync`,
`session_wizard`, `campaign_branch`, `update_xp`, `next_session`,
`new-campaign-group`. Quelli codificano *questo* modo di condurre una campagna
(ADR-0007: branch per gruppo, regioni marcate, visibilità per-PG).

⚠️ E anche quelli non sono «legati a RumblingStone»: sono legati a **un metodo**.
Un altro DM con un altro mondo li userebbe uguali. È il pezzo più originale del
lotto, non il più prigioniero.

---

## §2 · Le tre linee di prodotto software, e cosa costa ciascuna

| # | Prodotto | Da cosa nasce | Lavoro residuo |
|---|---|---|---|
| **S1** | **Pipeline mappe** — griglia → SVG stampa + export UVTT con muri, porte, luci | i 7 strumenti mappe, già generici | scorporo + UI: **il più corto** |
| **S2** | **Toolkit del DM** — prep incontro, generatore creature, bestiario, materiali | ~20 strumenti, cucitura di configurazione | scorporo + UI + documentazione: medio |
| **S3** | **Gestore di campagna** — stato, sessioni, recap, visibilità per-PG | il pipeline ADR-0007 | è il più originale e il più lungo: serve un modello dati che oggi è «il repo git» |

---

## §3 · Il valore onesto, con le ipotesi in chiaro

Qui servono due verità scomode prima dei numeri.

### Verità 1 — In questo mercato il vincolo è la distribuzione, non il codice

Un tool per DM non fallisce perché è scritto male: fallisce perché non lo trova
nessuno. 21.000 righe con 563 test sono ingegneria seria, e l'ingegneria **non è
il fossato**. Chi vende in questo settore vende perché ha un pubblico, non perché
ha una codebase.

### Verità 2 — 3.5 e PF1e sono sistemi legacy, e questo è un tetto

D&D 3.5 è del 2003, Pathfinder 1e del 2009. Il pubblico esiste, è appassionato, e
**è piccolo e poco propenso a comprare strumenti** — chi resta su un sistema di
vent'anni fa lo fa spesso proprio per non dipendere da un ecosistema commerciale.
Il mercato che paga è su 5e e PF2e.

⚠️ Questo è in **tensione diretta** con la decisione «restiamo su 3.5 e PF1e»
presa in `PIANO-AUDIT-PROVENIENZA-E-VENDIBILITA` §6. Quella decisione è giusta
*per la qualità* e costosa *per il mercato*, e le due cose vanno tenute separate
invece di far finta che coincidano.

⚠️ **L'eccezione, ed è quella che conta**: la pipeline mappe (S1) è
**indipendente dal sistema**. Un export UVTT con muri, porte e luci serve a chi
gioca 5e, PF2e, Shadowdark o Traveller. È l'unico asset tecnico del repo che non
paga il pedaggio del sistema legacy.

### Gli ordini di grandezza

Ipotesi: singolo autore, vendita diretta (itch.io, Ko-fi, DriveThruRPG) senza
budget di marketing, nessun pubblico preesistente.

| Prodotto | Come sta oggi | Con una UI usabile | Nota onesta |
|---|---|---|---|
| **S1 pipeline mappe** | ~0 come prodotto | **la scommessa migliore** | è l'unico system-agnostic, e risolve un dolore vero (muri/luci in Foundry). Ma compete con prodotti rifiniti e già noti |
| **S2 toolkit DM** | ~0 | modesto | il tetto è il pubblico 3.5/PF1e. Una UI moltiplica l'usabilità, non il mercato |
| **S3 gestore campagna** | ~0 | il più difensibile | metodo originale, nessun concorrente diretto. Ma è anche il più lungo, e serve un modello dati che non sia «un repo git» |
| **Server MCP** | ~0 come prodotto a sé | — | i server MCP oggi si regalano come leva d'adozione. Monetizzarlo direttamente è controcorrente; **come vetrina** invece funziona |

**Il verdetto sul software venduto così com'è: essenzialmente zero.** Nessuno
compra una CLI. Non è un giudizio sul valore del lavoro — è come funziona questo
mercato.

⚠️ **E qui il piano ribalta l'intuizione della richiesta.** «Una piccola revenue»
è un obiettivo raggiungibile, ma la strada più corta **non passa dagli
strumenti**: passa dal **contenuto**. Un modulo indipendente ben fatto e
playtestato si vende su DriveThruRPG a un pubblico che *già compra moduli*. Gli
strumenti, per arrivare allo stesso ricavo, chiedono una UI, una distribuzione e
un supporto che sono un lavoro molto più grande.

Il che riporta esattamente al cancello di qualità che il DM ha posto per primo, e
al Drappo come primo candidato.

### Quanto vale la UI, in concreto

Il salto da CLI a prodotto è reale e il core è pronto per riceverlo (§0). Ma va
detto quanto costa: **la UI è tipicamente più lavoro di tutto il core esistente**,
perché sposta il problema da «il comando funziona» a «una persona che non ha
letto niente ci arriva da sola». E in quello spazio ci sono già prodotti rifiniti.

Il moltiplicatore vero non è la UI da sola: è **UI + un pubblico**. Senza il
secondo, la prima è codice che nessuno apre.

---

## §4 · Le sfide, elencate

| # | Sfida | Perché è dura | Dove se ne parla |
|---|---|---|---|
| **C1** | **L'AP non è vendibile** | RHoD non è OGC; l'adattamento è derivato. Il pezzo più grosso del repo è fuori dal commercio | AUDIT §0 |
| **C2** | **Niente è stato giocato al metro del repo** | `collaudato` richiede due gruppi diversi; il Drappo è ad alfa, gli archi non hanno marcatore | AUDIT §7 |
| **C3** | **D1: le immagini non entrano nel volume da stampa** | un PDF in vendita che stampa `!Stemma Oca` al posto dell'illustrazione. Da solo blocca ogni consegna | RICERCA-AUDIT-2026-08 |
| **C4** | **D4: nessun gate CI sulla stampa** | l'unico pezzo del repo dove una regressione arriva al DM invece che alla CI è proprio quello che diventerebbe il prodotto | idem |
| **C5** | **Le tavole sono di terzi** | illustrazioni RHoD e mappe creditate a Mike Schley: non si vendono, e vanno rifatte | AUDIT §3 |
| **C6** | **Il sistema è legacy** | 3.5 e PF1e limitano il mercato di tutto tranne le mappe | §3 qui |
| **C7** | **Nessun pubblico** | il vincolo binding di tutto il piano, e l'unico che non si risolve scrivendo codice | §3 qui |
| **C8** | **La provenienza delle tavole raster è ignota** | blocca il lotto A dell'audit | ADR-0005 |
| **C9** | **Il MIT non protegge** | non blocca, ma non impedisce a nessuno di forkare l'ultima versione | §0 qui |

⚠️ **C7 è la sfida principale**, e nessuna delle altre otto la tocca. È l'unica
che non si chiude con un commit.

---

## §5 · La direzione

Detta in una riga: **il primo prodotto è contenuto, non software; il software
diventa prodotto dopo, e comincia dalle mappe.**

**Fase 1 — Rendere consegnabile una cosa sola.** Chiudere D1 e D4 (sono bug già
specificati), portare il Drappo a **beta** con un gruppo vero, e farlo uscire.
Serve a due cose insieme: è il primo prodotto candidato, ed è l'unico modo di
scoprire se il metro di qualità del repo coincide con quello di chi paga.

**Fase 2 — Scorporare la pipeline mappe.** È l'unico asset system-agnostic e i
sette strumenti sono già generici. Come progetto separato, MIT, con la sua
documentazione: serve da **vetrina** e costruisce il pubblico che manca (C7),
prima ancora di essere un prodotto.

**Fase 3 — Decidere se la UI si fa.** Solo con i numeri delle prime due fasi
sotto gli occhi: se la Fase 1 non vende e la Fase 2 non porta utenti, una UI non
cambia il risultato — lo rende solo più caro.

**In parallelo, e indipendente**: l'audit di provenienza (lotti A–C dell'altro
piano). Serve prima di **vendere**, non prima di **migliorare**.

---

## §6 · Le decisioni che restano al DM

1. **La licenza del core.** La raccomandazione è: **lasciarlo MIT** e mettere
   sopra ciò che si vende. Cambiarla ora protegge poco (il passato resta MIT) e
   costa l'adozione, che è la cosa che manca davvero.
2. **Il marchio.** «RumblingStone» oggi non è registrato e in un'ipotesi
   commerciale è ciò che difende dove il MIT non arriva. Va deciso presto perché
   ha tempi lunghi.
3. **Se accettare il tetto del sistema legacy** o rimettere in discussione la
   scelta 3.5/PF1e **per i soli prodotti**, tenendo la campagna com'è.
4. **Chi fa il playtest beta del Drappo**, che è l'unica voce di tutto questo
   piano che non si può eseguire al computer.

---

## §7 · La divergenza da RHoD, raccontata dal DM — e la dipendenza che nessuno contava

> **Racconto del DM, 2026-09-04.** L'idea iniziale era far vivere ai giocatori
> qualcosa di simile al *Signore degli Anelli*; RHoD era l'AP che ci si
> avvicinava di più, ma condotto al tavolo è risultato *«banale, lineare»*, e la
> modifica è cominciata subito.

Questo cambia la prognosi di §0 e va scritto, perché §0 era stato costruito sulla
**auto-descrizione del repo** (*«heavily based on Red Hand of Doom»*), non sul
contenuto reale.

### Quanto è già divergente, per come il DM lo racconta

| Pezzo | Origine dichiarata | Che cosa ne resta di RHoD |
|---|---|---|
| Battaglia di Hammerfist | il Fosso di Helm (Tolkien) | l'idea dell'assedio, non l'assedio di RHoD |
| Assalto a Rethmar | la battaglia di Gondor (Tolkien), più Harry Potter e il video d'apertura di ToEE | idem |
| Quest della Corona e gli altri artefatti | **inventata di sana pianta** | niente |
| L'arco nell'Underdark, il labirinto del minotauro, il giardino dei funghi, i poteri miceliali di Hella | **inventati** (spunto dal salto miceliale della *Discovery*) | niente |
| La Torre | concetto di follia e aberrazione da *Out of the Abyss*, livelli riscritti ed espansi, fazione drow e portali aggiunti | niente |
| La discesa nella miniera di Belkram | spunto d'ispirazione | la fazione dei nani di Abbattor, la cittadella deturpata, il beholder cieco, il rompicapo dei dipinti nanici e le stanze sotto il tempio sono **profondamente modificati** |

Un assedio notturno contro numeri schiaccianti, una città assediata che resiste,
una discesa nel sottosuolo: sono **scene di genere**, non espressione protetta, e
Tolkien viene prima di RHoD su tutte e tre. Se il racconto regge alla verifica
file per file, la parentela con RHoD è molto più sottile di quanto §0 assumesse.

⚠️ **Ma «per come il DM lo racconta» non è una verifica.** Nessuno può liberare
questo materiale da una descrizione a voce: serve il lotto A, e ora si sa cosa
deve cercare.

### La dipendenza vera, misurata: non è RHoD, è il bestiario

Contando i file che nominano **Product Identity D&D che NON sta nel SRD**:

| Entità | File | Nel SRD? |
|---|---:|---|
| **illithid** | **86** | ❌ |
| **githyanki** | **58** | ❌ |
| **Circolo degli Otto / Circle of Eight** | **31** | ❌ (Greyhawk) |
| **mind flayer** | 22 | ❌ |
| **beholder** | 10 | ❌ |
| maur · yuan-ti · githzerai · umber hulk | 13 | ❌ |

Per contrasto, questi sono **SRD e quindi liberi**: rakshasa (32 file), treant
(84), drow (176), retriever (6), basilisco (5), Moradin (169 — la lista di
divinità del SRD 3.5 lo contiene).

⚠️ **E qui c'è il rovescio che conta.** La concentrazione è nell'**arco 09** —
27 file con illithid, 33 con githyanki, 15 col Circolo degli Otto — cioè
**proprio l'arco inventato da zero**. Il contenuto più originale è quello che
porta più Product Identity altrui: l'invenzione è stata nella trama, il popolamento
è stato pescato dal bestiario chiuso.

*(Zuggtmoy non compare mai col suo nome: quella sostituzione è già fatta.)*

### Perché questa è una buona notizia

Un mostro si sostituisce; una trama si riscrive. Le **statistiche** di un
illithid sono meccanica derivabile dal SRD — è l'**identità** a essere protetta,
non i numeri. Un'aberrazione originale con lo stesso ruolo tattico costa una
scheda e un nome, non un arco.

Se la divergenza raccontata regge, il conto si ribalta rispetto a §0:

| | Prognosi di §0 | Dopo il racconto del DM |
|---|---|---|
| **Struttura RHoD** | il blocco principale | forse leggera, da verificare |
| **Bestiario non-SRD** | non contato | **~200 occorrenze**, ma economico da chiudere |

### La cosa più dannosa nel repo è un documento del DM

⚠️ Il README dichiara *«heavily based on Red Hand of Doom»*, e la stessa frase
ricorre in `campaign/lore/`, nelle skill e nei file d'arco. Se la verità è quella
raccontata qui — ispirazione iniziale, poi divergenza profonda — allora quella
riga è **inesatta**, ed è al tempo stesso **il documento peggiore del repo per
una causa commerciale**: un'ammissione di derivazione, scritta dall'autore, che
il lavoro forse non merita.

Non si tocca per convenienza: si corregge **se e solo se** il lotto A stabilisce
che è falsa. Riscriverla prima della verifica sarebbe la cosa peggiore di tutte.

### Cosa cambia nel lotto A

L'audit di provenienza cerca ora **due** cose invece di una:

1. **Struttura RHoD** — beat, sequenza, toponimi, PNG. Prognosi: più leggera del
   previsto, e il metodo è il test del lettore (§3 della risposta al DM: darlo a
   chi ha condotto RHoD e sentire se dice «stesso genere» o «coi nomi cambiati»);
2. **Product Identity non-SRD** — il bestiario, il Circolo degli Otto, i nomi
   propri di Forgotten Realms. Prognosi: più pesante del previsto, e si chiude
   con un lavoro di sostituzione che è **meccanico, elencabile e finito**.

E una regola per il lavoro nuovo, da subito: **quello che si popola d'ora in poi
si popola dal SRD.** Ogni illithid aggiunto oggi è un file in più da bonificare
domani.
