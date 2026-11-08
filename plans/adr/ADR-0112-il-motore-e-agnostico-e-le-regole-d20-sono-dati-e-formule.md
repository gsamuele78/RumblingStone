# ADR-0112 — Il motore non conosce nessun gioco: regole, formule e fonti stanno nel plugin

**Stato**: proposta (2026-11-08), decisioni al DM in [PIANO-MOTORE-AGNOSTICO-D20](../PIANO-MOTORE-AGNOSTICO-D20.md) §4
**Data**: 2026-11-08
**Decisione-fonte**: il DM (Jfs), 2026-11-08: *«se estrai dal codice fonti.regole lo metti in file esterno letto dal codice e fare derive e conformità non presupporre 3.5 ma […] caricarlo in relazione al plugin di gioco […] una serie di template e regole che vengono caricate in relazione a tipo di gioco selezionato […] le best practices in ambito di produzione per evitare di embeddare nel codice regole plugin e derive ed usare un sistema agnostico»*. Risposte dello stesso giorno: microkernel e design guidato dai dati; ambito «d20 system like»; le librerie migliori, standard di fatto della comunità, con indagini misurate; moduli di codice per plugin dove un dato non basta; misura deterministica e dettagliata, lavoro a fasi.
**Rapporti**: continua [ADR-0111](ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md) (plugin di dati, L0-L8 chiusi); chiede un'eccezione motivata ad [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md) solo dove l'indagine la giustifica; entra con la regola dei canali di [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md); [ADR-0103](ADR-0103-le-regole-si-riscontrano-sull-srd-in-cache.md) per le fonti.

## Contesto

Con ADR-0111 le **tabelle** sono uscite dal codice: 13 capacità su 13 sono dati per d20, 3.5 e PF1e, e un plugin d20 finto si aggiunge senza toccare Python (prova del nove, PR #336). Restano tre cose che il codice sa del 3.5:

1. **Il motore sceglie il sistema all'import.** Il censimento F0 ([censimento_formule.py](../esperimenti/motore-agnostico-2026-11-08/censimento_formule.py), con l'AST) trova 5 chiamate `dati("<sistema>", …)` eseguite quando un modulo viene importato, in 4 moduli del nucleo (`tabelle` e `incantesimi` col 3.5). I 6 strumenti che li usano (fra cui `derive_statblocks`, `conformita_statblocchi`, `genera_attributi`) non chiedono mai `sistema_di`, quindi leggono le tabelle 3.5 anche su una scheda del Drappo o del Giardino PF1e.
2. **Le formule sono codice.** Almeno 6 funzioni: `mod = (x − 10) // 2`, TS buono `2 + dv // 2`, TS cattivo `dv // 3`, la CD degli incantesimi, il livello d'incantatore ridotto, il BAB per frazione: piccole, ma sono regole del sistema scritte in Python.
3. **Le fonti sono codice.** `fonti.regole` sono URL, commit e sha256 in `riscontro_srd.py:FONTI`.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Microkernel guidato dai dati**: un nucleo che non conosce giochi; ogni sistema è un pacchetto (manifest, schema, tabelle, formule come espressioni, moduli di codice registrati per nome); gli strumenti ricevono un oggetto «regole del sistema» invece di importare costanti | è il modello di PCGen (game mode e file di dati) e di Foundry VTT (`system.json` più modello dati); deterministico; ogni plugin si valida con uno schema prima dell'uso; un sistema d20 nuovo non tocca il nucleo | bisogna scegliere e mantenere un linguaggio delle formule e uno schema; quello che è un algoritmo vero resta codice, anche se dentro il plugin |
| Solo i tre limiti noti, senza linguaggio di formule | poco lavoro | le formule restano Python: un sistema che cambia anche solo il TS buono tocca il nucleo |
| Plugin di solo codice (`importlib.metadata` entry point o `pluggy`) | massima libertà per sistema | codice eseguito per configurazione; regole non leggibili dal DM; più difficile da misurare |
| Motore generico di regole (Rete, Drools, `durable_rules`) | regole dichiarative complete | pesanti, non deterministici nell'ordine di scatto, nessun uso nella comunità dei giochi di ruolo per questo problema |

## Decisione

**Il nucleo non conosce nessun gioco. Tutto quello che è regola sta in `sistemi/<id>/` come dato, formula o modulo di codice registrato, e lo strumento lo riceve per il sistema del file su cui lavora.**

