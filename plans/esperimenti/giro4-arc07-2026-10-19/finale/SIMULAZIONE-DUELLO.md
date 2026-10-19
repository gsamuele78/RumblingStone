# Simulazione del duello con Skullcrusher — giro 4, 2026-10-19

Domanda del DM: *«è uno scontro epico la versione EL 14 con le wyvern aggiunte,
o finisce in 3 round?»*. Sola lettura: nessun file del repo è stato toccato.
Il master `DEF-4` era in modifica da un altro agente; i numeri sono quelli letti
alle 2026-10-19 (Scena 11, §0-bis, Appendice A.1, A.1-bis, A.6, mappa M7-B).

## 1. La risposta in tre righe

1. **Non finisce in 3 round.** Con valori medi dura **8-12 round** se il gruppo
   gioca come la regia suggerisce (A, B) e **6-7** se gioca le mosse migliori
   (C). La fuga a ~100 pf chiede 197 danni, e contro CA 37 in volo il gruppo ne
   fa 25-30 a round: quasi tutti con il blast di Artemis.
2. **Il rischio per i PG c'è, ed è alto.** In A e in B, sul percorso medio, un
   PG muore o resta a terra: Artemis per il veleno delle wyvern e i morsi in
   presa, oppure Hella ghermita e soffiata in bocca. Di passeggiata non si può
   parlare. Il difetto è un altro: Thorik e Tordek colpiscono il drago in quota
   con il 5-15%, e il duello rischia di diventare lungo e a una voce sola.
3. **Raccomandazione: non alzare.** Si resta su A.1 più le 2 wyvern (EL 14 sulla
   carta, 15 al tavolo), le tattiche scritte, e la variante dei 30 m di
   *Ghermire* solo quando il soffio è carico e solo su Thorik o Tordek. Durata
   attesa: **8 round** con un tavolo medio. Il Vecchio (A.1-bis, EL 17) è
   legale, ma porta il duello a 12-16 round e con buona probabilità uccide un
   PG.

## 2. I numeri usati, e quelli che mancano

Ogni numero viene da una fonte del repo. Dove la fonte manca, la riga lo
dice, e per poter simulare uso un'**ipotesi di lavoro** dichiarata. Le
schede vere di Thorik, Hella e Artemis non ci sono: l'unica scheda di un PG nel
repo è il PCGen di Tordek al 12° (`PG/Artefatti/Artefatti-Pg/Tordek/Tordek
Durinheart 12 lvl modificato.pdf`).

### Skullcrusher (A.1) e le wyvern (A.6)

| Voce | Valore | Fonte |
|---|---|---|
| pf · soglia di fuga | 297 · fugge al suo turno a ~100, a meno che nel round prima abbia preso ≥2 colpi | A.1, Scena 11 (D14) |
| CA | **37** con *armatura magica* (33 senza), contatto 10; la runa della Catena **41** | A.1, Scena 11 |
| RI · RD | 21 · 10/magia | A.1 |
| Soffio | linea 30 m, 14d4 = **35**, Riflessi CD 30; aderente: metà al round dopo (17,5) e ricarica 1d4+1 | A.1 |
| Mischia | morso +30 (2d8+10 = 19), 2 artigli +25 (12), 2 ali +25 (9,5), coda +25 (22) | A.1 |
| *Ghermire* · lotta | +40 alla presa, **+20** tenendo con la sola bocca; ogni prova vinta, danno del morso | Scena 11 |
| Iniziativa | +6: in tutti gli scenari agisce prima dei PG | A.1 |
| Wyvern (×2 dal round 2) | 59 pf, CA 18, pungiglione +10 (1d6+4 = 7,5) e veleno Tempra CD 17, 2d6 COS | A.6. Le altre armi naturali della wyvern SRD non sono nel repo: simulo solo il pungiglione, un attacco a round in volo |

Il veleno è la voce che pesa di più. 2d6 COS fanno in media 7 punti, cioè −3 o −4
al modificatore: per un PG di 13° vuol dire **circa −45 pf** in un colpo solo.

### I PG

