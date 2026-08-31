# Mistero e documento — il pilastro Eco, ridotto a operazioni

**Perché esiste questo file.** *Il nome della rosa* è, sotto il saio, una storia
di Sherlock Holmes: un investigatore che deduce (Guglielmo **da Baskerville**,
e il nome è dichiarato), il suo Watson che racconta senza capire (Adso), e un
delitto per volta dentro una **comunità chiusa che vive di regolamenti**. È la
forma esatta che serve a un modulo d'indagine — e non era coperta da nessuno
degli otto pilastri: Andor dà la *procedura* della cospirazione, GoT dà la
*politica*, BG1-2 dà la *struttura* della quest. Nessuno dei tre dice **come si
costruisce un indizio**.

> ⚠️ **Eco entra come metodo, non come atmosfera.** Non serve un'abbazia, non
> servono i monaci, non serve il latino. Servono quattro operazioni. Chi usa
> questo pilastro per scrivere paragrafi lunghi e dotti l'ha usato al contrario.

---

## 1. Le quattro operazioni

| # | Operazione | Cosa produce al tavolo |
|---|---|---|
| 1 | **Il documento è l'indizio, e conta ciò che vi manca** | un oggetto che i giocatori possono girare fra le mani invece di un tiro di dado |
| 2 | **La comunità chiusa e il suo regolamento** | un potere che si esercita *interpretando* la regola, non impugnando la spada |
| 3 | **L'errore fecondo** | la deduzione sbagliata del tavolo diventa una pista vera — l'antidoto al binario |
| 4 | **Il dettaglio erudito che è anche il meccanismo** | il particolare d'epoca che più avanti ammazza qualcuno |

---

## 2. Operazione 1 — il documento è l'indizio, e conta ciò che manca

Un documento non è un pezzo di colore: è un **testo scritto da qualcuno, per
qualcuno, con un motivo**. Tre domande prima di scriverne uno:

1. **Chi lo ha scritto** — e con quanta fretta, con quanta istruzione;
2. **Per chi** — un registro parla al padrone, una lettera all'amante, una
   ricevuta a nessuno (ed è per questo che le ricevute non mentono);
3. **Cosa ha taciuto** — ed è qui che sta l'indizio.

> **La riga da ricordare**: in un documento la prova non è quasi mai quello che
> c'è scritto. È **il buco**: la firma che manca, la riga che è stata cancellata
> troppo bene, il nome che compare due volte con due grafie.

Il repertorio delle assenze utili — ognuna è un indizio già pronto:

| L'assenza | Cosa lascia dedurre |
|---|---|
| la **firma che manca** su una correzione | qualcuno ha corretto senza volerne rispondere |
| la **data giusta** in mezzo a date sbagliate | quel giorno chi scriveva era attento: era presente |
| la **cifra che non torna** di poco | non è un furto: è un favore |
| lo **stesso nome con due grafie** | due mani diverse, o una che imita |
| una **pagina strappata a filo** | non fretta: uno strumento e tempo |
| un **atto perfettamente in regola** in un registro sciatto | è stato scritto **dopo**, per essere trovato |

Vincoli pratici, che valgono più di qualunque teoria:

- **si legge in trenta secondi.** Un handout che chiede due minuti di lettura
  silenziosa ferma il tavolo. Se il testo è lungo, l'indizio va **in alto**;
- **una sola bugia per documento.** Due e nessuno le trova entrambe;
- **il documento non spiega sé stesso.** Nessuna riga del tipo *«e questo prova
  che…»*: quella riga è del giocatore, non dell'autore;
- **la resa materiale è metà dell'indizio** — carta, mano, macchia, timbro. La
  regia dell'oggetto sta in [ADR-0014](../../../plans/adr/ADR-0014-regia-sensoriale-obbligatoria.md)
  e i template in `campaign/templates/homebrew/`.

---

## 3. Operazione 2 — la comunità chiusa e il suo regolamento

