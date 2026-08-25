# PIANO — Indagine e deduzione: il nono pilastro

> **Cos'è**: la copertura che mancava al repo per far girare **casi
> investigativi** — misteri, enigmi, indizi che sembrano slegati e che a un
> certo punto si ricompongono in un disegno solo. Nasce da una richiesta del
> DM (2026-08-25) dopo un audit delle skill: il Trono di Spade era già il
> pilastro 5 di `rumblingstone-narrative-style`, ma della deduzione — del
> caso ricomposto — non c'era **niente** in tutto il repo.
>
> **Vincolo che ha dato forma a tutto**: questo tavolo ha personaggi che non
> hanno speso un solo punto in abilità che non massimizzino il danno. Un caso
> che si apre solo con Cercare e Sapienza li esclude. Il piano non risolve il
> problema abbassando le CD: cambia l'unità di misura dell'indizio.

**Stato**: 🟢 eseguito (2026-08-25) · **Decisione-fonte**: richiesta DM in
sessione · **ADR**: [ADR-0022](adr/ADR-0022-competenza-guadagnata-sul-campo.md)

---

## 1. Il divario, misurato

Audit di `skills/` al 2026-08-25 (`grep -ril "sherlock\|indagine\|deduzion\|tre indizi"`):

| Cosa serve a un caso | Dov'era | Verdetto |
|---|---|---|
| Politica grigia, fazioni, tradimenti telegrafati | `style-pillars.md` §5 (Trono di Spade) | ✅ già coperto, e già filtrato dallo splatter (`Avoid` §5) |
| Infiltrazione procedurale, il piano messo sotto stress | `style-pillars.md` §4 (Andor) | ✅ coperto — ma è **come si esegue** un colpo, non come si **legge** una scena |
| Struttura a tappe, fazioni intrecciate | `quest-design-baldur.md` | ✅ coperto |
| **Indizi posati, letti, ricomposti** | — | ❌ **assente** |
| **Prove per chi non ha gradi** | — | ❌ assente |
| **Premio alla testa spremuta** | — | ❌ assente (l'XP premia il combattimento) |
| **Vicolo cieco: cosa fa il DM quando nessuno trova niente** | — | ❌ assente |
| **Enigmi, e il congegno che spiega tutto** | — | ❌ assente |

L'unica riga d'aggancio era il mixer di `SKILL.md:80`
(`Investigation / infiltration | Andor | BG1–2`), che descrive un'altra
cosa: in Andor l'informazione ce l'hai già e il problema è **usarla**; in un
caso l'informazione è sparsa e il climax è **cognitivo**.

## 2. Le quattro decisioni di design

1. **L'indizio non è una CD, è un nodo a tre strati** — *Fatto* (cosa c'è,
   oggettivo), *Lettura* (cosa significa), *Nome* (chi/che cosa
   precisamente). **Il Fatto non si tira mai**: fallire toglie la lettura,
   mai il fatto. È la regola dei tre indizi resa nativa, e chiude il vicolo
   cieco per costruzione invece che per pezza del DM.
2. **Sei porte sullo stesso nodo** — ogni nodo dichiara almeno **tre** delle
   sei caratteristiche come vie d'accesso, e almeno una dev'essere fisica
   (FOR/DES/COS). È la clausola che obbliga chi scrive il modulo a dare
   qualcosa da fare al guerriero, e si controlla a macchina.
3. **Due monete, non una** — *Acume* (per-PG, si spende nel caso, si azzera)
   premia l'intuizione nel momento in cui avviene; *Perizia* (permanente,
   tetto 1 grado/PG/livello) fa sì che un gruppo senza ladro sopperisca nel
   tempo senza sostituire il ladro. Vedi ADR-0022.
4. **L'enigma non è un lucchetto** — risolto dà un vantaggio, non risolto
   non ferma il caso: lo rende più caro. Un enigma che blocca è una trappola
   per il DM, non per i giocatori.

## 3. Lotti

- [x] **I1 — Piano + ADR.** Questo file + `ADR-0022` (competenza guadagnata
      sul campo: la regola della casa che tocca le schede).
      *Accettazione*: l'ADR dichiara tetto, interazione col massimale 3.5
      (livello+3 / (livello+3)/2) e cosa succede al salire di livello.
- [x] **I2 — Skill `rumblingstone-indagine`.** SKILL.md + quattro reference:
      nodi e sei porte · registro e ricompense · ricomposizione · congegno ed
      enigmi. *Accettazione*: `validate_skills.py` verde, nessuna reference
      orfana, confini con le altre skill dichiarati (ADR-0008 §1).
- [x] **I3 — Nono pilastro in `rumblingstone-narrative-style`.** «Il caso
      ricomposto» come pilastro 9 in `style-pillars.md`, righe nuove nel
      mixer, puntatore in Domain→File. *Accettazione*: il pilastro dichiara
      *take* / *avoid* / *in play* come gli altri otto, e **non nomina il
      film** (non-negoziabile 4: le fonti sono mestiere, non marchi).
- [x] **I4 — Deploy e tracciatura.** `build-skills.sh`, mirror per-agente,
      riga in INDEX e CHANGELOG.

## 4. Confini (cosa questo piano NON fa)

- **Non tocca il canone.** Nessun caso scritto, nessun PNG, nessuna riga in
  `state.md`. Questa è infrastruttura di scrittura: il primo caso vero si
  scriverà *usando* la skill, ed è un lavoro a parte.
- **Non è un sistema di abilità alternativo.** Sta dentro il d20 SRD:
  prove di caratteristica grezze (`core-mechanics.md`: d20 + mod, nessun
  grado) e prove d'abilità normali. Niente meccanica nuova da imparare.
- **Non promette che i giocatori dedurranno.** La ricomposizione è
  preparata dal DM come **rete di sicurezza** e ceduta al tavolo quando il
  tavolo ci arriva: è il `[HDYWTDT]` di Mercer applicato alla deduzione.

## 5. Coda (gated sul tavolo)

- ⬜ **I5 — Un caso vero**, scritto con la skill, giocato, e i suoi tempi
  reali riportati in `rumblingstone-playtest`. Senza una sessione vera non
  si sa se un caso da tre strati sta in una serata: **il tetto di Perizia e
  il numero di nodi per caso sono i due numeri da tarare al collaudo.**
- ⬜ **I6 — `validate_modules.py`**: gate meccanico sui nodi (tre porte
  dichiarate, una fisica, il Fatto senza tiro). Ha senso solo quando
  esistono nodi veri da validare — prima sarebbe un validatore senza corpus.
