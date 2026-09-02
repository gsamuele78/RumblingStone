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

---

## §1 · Lo stato in una tabella

Diciannove punti, più le quattro code preesistenti. La colonna «gate» è ciò che
decide l'ordine, non il costo.

| | Punto | Origine | Gate |
|---|---|---|---|
| P1 | Colophon nei volumi (crediti, licenza, edizione, versione, data) | colophon C1 | — |
| P2 | Skill `rumblingstone-edizione` + gate IP d'uscita | colophon C1+C3 | ⚠️ ADR-0008 |
| P3 | Passate redazionali + `validate_lingua.py` | colophon C2 | — |
| P4 | **Vendoring dei pacchetti Typst** | colophon §5 | ⚠️ **DM** |
| P5 | `pdfcpu` per l'imposizione | colophon T1 | ⚠️ ADR |
| P6 | Server MCP sui 44 tool già descritti | colophon MCP-1 | — |
| P7 | veraPDF + caratteri per riga + daltonismo | colophon T3/T6/T7 | dopo P1 |
| P8 | `dm.py volume` — l'ordine dei mestieri | colophon §3.4 | dopo P1-P3 |
| P9 | Riscalatura a tre assi | Abbazia | — |
| P10 | Avvertenza di contenuto e consenso del tavolo | Abbazia | — |
| P11 | Igiene di licenza per documento | Abbazia | confluisce in P2 |
| P12 | ADR di modulo | Abbazia | — |
| P13 | Indirizzamento delle aree fra documenti + gate | Abbazia | — |
| P14 | Il limite dichiarato del dry-run | Abbazia | — |
| P15 | Cancelli d'uscita a tempo per atto | Abbazia | — |
| P16 | Tavole non zenitali (veduta, profilo, tempi) | Abbazia | — |
| P17 | ⚠️ **L'Abbazia è fuori da ogni catena** | Abbazia | parziale |
| P18 | ⚠️ `LICENSE` GPL-3.0 su un'opera testuale | Abbazia | ⚠️ **DM** |
| P19 | Tabelle vive del borgo (dicerie false, reazione) | Abbazia | — |
| — | E8: 75 schede di bestiario su 157 non migrate | audit ago. | fatica, non decisione |
| — | Capolettera annegato · indice analitico | audit ago. | = P4 |
| — | Imposizione | audit ago. | = P5 |
| — | CMYK / PDF-X | ADR-0020 | rinuncia dichiarata |

---

## §2 · I lotti

Ordinati per **quanto si chiude senza chiedere niente a nessuno**.

### ⬜ Lotto A — Il gate che manca sull'Abbazia (P17, parte 1)

Il difetto più urgente dei nuovi, e la sua metà indolore.

*Il fatto*: `10-stand-alone/` non corrisponde a nessun pattern dei validatori —
la CI conosce `STANDALONE-*` (il Drappo) e basta. Quattro file, ~2.750 righe, e
**nessun controllo di nessun tipo**: un link rotto, un'area rinumerata o un file
rinominato non li vede nessuno finché non si apre al tavolo.

- [ ] **A1** — `validate_standalone.py` riconosce anche `10-stand-alone/*/`, con
      i controlli che valgono su HTML: link interni risolvibili, ancore
      `href="#..."` esistenti, titoli non duplicati.
- [ ] **A2** — step in CI, bloccante.
- [ ] **A3** — riga in `scripts/README-automation.md`.

**Deliverable**: un gate rosso se qualcuno rompe l'Abbazia.
**Criterio d'accettazione**: rompere di proposito un'ancora → CI rossa; ripararla → verde.
**Engine**: Sonnet · **impegno** medio · **dieta**: `scripts/validate_standalone.py`, `.github/workflows/ci.yml`, i 4 file dell'Abbazia.

> ⚠️ **Quello che questo lotto NON fa**: portare l'Abbazia dentro la catena
> (master markdown + manifest, ADR-0003). Quella è una conversione vera, sta nel
> **Lotto F**, e va decisa — non fatta di soppiatto.

### ⬜ Lotto B — Il colophon (P1)

