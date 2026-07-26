# AUDIT — Level design delle mappe e inquadratura delle immagini

> **Cos'è**: la misura dello scarto fra ciò che il toolkit DM (`scripts/`,
> `skills/`, `campaign/`) sa fare oggi e ciò che serve per raggiungere il
> livello di *level design* e di *prospettiva grafica* descritto nella guida
> operativa **«Dall'immagine mentale all'artefatto»** (2026-07-25).
>
> **Metodo**: non opinioni. Ogni riga di questo audit è o un fatto verificabile
> sul repo (grep/import) o una misura riproducibile (appendice A).
>
> **Non è un piano**: il piano di rimedio è
> [`plans/PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md`](../../plans/PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md).
>
> **Data**: 2026-07-26 · **Corpus**: `main` @ branch di analisi.

---

## 0. Riassunto in una pagina

| Dominio | Stato | Evidenza |
|---|---|---|
| Pipeline mappe (rendering, contratto, export) | 🟢 **matura** | 3 modalità implementate, 40 tool a manifest, CI con gate deterministici |
| **Semantica di gioco dei simboli** | 🔴 **assente come dato** | la funzione (copertura, blocco vista, quota) sta in prosa nella legenda e in `set` cablati in due script → **già divergenti** (§2.1) |
| **Metriche di level design** | 🔴 **inesistenti** | nessun tool le calcola; misurate a mano qui: mediane fuori soglia su M1/M2/M4/M8/M9 (§3) |
| **Elevazione / verticalità** | 🔴 **non rappresentabile** | 0 occorrenze di `elevation` in `scripts/`, negli schemi e nella legenda |
| **Grafo delle zone (anelli)** | 🔴 **non rappresentabile** | `@zone` è un bracket di presentazione derivato da `structures[].label`, non un distretto |
| **Intento di design dichiarato** | 🔴 **assente** | nessun `design_intent` nello schema; la scheda-mappa non esiste |
| Prompt immagine (Modalità 2) | 🟡 **ricchi ma non inquadrati** | 48 blocchi prompt: **0** dichiarano focale, altezza camera, figura di scala o prospettiva atmosferica (§4.1) |
| **Modalità 4 (blockout 3D → depth)** | 🔴 **assente** | nessun `scripts/blockout/`, nessun ControlNet depth, nessuna scheda-inquadratura |
| Regola di **ordine percettivo** nella prosa | 🔴 **assente** | `editorial-standards.md` normA texture e tipografia, non l'ordine di rivelazione (§4.3) |
| Igiene IP nei prompt | 🟡 **debito noto** | riferimenti in chiaro a IP protette nei prompt versionati (§4.4) |

**La diagnosi in una riga**: il repo ha una pipeline di **produzione** eccellente
e nessuna pipeline di **progettazione**. Sa disegnare qualunque cosa gli si dica,
in modo deterministico e verificato in CI; non ha alcun modo di dire se ciò che
gli si è detto di disegnare fosse una buona mappa o una buona inquadratura.

---

## 1. Cosa c'è già, e va riconosciuto

Prima dei buchi, il consuntivo — perché determina la strategia di rimedio
(estendere, non riscrivere):

- **40 tool a contratto machine-readable** (`scripts/tools.manifest.json`),
  con gate bloccante in CI (`tools_manifest --check`, ADR-0012).
- **Renderer deterministico** (`render_map_svg.py`, 1.530 righe): pattern
  procedurali, prop vettoriali in-house, occlusione ambientale, bussola,
  overlay professionale (ADR-0006). Nessun asset di terzi.
- **Contratto JSON rigido** + validatore (`compile_map_json.py`, schema
  `tactical_map.schema.json`) e **round-trip inverso** (`import_ultraclear.py`,
  registro conflitti R1-R10).
- **Export UVTT/dd2vtt** con muri, porte e luci → Foundry/Roll20.
- **Fonte unica parziale**: `compile_map_json.py` e `import_ultraclear.py`
  importano già `SYMBOLS` da `render_map_svg.py` invece di duplicarla.
