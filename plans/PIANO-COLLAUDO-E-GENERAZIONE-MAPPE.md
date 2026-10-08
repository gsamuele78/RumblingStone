# PIANO — Il collaudo delle mappe, e un generatore che non consegna bozze ingiocabili

> **Stato**: 🔵 pianificato (2026-10-08), D1-D9 e D11 decise dal DM lo stesso giorno, D10 (i glifi) aperta · **Classe**: G per il contratto e V0, C per i lotti di codice, K per le correzioni delle mappe giocate
> **Nasce da**: il documento *«Algorithmic Frameworks and Automated Evaluation
> Architectures for Deterministic Map Generation in Tabletop Role-Playing
> Games»*, portato dal DM il 2026-10-08 con la richiesta di verificare cosa si
> applica alla generazione e alla correzione delle mappe, usando quello che c'è
> nel repo, i progetti della community e le pratiche di Paizo e Wizards of the
> Coast per D&D 3.5 e Pathfinder 1e; di misurare prima cosa c'è e cosa va
> migliorato o validato; poi un piano e un ADR che coprano tutti i passi.
> **Decisione**: [ADR-0082](adr/ADR-0082-la-mappa-si-collauda-come-grafo-prima-che-come-immagine.md) (accettata il 2026-10-08, non attuata; l'estensione sulla posa dei simboli è la D8).
> **Ordine** (D1, cambiato da D8 il 2026-10-08): V2-bis (i simboli nuovi), V1 (il collaudo, con `@tipo` e `@deroga` presi da V2), il ruolo del collaudatore (V11-bis), poi il lotto mappe D28 rifatto col set nuovo e collaudato, poi AMBIENTE A1-A8, poi il resto.
> **Misura riproducibile**: `python3 -I plans/esperimenti/collaudo-mappe-2026-10/misura_mappe.py`, uscita del 2026-10-08 in [`misura-2026-10-08.txt`](esperimenti/collaudo-mappe-2026-10/misura-2026-10-08.txt), commit `8297670`.
>
> **In breve**: il repo sa disegnare una mappa in modo deterministico e
> verificarne il rendering al byte, e non ha nessuno strumento che dica se la
> mappa si può giocare. Del documento entra la parte di collaudo (grafo,
> raggiungibilità, agenti deterministici, distanza dalla giocabilità come somma
> di violazioni) e un generatore piccolo per i luoghi nuovi; restano fuori
> l'algoritmo genetico, MAP-Elites, Wave Function Collapse e ogni modello che
> tocca la geometria. Le regole sono quelle dell'SRD 3.5, che per la geometria
> coincide con PF1e, e non i numeri di 5e che il documento cita.

---

## §1 · Cosa ho guardato prima, e cosa questo piano NON rifà

Regola di apertura (ADR-0044): letti `plans/INDEX.md`, STATO-E-ORDINE §0, i
sei piani e le due ricerche che parlano di mappe, l'audit di luglio, gli ADR
della legenda. `fase1.py` sui file toccati: nessun archivio fra i bersagli.

| Documento | Cosa copre | Qui |
|---|---|---|
| [PIANO-LEVEL-DESIGN-E-INQUADRATURA](PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md) | rami C (scheda-mappa, riprogettazione delle tre mappe peggiori, parity pass) e D (inquadratura, prosa) | **non si toccano**: restano suoi. Il suo C2 dipende «dal linter di VENDIBILITA»: da oggi dipende da V1 e V5 di questo piano |
| [PIANO-VENDIBILITA](PIANO-VENDIBILITA.md) §6 | 1.2 profili di regole, 1.3 cucitura dominio/presentazione, 3.3 pipeline mappe scorporata | **non si rifanno**. 🔎 Il linter (B1-B5 di LEVEL-DESIGN, diventati P2.0-P2.4 del piano prodotto) e il campo `map_kind` (A3, diventato P1.3) **non compaiono** fra i lotti di §6: il loro 1.3 è la cucitura, e la Fase 2 è bonifica e IP. Nessun piano li esegue. Li prende questo piano (D6) |
| [AUDIT-LEVEL-DESIGN](../docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md) | definizioni di M1-M9, misura a mano su 29 griglie (luglio) | le definizioni si **riusano** così come sono; i numeri si rifanno con la legenda ratificata (§2.3) |
| [ADR-0048](adr/ADR-0048-legenda-funzionale-fonte-unica.md), [ADR-0043](adr/ADR-0043-le-montagne-sono-muri-e-nessun-master-esce-dal-controllo.md), VENDIBILITA §10 | `legend.yaml` con `blocks_movement`, `blocks_sight`, `cover`, `move_cost`; SVG e UVTT leggono gli stessi muri | **il dato c'è**: era il prerequisito che a luglio mancava. Nessuno script legge ancora `cover` né `move_cost` |
| [INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITÀ](PIANO-INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITA.md), [RENDER-FEDELTÀ](PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md), [IMPORT-ULTRACLEAR](PIANO-IMPORT-ULTRACLEAR-ASCII-TO-JSON.md), [RICERCA-GENERATORI-MAPPE](RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md) | produzione: tre modalità, contratto JSON, UVTT, renderer, import | **si usano**, non si toccano. Il generatore di V9 scrive nel contratto JSON che già esiste |
| [PIANO-EDITOR-VISUALE-MAPPE](PIANO-EDITOR-VISUALE-MAPPE-TATTICHE.md) | editor a griglia, progetto separato | fuori. Il formato dei rilievi di V1 è pensato perché l'editor possa mostrarli, come già il `--json-report` di `import_ultraclear` |
| Lotto **D28** di [LETTORE-E-PLAYTESTER](PIANO-LETTORE-E-PLAYTESTER.md) | le mappe di Hammerfist nel 372 e nel 1372 | **viene prima** e non si tocca. Le sue griglie nuove sono il primo banco di prova di V1 |
| [ADR-0037](adr/ADR-0037-stdlib-only-e-le-sue-eccezioni.md), [ADR-0039](adr/ADR-0039-profili-regole-multisistema.md), [ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md) | solo libreria standard; numeri nei profili; niente mappe di terzi come dato | vincoli. L'ADR-0015 della PR #72, che chiedeva `scipy`, `networkx` e `tcod`, resta rifiutato: §2.3 mostra che non servono |

---

## §2 · Fase A — Audit: cosa c'è, cosa manca, cosa dice il documento

### §2.1 · La pipeline che c'è

| Pezzo | Cosa controlla oggi |
|---|---|
| `render_map_svg.py` | dimensioni dichiarate contro celle lette (avviso, `--strict` fallisce); disegno deterministico |
| `validate_maps.py` (CI) | XML ben formato, provenienza, SVG identico al master al byte, determinismo, nessun master fuori controllo (ADR-0043) |
| `compile_map_json.py` | simboli della legenda, coordinate nella griglia, rettangoli validi, modo giusto per terreni e unità |
| `export_uvtt.py` | muri, porte e luci derivati dalla legenda; 100 px per quadretto, `--ppg` per cambiarli |
| `scripts/legend.json` | 64 simboli: 16 terreni, 42 oggetti, 6 unità; funzione neutra per 56 |
| `import_watabou.py`, `import_ultraclear.py`, `suggest_map.py` (10 modelli) | ingresso di layout esterni o di modello; conflitti figura-tabella |
| Test | `test_mappe_muri_e_copertura`, `test_legenda_fonte_unica`, `test_legenda_glifi`, `test_compile_meters`, `test_import_ultraclear`, `test_export_map_png`, `test_render_map_blender` |

Nessuno di questi risponde a: ci si arriva? la porta sta in un muro? ci passa
una creatura Grande? dove si prende copertura? da dove si vede cosa?

### §2.2 · Il corpus

38 griglie in 18 file (archi 07, 08, 09 e il Drappo), 32 almeno 12×12, 58.499
celle. Esclusi i derivati `.hb.md` (che ricopiano i master), gli archivi, le
fixture e gli esempi di `scripts/` e le guide di `docs/`. 41 SVG e 2 `.uvtt`
committati. 19 griglie dichiarano le dimensioni nell'intestazione, 20 hanno
`@north`.

### §2.3 · Le misure del 2026-10-08

Regole di movimento dell'SRD: niente diagonale oltre l'angolo di un muro,
porte considerate aperte, copertura dove la legenda dice `half`,
`three_quarters` o `total`. M1 e M2 come nell'audit: quota di celle percorribili
entro 2 quadretti da una copertura; quota del più grande spazio aperto senza.

| Misura | Valore | Lettura |
|---|---|---|
| Simboli né universali né dichiarati | 82 celle in 3 griglie | errore vero, poco esteso |
| Legenda locale che ridefinisce un simbolo universale | 57 voci in 10 griglie | la skill lo vieta (STEP 4), nessuno lo misura |
| …di cui con la funzione opposta | **7**, in 3 mappe | `⬛` come pavimento nella Stanza della Corona e nel Cuore della Montagna; `🌀` e `🌫` descritti come muro o vuoto |
| Celle-porta | 97 | 34 a cavallo di un muro o del bordo · 15 con un muro accanto ma non a cavallo · 28 senza un lato percorribile · 20 senza nessun muro accanto |
| Griglie con più di una zona percorribile (≥ 4 celle) | 9 su 38 | da leggere a mano: un piano superiore o una porta segreta lo giustificano |
| Griglie con unità in zone separate | 11 su 32 | idem; due sono il Cuore della Montagna (§2.3, punto 1) |
| M1 mediana (≥ 12×12) | 0,42; 19 su 32 sotto 0,60 | i campi aperti restano il problema dell'audit |
| M2 mediana (≥ 12×12) | 0,52; 22 su 32 sopra 0,20 | idem |
| Accesso di una creatura Grande (2×2) sotto l'80% del percorribile | 2 su 32 | raro, ma è il controllo che la GameMastery Guide chiede (§2.5) |
| Tempo dell'intera misura | 1,3 s, sola libreria standard | ADR-0037 regge |

🔎 **Quello che la misura ha corretto, compreso me.**

1. **Il Cuore della Montagna era la mappa modello dell'audit di luglio** (M1 =
   1,00, M2 = 0,00, §3.3) ed è la più rotta del corpus: con `⬛` letto come
   dice la legenda, 891 celle diventano 198 percorribili in 13 sacche, e le 71
   unità stanno in 17 sacche diverse. Il voto alto veniva dal pavimento letto
   come roccia. Le altre misure dell'audit vanno rifatte, e questa tabella lo
   fa.
