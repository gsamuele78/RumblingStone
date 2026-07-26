# PIANO — LEVEL DESIGN DELLE MAPPE E INQUADRATURA SCENICA

> **Origine**: guida operativa **«Dall'immagine mentale all'artefatto»**
> (2026-07-25, fornita dal DM) — Parte I §0-§10 (composizione visiva) e
> Parte II §L1-§L9 (level design e codifica nel toolkit).
> **Misura dello scarto**: [`docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md`](../docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md)
> — ogni lotto qui sotto rimedia a un buco misurato lì, mai a un'impressione.
> **Decisione architetturale portante**: [ADR-0014](adr/ADR-0014-legenda-funzionale-fonte-unica.md)
> (legenda funzionale come fonte unica) — **stato: proposta, gate DM**.
> **Stato**: 🔵 pianificato · **Data**: 2026-07-26 · **% completamento**: 0%

---

## 0. Il problema, in una riga

Il toolkit ha una pipeline di **produzione** matura (40 tool a contratto, CI
deterministica, 3 modalità mappa) e **nessuna pipeline di progettazione**: sa
disegnare qualunque cosa gli si dica, e non ha modo di dire se ciò che gli si
è detto di disegnare fosse una buona mappa o una buona inquadratura.

Le due conseguenze misurate:

- **mappe** — su 29 griglie ≥12×12: mediana M1 = 0.30 (soglia ≥0.60),
  M2 = 0.51 (≤0.20), M4 = 0.84 (≤0.45), M8 = 0 (≥3); **15/15** delle mappe con
  token PG+nemico fuori dalla banda 2-4 round. Gli interni passano, **tutti**
  gli esterni falliscono;
- **immagini** — su 48 blocchi prompt: **0** dichiarano focale, altezza camera,
  figura di scala o prospettiva atmosferica.

