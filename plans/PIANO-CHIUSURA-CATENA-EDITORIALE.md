# 🏗️ PIANO — Chiusura della catena editoriale

**Aperto**: 2026-08-27
**Mandato-fonte (DM)**: dopo il merge della PR #114 — *«guarda la seconda
standalone… se ci sono cose nuove non presenti in questo piano aggiungile come
altri punti. Poi vai da P1 a P8 e avanti, e poi anche quelli preesistenti, così
chiudiamo qualcosa — ovviamente con un plan»*.

**Da dove viene.** Tre documenti, in ordine di età:
[`RICERCA-AUDIT-COMPONENTI`](RICERCA-AUDIT-COMPONENTI-E-LIVELLO-EDITORIALE-2026-08.md)
(agosto: cinque difetti chiusi, quattro code aperte) ·
[`RICERCA-RUOLI-EDITORIALI-COLOPHON`](RICERCA-RUOLI-EDITORIALI-COLOPHON-PAIZO-2026-08.md)
(P1-P8, più l'addendum §8 con P9-P19) · la seconda standalone
`10-stand-alone/L'abbazia Della Rotta Sicura/`, che è insieme il modello e il
caso limite.

> **La riga da ricordare**: dei diciannove punti, **dodici non chiedono nessuna
> decisione** — sono lavoro che si può fare oggi. Tre sono decisioni del DM e
> bloccano gli altri quattro. Questo piano mette i dodici davanti.
>
> **Stato al 2026-09-02**: chiusi **A, B, C, D**. Restano **E** e **G** (nessuna
> decisione richiesta), **H1** (le 75 schede: fatica, non decisione) e **F**, che
> sono le quattro domande al DM. Il DM ha aggiunto **P20** (corpo + appendici) e
> confermato **P16** (tavole di supporto): entrambi chiusi dentro C.

---

## §1 · Lo stato in una tabella

Diciannove punti, più le quattro code preesistenti. La colonna «gate» è ciò che
decide l'ordine, non il costo.

| | Punto | Origine | Gate |
|---|---|---|---|
| P1 | Colophon nei volumi (crediti, licenza, edizione, versione, data) | colophon C1 | ✅ **fatto** (lotto B, ADR-0023) |
| P2 | Skill `rumblingstone-edizione` + gate IP d'uscita | colophon C1+C3 | ⚠️ ADR-0008 |
| P3 | Passate redazionali + `validate_lingua.py` | colophon C2 | 🟡 `validate_lingua` ✅ (D); le passate restano in E |
| P4 | **Vendoring dei pacchetti Typst** | colophon §5 | ⚠️ **DM** |
| P5 | `pdfcpu` per l'imposizione | colophon T1 | ⚠️ ADR |
| P6 | Server MCP sui 44 tool già descritti | colophon MCP-1 | — |
| P7 | veraPDF + caratteri per riga + daltonismo | colophon T3/T6/T7 | dopo P1 |
| P8 | `dm.py volume` — l'ordine dei mestieri | colophon §3.4 | dopo P1-P3 |
| P9 | Riscalatura a tre assi | Abbazia | ✅ (C) |
| P10 | Avvertenza di contenuto e consenso del tavolo | Abbazia | ✅ (C) |
| P11 | Igiene di licenza per documento | Abbazia | confluisce in P2 |
| P12 | ADR di modulo | Abbazia | ✅ (C) |
| P13 | Indirizzamento delle aree fra documenti + gate | Abbazia | ✅ (D) — trova 10 ambiguità vere |
| P14 | Il limite dichiarato del dry-run | Abbazia | ✅ (C) |
| P15 | Cancelli d'uscita a tempo per atto | Abbazia | ✅ (C) |
| P16 | Tavole non zenitali (veduta, profilo, tempi) | Abbazia | ✅ (C) — confermato dal DM |
| P17 | ⚠️ **L'Abbazia è fuori da ogni catena** | Abbazia | 🟡 **gate fatto** (lotto A); la conversione resta F4 |
| P18 | ⚠️ `LICENSE` GPL-3.0 su un'opera testuale | Abbazia | ⚠️ **DM** |
| P19 | Tabelle vive del borgo (dicerie false, reazione) | Abbazia | ✅ (C) |
| **P20** | ⭐ **Corpo + appendici** (punto nuovo del DM, 2026-09-02) | Abbazia | ✅ (C) — verificato che non era persa: **mai esistita** |
| — | E8: 75 schede di bestiario su 157 non migrate | audit ago. | fatica, non decisione |
| — | Capolettera annegato · indice analitico | audit ago. | = P4 |
| — | Imposizione | audit ago. | = P5 |
| — | CMYK / PDF-X | ADR-0020 | rinuncia dichiarata |

---

## §2 · I lotti

Ordinati per **quanto si chiude senza chiedere niente a nessuno**.

### ✅ Lotto A — Il gate che manca sull'Abbazia (P17, parte 1) — *chiuso 2026-09-02*

Il difetto più urgente dei nuovi, e la sua metà indolore.

*Il fatto*: `10-stand-alone/` non corrisponde a nessun pattern dei validatori —
la CI conosce `STANDALONE-*` (il Drappo) e basta. Quattro file, ~2.750 righe, e
**nessun controllo di nessun tipo**: un link rotto, un'area rinumerata o un file
rinominato non li vede nessuno finché non si apre al tavolo.

- [x] **A1** — `validate_standalone.py` riconosce `10-stand-alone/*/` come
      **seconda famiglia**: `<title>` non vuoto, almeno un `<h1>`, link relativi
      risolvibili, ancore esistenti **anche verso un altro file del modulo**,
      `id` non duplicati, termini 5e vietati sul testo spogliato dei tag.
- [x] **A2** — step CI rinominato e bloccante; 14 test in `test_standalone_html.py`,
      su cartelle temporanee e **non** sull'Abbazia (un test che dipende dal
      contenuto di un modulo vero diventa rosso il giorno in cui il DM lo riscrive).
