# PIANO — Un generatore di creature e PNG dalle tabelle

> **Stato**: ✅ **completo** — lotti A→H chiusi (2026-09-03).
> **Il debito del Bestiario è chiuso: 157 schede su 157 sistemate.** · **Aperto**: 2026-09-02 · **Avviato**: 2026-09-03
> **Decisioni del DM (§5)**: taratura **SRD 3.5 di norma, PF1e come variante
> più cattiva**; il generatore serve per **quello che nel Bestiario non c'è**;
> `suggest_encounter` deve poterne pescare una parte. Ruoli e tabelle del
> carattere: **proposti qui, da confermare**.
> **ADR**: [ADR-0034](adr/ADR-0034-generare-dalle-tabelle.md)
> **Nasce da**: domanda del DM — *«alla fine c'è un generatore di mostri e PNG,
> anche incantatori, fra i tool disponibili al DM, che usa quelle tabelle per
> generare le cose? ha senso creare un nuovo piano o è stato fatto?»*
> **Risposta**: **non è stato fatto.** `suggest_encounter` **pesca** dal catalogo
> (306 record esistenti); non costruisce niente di nuovo.
> **Precedenti da leggere prima**: [ADR-0021](adr/ADR-0021-statblocchi-machine-readable.md)
> · [ADR-0033](adr/ADR-0033-derivare-e-dichiararlo.md) · skill `dnd-35-srd`,
> `pathfinder-1e-srd`, `npc-villain-boosting`

---

## §1 · Perché questo è un problema DIVERSO da quello che è appena fallito

Va detto subito, perché il lotto H si è chiuso con una prova negativa e sarebbe
facile leggerla come un divieto.

Nel lotto H `derive_statblocks.py` ha provato a **ricavare i numeri da schede in
prosa già scritte**, e il collaudo li ha respinti quasi tutti. La causa è
strutturale: una scheda è un documento, non un dato, e un'espressione regolare ci
trova sempre qualcosa di plausibile — *«Esperto 2»* dove la riga diceva *«Esperto
2 / Acolita 6»*, i dadi di un morso scambiati per dadi vita.

**Generare è la direzione opposta, e non ha quel problema.** Non c'è prosa da
interpretare: si parte da **quello che il DM dichiara** — GS, ruolo, tipo,
taglia — e le tabelle producono i numeri. È esattamente l'uso per cui quelle
tabelle esistono. Un generatore non può leggere male una scheda perché **non
legge nessuna scheda**.

Il rischio qui è un altro, ed è il vero criterio di progetto: **produrre creature
generiche che si assomigliano tutte.** Un mostro che rispetta perfettamente la
riga della tabella e non ha niente di suo è peggio di nessun mostro: al tavolo si
gioca come tutti gli altri.

---

## §2 · Cosa esiste già (per non rifarlo)

| Strumento | Cosa fa | Cosa NON fa |
|---|---|---|
| `suggest_encounter.py` | sceglie 3-5 combinazioni per un EL bersaglio dal catalogo, per fazione/ambiente, con seed | non crea creature |
| `build_monster_catalog.py` | indicizza i 306 statblocchi esistenti | non genera |
| `derive_statblocks.py` | deriva CA/pf/TS **da una scheda esistente**; scrive i soli TS | non parte da zero |
| skill `npc-villain-boosting` | il **quadro decisionale** per potenziare | è dottrina, non un tool |
| `scripts/schemas/statblock.schema.json` | il **contratto** del blocco | — |

Il pezzo che manca è uno solo: **da (GS + ruolo + tipo) a un blocco completo.**

---

## §3 · Le tabelle, e quali sono davvero verificate

⚠️ **Prima cosa da fare, prima di scrivere codice.** In `derive_statblocks.py`
la tabella per GS ha venti righe, ma **solo otto sono verificate contro la fonte**
(GS 8 e 10-16); GS 1-7 e 17-20 le ho interpolate io, e il campo
`PER_GS_VERIFICATE` lo dichiara. Un generatore che le usasse come bersaglio
propagherebbe numeri non controllati su ogni creatura che produce.

**Lotto 0 del piano: verificare le dodici righe mancanti** contro la fonte
(`pathfinder-1e-srd/references/monster-advancement.md`, e la sua fonte a monte),
oppure dichiararle non disponibili e rifiutarsi di generare a quei GS.

Serve inoltre quello che oggi **non abbiamo in casa**:

