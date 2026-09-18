# 📐 PIANO — Portare il mestiere dei banchi nelle parti scritte prima

> **Cos'è**: la risposta misurata alla domanda del DM del 2026-09-18 — *«c'è un
> modo di misurare che il nuovo stile a 9 pilastri (e i vari stili) e le altre
> cose inserite sono presenti in quella parte citata, in che percentuale e se
> può essere migliorabile e dove»* — e il piano in tre fasi per colmare il
> divario, **arco per arco**, usando come banchi il **Palio** e l'**Abbazia**.
>
> **Strumento**: `python3 scripts/misura_craft.py [--densita|--copertura|--mancanti]`
> **Decisione**: [ADR-0055](adr/ADR-0055-il-mestiere-si-misura-per-congegni.md)

---

## 0 · Informazioni mancanti e assunzioni dichiarate

**Quello che non so, e che cambia il piano se la risposta è diversa:**

1. **Quali parti sono ancora riscrivibili.** DEF-1 è 🟡 *in corso al tavolo*. Un
   documento che i giocatori stanno vivendo si tocca con criteri diversi da uno
   non ancora giocato. **Assunzione**: i lotti su DEF-1 restano **additivi**
   (si aggiungono sidebar, non si riscrive prosa già letta).
2. **Se ARC-08 e ARC-09 vanno rifiniti o solo resi giocabili.** Sono archi
   chiusi come *piano* e ⬜ come *gioco*. **Assunzione**: si interviene solo
   dove manca un congegno **operativo al tavolo** (contingenze, vie non
   combattive, scalatura), non per uniformare lo stile di prosa.
3. **Se la «quarta colonna» e gli ADR interni sono da estendere o restano una
   firma dell'Abbazia.** È la domanda vera di §3.1 e **la lascio aperta al DM**:
   il piano la registra come decisione, non la decide.

**Assunzione trasversale**: ogni numero qui viene da `misura_craft.py` eseguito
sul repo al commit corrente. **Non è un voto** (ADR-0055): dice dove guardare.

---

## 1 · La risposta secca alle tre domande

### «In che percentuale lo stile nuovo è presente in DEF-4?»

🟢 **DEF-4 è fra i quattro documenti del repo che dichiarano i pilastri, e sta
in cima.** La *fusion rule* («UN pilastro guida, al più due di supporto») lascia
una marca scritta — `(Casa di Davide lead)`, `(BG3 lead)`, `(Andor support)` —
e quella marca esiste **solo qui**:

| Documento | marche di pilastro |
|---|---:|
| DEF-5 | 4 |
| **DEF-4** | **3** |
| DEF-2 | 3 |
| DEF-3 | 2 |
| **tutto il resto del repo** (DEF-1, Abbazia, Palio, ARC-08, ARC-09 — 90 file) | **0** |

⚠️ **Quindi la domanda va girata**: non «lo stile nuovo è arrivato in DEF-4»,
ma «**è arrivato solo lì**». DEF-4 non è la parte indietro: è una delle quattro
avanti. Le parti indietro sono ARC-08 e ARC-09, e lo stesso DEF-1.

Sul resto del mestiere DEF-4 copre **11 congegni su 17 (65%)** — esattamente
quanto il Palio (65%) e sopra DEF-2 (47%), DEF-3 (41%), DEF-5 (41%).

⚠️ **Ma la risposta ha una seconda metà, e la prima versione di questo piano
non ce l'aveva.** Sui pilastri DEF-4 è avanti; sugli **standard redazionali**
— che sono scritti, numerici e normativi quanto i pilastri — è indietro come
tutti tranne DEF-1: **una sola** regia etichettata su 5 read-aloud, **zero**
dialoghi nella forma prescritta, **zero** chiusure su «Che fate?», e uno dei
suoi due box veri **supera il tetto delle 12 righe**. Il perché sta in §1.3.

### «È migliorabile, e dove?»

Sì, e in tre punti precisi, tutti misurati contro i banchi:

