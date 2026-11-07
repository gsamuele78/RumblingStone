# ADR-0110 — I termini ufficiali hanno una tabella e un cancello

**Stato**: accettata (2026-11-07, Jfs nel thread «Standardizzare marcatura INFERRED e skill vincolate»)
**Data**: 2026-11-07
**Decisione-fonte**: il DM (Jfs), 2026-11-07: *«fai alla fine queste constrain sia sui termini che sulle regole una volta per tutte in modo da evitare continue allucinazioni e approssimazioni»*; *«il blocco delle regole sia più veloce possibile e non 2 settimane, misurando la versione precedente e quella nuova con almeno 30 test»*; *«per le stand alone dichiarate PF1e una tabella di corrispondenza diretta italiano → PF1e, non italiano → SRD → PF1e»*. Nomi decisi sulle card dello stesso giorno: Awesome Blow = Colpo Terrificante, Great Cleave = Incalzare Potenziato.
**Rapporti**: usa le fonti e la cache di [ADR-0103](ADR-0103-le-regole-si-riscontrano-sull-srd-in-cache.md); le marche di fonte sono quelle di [ADR-0109](ADR-0109-una-marcatura-sola-e-il-dm-decide-il-canone.md); è un cancello deterministico nel senso di [ADR-0108](ADR-0108-i-cancelli-deterministici-stanno-in-ogni-skill.md); i regolamenti come plugin attivabili sono ADR-0111.

## Contesto

Un agente che scrive il nome di un talento non ha modo di sapere, senza aprire
l'SRD, se esiste e come si chiama in italiano. Il repo usava per lo stesso
talento due o tre nomi (Fendere / Incalzare, Specializzazione in un'Arma /
Arma Specializzata, Colpo Devastante / Colpo Tremendo / Colpo Possente per
Awesome Blow), e nei moduli PF1e nomi della 3.5. La ricerca per nome di
`riscontro_srd.py regola` non trovava i talenti 3.5, perché l'SRD scrive
«Improved Trip <small>[General]</small>».

Misura del 2026-11-07, prima e dopo:
- 40 casi veri con risposta nota (`plans/esperimenti/regole-ufficiali-2026-11-07/casi.json`):
  13/40 prima, 40/40 dopo. Una parte dei casi italiani viene dalla stessa
  tabella che si misura: la prova dice che la tabella funziona, non che è completa.
- Fuori da `plans/`, sorgenti: varianti non ufficiali 71 → 0, nomi 3.5 nei
  moduli PF1e 10 → 0, talenti sconosciuti 142 → 140. Con i volumi di stampa:
  varianti 93 → 0.
- Riscontro indipendente dei nomi italiani 3.5 contro Golarion e
  miniaturefantasy: 68 concordi, 0 discordi, 12 non verificabili. Contro il
  database di Mephit: talenti 121/122, abilità 70/70, classi 30/31 concordi;
  i suoi nomi di incantesimi hanno refusi e scambi, lì non entrano. Contro la
  traduzione dell'SRD 3.5 di Editori Folli: 116 su 120 talenti base.
- Copertura: tabella 3.5 1.978 voci (talenti 384, incantesimi 607, oggetti
  magici 650, equipaggiamento 136, classi 53, domini 35, abilità 40,
  condizioni 38); tabella PF1e 4.762 voci (incantesimi 1.492, mostri 1.449,
  talenti 1.055, oggetti magici 415, classi 44, classi di prestigio 89,
  domini e sottodomini 103, stirpi 31). Mancano ancora gli archetipi PF1e
  (Golarion non dà il nome inglese per voce) e i mostri 3.5 in italiano.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| Elenco generato dalle fonti + tabella italiana a mano + cancello (scelta) | i nomi inglesi vengono dalla fonte, non dalla memoria; l'italiano si decide una volta | la tabella italiana 3.5 va estesa a mano |
| Solo il blocco vincoli nelle skill | nessun codice | un testo non impedisce un nome sbagliato; il 13/40 lo mostra |
| Tradurre automaticamente i nomi inglesi | copre tutto subito | inventa nomi italiani: è il problema da togliere |
| Copiare i testi delle regole nel repo | tutto a portata | ADR-0103: niente testo delle fonti nel repo |

## Decisione

**Ogni nome di talento in una scheda è un nome della tabella, un nome
delle fonti, o porta una marca di fonte; un controllo lo verifica a ogni PR.**

1. **Elenco generato** (`scripts/lessico_regole.py indice`): titoli e voci
   dell'SRD 3.5 e del PRD PF1e scaricati a commit fissato, nella cache, mai nel
   repo.
2. **Tabella italiano → SRD 3.5 → PF1e** (`scripts/lessico_it.yaml`): nome
   italiano ufficiale, voce 3.5, voce PF1e, varianti da correggere, nota sulle
   differenze. `verifica-tabella` fallisce se una voce non è nelle fonti.
3. **Tabella diretta italiano PF1e → PRD** (`scripts/lessico_it_pf1.tsv`):
   talenti e incantesimi dall'edizione italiana di Pathfinder come li riporta
   Golarion Insider, abilità e condizioni con il nome inglese riscontrato nel
   PRD; classi, classi di prestigio, domini, stirpi, mostri e oggetti magici dal
   link inglese che ogni pagina di Golarion porta (d20pfsrd o Archives of
   Nethys). Nei moduli PF1e vale solo questa; un nome della 3.5 è un errore.
   La tabella 3.5 (`scripts/lessico_it_35.tsv`) unisce miniaturefantasy, Sigil
   e il database bilingue di Mephit (github.com/mephitrpg/mephit); ogni riga
   dice chi ha fatto la coppia.
4. **Cancello bloccante da subito** (canale stable, ADR-0099), su richiesta
   del DM e dopo la misura: varianti e nomi 3.5 nei moduli PF1e fanno fallire
   la CI; i talenti sconosciuti hanno un ratchet che può solo scendere.
5. **I nomi incerti li decide il DM** con una card; la scelta entra in
   tabella con la data.

## Conseguenze

- Un nome sbagliato non arriva su main: la tabella dice quello giusto.
- Chi aggiunge un talento fuori SRD lo marca, o la CI lo segnala.
- La CI scarica circa 50 MB di fonti per questo job.
- Il controllo legge per ora solo le righe dei talenti; incantesimi, abilità e
  condizioni sono già in tabella PF1e, ma il loro cancello è un lotto successivo.
- I 140 sconosciuti restano: nomi inglesi fuori SRD senza marca, nomi italiani
  ambigui, residui di lettura. Si chiudono a lotti, ognuno con il conto.

**Da rivedere se**: il ratchet blocca PR legittime più di una volta su dieci;
o se il thread dei plugin (ADR-0111) sposta le tabelle in un descrittore per
sistema di gioco.
