# PIANO — DA REPO DI CAMPAGNA A PRODOTTO VENDIBILE

> **Cos'è**: il piano completo per trasformare il toolkit (`scripts/`, renderer,
> legenda, schemi) in un **prodotto professionale, riusabile e vendibile**,
> multi-sistema (D&D 3.5 · Pathfinder 1e · D&D 5e), senza toccare la campagna.
>
> **Decisioni DM del 2026-07-26** che questo piano attua:
> rilicenziare il toolkit · supportare **tre** sistemi di regole · distribuire
> come **wheel + eseguibile autonomo** · vendere **toolkit + map pack neutri +
> il metodo**.
>
> **ADR**: [0014](adr/ADR-0014-legenda-funzionale-fonte-unica.md) legenda fonte
> unica · [0015](adr/ADR-0015-dipendenze-a-livelli-e-pacchettizzazione.md)
> dipendenze e confezionamento · [0016](adr/ADR-0016-profili-regole-multisistema.md)
> profili multi-sistema · [0017](adr/ADR-0017-separazione-prodotto-e-rilicenziamento-toolkit.md)
> separazione e rilicenziamento.
> **Specifica normativa**: [`docs/guides/LEGENDA-FUNZIONALE-SPEC.md`](../docs/guides/LEGENDA-FUNZIONALE-SPEC.md).
> **Misura di partenza**: [`docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md`](../docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md).
>
> **Piano gemello**: [`PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA`](PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md)
> — quello è il *contenuto* (metriche, mappe, inquadratura), questo è il
> *prodotto*. Condividono i lotti fondativi: si eseguono **una volta sola**.
>
> **Stato**: 🔵 pianificato · **Data**: 2026-07-26 · **%**: 0%

---

## 1. Cosa si vende, e cosa no

| | Vendibile | Perché |
|---|---|---|
| ✅ **Il toolkit** | sì | codice originale, arte procedurale in-house, **nessun asset di terzi** |
| ✅ **Map pack neutri** | sì | mappe originali world-neutral prodotte col toolkit |
| ✅ **Il metodo** | sì | schede-mappa, 9 metriche, corpus di calibrazione: nessun concorrente ce l'ha |
| ❌ **La campagna** | **no** | RHoD + Forgotten Realms: blocco WotC assorbente (ADR-0005, invariato) |

**La regola operativa che ne discende, e che vale per ogni lotto**: nessun nome,
luogo, PNG o statblocco della campagna entra mai nel package del toolkit. Il
confine si verifica in CI (§P8.3), non a memoria.

**Il titolo che vende** resta *«scrivi la mappa come testo, ottieni una scena
Foundry con muri e luci»* — risolve un problema che le persone hanno già. Il
linter di level design è la funzione che, una volta dentro, fa dire *«questa cosa
l'ha scritta qualcuno che sa cosa fa»*: è ciò che trasforma un tool utile in un
tool di cui si parla, **ma non è ciò che porta il primo utente.** Non va messo in
copertina.

---

## 2. Il punto di partenza, misurato

Non un'impressione — i numeri dell'audit §6:

| Fatto | Valore | Conseguenza |
|---|---|---|
| Script con `sys.path.insert` | **11** | nulla è installabile o importabile |
| `render_map_svg.py` | **1.530 righe** (legenda + pattern + arte + parser + annotazioni + renderer + CLI) | 4 moduli lo importano *per il parser e la legenda*: il dominio dipende dalla presentazione |
| Validatori JSON Schema a mano | **2** | gli schemi draft-07 sono completi, i validatori no |
| Configurazione lint/format/tipi | **0** | i `# noqa: E402` in 8 file sono il fossile di un flake8 perso |
| Celle `⛰` senza muro nell'export UVTT | **3.689** in 6 mappe | il *Dirupo Mortale* è trasparente in Foundry |
| Copertura dei test | **non misurata** | 70 test verdi, ambito ignoto |

**Coerenza architetturale**: alta e non comune (13 ADR con gate CI, contratto
tool machine-readable bloccante, determinismo verificato per byte-identità,
scritture canone a triplo vincolo). **Il problema non è il progetto: è
l'imballaggio.**

