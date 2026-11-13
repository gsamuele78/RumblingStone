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

### Lotto 3-bis — i requisiti delle classi di prestigio (2026-11-12)

Una scheda poteva scrivere «Blackguard 10» senza nessun'altra classe e
`verifica_scheda` non diceva nulla: dei requisiti d'ingresso delle classi di
prestigio non c'era un dato. Ora la capacità `creature.prestigio` li porta e
`dmcore.prestigio` li giudica contro il personaggio **prima** del primo livello
della classe, che è quando i requisiti servono. La scheda scrive il personaggio
com'è adesso, quindi ogni giudizio è una condizione necessaria:

- **bonus di attacco base**: quello che danno le altre classi (dalla
  composizione dei dadi vita, quando la scheda la scrive tutta);
- **gradi**: il requisito non supera il massimo che i dadi vita prima
  dell'ingresso permettono (3.5: dadi vita + 3; PF1e: dadi vita), e l'abilità è
  scritta nella scheda con un bonus che quei gradi li regge. Un'abilità di
  Forza o Destrezza scritta con un bonus basso resta un dubbio (la penalità di
  armatura può nascondere i gradi); una non scritta è una violazione;
- **talenti**: per nome. La parentesi («Arma Focalizzata (martello da guerra)»)
  non si giudica. Se la scheda ha un talento che la lettura non conosce, il
  talento mancante è un dubbio e non una violazione;
- **razza** e **allineamento**: quelli scritti nel tipo;
- **livello d'incantesimo**: una delle altre classi lancia incantesimi arcani o
  divini di quel livello, contando lo slot che viene solo dagli incantesimi
  bonus (paladino 8 con Saggezza 14).

**I dati, e quello che non c'è.** `estrai_prestigio.py` scrive due file, solo
nomi e numeri. `sistemi/dnd35/dati/prestigio.toml`: 15 classi dalle sezioni
«Requirements» dell'SRD 3.5 e 478 dai tag `PRE…` di PCGen per i manuali (un
nome dell'SRD vince). `sistemi/pf1e/dati/prestigio.toml`: le 10 classi del Core
dal PRD, con i loro gradi (assassino: Camuffare 2 e Furtività 5, non 4 e 8).
Un requisito che non si riduce a un numero (speciale, divinità, lingua,
regione, «due scuole a scelta») **non si copia**: se ne tiene il conto in
`non_verificati` e la scheda lo porta fra i non verificabili.

| | 3.5 (493 classi) | PF1e (10 classi) |
|---|---|---|
| Requisiti ridotti a un numero | 1.301 (60%) | 26 (70%) |
| Requisiti solo contati (`non_verificati`) | 877 (40%) | 11 (30%) |
| Classi con soli requisiti speciali | 39 | 0 |
| Classi di cui i dati non hanno nessun requisito | 17 | 0 |
| Classi in più manuali con requisiti diversi (`diverge`) | 6 | 0 |

Le 17 classi senza requisiti e le 6 che divergono non danno mai una
violazione: la scheda esce con un dubbio che dice di leggere il manuale.

| | Prima (main f33282c0) | Lotto 3-bis |
|---|---|---|
| Requisiti tolti apposta dalle schede vere, visti da `verifica_scheda` | 0 su 30 | 30 su 30 |
| Requisiti tolti a ogni classe dei dati, visti da `dmcore.prestigio` | non c'era | tutti (test su 503 classi) |
| Violazioni vere trovate nel Bestiario | non misurate | 3 in 2 schede |
| `verifica_scheda Bestiario 0*/` | 54 violazioni in 17 schede, 308 dubbi | 57 in 19, 315 dubbi |

Il banco (`muta_prestigio.py`, `misure-prestigio.json`) è piccolo e va letto
per quello che è: le schede con una classe di prestigio sono 8, tutte nel
Bestiario, e le mutazioni sono 30 (allineamento 5, razza 1, talento 10, abilità
8, livelli 6). Due mutazioni perse al primo giro erano difetti del banco, una
era un difetto vero del controllo (un'abilità di Destrezza non scritta passava
per dubbio) ed è corretta. Il 30 su 30 dice che la lettura di queste 8 schede
regge, non che reggerà su una scheda scritta in un altro modo. Nessun modulo
(`0*/`) ha una classe di prestigio che la lettura riconosca.

