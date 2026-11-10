# ADR-0120 — La *d* eufonica si misura con una regex tarata su LanguageTool

**Stato**: proposta (2026-11-09)
**Data**: 2026-11-09
**Decisione-fonte**: il DM (Jfs), 2026-11-08, card D3 di PIANO-CODA-DEL-SECONDO-LETTORE: *ad* solo davanti alla stessa vocale, scritta in `editorial-standards.md` e misurata. Il 2026-11-09, Blocco 1 della roadmap: «fai tutte e 3 in ordine di importanza».
**Rapporti**: applica la regola del DM «si parte dallo standard di fatto, decide la misura». Segue [ADR-0079](ADR-0079-un-secondo-rilevatore-per-la-prosa.md) (LanguageTool come secondo lettore, l'apostrofo come regex del repo) e [ADR-0056](ADR-0056-una-norma-senza-misura-non-esiste.md) (una norma senza misura non esiste). Resta dentro [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md): nessuna dipendenza nuova.

## Contesto

Il repo scriveva *legato a Aegis Fang* accanto a *ad esempio* e *ad ogni*, senza
una norma. Il DM ha deciso la norma il 2026-11-08. Serve un rilevatore, e la
regola del progetto vuole lo standard di fatto prima di uno fatto in casa.

## Alternative considerate

1. **LanguageTool nel cancello di CI** (lo standard di fatto, regola ST_03_001).
   Scartata: vuole Java e un server locale di circa 200 MB in ogni giro di CI, e
   propone *od*, che la norma non vuole. Resta il riferimento contro cui si tara.
2. **Una regex del repo, tarata su LanguageTool** (scelta).
3. **Nessun rilevatore, solo la norma scritta**. Scartata da ADR-0056.

## Decisione

`validate_lingua.d_eufonica_righe` segnala come **errore**:
- *a* davanti ad *a*, *e* davanti ad *e* (anche accentate, anche con corsivo o
  grassetto in mezzo, anche quando la congiunzione chiude la riga);
- *ad* davanti a vocale diversa da *a*, *ed* davanti a vocale diversa da *e*,
  tranne *ad esempio* e *ad es.*, come in LanguageTool.

Fuori norma: *o/od* (arcaico) e le lettere-etichetta (*Unità A*, *§7.E*).

## Misura

`plans/esperimenti/d-eufonica-2026-11-09/RISULTATO.md`: sui 686 file di contenuto
la regex concorda con LanguageTool su 53 righe; le 28 solo di LanguageTool sono
*o o…* e lettere-etichetta (più due righe rientrate, corrette a mano); le 2 solo
della regex sono errori veri che LanguageTool perde. Dopo la correzione: 0
segnalazioni della regex, 26 di LanguageTool, tutte delle due classi escluse.

## Conseguenze

- Il cancello è a zero: una forma nuova fuori norma rompe `validate_lingua`.
- 58 righe corrette in 42 file, archivi compresi.
- Le righe rientrate come codice non si controllano: lo stesso limite degli
  altri controlli di `validate_lingua`.

**Da rivedere se**: LanguageTool trova sul repo una classe di forme che la regex
non vede (si rifà `misura.py` dopo un lotto grande di prosa nuova); il DM decide
di accettare *od*; la CI accetta un servizio Java, e allora il cancello passa a
LanguageTool.