---

## 3. Architettura bersaglio

```
  ┌──────────────────────────────────────────────────────────┐
  │  DOMINIO  (neutro, zero numeri di gioco, zero campagna)  │
  │  legend.yaml · parser griglia · modello mappa · metriche │
  └───────────────┬──────────────────────────────────────────┘
        ┌─────────┼─────────┬──────────────┬─────────────────┐
   ┌────▼────┐ ┌──▼─────┐ ┌─▼──────────┐ ┌─▼────────────┐
   │ render  │ │ export │ │  import    │ │ lint_design  │
   │  SVG    │ │ UVTT…  │ │ watabou…   │ │  (M1-M9)     │
   └─────────┘ └────────┘ └────────────┘ └──────────────┘
        └─────────┴─────────┴──────────────┴──────► CLI · wheel · exe

  ┌──────────────────────────────────────────────────────────┐
  │  PROFILI DI REGOLE (sostituibili, licenze separate)      │
  │  rules/dnd35.yaml   rules/pf1e.yaml  │  rules/dnd5e.yaml │
  │  ──── OGL 1.0a ─────────────────────  ── CC BY 4.0 ───── │
  └──────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────┐
  │  CAMPAGNA RumblingStone — CONSUMATORE, mai dipendenza    │
  │  resta GPL-3 / privata · ADR-0005 invariato              │
  └──────────────────────────────────────────────────────────┘
```

Tre invarianti verificabili in CI:

1. il **dominio non importa** render, export, CLI né profili;
2. il **package non contiene** stringhe della campagna;
3. `legend.yaml` non contiene **nessun numero di gioco**.

---

## 4. I lotti

Impegno secondo la regola DM 2026-07-22 (engine + livello per fase).

### Fase P0 — Substrato (sblocca tutto il resto)

#### ⬜ P0.1 — `pyproject.toml` e fine dei `sys.path.insert`

Package importabile con entrypoint da console; gli 11 `sys.path.insert`
spariscono. **Il layout attuale resta invocabile identico**: `python3
scripts/dm.py …` continua a funzionare — nessuna rottura per il DM.

- **Accettazione**: `pip install -e .` funziona; i 70 test passano sia dal
  package sia dal layout attuale; SVG **byte-identici**; `tools_manifest --check`
  verde.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: ADR-0015.

#### ⬜ P0.2 — Livelli di dipendenza + `jsonschema` sui gate

Livello 0 core **stdlib puro e offline** · livello 1 `analysis`
(numpy/scipy/networkx/tcod) **opzionale** · livello 2 dev. `jsonschema` valida in
CI gli schemi draft-07 già nel repo; i validatori a mano si riducono ai soli
**controlli semantici** che JSON Schema non può esprimere.

- **Accettazione**: gli esempi validano contro `tactical_map.schema.json` **senza
  modificarlo** (eccetto il caso documentato `units_in: meters`); un test per
  ogni errore che il validatore a mano sapeva già dare — **zero comportamenti
  persi**; il core resta eseguibile senza rete e senza `pip`.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 5-7 h · **Dip.**: P0.1.

#### ⬜ P0.3 — `ruff` + `pytest` + copertura

Un solo tool per lint e formato; `pytest` come runner (esegue i 70 `unittest`
esistenti **senza riscriverli**); baseline di copertura registrata. Non bloccante
al primo giro, bloccante dopo la bonifica.

- **Accettazione**: `ruff check` pulito; `pytest` verde sui test **non
  riscritti**; baseline pubblicata.
- **Engine**: Haiku, con Sonnet sulle correzioni non banali · **Impegno**: basso
  · **Stima**: 4-6 h · **Dip.**: P0.1.

#### ⬜ P0.4 — Cucitura dominio / presentazione

Legenda, parser della griglia e modello della mappa escono da `render_map_svg.py`
e diventano il **dominio**. Renderer, exporter, importer e linter ne dipendono; il
dominio non dipende da nessuno.

- **Accettazione**: `render_map_svg` non è più importato da nessuno per ottenere
  parser o legenda; **grafo delle dipendenze aciclico** con la presentazione
  sulle foglie, verificato da un test; SVG byte-identici; round-trip UVTT verde.