Cosa ha trovato, e **non è corretto** (i livelli di un PNG sono del DM): due
schede in un elenco «in attesa» esplicito nel test del cancello.

- `abbathor-blackguard-cr10`: «Blackguard 10» senza altre classi. La guardia
  nera chiede bonus di attacco base +6 e Nascondersi 5 gradi prima del primo
  livello: con zero livelli d'altro non si entra.
- `drow-assassina-lolth-cr10`: Ladro 4 / Assassino 5. Nascondersi e Muoversi
  Silenziosamente a 8 gradi chiedono 5 dadi vita prima dell'ingresso (massimo
  dei gradi 7 al 4° livello).

**Un buco del lotto 1, chiuso.** L'estrattore dei gradi non leggeva
«Spellcraft» (nell'SRD è l'unica abilità col titolo senza `<small>`):
`creature.gradi` aveva 37 abilità su 38 e Sapienza Magica non entrava né nel
massimo né nella somma dei punti. Corretto l'estrattore e rigenerato
`gradi.toml`: nessuna violazione nuova nelle 150 schede.

Limiti dichiarati: i requisiti si giudicano contro tutte le altre classi, non
contro l'ordine vero dei livelli (che la scheda non scrive), quindi un
personaggio con due classi di prestigio può passare anche se la prima è
servita a entrare nella seconda fuori ordine; oltre i 20 dadi vita il bonus di
attacco base non si ricostruisce; le razze si riconoscono in inglese e, in
italiano, solo per le cinque del lessico (elfo, gnomo, halfling, mezzelfo,
nano): le altre restano un dubbio; i 3.5 dei manuali vengono dai tag di PCGen
e non sono riscontrati sul libro. Il rigiudizio delle 7 violazioni di talenti
rimaste dalla #378 resta fuori: aspetta la risposta del DM alla card.

### Lotto 3-ter — l'avanzamento d'incantatore delle classi di prestigio (2026-11-12)

**Contesto.** Il controllo degli incantatori (lotto 3) giudicava una lista dal
livello scritto in testa, o da quello della classe nella riga `tipo:`. Una
classe di prestigio non entrava nel conto: «Chierico 3 / Assassino 2» con una
lista da chierico di 5° passava, e «Chierico 3 / Loremaster 2» senza livello
scritto si giudicava da chierico di 3°, con violazioni false sugli slot.

**Decisione.** I livelli della classe di prestigio che danno «+1 livello di
una classe che si aveva già» stanno nel plugin, in `prestigio.toml`, voce
`avanza` (`tipo`: arcane, divine, both, any o il nome della classe; `livelli`).
Li scrive `estrai_prestigio.py`: dall'SRD 3.5 e dal PRD PF1e la colonna
«Spells per Day» della tabella della classe, dai manuali 3.5 il tag
`ADD:SPELLCASTER` di PCGen, solo nomi e numeri. 201 classi 3.5 su 493 e 6 PF1e
su 10 hanno un avanzamento. `dmcore.prestigio.avanzamento` fa il conto;
`verifica_scheda`, regola nuova `numero.incantesimi.livello_incantatore`:
livello scritto in testa alla lista ≠ livelli della classe + avanzamento è una
violazione; se il livello non è scritto, la lista si giudica da quello che le
classi danno. È un dubbio, non una violazione, quando la classe viene da un
manuale e il plugin non ne ha l'avanzamento, quando due libri divergono, o
quando un'altra classe del personaggio potrebbe prendere quei livelli.

**Misura** (`muta_avanzamento.py`, `misure-avanzamento.json`). Nel Bestiario
una sola scheda ha una classe di prestigio che alza gli incantesimi, quindi il
banco le mette lui: in 6 schede con una lista giudicata, due livelli della
classe diventano due livelli di Loremaster (la lista resta giusta: controllo),
di Assassino o di Cavaliere Mistico (la lista è troppo alta: errore).