- 70+ test, CI con 12 gate, disciplina piani/ADR enforced (ADR-0009).

Questa maturità è esattamente la ragione per cui le metriche di §L5 della
guida sono **fattibili qui e quasi da nessun'altra parte**: parser, legenda,
estrazione muri, schema e CI esistono già.

---

## 2. Parte II — Level design: i buchi architetturali

### 2.1 Due fonti di verità sui simboli — e sono già divergenti

`SYMBOLS` in `scripts/render_map_svg.py:78` descrive **come si disegna** un
simbolo (`mode`, `pat`, `fill`) e ne dà un'etichetta italiana. La **funzione di
gioco** non è un campo: vive in due posti sbagliati.

**(a) In prosa, dentro l'etichetta**:

```python
"🪨": {..., "it": "Rocce/macerie (copertura +4 CA, terreno difficile)"},
"🌾": {..., "it": "Erba alta / cespugli (occultamento)"},
"🧱": {..., "it": "Muretto / copertura bassa (+4 CA)"},
```

Una stringa non è interrogabile: nessuno script può chiedere «questa cella dà
copertura?».

**(b) Cablata in `set` dentro gli script che la consumano**:

```python
# scripts/export_uvtt.py:50
WALL_SYMS  = {"🏰", "⬛", "🟪", "🗼", "🏛", "🗿"}
DOOR_SYMS  = {"🚪"}
LIGHT_SYMS = {...}
# scripts/import_ultraclear.py:72
HAZARD_SYMS = {"🔥", "💥", "💀", "🕳", "⚡", "❄", "🕸"}
```

**Le due fonti hanno già divergato, in entrambe le direzioni.** Verificabile:

```
renderer, solidi (HEAVY_PATS) : ⛰ ⬛ 🏰 🟪
export_uvtt, WALL_SYMS       : ⬛ 🏛 🏰 🗼 🗿 🟪
solido nel render ma NON muro UVTT : ⛰   (montagne / creste rocciose)
muro UVTT ma NON solido nel render : 🏛 🗼 🗿  (tutti in modo "icon")
```

Conseguenza concreta e giocabile: la parete rocciosa che occupa le colonne
01-10 della mappa *Dirupo Mortale* (ARC-08) **proietta ombra e occlude nell'SVG,
ma non blocca la linea di vista in Foundry**. L'SVG stampato e la scena VTT
della stessa mappa raccontano due regole diverse. Non è un difetto estetico:
è la mappa che al tavolo dice una cosa e al VTT un'altra.

È il tipo di debito che il repo non tollera altrove — ed è anche il blocco
architetturale che rende **impossibile** implementare le metriche di §L5 in
modo pulito: un linter di dominio dovrebbe importare `WALL_SYMS` **da un
exporter**. Un exporter non possiede il modello di dominio.

### 2.2 L'elevazione non esiste come dato

```
grep -rn "elevation|elevazione|quota" scripts/ scripts/schemas/ \
    skills/rumblingstone-mapmaking/references/   →  0 risultati
```

La verticalità esiste **solo come testo di callout**: nella mappa *Torrione di
Vedetta* la quota della torre è scritta come annotazione `DARA TOP (+18m)!` a
lato della griglia. È leggibile da un umano, invisibile a qualunque script —
e infatti **M6 (verticalità) non è calcolabile oggi**, come la guida stessa
anticipa (§L8).

Questo blocca anche l'export: UVTT non riceve alcuna informazione di quota, e
il renderer non può differenziare visivamente le bande di elevazione.

### 2.3 Il grafo delle zone non esiste (→ niente anelli)

Lo schema del contratto ha, ai livelli alti:

```
schema_version · units_in · title · scale_m_per_square · map_size ·
base_terrain · north · movements · regions · structures · hazards ·
lights · units · notes
```