- **Engine**: Opus (confini) → Sonnet (spostamento) · **Impegno**: alto ·
  **Stima**: 10-14 h · **Dip.**: P0.1, P1.1.

---

### Fase P1 — La legenda funzionale e i tre sistemi

#### ⬜ P1.1 — `legend.yaml`: fonte unica, funzione neutra

Attua [`LEGENDA-FUNZIONALE-SPEC.md`](../docs/guides/LEGENDA-FUNZIONALE-SPEC.md)
§2 e §4 su tutti e **62** i simboli. `render_map_svg.SYMBOLS` diventa derivato;
`export_uvtt` deriva muri/porte/luci da `function` ed **elimina** `WALL_SYMS`,
`DOOR_SYMS`, `LIGHT_SYMS`; `import_ultraclear.HAZARD_SYMS` idem;
`legenda-universale.md` si **genera** dal YAML.

Chiude la divergenza delle quattro classificazioni (spec §6): `⛰ 🏛 🗼 🗿` sono
tutte **copertura totale**, impenetrabili e opache.

- **Accettazione**: nessun set di simboli cablato resta in `scripts/`; **i 17 SVG
  legacy restano byte-identici** (modo di rendering e funzione sono ortogonali:
  una statua continua a disegnarsi come prop *e* a dichiararsi opaca); l'export
  UVTT delle **6 mappe con `⛰` cambia**, guadagnando **3.689 celle** di muro — è
  il bug, e il diff va verificato a mano una volta; `legend.yaml` **non contiene
  nessun numero di gioco** (test automatico); gate di sync YAML ↔
  `legenda-universale.md`.
- **Engine**: Opus (modello) → Sonnet (migrazione) · **Impegno**: alto ·
  **Stima**: 12-16 h · **Dip.**: P0.1. · **= lotto E1 di `PIANO-EDITOR`: un
  lavoro, tre piani.**

#### ⬜ P1.2 — I tre profili di regole

`rules/dnd35.yaml`, `rules/pf1e.yaml`, `rules/dnd5e.yaml` secondo spec §3 e
ADR-0016. Selettore `--rules`, default per campagna. Regola di **saturazione**:
un valore non esprimibile si riduce al più vicino **e si dichiara nel report**
(caso canonico: `move_cost: 4` non esiste in 5e).

- **Accettazione**: i tre profili passano una suite propria che verifica ogni
  traduzione contro la sua fonte; ⚠️ **`move_cost: 4` per PF1e va confermato sul
  PRD** — è l'unico valore della spec non verificato sul testo; ogni profilo
  dichiara in testa licenza, fonte e revisione; il motore non contiene il nome di
  nessun sistema.
- **Engine**: Opus (traduzioni) → Sonnet (file e test) · **Impegno**: alto ·
  **Stima**: 14-18 h · **Dip.**: P1.1.

#### ⬜ P1.3 — Zone, elevazione, `design_intent`, `map_kind` — schema v1.1

`zones[]` con `name`/`elevation_m`/`connects_to[]` (il grafo su cui si calcola
M3, distinto dal `@zone` attuale che resta un bracket di presentazione);
`design_intent{}`; `map_kind: battle|strategic|schematic|overland` — senza il
quale il linter produrrebbe rumore su **8 griglie su 29**.

- **Accettazione**: lo schema v1.1 valida **invariati** i contratti esistenti; un
  esempio nuovo con 3 bande di elevazione e `design_intent` compila, rende e passa
  `validate_maps`; le 8 griglie non-tattiche del corpus marcate e **saltate** dal
  linter con una riga informativa, non un warning.
- **Engine**: Opus (schema) → Sonnet · **Impegno**: alto · **Stima**: 12-16 h ·
  **Dip.**: P1.1.

---

### Fase P2 — Il linter (integrato, non riscritto)

#### ⬜ P2.1 — `lint_map_design`: M1, M2, M7, M8, M9

**M1 = `scipy.ndimage.binary_dilation` (5×5), M2 = `ndimage.label` +
`bincount`** — 4 righe, non 18. Nessun BFS a mano.

