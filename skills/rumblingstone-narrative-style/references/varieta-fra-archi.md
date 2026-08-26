# Varietà fra gli archi — la tavolozza e il governo del ritmo

Il mixer di `SKILL.md` decide **quale pilastro guida una scena**. Non dice
niente su **di che colore è un arco intero**, né se quel colore è già stato
usato nell'arco precedente. Questo file copre quel piano — ed è il piano su
cui una campagna diventa «abbatti abbatti mostro» senza che nessuna singola
sessione sia scritta male.

> **Il difetto che questo file previene**: ogni arco, preso da solo, può
> essere ottimo; e la campagna essere monotona lo stesso. La monotonia non è
> un difetto di scena, è un difetto di **sequenza**, e non si vede leggendo
> un modulo — si vede leggendo due recap di fila.

---

## 1. La tavolozza d'arco — cinque dichiarazioni

Ogni arco dichiara queste cinque cose **prima** che se ne scriva il
contenuto. Stanno in cinque righe, non in un documento.

```
COLORE DOMINANTE   la tinta che il tavolo ricorderà (una sola)
CONTRAPPUNTO       la seconda tinta, ~1/4 dell'arco. DIVERSA dal dominante
FAMIGLIA DI CASO   quale delle sei, oppure «nessuna» (dichiarata, non omessa)
CONGEGNO           uno, oppure «nessuno». Mai due
IL PICCO           la scena da fotografare (una per arco, dichiarata)
```

`«nessuna»` e `«nessuno»` sono risposte legittime e vanno **scritte**: un
arco senza indagine è una scelta, un arco che si è dimenticato di averne una
è un incidente. La differenza si vede solo se la casella è compilata.

## 2. Le sei tinte

| Tinta | Com'è al tavolo | Cosa stanca | L'antidoto (= il contrappunto giusto) |
|---|---|---|---|
| **Guerra / assedio** | pressione continua, decisioni di massa, perdite | la ripetizione tattica: dopo tre scontri il quarto è aritmetica | una tinta **stretta** — indagine o orrore: pochi, al chiuso, in silenzio |
| **Indagine** | lento, verbale, i giocatori parlano più del DM | l'immobilità: se non si muove niente si spegne | **guerra** o **esplorazione**: qualcosa che costringe a muoversi |
| **Politica** | tavoli, favori, reputazione come risorsa | l'astrazione: se non arriva a misura di PG è fondale | **orrore** o **indagine**: qualcosa di concreto e sporco |
| **Esplorazione / viaggio** | il mondo è grande, le risorse contano | la lista di luoghi: tre villaggi non sono tre scene | **politica**: arrivare da qualche parte e trovarci gente |
| **Orrore** | pochi, al buio, sotto qualcosa che non si capisce | l'assuefazione: al terzo mostro impossibile è un mostro | **cerimonia** o **guerra**: luce, gente, rumore |
| **Cerimonia / rito** | il tavolo guarda, il mondo riconosce i PG | non regge una sessione intera, quasi mai | **qualunque cosa la interrompa** |

L'ultima colonna è il vero contenuto della tabella: **il contrappunto non è
un capriccio, è la cura del difetto specifico del dominante.**

## 3. Le regole di rotazione — il governo

1. **Due archi consecutivi non hanno lo stesso colore dominante.** Nessuna
   eccezione, nemmeno «ma questa guerra è diversa».
2. **Il contrappunto di un arco è il dominante di quello dopo** (o di quello
   prima). Così la varietà è **preparata** invece che a scatti: il tavolo ha
   già assaggiato la tinta nuova prima che diventi il piatto principale.
3. **Un congegno per arco al massimo, e mai due archi di fila.** È la
   risorsa che si consuma più in fretta
   (`rumblingstone-indagine/references/congegno-e-enigmi.md` §9).
4. **Una famiglia di caso non si ripete a meno di due archi di distanza.**
   Due impostori vicini e il terzo lo indovinano dal titolo.
5. **Un arco senza indagine è legittimo** — ma allora il contrappunto deve
   essere forte, e dichiarato.
6. **Ogni arco ha almeno una sessione che non gioca come le altre.** È il
   quarto d'arco del contrappunto: se non riesci a indicarla col dito, non
   c'è.

## 4. La prova del recap — la diagnosi in trenta secondi

> Prendi i recap di due archi consecutivi, **togli i nomi propri**, e
> leggili di fila. Se suonano uguali, uno dei due va ricolorato.

Funziona perché il recap registra **cosa ha fatto il tavolo**, non cosa il
DM aveva preparato. Due archi possono avere ambientazioni diversissime e
produrre lo stesso recap: *«siamo arrivati, abbiamo combattuto, abbiamo
vinto, siamo ripartiti»*. Quello è il segnale.

Diagnosi correlate, più veloci:

- **Nell'ultimo arco, quante scene si sono chiuse senza tirare iniziativa?**
  Se meno di un quarto, il dominante è guerra qualunque cosa dica la
  tavolozza.