| Congegno | DEF-4 | Abbazia | Palio | Cosa vuol dire |
|---|---:|---:|---:|---|
| **read-aloud narrativo** | **5** | 11 | 41 | 🔴 DEF-4 ha **5 letture** in 955 righe. Il Palio ne ha 41 in 3.070. È il divario più grave |
| **orologio / countdown** | **1** | 31 | 41 | 🔴 una sola menzione. I due banchi reggono la tensione **con gli orologi**; DEF-4 no |
| **modi di fallimento** | **0** | 2 | 1 | il fallimento come *costo* invece che come *stop* non è scritto da nessuna parte |
| **nodo d'indizio** | **0** | 15 | 7 | zero — ed è un modulo con un'indagine (le Cronache dei Quattro Eroi) |
| **grigio politico** | **0** | 8 | 3 | Balvar Fuocospento *è* un grigio (§4-ter «sa da dove venite»), ma non è scritto come tale |
| eco / conseguenze | **18** | 0 | 13 | 🟢 **il più alto del repo in densità** (18,8/1.000). Qui DEF-4 è il banco |
| battute di dialogo | **59** | 20 | 26 | 🟢 densità 61,8/1.000, la seconda del repo |

### «Cosa fanno i banchi che non è mai arrivato nella skill dello stile?»

🔎 **Il sospetto del DM era fondato, e sono due congegni, entrambi dell'Abbazia.**
Nessun altro documento del repo — 100 file misurati — li porta:

1. **ADR interni al documento** (13 occorrenze). L'Abbazia scrive **dentro
   l'avventura** il *perché* di ogni scelta di design. Nessun arco lo fa.
