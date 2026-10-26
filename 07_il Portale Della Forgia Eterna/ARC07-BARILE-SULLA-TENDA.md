# ARC-07 · Il barile sulla tenda di Zog'tar

> **Che cos'è.** Il supplemento alle Scene 7 e 8 di `ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`
> per quello che il tavolo ha fatto davvero: invece di entrare nella tenda del
> comando, i PG ci hanno lasciato cadere sopra, da 48 m e invisibili, una botte
> d'olio piena di sassi, con i rostri dei fabbri nanici sotto e le fiale della
> fenice legate con le corde. Qui ci sono la caduta, dove finisce il barile, i
> danni della caduta, dell'olio e delle palle di fuoco, l'area che coprono, i
> TS e il danno massiccio, le tattiche di chi è dentro e del campo, round per
> round, e i due barilotti da 10 litri che restano in mano ai PG.
>
> **Le mappe** sono M7-C, lo spiazzo del capo con la tenda, e M7-H, il campo
> attorno (`Mappe/`). Le coordinate di questo documento sono quelle di M7-C; su
> M7-H si sommano otto colonne e otto righe.
>
> **Da dove vengono i numeri.** Dall'SRD 3.5. Dove l'SRD non ha una regola per
> quello che è successo, c'è una **variazione**, segnata come tale e costruita
> su una regola dell'SRD vicina; quando le letture possibili sono due, vale la
> più forte, come vuole il DM. Le probabilità vengono da 20.000 prove di
> `plans/esperimenti/barile-zogtar-2026-10-24/simula_barile.py`, che usa
> queste stesse regole: i risultati completi sono in `ESITI-SIMULAZIONE.md`,
> nella stessa cartella.

## In breve, per il tavolo

| Che cosa | Il numero | Da dove |
|---|---|---|
| La caduta | 3,2 secondi, arriva a 30 m/s (110 km/h): finisce nello stesso round dello sgancio | fisica |
| Lo sgancio | **nessun tiro per colpire**: non è un attacco, e l'invisibilità di chi lo lascia cadere resta | SRD, *invisibilità* |
| Dove cade | 1d8 per la direzione, **1d4−1 quadretti** dalla casella scelta | SRD armi a spargimento, con variazione |
| Chi sta nella casella | **15d6** dall'oggetto in caduta, senza TS | SRD, oggetti in caduta |
| La botte e le fiale | si rompono sempre: prendono anche loro i 15d6 della caduta | SRD, danni agli oggetti |
| Le fiale della fenice | due *palle di fuoco* da 6d6 dall'angolo della casella d'impatto, raggio 6 m, **Riflessi CD 14** dimezza | SRD, *palla di fuoco* e CD degli oggetti |
| L'olio | copre **52 quadretti**, quelli entro 6 m dall'impatto: la stessa area della palla di fuoco, che lo accende | SRD, olio, con variazione |
| Chi è nell'olio | nel cuore (3 × 3) colpito in pieno: 1d6 ora e 1d6 il round dopo, e prende fuoco; nel resto 1 danno, poi 1d3 a round e Riflessi CD 15 per non prendere fuoco | SRD, olio e fuoco dell'alchimista |
| Quanto brucia | il cuore 10 round, il resto 2 | SRD, una pinta brucia 2 round, con variazione |
| Danno massiccio | 50 o più da un solo attacco: **Tempra CD 15** o muore; un 1 naturale fallisce sempre | SRD 3.5 |
| Chi cade davvero | Grask quasi sempre se si mira al seggio, il sacerdote una volta su tre; Zog'tar quasi mai (§7) | simulazione |
| Le mura all'alba | allarme e Zog'tar vivo: due successi in meno, uno si può annullare (§10) | canone, Scena 10 |
| Il campo | il boato è l'allarme: ronde in 1d4+2 round, lance della Guardia in 2d4+2, il corno se Grask è vivo | Scena 8 |

## 1. Che cosa hanno fatto, e che cosa si suppone

Il racconto del DM, 2026-10-24, messo in ordine:

- I PG volano sopra il campo, invisibili, a **48 m** di quota, in una notte
  stellata. Partono dalla postierla in volo, come nella variante «dall'alto»
  della Scena 6.
- Lasciano cadere **una botte da 59 litri**: in fondo sassi, sopra **50 litri
  d'olio**, e sotto il fondo i **rostri**, lame forgiate dai fabbri nanici di
  Hammerfist. Alla botte sono legate con le corde le **fiale della fenice**, da
  6d6 con l'effetto di una *palla di fuoco*.
- Tengono in mano **due barilotti da 10 litri**, senza rostri e senza sassi,
  ciascuno con le sue fiale della fenice legate.