- **Il picco dichiarato è lo stesso tipo di scena del picco precedente?**
  (Due cariche di fila, due rivelazioni di fila.) Se sì, ricolora.

## 5. Il registro — dove vive

La tavolozza è **dato di campagna**, non di skill: vive in
`campaign/state.md` §7 accanto agli altri tracker, e si scrive col triplo
vincolo di [ADR-0007](../../../plans/adr/ADR-0007-scritture-canone-triplo-vincolo.md).
Formato:

```markdown
### §7.T — Tavolozza degli archi

| Arco | Dominante | Contrappunto | Famiglia di caso | Congegno | Picco |
|---|---|---|---|---|---|
| 07 | esplorazione | orrore | nessuna | — | … |
| 08 | guerra | ? | ? | ? | la carica (4C) |
| 09 | ? | ? | ? | ? | ? |
```

**Le celle `?` sono informazione**: dichiarano che la decisione non è stata
presa, e impediscono di scoprirlo a metà arco.

## 6. Applicazione proposta agli archi in corso

> ⚠️ **`[PROPOSTA — needs DM confirmation]`.** Questa sezione non è canone e
> non è stata scritta in `state.md`: ARC-08 e ARC-09 sono **preparati** e la
> loro colorazione è una decisione del DM, non di un agente
> (`campaign-coherence.md` §0). Serve come esempio lavorato del §1 e come
> proposta concreta da approvare, correggere o rifiutare.

### ARC-08 — Battaglia di Hammerfist

| | |
|---|---|
| **Dominante** | **guerra / assedio.** Non si discute: è l'arco della battaglia |
| **Contrappunto proposto** | **indagine, tinta stretta** — e *dentro* le scene già scritte, non in scene nuove |
| **Famiglia proposta** | **2 — l'impostore.** Un assedio è un cast chiuso in uno spazio chiuso: la condizione ideale della famiglia. Gli errori di competenza (§famiglie-di-caso 2) si posano dentro i consigli di guerra che l'arco ha già |
| **Congegno** | **nessuno.** L'arco ha già 68 read-aloud e un picco dichiarato (la carica, 4C): una macchina competerebbe col picco invece di servirlo. E per la regola 3 conviene spenderlo dopo |
| **In compenso** | **un innesco in piena vista** (`congegno-e-enigmi.md` §5) — a scala d'assedio: un tratto di mura minato, un pozzo, il meccanismo di una porta. Costa una descrizione, non un arco |
| **Picco** | resta quello già dichiarato dall'arco |

**Perché questa combinazione**: è la sola che aggiunge varietà **senza
riscrivere niente**. L'impostore gira dentro le scene esistenti; l'innesco è
una riga in una descrizione. Il costo di preparazione è quasi zero e il
recap dell'arco smette di essere *«abbiamo difeso e abbiamo vinto»*.

### ARC-09 — dopo Hammerfist

L'arco è **modulare** (una decina di quest parallele fra Day 20 e Day 42) e
per questo è il posto naturale per la varietà: le tinte non si susseguono,
**convivono**, e sceglie il tavolo.

Proposta di colorazione per ramo, una famiglia diversa ciascuno:

| Ramo | Tinta | Famiglia proposta | Nota |
|---|---|---|---|
| Torre Invisibile (Zalkatar) | orrore | — | **il congegno dell'arco**, se il DM ne vuole uno: una torre che non si vede *è già* la premessa di una macchina |
| Torneo di Dauth (Tordek) | cerimonia | **5 — accusa falsa** | cast chiuso, reputazione in gioco, e Tordek ha lo spotlight. ⚠️ **vincolo esistente**: il Giorno 3 è già occupato (INDEX, innesto I5) |
| Salvatore Mercante | esplorazione | **4 — la sparizione** | è già una quest di recupero: la famiglia costa zero |
| Ghostlord | politica | — | i tre rami esistenti fanno già il lavoro |
| Campi Drow | infiltrazione (Andor) | — | procedurale, non deduttivo: giusto così |
| Rethmar (battaglia finale) | guerra | — | il dominante torna, ed è giusto che torni **alla fine** |

⚠️ **Osservazione da portare al DM, non risolvibile da un agente**: ARC-09
come pianificato vale, per estensione e durata, più di un arco solo. La
regola 3 («un congegno per arco») va allora interpretata: *un congegno per
ARC-09 intero* è probabilmente troppo poco, *uno per ramo* è certamente
troppo. La proposta sopra ne mette **uno**, sulla Torre. È una decisione del
tavolo.

## 7. Autocontrollo, prima di dichiarare un arco pronto

1. Le cinque righe della tavolozza sono compilate, `«nessuna»` incluse?
2. Il dominante è diverso da quello dell'arco precedente?
3. Il contrappunto è la cura del difetto del dominante (§2, ultima colonna)?
4. So indicare **quale sessione** è il quarto d'arco che gioca diverso?
5. Il picco è di un tipo diverso dal picco precedente?
6. Prova del recap: tolti i nomi propri, questo arco suona come il
   precedente?
