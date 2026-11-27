# PIANO — Marcare gli incontri, perché l'EL smetta di essere una parola

> **Cos'è**: dare a ogni incontro del repo la forma dichiarata che `AGENTS.md`
> già prescrive, così che **EL, CR e budget** diventino un dato leggibile da uno
> strumento invece di una stringa in mezzo alla prosa.
>
> **Stato**: 🔵 pianificato (2026-09-21) · **Decisore**: DM
> **Nasce da**: la domanda del DM del 2026-09-21 — *«ci sono le regole 3.5 e
> PF1e come skill nel repo, non si possono usare per creare il verificatore in
> maniera deterministica?»* — e dalla misura che le ha risposto
> ([ADR-0059](adr/ADR-0059-il-punteggio-di-qualita-e-mqm-adattato.md) §Limiti)
> **Sblocca**: il **primo rilevatore di severità critica** del punteggio MQM
>
> **Stato (2026-11-27)**: 🔵 0%, **ripreso ridotto** dalla revisione dei piani
> fermi (verifica su `main` `21906369`). Il primo lotto è **M2.1 sui 7 master
> DEF** (ARC07-DEF-1..5, ARC08-DEF-1 e DEF-2), con M1 ristretto ai master e il
> test che prova il cancello mordere (Fase 3). Ultima modifica prima di oggi:
> 2026-09-27.

---

## 0 · Perché, con il numero

La risposta alla domanda del DM è **sì per l'aritmetica, no per il dato**.

Il tetto **EL ≤ APL+4** è interamente deterministico: l'APL è dichiarato in
`campaign/state.md` (**13**), il tetto è la regola di `npc-villain-boosting`
(**17**), la deroga è il `Boost log:`, e `validate_modules.py --tetto-el`
esiste, gira e legge tutto questo. Quello che non esiste è **la superficie**:

| | Misurato il 2026-09-21 |
|---|---|
| Incontri nella forma che `AGENTS.md` prescrive, `**EL**: [N]` | **0** |
| Stringhe `EL N` in forma nuda nel contenuto di gioco | **150** |
| Di queste, quante sono dichiarazioni e quante menzioni | **non distinguibile con una regex** |
| *Rimisurato il 2026-11-27*, stessa regex `\bEL \d{1,2}\b` e stesse esclusioni | **312 in 110 file** (erano 160 in 53 file al commit `6992c99b`); sui 569 file di `validate_modules._file_di_gioco()` la stessa regex dà 303 in 104 |
| *2026-11-27*, nei master sotto cancello (`copertura_scene`) | 83 scene, 17 di scontro, 10 con un EL scritto, **0 marcate** |

Le 150 mescolano *«Boss Fight - EL 14»*, *«| EL 11 |»* dentro una tabella PX,
*«Standard Treasure for EL 16»* e *«Nota di verifica EL (finale dichiarato
EL 20…)»*. Il primo è un incontro, il secondo è un incontro, il terzo è una
riga di tesoro, il quarto è **una nota su un numero**.

> **La conclusione che il repo ha già imparato quindici volte**: allargare il
> rilevatore per pescare le 150 darebbe un numero, e il numero sarebbe finto.
> Il difetto non è nel rilevatore, è che **gli incontri non si dichiarano**.

⚠️ **Non è un buco di codice, è la forma esatta delle nove norme che il
registro porta come 🔴**: *«la norma presuppone un dato che il testo non
porta»*. Questo piano porta quel dato.

---

## 1 · Assunzioni dichiarate

1. **La forma non si inventa: esiste già.** `AGENTS.md` §*Encounter file
   format* prescrive `**EL**: [N] | **CR breakdown**: [list]`. Questo piano la
   **applica**, non la ridiscute. Se il DM la vuole diversa, si cambia lì e il
   piano segue.
2. **Marcare non è riscrivere.** Un incontro che oggi dice *«Boss Fight (EL
   14)»* va marcato, non riformulato. La prosa resta; si aggiunge una riga che
   un parser legge.
3. **Le menzioni restano menzioni.** *«Standard Treasure for EL 16»* non
   diventa un incontro. Distinguere è un lavoro di lettura, ed è il motivo per
   cui questo è un lotto e non uno `sed`.
4. **L'EL non è l'unico parametro**, ma è l'unico che entra adesso. CR, budget
   PX e APL di riferimento seguono **solo se la marcatura dell'EL regge**: un
   campo in più che nessuno compila è peggio di un campo in meno.

---

## FASE 1 — Audit / accertamento

| | Lotto | Cosa produce | Come si verifica |
|---|---|---|---|
| ⬜ | **M1.1** Censire le 150 occorrenze, una per una *(312 al 2026-11-27: ristretto ai master, sotto)* | tabella: file · riga · **incontro / menzione / tabella PX / tesoro** | il totale torna al conteggio del giorno; ogni riga ha una classe |
| ⬜ | **M1.2** Quanti incontri veri ci sono | il numero che la marcatura dovrà produrre | ⚠️ è il numero che oggi **nessuno conosce**: 150 è il conteggio delle stringhe, non degli incontri |
| ⬜ | **M1.3** Quali portano già un `Boost log:` | 38 file lo contengono — ma quel conteggio è per **file**, non per incontro | incrocio con M1.1 |
| ⬜ | **M1.4** Quali sforerebbero il tetto | la lista vera degli EL > 17, oggi ignota | `--tetto-el` dopo M2 |