- Vogliono squarciare la tenda di Zog'tar.

Quello che il racconto non dice si suppone così, e ogni supposizione è una
domanda al DM in fondo (§12):

- Le fiale sulla botte sono **due**. Le tabelle danno anche una e tre.
- Una fiala della fenice **scoppia quando si rompe**: il vetro che va in pezzi
  è l'innesco, come per un'ampolla di fuoco dell'alchimista.
- Nella tenda c'è la **disposizione A** di M7-C (Scena 7): Zog'tar sul seggio
  che racconta, le quattro guardie attorno, Balvar che incide, il sacerdote
  che dorme, Grask fuori.
- Chi sgancia **sta fermo in aria**. La pozione di *volare* dà manovrabilità
  buona, e con la manovrabilità buona si resta sospesi (SRD, movimento
  aereo).

## 2. La caduta e dove finisce il barile

| | Botte (circa 93 kg, 205 libbre) | Barilotto (circa 14 kg, 31 libbre) |
|---|---|---|
| Quota | 48 m, 157 piedi | 48 m |
| Tempo di caduta | 3,15 s | 3,18 s |
| Velocità all'impatto | 30 m/s, 109 km/h | 29 m/s |
| Energia | 40 kJ | 6 kJ |
| Deriva con 5 m/s di vento laterale | 20 cm | 40 cm |
| Spostamento se chi sgancia vola a 18 m per round | 9,5 m in avanti | 9,5 m |

L'aria quasi non frena una botte così pesante: la velocità finale è il 98%
di quella nel vuoto, e il vento di una notte di pianura la sposta meno di un
quadretto. Contano due cose: se chi sgancia si muove, e quanto si sbaglia a
mirare dall'alto al buio.

**Nessun tiro per colpire.** L'SRD dice che chi è invisibile e «causa danno in
modo indiretto» non attacca: l'esempio è chi taglia le corde di un ponte con i
nemici sopra. Lasciar cadere un barile è lo stesso gesto. Non è un attacco,
quindi non c'è tiro per colpire, l'invisibilità resta, e lasciarlo andare è
un'azione gratuita; chi vuole mirare prima spende un'azione di movimento per
mettersi sulla verticale.

**La deviazione** `[Variazione sull'SRD — INFERRED, needs DM confirmation]`.
L'SRD ha una regola sola per un oggetto che cade dove non si voleva: l'arma a
spargimento che manca. Si tira **1d8 per la direzione** (1 è verso chi lancia,
poi in senso orario; qui chi sgancia sta sopra, quindi 1 è il nord) e la
distanza è di un quadretto per ogni incremento di gittata. Per un oggetto
lasciato cadere l'incremento è la quota: **un quadretto ogni 15 m di caduta**,
contati da zero, quindi da 48 m **1d4−1 quadretti** (da 0 a 3, cioè da 0 a 4,5
m). È lo sbaglio di chi mira a una tenda nera fra i falò da un palazzo di
quindici piani: una volta su quattro il barile cade dove si voleva.

| Che cosa | Dove cade |
|---|---|
| chi sgancia sta fermo in aria | 1d4−1 quadretti in direzione 1d8 dalla casella scelta |
| chi sgancia si è mosso in quel round | in più, la sua velocità divisa per due in quadretti, nella direzione del volo: a 18 m per round sono **6 quadretti** (9 m), e la tenda si manca |
| un barilotto, dalla stessa quota | lo stesso |

## 3. Il telo e il colmo

Il telo di pelle non ferma niente: i rostri lo tagliano come un coltello, e la
botte arriva a terra con la stessa velocità. Il telo si apre in uno squarcio
largo un metro e mezzo.

La riga 12 di M7-C, da J12 a R12, è quella del **colmo**: una trave sopra i tre
pali, alta 6 m. Se la botte cade su una casella di quella riga, tira d6: con 1 o
2 prende la trave, la spezza, e la tenda crolla subito, come nello stato F di
M7-C (tutti sotto il telo a terra e intralciati, Riflessi CD 15 per uscire, un
tentativo per round). Se cade su un palo (K12, N12, Q12) lo spezza, con lo
stesso effetto `[Regola della casa, costruita sullo stato F di M7-C]`.

La runa della barriera di lame è incisa sul palo centrale, N12. Se il palo si
spezza, la runa si spezza con lui **senza scattare**: scatta solo quando la
attiva Balvar `[INFERRED — needs DM confirmation: la versione più terribile è
che scatti da sola, 13d6 lungo la riga 12 su chiunque ci sia, guardie
comprese]`.

## 4. La botte e le fiale toccano terra

