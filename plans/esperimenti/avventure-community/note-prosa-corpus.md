# Il corpus di riferimento della prosa: i box letti dai PDF, misurati con i rilevatori del repo

**Data**: 2026-10-18 · **Lotto**: 4 di [PIANO-AVVENTURE-COMMUNITY](../../PIANO-AVVENTURE-COMMUNITY-2026-10.md) · **Segue**: `note-prosa-2.md` (gli indicatori di stile) e la prima misura a distanza del corpus, fatta lo stesso giorno senza i PDF.
**Legenda**: **[misurato]** = contato da me sui box estratti · **[letto]** = l'ho letto nel PDF · **[inferenza]** = deduzione mia.

⚠️ **I testi di terzi non sono nel repo.** I PDF, i box estratti e le misure box per box stanno nella cartella privata del progetto (`corpus-prosa/`). Qui ci sono solo numeri derivati e nessuna citazione.

---

## 0 · Che cosa è cambiato rispetto alla prima misura

La prima misura del corpus (stessa giornata) non aveva i PDF: la rete dell'ambiente rifiutava `downloads.paizo.com` e `www.gruppochimera.it`, e i conteggi venivano da un modello che leggeva il PDF a distanza. Con l'ambiente nuovo i due domini rispondono, e questa volta:

- i **22 PDF** sono scaricati dall'editore (10 Free RPG Day di Paizo, 12 avventure del Gruppo Chimera);
- i box si riconoscono dal **carattere tipografico** del read-aloud, non dalla posizione: Paizo stampa il testo per i giocatori in un carattere e un colore che il resto del modulo non usa, il Gruppo Chimera in corsivo;
- ogni box esterno viene riscritto nella forma del repo (`> *testo*`, a capo a 76 caratteri come i master) e passa per **gli stessi** `box_read_aloud`, `corpo_del_box`, `frasi_del_box`, `difetti_dei_box`, `gerundi_in_coda` e `avverbi_mente` di `scripts/misura_craft.py` (ramo della #246). Il difetto segnalato la prima volta, due tagliatori di frase diversi sui due lati, non c'è più.

Le definizioni che `misura_craft` non ha sono queste, e valgono uguali sui due lati: seconda persona (voi, vi, vostro; you, your), maiuscole non a inizio frase (limite superiore dei nomi propri, perché il registro dei nomi del repo non conosce i nomi di Golarion), il box che chiude con una domanda, e per l'inglese il participio -ing in coda e gli avverbi in -ly con un elenco di esclusioni.

## 1 · Il corpus

| Gruppo | Titoli | Box | Parole | Note |
|---|---:|---:|---:|---|
| Paizo, Free RPG Day 2007-2018 (EN) | 10 | 118 | 7.800 | due in D&D 3.5, otto in PF1e. Sono tutti i moduli gratuiti che la pagina delle risorse di Paizo elenca |
| Gruppo Chimera 2004-2014 (IT) | 12 | 1.644 | 88.000 | sette in 3.5 o PF1e, cinque in 4e o 5e. Su 39 avventure del sito solo queste hanno il PDF scaricabile |
| Repo, ARC-07 DEF su `main` | 5 | 107 | | i box come sono oggi |
| Repo, ARC-07 DEF sulla #249 | 5 | 139 | | il rifacimento in bozza |
| Repo, ARC-08 | 14 | 77 | | `ARC08-*.md` e la Cerimonia, senza i file `DEPRECATO`; i box stanno in cinque file |

Si scartano i box sotto le 12 parole e i doppioni (4 nel corpus). Il corpus IT si divide in **descrittivo** (1.022 box) e **dialogo** (622, il box comincia con una virgoletta o è per metà fra virgolette): il Gruppo Chimera mette in corsivo tutto quello che si legge ai giocatori, comprese le battute dei PNG.

Sul corpus EN il bersaglio di 300 box non si raggiunge, e non per la rete: Paizo non distribuisce altro di gratuito, Dragons' Lair vuole l'accesso, Raging Swan Press non risponde più, DriveThruRPG è fuori dai domini consentiti. L'italiano invece è venti volte il primo campione.

### 1.1 · Il controllo a mano [misurato]

Un campione a caso (seme 18) di 20 box EN e 30 IT, letti per intero:

- **EN**: 20 su 20 sono testo per i giocatori, nessun confine sbagliato. Uno è l'introduzione dell'avventura e non il box di un'area.
- **IT**: 28 su 30 sono testo per i giocatori. I due dubbi sono una voce della tabella delle dicerie e un'informazione da DM stampata in corsivo. **4 su 30 hanno il confine sbagliato**: sono pezzi di un box spezzato da un cambio di pagina o da una riga in tondo, e lo script li riunisce solo quando il pezzo comincia in minuscola.
- Il gerundio in coda della #246, su 15 colpi a caso nel corpus IT: 15 veri.
- I -ly inglesi: 13 falsi su 96, tutti aggettivi (*squealy*, *grisly*, *scaly*). I -ing in coda: 2 aggettivi su 24.

Il confine instabile pesa sulle lunghezze dell'italiano più che sui tassi per mille parole, che non dipendono da dove si taglia il box.

## 2 · Le misure [misurato]

Box descrittivi, che sono quelli confrontabili con i read-aloud del repo. Parole e frasi sono mediane; le colonne con la percentuale sono la quota di box.

| | Paizo EN | Chimera IT | ARC-07 `main` | ARC-07 #249 | ARC-08 |
|---|---:|---:|---:|---:|---:|
| box | 111 | 1.022 | 95 | 134 | 74 |
| parole (IQR) | 52 (33-80) | 41 (27-67) | 71 (55-94) | 52 (42-63) | 66 (54-73) |
| fra 30 e 70 parole | 52% | 46% | 46% | **90%** | 62% |
| oltre 100 parole | 15% | 10% | 22% | 0% | 0% |
| frasi per box | 3 | 2 | 5 | 3 | 3 |
| parole per frase, med · p90 | 18 · 29 | 17 · 33 | 13 · 27 | 14 · 26 | 17 · 29 |
| `>12 righe` (a 76 caratteri) | 4% | 3% | 0% | 0% | 0% |
| `>4 frasi` | 25% | 15% | 58% | 8% | 16% |
| `>500 car` | 23% | 17% | 28% | 0% | 16% |
| con parentesi | 2% | 6% | 7% | 0% | 5% |
| seconda persona | 9% | 25% | 33% | 15% | 19% |
| maiuscole interne per box | 0,95 | 1,79 | 1,76 | 0,66 | 2,93 |
| chiude con una domanda | 2% | 5% | 9% | 19% | 0% |
| coda ‰ (-ing EN, gerundio IT) | 3,5 | 2,2 | 0,0 | 0,0 | 1,7 |
| avverbi ‰ (-ly EN, -mente IT) | 12,6 | 6,0 | 0,4 | 0,15 | 6,2 |

I dialoghi del Gruppo Chimera (622 box) stanno vicini ai descrittivi in lunghezza (40 parole) e hanno frasi più corte (12 parole); gerundio 0,9‰, -mente 5,0‰.

### 2.1 · Quanto variano fra un'avventura e l'altra

I tassi per mille parole cambiano molto da un titolo all'altro, e tre avventure (*L'Aquila e il Drago*, *Mala Tempora Currunt*, *L'importante è partecipare*) fanno il 61% dei box IT. Per titolo, sui dieci titoli IT con più di dieci box:

- **-mente**: da 3,8 a 13,4‰, mediana **5,5**;
- **gerundio in coda**: da 1,0 a 3,1‰, mediana **1,7**;
- **parole per box**: mediana per titolo da 29 a 64.

Sui dieci titoli Paizo: -ly da 7,0 a 19,8‰, -ing in coda da 1,4 a 5,9‰.

## 3 · Che cosa dicono, con la cautela dovuta

1. **La lunghezza.** Il box descrittivo umano ha una mediana di 41 parole in italiano e 52 in inglese. ARC-07 su `main` sta a 71, e un box su cinque supera le 100 parole. Il rifacimento della #249 porta la mediana a 52, dentro la fascia, e nessun box oltre 100.
2. **La #249 è più regolare dei testi umani.** Il 90% dei suoi box sta fra 30 e 70 parole, contro il 46-52% del riferimento; l'IQR è largo 21 parole contro 40-47. Un autore umano alterna box brevi e lunghi. Che la regolarità si senta al tavolo non lo dice questa misura: lo dice il cieco di ADR-0093 [inferenza].
3. **Le frasi**, misurate questa volta con lo stesso tagliatore. Lo scarto della prima misura (11 contro 17-18) si riduce ma resta: ARC-07 scrive a 13-14 parole per frase, il riferimento a 17-18, ARC-08 a 17. La #249 riporta le frasi per box da 5 a 3, come il riferimento.
4. **`>4 frasi` e `>500 car`**, gli indicatori di D1 di PIANO-BOX-DI-LUOGO: il riferimento umano li supera nel 15-25% dei box. La #249 è a 8% e 0%, cioè più stretta degli autori umani misurati.
5. **Gerundio in coda e -mente: lo zero non è umano.** Il riferimento italiano sta a circa 2 gerundi e 6 -mente ogni mille parole; ARC-07, su `main` e sulla #249, a zero o quasi. ARC-08 (1,7 e 6,2) è **dentro** la fascia umana. È lo stesso risultato della prima misura, ora su 88.000 parole invece di 3.500.
6. **L'allarme dei -mente a 5‰** (Blatt, in `misura_craft --stile`) cade sulla mediana umana: la mediana per titolo del Gruppo Chimera è 5,5, e sette titoli su dieci lo superano. Su testo italiano da modulo l'allarme scatta per metà degli autori umani. Blatt misura romanzi inglesi, e la soglia non si trasferisce.
7. **Parentesi**: 2% nei box Paizo, 6% nel Gruppo Chimera. La norma «niente parentesi» è più severa di entrambi i riferimenti; la #249 la rispetta.
8. **La domanda in chiusura** è rara nei testi umani (2-5%) e frequente nella #249 (19%). Qui il repo è diverso apposta: ADR-0014 chiede «Che fate?» in fondo ai box di combattimento. Non è un difetto.
9. **La seconda persona** divide ancora le due scuole: Paizo la usa nel 9% dei box descrittivi, il Gruppo Chimera nel 25%, il repo fra 15 e 33%.

## 4 · I limiti

- **Selezione rovesciata.** I testi misurati sono i gratuiti: moduli introduttivi Paizo, un terzo umoristici (la serie dei goblin), e avventure da torneo di un'associazione italiana. Nessuno dei primi nove titoli della classifica della community è gratuito. Il riferimento descrive la prosa corrente e capace, non «la migliore».
- **Il Gruppo Chimera non è giudicato dalla community** per la prosa: le stelle del sito sono un'autovalutazione degli autori.
- **Cinque titoli IT su dodici sono 4e o 5e.** Per la prosa del box il sistema conta poco [inferenza]; sui soli sette titoli 3.5 e PF1e i -mente per titolo vanno da 3,8 a 13,4‰, la stessa fascia.
- **I confini dei box IT** sono sbagliati in circa un caso su sette (§1.1). Le mediane delle lunghezze IT vanno lette come approssimate di qualche parola; i tassi per mille no.
- **Le maiuscole interne** sono un limite superiore dei nomi propri e non la colonna `>1 nome` di `--box`, che sul corpus esterno darebbe zero perché il registro dei nomi è quello della campagna.
- **La #249 è una bozza** in movimento: i numeri valgono per il suo commit di oggi.

## 5 · Proposte (solo numeri, da decidere)

Nessuna è applicata: il lotto 4 dice che decide il cieco del DM, non il numero.

- In `--stile`, sostituire l'allarme dei -mente a 5‰ con la **fascia del riferimento italiano** (circa 3,8-13,4‰ per titolo, mediana 5,5) e aggiungere quella del gerundio (circa 1,0-3,1‰, mediana 1,7). Fuori fascia, in basso come in alto, è un indizio.
- Accanto a `>4 frasi` e `>500 car`, riportare la **quota del riferimento umano** (15-25% e 17-23%), perché zero non è il bersaglio.
- Se si vuole misurare la regolarità della #249, l'**IQR delle parole per box** è un numero che il riferimento dà (40-47 parole) e che `--box` non stampa.

## 6 · Come si riproduce

Gli script stanno nella cartella privata del progetto (`corpus-prosa/script/`), insieme ai PDF, perché lavorano su testi che il repo non può contenere:

```
python3 -I corpus-prosa/script/estrai.py PDF "font|size|color"     # un box per riga, JSONL
python3 -I corpus-prosa/script/misura_corpus.py --repo <checkout della #246> \
  --box corpus-prosa/grezzi/box-estratti --config corpus-prosa/script/config.tsv \
  --bersaglio "repo-ARC07-DEF-main=<checkout>:07_il Portale Della Forgia Eterna/ARC07-DEF-*.md" \
  --out corpus-prosa/misure-2026-10-18
```

`config.tsv` dice per ogni PDF quale carattere è il read-aloud. Si sceglie guardando i caratteri del PDF, e per i 22 PDF di oggi l'ho scelto a mano.