- [x] **A3** — riga in `scripts/README-automation.md` + `tools.manifest.json`
      aggiornato e artefatti derivati rigenerati (`docs/tools/*`).

**Esito.** Verde sull'Abbazia com'è. Criterio d'accettazione soddisfatto su sei
casi: ancora rotta, `id` duplicato, `<h1>` tolto, link relativo inesistente,
ancora inesistente nel file di destinazione → **exit 1**; ripristinati → **exit 0**.

🔎 **Due cose trovate guardando, che il gate non può trovare da solo:**

1. **L'«indice navigabile delle 48 aree» non è navigabile**: `indice_maestro.html`
   non contiene **un solo** `href`. I 47 `href` del modulo sono tutti `#bg`/`#bgb`,
   cioè riferimenti interni alle tavole SVG. Non è un errore — non c'è niente di
   rotto — ma la promessa del titolo non è mantenuta. È contenuto del DM: **non
   toccato**. Va con P13 (lotto D), dove l'indirizzamento fra documenti diventa
   una convenzione.
2. Il modulo **non ha master markdown**: il validatore ora lo dice a ogni
   passata come *warning*, così la cosa non sembra normale. Resta la domanda F4.

**Deliverable**: un gate rosso se qualcuno rompe l'Abbazia.
**Criterio d'accettazione**: rompere di proposito un'ancora → CI rossa; ripararla → verde.
**Engine**: Sonnet · **impegno** medio · **dieta**: `scripts/validate_standalone.py`, `.github/workflows/ci.yml`, i 4 file dell'Abbazia.

> ⚠️ **Quello che questo lotto NON fa**: portare l'Abbazia dentro la catena
> (master markdown + manifest, ADR-0003). Quella è una conversione vera, sta nel
> **Lotto F**, e va decisa — non fatta di soppiatto.

### ✅ Lotto B — Il colophon (P1) — *chiuso 2026-09-02* · [ADR-0023](adr/ADR-0023-colophon-di-edizione.md)

*«Se si fa una cosa sola»*, dice la ricerca. Vale ancora, e ora vale di più:
l'Abbazia dimostra che anche il modulo meglio scritto del repo esce **anonimo,
senza licenza e senza versione**.

- [x] **B1** — un **oggetto** `colophon` nello schema, non cinque chiavi piatte
      (`edizione`, `versione`, `data`, `autori`, `basato_su`, `licenza`, `nota`),
      con `additionalProperties: false`. ⚠️ **Scostamento dal piano scritto**, e il
      motivo: cinque chiavi sciolte in cima al manifest sono cinque cose da
      ricordare; un oggetto è una cosa sola e si valida come tale. Ha richiesto di
      far **ricorrere `validate_booklets.py` negli oggetti annidati** — prima lo
      faceva solo per gli array, quindi un refuso lì dentro sarebbe passato in
      silenzio: esattamente il difetto che lo schema esiste per impedire.
