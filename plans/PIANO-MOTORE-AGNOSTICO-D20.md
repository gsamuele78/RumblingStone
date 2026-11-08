# PIANO — Il motore agnostico: regole, formule e fonti d20 nel plugin

> **Stato**: 🟡 in corso (2026-11-08), F0, I1, I2 e I3 fatte, I4 da fare · **Classe**: G per la regola, C per le fasi
> **Nasce da**: i messaggi del DM del 2026-11-08 (citati in [ADR-0112](adr/ADR-0112-il-motore-e-agnostico-e-le-regole-d20-sono-dati-e-formule.md)).
> **Decisione**: [ADR-0112](adr/ADR-0112-il-motore-e-agnostico-e-le-regole-d20-sono-dati-e-formule.md), proposta. Continua [PIANO-SISTEMI-DI-GIOCO-PLUGIN](PIANO-SISTEMI-DI-GIOCO-PLUGIN.md) (L0-L8 chiusi).
> **Fuori da questo piano**: l'installazione automatica di typst e pdfcpu (mise, lockfile, Renovate) ha un thread suo.
>
> **In breve**: dopo ADR-0111 le tabelle sono dati, ma il motore carica ancora i sistemi all'import (5 chiamate in 4 moduli; 6 strumenti a valle che non chiedono mai il sistema del file), le formule sono Python e le fonti sono una costante. Questo piano porta il motore a ricevere le regole per il sistema del file, sposta formule e fonti nei plugin, sceglie con indagini misurate il linguaggio delle formule e lo schema, e chiude con una seconda prova del nove: un sistema d20 con formule diverse aggiunto senza toccare il nucleo.

---

## §1 · Audit: lo stato di oggi (2026-11-08, main e06c2cf)

| Misura | Valore | Come si rifà |
|---|---|---|
| **A1** chiamate `dati("<sistema>", …)` eseguite all'import | 5: `tabelle.py:64` e `incantesimi.py:84` «dnd35», `incantesimi.py:175` e `lettura_creatura.py:572` «pf1e», `statblock.py:55` «d20» | `censimento_formule.py` |
| **A2** strumenti che importano il nucleo con regole (`tabelle`, `incantesimi`, `progressione`, `caratteristiche`) | 6: `conformita_statblocchi`, `derive_statblocks`, `genera_attributi`, `genera_creatura`, `impronta_creature`, `validate_bestiario` | idem |
| **A3** formule del sistema scritte in Python (funzioni di un solo `return` aritmetico) | 6: `mod`, `ts_buono`, `ts_cattivo`, `cd_incantesimo`, `da_modificatore`, `creature_pf1e._mod`. È un limite inferiore: le formule dentro funzioni più lunghe (`progressione.ts_base_di`, `bab_atteso`, `livello_incantatore`) non le conta, e I1 le elenca a mano | idem |
| **A4** capacità ancora in codice | 2 (`fonti.regole` in dnd35 e pf1e) | idem |
| **A5** strumenti che importano il nucleo senza mai chiedere `sistema_di` | 6 (gli stessi di A2): usano il predefinito anche su un file PF1e | idem |
| **A6** PDF typst prima/dopo L7 | 20 PDF, testo e pagine identici | `pdftotext` e `pdfinfo` su `export_booklet_typst.py` di ogni manifest, a 340fae0^ e a main |

