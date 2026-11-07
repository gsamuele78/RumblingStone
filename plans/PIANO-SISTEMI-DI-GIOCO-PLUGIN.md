# PIANO — I sistemi di gioco come plugin attivabili

> **Stato**: 🟡 proposta (2026-11-07), L0 fatto, D1-D5 al DM · **Classe**: G per la regola, C per i lotti
> **Nasce da**: il messaggio del DM del 2026-11-07 (citato in [ADR-0111](adr/ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md)): plugin per tutto il giro di strumenti, skill e agent, un set di regole diverso senza rifare tutto, in modo misurabile e deterministico, con un file di configurazione generale che attiva e disattiva i sistemi e mostra quelli supportati.
> **Decisione**: [ADR-0111](adr/ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md), proposta.
> **Dipende da**: ADR-0110 (termini ufficiali, ramo `regole-ufficiali`): `lessico_it.yaml`, `lessico_it_pf1.tsv`, `lessico_regole.py` sono il primo contenuto dei plugin, e restano loro.
> **Misure**: [plans/esperimenti/sistemi-plugin-2026-11-07/](esperimenti/sistemi-plugin-2026-11-07/) (`censimento.py`, `CENSIMENTO.json`, `impronte.py`, `IMPRONTE.json`).
>
> **In breve**: su 202 script, 31 dipendono dal sistema di gioco e 171 no. Il sistema di un modulo si decide in tre modi diversi, la lista dei termini 5e vietati ha due copie, e un sistema d20 nuovo oggi tocca 24 file. Il piano porta tutto a un file `sistemi.toml` e a plugin di dati in `sistemi/<id>/`, un lotto alla volta, con un banco che verifica che le uscite sui moduli 3.5 non cambino di un byte.

---

## §1 · Audit: lo stato di oggi

### §1.1 Gli script (censimento deterministico)

`python3 plans/esperimenti/sistemi-plugin-2026-11-07/censimento.py` conta nove famiglie di termini in ogni script e confronta il risultato con una classificazione scritta a mano, riga per riga, con il motivo. Con `--check` esce 1 se un file con punteggio ≥ 10 non è classificato. La conta da sola è rumorosa («GS» in `render_schemi.py` è il Giardino di Sale), per questo decide la classificazione e non il punteggio.

| Fascia | Cosa vuol dire | File | Esempi |
|---|---|---|---|
| A | regole cablate nel codice | 17 | `dmcore/tabelle.py` (TIPI, CLASSI, BAB, TAGLIE, ARMATURE), `dmcore/progressione.py` (DV, TS, BAB), `dmcore/caratteristiche.py`, `dmcore/incantesimi.py`, `dmcore/lettura_creatura.py` (`NON_MORTO_PF1E`), `update_xp.py` (soglie PE 3.5), `suggest_loot.py` (DMG 3.5 Tab. 3-5), `suggest_encounter.py`, `validate_bestiario.py`, i generatori |
| B | liste di termini per sistema | 5 | `validate_modules.py` e `validate_standalone.py` (5e vietati, due copie), `validate_prosa.py` (abilità 3.5), `coerenza_campagna.py` (classi e razze), `riscontro_srd.py` (fonti) |
| C | decide il sistema di un modulo | 2 | `domande_developer.py` (profilo + `ABILITA_ESTRANEE`), `dmcore/censimento.py` (Drappo per percorso) |
| D | etichette d20 in stampa | 7 | `build_booklet_html.py`, `export_booklet_typst.py`, `dmcore/schede.py`: oggi uguali in 3.5 e PF1e, tranne BMC/DMC sulla scheda del PG PF1e |
| N | neutro | 171 | mappe, stampa, prosa, piattaforma |

Le quattro misure di partenza (da `CENSIMENTO.json`):

| Misura | Oggi | Obiettivo |
|---|---|---|
| M1 · modi di decidere il sistema di un modulo | 3 (percorso, riga «**Sistema:**» in 26 master con 10 grafie, `sistema` in 3 profili) | 1 (`sistemi.toml`) |
| M2 · copie della lista dei termini 5e | 2 | 1 |
| M3 · costanti maiuscole a livello di modulo nei file A (tabelle e regex insieme) | 76 | tetto a cricchetto, scende a ogni lotto; le regex restano |
| M4 · file di codice da toccare per un sistema d20 nuovo | 24 | 0 (solo `sistemi/<id>/` e una riga in `sistemi.toml`) |

### §1.2 Skill e agent

