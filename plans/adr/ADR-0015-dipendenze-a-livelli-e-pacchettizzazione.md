# ADR-0015 — Dipendenze a livelli e pacchettizzazione: il core resta stdlib, l'analisi integra librerie mature

**Stato**: proposta — **gate: decisione DM**
**Data**: 2026-07-26
**Decisione-fonte**: revisione del design software richiesta dal DM (2026-07-26) sul `PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA`: *«non reinventare la ruota — se esiste già ed è usabile in questo progetto, integrare invece di sviluppare da zero»*. Misure in `docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md` §6.

## Contesto

Il repo ha oggi una politica implicita e molto rigida: **stdlib only**. 30 tool su 39
la dichiarano nel manifest; le uniche eccezioni sono `pyyaml` (pipeline skill) e
binari esterni (`pandoc`, `cwebp`, `git`, `bash`). La CI installa una sola
dipendenza Python.

**Questa politica ha un valore reale e va nominato prima di toccarla**: il DM può
eseguire qualunque script su qualunque macchina con `python3` e basta — niente
venv, niente rete, niente `pip install` prima di una sessione. Per uno strumento
che deve funzionare la sera del gioco, è una proprietà, non un dettaglio.

Ha però un costo, oggi misurabile:

1. **Due validatori JSON Schema scritti a mano** — `tools_manifest.validate()` (che
   si autodefinisce «subset pragmatico, stdlib-only») e `compile_map_json.validate()`.
   Gli schemi draft-07 nel repo sono completi; i validatori no. Verificato:
   `jsonschema` valida **3 esempi su 4** contro `tactical_map.schema.json` **così
   com'è**, e il quarto fallisce *correttamente* (`units_in: meters`, che lo schema
   stesso documenta come da validare dopo la conversione).
2. **Il piano di level design stava per aggiungerne altri tre**: componenti connesse,
   dilatazione binaria, grafi, raycast. Misurato sulla mappa *Dirupo Mortale* 40×40:

   | Metrica | A mano (stdlib) | Con libreria | Guadagno |
   |---|---|---|---|
   | M1+M2 | ~18 righe di logica, 11,5 ms | **4 righe**, 0,8 ms (`scipy.ndimage`) | 14× più veloce, ¼ del codice |
   | M3 anelli + strozzature | grafo + punti di articolazione da scrivere | **1 riga ciascuna** (`networkx`) | codice che non esiste non ha bug |
   | M4 esposizione | «minuti in Python puro» → la guida ripiega sul **campionamento** | censimento **completo** 1.585 celle in **34 ms** (`tcod`, shadowcasting simmetrico) | la mitigazione diventa inutile: M4 esatta, non stimata |

   I valori coincidono al bit con l'implementazione a mano (M1 0.0309, M2 0.9691).
   E la M4 campionata **sottostimava**: esatta 0.913 contro 0.88 stimata.
3. **Nessuna pacchettizzazione**: 11 script fanno `sys.path.insert(0, ...)` per
   importarsi a vicenda. Nulla in `scripts/` è installabile o importabile da fuori.

Il terzo punto è quello che pesa sull'obiettivo dichiarato dal DM — un prodotto
**professionale e riusabile**: oggi il toolkit non è un pacchetto, è una cartella.

## Decisione

**Dipendenze a tre livelli, con il livello 0 intoccabile, e pacchettizzazione
del toolkit come libreria installabile.**

### 1. Livelli

| Livello | Chi | Dipendenze | Regola |
|---|---|---|---|
| **0 · core** | tutto ciò che sta sul percorso della sessione: `dm.py`, pipeline sessione/stato, `render_map_svg`, `compile_map_json`, `export_uvtt`, i validator di CI | **solo stdlib** | non negoziabile: `python3 scripts/dm.py` funziona su una macchina nuda, offline |
| **1 · analysis** (opzionale) | strumenti di *analisi*, non di produzione: `lint_map_design` e successori | `numpy` · `scipy` · `networkx` · `tcod` | assente la dipendenza → exit code documentato e messaggio azionabile, **mai** un crash e **mai** un impatto sul livello 0 |
| **2 · dev** | qualità del codice | `pytest` · `ruff` · `jsonschema` | non richiesto per usare il toolkit |

`jsonschema` sta al livello 2 e non al 1 perché serve ai **gate**, non all'uso: in
CI valida gli schemi; a runtime i tool mantengono i controlli semantici propri
(«questo simbolo è nella legenda ed è un terreno?»), che JSON Schema non può
esprimere. La divisione è netta: **struttura → `jsonschema`, semantica → codice
nostro**.

### 2. Criterio di ammissione di una libreria

Una dipendenza entra **solo se cancella codice che altrimenti scriveremmo e
manterremmo noi**, mai per comodità. Ogni voce dichiara nel manifest quale
implementazione a mano sostituisce. Se una libreria non elimina codice, non entra.

### 3. Gate di licenza

Solo licenze permissive (BSD / MIT / Apache-2.0 / PSF). Niente copyleft: il
toolkit è pensato per essere distribuibile (ADR-0005). Verificato sui candidati:
numpy BSD-3, scipy BSD-3, networkx BSD-3, jsonschema MIT, tcod BSD-2.

### 4. Pacchettizzazione

`pyproject.toml` alla radice, il toolkit diventa un package importabile con
entrypoint da console; gli 11 `sys.path.insert` spariscono. `[project.optional-
dependencies]` porta i livelli 1 e 2. Il layout `scripts/*.py` resta invocabile
com'è oggi (nessuna rottura per il DM): l'installazione è un'aggiunta, non una
sostituzione.

## Conseguenze

**Cosa diventa più facile**

- il toolkit diventa **installabile e importabile**: il presupposto di qualunque
  riuso fuori da questo repo, e dell'editor visuale come progetto separato;
- gli algoritmi che non scriviamo non hanno bug nostri, e sono già ottimizzati:
  M4 passa da «campionata per forza» a **esatta**, il che rende la metrica
  difendibile invece che approssimata;
- i validatori a mano si riducono ai soli controlli semantici — meno codice, e
  gli schemi smettono di essere documentazione decorativa;
- `ruff` e `pytest` sostituiscono la disciplina a memoria (i `# noqa: E402`
  sparsi indicano un flake8 usato e poi perso: senza configurazione, la regola
  esiste solo nella testa di chi scrive).

**Cosa diventa più difficile / a cosa si rinuncia**

- il livello 1 richiede `pip install` e quindi rete: **per questo è opzionale e
  fuori dal percorso di sessione**. Un linter di progettazione si usa mentre si
  prepara, non mentre si gioca;
- superficie di dipendenza da manutenere (CVE, breaking change a monte). Mitigazione:
  4 librerie, tutte mature, tutte permissive, tutte confinate a un solo tool;
- `tcod` emette già un `FutureWarning` sulle costanti (`tcod.FOV_*` →
  `libtcodpy.FOV_*`): usare la forma nuova fin da subito;
- la pacchettizzazione tocca 11 file di import. Il rischio è reale; la mitigazione
  è la suite esistente (70 test) più la byte-identità degli SVG.

**Cosa va rivisitato e quando**

- se il livello 1 crescesse oltre 4-5 librerie, o se una di esse entrasse nel
  percorso di sessione, questo ADR va riaperto: sarebbe il segnale che il confine
  fra core e analisi si è spostato;
- se il toolkit venisse davvero estratto come prodotto separato (vedi
  `PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA` §0-bis), la scelta fra un repo unico
  con package interno e due repo va decisa lì, non qui.
