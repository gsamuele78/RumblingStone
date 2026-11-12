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

### Lotto 1-bis — CA del 3.5, sensi e CD (2026-11-12)

`verifica_scheda` sul 3.5 non guardava la classe armatura: il cancello dei
moduli la controlla solo per il PF1e. Ora `dmcore.classe_armatura` legge la
parentesi di `ca-dettaglio` e ricostruisce la CA dalle sue voci:

- armature e scudi dalla tabella della capacità `creature.costruzione` (bonus
  base più potenziamento, Destrezza massima, mithral +2 alla Destrezza massima);
- gli altri bonus per tipo, con la stessa regola del cumulo del lotto 1
  (deviazione, naturale, potenziamento dell'armatura naturale, cognitivo, sacro,
  profano, fortuna, morale: vale il più alto; schivare e senza tipo si sommano);
- contatto (senza armatura, scudo e naturale) e sprovvista (senza Destrezza e
  schivare; con schivare prodigioso la Destrezza resta);
- una clausola a condizione («+1 contro i giganti») non entra nel numero.

Nella stessa passata entrano i conti che il cancello dei moduli faceva solo
sui recinti dei master: i sensi dati dalla razza e la CD delle capacità
speciali (10 + metà DV + caratteristica).

| | Prima (main) | Lotto 1-bis |
|---|---|---|
| Errori di CA messi apposta, visti da `verifica_scheda` | 0 su 379 | 377 su 379 |
| Scurovisione tolta a chi la ha, vista | 0 su 25 | 10 su 25 |
| Scarti veri trovati nel Bestiario | non misurati | 21 di CA in 18 schede, 10 di sensi, 0 di CD |
| Scarti rimasti dopo le correzioni | | 0 |

Banco: `plans/esperimenti/regole-senza-omissioni-2026-11-12/muta_ca.py`
(CA +1, CA −2, voce +1 con la somma che torna, contatto +1, sprovvista +1,
scurovisione tolta), misure in `misure-ca.json` accanto.

Cosa è stato corretto, con la regola del DM «il numero più forte, se si
ricostruisce da una scheda legale» (ADR-0118):

- 18 schede: la CA scritta non era la somma delle voci, oppure una voce non
  era quella della tabella. Dove due letture erano legali è rimasta la più
  alta: in 8 schede la CA sale di 1 (tra queste difensore nanico di Dauth,
  sacerdotessa drow, capitano githyanki, comandante del Teschio Nero), nelle
  altre cambia solo il dettaglio. Ogni scheda porta la nota in fondo;
- 10 schede: duergar, nani, gnoll, flind e orchi senza la scurovisione della
  razza nella riga `sensi:`;
- 1 difetto del verificatore: i dadi vita di più classi («12d8+4d10») si
  contavano solo dal primo gruppo, e la CD del soffio di Azarr Kul risultava
  sbagliata. Ora si sommano.

Limiti, detti:

- 28 schede su 145 restano **non verificabili** per la CA: 23 non elencano le
  voci, 4 nominano gli oggetti senza i bonus, 1 ha una voce che il lettore non
  riconosce. Stanno in `non_verificabili`, non fra le violazioni; il generatore
  dovrà scrivere le voci (lotti 2-5);
- 2 errori di sprovvista su 60 non si vedono (bruto deforme, alleato orso del
  druido): la Destrezza è negativa o la scheda non la scrive fra le voci;
- la scurovisione si vede solo per le razze che la tabella conosce (10 su 25):
  i mostri che la hanno per tipo arrivano col lotto dei tipi di creatura;
- gli **oggetti dell'SRD col prezzo** erano previsti qui e non ci sono: vanno
  nel lotto 8 insieme alla ricchezza per livello, perché senza quel tetto il
  prezzo da solo non giudica niente. Le armature salite a +1 e i mantelli del
  lotto 1 vanno ricontati lì;
- il PF1e non cambia: contatto, sprovvista e DMC stanno già nel cancello dei
  moduli.

### Lotto 2 — armi e danno (2026-11-12)

`verifica_scheda` non guardava il danno: né il dado, né il bonus, né il
critico. Ora la capacità `creature.armi` porta la tabella delle armi dell'SRD
(`sistemi/dnd35/dati/armi.toml`, 72 armi, scritto da `estrai_armi.py` da
«Table: Weapons» e dai nomi italiani del lessico) e `dmcore.danno` ricostruisce
il danno di ogni attacco con un'arma della tabella:

- **dado** della tabella portato alla taglia di chi impugna (SRD, «Weapon
  Size»); la taglia viene dalla riga `tipo:` o dalla voce di taglia della CA;
