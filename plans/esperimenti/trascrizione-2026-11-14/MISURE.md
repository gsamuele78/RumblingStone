# Misure della trascrizione locale — banco non personale (ADR-0135)

**Dove**: container del repo, CPU a 4 thread, nessuna GPU. whisper.cpp
5922450 (2026-11-13), modello `ggml-large-v3-turbo-q5_0`, `-l it`. Sul PC del DM
si userà `q8_0` sulla RTX 4050: la velocità di qui **non** vale là.

**Audio**: nessuno di un tavolo vero.

- **FLEURS** (Google, CC BY 4.0): le prime 40 righe di `it_it/dev`, 10,8 minuti,
  lettori umani. Attenzione: sono 17 frasi diverse lette da più persone, quindi
  molte frasi si ripetono.
- **Copione finto** (`copione.txt`, 16 battute, 80 secondi) letto dalla voce
  sintetica Piper `it_IT-paola-medium` (CC0), pulito e con rumore rosa ed eco
  (`banco.sh`). Riferimento corretto in `copione-riferimento.txt` (numeri in
  cifre, come li scrive whisper). Ci sono 20 occorrenze di nomi della campagna.

**Misura**: `transcribe_session.py misura`: errori di parola sulla versione
corretta (minuscolo, senza punteggiatura, accenti e apostrofi). «Nomi giusti»
conta le occorrenze dei nomi di `state.yaml` scritte esattamente; «inventati»
quelle che la trascrizione mette dove il riferimento non le ha.

## Risultati

### FLEURS, italiano letto

| Configurazione | Parole sbagliate | Parole perse in buchi ≥ 8 | Tempo |
|---|---|---|---|
| contesto acceso (default di whisper) | **16,6%** (168/1012) | 135 | 819 s |
| `-mc 0` (senza testo precedente) | **5,8%** (59/1012) | 33 | 582 s |

Col contesto acceso whisper **salta interi pezzi** quando una frase somiglia a
una già detta (qui succede perché le frasi si ripetono; al tavolo succede con
«tiro per colpire», «tira i danni», le formule che tornano). Tolti i buchi,
l'errore è circa 3%, in linea con quello che si pubblica per whisper
sull'italiano letto. Da qui la scelta: `-mc 0` di serie.

### Quantizzazione e VAD (17/11, sullo stesso FLEURS, sempre `-mc 0`)

Il kit della 4050 (#469) ha trovato 8,6% con `q8_0` + VAD contro il 5,8% di
qui (`q5_0` senza VAD). Stesso audio, stessa colonna 3 di `dev.tsv` (la
trascrizione grezza) come riferimento in tutti e due i casi: la differenza non
viene da lì. Rifatto tutto qui, CPU a 4 thread:

| Modello | VAD | Parole sbagliate | Parole perse in buchi ≥ 5 | Tempo |
|---|---|---|---|---|
| `q5_0` | no | 5,8% (59/1012) | — | 582 s |
| `q5_0` | silero-v6.2.0 | 6,1% (62/1012) | 62 | 484 s |
| `q8_0` | no | **2,3%** (23/1012) | 0 | 237 s |
| `q8_0` | silero-v6.2.0 | **8,6%** (87/1012) | 62 | 188 s |

- Il kit è riprodotto esatto (8,6%).
- **La quantizzazione** conta: `q8_0` sbaglia 2,3% contro 5,8% di `q5_0`.
- **Il VAD** fa perdere pezzi di frase (62 parole in buchi, tre frasi
  intere o quasi). Qui le frasi FLEURS sono incollate senza pause, quindi il
  banco è sfavorevole al VAD; al tavolo, con lunghi silenzi, il VAD può invece
  evitare frasi inventate. Non è misurato: di serie resta spento, e si prova
  sulla serata solo se compaiono frasi inventate.
- I tempi di oggi (237 s per `q8_0`) e quelli del 14/11 (582 s per `q5_0`)
  non sono confrontabili: il container non era lo stesso.

Soglia di riferimento per la 4050: **2,3%** con `q8_0`, `-mc 0`, senza VAD.

### Copione finto, nomi della campagna

| Configurazione | Pulita: errori · nomi giusti · inventati | Rumore: errori · nomi giusti · inventati |
|---|---|---|
| contesto acceso, senza prompt | 14,5% · 4/20 · 0 | 14,1% · 7/20 · 1 |
| contesto acceso, prompt coi nomi scritto a mano¹ | 11,3% · 10/20 · 4 | 14,1% · 9/20 · 4 |
| `-mc 0` (di serie) | 13,3% · 6/20 · 0 | 12,5% · 6/20 · 0 |
| `-mc 0` + prompt dai nomi di `state.yaml` | identico alla riga sopra | identico alla riga sopra |

¹ nove nomi scelti a mano, non quelli che genera lo script.

- Col contesto spento il prompt **non conta niente**: whisper lo tiene nel
  contesto, che `-mc 0` azzera. Le due opzioni si escludono, e lo script lo dice.
- Il prompt coi nomi ne corregge alcuni (Hammerfist, Ushgar Occhio Reso,
  Cenerevento) ma ne **sostituisce** altri: «Tordek chiede» diventa «Thorik
  chiede». Quattro nomi inventati su venti occorrenze sono peggio di un nome
  storpiato, perché un nome storpiato si riconosce e uno sbagliato no.
- Il numero dei nomi è pessimista e poco affidabile: la voce sintetica legge
  «Thorik» come «Tordic» e «Azarr Kul» come «Ansar qui». Con voci vere i nomi
  saranno diversi, non per forza migliori. Il 6/20 dice solo che sui nomi
  inventati whisper sbaglia **più della metà delle volte**.
- I numeri (tiri, danni, monete, PX, giorni) escono giusti in tutte le prove.

### Velocità

Sulla CPU a 4 thread `-mc 0` va a circa 1,1 volte il tempo reale: quattro ore
di serata sarebbero quasi quattro ore di calcolo. Sulla RTX 4050 la velocità
va misurata (`misura.json` la scrive da sé).

## Cosa non dice questo banco

Nessuna voce vera di un tavolo, nessuna sovrapposizione di voci, nessun
microfono lontano, nessun dado che rotola. La misura che decide è la serata
(guida §4).
