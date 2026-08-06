# ADR-0018 — Il multi-gruppo è una directory, non un branch

**Stato**: accettata — esecuzione pianificata (lotto G12)
**Data**: 2026-08-05
**Decisione-fonte**: domanda DM 2026-08-05 — *«preferisco la struttura
`groups/<nome>/`; magari bisogna salvarsi il nome del gruppo in un file yml o
json e poi usarlo negli script group-aware, così hanno la cartella automatica
senza chiederlo ogni volta»*
**Sostituisce**: il meccanismo branch-per-gruppo di
[ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md) §branch (la guardia
resta, cambia su cosa vigila)

## Contesto

Il lotto G2-quater ha reso completo il reset per gruppo nuovo, ma ha lasciato
aperta la domanda strutturale: `main` continua a essere **due cose insieme** —
il *prodotto* (archi, Bestiario, mappe, skill) e il *file di salvataggio* di un
gruppo (stato, sessioni, storico, cronaca).

Finché convivono:

- ogni miglioria del prodotto va **mergiata in ogni branch di gruppo**, e il
  merge tocca esattamente i file che divergono sempre;
- due gruppi non possono coesistere senza cambiare branch;
- ogni file di stato nuovo va ricordato a mano nel reset — ed è già stato
  dimenticato due volte in un giorno solo (G2-bis, G2-ter).

## Decisione

### 1. Struttura

```
groups/
├── registry.yaml          # COMMITTATO: elenco gruppi (nome, DM, creato, stato)
└── <slug>/
    ├── state.yaml         ├── state.md
    ├── state-changelog.md ├── chronicle.md
    ├── sessions/          └── recaps/

campaign/                  # SOLO prodotto: premise, house rules, templates, glossario
```

Il gruppo esistente diventa **`groups/rumblingstone/`**.

### 2. Risoluzione del gruppo attivo — catena di precedenza

```
--group <slug>              esplicito, vince su tutto
RUMBLINGSTONE_GROUP=<slug>  variabile d'ambiente
.rumblingstone-group        file locale GITIGNORED (da .rumblingstone-group.example)
un solo gruppo nel registro → si usa quello, senza chiedere
altrimenti                  errore che elenca i gruppi disponibili
```

Il puntatore locale è **gitignored** per scelta: due DM sullo stesso repo non se
lo contendono. Il template committato `.rumblingstone-group.example` contiene il
valore fra virgolette doppie.

**Perché `registry.yaml` è committato**, e non è un dettaglio: gli **agenti AI
non eseguono il resolver**, leggono file — e un puntatore gitignored su un clone
fresco non esiste. Col registro committato, la regola «un solo gruppo → usalo»
smette di essere una comodità e diventa **il meccanismo che permette a un agente
di orientarsi da solo**. Con due o più gruppi, l'agente chiede.

### 3. Lo slug, non le virgolette

I nomi di gruppo rispettano `^[a-z0-9][a-z0-9-]{1,30}$`, verificato alla
creazione.

Quotare il valore nell'env cura il *sintomo* (spazi, accenti); lo slug elimina la
*classe* — un nome che non può contenere spazi, slash o accenti non rompe né un
path, né una shell, né un nome di branch. Le virgolette restano comunque, come
cintura oltre alle bretelle.

### 4. Un solo resolver

`dmcore/groups.py` espone `resolve(group=None) -> GroupPaths` con i campi
`state_yaml`, `state_md`, `changelog`, `chronicle`, `sessions`, `recaps`.

> **Nessuno script conosce più un percorso di stato.**

Oggi `campaign/state.yaml` è cablato in sei punti; dopo, in zero. È il punto di
design che decide se il refactor regge o si sfalda al primo file nuovo — ed è la
stessa lezione della regola R2 di `validate_state`, che elencava le sezioni a
mano e si è disallineata al primo lotto: **una lista scritta due volte diverge**.

Un parent parser argparse condiviso dà `--group` a tutti gli script senza
duplicare il codice.

### 5. La guardia: canone, non commit

La guardia di ADR-0007 si sposta dal branch alla directory. Vigila su **due**
condizioni:

1. una scrittura di canone con gruppo **non risolto** → blocco, con l'istruzione
   di creare `.rumblingstone-group` o esportare `RUMBLINGSTONE_GROUP`;
2. una scrittura dentro `groups/<x>/` mentre il gruppo attivo è `<y>` → blocco.

**Non** blocca i commit privi di gruppo in generale: i commit al **prodotto**
(script, skill, piani, archi, Bestiario) non hanno un gruppo e non devono
averlo. Una guardia che bloccasse tutto verrebbe disattivata in una settimana.

### 6. Memoria degli agenti: context pack generato, nessun memory store

Domanda collegata del DM: *«ha senso un sistema di memory per gli agenti, o
basta il campaign state?»*

**Basta lo stato — a condizione di renderlo consultabile.** Un memory store
esterno è non versionato, non revisionabile e può divergere dal repo: cioè
reintroduce il finding **C2** (due fonti di verità) nella forma peggiore, perché
una memoria che contraddice `state.yaml` è **invisibile a ogni gate**. E un
agente che «ricorda» qualcosa mai approvato dal DM è precisamente il vettore
contro cui è costruito l'impianto `[INFERRED]`.

Il problema vero non è la memoria, è che **lo stato non entra in un contesto**.
Rimedio: `dm.py brief --for-agent`, un pacchetto **generato** dai dati
(~200 righe) con confine giocato/preparato, party di oggi, clock attivi, fili
aperti, `[INFERRED]` pendenti, ultime sessioni.

**Vincolo di progetto**: il brief è un **indice, non un riassunto**. Ogni riga
porta il puntatore al dato pieno (`state.yaml#villain[Ghaurush]`,
`Bestiario/villain/…`), così l'agente che deve approfondire sa dove andare invece
di rileggere tutto. Un riassunto senza puntatori è un vicolo cieco.

Il *perché* delle decisioni — l'altra metà della memoria — **esiste già**: ADR
per l'infrastruttura, `plans/CHANGELOG.md` per i lotti, `state-changelog.md` per
il canone, Echo Ledger §7.E per le scelte che il mondo ricorda.

## Conseguenze

**Positive**

- `main` torna a essere **solo prodotto**: `git pull` non conflitta mai con la partita.
- Più gruppi coesistono senza cambiare branch.
- I path di stato spariscono dagli script: aggiungere un file di stato è una
  riga nel resolver, non una caccia in sei sorgenti.

**Negative, dichiarate**

- Refactor su ~10 script, più i path in `AGENTS.md`, nelle skill e nei test.
- Migrazione = diff enorme su file di canone: va in una **PR dedicata**, altrimenti
  non è rivedibile.
- Per un po', i vecchi path resteranno nella memoria di chi ha già letto il repo.
- Un livello di indirezione in più rispetto a «i file stanno in `campaign/`».

**Gate**: la migrazione parte dopo G3 e G4, in una PR sua.
