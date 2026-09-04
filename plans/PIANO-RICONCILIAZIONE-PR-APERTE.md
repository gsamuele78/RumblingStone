# PIANO — Riconciliazione delle PR aperte e dei piani

> **Stato**: 🟡 **in corso** · **Aperto**: 2026-09-04
> **Richiesta-fonte (DM, 2026-09-04)**: *«controlla le vecchie PR se sono ancora
> valide e se sono state superate […] fai la riconciliazione di PR e piani»*, poi
> *«#109 analizza le modifiche […] se le modifiche sono valide fammi le domande
> per risolvere i dubbi e aggiorna il main»*.

## Perché questo piano esiste

Sette PR erano aperte senza che nessuno le avesse più guardate. La più vecchia,
la #72, stava in bozza dal 26 luglio e conteneva **tre piani commerciali e due
ADR** che a settembre sono stati riscritti da zero da chi non l'aveva letta.
Il costo non è stato il lavoro doppio: è stato che **due dei suoi ADR erano
migliori** di quello che è stato riscritto al posto loro.

Il rimedio in `PIANO-VENDIBILITA` §8.4 — *prima di aprire un piano, si guardano
le PR aperte* — è una regola, e una regola senza gate si stacca dalla realtà.
Questo piano è il lavoro di rientro: portare su `main` ciò che nelle PR aperte è
**valido e non superato**, un pezzo alla volta e con la fonte dichiarata.

Il criterio di giudizio è uno solo, e non è l'età della PR:

> Una PR è **superata** se il suo contenuto è stato riscritto altrove, meglio o
> uguale. È **abbandonata** se nessuno l'ha ripresa, ma il contenuto è ancora
> l'unico che quel problema abbia. Le abbandonate **non si chiudono per far
> scendere un contatore**: si svuotano portando fuori quello che vale.

---

## Lotto R1 — la correzione del Peso del Mondo `[✅ fatto]`

**Fonte**: PR #99, correzione DM del 2026-08-06, mai arrivata su `main`.

`main` diceva che al rito dello Smeraldo il **Peso del Mondo** l'aveva accettato
**Tordek**. Il DM ha stabilito il 6 agosto che era **Thorik**, il portatore della
Corona — e la #99 lo aveva scritto, ma è rimasta bozza. Per un mese il canone
pubblicato ha attribuito a un PG un pegno permanente di un altro.

⚠️ Il DM ha riconfermato la correzione il 2026-09-04 prima che partisse.

Non era uno scambio di nomi. La #99 stabilisce la regola, e questo lotto la
segue: *un'eco registra **una scelta**; se cambia la mano che ha scelto, l'eco o
si riscrive da zero o si annulla. Gli ID non si riusano.*

- [x] `campaign/state.md`: riga di riepilogo, riga di Tordek, riga di Thorik,
      riga della **Corona**, ed **E-07c riscritta** da zero
- [x] `campaign/state.md`: **E-07e annullata** (`✖ annullata`) e **E-07f** nuova —
      la presenza verde al rito era Hella, e Thorik non lo sa
- [x] `ARC07-DEF-1` §9: blocco «CANONE GIOCATO» riscritto, con la nota di
      correzione che dice cosa diceva prima e perché
- [x] `ARC07-DEF-2` §7-bis «Le Quattro Ore Rubate»: le **mani fredde sotto la
      trave** tornano a Thorik; la notte di Tordek scende a **una scena sola**
- [x] Booklet della sessione Terros e del ritorno alla Forgia (`.hb.md` + `.html`
      rigenerati dal manifest), `00-INTRO-DOVE-SIAMO.md`
- [x] Scheda giocatore della Corona + versione DM (`02_Corona_2_Gemme_DM.html`):
      «il bilancio di Thorik» non dice più che *ha guardato Tordek pagare*
- [x] Scheda Bracieri di Tordek: l'avvertenza sommava un **−2 DES che non è suo**
- [x] `plans/PIANO-INCANTATORI-MEMORABILI-…`: il −2 DES passa alla riga di Thorik
- [x] `plans/PIANO-DM-TOOLKIT-HYPE-…` e `plans/CHANGELOG.md`: **non corretti**,
      annotati. Sono log storici: dicono cosa fu deciso allora, ed è vero

**Portato dentro anche il ritrovamento del 2026-08-09**, perché è un fatto del
modulo giocato e non una decisione nuova: `PortaleForgia-P1-REVISED-Corretta.md`
elenca fra le **Limitazioni** della Corona indossata un **−2 DES**, con il
ricalcolo scritto (*DES 10 → 8, CA 22 → 21, CAR 8 → 12*). Quel blocco non era
mai stato riportato in nessuna scheda successiva: tutte elencavano solo i bonus.
Sommato al pegno del rito, Thorik è a **DES 6**.

