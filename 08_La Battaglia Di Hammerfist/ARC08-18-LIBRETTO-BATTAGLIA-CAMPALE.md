# Il libretto della battaglia campale

> **Per chi**: i giocatori e il DM, lo stesso libretto per tutti. Si legge
> nella sessione delle regole, prima dell'assedio, e si tiene aperto al tavolo.
> **Dove si usa**: i tre giorni dell'assedio di Hammerfist, giocati con i
> quattro eroi della visione della Corona (`ARC08-15`, handout 0-4).
> **Fonte delle regole**: il sistema canonico di `mass_combat_guide_Dm.md`
> (1d20 + AU contro DU, PFU, morale), con le stesse probabilità, ma con i
> dadi in mano ai giocatori. Perché e come è stato provato:
> [ADR-0096](../plans/adr/ADR-0096-la-battaglia-campale-si-gioca-con-un-libretto.md).
> **Stato**: proposta, provata in simulazione e con due letture a freddo;
> manca la prova al tavolo.

---

## 1. In una pagina

- **Il reparto** è un gruppo di dieci soldati. Ha tre numeri: **AU**
  (quanto colpisce), **DU** (quanto si difende) e **PFU**, i suoi punti ferita.
  Un PFU è un soldato: quando i PFU arrivano a zero, il reparto non c'è più.
- **La schiera** è la tua: il tuo eroe e i suoi due reparti.
- **Il settore** è il pezzo di fortezza che la tua schiera tiene: il
  Cancello, le Mura, la Torre Ovest o la Torre Est.
- **Il round di battaglia** dura un minuto. In un giorno d'assedio ce ne sono
  cinque.
- **I dadi li tirate voi**, anche quelli che dicono quanto vi colpisce
  l'orda. Il DM pesca l'orda, gioca le sue carte, tira i tiri salvezza dei
  reparti nemici e racconta.
- **Una tabella sola** decide tutti i tiri (§3).

Servono due d20 di colore diverso per giocatore: uno **rosso** per
l'attacco, uno **bianco** per la difesa. Un foglio con i quadratini dei PFU
per ogni reparto, e un segnalino per le tacche del settore.

**Chi tiene cosa**, se il gruppo non decide altro:

| Eroe | Settore | Reparti | Fronte |
|---|---|---|---|
| **Borin** | il Cancello | due di Guardia del Cancello | 3 |
| **Thorin** | le Mura | due di veterani | 3 |
| **Dara** | la Torre Ovest | due di balestrieri | 2 |
| **Nala** | la Torre Est | due di veterani | 2 |

Il **fronte** è quanti reparti nemici ti stanno addosso nello stesso
momento.

---

## 2. Il round in quattro passi

**1 · L'orda avanza.** Ogni settore ha il suo **mazzo dell'orda** per il
giorno (§12). Il DM pesca reparti dal mazzo finché davanti al settore ce ne
sono tanti quanti dice il fronte. I reparti nemici feriti restano dove sono,
con i PFU che hanno. Poi il DM gioca una carta, se ne ha una per quel round,
e la racconta.

**2 · Gli ordini.** Ogni giocatore sceglie un **ordine** per ognuno dei suoi
reparti (§4) e un **gesto** per il suo eroe (§5). Decidi tu quale reparto
sta davanti a quale nemico. L'eroe non occupa un posto sul fronte.

**3 · Il lancio.** Prima i rossi, poi i bianchi.

- **Rosso, l'attacco.** Per ogni tuo reparto: d20 + AU contro la DU del
  nemico che ha davanti. L'eroe tira il suo gesto.
- **Bianco, la difesa.** Per ogni reparto nemico **ancora in piedi**: d20 +
  la DU del tuo reparto che ha davanti, contro **22 + AU** del nemico. Un
  nemico distrutto dai rossi non tira. Se i nemici sono più dei tuoi
  reparti, quelli in più li fai cadere tu sul reparto che scegli.

**4 · Il conto.** Si segnano i PFU persi da tutti e due i lati. Un reparto
a zero è distrutto. Poi si guarda la pressione sul settore (§7).

**Il primo giorno** le mura e le torri sono intatte: **+1** al bianco in
tutti i settori. Dal secondo giorno, niente.

---

## 3. La tabella unica

| Il tuo tiro… | Rosso (attacco) | Bianco (difesa) |
|---|---|---|
| arriva al bersaglio o lo supera di 0-4 | il nemico perde **1 PFU** | non perdi niente |
| lo supera di 5-9 | il nemico perde **2 PFU** | non perdi niente |
| lo supera di 10 o più | il nemico perde **3 PFU** | non perdi niente |
| lo manca di 1-5 | niente | perdi **1 PFU** |
| lo manca di 6-10 | niente | perdi **2 PFU** |
| lo manca di 11 o più | niente | perdi **3 PFU** e l'eroe è ferito (§5) |