| PG | pf | CA | Attacco contro il drago | Danno medio | Difese | Fonte, e cosa manca |
|---|---|---|---|---|---|---|
| **Thorik** (Guerriero 13) | **mancante** · ipotesi 155 (145 in P1, poi +2 COS) | **21**: 21 in P1, −1 DES allo Smeraldo, deflessione residua +1. **23** su pietra naturale (Consapevolezza della Pietra, se il DM conta il cortile) | Aegis Fang +22/+17/+12 (BAB 13, FOR 20, +2 arma, +2 morale); lanciata −4 | 14,5 (1d10+2+5+2); *Dragondoom* +2d6 3/giorno | **RD 5/epico e male** (Manto di Pietra e Spirito: il drago e le wyvern non la superano); immune alla paura; lotta +18; Riflessi ~+2 (mancante) | P1, scheda della Corona, scheda di Aegis Fang. Mancano i talenti d'arma: con Arma Focalizzata Superiore l'attacco sale di 2 |
| **Tordek** (Guerriero 4/Monaco 9) | **mancante al 13°** · 99 al 12° (PCGen), ipotesi 106 | **24** a mani nude; con lo scudo pesante +2 diventa 23, e perde Saggezza alla CA **e la raffica** (SRD, monaco) | raffica +19/+19/+14 (PCGen +15/+15/+10, Castigo del Drago +2, morale +2); con l'ascia d'adamantio e lo scudo +19/+14, niente raffica e niente Castigo | 21,5 a mani nude (1d10+5+2+2 e +2d6 Castigo); 14,5 con l'ascia | RD 5/adamantio (Pelle di Scorie, se resta dopo il Dono); Riflessi +11 con **eludere**; lotta +15 (+19 se la Lotta Migliorata del PCGen non è già nel totale) | Il PCGen porta anche i Guanti della Forza dell'Orco nello slot delle mani, che i Bracieri occupano: senza, FOR 18 e −1 a colpire e danni |
| **Hella** (Ranger 1/Druida 12) | 110 | 20 | incantesimi al LI 12 contro RI 21: passano il 60% | *tempesta di ghiaccio* 17,5 → **10,5** atteso; *Rovo Eldritch* 2d6 | Riflessi +8, Tempra +16, RD 3/adamantino, *Scudo del Custode* 1/giorno | `DEF-3` A.1. Quali slot restano dopo Zog'tar non è scritto, e nemmeno se ha preparato *dissolvi magie* |
| **Artemis** (Warlock 13) | **mancante** · ipotesi 75 | **mancante** · ipotesi 20 | blast, contatto a distanza contro CA 10 (~95%), poi RI 21 (LI 13: 65%) | 8d6 = 28 (6d6 più 1d6 fuoco e 1d6 freddo della Doppia Fiamma) → **17,3** atteso | Tempra **mancante** · ipotesi +7: contro CD 17 fallisce una volta su due; lotta ~+9 | state, scheda dell'Anello |
| **Durik** | 102 | 21 | morso +15: contro CA 37 solo col 20 | — | acido **×1,5**; Tempra +11; RD 5/adamantio | `DEF-3` A.1 |

Bonus che valgono per tutti: la **benedizione dei chierici** (+2 morale al colpire
e ai danni, 12 ore dal consiglio, già nei numeri qui sopra) e le Benedizioni della
Sala se il gruppo ha pregato all'ingresso (3 cariche di *Vigore della Forgia* a
testa, 3d8+5 su di sé). La *Luce di Lathander* dell'Anello dà +2 morale, che non
si somma a quello dei chierici; al drago nero toglie 2 al colpire e ai danni.

### Le risorse di stasera, contate davvero

| Risorsa | Quante all'alba | Perché |
|---|---|---|
| *Volare* | **1**, se il gruppo è andato e tornato in volo | 5 pozioni; la regia ne spende 4 per Thorik e Tordek (§1) |
| *Velocità* | da 1 a 3 | 3 pozioni, 5 round l'una; una può essere finita alla tenda |
| Rune di acido 20 | 2 | 70 minuti: attivate al corno, ci sono ancora quando arriva il drago |
| Cure | 5 «di CFC» (24,5), 3 CFG (18,5), 10 bacchette CFL, 12 cariche di *Vigore* | sessione-4, regia «Cosa hanno in mano» |
| Neutralizza veleno | 5 pozioni, 3 pergamene | ferma il danno secondario; il COS perso non torna |