Non c'è `zones`. La direttiva `@zone` che la CI verifica viene emessa da
`compile_map_json.py:538-542` a partire da `structures[]`/`hazards[]` che
hanno `rect` **e** `label`: è una **parentesi grafica di presentazione**, non
un distretto nel senso di Lynch. Non ha adiacenze, quindi non c'è un grafo,
quindi **M3 (anelli, μ = E − V + 1) non ha un supporto dati** — e calcolarlo
sulle celle, come avverte §L5.3, produrrebbe un numero privo di significato.

### 2.4 Nessun intento dichiarato

Non esiste `design_intent` nello schema, né una scheda-mappa. Il template
`campaign/templates/mappa-tattica-template.md` è ottimo per la **resa** (i tre
blocchi Ambiente / Tattiche / Evoluzione) e non chiede mai:

- qual è la domanda che i giocatori devono porsi;
- come si vince, se non uccidendo tutti;
- quali assi tattici la mappa deve esprimere.

Senza intento dichiarato, il salto di §L5.6 (verificare *dichiarato contro
realizzato*) è impossibile — ed è la parte che nessun altro strumento fa.

### 2.5 Collisione di nomi già in essere

`scripts/dmcore/visibility.py` esiste, ma è la **policy di visibilità spoiler
dei session log** (blocchi `## Split`, `## DM notes`). Il nome ovvio per la
linea di vista tattica è già occupato: la line-of-sight va in un modulo
distinto (`dmcore/los.py`), altrimenti si crea confusione permanente in un
package condiviso.

---

## 3. Parte II — Level design: la misura del contenuto

Metriche M1, M2, M4, M7, M8, M9 di §L5.2 calcolate sulle **29 griglie ≥12×12**
estratte dai master del repo (metodo e sorgente in **appendice A**).

### 3.1 Distribuzioni

| Metrica | Mediana | Media | Min | Max | Soglia guida | Fuori soglia |
|---|---|---|---|---|---|---|
| **M1** copertura raggiungibile | **0.30** | 0.37 | 0.00 | 1.00 | ≥ 0.60 | **22 / 29** |
| **M2** vuoto massimo | **0.51** | 0.56 | 0.00 | 1.00 | ≤ 0.20 | **24 / 29** |
| **M4** esposizione media | **0.84** | 0.69 | 0.13 | 1.00 | ≤ 0.45 | **22 / 29** |
| **M7** simmetria | **0.87** | 0.82 | 0.38 | 0.99 | ≤ 0.85 | ~14 / 29 |
| **M8** landmark nominabili | **0** | 0.7 | 0 | 3 | ≥ 3 (≥20×20) | **21** |
| **M9** distanza d'ingaggio | — | — | 0.2 | 7.7 | 2-4 round | **15 / 15** * |

\* solo 15 griglie su 29 portano contemporaneamente token PG e nemico; di
quelle, **nessuna** cade nella banda 2-4 round.

### 3.2 Le cinque mappe peggiori

| M1 | M2 | M4 | M8 | M9 | Dim. | Mappa |
|---|---|---|---|---|---|---|
| 0.00 | 1.00 | 1.00 | 1 | 0.5 | 26×26 | Ondata 2 Positions (Round 22 Fase 2) |
| 0.02 | 0.98 | 0.94 | 1 | 6.0 | 30×71 | Ground Battle (120 m × 200 m) |
| **0.03** | **0.97** | **0.88** | **0** | **1.5** | 40×40 | **Dirupo Mortale / Campo Hobgoblin** |
| 0.04 | 0.96 | 0.98 | 0 | — | 28×30 | (griglia senza banner, ARC-09) |
| 0.08 | 0.92 | 0.87 | 0 | — | 24×16 | Camera Centrale — sfera Ø 60 m |