1. **Contesto esplicito.** `dmcore.sistemi.regole(id)` restituisce un oggetto immutabile con tabelle, formule e moduli del sistema, caricato una volta e messo in cache. Nessun modulo del nucleo carica un sistema all'import; le costanti di modulo di oggi restano come involucro del sistema predefinito finché ci sono chiamanti, poi spariscono (cricchetto).
2. **Formule come espressioni.** Le regole aritmetiche stanno in `sistemi/<id>/dati/formule.toml` (per esempio `ts_buono = "2 + dv // 2"`). Il linguaggio e il valutatore li sceglie l'indagine I1 del piano tra lo standard di fatto (CEL), le librerie diffuse (simpleeval, asteval) e un valutatore minimo su `ast`. Il criterio è misurato: correttezza su tutto il dominio delle formule attuali, nessun accesso fuori dall'espressione, determinismo, funzionamento nelle skill impacchettate.
3. **Schema per ogni capacità.** Ogni file di dati ha uno schema, e `sistemi.py --check` lo verifica in CI. Lo schema si esporta in JSON Schema per gli editor (`taplo`, `#:schema`). Strumento scelto dall'indagine I2 ([report](../esperimenti/motore-agnostico-2026-11-08/i2_schema/REPORT.md)): JSON Schema scritto con le parole della bozza 7, nel plugin accanto ai dati; nella skill lo valida fastjsonschema (puro Python, portato dentro il pacchetto), in CI anche `jsonschema`. Prende 492 difetti su 503 contro i 123 di oggi. Pydantic (496) è bocciato perché compilato e perché lo schema diventerebbe codice. Le due regole fra campi (predefinito fra gli attivi, soglie crescenti) restano in `sistemi.py --check`.
4. **Moduli di codice per plugin.** Un algoritmo che non è una tabella né una formula, come un nuovo modo di sommare i GS, sta in `sistemi/<id>/codice/` ed è registrato per nome nel `sistema.toml`. Il nucleo li carica solo da lì, mai da percorsi arbitrari. L'indagine I3 ([report](../esperimenti/motore-agnostico-2026-11-08/i3_moduli/REPORT.md)) ha scelto `importlib.util.spec_from_file_location`, dalla libreria standard, con un nome di modulo unico per ogni sistema: rifiuta 12 dichiarazioni ostili su 12. Gli entry point di PyPA sono bocciati: accettano `os:system`, richiedono un'installazione e due plugin con lo stesso modulo si scambiano il codice. Anche pluggy è bocciato per ora, perché dà lo stesso risultato con una dipendenza in più.
5. **Fonti come dati.** `fonti.regole` va in `sistemi/<id>/dati/fonti.toml`; gli sha256 restano rivisti nel diff come oggi.
6. **Ambito**: la famiglia d20 (3.5, PF1e e sistemi simili). Un sistema non d20 resta fuori finché il DM non lo chiede; il nucleo non deve impedirlo, ma non lo prepara.

## Conseguenze

- `derive_statblocks`, `conformita_statblocchi` e `genera_attributi` useranno le tabelle PF1e sulle schede PF1e: le loro proposte sul Drappo e sul Giardino cambiano. La differenza si misura e il DM la legge prima del merge (D6 del 2026-11-08: «ok»).
- Una libreria esterna nel nucleo romperebbe le skill che girano senza `pip`. Perciò una libreria entra solo se l'indagine mostra che il guadagno misurato la paga, e allora entra **dentro il pacchetto**, come in iemod-fetch: versione e sha256 fissati, licenza scritta, portata nell'archivio della skill e nel bundle di rilascio (DM, 2026-11-08: *«tutto quello che serve deve essere scaricato come bundle con tutti i requisiti»*). È l'eccezione ad ADR-0037, una libreria alla volta.
- Il banco d'invarianza di ADR-0111 (12 impronte) resta il cancello di ogni fase sui moduli 3.5, e si aggiungono il banco delle formule e i PDF typst (testo e pagine dei 20 booklet).

**Da rivedere se**: l'indagine I1 non trova un linguaggio che passi tutti i criteri (allora le formule restano funzioni registrate nei moduli di plugin); oppure una fase cambia un'uscita 3.5 senza una correzione voluta dal DM; oppure il DM porta un sistema non d20.