*(2026-11-27, consigliata seguita)* **M1 si restringe ai master**: il censimento
delle 312 occorrenze costa molto e vale poco, perché sta in archi non
consolidati che i master sostituiranno; sui master sono circa 17 righe. Il
rilevatore accetta anche `**EL:** N` e gli intervalli («6–11»), la forma degli
stand-alone (5 casi in 4 file). Le misure del giorno: i `Boost log:` sono 149
in 98 file (il piano ne contava 38 file); gli EL nudi oltre 17 sono 5 in 3 file,
e uno solo senza `Boost log:` (`Mappe/ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.md`
r.114, «oltre il tetto, voluto dal DM»).

🔎 **M1.2 è il lotto che giustifica il piano.** Il repo oggi non sa **quanti
incontri ha**. Sa quante volte compare la stringa «EL», che è un'altra cosa.

---

## FASE 2 — Sviluppo

⚠️ *(2026-09-27, ADR-0075)* La marcatura non riscrive prosa, quindi non segue
il ciclo del master per intero. Due passi però la toccano: nei master col
contratto l'`**EL**` sta dentro la scena, e dopo averlo aggiunto si rigenera
l'apparato (`componenti.py --apparato`, passo 3); un master che F4 di
PIANO-LETTORE sta convertendo si marca dopo, non prima.

| | Lotto | Cosa |
|---|---|---|
| ⬜ | **M2.1** Marcare gli incontri dei **7 master DEF** *(erano 5; dal 2026-10-21 ci sono ARC08-DEF-1 e DEF-2)* | il campione più curato e più piccolo: si impara lì la forma, e `validate_modules` già li guarda. Con l'EL si marca il «CR breakdown» e si ricalcola l'EL con `suggest_encounter.el_di` (ADR-0118). ⚠️ ARC08-DEF-1 e DEF-2 dovevano nascere marcati (PIANO-MASTER-DEF §1) e hanno «EL 9», «EL 12,6» nudi. **Ripreso il 2026-11-27**, da fare |
| ➡️ | **M2.2** Marcare ARC-07 non consolidati, ARC-08, ARC-09 | il grosso. *(2026-11-27)* Assorbito da PIANO-MASTER-DEF: ARC-08 e ARC-09 confluiscono nei master, che nascono marcati |
| ⬜ | **M2.3** Marcare `Bestiario/` e gli stand-alone | dove gli statblocchi hanno già un GS/CR dichiarato |
| ⬜ | **M2.4** Il gate diventa bloccante | `--tetto-el` passa da rilievo a errore: da quel momento un incontro oltre APL+4 senza `Boost log:` **ferma la CI** |
| ⬜ | **M2.5** La norma entra nel punteggio MQM | `specifiche-qualita.yaml`: `tetto_el_superato` con severità **critico**, ed è il **primo critico vero**; dopo 14 giorni in testing |
| ⬜ | **M2.6** «Adventure at a glance» *(da P4 di PIANO-PORTARE-IL-MESTIERE-DEI-BANCHI, 2026-11-27)* | una tabella per modulo con ogni incontro, EL, PX e dove sta, generata da `componenti.py --apparato` quando EL, CR e PX sono marcati. Dopo M2.1 |

### La forma, per esteso

```markdown
**EL**: 14 | **CR breakdown**: Skullcrusher CR 13, 2× Hobgoblin Warcaster CR 6
```

Una riga, subito sotto il titolo dell'incontro. ⚠️ **Il `|` dentro una tabella
markdown va evitato**: negli incontri che vivono dentro una tabella si usa la
forma su due righe, e il rilevatore accetta entrambe.

---

## FASE 3 — Validazione

| Prova | Criterio |
|---|---|
| `validate_modules.py --tetto-el` | riporta un numero di incontri **> 0**, e quel numero coincide con M1.2 |
| il cancello morde | un `**EL**: 25` iniettato in un master → rosso; con un `Boost log:` accanto → verde; rimosso → verde |
| nessuna menzione marcata | le righe classificate «tesoro» e «nota» in M1.1 **non** compaiono fra gli incontri |
| `punteggio_mqm --soglia` | resta verde: marcare non deve far scendere nessun punteggio |
| non-regressione | `git diff` non tocca nessun `.svg`, `.png`, `.uvtt`: questo lotto marca testo |

*(2026-11-27)* In `scripts/tests` non c'è ancora un test di `--tetto-el`. Il
cancello gira in CI (`ci.yml` r.558) ed esce 0 solo perché gli incontri
marcati sono zero; il test della riga «il cancello morde» entra con M2.1. Il
numero 150 resta scritto anche in `scripts/validate_modules.py` (r.218) e in
`scripts/specifiche-qualita.yaml`: si correggono col codice di M2.1, non in un
lotto di documenti.

---

## Cosa questo piano NON fa

| | Cosa | Perché |
|---|---|---|
| 🔵 | **Ribilanciare gli incontri che sforano** | marcare è misurare. Cosa fare di un EL 20 su APL 13 è una decisione di difficoltà, e la prende il DM con il numero davanti |
| ⬜ | Marcare CR, budget PX, APL di riferimento | assunzione 4: solo se l'EL regge |
| 🔴 | Toccare gli archivi | `_ARCHIVIO/`, gli `_SNAPSHOT-STORICO.md` e i `DEPRECATO` restano come sono (ADR-0054) |