> ⚠️ **Due cose restano da decidere dal DM** (`INF-007` nella #99), perché sono
> nel testo di P1 e nessuno le ha né confermate né revocate: il **+4 CAR** e la
> clausola che la Corona **non sia rimovibile** finché mancano gemme. Il +4 CAR
> è a favore del giocatore, la non-rimovibilità è un vincolo di trama. Se
> valgono, valgono entrambi. Segnate sulla scheda, non applicate d'ufficio.

---

## Lotto R2 — l'instradamento delle skill `[✅ fatto]`

**Fonte**: PR #109 (rilievo), decisione DM 2026-09-04 *«Obbligo, e con un gate
che lo verifica»*.

`AGENTS.md` §Skills apriva dicendo che *gli agenti scoprono le skill da soli* —
falso — ed elencava **13** skill a fronte di **18** directory con un `SKILL.md`.
Le cinque mancanti (`editoria`, `edizione`, `indagine`, `module-standard`,
`prosa-documenti`) sono tutte nate dopo l'ultima riscrittura della sezione.
Nessuna era stata rimossa: nessuna era mai stata aggiunta.

- [x] [ADR-0041](adr/ADR-0041-instradamento-delle-skill-con-un-gate.md):
      il principio prima degli esempi, e il gate bidirezionale
- [x] `AGENTS.md` §Skills riscritta: **principio** (chi legge, in che forma esce)
      → **tabella per compito** → **inventario completo** delle 18
- [x] `scripts/validate_skills.py`: quarto controllo **bloccante**, nelle due
      direzioni (skill orfana · puntatore morto)
- [x] `scripts/tests/test_skills_routing.py`: 5 test, di cui **tre che provano
      che il gate morde** — senza quelli, il test sul repo reale passerebbe
      anche con un gate vuoto

**Non fatto, e dichiarato**: i banner «Caricami quando» in testa a ciascun
`SKILL.md`. Sarebbero 18 file toccati per duplicare quello che il frontmatter
`description:` già dice agli agenti che lo leggono. Il difetto misurato era
l'**omissione nell'instradamento**, e quello lo chiude il gate.

---

## Lotto R3 — la legenda funzionale `[✅ recuperata, ⬜ non risolta]`

**Fonte**: PR #72, `docs/guides/LEGENDA-FUNZIONALE-SPEC.md`.

Il documento è stato recuperato e **ri-verificato sui numeri di oggi**, non
ricopiato: parte dei difetti che elencava sono già stati chiusi, e ne è emerso
uno nuovo che nella #72 non c'era.

| Simbolo | Stato oggi |
|---|---|
| 🗿 🗼 🏛 | ✅ già corretti dopo la #72 |
| ⛰ «Montagne / creste rocciose» | ⬜ **2.415 celle in 16 file** — ancora aperto |
| ⬛ «Struttura (tenda, edificio, dais)» | 🔴 **8.205 celle in 21 file** — **nuovo**: simbolo sovraccarico, tre significati diversi sotto un glifo |
| 🪨 | ✅ correttamente **non** un muro (copertura parziale) |

⚠️ ⬛ **non si chiude con una riga in `WALL_SYMS`.** Un dais non è un muro, una
tenda lo è a metà, un edificio lo è. Serve una **decisione di legenda** — cioè
tre glifi invece di uno — e cambierebbe gli SVG, non solo l'export. È una
domanda per il DM, non un fix.

---

## Cosa resta aperto

| # | PR | Giudizio | Cosa ne resta da fare |
|---|---|---|---|
| R4 | **#99** | **abbandonata, non superata** | È la più grossa: 88 file, `state.yaml` come sorgente dei fatti + `state.md` generato ([ADR-0017](https://github.com/gsamuele78/RumblingStone/pull/99)), 4 validatori nuovi, schede PG a dati, tre audit. Da valutare **a lotti**, non in blocco |
| R5 | **#106**, **#63**, **#52** | da giudicare | Analisi nel merito ancora da consegnare al DM |
| R6 | ⬛ legenda | **decisione DM** | Tre glifi o uno? Vedi R3 |
| R7 | Corona: +4 CAR e non-rimovibilità | **decisione DM** | Vedi R1 |

---

## Piano di validazione

Ogni lotto chiude solo se passano, **nello stesso commit**:

- `python3 -m pytest scripts/tests/ -q`
- `python3 scripts/validate_skills.py` (ora comprende il gate ADR-0041)
- `python3 scripts/dm.py doctor --ci`
- `python3 scripts/check_plans_discipline.py`
- per R1, in più: **zero** occorrenze residue dell'attribuzione sbagliata fuori
  dai log append-only (`plans/CHANGELOG.md`, `_ARCHIVIO/`), che restano com'erano
  perché sono record storici e non canone vivo