- **bonus**: Forza (una volta e mezza a due mani, metà con la mano secondaria,
  niente per archi e balestre, fino alla Forza per gli archi compositi), più il
  potenziamento dell'arma, più i talenti dichiarati (Arma Specializzata e
  Superiore sull'arma nominata; specialista del martello del chierico nano);
- **critico** della tabella; l'intervallo raddoppia con Critico Migliorato
  sull'arma o con un'arma affilata. Il 20/x2 si può tacere, gli altri no.

Una clausola a condizione («in Ira», «con Attacco Poderoso», «entro 9 m») non
si giudica. Il manuale base del PF1e ha le stesse 72 armi con lo stesso dado e
lo stesso critico (riscontro su PSRD-Data, 72 su 72): il plugin `pf1e` eredita
la capacità, ma la verifica resta sul 3.5 fino al lotto 10.

| | Prima (main) | Lotto 2 |
|---|---|---|
| Errori di danno messi apposta, visti da `verifica_scheda` | 0 su 364 | 336 su 364 (92%) |
| per campo: dado, critico tolto, critico sbagliato | 0 | 95/96, 54/54, 20/20 |
| per campo: bonus +1, bonus −2 | 0 | 80/97, 87/97 |
| Scarti veri trovati (Bestiario e moduli) | non misurati | 17: 15 critici non scritti, 2 bonus |
| Scarti rimasti dopo le correzioni | | 4, tutti di ARC-07, in attesa del DM |

Banco: `plans/esperimenti/regole-senza-omissioni-2026-11-12/muta_danno.py`,
misure in `misure-danno.json` accanto.

Cosa è stato corretto, in 11 schede del Bestiario:

- 12 critici non scritti (stocco 18-20, spada lunga e spadone 19-20, spada
  bastarda, balestre, pugnale): è il numero della tabella;
- il cavaliere githyanki d'élite: mazzafrusto pesante a due mani 1d10+3 →
  1d10+4 (Forza +3 per una volta e mezza), regola del DM «il numero più forte,
  se si ricostruisce» (ADR-0118).

Cosa **non** è stato corretto, e perché. Quattro scarti stanno nel master di
ARC-07 (`ARC07-DEF-4`) e nelle sue copie: toccarlo cambia le impronte dei
booklet della serata e la copia di Balvar che un test tiene uguale al
Bestiario. Restano violazioni nell'uscita di `verifica_scheda` e vanno al DM:

- Zog'tar, giavellotti Grandi 1d8+13: con Forza 30 la regola dà +10; +13 è il
  danno in Ira Superiore (Forza 36) e la riga non lo dice;
- guardie di Zog'tar, spadone 2d6+6 senza critico (19-20);
- Balvar, martello da guerra runico +1 senza critico (x3), nel master e nella
  scheda del Bestiario.

Difetti del verificatore trovati e chiusi lungo la strada: i talenti scritti
nella prosa sotto il recinto, la condizione scritta dopo la parentesi, la
stessa arma ripetuta senza nome, il potenziamento dello scudo che non va al
danno, il dado del colpo senz'armi del monaco.

Limiti, detti:

- **attacchi naturali** (78 righe) e **armi fuori tabella** (19: balista, nerbo,
  raffica, righe senza nome) restano non verificabili: il dado di un morso viene
  dalla creatura (lotto 5), le armi dei manuali arrivano con gli oggetti;
- 28 errori messi apposta su 364 non si vedono: un'arma a una mano senza scudo
  ammette due letture (una mano o due), l'arco composito ammette ogni bonus fino
  alla Forza, il monaco e le schede senza Forza leggibile non si giudicano;
- il danno aggiuntivo (furtivo, elementale, «più veleno») non si giudica;
- Arma Specializzata scritta senza l'arma fra parentesi vale come «forse»: sono
  ammessi il numero con e quello senza;
- i talenti di una scheda con più recinti si cercano dal recinto al successivo:
  una nota di un'altra creatura in quel tratto può ammettere un numero in più.

### Lotto 3 — incantatori: slot, conosciuti, livello e CD (2026-11-12)

`verifica_scheda` controllava che un incantesimo stesse nella lista della
classe, non quanti se ne possono lanciare. Ora la capacità
`creature.incantatori` porta le tabelle delle classi che lanciano (bardo,
chierico, druido, paladino, ranger, stregone, mago, adepto) e `dmcore.magia`
ricostruisce, per ogni lista di cui si leggono classe, livello e
caratteristica:

