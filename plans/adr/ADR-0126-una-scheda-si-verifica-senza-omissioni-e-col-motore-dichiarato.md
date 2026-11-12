# ADR-0126 — Una scheda si verifica senza omissioni, senza tolleranza e col motore di gioco dichiarato

**Stato**: proposta (2026-11-12); D-B, D-B-bis, D-B-ter e D-C scelte dal DM il 2026-11-12
**Data**: 2026-11-12
**Decisione-fonte**: il DM (Jfs), 2026-11-12: completare le regole di SRD d20, D&D 3.5 e PF1e «senza omettere nulla», stringere la tolleranza sui bonus («un +4 è un bonus davvero importante»), aggiungere la variante della campagna (il risultato più forte fra SRD → 3.5 → PF1e) con una logica deterministica, poter vincolare il motore di gioco, accettare le forme ibride solo nella variante.
**Rapporti**: prosegue [ADR-0124](ADR-0124-le-regole-si-verificano-in-python-e-l-llm-riceve-regola-e-controesempio.md) (verifica via MCP); applica [ADR-0118](ADR-0118-un-numero-entra-solo-se-la-regola-lo-calcola.md) (il numero più forte vale solo se si ricostruisce) e [ADR-0121](ADR-0121-un-plugin-di-regole-si-misura-contro-la-fonte.md) (un plugin si misura contro la fonte). È un ADR di programma: una sezione per lotto, aggiunta quando il lotto arriva.

## Contesto

Dopo la PR #378 `verifica_scheda` giudica talenti, numeri, gradi e
incantesimi, ma con tre limiti misurati:

- una tolleranza larga sui numeri: un tiro salvezza passava fino a +4 sopra
  l'atteso e un attacco fra −1 e +2. Sul banco degli errori messi apposta un
  tiro salvezza gonfiato di +2 si vedeva 1 volta su 362;
- campi della scheda che nessuna regola guarda (CA nel 3.5, danno, abilità
  totali, RI, RD, sensi, velocità, equipaggiamento, GS, conto dei talenti);
- la cascata delle fonti cablata nel codice: una scheda 3.5 accetta un talento
  PF1e senza che nessuno l'abbia chiesto.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Tolleranza zero, bonus dichiarati e sommati per tipo** (scelta) | ogni punto ha una sorgente scritta; la regola del cumulo è quella dell'SRD; sul banco gli errori visti passano dal 55% al 79% | 22 numeri di 20 schede vere diventano violazioni e vanno chiusi uno per uno |
| Stringere la fascia (per esempio +1) | meno violazioni da decidere | resta una soglia arbitraria; un +1 non dichiarato è comunque un bonus che nessuno ha scelto |
| Tenere la fascia e marcare «sospetto» | nessuna scheda cambia stato | è la situazione di prima con un'etichetta: non verifica niente |
| Il più forte regola per regola | massimizza ogni numero | mescola pezzi di sistemi diversi senza controllo; il DM ha scelto «per elemento intero» |

## Decisione

**D-A. Nessuna tolleranza sui numeri.** Tiri salvezza e attacco devono essere
uguali al conto. Ogni punto sopra la base viene da una sorgente che la scheda
dichiara. `--tolleranza` (e `severo=False` nelle funzioni) rimette la fascia
di prima, per confronto. I pf restano nella fascia dei dadi, che è una regola
e non una tolleranza.

**D-B. La variante della campagna sceglie per elemento intero** (card del DM,
2026-11-12). Classe, talento, incantesimo, oggetto, capacità: si prende la
versione più forte fra SRD → 3.5 → PF1e dell'elemento intero, mai un numero
dell'una dentro il testo dell'altra.

**D-B-bis. Il motore di gioco si dichiara e si può vincolare.** Un solo
parametro `motore` per il costruttore e per il verificatore, con quattro
valori: `srd35` (solo SRD), `dnd35` (SRD e manuali 3.5), `pf1e`,
`rumblingstone` (la variante D-B). Con un motore vincolato un elemento di un
altro sistema è una violazione `motore.fuori`. Il valore predefinito resta il
sistema dichiarato dal file.