| | Prima (main d6c3740e) | Dopo |
|---|---|---|
| Liste troppo alte messe apposta, viste | 0 su 12 | 12 su 12 |
| Liste giuste (controllo) segnate a torto | 0 su 6 | 0 su 6 |
| `verifica_scheda Bestiario 0*/` | 72 violazioni, 321 dubbi | 72 violazioni, 321 dubbi |

**Conseguenze e limiti dichiarati.** Nessuna scheda vera cambia giudizio.
Balvar (chierico 9 / Runecaster 4, lista da chierico di 13°) torna. Il banco è
piccolo (6 schede) e sintetico. Il controllo parte solo se la scheda ha una
riga `tipo:` con la classe e il suo numero e una lista con gli incantesimi fra
asterischi: `underdark-dovil-runecaster-cr7` scrive in prosa «Incantesimi da
Diviner 5» mentre Diviner 5 / Deep Diviner 1 dà 6, e il controllo non lo vede
(trovato a mano, non corretto: lo decide il DM). Per i manuali 3.5 l'assenza
del tag in PCGen non prova che la classe non avanzi: per questo è un dubbio.
Le classi di prestigio con una lista propria (Assassino, Guardia Nera) non
hanno una tabella degli incantesimi nel plugin. Il livello d'incantatore di
paladino e ranger scritto come «LI» (metà del livello) non si confronta.

### Lotto 4 — il numero dei talenti (2026-11-12)

Il generatore sapeva quanti talenti spettano a un personaggio
(`dmcore.talenti.quanti`, dal lotto 3 delle regole complete); il verificatore
no: controllava i prerequisiti di ogni talento, non quanti fossero. Una scheda
con due talenti di troppo passava. Ora `verifica_scheda.numero_talenti` conta:

- **quanti ne spettano**: i generali per dadi vita (3.5: 1 + 1 ogni 3; PF1e: uno
  ai livelli dispari; i dadi vita razziali contano), i talenti bonus delle
  classi (capacità `creature.talenti`), il talento dell'umano. Per il ladro il
  conto è una forbice: una capacità speciale (3.5, dal 10°) o un talento da
  ladro (PF1e) può essere un talento oppure no;
- **quanti ne scrive la scheda**: le voci della riga, tolte quelle che la classe
  concede per nome (Seguire Tracce del ranger, Scrivere Pergamene del mago, i
  due del dominio della Guerra 3.5 se la scheda nomina il dominio) e quelle che
  la scheda **dichiara** fuori dal conto accanto al nome: «(B)» del mostro,
  «(razziale)», «(dominio)», «(difetto)», «(tratto)». Un nome che la lettura non
  conosce è comunque un talento scritto e si conta.

