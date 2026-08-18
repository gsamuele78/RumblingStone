# ADR-0021 — Le skill si caricano esplicitamente, e AGENTS.md dice quando

**Stato**: accettata *(richiesta del DM 2026-08-17)*
**Data**: 2026-08-18
**Decisione-fonte**: domanda del DM — *«perché non le hai caricate in automatico
le skill e gli altri tool disponibili? magari c'è bisogno di aggiornare AGENTS,
ADR o altro per permettere di scoprire le skill, gli script, le pipeline e i
validate?»*

## Contesto

[ADR-0008](ADR-0008-governance-set-skill-focalizzate.md) ha stabilito **quali**
skill esistono e come si governa il set. Non ha mai detto **quando un agente
deve caricarle** — e `AGENTS.md`, che è il primo file che ogni sessione legge,
affermava:

> *«AI agents that support SKILL.md will discover them automatically»*

**Non è vero.** Un agente vede i nomi in un indice; nessuno gliele carica, e
niente le fa scattare in base ai file che sta toccando. La frase descriveva
un'aspirazione come se fosse un meccanismo, ed è peggio di un silenzio: un
agente che la legge conclude — ragionevolmente — che il materiale è già in
memoria e che non c'è niente da invocare.

### Cosa è costato, misurato e non ipotizzato

Nella settimana del 2026-08-14/18, due sessioni hanno lavorato al modulo
`STANDALONE-Il-Drappo-di-Tarsilia` su due branch diversi. Nessuna delle due ha
invocato una skill. Esiti:

1. **Lo stesso tool scritto due volte.** `build_image_derivatives.py` (un ramo) e
   una ricetta Pillow dentro un README (l'altro) fanno la stessa cosa con
   tarature diverse. `scripts/README-automation.md` — la mappa dei tool — non
   era stata aperta da nessuno dei due.
2. **Dodici link rotti invisibili per giorni.** Un ramo puntava a derivate
   `web/*.jpg` che `.gitignore` escludeva. `validate_standalone.py` le avrebbe
   prese subito: quel ramo non aveva una PR, quindi la CI non è mai girata.
3. **Un audit meccanico saltato.** Le sei schede pregenerate sono state
   impaginate senza la passata 1 di `rumblingstone-playtest`. Fatta dopo, ha
   trovato **due numeri sbagliati** (un CMD e una CD) che erano lì da giorni,
   uno dei due a favore del giocatore — cioè del tipo che al tavolo nessuno
   segnala.
4. **Una regola verificata a memoria.** Il CMD è stato ricalcolato solo dopo
   aver caricato `pathfinder-1e-srd`. A memoria era giusto lo stesso, ma è
   fortuna, non metodo.

Nessuno di questi è un difetto di codice. Sono tutti difetti di **scoperta**.

## Decisione

**Il caricamento delle skill è esplicito e obbligatorio, e la regola di
instradamento vive in `AGENTS.md`** — il file che ogni agente legge per primo,
non in un documento che bisogna già sapere di dover cercare.

1. `AGENTS.md` §Skills perde la frase sulla scoperta automatica e guadagna una
   **tabella «se stai per fare X, carica Y»**, più il rimando obbligatorio a
   `scripts/README-automation.md` prima di scrivere un tool nuovo.
2. Ogni `SKILL.md` del repo porta in testa una riga **«Caricami quando…»**: la
   descrizione dice *di cosa parla*, quella riga dice *in che momento serve*.
3. La regola vale **prima** di scrivere, non dopo: una skill caricata a lavoro
   finito serve a scrivere il changelog, non a evitare l'errore.

### Cosa NON si fa

- **Nessun gate in CI.** «Hai caricato la skill giusta?» non è verificabile a
  macchina: non lascia traccia nei file. Un gate semantico che indovina sarebbe
  peggio del problema — e la stessa scelta è già scritta in
  `rumblingstone-plans` per il routing engine.
- **Niente auto-caricamento simulato** (uno script che stampa «carica X»): non
  cambia il comportamento di chi non legge, e aggiunge un pezzo da mantenere.

Il gate resta indiretto e reale: `check_plans_discipline.py` (ADR-0009) sui
file strutturali, `tools_manifest.py --check` (ADR-0012) sui tool orfani, i
`validate_*` sui contenuti. Questa decisione riduce la probabilità di sbagliare;
non promette di renderla zero, perché non può.

## Conseguenze

- **Più facile**: un agente nuovo apre `AGENTS.md`, trova la riga che
  corrisponde a quello che sta per fare, e carica. Costo: due minuti.
- **Più difficile**: la tabella va tenuta allineata quando nasce una skill. È lo
  stesso costo che ADR-0012 impone al manifest dei tool, e si accetta per lo
  stesso motivo.
- **Rinuncia dichiarata**: nulla impedisce a un agente di ignorare la tabella.
  Questa è governance documentale, non un blocco — e va detto, invece di
  lasciar credere che ora sia impossibile sbagliare.
- **Da rivisitare**: se una piattaforma introdurrà un caricamento davvero
  automatico e verificabile, la frase tolta da `AGENTS.md` tornerà vera e questo
  ADR si potrà chiudere.

## Copertura

- `AGENTS.md` §Skills — l'avvertenza e la tabella di instradamento
- `skills/*/SKILL.md` — la riga «Caricami quando…» in testa
- [ADR-0008](ADR-0008-governance-set-skill-focalizzate.md) — quali skill esistono
- [ADR-0012](ADR-0012-standard-ingegneria-tool-verificabile.md) — il manifest dei
  tool, che risolve lo stesso problema per gli script
- `scripts/README-automation.md` — la mappa da leggere prima di scriverne uno nuovo
