# ADR-0017 — Lo stato di campagna: dati validati per i fatti, markdown per la prosa

**Stato**: accettata
**Data**: 2026-08-05
**Decisione-fonte**: domanda DM 2026-08-05 — *«non sarebbe meglio trovare un
formato più opportuno e meno prono alle allucinazioni, JSON con manifest da
rispettare, mettendo i changelog in un altro file separato?»*
**Lotto**: G2-bis di [`PIANO-REVISIONE-GLOBALE-2026-08`](../PIANO-REVISIONE-GLOBALE-2026-08.md)

## Contesto

Il finding **C1** dell'audit 2026-08 non era un refuso: `campaign/state.md` §1
collocava i quattro PG **dopo** una battaglia mai giocata, con Hella già risorta
e Thorik che aveva già pagato il prezzo di quella resurrezione. Il lotto G1 l'ha
corretto **per convenzione** — colonne etichettate «Oggi al tavolo» / «Preparato»,
banner in testa alle sezioni.

Una convenzione, però, si può dimenticare. Era già successo: il pattern a due
tempi esisteva in §6 dal 2026-07-04, **DM-confermato**, e nessuno l'aveva esteso
a §1 per un mese. Nulla impediva che succedesse di nuovo alla prossima sessione.

Tre misure hanno inquadrato la decisione:

| Misura | Valore |
|---|---|
| `state.md` totale | 1677 righe |
| di cui §8 changelog | **1150 (68%)** |
| contenuto vivo | 527 righe — di cui **215 tabellari**, **234 prosa e banner** |

## Alternative considerate

**A. Conversione integrale a dati** (la proposta letterale: tutto in JSON con
manifest). Scartata: il 44% del contenuto vivo è prosa — il ramo di Ushgar, il
Marchio di Varis, il Debito della Radice. In JSON diventano stringhe: si perde la
leggibilità al tavolo e **non si guadagna nulla contro le allucinazioni**, perché
uno schema vincola la forma e non la verità.

**B. Solo lo split del changelog**, formato invariato. Scartata come insufficiente:
risolve il 68% del *volume* e lo 0% del problema C1.

**C. Ibrido** — dati validati per i fatti tabellari, markdown per la prosa, vista
generata. **Scelta.**

**JSON o YAML?** YAML, per tre ragioni concrete: JSON **non ammette commenti**, e
questo file è fatto di annotazioni datate («DM clarified 2026-07-03»); YAML regge
le stringhe multilinea della prosa lunga; il repo ha già cinque file dati YAML e
un `load_yaml` stdlib. Lo schema si applica identico — si valida l'oggetto dopo
il parsing, come già si fa per le mappe.

## Decisione

**I fatti di canone tabellari vivono in `campaign/state.yaml`, validato da uno
schema. La prosa resta in `campaign/state.md`, scritta a mano. Le tabelle di
`state.md` sono generate dai dati. Lo storico sta in un file a parte.**

### 1. Il vincolo che conta

Nello schema, `oggi` e `preparato` sono **chiavi**, e `oggi` è **obbligatoria**.
Per gli archi, `tempo: giocato | in_corso | preparato` è obbligatorio.

> **Un fatto senza tempo dichiarato non è esprimibile.** Non è una linea guida da
> ricordare: è un file che non passa il gate.

È la differenza fra «ci siamo dimenticati di dire che quella riga era futura» e
«quella riga non poteva esistere».

### 2. Il limite, dichiarato

Uno schema vincola la **forma**, non la **verità**. Un agente può ancora scrivere
un fatto falso in un file perfettamente valido. Ciò che questo contratto rende
impossibile è più ristretto e più utile: scriverlo **senza dire a quale tempo
appartiene**. Chi si aspetta che lo schema impedisca le allucinazioni resterà
deluso; chi si aspetta che impedisca *quella specifica classe* di errore — quella
che è già costata un mese di canone ambiguo — sarà servito.

### 3. Un master, mai due

`state.yaml` è il master dei fatti di §0, §1, §6. Le tabelle corrispondenti in
`state.md` stanno fra marcatori `<!-- gen:state:NOME -->` e sono **rigenerate**
da `scripts/render_state.py`; `--check` è un gate CI.

Questo punto non è negoziabile ed è la ragione per cui il lotto è stato eseguito
tutto insieme: creare `state.yaml` **senza** il rendering avrebbe prodotto una
seconda fonte di verità, cioè esattamente il finding **C2** appena chiuso
(`state.md` e `campaign-history.md` che si dichiaravano entrambi sorgente unica).

### 4. Cosa NON diventa dati

§5 (promesse e debiti), §7 (fili narrativi ed Echo Ledger), §2 (orda e orologi,
per ora), §3 (clock dei villain, per ora) e tutti i banner restano markdown a
mano. La migrazione è **incrementale**: §3 è il candidato successivo perché è
tabellare e porta clock numerici; §2 e §4 seguono solo se il beneficio supera il
costo di renderizzarne la prosa.

### 5. `[INFERRED]` come record

Non più una stringa da cercare col grep, ma una voce con `id`, `dove`, `domanda`,
`a_chi`, `aperto_dal`. La domanda è formulata perché il DM possa rispondere senza
rileggere i file. Questo cambia il progetto del lotto G4: l'inventario si legge
dai dati, non si estrae dal markdown.

### 6. Rapporto con ADR-0003 e ADR-0007

- **ADR-0003** («markdown master, layout generati») **non è contraddetto ma
  ristretto**: vale per i *documenti* — moduli, booklet, handout, dove il
  markdown è la sorgente e l'impaginazione l'artefatto. Per lo *stato*, che è
  una base di fatti e non un documento, la direzione si inverte: dati master,
  markdown vista. Il criterio è: **se una cosa si valida, è dato; se si legge, è
  documento.**
- **ADR-0007** (triplo vincolo sulle scritture di canone) resta pieno. Le regioni
  `gen:state:` sono generate da dati che un umano ha scritto e una PR ha
  rivisto; non sono scritture automatiche di canone. `state_apply.py` e le sue
  regioni `auto:` non sono toccati.

## Conseguenze

**Positive**

- La classe di errore C1 diventa strutturalmente impossibile.
- `state.md` passa da **1677 a 546 righe**: quello che il DM apre a sessione è
  ora quasi solo ciò che gli serve.
- L'inventario `[INFERRED]` è gratuito e porta con sé le domande.
- Due gate nuovi (`validate_state`, `render_state --check`), entrambi bloccanti.

**Negative, dichiarate**

- Una dipendenza in più sul percorso critico: `pyyaml` (già usato da
  `validate_skills`, già installato in CI, con lo stesso fallback a exit 2).
- Chi modifica i fatti deve toccare `state.yaml` e rigenerare: un passaggio in
  più rispetto a editare il markdown. Il banner nelle regioni lo dice a chi ci
  finisce sopra.
- Il repo ha ora **due formati** per lo stato. Mitigazione: il confine è scritto
  qui e ripetuto in testa a `state.yaml` — si valida → dato; si legge → documento.

## Verifica

```bash
python3 scripts/validate_state.py          # schema + 5 regole di coerenza
python3 scripts/render_state.py --check     # state.md in sync con state.yaml
```