**La diagnosi del §7 della guida su *Dirupo Mortale* è confermata dai numeri,
e sottostimata.** La guida stimava M1 ≈ 0.25 e M2 ≈ 0.55; la misura dà
**M1 = 0.03** e **M2 = 0.97**. Il 97% dello spazio percorribile è una singola
componente connessa priva di copertura entro mezzo movimento. Su 1.600
quadretti, circa 1.360 sono `🟩` pianura aperta identica. Chi la attraversa
non prende decisioni: tira dadi.

### 3.3 Le mappe che invece funzionano — e perché conta

| M1 | M2 | M4 | M8 | Mappa |
|---|---|---|---|---|
| 1.00 | 0.00 | 0.13 | 3 | Il Cuore della Montagna — caverna sacra |
| 0.92 | 0.08 | 0.46 | 0 | Griglia 33×33 (Caverna Intersection) |
| 0.88 | 0.08 | 0.67 | 1 | MAPPA PF-1: Stanza della Corona |
| 0.75 | 0.09 | 0.84 | 0 | Corridoio del Fuoco (21×53) |

Il pattern è netto e vale come **prova che le soglie non sono arbitrarie per
questo repo**: gli **interni** (caverne, sale, corridoi) passano; gli **esterni
e i campi di battaglia** falliscono tutti. La ragione è strutturale, non
autoriale — in una caverna la copertura è un sottoprodotto gratuito della
roccia; in campo aperto va **progettata**, e senza uno strumento che la misuri
nessuno si accorge che manca.

### 3.4 Un limite del corpus che è a sua volta un buco

8 delle 29 griglie **non sono battlemap**: sono viste strategiche o schematiche
(assedio 120×80, *Ground Battle* 30×71, sezioni della sfera, panoramiche della
fortezza). Applicare loro M1/M4 è privo di senso, ma **nulla nel formato lo
dichiara**: non esiste un campo `map_kind`. Un linter costruito oggi
produrrebbe rumore su un terzo del corpus, e il rumore è ciò che fa spegnere
i linter. Il discriminante va aggiunto **prima** dello strumento.

### 3.5 Onestà sui numeri

Vanno letti come **ordine di grandezza, non come verdetti**:

- il set di simboli che «danno copertura» è stato **inventato per questo
  audit** (`🧱🪨📦🌳🗿🌾🛢🪑⛺🏺🕸🍄`) — precisamente perché il dato non
  esiste (§2.1). Con una legenda funzionale i valori cambieranno;
- M4 è campionata (≤120 celle per mappa) — è una stima, non un censimento;
- M8 è un proxy (simboli in modo `icon` presenti in ≤3 celle), non «il
  giocatore può nominarlo»;
- le soglie della guida sono **euristiche dichiarate**, non calibrate
  (§L5.4). Restano da calibrare su un corpus liberamente licenziato — **mai**
  sulle mappe RHoD (ADR-0005).

Ciò che i numeri stabiliscono con certezza è la **forma** del problema:
distribuzioni concentrate agli estremi sbagliati, non a cavallo della soglia.
Una mappa a M2 = 0.97 non diventa conforme spostando una soglia.

---

## 4. Parte I — Inquadratura e prospettiva

### 4.1 I prompt esistenti non inquadrano

`campaign/ai-media-prompts/` — 12 file, **48 blocchi prompt** (video intro +
immagini di sessione). Conteggio sul vocabolario di §1 della guida:

| Leva (§1) | Blocchi che la dichiarano |
|---|---|
| **Focale** (mm, wide/tele) | **0 / 48** |
| **Altezza e angolo camera** | **0 / 48** ¹ |
| **Figura di scala** | **0 / 48** ² |
| **Prospettiva atmosferica** | **0 / 48** |
| **Primo piano** esplicito | 6 occorrenze in tutto il corpus |
| Struttura dei valori (nero/contrasto max) | 6 occorrenze in tutto il corpus |

¹ Il tag `[CAMERA]` esiste, ma solo nei **video intro** (1 per file) e descrive
il movimento («medium shot, slow push-in»), mai l'altezza né l'inclinazione.
² Le 3 occorrenze in `11_PG_E_VILLAIN_PROMPTS.md` sono ritratti, non scale
ambientali.