🔴 **Lo scenario A, preso alla lettera, spreca due pozioni.** Il drago arriva 70
round dopo il corno. *Volare* dura 5 minuti (50 round) e *velocità* 5 round:
bevute al corno sono finite prima che il drago compaia. Al corno vanno attivate
solo le rune. *Volare* e *velocità* si bevono all'avvistamento, che con le
campane suonate arriva prima della picchiata. Nella simulazione A le tratto così.

## 3. Ghermire e Fluttuare, per esteso (la sequenza del master)

Il master (Scena 11, «La sequenza») dice questo: in picchiata morde, se colpisce
ghermisce e risale nello stesso movimento; al turno dopo si ferma a 15 m e,
se il soffio è tornato, soffia sugli altri con la preda in bocca, poi la lascia
cadere. Chi è in bocca non ha il TS.

### I conti sul PG ghermito, valori medi

Il morso colpisce Thorik (CA 21) e Tordek (CA 24) col 2 o più: 95%. La presa a +40
contro +18 o +15 riesce sempre. Il danno del morso, 19, perde 5 sulla RD di
entrambi.

| Variante | Round | Thorik | Tordek |
|---|---|---|---|
| **S1 — master, 15 m** | T: morso e presa | 13,3 | 13,3 |
| | T+1: soffio con la preda in bocca, nessun TS | 35 (15 con la runa) | 35 (15 con la runa; **eludere non vale**, perché senza TS non c'è niente da eludere) |
| | T+1: la lascia cadere, 5d6 | 17,5 | 17,5 |
| | T+2: soffio aderente | 17,5 (0 con la runa) | 17,5 (0 con la runa) |
| | **Totale** | **≈ 83** (46 con la runa) | **≈ 83** (46 con la runa) |
| **S2 — la variante dei 30 m** | T: morso e presa, risale di ~10 m con il movimento che resta | 13,3 | 13,3 |
| | T+1: fluttua e sale a metà velocità (22,5 m, SRD *Hover*) fino a ~30 m; soffio sugli altri, la preda senza TS; caduta 10d6 | 35 + 35 | 35 + 35 |
| | T+2: soffio aderente | 17,5 | 17,5 |
| | **Totale** | **≈ 101** (63 con la runa) | **≈ 101** (63 con la runa) |
| S1 o S2 **senza soffio carico** | T+1: un morso in presa per round (lo vince il 62% delle volte contro Thorik, il 74% contro Tordek), poi la caduta | 8,7 a round, poi 17,5 o 35 | 10,4 a round, poi 17,5 o 35 |

Ad aprire la combo è la ricarica. Il soffio aderente del round 1 torna dopo 1d4+1
round, in media al round 4-5: è lì che Ghermire e Fluttuare fanno più paura.
Thorik con 155 pf (ipotesi) regge anche S2 e ne esce a metà. Tordek con 106 esce
da S2 a 5 pf, e la prima *Collina* dei Bracieri scatta da sola già dopo il soffio
(sotto metà pf contro un Enorme).

**S2 è legale.** Il peso non è un problema: FOR 31 dà un carico leggero di
circa 2.400 libbre per una creatura Media (Str 21 × 4, regola SRD sopra FOR 29),
×4 per la taglia Enorme. Il mirror del repo arriva a FOR 20, quindi questo
calcolo va verificato su d20srd.org, *Carrying Capacity*. Un nano con la
corazza pesa circa 250 libbre: carico leggero, nessuna penalità al volo. *Fluttuare*
permette la salita a metà velocità anche con la manovrabilità scarsa. La caduta
è 1d6 ogni 3 m, fino a 20d6. Con un turno di salita in più si arriva a 45 m:
15d6, cioè 52,5 in media, sopra la soglia del danno massiccio (Tempra CD 15).
Gli alleati però hanno un round intero per reagire. Ingoiare intero non c'è
nel drago nero, e qui non compare.

### Le contromosse, e cosa annullano davvero

| Contromossa | Annulla | Non annulla | Con che probabilità |
|---|---|---|---|
| ***Volare* già bevuto** | tutta la caduta (17,5 o 35) | morso, soffio, aderente | certa, se è addosso prima della presa. **Bere in bocca al drago**: l'SRD completo permette di attivare un oggetto magico in lotta, tranne quelli a completamento d'incantesimo (le pergamene). Il mirror del repo non riporta questa regola, quindi va verificata su d20srd.org (*Grapple*) prima di stasera. Se vale, il ghermito beve *volare* o una cura al suo turno |
| **Fuga dalla lotta** (prova di lotta contro +20) | il soffio senza TS, se riesce prima del turno T+1 | la caduta: chi scappa a 15 m senza volare cade lo stesso | Thorik +18: **38%** a tentativo · Tordek +15: **26%** (43% se +19) · Hella +11: 14% · Artemis ~+9: 9%. Per chi non vola, scappare e cadere (≈17,5) costa meno che restare (≈52,5) |
| **Caduta morbida** | la caduta | — | **nessuno ce l'ha**: non è fra gli acquisti, e non è un incantesimo del druido. *Caduta lenta* di Tordek vale solo con un muro a portata di braccio, al 9° livello da monaco: −12 m, cioè 15 m diventano 3 (1d6) e 30 m diventano 18 (6d6). Sopra il centro del cortile non c'è muro |
| **Runa d'acido addosso** | 20 del soffio, e tutto l'aderente | morso, caduta | certa, se attivata al corno sul PG giusto |
| **Scudo del Custode** (Hella, 1/giorno, immediata) | metà del soffio, che Hella prende su di sé | il resto | solo entro 9 m: con la preda a 15-30 m serve che Hella voli (forma d'aquila). Non si usa se Hella è colta alla sprovvista (round di sorpresa) |
| **Ombra di Mask** (Artemis, 1/giorno: *invisibilità superiore* su sé e su un alleato) | metà dei morsi, e con loro le prese | il soffio, che è un'area | solo se il drago non ha *vedere invisibilità* addosso. Dura 50 minuti, e il master lo fa lanciare al primo allarme: va prima tolto con *dissolvi magie* |
| Colpire il drago | niente sulla presa | — | nessuna regola gli fa lasciare la preda per un colpo subito |

## 4. Scenario A — il gruppo prepara bene (regia)

Rune al corno su Artemis e Hella. Campane suonate: niente round di sorpresa.
*Velocità* all'avvistamento per Tordek; Thorik prende l'accelerazione dall'Eco
del Custode. Schieramento di M7-B, con Artemis in Q16 e Hella con Durik in
T16-U16: è la linea più fitta.

| Round | Cosa fa il drago (e le wyvern) | Danno subito dai PG | Cosa fa il gruppo | Danno al drago | pf drago |
|---|---|---|---|---|---|
| 1 | Presenza (Tordek scosso 40%). Soffio aderente sulla linea Artemis-Hella-Durik | Artemis 15 · Hella 6 (prende lo *Scudo* per Durik: 26, −20 di runa) · Durik 0 | Artemis blast 17 · Hella *tempesta di ghiaccio* 10,5 · Thorik lancia Aegis 3 · Tordek beve *velocità* | 31 | 266 |
| 2 | Picchiata su Artemis, che lo ha ferito di più: morso e presa, risale a 15 m. La corda scatta (27%, manca). Wyvern 1 su Artemis, wyvern 2 su Thorik alla corda | Artemis 19 + 16,5 (pungiglione e veleno, valore atteso) · Thorik 4,6 | Artemis beve una CFC in bocca (+24,5, se la regola regge) · Hella 10,5 · Thorik 3 · Tordek sulla wyvern 2: 45 | 13,5 | 252 |
| 3 | Fluttua a 15 m con Artemis; soffio scarico, quindi morde in presa (91%) | Artemis 17,3 + 16,5 · Thorik 4,6 | Artemis beve un'altra cura · Hella 10,5 · Thorik e Tordek finiscono la wyvern 2 | 10,5 | 241 |
| 4 | Soffio carico: Artemis in bocca senza TS, poi la linea su Hella, Durik e Thorik. Lascia Artemis, che apre le ali | Artemis 15 · Hella 15 · Durik 52,5 (danno massiccio: 15% che torni polvere) · Thorik 35 · wyvern 1 su Artemis 16,5 | Artemis 17 · Hella 10,5 | 27,5 | 214 |
| 5 | Aderente; nuova picchiata su Artemis | Durik 26 · Thorik 17,5 · **Artemis a terra** (morso 19 su ~9 pf rimasti), in bocca a 15 m | Hella 10,5 · Thorik 3 | 13,5 | 200 |
| 6 | Picchiata su Hella; **la corda tiene** (terzo tentativo, al 27% l'uno) | Hella 16 | Hella 10,5 · Thorik 3 | 13,5 | 187 |
| 7 | Round inchiodato, attacco completo su Thorik (RD 5 su ogni colpo) | Thorik ~50 | attacchi completi con fiancheggiamento: Thorik 10, Tordek 13 (la *velocità* è finita), Hella 10,5, Durik 1 | 35 | 152 |
| 8-11 | Riprende quota; morsi in presa su Hella, wyvern 1 sulla corda | ~20 a round su Hella e Thorik, curati con *Vigore* e bacchette | Hella 10,5 · Thorik 3 | 13,5 a round | 98 al round 11 |
| 12 | Sotto ⅓ al suo turno: **fugge** (FERITO GRAVE) | | | | ~98 |

**Esito A: 12 round, FERITO GRAVE.** Artemis è a terra al round 5. Se il drago
lo lascia cadere da 15 m (5d6) è **morto**, perché la soglia SRD è −10. Durik ha
il 15% di tornare polvere al round 4. Il percorso medio conta il veleno come
valore atteso; nella metà dei tavoli in cui Artemis supera i due TS sulla
Tempra resta in piedi a ~30 pf, il blast continua e il drago fugge al **round
8**.

## 5. Scenario B — colto a metà

Zog'tar è morto in modo spettacolare, le campane tacciono, nessuno sente la
picchiata: il drago ha il round di sorpresa e il gruppo è colto alla
sprovvista. Le rune non sono attive, nessuno ha bevuto *velocità*.

| Round | Cosa fa il drago (e le wyvern) | Danno subito dai PG | Cosa fa il gruppo | Danno al drago | pf drago |
|---|---|---|---|---|---|
| S | Soffio aderente lungo la riga 16: Thorik, Tordek, Artemis, Hella. Lo *Scudo* è un'azione immediata e da colti alla sprovvista non si usa | Thorik 35 · Tordek 31,5 (eludere al 10%) · Artemis 35 · Hella 35 | — | 0 | 297 |
| 1 | Aderente. Nessuno ha ancora un nome, quindi decide l'arroganza: picchiata su Hella, «la druida tornata dalla morte», morso e presa | Thorik 17,5 · Tordek 15,8 · Artemis 17,5 · Hella 17,5 + 16 | Artemis beve una CFC (era a 22,5) · Tordek *velocità* · Thorik attiva la runa su di sé · Hella prova a liberarsi (14%) | 0 | 297 |
| 2 | Fluttua a 15 m con Hella e la morde in presa (86%). Arrivano le wyvern | Hella 13,8 · Artemis 16,5 · Thorik 4,6 | Artemis 17 · Thorik 3 · Tordek alla gru · Hella prova a liberarsi | 20 | 277 |
| 3 | Morde ancora Hella | Hella 13,8 · Artemis 16,5 | Artemis si cura · Tordek, accelerato, sulla wyvern 2: 45 · Thorik 3 | 3 | 274 |
| 4 | **Soffio carico con Hella in bocca**, sulla linea Thorik-Tordek. Poi la lascia cadere | Hella 35 senza TS + 17,5 di caduta → **morta** (−14,5) · Thorik 15 (runa) · Tordek 31,5 | Artemis 17 · Thorik 3 | 20 | 254 |
| 5-13 | Picchiate su Artemis e sulla corda; una corda va a segno verso il round 8 | ~25 a round, ripartiti | Artemis 17 a round, un round inchiodato da ~45 | ~20 a round | ~100 al round 13 |

**Esito B: 13-14 round, FERITO GRAVE, Hella morta sul percorso medio.** Il punto
è la presa che dura tre round con il 14% di fuga a tentativo: la probabilità
che Hella esca prima del soffio è del 36%. Con *volare* bevuto in presa (se la
regola regge) la caduta sparisce e Hella sopravvive a 14 pf. È il caso che il
DM deve guardare per primo: nel round 1 dello scenario B è proprio la regola
d'arroganza a mandare il drago sulla druida appena risorta.

## 6. Scenario C — le mosse più furbe

Campane suonate. Schieramento largo, perché la linea non ne prenda più di due.
Rune su Artemis e su Durik, che ha il +50%. Hella ha preparato ***dissolvi
magie*** (druida 4°, nessuna RI: SRD) e prende dall'Anello il *Dono
dell'Unità*, un'azione standard in più. Artemis apre con *Ombra di Mask* su sé e
su Tordek. L'unico *volare* va a Tordek, che beve anche *velocità*. Thorik,
accelerato dall'Eco, si occupa delle wyvern e della corda.

| Round | Cosa fa il drago (e le wyvern) | Danno subito dai PG | Cosa fa il gruppo | Danno al drago | pf drago |
|---|---|---|---|---|---|
| 1 | Soffio aderente: prende solo Artemis e Durik | Artemis 15 · Durik 32,5, e lo *Scudo* lo passa a Hella dimezzato: Hella 16, Durik 0 | Hella *dissolvi magie*: via l'*armatura magica* (75%) e *vedere invisibilità* → **CA 33** · col Dono anche *tempesta di ghiaccio* 10,5 · Artemis blast 17 · Thorik lancia Aegis contro CA 33: 7,5 · Tordek *velocità* | 35 | 262 |
| 2 | Picchiata su Artemis, invisibile: il morso manca il 50% | Artemis 9 · wyvern 1 su Artemis 8,3 · wyvern 2 su Thorik 4,6 | Artemis 9 (ghermito una volta su due) · Hella 10,5 · Tordek beve *volare* e sale, un attacco: 8,6 · Thorik 7,5 | 35,6 | 226 |
| 3 | Fluttua e fa l'attacco completo su Tordek, che gli è accanto in volo | Tordek ~40 (RD 5 su ogni colpo) | **Raffica accelerata di Tordek contro CA 33: 34** · Artemis 17 · Hella 10,5 · Thorik uccide la wyvern 2 (52) | 61,5 | 164 |
| 4 | Soffio sulla linea Tordek-Artemis | Tordek 30 → a 36, **la Collina scatta** · Artemis 15 | Tordek 34 · Artemis 17 · Hella 10,5 | 61,5 | 103 |
| 5 | A 103 resta. Attacco completo su Tordek | Tordek: aderente 15 e attacco 40 → **a terra** (−19) | Artemis 17 · Hella 10,5 · Thorik 7,5: sotto ⅓, ma ha preso più di due colpi | 35 | 68 |
| 6 | Resta un round ancora (D14) | ~30 su Artemis o Hella | Artemis 17 · Hella 10,5 · Thorik 7,5 | 35 | 33 |
| 7 | **Fugge** (FERITO GRAVE) | | | | 33 |

**Esito C: 6-7 round, FERITO GRAVE vicinissimo all'UCCISO.** Tordek va a terra al
round 5 (e Hella o Durik lo rialzano: *Vigore* a un alleato, 2d8+2). Le tre leve
che accorciano il duello sono *dissolvi magie* (−4 CA, e l'invisibilità torna
utile), Tordek in volo accanto al drago fermo, e Thorik sulle wyvern. Senza la
prima (Hella non l'ha preparata, o la prova fallisce) C torna a **9 round**.

**La scorciatoia della Catena.** Dopo *dissolvi magie* la runa sta a CA 37 invece
di 41. Thorik accelerato ci arriva col 35% a colpo, se è entro 9 m del drago
(volando, o nel round inchiodato): un colpo la spezza e il drago se ne va. Con
la runa a CA 41 la stessa mossa riesce solo col 20 naturale. È la sola strada
che chiude in **3-4 round**, e ci arriva soltanto un tavolo che ha sentito Balvar.

## 7. Perché non dura 3 round, e dove sta l'epica

- **Il conto del tempo.** Per farlo fuggire servono 197 danni. Con il drago in
  quota il gruppo ne fa 25-35 a round: 17 Artemis, 10 Hella, 3-7 Thorik con
  l'ascia lanciata. Tordek fa zero finché non vola o non tiene la corda. Il
  round inchiodato vale 35-65.
- **Il drago non può essere ucciso «presto»** se non con la Catena o con un
  colpo di fortuna. Questo protegge l'esito FERITO GRAVE, che il master dichiara
  il più probabile, e lo conferma: è l'esito in tutti e tre gli scenari.
- **Il pericolo non è il soffio**, che le rune e lo *Scudo* addomesticano. È la
  presa (morsi senza TS, soffio senza TS, caduta) e il veleno delle wyvern sul PG
  che vola. Il gruppo lo sente fin dal round 2.
- **I momenti di scelta ci sono tutti**: la corda (27% a picchiata), lo *Scudo*
  su chi, la runa su chi, la Catena, le wyvern, il re se nessuno chiama il drago,
  e chi beve *volare*. Uno solo è debole: in A e in B Thorik e Tordek passano i
  round in quota ad aspettare la corda.

## 8. Le opzioni dentro il tetto EL ≤ APL+4 = 17

| Opzione | EL | Round attesi (tavolo medio · furbo) | Rischio per i PG | Cosa fanno i nani |
|---|---|---|---|---|
| **A.1 + 2 wyvern, come scritto** | 14 (15 al tavolo) | 10-12 · 6-7 | un PG a terra o morto sul percorso medio | wyvern e corda |
| A.1 + 2 wyvern + **S2 (30 m) quando il soffio è carico** | come sopra | 9-11 · 6-7 | come sopra, con un picco da ~100 sul ghermito | come sopra |
| A.1 + 4 wyvern | ~15 | 10-12 · 7 | più alto: il veleno è il colpo più pesante del duello | più bersagli che colpiscono (CA 18) |
| **A.1-bis, il Vecchio** + 2 wyvern | 17 | 14-16 · 9-10 | molto alto: CA 40, 337 pf con fuga a ~112, soffio 16d4 CD 31, *dissolvi magie* e *lentezza* da stregone di 7° che tolgono *volare*, *velocità* e le rune | quasi niente: Thorik colpisce la CA 40 solo col 20 naturale |

🟠 **Il GS del Vecchio non torna fra la richiesta e il master.** La richiesta dice
«A.1-bis, GS 16, che con le wyvern fa EL 17»; il master (A.1-bis) dice **GS 17**
(Vecchio GS 16 più 1 per il template Avanzato). Con le due wyvern, che pesano
meno di mezzo punto, l'EL resta **17**: è il tetto esatto, quindi l'opzione è
legale in entrambe le letture. Il master però la riserva al gruppo di 14° (D60).

## 9. Raccomandazione

**Si gioca A.1 più le 2 wyvern, come scritto, con la variante S2 (30 m)
riservata ai round in cui il soffio è carico e il ghermito è Thorik o Tordek.
Durata attesa: 8 round con un tavolo medio (6-7 se il tavolo è furbo, fino a 12
se Artemis cade presto).**

È già la versione che fa paura: la presa con il soffio in bocca è la mossa più
terrificante del duello, e con S2 arriva a ~100 pf su un nano solo. Alzare il
drago al Vecchio non aggiunge paura, aggiunge round: i due nani diventano
spettatori, e il rischio di perdere un PG sale da probabile a quasi certo.
Restringere S2 a Thorik e Tordek ha un motivo preciso: sono gli unici due che
reggono ~100 pf. Su Hella o su Artemis la stessa sequenza uccide.

Tre cose da decidere prima della serata, perché cambiano la simulazione più di
qualunque statblocco:

1. 🔴 **Drago che lascia cadere un PG a terra.** La sidebar dice «Un PG
   abbattuto: Skullcrusher lo ignora». Ma se lo ha in bocca a 15 m, ignorarlo
   vuol dire lasciarlo cadere, e 5d6 su un morente sono la morte. Va deciso se
   lo posa o lo lascia.
2. 🟠 **Bere in presa.** Se in bocca al drago si può bere (SRD completo, *Grapple*,
   attivare un oggetto magico), *volare* e le cure tolgono la caduta e allungano
   la vita del ghermito. Il mirror del repo non lo dice: va verificato.
3. 🟠 **Le pozioni del regia, al corno.** *Volare* e *velocità* bevute al corno
   scadono prima che il drago arrivi (70 round). Al corno si attivano solo le
   rune: una riga nella regia lo dice al tavolo prima che lo scopra a sue spese.

Numeri mancanti che spostano i risultati: pf, CA e Tempra di Artemis (decidono
se cade al round 3-5 o regge fino alla fuga), i talenti d'arma di Thorik
(+2 al colpire cambiano il 15% in 25%), gli slot di Hella dopo Zog'tar, e se
ha preparato *dissolvi magie*.