- **incantesimi al giorno**: la cella della tabella al livello di classe, più
  gli incantesimi bonus della caratteristica (la tabella dei bonus è una
  formula, riscontrata riga per riga dall'estrattore), più lo slot di dominio
  del chierico e quello di scuola del mago specialista. Si giudicano la riga
  «N/N+1/… al giorno» dell'intestazione, la parentesi «(5+1)» di una riga e il
  numero di incantesimi preparati: più degli slot è uno scarto, meno no (una
  scheda può scrivere solo gli incantesimi chiave);
- **incantesimi conosciuti** di bardo e stregone, fissi;
- **livello**: una riga a un livello che la classe non lancia ancora, o che la
  caratteristica non regge (serve 10 + livello);
- **CD**: 10 + livello + modificatore, +1 o +2 se la scheda dichiara
  Incantesimi Focalizzati.

I dati sono due file scritti da `estrai_incantatori.py`, solo numeri:
`sistemi/dnd35/dati/incantatori.toml` dall'SRD 3.5 e
`sistemi/pf1e/dati/incantatori.toml` dal PRD (PSRD-Data, book-cr). Il PF1e non
eredita: bardo e stregone non hanno slot di livello 0 (trucchetti a volontà),
il paladino lancia col Carisma, lo stregone ha i conosciuti di stirpe.

**Forma ibrida dichiarata.** Per il bardo il DM ha scelto la tabella del PF1e
(card del 2026-11-09, `[griglie.bardo]` di `creature.toml`). Una lista di bardo
3.5 che torna con la tabella PF1e non è una violazione: esce fra i non
verificabili con la regola `numero.incantesimi.variante`, perché il lotto 11
la scriva nel registro delle regole custom (D-B-ter). Una lista che non torna
con nessuna delle due tabelle è una violazione.

| | Prima (main 942899b5) | Lotto 3 |
|---|---|---|
| Errori messi apposta negli incantesimi, visti da `verifica_scheda` | 0 su 616 | 376 su 616 (61%) |
| di cui in liste che si leggono (classe, livello, caratteristica) | 0 su 449 | 376 su 449 (84%) |
| per campo: CD +1, CD −1 | 0 | 84/126, 80/126 |
| per campo: slot +1, slot −1, livello | 0 | 58/85, 48/85, 20/29 |
| per campo: un incantesimo in più | 0 | 86/165 |
| Scarti veri trovati (Bestiario e moduli) | non misurati | 40 righe in 9 file |
| `verifica_scheda Bestiario 0*/` | 14 violazioni in 9 schede | 54 in 17 |

Banco: `muta_magia.py`, misure in `misure-magia.json`.

Cosa ha trovato, e **non è corretto**: togliere un incantesimo preparato o
cambiare gli slot di un personaggio è una scelta del DM, e i moduli toccano i
booklet. Quattro schede del Bestiario stanno in un elenco «in attesa» esplicito
nel test del cancello:

- `ur-vrax-voce-del-drago-cr10` (chierico 9, Sag 23): ogni livello dal 1° al 5°
  ha uno slot in più della tabella (7+1 contro 6+1 al 1°);
- `morlin-coalhewer-cr12` (chierico 12, Sag 19): 3° e 4° livello, uno in più;
- `abbathor-cleric11-cr11` (chierico 11, Sag 18): 2° livello, 6+D contro 5+D;
- `lomyn-redtongue-bardo8-cr8`: slot da bardo 3.5 e conosciuti di 1° da bardo
  PF1e (5 contro 4), cioè nessuna delle due tabelle per intero;
- nei moduli: ARC-08 guida del DM (chierico 8, chierico 12, ranger 4 con
  incantesimi di 2°, druido 14) e schede (drago nero «come stregone 7»,
  6/8/8/6 contro 6/7/7/5), ARC-05 stanza runica, l'errata dell'arco
  post-Hammerfist (CD più alte di uno), `villans.md` della Corona (CD da
  Carisma 20 con Carisma 24 scritto).

Limiti, detti:

- 167 errori messi apposta su 616 cadono in liste che **non si leggono**: manca
  la caratteristica o il livello nel blocco (schede a prosa dei moduli), o la
  classe non ha tabella nel plugin (anima prescelta, accordo sublime: manuali,
  lotto 9). Stanno fra i non verificabili, una riga per lista;
- 73 errori in liste lette non si vedono: una CD dentro il margine degli
  Incantesimi Focalizzati (la scuola dell'incantesimo non si guarda ancora), un
  incantesimo in più in una riga che non riempiva gli slot, uno slot in meno
  che porta al numero giusto una riga già sbagliata;
- la verifica dei conosciuti guarda solo l'eccesso;
- oggetti che danno slot (perla del potere, anello della stregoneria) non si
  leggono: una scheda che li conta negli slot esce come violazione, e va
  dichiarata come per i bonus del lotto 1;
- il lotto 3 del piano aveva anche i requisiti delle classi di prestigio e il
  rigiudizio delle 7 violazioni vecchie: vanno in un **lotto 3-bis**, come è
  stato per la CA nel lotto 1.

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
