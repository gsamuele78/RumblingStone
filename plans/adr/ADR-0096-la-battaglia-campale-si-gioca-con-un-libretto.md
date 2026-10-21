# ADR-0096 — La battaglia campale di Hammerfist si gioca con un libretto

**Stato**: proposta
**Data**: 2026-10-21
**Decisione-fonte**: richiesta del DM del 2026-10-21 nel thread di PIANO-MASTER-DEF («un libretto comune di poche pagine sia per i giocatori e i dm … ogni pregen avrà il suo gruppo di armata se possibile da gestire»); simulazioni in `plans/esperimenti/battaglia-campale-2026-10-21/`

## Contesto

Con D4 il flashback dei pregenerati resta prima di Hammerfist. Il DM vuole che
i giocatori provino qualcosa di diverso: l'assedio come battaglia campale, con
regole semplici e lo stesso libretto per giocatori e DM. Il sistema canonico
(`mass_combat_guide_Dm.md`, `ARC08-02` §4) fa tirare l'attacco dell'orda al
DM, e non dice cosa fa un eroe dentro la battaglia di massa. Il Fronte di
ARC-09 (D13) è invece un contatore nascosto del DM, quindi Hammerfist è
l'unico posto in cui il tavolo muove le truppe.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| Libretto con il sistema canonico rovesciato: i giocatori tirano attacco e difesa, l'eroe ha quattro gesti | stesse probabilità del canonico; i dadi sono tutti in mano al tavolo; si può tarare con una simulazione | regole nuove da insegnare: serve una Sessione 0 |
| Sistema canonico così com'è | niente da scrivere | il DM tira metà dei dadi; l'eroe non ha un ruolo nella massa |
| Solo i pregen sulla mappa, la battaglia raccontata | nessuna regola nuova | non è quello che il DM ha chiesto; diventa il modo A del libretto |

## Decisione

L'assedio dei pregen si gioca con `ARC08-18-LIBRETTO-BATTAGLIA-CAMPALE.md`:
una tabella sola, tre ordini, quattro gesti dell'eroe, la pressione che apre
le brecce, tre modi di giocare (solo l'eroe, l'eroe con due reparti, il
capitano con tre). Il dado bianco della difesa è il tiro d'attacco dell'orda
rovesciato (d20 + DU contro 22 + AU), con la stessa probabilità.

Le sessioni diventano Sessione 0 (regole e battaglia di prova senza posta),
poi Sessione 1, 2 e 3a come nel master (`ARC08-10` §5.4-bis). Chi non vuole
un pregen gioca il capitano o l'orda (libretto §9). Ogni pregen ha una carta
dei poteri con i numeri già calcolati (`ARC08-15`, handout 1-4 bis). L'orda di default è quella feroce (+1 ad AU e DU sulla normale), con
una terza manopola terrificante, per la preferenza del DM per la versione
più forte.

## Conseguenze

- Nelle simulazioni (3.000 battaglie per variante) nessun ordine fisso
  vince: tenere sempre chiude i giorni 1-2 senza brecce il 9% delle volte,
  caricare sempre perde quasi tutti i reparti. Il gioco attento con l'orda
  feroce fa 70/21/8% sulla breccia e 74/18/9% sulle posizioni; l'orda
  terrificante scende a 45% e 37% di «pieno».
- Il modo C (tre reparti, l'eroe non tira) ferma la breccia quanto il modo B
  ma perde più reparti (58% «pieno» sulle posizioni contro 74%).
- Le letture a freddo di un giocatore e di un DM hanno trovato un errore di
  uno nel dado bianco; corretto nel libretto e nel simulatore, e i numeri qui
  sono quelli dopo la correzione.
- Le carte dei comandanti e la palla di fuoco non sono simulate e restano
  `[INFERRED]`.
- Le schede dei pregen negli handout 1-4 hanno numeri vecchi rispetto al
  Bestiario; il libretto usa quelli del Bestiario.
- Manca la prova al tavolo, che è il solo modo di sapere se è divertente.

**Da rivedere se**: alla Sessione 0 un round dura più di cinque minuti, o i
giocatori del modo B finiscono per scegliere sempre lo stesso ordine.