2. **La mia prima regola sulle porte segnalava 283 porte storte su 303.** Le
   porte larghe tre celle (`🚪🚪🚪`) contavano come tre porte senza muro, e i
   duplicati `.hb.md` raddoppiavano tutto. Con le file di porte trattate come un
   varco solo i numeri sono quelli della tabella.
3. **Il corpus comprendeva le fixture dei test**, che sono rotte apposta (una
   serve a provare i simboli sbagliati), e gli esempi di `scripts/examples/`.
   Davano 47 griglie invece di 38 e 51 porte «senza muro» in una griglia sola,
   che era una fixture. Tolte quelle, le 20 porte senza muro sono 13 in una
   vista d'insieme della fortezza di Hammerfist e 7 nelle mappe del Drappo: a
   quella scala `🚪` è «il portone» e il muro non si disegna. Un campo che dica
   che la mappa è strategica serve comunque, ma il rumore è meno di quanto la
   prima misura faceva credere.
4. **I numeri di M1 e M2 non si confrontano con quelli di luglio**: a luglio
   l'insieme delle coperture era stato inventato per l'audit, oggi viene dalla
   legenda ratificata. Lo stesso segno (gli esterni falliscono), valori diversi.

### §2.3-bis · La legenda per porte, chiusure e passaggi fra livelli

Il DM, il 2026-10-08, dopo le decisioni: *«c'è una mappa completa dei simboli
per i diversi tipi di porte, muri, arredi e scale per salire e scendere,
prigioni con le sbarre e gabbie? tutti questi asset saranno usati nella mappa
con tessere diverse: si può capire se ogni tessera è usata correttamente?»*

Misurato con lo stesso script:

| Concetto | Simboli nella legenda universale |
|---|---|
| porta | **1** (`🚪`, «Porta / ingresso»: nessuna distinzione fra legno, ferro, pietra, chiusa a chiave, sbarrata) |
| porta segreta | 0 |
| saracinesca o grata | 0 |
| sbarre, cella, gabbia | 0 |
| botola, pozzo | 0 |
| scala | **1** (`🪜`, «Scale / rampa»: non dice se sale o scende, né dove porta) |
| salire o scendere | 2, e nessuno è un passaggio fra livelli: `⬇` è una pendenza, `🔳` una pedana |
| finestra o feritoia | 0 |
| muri | 4 terreni (`🏰 ⬛ 🟪 ⛰`) e 2 strutture (`🏛 🗼`), più il muretto `🧱` |

Nei 18 file con griglie le grate, le gabbie, le prigioni, le botole e le porte
segrete compaiono **17 volte, solo nella prosa** (4 file): nessuna griglia le
disegna, perché non c'è il simbolo. Dentro le griglie ci sono **350 celle** di
**11 simboli** fuori legenda, quasi tutti dichiarati in una legenda locale
(`☁ 💠 🔷 🔲 🔺 …`): è il segno che chi disegna inventa il simbolo quando la
legenda non ce l'ha.

