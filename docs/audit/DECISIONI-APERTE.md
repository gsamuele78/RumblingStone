<!-- Vista operativa delle decisioni pendenti. Aggiornare quando una si chiude. -->
# Decisioni aperte — cosa serve al DM per far avanzare il piano

**Aggiornato:** 2026-08-06 · **Piano:** [`PIANO-REVISIONE-GLOBALE-2026-08`](../../plans/PIANO-REVISIONE-GLOBALE-2026-08.md)

> **A cosa serve questo file.** Ogni lotto fermo lo è per una ragione precisa, e
> quasi sempre è **una domanda al DM**, non lavoro mancante. Qui stanno tutte,
> con il tempo che costano e cosa sbloccano — così si decide in blocco invece
> che una alla volta a ogni giro.
>
> Le domande di **canone** vivono anche come record in
> [`campaign/state.yaml`](../../campaign/state.yaml) (`inferred:`), dove
> `validate_state.py --verbose` le elenca con la domanda già formulata.

---

## A. Decisioni che sbloccano lotti

### 1. I 13 asset del `PALIO-BOOKLET` — 2 minuti, sblocca **G3**

`09_…/homebrew/PALIO-BOOKLET.hb.md` referenzia **8 stemmi `.svg`**, **4 mappe** e
**1 panorama `.png`** che non esistono. Il booklet si genera, ma esce con 13
immagini rotte.

| Opzione | Conseguenza |
|---|---|
| **Togli i riferimenti** (sostituiti da segnaposto testuali) | il booklet torna pulito subito; se un giorno produci l'arte, si rimette |
| Lasciali marcati «da produrre» | onesto, ma il deliverable resta rotto e il gate nasce con 13 eccezioni |
| Segnaposto SVG generati | booklet completo subito, ma sono disegni provvisori, non arte tua |

### 2. Il PRD: chi è il destinatario? — 30-45 min, **è il collo di bottiglia**

Ha già bloccato **due** decisioni architetturali. Tre risposte possibili, con
conseguenze molto diverse:

| Risposta | Conseguenze a valle |
|---|---|
| **Solo il mio tavolo** | branch-per-gruppo basterebbe → **ADR-0018 va ridimensionato**; PRD breve; bonifica IP del Palio non serve |
| **Ereditabile da un DM terzo** (gratis) | `groups/` è obbligato; il contratto di tavolo serve davvero; è ciò che già promettono `DM-QUICKSTART-NUOVI-DM.md` e `new-campaign-group.sh` |
| **Verso una pubblicazione** | bonifica IP del Palio **obbligatoria**; serve la matrice delle edizioni; G7 alza l'asticella |

Sblocca: **G5**, e a cascata G7 (prosa), G9 (CD), la bonifica Palio ferma da
luglio, e la conferma o il ridimensionamento di ADR-0018.

### 3. Il contratto di tavolo — 30 min + una conversazione coi giocatori, sblocca **G6**

Confini di contenuto dichiarati e strumento di stop condiviso. **Lo scrivi tu**:
è l'unico documento del repo il cui contenuto non è deducibile dai file.

### 4. Prima sessione reale con `dm.py session end` — 20 min al tavolo, sblocca **G10**

Accende la pipeline ADR-0007, costruita, testata e mai usata.

### 5. Intervista di ricostruzione — ~30 min × 7 archi, sblocca **G11**

Date, presenti, XP, bottino, tre decisioni chiave per arco. **Nessun agente può
sbloccarla**: quei dati non stanno nei file.

---

## B. Domande di canone — cinque, tutte veloci

| ID | Domanda | Impatto se non risolta |
|---|---|---|
| **INF-001** | Il **−2 COS di Thorik** è il prezzo della resurrezione (non giocata) o residuo della morte all'Arco 00? | la scheda di Thorik resta ambigua sul malus |
| **INF-002** | **Giorno di Marcia 19 o ~15?** §2.1 dice 19, l'orologio Hammerfist a 3g 16h implica ~15 | sposta i numeri di §2.4 e **la finestra quest di Arco 09** |
| **INF-003** | La classificazione `tempo` di §4 — **31 righe assegnate a macchina** — regge? | i PNG potrebbero rivelare cose che non hanno imparato |
| **INF-004** | Ghaurush, Zin'thara e Ushgar «sanno dei **Custodi Eterni**», ma il titolo si conferisce nell'Arco 08 | tre righe di canone del 2026-08-05 sono anacronistiche |
| **INF-005** | I clock di quei tre **stanno già avanzando**, o partono con l'Arco 09? | cambia cosa succede fra una sessione e l'altra |

`INF-004` è l'unica che segnala un'**incoerenza vera** già nel canone approvato:
le altre quattro sono conferme.

---

## C. Ferme da luglio, indipendenti dall'audit

- **PR #42** — Ultra-Clear P4 Piano Terra: aperta e non mergiata.
- **PR #46** — tavole Channathgate: aperta e non mergiata.

Finché restano aperte, `plans/INDEX.md` le elenca come pendenti e l'indice non
dice il vero. Vanno mergiate o chiuse.

---

## Cosa NON aspetta nessuna decisione

Questi lotti si possono fare adesso, e infatti si stanno facendo:

- **G3** — validatore link + i **4 path `/home/jfs/…`** committati + i link rotti <!-- validate-links: ignore -->
  non-Palio. *(Solo la sorte dei 13 asset attende la decisione A1.)*
- **G4** — inventario e ratchet degli `[INFERRED]`, ora leggibili dai dati
  tipizzati invece che col grep.
- **G8** — igiene Python e CI hardening.