- [x] **B2** — `#colophon()` nel tema: pagina **autonoma e senza testatina**, sul
      verso del frontespizio. La testatina c'era alla prima resa e ripeteva due
      volte lo stesso titolo — visto rendendo la pagina in PNG, non deducendolo.
- [x] **B3** — entrambe le catene la emettono, con **le stesse voci nello stesso
      ordine** (`VOCI_COLOPHON` in tutte e due, e un test che verifica siano
      identiche). Nessun `today()` in nessun punto.
- [x] **B4** — esemplare sul manifest del Palio: edizione, versione, data,
      `basato_su` (SRD 3.5 · OGL 1.0a · adattamento di *Red Hand of Doom*) e la
      riga di licenza che rimanda ad ADR-0005 e alla guida IP.
- [x] **B5** — 11 casi in `test_booklets.py`, fra cui la retrocompatibilità (senza
      la chiave il volume esce identico) e la parità d'ordine fra le catene.

**Esito.** Tutti e **11 i volumi del repo compilano davvero** (`validate_booklets
--stampa`, con typst 0.15.1, la stessa versione fissata in CI), e la pagina è
stata **guardata**, non solo compilata: resa in PNG e ispezionata, prima e dopo
la correzione della testatina.

⚠️ **Una riga che solo il DM può scrivere**: `autori` è deliberatamente **assente**
dal colophon del Palio. Inventare un nome in una pagina di crediti è peggio che
non averla.

**Deliverable**: PDF e HTML che portano il proprio nome, la propria data e la riga di licenza.
**Criterio d'accettazione**: `validate_booklets.py --stampa` verde e il colophon presente nel PDF compilato.
**Engine**: Sonnet · **impegno** medio · **dieta**: tema Typst, i due builder, lo schema, un manifest.

### ✅ Lotto C — Lo standard del modulo (P9, P10, P12, P14, P15, P19, **P20**) — *chiuso 2026-09-02*

Sei punti, tutti scrittura di skill, **zero decisioni**. È il lotto che trasforma
l'Abbazia da eccezione fortunata in regola.

- [x] **C0** — ⭐ **P20, punto nuovo del DM**: l'architettura **corpo + appendici** in testa a `module-standard`. Verificato che non era «persa» ma **mai esistita**: `grep -ril "appendice" skills/` non trova niente, nessun master `ARC*-DEF-*` la usa, il Drappo nemmeno. Il corpo è ciò che si gioca in ordine; le appendici sono ciò che si consulta a salto (bestiario, gazetteer, cast, incontri), numerate a lettere.
- [x] **C1** — `module-standard`: **riscalatura a tre assi** come sezione
      obbligatoria (livello · numero di PG · durata), con la colonna «cosa si
      perde davvero». Modello: l'indice maestro dell'Abbazia.
- [x] **C2** — `module-standard`: **avvertenza di contenuto e consenso**, con la
      sostituzione alternativa già scritta. Aggancio ad ADR-0018.
- [x] **C3** — `module-standard`: **cancelli d'uscita a tempo** per atto, con il
      rimedio (chi entra in scena e cosa dice se il segnale non è arrivato).
- [x] **C4** — convenzione **ADR di modulo**: quando una decisione è locale e
      quando sale in `plans/adr/`.
- [x] **C5** — `playtest`: la **dichiarazione del limite** del dry-run — cosa non
      ha potuto verificare, e perché solo il tavolo può.
- [x] **C6** — `narrative-style`/`indagine`: **dicerie con falsi deliberati** e
      **tabella di reazione**. Una diceria falsa è un nodo d'indizio a costo zero.
- [x] **C7** — `playtest` §2.6 rimanda a C1 invece di coprire il solo numero di giocatori.
- [x] **C8** — **P16 confermato dal DM** («per le mappe vanno bene le verticali,
      aggiungendo anche le visualizzazioni presenti nella standalone»):
      `mapmaking` guadagna **le tavole di supporto** — veduta, profilo laterale con
      quote e **tempi di percorrenza** — con la regola che si aggiungono *quando
      rispondono a una domanda che la griglia non può*, non per completezza, e la
      numerazione `Tavola I` / `I-a` / `I-b` che le tiene riconoscibili come lo
      stesso luogo visto in un altro modo.