**Si può capire se una tessera è usata bene? Sì, a una condizione.** La
legenda oggi dice cosa fa una tessera (blocca il movimento, la vista, dà
copertura); non dice **dove può stare**. Una porta in mezzo al prato e una
porta in un muro hanno la stessa funzione e solo una ha senso. Il collaudo può
giudicare la posa solo se la posa è un dato. Da qui il lotto V2-bis e la D8:
ogni simbolo dichiara una **regola di posa**, e il collaudo la verifica.

| Regola di posa | Per chi | Cosa controlla il collaudo |
|---|---|---|
| `nel_muro` | porte di ogni tipo, porta segreta, saracinesca, grata, finestra, feritoia | la fila sta fra due muri (o un muro e il bordo) lungo un asse, ed è percorribile o visibile dai due lati dell'altro |
| `recinto` | sbarre, gabbia | la zona chiusa da muri e sbarre ha almeno un varco `nel_muro` (porta o grata), oppure una deroga («cella murata») |
| `fra_livelli` | scala che sale, scala che scende, botola, pozzo, scala a pioli | sta su una cella percorribile con un vicino percorribile, e ha **la sua coppia** dichiarata con `@collega` su un'altra mappa o un altro livello; la coppia esiste ed è del verso opposto |
| `sul_pavimento` | arredi (tavolo, letto, baule, rastrelliera, altare) | non sta dentro un muro e non chiude **l'unico** varco di una stanza (punto d'articolazione), salvo deroga |
| `solo_master` | porta segreta, botola nascosta, trappola | non compare nella versione per i giocatori di una mappa (`versione giocatore`), dove si disegna come muro o pavimento |

I numeri di gioco restano fuori dalla legenda (ADR-0039): durezza, punti
ferita, CD per sfondare o forzare, CD di Cercare per una porta segreta stanno
nel profilo, presi dall'SRD (*Dungeons*, porte e saracinesche) quando il
profilo si scrive, e verificati lì.

⚠️ **Un limite da dichiarare subito**: le sbarre bloccano il movimento e non la
vista. Il formato UVTT non ha un muro di quel tipo, quindi l'export deve
scegliere, e la scelta va scritta come deroga, come quella del bosco `🌲` in
`legend.yaml`. Da verificare sul formato quando si fa il lotto.

### §2.5-bis · Chi verifica le mappe, fuori di qui: editori, community, ricerca

Il DM, il 2026-10-08: *«supponendo che gli script esistano, quali sono i
migliori usati dalla community e dagli editori come Wizards of the Coast e
Paizo per creare o usare gli algoritmi che servono: asset delle mappe,
verifica della mappa, controllo del level design e della giocabilità, sia per
il DM sia per i giocatori?»*

**La risposta onesta comincia da un'assenza.** Né Wizards né Paizo
pubblicano uno strumento automatico che verifichi una mappa. Da quello che si
trova (forum ufficiali di Paizo, interviste a cartografi di Wizards, il blog
*Maps, Maps, Maps*), le loro mappe nascono da uno schizzo dell'autore, passano
dalla redazione che le controlla contro la continuità e la leggibilità,
arrivano a un cartografo che le ridisegna a mano (Photoshop, Illustrator,
GIMP, Campaign Cartographer), e tornano alla redazione per il confronto. La
verifica è **editoriale e di playtest**, non algoritmica. È la stessa catena
del repo, e questo piano le aggiunge il pezzo che a loro manca.

Gli algoritmi di verifica veri stanno in tre posti:

| Dove | Strumento | Cosa fa che serve qui | Licenza | Come entra |
|---|---|---|---|---|
| Editor di livelli | **LDtk** | ogni tessera porta un'etichetta semantica (*enum tag*: muro, acqua, porta) e regole automatiche dicono quale tessera va dove | MIT | **come schema**: è il campo `function` della legenda più il campo `posa` di V2-bis. Non come dipendenza |
| Editor di livelli | **Tiled** (Automapping) | regole «se trovi questo, metti quello» su mappe a tessere; proprietà tipizzate per tessera; la validazione delle proprietà però va scritta a mano con gli script | GPL per l'editor | idem: lo schema delle regole di posa |
| VTT | **Foundry**: Universal Battlemap Importer, *Levels*, *Multilevel Tokens* | muri, porte e luci importati da UVTT; piani diversi della stessa mappa; una scala `@stairs` su un piano teletrasporta alla scala gemella sull'altro | moduli della community, licenze varie | `@collega` di V2-bis è lo stesso accoppiamento, controllato **prima** di esportare. L'export UVTT resta quello di oggi |
| Ricerca | **Sentient Sketchbook** (Liapis, Yannakakis, Togelius) | il progettista schizza la mappa; lo strumento verifica la giocabilità e misura controllo dell'area, esplorazione ed equilibrio | articoli | le metriche di esplorazione e di sicurezza delle zone entrano come avvisi in V5 e V7 |
| Ricerca | **Expressive Range Analysis** (Smith e Whitehead, 2010) | misure globali (leniency, linearità, densità) per vedere che tipo di mappe un generatore produce | articolo | serve solo a V9, per sapere se il generatore fa sempre la stessa mappa |
| Ricerca | **Evolutionary Dungeon Designer**, FI-2Pop, MAP-Elites | il documento portato dal DM | articoli | §2.4 |