**Cosa fanno gli altri (ricerca del 2026-11-08).**
- [PCGen](https://deepwiki.com/PCGen/pcgen/5-game-data-system) tiene le regole d20 in file di testo raggruppati per *game mode*, con un manifest per campagna. Ha dovuto riscrivere il suo linguaggio delle formule (via da JEP, verso `MODIFY` e variabili con scope): il linguaggio è la parte che costa.
- [Foundry VTT](https://foundryvtt.com/article/system-development/) fa di ogni sistema una cartella con `system.json` e un modello dati dichiarato; il codice del sistema vive nel pacchetto, non nel nucleo.
- [CEL](https://python-common-expression-language.readthedocs.io/) è il linguaggio di espressioni di riferimento per regole in configurazione (Kubernetes, Envoy): non Turing-completo, termina sempre, non ha effetti collaterali.

## §2 · Sviluppo a fasi

Ogni fase è una PR, misurata prima e dopo con gli stessi comandi.

| Fase | Cosa | Criterio di uscita |
|---|---|---|
| **F0** audit come codice ✅ | [`censimento_formule.py`](esperimenti/motore-agnostico-2026-11-08/censimento_formule.py) conta A1-A5 con l'AST (non con le regex), scrive [`CENSIMENTO.json`](esperimenti/motore-agnostico-2026-11-08/CENSIMENTO.json); `--check` è un cricchetto | numeri ripetibili byte per byte (provato: due esecuzioni, file identici); un test lo fissa |
| **I1** indagine: linguaggio delle formule ✅ [report](esperimenti/motore-agnostico-2026-11-08/i1_formule/REPORT.md): vince **simpleeval ristretto** (7/7 formule, 0/50 ostili, un file MIT senza dipendenze); CEL bocciato su (d) e sulla divisione che tronca (5 casi su 61 sbagliati in silenzio); asteval apre file | candidati CEL (`cel-python`, Apache-2.0), simpleeval (MIT), asteval (MIT), valutatore minimo su `ast` della libreria standard | (a) tutte le formule di A3 danno lo stesso risultato su tutto il dominio (livelli/DV 0-40, punteggi 1-60); (b) 50 espressioni ostili (attributi, import, cicli, numeri enormi) rifiutate; (c) stesso risultato in 100 esecuzioni; (d) funziona in una skill impacchettata senza `pip`; (e) licenza, manutenzione, tempo per formula. Report con tabella |
| **I2** indagine: schema dei plugin ✅ [report](esperimenti/motore-agnostico-2026-11-08/i2_schema/REPORT.md): su 503 difetti generati, oggi se ne prendono 123 con 77 crash; **JSON Schema** 492 senza falsi allarmi, validato nella skill da **fastjsonschema** (puro Python, BSD-3) e in CI da `jsonschema`; pydantic 496 ma compilato e lo schema diventa codice, bocciato | Pydantic v2 (MIT), `jsonschema` (MIT), validazione a mano di oggi | **punteggio di mutazione**: 200 difetti generati in modo deterministico (seme fisso) nei TOML dei plugin (chiave mancante, tipo sbagliato, capacità sconosciuta, riferimento a file assente, eredità circolare); % presi e qualità del messaggio; export JSON Schema per `taplo` |
| **I3** indagine: moduli di codice per plugin ✅ [report](esperimenti/motore-agnostico-2026-11-08/i3_moduli/REPORT.md): vince **importlib** (`spec_from_file_location`, libreria standard, 14 righe, 12/12 ostili rifiutate, EL identici su 4.494 liste); gli entry point accettano `os:system` e fanno arrivare al PF1e l'algoritmo del 3.5 (72/4.494); pluggy uguale a importlib ma con una dipendenza che oggi non serve | registro per nome in `sistema.toml` caricato con `importlib` da `sistemi/<id>/codice/`, entry point di `importlib.metadata`, `pluggy` (MIT) | righe di codice, test necessari, impossibilità di caricare codice fuori da `sistemi/` (test ostile) |
| **I4** indagine: PCGen | lettura dei *game mode* e del sistema di formule di PCGen; tabella «concetto loro → nostro» | cosa adottiamo e cosa no, con il motivo |
| **F1** fonti come dati | `fonti.regole` → `sistemi/<id>/dati/fonti.toml`, letto da `riscontro_srd.py` | A4 1 → 0; impronte 12/12 identiche; `riscontro_srd --check` invariato |
| **F2** contesto esplicito | `dmcore.sistemi.regole(id)`; nessun modulo carica un sistema all'import; involucri per il predefinito | A1 5 → 0; impronte 12/12; grafo d'import delle creature verde |
| **F3** formule nei dati | un file `formule.toml` nei dati del plugin d20, valutato con il vincitore di I1; schema di I2 | A3 → 0 nel nucleo; banco delle formule identico su tutto il dominio |
| **F4** strumenti per sistema del file | `derive_statblocks`, `conformita_statblocchi`, `genera_attributi` usano `regole(sistema_di(file))` | A5 6 → 0; uscite 3.5 identiche; diff delle uscite PF1e misurato e **letto dal DM** prima del merge |
| **F5** moduli di plugin | `METODI` di `suggest_encounter` → registro del plugin (I3) | nessun algoritmo di sistema nel nucleo; test ostile verde |
| **F6** prova del nove 2 | plugin d20 finto con formule diverse (es. TS buono `3 + dv // 2`) e un metodo EL suo | 0 file del nucleo toccati; le uscite cambiano esattamente come le formule dicono |

## §3 · Validazione

| Controllo | Quando | Criterio |
|---|---|---|
| Banco d'invarianza (`impronte.py --confronta`, ADR-0111) | ogni fase | 12/12 impronte identiche sui moduli 3.5 |
| Banco delle formule | da F3 | ogni formula dà lo stesso risultato della funzione Python che sostituisce, su tutto il dominio |
| PDF typst | ogni fase che tocca la stampa | testo (`pdftotext`) e pagine (`pdfinfo`) dei 20 PDF identici |
| Punteggio di mutazione dello schema | da F3, in CI | non scende sotto il valore misurato in I2 (492/503), 0 crash |
| Censimento F0 (`--check`) | ogni fase, in CI | A1-A5 non salgono (cricchetto) |
| Suite e CI | ogni fase | «Validate skills & scripts» e «Build skill packages» verdi; in questo container 49 test falliscono anche su main, e il numero non deve salire |
| Lettura del DM | F4 | il DM legge le proposte PF1e cambiate sul Drappo e sul Giardino |

## §4 · Decisioni al DM

| # | Domanda | Consigliata | Cosa cambia |
|---|---|---|---|
| D1 | Come entra una libreria nel motore | **come in iemod-fetch (ADR-0043 di quel repo): libreria standard a runtime più le poche librerie che si guadagnano il posto, *portate dentro* il pacchetto (versione e sha256 fissati, licenza scritta, nell'archivio della skill e nel bundle di rilascio con SHA256SUMS e attestazione), così niente `pip` dove la skill gira**. Ogni libreria entra solo se l'indagine (I1, I2, I3) misura un guadagno | il DM l'ha indicato il 2026-11-08 («tutto quello che serve deve essere scaricato come bundle con tutti i requisiti»); resta da decidere caso per caso quali librerie superano la misura |
| D2 | Accettare ADR-0111 | dopo questo piano, insieme ad ADR-0112 | i due ADR descrivono la stessa architettura in due tempi |

Già deciso dal DM il 2026-11-08: microkernel guidato dai dati; ambito d20; librerie standard di fatto scelte con indagini misurate; moduli di codice per plugin; diff PF1e letto prima del merge; typst nel thread suo.

## §5 · Note oneste

- Il linguaggio delle formule è il rischio maggiore: PCGen l'ha rifatto una volta. Se I1 non trova un candidato che passi tutti i criteri, le formule restano funzioni Python, ma dentro i moduli di plugin (F5) e non nel nucleo.
- F4 **cambia** uscite di proposta sui moduli PF1e. È voluto, ma è l'unica fase che non è invarianza pura.
- Un sistema non d20 resta fuori: i campi del blocco statistiche (GS, CA, TS) sono d20 per costruzione.