L'abbazia di Eco funziona come un motore politico diverso da quello di GoT, e la
differenza è precisa:

| | Game of Thrones | Eco |
|---|---|---|
| Il potere sta in | alleanze, eserciti, matrimoni | **chi ha il diritto di interpretare la regola** |
| Si vince | facendo fuori l'avversario | facendo **applicare** la regola all'avversario |
| L'arma | la spada, il veleno | il **precedente** |

Tre mosse che rendono la cosa giocabile:

1. **La regola citata a memoria, e sbagliata.** Un PNG cita un articolo e ne
   storpia il numero o il senso. Chi lo corregge in pubblico **si fa un nemico**;
   chi lo lascia correre ottiene un favore. È una scelta vera, e costa zero.
2. **L'eccezione che diventa precedente.** I PG chiedono uno strappo. Glielo si
   concede — e nella scena successiva **qualcun altro lo invoca contro di loro**.
3. **Il custode del regolamento non ha altro potere.** Il funzionario, il
   sagrestano, il maestro di campo: contano solo finché la regola conta. Difendono
   la regola come si difende la propria casa, perché è la propria casa.

Comunità chiuse già disponibili nel repo: le **contrade** (regolamento di gara,
diritti di rione), gli **ordini** e le **gilde**, un **collegio di custodi**. Non
serve inventarne di nuove per usare questa operazione.

---

## 4. Operazione 3 — l'errore fecondo (il pezzo anti-binario)

In *Il nome della rosa* l'investigatore arriva alla verità **seguendo uno schema
che non esiste**. È l'ammissione più preziosa del libro per chi mastera: la
deduzione sbagliata può portare al posto giusto, e questo legittima esattamente
la cosa che al tavolo succede sempre.

> **La regola per il DM**: quando il tavolo deduce male, non si corregge e non si
> conferma. **Si lascia che il mondo risponda** — e il mondo, spesso, dà loro
> ragione per un altro motivo.

Tre modi di renderlo concreto:

1. **La pista falsa vera.** L'indizio è autentico; è il **nesso** a essere
   sbagliato. La ricevuta esiste davvero, la cifra è davvero strana — ma per una
   ragione che non c'entra col delitto. Chi la segue **trova qualcos'altro di
   vero**, e non ha perso la serata.
2. **Il colpevole sbagliato confessa un altro reato.** Si accusa la persona
   sbagliata e quella, messa alle strette, ammette la *sua* cosa: un contrabbando,
   un debito, un figlio. La trama guadagna un ramo che non avevi scritto.
3. **L'ipotesi del tavolo diventa canone** se non contraddice niente di già
   scritto. È la stessa disciplina dello *yes-and* di Mercer, applicata alla
   soluzione invece che alla scena — e va **annotata in `state.md`** nello stesso
   momento, altrimenti è solo una cortesia che il DM dimentica.

⚠️ **Il limite onesto, e non è negoziabile**: l'errore fecondo funziona solo se
**la soluzione vera esiste, è scritta e è raggiungibile**. Un mistero senza
risposta preparata non è aperto: è sciatto, e i giocatori lo sentono al secondo
tentativo. Vedi §5.

---

## 5. La regola dei tre indizi e l'orologio degli indizi

L'attrezzo di design che tiene in piedi le operazioni 1 e 3 (la *three-clue
rule*, formulata da Justin Alexander e ormai patrimonio comune del mestiere):

> **Per ogni conclusione a cui i giocatori devono poter arrivare, si scrivono
> TRE indizi indipendenti.** Non perché servano tutti: perché due si perdono.

Come si applica qui:

- i tre indizi devono stare su **canali diversi** — un documento, una
  testimonianza, una cosa fisica in un luogo. Tre documenti sono **un** canale;
- **indipendenti** vuol dire che nessuno dei tre richiede di aver trovato gli
  altri due;
- il terzo indizio è quello che si può **muovere**: se il tavolo non ha in mano
  niente dopo tre scene, **l'indizio va da loro** — per bocca di un PNG che ha
  una sua ragione per parlare, mai per intuizione gratuita di un PG;
