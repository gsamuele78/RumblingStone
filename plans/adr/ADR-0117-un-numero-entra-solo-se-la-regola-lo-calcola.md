# ADR-0117 — Un numero entra solo se la regola lo calcola

**Stato**: accettata (2026-11-09)
**Data**: 2026-11-09
**Decisione-fonte**: il DM (Jfs), 2026-11-09, thread «Scelte dell'8/11». Dopo che una ★ aveva portato nel canone l'AU +10 della Fanteria Hobgoblin, preso da una chat e non da una scheda: *«i valori sempre i più forti ma calcolati e non inventati; nel caso, se la versione PF1e è più forte usa PF1e, ma non inventare: deve essere compliant con le regole, altrimenti a cosa servono?»*. Poi: *«questa regola deve essere dentro un ADR per essere rispettata da tutti i thread, o ogni proposta di calcolo deve essere vincolata a questo controllo»*. Sulla card ha scelto «ADR più cancello in CI». E sulla copertura: *«vale per tutti gli stat block e le regole usate nel repo, nei booklet e negli stand alone? […] deve coprire tutto»*.
**Rapporti**: precisa [ADR-0091](ADR-0091-la-scheda-del-png-ha-una-forma.md) §4-bis (la versione più forte, costruita con un mezzo legale) e la estende a ogni numero di combattimento del repo. Usa i conti di `conformita_statblocchi.py` ([ADR-0064](ADR-0064-gli-attributi-si-scrivono-nel-bestiario.md), [ADR-0066](ADR-0066-le-creature-hanno-una-libreria-e-il-verificatore-non-importa-la-scelta.md)) e i dati dei sistemi di [ADR-0112](ADR-0112-il-motore-e-agnostico-e-le-regole-d20-sono-dati-e-formule.md). Le marche sono quelle di [ADR-0109](ADR-0109-una-marcatura-sola-e-il-dm-decide-il-canone.md).

## Contesto

La regola «la versione più forte» era scritta in ADR-0091 §4-bis e nel blocco «Vincoli sui fatti» di dieci skill. Non l'ha fatta rispettare nessun controllo, e il 2026-11-09 una ★ ha portato nel canone un AU +10 che nessuna scheda 3.5 o PF1e produce: l'ha fermato il DM, non la CI.

Misura dello stesso giorno, su `main`:

| Dove | Conti prima di questo ADR |
|---|---|
| Bestiario (119 schede) | pf, TS, BAB, lotta, attacco, iniziativa; l'attacco con una tolleranza da −1 a +2; in CI blocca solo `pf-dado` |
| Master in forma `**Campo:**` (ARC-08) | pf, CA, iniziativa, lotta; **non l'attacco**; solo rapporto. Un morso +37 finto di Fauci passava con «0 conti che non tornano» |
| Recinti ```statblocco``` dei master e degli stand alone | pf, CA, CD, scurovisione; non l'attacco |
| Unità di massa (AU) | nessun conto |
| Altri file con numeri di combattimento | nessuno legge i loro statblocchi: 75 file, soprattutto ARC-09, ARC-07 e PG |

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **ADR più cancello a cricchetto dentro `conformita_statblocchi.py`** (scelta del DM) | un numero nuovo che la regola non ricostruisce fa fallire la CI; si allarga lo strumento che il repo ha già | le discrepanze di oggi restano finché il DM non le decide; la copertura dei file in prosa si fa a lotti |
| Solo ADR | nessun codice | il +10 è passato con la regola già scritta: un agente la può saltare |
| Solo cancello, richiamando ADR-0091 | meno documenti | ADR-0091 parla delle schede dei PNG, non di unità, moduli e stand alone |
| Uno script nuovo | nessuna dipendenza dal vecchio | duplica il lettore delle creature (ADR-0066 lo vieta) |

## Decisione

