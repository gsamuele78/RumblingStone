# PIANO — Uno standard solo per i dati delle creature e per la stampa dei booklet

> **Stato**: 🟡 in corso (2026-10-29). Audit A1 e A2 fatti, misura registrata e in CI. Le decisioni D1-D4 sono proposte e aspettano il DM · **Classe**: C per il codice, K per i master da convertire
> **Nasce da**: la richiesta del DM del 2026-10-29, dopo la PR #295: *«uniformare tutti i master nel miglior template possibile […] e poi il miglior layout possibile per la stampa usando questo master di dati […] in una pipeline che azzera i glitch […] e sia misurabile e registri il miglioramento […] creando delle pipeline std e dei test concreti e reali e professionali che verifichino la correttezza, il miglioramento e l'aderenza agli standard professionali dell'editoria»*. Poi, sulla scheda di decisione: la #295 non si unisce, si rifà dentro questo standard (scelta B, «Fermarla»), e il layout si confronta con quello degli AP 3.5 e PF1e più apprezzati dalla community.
> **Decisioni collegate**: [ADR-0105](adr/ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md) (il riquadro unico, proposta, nella #295); [ADR-0020](adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md) (la catena Typst); [ADR-0070](adr/ADR-0070-l-apparato-di-lavoro-non-va-in-stampa-e-ogni-pagina-si-stampa-una-volta.md) (l'apparato non va in stampa).
> **Misura riproducibile**: `python3 scripts/misura_stampa.py --tutti`, registro in [`docs/audit/stampa-booklet.json`](../docs/audit/stampa-booklet.json).

## Dove siamo

La #295 fa metà del lavoro: le creature escono in una forma sola. Restano tre
problemi.

1. **I numeri sono scritti due volte.** Nel master c'è il blocco
   ` ```statblocco ` e sotto ci sono le righe leggibili (Difesa, Attacco…) che
   ripetono gli stessi numeri a mano. Possono divergere. Oggi lo impedisce
   solo un confronto dei numeri fatto durante la conversione.
2. **Il layout esiste in tre copie.** Typst, HTML e Homebrewery implementano
   ognuno ogni elemento (riquadro, read-aloud, tabella, nota DM, figura).
   Colori, caratteri e spaziature sono ripetuti in tre posti, e le schede dei
   PG (`scheda-pg.typ`) hanno margini propri, non speculari.
3. **La stampa si misurava solo in parte.** Fino a questo piano la CI
   controllava che il libro compilasse, che l'apparato non finisse in stampa e
   che le righe non si sovrapponessero. Non misurava corpo minimo, immagini,
   font, gabbia, riquadri spezzati.

## Prima misura (A2, 2026-10-29)

`misura_stampa.py` compila i 17 booklet e ne legge il PDF.

| Misura | Esito |
|---|---|
| Font non incorporati | 0 in tutti i booklet |
| Corpo mediano del testo | 10 pt (9 pt le schede PG del Drappo) |
| Testo oltre la gabbia dei margini | 0, tranne il titolo di copertina del Ritorno alla Forgia (1) e le schede PG del Drappo (299: margini di 1 cm, non quelli del tema) |
| Testo sotto 7 pt | 1.393 pezzi in 7 booklet, quasi tutti etichette di mappe SVG rimpicciolite fino a 2,5-3,9 pt; nel Drappo anche le griglie a spaziatura fissa a 6,1 pt |
| Immagini sotto 300 dpi | 222, soprattutto nell'appendice mappe di ARC-07 (strati a 72 dpi) |
| Riquadri di creatura spezzati fra due pagine | 14 su 76 riquadri stampati (Terros, la Sentinella, Fra' Timoteo…) |
| Pagine con un'immagine di almeno un quarto di pagina | 0-26%; le mappe vettoriali non contano |

Note oneste sulla misura:
- La gabbia ammette 4 pt di sporgenza: è la punteggiatura che Typst appende al
  margine di proposito.
- Gli strati sfocati che Typst rasterizza sopra un'immagine a piena
  risoluzione non contano come immagini sgranate. Quelli a 72 dpi di ARC-07
  contano, perché sotto non c'è un'immagine buona. Non ho ancora guardato a
  occhio se si vedono stampati.
- Vedove e orfane non si misurano ancora.

## Decisioni proposte

- **D1. Dati una volta sola.** La creatura diventa un dato con uno schema, come
  già le schede dei PG in `PG/schede/*.yaml`. Lo schema copre 3.5 e PF1e
  (BMC/DMC, Percezione), capacità, incantesimi, tattiche, fonte e marcatori di
  canone. Le righe leggibili si generano dal dato.
- **D2. Un layout, tre uscite.** Il markdown diventa una rappresentazione
  intermedia di elementi tipizzati. I tre renderer partono da quella. Colori,
  caratteri e misure stanno in un solo file di token letto da Typst e dal CSS.
- **D3. Varianti di layout misurate.** La pipeline scarta le varianti con
  errori misurabili. Fra quelle senza errori sceglie il DM alla cieca, come per
  la prosa.
- **D4. Un registro.** Ogni booklet ha i suoi tetti di stampa in git, che
  scendono soltanto. ✅ attuato con `docs/audit/stampa-booklet.json`.

## Fase 1 — Audit

- [x] **A1** I riferimenti: gli AP 3.5 e PF1e più premiati e più citati per
  l'impaginazione, e 15 criteri misurabili (C1-C15). Ricerca nella cartella
  condivisa `standard-stampa/RIFERIMENTI-AP.md`; Reddit e archive.org erano
  chiusi dal proxy.
- [x] **A2** La prima misura di stampa dei 17 booklet, in CI con i tetti.
- [ ] **A3** Il confronto con 4-5 pagine per titolo degli AP di riferimento
  (anteprime ufficiali, web enhancement, pagine del DM): stessa misura, fuori
  dal repo.
- [ ] **A4** Il censimento degli elementi di layout nei tre renderer e delle
  forme dei dati (Bestiario, master, PG, Drappo PF1e).

## Fase 2 — Implementazione, a PR piccole

- [ ] **I1** File dei token di stile, letto da Typst e dal CSS. La misura deve
  restare uguale.
- [ ] **I2** Le etichette delle mappe non scendono sotto il corpo minimo: la
  scala della figura decide la dimensione delle etichette nel renderer.
- [ ] **I3** Il riquadro che si spezza ripete la testata («segue»), oppure
  passa intero alla colonna dopo quando è più corto di una colonna.
- [ ] **I4** Schema della creatura e generatore delle righe leggibili.
  Migrazione a lotti: ARC-07 e il Bestiario, poi il resto.
- [ ] **I5** Rappresentazione intermedia e renderer unici, un elemento alla
  volta, con il confronto visivo delle pagine.
- [ ] **I6** Varianti di layout e scelta alla cieca del DM.
- [ ] **I7** Le schede PG del Drappo nello stesso tema.

## Fase 3 — Validazione

- [ ] **V1** Ogni PR mostra le misure prima e dopo; nessuna sale (la CI lo fa
  rispettare dal 2026-10-29).
- [ ] **V2** Confronto visivo pagina per pagina con la versione approvata.
- [ ] **V3** Una stampa di prova di un fascicolo su carta, guardata dal DM.

## Cosa manca e cosa si assume

- Dove stampa il DM: si assume casa o copisteria, A4, senza abbondanza, RGB.
  Una tipografia chiederebbe abbondanza di 3 mm, CMYK e PDF/X.
- Formati: si assume A4; A5 c'è già nel tema per i libretti.
- Le pagine degli AP per A3: dal DM o dalle fonti legali che si raggiungono
  dall'ambiente.
