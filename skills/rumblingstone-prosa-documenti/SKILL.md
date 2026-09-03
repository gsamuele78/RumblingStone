---
name: rumblingstone-prosa-documenti
description: >
  Come si scrivono i DOCUMENTI di questo repo — guide, ADR, piani, ricerche,
  skill, README, corpi delle PR e messaggi di commit — perché non suonino
  generati a macchina. Copre i tic di composizione dell'IA (trattino lungo come
  respiro, numero annunciato prima dell'elenco, antitesi «non X: è Y», riassunti
  a ogni livello, preamboli, chiusura che riporta alla domanda) e dice quali
  tropi inglesi NON vanno importati in italiano. Use WHENEVER si scrive o si
  revisiona un documento del repo: "scrivi la guida", "apri un piano", "scrivi
  l'ADR", "aggiorna il README", "corpo della PR", "messaggio di commit",
  "documenta questo", "rivedi il documento", "questo testo sembra scritto
  dall'IA". ⚠️ NON è per la prosa di gioco: read-aloud, handout, dialoghi ed
  echi seguono `rumblingstone-narrative-style` e `italiano-nativo.md`, dove
  alcune di queste regole sarebbero sbagliate.
---

# La prosa dei documenti del repo

I documenti di questo repo si riconoscono come generati a macchina, e si
riconoscono da poche abitudini che si ripetono. Non dai contenuti.

Misurato sui 177 documenti in `docs/`, `plans/`, `skills/` e nella radice
(32.566 righe, contando la sola prosa: fuori tabelle, codice, titoli e
citazioni):

| Tic | Quante volte | Densità |
|---|---:|---|
| Trattino lungo | 2.080 | 92 ogni 1.000 righe di prosa |
| Numero annunciato prima dell'elenco | 138 | — |
| Antitesi «non X: è Y» | 58 | — |

Il trattino è il primo tell. La mediana dei documenti sta a 82 ogni mille righe;
`AGENTS.md` è a 315 e `plans/INDEX.md` a 831.

Si misura con:

```bash
python3 scripts/validate_prosa.py --documenti          # tutti
python3 scripts/validate_prosa.py --documenti FILE     # solo questo
```

Non blocca la CI. La norma è questo file; il comando dice se il testo la rispetta.

## I tic che contano qui

### Il trattino lungo usato come respiro

In inglese l'em dash è un segno di punteggiatura corrente. In italiano il
trattone è raro, e usarlo per ogni pausa drammatica è il modo più veloce per
suonare tradotti.

> «la regola — e questa è la parte che nessuno dice — vale sempre»

Antidoto: due punti, punto e virgola, una virgola, oppure niente. Se in un
paragrafo ne servono due, il paragrafo va riscritto.

### Il numero annunciato prima dell'elenco

> «Cambiano tre cose.» · «per due ragioni» · «Tre punti, e sono tutti misurati.»

L'elenco che segue rende il numero superfluo, e sbagliarlo è imbarazzante.
Scrivi l'elenco. Se il numero conta davvero (un budget, un conteggio di file),
tienilo: lì è un dato.

### L'antitesi «non X: è Y»

Vale una volta a documento, dove vuoi il colpo più forte. Alla terza il lettore
sente il telaio. Togliere la prima metà quasi sempre migliora la frase: «c'è
peso» dice più di «non c'è collera: c'è peso».

### Il preambolo che annuncia invece di dire

> «Due vincoli guidano il progetto.» · «Vale la pena chiarire una cosa.»

Di' la cosa. Il lettore capisce da solo che ne stai dicendo una.

### Il riassunto a ogni livello

Un documento che apre dicendo cosa dirà, ripete a ogni sezione cosa ha detto e
chiude riassumendo tutto ha scritto tre volte lo stesso testo. Le sezioni non
hanno bisogno di un recap; il documento non ha bisogno di «In conclusione».

### La chiusura che riporta alla domanda

> «Quindi, per rispondere: sì, il gate funziona.»

La risposta era già data. Fermarsi.

### La narrazione del proprio ragionamento

> «Voglio essere preciso su cosa cambia qui.» · «Prima di rispondere, misuro.»

Nel documento finale non ci va: è residuo del ragionamento. In una chat va
benissimo dire cosa stai per fare; in un ADR no.

## Quello che invece va tenuto

Questo repo ha una convenzione che somiglia a un tic e non lo è: **ogni
documento dice perché una decisione è stata presa e cosa è costata**. Gli ADR
hanno una sezione «Le conseguenze» con «quello che si paga»; i piani hanno i
criteri d'accettazione. Non è verbosità: è la cosa che rende il repo leggibile
fra sei mesi.

E i **numeri misurati** vanno sempre citati. «Sette implementazioni di `slug`, e
una butta via le lettere accentate» vale più di «c'è della duplicazione».

## I tropi inglesi che NON vanno importati

Provati sul repo e scartati, con la misura accanto:

- **Nomi ornati** (arazzo, panorama, ecosistema): 64 occorrenze, 64 falsi
  positivi. `sinergia` è un termine di regole 3.5, `panorama` sta dentro il nome
  di un file PNG, `ecosistema` è ecologia letterale.
- **Intestazioni con parola interrogativa**: è un tell dell'inglese. In italiano
  «Come si usa» è il titolo giusto per la sezione che spiega come si usa.
- **Frasi brevi come paragrafo**: in inglese è un tic; in italiano tecnico una
  frase secca dopo un periodo lungo è ritmo normale. Il problema è farne dieci
  di fila.
- **Bullet che aprono in grassetto**: 1.312 nel repo, e per lo più sono elenchi
  di definizioni, dove il grassetto è il termine definito. Diventa un tic quando
  *ogni* bullet lo fa, comprese le frasi che non definiscono niente.
- **Gerundio d'analisi**, **rotazione dei sinonimi**, **anafora**: cercati e non
  trovati. I 135 gerundi del repo sono italiano normale.

## Prima di consegnare un documento

1. `python3 scripts/validate_prosa.py --documenti <file>`
2. Rileggi solo la **prima frase di ogni sezione**. Se tre su cinque annunciano
   quello che segue invece di dirlo, il documento è da rivedere.
3. Togli l'ultima frase di ogni sezione e rileggi. Se non manca niente, restava
   di troppo.

## Chi fa cosa

| Cosa | Dove |
|---|---|
| Prosa di gioco (read-aloud, handout, echi, dialoghi) | `rumblingstone-narrative-style` → `italiano-nativo.md` |
| Documenti del repo (guide, ADR, piani, skill, PR) | questo file |
| Struttura e disciplina dei piani | `rumblingstone-plans` |
| Termini banditi nei master di modulo | `validate_modules.py` |
