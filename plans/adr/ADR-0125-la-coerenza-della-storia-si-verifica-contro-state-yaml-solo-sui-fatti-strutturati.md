# ADR-0125 — La coerenza della storia si verifica contro state.yaml, e solo sui fatti che state.yaml ha come campi

**Stato**: proposta (2026-11-12)
**Data**: 2026-11-12
**Decisione-fonte**: il DM (Jfs), 2026-11-11, nel thread della #378: *«L'idea che ha dato inizio al thread ha senso applicarla per la parte di generazione e coerenza della storia?»*; poi la card «Sì, thread separato».
**Rapporti**: applica alla storia il pattern di ADR-0124 (regola, atteso, ha, `file:riga`; PR #378, ancora aperta); si appoggia ad [ADR-0050](ADR-0050-stato-di-campagna-dati-e-prosa.md) (`state.yaml` è il master dei fatti) e ad [ADR-0067](ADR-0067-il-confine-dichiarato-fra-codice-e-llm.md). Misure in [plans/esperimenti/coerenza-storia-2026-11-12/ESITO.md](../esperimenti/coerenza-storia-2026-11-12/ESITO.md).

## Contesto

Per la storia c'erano già due controlli deterministici. `coerenza_campagna
fatti` confronta la prosa con la prosa (due valori diversi per la stessa
entità) e non sa quale è giusto. `validate_state` controlla `state.yaml` ma
non legge la prosa. Mancava il pezzo in mezzo: la prosa contro il canone
strutturato, con un valore atteso da rimandare a chi scrive.

Banco: 35 incoerenze di storia già trovate e corrette nel progetto, un
prototipo con sette regole, il replay sui commit prima delle correzioni, 37
mutanti, la lettura di ogni rilievo su main.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Regole Python con àncora su `state.yaml`, solo sui campi che ci sono** (scelta) | dice `atteso`; 18 mutanti piani su 19; ha trovato su main un residuo di 4 mesi (Day 40 nel playbook) che nessun cancello vedeva | aggiunge 4 difetti storici su 35; 1 parafrasi su 18; precisione 7 su 13 su main |
| Strutturare altri fatti in `state.yaml` (numeri delle armate, anni del viaggio, «chi sa cosa» con il tempo) per coprire i K2 | 8 difetti storici in più diventerebbero deterministici | è canone nuovo: il tempo di §4 e i numeri di §2 li decide il DM, non un lotto d'infrastruttura (R7) |
| Prolog o clingo sul grafo degli eventi | ricorsione e regole temporali dichiarative | nessuna delle 35 incoerenze chiedeva una regola ricorsiva o temporale; §4 non ha il tempo, quindi la condizione di ADR-0124 per riaprirli non c'è |
| NLI o giudice LLM sulla prosa | legge le parafrasi | NLI già misurata e scartata (28 delle prime 30 sono rumore); un giudice LLM non è deterministico e va contro ADR-0067 |

## Decisione

1. **Per la storia vale il pattern di ADR-0124**: ogni verificatore che un
   LLM chiama restituisce `regola`, `atteso`, `ha`, `file`, `riga`. L'atteso
   viene da `campaign/state.yaml`, mai da un altro file di prosa.
2. **Si verificano solo i fatti che `state.yaml` ha già come campi.** Per gli
   altri il verificatore tace e lo dice (`non_verificabili`): oggi «chi sa
   cosa», 31 righe su 31 senza tempo.
3. **Nessun motore logico e nessun modello** per la coerenza della storia: la
   misura dice che il collo di bottiglia è leggere il fatto, non ragionarci.
4. **Il prototipo resta nel laboratorio** finché il DM non sceglie (card del
   2026-11-12). La proposta consigliata: le regole precise (S1 arrivo
   dell'orda, S5 portatore, S6 modifiche permanenti, S7 echi armati senza
   scena) entrano in `coerenza_campagna` come opzione `--state`, una norma e
   un rilevatore, in canale testing ([ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md)) e nel server MCP in sola
   lettura. S2, S3 e S4 restano fuori finché la precisione non passa.
5. **Non è un cancello.** Una frase d'autore sfugge quasi sempre, quindi il
   verde non vuol dire coerente. Il DM che legge resta il controllo vero
   (vedi la lettura scena per scena del 2026-11-02).

## Conseguenze

- Chi genera un master nuovo (un LLM via MCP, o il DM) riceve «atteso 42,
  trovato 40, `file:riga`» invece di «42 e 40 si contraddicono».
- Ogni nuovo campo strutturato di `state.yaml` diventa verificabile a costo
  basso, con una regola di poche righe.
- Si rinuncia a coprire le parafrasi e le incoerenze di struttura (generazioni
  di file, sequenze di eventi, fazioni fuse): 13 delle 35 storiche restano al
  giudizio.
- Se l'àncora è sbagliata il verificatore la difende (caso del pegno del
  Rituale 3, 2026-08-06).

**Da rivedere se**: il DM dà il tempo alle righe di §4 «chi sa cosa» (allora
le regole diventano temporali, e Prolog o clingo vanno rimisurati come dice
ADR-0124); oppure su 30 rilievi letti in canale testing la precisione delle
regole promosse scende sotto il 70%; oppure un master scritto via MCP mostra
che l'LLM non corregge con `atteso` meglio che con il solo messaggio.
