# PIANO — Il collaudo delle mappe, e un generatore che non consegna bozze ingiocabili

> **Stato**: 🔵 pianificato (2026-10-08), D1-D7 aperte · **Classe**: G per il contratto e V0, C per i lotti di codice, K per le correzioni delle mappe giocate
> **Nasce da**: il documento *«Algorithmic Frameworks and Automated Evaluation
> Architectures for Deterministic Map Generation in Tabletop Role-Playing
> Games»*, portato dal DM il 2026-10-08 con la richiesta di verificare cosa si
> applica alla generazione e alla correzione delle mappe, usando quello che c'è
> nel repo, i progetti della community e le pratiche di Paizo e Wizards of the
> Coast per D&D 3.5 e Pathfinder 1e; di misurare prima cosa c'è e cosa va
> migliorato o validato; poi un piano e un ADR che coprano tutti i passi.
> **Decisione**: [ADR-0082](adr/ADR-0082-la-mappa-si-collauda-come-grafo-prima-che-come-immagine.md) (proposta).
> **Ordine**: dopo il lotto mappe D28 di LETTORE-E-PLAYTESTER, che resta la riga ▶ di STATO-E-ORDINE §0. Il rapporto con AMBIENTE-RIPRODUCIBILE è la D1.
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

🔎 **Cinque cose che la misura ha corretto, compreso me.**

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
  `scripts/schemas/map_findings.schema.json`: per ogni rilievo codice, classe, <!-- validate-docs: futuro -->
  cella in coordinate A1, messaggio, deroga se c'è. In fondo la **distanza
  dalla giocabilità**, la somma pesata dei rilievi E.
- `--report` esce sempre 0. Voce nel manifest (ADR-0012), `--help` senza
  effetti, smoke in CI. Lo script di `plans/esperimenti/` resta come prova
  della misura e non si importa.
- Primo cliente: le griglie del lotto D28 appena fatte.

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
D28 (LETTORE) ─► V0 ─► V1 ─► V2 ─► V3 ─► V4
                        │      └──────► V5 ─► V8
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
| D1 | V0 | **Quando parte, rispetto a D28 e ad AMBIENTE?** Entrambi aspettano D28. Proposta: D28, poi V1 (piccolo, e collauda le mappe appena fatte), poi AMBIENTE A1-A8, poi V2 in avanti |
| D2 | V3 | **Che simbolo prende il pavimento oggi disegnato con `⬛`** nella Stanza della Corona e nel Cuore della Montagna? Proposta: `⬜` pavimento lavorato per la sala, `🟫` per la caverna; il colore scuro, se serve, lo dà un terreno nuovo in `legend.yaml`, non la ridefinizione locale |
| D3 | V1, V4 | **Quali controlli sono errori e bloccano a tetto**, e quali solo avvisi? Proposta: quelli di ADR-0082 §3 |
| D4 | V9 | **Il generatore di bozze serve?** Proposta: sì, piccolo (BSP e caverne), dopo V6; per gli incontri casuali e i luoghi nuovi dell'arco 09 |
| D5 | V6 | **Come dichiara la taglia una griglia emoji?** Proposta: una direttiva `@taglia <coordinata> ; Grande`, solo dove serve; nel contratto JSON il campo `size` |
| D6 | V0 | **Il linter di level design e `map_kind` passano a questo piano?** Oggi LEVEL-DESIGN li dà a VENDIBILITA, che non li elenca. Proposta: sì, e LEVEL-DESIGN C2 dipende da V1 e V5 |
| D7 | V5 | **La copertura parziale di PF1e** (+2 CA, +1 Riflessi) entra nel livello neutro già ora o col profilo PF1e di VENDIBILITA 1.2? Proposta: col profilo; il collaudo distingue solo i quattro livelli neutri |

---

## Checklist di avanzamento

```
Fase A — Audit
☑ A1  misura del corpus, script e uscita in plans/esperimenti/collaudo-mappe-2026-10/
☑ A2  il documento del DM affermazione per affermazione (§2.4)
☑ A3  Paizo, WotC, SRD e community: pratiche → controlli (§2.5)
☑ A4  ADR-0082 (proposta)

Fase S — Sviluppo
□ V0  decisioni D1-D7
□ V1  collaudo_mappe.py in sola lettura, schema dei rilievi, manifest
□ V2  @tipo e @deroga; 38 griglie classificate; due norme registrate
□ V3  correzioni del corpus, mappa per mappa col DM
□ V4  gate a tetto in CI
□ V5  linea di vista e copertura SRD; M4, M7, M8
□ V6  agenti per taglia; raggiungibilità di obiettivi e nemici
□ V7  grafo delle zone, anelli, aree numerate
□ V8  M9 sulla distanza d'incontro dell'SRD
□ V9  generatore di bozze (se D4 = sì)
□ V10 riparazione proposta in diff
□ V11 skill, guida, chiusura

Fase V — Validazione: la tabella di §4, lotto per lotto
```

> **Regola d'oro dei piani**: chi chiude un lotto aggiorna, nello stesso
> commit, questa checklist, la riga in `plans/INDEX.md` e una riga in
> `plans/CHANGELOG.md`.