Nell'SRD un oggetto che cade prende anche lui il danno della caduta, 1d6 ogni
3 m, e la durezza lo riduce. La botte e le fiale cadono da 48 m: **15d6**, in
media 52.

| Che cosa | Durezza e pf (SRD) | Che fine fa |
|---|---|---|
| La botte, doghe di quercia e cerchi di ferro | durezza 5, 10 pf, come una porta di legno semplice `[INFERRED]` | si apre sempre: anche il minimo, 15, passa la durezza e i punti ferita |
| Le fiale della fenice, legate alle doghe | vetro: durezza 1, 1 pf | si rompono sempre, nella casella dell'impatto, e scoppiano insieme |
| I barilotti | durezza 5, 5 pf `[INFERRED]` | si aprono sempre |

I sassi tengono il fondo in basso, quindi la botte cade dritta, sui rostri, e
i rostri la piantano nel terreno: non rotola. Che il barile non scoppi o che
una fiala resti intera non succede con le regole dell'SRD: la versione di
prima, con il d20 per la tenuta, è tolta.

## 5. I danni

### Il colpo diretto: l'oggetto in caduta

Chi sta nella casella dove cade la botte prende il danno di un **oggetto in
caduta** (SRD 3.5, «Falling Objects»): un oggetto da 200 libbre in su fa 1d6
ogni 200 libbre, più 1d6 per ogni 3 m di caduta oltre i primi, fino a 20d6. Da
48 m sono **15d6**, in media 52. L'SRD non dà un TS e non chiede un tiro per
colpire: lo prende chi sta sotto. La riduzione del danno conta (Zog'tar ha RD
3/—). I rostri non aggiungono dadi: fanno sì che il danno sia tagliente e che
la botte passi il telo.

Una creatura sola prende il colpo diretto, quella della casella. Per Zog'tar,
che è Grande, basta una delle sue quattro caselle.

> **Il peso sta sul filo.** Botte di quercia da 59 litri con i cerchi di ferro
> 14-16 kg, olio 45,5 kg, sassi 15-24 kg (al massimo i 9 litri che l'olio
> lascia liberi), rostri 4-6 kg, fiale e corde 2 kg: da **80 a 93 kg**. Dalle
> 200 libbre (91 kg) in su l'SRD dà 15d6; sotto, nella fascia da 101 a 200
> libbre, dà 1d6 ogni 6 m, cioè **7d6**. Con i sassi fino all'orlo la botte
> pesa 93 kg e vale la prima riga: 15d6. La fisica è d'accordo: 40 kJ uccidono
> un uomo, e 7d6 non ucciderebbero una guardia hobgoblin
> `[INFERRED — needs DM confirmation: quanti sassi]`.

### Le palle di fuoco

Ogni fiala rotta è una *palla di fuoco* da 6d6. L'SRD fa partire un'area da un
incrocio della griglia: l'origine è **l'angolo della casella d'impatto** più
vicino al punto mirato (o 1d4, se non si sa). La palla è uno spargimento di
**6 m di raggio, 4 quadretti**: gira attorno agli angoli, passa il telo e lo
brucia, e accende quello che brucia, l'olio, le pelli, la mappa di Hammerfist
sulla tavola. Riflessi **CD 14** dimezza: è la CD dell'SRD per un oggetto con
un incantesimo di 3° livello, 10 + 3 + 1. Due fiale sono due palle di fuoco,
dallo stesso angolo, con due TS e i danni che si sommano. Nessuno nella tenda
ha Eludere.

### L'olio: quanto ne cade e dove

L'SRD dà due regole per l'olio, e qui servono tutte e due.

- **La pinta versata.** Mezzo litro d'olio (una pinta) copre un quadretto, se
  il terreno è liscio; acceso, brucia **2 round** e fa **1d3 da fuoco** a round
  a chi ci sta.
- **L'ampolla lanciata.** Un'ampolla d'olio è un'arma a spargimento, con le
  regole del fuoco dell'alchimista: chi è colpito in pieno prende **1d6**, e
  **1d6 ancora il round dopo**, se non spende un round intero a spegnersi con
  Riflessi CD 15; chi è nel quadretto accanto prende lo **spruzzo, 1 danno**.

La botte ha 50 litri, cioè **105 pinte**. L'impatto le sparge così
`[Variazione sull'SRD — INFERRED, needs DM confirmation]`:

| Zona | Quadretti | Olio | Che cosa fa |
|---|---|---|---|
| **Cuore** | la casella d'impatto e le otto attorno, 3 × 3 | 5 pinte a quadretto, 45 in tutto | chi c'è è **colpito in pieno** come da un'ampolla: 1d6 subito, 1d6 il round dopo. Acceso, ogni quadretto brucia **10 round** |
| **Area** | gli altri quadretti entro 6 m dall'angolo d'origine, 43 | 1 pinta a quadretto, 43 in tutto | chi c'è prende lo **spruzzo**, 1 danno. Acceso, ogni quadretto brucia **2 round** |
| Il resto | | 17 pinte | assorbite dalle pelli per terra, dal telo e da chi è nel cuore |

