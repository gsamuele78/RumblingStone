# ADR-0014 — La legenda funzionale è la fonte unica: la funzione di gioco di un simbolo è un dato, non prosa né un `set` cablato

**Stato**: proposta — **gate: decisione DM** (in particolare le 4 classificazioni di §Decisione.3)
**Data**: 2026-07-26
**Decisione-fonte**: lotto A1 di `plans/PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md`; misura in `docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md` §2.1; §L5.5 della guida «Dall'immagine mentale all'artefatto» (2026-07-25). Coincide con il lotto **E1** di `PIANO-EDITOR-VISUALE-MAPPE-TATTICHE`.

## Contesto

Un simbolo della griglia porta due informazioni distinte: **come si disegna**
(pattern, colore, prop) e **cosa fa in gioco** (blocca il movimento? la vista?
dà copertura? a che quota sta? è nominabile al tavolo?).

Oggi solo la prima è un dato. `SYMBOLS` in `scripts/render_map_svg.py` descrive
il rendering; la funzione di gioco vive in due posti che nessuno script può
interrogare:

1. **in prosa, dentro l'etichetta** — `"🪨": {"it": "Rocce/macerie (copertura
   +4 CA, terreno difficile)"}`;
2. **cablata in `set` dentro i consumatori** — `WALL_SYMS`, `DOOR_SYMS`,
   `LIGHT_SYMS` in `export_uvtt.py`, `HAZARD_SYMS` in `import_ultraclear.py`.

Due fonti di verità che possono divergere in silenzio — e **hanno già
divergiuto, in entrambe le direzioni**:

```
renderer, solidi (HEAVY_PATS)      : ⛰ ⬛ 🏰 🟪
export_uvtt, WALL_SYMS             : ⬛ 🏛 🏰 🗼 🗿 🟪
solido nel render ma NON muro UVTT : ⛰
muro UVTT ma NON solido nel render : 🏛 🗼 🗿
```

Conseguenza concreta: la parete rocciosa di *Dirupo Mortale* (ARC-08) occlude
nell'SVG stampato e **non blocca la linea di vista in Foundry**. La stessa
mappa applica due regole diverse a seconda del supporto.

Ci sono due forze aggiuntive:

- **Layering.** Le metriche di level design (§L5) hanno bisogno di sapere se
  una cella dà copertura o blocca la vista. Implementate oggi, dovrebbero
  importare `WALL_SYMS` **da un exporter**. Un exporter non possiede il modello
  di dominio.
- **Convergenza di piani.** L'editor visuale (`PIANO-EDITOR-VISUALE-MAPPE`,
  lotto E1) ha già pianificato una legenda condivisa. Farla una volta serve
  tre consumatori: editor, linter, export.

## Decisione

**Promuovere la funzione di gioco a dato di prima classe in una fonte unica,
`scripts/legend.yaml`, da cui tutto il resto è derivato.**

1. **Struttura.** Ogni simbolo dichiara `label`, `render{}` (mode, pat, prop,
   fill) e `function{}`:

   ```yaml
   symbols:
     "🪨":
       label: "Rocce / macerie"
       render:   {mode: icon, prop: pr_rocks, fill: "#ced4da"}
       function:
         blocks_movement: false
         blocks_sight: false
         cover: half              # none | half | full
         difficult_terrain: true
         elevation_m: 0
         destructible: true
         nameable: true           # → può fare da landmark (M8, Lynch)
   ```

2. **Derivazione, non duplicazione.**
   - `render_map_svg.SYMBOLS` è generata dal YAML (o da un `legend.json`
     committato e verificato in CI, come già si fa per `docs/tools/`);
   - `export_uvtt.py` deriva muri, porte e luci da `function` ed **elimina** i
     propri `set`; `import_ultraclear.HAZARD_SYMS` idem;
   - `skills/rumblingstone-mapmaking/references/legenda-universale.md` si
     **genera** dal YAML, con gate di sincronizzazione in CI;
   - i tool nuovi (linter, editor) leggono la legenda, mai un set proprio.

3. **Le quattro divergenze si risolvono con una decisione dichiarata**, non con
   una scelta implicita del codice — è una questione di regole 3.5, non di
   implementazione, e va **al DM**:
   - `⛰` montagne/creste — muro pieno, o copertura totale scalabile?
   - `🏛` edificio/tempio, `🗼` torre, `🗿` statua — muro pieno, o prop
     occludente che dà copertura senza essere impenetrabile?

4. **Nessuna regressione visiva.** Il refactor è verde solo se i 17 SVG legacy
   restano **byte-identici** (`validate_maps.py`) e il round-trip UVTT della CI
   passa.

## Conseguenze

**Cosa diventa più facile**

- una sola verità su cosa sia un muro: SVG, UVTT ed editor non possono più
  divergere in silenzio;
- le metriche M1-M8 diventano calcolabili senza set hardcoded sparsi, e il
  linter dipende dal dominio invece che da un exporter;
- `elevation_m` trova finalmente dove vivere (per simbolo qui, per zona nel
  contratto JSON) → M6 diventa possibile;
- `nameable` rende misurabile un concetto finora solo narrativo: se i giocatori
  possano dire «mi sposto dietro il carro bruciato» invece di «vado in K12»;
- `legenda-universale.md` smette di essere una copia manuale da tenere allineata.

**Cosa diventa più difficile / a cosa si rinuncia**

- una dipendenza in più nel percorso di rendering (parser YAML stdlib o
  `legend.json` committato: **niente pyyaml obbligatorio**, coerentemente con
  `stdlib_only` del manifest);
- aggiungere un simbolo richiede di dichiararne la funzione — attrito voluto:
  è il punto;
- il refactor tocca 4 script maturi e ben testati. Il rischio è reale e la
  mitigazione è il gate di byte-identità, non la prudenza.

**Cosa va rivisitato e quando**

- se l'editor visuale (E2-E10) richiede campi non previsti qui, si estende
  `function` — mai si crea una seconda fonte;
- `cover` è oggi un enum a tre valori (`none|half|full`). Se le regole 3.5 al
  tavolo mostrassero che serve il caso «copertura totale ma non blocca la
  vista» (feritoie, grate), va aggiunto un campo, non abusato l'enum;
- la scelta fra YAML sorgente + JSON derivato committato, o solo YAML letto a
  runtime, si decide in A1 sulla base del vincolo `stdlib_only`.
