# ADR-0119 — Le regole PF1e del cancello delle schede vengono dal PRD, e i conti nuovi partono in prova

**Stato**: proposta (2026-11-09)
**Data**: 2026-11-09
**Decisione-fonte**: il DM (Jfs), 2026-11-09, thread «Scelte dell'8/11: Bestiario e norme»: *«deve coprire tutto. per le parti bloccanti nelle regole di pf1e apri i threads necessari a colmare questo vuoto nelle regole così sono complete»*. Regola del DM del 2026-11-03: un cancello nuovo parte non bloccante e diventa bloccante dopo la promozione.
**Rapporti**: completa F4 di [ADR-0112](ADR-0112-il-motore-e-agnostico-e-le-regole-d20-sono-dati-e-formule.md) (`creature.conformita`) e chiude la sua card F4 3 («lo dice e salta il conto»). Usa i dati del plugin PF1e di [ADR-0111](ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md) e il PRD a commit fissato di [ADR-0110](ADR-0110-i-termini-ufficiali-hanno-una-tabella-e-un-cancello.md). Il conto dell'attacco e il cancello dei numeri sui master sono di ADR-0118 (thread «Scelte dell'8/11»): questo ADR non li tocca. Segue la regola del DM «si parte dallo standard di fatto»: lo standard qui è il PRD, non una tabella nostra.

## Contesto

`conformita_statblocchi.py --cancello-moduli` controlla in CI le schede ```statblocco``` dei moduli PF1e (Il Drappo di Tarsilia, Il Giardino di Sale e Calce PF1e). Il 2026-11-09 ne saltava tre conti, perché nei dati del plugin PF1e mancava la regola: lotta (in PF1e BMC e DMC), scurovisione e la CD di *corrompere l'acqua*. Il censimento di tutti i numeri delle 14 schede ne ha trovati altri otto che nessun conto guardava, in nessuno dei due sistemi:

| Numero della scheda | Prima | Ora (conto) | Regola, dal PRD |
|---|---|---|---|
| BMC | saltato | `BMC` | BAB + For + taglia; Des se Minuscola o più piccola o con Manovre Agili (Core, book-cr 3437) |
| DMC | saltato | `DMC` | 10 + BAB + For + Des + taglia + deviazione, schivare, sacro… della CA (book-cr 3439) |
| scurovisione | saltata | `scurovisione` | dal tipo, dal sottotipo o dalla razza del Bestiario 1-4 (book-b1 361-433) |
| *corrompere l'acqua* | saltata | `corrompere_acqua` | la CD della presenza terrificante, come in 3.5 (book-b1 1112) |
| BAB | mai | `BAB` | classe per classe (55 tabelle del PRD) più i DV razziali del tipo |
| TS | mai | `TS` | base di classi e DV razziali + caratteristica + Tempra Possente, Riflessi Fulminei, Volontà di Ferro + mantello della resistenza |
| contatto, colto alla sprovvista | mai | `contatto_sprovvista` | CA − armatura − scudo − naturale; CA − Des − schivare |
| iniziativa nel recinto | mai | `iniziativa_recinto` | Des, +4 con Iniziativa Migliorata |
| talento Schivare | mai | `schivare` | +1 di schivare alla CA, sempre |
| visione crepuscolare | mai | `visione_crepuscolare` | come la scurovisione |
| bonus di `pf-dado` | mai | `pf_bonus` | DV × Cos + Robustezza (3, o 1 per DV) + fino a 1 per livello di classe preferita |
| pf con dadi di più tipi | mai | `pf_misti` | media dei dadi + bonus (primo dado al massimo se è di classe) |
| CD e LI degli incantesimi | mai | `cd_incantesimi` | 10 + caratteristica della classe + livello; LI = livello di classe |
| incanalare energia | mai | `incanalare` | (L+1)/2 d6, CD 10 + ½ L + Car, 3 + Car al giorno |

Restano fuori, e lo si dice:

- **attacco e danni**: il conto `attacco` è di ADR-0118, uguale nei due sistemi.
- **abilità**: le schede non scrivono i gradi, quindi il totale non si ricostruisce.
- **CD delle capacità speciali** (veleno, tentacoli paralizzanti…): la regola 10 + ½ DV + mod c'è, ma quale caratteristica usa lo dice la voce di ogni mostro, non una regola generale.
- **GS, velocità, portata**: vengono dalla voce del Bestiario o dal modulo, non da un conto.
- **le schede dei PG pregenerati** (`PREGEN-SEI-SCHEDE-PF1E.md`): non sono recinti ```statblocco```, e il cancello non le legge.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Tabelle generate dal PRD (`conformita_prd.toml`), scelte e alias a mano (`conformita.toml`), conti nuovi in prova** (scelta) | ogni numero ha libro e sezione; `estrai_prd_pf1e.py --check` ridà gli stessi byte; un conto nuovo non rompe la CI di nessuno il giorno in cui arriva | due file per una capacità; gli alias italiani dipendono dal lessico |
| Scrivere le regole a mano in `conformita.toml` | un file solo | numeri senza fonte verificabile: è quello che la regola del DM sui numeri ricostruibili esclude |
| Riusare le tabelle 3.5 (`dnd35/creature.toml [classi]`) per il BAB e i TS | già pronte | in PF1e cambiano i DV e i tipi (costrutto, umanoide, esterno, non morto): sarebbe la regola di un altro sistema senza dirlo, quello che F4 vieta |
| Conti nuovi subito bloccanti | protezione piena da subito | contro la regola del DM sui cancelli nuovi; un falso positivo (un bonus razziale che il conto non conosce) fermerebbe ogni PR |