La variazione è una sola: le pinte nello stesso quadretto si sommano, e ogni
pinta in più fa bruciare il quadretto 2 round in più, non più forte. Il resto
è l'SRD. L'area dell'olio è la stessa della palla di fuoco, 6 m attorno allo
stesso angolo: al tavolo si disegna un cerchio solo.

### L'olio acceso

- **Si accende subito.** La palla di fuoco accende i combustibili nell'area
  (SRD), e l'olio è tutto dentro.
- **Chi sta nell'olio che brucia** prende **1d3 da fuoco** a round (SRD, la
  pinta) e tira **Riflessi CD 15** per non prendere fuoco (SRD, «Catching on
  Fire»: chi è esposto a olio in fiamme).
- **Chi era nel cuore è inzuppato**: prende fuoco **senza TS**
  `[Variazione — la versione più terribile; per l'SRD tira anche lui Riflessi
  CD 15]`.
- **Chi brucia** prende **1d6 a round** finché non riesce Riflessi CD 15;
  rotolarsi a terra dà +4, ma non dentro l'olio, che riaccende. Una palla di
  fuoco da sola non accende i vestiti (SRD: gli effetti istantanei non lo
  fanno); l'olio sì.

### Il fumo e il crollo

- **Fumo**, da subito, sotto il telo: Tempra CD 15, +1 per ogni prova
  precedente, o il round si passa a tossire; due round di fila fanno 1d6 non
  letali. Il fumo dà occultamento (20%) a tutti quelli dentro (SRD, «Smoke
  Effects»).
- **Il telo brucia** dal primo round. Alla fine del round **1d4+1** crolla, se
  non è crollato prima per il colmo: chi è ancora sotto prende 2d6 da fuoco, è
  intralciato e tira Riflessi CD 15 per uscire, un tentativo per round, con 1d6
  da fuoco a ogni round sotto il telo che brucia `[Regola della casa, costruita
  sullo stato F di M7-C]`.
- **La luce**: la tenda che brucia illumina lo spiazzo come un falò grande. Il
  fondo buio di M7-C non c'è più.

### Il danno massiccio

Nel 3.5 chi prende **50 danni o più da un solo attacco** e non è già morto tira
**Tempra CD 15**: se fallisce, muore, quali che siano i suoi punti ferita. Un 1
naturale fallisce sempre, quindi anche Zog'tar, con Tempra +18, ha il 5%.

- Il **colpo diretto** da 15d6 arriva a 50 due volte su tre.
- **Le due palle di fuoco contano come un attacco solo**: si sommano, e la
  somma è quella che conta per i 50 `[Variazione, la versione più terribile —
  INFERRED, needs DM confirmation: per l'SRD ogni palla di fuoco è un attacco a
  sé, e 6d6 non arrivano mai a 50]`. Con due fiale e il TS fallito, la somma
  arriva a 50 una volta su dieci.
- Il colpo diretto, il fuoco e l'olio restano attacchi diversi.

### Le cose

| Che cosa | Che fine fa |
|---|---|
| La mappa di Hammerfist con le croci rosse, sulla tavola a J10 | brucia nel primo round se J10 è nella palla di fuoco; chi la vuole la prende prima |
| La lastra d'ardesia di Balvar | non brucia. La ha in mano, e la porta fuori con sé |
| Il corno di ferro nero, nella custodia al polso di Grask | non brucia. La custodia è di cuoio e ferro, e il glifo resta |
| Le armature delle guardie | niente: l'SRD fa danneggiare gli oggetti indossati solo con un 1 naturale al TS |

## 6. L'area, sulla griglia

Il cerchio da disegnare è uno solo: **6 m dall'angolo d'origine**, 52 quadretti,
dove arrivano la palla di fuoco e l'olio. Dentro, il cuore di 3 × 3.