I prompt non sono poveri — sono **lunghi e ricchi di sostantivi**. È esattamente
il difetto che la guida descrive: si elencano oggetti, e il generatore
restituisce la sua media statistica di quegli oggetti. La struttura in uso
(`[STILE] [SCENA] [CAMERA] [PALETTE] [DURATA]`) ordina per **categoria di
metadato**; quella proposta (`soggetto e momento · inquadratura · luce e valore
· atmosfera · medium`) ordina per **come si costruisce un'immagine**. E manca
del tutto il campo più importante: **il momento** — non «la sala», ma l'attimo.

### 4.2 La Modalità 4 non esiste

| Modalità | Stato nel repo |
|---|---|
| 1 · griglia emoji → SVG pergamena | ✅ `render_map_svg.py` |
| 2 · SVG → repaint pittorico | ✅ `hero-map-comfyui.md` |
| 3 · JSON contratto → mappa | ✅ `compile_map_json.py` |
| **4 · blockout 3D → depth → illustrazione** | ❌ **assente** |

Verifiche: nessun `scripts/blockout/`; `scripts/comfyui-local/README.md` cita
solo ControlNet **lineart/canny**, mai depth; `grep -ri "blockout|inquadratura|
focale"` su `campaign/ skills/ scripts/ docs/ plans/` non restituisce nulla di
pertinente. La skill mapmaking documenta 3 modalità in
`references/tre-modalita-mappe.md`.

È l'unico anello della catena che parte da **niente** — dall'immagine mentale —
e costruisce il vincolo geometrico prima di generare. È anche l'unico pezzo con
provenienza al 100% pulita (il blockout è originale), il che ha valore diretto
sotto ADR-0005.

### 4.3 La prosa: il buco a ritorno più alto

`skills/rumblingstone-narrative-style/references/editorial-standards.md` §2
norma il read-aloud su: blockquote in corsivo, 3-10 righe, un dettaglio
sensoriale concreto per paragrafo, chiusura sul decision point, tipografia dei
numeri, etichetta di regia. Tutto giusto — e tutto sulla **texture**.

**Non c'è alcuna regola sull'ordine di rivelazione.** Mancano le tre che il §6
della guida isola:

1. descrivere nell'ordine in cui la percezione arriva
   (non-visivo → primo piano → piano medio → sfondo);
2. dare la scala per **rapporto** prima che per numero
   («le spalle a metà della volta», *poi* «e la volta è a diciotto metri»);
3. inquadrare **un momento**, non un luogo.

Questo è il punto di maggior ritorno dell'intero audit: non richiede GPU, non
richiede Blender, non richiede codice. È una regola in una skill già montata e
già obbligatoria per ogni generazione di contenuto, e agisce su ciò che il
repo produce di più — la prosa dei master DEF.

### 4.4 Igiene IP nei prompt versionati

I prompt contengono riferimenti in chiaro a IP protette, es. in
`08_ARC07_portale-forgia-eterna.md`:

```
[STILE] … visual style of Doctor Strange (portal magic) mixed with
        Lord of the Rings dwarven aesthetics.
[MUSICA] Riferimento: "Thor: Ragnarok" o "Doctor Strange" portal themes
```

Per uso privato è coperto da ADR-0005. Ma sono file **versionati e pubblici**
nel repo, e sono precisamente ciò che §9 della guida indica di rimuovere da
qualunque edizione distribuita. Oggi non esiste una policy scritta né un
promemoria: è un debito silenzioso, a costo di rimedio crescente col numero
di prompt.

---

## 5. Il grafo delle dipendenze del rimedio

