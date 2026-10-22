# PIANO — Cosa portiamo dalle avventure della community

**Aperto**: 2026-10-18, su richiesta del DM · **Fonte**: [RICERCA-AVVENTURE-COMMUNITY-2026-10](RICERCA-AVVENTURE-COMMUNITY-2026-10.md) · **Decisione**: [ADR-0092](adr/ADR-0092-le-domande-dell-alto-livello.md), [ADR-0093](adr/ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md) · D1-D3 decise dal DM il 2026-10-18, nessuna aperta

Il DM ha chiesto di confrontare i master DEF, il developer e il playtester con
le migliori avventure della community 3.5 e PF1e, in Italia e fuori, e di
portare ciò che migliora. La ricerca ha proposto tre lotti. Questo piano li
tiene, e il primo è chiuso dalla PR che lo apre.

Regola d'apertura (ADR-0044): nessun piano esistente copre la stessa cosa.
`PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE` scrive i master; questo cambia le
domande che quei master devono superare, e i suoi lotti si applicano lì.

## 1 · I lotti

### Lotto 1 · Alto livello e statblocchi ✅ (2026-10-18)

- [x] FASE 1 in sola lettura: `fase1.py` sui bersagli, registro delle norme (nessuna delle quattro era misurata)
- [x] §9-§16 in `skills/rumblingstone-module-standard/references/sviluppo-degli-incontri.md`, e il rimando nel `SKILL.md`
- [x] D9, D10, D15, D16 in `scripts/domande_developer.py`, con dodici test nuovi
- [x] profili `apl` e residui con la ragione in `plans/domande-developer.json`
- [x] la riga «Statistiche base» e i due stati di *Prima del combattimento* (ADR-0092 §3)
- [x] le righe nel registro delle norme
- [ ] **applicazione**: i master di ARC-08 nascono sotto le regole nuove (S1 di MASTER-DEF); gli 11 statblocchi con una preparazione (§3) prendono la riga quando un lotto li tocca

### Lotto 2 · Il sito come sistema e gli indici ⬜

Il roster dei nemici del sito (normale e in allerta) come componente di
ADR-0074, il foglio dello scontro con il testo breve degli incantesimi, la
tabella degli incontri e l'elenco degli statblocchi generati da `componenti.py`,
l'intestazione di zona. La ricerca, §3.1 P2 e P5 e §3.2. Si applica alle ondate
di ARC-08.

### Lotto 3 · Mappe, playtest, indagine, stile ⬜

Il resto della §3.2 della ricerca. Si apre dopo aver visto se i lotti 1 e 2
trovano difetti veri.

### Lotto 4 · La prosa, e come si misura se migliora ✅ (2026-10-18)

Aperto su richiesta del DM, per il rifacimento dei DEF di ARC-07: metodi presi
dalla rete che si possono misurare e applicare. Decisione in
[ADR-0093](adr/ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md),
note in `plans/esperimenti/avventure-community/note-prosa-*.md`.

