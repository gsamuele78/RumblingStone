# PIANO — Un generatore di creature e PNG dalle tabelle

> **Stato**: ⬜ proposto, non iniziato · **Aperto**: 2026-09-02
> **Nasce da**: domanda del DM — *«alla fine c'è un generatore di mostri e PNG,
> anche incantatori, fra i tool disponibili al DM, che usa quelle tabelle per
> generare le cose? ha senso creare un nuovo piano o è stato fatto?»*
> **Risposta**: **non è stato fatto.** `suggest_encounter` **pesca** dal catalogo
> (306 record esistenti); non costruisce niente di nuovo.
> **Precedenti da leggere prima**: [ADR-0021](adr/ADR-0021-statblocchi-machine-readable.md)
> · [ADR-0033](adr/ADR-0033-derivare-e-dichiararlo.md) · skill `dnd-35-srd`,
> `pathfinder-1e-srd`, `npc-villain-boosting`

---

## §1 · Perché questo è un problema DIVERSO da quello che è appena fallito

Va detto subito, perché il lotto H si è chiuso con una prova negativa e sarebbe
facile leggerla come un divieto.

Nel lotto H `derive_statblocks.py` ha provato a **ricavare i numeri da schede in
prosa già scritte**, e il collaudo li ha respinti quasi tutti. La causa è
strutturale: una scheda è un documento, non un dato, e un'espressione regolare ci
trova sempre qualcosa di plausibile — *«Esperto 2»* dove la riga diceva *«Esperto
2 / Acolita 6»*, i dadi di un morso scambiati per dadi vita.

**Generare è la direzione opposta, e non ha quel problema.** Non c'è prosa da
interpretare: si parte da **quello che il DM dichiara** — GS, ruolo, tipo,
taglia — e le tabelle producono i numeri. È esattamente l'uso per cui quelle
tabelle esistono. Un generatore non può leggere male una scheda perché **non
legge nessuna scheda**.

Il rischio qui è un altro, ed è il vero criterio di progetto: **produrre creature
generiche che si assomigliano tutte.** Un mostro che rispetta perfettamente la
riga della tabella e non ha niente di suo è peggio di nessun mostro: al tavolo si
gioca come tutti gli altri.

---

## §2 · Cosa esiste già (per non rifarlo)

| Strumento | Cosa fa | Cosa NON fa |
|---|---|---|
| `suggest_encounter.py` | sceglie 3-5 combinazioni per un EL bersaglio dal catalogo, per fazione/ambiente, con seed | non crea creature |
| `build_monster_catalog.py` | indicizza i 306 statblocchi esistenti | non genera |
| `derive_statblocks.py` | deriva CA/pf/TS **da una scheda esistente**; scrive i soli TS | non parte da zero |
| skill `npc-villain-boosting` | il **quadro decisionale** per potenziare | è dottrina, non un tool |
| `scripts/schemas/statblock.schema.json` | il **contratto** del blocco | — |

Il pezzo che manca è uno solo: **da (GS + ruolo + tipo) a un blocco completo.**

---

## §3 · Le tabelle, e quali sono davvero verificate

⚠️ **Prima cosa da fare, prima di scrivere codice.** In `derive_statblocks.py`
la tabella per GS ha venti righe, ma **solo otto sono verificate contro la fonte**
(GS 8 e 10-16); GS 1-7 e 17-20 le ho interpolate io, e il campo
`PER_GS_VERIFICATE` lo dichiara. Un generatore che le usasse come bersaglio
propagherebbe numeri non controllati su ogni creatura che produce.

**Lotto 0 del piano: verificare le dodici righe mancanti** contro la fonte
(`pathfinder-1e-srd/references/monster-advancement.md`, e la sua fonte a monte),
oppure dichiararle non disponibili e rifiutarsi di generare a quei GS.

Serve inoltre quello che oggi **non abbiamo in casa**:

- la **riga per gli incantatori** (livello dell'incantatore e CD primaria per GS)
  — il DM la segnala come esistente, va procurata e verificata;
- le **statistiche per GS dei PNG**, distinte da quelle dei mostri;
- ⚠️ e una **taratura 3.5**: le righe PF1e sono più dure a parità di GS, e questa
  campagna gira su 3.5. Generare sui numeri PF1e produrrebbe mostri
  sistematicamente più cattivi di quanto il GS promette. Va deciso e scritto in
  un ADR: o si tara, o si dichiara che il generatore produce «GS PF1e».

---

## §4 · I lotti

### ⬜ Lotto A — Le tabelle, verificate e in un posto solo
Le righe per GS (mostri · PNG · incantatori) diventano un dato del repo, con la
**provenienza per riga** e il segno di quali sono verificate. Nessuna riga
inventata in silenzio. **Accettazione**: ogni riga cita la sua fonte; un test
confronta la tabella con le righe d'ancora della skill.

### ⬜ Lotto B — Il generatore, per creature non incantatrici
`scripts/genera_creatura.py`: da `--gs`, `--tipo`, `--taglia`, `--ruolo`
(bruto · schermagliatore · tiratore · comandante) a un blocco completo, con
`--seed` per la riproducibilità (come `suggest_encounter`).
**Accettazione**: il risultato **supera il collaudo sul GS** — cioè la stessa
guardia che nel lotto H respingeva tutto, qui deve passare, e se non passa il
generatore è sbagliato. Test su tutti i GS disponibili e tutti i ruoli.

### ⬜ Lotto C — I PNG con livelli di classe
Razza + classi (comprese le classi PNG del SRD) + matrice elite/standard +
equipaggiamento per livello. **Accettazione**: un PNG generato e uno scritto a
mano dallo stesso profilo stanno nella stessa fascia.

### ⬜ Lotto D — Gli incantatori
La parte che il DM ha chiesto per nome e che è la più delicata: livello
dell'incantatore, incantesimi al giorno dalle tabelle di classe SRD, CD primaria
dal GS, e **la scelta degli incantesimi** — che è dove un generatore diventa
banale se la fa a caso. Proposta: non estrarre a sorte da tutto il SRD, ma da
**liste per ruolo** (controllore · artigliere · sostegno) scritte a mano una
volta. **Accettazione**: le CD stanno sulla riga del GS; nessun incantesimo fuori
lista di livello.

### ⬜ Lotto E — Il carattere, cioè la ragione per cui non è banale
Una creatura generata esce con **una cosa sua**: un talento firma, una tattica in
una riga, una debolezza sfruttabile. Prese da tabelle scritte a mano per ruolo,
non generate. ⚠️ **È questo lotto che decide se il tool serve**: senza, produce
mostri intercambiabili, e un mostro intercambiabile il DM se lo scrive prima da
solo che a leggerlo.

### ⬜ Lotto F — Dove finisce l'output
**Non scrive mai dentro `Bestiario/`.** Stampa il blocco, o scrive in una
cartella di lavoro, e il DM decide se e come farlo entrare — lo stesso confine di
ADR-0033. Con `fonte: generato-SRD — <parametri e conto>`, così fra sei mesi si
sa da dove viene e lo si rifà uguale.

---

## §5 · Le domande da porre al DM prima di cominciare

1. **La taratura**: 3.5 o PF1e? (vedi §3 — cambia ogni numero prodotto)
2. **I ruoli**: quali servono davvero al tuo tavolo? Bruto, schermagliatore,
   tiratore, comandante, controllore, artigliere — o meno?
3. **Il carattere (lotto E)**: le tabelle di talenti/tattiche firma le scrivi tu
   o le propongo io per la tua conferma?
4. **Dove finisce**: stampa a schermo, o un file in una cartella di lavoro?

---

## §6 · Quando NON usarlo

Va scritto adesso, o il tool diventa la scorciatoia per tutto:

- se nel catalogo c'è già qualcosa di simile → **potenzialo** (`npc-villain-boosting`);
- se la creatura ha un ruolo nella trama → **si scrive a mano**, il generatore dà
  al massimo l'ossatura;
- se serve per **un incontro di passaggio** → è esattamente il suo caso.