- **Accettazione**: ADR-0012 pieno; riproduce i valori dell'appendice A
  dell'audit (M1 0.0309 · M2 0.9691 su *Dirupo Mortale*), **già confermati in
  laboratorio**; fixture sintetiche (corridoio, campo aperto, arena ad anello);
  senza le librerie del livello 1 → exit code documentato, **mai** un crash.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: P0.2,
  P1.1, P1.3.

#### ⬜ P2.2 — M3 anelli e strozzature, M4/M5 visibilità, M6 verticalità

`networkx` per μ = E−V+C e `articulation_points` (1 riga ciascuna); **`tcod`
`compute_fov`** (shadowcasting simmetrico) per la visibilità. ⚠️ **Il
campionamento è cancellato**: censimento completo di 1.585 celle su 40×40
misurato in **34 ms**. M4 diventa **esatta**, quindi deterministica per
costruzione — e la stima campionata **sottostimava** (0.88 contro 0.913).

- **Accettazione**: linter completo su 40×40 in **< 1 s**; M3 = 2 sulla fixture
  ad anello, 0 sul corridoio; nessun seme di campionamento da fissare.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: P1.3,
  P2.1.

#### ⬜ P2.3 — Dichiarato contro realizzato

Il linter confronta `design_intent` con le metriche: *«`tactical_axes` include
verticality ma M6 = 1»*, *«landmark dichiarato su cella `nameable: false`»*,
*«`combat_role: ambush` ma M4 = 0.91»*. **Nessuna soglia arbitraria: il metro è
la dichiarazione dell'autore.** È la funzione che nessun altro strumento ha.

- **Accettazione**: i 3 casi riprodotti da fixture; una mappa senza
  `design_intent` non produce warning di questa classe.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 8-10 h · **Dip.**: P1.3,
  P2.2.

#### ⬜ P2.4 — Calibrazione delle soglie

10-15 mappe **che si sa funzionare al tavolo**, di proprietà o liberamente
licenziate → trascritte → misurate → soglie ai **percentili della distribuzione
reale**. ⚠️ **Mai mappe RHoD** (ADR-0005), e per un prodotto venduto il vincolo è
più stretto: solo materiale di cui si possa **documentare** la licenza.

- **Accettazione**: ogni soglia ha accanto percentile e dimensione del corpus;
  corpus e licenze documentati; le soglie pre-calibrazione **sostituite**, non
  affiancate. Finché non è fatto, il tool **dichiara** che le soglie sono
  euristiche.
- **Engine**: Sonnet (trascrizione) + Opus (percentili) · **Impegno**: medio ·
  **Stima**: 12-16 h · **Dip.**: P2.2 · **Gate**: corpus scelto dal DM.

---

### Fase P3 — Confezionamento e distribuzione

#### ⬜ P3.1 — Wheel

Build riproducibile, versionamento semantico, `python -m build`, pubblicazione
su indice.

- **Accettazione**: `pip install <pkg>` su una macchina pulita → la CLI funziona;
  extra `[analysis]` installabile a parte; wheel senza file di campagna.
- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 5-7 h · **Dip.**: P0.1.

#### ⬜ P3.2 — Eseguibile autonomo (PyInstaller)

Un file da scaricare e lanciare, **tutte le dipendenze incluse**: il DM medio non
deve sapere cosa sia `pip`. Matrice Linux / Windows / macOS in CI.

- **Accettazione**: l'eseguibile parte su una macchina **senza Python**; il
  linter funziona (livello 1 incluso nel bundle); avvisi di licenza delle
  dipendenze bundled inclusi nel pacchetto — **requisito, non cortesia**
  (ADR-0017 §4).
- **Engine**: Sonnet · **Impegno**: alto · **Stima**: 10-14 h · **Dip.**: P3.1.

#### ⬜ P3.3 — Rilicenziamento e provenienza

Verifica **dimostrata** — non assunta — che ogni file del package sia originale;
inventario delle licenze delle dipendenze; cambio di licenza del solo toolkit; la
campagna resta com'è.

- **Accettazione**: inventario di provenienza committato; nessun file del package
  senza attribuzione chiara; `LICENSE` della campagna invariato.