| Dove cade | Nel cuore (colpiti in pieno dall'olio) | Nell'area (palla di fuoco e spruzzo) | Fuori |
|---|---|---|---|
| **Sul palo centrale, N12**, senza deviazione | Zog'tar con la casella O13, le guardie M13 e N13 | il sacerdote a N14, la guardia M14, e quasi sempre la guardia Q14; Balvar e Grask solo se l'angolo d'origine è quello di sud-est | con gli altri tre angoli, Balvar a R14 e Grask a P16 |
| **Sul seggio, P14**, senza deviazione | Zog'tar e la guardia Q14 | tutti gli altri: le guardie M13, N13 e M14, il sacerdote, Balvar e Grask | nessuno, tranne le guardie del turno dopo |
| **3 quadretti a nord del palo**, sul telo nord (il peggio della deviazione) | nessuno | Zog'tar, M13 e N13 se l'angolo è quello verso sud; con l'altro angolo nessuno | tutti gli altri |

## 7. Che cosa succede, in numeri

Venti mila prove con le regole di questo documento, la disposizione A e due
fiale sulla botte. Il conto va fino alla fine del primo round: sgancio,
scoppio, l'olio che brucia una volta, chi prende fuoco.

| | Mirando al palo centrale (N12) | Mirando al seggio (O13-P14) |
|---|---|---|
| Il barile cade dove si mirava | 25% | 25% |
| Zog'tar colpito in pieno | 6% | 34% |
| Zog'tar, punti ferita alla fine del round 1 (mediana) | 251 su 283 | 246 su 283 |
| Zog'tar morto (danno massiccio) | sotto l'1% | 1% |
| Il sacerdote a terra / morto | 37% / 13% | 37% / 13% |
| Una guardia a terra (ciascuna) | 1-5% | 1-5% |
| Balvar a terra | 0% | 1% |
| Grask morto | 30% | 83% |
| Il colmo spezzato, la tenda giù subito | 14% | 3% |

Con tre fiale il sacerdote muore una volta su due e ogni guardia una volta su
sette; con una sola, il sacerdote resta quasi sempre in piedi. Con la lettura
SRD pura (ogni palla di fuoco è un attacco a sé, l'inzuppato tira il TS) i
numeri cambiano di un punto o due. Se chi sgancia si muove, il barile cade 9 m
più in là e manca la tenda: nessuno è colpito.

**Che cosa vuol dire.** Il barile **non uccide Zog'tar**: 283 punti ferita, RD
3 e Riflessi +9 reggono anche il colpo in pieno. Il suo guadagno sta altrove.
Brucia la tenda, la scena di Balvar e la mappa dell'assalto. Può togliere di
mezzo chi regge la notte dell'orda dietro le quinte: il sacerdote, una volta
su tre, e soprattutto Grask, se si mira al seggio, che è l'unico ad aprire il
corno senza farsi scoppiare il glifo in faccia. E sveglia il campo, che alle
mura costa (§10). Con 50 litri d'olio in una tenda di 100 metri quadri un
giocatore si aspetta una strage, e per Zog'tar questa non è una strage: va
detto al tavolo prima di tirare.

## 8. Le tattiche, round per round

L'iniziativa si tira **dopo** lo scoppio: nella tenda nessuno ha visto arrivare
la botte, quindi il round di sorpresa è tutto dei PG. Ognuno di loro ha
un'azione standard o di movimento, e in quel round si possono lasciare cadere
anche i barilotti (§9).

| Chi | Round 1 | Round 2-3 | Dal round 4 |
|---|---|---|---|
| **Zog'tar** (Iniz +9) | si sveglia nell'Ira Superiore (azione gratuita) e grida *«A ME, CANI! IL CORNO!»*. Esce dal lato più corto, tagliando il telo con l'ascia: attraversare il telo in fiamme è un quadretto di fuoco, 1d6 e Riflessi CD 15 per non prendere fuoco | fuori, nello spiazzo, cerca il nemico e non lo trova: guarda in alto e non vede niente, perché a 48 m la sua scurovisione (18 m) non arriva. Se Grask è morto va al corpo e strappa la custodia: il glifo gli scoppia addosso, 5d8 sonori, Riflessi CD 18, e lui suona lo stesso. Il corno suona al round 3 | nello spiazzo, fra le sue guardie, finché brucia la tenda; quando arrivano le lance li manda a cercare per il campo chi ha portato il fuoco. Se un PG scende sotto i 18 m, lo carica, con i giavellotti se vola fuori portata d'ascia |
| **Le quattro guardie** (Iniz +1) | due prendono il sacerdote, se è vivo, e lo trascinano fuori dalla soglia; due escono dietro Zog'tar e gli si mettono ai fianchi | spengono chi brucia con i mantelli (+4 al TS di chi brucia, un'azione standard ciascuno); poi fanno quadrato attorno al generale | come Zog'tar; lanciano giavellotti verso l'alto solo se qualcuno indica un bersaglio, e oltre 45 m un giavellotto non arriva |
| **Il sacerdote** (se è vivo) | si sveglia nel fuoco e striscia fuori | *vedere invisibilità* e guarda il cielo: vede gli invisibili, ma a 48 m è buio e la sua scurovisione si ferma a 18 m, quindi non vede i PG. Poi *benedizione* sulle guardie | cura chi brucia; se vede un PG, *comando* «Cadi!», Volontà CD 13, su chi vola |
| **Balvar** (se è vivo) | esce dal telo est, quello a sinistra, e si spegne. Guarda la botte squarciata e i rostri: lavoro dei fabbri di Hammerfist, lo riconosce al primo sguardo | va da Zog'tar e gli dice due parole: *«Nani. Dall'alto.»* Poi la terza, quella che conta: *«Chiamate il drago.»* Il drago vede al buio e sente chi è invisibile entro 18 m, ed è l'unico nel campo che vola. Se Grask è morto e la custodia è intera, dà a Zog'tar la parola che la apre senza il glifo | si mette con Zog'tar. Il barile è un attacco, quindi Balvar passa alla riga «minacciato, o attaccato» della Scena 7. La trattativa non si apre più da sola: vedi §10 |
| **Grask** | se è vivo, sveglio o no, il boato lo sveglia: suona il corno entro **1d4 round**, come al primo grido di Zog'tar (Scena 6) | | |
| **Le due guardie del turno dopo** | si svegliano nella loro tenda, a X4–Y5 | arrivano al round 2, armate, e vanno da Zog'tar | con le altre |
| **Il campo** (M7-H) | le sentinelle dei fuochi gridano. I clan degli orchi si svegliano tutti insieme | le ronde d'orchi arrivano dalla via ovest in 1d4+2 round, le lance della Guardia della Mano dalle vie nord e sud in 2d4+2. Finché Zog'tar è in piedi non vanno addosso alla tenda: fanno quadrato nello spiazzo, a una decina di metri dal telo, e portano acqua e pelli bagnate | gli sciamani dei clan, una quindicina, cercano con *vedere invisibilità*; nessuno vede a 48 m. Il campo resta sveglio fino all'alba |
| **Skullcrusher** | | | se il corno ha suonato, arriva **70 round** dopo il primo suono e caccia sopra il campo: vede al buio e sente gli invisibili entro 18 m (Scena 6, «Se il corno suona di notte») |

**Che cosa rischiano i PG.** Finché restano a 48 m, fermi e invisibili, niente:
nessuno nel campo vede così in alto al buio, e chi li sente non sa dove
mirare. Il rischio è il tempo. Le pozioni di *volare* durano 5 minuti, 50
round, e una parte l'hanno già spesa venendo; l'invisibilità comprata dura 3
minuti. Il ritorno in salita costa il doppio (Scena 6). Se restano a guardare la
tenda bruciare, a un certo punto scendono, visibili, in mezzo a un campo
sveglio. E se il corno ha suonato, il drago arriva al round 70: chi riparte
subito è dentro le mura prima di lui.


## 9. I due barilotti da 10 litri

| | Il numero | Da dove |
|---|---|---|
| Peso | circa 14 kg, 31 libbre: 9 kg d'olio, 5 di doghe e cerchi | |
| Dove cade | come la botte: 1d8 per la direzione, 1d4−1 quadretti | §2 |
| Colpo diretto | oggetto in caduta da 31 a 50 libbre: 1d6 ogni 12 m, da 48 m **3d6** | SRD |
| Tenuta | si apre sempre: 15d6 contro durezza 5 e 5 pf | §4 |
| Fiale | una per barilotto `[INFERRED — needs DM confirmation]`: una *palla di fuoco* da 6d6, 6 m di raggio, Riflessi CD 14 | §5 |
| Olio | 21 pinte: il cuore è la sola casella d'impatto (5 pinte, 10 round, colpito in pieno chi c'è), l'area i quadretti entro 3 m dall'angolo d'origine (11, una pinta l'uno, 2 round, lo spruzzo) | §5, con la stessa variazione |