**Deliverable**: sei convenzioni scritte dove un agente le incontra.
**Criterio d'accettazione**: `validate_skills.py` verde; ogni voce cita l'Abbazia come implementazione di riferimento.
**Engine**: Opus (sono decisioni di design) · **impegno** alto · **dieta**: le tre skill toccate + le sezioni citate dell'Abbazia, **non** i quattro file interi.

### ✅ Lotto D — I gate a macchina (P13, P3) — *chiuso 2026-09-02*

- [x] **D1** — **numerazione delle aree**: prefisso di livello obbligatorio, e
      `validate_modules.py` che rifiuta una collisione fra documenti dello stesso
      modulo. È il difetto **D1 del dry-run dell'Abbazia** (16/17/18 usati tre
      volte su tre file): una macchina lo trova gratis, un umano lo trova al tavolo.
- [x] **D2** — `scripts/validate_lingua.py`, stdlib: perché/perchè, virgolette
      dritte, doppi spazi, apostrofi, d eufonica. Non bloccante alla prima
      passata, poi bloccante quando il rumore è a zero.
- [x] **D3** — entrambi in CI + `tools.manifest.json` + `README-automation` + test.

**Esito.**

- **D1** trova **dieci ambiguità vere e tuttora aperte** nell'Abbazia: il dry-run
  del modulo aveva corretto la numerazione nelle *chiavi* con i prefissi di
  livello, ma i rimandi **in prosa** sono rimasti nudi — 55 `area N` senza
  prefisso, e dieci numeri (`area 6`, `area 27`…) usati in **file diversi**. Da
  fuori non si distingue se sono la stessa stanza o due. È **warning**, non
  errore: la convenzione nasce oggi.
- **D2** trova **23 refusi** in 494 file di contenuto: spazi prima della
  punteggiatura, doppi spazi, un «ad Damarath». Anche questo **non bloccante in
  CI** (`continue-on-error`), come `validate_bestiario --rules`: diventa `--strict`
  il giorno in cui il rumore è a zero. Un validatore rumoroso viene disattivato
  entro una settimana, e allora non trova più nemmeno i refusi veri.
  ⚠️ **La prima passata produsse 423 rilievi, quasi tutti creati dal validatore
  stesso**: mascherava il codice inline con *uno spazio* e poi segnalava i doppi
  spazi che aveva introdotto. Metà dei 14 test esistono per quel difetto.
  Esentate anche le **guide alla pronuncia** (`*nè-this*`), dove l'accento grave
  dice il suono ed è messo apposta.

### ⬜ Lotto E — La skill dell'edizione (P2, P11, P3-prosa) ⚠️ ADR-0008

- [ ] **E1** — ADR: perché la diciassettesima skill è giustificata (la
      motivazione è già scritta nella ricerca §3.1; qui diventa decisione).
- [ ] **E2** — `skills/rumblingstone-edizione/`: colophon, dichiarazioni Product
      Identity/Open Content, **gate d'uscita** (la checklist §7 di
      `GUIDA-CONDIVISIONE-IP.md`, che oggi nessuna skill carica), versione ed errata.
- [ ] **E3** — **igiene di licenza per documento** (P11) come tabella obbligatoria
      in stesura. L'Abbazia è l'implementazione di riferimento: ha separato le
      divinità inventate dai nomi FR non-SRD *prima* del commit, non dopo.
- [ ] **E4** — `references/passate-redazionali.md` in `narrative-style`: le tre
      passate, quando un master è chiuso, come si riapre.

**Deliverable**: il mestiere dell'editore, caricabile da un agente.
**Criterio d'accettazione**: un agente che genera un handout incontra il gate IP **prima** di consegnare.
**Engine**: Opus · **impegno** alto · **dieta**: guida IP, ADR-0005/0008/0016, `editorial-standards.md`.

### ⬜ Lotto F — Le decisioni del DM (P4, P5, P18, P17 parte 2)

Qui non si esegue: si chiede. Ogni voce è una domanda sola con una risposta sola.

- [ ] **F1** — **Si vendorizzano i pacchetti Typst** nella cache locale, con la
      loro licenza, come ADR-0010 fa per le skill di terzi? → **sì** sblocca
      capolettera annegato **e** indice analitico (`droplet` + `in-dexter`); **no**
      li chiude entrambi come «non si fa».