## Decisione

1. **`sistemi/pf1e/dati/conformita_prd.toml`** è generato da `plans/esperimenti/sistemi-plugin-2026-11-07/estrai_prd_pf1e.py` dal PRD a commit fissato:
   - `[classi]`: BAB e TS di 55 classi (Core, APG, ACG, UC, UM, PNG e prestigio), ciascuna controllata livello per livello contro la formula;
   - `[alias_classi]`: il nome italiano ufficiale dal lessico;
   - `[sensi.tipi]`, `[sensi.sottotipi]`, `[sensi.razze]`: scurovisione in metri e visione crepuscolare;
   - `[corrompere_acqua]`: la frase del PRD, verificata dal generatore.
2. **`sistemi/pf1e/dati/conformita.toml`** tiene le scelte: quali conti si fanno, quali bonus della CA entrano nel DMC, i talenti dei TS, gli alias di tipo, razza e taglia. `[conti.mancanti]` è vuoto. La lotta 3.5 va in `[conti.non_applicabili]`.
3. **Due liste di conti.** `fatti` blocca il cancello, come prima. `in_prova` si conta, e `--cancello-moduli` lo stampa come avviso (⚠) senza fallire. `--cancello-moduli --severo` fa bloccare anche i conti in prova: serve ai test e alla promozione. Promuovere un conto vuol dire spostarlo da `in_prova` a `fatti`.
4. **Il 3.5 non cambia.** I conti nuovi vivono in `conti_di_classe` e `conti_dei_sensi`, e partono solo se il sistema ha `[classi]` e `[sensi]` nei dati. `--master` sui 34 file 3.5 dà lo stesso rapporto di prima, riga per riga.

## Misura

- **Sulle 14 schede vere**, i conti nuovi hanno trovato 7 numeri sbagliati. Tutti sono stati corretti alla regola, nella versione legale:
  - Vidalia: Volontà +6 → **+8**;
  - Sfregio: CA 18 → **19** (talento Schivare), contatto 16, DMC 18 → **20** (anello di deviazione e schivare);
  - cavallo: DMC 18 → **17** (21 contro sbilanciare), come il Bestiary; mancava la visione crepuscolare;
  - skum guerriero 8: Volontà +6 → **+8** (Volontà di Ferro);
  - Mastro Tariq: Robustezza non contata, 13d8+26 → **13d8+39**, pf 88 → **101**.
  Dopo le correzioni `--cancello-moduli --severo` è verde.
- **Prova del contrario** (`scripts/tests/test_conformita_pf1e.py`): quattro schede giuste passano. 27 mutazioni di un solo numero vengono bocciate tutte sul conto giusto. Un numero sbagliato nel Drappo o nel Giardino veri fa uscire il cancello con 0 in prova e con 1 da severo, o da promosso.
- **3.5:** il rapporto `--master` dei 34 file 3.5 è identico a quello di main, e `--riepilogo` e `--check` pure.

## Conseguenze

- Nessun conto PF1e si salta più per regola mancante. Le parti ancora fuori (sopra) non dipendono da una regola che manca nei dati.
- Un modulo PF1e nuovo prende i conti senza codice nuovo. Una classe o una razza che il PRD non ha (Vigilante, i nomi italiani non nel lessico) non viene riconosciuta, e il conto di BAB e TS su quella scheda non parte. Non dà un falso allarme.
- Il TS non conosce i bonus razziali (per esempio la fortuna dell'halfling) né altri oggetti oltre al mantello della resistenza. Per questo il conto è in prova.
- Le correzioni ai moduli sono passate anche nel booklet DM del Drappo (`DRAPPO-BOOKLET-DM.hb.md`, rigenerato) e nella tabella degli scontri in `06-VILLAIN-E-AGENDE.md`.

## Da rivedere se

- Due settimane con il cancello verde sui moduli (2026-11-23): i conti in prova passano in `fatti`, come gli avvisi di `check_schede` (ADR-0114).
- Arriva un modulo PF1e con PNG di razze con bonus ai TS: allora `[ts]` prende i tratti razziali dal PRD.
- Il 3.5 vuole gli stessi conti (contatto e sprovvista, iniziativa nel recinto e Schivare sono identici): basta scrivere i dati nel plugin dnd35.
