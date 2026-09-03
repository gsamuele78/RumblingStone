# PIANO — Prosa che non sembri generata

> **Stato**: 🟡 **in corso** — lotti A, B e C chiusi (2026-09-03); resta D
> **Aperto**: 2026-09-03
> **Nasce da**: il DM porta due file esterni — la skill *the writing whip* e
> l'elenco *tropes.fyi* di Ossama Chaib — e chiede se convenga usarli per
> migliorare la prosa del repo e chiudere rilievi emersi al tavolo.
> **Risposta**: sì, ma su un bersaglio diverso da quello che sembrava.
> **ADR**: [ADR-0035](adr/ADR-0035-due-prose-due-norme.md)

---

## §1 · Il rilievo che torna

I giocatori hanno detto la stessa cosa due volte: **2026-07-31** e
**2026-09-02**, *«la prosa sembra tradotta dall'inglese»*. Fra le due date sta un
motore di stile da 1.900 righe. La norma quindi non manca; quello che mancava
era la misura, e per la prosa di gioco l'ha aggiunta `validate_prosa.py`
(lotto P della catena editoriale).

Questo piano risponde alla domanda successiva: **i tropi dell'elenco esterno
aggiungono qualcosa a quella norma?**

---

## §2 · Cosa dice la misura

Provati tutti sul repo prima di scriverne uno. I numeri decidono, non il
giudizio.

### Sul contenuto di gioco (255 file)

| Tropo provato | Occorrenze | Verdetto |
|---|---:|---|
| Nomi ornati (arazzo, panorama, ecosistema) | 64 | **64 falsi positivi**: `sinergia` è un termine di regole 3.5, `panorama` sta in un nome di file PNG, `ecosistema` è ecologia letterale in una prova di Natura |
| Rotazione dei sinonimi | 31 | falsi positivi: descrizioni di mappe (`stanza`/`camera` sono due posti) e un'iscrizione runica |
| Gerundio d'analisi | 135 | gerundi italiani normali (*irradiando un'aura*, *innescando la Sfida*); il tic vero compare **una volta** |
| Anafora ravvicinata | 291 finestre | un file di tattiche in inglese e un'etichetta `**Costo**` ripetuta |
| Autocitazione | 2.149 candidati | termini di dominio ripetuti (`illithid`, `oscurità`) |

Nessuno di questi regge come controllo automatico. Metà dell'elenco esterno,
inoltre, era **già coperta** da `italiano-nativo.md` §9: antitesi, trattino
lungo, tricolon, chiusura a effetto, maiuscole di portento.

### Sui documenti del repo (177 file, 32.566 righe)

Contando la sola prosa — fuori tabelle, codice, titoli e citazioni:

| Tic | Occorrenze | Densità |
|---|---:|---|
| Trattino lungo | 2.080 | 92 ogni 1.000 righe · mediana 82 · quartile alto 118 |
| Numero annunciato prima dell'elenco | 138 | `AGENTS.md` a 315/1000, `plans/INDEX.md` a 831/1000 |
| Antitesi «non X: è Y» | 58 | |

Qui il segnale c'è, è denso, ed è quasi tutto scritto da un agente.

---

## §3 · La conclusione che la misura impone

**I tropi non si trapiantano da una lingua all'altra né da un genere all'altro.**

Tre di quelli dell'elenco sono **attivamente sbagliati** per la narrativa: la
frase breve isolata è legittima in un read-aloud, l'apertura *«immagina di…»* è
letteralmente cosa fa un box in seconda persona, e il tricolon è uno strumento
retorico vero. Applicarli alla prosa di gioco la peggiorerebbe.

E uno è un tell **solo in inglese**: le intestazioni con parola interrogativa. In
italiano «Come si usa» è il titolo giusto per la sezione che spiega come si usa.

**Ma una prescrizione e un gate non sono la stessa cosa**, ed è l'errore che
questo piano ha commesso a metà strada: i quattro tic immisurabili erano stati
lasciati cadere insieme alle regole scartate dal validatore. Un occhio umano vede
la rotazione dei sinonimi che una regex non trova. Vanno **scritti**, non
**contati**.