Il bianco è il tiro d'attacco del nemico rovesciato, con le stesse
probabilità: per questo le sue fasce sono spostate di uno.

---

## 4. Gli ordini

| Ordine | Effetto | Quando conviene |
|---|---|---|
| **Tenere** | niente rosso; **+4** al bianco | un reparto è ridotto male e deve durare |
| **Colpire** | nessun modificatore | quasi sempre |
| **Caricare** | **+2** al rosso, **−2** al bianco | contro gli orchi, o per finire un reparto quasi distrutto |

Ogni reparto ha il suo ordine: uno può tenere mentre l'altro carica.

⚠️ **Tenere sempre perde la battaglia.** Chi non colpisce non toglie PFU
all'orda, e la pressione (§7) apre la breccia. Nelle prove, un gruppo che
tiene sempre chiude i primi due giorni senza brecce meno di una volta su
dieci. Caricare sempre è peggio: alla ritirata non resta quasi nessuno.

---

## 5. Il gesto dell'eroe

Ogni round il tuo eroe fa **una** di queste cose.

- **Combattere.** Tira d20 + il **miglior bonus d'attacco** della sua scheda
  contro la DU di un reparto nemico del tuo settore, e usa la tabella unica.
  Borin e Dara valgono da soli due reparti; Thorin e Nala poco più di uno.
  Dara, con l'arco, può tirare anche contro un reparto di un settore vicino.
- **Comandare.** L'eroe non colpisce: gira fra i suoi, chiama i nomi, tiene
  la linea. **+2** a tutti i dadi, rossi e bianchi, dei suoi reparti per quel
  round.
- **Incantesimo.** Spende un incantesimo di 3° livello o più della sua
  scheda, o un uso di un canto bardico.
  - Un incantesimo d'area che fa danni toglie **1d4+1 PFU** a un reparto
    nemico. Il DM tira il TS del reparto (d20 + 4 contro la CD
    dell'incantesimo): se riesce, i PFU si dimezzano, arrotondando per
    difetto.
  - Una cura di massa ridà **1d4 PFU** a un tuo reparto, fino al suo
    massimo.
  - Un incantesimo o un canto che aiuta tutti (*preghiera*, *eroismo*, il
    canto di Nala) dà **+1** ai dadi dei tuoi reparti per tutto il giorno.
    Due uguali non si sommano.
- **Sfidare.** Solo quando il DM gioca la carta di un comandante nemico
  nel tuo settore (§12). Il duello si gioca sulla mappa con le regole
  normali, quanti round servono, e vale come un round di battaglia: in quel
  round i tuoi reparti tirano senza di te, e il settore non prende tacche.
  Un comandante non muore nell'assedio: sotto metà dei suoi punti ferita
  fugge, ferito. Quando fugge, **+2** al morale della rocca (§6), e la sua
  carta esce dal giorno.

**L'eroe ferito.** Quando un tuo bianco manca di 11 o più, il colpo arriva
anche al tuo eroe: **3d6 danni** veri sulla sua scheda. Un eroe a zero esce
dalla battaglia per il giorno, e i suoi reparti restano senza gesto.

---

## 6. Il morale della rocca

Un numero solo per tutto l'esercito dei nani, da **−5** a **+5**. Parte da
**+1**. Si somma a **tutti** i dadi dei reparti nanici, rossi e bianchi, non
ai gesti degli eroi. I numeri dei reparti in §11 hanno già dentro il morale
di ogni singolo reparto: il morale della rocca si aggiunge.

| Cosa succede | Morale |
|---|---|
| un vostro reparto è distrutto | **−1** |
| un settore cede (breccia) | **−2** |
| un comandante nemico fugge | **+2** |
| un giorno finisce senza brecce | **+1**, la notte |
| carte dell'orda | quello che dice la carta |

A **−5** la rocca è sull'orlo della rotta: il DM può raccontare un reparto
che si sbanda, ma le regole non cambiano.

---

## 7. La pressione e la breccia

L'orda è sette volte più numerosa. Non vince uccidendo: vince spingendo.

- Se in un round la tua schiera, eroe compreso, toglie all'orda **meno di 2
  PFU**, il tuo settore prende **una tacca**.
- Alla **terza tacca** dello stesso giorno, o quando la tua schiera non ha
  più reparti, **il settore cede**: è una breccia, e il morale scende di 2.
- **Il settore caduto.** La tua schiera si ritira sulla seconda linea con
  quello che le resta e per quel giorno non combatte più. Gli altri settori
  vanno avanti come prima. Il giorno dopo la schiera torna al suo posto, con
  i reparti che le sono rimasti.
- Le tacche si azzerano a ogni giorno nuovo.

---

## 8. La notte

Fra un giorno e l'altro: ogni reparto ancora vivo **recupera 1 PFU** (i
feriti leggeri tornano in linea), gli eroi dormono e recuperano incantesimi e
punti ferita come sempre, il morale sale di 1 se il giorno è finito senza
brecce. I reparti distrutti non tornano.

