<!-- GENERATO da scripts/build_booklet_html.py --format hb (ADR-0013).
     Manifest: ARC07-MILLE-ANNI-VOLUME.manifest.json — i capitoli CITANO i master (ADR-0003).
     Le immagini restano riferimenti relativi al repo: per la resa con
     immagini incorporate usa la via HTML (--format html). -->

{{frontCover}}

{{logo ![](/assets/naturalCritLogoRed.svg)}}

# RUMBLING STONE
## Il Viaggio a Mille Anni fa
___

### Hammerfist ≈372 DR · la notte dell'orda · il duello con Skullcrusher · il Rituale della Forgia Eterna

{{banner VOLUME DEL DM}}

{{footnote
  Avventura D&D 3.5 per 4 personaggi di 13° livello · Faerûn, ≈372 DR (mille anni prima del 1372) · Campagna privata RumblingStone · master ARC07-DEF-4 integrale, cast, statblocchi, mappa, carry-over, handout
}}

\page

# Il viaggio a mille anni fa — il volume

> *Il portale non vi trasporta: vi rifà. Per un istante lunghissimo siete
> scomposti nei vostri mille anni, e quando vi ricomponete dall'altra parte le
> ferite che avevate non ci sono più.*
>
> *C'è odore di calcare appena tagliato. Le mura sono bianche. Su una targa di
> bronzo, alle porte, qualcuno ha inciso il vostro destino stamattina.*

**Cos'è questo volume.** Tutto il beat del viaggio a ≈372 DR in un solo libro,
da stampare o da tenere sul tablet: il master `ARC07-DEF-4` integrale, le
schede del cast, lo statblocco di Balvar, la tabella B4 che porta le ferite del
duello fino a Fauci di Palude, la mappa del cortile a pergamena e l'handout
delle Cronache.

**Sostituisce il Fascicolo V** (`homebrew/ARC07-BOOKLET-FASCICOLO-5-P5-MILLE-ANNI.hb.md`),
un riassunto di luglio che non conosce Balvar, l'orologio della notte, Zeth, il
Rituale 4 e l'Aura della Forgia Eterna: tutto è arrivato dopo, con le
riscritture di settembre. Il fascicolo resta nel repo come storia; al tavolo si
usa questo.

**Come si gioca, in due sessioni** *(decisione S1 del DM, 2026-09-24)*:

| Sessione | Da dove a dove | Nel master |
|---|---|---|
| **2026-09-25**, insieme alla resurrezione | l'arrivo, la targa, Durin, il consiglio di Re Thorek I, la notte con le sue otto tacche, Zeth, Balvar, Zog'tar, Vatore. **Ci si ferma al primo ariete sulle mura** | §3 Scene 1-3, §4-ter, §4-bis, §5 |
| **la successiva** | le mura all'alba, il duello con Skullcrusher, il Rituale della Forgia Eterna, il ritorno | §3 Scene 4-6, §4, §4-quater, §9 → `ARC07-DEF-5` |

La regia minuto per minuto della prima metà sta nel booklet della serata
(`homebrew/sessione-resurrezione-mille-anni/`, capitolo I, Atto IV). Qui c'è il
materiale completo, per entrambe le sessioni.

**Cosa annotare, per la sessione dopo.** Le tacche spese all'uscita dalla tenda,
come è morto Zog'tar (in silenzio, in modo spettacolare, umiliato), se
qualcuno ha letto la runa sulla scaglia del drago, cosa hanno promesso a
Balvar, e l'esito con Vatore. Decidono come comincia il duello.

**Cosa è stato corretto nel master il 2026-09-24**, per allinearlo al canone
giocato dopo la sua ultima riscrittura:

- i «3 semi di treant» da piantare la notte: dopo il rito stanno nella
  Collana. All'alba Hella evoca **due Treant di Adamantio** (Scena 1-bis);
- il **Marchio di Varis** era scritto come probabile: nel canone giocato **non è
  attivo**, e la risonanza con Vatore non scatta (§1, Artemis);
- **Durik** entra nel viaggio e nel duello, con la sua vulnerabilità all'acido
  (§1, e una battuta nella regia dei round di §4);
- il **dono a metà** di `DEF-3` §9 si incassa qui, al primo uso (§1, Hella);
- l'immagine del portale era la foto di un testo (§9).

**Quattro contraddizioni, decise dal DM il 2026-09-24** e già scritte nei
file che le contenevano:

| | Cosa dicevano i file | Cosa vale adesso |
|---|---|---|
| 1 | **Chi ha perso la Corona.** Re Thorek I diceva *«suo nonno»*, Thorgrim *«mio nonno»* | sono **cugini**, nipoti dello stesso re caduto contro Skullcrusher (`DEF-4` Scena 1-bis, scheda di Thorgrim) |
| 2 | **Frostcleaver.** In mano a Re Thorek I in `DEF-4`, a Thorgrim nell'affresco A3 | è **del re**. Nell'affresco Thorgrim tiene **Aegis Fang**, mille anni fa (`DEF-2` A3, `PortaleForgia-P2`) |
| 3 | **Zeth.** La scheda del Ghostlord diceva ottocento anni fa, un'invasione phaerimm, un lich di epoca Netherese | **mille anni fa, durante l'assedio dell'orda**; il cultista di Shar è la mano del Collezionista. Riallineati il Ghostlord, due file di ARC-09 e il Consiglio di Rethmar |
| 4 | **Balvar.** INT 9 e SAG 18 nella riga generata, INT 16 e SAG 20 nel testo | vale il testo: la riga dello statblocco è stata corretta |

E due dettagli: l'**Occhio di Ossidiana** di Zog'tar è un occhio vero, al posto
dell'occhio destro (statblocco in `DEF-4` §4-bis).

**Come si rigenera**, dalla radice del repo:

- volume completo, schermo e stampa:
  `python3 scripts/dm.py volume "07_il Portale Della Forgia Eterna/homebrew/volume-mille-anni/ARC07-MILLE-ANNI-VOLUME.manifest.json" --stampa`
- solo le pagine ✉, un PDF ciascuna:
  `python3 scripts/dm.py booklet <lo stesso manifest> --pdf`


\page

# I · Il cast di mille anni fa

{{note
##### ⚠ SOLO DM
Questo capitolo è materiale del DM: non mostrarlo ai giocatori.
}}

# Il cast di mille anni fa

> **Come si usa.** Una scheda per ogni PNG e villain di Hammerfist ≈372 DR, in
> ordine di entrata. Ogni scheda ha sei righe fisse: **aspetto** (per
> descriverlo e per il ritratto), **cosa vuole** (e non riguarda i PG), **come
> suona**, **cosa sa e cosa no**, **in scena** (dove stanno i numeri) e
> **l'eco**. Le voci vengono dalla Cassetta del DM e dai master; dove un master
> tace la riga è marcata `[PROPOSTA]`, e la cambi senza chiedere.
>
> ⚠️ **Le statistiche non si copiano qui** (ADR-0021): stanno nel master
> `ARC07-DEF-4`, che è in questo stesso volume, e la riga «in scena» dice dove.
> Una seconda copia diverge alla prima errata.
>
> 🖼 **I ritratti non esistono ancora.** Sotto ogni nome c'è il prompt da
> usare (sezione «Ritratti del cast di mille anni fa» di
> `Immagini/PROMPT-IMMAGINI-07ILP.md`) e il nome del file. Quando il ritratto
> c'è, si sostituisce quella riga con l'immagine e si rilancia `dm.py volume`.

---

## Durin Rocciadura, la pattuglia

*🖼 Ritratto da generare: il prompt **R1** di `Immagini/PROMPT-IMMAGINI-07ILP.md`; salvalo come `Immagini/ritratti/durin-rocciadura.jpg`.*

| | |
|---|---|
| **Aspetto** | veterano, armatura completa e scudo, ascia doppia. Sta davanti ai suoi sei e ha paura. `[PROPOSTA]`: si vede dal modo in cui tiene l'ascia troppo stretta |
| **Vuole** | riportare a casa i suoi sei. Ha paura e fa il suo lavoro lo stesso |
| **Suona** | la voce gli scappa in alto quando è teso. `[PROPOSTA]`: ride un attimo prima di dire una cosa seria |
| **Sa** | il bosco a est delle mura, il campo dell'orda visto da lontano |
| **Non sa** | chi siano i PG, finché non vede la Corona o sente il tuono |
| **In scena** | `DEF-4` §3 Scena 1-bis (i tre modi di farsi riconoscere) · statistiche §4-bis: Guerriero 6, PF 52, CA 22 |
| **Eco** | è l'**antenato di Othrek**, a Hammerfist nel 1372. Se muore alle mura, la Cerimonia delle 100 Asce può portarne il nome |

## Re Thorek I, il re di una fortezza giovane

*🖼 Ritratto da generare: il prompt **R2** di `Immagini/PROMPT-IMMAGINI-07ILP.md`; salvalo come `Immagini/ritratti/re-thorek-i.jpg`.*

| | |
|---|---|
| **Aspetto** | 182 anni, e li porta come un muro porta la pioggia. Armatura di mithral, l'ascia **Frostcleaver** in pugno anche al tavolo di guerra. `[PROPOSTA]`: una corona semplice, senza gemme |
| **Vuole** | reggere le mura fino all'alba. Ottocento nani contro diecimila |
| **Suona** | lento, al passato remoto quando cita la profezia. `[PROPOSTA]`: parla al plurale anche di sé, *«la fortezza pensa»* |
| **Sa** | la profezia, perché l'ha incisa stanotte: gli è venuta in sogno. Che suo nonno perse la Corona contro Skullcrusher. **Thorgrim è suo cugino**: lo stesso nonno |
| **Non sa** | che la profezia parla di questi quattro, finché non vede la Corona |
| **In scena** | `DEF-4` §3 Scena 1-bis, il consiglio di guerra. Guerriero 16; **non combatte** e non ha uno statblocco completo |
| **Eco** | la prova di fiducia (aiuti pieni o dimezzati) e il **Torque di Thorek I** (`DEF-4` §8). Nel 1372 i nani si scoprono il capo davanti a chi lo porta |

⚠️ A voce **Thorek** e **Thorik** si confondono: di' sempre **«Re Thorek»**.

## Thorgrim Barbadiferro, l'antenato

*🖼 Ritratto da generare: il prompt **R3** di `Immagini/PROMPT-IMMAGINI-07ILP.md`; salvalo come `Immagini/ritratti/thorgrim-barbadiferro.jpg`.*

| | |
|---|---|
| **Aspetto** | un vecchio seduto che non si alza. Le mani sulle ginocchia, e il callo nello stesso punto in cui ce l'ha Thorik, perché hanno tenuto la stessa ascia |
| **Vuole** | che l'ascia torni in una mano che sa perché la tiene. È **cugino di Re Thorek I**: il nonno che perse la Corona è lo stesso |
| **Suona** | la voce non trema, gli occhi sì. Nomina il sangue, mai la persona: *«il sangue riconosce il sangue»* |
| **In scena** | `DEF-4` §3 Scena 2, prova sociale **CD 20**. È una **non-creatura**: nessuno statblocco esiste, e non va inventato |
| **Eco** | l'affresco A3 (*«Portala bene, fratello. Ora è tua.»*) e la Cerimonia delle 100 Asce in ARC-08 |

## Mastro Costruttore Zeth, il seme del Ghostlord

*🖼 Ritratto da generare: il prompt **R4** di `Immagini/PROMPT-IMMAGINI-07ILP.md`; salvalo come `Immagini/ritratti/zeth-mastro-costruttore.jpg`.*

| | |
|---|---|
| **Aspetto** | mezz'elfo, occhi febbrili, polvere di roccia fino ai gomiti. Traccia rune sulle pareti dei tunnel. `[PROPOSTA]`: col gesso, e ne cancella metà col pollice |
| **Vuole** | che le gallerie non cedano. È disposto a legarci l'anima |
| **Suona** | parla mentre lavora. `[PROPOSTA]`: finisce le frasi degli altri |
| **Sa** | che un chierico incappucciato gli ha dato «i componenti perfetti» |
| **Non sa** | che quei componenti servono a una **lichificazione**, e che la mano è del **Collezionista** attraverso il tempo |
| **In scena** | `DEF-4` §3 Scena 1-bis, «Seme del Ghostlord». Costa **una tacca** della notte cercarlo |
| **Eco** | il **dilemma di Hella su Zeth il Murato** in ARC-09. I PG assistono all'origine del Ghostlord **senza saperlo** |

## Balvar Fuocospento, il runaio esiliato

*🖼 Ritratto da generare: il prompt **R5** di `Immagini/PROMPT-IMMAGINI-07ILP.md`; salvalo come `Immagini/ritratti/balvar-fuocospento.jpg`.*

| | |
|---|---|
| **Aspetto** | nano dello scudo vecchio, grembiule di cuoio, seduto su uno sgabello da bottega in fondo alla tenda. Sulle ginocchia una lastra d'ardesia, in mano una punta di ferro |
| **Vuole** | che Hammerfist cada **in fretta**, perché un assedio lungo è fame, e lui l'ha già vista. E che qualcuno dica che c'era |
| **Suona** | non smette di incidere mentre parla. La punta sull'ardesia continua sotto le frasi |
| **Sa** | **che i PG non sono di questo secolo**, unico in tutta Hammerfist. Dove vanno colpite le mura. La runa-vincolo sulla scaglia del drago, perché l'ha incisa lui |
| **Non dice** | che ha un nipote di diciannove anni sul camminamento. Mai per primo |
| **In scena** | `DEF-4` §4-ter · statblocco nel capitolo **«Balvar Fuocospento — scheda del Bestiario»** di questo volume |
| **Eco** | *«dite che c'ero»*: se promesso, un pannello in più negli affreschi, e Aegis Fang lo riconosce. Se lo uccidono senza ascoltarlo, una lastra a metà che qualcuno troverà in ARC-09 |

## Zog'tar Deatheye, il generale

*🖼 Ritratto da generare: il prompt **R6** di `Immagini/PROMPT-IMMAGINI-07ILP.md`; salvalo come `Immagini/ritratti/zogtar-deatheye.jpg`.*

| | |
|---|---|
| **Aspetto** | mezzo-ogre, grande quanto una porta di stalla, armatura completa di piastre annerite. L'ascia a due mani appoggiata alla spalla. Al posto di un occhio, una pietra nera levigata: l'**Occhio di Ossidiana** |
| **Vuole** | Hammerfist. Sa uccidere diecimila uomini, non sa dove colpire le mura: per quello c'è Balvar |
| **Suona** | conta, sempre: *«due file», «tre ore», «cento»*. In ira: *«A ME, CANI! ABBATTETE LE OMBRE!»* |
| **Sa** | niente dei PG, a meno che il corridore non arrivi |
| **In scena** | `DEF-4` §4-bis: statblocco, quattro guardie, tattiche round per round, due vie che non passano dall'iniziativa |
| **Eco** | come muore decide come comincia il duello. Se viene **umiliato e non ucciso**, la Mano Rossa ha un generale in più nella sua storia |

L'Occhio di Ossidiana è **un occhio vero**, al posto dell'occhio destro (decisione del DM, 2026-09-24).

## Vatore, il ladro che diventerà Sal

*🖼 Ritratto da generare: il prompt **R7** di `Immagini/PROMPT-IMMAGINI-07ILP.md`; salvalo come `Immagini/ritratti/vatore.jpg`.*

| | |
|---|---|
| **Aspetto** | lo stesso volto di Sal, irriconoscibile nel portamento. Vesti di seta grigia di taglio drow, cappuccio, niente ornamenti. Stringe al petto un fagotto |
| **Vuole** | la stessa cosa che vorrà Sal: potere, e il conto lo pagano altri |
| **Suona** | il tono del collega, non del nemico. Monosillabi. Terrore reverenziale mal nascosto |
| **Sa** | di aver visto quattro persone che non dovrebbero esistere. Che il **Sigillo di Ossidiana** divora anime |
| **Non sa** | niente di Sal. Nessuno al tavolo lo sa |
| **In scena** | `DEF-4` §5: cinque risposte del party, tutte grigie · il Sigillo nello stesso paragrafo · scheda completa di Sal in `Bestiario/villain/Salvatore/` |
| **Eco** | la sincronizzazione su Sal nel 1372: sanguina nello stesso punto, gli manca un asso, li teme, li odia. Qualunque cosa facciano, **sopravvive** |

## Skullcrusher il Nero, il capostipite

*🖼 Ritratto da generare: la scheda **41** di `Immagini/PROMPT-IMMAGINI-07ILP.md`; salvalo come `Immagini/ritratti/skullcrusher-il-nero.jpg`.*

| | |
|---|---|
| **Aspetto** | drago nero adulto, snello e arrogante: collo lungo, cranio stretto e cornuto, scaglie nere opache con un riflesso verde d'olio. L'acido gli cola dalle fauci chiuse |
| **Vuole** | vincere **davanti all'orda**, perché per lui il potere è quello che gli altri hanno visto |
| **Suona** | dice **il nome** dell'avversario prima di colpire, ogni volta |
| **In scena** | `DEF-4` §4: statblocco GS 12, regia dei primi due round, il cortile, i tre esiti. Si gioca nella **sessione dopo** questa serata |
| **Eco** | la tabella B4 (in questo volume): ogni ferita che gli fate, la Forgia la ricorderà contro **Fauci di Palude** nel 1372 |


\page

# II · Master — Il Viaggio a 1.000 anni fa (DEF-4)

{{note
##### ⚠ SOLO DM
Questo capitolo è materiale del DM: non mostrarlo ai giocatori.
}}

# ARC-07 · DEFINITIVO #4 — IL VIAGGIO A 1.000 ANNI FA
## Il Portale della Forgia Eterna — Hammerfist ≈372 DR, il duello con Skullcrusher, il Rubino

