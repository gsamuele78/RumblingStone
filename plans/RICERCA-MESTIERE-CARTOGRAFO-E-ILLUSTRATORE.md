# 🎨 RICERCA — Il mestiere: cartografia e illustrazione a confronto con la pratica professionale

> **Stato**: 🔵 **aperta, da eseguire** · **Data**: 2026-09-04
> **Richiesta-fonte (DM)**: *«la generazione delle mappe usa tutte le best
> practice e le tecniche utilizzate dai cartografi, ed automatizzabili o
> generabili by AI tools? La stessa domanda è per le illustrazioni: utilizzano
> le best practice utilizzate dagli illustratori di AP ed automatizzabili o
> generabili by AI tools?»*

## §1 — Cosa NON rifà *(obbligatorio, ADR-0044)*

Prima di aprirla ho guardato i piani che ci sono. Quattro documenti toccano
l'argomento e **nessuno risponde a questa domanda**; questa ricerca dichiara i
confini contro tutti e quattro.

| Documento esistente | Cosa copre | Perché non basta |
|---|---|---|
| `RICERCA-GENERATORI-MAPPE-QUALITA-RHOD` (2026-07-12) | **censimento di strumenti** open source: Watabou, Azgaar, mipui, texture procedurali SVG | Risponde a *«che cosa possiamo usare»*, non a *«disegniamo bene»*. Tocca la tecnica di sfuggita (texture, bordi inchiostrati) e mai la **leggibilità al tavolo** |
| `PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI` | il renderer non deve **perdere** ciò che l'ASCII porta | Fedeltà ≠ qualità: una mappa può essere resa fedelmente e restare illeggibile |
| `PIANO-INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITA` | le tre modalità, il contratto JSON, l'export VTT | È la **catena**, non il disegno |
| `PIANO-EDITOR-VISUALE-MAPPE-TATTICHE` | un front-end di authoring | È lo **strumento di input** |
| skill `rumblingstone-art-direction` (ADR-0019) | il **mestiere applicato**: bibbia visiva, scheda-personaggio, lock di seed/luce/camera, gate di rifiuto | È la norma da seguire, **non la misura di quanto la si segua** — e non copre la cartografia |
| `PIANO-RIPRESA-PR-ABBANDONATE` **F3** (la #106) | la **catena raster riproducibile**: seed da SHA-256, `PROVENIENZA.txt`, ControlNet depth dalla geometria vera | È l'**automazione**. Questa ricerca non la ridisegna: ne è il committente, e le passa i criteri |

> **Un documento solo, non due.** Il DM ne aveva proposti due. Cartografia e
> illustrazione condividono la stessa domanda in tre parti — *qual è il
> mestiere · quanto lo seguiamo · quanto si automatizza* — e soprattutto lo
> stesso committente (la F3). Due documenti si sarebbero rimandati a vicenda.

**È una RICERCA, non un piano**: misura un divario e propone. I lotti li apre
dopo, citandosi.

---

## §2 — Le tre domande, per asse

Ogni asse si misura sulle stesse tre, in quest'ordine — e l'ordine conta,
perché la terza senza le prime due produce automazione di qualcosa di sbagliato.

1. **Qual è il mestiere?** Che cosa fa un cartografo (o un illustratore di AP)
   che noi non stiamo facendo — non «che strumento usa», ma **che decisione
   prende**.
2. **Quanto lo seguiamo?** Misurato sugli artefatti che il repo ha davvero, non
   in astratto.
3. **Quanto si automatizza, e quanto no?** Con la distinzione che il repo già
   applica altrove: la macchina conta, l'essere umano giudica.

---

## §3 — Asse A: cartografia

### A1 · Il mestiere, come lo si misura

Le nove cose che un cartografo di gioco decide, e su cui si può fare un audit
verificabile:

| # | Decisione | Come si misura sul nostro repo |
|---|---|---|
| A1.1 | **Gerarchia visiva**: cosa si vede per primo | il fuoco della scena si distingue dallo sfondo a 50 cm dal tavolo? |
| A1.2 | **Leggibilità della griglia**: si contano i quadretti senza sforzo | contrasto griglia/terreno, spessore, colore |
| A1.3 | **Orientamento**: nord, scala, coordinate | quante mappe hanno tutti e tre? Le direttive `@compass` esistono: **quante le usano** |
| A1.4 | **Confine leggibile**: dove finisce la mappa | il bordo dice «qui è finita» o «continua fuori»? |
| A1.5 | **Codice colore coerente fra mappe** | lo stesso terreno ha lo stesso colore in tutte? La legenda è unica ma le palette? |
| A1.6 | **Daltonismo**: distinguibile senza il colore | ADR-0032 misura la leggibilità tipografica — **non le mappe** |
| A1.7 | **Stampa in scala di grigi** | il tavolo stampa in bianco e nero più spesso di quanto si creda |
| A1.8 | **Densità informativa**: quanto entra prima che diventi illeggibile | le mappe grosse (1.800 celle) reggono? |
| A1.9 | **Il doppio uso**: mappa del DM e mappa dei giocatori | `tarsilia-la-ruota` ha le due versioni: è **una** su quante? |

### A2 · Quello che già sappiamo prima di cominciare

Non parte da zero. Tre cose sono **già misurate** e vanno messe nella tabella
finale invece di essere riscoperte:

- **La legenda funziona ed è unica** (`LEGENDA-FUNZIONALE-SPEC`), e dopo
  ADR-0042/0043 i simboli dicono una cosa sola ciascuno.
- 🐛 **Sei mappe hanno l'intestazione discorde dalla griglia** — misurato il
  2026-09-04, coda in §6.
- **La resa è a pergamena con texture procedurali**, quindi A1.5 (palette) è
  centralizzata per costruzione: è un punto di forza, non un rischio.

### A3 · Cosa si automatizza

| | Chi lo fa |
|---|---|
| A1.2 contrasto griglia, A1.6 daltonismo, A1.7 grigi | **macchina**: sono rapporti di contrasto, si calcolano. Estensione naturale di `validate_tipografia` |
| A1.3 nord/scala/coordinate, A1.9 doppia versione | **macchina**: è un conteggio di presenza, come il gate di ADR-0041 |
| A1.4 confine, A1.8 densità | **macchina con soglia**, e la soglia va tarata su mappe che il DM giudica buone |
| A1.1 gerarchia visiva, A1.5 coerenza percepita | **essere umano**. Nessun contrasto misura «si capisce dov'è il boss» |

⚠️ **Quello che gli AI tools NON danno**: un generatore produce una mappa
plausibile, non una mappa **che serve a quella scena**. Il vincolo del repo —
il markdown è il master, la mappa è compilata da un contratto — è più forte di
qualunque generatore, e va difeso: un tool che produce solo un'immagine
finita **non entra nella catena** (quarta soglia di `RICERCA-TOOL-ESTERNI` §6).

---

## §4 — Asse B: illustrazione

### B1 · Il mestiere di un illustratore di AP

| # | Decisione | Come si misura |
|---|---|---|
| B1.1 | **Che cosa illustrare**: il momento, non il luogo | quante nostre immagini mostrano un'**azione** invece di un ambiente vuoto? |
| B1.2 | **Riconoscibilità del personaggio** fra tavole diverse | `rumblingstone-art-direction` lo chiede: **quante schede-personaggio esistono davvero**? |
| B1.3 | **Coerenza di luce e ora del giorno** dentro un arco | verificabile a occhio su un set |
| B1.4 | **Composizione per l'impaginato**: dove cadrà il testo | le nostre immagini sono generate ignorando la gabbia? |
| B1.5 | **Palette d'arco**: ogni arco ha una dominante | esiste? È dichiarata da qualche parte? |
| B1.6 | **La copertina è un altro mestiere** dalla tavola interna | |
| B1.7 | **Ancora storica in pubblico dominio** invece di imitare uno stile vivente | ✅ **già deciso e applicato** (R2 di `RICERCA-TOOL-ESTERNI`, ancora fiamminga) |
| B1.8 | **Licenza dei pesi** | ✅ **già codice**, non avvertimento (F3: exit 1 su FLUX.1 [dev]) |
| B1.9 | **Il gate di rifiuto**: quando un'immagine si butta | ✅ nella skill · ⚠️ **non lascia traccia**: è il buco che F3 chiude con `SCARTI.txt` |

### B2 · Il divario che si vede già

Tre voci su nove sono **già a posto** (B1.7, B1.8, B1.9-in-norma) e sono quelle
che riguardano **licenza e disciplina**. Le sei che restano riguardano il
**disegno**, e nessuna è misurata. È lo stesso squilibrio dell'asse A: il repo è
forte dove la regola si scrive, debole dove serve un occhio.

### B3 · Cosa si automatizza

| | Chi lo fa |
|---|---|
| B1.2 riconoscibilità, B1.5 palette d'arco | **macchina, in parte**: un lock di seed e una palette dichiarata sono verificabili; la somiglianza di un volto no |
| B1.4 composizione per l'impaginato | **macchina**: la gabbia la conosce `rumblingstone-editoria`, quindi la richiesta d'aspetto si può derivare dal manifest invece di indovinarla |
| B1.1 che cosa illustrare, B1.3 luce, B1.6 copertina | **essere umano** |
| B1.9 il registro degli scarti | **macchina scrive, umano decide** → è `SCARTI.txt`, F3 |

---

## §5 — Piano di esecuzione in tre fasi *(quando il DM la autorizza)*

> **Taglio dei lotti** (ADR-0045). L'audit è **ricognizione**, i gate sono
> **costruzione**, le norme sono **giudizio**: tre classi diverse, ed è il motivo
> per cui la Fase 2 non può partire prima della 1.
>
> | Lotto | Classe | `[engine · effort · qualità]` |
> |---|---|---|
> | **F1a** misurare i 9 criteri di cartografia su 31 SVG / 17 master | **R** ricognizione | `[subagente `Explore`, `Sonnet 5` · basso-medio · **un numero per riga**, e il comando che lo riproduce]` |
> | **F1b** misurare i 9 criteri d'illustrazione sul set esistente | **R** ricognizione | `[subagente `Explore`, `Sonnet 5` · basso-medio · come sopra]` |
> | **F1c** le 6 mappe con l'intestazione discorde (§6) | **K** canone | `[**Opus 5, mai delegato** · xhigh · **una per una**: decidere se sbaglia l'intestazione o la griglia. Un `sed` le rovinerebbe tutte]` |
> | **F2** i gate sulle righe marcate «macchina» | **C** costruzione | `[Sonnet 5 · medio-alto · ogni gate con un test **che lo prova mordere**, e soglie tarate sui numeri della F1 — non a occhio]` |
> | **F3** le norme nelle skill esistenti | **G** giudizio | `[Opus 5, sessione principale · alto · il DM riconosce il proprio metro di qualità]` |

**Fase 1 — Audit misurato.** Applicare A1 e B1 agli artefatti che il repo ha:
**31 SVG / 17 master** per le mappe, e il set di immagini esistente. Uscita: una
tabella con un numero per riga, non un giudizio.

**Fase 2 — I gate che si possono scrivere.** Solo per le righe marcate
«macchina» in §3 e §4. Ogni gate nasce bloccante (regola già scritta) e ogni
gate porta un test **che lo prova mordere**.

**Fase 3 — Le norme per quelle che non si automatizzano.** Vanno nelle skill
che già esistono (`rumblingstone-mapmaking`, `rumblingstone-art-direction`), non
in un documento nuovo — altrimenti si ricade nel difetto che ADR-0044 chiude.

⚠️ **Fase 2 non parte prima della 1.** Un gate tarato su una soglia inventata
boccia il lavoro buono e passa quello cattivo, e si disattiva entro un mese.

---

## §6 — Il difetto già misurato, che questa ricerca eredita

Il 2026-09-04, ridisegnando la mappa 3 di `…P1C-Rituale` su richiesta del DM, è
emerso che **sei mappe dichiarano dimensioni diverse da quelle che hanno**:

| Master | mappa | dichiara | griglia vera |
|---|---|---|---|
| `Portale-Forgia-L1-REVISED-UltraClear` | 1 | 20×13 | **20×14** |
| `Portale-Forgia-L2-REVISED-UltraClear` | 1 | 53×10 | **21×53** |
| `Portale-Forgia-L2-REVISED-UltraClear` | 2 | 33×33 | **33×25** |
| `Hammerfist-L2-REVISED-Ultra-Clear` | 1 | 120×80 | **50×80** |
| `Hammerfist-Lotto-2-Assedio` *(deprecato)* | 1 | 120×80 | **34×80** |
| `Arco-Post-Hammerfist-P1C-Rituale` | 1 | 53×40 | **33×40** |

Il renderer **avvisa e disegna lo stesso**. Al tavolo significa che la scala
stampata non corrisponde alla griglia, quindi movimento e gittate si contano
sbagliati: è un difetto di **A1.3**, e questa ricerca lo eredita già misurato.

⚠️ **Non sono tutte lo stesso caso, e vanno lette una per una**: `120×80` sono
**metri**, non quadretti (80×53 a 1,5 m); `53×10` sembra un'intestazione con i
numeri invertiti; `20×13 → 20×14` è una riga di scarto. Un `sed` le rovinerebbe
tutte e sei.

**Proposta**: un lotto della Fase 1, con la stessa cura data alla mappa 3 —
leggere, decidere per ciascuna se è l'intestazione o la griglia a sbagliare, e
poi un gate che renda l'avviso **bloccante** (oggi non lo è, ed è il motivo per
cui sei mappe sono rimaste così).

---

## §6-bis — Rilette una per una (2026-09-11), e la tabella §6 era sbagliata

Il DM ha chiesto di leggerle tutte e proporre mappa per mappa. Contate le celle
invece di fidarsi delle intestazioni, **tre righe su sei di §6 non reggono**, e
soprattutto **non sono tutte lo stesso difetto**: sono tre famiglie diverse, e
due chiedono decisioni opposte.

### Famiglia A — sbaglia l'intestazione, la griglia è giusta

| Master · mappa | Dichiara | Griglia vera | Proposta |
|---|---|---|---|
| `Portale-Forgia-L1` · 1 | 20×13 | **20 colonne × 14 righe** | correggere l'intestazione a `20×14`. Una riga di scarto, nessuna coordinata cambia |
| `Portale-Forgia-L2` · 1 | «53 COLONNE × 10 RIGHE» | **21 colonne × 53 righe** | ⚠️ è **trasposta** *e* sbagliata: correggere a `21×53`. Il numero 53 era giusto ma sull'asse sbagliato |
| `Portale-Forgia-L2` · 2 | 33×33 | **33 colonne × 25 righe** | correggere a `33×25` |

Su queste la proposta è la stessa: **si tocca l'etichetta, mai la griglia**. La
griglia è ciò su cui si gioca; l'intestazione è un cartellino, e il cartellino
mente.

### Famiglia B — l'intestazione è **giusta**, la griglia è incompleta

| Master · mappa | Dichiara | Disegnato | Il conto torna? |
|---|---|---|---|
| `…P1C-Rituale` · Campo Drow 1 | 53×40 (80 m × 60 m a 1,5 m) | **~33 colonne, 9 righe su 40** | ✅ 80 ÷ 1,5 = 53 · 60 ÷ 1,5 = 40. **L'aritmetica è corretta** |
| `Hammerfist-L2` · Disposizione Generale | 60×108 (1 quadretto = 3 m) | **60 colonne × 99 righe** | mancano **9 righe** |

🔴 **Qui correggere l'intestazione sarebbe il rimedio sbagliato.** Rimpicciolire
l'etichetta per farla combaciare con quel che è disegnato **restringerebbe il
campo di battaglia** — nel Campo Drow 1 da 80×60 m a circa 50×14 m. Sono mappe
**disegnate a metà**, non mal etichettate.

**Proposta**: marcarle come **estratto** in modo esplicito e verificabile,
lasciando l'area dichiarata dov'è. Completarle è lavoro di progettazione — cosa
c'è in quelle righe è una scelta di gioco, non una correzione — e va deciso a
parte.

### Famiglia C — nessun difetto

| Master · mappa | Dichiara | Griglia vera |
|---|---|---|
| `Hammerfist-L2` · 2A Fortezza | 120×80 | **120 × 80** ✅ |
| `Hammerfist-L2` · 2B Bastioni | 40×26 | **40 × 26** ✅ |

⚠️ **§6 dava `Hammerfist-L2` mappa 1 per «dichiara 120×80, griglia vera 50×80»**:
è falso, la griglia ha esattamente 120 colonne e 80 righe. L'ipotesi che «120×80
fossero metri» non regge: se lo fossero, a 1,5 m il campo sarebbe 80×53
quadretti, e i quadretti disegnati sono 120×80. **Nessuna azione.**

E la sesta riga di §6, `Hammerfist-Lotto-2-Assedio`, è finita in `_ARCHIVIO/`
con la decisione D1: è un master deprecato, fuori dal perimetro.

### Cosa resta da approvare

**Tre correzioni di etichetta** (famiglia A), **due marcature di estratto**
(famiglia B), **zero interventi** su famiglia C. Gli originali vanno in
`_ARCHIVIO/` prima di toccarli, come chiesto dal DM.

⚠️ **Una nota sull'archiviazione, da decidere insieme alle proposte**: per la
famiglia A la modifica è **una riga di cartellino**, e `git` conserva già ogni
versione precedente. Una copia in `_ARCHIVIO/` creerebbe un **secondo master**
della stessa mappa, che `validate_maps` poi sorveglia come se fosse vivo — è
esattamente ciò che è successo con D1, dove però i master erano davvero
superati. Proposta: archiviare **solo** dove si tocca la griglia (oggi: nessuno),
e per le etichette fidarsi di `git`. Se il DM preferisce la copia comunque, si fa
— basta saperlo prima.

---

## §7 — Le domande al DM prima di partire

> I numeri **D7-D10** erano citati in `STATO-E-ORDINE` §4 **senza esistere qui**:
> l'aggregato se li era inventati, ed è il difetto che ha fatto nascere
> [ADR-0047](adr/ADR-0047-le-decisioni-aperte-hanno-una-casa-sola.md). Numerazione
> conservata così com'era, perché i riferimenti già scritti restino validi.

<!-- decisioni-dm: RICERCA-MESTIERE -->

| # | Ambito | Domanda |
|---|---|---|
| ~~D7~~ | metro di paragone | ✅ **decisa 2026-09-11: le mappe di *Red Hand of Doom* e quelle di *Rise of the Runelords* (Paizo)** — *«voglio quella qualità e risultato, o il più vicino possibile»*. 🔎 Le prime **sono già nel repo**: **69 immagini** in `00_Red Hand Of Doom/Immagini/`, divise in `MappeIncontri`, `MappeLuoghiTattiche`, `MappeVarie` — il metro si guarda, non si immagina. ⚠️ **Rise of the Runelords non si porta nel repo**: è IP Paizo (ADR-0005). Si nomina come riferimento e si tiene fuori; l'audit cita numeri e criteri, mai i file |
| ~~D8~~ | stampa | ✅ **decisa 2026-09-11: a colori.** A1.6 (daltonismo) e A1.7 (resa in grigi) **restano non bloccanti**: la seconda perde quasi tutto il suo senso, la prima no — il daltonismo non dipende dalla stampante, e va tenuta come avviso |
| ~~D9~~ | doppia versione | ✅ **decisa 2026-09-11: né tutte né solo le hero map — quelle che nascondono qualcosa.** Il DM: *«per le mappe che hanno interazione con i giocatori e che devono nascondere cose ai giocatori o dettagli che devono scoprire»*. Il criterio è **funzionale**, quindi decidibile da chi scrive la mappa e non da una lista: se la griglia contiene una porta segreta, un nemico non ancora visto, una trappola o un indizio da scoprire, serve la versione giocatori. Oggi ce l'ha **una sola** (`tarsilia-la-ruota-giocatori`) |
| D10 | §6 | Le mappe con l'intestazione discorde. ✅ **Metodo scelto dal 2026-09-11: le leggo tutte e propongo mappa per mappa, il DM approva; gli originali vanno in `_ARCHIVIO/` prima di toccarli.** 🔎 **Lette il 2026-09-11, e la tabella §6 era sbagliata in tre punti su sei** — vedi §6-bis. La decisione **resta aperta**: si chiude quando il DM ha approvato le proposte |