**D-B-ter. Le forme ibride sono lecite solo nella variante, e solo se
registrate.** Una scheda che mescola regole di sistemi diversi passa col
motore `rumblingstone` se l'ibrida è nel registro delle regole custom del DM
(elemento, sistema d'origine, sistema della scheda, fonte, data). Il
verificatore controlla che l'elemento sia legale nel suo sistema e coerente
col resto della scheda. Non registrata è `ibrida.non_dichiarata`.

**D-C. Ogni campo scritto ha un esito** (card del DM: «tutto ciò che una
scheda può scrivere»). Per ogni campo del recinto e della prosa meccanica
l'uscita dice verificato, violazione o non verificabile col motivo.
Descrizione e tattiche restano al verificatore della storia (ADR-0125), che
riceve da qui talenti, incantesimi e capacità per controllarne la coerenza.

**D-D. Due fonti per ogni dato fuori SRD.** Dove due fonti divergono la voce
resta non verificabile finché un libro non la decide. Dalle fonti non OGL
entrano solo nomi e numeri.

## Lotti

### Lotto 1 — cumulo dei bonus per tipo (2026-11-12)

- `sistemi/d20/dati/bonus.toml`, capacità `bonus.cumulo` della famiglia d20:
  i tipi di bonus, quali si sommano (schivare, circostanza, razziale, senza
  tipo: SRD 3.5, «Bonus Types»), le parole che fanno di un bonus un bonus a
  condizione, e 16 sorgenti con la loro fonte (mantello e veste della
  resistenza, veste dell'arcimago, pietra della buona fortuna, veste delle
  stelle, prisma verde pallido, i sei talenti dei tiri salvezza, Fortuna degli
  Eroi, Anima Forte, il bonus razziale dell'halfling).
- `dmcore.bonus`: `somma` (per tipo), `dichiarati` (sorgenti note più le
  dichiarazioni esplicite nella riga dei tiri salvezza, «+1 fortuna a tutti»),
  `totali`. `lettura_creatura.talenti` lo usa: il lettore resta uno.
- `conformita_statblocchi.verifica(severo=True)` e `verifica_scheda` senza
  tolleranza; i tiri salvezza condivisi col padrone (cavalcatura, famiglio) non
  si giudicano verso l'alto.
- Ogni violazione di tiro salvezza o attacco elenca i bonus contati.

Misura (banco `muta_numeri.py`, stessi errori messi apposta):

| | Prima (#378) | Lotto 1 |
|---|---|---|
| Errori visti | 701 su 1.279 (55%) | 1.007 su 1.279 (79%) |
| Tiri salvezza gonfiati di +2 visti | 1 su 362 | 286 su 362 |
| Violazioni di numero sulle schede vere | 0 (nascoste dalla fascia) | 22 trovate, 0 rimaste |

Le 22 trovate, chiuse nello stesso lotto:

- 6 erano difetti del verificatore sull'attacco (potenziamento in mezzo al
  nome dell'arma, Arma Focalizzata contata anche su un'altra arma, Arma
  Focalizzata Superiore non contata): senza tolleranza si usa il conto fine
  di `attacco_atteso`;
- 2 (Avarthel) erano il talento Anima Forte, ora fra le sorgenti;
- 16 numeri in 14 schede erano tiri salvezza senza sorgente. Scelta del DM
  (card del 2026-11-12): «tenere il numero, dichiarare la sorgente». Undici
  PNG e umanoidi ricevono un *mantello della resistenza* (+1 o +2, SRD), che
  alza anche gli altri tiri salvezza; tre creature fatte in casa (due
  razorfiend, la guardia d'élite dei miconidi) dichiarano un bonus razziale
  alla Volontà, segnato «Non SRD». Ogni scheda porta la nota in fondo.

Restano fuori dal lotto 1, detti: la CA del 3.5, i bonus all'attacco diversi
da potenziamento, perfetta, Arma Focalizzata e prisma; gli oggetti col prezzo;
BAB e lotta delle schede senza composizione leggibile.

## Conseguenze

- Una scheda nuova deve dichiarare da dove viene ogni punto: il generatore
  dovrà scriverlo (lotti 2-5).
- Le violazioni salgono a ogni lotto prima di scendere: è la misura che si
  stringe, non le schede che peggiorano. L'elenco va al DM dopo ogni lotto.
- `verifica_scheda` resta nel canale testing: misura, non cancello.
- Il programma è di dodici lotti (piano in
  `plans/esperimenti/regole-senza-omissioni-2026-11-12/INVENTARIO-E-PIANO.md`);
  i parametri MCP nuovi (`motore`) arrivano coi lotti 11 e 12.

## Da rivedere se

- il registro delle ibride supera qualche decina di voci (serve una regola
  generale);
- una sorgente di bonus dei manuali diverge fra due fonti (D-D);
- il DM vuole un quinto motore (3.0, PF1e solo manuale base).