1. **La regola.** Un numero di combattimento (pf, CA, TS, BAB, lotta o BMC, attacco, iniziativa, CD, AU) entra in una scheda del repo, in un booklet o in uno stand alone solo se la regola del suo sistema lo ricostruisce dalla scheda: 3.5 per il canone, PF1e per i moduli PF1e. Fra le versioni che si ricostruiscono vince la più forte (ADR-0091 §4-bis). Un numero che viene da una fonte esterna (una chat, un PDF, un modulo vecchio) e non si ricostruisce non entra, anche se è più alto. Un bonus che la regola non vede (oggetto, incantesimo, regola della casa) la scheda lo scrive accanto, con la marca di ADR-0109.
2. **I conti.** `conformita_statblocchi.py` fa tutti i conti che sa fare, **esatti**:
   - Bestiario: ogni scarto di `giudica`, più l'attacco esatto;
   - master in forma `**Campo:**`: anche l'attacco;
   - recinti ```statblocco```: anche l'attacco;
   - unità di massa: **AU = attacco della scheda uno contro uno + 2** (`mass_combat_guide_Dm.md`, «Bonus Attacco: Media +2»). L'unità deve rimandare alla sua scheda con una riga `Uno contro uno: \`Bestiario/…\``.

   L'attacco è BAB + For in mischia (Des a distanza o con Arma Accurata) + taglia + potenziamento dell'arma (+1 se perfetta) + Arma Focalizzata (+1) + Arma Focalizzata Superiore (+1). La formula è la stessa in 3.5 e PF1e: il conto `attacco` sta in `sistemi/*/dati/conformita.toml`.
3. **Il cancello.** `python3 scripts/conformita_statblocchi.py --cancello-numeri` è un cricchetto. `docs/audit/numeri-baseline.json` tiene gli scarti di oggi e i file che nessun conto legge ancora:
   - uno scarto nuovo, o un file nuovo con numeri che nessuno legge, fa fallire;
   - uno risolto si toglie con `--aggiorna-numeri`, che non aggiunge niente.

   In CI parte **non bloccante** (`continue-on-error`) e diventa bloccante dal 2026-11-23, come i cancelli di ADR-0109 e ADR-0114.
4. **La copertura.** «Tutto» si misura con `non_coperti` della baseline e scende a lotti, un thread alla volta coordinato dal thread padre. Un lotto insegna allo script una forma nuova (la riga «A.5 · … · **morso** +34» delle appendici DEF, le tabelle di ARC-09, le schede dei PG), oppure porta la scheda nella forma di ADR-0091. Le regole PF1e che il cancello oggi salta (BMC e DMC al posto della lotta, scurovisione, *corrompere l'acqua*) le scrive nel plugin PF1e il thread «Completare le regole PF1e per il cancello».

## Misura

Il 2026-11-09, sul repo:
- **38 scarti in baseline**: 15 AU di unità (13 senza scheda uno contro uno, 1 Orog a +12 contro +15, la «Supporto Tecnico» di ARC08-03); Gorthak e Madre Dana (+1, nelle due copie di ARC-08); Zog'tar (+3, in ARC07-DEF-4 e nel booklet); 9 schede del Bestiario (8 da +1 a +2, duergar −3) che la tolleranza nascondeva; 7 statblocchi degli stand alone PF1e; 2 pf dell'Abbazia; la scurovisione di Skullcrusher nel booklet.
- **75 file non coperti**.
- La prova: con Fauci a +37 e gli Orog a +16 il cancello fallisce e dice il conto (`test_il_numero_gonfiato_non_torna`, `test_l_au_e_l_attacco_della_scheda_piu_due`). Con +33 e +15 passa.

## Conseguenze

- Una ★ «più forte» si propone solo col conto scritto accanto, e il cancello lo rifà.
- I 38 scarti diventano decisioni del DM. Ciascuno si corregge col conto, oppure con un mezzo legale che porta il numero dove serve (ADR-0091 §4-bis.2). Il «+1 da spiegare» è la parte più grande.
- `--master` resta un rapporto e ora conta anche l'attacco. Il test `test_il_cricchetto_dei_master` ha il tetto di Gorthak e Dana.
- **Quello che non è misurato**: gli attacchi secondari (artigli, ali, coda con Multiattacco), le iterazioni (+22/+17), i danni, le CA delle unità (DU). Le capacità che alzano l'attacco senza un talento elencato (Ira, *favore divino*, Odio della stirpe) la scheda le deve scrivere, altrimenti il conto le segna.

## Da rivedere se

- Il cancello blocca un numero giusto per una regola che lo script non conosce: si aggiunge la regola con la sua prova, non si allarga la tolleranza.
- I lotti di copertura non scendono per un mese: il DM decide se portare quei file nella forma di ADR-0091 o se archiviarli.