Regola `numero.talenti`: di più è una violazione, di meno pure (uno slot non
speso è un'omissione). Resta un dubbio, mai una violazione, quando il conto non
si può fare: una classe di cui il plugin non ha i talenti bonus (classi di
prestigio e dei manuali 3.5), la composizione dei dadi vita non letta, un
umanoide con più di tre dadi «razziali» e nessuna classe (sono livelli non
letti), prosa finita nella riga dei talenti.

I tre dati nuovi stanno in `talenti_in_piu.toml` dei due plugin (capacità
`creature.costruzione`), scritti a mano
con la fonte: umano +1 (SRD e PRD, «Humans»), dominio della Guerra 3.5,
livelli a cui il ladro può scegliere un talento.

| | Prima (main 74a6cf80) | Lotto 4 |
|---|---|---|
| Un talento in più o in meno messo apposta, visto da `verifica_scheda` | 0 su 127 | 101 su 127 (80%) |
| di cui nelle schede di cui il conto si può fare | 0 su 101 | 101 su 101 |
| nelle schede dove il conto è un dubbio (13 schede) | 0 su 26 | 0 su 26 |
| Schede del Bestiario fuori conto | non misurate | 15 su 73 |
| `verifica_scheda Bestiario 0*/` | 57 violazioni in 19 schede, 315 dubbi | 72 in 33, 321 dubbi |

Banco: `muta_numero_talenti.py`, misure in `misure-numero-talenti.json`. Dieci
mutazioni non entrano nel conto: cadono su una scheda già fuori conto e la
rimettono in regola, non sono un errore messo apposta. Le violazioni salgono da
57 a 72 perché il controllo vede di più: nessuna scheda è stata modificata.

Cosa ha trovato, e **non è corretto**: quale talento togliere, aggiungere o
dichiarare lo sceglie il DM. Quindici schede in un elenco «in attesa» nel test
del cancello:

- **di troppo** (11): `duergar-chierico3-cr4` (4 contro 2), `underdark-cleric-ainin-cr5`
  (4 contro 2: ha i due talenti del dominio della Guerra ma la scheda non nomina
  il dominio), `gnoll-hyenodon-rider-cr4` (3 contro 1), `ogre-skullcrusher-cr5`
  (5 contro 3), `drow-wizard7-cr8`, `duergar-ladro1-cr1`, `duergar-mago3-cr4`,
  `hell-hound-mezzoimmondo-cr4` (Seguire Tracce è il bonus del segugio: va
  scritto «(B)»), `myconid-sovereign-cr7`, `warpriest-tiamat-cr7`,
  `koth-signore-dei-dragoni-cr8` (uno di troppo ciascuna);
- **in meno** (4): `bruto-deforme-sottosuolo-cr11` (4 contro 6),
  `ogre-micelio-sporeborn-cr8`, `lomyn-redtongue-bardo8-cr8` e
  `avarthel-druido-cr9` (uno in meno; gli ultimi due sono umani).

**Le capacità dichiarate.** `verifica_scheda` leggeva 13 capacità dei plugin e
nel manifest ne dichiarava una (`creature.talenti`): lo stesso buco che la #376
ha chiuso per `genera_creatura`, trovato dal thread della documentazione. Ora le
dichiara tutte e 13 (misura: `misura_capacita_verifica_scheda.py`, da 1 su 13 a
13 su 13) e un test boccia una capacità letta e non dichiarata. I due plugin di
prova dichiarano le quattro che mancavano (`bonus.cumulo`, `creature.armi`,
`creature.incantatori`, `creature.prestigio`); nel censimento del plugin non
d20 lo strumento passa da «nessuna» a «in parte».

Limiti dichiarati: i difetti (Arcani Rivelati) e i tratti si accettano solo se
dichiarati, non si verifica che il personaggio li abbia; i talenti bonus dei
mostri del manuale non sono nei dati, si riconoscono solo dal «(B)»; i talenti
epici oltre il 20° non si contano a parte; gli «effetti dei talenti sui
numeri» del piano non sono in questo lotto (`dmcore.talenti.effetti` li calcola
per il generatore, il cancello ne riconosce una parte): restano da misurare.

### Lotto 4, seconda parte — gli effetti dei talenti sulle abilità (2026-11-12)

**Contesto.** Degli effetti dei talenti sui numeri, i conti di scheda
coprivano già pf (Robustezza), tiri salvezza (Tempra Possente, Riflessi
Fulminei, Volontà di Ferro), iniziativa (Iniziativa Migliorata), attacco (Arma
Focalizzata e Superiore, Arma Accurata) e danno (Arma Specializzata, lotto 2).
Restavano le abilità. Il conto dei gradi dava 3 punti di margine a **tutte** le
abilità di una scheda che nominasse, in qualsiasi punto del testo, un talento
d'abilità: «Allerta» alzava il tetto anche di Scalare, e bastava la parola
«agile» o «furtivo» in una frase («attacco furtivo») per avere il margine.

**Decisione.** Il bonus va solo alle abilità che il talento nomina, col suo
numero, e i numeri stanno nel plugin: `sistemi/dnd35/dati/effetti_talenti.toml`
(19 talenti: i quindici da +2 a due abilità e Abilità Focalizzata dell'SRD,
Abilità Focalizzata Epica, i due psionici) e `sistemi/pf1e/dati/effetti_talenti.toml`
(11 talenti del manuale base, col bonus che raddoppia a 10 gradi), generati da
`estrai_effetti_talenti.py` dalla riga «Benefit» delle fonti, solo nomi e
numeri, e letti dalla capacità `creature.gradi`. L'abilità scelta di Abilità
Focalizzata si legge fra parentesi; se manca, il bonus vale per tutte. Un
talento nominato fuori dalla riga dei talenti («Allerta dal famiglio», o una
riga dei talenti che la lettura non trova) vale lo stesso, ma solo sulle sue
abilità. In PF1e si prende il bonus alto quando i dadi vita permettono 10 gradi.

**Misura** (`muta_effetti_talenti.py`, `misure-effetti-talenti.json`): nelle 10
schede del Bestiario che nominano un talento d'abilità, il bonus di ogni abilità
alzato al valore più alto che il conto di prima accettava.

| | Prima (main 813213e4) | Dopo |
|---|---|---|
| Abilità fuori regola messe apposta, viste | 0 su 44 | 44 su 44 |
| Abilità in regola (talento da +3 proprio su quella) segnate a torto | 0 su 2 | 0 su 2 |
| `verifica_scheda Bestiario 0*/` | 72 violazioni, 321 dubbi | 72 violazioni, 321 dubbi |

**Conseguenze e limiti dichiarati.** Nessuna scheda vera cambia giudizio: il
conto dei gradi resta una condizione necessaria con un margine di 4 o più punti
(sinergia, razza), e vede gli errori grossi. Il banco tocca solo 10 schede,
perché solo quelle nominano un talento d'abilità. Il bonus PF1e a 10 gradi si
concede a chi ha 10 dadi vita, senza sapere se i gradi ci sono davvero.
«Furtivo» in «attacco furtivo» conta ancora come il talento Furtivo quando la
riga dei talenti non ne ha (ora solo su Nascondersi e Muoversi Silenziosamente,
prima su tutte). I talenti dei manuali che alzano un'abilità non sono nei dati.
Autoipnosi manca dalle abilità 3.5 del plugin (`gradi.toml`): il bonus di
«Autonomous» su quella non si applica. Gli effetti condizionali (Schivare,
Incantare in Combattimento, Resistenza Fisica) non spostano un numero scritto e
restano fuori. Con questo il lotto 4 del piano è chiuso.

### Lotto 3, coda — i fatti di una scheda in JSON (2026-11-12)

**Contesto.** Il controllo di coerenza della storia (regola S8) deve incrociare
«Tattiche» e «Descrizione» con la scheda: se la prosa fa lanciare un
incantesimo, la scheda deve averlo. Per farlo gli servono i fatti della scheda
con la riga, e li rileggeva per conto suo con espressioni sue.

**Decisione.** `verifica_scheda --fatti` (funzione `fatti`) stampa in JSON, per
file: i talenti (nome scritto, nome canonico, riga), gli incantesimi (nome,
canonico, livello, usi o slot, volte, riga), le capacità speciali (nome, tipo
Str/Sop/Mag, riga) e le righe di inizio e fine di ogni «Tattiche» e
«Descrizione». Non giudica nulla ed esce sempre 0. Usa le capacità che lo
strumento dichiara già (talenti e liste d'incantesimi): il manifest dei plugin
non cambia.

**Misura** (`misure-fatti-scheda.json`, `Bestiario 0*/`): 186 file con almeno
un fatto; 486 talenti canonici su 508; 626 incantesimi canonici su 688; 214
capacità speciali; 265 sezioni «Tattiche» in 111 file; 120 «Descrizione».

**Limiti dichiarati.** I talenti sono quelli della prima riga «Talenti» del
file: in un booklet con più blocchi gli altri non escono. Un incantesimo
scritto in italiano che il dizionario dell'SRD non ha esce con `canonico`
nullo (62 su 688). Fuori da una scheda riconosciuta una riga «1° …» conta solo
se almeno un nome è un incantesimo noto, per non prendere gli elenchi di prosa.
Le capacità speciali senza la sigla fra parentesi non escono.

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