**Per il DM e per i giocatori** la differenza è la vista. Il DM vede tutto e
deve poter giocare la mappa (raggiungibilità, coperture, tempi d'ingaggio);
il giocatore vede la versione senza segreti, e lì il controllo è che non ci sia
niente che non dovrebbe vedere (D9) e che la mappa si legga da sola (il nord
dichiarato, la legenda, i simboli riconoscibili). Nessuno degli strumenti qui
sopra fa le due cose insieme: lo farà il collaudatore di V11-bis, con lo
strumento di V1 sotto.

⚠️ Le fonti sono in gran parte di seconda mano (forum, interviste, note di
rilascio), e quelle sui flussi di Wizards e Paizo hanno anni. Le licenze di
LDtk e Tiled valgono per gli strumenti, che qui non si installano: se ne prende
l'idea.

### §2.4 · Il documento portato dal DM, affermazione per affermazione

| Il documento dice | Per questo repo | Esito |
|---|---|---|
| L'IA scrive il codice e i parametri, a runtime gira un algoritmo deterministico | è già la regola d'oro di `tre-modalita-mappe.md`: l'LLM scrive JSON, mai la griglia | ✅ c'è |
| Quadretti da 5 piedi, seme riproducibile | 1,5 m; rendering verificato al byte in CI | ✅ c'è |
| Copertura +2 (mezza), +5 (tre quarti) | sono valori di **5e**. In 3.5 e PF1e: copertura +4 CA e +2 Riflessi, migliorata +8 e +4, totale non bersagliabile, copertura morbida delle creature +4 CA contro il tiro a distanza (`skills/dnd-35-srd/references/combat.md`; `LEGENDA-FUNZIONALE-SPEC.md` §3.1). Il collaudo dice *se* c'è copertura; il valore lo dà il profilo (ADR-0039) | ⚠️ corretto |
| Corridoi larghi almeno un quadretto per una creatura Media | giusto e incompleto. L'SRD aggiunge: niente diagonale oltre l'angolo di un muro, sì oltre una fossa; Grande 2×2, Enorme 3×3; si passa strizzandosi in uno spazio largo metà, a costo doppio e con −4 a colpire e alla CA | ⬜ V6 |
| BSP, WFC, simmetria locale, automi cellulari, rumore | servono solo per luoghi **nuovi**: una mappa giocata è canone (`audit-mappe-workflow.md` STEP 2). Watabou, che è la simmetria locale, è già importato | 🟡 BSP e automi cellulari in V9; WFC no (ADR-0082) |
| FI-2Pop, due popolazioni che evolvono | troppo per 38 mappe scritte a mano. Entra la sua idea utile: **la distanza dalla giocabilità come somma pesata delle violazioni**, che è il formato dei rilievi di V1 | 🟡 V1, V9 |
| Agenti di playtest, persone «Monster Killer» e «Treasure Collector» | entrano come interrogazioni deterministiche sul grafo: dall'ingresso a ogni obiettivo e tesoro; da ogni nemico ai PG; con l'ingombro della creatura più grande. Niente MCTS né reinforcement learning | ⬜ V6 |
| MAP-Elites per la diversità | risolve un problema che qui non c'è (§2.3: le mappe di campo aperto sono tutte uguali per povertà, non per eccesso di generazione) | ❌ rimandato, criterio di riapertura in ADR-0082 |
| Arricchimento con statblocchi e testi generati dall'IA | AGENTS.md vieta di inventare statblocchi; le unità puntano al Bestiario | ❌ |
| Export VTT ortogonale con muri, porte e luci; 70 o 140 px per quadretto | `export_uvtt.py`, 100 px di default, `--ppg` | ✅ c'è |
| «Un seme non validato non va mai mostrato all'utente» | si adotta così com'è per il generatore | ⬜ V9 |

### §2.5 · Le pratiche di Paizo, Wizards of the Coast e della community

Ogni pratica diventa un controllo misurabile, o resta dichiaratamente fuori.

| Fonte | Pratica | Come entra |
|---|---|---|
| Paizo, *Maps, Maps, Maps* (blog) | l'autore disegna la mappa grezza; la redazione la controlla contro la continuità e la ritocca per leggibilità; il cartografo la ridisegna; si confronta il risultato con l'originale | è già la catena del repo: master → `validate_maps` → SVG → verifica a vista (STEP 5). Il collaudo aggiunge il controllo che la redazione fa a occhio |
| *GameMastery Guide* (PF1e), p. 52, via Archives of Nethys | le creature devono passare dai varchi del loro covo (l'esempio è il drago e l'ingresso della tana) | V6: accesso con l'ingombro della taglia più grande dichiarata |
| idem | ogni stanza ha un perché | è la scheda-mappa di LEVEL-DESIGN C1, non qui |
| idem | niente simmetria inutile né layout ripetitivi | M7 dell'audit, avviso in V5 |
| idem | numerare le aree e usare quei numeri nelle note | V7: ogni `@mark` ha la sua voce nel testo e viceversa |
| SRD 3.5, *Wilderness* | distanza massima a cui comincia un incontro per tipo di terreno (bosco rado 3d6×10 piedi, medio 2d8×10, fitto 2d6×10) | V8: M9 calibrata sulla regola invece che su una soglia a occhio |
| SRD 3.5, *Movement, Position, and Distance* | angoli, ingombri, strizzarsi | V6 |
| Justin Alexander, *Jaquaying the Dungeon* | più ingressi, anelli, più strade per lo stesso obiettivo | V7: anelli μ = E − V + C sul grafo delle zone; ingressi contati. Avviso |
| Joris Dormans, generazione ciclica di *Unexplored* (analisi di Boris the Brave) | il dungeon si compone di cicli (chiave e serratura, scorciatoia nascosta), non di rami | V9: il generatore BSP chiude almeno un anello per costruzione |
| DMG di 4e e del 2024 | quota che premia la posizione, pericoli in cui spingere, ragioni per muoversi | **altra edizione**: si citano come buon senso, non come regola. La scheda-mappa di LEVEL-DESIGN le raccoglie già |

⚠️ **Cosa non ho potuto leggere.** Il testo del DMG II e di *Dungeonscape*
(3.5) non era raggiungibile: il piano non afferma niente di quei libri. Le
mappe di *Red Hand of Doom* restano riferimento visivo e mai dato (ADR-0005,
STEP 1). Lo shadowcasting simmetrico di Albert Ford è dato per CC0 solo da chi
lo ha tradotto in Rust; prima di copiarne il codice va verificata la licenza
all'origine (`rumblingstone-edizione`), altrimenti si scrive dalla descrizione.

---

## §3 · Fase S — Sviluppo, lotto per lotto

Ogni lotto dichiara chi lo esegue, quanto impegno e come si sa che è finito
(ADR-0045). Un ramo e una PR per lotto.

### V0 · Le decisioni del DM

`[engine: Opus 5, sessione principale · effort: alto · qualità: D1-D7 chiuse nella tabella di §7, con l'eco se ne arrivano due o più insieme]` · **G**

### V1 · `collaudo_mappe.py`, il rapporto in sola lettura

`[engine: Sonnet 5 · effort: medio-alto · qualità: riproduce al numero la tabella di §2.3 sul commit 8297670; ogni controllo ha un caso rosso e uno verde nei test; 41 SVG identici]` · **C**

- Legge `legend.json` con `dmcore/legenda.py` e la griglia col parser di
  `render_map_svg.py`, come `validate_maps.py`. Solo libreria standard.
- Controlli della classe **E** (ADR-0082 §3): `simbolo/ignoto`,
  `legenda/funzione-opposta`, `porta/senza-muro`, `porta/murata`,
  `raggiungibile/obiettivo`, `raggiungibile/unita`. Della classe **A**: M1, M2,
  `zone/separate`, `ingombro/grande`.
- Uscita testuale e `--json` contro uno schema nuovo
  `scripts/schemas/map_findings.schema.json`: per ogni rilievo codice, classe,
  cella in coordinate A1, messaggio, deroga se c'è. In fondo la **distanza
  dalla giocabilità**, la somma pesata dei rilievi E.
- `--report` esce sempre 0. Voce nel manifest (ADR-0012), `--help` senza
  effetti, smoke in CI. Lo script di `plans/esperimenti/` resta come prova
  della misura e non si importa.
- Primo cliente: le griglie del lotto D28 appena fatte.

**Fatto il 2026-10-08**, con `@tipo` e `@deroga` presi da V2 e le direttive
`@collega`, `@taglia` e `@vista giocatori` di V2-bis e D9. 20 test, uno rosso e
uno verde per controllo; passo non bloccante in CI; voce nel manifest. Sul
corpus: **38 mappe, 97 errori, 53 avvisi, 1,4 secondi**.

Il confronto con la misura di §2.3, che il criterio di qualità chiedeva:

| Misura | §2.3 (script di misura) | `collaudo_mappe` | Perché |
|---|---:|---:|---|
| legende locali che rovesciano un universale | 7 | 7 | stessa regola |
| griglie con più zone percorribili | 9 | 9 | stessa regola |
| M1 sotto 0,60 · M2 sopra 0,20 | 19 · 22 | 19 · 22 | stessa regola |
| simboli ignoti | 82 celle in 3 griglie | 7 rilievi in 3 griglie | il collaudo conta un rilievo per simbolo, non per cella |
| porte fuori posto | 63 celle | 31 rilievi | il collaudo conta una fila di porte come un varco solo, e riconosce tutte le chiusure di V2-bis |
| griglie con unità separate | 11 | 9 | la misura fermava la diagonale a ogni cella che blocca il movimento; il collaudo la ferma solo all'angolo di un muro, come dice l'SRD (una fossa o un barile non la fermano) |

🐛 **Un difetto trovato dal test prima del commit**: la funzione che cerca la
gemella di una scala restituiva una stringa sia per l'errore sia per il simbolo
trovato, quindi ogni scala ben collegata risultava rotta. Il caso verde l'ha
preso; con il solo caso rosso sarebbe passato.

### V2 · `@tipo` e `@deroga`

`[engine: Sonnet 5 per il codice, Opus 5 per la classificazione · effort: medio · qualità: le 38 griglie hanno @tipo; il renderer resta byte-identico; due norme nuove registrate e misurate]` · **C + G**

- Le due direttive di ADR-0082 §4. Il renderer già ignora le `@` che non
  conosce (`parse_annotations`), quindi gli SVG non cambiano: va provato, non
  supposto.
- Il contratto JSON prende `kind` e `derogations`, additivi;
  `compile_map_json.py` li scrive come direttive.
- Classificazione delle 38 griglie in tattiche, strategiche e schemi: la
  proposta la fa l'agente, la lista la conferma il DM (è giudizio).
- Le due norme in `skills/REGISTRO-NORME-EDITORIALI.md` col loro rilevatore
  (G3, ADR-0056), e in `audit-mappe-workflow.md` STEP 4.

### V2-bis · Il corredo dei simboli e la loro posa (D8, D9)

`[engine: Opus 5 per il set e le regole, Sonnet 5 per il codice · effort: alto · qualità: ogni simbolo nuovo ha la sua arte in-house, la sua funzione, la sua regola di posa e un caso rosso e uno verde nei test; 41 SVG di oggi identici; il gate legend/single-source verde]` · **G + C**

- Il set, deciso in D8 e allargato dal DM lo stesso giorno (nord leggibile,
  acqua, fogne, detriti, arredi, caverne). I glifi sono la D10, proposti qui e
  verificati contro il parser delle griglie (`⏬` e `⏫` non passano) e contro
  il corpus (nessuno è già usato):

  | Famiglia | Glifo | Cosa | Posa |
  |---|---|---|---|
  | chiusure | `🚪` | porta (c'è già) | nel muro |
  | | `🔒` | porta chiusa a chiave o sbarrata | nel muro |
  | | `❔` | porta segreta | nel muro, solo nel master |
  | | `🥅` | saracinesca o grata | nel muro |
  | | `🪟` | finestra o feritoia | nel muro |
  | | `⛓` | sbarre di cella o gabbia | recinto |
  | fra livelli | `🔼` | scala che sale | fra livelli |
  | | `🔽` | scala che scende | fra livelli |
  | | `🔻` | botola o pozzo | fra livelli |
  | terreni | `🟤` | pavimento di caverna, roccia naturale | libera |
  | | `💧` | acqua bassa, pozza | libera |
  | | `🫧` | fogna, liquame | libera |
  | | `🪵` | detriti, travi crollate | libera |
  | arredi | `🗄` | armadio o scaffale | sul pavimento |
  | | `📚` | libreria, archivio | sul pavimento |
  | | `🧰` | baule o forziere | sul pavimento |
  | | `⛲` | fontana o cisterna | sul pavimento |
  | | `⚒` | incudine e forgia | sul pavimento |
  | | `🧪` | banco dell'alchimista | sul pavimento |
  | | `🛐` | altare | sul pavimento |
  | | `🏗` | gru o argano | sul pavimento |

  `🪜` resta «scale o rampa» senza regola di posa: sei celle di Hammerfist la
  usano per salire ai camminamenti, e cambiarle senso adesso sarebbe toccare
  una mappa giocata. Il nord **non è una tessera**: è la direttiva `@north`,
  che il renderer già disegna come rosa dei venti; il collaudo la rende
  obbligatoria nelle mappe tattiche (errore E `nord/mancante`), e le
  annotazioni a lato possono dire «parete nord» sapendo dov'è.
- Ogni simbolo entra in `legend.yaml` con `render`, `function` e il campo nuovo
  `posa`. Il disegno è vettoriale e fatto in casa (regola 5 della skill
  mapmaking), come gli altri prop.
- Direttiva `@collega <coordinata> ; <file o mappa> <coordinata>` per le scale
  e le botole; il contratto JSON prende `links`, additivo.
- Il collaudo legge `posa` e verifica le regole della tabella di §2.3-bis. Le
  violazioni di `nel_muro`, `fra_livelli` (coppia mancante) e `solo_master`
  sono errori della classe E; `recinto` e `sul_pavimento` sono avvisi.
- I simboli locali delle griglie che hanno un equivalente nuovo si migrano in
  V3, mappa per mappa.

**Fatto il 2026-10-08.** 20 simboli nuovi in `legend.yaml` (84 in tutto), con
funzione e posa; `posa`, `verso` e `solo_master` sono campi della legenda e
`build_legend.py` li porta in `legend.json`. Il renderer ha 17 prop e 3
pattern nuovi, aggiunti in coda: i 41 SVG committati restano identici al byte.
`🚪` prende `posa: nel_muro`, dieci arredi di prima `sul_pavimento`; `🪜` resta
senza regola. I test che congelavano la legenda sono aggiornati con i nomi dei
simboli nuovi, e una classe di test nuova controlla verso, porte segrete e
disegni.

🔎 Trovato facendolo. **Al primo giro la porta chiusa a chiave, il
baule e la botola si confondevano**: tre rettangoli marroni con una placca
dorata. Lo ha mostrato la verifica a vista del PNG, non un test; ridisegnati
(assi e lucchetto di lato, baule tondo con le maniglie, botola con la freccia).
E **il pattern del dais `🔳` non ha posto nell'ordine di pittura** dal giorno di
ADR-0042: si dipinge dopo i muri. Nessuna cella del repo usa `🔳`, quindi non ha
effetti oggi; è scritto nel test e non è corretto qui.

### V3 · Le correzioni del corpus

`[engine: Opus 5, mai delegato · effort: xhigh · qualità: conferma esplicita del DM mappa per mappa; i rilievi E scendono a zero o hanno una deroga scritta]` · **K**

- `⬛` come pavimento nella Stanza della Corona e nel Cuore della Montagna (tre
  sorgenti: `ARC07-DEF-2`, `ARC07-DEF-5` e l'atlante `ARC07-MAPPE-DEFINITIVO`;
  i booklet `.hb.md` si rigenerano, non si toccano a mano): si cambia **il simbolo, mai la
  posizione** (STEP 2). Quale simbolo è la D2. Gli SVG si rigenerano e il
  delta si misura prima.
- `🌀` e `🌫` ridefiniti nella Stanza della Corona e nella Camera Centrale; le
  82 celle di simboli ignoti in 3 griglie.
- Le porte senza muro nelle mappe che V2 ha classificato tattiche; le zone
  separate e le unità irraggiungibili, una per una: o si corregge, o si scrive
  la deroga con il motivo.

### V4 · Il gate a tetto

`[engine: Sonnet 5 · effort: medio · qualità: il gate morde (un rilievo E in più fa fallire la CI in una prova a rovescio) e non boccia niente di oggi]` · **C**

- `scripts/collaudo-mappe-tetti.json` con i conteggi E per griglia dopo V3, <!-- validate-docs: futuro -->
  come `scripts/apparato-residui.json`. Il gate fallisce se un conteggio
  cresce; quando scende, il tetto si abbassa nello stesso commit.
- I rilievi A **non entrano** nel gate (ADR-0082 §3).
- Passo in `ci.yml` e in `dm.py doctor`, voce in `scripts/README-automation.md`.

### V5 · Linea di vista e copertura secondo l'SRD

`[engine: Sonnet 5 · effort: alto · qualità: casi d'esame tratti dall'SRD (angolo, muretto, creatura in mezzo) verdi; M4 esatta su tutto il corpus sotto i 10 s]` · **C**

- Shadowcasting simmetrico in libreria standard, scritto dalla descrizione o
  copiato dopo la verifica della licenza (§2.5). M4 esatta, senza
  campionamento. M7 e M8 dalle definizioni dell'audit.
- Copertura fra due celle con la regola dell'SRD: da un angolo del quadretto
  di chi attacca a tutti gli angoli del bersaglio. Il risultato è il livello
  neutro (`none`, `half`, `three_quarters`, `total`); il numero lo dà il
  profilo.
- Avviso utile al DM: tiratori nemici senza linea di tiro sull'ingresso da cui
  arrivano i PG.

### V6 · Gli agenti deterministici

`[engine: Sonnet 5 · effort: medio-alto · qualità: per ogni taglia un caso che passa e uno che non passa; le domande del §2.4 hanno risposta per tutte le mappe tattiche]` · **C**

- Ricerca in ampiezza con l'ingombro della taglia: Media 1×1, Grande 2×2,
  Enorme 3×3, con lo strizzarsi a costo doppio e i costi di `move_cost`
  (terreno difficile ×2, la foresta ×4 nel valore neutro).
- Le tre interrogazioni: dall'ingresso a ogni `⭐ 🎯 💎 🏺`; da ogni nemico al
  PG più vicino, in round di movimento; la creatura più grande dichiarata fino
  al suo obiettivo.
- La taglia: nel contratto JSON le unità prendono `size`, additivo; nelle
  griglie emoji la dice una direttiva o niente (D5).

### V7 · Il grafo delle zone, gli anelli, le aree numerate

`[engine: Sonnet 5 · effort: medio · qualità: μ calcolato per ogni mappa con zone; ogni @mark ha la sua voce e viceversa]` · **C**

- Zone dai rettangoli di `@zone` e dalle stanze separate da porte; anelli
  μ = E − V + C, strozzature come punti d'articolazione, ingressi contati. È
  l'A2 orfano di LEVEL-DESIGN, ridotto a ciò che serve a M3.
- Aree numerate: le `@mark` della griglia contro le voci del testo. Avviso.

### V8 · La distanza d'ingaggio calibrata sull'SRD

`[engine: Opus 5 per le scelte, Sonnet 5 per il codice · effort: medio · qualità: la tabella dell'SRD trascritta con la fonte; il DM riconosce come giuste le segnalazioni sulle mappe che conosce]` · **C + G**

- M9 smette di essere la banda «2-4 round» a occhio: per ogni mappa di
  esterno, la distanza iniziale fra PG e nemici contro la distanza massima
  d'incontro del terreno prevalente.

### V9 · Il generatore di bozze (solo se D4 = sì)

`[engine: Sonnet 5 · effort: alto · qualità: 1.000 semi per tipo, zero bozze consegnate con rilievi E; due giri con lo stesso seme danno lo stesso JSON]` · **C**

- `genera_mappa.py`: BSP con corridoi sul minimo albero ricoprente più almeno
  un anello (Dormans) per gli interni; automi cellulari con la regola 4-5 e
  pulizia delle sacche per le caverne. Seme obbligatorio. Esce un contratto
  JSON, poi `compile_map_json` e il collaudo; se la distanza dalla giocabilità
  non è zero si ritenta col seme successivo, entro un limite, e si dice quanti
  tentativi sono serviti.
- Solo per luoghi nuovi e incontri casuali. Non tocca le mappe dei master.

### V10 · La riparazione proposta

`[engine: Sonnet 5 · effort: medio · qualità: ogni riparazione è un diff leggibile che il DM applica o rifiuta; nessuna scrittura sui master]` · **C**

- Per i rilievi E con una correzione meccanica (porta da allineare, sacca da
  collegare, varco da allargare per un Grande): una proposta in diff, solo per
  le bozze di V9 e i contratti JSON non ancora giocati (ADR-0082 §6).

### V11 · Skill, guida e chiusura

`[engine: Sonnet 5 · effort: basso-medio · qualità: build-skills e validate_skills verdi; la guida descrive il giro completo su un esempio vero]` · **M + C**

- Reference nuova `skills/rumblingstone-mapmaking/references/collaudo-mappe.md`
  e una riga nella tabella della skill; `docs/guides/GUIDA-MAPPE.md`; STEP 5 di
  `audit-mappe-workflow.md` con il collaudo prima del PNG.

### V11-bis · Il collaudatore di mappe, un ruolo LLM (D11)

`[engine: Opus 5 · effort: alto · qualità: la rubrica trova, su una mappa con difetti messi apposta, tutti quelli che lo strumento trova e almeno uno che lo strumento non può trovare; non vede il piano né la conversazione]` · **G**

- Un ruolo come il lettore e il playtester a freddo di `rumblingstone-playtest`:
  un agente che **non ha disegnato la mappa** la riceve con il master, il suo
  testo d'arco e il rapporto di `collaudo_mappe.py`, e risponde a una rubrica
  fissa in due viste.
  - **Vista del DM**: lo strumento è stato eseguito e i rilievi E sono a zero o
    hanno una deroga motivata? Ogni scala ha la sua gemella? Le posizioni
    coincidono col testo della scena? Si capisce chi entra da dove e in quanti
    round arriva al contatto?
  - **Vista del giocatore**: la versione per i giocatori non mostra porte
    segrete né trappole (D9); il nord è dichiarato; i simboli si leggono senza
    la legenda locale; nessun simbolo fuori legenda.
  - **Gli algoritmi**: per una mappa generata (V9), il seme è scritto, la bozza
    è passata dal collaudo, le correzioni proposte da V10 sono state applicate
    o rifiutate per scritto.
- Lo strumento risponde a ciò che si conta; il ruolo a ciò che si giudica
  (ADR-0067, il confine fra codice e LLM). Il ruolo **non corregge**: segnala,
  e la correzione la fa chi ha disegnato, col DM.
- Vive in `skills/rumblingstone-mapmaking/references/collaudo-mappe.md`,
  citato dalla tabella della skill, e la sua norma entra nel registro (G3).

---

## §4 · Fase V — Validazione

| Cosa | Come si prova | Quando |
|---|---|---|
| La misura è vera | V1 riproduce la tabella di §2.3 sul commit `8297670`; ogni differenza si spiega per scritto | V1 |
| I controlli mordono | per ogni codice un caso che deve fallire e uno che deve passare; il caso rosso si verifica rosso prima di scrivere il verde | V1, V5, V6, V7 |
| Il rumore è contato | su un campione di 10 griglie i rilievi si leggono a mano e i falsi positivi si pubblicano col loro numero (G6) | V1, poi a ogni controllo nuovo |
| Il rendering non cambia | 41 SVG identici al byte dopo V1, V2, V4-V8; in V3 cambiano solo quelli delle mappe corrette, col delta misurato prima | sempre |
| Determinismo | due giri danno lo stesso JSON; il generatore, a seme uguale, lo stesso contratto | V1, V9 |
| Tempo | il corpus intero sotto i 10 s in CI, linea di vista compresa | V5 |
| Il gate non boccia la storia | dopo V4 la CI è verde su `main`; una prova a rovescio con un rilievo E in più è rossa | V4 |
| Il DM riconosce il problema | su tre mappe che conosce bene (una giocata, una di D28, una strategica) le segnalazioni corrispondono a ciò che vede al tavolo | V3, V8 |
| Al tavolo | una mappa corretta in V3 o nata in V9 giocata una sera, con la scheda di feedback di `rumblingstone-playtest` | dopo V3 |
| Disciplina | `check_plans_discipline`, `decisioni_dm --check`, `eco_decisioni --check`, `validate_norme_editoriali`, `tools_manifest --check` verdi a ogni PR | sempre |

---

## §5 · Ordine e dipendenze

```
V2-bis ─► V1 (+ @tipo, @deroga) ─► V11-bis ─► D28 (LETTORE, rifatto e collaudato)
                                                 └─► AMBIENTE A1-A8 ─► V2 ─► V3 ─► V4
                                                                        └──► V5 ─► V8
                        └─► V6 ─► V7
                                   └──► V9 ─► V10   (solo se D4 = sì)
                 V11 chiude, dopo V4 e dopo ogni lotto che aggiunge un controllo
```

V1 e V2 non toccano artefatti; V3 è l'unico lotto che cambia mappe giocate.
LEVEL-DESIGN C2 può partire dopo V1 e V5.

---

## §6 · Rischi

| Rischio | Mitigazione |
|---|---|
| Il collaudo segnala troppo e lo si spegne | `@tipo` prima delle porte; i rilievi A non bloccano mai; falsi positivi contati e pubblicati |
| V3 cambia mappe giocate | si cambia il simbolo e non la posizione; ogni mappa con conferma del DM; SVG col delta misurato prima |
| Il profilo «d20» dentro lo strumento diverge dai profili di VENDIBILITA 1.2 | è dichiarato come temporaneo in ADR-0082 §2; quando 1.2 arriva si sposta e un test confronta i valori |
| La licenza dello shadowcasting non è CC0 | si scrive dalla descrizione dell'algoritmo, che non è protetta |
| Il generatore cresce oltre il bisogno | V9 parte solo con D4 = sì; due algoritmi, non quattro; niente MAP-Elites finché il criterio di ADR-0082 non scatta |
| Il piano parte prima di D28 o di AMBIENTE e li rallenta | l'ordine è la D1; V1 è piccolo e serve proprio a D28 |

## §6-bis · Cosa questo piano NON risolve

- Non misura il divertimento: misura se una mappa si gioca e quali scelte
  offre. Una mappa può passare ogni controllo ed essere noiosa.
- Non giudica esplorazione, indagine e scene sociali.
- Non calibra le soglie di M1-M9: manca un corpus proprio o con licenza libera.
- Non sostituisce la verifica a vista del PNG né la prova al tavolo.

---

## §7 · Le decisioni del DM

<!-- decisioni-dm: COLLAUDO-MAPPE -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | V0 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Quando parte, rispetto a D28 e ad AMBIENTE?** Entrambi aspettano D28. Proposta: D28, poi V1 (piccolo, e collauda le mappe appena fatte), poi AMBIENTE A1-A8, poi V2 in avanti |
| ~~D2~~ | V3 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Che simbolo prende il pavimento oggi disegnato con `⬛`** nella Stanza della Corona e nel Cuore della Montagna? Proposta: `⬜` pavimento lavorato per la sala, `🟫` per la caverna; il colore scuro, se serve, lo dà un terreno nuovo in `legend.yaml`, non la ridefinizione locale |
| ~~D3~~ | V1, V4 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Quali controlli sono errori e bloccano a tetto**, e quali solo avvisi? Proposta: quelli di ADR-0082 §3 |
| ~~D4~~ | V9 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Il generatore di bozze serve?** Proposta: sì, piccolo (BSP e caverne), dopo V6; per gli incontri casuali e i luoghi nuovi dell'arco 09 |
| ~~D5~~ | V6 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Come dichiara la taglia una griglia emoji?** Proposta: una direttiva `@taglia <coordinata> ; Grande`, solo dove serve; nel contratto JSON il campo `size` |
| ~~D6~~ | V0 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **Il linter di level design e `map_kind` passano a questo piano?** Oggi LEVEL-DESIGN li dà a VENDIBILITA, che non li elenca. Proposta: sì, e LEVEL-DESIGN C2 dipende da V1 e V5 |
| ~~D7~~ | V5 | ✅ **Decisa il 2026-10-08, il DM: come proposto.** Era: **La copertura parziale di PF1e** (+2 CA, +1 Riflessi) entra nel livello neutro già ora o col profilo PF1e di VENDIBILITA 1.2? Proposta: col profilo; il collaudo distingue solo i quattro livelli neutri |
| ~~D8~~ | V2-bis | ✅ **Decisa il 2026-10-08, il DM: anticipato, e il lotto D28 si rifà col set nuovo** (*«check if there are the d28 maps and recreate d28 with new simbol set»*). Era: **Il corredo dei simboli e la regola di posa**: entrano i simboli di §2.3-bis (porte per tipo, porta segreta, saracinesca, grata, finestra, sbarre, scale che salgono e che scendono, botola, pozzo, arredi), ognuno con un campo `posa` che il collaudo verifica? E quando: dopo V2, come nell'ordine di D1, oppure prima di D28, perché le mappe di Hammerfist (fucina, gallerie, cappella, armeria, la sezione a livelli) sono proprio quelle con scale, porte e grate? Proposta: dopo V2; D28 si disegna con i simboli di oggi più simboli locali dichiarati, e V3 li migra. Anticiparlo costa a D28 il tempo dell'arte nuova e del lotto di test |
| ~~D9~~ | V2-bis | ✅ **Decisa il 2026-10-08, il DM: sì.** Era: **Le porte segrete nella versione per i giocatori**: si disegnano come muro (il giocatore non sa che c'è) e il collaudo boccia una porta segreta che compare in una mappa per i giocatori? Proposta: sì |
| D10 | V2-bis | **I glifi del set nuovo**: quelli della tabella di V2-bis? Proposta: sì; se un glifo non si legge bene al tavolo, si cambia lì, prima che una mappa lo usi |
| ~~D11~~ | V11-bis | ✅ **Decisa il 2026-10-08, il DM: serve un ruolo LLM in più** che controlli che le mappe siano corrette, che gli algoritmi richiesti siano stati usati e che le parti sbagliate siano state corrette (*«it will need another llm role for checking that maps are correct»*). Diventa V11-bis: il collaudatore di mappe |

<!-- eco: COLLAUDO-MAPPE 2026-10-08 -->
- **Decise**: (primo messaggio) D1 l'ordine D28, V1, AMBIENTE A1-A8, poi V2 in avanti · D2 `⬜` per la sala, `🟫` per la caverna · D3 le classi E e A di ADR-0082 §3 · D4 sì al generatore, piccolo, dopo V6 · D5 `@taglia` nelle griglie emoji, `size` nel contratto · D6 il linter e `map_kind` passano qui, LEVEL-DESIGN C2 dipende da V1 e V5 · D7 la copertura parziale di PF1e col profilo. (Secondo messaggio) D8 il set dei simboli prima di D28, e D28 rifatto col set nuovo · D9 le porte segrete non compaiono nella versione per i giocatori · D11 un ruolo LLM di collaudo
- **Aperte**: D10 i glifi del set nuovo, proposti in V2-bis
- **Cambiate**: D8 dalla proposta «dopo V2, D28 con i simboli di oggi» a «prima di D28, e D28 rifatto»; quindi cambia l'ordine di D1: V2-bis, V1, il ruolo, D28, AMBIENTE
- **Dedotto da me** (secondo messaggio): che V1 vada **prima** di D28 anche se il DM ha nominato solo i simboli, perché il ruolo di collaudo che chiede ha bisogno dello strumento per verificare le mappe di D28; che `@tipo` e `@deroga` passino da V2 a V1 per lo stesso motivo; che «underground cavern» chieda un pavimento di caverna proprio (`🟤`), che per il Cuore della Montagna sostituisce il `🟫` deciso in D2; che il nord leggibile sia la direttiva `@north` obbligatoria e non una tessera, perché una tessera nord spezzerebbe la griglia
- **Dedotto da me** (primo messaggio): che «approved as proposed» valga anche per lo stato di ADR-0082, che passa da proposta ad accettata; che la domanda sugli «asset» parli della legenda dei simboli e non di immagini raster (le mappe del repo sono griglie di simboli e l'arte è vettoriale, regola 5); che «scaricare» nel messaggio voglia dire «scale», per salire e scendere (✅ confermato dal DM lo stesso giorno: *«staircase»*)

---

## Checklist di avanzamento

```
Fase A — Audit
☑ A1  misura del corpus, script e uscita in plans/esperimenti/collaudo-mappe-2026-10/
☑ A2  il documento del DM affermazione per affermazione (§2.4)
☑ A3  Paizo, WotC, SRD e community: pratiche → controlli (§2.5)
☑ A4  ADR-0082 (accettata il 2026-10-08)
☑ A5  la legenda per porte, chiusure e scale misurata (§2.3-bis)
☑ A6  editori, community e ricerca: chi verifica le mappe (§2.5-bis)

Fase S — Sviluppo
☑ V0  decisioni D1-D9 e D11 (2026-10-08) · □ D10
☑ V1  collaudo_mappe.py in sola lettura, schema dei rilievi, manifest (2026-10-08: 20 test, 38 mappe, 97 errori, 53 avvisi)
□ V2  @tipo e @deroga; 38 griglie classificate; due norme registrate
☑ V2-bis il corredo dei simboli e la regola di posa (2026-10-08: 20 simboli, 17 prop e 3 pattern disegnati in casa, campo `posa`; 41 SVG identici) · □ D10 i glifi, da confermare al tavolo
□ V3  correzioni del corpus, mappa per mappa col DM
□ V4  gate a tetto in CI
□ V5  linea di vista e copertura SRD; M4, M7, M8
□ V6  agenti per taglia; raggiungibilità di obiettivi e nemici
□ V7  grafo delle zone, anelli, aree numerate
□ V8  M9 sulla distanza d'incontro dell'SRD
□ V9  generatore di bozze (se D4 = sì)
□ V10 riparazione proposta in diff
□ V11-bis il collaudatore di mappe, ruolo LLM (D11)
□ V11 skill, guida, chiusura

Fase V — Validazione: la tabella di §4, lotto per lotto
```

> **Regola d'oro dei piani**: chi chiude un lotto aggiorna, nello stesso
> commit, questa checklist, la riga in `plans/INDEX.md` e una riga in
> `plans/CHANGELOG.md`.