---

## §4 · I lotti

### ✅ Lotto A — La skill per i documenti del repo
`skills/rumblingstone-prosa-documenti`. Copre guide, ADR, piani, ricerche,
skill, README, corpi delle PR e messaggi di commit. Porta i numeri misurati, i
sei tic che contano lì, e l'elenco esplicito di **cosa non importare
dall'inglese** con la misura accanto.
**Accettazione**: la skill dichiara il proprio perimetro e il confine con la
prosa di gioco; `validate_skills` verde.

**✅ Chiuso 2026-09-03.**

### ✅ Lotto B — I quattro tic che una macchina non trova
`italiano-nativo.md` §9.2-bis: rotazione dei sinonimi, autocitazione, anafora
ravvicinata, gerundio d'analisi. Ognuno con **la ragione per cui non è
misurabile** accanto all'antidoto, così nessuno prova a metterli in un gate fra
sei mesi.
**Accettazione**: i quattro tic sono scritti con esempio italiano e antidoto; la
sezione dichiara di essere l'unica parte di §9 che dipende da un occhio.

**✅ Chiuso 2026-09-03.**

### ✅ Lotto C — La misura sui documenti
`validate_prosa.py --documenti`: densità del trattino, conteggio annunciato,
antitesi. Non bloccante, come `validate_lingua`. Soglie tarate sulla
distribuzione reale.
**Accettazione**: il rilievo copre circa un terzo dei documenti, non tutti — un
rilievo che compare ovunque non lo legge nessuno. 18 test, e le quattro soglie
**fissate da una mutazione**.

**✅ Chiuso 2026-09-03.** Risultato: 54 rilievi su 154 documenti.

⚠️ Due difetti nei test, trovati mutando il validatore e non rileggendolo:
- il caso «sotto soglia» usava cinque trattini, che stanno anche sotto il
  **minimo di dieci occorrenze**: era quello a tenerlo quieto, e abbassare la
  soglia da 150 a 5 non lo faceva cadere;
- il caso «poche occorrenze» stava sotto entrambe le condizioni, quindi azzerare
  il minimo non lo faceva cadere. Ora usa otto trattini su cinquanta righe:
  sopra la densità, sotto il minimo.

### ⬜ Lotto D — Ripulire i documenti peggiori
I 54 rilievi aperti. `plans/INDEX.md` a 831 trattini ogni mille righe,
`AGENTS.md` a 315, `PIANO-CHIUSURA-CATENA-EDITORIALE.md` con 144 trattini e
undici conteggi annunciati.
**Accettazione**: i dieci file peggiori sotto la soglia; la mediana del repo
scende sotto 82/1000. ⚠️ **Da fare a mano**: una sostituzione automatica del
trattone produce punteggiatura sbagliata, perché il segno giusto (due punti,
punto e virgola, virgola, niente) dipende dalla frase.

---

## §5 · Da dove si comincia, in una chat nuova

```bash
python3 scripts/validate_prosa.py --documenti           # i 54 rilievi aperti
python3 scripts/validate_prosa.py --documenti plans/INDEX.md
python3 -m pytest scripts/tests/test_prosa_documenti.py -q
```

**L'ordine**: partire dai file che si leggono di più — `README.md`, `AGENTS.md`,
`plans/INDEX.md` — invece che dai piani vecchi, che nessuno riapre.

**Il metodo**: sostituire il trattone frase per frase. Nella maggior parte dei
casi il segno giusto è **due punti** (quando la seconda metà spiega la prima) o
**niente** (quando l'inciso si può togliere). Se la frase perde senso togliendo
l'inciso, l'inciso era il punto e va promosso a frase.

**Cosa NON fare**: `sed` sul trattone. La punteggiatura non è sostituibile in
blocco, e il risultato sarebbe peggiore del difetto.