2. **La «quarta colonna» sensoriale** (5 occorrenze, ADR-12 dell'Abbazia):
   la regola contro «l'atmosfera divora l'indagine» — *il dettaglio che non dici
   mai appartiene a chi fa la domanda*.

E due che l'Abbazia ha in quantità doppia rispetto a chiunque: **contingenze**
(32 in 1.422 righe, 22,5/1.000 — il primato) e **vie non combattive** (12).

---

## 2 · La mappa completa: tutte le parti, non solo DEF-4

Copertura dei congegni e **debito verso i banchi** (congegni che Abbazia o
Palio hanno e questo documento no):

| Parte | file | righe | copertura | debito | Il buco che conta di più |
|---|---:|---:|---:|---:|---|
| ★ **Abbazia** | 4 | 1.422 | **71%** | 2 | — *(è un banco)* |
| ★ **Palio** | 15 | 3.070 | 65% | 3 | — *(è un banco)* |
| DEF-1 Piano della Terra | 1 | 2.277 | 65% | 5 | **0 vie non combattive** in 2.277 righe |
| DEF-2 Ritorno e affreschi | 1 | 909 | 47% | 8 | 0 vie non combattive, 0 indizi |
| DEF-3 Resurrezione Hella | 1 | 852 | 41% | 8 | 0 orologi *(3)*, 0 vie non combattive |
| **DEF-4 Viaggio 1.000 anni** | 1 | 955 | **65%** | 6 | **5 read-aloud, 1 orologio** |
| DEF-5 Ritorno Hammerfist | 1 | 513 | 41% | 9 | 🔴 **0 read-aloud narrativi** |
| ARC-09 Torre di Zalkatar | 12 | 1.193 | 59% | 5 | 🔴 **0 read-aloud, 0 dialogo** in 12 file |
| ARC-09 Torneo di Dauth | 22 | 4.680 | 65% | 4 | 8 read-aloud in 4.680 righe (1,7/1.000) |
| ARC-09 Rhest | 8 | 1.151 | 59% | 5 | **0 dialogo**, 0 echi |
| ARC-09 Battaglia Finale | 16 | 3.218 | 47% | 7 | 🔴 **0 read-aloud** in 16 file |
| ARC-08 Hammerfist | 13 | 6.096 | 59% | 5 | 🟢 90 read-aloud: il più ricco. 0 indizi |

### Le tre assenze che attraversano **tutto** il repo

| Congegno | Chi ce l'ha | Chi non ce l'ha |
|---|---|---|
| **scalare lo scontro** | DEF-1 (3), DEF-4 (1) | 🔴 **tutti e dieci gli altri, a zero** — ed è una *sidebar obbligatoria* di `module-standard` §8 |
| **ADR interni** | solo l'Abbazia (13) | tutto il resto |
| **quarta colonna** | solo l'Abbazia (5) | tutto il resto |

🔴 **La scalatura è il buco più grosso del repo**, e non è un'impressione: la
lingua della scalatura (`scalatura`, `Scalare lo scontro`, `party più forte`,
`PG abbattuto`) è dichiarata **7 volte in due skill canoniche**
(`rumblingstone-module-standard`, `rumblingstone-playtest`), compare in 4 file
di ARC-07 e in 1 dell'Abbazia — e **zero volte nei 71 file di ARC-08 e
ARC-09**. Lo standard è scritto; non è stato applicato.

---

## FASE 1 — Audit / accertamento *(fatta, riportata per il commit)*

### 1.1 · Lo strumento e come è stato provato

`scripts/misura_craft.py`, 17 congegni, ognuno con la **fonte dichiarata** nel
terzo campo: un congegno che nessun documento del repo dichiara non è un
criterio, è un gusto personale, e non entra.

🔴 **La prima tabella diceva il falso, ed è la parte più importante di questo
audit.** Cinque rilevatori su diciassette erano sbagliati e un sesto difetto non
era in nessun rilevatore. L'elenco completo, con le misure che l'hanno imposto,
è in [ADR-0055](adr/ADR-0055-il-mestiere-si-misura-per-congegni.md) §«La prova
che la decisione serviva». Il più grave: `^>` contava come read-aloud **ogni**
citazione, e DEF-1 segnava **183 read-aloud** che erano note editoriali
(`> **Sistema: D&D 3.5 SRD**`), mentre l'Abbazia ne segnava 11 tutti veri —
**il numero diceva il contrario del vero**.

Il sesto: **misuravo 6 file del Palio su 15 e 1 di ARC-08 su 23**. Gli zeri
sembravano assenze di mestiere ed erano assenze di misura.

### 1.2 · I cancelli, provati all'indietro

`scripts/tests/test_misura_craft.py` — 17 test, 13 subtest. Ogni classe fissa
**una** delle sei bugie **dal lato che morde**, e le due sabotature fatte a mano
prima del commit sono andate rosse:

| Sabotaggio | Esito |
|---|---|
| rimesso `^>` largo sul read-aloud | 🔴 `test_la_nota_editoriale_non_conta` |
| rimesso il grassetto obbligatorio sullo spotlight | 🔴 `test_il_PG_conta_anche_senza_grassetto` |

### 1.3 · 🔴 Il lavoro annegato in un commit — l'ipotesi del DM, verificata

Il DM il 2026-09-18: *«non era stato definito qualcosa di più grande? erano
stati fatti degli aggiornamenti dello stile della scrittura per rendere le
scene editoriali più effettive ed importanti — probabilmente è annegato in
qualche commit che non è stato seguito»*.

**Era esatto, e l'audit precedente non l'aveva visto perché non aveva letto le
fonti.** I congegni del §1.1 li avevo presi da `module-standard` e dalla skill
dell'indagine. Le skill hanno una cartella `references/` — **dieci file solo in
`rumblingstone-narrative-style`** — e dentro ci sono standard di scrittura
**numerici** che nessuno misura.

#### Cosa esiste davvero, ed è normativo

| File | Cosa prescrive |
|---|---|
| `references/read-aloud-adulti.md` (171 righe) | **si ascolta, non si legge**: box **≤ 12 righe** (2-4 per un round di combattimento), **un solo nome proprio nuovo per box**, niente parentesi né incisi, max due livelli di subordinate, l'ultima riga è quella che resta |
| `references/editorial-standards.md` §2 | `**Read-aloud (pilastro lead).**` per etichettare la regia · `**NOME (registro/tono):** *«battuta»*` per i dialoghi |
| `ADR-0014` (regia sensoriale obbligatoria) | **nessuna sequenza a battute senza regia** (apertura di round, una battuta per attore, esito riuscita **e** fallimento, chiusura) · **occhio da avventuriero, non da architetto** · **chiusura su «Che fate?»** |
| `references/passate-redazionali.md` · `italiano-nativo.md` · `varieta-fra-archi.md` | le tre passate, i tic dell'IA, la tavolozza d'arco |

#### E i due commit che li hanno introdotti senza applicarli

| Commit | Cosa ha aggiunto | Cosa ha applicato |
|---|---|---|
| `10795aa` (PR #89) | `read-aloud-adulti.md`, **171 righe** di standard | 🔴 **nessun file d'arco**: 7 file toccati, tutti skill/piani/glossario |
| `d9c357b` | `ADR-0014` + 21 righe in `module-standard` + 13 in `editorial-standards` | **ARC07-DEF-1 e basta** (309 righe) |

🔎 **Ed è questo che spiega la tabella del §2**: DEF-1 svetta in ogni colonna
non perché sia scritto meglio, ma perché **è l'unico documento che ha ricevuto
il trattamento**. Tre colonne indipendenti lo provano:

| Congegno ADR-0014 | DEF-1 | tutti gli altri 11 bersagli |
|---|---:|---:|
| regia di round (una battuta per attore) | 3 | **0** |
| chiusura su «Che fate?» | 1 | **0** |
| dialogo nella forma prescritta | 3 | 3 *(DEF-3: 1 · DEF-5: 2)* |

**«Che fate?» esiste una volta sola in tutto il repo**, ed è prescritto per
**ogni** box di combattimento.

#### Perché nessuno se n'è accorto: il cancello sembra coprirlo e non lo copre

🔴 `validate_modules.py` — l'unico lint redazionale — ha **due buchi**:

1. **Conta le occorrenze della parola.** `n_readaloud = len(re.findall(r"[Rr]ead-aloud", text))`, avviso sotto 5. Un master con cinque **menzioni** e **zero box** passa. DEF-4 ha 5 box veri e DEF-5 ne ha **zero**, e nessuno dei due è mai stato segnalato.
2. **Gira solo su `ARC*-DEF-*.md`.** ARC-08, ARC-09, il Palio e l'Abbazia — **96 file su 100** — non sono mai stati guardati da nessun cancello. È la ragione per cui «Scalare lo scontro» sta a zero in 71 file: è nella checklist, ma la checklist non arriva lì.

E nessuna delle soglie numeriche di `read-aloud-adulti.md` è sotto cancello.
Misurate adesso (`misura_craft --box`):

| Bersaglio | box | >12 righe | con parentesi | >1 nome proprio |
|---|---:|---:|---:|---:|
| ★ **Abbazia** | 11 | **0** | **0** | 1 |
| ★ Palio | 40 | 0 | 2 | 17 |
| DEF-1 | 14 | 2 | 6 | 12 |
| **DEF-4** | 2 | **1** | 2 | 2 |
| DEF-5 · Torre · Battaglia Finale | **0** | — | — | — |
| ARC-08 | 82 | 0 | 3 | **63** |

🟢 **L'Abbazia rispetta la norma quasi alla perfezione** — zero box oltre il
tetto, zero parentesi — ed è la prova che il metro non è impossibile: è la
norma del repo, applicata da un documento solo.

### 1.4 · Trovato misurando, **fuori scopo, dichiarato**

- **La Torre di Zalkatar non ha una sola battuta di dialogo** in 12 file, né
  `«…»` né virgolette dritte. Zalkatar è *il padrone delle menti* (canone DM) e
  non parla mai. → lotto S5.
- **DEF-5 e la Battaglia Finale hanno 0 read-aloud narrativi.** DEF-5 è il
  finale dell'arco; la Battaglia Finale è 16 file. → lotti S2, S5.

---

## FASE 2 — Sviluppo / attuazione

Sette lotti, **in ordine di rapporto fra danno al tavolo e costo**. Ogni lotto è
un commit, e ogni commit porta la sua misura prima/dopo (ADR-0036).

### Onda 0 — il cancello, prima della prosa *(nuova, da §1.3)*

🔴 **Va per prima perché senza di lei ogni lotto di prosa è reversibile in
silenzio**: gli standard ci sono da luglio e agosto, e sono rimasti fermi
proprio perché nessuno li guardava.

| | Lotto | Cosa |
|---|---|---|
| ⬜ | **S0a · `validate_modules` conti i box, non le parole** | oggi `len(re.findall("[Rr]ead-aloud"))` ≥ 5 basta: DEF-5 ha **zero box** e passa. Si conta `box_read_aloud()`, e si applicano le soglie di `read-aloud-adulti.md` (≤12 righe, un nome proprio, niente parentesi) come **avvisi** al primo giro |
| ⬜ | **S0b · il lint esca dai 5 DEF** | ARC-08, ARC-09, Palio e Abbazia — **96 file su 100** — non sono mai stati guardati. Prima in sola lettura, per misurare quanto verrebbe rosso, **poi** si sceglie la soglia |

⚠️ **Il rischio di S0b, dichiarato**: accendere il lint su 96 file mai
controllati produrrà centinaia di rilievi. Per questo il lotto **misura
prima e blocca poi**, ed è l'errore che il repo ha già evitato una volta
(`validate_docs --sorgenti`, lotto 4b).

### Onda A — quello che manca *al tavolo* (un DM ne ha bisogno mentre gioca)

| | Lotto | Cosa | Perché prima |
|---|---|---|---|
| ⬜ | **S1 · La scalatura che non c'è** | sidebar «Scalare lo scontro» ai boss di ARC-08 e ARC-09 (oggi **zero** in 71 file) | è una sidebar **obbligatoria** dello standard, e senza il DM improvvisa il bilanciamento |
| ⬜ | **S2 · Gli orologi di DEF-3 e DEF-4** | DEF-4 ha **1** menzione, DEF-3 ne ha 3; i banchi 31 e 41 | è il congegno che regge la tensione: la sua assenza si sente **subito** |
| ⬜ | **S3 · Le vie non combattive dei DEF** | DEF-1, DEF-2, DEF-3, DEF-5 sono a **zero**; lo standard chiede **≥2 per scontro** | un tavolo che vuole parlare oggi non trova niente di scritto |

### Onda B — la prosa (dove l'assenza è misurata, non un'impressione)

| | Lotto | Cosa |
|---|---|---|
| ⬜ | **S4 · I read-aloud di DEF-4 e DEF-5** | DEF-4 ne ha 5 in 955 righe, DEF-5 **zero** in 513. Banco: il Palio (41) e ARC-08 (90). ⚠️ Si scrivono **al metro di `read-aloud-adulti.md`**, non a occhio: ≤12 righe, un nome proprio nuovo, niente parentesi |
| ⬜ | **S4-bis · ADR-0014 esce da DEF-1** | la regia di round, la chiusura su «Che fate?» e il dialogo `**NOME (registro):**` esistono **solo** in DEF-1 (e 3 battute sparse). Sono prescritti per **ogni** modulo dal 2026-07-30 |
| ⬜ | **S5 · La Torre parla** | 12 file, **zero dialogo**. Zalkatar, i grimlock ceremorfi, i drow psionici: nessuno ha una battuta |
| ⬜ | **S6 · I read-aloud della Battaglia Finale** | 16 file, zero letture. È il climax della campagna |

### Onda C — i due congegni dell'Abbazia *(gated sul DM, §3.1)*

| | Lotto | Cosa |
|---|---|---|
| 🔵 | **S7 · La quarta colonna e gli ADR interni** | portarli nella skill dello stile e in un arco pilota — **solo se il DM decide che sono standard e non firma dell'Abbazia** |

---

## FASE 3 — Validazione

Il criterio non è «il numero sale». È **ADR-0036**: ogni lotto dichiara la sua
misura prima, la sua misura dopo, e **cosa si vedrebbe al tavolo**.

### 3.1 · Criteri per lotto

| Lotto | Cancello | Verifica al tavolo (il vero giudice) |
|---|---|---|
| S1 | `misura_craft --densita`: «scalare lo scontro» > 0 in ARC-08 e in ≥3 bersagli ARC-09 | il DM alza o abbassa un boss **senza fermare il gioco** |
| S2 | DEF-3 e DEF-4 sopra 8/1.000 (metà del Palio) | esiste una scena in cui i PG **perdono qualcosa** perché hanno tardato |
| S3 | ogni DEF ≥ 1; nessuno scontro senza ≥2 vie | un gruppo che vuole parlare trova una CD scritta |
| S4/S5/S6 | read-aloud narrativi > 0 in **ogni** bersaglio; DEF-4 ≥ 10 | il DM legge senza dover improvvisare |
| S7 | — | decisione del DM (D1) prima di qualunque cancello |

### 3.2 · Non-regressione, a ogni commit

```bash
python3 scripts/misura_craft.py --copertura      # nessuna colonna scende senza motivo scritto
python3 scripts/validate_modules.py              # i 5 master ARC-07 restano conformi (0 errori)
python3 -m pytest scripts/tests -q               # compresi i 17 di test_misura_craft
python3 scripts/tools_manifest.py --check        # 64 tool conformi
python3 scripts/check_plans_discipline.py        # regola d'oro
```

🔴 **Una colonna che scende dev'essere spiegata per iscritto**, come una soglia
che cala: altrimenti questo piano diventa un tappeto.

### 3.3 · Il limite che questo piano non supera

⚠️ **Nessuno dei cancelli sopra dimostra che la prosa è buona.** Dimostrano che
il congegno **c'è**. Un read-aloud brutto passa `misura_craft` esattamente come
uno bello — ed è per questo che ogni lotto ha la colonna «verifica al tavolo»,
che è l'unica che conta e che **nessuno script può chiudere**.

---

## Decisioni aperte al DM

<!-- decisioni-dm: MESTIERE-BANCHI -->

| # | Fase | Domanda |
|---|---|---|
| D1 | F2 · S7 | **Gli ADR interni al documento e la «quarta colonna» sensoriale sono standard, o restano la firma dell'Abbazia?** Sono 13 e 5 occorrenze, in **un documento solo su 100** — l'unico congegno del repo che un banco ha e nessun altro. Estenderli è lavoro su tutti gli archi e un'aggiunta alla skill dello stile; lasciarli all'Abbazia è una scelta legittima, ma finché non è **scritta** sembra una dimenticanza. Il lotto S7 è gated su questa risposta |
| D2 | F2 · S4-S6 | **ARC-08 e ARC-09 si rifiniscono nello stile, o si toccano solo dove manca un congegno operativo al tavolo?** Cambia l'ampiezza dei lotti da «aggiungere una sidebar» a «riscrivere prosa». I due archi sono chiusi come *piano* e ⬜ come *gioco*: la Torre non ha **una sola battuta** in 12 file e la Battaglia Finale **zero read-aloud** in 16, ma nessuno dei due è mai stato giocato, quindi nessuno li ha visti mancare |
| D3 | F2 · S2-S3 | **DEF-1 è 🟡 in corso al tavolo: i lotti su di lui restano additivi?** Il piano assume di sì (si aggiungono sidebar, non si riscrive prosa già letta ai giocatori), ma è un'assunzione mia. DEF-1 ha **0 vie non combattive in 2.277 righe**: colmarlo è additivo, ma toccare i suoi read-aloud non lo sarebbe |