La palla di fuoco del barilotto è grande quanto quella della botte; l'olio
copre un quarto dell'area.

Dove fanno più male, in ordine:

1. **Su Grask, prima che suoni.** Ha 6 pf e Riflessi +1: una palla di fuoco lo
   uccide quasi sempre, e senza Grask il corno resta nella custodia col glifo.
   È l'unico modo di tenere lontano il drago senza scendere. Dal round 1 Grask
   è a P16, o dove è corso: il barilotto deve cadere entro 4 quadretti da lui,
   e con la deviazione una volta su quattro finisce più in là di 2.
2. **Su una via battuta quando arrivano i rinforzi.** Le ronde d'orchi
   arrivano in fila dalla via ovest: gli orchi hanno 5 pf, e una palla di
   fuoco ne ammazza una ronda intera. Le lance della Guardia (guerrieri di 4°,
   30 pf) passano bruciate ma vive.
3. **Su Zog'tar fuori dalla tenda.** Fa poco: 3d6 se lo prende in pieno, 6d6
   di fuoco, e lo trova già in Ira.
4. **Sulla tenda del turno dopo**, a X4–Y5, prima che le due guardie escano.

Un consiglio da dire al tavolo solo se lo chiedono: i barilotti valgono di più
**contro il corno** che contro Zog'tar.