- **Engine**: Opus · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: P0.4.
  **Gate**: ⚠️ **verifica di un avvocato IP prima di qualunque vendita.**

#### ⬜ P3.4 — Conformità OGL / CC BY

Testo OGL 1.0a e catena Section 15 per i profili 3.5 e PF1e; attribuzione CC BY
4.0 per il profilo 5e; dichiarazione di Product Identity e Open Game Content;
formula di compatibilità **verificata testo alla mano** per ciascuno dei tre.
Marchi «D&D» e «Pathfinder» **fuori** da nome e marketing.

- **Accettazione**: un gate CI verifica che ogni release includa i file di
  licenza dovuti per i profili inclusi; nessun marchio nel nome del prodotto.
- **Engine**: Opus · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: P1.2.
  **Gate**: ⚠️ avvocato IP.

---

### Fase P4 — I due prodotti di contenuto

#### ⬜ P4.1 — Map pack neutri

Mappe **originali, world-neutral**, progettate con la scheda-mappa e verificate
dal linter, esportate in SVG/PNG/UVTT. Zero contenuto WotC — **nessuna mappa
RHoD, nemmeno riprogettata**. Etichetta `Contains AI-Generated Content` dove
pertinente.

- **Accettazione**: ogni mappa del pack passa le soglie o porta una **deroga
  scritta**; un gate verifica l'assenza di stringhe della campagna; ogni mappa ha
  la sua scheda-mappa pubblicata.
- **Engine**: Opus (design) → Sonnet (griglie) · **Impegno**: alto · **Stima**:
  6-8 h a mappa · **Dip.**: P2.1, e la scheda-mappa del piano gemello.

#### ⬜ P4.2 — Il metodo, come guida vendibile

Schede-mappa, le 9 metriche, il corpus di calibrazione, la disciplina di
progettazione — e la parte di inquadratura (blockout, ordine percettivo). È la
parte **senza concorrenti**, e utile anche a chi non compra il software.

- **Accettazione**: la guida sta in piedi **senza** il toolkit installato; ogni
  metrica ha un esempio prima/dopo su una mappa che il lettore può vedere.
- **Engine**: Opus · **Impegno**: alto · **Stima**: 20-25 h · **Dip.**: P2.4.

---

### Fase P5 — Gate di prodotto in CI

#### ⬜ P5.1 — Le tre invarianti dell'architettura, verificate

```
□ il dominio non importa render/export/CLI/profili   (grafo aciclico)
□ il package non contiene stringhe della campagna    (lista di termini vietati)
□ legend.yaml non contiene numeri di gioco           (nessun +N, %, CD)
□ ogni release include le licenze dei profili inclusi
□ l'eseguibile parte su macchina senza Python        (smoke su matrice OS)
```

- **Engine**: Sonnet · **Impegno**: medio · **Stima**: 6-8 h · **Dip.**: P0.4,
  P3.2.

---

## 5. Sequenza

| # | Lotti | Ore | Cosa hai in mano alla fine |
|---|---|---|---|
| 1 | P0.1 → P0.3 | 15-21 | il toolkit è **installabile**, con lint e test veri |
| 2 | **P1.1 + P0.4** | 22-30 | legenda funzionale + dominio separato. **La divergenza SVG↔UVTT è chiusa**: 3.689 celle di muro recuperate |
| 3 | P1.2 | 14-18 | **tre sistemi supportati** — il mercato passa da «i DM di 3.5» a 3.5+PF1e+5e |
| 4 | P3.1 + P3.3 | 11-15 | wheel pubblicabile, provenienza dimostrata |
| 5 | P1.3 → P2.1 → P2.2 | 24-32 | il linter completo e veloce |
| 6 | P3.2 + P3.4 + P5.1 | 22-30 | **eseguibile per DM non tecnici**, conformità, gate |
| 7 | P2.3 + P2.4 | 20-26 | dichiarato-vs-realizzato e soglie calibrate |
| 8 | P4.1 + P4.2 | 40+ | i due prodotti di contenuto |

**Totale**: ~170-215 h al netto di P4 (che scala con quante mappe si vendono).