---

## 9. Tre modi di giocare, soli o insieme

Il gruppo sceglie il modo prima di ogni giorno, e ogni giocatore può
cambiarlo per la sua schiera.

| Modo | Cosa giochi | Cosa succede intorno a te |
|---|---|---|
| **A · Solo l'eroe** | il tuo eroe, nei combattimenti sulla mappa che il DM prepara: le scale, il cancello, i comandanti | la battaglia di massa va come la racconta il DM, senza tiri |
| **B · L'eroe alla testa della schiera** (consigliato) | eroe e due reparti, con le regole di questo libretto | |
| **C · Il capitano** | **tre** reparti dello stesso tipo; l'eroe resta dietro la linea a dare gli ordini e non tira | |

Nelle prove i modi B e C hanno quasi la stessa probabilità di fermare la
breccia, ma nel modo C si perdono più reparti: senza un eroe in linea l'orda
logora di più.

**Chi non vuole un pregen.** Non lo si obbliga. Ha due posti, e sceglie lui:

- **il capitano** (modo C): tre reparti suoi e nessuna scheda d'eroe da
  imparare. Il suo pregen resta nelle retrovie e lo muove il DM, senza tiri;
- **l'orda**: gioca contro gli amici. Pesca il mazzo, sceglie dove cadono le
  carte e dà voce a Gorthak e Grimjaw, con il DM accanto che decide i limiti.

Nella Sessione 1, dove la battaglia campale non c'è, il capitano guida la
pattuglia di nani che accompagna gli eroi (prove di gruppo, nessuna scheda),
e chi ha scelto l'orda gioca gli esploratori della Mano Rossa.

**Soli o insieme.** Due o più eroi possono tenere lo stesso settore: ognuno
porta i suoi reparti e il suo gesto, e il fronte si allarga di **un** reparto
nemico per ogni eroe in più. Un settore che resta senza eroi lo tiene un
capitano del re: a fine giorno il DM tira 1d6, e con **1-2** quel settore ha
ceduto.

---

## 10. Un round giocato

**Il Cancello, primo giorno, secondo round.** Borin e due reparti della
Guardia del Cancello (AU 11, DU 22, PFU 12) contro tre reparti pescati dal
mazzo: due di hobgoblin (AU 11, DU 21) e uno d'orchi (AU 8, DU 15). Il
morale della rocca è +1, il primo giorno dà +1 al bianco. Il settore ha una
tacca.

1. **L'orda avanza.** Il fronte è pieno. Il DM gioca i giganti: un macigno
   su un reparto di Borin. È un tiro diretto del DM: d20 = 17, + AU 14 =
   **31**, contro DU 22 + 1 + 1 = **24**: supera di 7, il primo reparto perde
   **2 PFU** (ne restano 10).
2. **Gli ordini.** Il giocatore mette il primo reparto contro il primo
   hobgoblin e il secondo contro il secondo; l'orco resta senza nessuno
   davanti. Tutti e due **Colpire**; Borin **Combattere** sull'orco.
3. **Il lancio.** Rossi: Borin 7 + 21 = **28** contro DU 15, supera di 13,
   l'orco perde **3 PFU** (ne restano 5). Primo reparto 12 + 11 + 1 = **24**
   contro 21, **1 PFU**. Secondo reparto 4 + 12 = **16**, niente.
   Bianchi, uno per nemico in piedi: primo hobgoblin contro il primo reparto,
   14 + 22 + 1 + 1 = **38** contro 22 + 11 = **33**, niente; secondo hobgoblin
   contro il secondo reparto, 6 + 24 = **30** contro 33, manca di 3, **1
   PFU**; l'orco lo fa cadere il giocatore sul primo reparto, 11 + 24 = **35**
   contro 22 + 8 = **30**, niente.
4. **Il conto.** L'orda ha perso 4 PFU, più dei 2 che servono: nessuna
   tacca nuova. La Guardia ha perso 3 PFU in tutto.

Al tavolo, così, un round dura tre o quattro minuti: si tira tutti insieme e
il DM racconta il conto.

---

## 11. I reparti

**I nani.** Il morale di ogni reparto è già dentro i numeri.

| Reparto | AU | DU | PFU |
|---|---|---|---|
| **Guardia del Cancello** (élite) | 11 | 22 | 12 |
| **Veterani** | 10 | 21 | 11 |
| **Balestrieri** | 9 | 18 | 9 |