## 10. Che cosa cambia per la storia

- **Balvar.** Se è vivo, è stato attaccato: non tratta più da solo. La
  Diplomazia CD 18 del nipote funziona solo con chi non l'ha minacciato, e
  bruciargli la tenda è una minaccia. Resta la lastra d'ardesia, che porta
  fuori dal fuoco: chi la guarda (Osservare CD 20, da vicino) legge il nome di
  Hald, e chi gli parla del ragazzo per primo lo trova ancora aperto, perché
  quella leva non dipende da come lo si è trattato (Scena 7, «Ricattabile»).
  Se è morto nel fuoco è il caso «ucciso senza ascoltarlo» della Scena 7: la
  lastra resta fra le ceneri della tenda, e qualcuno la trova in ARC-09. La
  Catena sul drago e la sua gemella sul corno restano: le rune incise
  sopravvivono al runaio `[INFERRED — needs DM confirmation]`.
- **Il corno e il drago.** Se Grask muore e nessuno apre la custodia, all'alba
  nessuno chiama il drago, ed è il caso «se rubano o rompono il corno» della
  Scena 6: arriva tardi, a metà mattina, furioso. Se il corno suona di notte,
  vale «se il corno suona di notte»: il duello all'alba si fa senza sorpresa,
  con il drago già in quota.
- **L'assalto dell'alba.** Le mura contano quello che arriva dalla notte
  (Scena 10), e il barile ci porta due righe del canone: il boato è un
  **allarme**, quindi un successo in meno, e Zog'tar quasi sempre è **vivo
  all'alba**, quindi un altro successo in meno, e guida l'assalto. Tutte e due
  valgono anche se la tenda è bruciata. Per bilanciarle propongo di leggere la
  tenda in fiamme come la riga «Zog'tar umiliato davanti alle guardie»: il
  generale tirato fuori dal fuoco davanti ai suoi annulla il successo in meno
  dell'allarme `[INFERRED — needs DM confirmation]`. Se il barile uccide il
  sacerdote, Zog'tar sale sulla breccia senza di lui, come il canone prevede
  già (EL 16, senza Balvar e senza il sacerdote).
- **Hammerfist vede.** Dalle mura le sentinelle vedono la tenda nera prendere
  fuoco a un chilometro, nel mezzo del campo. Re Thorek lo sa prima che i PG
  rientrino.
- **Echo Ledger** (§7 di DEF-4): «la notte del barile», con chi è morto e se il
  corno ha suonato.

## 11. Le mappe