*«Se si fa una cosa sola»*, dice la ricerca. Vale ancora, e ora vale di più:
l'Abbazia dimostra che anche il modulo meglio scritto del repo esce **anonimo,
senza licenza e senza versione**.

- [ ] **B1** — chiavi `credits`, `license`, `edition`, `version`, `date` in
      `scripts/schemas/booklet_manifest.schema.json`.
- [ ] **B2** — `#colophon()` nel tema Typst: opera, base OGL/SRD, versione, data,
      autore, regime d'uso. Faccia del repo (avorio/seppia/rosso), non trade dress altrui.
- [ ] **B3** — `export_booklet_typst.py` e `build_booklet_html.py` la emettono
      entrambe; la data viene dal manifest, **mai** da `today()` (rovinerebbe il
      determinismo byte-identico).
- [ ] **B4** — un manifest esistente aggiornato come esemplare (il Palio).
- [ ] **B5** — caso in `scripts/tests/test_booklets.py`.

**Deliverable**: PDF e HTML che portano il proprio nome, la propria data e la riga di licenza.
**Criterio d'accettazione**: `validate_booklets.py --stampa` verde e il colophon presente nel PDF compilato.
**Engine**: Sonnet · **impegno** medio · **dieta**: tema Typst, i due builder, lo schema, un manifest.

### ⬜ Lotto C — Lo standard del modulo (P9, P10, P12, P14, P15, P19)

Sei punti, tutti scrittura di skill, **zero decisioni**. È il lotto che trasforma
l'Abbazia da eccezione fortunata in regola.

- [ ] **C1** — `module-standard`: **riscalatura a tre assi** come sezione
      obbligatoria (livello · numero di PG · durata), con la colonna «cosa si
      perde davvero». Modello: l'indice maestro dell'Abbazia.
- [ ] **C2** — `module-standard`: **avvertenza di contenuto e consenso**, con la
      sostituzione alternativa già scritta. Aggancio ad ADR-0018.
- [ ] **C3** — `module-standard`: **cancelli d'uscita a tempo** per atto, con il
      rimedio (chi entra in scena e cosa dice se il segnale non è arrivato).
- [ ] **C4** — convenzione **ADR di modulo**: quando una decisione è locale e
      quando sale in `plans/adr/`.
- [ ] **C5** — `playtest`: la **dichiarazione del limite** del dry-run — cosa non
      ha potuto verificare, e perché solo il tavolo può.
- [ ] **C6** — `narrative-style`/`indagine`: **dicerie con falsi deliberati** e
      **tabella di reazione**. Una diceria falsa è un nodo d'indizio a costo zero.
- [ ] **C7** — `playtest` §2.6 rimanda a C1 invece di coprire il solo numero di giocatori.

**Deliverable**: sei convenzioni scritte dove un agente le incontra.
**Criterio d'accettazione**: `validate_skills.py` verde; ogni voce cita l'Abbazia come implementazione di riferimento.
**Engine**: Opus (sono decisioni di design) · **impegno** alto · **dieta**: le tre skill toccate + le sezioni citate dell'Abbazia, **non** i quattro file interi.

### ⬜ Lotto D — I gate a macchina (P13, P3)

- [ ] **D1** — **numerazione delle aree**: prefisso di livello obbligatorio, e
      `validate_modules.py` che rifiuta una collisione fra documenti dello stesso
      modulo. È il difetto **D1 del dry-run dell'Abbazia** (16/17/18 usati tre
      volte su tre file): una macchina lo trova gratis, un umano lo trova al tavolo.
- [ ] **D2** — `scripts/validate_lingua.py`, stdlib: perché/perchè, virgolette
      dritte, doppi spazi, apostrofi, d eufonica. Non bloccante alla prima
      passata, poi bloccante quando il rumore è a zero.
- [ ] **D3** — entrambi in CI + `tools.manifest.json` + test.

**Deliverable**: due controlli che costano una volta e pagano sempre.
**Criterio d'accettazione**: golden case che fallisce prima e passa dopo, per ciascuno.
**Engine**: Sonnet · **impegno** medio · **dieta**: i due validatori + un modulo campione.

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