> ⭐ **MASTER DEFINITIVO — fast-play cinematografico (D1: una sessione).** Non
> un dungeon completo: una **sessione-leggenda** a montaggio, con **un solo
> scontro tattico** (il duello con Skullcrusher) reso a qualità AP. Benchmark di
> craft: il **Palio di Channathgate** (`09_.../…PALIO-DM-MASTER-REFERENCE.md`)
> — matrice di conseguenze, asse temporale, spotlight per PG.
> **Sostituisce e fonde**: `_ARCHIVIO/PortaleForgia-P5-FASTPLAY.md` (master da tavolo B3),
> `PortaleForgia-P5-DEFINITIVO-PARTE1/2.md` (prosa e dialoghi estesi),
> `PortaleForgia-P5-B4-CARRYOVER-Forgia-Ricorda.md` (il ponte «la Forgia
> ricorda le ferite», valori DM-approved), `Bestiario/villain/Salvatore/Salvatore.md`
> (**Vatore**, Sal a −1000), MAP 7 di `Mappe/_ARCHIVIO/TACTICAL-GRIDS-COMPLETE.md`.
> Deprecati a valle: `P5-RICALIBRATO`, la sezione «battaglia antica» di `P6`.
>
> **Sistema: D&D 3.5 SRD** (max PF1e), MAI 5e. Italiano, **CD** non DC. Il
> viaggio è a **1.000 anni prima ≈372 DR** (D7). Scala mappe **1,5 m/quadretto**.
>
> **Stato al tavolo**: si gioca **dopo** la resurrezione di Hella (master #3):
> il party è di **4 PG** (Hella tornata), **APL 13 pieno**. Alla vittoria il
> **Rubino** si accende e riporta i PG al 1372 → **master #5** (raccordo al
> Cuore della Montagna). **Canone**: la Corona ha Topazio + Smeraldo (aprono il
> portale del Tempo); il **Rubino si accende SOLO alla vittoria antica** (D5/D16).

---

## INDICE DEL MODULO

| § | Sezione | Contenuto |
|---|---|---|
| §0 | **Quickstart DM** | dove siete, la regola di montaggio, cosa stampare, come si chiude |
| §0-bis | **Quick-Reference** | CD delle prove di gruppo, il giro di Skullcrusher, carry-over B4, box PF1e |
| §1 | **Highlight per PG** | il beat di ciascuno dei QUATTRO (Hella è tornata) |
| §2 | **Le Zone di Hammerfist ≈372 DR** | Atlante: fortezza, campo dell'orda, mura all'alba |
| §3 | **Le Scene** (doppia modalità) | Cronache · **arrivo esteso (Durin, Re Thorek, notte, Zeth)** · Infiltrazione+Zog'tar · Mura · Rubino |
| **§4-quater** | **IL RITUALE DELLA FORGIA ETERNA** | **il Rituale Legacy 4: il Rubino entra, la Corona passa a +3, la Senzienza arriva calda o fredda secondo `DEF-3` §5, e Aegis Fang si sveglia allo Stage 1. Dopo il combattimento, senza costi** |
| §4-bis | **Zog'tar & PNG antichi** | statblock+tattiche per [COMBATTIMENTO COMPLETO]: Zog'tar, guardie, Durin |
| **§4-ter** | **BALVAR FUOCOSPENTO** (GS 13) | **il consigliere runaio: sa che i PG vengono dal futuro, e ha incatenato Skullcrusher all'orda** |
| §4 | **BOSS: Skullcrusher il Nero** | statblock, tattiche round-per-round, scaling, «la Forgia ricorda» |
| §5 | **VATORE** | Sal a −1000: la scena grigia + la sincronizzazione temporale (eco su Sal 1372) |
| §6 | **Contingenze & sconfitta** | «Se i PG fanno X»; il paradosso; una sconfitta nel passato |
| §7 | **Echo Ledger** | carry-over B4 (Skullcrusher→Fauci) + Vatore→Sal + tono del Rubino |
| §8 | **Avanzamento** | budget PX per scena + tesoro pregenerato (doni di Re Thorek I) |
| §9 | **Ponte** al master #5 + **Handout & Asset** (le Cronache dei Quattro Eroi) |
| MAPPE | **M7-A campo & fortezza · M7-B arena del duello** | ASCII ultra-clear 1,5 m |

---

## §0 — QUICKSTART DM

**Dove siete.** La Corona (Topazio + Smeraldo) ha aperto il portale del Tempo
(affresco A6). I **quattro** Custodi — Hella di nuovo tra loro — precipitano
attraverso mille anni e atterrano a **Hammerfist ≈372 DR**: la fortezza è
giovane, le mura nuove, e un'orda primitiva la assedia sotto le ali di un drago
nero. Su una targa di bronzo alle porte, una profezia già incisa parla di
**«Quattro Eroi dal futuro»**. Quei Quattro siete voi: la leggenda che avete
sempre creduto passato è il vostro presente. **Paradosso bootstrap.**

**La regola di montaggio (D1).** Questa è **una sessione unica e
cinematografica**, non un dungeon:
- **Un solo scontro tattico completo**: il **duello con Skullcrusher** (§4), su
  griglia (M7-B).
- **Tutto il resto è a montaggio**: ogni scena non-tattica è una **prova di
  gruppo a CD fissa** (party di 4, APL 13). Ogni PG tira; se **≥ metà** (2/4)
  supera, la scena riesce. Fallimento = riesce comunque, ma con una
  **complicazione** (costo narrativo, mai game-over).
- **Ogni scena registra un ESITO** (riquadro ► **Esito registrato**): sono i
  dati che alimentano il carry-over B4 (§7) verso Fauci di Palude in ARC-08.

> **🎚️ DOPPIA MODALITÀ (scelta del DM, scena per scena).** Questo master è
> giocabile a **due velocità**, e puoi mescolarle: espandi dove vuoi respiro,
> lima dove vuoi ritmo.
> - **[FAST-PLAY]** — la scena si risolve a **montaggio** (una prova di gruppo,
>   un esito): 10-15 minuti. È il default cinematografico (D1).
> - **[COMBATTIMENTO COMPLETO]** — la scena si gioca **su griglia con statblock
>   pieni**, guardie, tattiche round-per-round e stati di fallimento: 45-90
>   minuti. Per quando vuoi che quella scena SIA la sessione.
>
> Le scene con entrambe le opzioni sono marcate. **Consiglio**: tieni
> [COMBATTIMENTO COMPLETO] almeno per l'**infiltrazione+Zog'tar** (§3) e il
> **duello con Skullcrusher** (§4) se vuoi una vera "sessione di battaglia
> antica"; usa [FAST-PLAY] per il contorno (arrivo, mura) se hai poco tempo.

**Chi c'è.** I 4 PG (Thorik, Tordek, Hella, Artemis); **Thorgrim Barbadiferro**
(antico portatore di Aegis Fang) e **Re Thorek I**; il generale **Zog'tar
Deatheye**; il drago **Skullcrusher il Nero**; e — nell'ombra — **Vatore** (il
ladro che diventerà Sal, §5).