E un difetto strutturale che vale da solo il primo lotto: **l'SVG e l'export
UVTT della stessa mappa non concordano su cosa sia un muro** (`⛰` occlude
nell'SVG e non blocca la vista in Foundry; `🏛 🗼 🗿` il contrario).

## 1. Obiettivo e non-obiettivi

**Obiettivo**: portare nel toolkit, come **dato e come gate**, la disciplina di
level design (affordance misurabili, intento dichiarato e verificato) e quella
di inquadratura (blockout geometrico prima della generazione, ordine percettivo
nella prosa).

**Non-obiettivi dichiarati** — per non far crescere il piano oltre il suo scopo:

- ❌ non si riprogettano tutte le mappe del repo (solo le 3 di §C2; il resto è
  gated dal tavolo);
- ❌ il linter **non è bloccante**, mai: apre una domanda, non chiude una porta
  (una mappa può violare ogni soglia ed essere ottima — un ponte stretto sopra
  il vuoto viola M1, M2, M3 e M4 *di proposito*);
- ❌ non si costruisce l'editor visuale (piano separato);
- ❌ non si punta a un prodotto commerciale: i confini restano ADR-0005.

## 2. Principi vincolanti

1. **Il dato prima dello strumento.** Nessuna metrica viene implementata prima
   che la sua informazione esista come dato interrogabile (A prima di B).
2. **Advisory, non bloccante** — come già `validate_bestiario --rules`.
3. **Soglie euristiche finché non calibrate** (§L5.4): prima della
   calibrazione sono un'opinione informata, e vanno dichiarate come tali nei
   messaggi del tool.
4. **Nessuna regressione visiva**: i 17 SVG legacy restano byte-identici
   (`validate_maps.py`) attraverso ogni refactor.
5. **Ogni tool nuovo è ADR-0012-conforme**: manifest, exit code, determinismo
   dichiarato, `--help` senza side-effect, test, smoke in CI.
6. **La calibrazione non usa mappe RHoD** (ADR-0005): solo materiale proprio o
   liberamente licenziato, con corpus dichiarato.

---

## 3. Lotti

Legenda impegno: **engine consigliato** e **livello** secondo la regola DM
2026-07-22 (piani con routing engine).

### Ramo A — Fondamenta dati (prerequisito di tutta la Parte II)

#### ⬜ A1 — Legenda funzionale come fonte unica (`scripts/legend.yaml`)

*Rimedia*: audit §2.1 (due fonti di verità, già divergenti).
**È il lotto E1 di `PIANO-EDITOR-VISUALE-MAPPE-TATTICHE`** — si esegue una
volta e serve tre piani (editor, linter, export). Non duplicare.

Promuovere la funzione di gioco a dato di prima classe:

```yaml
symbols:
  "🪨":
    label: "Rocce / macerie"
    render: {mode: icon, prop: pr_rocks, fill: "#ced4da"}
    function:
      blocks_movement: false
      blocks_sight: false
      cover: half              # none | half | full
      difficult_terrain: true
      elevation_m: 0
      destructible: true
      nameable: true           # → landmark, M8 / Lynch
  "🏰":
    label: "Muro / roccia solida"
    render: {mode: fill, pat: t_wall, fill: "#3f3931"}
    function: {blocks_movement: true, blocks_sight: true, cover: full, nameable: false}
```

- `render_map_svg.SYMBOLS` diventa **derivato** dal YAML (parser stdlib o
  `export_legend_json.py` → `legend.json` committato + gate di sync in CI,
  come già si fa per `docs/tools/`);
- `export_uvtt.py` deriva muri/porte/luci da `function`, **elimina**
  `WALL_SYMS`/`DOOR_SYMS`/`LIGHT_SYMS`; `import_ultraclear.HAZARD_SYMS` idem;
- `references/legenda-universale.md` si **genera** dal YAML;
- **decidere esplicitamente** i 4 simboli divergenti: `⛰` (muro o copertura
  totale non-muro?), `🏛 🗼 🗿` (muro pieno o prop occludente?). È una
  decisione di regole 3.5, non di codice → va nel changelog.

**Accettazione**: nessun set di simboli cablato resta in `scripts/`;
`validate_maps.py` verde con i 17 SVG legacy **byte-identici**; round-trip
UVTT della CI verde; `⛰` e `🏛🗼🗿` classificati coerentemente fra SVG e UVTT;
gate di sync YAML↔`legenda-universale.md` rosso se divergono.
**Engine**: Opus (modello di dominio + le 4 decisioni) → Sonnet (migrazione
meccanica dei consumatori). **Impegno**: alto. **Stima**: 12-16 h.

#### ⬜ A2 — Zone, elevazione e intento nel contratto JSON (schema v1.1)

*Rimedia*: audit §2.2, §2.3, §2.4 (M3 e M6 senza supporto dati; nessun intento).

- `zones[]`: `name` (nominabile), `rect`/`polygon`, `elevation_m`,
  `connects_to[]` → **il grafo su cui si calcola M3**, distinto dal `@zone`
  attuale che resta un bracket di presentazione;
- `design_intent{}` secondo §L5.6: `combat_role`, `expected_party`,
  `intended_rounds`, `tactical_axes`, `central_decision`, `landmarks`,
  `elevation_bands`, `evolution`;
- `compile_map_json.py` emette le direttive nuove; `render_map_svg.py` rende
  le bande di elevazione (banda leggera + etichetta quota, non un secondo
  livello di disegno).

**Accettazione**: lo schema v1.1 valida **invariati** i contratti esistenti
(`scripts/examples/*.json`); un esempio nuovo con 3 bande di elevazione e
`design_intent` compila, rende e passa `validate_maps`; il campo elevazione
raggiunge l'export UVTT o è dichiarato «non trasportabile» nel README.
**Engine**: Opus (schema) → Sonnet (compilatore/renderer). **Impegno**: alto.
**Stima**: 10-14 h. **Dipende da**: A1.

#### ⬜ A3 — Discriminante `map_kind`

*Rimedia*: audit §3.4 — 8 griglie su 29 non sono battlemap (viste strategiche,
sezioni, panoramiche) e nulla nel formato lo dichiara.

`map_kind: battle | strategic | schematic | overland`, nel contratto **e** come
riga d'intestazione dei master ultra-clear. Il linter valuta solo `battle`.

**Accettazione**: le 8 griglie non-tattiche del corpus marcate; il linter le
salta con una riga informativa, non con un warning.
**Engine**: Sonnet. **Impegno**: basso. **Stima**: 3-4 h. **Dipende da**: A1.

---

### Ramo B — Il linter di level design

#### ⬜ B1 — `scripts/lint_map_design.py`, metriche senza visibilità

*Realizza*: §L5.1-L5.2 per M1, M2, M7, M8, M9 (+ conteggio strozzature).

- modello di dominio in `dmcore/mapmodel.py` — **non** `dmcore/visibility.py`,
  già occupato dalla policy spoiler dei session log (audit §2.5);
- legge la funzione dei simboli da A1: **nessun set hardcoded**;
- output umano + `--json`; advisory (exit 0 salvo `--strict`);
- i messaggi dichiarano che le soglie sono pre-calibrazione.

**Accettazione**: ADR-0012 pieno (manifest, `--help` pulito, exit code,
determinismo); rieseguito sul corpus riproduce le mediane di audit §3.1 entro
tolleranza, con le differenze da A1 **documentate**; test su fixture
sintetiche (corridoio lineare, campo aperto, arena con anello).
**Engine**: Sonnet (implementazione) con Opus sul disegno delle interfacce.
**Impegno**: medio-alto. **Stima**: 10-12 h. **Dipende da**: A1, A3.

#### ⬜ B2 — Metriche costose: M3 anelli, M4/M5 visibilità, M6 verticalità

- **M3** su grafo delle **zone** (A2), mai sulle celle — μ = E − V + 1;
  strozzature = punti di articolazione dello stesso grafo;
- **M4/M5** in `dmcore/los.py`: Bresenham fermato dai bloccanti vista, con
  **campionamento** (1 cella ogni 3 per lato → 1/9 del costo). 40×40
  tutto-percorribile = ~2,5 M raycast: in Python puro sono minuti, in CI il
  campionamento basta e avanza;
- **M6** dal campo `elevation_m` di A2.

**Accettazione**: linter completo su una mappa 40×40 in < 10 s; M3 = 2 sulla
fixture ad anello e 0 sul corridoio; risultato deterministico (seme fisso del
campionamento).
**Engine**: Sonnet. **Impegno**: medio-alto. **Stima**: 10-14 h.
**Dipende da**: A2, B1.

#### ⬜ B3 — Dichiarato contro realizzato (`design_intent`)

*Realizza*: §L5.6 — **la parte che nessun altro strumento sul mercato fa.**

```
⚠ tactical_axes include "verticality" ma M6 = 1 livello
  → asse dichiarato e non realizzato
⚠ landmark "albero-fulminato" dichiarato in [14,12] ma la cella
  contiene 🟩 (nameable: false) → non riconoscibile al tavolo
⚠ combat_role = "ambush" ma M4 = 0.91 → i PG vedono tutto entrando
```

Nessuna soglia arbitraria: il metro è la dichiarazione dell'autore.

**Accettazione**: i 3 casi sopra riprodotti da fixture; una mappa senza
`design_intent` non produce alcun warning di questa classe.
**Engine**: Sonnet. **Impegno**: medio. **Stima**: 8-10 h. **Dipende da**: A2, B2.

#### ⬜ B4 — Integrazione: CI, manifest, docs, skill

```
□ scripts/tools.manifest.json                 (gate ADR-0012)
□ docs/tools/                                 rigenerato dal manifest
□ scripts/README-automation.md                tool map + sottocomando dm.py maps lint
□ .github/workflows/ci.yml                    step con continue-on-error: true
□ skills/rumblingstone-mapmaking/references/level-design-metriche.md
```

**Accettazione**: `tools_manifest --check` pulito; CI verde con lo step
advisory presente e **non bloccante**; `validate_skills.py` verde.
**Engine**: Haiku (meccanico). **Impegno**: basso. **Stima**: 3-4 h.
**Dipende da**: B1.

#### ⬜ B5 — Calibrazione delle soglie su corpus dichiarato

*Realizza*: §L5.4 — è ciò che separa questo strumento da un blog post con dei
numeri inventati.

10-15 mappe **che si sa funzionare al tavolo**, di proprietà o liberamente
licenziate (Dyson Logos rilascia molto con licenza permissiva) → trascritte in
griglia → misurate → soglie ai **percentili della distribuzione reale**, non ai
numeri della guida. Corpus e licenze documentati in
`references/level-design-metriche.md`.

> ⚠️ **Vincolo ADR-0005**: nessuna mappa RHoD nel corpus di calibrazione.

**Accettazione**: ogni soglia del tool ha accanto il percentile e la
dimensione del corpus; le soglie pre-calibrazione sono sostituite, non
affiancate.
**Engine**: Sonnet (trascrizione) + Opus (scelta dei percentili).
**Impegno**: medio. **Stima**: 12-16 h. **Dipende da**: B2. **Gate**: decisione
DM sul corpus.

---

### Ramo C — Il debito di contenuto (le mappe)

#### ⬜ C1 — `campaign/templates/scheda-mappa-template.md`

*Realizza*: §L6. **Si compila prima di disegnare**, ed è il gemello della
scheda-inquadratura (D1). Contiene: intento (la domanda che i giocatori devono
porsi · come si vince, mai «uccidere tutti» · come si perde, mai TPK gratuito),
i cinque elementi di Lynch (path/edge/district/node/landmark), i sei parametri
(anelli, copertura, linee di vista, verticalità, strozzature, distanza
d'ingaggio), l'ambiente dinamico, i target del linter e le **deroghe motivate**.

Il template esistente `mappa-tattica-template.md` resta e non si tocca: norma
la **resa** (Ambiente/Tattiche/Evoluzione); la scheda-mappa norma il
**progetto**. Il puntatore reciproco va scritto in entrambi.

**Accettazione**: template committato, referenziato dalla skill mapmaking, e
compilato su **una** mappa reale come esempio vivo.
**Engine**: Opus (è design). **Impegno**: medio. **Stima**: 4-6 h.
**Indipendente da A/B** — candidabile per primo.

#### ⬜ C2 — Riprogettazione delle 3 mappe peggiori

Dalla classifica di audit §3.2, in ordine di urgenza al tavolo:

1. **Dirupo Mortale / Campo Hobgoblin** (ARC-08, 40×40) — M1 0.03 · M2 0.97 ·
   M4 0.88 · M8 0 · M9 1.5. Riprogettazione secondo §L7: 3-4 coperture nel
   terzo centrale, 3 landmark asimmetrici nominabili (l'albero fulminato, il
   carro bruciato, il masso spaccato), 3 bande di elevazione (canalone −2 m ·
   campo 0 · costone +3 m), un secondo accesso che chiuda un anello, una
   linea di vista bloccata che divida il campo, e un **orologio** (il fuoco di
   segnalazione entro il round 6 → sconfitta = incontro successivo +1 GS, non
   TPK);
2. **Ondata 2 Positions** (26×26) — M1 0.00, M2 1.00;
3. **Ground Battle** (30×71) — da valutare: se è una vista strategica va
   marcata `map_kind: strategic` (A3) invece che riprogettata.

**Non aggiungere decorazioni: aggiungere compromessi.** Il criterio non è «più
bella» ma «ogni posizione comporta un guadagno e una perdita».

**Accettazione**: per ciascuna, scheda-mappa compilata **prima**; dopo la
riprogettazione M1 ≥ 0.60, M2 ≤ 0.20, M8 ≥ 3, M9 ∈ [2,4], o deroga scritta e
motivata; SVG rigenerato; companion Ambiente/Tattiche/Evoluzione aggiornati.
**Engine**: Opus (design) → Sonnet (griglia). **Impegno**: alto.
**Stima**: 6-8 h a mappa. **Dipende da**: C1, B1. **Gate**: prova al tavolo.

#### ⬜ C3 — Parity pass sul resto del corpus

Le ~26 griglie restanti, una alla volta, su decisione DM. Le mappe che il
linter promuove già (le caverne: *Cuore della Montagna* M1 1.00 · M2 0.00,
*Stanza della Corona* M1 0.88) **non si toccano**.

**Engine**: Sonnet. **Impegno**: medio. **Gate**: tavolo, a mappa singola.

---

### Ramo D — Inquadratura e prosa (indipendente da A/B/C)

#### ⬜ D1 — Scheda-inquadratura e campo `## Inquadratura`

*Realizza*: §2 e §3.6. Aggiungere a `campaign/ai-media-prompts/` il blocco
strutturato — formato, focale, altezza e inclinazione camera, **momento**
(l'istante esatto, non il luogo), primo piano / piano medio / sfondo, struttura
dei valori, **figura di scala**, elemento vivo, atmosfera, **ancora non
visiva** (che serve al read-aloud, non all'immagine).

Riscrittura dei prompt nella struttura in cinque blocchi
(`soggetto e momento · inquadratura · luce e valore · atmosfera · medium`), a
sostituzione di `[STILE] [SCENA] [CAMERA] [PALETTE]` che ordina per categoria
di metadato invece che per costruzione dell'immagine.

**Retrofit**: non tutti i 48 blocchi. Le **3 scene chiave di ARC-07** come
pilota, poi si valuta.

**Accettazione**: template nel repo; 3 schede compilate; ogni scheda dichiara
focale, altezza camera e figura di scala (oggi: 0/48).
**Engine**: Opus (le schede sono design) → Sonnet (retrofit).
**Impegno**: medio. **Stima**: 6-8 h.

#### ⬜ D2 — Regola d'ordine percettivo nel read-aloud ⭐

*Realizza*: §6. **È l'item a ritorno più alto dell'intero piano**: nessuna GPU,
nessun Blender, nessun codice — e agisce su ciò che il repo produce di più.

In `skills/rumblingstone-narrative-style/references/editorial-standards.md` §2
(che oggi norma texture e tipografia, mai l'ordine di rivelazione — audit §4.3)
aggiungere le tre regole:

1. descrivere nell'**ordine in cui la percezione arriva**:
   non-visivo → primo piano → piano medio → sfondo;
2. dare la scala per **rapporto prima che per numero** («le spalle a metà della
   volta», *poi* «e la volta è a diciotto metri»);
3. inquadrare **un momento**, non un luogo — e chiudere su qualcosa che si
   muove, restituendo il turno ai giocatori.

Con l'esempio prima/dopo della Forgia Adamantina come riferimento canonico.

**Accettazione**: regola nella skill; `build-skills.sh --no-deploy` e
`validate_skills.py` verdi; **un** read-aloud esistente riscritto secondo la
regola e provato al tavolo.
**Engine**: Opus. **Impegno**: medio. **Stima**: 4-5 h. **Gate accettazione
finale**: prova al tavolo.

#### ⬜ D3 — Modalità 4: blockout 3D → depth → illustrazione

*Realizza*: §3, §5. La quarta modalità mancante — l'unica che parte
dall'immagine mentale invece che da un artefatto 2D esistente, e l'unica con
provenienza al 100% originale (rilevante sotto ADR-0005).

```
scripts/blockout/
├─ render_blockout.py     # Blender headless: clay + depth normalizzata
├─ README.md              # contratto I/O secondo ADR-0012
└─ scenes/                # .blend, gitignorati (binari pesanti)
rendered/blockout/        # gitignorata: output non deterministico, non canone
skills/rumblingstone-mapmaking/references/blockout-3d-illustrazione.md
```

Punti critici da non sbagliare: `--near`/`--far` (se sbagliati la depth esce
piatta e il ControlNet non vincola niente — deve essere un **gradiente pieno**,
vicino = bianco); `CompositorNodeOutputFile` aggiunge il numero di frame al
nome (`_depth0001.png`), va gestito a valle; ControlNet **Union** consigliato
sulle 8 GB di VRAM (un file solo invece di tre); `end_percent` **0.80**, non
1.0, altrimenti l'immagine esce plasticosa.

Aggiornare `scripts/comfyui-local/README.md` (oggi cita solo lineart/canny) e
`references/tre-modalita-mappe.md` (oggi dichiara 3 modalità).

**Accettazione**: il test di §4 eseguito end-to-end su una scena
(`--focal 24 --near 2 --far 45`), con il criterio dichiarato dalla guida —
**«le masse principali stanno dove le hai messe nel blockout»**, non «l'immagine
è bella»; depth PNG con gradiente pieno verificato a occhio; `rendered/blockout/`
fuori da `validate_maps.py`; script a manifest se committato.
**Engine**: Sonnet (script) — il collaudo è **al DM, sulla sua macchina**.
**Impegno**: medio. **Stima**: 8-10 h + collaudo.
**Gate**: GPU e Blender sulla macchina del DM. ⚠️ I nomi dei modelli ControlNet
cambiano rapidamente: verificare licenza e nome **al momento del download**.

#### ⬜ D4 — Igiene IP dei prompt versionati

*Rimedia*: audit §4.4. I prompt contengono riferimenti in chiaro a IP protette
(«visual style of Doctor Strange», «Lord of the Rings dwarven aesthetics»,
«Thor: Ragnarok»). Coperto da ADR-0005 per uso privato, ma sono file
**versionati e pubblici**, ed è precisamente ciò che va rimosso da qualunque
edizione distribuita.

Sostituire con linguaggio **descrittivo** (ciò che si vuole vedere, non da
quale film), aggiungere la policy in ADR-0005 e una riga di promemoria nella
testata di `00_INDICE-PROMPT-MEDIA-CAMPAGNA.md`. Documentare che ogni immagine
così prodotta va etichettata `Contains AI-Generated Content` sulle piattaforme
di distribuzione.

**Accettazione**: nessun titolo di film/IP protetta resta nei prompt;
il senso visivo dei prompt bonificati è preservato (verifica a occhio del DM).
**Engine**: Sonnet. **Impegno**: basso. **Stima**: 3-4 h.

---

## 4. Sequenza consigliata

L'ordine **non** è quello dei lotti. La guida stessa avverte: *leggere prima di
aver misurato lo scarto significa studiare a caso.* Lo scarto è misurato
(audit); la sequenza segue il ritorno.

| # | Lotto | Perché qui |
|---|---|---|
| 1 | **D2** — ordine percettivo | ~4 h, zero dipendenze, agisce su ciò che il repo produce di più |
| 2 | **A1** — legenda funzionale | collo di bottiglia di tutta la Parte II; **chiude oggi** la divergenza SVG↔UVTT; è il lotto E1 già pianificato → un lavoro, tre piani |
| 3 | **C1** — scheda-mappa | indipendente; serve a C2 e insegna la disciplina prima di avere il tool |
| 4 | **A3 + A2** | il dato che manca alle metriche |
| 5 | **B1 + B4** | il linter utile con il minimo di lavoro |
| 6 | **C2** (Dirupo Mortale) | la prima mappa che il linter ripaga |
| 7 | **D1 + D4** | inquadratura e igiene IP, in parallelo |
| 8 | **B2 → B3 → B5** | le metriche costose e la calibrazione |
| 9 | **D3** | Modalità 4 — gated dalla macchina del DM |
| 10 | **C3** | parity pass, a mappa singola, sulla lunga |

**Totale stimato**: ~100-130 h, di cui **~20 h** (D2 + A1 parziale + C1) danno
la maggior parte del valore percepito.

## 5. Rischi dichiarati

| Rischio | Mitigazione |
|---|---|
| A1 rompe i render legacy | `validate_maps.py` esige byte-identità: il gate è già lì, va solo tenuto verde |
| Le 4 decisioni sui simboli divergenti (`⛰ 🏛 🗼 🗿`) sono di **regole**, non di codice | vanno al DM, non risolte dall'agente; documentate nel changelog |
| Il linter genera rumore e viene ignorato | A3 (`map_kind`) **prima** di B1; advisory sempre; messaggi che dichiarano di essere pre-calibrazione |
| Le soglie restano opinione | B5 con corpus dichiarato e licenze verificate, o le soglie restano marcate «euristiche» per sempre — mai spacciate per misura |
| D3 dipende da hardware e da modelli che cambiano nome | collaudo sulla macchina del DM; nomi ControlNet verificati al download; `rendered/blockout/` fuori dal canone |
| Il piano cresce e non chiude mai | i non-obiettivi di §1 sono vincolanti; C3 è esplicitamente a mappa singola e gated |

## 6. Cosa questo piano NON risolve

Onestà, in coerenza con §L8 della guida:

- **il linter non misura il divertimento**, misura le affordance. Una mappa può
  passare ogni soglia ed essere noiosa;
- **vale per lo spazio di combattimento**, non per esplorazione, investigazione
  o scene sociali;
- **la scala resta il punto debole dei modelli generativi**: anche con la figura
  di scala, sbagliano spesso. Preventivare più iterazioni sulle scene
  monumentali;
- **coerenza fra immagini diverse: bassa.** Lo stesso luogo in due immagini non
  sarà lo stesso luogo;
- **il ControlNet depth vincola le masse, non il dettaglio.**

---

## Checklist di avanzamento

```
Ramo A — fondamenta dati
□ A1  legend.yaml fonte unica (= E1 PIANO-EDITOR) + ADR-0014 accettato
□ A2  zones/elevation/design_intent — schema v1.1
□ A3  map_kind discriminante

Ramo B — linter
□ B1  lint_map_design.py — M1 M2 M7 M8 M9 + dmcore/mapmodel.py
□ B2  M3 anelli (grafo zone) · M4/M5 visibilità (dmcore/los.py) · M6
□ B3  design_intent — dichiarato vs realizzato
□ B4  manifest + docs/tools + CI non bloccante + skill reference
□ B5  calibrazione su corpus dichiarato (mai RHoD)

Ramo C — contenuto mappe
□ C1  scheda-mappa-template.md
□ C2  riprogettazione Dirupo Mortale · Ondata 2 · (Ground Battle → map_kind?)
□ C3  parity pass — a mappa singola, gated dal tavolo

Ramo D — inquadratura e prosa
□ D2  ⭐ ordine percettivo nel read-aloud (narrative-style)
□ D1  scheda-inquadratura + campo ## Inquadratura (pilota: 3 scene ARC-07)
□ D4  igiene IP dei prompt versionati
□ D3  Modalità 4 — blockout 3D → depth → ControlNet (gated: GPU DM)
```

> **Regola d'oro dei piani**: chi chiude un lotto aggiorna — nello stesso
> commit — questa checklist, la riga in `plans/INDEX.md` e una riga in
> `plans/CHANGELOG.md`.