- l'orologio si scrive accanto al mistero, non si tiene a mente: *«scena 3 senza
  nulla in mano → il carrettiere racconta della ricevuta»*.

Il rapporto con il resto: gli indizi mossi sono **echi in entrata** — si
registrano come qualsiasi altra conseguenza
(`consequence-echoes.md`), perché un indizio consegnato a forza è un debito che
il mondo ha contratto e il tavolo se ne ricorderà.

---

## 6. Operazione 4 — il dettaglio erudito che è anche il meccanismo

In Eco nessun dettaglio tecnico è ornamento: il modo in cui si costruisce una
biblioteca, si mescola un inchiostro, si conserva un veleno è sempre **la cosa
che poi uccide qualcuno**. Il test è di una riga:

> **Se tolgo questo dettaglio, cambia qualcosa nella soluzione?**
> Se no, è colore — legittimo, ma non va presentato come indizio.

Le due metà della regola, e la seconda si dimentica sempre:

1. **Il dettaglio che è meccanismo va piantato presto**, in un contesto in cui
   sembra innocuo (un mestiere descritto, un prezzo, una precauzione). Se compare
   per la prima volta nella scena in cui serve, è un *deus ex machina*.
2. **Il colore resta colore, e non si traveste.** Un particolare inutile ma vero
   fa bene alla scena (`read-aloud-adulti.md` §sul dettaglio inutile) — a patto
   che il DM sappia quali dei due è, perché il tavolo inseguirà comunque
   entrambi.

Sul livello di competenza: **si scrive come chi il mestiere lo conosce**, non
come chi lo ha studiato. Un tintore non spiega la tintura: si lamenta del prezzo
dell'allume e del fatto che con questo tempo il blu «prende male».

---

## 7. La clausola di salvaguardia — dove Eco NON entra

Il pilastro ha una controindicazione precisa, e va dichiarata perché è la sua
tentazione naturale:

> **Eco entra al livello della struttura e dell'oggetto, mai a quello della
> lunghezza del paragrafo. In caso di conflitto vincono i limiti del
> read-aloud.**

In concreto:

- **niente descrizioni lunghe**: i tetti del read-aloud di `read-aloud-adulti.md`
  restano quelli (max ~12 righe per box, **un solo nome proprio nuovo**, massimo
  due subordinate). Un incipit da romanzo letto ad alta voce **stacca il tavolo**
  al terzo periodo;
- **niente erudizione esibita**: nessuna citazione latina, nessun trattato
  riportato, nessun elenco di autorità. La competenza si mostra con **una** cosa
  concreta;
- **niente name-dropping** (non-negoziabile 4 della skill): il pilastro è una
  fonte di mestiere, mai un riferimento da nominare nella finzione o da imitare
  così da vicino da leggersi come la fonte;
- **non è il pilastro di ogni scena.** Eco guida le scene di **mistero e
  documento**. Un combattimento resta Salvatore, una scena politica resta GoT.

---

## 8. Rapporto con gli altri riferimenti

| Cosa | Dove |
|---|---|
| I profili completi dei nove pilastri | `style-pillars.md` §9 |
| I **tetti** del read-aloud, che vincono sempre | `read-aloud-adulti.md` |
| La **lingua** dei documenti in-fiction | `italiano-nativo.md` |
| L'indizio consegnato = **eco in entrata** | `consequence-echoes.md` |
| Le **fasi** della quest in cui il mistero si incastra | `quest-design-baldur.md` |
| La resa **materiale** dell'handout (carta, mano, macchia) | ADR-0014 + `campaign/templates/homebrew/` |

> **Ordine d'applicazione**: prima la struttura (questo file), poi la voce
> (`style-pillars.md`), poi la lingua (`italiano-nativo.md`), **infine i tetti
> del read-aloud** — che sono l'ultima parola e non si negoziano.