- [ ] **F2** — **Si accetta `pdfcpu`** (Apache-2.0, binario Go singolo, offline,
      `booklet` nativo) come seconda dipendenza binaria dopo Typst? → sblocca
      l'imposizione. Richiede un ADR con la regola di degradazione pulita.
- [ ] **F3** — **`LICENSE` GPL-3.0 su un'opera testuale**: si corregge? La GPL è
      scritta per il software; il repo è per tre quarti prosa. Candidati per il
      testo: CC BY-NC-SA (coerente con ADR-0005, uso non commerciale) tenendo la
      GPL — o la MIT — sui soli `scripts/`. ⚠️ **Non è una modifica cosmetica**:
      cambia cosa altri possono fare col materiale, e va decisa dal DM.
- [ ] **F4** — **L'Abbazia si converte** a master markdown + manifest (ADR-0003),
      o si dichiara un'eccezione motivata? Convertirla la fa entrare nelle due
      catene, le dà un colophon e la rende impaginabile; lasciarla com'è è
      legittimo, ma va **scritto**, non sottinteso.

**Deliverable**: quattro risposte, ognuna con il suo ADR.
**Engine**: nessuno — è una conversazione col DM.

### ⬜ Lotto G — Infrastruttura (P6, P7, P8, P16)

- [ ] **G1** — **server MCP** sui 44 tool di `docs/tools/mcp-tools.json`: JSON-RPC
      su stdio, stdlib, zero dipendenze. Chiude la promessa di ADR-0012.
- [ ] **G2** — veraPDF in CI (fa togliere da solo il ripiego `--no-pdf-tags`),
      misura dei **caratteri per riga** sul PDF compilato, simulatore di
      daltonismo sulle mappe.
- [ ] **G3** — `dm.py volume`: la catena dei mestieri in ordine, che assorbe anche
      il `dm.py stampa` mai fatto.
- [ ] **G4** — `mapmaking`: **tavole non zenitali** — veduta prospettica e profilo
      laterale con quote, distanze e **tempi di percorrenza**.

**Engine**: Sonnet (G1-G3), Opus (G4: è una convenzione) · **impegno** medio-alto.

### ⬜ Lotto H — Le code preesistenti

- [ ] **H1** — **E8**: le 75 schede di bestiario su 157 non ancora migrate al
      formato machine-readable (ADR-0021). Non è una decisione, è fatica: o si
      completano, o si accetta che la libreria abbia due velocità — e si scrive.
- [ ] **H2** — capolettera annegato + indice analitico → **gated su F1**.
- [ ] **H3** — imposizione → **gated su F2**.
- [ ] **H4** — CMYK/PDF-X: **rinuncia confermata** (ADR-0020), si riapre solo il
      giorno di una tiratura vera.

---

## §3 · L'ordine consigliato

```
  A ──► B ──► D ──► G2  (nessuna decisione: si può partire oggi)
        │
  C ────┤     (parallelo ad A/B: tocca skill, non codice)
        │
  E ────┘     (dopo B, perché il colophon è il suo primo oggetto)

  F ──► H2, H3, G3   (tutto ciò che aspetta il DM)
```

**Se si fa un lotto solo**: **A**. Non perché sia il più prezioso — lo è B — ma
perché è l'unico dove oggi il repo è *cieco*: 2.750 righe senza nessun controllo
sono il posto dove il prossimo difetto arriverà al tavolo invece che alla CI.

---

## §4 · Cosa questo piano NON fa

Scritto qui perché non si riapra a ogni lotto.

1. **Non riapre le rinunce già decise**: niente edizione inglese (ADR-0016),
   niente CMYK/PDF-X (ADR-0020), niente skill di traduzione o di vendite
   (ADR-0005). Restano no.
2. **Non converte l'Abbazia di nascosto.** Il Lotto A le dà un gate; la
   conversione è F4, ed è una domanda.
3. **Non aggiunge skill per simmetria.** Una sola nuova (`rumblingstone-edizione`,
   Lotto E), e con l'ADR-0008 davanti. Tutto il resto sono estensioni.
4. **Non tocca il contenuto giocato.** Nessun lotto qui riscrive una scena, un
   read-aloud o un canone: è tutto apparato, gate e supporto.