| Skill | Asse | Nota |
|---|---|---|
| `dnd-35-srd`, `dnd-35-rules` | sistema `dnd35` | |
| `pathfinder-1e-srd` | sistema `pf1e` | serve anche ai moduli 3.5, come rinforzo: non si può spegnere quando PF1e non è il sistema base |
| `npc-villain-boosting` | rinforzo 3.5 + PF1e | usa i template PF1e sui PNG 3.5 |
| `forgotten-realms-lore` | ambientazione | Golarion non ha una skill sua: sta dentro `pathfinder-1e-srd` |
| le altre 13 `rumblingstone-*` | neutre | `module-standard` scrive la riga «Sistema: D&D 3.5 SRD (max PF1e), MAI 5e» come norma |

`build-skills.sh` e `sync-skills.sh` (matrice in `scripts/agents.conf`) installano tutte le 18 skill per sette agenti, senza sapere quale sistema è in uso.

### §1.3 Cosa il piano non rifà

- Le tabelle dei termini e il cancello sui nomi (ADR-0110): il plugin le punta per percorso.
- Le fonti in cache (ADR-0103, `riscontro_srd.py`): il plugin dichiara quale fonte è sua.
- Il manifest dei tool (ADR-0012): si aggiunge un campo, non un secondo registro.

## §2 · Sviluppo: i lotti

Ogni lotto è una PR. Ogni PR lancia `impronte.py --confronta` prima e dopo: le 12 impronte restano identiche, o la differenza è una correzione che il DM ha visto.

| Lotto | Cosa | File toccati | Misura |
|---|---|---|---|
| **L0** ✅ | censimento, banco d'invarianza, ADR-0111 proposta, questo piano | `plans/` | M1-M4 di partenza |
| L1 | fondazione: `sistemi.toml`, `sistemi/dnd35/` e `sistemi/pf1e/` con i soli descrittori, `scripts/dmcore/sistemi.py` (caricatore), `scripts/sistemi.py` (elenco, `--di FILE`, `--check`), campo `sistema` nello schema del manifest, test | nessuno strumento esistente | impronte 12/12; `sistemi.py` elenca 2 sistemi | <!-- validate-docs: futuro -->
| L2 | un rilevamento solo: `domande_developer`, `dmcore/censimento`, `build_monster_catalog` leggono `sistema_di()`; la riga «**Sistema:**» dei master diventa testo controllato (deve dire lo stesso sistema della configurazione); `e_pf1()` involucro, con l'ok del thread delle regole | 3 + test | M1 3 → 1 |
| L3 | termini: una lista 5e sola (nel plugin di famiglia d20, letta da tutti e due i validatori), `ABILITA_ESTRANEE`, le abilità di `validate_prosa`, classi e razze di `coerenza_campagna` | 5 | M2 2 → 1; stessi rilievi sui master |
| L4 | regole semplici: soglie PE (`update_xp`, e la traccia PF1e lenta/media/veloce come dato), tesoro per EL/GS (`suggest_loot`), EL (`suggest_encounter`) | 3 | M3 scende; PF1e passa da `non supportato` a supportato dove il dato c'è |
| L5 | nucleo delle creature: `dmcore/tabelle`, `progressione`, `caratteristiche`, `incantesimi`, `lettura_creatura` leggono le tabelle dal plugin; il grafo d'import resta quello di `test_grafo_import_creature.py` | 5 + 7 consumatori | M3 al minimo; impronte dei generatori identiche |
| L6 | skill e agent: `build-skills.sh`/`sync-skills.sh` chiedono a `sistemi.py --skill` quali skill installare (D5); `AGENTS.md` e `skills/ORCHESTRAZIONE.md` lo dicono | 4 | numero di skill installate per configurazione |
| L7 | etichette di stampa dal plugin (serve solo per BMC/DMC sulla scheda PF1e o per un sistema non d20) | 3 | stampa identica sui booklet 3.5 |
| L8 | prova del nove: un sistema d20 finto nei dati dei test (`prova-d20`) si aggiunge senza toccare codice | 0 | M4 = 0 |

### §2.1 Come sarebbe il file generale (bozza, D1-D4 aperte)

```toml
# sistemi.toml — i sistemi di gioco del progetto (ADR-0111)

[progetto]
predefinito = "dnd35"
attivi = ["dnd35", "pf1e"]
# dove si cerca la versione più potente di una regola, in ordine
# (preferenza del DM del 2026-10-18)
rinforzo = ["dnd35", "pf1e"]

[moduli]
# percorso dalla radice = sistema; vince il più specifico
"10-stand-alone/Il-Drappo-di-Tarsilia" = "pf1e"
"10-stand-alone/Il Giardino di Sale e Calce PF1e" = "pf1e"

[ambientazioni]          # solo se D4 = sì
attive = ["forgotten-realms", "golarion"]
"10-stand-alone/Il-Drappo-di-Tarsilia" = "golarion"
```