- la **riga per gli incantatori** (livello dell'incantatore e CD primaria per GS)
  — il DM la segnala come esistente, va procurata e verificata;
- le **statistiche per GS dei PNG**, distinte da quelle dei mostri;
- ⚠️ e una **taratura 3.5**: le righe PF1e sono più dure a parità di GS, e questa
  campagna gira su 3.5. Generare sui numeri PF1e produrrebbe mostri
  sistematicamente più cattivi di quanto il GS promette. Va deciso e scritto in
  un ADR: o si tara, o si dichiara che il generatore produce «GS PF1e».

> **⚠️ Correzione, 2026-09-03 (ADR-0034).** L'ultimo punto qui sopra l'avevo
> scritto io e **è sbagliato**. Misurata contro i mostri del SRD 3.5, la riga
> PF1e non è «molto più dura»: Ogre GS 3 ha 29 pf contro i 30 della riga; il
> Gigante delle Colline GS 7 ne ha 102 contro 85. Sui punti ferita le due
> tarature si sovrappongono, e PF1e sta un punto o due sopra su CA e attacco.
> La taratura 3.5 è quindi la riga PF1e con **CA −1 e attacco −1** — non una
> derata al 70%, che avrebbe prodotto mostri di carta. La differenza vera fra i
> due sistemi sta nei **template**, ed è da lì che viene la variante più cattiva.
> *(Lascio il testo originale sopra invece di riscriverlo: la premessa sbagliata
> ha guidato il primo tentativo, e cancellarla nasconderebbe perché.)*

---

## §4 · I lotti

### ✅ Lotto A — Le tabelle, verificate e in un posto solo
Le righe per GS (mostri · PNG · incantatori) diventano un dato del repo, con la
**provenienza per riga** e il segno di quali sono verificate. Nessuna riga
inventata in silenzio. **Accettazione**: ogni riga cita la sua fonte; un test
confronta la tabella con le righe d'ancora della skill.

**✅ Chiuso 2026-09-03.** `scripts/dmcore/tabelle.py` — provenienza riga per riga, `PER_GS_VERIFICATE` conservato, e `derive_statblocks.py` ora **importa** invece di tenere una seconda copia. `test_tabelle.py`: 12 test, 134 sotto-test, che confrontano le griglie con le **ancore scritte nelle skill**, non con una costante accanto.

### ✅ Lotto B — Il generatore, per creature non incantatrici
`scripts/genera_creatura.py`: da `--gs`, `--tipo`, `--taglia`, `--ruolo`
(bruto · schermagliatore · tiratore · comandante) a un blocco completo, con
`--seed` per la riproducibilità (come `suggest_encounter`).
**Accettazione**: il risultato **supera il collaudo sul GS** — cioè la stessa
guardia che nel lotto H respingeva tutto, qui deve passare, e se non passa il
generatore è sbagliato. Test su tutti i GS disponibili e tutti i ruoli.

**✅ Chiuso 2026-09-03.** `scripts/genera_creatura.py`. ⚠️ La **prima versione non passava il collaudo**: un GS 7 con 38 pf e CA 12, −55% sul bersaglio. Costruiva ogni cosa come un PNG con la matrice standard; un mostro non si fa così. Riscritto risolvendo le caratteristiche **verso** il bersaglio, e ora sta nella fascia di Ogre, Troll, Ettin, Chimera, Gigante delle Colline e Osyluth.

### ✅ Lotto C — I PNG con livelli di classe
Razza + classi (comprese le classi PNG del SRD) + matrice elite/standard +
equipaggiamento per livello. **Accettazione**: un PNG generato e uno scritto a
mano dallo stesso profilo stanno nella stessa fascia.

**✅ Chiuso 2026-09-03.** Matrice élite/standard, aumenti ogni 4 livelli (senza, un mago di 9° usciva con Int 15), equipaggiamento per livello, e un collaudo **diverso**: per un PNG con classi il metro non è la riga dei mostri — sono i livelli. Il confronto col mostro resta stampato, ma per un'altra domanda: *regge un incontro da solo?*

### ✅ Lotto D — Gli incantatori
La parte che il DM ha chiesto per nome e che è la più delicata: livello
dell'incantatore, incantesimi al giorno dalle tabelle di classe SRD, CD primaria
dal GS, e **la scelta degli incantesimi** — che è dove un generatore diventa
banale se la fa a caso. Proposta: non estrarre a sorte da tutto il SRD, ma da
**liste per ruolo** (controllore · artigliere · sostegno) scritte a mano una
volta. **Accettazione**: le CD stanno sulla riga del GS; nessun incantesimo fuori
lista di livello.

**✅ Chiuso 2026-09-03.** Griglie SRD complete di mago, stregone, chierico, druido, adepto. ⚠️ Un difetto vero trovato dal test: un **chierico costruito come «controllore» prendeva Int 18 e Sag 13**, e la sua CD restava cinque punti sotto la riga del GS. La caratteristica da incantatore ora batte quella del ruolo. Le CD di mago e chierico cadono **esattamente** sulla riga PF1e a GS 5, 9 e 13.

### ✅ Lotto E — Il carattere, cioè la ragione per cui non è banale
Una creatura generata esce con **una cosa sua**: un talento firma, una tattica in
una riga, una debolezza sfruttabile. Prese da tabelle scritte a mano per ruolo,
non generate. ⚠️ **È questo lotto che decide se il tool serve**: senza, produce
mostri intercambiabili, e un mostro intercambiabile il DM se lo scrive prima da
solo che a leggerlo.

**✅ Chiuso 2026-09-03.** Quattro terne (talento firma · tattica · **debolezza sfruttabile**) per ognuno dei sei ruoli, scritte a mano. ⚠️ **Proposte al DM**, come chiedeva §5.

### ✅ Lotto F — Dove finisce l'output
**Non scrive mai dentro `Bestiario/`.** Stampa il blocco, o scrive in una
cartella di lavoro, e il DM decide se e come farlo entrare — lo stesso confine di
ADR-0033. Con `fonte: generato-SRD — <parametri e conto>`, così fra sei mesi si
sa da dove viene e lo si rifà uguale.

**✅ Chiuso 2026-09-03.** `--in <cartella>`, e un rifiuto esplicito a scrivere sotto `Bestiario/` con la ragione scritta. `fonte:` porta parametri e taratura.

---

### ✅ Lotto G — Il generatore dentro `suggest_encounter`
Aggiunto su richiesta del DM dopo l'apertura del piano: `suggest_encounter`
pesca dal catalogo, e con un'opzione **pesca in parte dal generatore**, così gli
incontri non escono mai due volte uguali. L'opzione «più cattivi» si propaga
alla sola parte generata. **Accettazione**: stesso seed → stesso incontro; il
GS combinato resta quello dichiarato.

**✅ Chiuso 2026-09-03.** `--con-generatore` e `--piu-cattivi`. L'innesto è nel
**pool**, non nel costruttore: aggiungere candidati e lasciar scegliere la logica
di bilanciamento di sempre evita di scriverne una seconda da tenere allineata.
⚠️ Metterli solo nel pool **non bastava**: dodici candidati contro 308 record del
catalogo non uscivano quasi mai, e l'opzione sembrava accesa senza esserlo — che
è il modo peggiore di sbagliare, perché non si vede. Ora una creatura generata
entra per forza in ogni proposta e il resto resta pescato dal Bestiario.
Verificato: stesso seed → output identico; **senza il flag l'output è byte per
byte quello di prima**.

---

## §5 · Le domande da porre al DM prima di cominciare

> **Risposte ricevute il 2026-09-03**, riportate qui perché il piano si legga da solo.

1. **La taratura**: 3.5 o PF1e? (vedi §3 — cambia ogni numero prodotto)
   → **SRD 3.5 di norma; PF1e come variante più cattiva, a richiesta.** Attuato
   in ADR-0034. ⚠️ Nel farlo è emerso che la premessa del piano era sbagliata:
   sulla riga base PF1e **non** è molto più duro del 3.5 (Ogre GS 3: 29 pf
   contro 30). La differenza sta nei *template*, e la variante più cattiva viene
   da lì — Advanced applicato senza alzare il GS.
2. **I ruoli**: quali servono davvero al tuo tavolo? Bruto, schermagliatore,
   tiratore, comandante, controllore, artigliere — o meno?
   → **Non risposta.** Proposti tutti e sei, come dati e non come rami del
   codice: toglierne uno è una riga in `RUOLI`.
3. **Il carattere (lotto E)**: le tabelle di talenti/tattiche firma le scrivi tu
   o le propongo io per la tua conferma?
   → **Proposte io**, in `CARATTERE`: 24 terne, quattro per ruolo. Da confermare.
4. **Dove finisce**: stampa a schermo, o un file in una cartella di lavoro?
   → **Tutt'e due**: stampa di norma, `--in <cartella>` quando serve un file.
   Mai dentro `Bestiario/`, che il tool rifiuta.

---

## §6 · Quando NON usarlo

Va scritto adesso, o il tool diventa la scorciatoia per tutto:

- se nel catalogo c'è già qualcosa di simile → **potenzialo** (`npc-villain-boosting`);
- se la creatura ha un ruolo nella trama → **si scrive a mano**, il generatore dà
  al massimo l'ossatura;
- se serve per **un incontro di passaggio** → è esattamente il suo caso.

### ✅ Lotto H — Le 52 schede che restavano
Punto 2 del DM: *«finisci le schede dei mostri e PNG che mancano»*.

**✅ Chiuso 2026-09-03 — 157 su 157.** Anche qui, come nel lotto H della catena
editoriale, il debito **non era una cosa sola**: erano quattro problemi diversi
contati come uno.

| Quante | Cos'erano | Cosa si è fatto |
|---:|---|---|
| **27** | i numeri stanno **altrove** e duplicarli sarebbe peggio: schede dei pregen in `ARC08-02`, PNG alleati in `ARC08-01`, dossier che puntano al proprio statblocco e viceversa, due schede di **stato finale post-mortem** che dicono a chiare lettere di non essere statblocchi | marcatore `[RIMANDO]`, **verificabile**: la scheda deve dire *dove*, e `--check` va a vedere che quel posto esista |
| **1** | non è una creatura: «Duergar della Scala di Ossa» è un **set d'incontro** di quattro PNG nominati, e il suo «GS 11» è il livello dell'incontro | `[NON-CREATURA]`, la sesta |
| **11** | avevano i numeri del DM in **dialetti che il parser non leggeva** | tre dialetti nuovi insegnati (vedi sotto) |
| **13** | dichiaravano i parametri ma non i numeri | costruite con le tabelle SRD, `fonte:` che dice quali campi sono derivati e quali letti |

**I difetti trovati per strada**, che valgono più delle schede:

- il parser leggeva righe che descrivono **altre creature dello stesso dossier**
  — il Conte Valerius prendeva la CA giusta (13) col dettaglio delle sue guardie
  («armatura completa +2») e i punti ferita esatti marcati «approssimati» per via
  del `~` delle guardie. Un blocco che descriveva due creature diverse;
- una **forbice** lasciata aperta dal DM non è un numero da scegliere: il
  Ghostlord dice «58–90, il DM adatta al livello del party». Il blocco tiene
  l'estremo basso e **scrive la forbice accanto**;
- tre schede dicevano «CA da SRD» citando il file d'origine, che è nel repo:
  lette invece che ricordate, e **tre numeri su quattro erano sbagliati a
  memoria** (Bebilith CA 22 e non 19, Phantom Fungus 14 e non 15, Retriever col
  BAB trascritto +10 dove il SRD dice +7);
- il generatore dava **CA 11 a un arcimago di GS 14**, perché non contava
  l'equipaggiamento: un PNG di quel livello ha 27.000 mo addosso, e la prima cosa
  che compra un incantatore sono bracciali e anello.

⚠️ Le 13 costruite sono **proposte da rileggere al tavolo**, e ognuna lo dichiara
nel proprio `fonte:`. Il confine di ADR-0033 resta: lo strumento propone.

### ✅ Documentazione
Un tool che nessuno sa di avere è un tool che non esiste. Misurato prima di
scrivere: `genera_creatura`, `--piu-cattivi`, `--con-generatore` e `[RIMANDO]`
comparivano in **zero** guide e **zero** skill.

- `GUIDA-BESTIARIO` §0 (la domanda «serve davvero una scheda nuova?»), §6-bis
  (tre strumenti invece di due, più «quando i numeri stanno da un'altra parte»),
  **§6-ter nuova** (costruire una creatura che non c'è, i sei ruoli, il carattere,
  `--piu-cattivi`, gli incontri che non si ripetono, e ⚠️ quando NON usarlo), §8
  (il rimando incrociato: potenziare se qualcosa c'è, generare se non c'è);
- skill `npc-villain-boosting`: una sezione **prima** dell'albero decisionale —
  potenziare presuppone qualcosa da potenziare;
- skill `rumblingstone-automation`: le due opzioni di `suggest_encounter`.