- [x] FASE 1: la lunghezza dei box aveva già un indicatore (`>500 car`, D1 di PIANO-BOX-DI-LUOGO); la fonte dScryb (30-70 parole) si aggiunge a quella decisione, non fa un rilevatore nuovo
- [x] `cieco_versioni.py`: campione congelato con un seme, coppie in ordine casuale con la chiave a parte, esito con il criterio dei 14 su 20
- [x] `misura_craft --stile`: gerundio in coda, avverbi in -mente, battute dei PNG lunghe, con i falsi positivi contati a mano
- [x] due candidati scartati con la misura (pronome soggetto, spiegazione dopo il gesto); la norma pro-drop nel registro come 🔴
- [x] la fotografia di partenza e il campione di ARC-07 in `plans/esperimenti/prosa-cieco/`
- [x] il corpus di riferimento misurato sui PDF gratuiti (PR #250, [note-prosa-corpus.md](esperimenti/avventure-community/note-prosa-corpus.md)); gerundi e avverbi in `--stile` si leggono contro la sua fascia italiana, non contro una soglia
- [x] **il dopo**: le stesse misure sul rifacimento di ARC-07 (#249) migliorano tutte, ma il DM sceglie alla cieca la nuova in 8 coppie su 16: miglioramento non dimostrato ([ESITO-ARC07-2026-10-18](esperimenti/prosa-cieco/ESITO-ARC07-2026-10-18.md)). Le sette versioni vecchie preferite e le due ipotesi (non tagliare il dettaglio sensoriale, non spezzare i monologhi) passate al thread del rifacimento, che tiene i file
- [x] **la misura aggiornata dai voti** (richiesta del DM, la sera): le due regole in `read-aloud-adulti.md` §2-ter, applicate da `cieco_versioni.py coppie` (al cieco solo le indecise e quattro di controllo) e da `ciclo_prosa misura` come cancello; sulle sedici coppie decide 13 e ne sbaglia una; 26 box impoveriti in ARC-07, passati al thread del rifacimento

- [x] **ADR-0093 accettata** dal DM il 2026-10-19

### Lotto 5 · Il giro completo, misurato contro la versione di prima 🟡 (2026-10-19)

Aperto su richiesta del DM per la riscrittura di DEF-4 e DEF-5 prima della
serata del 2026-10-19. I file di ARC-07 sono del thread «Schede PNG e cattivi
uniformi»; qui c'è lo strumento e la regola.

- [x] `ciclo_prosa.py confronta --rif`: ogni file del giro contro la sua versione di partenza, master e handout in una tabella, esce 1 se uno peggiora
- [x] gli handout di ARC-07, ARC-08 e ARC-09 bersagli di `misura_craft`
- [x] il primo giro sotto la regola (giro 4 di ARC-07, PR #254): nessun peggioramento di prosa; i numeri aggiunti per il DM ora sono «solo aggiunti» e non ✗
- [ ] **la regola** ([ADR-0094](adr/ADR-0094-il-giro-completo-si-misura-contro-la-versione-di-prima.md), proposta): `ciclo_prosa.py confronta --rif` su master e handout, gli handout come bersagli di `misura_craft`; si chiude quando il giro di DEF-4 e DEF-5 della serata del 2026-10-19 dice se regge

### Lotto 6 · La skill esterna scrittura-italiana come eccezione ✅ (2026-10-21)

Aperto dopo che il giocatore di Artemis non ha capito il contratto del Seme
letto a voce. Riscritto con e senza la skill esterna
[scrittura-italiana](https://github.com/hypnosdesign/claude-skill-scrittura-italiana),
il DM ha scelto alla cieca la versione che la usava; `misura_craft` non le
distingueva, l'indice Gulpease sì (67,1 → 70,0 → 72,6).

- [x] il contratto del Seme in due handout, DM e giocatore (`/mnt/project-files/contratto-seme/`); li porta in ARC-07 il thread «Schede PNG e cattivi uniformi»
- [x] la reference `rumblingstone-narrative-style/references/scrittura-italiana-eccezione.md`: tre casi in cui si apre, il testo CC BY-SA fuori dal repo, i quattro conflitti con il repo
- [x] la colonna `Gulp.` in `misura_craft --stile`, con quattro test
- [x] **la prova**: 35 box di DEF-4 e DEF-5 (gli 8 già votati al giro 3 restano fuori) riscritti con la reference, misurati con `cieco_versioni.py` e votati alla cieca dove la misura non decide ([ADR-0097](adr/ADR-0097-scrittura-italiana-entra-come-eccezione.md)). Cieco del DM: nuova 10, vecchia 3, soglia 10 su 13 raggiunta; le 3 vecchie vincitrici rimesse, ADR-0097 accettata

### Lotto 7 · Qualità misurabile: cosa dice la rete, e cosa prevede il DM 🟡 (2026-10-22)

Aperto dalla richiesta del DM di cercare metodi misurabili per la prosa e
l'architettura delle avventure ([RICERCA-QUALITA-MISURABILE-2026-10](RICERCA-QUALITA-MISURABILE-2026-10.md)).
La ricerca ha provato le misure di prosa della letteratura sulle 38 coppie già
votate alla cieca: nessuna prevede il voto del DM. Le regole d'architettura
(Three Clue Rule, domanda drammatica, conseguenza visibile, presagio del
cattivo) sono invece regole di mestiere, e la domanda drammatica manca in
tutte le 39 scene di ARC-07.

- [x] censimento di ciò che il repo misura già e ricerca in rete (prosa e architettura)
- [x] calibrazione delle misure di prosa sui 38 voti ciechi (`plans/esperimenti/qualita-misurabile-2026-10-22/`)
- [ ] **7a, prosa**: il voto cieco porta un'etichetta facoltativa del perché (LAMP e TTCW); dopo ~50 voti etichettati si rifà la calibrazione
- [ ] **7b, architettura**: quattro domande del developer nuove (domanda drammatica, scelta con conseguenza, presagio del cattivo, rete degli indizi), calibrate su ARC-07 e ARC-08 come la D10, cancello solo per i master nuovi
- [ ] **7c, coerenza**: fronti e orologi con uno schema in `state` e negli archi

## 2 · La calibrazione del lotto 1

Le quattro regole nuove eseguite sui nove moduli sotto cancello, prima di
attivarle. Ogni rilievo è stato letto a mano.

| Regola | Rilievi | Veri | Falsi | Note |
|---|---|---|---|---|
| D10 la riga di scala | 9 | 6 | 3 | veri: DEF-1 Scena 3, DEF-4 Scene 6, 8 e 10, DEF-5 Scena 3, la rissa del Drappo. Falsi: DEF-4 Scena 7 (lo scontro si gioca nella 8) e i due atti dell'Abbazia, che scala in un indice maestro |
| D9 il segreto e la divinazione | 1 | ½ | ½ | DEF-4: la targa della Scena 3 è un indizio da leggere, non un segreto; la natura di Balvar nella Scena 7 si divina, e il master non dice cosa succede |
| D15 l'orda di GS basso | 1 | 0 | 1 | DEF-4 Scena 6: gli otto hobgoblin non vanno battuti, conta l'allarme |
| D16 il PG fuori gioco | 0 | — | — | **non calibrata**: i quattro effetti trovati avevano tutti una via d'uscita, o erano stordito e frastornato, che non contano |

Il primo tentativo di D9 contava «segreto» e «indizio» scena per scena, e dava
2 veri su 7: la regola è passata a livello di modulo, con la risposta in forma
fissa (il blocco «Se lo divinano»). Precisione d'insieme delle regole nuove:
**6½ su 11**, vicina al 5 su 9 delle regole di settembre. Sono indicatori.

## 3 · La riga «Statistiche base», contata

37 statblocchi del Bestiario hanno *Prima del combattimento*. **11** dichiarano
incantesimi, pozioni o oggetti di preparazione senza la riga; due scrivono già
nel testo quali numeri la includono (Draxoksus «i numeri del blocco»,
Ozyrrandion «CA 35»). Uno è dubbio: l'*unto* di Lirien va sul pavimento, non su
di lei.

Gli undici: Lirien, Tempestas, l'arcidruido del circolo, Avarthel, Morlin
Coalhewer, Azarr Kul, Arbitrax, Draxoksus, l'emissario della Mano Rossa, Koth,
Ozyrrandion. Il conto si rifà con il comando della §5.

## Decisioni del DM

<!-- decisioni-dm: AVVENTURE-COMMUNITY -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | 1 | ✅ **Decisa il 2026-10-18** (il DM: *«sì sono d'accordo»*): la riga «Statistiche base» entra negli undici statblocchi della §3 quando un master li usa, a cominciare da quelli di ARC-08. Niente lotto a sé |
| ~~D2~~ | 1 | ✅ **Decisa il 2026-10-18, poi cambiata lo stesso giorno** (il DM sulla card: *«Sì, nella #245»*): le quattro righe di scala che mancano nei master di ARC-07 (DEF-1 Scena 3, DEF-4 Scene 6, 8 e 10) **si aggiungono**, nel giro della PR #245 che quei file li sta già toccando. Sono aggiunte, non riscritture. Era: non aggiungerle, salvo per un gruppo nuovo |
| ~~D3~~ | 2 | ✅ **Decisa il 2026-10-18**: il lotto 2 si apre **insieme** a S1 di MASTER-DEF (ARC-08), perché il roster serve alle ondate |

<!-- eco: AVVENTURE-COMMUNITY 2026-10-18 -->
- **Decise**: D1 la riga «Statistiche base» quando un master usa lo statblocco · D2 niente righe di scala nei master di ARC-07 già giocati, salvo per un gruppo nuovo · D3 il lotto 2 insieme a S1 di MASTER-DEF
- **Aperte**: nessuna
- **Cambiate**: nessuna, tutte e tre come proposte
- **Dedotto da me**: che il «sì sono d'accordo» valga per tutte e tre le proposte del piano, anche se il messaggio a cui rispondeva nominava per esteso solo la D1
- **Confermato dal DM il 2026-10-18**: *«sì grazie procedi con tutte e tre»*, la deduzione era giusta
- **Cambiata il 2026-10-18, dopo il merge della #244**: D2. Il DM ha visto le regole sui master di ARC-07 e ha scelto di aggiungere le quattro righe di scala nella #245; il blocco «Se lo divinano» di DEF-4 l'ho passato a quel thread come incluso, ma la scelta sulla card riguardava le righe

## 4 · Come si riparte in una chat nuova

Leggere la ricerca §3 e §5, poi questo piano §2. Le note delle quattro ricerche,
con le fonti, sono in `plans/esperimenti/avventure-community/`.

## 5 · Come si riproduce

```
python3 scripts/domande_developer.py            # il rapporto, con i rilievi D9, D10, D15, D16
python3 scripts/domande_developer.py --check    # il cancello
python3 -m pytest -q scripts/tests/test_domande_developer.py
python3 scripts/misura_craft.py --stile          # lotto 4, gli indicatori di stile
python3 -m pytest -q scripts/tests/test_cieco_versioni.py
```

Il conto della §3 è un grep su `Bestiario/` (la preparazione dentro *Prima del
combattimento*, l'assenza di `Statistiche base`); diventa un controllo con il
primo lotto che porta la riga (ADR-0092, Conseguenze).