**Il primo punto di rilascio possibile è dopo il passo 4**: un toolkit
installabile, multi-sistema, con la legenda corretta e la provenienza pulita —
**senza** il linter. Il linter è ciò di cui si parla, non ciò che porta il primo
utente: rilasciare prima e aggiungerlo dopo è la sequenza giusta, non un
compromesso.

---

## 6. Rischi

| Rischio | Mitigazione |
|---|---|
| P0/P1 rompono ciò che oggi funziona (11 import, modulo da 1.530 righe) | la rete c'è già: 70 test, byte-identità SVG, round-trip UVTT. Il layout `scripts/*.py` **resta invocabile identico** |
| L'export UVTT cambia su 6 mappe | **è il bug**, non una regressione: diff verificato a mano una volta e documentato |
| Tre profili = tre fonti da riseguire a ogni errata | suite di verifica per profilo; ogni profilo dichiara fonte e revisione; un profilo si può **ritirare** senza toccare il prodotto |
| `move_cost: 4` per PF1e non verificato | bloccante per il rilascio di **quel** profilo, non degli altri due |
| Conformità OGL sbagliata | gate CI sui file di licenza **+ avvocato IP prima della vendita**. Non autocertificabile |
| Le dipendenze bundled non sono ridistribuibili | gate di licenza permissiva già in ADR-0015, promosso a **requisito di prodotto** |
| Contenuto di campagna finisce nel package | gate automatico (P5.1), non disciplina a memoria |
| Il prodotto non trova compratori | i tre prodotti sono indipendenti: il metodo (P4.2) vende anche senza il software, e i map pack hanno il pubblico più largo |
| Il piano non chiude mai | il primo rilascio è al passo 4 di 8. Tutto il resto è incrementale su un prodotto **già uscito** |

---

## 7. Cosa questo piano NON risolve

- **Non rende la campagna vendibile.** ADR-0005 resta intatto: il blocco WotC è
  assorbente e non si aggira separando i prodotti.
- **Non è consulenza legale.** OGL, CC BY, marchi e rilicenziamento richiedono un
  avvocato IP prima della vendita.
- **Non garantisce un mercato.** Un linter di design non esiste — ma novità non
  significa domanda: è uno strumento **da progettista**, non da DM, e il pubblico
  è più piccolo e più tecnico di quello dell'export UVTT.
- **Non copre l'editor visuale**, che resta un piano separato — al quale però
  questo piano finalmente dà **qualcosa da importare**.

---

## Checklist

```
P0 substrato
□ P0.1 pyproject + fine degli 11 sys.path.insert
□ P0.2 livelli di dipendenza + jsonschema sui gate
□ P0.3 ruff + pytest + baseline copertura
□ P0.4 cucitura dominio/presentazione (grafo aciclico verificato)

P1 legenda e sistemi
□ P1.1 legend.yaml — 62 simboli, funzione neutra, 4 correzioni ⛰🏛🗼🗿
□ P1.2 rules/dnd35 · rules/pf1e · rules/dnd5e (+ verificare PF1e move_cost 4)
□ P1.3 zones/elevation/design_intent/map_kind — schema v1.1

P2 linter
□ P2.1 M1 M2 M7 M8 M9 (scipy)
□ P2.2 M3+strozzature (networkx) · M4/M5 ESATTE (tcod) · M6
□ P2.3 dichiarato vs realizzato
□ P2.4 calibrazione su corpus documentato

P3 prodotto
□ P3.1 wheel
□ P3.2 eseguibile autonomo (matrice Linux/Win/macOS)
□ P3.3 rilicenziamento + provenienza dimostrata   [gate: avvocato IP]
□ P3.4 conformità OGL 1.0a / CC BY 4.0 + marchi   [gate: avvocato IP]

P4 contenuto
□ P4.1 map pack neutri
□ P4.2 il metodo come guida

P5 gate
□ P5.1 le tre invarianti verificate in CI
```

> **Regola d'oro dei piani**: chi chiude un lotto aggiorna — nello stesso commit
> — questa checklist, la riga in `plans/INDEX.md` e una riga in
> `plans/CHANGELOG.md`.