**Perché al tavolo la tenda sembrava enorme.** Il ramo di gruppo
`campaign-group-rumblingstone` e il booklet stampato il 12 ottobre hanno
ancora la vecchia M7-C: un salone da 18 × 16,5 m su un palo solo, con sette
croci di tendine attaccate. Su `main` la tenda è stata rifatta il 21 ottobre
(PR #261) come padiglione a tre pali, 13,5 × 7,5 m di pavimento, ed è quella
del booklet ristampato il 22. Questa PR fa un passo in più, e toglie lo
steccato che la #261 ci aveva messo attorno: orchi e hobgoblin dell'orda sono
un'orda nomade, non una legione.

Il modello è il campo di un capo nomade: l'ordo di un khan mongolo, con la
tenda del capo sola in mezzo e gli anelli di tende attorno; il khalasar di un
khal, senza mura, dove il capo dorme al centro e i suoi fedeli più vicini; il
campo di una banda gota o gallica, raccolta attorno al fuoco del capo e ai
pali dei trofei, con i carri del bottino lasciati dove si sono fermati.

- **M7-C** è lo **spiazzo del capo**: terra battuta senza recinto, larga una
  quarantina di metri, con la tenda sola nel mezzo. Davanti alla soglia il
  fuoco del consiglio, a notte fonda ridotto a brace (luce fioca solo entro 3
  m, così l'avvicinamento della Scena 6 non cambia), e i due pali dei trofei
  con lo stendardo della Mano Rossa; il bottino della valle ammucchiato
  davanti al capo. Sul bordo, staccate l'una dall'altra, le tende dei servi e
  del bottino, senza soldati, e la tenda del turno dopo a 9 m (X4–Y5). La
  tenda, le persone e tutte le coordinate delle scene **non cambiano**.
- **M7-H** è il **campo attorno**, 66 × 60 m. A 20-30 m dal telo le lance della
  Guardia della Mano: quattro tende da otto attorno al fuoco della lancia, a
  gruppi staccati, con 3 m fra il fuoco e i teli; a ovest i clan degli orchi,
  ripari storti attorno al fuoco della banda, con il vuoto fra un clan e
  l'altro; i lupi da guerra ai picchetti, i carri del bottino, il palo degli
  sciamani. Le vie sono solo terra battuta, a raggiera dallo spiazzo, e i
  rinforzi arrivano da lì. Nessuna tenda della Guardia è dentro i 6 m del
  barile.

Le misure vengono dalla ricerca del 21 ottobre sugli accampamenti
(`plans/esperimenti/mappe-campo-2026-10-21/RICERCA-ACCAMPAMENTI.md`, le parti
sui campi mongoli e d'avventura). Le due mappe passano il collaudo senza
errori, con voto di qualità 100 tutte e due.

## 12. Domande al DM

Ogni domanda ha la proposta ★, scelta come la versione più forte quando le
regole lasciano scegliere.

| # | Domanda | ★ Proposta | Le altre |
|---|---|---|---|
| B1 | Quante fiale della fenice ci sono sulla botte, e quante su ciascun barilotto? | due sulla botte, una per barilotto | una o tre sulla botte: §7 dà i numeri |
| B2 | Una fiala della fenice scoppia quando si rompe? Con che CD? | sì, Riflessi CD 14 | CD 15 se è una pozione del re fatta al 6°; o un innesco a miccia, con il 50% di accensione dell'olio dell'SRD |
| B3 | Il colpo diretto della botte: 15d6 o 7d6? | 15d6: con i sassi fino all'orlo pesa più di 200 libbre | 7d6 se la botte pesa meno |
| B4 | La deviazione senza tiro per colpire: 1d8 per la direzione, un quadretto ogni 15 m di caduta (1d4−1 da 48 m) | sì | un quadretto ogni 10 piedi come l'arma a spargimento (fino a 15 quadretti: la tenda si manca quasi sempre); oppure nessuna deviazione da fermi |
| B5 | Le palle di fuoco che scoppiano insieme contano come un attacco solo per il danno massiccio? | sì | no, come nell'SRD: ogni fiala è un attacco |
| B6 | L'olio: cuore di 3 × 3 colpito in pieno (10 round), il resto entro 6 m con lo spruzzo (2 round), l'inzuppato prende fuoco senza TS | sì | l'SRD puro: ogni quadretto brucia 2 round, e anche l'inzuppato tira Riflessi CD 15 |
| B7 | Il palo centrale spezzato fa scattare la barriera di lame? | no, la runa si spezza | sì, 13d6 lungo la riga 12, Riflessi CD 21 |
| B8 | Zog'tar sa la parola della custodia del corno? | no: la sanno Grask e Balvar | sì, e il corno suona al round 2 senza glifo |
| B9 | In che tacca è caduta la botte, e quindi Grask era sveglio? | quella del tavolo: lo stato di Grask si fissa all'arrivo dei PG (Scena 6) | |
| B10 | La Catena del drago sopravvive a Balvar morto? | sì | no: con Balvar morto la Catena si spezza, e il drago è libero e furioso |
| B11 | La tenda bruciata col generale dentro vale come «Zog'tar umiliato davanti alle guardie» sulle mura? | sì: annulla il successo in meno dell'allarme | no: restano i due successi in meno (allarme e Zog'tar vivo) |

## Fonti

- SRD 3.5, «Falling Objects», «Catching on Fire», «Smoke Effects»:
  <https://www.d20srd.org/srd/environment.htm>
- SRD 3.5, olio (la pinta versata, l'ampolla lanciata, la miccia) e fuoco
  dell'alchimista: <https://www.d20srd.org/srd/equipment/goodsAndServices.htm>
- SRD 3.5, armi a spargimento e deviazione:
  <https://www.d20srd.org/srd/combat/specialAttacks.htm>
- SRD 3.5, danni agli oggetti, durezza e punti ferita:
  <https://www.d20srd.org/srd/combat/specialAttacks.htm>
- SRD 3.5, *invisibilità* («causing harm indirectly is not an attack»), *palla
  di fuoco*, aree e incroci della griglia, danno massiccio, CD degli oggetti
  magici: d20srd.org, voci omonime
- La fisica della caduta: `simula_barile.py` nella cartella dell'esperimento;
  densità dell'olio 0,91 kg/l, aria a 870 m 1,12 kg/m³, coefficiente di
  resistenza 0,9.