**Cosa stampare.** La **Quick-Reference §0-bis**; l'**handout delle Cronache dei
Quattro Eroi** (§9, da dare all'arrivo); lo statblock di **Skullcrusher** (§4);
le mappe **M7-A/M7-B**; la tabella **B4** (§7).

**Come si chiude.** Vinta la battaglia antica, il **Rubino** si accende («Cuore
della Leggenda»): la profezia è compiuta — era sempre stata vostra. La luce vi
strappa al passato. → **master #5: il ritorno a Hammerfist** (riemersione al
Cuore della Montagna, Giorno 3 dell'assedio del 1372).

---

## §0-bis — QUICK-REFERENCE DM (una pagina)

### Le prove di gruppo delle scene a montaggio (party 4, ≥2 successi)
| Scena | Prova | CD |
|---|---|---|
| 1 — Cronache | Conoscenze (storia)/Sapienza | 18 |
| 2 — Thorgrim | Diplomazia/Intimidire | 20 |
| 3 — Infiltrazione | Muoversi Silenz./Nascondersi/Osservare | 20 (−2 se Sc.2 fallita) |
| 4 — Mura | Forza / Diplomazia-Guarire / Disattivare (scelta collettiva) | 18 / 18 / 20 |
| 5 — Vatore (opzionale) | Intuizione/Raggirare/Furtività (a seconda dell'approccio) | 18-22 |

### Il giro di Skullcrusher (boss, §4) — 3.5, niente 5e
- **Soffio acido** cono 18 m, 12d4, Riflessi CD 24 ½, **ricarica 1/1d4 round**.
- **Full-attack** (se a terra/quota bassa): morso +26, 2 artigli +21, 2 ali +21,
  coda +21.
- **Volo**: resta in quota, picchia e risale (Attacco in Volo) — punisce chi non
  ha gittata/volo.
- **Presenza Terrificante** CD 22 all'ingresso (Volontà o scossi).
- **«La Forgia ricorda»**: CONTA i colpi a segno (ferite ancestrali, N≤3) e
  l'esito → tabella B4 (§7). La Cintura di Tordek **rifiuta** di attivarsi qui.

### 🐾 Supporto Pathfinder 1e (dove il 3.5 è vago) — opzionale, dichiarato
> - **Viaggio nel tempo & paradosso**: il 3.5 non ha regole. Usa il principio
>   **«timeline auto-consistente»** (Novikov): tutto ciò che i PG fanno è
>   *già accaduto* — non possono cambiare che vincono, solo COME. Nessun
>   TS/meccanica: è una **cornice**, non un puzzle da rompere.
> - **Sincronizzazione di Vatore** (§5): danno/marchio inflitto a Vatore a −1000
>   → si manifesta su **Sal nel 1372** (ARC-09). Trattalo come un **legame
>   simpatico** permanente (stile *sympathy/antipathy* narrativo): nessun TS,
>   è un eco garantito. Registra il tipo di segno.

---

## §0-ter — QUANDO UN GIOCATORE HA UN'IDEA CHE NON È SCRITTA QUI

> **Una pagina sola, e serve mentre giochi.** Questo master ha molte vie
> scritte. I giocatori ne troveranno una che non c'è — è quello che si spera —
> e quel momento decide se la serata resta in piedi o si affloscia in un
> «mmh, non credo si possa».

### La regola, dalla skill dello stile: **assorbi, poi rilancia**

`references/style-pillars.md` §Mercer la chiama *«yes-and with teeth»*:
**l'invenzione del giocatore entra nel canone *e* genera una complicazione.**
Non «sì»; non «no». **Sì, e adesso c'è un problema nuovo.**

| Il giocatore dice | ❌ Come si spegne | ✅ Come si assorbe e si rilancia |
|---|---|---|
| *«Conosco un nano di qui — mio bisnonno me ne parlava»* | «Non c'è nessuno così» | «C'è. È il fratello di Durin, e ti riconosce dal naso. **Ma sta sul camminamento est, e stanotte non dovrebbe esserci nessuno lì.**» |
| *«Verso l'olio delle lanterne sulle scale e do fuoco»* | «Non è previsto» | «Funziona: due scale bruciano. **Il fumo sale dritto sul camminamento dove siete voi**, e adesso non vedete chi arriva» |
| *«Grido ai nani che la profezia parla di noi»* | tira Diplomazia | «La linea si rinsalda, +2 morale. **E l'orda sente il nome**: da adesso puntano voi» |
| *«Prendo la lastra di Balvar e la porto via»* | «È troppo pesante» | «Te la carichi. **Pesa, −1 alla DES finché non la posi**, e Balvar adesso sa esattamente dove sei» |

**Il metro, in una riga**: se l'idea è **specifica** e il giocatore accetta che
il mondo reagisca, **funziona**. Se è generica («cerco un modo»), chiedi
*«come, di preciso?»* — e poi funziona.

### Tre cose da non fare, che costano il tavolo

1. **Non chiedere un tiro per dire di no.** Un tiro è una domanda vera solo se
   entrambi gli esiti ti vanno bene. Se l'idea non deve riuscire, dillo e di'
   **perché**, in finzione.
2. **Non far pagare l'ingegno più della forza bruta.** Se spaccare la porta
   costa un round e aprirla con l'astuzia ne costa tre, hai insegnato al tavolo
   a spaccare le porte.
3. **Non salvare la scena scritta.** Se l'idea del giocatore salta un incontro
   che avevi preparato, **è saltato**. Il tempo che avanza lo spendi
   sull'orologio della notte — e i giocatori se ne accorgono, e ti ringraziano.

### 🎁 Il finisher va al giocatore — `[HDYWTDT]`

`style-pillars.md` §Mercer lo chiede per iscritto: al colpo che uccide un boss,
**la narrazione passa a chi l'ha tirato**. In questo master ci sono **due**
punti, e li trovi marcati nel testo:

- `[HDYWTDT — il finisher a chi abbatte Zog'tar]` → §4-bis
- `[HDYWTDT — il finisher a chi abbatte Skullcrusher]` → §4

🔎 **Non è un abbellimento, ed è la quarta cosa dichiarata e mai applicata di
questo repo**: il marcatore `[HDYWTDT]` era a **zero in tutti e nove gli
archi**, benché la skill dica che va scritto *«at boss-death points in
encounter content»*.

⚠️ **Come si fa senza che diventi imbarazzante**: non si dice «descrivi tu».
Si dice **«com'è che lo fai?»**, e si aspetta. Se il giocatore non vuole,
descrivi tu in una riga e vai avanti: è un regalo, non un compito.

---

## §1 — HIGHLIGHT ASIMMETRICI PER PG (i QUATTRO, Hella è tornata)

### 🛡️ THORIK — la profezia fatta carne (Casa di Davide lead)
- È la SUA leggenda: la Corona che porta è la stessa che il nonno di Thorgrim
  perse contro Skullcrusher. Aegis Fang, nelle sue mani e in quelle di Thorgrim,
  **canta la stessa nota** attraverso mille anni. Thorik non compie la profezia:
  **la profezia era sempre stata Thorik.**
- Al duello, **Aegis Fang scaglia la Cicatrice Ancestrale** (§4): è il gesto che
  segna Skullcrusher e, mille anni dopo, Fauci (carry-over B4).

### 🌙 HELLA — la seconda vita alla prova (BG3 lead — il ritorno che conta)
- È il suo **primo scontro da risorta**: Ibrido Treant, Collana, Durik al
  fianco. Il DM lo faccia pesare — la morte l'ha cambiata, e ora combatte in un
  passato dove non è mai esistita.
- ⚠️ **Vulnerabilità al fuoco** (costo del viaggio): Skullcrusher è acido, non
  fuoco — ma l'orda ha incendiari. E se evoca l'**Avatar della Radice** (Enorme),
  diventa un bersaglio: gioca il dilemma.
- 🐾 **Durik c'è, sempre** *(decisione DM 2026-09-24)*: attraversa il portale con
  lei, perché è legato alla Collana. Contro Skullcrusher conta una riga della sua
  scheda: **vulnerabile all'acido, +50%**. Il soffio del drago è l'unica cosa in
  questo viaggio che lo corrode davvero, e la giocatrice lo sa.
- 🌱 **Il dono «a metà»** *(`DEF-3` §9, riga «2 su 3»)*: se al rito i successi
  dello Step 5 sono stati **due su tre**, il PG che ha fallito lo scopre **qui**,
  al primo uso: il seme che porta il suo dono **non risponde al primo
  tentativo**. Risponde al secondo. Dillo in una riga, nel momento peggiore, e
  non spiegarlo.

### ⚒️ TORDEK — il pugno che deve trattenersi (Andor support)
- La **Cintura della Devastazione rifiuta di attivarsi** qui (*«il vero scontro
  appartiene al futuro»*): è coerenza, non nerf — Tordek deve vincere **senza**
  la sua arma migliore, che è riservata a Fauci nel 1372. Beat di disciplina.
- I **Bracieri** (coscienza) riconoscono la fucina antica di Hammerfist: *«Qui
  è dove tutto è cominciato, ragazzo. Batti bene.»*

### 🔮 ARTEMIS — il predone davanti al ladro (Andor lead)
- **Vatore** (§5) è il suo specchio oscuro: un ladro che ruba attraverso il
  tempo. L'Anello lo **percepisce** (aura temporale) prima di chiunque. È il PG
  giusto per fiutare che quel ladro «non è di qui» — e per decidere cosa farne
  (grigio: robarlo? ucciderlo? lasciarlo?). La sua avidità incontra un pari.
- ⚠️ **Il Marchio di Varis non è attivo** `[CANONE GIOCATO 2026-07-31]`: Artemis
  ha preso il Seme senza toccarlo e l'ha fatto mettere nello zaino di Tordek, e
  il Marchio si chiude col tocco. Quindi la risonanza qui sotto **non scatta**.
  Scatta solo se, prima del viaggio, qualcuno ha toccato il Seme: allora la
  sente chi lo ha toccato, anche se è Tordek. *Se scatta*: il marchio
  «riconosce» la firma temporale di Vatore, due fili della **stessa rete**
  (Varis ↔ Il Collezionista, CANONE DM 2026-07-23), mille anni prima che esista.

---

## §2 — LE ZONE DI HAMMERFIST ≈372 DR (Atlante)

> Mappa **M7-A**. Tre ambienti, una notte e un'alba: la fortezza giovane, il
> mare di tende dell'orda, le mura all'assalto.

### 🎚️ Scheda sensoriale delle tre zone — e cosa NON dire

> **Come si usa.** Le prime tre colonne sono quello che i PG colgono **in sei
> secondi** senza tirare. La quarta è **vincolante quanto le altre**
> ([ADR-0057](../../../plans/adr/ADR-0057-la-quarta-colonna-e-di-tutto-il-repo.md)):
> sono le cose che il tavolo deve **scoprire**, e che l'atmosfera, se ti scaldi,
> racconta al posto loro.

| Zona | Occhi | Orecchie | Pelle / naso | 🚫 Cosa NON dire |
|---|---|---|---|---|
| **1** Fortezza giovane | Pietra bianca, spigoli ancora vivi. **Una** statua di re, non venti | Scalpelli. Di giorno, a quest'ora, in tempo di guerra | Polvere di taglio fresco, che sa di calcare e non di fuliggine | **Che la targa è la profezia su di loro.** Lasciala leggere: è il nodo della Scena 1 |
| **2** Mare di tende | Mille fuochi fino all'orizzonte; una tenda più alta, nera | Un russare che non si interrompe mai del tutto | Grasso bruciato, ferro, bestia | **Quale tenda è quella del generale.** Si deduce da dove *non* passano le pattuglie (Osservare CD 18) |
| **3** Mura all'alba | Scale contro la pietra; nani spalla a spalla che non indietreggiano | Il boato di diecimila gole che diventa **una** | Fumo, sangue di nano (ferro dolce), corda bagnata degli arieti | **Che la linea terrà.** Non lo sai nemmeno tu: dipende dalla prova di gruppo |

⚠️ **Le tre righe «non dire» non sono suggerimenti di stile.** Ognuna protegge
una prova che sta più avanti in questo stesso documento. Dirle in anticipo non
rovina l'atmosfera: rovina **la scena dopo**.

### ZONA 1 — La Fortezza Giovane (Hammerfist appena eretta)
> **Read-aloud (LotR lead — deep time al contrario).** *Conoscete Hammerfist:
> le sue sale annerite dai secoli, le statue consumate, i nomi dei re incisi e
> riincisi. Ma QUESTA Hammerfist non ha ancora storia. Le mura sono bianche di
> pietra appena tagliata, gli spigoli ancora vivi. Le statue dei re sono una
> sola. E sulla porta, la targa di bronzo con la profezia dei Quattro Eroi è
> stata incisa OGGI, l'inchiostro del cesello ancora fresco. Questa è la vostra
> stessa leggenda, e la stanno scrivendo adesso: ogni pietra di queste mura è la
> stessa che fra mille anni sarà vecchia di un millennio.*

**Terreno (callout):** cortili di pietra chiara (movimento normale); la Sala del
Trono di Re Thorek I; la fucina originale (i Bracieri di Tordek la
riconoscono). Zona **sicura** (dentro le mura). Punto d'arrivo del portale.

### ZONA 2 — Il Mare di Tende (l'orda, di notte)
> **Read-aloud (Salvatore — l'infiltrazione).** *Fuori dalle mura, il buio è
> vivo. Diecimila nemici dormono attorno a mille fuochi — orchetti, hobgoblin,
> cose peggiori — e il campo si stende fino all'orizzonte come un mare in cui
> ogni onda è una gola che russa. L'aria sa di grasso bruciato, di ferro e di
> bestia. Da qualche parte, al centro, la tenda del generale. Un passo falso e
> il mare si sveglia tutto insieme.*

**Terreno (callout):** tende fitte (copertura, difficile in mischia); 4 posti di
guardia (GP1-GP4 agli angoli); la **tenda del comando** (Zog'tar) al centro;
notte = furtività CD 20; ogni fuoco è luce fioca a 3 m. Vedi M7-A zoom.

### ZONA 3 — Le Mura all'Alba (l'assalto)
> **Read-aloud (Salvatore lead, LotR support).** *Il primo ariete arriva alle
> mura che il sole non è ancora sopra il crinale. Il legno prende la pietra con
> un tonfo che prende lo sterno prima delle orecchie, e il camminamento
> vi si muove sotto i piedi di un dito. Un nano accanto a voi si sputa nelle
> mani, riprende l'ascia e non dice niente. Quello dopo di lui si è già
> incastrato la barba nella cinghia dell'elmo, e non ha il tempo di
> tirarla fuori. In basso, le scale salgono.*
>
> **Che fate?**

⚠️ **Perché questo box è stato riscritto** *(riscrittura 2026-09-18)*. Il
precedente diceva *«Dove vi gettate, la linea tiene»* e chiamava i PG *«quattro
leggende venute dal futuro»*. Due difetti dichiarati, non questioni di gusto:

- `editorial-standards.md` §2 — **mai risolvere l'azione dei PG dentro il
  read-aloud**. «La linea tiene» era l'**esito della prova di gruppo** della
  Scena 4, letto prima che qualcuno tirasse.
- `read-aloud-adulti.md` §4 — *il predestinato senza costo* e *tutto epico*
  sono due delle sei cose che fanno staccare un lettore adulto. Il nano che si
  sputa nelle mani fa lo stesso lavoro e non chiede di essere creduto.

**Terreno (callout):** camminamenti sopraelevati (+4,5 m); brecce dove gli
arieti mordono; scale d'assedio (Forza per rovesciarle); il cortile interno
dove, alla fine, Skullcrusher cala. Vedi M7-B (arena del duello).

---

## §3 — LE SEI SCENE (montaggio)

> Ogni scena: read-aloud, prova di gruppo, ► Esito registrato. Il ritmo è
> cinematografico: non attardarsi, tranne al duello (§4) e a Vatore (§5).

### SCENA 1 — L'Arrivo e le Cronache dei Quattro Eroi
> **Read-aloud.** *Il portale vi risucchia — colori invertiti, mille vite in un
> istante — e poi fango, fumo, corni di guerra. Su una targa di bronzo alle
> porte, una profezia nanica già incisa: «Quattro Eroi dal futuro salveranno la
> fortezza dalla Mano Rossa e dal drago Skullcrusher il Nero». Quei Quattro
> Eroi… siete VOI.*
- ⚕️ **GUARIGIONE DEL PASSAGGIO (all'arrivo, automatica)** `[CANONE — DM
  2026-07-31]`: attraversare mille anni **rimette in ordine il corpo**. I quattro
  arrivano a **pf pieni**, senza livelli di affaticamento, con danni da
  caratteristica temporanei azzerati e **tutti gli usi giornalieri ricaricati**
  (invocazioni, poteri dei Bracieri, sinergie 1/giorno, incantesimi di Hella).
  **Nessun tiro, nessun costo, non è una scelta.**
  - **Cosa NON guarisce**: i costi **permanenti** di Thorik — **−4 DES** fra Corona
    e rito dello Smeraldo, e il **−1 CA** se al rito di `DEF-3` §5 ha donato il +2 di
    deflessione (sono prezzi pagati, non ferite) — gli oggetti spesi (Cuore di Moradin, Diapason, Rubino
    quando si accenderà) e le condizioni narrative dell'Echo Ledger.
  - **Perché esiste**: senza questa regola il party arriva al duello con
    Skullcrusher con quello che è avanzato da Terros e dal rito — cioè, molto
    probabilmente, **con dei nani mezzi morti**. Il #4 è una sessione-leggenda
    con un solo scontro tattico: deve partire pulita.
  - **Come si racconta** (mai come una ricarica): *«Il portale non vi trasporta:
    vi RIFÀ. Per un istante lunghissimo siete scomposti nei vostri mille anni —
    e quando vi ricomponete dall'altra parte, le ferite che avevate non ci sono
    più, perché in questo momento della storia non le avete ancora ricevute.»*
  - Il **costo sull'orologio di Hammerfist è zero**: il Rubino riporta i PG
    all'istante esatto della partenza (`ARC07-DEF-5` §Supporto PF1e).
- **Handout**: la **pagina delle Cronache** (§9) — scoprono di essere la profezia.
- **Shock temporale (all'arrivo)**: TS Volontà **CD 20** o **confusi 1d4 round**
  (−2 concentrazione/percezione), poi chiarezza. *(È l'unico prezzo del
  passaggio: il corpo torna intero, la testa no.)*

#### 🔍 Nodo d'indizio — la targa di bronzo *(Fatto · Lettura · Nome)*

> **Perché è un nodo e non una prova.** Questo master ha un'indagine dentro — i
> PG devono capire **che la profezia parla di loro** — e finora era una prova
> sola, **CD 18**, che si superava o si sbagliava. La skill `rumblingstone-indagine`
> chiede tre strati e **almeno tre porte**, perché un tavolo di picchiatori
> deve poterci entrare lo stesso.

| Strato | Cosa dà | Come si prende |
|---|---|---|
| **Fatto** | *«La targa dice: quattro eroi dal fuoco e dalla pietra.»* | **gratis**, chiunque sappia leggere il nanico. Non si tira |
| **Lettura** | *«L'inchiostro del cesello è fresco. È stata incisa oggi.»* | **una** porta qualsiasi, sotto |
| **Nome** | *«Quei quattro siamo noi, e lo eravamo già prima di partire.»* | **due** porte diverse, o una porta + la Lettura |

**Le sei porte** — tre bastano, e almeno una è fisica, così anche chi non ha
gradi entra:

| Porta | Prova | Cosa vede |
|---|---|---|
| 🧠 Sapere | Conoscenze (storia) **CD 18** | la profezia non è nelle cronache che hanno letto nel 1372: **è stata cancellata** |
| 👁️ Guardare | Osservare **CD 15** | i trucioli di bronzo sono ancora per terra sotto la targa |
| ✋ **Toccare** | **FOR o DES grezza CD 12** — passarci sopra il pollice | il taglio è **vivo**, taglia il polpastrello. Chiunque, nessun grado richiesto |
| 👃 Annusare | Sopravvivenza **CD 14** o un nano, gratis | odore di metallo caldo: il cesello ha lavorato **stamattina** |
| 🗣️ Chiedere | Diplomazia **CD 12** a un qualsiasi nano di guardia | *«L'ha incisa il Re stanotte. Ha detto che gli è venuto in sogno»* |
| ⚒️ Mestiere | Artigianato (fabbro) **CD 15** — Tordek, gratis | riconosce la **mano**: è lo stesso cesello della fucina che userà tra mille anni |

🚫 **Cosa NON dire**: che la profezia parla di loro. Anche se nessuno prende il
**Nome** subito, non si regala: torna alla Scena 2 quando Thorgrim mostra la
gemma, e alla Scena 6 quando il Rubino si accende. **Un vicolo cieco non
esiste** — l'indizio ripassa, cambiato.

- **Se prendono il Nome in Scena 1** → arrivano al consiglio di guerra sapendo
  chi sono: Re Thorek I li riconosce **prima** che mostrino la Corona, e la
  prova di gruppo della Scena 1-bis scende a **CD 16**.
- **Se non lo prendono** → non perdono niente. Lo prendono dopo, e la scena in
  cui lo prendono diventa la più forte della serata.
- ► **Esito**: accettano/subiscono il ruolo. Imposta il tono «nessuna pietà» vs
  «misericordia» del Rubino (eco §7).

### SCENA 1-bis — La Pattuglia di Durin, Re Thorek I e la Notte `[ESPANDIBILE]`
> **[FAST-PLAY]**: salta a Scena 2 (Thorgrim/Re Thorek riassunti lì). **[SCENE
> COMPLETE]**: gioca l'arrivo esteso qui sotto — è il cuore "umano" del viaggio.

**La pattuglia di Durin (riconoscimento — 3 vie).** Nel bosco a est delle mura,
una pattuglia nanica (6 veterani) li ferma.

**DURIN (teso, voce che gli scappa in alto):** *«FERMI! Chi siete?»* La guida è
**Durin Rocciadura** (Guerriero 6, statblock §4-bis), veterano spaventato e
onesto. Fissa la Corona sulla fronte di Thorik.

**DURIN (piano, quasi a sé stesso):** *«Quella cosa… brilla come il sole
forgiato. È… una leggenda?»* **Tre modi di farsi riconoscere** (tutti
funzionano, nessun tiro se sinceri):
- **A — Mostrare la Corona**: Durin cade in ginocchio.
  **DURIN (rotto):** *«La Corona dei Padri. Pensavo fosse un mito.»*
- **B — Invocare Moradin** (preghiera sincera): un **tuono** solo, dal cielo
  sereno. Durin e i suoi si inginocchiano.
  **DURIN (fermo, per la prima volta):** *«Il Padre ha parlato.»*
- **C — Mostrare potere divino** (Benedizione della Forgia, aura dorata su
  Aegis Fang):
  **DURIN (a bassa voce, ai suoi):** *«Dio ha parlato attraverso l'arma.»*
Esito identico: Durin passa da diffidente a **fedele fino alla morte**, li porta
a cavallo al castello. *(Se attaccano la pattuglia: è un tragico
malinteso — i nani che erano venuti a salvare li credono spie; §6 Contingenze.)*

**Re Thorek I — il consiglio di guerra.** Il re antico (Guerriero 16, 182 anni,
Frostcleaver in pugno) chiede di vedere la Corona che «suo nonno perse contro
Skullcrusher 50 anni fa». Riconosciutala, si inginocchia e recita la profezia.

> 🩸 **Re Thorek I e Thorgrim sono cugini** *(decisione DM 2026-09-24)*: nipoti
> dello **stesso re**, quello caduto contro Skullcrusher cinquant'anni prima.
> Per questo dicono tutti e due *«mio nonno»*, e nessuno dei due mente. La
> Corona è il lutto del re; l'ascia, Aegis Fang, è rimasta a Thorgrim.

**RE THOREK I (lento, passato remoto, come chi cita a memoria):** *«Quattro
eroi dal fuoco e dalla pietra… nella notte più oscura salveranno gli antenati
e i futuri.»* Poi, alla tavola di guerra: **800 nani** contro **10.000
nemici** + il drago; le mura reggono 2 ore; l'unica chance è **uccidere Zog'tar
di notte** (per fiaccare l'orda) e **affrontare Skullcrusher** all'alba.
- **Handout 1A — Piano di Battaglia** (§9): forze, obiettivi, equipaggiamento.
- **Prova di gruppo**: Diplomazia/Intimidire **CD 20** → **fiducia piena** (4
  Pozioni di Invisibilità CL 12, Benedizioni di Moradin +2/+2, mappa accurata
  del campo). Fallimento: aiuti dimezzati (−2 alla Scena 3). *(Questa prova
  ASSORBE la Scena 2: se giochi le scene complete, Thorgrim e Re Thorek sono
  QUI.)*

**La notte prima (prep).** Nei quartieri ospiti: banchetto (+1 morale 12 h se
mangiano), fabbri che affilano le armi, chierici che benedicono.
- **HELLA — i Treant dell'alba.** *(Allineato al rito il 2026-09-24: la prima
  stesura le faceva piantare «i 3 semi di treant», ma al rito di `DEF-3` §7 i
  tre semi sono entrati nella **Collana dei Semi Eterni**, e da qui in poi non
  si piantano più.)* All'alba Hella usa l'**Evocazione dei Guardiani** sui semi
  I e II: **due Treant di Adamantio** (statblock `DEF-3` §7: 90 pf, RD
  10/adamantio, 2 schianti +18, danni doppi alle strutture) che caricano il
  fianco dell'orda. Costa **due** delle tre cariche del giorno, e la tacca della
  notte resta **una**: vegliare i semi che si aprono. È il beat di potere della
  druida risorta, e ha un prezzo: se Durik viene distrutto nel duello, resta
  **una carica sola** per richiamarlo.
  `[PROPOSTA — conferma DM]` Se al rito Hella ha trovato la **ghianda
  annerita** e non l'ha ancora piantata, «il primo suolo sacro che tocca» può
  essere questo: niente Treant in più, ma una quercia che fra mille anni sarà
  vecchia di mille anni.
- **⚫ SEME DEL GHOSTLORD (hook a lunghissimo termine — CANONE, DM 2026-07-23).**
  Il party incrocia il **Mastro Costruttore Zeth**, un mezz'elfo dagli occhi
  febbrili, che traccia rune sui tunnel: *«Le mura di Thorek potrebbero cedere.
  Ma legherò la mia anima alla montagna in una Consacrazione. I miei leoni di
  pietra proteggeranno queste gallerie per sempre. Un chierico incappucciato mi
  ha appena dato i componenti perfetti.»* → **È il futuro Ghostlord / Zeth il
  Murato**: i "componenti" sono in realtà per una **Lichificazione**, inflittagli
  dalla fazione del **Collezionista** che viaggia tra i piani e le epoche. I PG
  seminano (senza saperlo) il dilemma etico di Hella su Zeth in ARC-09. Registra
  nell'Echo Ledger (§7) e in `state.md §7`.
- **Riposo — scelta**: **breve** (3 h: metà slot/pf, ma 5 h per l'infiltrazione,
  IDEALE) vs **lungo** (6 h: recupero pieno, ma solo 2 h all'alba — tempo
  strettissimo). Il momentum spinge al riposo breve.

---

### ⏳ L'OROLOGIO DELLA NOTTE — otto ore, e ogni cosa ne costa

> **Perché esiste.** La scelta del riposo qui sopra era già un orologio, scritto
> a parole: «5 ore» contro «2 ore». Ma un tempo che non si segna non si sente,
> e il tavolo non può *scegliere di correre un rischio* se non sa quanto ha in
> mano. Questo è il congegno che i due banchi del repo — il Palio e l'Abbazia —
> usano per reggere la tensione, e questo master ne aveva **una menzione sola**.

**Si segna su un foglio, in vista.** Dal tramonto all'alba ci sono **8 tacche**.
Ogni tacca è mezz'ora scarsa di gioco reale.

| Cosa | Tacche |
|---|---:|
| Consiglio di guerra con Re Thorek I (Scena 1-bis) | **1** |
| Riposo **breve** | **2** · Riposo **lungo** | **5** |
| Banchetto e benedizioni (facoltativo, +1 morale 12 h) | **1** |
| I tre semi di Hella, piantati e vegliati | **1** |
| Attraversare il mare di tende (Scena 3, skill challenge) | **2** |
| Ogni **fallimento** nello skill challenge | **+1** |
| Parlare con Balvar invece di ucciderlo subito (§4-ter) | **1** |
| Cercare il Mastro Costruttore Zeth (seme del Ghostlord) | **1** |

**Quando le tacche finiscono, sorge il sole.** Non è una punizione: è la Scena 4
che comincia, con i PG dove sono in quel momento.

| Tacche spese all'uscita dalla tenda | Come si arriva alle mura |
|---|---|
| ≤ 6 | in tempo. Si rientra, si schiera, §4 normale |
| 7 | 🟡 si rientra **correndo**: nessun riposo prima del drago, −1 a tutti i TS del primo round di §4 |
| 8 | 🔴 **l'alba vi coglie fuori dalle mura.** Non morite: attraversate un campo che si sta svegliando. Prova di gruppo Muoversi Silenziosamente **CD 20**, poi §4 comincia con i PG **fuori**, e Skullcrusher li vede per primo |

⚠️ **L'orologio corre sulle SCELTE, non sul tempo reale.** Un tavolo che discute
mezz'ora su cosa fare non spende una tacca; un tavolo che decide di andare a
cercare Zeth sì. È la regola dell'Abbazia (`ADR-10` interno: *l'oppressione
avanza sulle scoperte*), e serve a non punire proprio il comportamento che
questo master vuole ottenere — **guardarsi intorno**.

🔎 **E qui l'orologio dice una cosa che il testo prima non diceva**: parlare con
Balvar, cercare Zeth e fare il banchetto costano **3 tacche** in tutto. Sono i
tre pezzi migliori della notte, e sommati sono anche il rischio più grosso. È
il bivio, ed è **vero** — non una finta scelta con una risposta giusta.

### SCENA 2 — Thorgrim Barbadiferro e gli Antenati `[FAST-PLAY — assorbita in 1-bis se giochi le scene complete]`
> **Read-aloud (Mercer lead, Casa di Davide support).** *Il vecchio è seduto e
> non si alza. Ha le mani appoggiate sulle ginocchia, e sono mani che hanno
> tenuto la stessa ascia che tenete voi: si vede dal callo, nello stesso punto.
> Guarda la gemma sulla vostra fronte per il tempo di tre respiri. Poi gli
> occhi gli si riempiono e lui non se ne accorge, perché sta già parlando.*
>
> **THORGRIM (voce che non trema, occhi che sì):** *«Mio nonno l'ha persa. Se
> dite il vero, mettetemela in mano.»*
>
> *Quando l'ascia passa fra le sue dita e le vostre, per un istante le due prese
> si toccano sul legno. E il legno **suona**.*

⚠️ **Perché questo box è stato riscritto** *(2026-09-18)*. Il precedente
portava **otto nomi propri** in cinque righe — Thorgrim, Barbadiferro, Aegis
Fang, Re Thorek, Skullcrusher, la Corona — ed è **l'esempio testuale** che
`read-aloud-adulti.md` §1 usa per spiegare il difetto: *«Se in un box compaiono
Skullcrusher, Thorgrim e Barbadiferro, la metà del tavolo ne ha persi due»*.
Adesso il nome proprio nuovo è **uno**, il resto sono mani, callo e legno — e
il tono di Thorgrim è dichiarato, come chiede `editorial-standards` §2.
- **Prova di gruppo**: Diplomazia/Intimidire **CD 20** → fiducia piena
  (invisibilità, benedizioni, mappa del campo). Fallimento: aiuti dimezzati
  (−2 alla Scena 3).
- **Gancio**: Thorgrim riecheggerà nella Cerimonia delle 100 Asce (ARC-08).
- ► **Esito**: *aiuti pieni / dimezzati*.

### SCENA 3 — Infiltrazione e Zog'tar `[FAST-PLAY / COMBATTIMENTO COMPLETO]`
> **Read-aloud.** *Notte. Diecimila nemici dormono attorno a mille fuochi. Vi
> muovete invisibili tra le tende verso quella, enorme, di pelle nera e ossa di
> nani: la tenda del generale **Zog'tar Deatheye**. Un passo falso e il mare si
> sveglia tutto insieme. Ma se cade lui, il coro di diecimila perde il direttore.*

> ⚠️ **Nella tenda non c'è solo Zog'tar.** C'è anche **Balvar Fuocospento**
> (**§4-ter**), che vi lascerà entrare apposta e vi dirà una cosa che nessun
> altro in questo secolo può dirvi. **Leggi il §4-ter prima di giocare questa
> scena**: la tenda ha quattro rune già incise, e una di esse impedisce i
> teletrasporti.

#### 🎚️ [FAST-PLAY] — montaggio (10-15 min)
- **Infiltrazione (3 tiri)**: Muoversi Silenz./Nascondersi/Osservare **CD 20**
  (−2 se aiuti dimezzati). Metà successi = raggiungete la tenda non visti.
- **Zog'tar (risoluzione veloce, GS 14)**: un **assalto coordinato** (sorpresa +
  il colpo più forte del party) lo abbatte se dichiarano tattica sensata e
  vincono **un** tiro contrapposto. Se l'infiltrazione è fallita, è sveglio: −4
  alla sorpresa, un solo scambio.

#### 🎚️ [COMBATTIMENTO COMPLETO] — infiltrazione giocata + boss su griglia (60-90 min)
**Skill Challenge «Attraversare il Mare di Nemici»** (~2 km, a blocchi di 200 m):
- Ogni blocco: **Muoversi Silenziosamente CD 20** + **Nascondersi CD 22**.
  L'invisibilità dà **+20 a Nascondersi** finché non attaccano/lanciano offensivi.
- **3 fallimenti prima di 5 successi = pattuglia** (scontro CR 10, rischio
  allarme locale → malus tattici a Zog'tar/Skullcrusher).
- **Complicazioni (tira 1d6 per blocco):**

| d6 | Complicazione |
|---|---|
| 1-2 | Nessun evento. |
| 3 | **Pattuglia di 4 orchi** (Guerriero 3) passa a 6 m: restare immobili, Muoversi Silenz. **CD 18**. |
| 4 | **Lupo da guerra** (Olfatto acuto, Ascoltare/Osservare +8): un fallimento di Furtività → abbaia, la pattuglia si ferma. |
| 5 | **Falò vicino**: luce intensa, Nascondersi **CD +4** per quel blocco. |
| 6 | **Squadrone hobgoblin (6)** a 24 m: se falliscono >2 prove, mandano un **corridore** alla tenda di comando (Zog'tar sarà pre-allertato). |

**Boss: ZOG'TAR DEATHEYE** (statblock completo §4-bis). I PG invisibili hanno un
**round di sorpresa pieno** se nessuno ha parlato/lanciato incantesimi
rivelatori. Round-by-round e le scelte-costo dei PG → **§4-bis**.

#### ⚖️ Due vie che non passano dall'iniziativa

> `module-standard` §7 ne chiede **almeno due per scontro**, e questa scena ne
> aveva **zero**: c'era un solo modo di risolvere Zog'tar, ed era ucciderlo.
> ⚠️ Nessuna delle due è «vincere gratis»: entrambe costano, e una **non lo
> ammazza**.

**Via A — l'Occhio contro il suo padrone** *(Artemis, Hella, chi ha visto la runa)*.
L'**Occhio di Ossidiana** è un artefatto **maledetto** e Zog'tar lo sa a metà:
il prezzo è che la luce divina lo brucia. Chi lo capisce — Sapienza Magica
**CD 20**, oppure **gratis** se in Scena 1-bis hanno accettato la Benedizione
di Moradin e la vedono reagire — può **mostrargliela invece di colpirlo**:
Intimidire **CD 22** con la Corona scoperta o la Luce di Lathander in mano.
- **Riesce** → Zog'tar **arretra**, e arretrando esce dalla tenda davanti alle
  sue guardie. Perde la faccia, e con lei il campo: l'orda all'alba combatte a
  **−1 morale**, che vale i due nemici in più della Scena 4 tolti.
- ► **Esito nuovo**: *umiliato, non ucciso*. 🔴 **Ed è un problema, non un
  premio**: Zog'tar **vive**, e in ARC-08 la Mano Rossa ha un generale in più
  nella sua storia. Registra nell'Echo Ledger (§7).

**Via B — il corridore che non parte** *(chiunque, e non serve nessun grado)*.
Se la complicazione **6** dello skill challenge è uscita, c'è un corridore
hobgoblin che sta per andare alla tenda. Fermarlo **non richiede di ucciderlo**:
- **DES grezza CD 14** — sgambetto nel buio, e il ragazzo cade nel fuoco altrui;
- **Raggirare CD 16** in orchesco (chi lo parla) — *«Messaggio già passato, torna
  in fila»*;
- **FOR grezza CD 16** — una mano sulla bocca, e lo si tiene finché non sviene.
- **Riesce** → Zog'tar non è pre-allertato, e il round di sorpresa resta pieno.
- **Fallisce** → il corridore arriva. **Non è la fine**: Zog'tar sveglio è più
  duro, e il §4-bis ha già la riga per quel caso.

⚠️ **Perché due e non una.** Una via alternativa sola diventa «la soluzione
giusta» e il tavolo la cerca invece di giocare. Due che costano in modi diversi
— una la fama del nemico, l'altra il fiato — restano **scelte**.

- ► **Esito (entrambe le modalità)**: *ucciso in silenzio / spettacolare*. Se
  **spettacolare** (esplosione, decapitazione davanti alle guardie), il terrore
  dilaga MA **Skullcrusher interviene furioso** → §4 inizia col drago già in
  picchiata (i PG perdono la prima azione). Se l'orda è stata **pre-allertata**
  (corridore, allarme): +2 nemici nelle mura (Scena 4) e Zog'tar non è di
  sorpresa.

### SCENA 4 — Le Mura sotto Assalto (alba)
> **Read-aloud (Salvatore lead).** *Il camminamento è largo quanto un tavolo da
> pranzo e lungo quanto la fortezza. Sotto, l'orda non urla più: ha smesso
> quando ha cominciato a salire, e il silenzio che ha lasciato è peggio. Un
> uncino morde la pietra a tre passi da voi, poi un altro, poi sei insieme. Il
> capitano delle mura guarda voi, non i suoi.*
>
> **Che fate?**

**Le tre vie, e nessuna è quella giusta.** La prova è **collettiva**: il party
sceglie **una** via, tutti tirano quella. Non c'è una scelta migliore — c'è
quella che costa meno a *questo* gruppo.

| Via | Prova | Se riesce | Il costo, anche riuscendo |
|---|---|---|---|
| **Tenere la breccia** | Forza o attacco, **CD 18** | la falla regge; i nani vi vedono farlo | ci si arriva al duello **stanchi**: −2 al primo tiro d'iniziativa del §4 |
| **Rincuorare i difensori** | Diplomazia o Guarire, **CD 18** | +2 morale a tutta la linea per l'assalto | la breccia la tiene qualcun altro, e **qualcuno muore**: tira sul *Registro delle Perdite* di ARC-08 |
| **Sabotare gli arieti** | Disattivare o Artigianato, **CD 20** | due arieti fuori uso, l'assalto rallenta di mezz'ora | siete **fuori** dalle mura quando il drago arriva: §4 comincia con i PG separati di 18 m |

**🚫 Modi di fallimento — il fallimento è un costo, mai uno stop.** Nessuna
combinazione di tiri ferma l'avventura: il duello con Skullcrusher si gioca
comunque, perché è già accaduto.

| Successi (su 4) | Cosa cambia davvero |
|---|---|
| 4 | le mura reggono pulite; §4 parte con i PG schierati e **Re Thorek in piedi dietro di loro** |
| 2-3 | reggono a stento. §4 parte normale |
| 1 | i nani perdono il camminamento est: il duello si combatte **con Re Thorek a 8 pf alle spalle**. Pressione emotiva, **nessun malus meccanico** — il re non è una barra della vita |
| 0 | 🔴 **la breccia cede.** Il duello si sposta **dentro il cortile**, in mezzo ai feriti: M7-B con 6 quadretti di terreno difficile e **due nani a terra** che Hella può scegliere di raggiungere invece di combattere. Nessun malus: una **scelta in più**, e più dura |

⚠️ **La riga a zero successi è il punto di questa tabella.** Il modo più veloce
di insegnare a un tavolo che indagare e rischiare non conviene è punire il
fallimento con meno gioco. Qui a zero successi **si gioca di più**, non di meno.

- ► **Esito**: *mura tenute saldamente / a stento / breccia ceduta*.

### SCENA 5 — ⚔️ Il Duello con Skullcrusher → **§4** (unico scontro tattico)

### SCENA 6 — Il Rubino e il Ritorno
> **Read-aloud (Casa di Davide — la profezia compiuta).** *L'orda, senza
> generale e senza drago a spronarla, si sfalda come sabbia. Hammerfist regge. E
> sulla vostra fronte il **Rubino** — la terza gemma, muta da sempre — si accende
> per la prima volta, e la sua luce è calda come sangue e antica come la pietra:
> «Cuore della Leggenda». La vittoria che credevate storia era la vostra, adesso,
> con le vostre mani. Non avete cambiato il passato. Il passato ha sempre avuto
> il vostro volto. La luce del Rubino vi avvolge — e vi strappa via, verso casa,
> verso una fortezza che brucia mille anni più in là.*
- **Attivazione gemme (D5/D16)**: portale aperto da Topazio+Smeraldo; il **Rubino
  si accende SOLO ORA** e diventa il motore del ritorno al 1372.
- **Raccordo (D16)**: → riemersione al **Cuore della Montagna**, Giorno 3
  dell'assedio del 1372. La **cucitura** è il **master #5**.
- ► **Esito**: il **tono del Rubino** dipende da come è finito il duello (§7).
  Corona ora a **3 gemme accese**.

---

## §4-ter — BALVAR FUOCOSPENTO, il consigliere `[CANONE — DM 2026-07-31]`

> **Perché esiste.** Due giocatori hanno chiesto la stessa cosa da due lati:
> Artemis non ha mai niente da individuare, Thorik non incontra mai
> incantatori (`DM-CAMPAIGN-PLAYBOOK` §1-bis). Balvar è la risposta — ma non è
> un boss in più appiccicato al modulo: è **il motivo per cui l'orda ha un
> drago**. Toglilo e la §4 cambia. Statblock:
> `Bestiario/villain/balvar-fuocospento-cr13.md`.

### Chi è

Un **nano dello scudo**, vecchio, esiliato da Hammerfist prima che i PG
nascessero — anzi: prima che nascessero i bisnonni dei nani che i PG hanno
appena conosciuto. Era il **runaio della fortezza**, quello che incideva le
protezioni sulle porte. Adesso incide per Zog'tar, e Abbathor gli tiene la
mano ferma.

Non comanda l'orda. **Consiglia**, e per questo è più pericoloso del generale:
Zog'tar sa uccidere diecimila uomini, Balvar sa **dove** vanno colpite le mura.

#### ⚖️ Il grigio — perché **crede di aver ragione** *(pilastro GoT)*

> **Aggiunto nella riscrittura del 2026-09-18.** Balvar era già il personaggio
> migliore del master, ma era scritto come **un nemico interessante**, non come
> una fazione. La differenza è che di un nemico interessante si chiede *come lo
> batto*; di una fazione che crede di aver ragione si chiede *cosa vuole, e cosa
> gli costa averlo*. È l'unica riga che il pilastro 5 chiede davvero.

| | |
|---|---|
| **Vuole** | che Hammerfist **cada in fretta**. Non per odio: perché un assedio lungo significa fame dentro le mura, e lui l'ha già vista una volta |
| **Crede** | che i re nanici mentano ai loro, e che le sue rune abbiano protetto per trent'anni una fortezza che l'ha esiliato **senza processo** |
| **La leva** | = suo nipote. È dentro le mura, ha diciannove anni, e Balvar sa esattamente su quale camminamento monta la guardia |
| **Ricattabile** | sì, e da nessuno che non gliene parli **per primo**. Se i PG lo minacciano, si chiude; se gli dicono che il ragazzo è vivo, no |
| **Non è un mostro** | e questo è il punto: se il tavolo lo tratta da mostro, lo scontro funziona lo stesso. Se lo tratta da nano, il master cambia forma |

⚠️ **È una fazione recuperabile, non una fazione debole.** Balvar in combattimento
resta un GS 13, e le sue rune fanno male. Recuperarlo **non lo indebolisce**:
gli cambia bersaglio. *(È la stessa regola dell'`ADR-06` interno dell'Abbazia
sui corsari — il banco l'aveva già capito.)*

🚫 **Cosa NON dire.** Che il nipote esiste. Balvar non lo nomina mai per primo:
si arriva al ragazzo solo se qualcuno **guarda** cosa sta incidendo sull'ardesia
(Osservare **CD 20**: è un nome nanico, e sotto una data di nascita), oppure se
un PG nano gli chiede chi ha lasciato a Hammerfist — **Diplomazia CD 18**, e
funziona solo se non l'hanno ancora minacciato.

> **Read-aloud — il primo incontro (dentro la tenda del comando, Scena 3).**
> **Read-aloud (Andor lead) — 1 di 3, poi FERMATI.** *In fondo alla tenda, dove
> la luce dei bracieri non arriva, un vecchio è seduto su uno sgabello da
> bottega. Grembiule di cuoio. Sulle ginocchia una lastra di ardesia che sta
> incidendo con una punta di ferro, piano, come se fuori non ci fossero
> diecimila tende e un drago.*

> **2 di 3 — dopo che qualcuno ha reagito.** *Alza la testa. Vi guarda uno per
> uno, con calma. Quando arriva alla gemma sulla fronte del vostro capo si
> ferma un istante di troppo. Poi torna a incidere. **Non chiama la guardia.***

> **3 di 3 — solo quando il silenzio diventa scomodo.**
> **BALVAR (voce da vecchio artigiano, nessuna minaccia, nessuna fretta):**
> *«Quella corona la finirono con tre gemme. Tu ne hai due.»* — *un colpo di
> punta sull'ardesia* — *«Quindi non è oggi.»*
>
> **Che fate?**

⚠️ **Spezzato in tre il 2026-09-18, e non per pignoleria.** Era **un box da 15
righe**, sopra il tetto di 12 di `read-aloud-adulti.md` §2, e la self-check
della skill dello stile ha una domanda apposta: *«Did any box grow past the
ceiling because the prose got interesting? → cut; the ceiling wins»*. Qui la
prosa **era** diventata interessante, ed è il motivo per cui era cresciuta.
Spezzandolo in tre beat si guadagna anche una cosa che il box unico non aveva:
**Balvar aspetta che i PG reagiscano prima di parlare**, e il suo silenzio
diventa la prima battuta.

### La cosa che lo rende memorabile: sa da dove venite

**Leggere il Fuori-Posto** (3/giorno) è l'unica capacità che conta davvero. In
tutta Hammerfist del ≈372 DR, **Balvar è il solo che sa che i PG non
appartengono a questo secolo** — e non lo dice a nessuno, perché
un'informazione che nessuno ha vale più di un'informazione condivisa.

**Non li smaschera. Tratta.** È un mercante di segreti come Varis è un mercante
di merce, e la scena giusta è la stessa: un affare vero con un amo vero.

> **BALVAR:** *«Non chiedo chi siete. Chiedo una cosa sola, e ve la chiedo
> adesso perché fra un'ora saremo tutti occupati. Quando avrete finito quello
> che siete venuti a fare — e lo finirete, lo vedo da come camminate — **dite
> che c'ero**. Non che ho vinto. Che c'ero. La Cronaca scrive solo i nomi che
> qualcuno pronuncia.»*

Questo è il suo prezzo, ed è per questo che ha lasciato passare i PG. Un uomo
cancellato dagli annali che chiede a dei viaggiatori del tempo di **essere
ricordato**. Se accettano, in ARC-08 e ARC-09 gli affreschi della Sala avranno
**un pannello in più**, e nessuno saprà spiegarlo — tranne loro.

### La Catena: perché il drago combatte per l'orda

Balvar ha inciso una **runa-vincolo** nella scaglia sternale di Skullcrusher.
Non è dominazione: è un **contratto scritto nella carne**, e il drago lo sa,
e lo odia. Questo aggancia direttamente la §4:

| Cosa fanno i PG | Effetto sul duello con Skullcrusher (§4) |
|---|---|
| **Non se ne accorgono** | il duello va come scritto |
| **Individuano la runa** (Sapienza Magica **CD 24**, o Conoscenze storia CD 22 per riconoscere il nanico antico — **è scritta, quindi si legge**) | sanno dove colpire: un colpo mirato alla scaglia sternale (**CA +4**) durante il duello **spezza la Catena** |
| **Spezzano la Catena** | Skullcrusher **smette di combattere per l'orda**. Non diventa alleato — è un drago nero — ma se ne va, e l'assalto alle mura perde le ali. *Esito «FUGGITO» garantito, senza doverlo ridurre a ⅓ pf* |
| **Uccidono Balvar prima dell'alba** | la runa resta (è incisa, non sostenuta), **ma** senza chi la rinnova si indebolisce: Skullcrusher parte con **−2 a tutto** e fugge a **metà** pf invece che a ⅓ |

⚠️ **È qui che il gruppo diventa un gruppo.** Artemis vede l'aura, Thorik legge
il nanico antico, Tordek arriva alla scaglia. Nessuno dei tre ce la fa da solo:
**è esattamente la scena che mancava all'arco.**

### Come si combatte, se si arriva a combatterlo

**Non ingaggiarlo in campo aperto**: non è un duellante, è un **preparatore**.
Ha **quattro rune già incise** nella tenda del comando, e le ha incise sapendo
che qualcuno sarebbe entrato:

1. sulla **soglia** — *dimensional anchor*: niente *Flee the Scene*, niente
   teletrasporti. **Chi entra, entra e basta.**
2. sul **palo centrale** — *blade barrier*, che scatta a taglio della tenda in
   due, separando il party;
3. **su di sé** — *silence*, che attiva a comando: chi conta sul verbale è
   fuori, lui no (le rune non richiedono componenti verbali);
4. la **quarta è vuota**, e la incide **durante** lo scontro. Falla vedere:
   *«continua a incidere mentre combattete»* è l'immagine che li terrorizza.

**Tattica**: *righteous might* al round 1, poi *blade barrier* e *slay living*
sul più fragile. Se scende sotto **30 pf** non fugge e non implora: **finisce
di incidere la quarta runa** e la lascia lì. `[DM: decidi tu cosa c'è scritto —
è un gancio bianco per ARC-09.]`

### L'eco a 1372 (il motivo per cui vale la pena)

Balvar è morto da mille anni comunque vada. Ma:

- se i PG hanno **pronunciato il suo nome**, in ARC-08 la Cronaca ha un
  pannello in più — e **Aegis Fang lo riconosce**;
- se hanno **spezzato la Catena**, il carry-over B4 verso **Fauci di Palude**
  cambia di tono: il figlio del drago incatenato ha una ragione in più per
  odiare i nani, o per **non** volere una catena addosso;
- se lo hanno **ucciso senza ascoltarlo**, resta una lastra d'ardesia incisa a
  metà tra le rovine del campo. Qualcuno, in ARC-09, l'ha trovata.

→ Registra l'esito nell'**Echo Ledger** (§7).

---

## §4 — BOSS: SKULLCRUSHER IL NERO (il duello — unico scontro tattico)

> **Mappa M7-B.** Il drago entra dall'alto (quota ~45 m) e picchia sul cortile
> interno. È il capostipite della stirpe di **Fauci di Palude**: ogni ferita che
> gli infliggete qui, la Forgia la ricorderà mille anni dopo (§7, carry-over B4).

> **Read-aloud (Salvatore lead).** *Prima arriva il freddo. L'ombra passa e
> l'aria del cortile perde dieci gradi in un respiro, e la pelle lo sa prima
> che lo sappiate voi. Poi il rumore: non un ruggito — un **risucchio**, come
> quando il mare si tira indietro prima di tornare. Le braci della forgia si
> piegano tutte nella stessa direzione. Un nano vicino a voi lascia cadere lo
> scudo e non si china a raccoglierlo.*
>
> *Dove atterra, la pietra fuma. L'acido gli cola dalle fauci chiuse e si
> mangia il selciato come acqua nella neve.*
>
> **Che fate?**

> 🎚️ **Se e solo se Thorik tiene Aegis Fang in mano** — *un secondo box, corto,
> e a lui soltanto*: **AEGIS FANG (non canta: urla, dentro il cranio):**
> *«SANGUE ANTICO. ARTEFICE DI LACRIME.»* — *e per un istante la Corona ti
> mostra due immagini sovrapposte: questo drago adesso, e un altro drago sopra
> mura che bruciano, che non hai mai visto.*

⚠️ **Perché è stato spezzato in due** *(2026-09-18)*. Il box unico portava
**nove nomi propri** e finiva su *«state per insegnare a quel sangue cosa vuol
dire aver paura»* — che dice ai giocatori cosa stanno per fare, cioè
**l'esito**. Adesso l'ingresso è **quello che il corpo sente** (freddo, il
risucchio, le braci che si piegano, lo scudo che cade), la visione è un
**micro-box per un solo PG** come chiede `ADR-0014` §1, e l'ultima riga è
**«Che fate?»** invece di una promessa.

```
============================================================
   SKULLCRUSHER IL NERO — il Primo Nero (GS 12) [verifica B5]
   Drago Nero Adulto potenziato · capostipite di Fauci di Palude
============================================================
Taglia: Enorme (Huge, 4,5 m) · Tipo: Drago (Terra, acido)
PF: 240 · CA 27 (−2 taglia, +19 nat) · tocco 8 · impreparato 25 · Iniz +4
BAB/Lotta: +22 / +39 (Enorme) · FOR 27 · DES 10 · COS 21 · SAG 15 · CAR 14
Velocità: Terra 12 m · Volare 36 m (scarsa)
Attacchi: Morso +26 (2d6+9) · 2 Artigli +21 (1d8+4) ·
          2 Ali +21 (1d6+4) · Coda +21 (1d8+13)
Full-attack (a terra): morso + 2 artigli + 2 ali + coda
Soffio ACIDO: cono 18 m, 12d4, Riflessi CD 24 ½, ricarica 1/1d4
Presenza Terrificante: CD 22 (Volontà o scossi), all'ingresso
Incantesimi da stregone (5°-6°) · Immune acido, sonno, paralisi
------------------------------------------------------------
NOTA D8 (party APL 13, 4 PG con artefatti): GS 12 è VOLUTO
"medio" — il duello dev'essere epico ma vincibile, perché il
vero climax è Fauci nel 1372. Non gonfiarlo: qui si SEMINA.
============================================================
```

> **🎚️ [FAST-PLAY] del duello** (se vuoi chiudere veloce): 3 scambi narrati a
> prova di gruppo (Attacco/Volare **CD 22**), poi si sceglie l'esito tra i tre
> sotto in base a quanti scambi i PG hanno "vinto" (0-1 = fuggito, 2 = ferito
> grave, 3 = ucciso). Registra comunque N ferite per B4. **[COMBATTIMENTO
> COMPLETO]** = la regia round-per-round qui sotto, su M7-B.

### 🎬 La regia dei primi due round — una battuta per attore *(ADR-0014 §1)*

> **Perché c'è.** Sotto trovi le tattiche **del drago**, che questo master aveva
> già e sono buone. Quello che mancava è l'altra metà, che `ADR-0014` prescrive
> dal luglio 2026 per **ogni** sequenza a battute e che esisteva in **un solo
> documento del repo**: i PG agiscono uno alla volta, e se ogni turno è un tiro
> senza descrizione il pathos evapora al terzo round.
>
> **Non sono numeri nuovi.** CD e danni restano quelli del §4. Qui c'è solo
> **cosa leggere, quando**, e sono sei secondi a testa.

**Apertura di round — cosa è cambiato nel mondo.** Prima di ogni giro, una riga
sola: *dove* è il drago (in cielo, in picchiata, a terra) e *cosa* ha lasciato
il round prima (una crepa, un nano che non si rialza, il fumo dell'acido).

**Il giro, in quattro battute** *(ordine di gioco dichiarato: chi ha vinto
l'iniziativa parla per primo, ma la descrizione segue sempre questo ordine)*:

| | Attore | Riuscita — **una riga** | Fallimento — **una riga, e non è «manchi»** |
|---|---|---|---|
| 1 | **THORIK** — regge | l'ascia entra fra due scaglie e ci resta un istante di troppo: il drago **si gira verso di lui**, ed è quello che serviva | il colpo scivola sulla scaglia bagnata d'acido. Thorik resta in piedi, ma adesso ha le mani che bruciano |
| 2 | **TORDEK** — colpisce | il pugno prende l'ala dove l'osso è sottile: un suono secco, e la picchiata si sbilancia | il drago si alza di un metro e il colpo passa sotto. Tordek finisce in avanti e per un momento **non vede dov'è** |
| 3 | **ARTEMIS** — sceglie il bersaglio | il blast arriva **all'occhio**, e per un round il drago tiene la testa girata di tre quarti | l'ombra si apre troppo presto. Il drago la vede arrivare e **ricorda da dove è partita** |
| 4 | **HELLA** — cambia il campo | le radici salgono dal cortile e chiudono una via di fuga: il drago **deve** restare | la pietra non risponde — qui la terra è giovane e non la conosce. Hella sente l'assenza, e le costa |
| 4-bis | **DURIK** — si mette in mezzo | il drago deve scavalcarlo per arrivare a Hella, e scavalcarlo gli costa il turno di picchiata | il soffio lo prende in pieno: la pietra **fuma**, e l'acido gli fa il 50% in più. Durik non arretra |

**Chiusura di round — l'avanzamento visibile.** Una riga che dica cosa è
**cambiato**, non quanti pf restano: la prima scaglia che manca, il fiato che si
accorcia, il primo passo indietro che il drago fa senza volerlo.

> **Round 1 — apertura da leggere.** *L'ombra passa sul cortile prima del
> rumore. Quando il rumore arriva, è il vostro stesso nome gridato da ottocento
> nani che hanno smesso di combattere per guardare in alto.*
>
> **Che fate?**

⚠️ **Dal round 3 si smette.** La regia serve a far **atterrare** l'inizio; se la
tieni per otto round diventa una lettura e il combattimento si ferma. Dal terzo
round si torna alle tattiche del drago qui sotto, e si descrive solo quello che
cambia davvero.

### Tattiche di Skullcrusher — regia round per round (stile RHoD, aggancio M7-B)
> Scritte dal punto di vista del drago. Skullcrusher è **giovane nella sua
> arroganza**: non ha mai perso, non sa ancora aver paura. È questo che i PG gli
> insegnano — ed è questo che il suo sangue ricorderà.

- **Round 1 — la Presenza.** Cala dall'alto (Presenza Terrificante CD 22:
  chi fallisce è scosso). Se la Scena 3 è finita «spettacolare», arriva **già
  in picchiata** e i PG perdono la prima azione. Apre col **Soffio acido** sul
  gruppo più fitto (Riflessi CD 24). *Non atterra: vuole restare in cielo, dove
  si sente un dio.*
- **Round 2-3 — il predatore aereo.** Resta in **quota**, picchia con Attacco in
  Volo (morso + coda) e risale — punisce chi non ha gittata o volo. Bersaglio
  preferito: chi lo ha ferito di più (l'arroganza non perdona l'insulto).
  *Momento Artemis*: in volo (Ali d'Ombra) è l'unico che lo raggiunge alla pari.
  *Momento Aegis Fang*: Thorik la **scaglia** — se colpisce in volo, incide la
  **Cicatrice a forma di martello** su un'ala (§7: −2 alla Volare di Fauci nel 1372).
- **Soglia ~⅓ pf (~80) — la prima paura.** Per la prima volta nella sua vita,
  Skullcrusher **esita**. È il momento dei tre esiti (sotto). Se i PG premono,
  può essere ucciso; se allentano, fugge nelle paludi. *«Qualcosa in lui — nel
  sangue — capisce che questi quattro non sarebbero dovuti esistere.»*
- **«La Forgia ricorda» (meccanica cardine).** **CONTA i colpi a segno** su
  Skullcrusher (ferite ancestrali, N≤3) — è il dato per il carry-over B4 (§7).
  Moradin, nella mente di Thorik: *«Ogni ferita che infliggi ora all'antenato,
  la mia Forgia la ricorderà quando affronterai il discendente.»*
- **La Cintura di Tordek RIFIUTA di attivarsi** qui (*«il vero scontro appartiene
  al futuro»*): coerenza col 1372, non nerf. È voluto — Tordek vince senza.
- **Sviluppi.** Comunque finisca (ucciso/ferito/fuggito), il sangue di
  Skullcrusher **sopravvive**: se ferito o fuggito, si ritira nelle paludi a
  leccarsi le ferite e a generare la stirpe che, mille anni dopo, culminerà in
  **Fauci di Palude**. Se **ucciso**, la stirpe nasce comunque (aveva già figli):
  la profezia non spezza il sangue, lo **segna** (carry-over B4). In ogni caso,
  con il drago via, l'orda perde lo sprone e si sfalda entro poche ore (→ Scena
  6). Se Skullcrusher ha **visto** Aegis Fang scagliata, il terrore di
  quell'arma entra nel sangue: Fauci, mille anni dopo, la riconoscerà (gancio
  inverso B4).

### 🏟️ IL CORTILE — cosa c'è, e cosa ci si può fare che qui non è scritto

> **Perché questa tabella esiste.** Il duello aveva la regia, le tattiche del
> drago e la scalatura, ma **niente sull'arena**: un tavolo che volesse essere
> furbo non trovava appigli, e restava l'iniziativa. Qui non ci sono soluzioni
> pronte — ci sono **cose**, e una riga su cosa succede se qualcuno le usa.
> Per tutto il resto vale il §0-ter: **assorbi, poi rilancia**.

| Nel cortile c'è | Se qualcuno lo usa |
|---|---|
| **Le corde degli arieti**, tese e bagnate | tirarle mentre è basso: Lotta contrapposta con **+4** per la leva. Non lo atterra: gli **inchioda un'ala a terra per un round**, ed è tutto quello che serve |
| **La fucina originale**, accesa da stanotte | ci si può spingere dentro qualcosa. Il drago è **immune all'acido, non al calore della forgia**: 4d6 e — più utile — il fumo gli toglie l'olfatto per 1d4 round |
| **La cisterna sotto il pozzo** | l'acido colpisce l'acqua e **ribolle**: nuvola che oscura, −4 agli attacchi di tutti. Danneggia i PG quanto lui. È una **scelta**, non un trucco |
| **Le campane della torre nord** | il suono nell'aria fredda copre il battito d'ali: chi le suona toglie al drago il vantaggio del suono in picchiata (e si fa **bersagliare**) |
| **Ottocento nani che guardano** | chiamarli è gratis. Arrivano, **e muoiono**: tira sul Registro delle Perdite di ARC-08. Il drago fa un attacco pieno su di loro invece che sui PG. Nessuno lo dice al tavolo prima |

🚫 **Cosa NON dire.** Che la fucina funziona contro di lui. Se lo dici, la
tabella diventa un elenco di mosse; se aspetti, resta un cortile. Il DM **non
legge questa tabella ai giocatori**: la tiene sotto gli occhi e risponde.

⚠️ **E se hanno un'idea che non è in tabella**, la risposta è già scritta in
§0-ter: sì, e adesso c'è un problema nuovo. **Questa tabella è un esempio di
tono, non l'elenco delle cose permesse.**

### ► ESITO DEL DUELLO (aperto — MAI fisso) → carry-over B4 (§7)

`[HDYWTDT — il finisher a chi mette a terra il drago. «Com'è che lo fai?», e
aspetta. È il momento più grosso della campagna finora: non riempirlo tu.]`

1. **UCCISO** (0 pf): impresa immensa, la profezia in pieno. → Fauci nel 1372
   parte con **−10% PF** e Presenza ridotta contro i portatori (B4).
2. **FERITO GRAVE** (fugge sotto ⅓ pf): esito "medio", il più probabile. →
   Fauci perde **un uso del soffio** (B4).
3. **FUGGITO** (i PG scelgono la sopravvivenza / non lo intaccano): quasi illeso,
   ma **vi ha visti e riconosciuti**. → Fauci **+2 iniziativa** ma morale
   fragile (fugge sotto 75 pf invece di 50) (B4).
*Registra esito + N ferite + se Aegis Fang colpì in volo.*

### Sidebar — Scalare lo scontro (stile RHoD)
| Situazione | Aggiustamento |
|---|---|
| Party **straripante** (4 PG L14, tutti gli artefatti, aiuti pieni Sc.2) | Skullcrusher **avanzato a Vecchio (GS 14)**: PF 300, soffio 14d4 CD 26, +2 a tutti gli attacchi; oppure 2 **wyvern** scortano il drago dai round 2 |
| Party **logorato** (Sc.3/4 fallite, risorse spese, Hella ancora fragile) | Skullcrusher NON usa il soffio 2 volte di fila; a ⅓ pf **fugge subito** (esito FUGGITO garantito) invece di premere |
| **Hella appena risorta** — vuoi proteggerla | Il drago la ignora finché non lo ferisce (predatore: va per la minaccia, non per la novità) — dà alla giocatrice spazio per il suo primo scontro |
| Un PG **abbattuto** | Skullcrusher lo ignora (caccia chi è in piedi e lo minaccia): finestra per stabilizzarlo |

---

## §4-quater — IL RITUALE DELLA FORGIA ETERNA `[CANONE — state.md §5; D-B/D-A, DM 2026-09-19]`

> **Cos'è, e perché esisteva solo in `state.md`.** Questo viaggio **è** il
> **Rituale Legacy 4**, che la matrice degli artefatti chiama *«Siege of the
> Eternal Forge»*. `state.md` §5 dice che **Corona +3, Senzienza e Rubino si
> sbloccano qui**. Fino a oggi il master consegnava il duello e basta: il DM
> tornava dal tavolo a segnare un avanzamento che nel modulo non era successo.
>
> ⏱️ **Quando** *(decisione DM)*: **dopo il combattimento**, sull'esito
> dell'incontro. Non è una prova sotto pressione ed è **senza ulteriori costi** —
> il prezzo di questo arco Thorik lo ha già versato altrove.

### Il rito si fa comunque. Cambia il tono, non l'esito

Il canone di §6 è esplicito: la fortezza regge perché **la profezia è incisa**.
Anche un duello andato malissimo finisce con gli antenati che ricacciano il
drago. Quindi il Rituale **non si fallisce**: si gioca in una delle quattro voci
che l'incontro ha appena scelto.

| Esito del duello | La voce del rito | La riga che il DM dice |
|---|---|---|
| **UCCISO** | trionfo, e un imbarazzo | i nani antichi non sanno se inginocchiarsi o abbracciarli, e provano tutti e due |
| **FERITO GRAVE** *(il più probabile)* | mestiere | nessuno canta. Si conta chi manca, poi si accende la pietra |
| **FUGGITO** | sollievo con un'ombra | il drago vi ha visti. Il rito si fa lo stesso, e qualcuno guarda il cielo mentre si fa |
| **VINTO SPORCO** *(§6, gli avi intervengono)* | misericordia e dovere | siete venuti a salvarli, e vi hanno salvati loro. La pietra si accende uguale, e pesa di più |

### La scena, in tre momenti

> **Read-aloud (LotR lead) — l'incudine.** *Quello che chiamano altare è
> un'incudine, e si vede: il piano è segnato da mille anni di martelli. Intorno
> non c'è un tempio, c'è un cortile pieno di feriti. Un nano molto vecchio
> appoggia sull'incudine una pietra rossa grande come una noce, e si tira
> indietro di un passo. Nessuno spiega niente. Tutti guardano la corona.*

**Momento 1 — la pietra entra.** Il Rubino trova il suo incasso, quello che per
tutto l'arco non rifletteva la luce. Non serve un tiro: **la Corona lo prende da
sé**, come una serratura che riconosce la chiave. La Corona passa a **+3**.

> **Read-aloud (Salvatore) — l'incasso che si chiude.** *Il vuoto sulla corona
> si riempie e smette di essere un vuoto. Per la prima volta da quando Thorik
> l'ha in testa, l'oro torna indietro da tutte e tre le pietre, e la luce che ne
> esce non è di nessuna delle tre: è di quello che adesso sono insieme. Il metallo
> gli si scalda contro la fronte, poi si raffredda, e resta caldo come una mano.*

**Momento 2 — la Corona parla, o non lo fa.** Qui **si incassa la promessa di
`ARC07-DEF-3` §5**, e i due rami sono già canone:

| Al rito di DEF-3, Thorik… | La Senzienza arriva | E la prima cosa che dice |
|---|---|---|
| **ha donato** il +2 di deflessione | **sveglia**, e con qualcosa da dire su di lui | *«Tre volte hai pagato tu. La terza non te l'ho chiesta io.»* |
| **ha rifiutato** | **fredda**: i poteri sì, il tono no | una voce corretta e senza calore, che dà informazioni e non commenti. ⚠️ **Reversibile**: si scalda in ARC-09, quando lui rischia qualcosa di suo |

> 🎭 **Grigio politico.** La Corona **non è dalla parte di Thorik**. Il suo
> *Want* è la montagna, non il portatore: ha accettato tre gemme e un pegno
> perché le servivano, e lo dirà con la stessa calma con cui dice tutto il resto.

**Momento 3 — Aegis Fang si sveglia** *(decisione DM: è una scena, non una riga
di scheda)*. `state.md` §5 dice: *«Unchanged until the Siege is won → then Stage
1 full awakening»*. L'Assedio è questo, ed è appena stato vinto.

> **Read-aloud (Mercer lead) — l'ascia prende la parola.** *L'ascia si scalda
> nella mano di Thorik, e non è il calore della forgia. È la prima volta in tre
> anni che si fa sentire senza essere interrogata. Nel cortile nessuno se ne
> accorge, perché nessuno sta guardando le armi.*

- **AEGIS FANG (Ego 14, servo del popolo nanico prima che del portatore):**
  *«Ho visto. Non chiedo più.»* — se al rito di DEF-3 Thorik **ha donato**.
- **AEGIS FANG:** *«Ho visto anche cosa non hai dato.»* — se **ha rifiutato**.
  L'ascia non lo abbandona: lo **guarda**, e il giudizio finisce la prima volta
  che lui rischia qualcosa di suo per Hella.

> **`[HDYWTDT]`** Il primo uso dello Stage 1 non lo descrive il DM. Si chiede al
> giocatore di Thorik: *«L'ascia parla, e per la prima volta non risponde a una
> domanda. Cosa ti dice, e tu cosa fai con quella frase davanti a ottocento nani
> che ti stanno guardando?»*

> **Chiusura.** Tre pietre accese, un'ascia che ha appena parlato, e un cortile
> che non sa ancora di essere una leggenda. **«Che fate?»**

### ⚠️ Due cose per il DM, e una da decidere

- **Il Rubino è a uso singolo e si spende nel ritorno** (D16, `DEF-5` §3). Non
  è un potere nuovo in tasca: è il motore del viaggio di casa.
- **Non ci sono altri costi qui** — né TS, né pegni, né punti caratteristica.

### Momento 4 — l'Aura della Forgia Eterna `[CANONE — DM 2026-09-20]`

**Il quarto potere, quello che la Corona non aveva mai avuto.** La matrice
degli artefatti lo chiama *Aura of the Eternal Forge* e lo dà al **Rituale 4,
alla vittoria nella battaglia antica**. È adesso.

| Chi | Cosa riceve |
|---|---|
| **I quattro** | *Possenza Divina* e *Protezione dal Male* |
| **Ogni nano entro 30 metri** | *Possenza Divina*, *Protezione dal Male*, *Benedizione*, e un uso di *Scolpire Pietra* |
| **Thorik** | irradia **+4 di morale** ad attacchi e tiri salvezza per ogni nano che lo veda |
| **I nemici dei nani** | **Volontà CD 20** o **scossi** per 1 minuto |

⏱️ **Durata e cadenza**: dura **fino all'alba** la prima volta, e da allora
resta alla Corona come potere **1/settimana**. Non è una ricarica: è la cosa
che la Corona sa fare da quando è intera.

> **Read-aloud (LotR lead) — l'aura.** *Il vecchio che ha posato la pietra
> alza la testa, e non guarda Thorik: guarda dietro di lui. In tutto il
> cortile i feriti stanno smettendo di essere feriti. Un fabbro con una
> gamba sola si tira su appoggiandosi al muro, e il muro gli si apre sotto
> la mano come argilla, e lui ci infila la gamba e resta in piedi. Nessuno
> grida. Ottocento nani guardano un uomo con una corona e capiscono, tutti
> insieme e senza parlare, di essere dentro una storia che verrà raccontata.*

⚠️ **Tre cose per il DM, e la prima è di bilancio.**

- **L'Aura arriva DOPO il duello, non prima.** L'innesco è *«vittoria nella
  battaglia antica»*, non l'arrivo: `§4` resta tarato come è scritto, e nessun
  numero di Skullcrusher va toccato. 🔎 Una fonte d'artefatto più vecchia la
  dava *«automatica all'arrivo»*, ed è una mappatura superata — quella
  descriveva un Rituale 4 di una scena sola.
- **Metà dell'Aura la giocate già**, sotto un altro nome. La **Guarigione del
  passaggio** di `§3 SCENA 1` — pf pieni, usi ricaricati, niente tiri — è la
  metà curativa di questo stesso potere, attribuita al portale. Resta lì e non
  si somma: qui arriva **solo la metà che potenzia**.
- **Il Manto di Pietra e Spirito NON è di questo rituale**, e il giocatore lo
  sa: è sulla sua scheda dal **Rituale 3**, riga «Rit. 3», *Mente Vuota*
  permanente e RD 5/epico. La riga della matrice che lo dava qui era una
  mappatura vecchia, ed è stata corretta.

---

## §4-bis — ZOG'TAR DEATHEYE & PNG antichi (per [COMBATTIMENTO COMPLETO])

> Statblock e tattiche per chi gioca l'infiltrazione + boss su griglia (§3
> modalità completa). In [FAST-PLAY] bastano CR e l'assalto coordinato.

```
============================================================
   ZOG'TAR DEATHEYE — generale della Mano Rossa (GS 14)
   Mezzo-Ogre/Orco · Barbaro 10 / Guerriero 4 · Grande · CM
============================================================
PF: 230 (14 DV) · CA 24 (−1 taglia, +10 arm. completa, +3 DES, +2 nat)
   tocco 12 · impreparato 21 · Iniz +3
BAB/Lotta: +14 / +26 · Velocità 12 m
FOR 26 (32 in Ira) · DES 16 · COS 20 · INT 12 · SAG 12 · CAR 14
Attacco: Ascia a due mani +1 +26 mischia (3d6+15, 19-20/×3) in Ira
Full-attack: +26/+21/+16 (3d6+15)
TS: Tempra +16 · Riflessi +8 · Volontà +7 (+2 in Ira)
------------------------------------------------------------
• Ira Barbarica Superiore (3/g): +6 FOR, +6 COS, +3 Vol, −2 CA, 10 round
• RD 5/— · Presenza Minacciosa: entro 9 m, Vol CD 20 o scosso 1d4 round
• Colpo Possente: fino a −10 TxC per +20 danni (Attacco Poderoso migliorato)
• OCCHIO DI OSSIDIANA (artefatto minore maledetto, incastonato al posto
  dell'occhio destro — decisione DM 2026-09-24): 3/g azione di movimento,
  marca un bersaglio → −2 CA contro Zog'tar e +2 danni subiti da lui, 5 round.
  Prezzo: Zog'tar è VULNERABILE alla luce divina (Luce di Lathander/Corona).
Talenti: Attacco Poderoso, Ira Extra, Critico Migl. (ascia), Arma Focalizzata
   & Specializzata (ascia), Robustezza, Iniziativa Migliorata.
GUARDIE (4): Hobgoblin Guerriero 8 · CA 20 · PF 60 · spadone +14 (2d6+6)
============================================================
```

### Tattiche di Zog'tar — round per round (stile RHoD)
> È un macellaio arrogante che si crede immortale: non conosce la paura finché
> non gli entra nelle ossa. Non sa che la Morte è già nella tenda.

- **Round di sorpresa** (se i PG sono invisibili e silenziosi): il party ha un
  round pieno. *È qui che si vince o si complica.* Un colpo coordinato può
  portarlo subito sotto metà.
- **Round 1** (se reagisce): **Ira Barbarica** (*«A ME, CANI! ABBATTETE LE
  OMBRE!»*) + **Occhio di Ossidiana** su Thorik (la minaccia). Le 4 guardie
  ingaggiano i PG più esposti.
- **Round 2-3**: carica il bersaglio che fa più danni, **Colpo Possente**
  moderato (−5/+10) se ha colpito bene. Se Artemis lo martella, si gira su di lui.
- **Soglia 30% pf**: combatte disperato, cerca di **portare un PG con sé** nella
  morte (un ultimo Colpo Possente pieno −10/+20).
- **Sviluppi.** Zog'tar **muore in questa scena** (la storia dice così), ma il
  COME conta (esito §3). `[HDYWTDT — il finisher a chi lo abbatte: «com'è che
  lo fai?», e aspetta. Se non vuole, una riga tua e si va avanti.]` Alla sua morte, l'Occhio di Ossidiana si spegne; il
  campo perde il direttore. *Se catturato/interrogato invece che ucciso*: Moradin
  approva la saggezza pragmatica (nessun tono «nessuna pietà» sul Rubino).

### Le scelte-costo dei PG contro Zog'tar (interazioni d'artefatto)
> ⚠️ **Niente tentazione Lathander/Mask per Artemis** (mai giocata, §1). Le sue
> scelte qui sono **tattiche e morali**, non divine.
- **THORIK — Benedizione della Forgia**: può chiedere a Moradin +2 sacro ai
  danni vs Zog'tar e guardie, al **costo di 1 livello di affaticamento** dopo la
  battaglia (peserà su Skullcrusher). *Scelta: potenza ora vs freschezza al drago.*
- **THORIK — finire o interrogare Zog'tar**: colpo finale spettacolare → il
  Rubino registra «nessuna pietà» (tono §7); interrogarlo → «saggezza pragmatica».
- **TORDEK — Cintura della Devastazione**: 3 cariche/giorno (+2d6/+3d6/+4d6). Se
  le brucia tutte per l'overkill, la Cintura lo «assaggia»: contro **Fauci nel
  1372** dovrà superare **Volontà CD 18** per non cedere all'aggressività. Se
  **modera** (1-2 cariche, colpi mirati) → Moradin gli concede **+1 sacro ai TS
  vs paura** in futuro. *(Nota: contro Skullcrusher la Cintura si rifiuta, §4.)*
- **ARTEMIS — pulito o spettacolare**: uccidere Zog'tar in **silenzio** (blast
  mirato) tiene basso l'allarme; ucciderlo in modo **spettacolare** (esplosione
  davanti alle guardie) sparge terrore ma **fa infuriare Skullcrusher** (§4
  inizia in picchiata). È il suo bivio da predone: efficienza vs leggenda.
- **HELLA — controllo o distruzione**: *Intralciare* fuori dalla tenda blocca i
  rinforzi (controllo); fulmini/spine (distruzione). Nessun effetto meccanico
  immediato, ma orienta come gli spiriti/Moradin la giudicheranno alla battaglia
  di Rethmar (ARC-09): bonus a controllo-campo o a danni elementali.
- **XP Zog'tar**: ~5.000 totali (~1.250/PG).

### DURIN ROCCIADURA — la guida (PNG antico, §1-bis)
Nano Guerriero 6 · PF 52 · CA 22 (arm. completa +1, scudo) · BAB/Lotta +6/+10 ·
Ascia Doppia +1 +9 (per lato, 1d8+5, 19-20/×3) · TS Temp +8, Rifl +2, Vol +3 ·
FOR 18, COS 16, SAG 14. **Onesto e leale fino alla morte** una volta convinto;
antenato di Othrek (Hammerfist 1372). *Se muore alle mura (Scena 4), la Cerimonia
delle 100 Asce (ARC-08) può portarne il nome — eco commovente.*

---

## §5 — VATORE (Sal a −1000: la scena grigia + la sincronizzazione)

> **La scena "molto bella" (canone `Bestiario/villain/Salvatore/Salvatore.md`).**
> Opzionale ma consigliata: durante l'infiltrazione (Scena 3) o nel caos delle
> mura (Scena 4), i PG **incrociano un ladro** che non c'entra con l'orda — un
> uomo incappucciato che si muove tra le tende con troppa grazia, un fagotto
> stretto al petto. È **Vatore**: mille anni prima di diventare **Salvatore
> "Sal" della Luna d'Argento**, il mercante-spia che li tradirà in ARC-09. Loro
> **non possono saperlo**. Questo è il cuore grigio della scena.

**Chi è, adesso.** Vatore, il "Ladro d'Ombra" di Hammerfist. Ha **appena rubato
il Sigillo di Ossidiana** (§Artefatto ↓) e pianifica la fuga nel futuro (userà un
Cronolito). Ha appena visto **quattro individui respingere un'orda da soli** — e
ne è **ossessionato**. Personalità: freddo, parla il meno possibile, li osserva
con un **terrore reverenziale mal mascherato**.
> **Canone (DM 2026-07-23) — cosa lo corrompe.** Vatore è **già marcio di
> avidità e sete di potere**: non gli importano le conseguenze. Ha rubato il
> Sigillo *sapendo* che divora anime — e ha deciso che le pagherà con quelle
> degli altri, e poi con la propria. È questa scelta, non un incidente, a
> renderlo **Sal**. Nella scena non è un innocente ingenuo: è un uomo che ha
> già scelto l'ombra, e che ora vede in VOI un potere che vorrebbe rubare.

> **Read-aloud (Andor lead — l'incontro che non capiscono).** *Tra due tende, un
> uomo. Non è dell'orda: veste ombre cucite bene, e stringe al petto qualcosa
> avvolto in un panno. Vi guarda — e nei suoi occhi non c'è l'odio del nemico:
> c'è TERRORE. Il terrore di chi ha appena visto un mito camminare. Non attacca.
> Non scappa nemmeno, subito. Vi fissa come si fissa qualcosa che non dovrebbe
> esistere, e sussurra, più a sé stesso che a voi: «…quattro. Eravate davvero in
> quattro.» Poi la maschera torna: un sorriso freddo, un passo indietro verso
> l'ombra. Artemis — il tuo Anello è diventato gelido. Quell'uomo non è di qui.
> Non di QUESTO tempo.*

**Le risposte del party (grigie — non sanno cosa diventerà):**

| Approccio | Prova | Cosa succede | Eco su Sal nel 1372 (ARC-09) |
|---|---|---|---|
| **Lo ignorano / lo lasciano andare** | — | Vatore svanisce nell'ombra col Sigillo. | Sal esiste "intatto" in ARC-09 — nessun vantaggio, ma nessun sospetto reciproco. |
| **Gli parlano** (Intuizione/Diplomazia CD 18) | 18 | Vatore, terrorizzato, lascia sfuggire un frammento: *«Voi non morite. L'ho letto. Nelle cronache che non sono ancora scritte.»* Poi fugge. | In ARC-09 Sal **esita** un istante di fronte a loro (li ha già temuti mille anni fa): +2 dei PG a Intuizione/Diplomazia contro Sal la prima volta. |
| **Lo derubano** (Furtività/Rapidità di Mano CD 22) | 22 | Gli sfilano il **Sigillo di Ossidiana** (o parte del bottino). | In ARC-09 Sal si presenta **senza** un asso che avrebbe avuto (il DM toglie a Sal un oggetto/piano — es. l'Olio di Sabotaggio parte scarico). |
| **Lo feriscono** (attacco riuscito) | — | Vatore urla, sanguina, attiva il **Cronolito** e sparisce nel tempo. | **Sincronizzazione**: nel 1372 **Sal sanguina nello stesso punto**, all'improvviso, davanti a chi lo osserva (la maschera vacilla) — i PG lo **riconoscono** come "l'uomo del passato" se collegano i punti. |
| **Cercano di ucciderlo** | scontro breve | Non muore qui (il Cronolito lo salva a 1 pf: *deve* sopravvivere per esistere nel 1372 — paradosso auto-consistente). | Sal in ARC-09 porta una **cicatrice antica** e un odio personale: sa che loro ci hanno provato. Nemico più cattivo, ma più fragile emotivamente. |

> **Perché è grigia (nota di tono).** I PG hanno davanti un ladro spaventato che
> **non ha ancora fatto nulla** — ma che (loro non lo sanno) diventerà un
> traditore. Ucciderlo "preventivamente" è un atto oscuro contro un innocente-per-
> ora; lasciarlo andare significa (senza saperlo) crescere il proprio nemico. Non
> c'è scelta pulita. **Registra tutto**: paga in ARC-09. *(Il paradosso regge
> sempre: Vatore DEVE sopravvivere per diventare Sal — il Cronolito lo garantisce.
> I PG possono segnarlo, derubarlo, terrorizzarlo, non cancellarlo.)*

> **Registrazione**: annota l'esito in `state.md §7` (thread «[VATORE/SAL]») e
> nell'Echo Ledger (§7). Cross-link: `Bestiario/villain/Salvatore/Salvatore.md`
> §Sincronizzazione.

### 🖤 ARTEFATTO — IL SIGILLO DI OSSIDIANA (minore, allineato a Shar) `[CANONE — DM 2026-07-23]`

> **Cos'è.** Un sigillo/anello-sigillo di **ossidiana nera**, gelido al tatto,
> che «beve» la luce intorno; inciso con la runa-vuoto di **Shar** (Signora della
> Notte, dea di perdita, oscurità e segreti). È ciò che Vatore ha appena rubato,
> e ciò con cui diventerà **Sal**. Shar è più pertinente di Mask perché il
> **prezzo è la perdita di anime**, non solo il furto.

| Potere | Effetto |
|---|---|
| **1 · Manto di Notte Assoluta** (passivo, gratis) | Entro **9 m** dal portatore gli incantesimi di **luce** di livello ≤2 sono **soppressi**; *daylight* e superiori richiedono **prova di livello incantatore CD 20** o falliscono. La luce non-magica è solo attenuata (penombra). |
| **2 · Furto della Notte** (1/giorno, azione) | Il portatore compie **un'azione furtiva** (furto, colpo, passaggio) come se fosse **invisibile e silenzioso** per **1 round**. NON attivabile in piena luce naturale. |

> **⚖️ IL PREZZO — «consuma anime» (il cuore oscuro dell'oggetto).** Ogni uso del
> **Potere 2** — e ogni giorno in cui il **Potere 1** resta attivo oltre la prima
> ora — **divora un'anima**: infliggi **1 livello negativo** a una creatura
> senziente **toccata nelle ultime 24 h** (il Sigillo «raccoglie» il pegno), o
> consuma un'**anima intrappolata** (gemma-spirito, non-morto legato). **Se
> nessuna anima è disponibile, consuma il PORTATORE**: 1 livello negativo a sé,
> che diventa **permanente** dopo 24 h se non redento (*restoration*). È il
> meccanismo che trasforma **Vatore in Sal**: lo usa sugli altri, poi su sé
> stesso, e la **sete di potere lo acceca** al conto che sta accumulando.

> **⚔️ AGGANCIO — l'Anello di Artemis (Lathander vs Shar).** L'Anello Riforgiato
> di Artemis porta una **scintilla di Lathander** (dio dell'**Alba**, nemesi
> cosmica di Shar). Se **Artemis** impugna il Sigillo, i due artefatti si
> **annullano a vicenda**: (a) il Manto di Notte **non può sopprimere** la luce
> d'Alba dell'Anello; (b) i **poteri di luce/alba dell'Anello diventano
> instabili o non disponibili** finché porta il Sigillo — e viceversa il Sigillo
> è **soppresso** in sua mano. Artemis deve **scegliere quale servire**: Notte o
> Alba. È il suo **bivio d'artefatto per l'ARC-09** (se lo prende lui, il DM lo
> gioca come una lotta interna tra i due patroni; se lo prende un altro PG, il
> prezzo delle anime è pieno).

> **Gancio ARC-09.** Se i PG lo **rubano a Vatore** e lo riportano nel presente
> (paradosso auto-consistente del Cronolito), Sal si presenta **senza il suo
> asso** e la **sincronizzazione** con lui si complica (vedi tabella §5). Scheda
> speditiva → `Bestiario/villain/Salvatore/Salvatore.md` §Sigillo; thread
> `state.md §7 [SIGILLO DI OSSIDIANA]`.

---

## §6 — CONTINGENZE & SCONFITTA

| Mossa | Risposta del modulo |
|---|---|
| **Vogliono cambiare il passato** (salvare qualcuno destinato a morire, avvisare i nani di eventi futuri) | Timeline auto-consistente: ci **provano**, ma "va sempre come doveva". Il nano che vogliono salvare muore comunque, in un altro modo. Non è fato crudele: è che **è già successo**. Ottimo pathos, zero paradossi. |
| **Cercano tesori/conoscenze da riportare nel futuro** | Possono! Ma la maggior parte **non attraversa** il Rubino (solo ciò che è "loro" torna — corpi, artefatti legati). L'**eccezione canonica** è il **Sigillo di Ossidiana** rubato a Vatore (§5 Artefatto): il Cronolito che lo lega a Vatore lo fa «passare» come gancio ARC-09. |
| **Vogliono reclutare Thorgrim / portarlo nel futuro** | Impossibile (non è "loro"): Thorgrim resta, e la sua eco è la Cerimonia delle 100 Asce (ARC-08). Commovente: si separano da un fratello che è già polvere da mille anni. |
| **Evitano del tutto il duello con Skullcrusher** | Difficile ma possibile (montaggio): allora il Rubino si accende comunque (la fortezza regge), ma **senza ferite ancestrali** → nessun carry-over B4 (Fauci al 1372 a piena forza). La scelta ha un prezzo futuro. |
| **FALLIMENTO — il duello va malissimo / un PG cade / fuggono sconfitti** | Non c'è TPK: la timeline **esige** che vincano (la profezia È incisa). Se il combattimento crolla, Thorgrim e gli antenati **intervengono** e ricacciano il drago (a caro prezzo: molti nani antichi muoiono — pathos, e la Cerimonia delle 100 Asce ne porterà i nomi). I PG vincono "sporco": **nessuna ferita ancestrale** registrata, il Rubino si accende col tono «misericordia/dovere», e portano il peso di essere stati salvati dagli avi che erano venuti a salvare. |

---

## §7 — ECHO LEDGER (le conseguenze che attraversano gli archi)

| Evento (qui) | Eco | Quando riemerge | Dove si gestisce |
|---|---|---|---|
| **Esito del duello con Skullcrusher** (§4) | UCCISO/FERITO/FUGGITO → effetto quantificato su Fauci di Palude | ARC-08 (boss di Hammerfist) | **`PortaleForgia-P5-B4-CARRYOVER-Forgia-Ricorda.md`** + statblock Fauci ARC-08 |
| **Ferite ancestrali segnate** (N≤3) | +N TxC **o** +Nd6 ai portatori vs Fauci; Aegis Fang in volo → cicatrice d'ala (−2 Volare Fauci) | ARC-08 | B4 §3 |
| **Aegis Fang «sente» Fauci** (gancio inverso) | +2 circostanza a Thorik vs Fauci + preavviso del soffio | ARC-08 | B4 §4 |
| **Vatore segnato/derubato/ferito** (§5) | sincronizzazione su Sal nel 1372 (sanguina / manca un asso / vi teme) | ARC-09 (Sal mercante-spia) | **state.md §7** + `Bestiario/villain/Salvatore/` |
| **Seme del Ghostlord** (§1-bis, incontro con Zeth) | i PG assistono all'inizio della Lichificazione di Zeth (mano del Collezionista attraverso il tempo) | ARC-09 (dilemma etico di Hella su Zeth il Murato) | **state.md §7** + `Bestiario/villain/Ghostlord/` |
| **Scelte-costo vs Zog'tar** (§4-bis) | Thorik affaticato / Cintura di Tordek «assaggiata» o disciplinata / tono del Rubino | ARC-08 (vs Fauci) | §4-bis + B4 |
| **Tono del Rubino** (esito duello) | «nessuna pietà» (UCCISO) / «dovere» (FERITO) / «vigile» (FUGGITO) → colore della Corona in ARC-08 | ARC-08 ingresso | `ARC07-CONSEGUENZE-ECHI.md` §2 |
| **La Senzienza arriva calda o fredda** (§4-quater) | il ramo lo ha deciso `DEF-3` §5: se Thorik ha donato il +2 di deflessione la Corona **commenta**, se ha rifiutato **informa e basta**. ⚠️ Il freddo e' **reversibile** | ARC-08 e ARC-09, ogni volta che la Corona parla | `state.md` §5 · `ARC07-CONSEGUENZE-ECHI.md` |
| **Aegis Fang allo Stage 1** (§4-quater) | l'ascia ha smesso di interrogare Thorik — **oppure** lo giudica, e il giudizio finisce la prima volta che lui rischia qualcosa di suo per Hella | ARC-08, alla prima scena che riguarda Hella o nani da proteggere | `Bestiario/` scheda Aegis Fang + `state.md` §5 |
| **La prima frase dell'ascia, detta dal giocatore** (`[HDYWTDT]`, §4-quater) | quella frase e' canone: ottocento nani l'hanno sentita, e a Hammerfist qualcuno la **ripetera' storta** | ARC-08, arrivo al Cuore della Montagna | `ARC07-CONSEGUENZE-ECHI.md` |
| **Cronache dei Quattro Eroi compiute** | fama crescente presso i nani → Custodi Eterni | ARC-08 E5 / Cerimonia 100 Asce | ARC-08 |
| **Sigillo di Ossidiana** (se rubato a Vatore) | artefatto di Shar (anti-luce / furto d'ombra, divora anime) — vedi §5 Artefatto; contrasta l'Anello di Artemis | ARC-09 | `state.md §7 [SIGILLO DI OSSIDIANA]` + `Bestiario/villain/Salvatore/` |

---

## §8 — AVANZAMENTO (budget PX per scena + tesoro pregenerato)

### A. Budget PX del beat (party 4 PG, APL 13 · fast-play)
| Scena | Tipo | PX/PG `[verif. ✓ ERRATA/TESORO-WBL 2026-07-23]` |
|---|---|---|
| Sc.1-2 Cronache + Thorgrim | storia/social | 600 |
| Sc.3 Infiltrazione + Zog'tar (GS 14, risoluzione veloce) | combattimento veloce | 2.400 |
| Sc.4 Mura | montaggio/eroico | 600 |
| §5 Vatore (scena grigia, qualunque esito) | roleplay grigio | 500 |
| **§4 Skullcrusher (GS 12, unico scontro tattico)** | boss | **2.700** (party 4, APL 13) |
| Sc.6 Rubino + profezia compiuta | premio di storia maggiore | 800 |
| **TOTALE beat** | | **~7.600/PG** |

> Sommato a Terra (~11.600) + Affreschi (~1.900) + Resurrezione (~1.900), il
> party **matura il 14° verso Hammerfist** (D8). Le parti giocate non si ritoccano.

### B. Tesoro PREGENERATO (i doni di Re Thorek I + il bottino del passato)
| Dove | Oggetto (pregenerato) | Valore |
|---|---|---|
| Sc.2 (Thorgrim/Re Thorek I, se fiducia piena) | **Benedizione degli Antenati**: 4 **Pozioni di Cura Ferite Serie** dell'antica fucina (curano 3d8+11) | ~3.000 mo |
| Sc.2 (dono cerimoniale) | **Torque di Thorek I** — monile nanico antico (+1 sacro ai TS vs paura; e nel 1372 è una **reliquia storica**: i nani si scoprono il capo davanti a chi lo porta) | ~2.000 mo + valore storico |
| §5 (se derubano Vatore) | **Sigillo di Ossidiana** — artefatto minore di Shar (Manto di Notte + Furto della Notte, divora anime; contrasta l'Anello di Artemis — scheda §5 Artefatto) | speciale (gancio ARC-09) |
| Sc.4 (bottino dell'orda antica, se sabotano gli arieti) | armi orchesche primitive (poco valore) + un **corno da guerra di ferro nero** (curiosità, 300 mo) | ~300 mo |
| §4 (resti di Skullcrusher, se UCCISO) | **scaglia del Primo Nero** — trofeo: materiale per **1 oggetto ad acido** (arma/armatura +1d6 acido, o focus per incantesimi acidi; a discrezione del fabbro), e prova che la profezia è compiuta | ~1.500 mo |

> ⚠️ **Cosa torna nel 1372**: solo ciò che è "loro" o legato (corpi, artefatti,
> il Sigillo rubato). Le pozioni consumate qui restano qui; i doni indossati
> tornano. Il DM decida caso per caso (§6).

---

## §9 — PONTE al master #5 + HANDOUT & ASSET

**Ponte.** Il Rubino acceso, la profezia compiuta, la Corona a **tre gemme**: la
luce strappa i quattro al passato. Ma non tornano nella Sala della Forgia da cui
erano partiti — il Rubino, «Cuore della Leggenda», li deposita **dove serve**:
al **Cuore della Montagna**, sotto Hammerfist, il **Giorno 3 dell'assedio del
1372**, mentre la fortezza brucia sopra di loro. → **master #5: il Ritorno a
Hammerfist** (la cucitura D16, il raccordo all'ARC-08).

### Handout giocatore
1. **Le Cronache dei Quattro Eroi** — la pagina di profezia da consegnare
   all'arrivo (Scena 1): *«Quattro Eroi dal futuro salveranno la fortezza dalla
   Mano Rossa e dal drago Skullcrusher il Nero»*. I giocatori scoprono di
   **essere** la profezia (il momento più forte dell'arco).
2. **La tabella di carry-over B4** (per il DM): esito del duello → effetto su
   Fauci nel 1372.
3. **Statblock di Skullcrusher** (§4) per il duello.

### Immagini (atlante C1 — momenti d'uso)
| Momento | Immagine |
|---|---|
| Il portale del Tempo / l'arrivo | ⚠️ **nessuna immagine adatta**: `PortaleDellaForgiaEterna.webp` è la fotografia di un blocco di testo, non un'illustrazione (verificato il 2026-09-24). Il prompt per rifarla è la scheda **22** di `Immagini/PROMPT-IMMAGINI-07ILP.md` |
| La fortezza giovane, all'arrivo | da generare: scheda **33** dello stesso file |
| Skullcrusher nel cortile | da generare: scheda **41** |
| I ritratti del cast | da generare: sezione «Ritratti del cast di mille anni fa» dello stesso file; i riquadri sono già nel volume `homebrew/volume-mille-anni/` |
| L'affresco del Tempo (partenza) | `Sala Forgia Eterna - Camera Ottagono con 8 Affreschi Divini (Parte 2).webp` |

### Musica
- **`Musica/LaCanzoneDellePietre.mp3`** — all'accensione del **Rubino** (Scena
  6): la leggenda che si compie merita il tema della pietra al suo apice.

---

### FILE-FONTE ASSORBITI DA QUESTO MASTER (→ `_ARCHIVIO/` a consolidamento chiuso)
`_ARCHIVIO/PortaleForgia-P5-FASTPLAY.md` (master da tavolo B3) · `PortaleForgia-P5-DEFINITIVO-PARTE1/2.md`
(prosa estesa) · `_ARCHIVIO/PortaleForgia-P5-RICALIBRATO.md` (deprecato) · sezione «battaglia
antica» di `_ARCHIVIO/PortaleForgia-P6-INTEGRAZIONE-Completa.md` (deprecata).
`PortaleForgia-P5-B4-CARRYOVER-Forgia-Ricorda.md` resta **vivo** (tabella
DM-approved citata da qui e dall'ARC-08). `Bestiario/villain/Salvatore/Salvatore.md`
resta vivo (Vatore/Sal).

---

## MAPPE ASCII ULTRA-CLEAR (scala 1,5 m/quadretto)

> 📗 **Versione a piena scheda tattica** (posizioni PG/PNG/villain, terreno &
> altitudini, tattiche di villain/mostri, evoluzione) nell'**Atlante Mappe
> Definitivo**: `Mappe/ARC07-MAPPE-DEFINITIVO.md`. Le griglie qui sotto sono
> identiche; là hanno gli add-on DM. **I booklet includono l'Atlante.**

### MAPPA M7-A — HAMMERFIST ≈372 DR: fortezza, campo dell'orda, mura (strategica)

```
════════════════════════════════════════════════════════════════════════
 HAMMERFIST ≈372 DR — vista strategica (non in scala; il duello è su M7-B)
════════════════════════════════════════════════════════════════════════
   NORD ▲  ╔══════════════════════════════════════════════╗
          ║   🏰🏰🏰  HAMMERFIST GIOVANE (mura bianche)  🏰🏰🏰 ║  ← Zona 1 (sicura)
          ║   🏰  [Sala del Trono: Re Thorek I]  [Fucina]  🏰 ║     arrivo del portale
          ║   🏰🏰  ═══ camminamenti ═══  BRECCIA▓▓  🏰🏰🏰🏰 ║  ← Zona 3 (mura, alba)
          ╚════════════════▲▲▲═══════════════▲▲▲═════════════╝
                    scale d'assedio / arieti ↑ (l'orda preme)
   ~~~~~~~~~~~~~~~~~~~~~~~ CORTILE INTERNO (arena del duello → M7-B) ~~~~~~~~~
          ⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺  ← Zona 2: MARE DI TENDE
   GP1▪   ⛺⛺⛺  ╔═══════════╗  ⛺⛺⛺   👤VATORE (§5, tra le tende)  ▪GP2
          ⛺⛺  ║ TENDA DEL  ║  ⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺
          ⛺⛺  ║  COMANDO   ║  ⛺⛺  ⚔️ZOG'TAR + 4 sergenti (Sc.3)
          ⛺⛺  ╚═══════════╝  ⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺
   GP3▪   ⛺⛺⛺⛺⛺⛺ (10.000 dormono) ⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺⛺  ▪GP4
          — — — — foresta d'approccio (partenza PG, Sc.3) — — — —  SUD ▼
────────────────────────────────────────────────────────────────────────
LEGENDA · 🏰 mura/fortezza (bianche, nuove) · ▓ breccia · ⛺ tende (copertura)
· ▪GP posti di guardia · ╔╗ tenda del comando (Zog'tar) · 👤 Vatore · ⚔️ scontro
veloce · SKULLCRUSHER entra dall'alto sul cortile interno → M7-B.
════════════════════════════════════════════════════════════════════════
```

### MAPPA M7-B — L'ARENA DEL DUELLO (cortile interno · Skullcrusher)

```
════════════════════════════════════════════════════════════════════════
 CORTILE INTERNO — 36 m × 27 m (24 col × 18 righe · 1,5 m) · cielo aperto
 Skullcrusher entra da V1 (quota ~45 m) e picchia. PG partono da riga 16-17.
════════════════════════════════════════════════════════════════════════
COL →  A B C D E F G H I J K L M N O P Q R S T U V W X
01    ☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️🐉☁️☁️  ← 🐉 Skullcrusher (quota ~45 m, V1)
02    ☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️     ZONA AEREA (solo volo/gittata)
03    ☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️
04    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰  ← camminamenti +4,5 m (arcieri nani)
05    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
06    🏰🟫🟫🟫▓▓🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫▓▓🟫🟫🟫🟫🟫🏰  ← ▓ macerie (copertura +4 CA)
07    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
08    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰     ⬛ = dove Skullcrusher
09    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫⬛⬛⬛🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰       atterra se scende (4,5 m)
10    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫⬛⬛⬛🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
11    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫⬛⬛⬛🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
12    🏰🟫🟫🟫▓▓🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫▓▓🟫🟫🟫🟫🟫🏰
13    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
14    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
15    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰
16    🏰🟫🟫🛡️🟫🟫🥋🟫🟫🟫🟫👑🟫🟫🟫🟫🔮🟫🟫🌙🟫🟫🟫🏰  ← 🛡️Thorik 🥋Tordek 🔮Artemis 🌙Hella
17    🏰🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🟫🏰    👑 Re Thorek I (alle spalle; 8 pf se Sc.4 fallita)
18    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
════════════════════════════════════════════════════════════════════════
LEGENDA · ☁️ zona aerea (Skullcrusher resta qui: serve volo o gittata) · 🐉
Skullcrusher (quota) · ⬛ impronta d'atterraggio del drago (Enorme) · 🟫 cortile
· ▓ macerie (copertura +4) · 🏰 mura/camminamenti (+4,5 m, arcieri nani) · 👑 Re
Thorek I · 🛡️🥋🔮🌙 i 4 PG.
DILEMMA: il drago NON vuole atterrare (in cielo è un dio). Costringerlo giù =
Artemis in volo che lo tormenta, Aegis Fang scagliata (cicatrice d'ala → B4),
tiri dai camminamenti. A terra è vulnerabile al full-attack del party ma
devastante. In aria è sicuro ma i suoi danni calano. Portalo giù, o colpiscilo
dall'alto: la scelta è dei PG.
════════════════════════════════════════════════════════════════════════
```


\page

# III · Balvar Fuocospento — scheda del Bestiario

{{note
##### ⚠ SOLO DM
Questo capitolo è materiale del DM: non mostrarlo ai giocatori.
}}

# Balvar Fuocospento, il Consigliere dell'Orda (CR 13) [INFERRED — creato 2026-07-31 su richiesta DM]
**Faction**: orda-antica-372dr | **Role**: caster-divine-boss | **Environment**: mountain | **CR**: 13 | **Source**: creato per `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` (assedio di Hammerfist ≈372 DR) — richiesta DM «un incantatore memorabile e antico che possa rivaleggiare coi Rumbling Stone» | **Status**: inferred-dm-request


```statblocco
gs: 13
tipo: Medium humanoid (dwarf), Chierico 9 di Abbathor / Runecaster 4, NE
ca: 24
ca-dettaglio: contatto 12, colto 22 (mithral +2, anello +2, DES +2)
pf: 96
ts: Temp +13, Rifl +8, Vol +17
attributi: For 12 Des 14 Cos 16 Int 16 Sag 20 Car 14
velocita: 6 m
iniziativa: +2
attacchi:
  - Mischia martello da guerra runico +1 +10/+5 (1d8+2)
```

> [INFERRED — needs DM confirmation] `pf-dado` tolto da `scripts/conformita_statblocchi.py`: portava «1d8+2», che non sono i dadi vita (pf-dado «1d8+2» ha 1 dado, il testo dichiara 13 DV). I dadi non si ricostruiscono senza inventare: la composizione delle classi non e' leggibile o comprende una classe non SRD. Da completare a mano.

> ✅ `attributi` **allineati al testo della scheda** su decisione del DM (2026-09-24): la riga generata da `scripts/genera_attributi.py` diceva Int 9, Sag 18, Car 10, e contraddiceva il profilo sotto (Int 16, Sag 20, Car 14) e i TS di Volontà.

Medium humanoid (dwarf), **Chierico 9 di Abbathor / Runecaster 4**, NE. **hp 96** (13 DV); **CA 24**, contatto 12, colto 22 (mithral +2, anello +2, DES +2). Init +2; Vel 6 m. TS Temp +13, Rifl +8, **Vol +17** (+2 razziale vs magia). BAB +8; Lotta +9. For 12, Des 14, Cos 16, Int 16, **Sag 20**, Car 14.
**Mischia** martello da guerra runico +1 +10/+5 (1d8+2). Domini **Inganno** e **Runa** `[INFERRED: dominio Runa = FRCS]`. Incantesimi da Chierico 9 (CD 15+liv): tipici *dispel magic, magic circle against good, greater magic weapon, divination, righteous might, blade barrier, slay living, silence, invisibility purge, glyph of warding, dimensional anchor*.
**RUNE INCISE (Runecaster 4)**: incide fino a **4 rune persistenti** su superfici o creature consenzienti/legate; una runa incisa **non consuma slot al momento dell'uso** e scatta alla condizione scritta. Rune tipiche: *dimensional anchor* sulla soglia, *blade barrier* su una parete, *silence* su sé stesso, **la Catena** (sotto).
**LA CATENA DI SKULLCRUSHER (Su, unica)**: la runa-vincolo incisa nella scaglia sternale del drago. Finché regge, **Skullcrusher combatte per l'orda**. Non è dominazione — è un **contratto scritto nella carne**, e il drago lo sa.
**LEGGERE IL FUORI-POSTO (Su, 3/giorno)**: come *detect magic* ma sulle **anomalie temporali**: percepisce chi non appartiene a questo secolo. **È il solo, in tutta Hammerfist ≈372 DR, che sa cosa sono i PG.**
Scurovisione 18 m. Immune a paura (patto con Abbathor). **Debolezza**: le sue rune sono **scritte** — chi legge il nanico antico e le vede può contrastarle (vedi il modulo).
Notes: consigliere del generale **Zog'tar Deatheye** (CR 14) all'assedio di ≈372 DR. Nano dello scudo **esiliato**, ex-runaio della fortezza, passato ad Abbathor. Non è il capo: è **il motivo per cui il capo ha un drago**. Dossier narrativo, tattiche e ganci → `ARC07-DEF-4` §4-ter.


\page

# IV · Le mappe a stampa

{{note
##### ⚠ SOLO DM
Questo capitolo è materiale del DM: non mostrarlo ai giocatori.
}}

# Le mappe a stampa

> **Cosa c'è.** La griglia del cortile del duello (M7-B) resa a pergamena dal
> renderer del repo, alla scala di **1,5 m per quadretto**: si stampa e si mette
> sul tavolo. La vista strategica M7-A (fortezza, campo, mura) è schematica per
> scelta e resta in ASCII, in fondo al master `DEF-4`.

## M7-B · il cortile interno, 36 × 27 m

![Il cortile interno di Hammerfist, arena del duello con Skullcrusher](../../Mappe/rendered/ARC07-MAPPE-DEFINITIVO_map05_cortile-interno-36-m-27-m-24-col-18-righe-1-5-m.svg)

**Legenda di gioco.** Il drago entra dall'alto sulla colonna V e resta in quota
finché qualcuno non lo porta giù. I PG partono dalle righe 16-17, Re Thorek I
alle loro spalle. Le macerie danno copertura +4. I camminamenti sono a +4,5 m,
con gli arcieri nani. Le posizioni di dettaglio, il terreno e l'evoluzione
round per round stanno nell'Atlante (`Mappe/ARC07-MAPPE-DEFINITIVO.md`, M7-B).

**Cosa c'è nel cortile e non è disegnato**: le corde degli arieti, la fucina
accesa da stanotte, la cisterna sotto il pozzo, le campane della torre nord.
La tabella di cosa succede se qualcuno le usa è in `DEF-4` §4, «Il cortile».
Il DM non la legge ai giocatori: la tiene sotto gli occhi e risponde.


\page

# V · La Forgia ricorda le ferite — carry-over B4

{{note
##### ⚠ SOLO DM
Questo capitolo è materiale del DM: non mostrarlo ai giocatori.
}}

# B4 — "LA FORGIA RICORDA LE FERITE" (tabella di carry-over)
## Ponte meccanico P5 (duello con Skullcrusher, ≈372 DR) → ARC-08 (Fauci di Palude, 1372 DR)

> **Stato (B4)**: ⭐ deliverable cross-arc più importante dell'arco. Traduce
> l'**esito del duello con Skullcrusher** (P5 fast-play, Scena 5) in un
> **effetto quantificato** sullo statblock di **Fauci di Palude** nell'ARC-08
> (`08_.../00_Schede_dei_Personaggi_Unità_e_Regolamento_di_Battaglia.md`, GS
> 15, 312 PF). Chiude il task **ARC-08 A12**.
>
> **Fonte narrativa**: Moradin, P5-DEFINITIVO-PARTE2 r.290 — *«Ogni ferita che
> infliggi ora all'antenato, la mia Forgia la ricorderà quando affronterai il
> discendente.»* + Aegis Fang, P6 r.746 (*"sangue Skullcrusher chiama"*).
>
> ✅ **Valori APPROVATI dal DM (2026-07-03)** — canone di carry-over. Sistema
> **D&D 3.5** — solo bonus tipizzati (competenza/circostanza/morale), **niente
> vantaggio/svantaggio 5e**. (Il DM può sempre ritoccare in corsa, ma questi
> sono i valori di riferimento su cui l'ARC-08 può contare.)

---

## 1. INPUT DAL P5 (cosa registra il fast-play)

Dalla **Scena 5** del `_ARCHIVIO/PortaleForgia-P5-FASTPLAY.md` si registrano due dati:

1. **Esito del duello**: `UCCISO` / `FERITO GRAVE` / `FUGGITO`.
2. **Ferite ancestrali segnate** (`N`): numero di colpi andati a segno su
   Skullcrusher durante il duello (la "Cicatrice della Forgia"). Cap
   consigliato **N ≤ 3** ai fini del bonus.

---

## 2. TABELLA ESITO → EFFETTO SU FAUCI DI PALUDE (1372)

| Esito del duello | Effetto sullo statblock di Fauci (GS 15, 312 PF) | Razionale |
|---|---|---|
| **UCCISO** (Skullcrusher a 0 pf) | **Cicatrice ancestrale attiva**: Fauci entra in campo con **−10% PF** (312 → **281 PF**) e **Presenza Terrificante CD 25 → 23** contro i **portatori degli artefatti** (Thorik/Corona, Tordek/Bracieri+Cintura, Hella/Collana, Artemis/Ring). | La stirpe porta la ferita mortale del capostipite: il sangue "ricorda" di poter cadere. |
| **FERITO GRAVE** (fugge sotto ⅓ pf) | **−1 uso del soffio**: il primo **Soffio a Cono** (1/giorno) è **indisponibile**; il soffio in linea parte comunque ma la **prima** volta a −2 alla CD (27 invece di 29). Nessuna riduzione di PF. | La ferita non è letale ma "storpia" l'arma migliore del sangue. |
| **FUGGITO** (Skullcrusher si allontana quasi illeso) | Fauci **vi ha visti e riconosciuti**: **+2 iniziativa** e nessuna sorpresa contro di voi (sa chi siete) **MA morale fragile** — **fugge sotto i 75 PF** invece di 50 (soglia di ritirata alzata di 25). | Il drago è forte ma il sangue teme già i "quattro del futuro": più cauto, meno disposto a morire. |

---

## 3. BONUS PER "FERITE ANCESTRALI SEGNATE" (N)

Indipendente dall'esito (si somma), riflette P5-DEF-P2 r.294:

- **Ogni ferita ancestrale segnata** dà ai **portatori d'artefatto**, **solo
  contro Fauci nel 1372**, a **scelta unica del gruppo** all'inizio della
  battaglia:
  - **+1 di competenza ai tiri per colpire** contro Fauci, **oppure**
  - **+1d6 danni** ai colpi che vanno a segno su Fauci.
- Cap: **N ≤ 3** (max **+3 TxC** o **+3d6**).
- **Cicatrice fisica** (se Aegis Fang colpì Skullcrusher in volo, P5 Scena 5):
  Fauci ha una **cicatrice a forma di martello** su un'ala → **−2 metri alla
  Volare** (45 → 43) e i PG che lo sanno hanno **+2 di circostanza** a
  colpirlo mentre è in volo.

---

## 4. IL GANCIO INVERSO — AEGIS FANG "SENTE" FAUCI

- Quando Fauci di Palude entra in scena nel 1372, **Aegis Fang canta**
  (*"sangue Skullcrusher chiama"*, P6 r.746). Meccanicamente: **Thorik ottiene
  +2 di circostanza ai tiri per colpire contro Fauci** (bonus di circostanza
  3.5, definito e non 5e) e **avverte in anticipo** il primo soffio di Fauci
  (può dichiarare *pronto a ripararsi* → TS Riflessi del soffio **+2**).
- È l'eco meccanica del legame ancestrale: l'arma che uccise il capostipite
  riconosce il discendente.

---

## 5. PROPAGAZIONE (checklist)

- [x] **Tabella creata** (questo file), con esiti aperti e valori quantificati.
- [x] **Nota nello statblock ARC-08 di Fauci**: aggiunto un rimando a questo
  file in `08_.../00_Schede_dei_Personaggi_Unità_e_Regolamento_di_Battaglia.md`
  §FAUCI DI PALUDE.
- [x] **P5 fast-play** rimanda qui (Scena 5 + sezione carry-over).
- [x] **Valori validati dal DM (2026-07-03)** → l'ARC-08 A12 può integrarli
  come canone (riga matrice esiti + read-aloud del primo avvistamento).


\page

# ✉ Le Cronache dei Quattro Eroi

{{note
##### ✉ HANDOUT GIOCATORE
Pagina da consegnare al giocatore indicato, in privato.
}}

<!-- Auto-generated — do not edit by hand.
     Sorgente: 07_il Portale Della Forgia Eterna/ARC07-HANDOUTS.md
     Rigenera con: python3 scripts/dm.py handout --tipo profezia --da 07_il Portale Della Forgia Eterna/ARC07-HANDOUTS.md
     Incolla tutto su https://homebrewery.naturalcrit.com/ (New brew). -->

{{margin-top:60px}}

{{banner PROFEZIA}}

# Le Cronache dei Quattro Eroi

{{note
> *Dalle Cronache di Thorgrim Barbadiferro, incise nella pietra di Hammerfist:*
>
> *«Quando la Mano Rossa calò sul nostro focolare e il cielo si fece nero di
> ali, non fu un re a salvarci, né un esercito. Furono **Quattro Eroi** venuti
> da un tempo che non era ancora. Portavano una corona di stelle di pietra, un
> martello che cantava, un anello di luce e ombra, e con loro camminava la vita
> stessa rifiorita dalla morte.*
>
> *Abbatterono il drago nero e spezzarono l'orda. Poi svanirono, come erano
> venuti, lasciando solo il loro nome nella roccia.»*
>
> — Moradin, nella mente di Thorik: *«Le Cronache dicono che 'Quattro Eroi'
> salvarono Hammerfist. Siete VOI. Siete sempre stati voi. Andate. Chiudete il
> cerchio.»*
}}

{{margin-top:30px}}

{{footnote Handout giocatori · 2026-07-10 · Rumbling Stone}}
{{pageNumber,auto}}