E il descrittore di un plugin:

```toml
# sistemi/pf1e/sistema.toml
id = "pf1e"
nome = "Pathfinder 1ª edizione"
famiglia = "d20"
licenza = "OGL 1.0a"
fonti = ["PRD PSRD-Data@76ea4784"]
skill = ["pathfinder-1e-srd"]

[capacita]
"lessico.italiano" = "../../scripts/lessico_it_pf1.tsv"     # ADR-0110
"creature.statistiche_per_gs" = "../../scripts/pf1e-statistiche-per-gs.yaml"
"termini.vietati" = { eredita = "d20", motivo = "le meccaniche 5e sono vietate in tutta la famiglia" }
"pe.soglie" = "dati/pe.toml"
"creature.costruzione" = "non supportato"   # oggi si costruisce in 3.5 con il rinforzo PF1e
```

`python3 scripts/sistemi.py` stamperà la matrice:

```
strumento            capacità                  dnd35   pf1e
update_xp            pe.soglie                 ✅      ✅
suggest_loot         tesoro.per_gs             ✅      ⬜ non supportato
genera_creatura      creature.costruzione      ✅      ⬜ non supportato
validate_modules     termini.vietati           ✅      ↪ eredita d20
```

## §3 · Validazione

| Controllo | Quando | Criterio |
|---|---|---|
| Banco d'invarianza (`impronte.py --confronta`) | ogni lotto, prima e dopo | 12/12 impronte identiche sui moduli 3.5 |
| `censimento.py --check` | ogni lotto, poi in CI | nessun file con punteggio ≥ 10 senza classe; M3 non sale |
| `sistemi.py --check` | da L1, in CI (canale testing di ADR-0099, poi stable) | ogni capacità chiesta da uno strumento esiste, eredita con motivo, o è `non supportato` dichiarato |
| Rifiuto pulito | da L4 | uno strumento su un modulo senza la capacità esce 2 prima di scrivere, come `binari.py` |
| Test esistenti | ogni lotto | `test_grafo_import_creature.py` e tutta la suite verdi; nessun test saltato |
| Prova del nove | L8 | un sistema finto si aggiunge con 0 file di codice toccati |
| Lettura del DM | L2 e L5 | la matrice e un booklet 3.5 rigenerato letti dal DM, non solo i validatori |

## §4 · Decisioni al DM

| # | Domanda | Consigliata | Cosa cambia |
|---|---|---|---|
| D1 | Formato del file generale | **TOML** | TOML ha le sezioni di un INI, liste e tipi veri, e si legge con `tomllib` della libreria standard. INI (`configparser`) non ha liste né tipi: «attivi» diventa una stringa da spezzare. YAML è già nel repo ma chiede PyYAML o il lettore ridotto di `dmcore/config.py` |
| D2 | Dove si dichiara il sistema di un modulo | **in `sistemi.toml` per cartella; la riga «Sistema:» resta nel master per chi legge, e un controllo verifica che dica lo stesso** | con la riga come fonte servirebbe normalizzare 10 grafie in 26 file; con i profili resterebbero fuori i master senza profilo |
| D3 | Quanto fare adesso | **L1 e L2 in una PR, poi un lotto per PR con il banco** | tutto in una PR vuol dire L5 (il rischio più alto) insieme alla fondazione, e una revisione molto più difficile |
| D4 | L'ambientazione (Forgotten Realms, Golarion) nello stesso file | **sì, in una sezione separata** | i due assi sono diversi (il Drappo è PF1e e Golarion, il Giardino PF1e è PF1e ma non Golarion); tenerli insieme evita un secondo file |
| D5 | Quali skill installare per gli agent | **quelle dei sistemi attivi più quelle dei sistemi di rinforzo** | filtrare solo sugli attivi toglierebbe `pathfinder-1e-srd` a una campagna solo 3.5, che la usa per i villain; installare sempre tutto lascia la configurazione solo informativa |

## §5 · Checklist

- [x] L0 · censimento, banco d'invarianza, ADR-0111 proposta, piano (2026-11-07)
- [ ] D1-D5 decise
- [ ] L1 · fondazione
- [ ] L2 · un rilevamento solo
- [ ] L3 · termini
- [ ] L4 · regole semplici
- [ ] L5 · nucleo delle creature
- [ ] L6 · skill e agent
- [ ] L7 · etichette di stampa
- [ ] L8 · prova del nove