```
              ┌──────────────────────────────────┐
              │ A1 legenda funzionale (legend.yaml) │ ← ADR-0014
              │    = lotto E1 del PIANO-EDITOR      │
              └───────────────┬──────────────────┘
                    ┌─────────┴─────────┐
        ┌───────────▼──────┐   ┌────────▼─────────────┐
        │ A2 zones+elevation│   │ A3 map_kind          │
        │    +design_intent │   │    (discriminante)   │
        └───────────┬───────┘   └────────┬─────────────┘
                    └─────────┬──────────┘
                    ┌─────────▼──────────┐
                    │ B1 lint_map_design │  M1 M2 M7 M8 M9
                    └─────────┬──────────┘
              ┌───────────────┼───────────────┐
      ┌───────▼──────┐ ┌──────▼──────┐ ┌──────▼───────┐
      │ B2 M3/M4/M6  │ │ B3 intento  │ │ B4 CI+skill  │
      └──────────────┘ └─────────────┘ └──────┬───────┘
                                       ┌──────▼───────┐
                                       │ B5 calibraz. │
                                       └──────────────┘

  C1 scheda-mappa ──► C2 riprogettazione mappe ──► C3 parity pass
  (indipendente)      (richiede C1 + B1)           (gated dal tavolo)

  D1 scheda-inquadratura   D2 regola percettiva (prosa)   ← indipendenti
  D3 Modalità 4 blockout   D4 igiene IP                     da A/B/C
```

**A1 è il collo di bottiglia di tutta la Parte II** e ha valore autonomo anche
se il resto venisse abbandonato: chiude la divergenza SVG↔UVTT di §2.1 oggi.
Non è lavoro nuovo — **è il lotto E1 già pianificato** in
`PIANO-EDITOR-VISUALE-MAPPE-TATTICHE` (`export_legend_json.py` + gate CI di
sincronizzazione). Farlo una volta serve tre piani.

**Il ramo D non dipende da nulla** e contiene l'item a ritorno più alto (D2).
Va avviato in parallelo, non in coda.

---

## Appendice A — Riproducibilità delle misure

Le misure di §3 provengono da un harness *usa-e-getta* eseguito il 2026-07-26
sul branch di analisi. Definizioni operative usate:

| Termine | Definizione nell'harness |
|---|---|
| celle | tutte le celle non vuote delle griglie estratte da `render_map_svg.extract_maps()` |
| percorribile | cella non in `WALL_SYMS ∪ {🌲}` |
| copertura | cella in `WALL_SYMS` **oppure** in `{🧱 🪨 📦 🌳 🗿 🌾 🛢 🪑 ⛺ 🏺 🕸 🍄}` (insieme **inventato per l'audit** — vedi §3.5) |
| M1 | frazione di celle percorribili con copertura entro Chebyshev 2 |
| M2 | più grande componente 4-connessa di celle percorribili **senza** copertura entro 2, su percorribili |
| M4 | media, su ≤120 celle campionate (1 ogni 7 in ordine lessicografico), della frazione del campione mutuamente visibile via Bresenham fermato dai bloccanti vista |
| M7 | max(simmetria orizzontale, verticale) come frazione di celle coincidenti col mirror |
| M8 | simboli in modo `icon` presenti in ≤3 celle |
| M9 | min distanza Chebyshev fra un `🔵` e un token in `{🔴 ⚫ 🟡 🟣}`, diviso 6 quadretti/round |
| filtro | solo griglie ≥12×12; esclusi `build/ .git/ plans/ docs/ skills/` |

L'harness **non è stato committato di proposito**: la sua funzione — misurare
in modo dichiarato e ripetibile — è il deliverable del **lotto B1**
(`scripts/lint_map_design.py`), che nascerà conforme ad ADR-0012 (manifest,
exit code, determinismo, test, CI non bloccante) invece che come script
volante. Le definizioni qui sopra sono la sua specifica di comportamento
iniziale e il suo primo caso di regressione: rieseguito su questo corpus, B1
deve riprodurre le mediane di §3.1 entro tolleranza, **salvo** le differenze
imputabili alla legenda funzionale di A1 — differenze che vanno documentate,
non nascoste.