**L'orda feroce**, quella che il DM usa se non dice altro (§12).

| Reparto | AU | DU | PFU | Nota |
|---|---|---|---|---|
| **Hobgoblin** | 11 | 21 | 10 | il grosso dell'orda |
| **Guerrieri hobgoblin** | 7 | 19 | 11 | lenti, duri da finire |
| **Orchi** | 8 | 15 | 8 | caricano a testa bassa: conviene **Caricare** |
| **Lupi e goblin** | 8 | 18 | 10 | veloci, arrivano dai fianchi |
| **Giganti** (carta) | 14 | — | — | lanciano macigni da lontano; non si attaccano dalle mura |

**Gli eroi.** Bonus d'attacco per **Combattere**, dalle schede del Bestiario:
Borin **+21**, Dara **+19**, Thorin **+14**, Nala **+13**.

---

## 12. Per il DM

**Il mazzo dell'orda.** Ogni giorno, per ogni settore, quattordici reparti
mescolati: sei di hobgoblin, quattro di guerrieri, tre d'orchi, uno di lupi.
Si pesca a caso. Quello che resta nel mazzo a fine giorno non torna.

**La ferocia.** Un numero solo, da dire prima della battaglia, che si somma
ad AU e DU di tutti i reparti dell'orda.

| Orda | AU e DU | Breccia contenuta, gioco attento | Posizioni tenute |
|---|---|---|---|
| **Normale** | −1 rispetto a §11 | pieno 8 volte su 10 | pieno 9 volte su 10 |
| **Feroce** (default) | come in §11 | pieno 7 volte su 10 | pieno 7 volte su 10 |
| **Terrificante** | +1 rispetto a §11 | pieno meno di 5 volte su 10 | pieno meno di 4 volte su 10 |

**Le carte dell'orda.** Una per round al massimo, in un settore a scelta.
Le simulazioni hanno provato i giganti, la breccia del cancello e il soffio;
Gorthak, Grimjaw, la palla di fuoco e il gesto Sfidare sono `[INFERRED]` e si
tarano al primo tavolo.

| Giorno | Carta | Effetto |
|---|---|---|
| 1-2 | **I giganti** | round 2: il DM tira d20 + 14 contro la DU di un reparto (con mura e morale), e usa la tabella del rosso |
| 1-2 | **Gorthak al cancello** | comandante: il Cancello può **Sfidare**. Finché c'è, il fronte del Cancello sale di uno |
| 1-2 | **La palla di fuoco** | 1d4+1 PFU a un reparto; il giocatore tira d20 + 5 contro 16, se riesce dimezza |
| 2 | **La breccia del cancello** | non occupa un round: dall'inizio del giorno il fronte del Cancello sale di uno. Con Gorthak sale di due |
| 2-3 | **Grimjaw e la guardia nera** | comandante: si può **Sfidare** |
| 3 | **Il soffio** | round 2: ogni reparto sulle Mura perde 1d4 PFU |
| 3 | **La ritirata** | non occupa un round: il terzo giorno ha quattro round, poi tutti verso il Cuore della Montagna |

**Cosa si legge nella tabella dei bonus** (`ARC08-10-ESITI-E-CONTINGENZE.md`
§5) alla fine dell'assedio:

| Obiettivo | Pieno | Parziale | Fallito |
|---|---|---|---|
| **Breccia contenuta** (§5.2) | nessuna breccia nei giorni 1 e 2 | una | due o più |
| **Comandanti logorati** (§5.2) | Gorthak e Grimjaw fuggiti feriti | uno dei due | nessuno |
| **Cantitrici protette** (§5.2) | le Mura non cedono il giorno 2 | cedono al round 4 o 5 | cedono entro il round 3 |
| **Posizioni tenute** (§5.3) | alla ritirata restano tre quarti dei reparti o più | da un terzo a tre quarti | meno di un terzo |
| **Re Thorek** ed **evacuazione** (§5.3) | come nel master, nella resistenza al Cuore | | |

Le Cantitrici sono un obiettivo, non una carta: si annunciano all'alba del
secondo giorno. Nel modo A le righe di massa sono **parziali**, e contano solo
i combattimenti sulla mappa.

**La battaglia di prova** (Sessione 0) `[INFERRED]`: un solo giorno, tre
round, orda normale, solo la carta dei giganti, ogni giocatore nel suo
settore. Non ha posta: serve a imparare, e si può rifare finché il tavolo
non tira senza guardare il libretto. Si gioca dopo aver letto §1-§8 insieme,
e la Sessione 1 dell'avvistamento viene dopo.

**Il tempo.** Tre o quattro minuti a round, cinque round a giorno: il
primo e il secondo giorno stanno in una serata con i duelli. Il terzo giorno
dura quattro round e lascia il resto della serata alla resistenza al Cuore.
