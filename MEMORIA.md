# 🧠 MEMORIA — il lavoro su RumblingStone in un posto solo

> **Generata da `scripts/memoria.py`: non si scrive a mano** ([ADR-0087](plans/adr/ADR-0087-la-memoria-del-lavoro-e-generata.md)). Ogni riga viene da una fonte che ha la sua casa, e il link porta lì: si corregge la fonte, poi `python3 scripts/memoria.py`. La CI boccia questo file se resta indietro.

## Come si riparte, in una sessione nuova

```bash
git fetch --prune origin
python3 scripts/memoria.py --check      # questa pagina è allineata?
python3 scripts/decisioni_dm.py --check # le decisioni aperte
python3 scripts/fase1.py <file>         # sempre, prima di toccare
```

Poi si legge questa pagina dall'alto: prima cosa aspetta il DM, poi da dove riparte l'agente. Le regole di lavoro stanno in [`AGENTS.md`](AGENTS.md).

## Aspetta il DM: 32 decisioni aperte

Fonte: le tabelle `decisioni-dm` dei piani, aggregate in [STATO-E-ORDINE §4](plans/STATO-E-ORDINE-DEI-PIANI.md). Si risponde col numero e il piano: *«CODA-SECONDO-LETTORE D2 sì»*.

| Piano | # | Ambito | Domanda |
|---|---|---|---|
| `BOX-LUOGO` | D1 | B3 | **Il tetto del box di luogo: righe, frasi o caratteri?** Oggi la norma è ≤ 12 righe; *Dungeon* conta le frasi; i 300-500 caratteri non hanno fonte. Proposta: si tiene ≤ 12 righe come norma pesata; **≤ 4 frasi** diventa… |
| `BOX-LUOGO` | D2 | B0 | **Le dimensioni nella prima frase del box** («camera quadrata di quaranta piedi»), come nel modello del 2026-10-01, o il paragone di ADR-0014 con le misure nei Dati per il DM? Proposta: resta ADR-0014. Dal modello ester… |
| `BOX-LUOGO` | D3 | B2 | **Ogni box dichiara il suo tipo?** Per esempio `**Read-aloud (luogo · Salvatore lead).**`, con i tipi luogo, ingresso, round, rivelazione, chiusura. Sblocca la norma «niente creature nel box di luogo» e le soglie per ti… |
| `BOX-LUOGO` | D4 | — | **I box già giocati fuori dalle nuove misure**: nei DEF di ARC-07, 27 box oltre i 500 caratteri e 61 oltre le quattro frasi. Proposta: non si toccano, come per D9 di PIANO-LETTORE: si spezzano solo se lo chiedi, e senza… |
| `BOX-LUOGO` | D5 | B5 | **L'Abbazia con le stanze *keyed*** (è la F5 di PIANO-LETTORE, «decidere col DM se ogni stanza vuole un box»). Proposta: sì, un box di luogo breve per stanza nell'ordine di *Dungeon*, quando F5 tocca l'Abbazia; è il ban… |
| `BOX-LUOGO` | D6 | B1 | **Il template d'area va in `campaign/templates/`**, accanto a quelli di sessione e di mappa, in due versioni (3.5 e PF1e)? Proposta: sì, tutte e due, con la creatura sempre come rimando al Bestiario e mai trascritta |
| `CODA-SECONDO-LETTORE` | D2 | 3 | **Il campo *Etichetta regia* troncato in `PROMPT-IMMAGINI-07ILP.md`**: si cerca chi compila il file e si corregge lì, o si correggono a mano le 32 righe? *Proposta*: prima si cerca il generatore (`extract_scene_prompts`… |
| `CODA-SECONDO-LETTORE` | D3 | 4 | **La *d* eufonica** (*legato a Aegis Fang*, *a area*): la vuoi come norma? *Proposta*: sì, *ad* solo davanti alla stessa vocale, scritta in `editorial-standards.md` e misurata; se no, resta com'è |
| `LETTORE-PLAYTESTER` | D35 | F4 | **DEF-3, il rito quando va male** (i due 🔴 del playtester a freddo). **(a)** Gli Step 1-3 falliti dicono solo «riprova» (−2 cumulativo, 2d6 non letali, −10 min), senza tetto né uscita, e Conoscenze e Utilizzare Oggetti… |
| `LETTORE-PLAYTESTER` | D36 | F4 | **I 🟠 di regole di DEF-1, DEF-2 e DEF-3 che chiedono canone**, raccolti dalle letture a freddo del 2026-09-30 (`esperimenti/f4-def1-def3/`). **(a)** DEF-1: la Benedizione «ignora le penalità» ma la tabella della gravità… |
| `LETTORE-PLAYTESTER` | D37 | F4 | **DEF-1 Scena 7: Tordek da solo contro la Sentinella, e se cade?** (🔴 del playtester a freddo). L'anticamera immobilizza Thorik (Forza CD 28, che lui al massimo fa 27) e lascia Artemis prono e indifeso: se Tordek va a 0… |
| `LETTORE-PLAYTESTER` | D49 | F3-quinquies | **Le pozioni del re per i gruppi futuri** (🔴 del lettore, giro 3). La Scena 4 e C.1 danno 4 pozioni d'*invisibilità* CL 12, le Benedizioni e la mappa; il banco e §8 B danno 5 *volare* e 4 *cura ferite gravi*, che è il c… |
| `LETTORE-PLAYTESTER` | D50 | F3-quinquies | **Grask a 4 tacche esatte** (🟠 del lettore). «Sveglio fino alla 4ª tacca, addormentato dalla 5ª»: chi arriva alla tenda con 4 tacche segnate lo trova sveglio o addormentato? Proposta: **sveglio** finché la 4ª tacca è l'… |
| `LETTORE-PLAYTESTER` | D51 | F3-quinquies | **Ucciso «in silenzio» o «spettacolare»** (🟠 del lettore). Decide se all'alba i PG perdono la prima azione. Proposta: è **spettacolare** se almeno una guardia o Grask, vivi e coscienti, vedono la morte di Zog'tar **e**… |
| `LETTORE-PLAYTESTER` | D52 | F3-quinquies | **La lastra di Balvar** (🟠 del lettore). Il master lascia al DM cosa c'è inciso («gancio bianco per ARC-09»). Proposta: resta un gancio bianco, ma il master dà una riga da leggere se il tavolo la legge subito (tre rune… |
| `LETTORE-PLAYTESTER` | D53 | F3-quinquies | **Il prezzo delle rune d'annullamento di Zeth** (🟡 del playtester, giro 3). Q5 le prezza come una pergamena di *dissolvi magie* all'incantatore di 9°, 675 mo: è il prezzo del 3° livello (chierico, mago). Ma Zeth è un dr… |
| `LETTORE-PLAYTESTER` | D54 | F3-quinquies | **I Treant di Hella entrano nel duello?** (🟠 del playtester). Durano 1 ora (`DEF-3` A.2) e caricano il fianco dell'orda all'alba; il master non dice se sono ancora lì quando cala il drago. Proposta: no. Restano sul fian… |
| `LETTORE-PLAYTESTER` | D55 | F3-quinquies | **Balvar recuperato e il ritorno in volo** (🟠 del playtester). Il master porta Balvar al cortile solo a piedi; il gruppo che torna in volo lo lascia al campo. Proposta: Balvar non vola; esce dal campo da solo nella conf… |
| `LETTORE-PLAYTESTER` | D56 | F3-quinquies | **Zog'tar catturato: come si porta via?** (🟠 del playtester). Il successo in più sulle mura c'è, il trasporto no. Proposta: solo legato e privo di sensi; in volo non si porta (Grande, in mithral, oltre il carico di chiu… |
| `LETTORE-PLAYTESTER` | D57 | F3-quinquies | **La Presenza Minacciosa di Zog'tar** (🟠 del developer, giro 3). Non è SRD, non è nei tre `Boost log:` e ha CD 22. Proposta: resta, presa sul modello della presenza terrificante dei draghi (10 + ½ DV + mod. CAR = 10 + 7… |
| `LETTORE-PLAYTESTER` | D58 | F3-quinquies | **I PX delle Scene 6-8** (🟠 del developer). Il master dà 2.400 a testa; il developer, a tabella DMG, stima ≈ 3.650 a testa per la tenda intera (≈ 2.700 con Balvar recuperato) e trova pattuglia e lupi senza voce. D40 ha… |
| `LETTORE-PLAYTESTER` | D59 | F3-quinquies | **Il bottino della tenda** (🟠 del developer). §8 B elenca ≈ 10.400 mo più il Sigillo; l'equipaggiamento di Zog'tar, delle guardie e (se muore) di Balvar vale, a stima del developer, ≈ 40.000-45.000 mo, cioè il tesoro di… |
| `LETTORE-PLAYTESTER` | D60 | F3-quinquies | **Il drago Vecchio del «party straripante»** (🟠 del DM a freddo, giro 3). La riga dovrebbe rendere il duello più duro, e invece dà meno pf e CD più basse del drago di base, che ha già il template Avanzato (297 pf, CD 28… |
| `LETTORE-PLAYTESTER` | D61 | F3-quinquies | ***Dragondoom* di Aegis Fang contro Skullcrusher** (🟠 del DM a freddo). Per la Cintura di Tordek il master dice che rifiuta; per Aegis Fang non dice niente, e il giocatore lo chiederà. Proposta: funziona, come contro og… |
| `LETTORE-PLAYTESTER` | D62 | F3-quinquies | **Cosa vuol dire «un tiro sul *Registro delle Perdite*»** (🟠 di lettore e DM a freddo). Q11 lo vuole, DEF-4 e `ARC08-17` lo citano, ma `ARC08-03-REGISTRO-PERDITE.md` è un foglio di caselle per unità e **non ha una tabel… |
| `LETTORE-PLAYTESTER` | D63 | F3-quinquies | **Che cosa muove Skullcrusher** (risposta al passo 7, scritta su richiesta del DM, `[INFERRED]` in DEF-4 Scena 7 e 11). Il drago non ha mai perso; ha accettato il patto di Balvar per il tesoro del re, e ha scoperto dopo… |
| `RECUPERO` | D3 | L5 | **`RIPRESA-PR#D2` e la #106**: il collaudo SDXL accanto a Gemini tiene aperta la #106 da otto settimane, e il suo codice è già su `main` in forma nuova. La #230 installa ComfyUI e scarica SDXL sulla tua Debian 13. *Prop… |
| `RECUPERO` | D4 | L5 | **`RIPRESA-PR#D11` (ADR-0049, l'AP originale)**: resta aperta dal 2026-09-11, legata a un avvocato IP e a VENDIBILITA, che non è autorizzato. *Proposta*: passa a voce di `adozioni-in-attesa.json` con la condizione «VEND… |
| `RECUPERO` | D5 | L4 | **I ⬜ opzionali dei piani chiusi o fermi**, per gruppo. *Proposta*: (a) chiusi come «non si fa»: AUDIT-SCRIPTS (shellcheck lo fa AMBIENTE A6), IMPORT-ULTRACLEAR (migrazione delle ~30 mappe, ora COLLAUDO-MAPPE), RENDER-F… |
| `RECUPERO` | D6 | L3 | **RICONCILIAZIONE-PR-APERTE si chiude come superato?** R3, R6, R7, R8 sono decisi o fatti altrove (§2.3). *Proposta*: sì, ✅ con il rimando a dove sta ognuno |
| `RIPRESA-PR` | D2 | F3 · 3d | **Riformulata il 2026-09-11: la domanda di prima partiva da un fatto falso.** Diceva *«i diciotto raster si generano sulla tua macchina — quando?»*, ma **esistono tutti e diciotto** (più le due extra), generati dal DM *… |
| `RIPRESA-PR` | D11 | F4 · 4b | **L'ADR ex-0018 della #72: recuperato il 2026-09-11 come [ADR-0049](plans/adr/ADR-0049-edizione-commerciale-ap-originale.md), e resta 🔵 *proposta* — non accettata.** Dice che, *se e quando* si pubblica, si pubblica un *… |

### Revisioni della prosa da approvare: 4

Fonte: i documenti `REVISIONE-*.md` sotto `plans/scrittura/` che `ciclo_prosa.py applica` può ancora applicare. Ogni cartella ha un `LEGGIMI.md` con i passaggi interi.

| Documento | Originale | Modifiche | Spuntate |
|---|---|---:|---:|
| [`REVISIONE-ARC08-11-PONTE-ARRIVO-r1.md`](plans/scrittura/revisioni-pilota-ARC08/REVISIONE-ARC08-11-PONTE-ARRIVO-r1.md) | `08_La Battaglia Di Hammerfist/ARC08-11-PONTE-ARRIVO.md` | 3 | 0 |
| [`REVISIONE-ARC08-15-HANDOUTS-GIOCATORE-r1.md`](plans/scrittura/revisioni-pilota-ARC08/REVISIONE-ARC08-15-HANDOUTS-GIOCATORE-r1.md) | `08_La Battaglia Di Hammerfist/ARC08-15-HANDOUTS-GIOCATORE.md` | 2 | 0 |
| [`REVISIONE-Cerimonia-delle-100-Asce-r1.md`](plans/scrittura/revisioni-pilota-ARC08/REVISIONE-Cerimonia-delle-100-Asce-r1.md) | `08_La Battaglia Di Hammerfist/Cerimonia-delle-100-Asce.md` | 5 | 0 |
| [`REVISIONE-hammerfist_encounters-r1.md`](plans/scrittura/revisioni-pilota-ARC08/REVISIONE-hammerfist_encounters-r1.md) | `08_La Battaglia Di Hammerfist/hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md` | 3 | 0 |

## ▶ In corso: da qui si riparte: 7

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **Le PR aperte al 2026-10-10, dopo il merge di #229, #230 e #232, e cosa resta a ciascuna** *(rimisurate con `git merge-tree` su `e63fddd5`)*: **#216** la revisione della prosa (D13, D17, D38, la *Torre*, `MEMORIA.md`):… | [PIANO-RECUPERO](plans/PIANO-RECUPERO-DECISIONI-E-REVISIONI-INCOMPIUTE-2026-10.md) §2.6 · RIPRESA-PR | DM: il merge della PR del riallineamento e della #231, poi D3-D7 di RECUPERO |
| **Le decisioni D49-D63 di DEF-4, poi il giro 4 di conferma**; poi DEF-5. Il giro 3 completo e il passo 7 sono fatti *(2026-10-12, PR #239)*: nessun 🔴 dopo il lettore, quiz 10 su 14 dal diario | [LETTORE-E-PLAYTESTER](plans/PIANO-LETTORE-E-PLAYTESTER.md) F3-quinquies | DM, poi agente |
| **Le `[PROPOSTA]` e gli `[INFERRED]` degli altri archi**, un lotto alla volta: 568 in tutto il repo, circa 400 nel contenuto | §12.1 | agente: il prossimo lotto è ARC-08 (32), poi ARC-09 (53), `campaign/` (50), `PG/` (22), il Bestiario (212) per ultimo perché è il più grande |
| **Le regole di 3.5 fuori rete**: gli incantesimi nelle esportazioni PCGen di `Bestiario/pregen-pcgen/` | §8.3 | agente: una riga in `dnd-35-srd/references/resources.md` e la sua voce nel registro delle norme |
| **DEF-1, 2, 3 nella forma del ciclo** *(30 settembre, sera)*: passi 1-4 fatti (scene, contratto, schede, apparati), box letti al tavolo invariati. Letture cieche: DEF-1 lettore 🔴 2, DEF-2 🔴 2 + 2, DEF-3 🔴 1 + 2, DEF-1 p… | LETTORE F4 · `esperimenti/f4-def1-def3/` | DM: D35 (il rito che va male), D36 (sei rilievi di regole), D37 (la Sentinella); D34 e D9 sono decise. Poi agente: applica e rilegge |
| **ARC-07 al ciclo completo** *(30 settembre)*: DEF-5 ai passi 1-6 (tre scene col contratto, schede di Re Thorek e Madre Dana, box al metro, letture a freddo prima e dopo). Restano il passo 7 di DEF-5 (il quiz, D10) e DE… | [LETTORE](plans/PIANO-LETTORE-E-PLAYTESTER.md) F4 | agente: DEF-1 (Varis), poi DEF-2 e DEF-3, `fase1.py` prima di ognuno; una scena già letta al tavolo si converte nella forma, non si riscrive |
| **Il giro delle quattro letture** *(30 settembre, notte)*: lettore, playtester, developer e il DM a freddo (rubrica nuova) su DEF-4 e DEF-5; la procedura è il passo 6 del ciclo in `module-standard`. Giro 1: DEF-5 🔴 2 →… | LETTORE F4 · `esperimenti/giro-def4-def5/` | fatti D39, D40, il lotto mappe D28 (2026-10-08) e il giro 2 su DEF-4; D38 è decisa nella #216, non ancora su `main`. Resta il giro 3 di DEF-4 |

## 🙋 Aspetta il DM: 10

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **Al DM: il lotto D13 e la D17 di AGENT-SKILLS** *(dalla #206)*: undici documenti di revisione, 23 modifiche applicabili con `ciclo_prosa.py applica --auto` e quattro da guardare; la D17 decide se i box con «sembra» seg… | `plans/scrittura/revisioni-D13/LEGGIMI.md` · §14.4-bis | DM: approvare il lotto, rispondere alla D17; agente: `applica` e rimisura |
| **Al DM: quattro incoerenze di canone** trovate dalle corse di L11 e L12 *(dalla #206)*: il carry-over su Fauci nell'handout di DEF-5 §9, le pozioni antiche fra DEF-4 §6 e DEF-5 §0-bis, il «−2 COS» di Thorik in… | `plans/scrittura/RISULTATI.md` «Cosa hanno trovato le corse» | DM: quale versione vince, una riga per incoerenza |
| **Al DM: le D1-D6 di BOX-DI-LUOGO** *(dalla #206)*: il tetto del box di luogo, le dimensioni nella prima frase, il tipo del box, i box già giocati, l'Abbazia *keyed*, il template d'area | [BOX-DI-LUOGO](plans/PIANO-BOX-DI-LUOGO-E-AREA-CHIAVE.md) | DM; poi la chat editoriale di quel piano, da B1 |
| **Al DM: le quattro revisioni della prova sull'ARC-08** (13 modifiche, segnalazioni da 11 a 5, MQM su in tre file su quattro) | `plans/scrittura/revisioni-pilota-ARC08/LEGGIMI.md` | DM: spuntare e `applica`; poi l'agente fa il lotto di `ARC08-01-GUIDA-DM` (55 segnalazioni) |
| **Al DM, per le mappe** *(dopo la #227)*: il giro di prova di R4-ter e il confronto su M7-D e sul cortile di ARC07 (GUIDA-MAPPE §5.1.1); lo zip Standard di Quaternius e l'elenco dei suoi modelli; la pianta di Dauth da e… | [RESA-ASSET](plans/PIANO-RESA-E-ASSET-DELLE-MAPPE.md) §8 | DM; poi l'agente: le tessere nel tema, il peso misurato, la tabella Quaternius |
| **Al DM: la bozza del Caos Ultimo** (D13) e due righe per `state.md` sul ramo del gruppo: RD del Manto 5/epico e male, *Fortezza Mentale* di Artemis | `04_Anello_S3_Caos_Ultimo_DM.html` · audit §7-bis | DM: approvare o correggere la bozza; `dm.py session end` per `state.md` |
| **Al DM: chiudere la serata del 2026-09-25.** In `campaign/sessions/` non c'è ancora il log: cosa è successo al tavolo lo sa solo il DM | regia della serata §6 (il registro) · `rumblingstone-automation` | `python3 scripts/dm.py session end` sul ramo `campaign-group-rumblingstone-dm-gianfranco`, mai su `main` (ADR-0007) |
| **Al DM: le marcature `[INFERRED]` di DEF-5**: in DEF-4 sono **0** dal 2026-10-07 (chiuse con Q1-Q50); in DEF-5 restano **12** (`grep -c INFERRED`, rimisurato il 2026-10-10) | LETTORE F4 | DM |
| **Al DM: D35, D36, D37** *(30 settembre, sera)*: il rito di DEF-3 quando va male; sei rilievi di regole; la Sentinella di DEF-1. Ognuna con la proposta | §4 | DM: rispondere col numero |
| **Al DM: `state.md` e il Rubino**: §6 lo dà «speso»; ora si usa una volta sola, resta nell'incasso, e dopo l'uso la Corona è intera, +3 e Senzienza (D6). E il log delle serate del 25-27 settembre | `campaign/state.md` §6 · `campaign/sessions/` | `dm.py session end` sul ramo del gruppo, mai su `main` (ADR-0007) |

## ⬜ Da fare, nell'ordine dei piani: 13

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **Al DM, dalla #230**: la scelta delle texture (`terreni-scelta`) e delle tessere CC0 (`coppie`), la prima immagine di ComfyUI, le celle `[PROPOSTA]` di M7-C, PF-4 e Campo Drow 1 (13 tende su 15), il livello B | RESA-ASSET R8 e R4-quinquies · GUIDA-MAPPE §5.1.2 | DM, sulla sua macchina |
| **Due lavori mai arrivati su `main`, non persi**: le schede A4 dei quattro PG (ramo della #99, `fce04907`; lotto 4g di RIPRESA-PR) e la riscrittura di voce di quattro file della sessione Terros (02, 03, 04, 06; 4 riliev… | RIPRESA-PR 4g · CHIUSURA-CATENA lotto P | DM |
| **Drappo L9, il collaudo**: lettore e playtester a freddo sul §2-bis (passo 6 di ADR-0075, rubrica di LETTORE F5), dry-run cronometrato (sta in cinque minuti per taglio?), poi il tavolo. Il booklet `DRAPPO-BOOKLET-DM` è… | DRAPPO Lotto 9 | agente: due agenti che non vedono il piano; poi il DM al tavolo |
| **L'ambiente riproducibile: la macchina come la CI** *(ordine del DM, 2026-10-08; D1-D11 decise)*. La CI è lo standard e la macchina combacia: versione e checksum di ogni binario nel registro, Python 3.13 ovunque, lock… | [AMBIENTE-RIPRODUCIBILE](plans/PIANO-AMBIENTE-RIPRODUCIBILE.md) ·… | agente, dopo D28: A1, un ramo e una PR per lotto. |
| **I residui d'apparato del Palio (26) e del Drappo (43)**: patch a `state.md`, procedura degli stemmi, mappa dei file dell'hub. Cosa è apparato in un modulo autonomo | CICLO-SESSIONE 2g · `scripts/apparato-residui.json` | agente con il DM: una domanda per gruppo, poi i marcatori, poi si abbassa il tetto |
| **Il rilevatore dei box non apre le battute etichettate** (`> **2 di 3 — …** *…`, la forma di Balvar in `DEF-4`): `--box`, `--p1` e `validate_corredo` misurano la prima battuta e non le altre | `misura_craft.box_read_aloud` | agente: allargare l'apertura del box e rimisurare; il denominatore di `--p1` sale, i 22 residui vanno riverificati uno per uno |
| **Due residui editoriali minori**: l'ultima riga dell'indice delle 48 aree dell'Abbazia cade sola a pagina 35; il Palio stampa «Naviga i capitoli qui sopra», che è una frase della catena HTML | §11.3 | agente: il primo si prova con una soglia di righe per pagina, il secondo va tolto dall'introduzione del manifest solo nella stampa |
| **PI-6**, **PI-2**, **PI-5**, **PI-4** (dopo CICLO D6) | PRATICHE §5 e §8 | in quest'ordine, una PR ciascuno |
| **Ciclo di sessione e menu**: Fase 0, poi F1-F4. **D1-D6 decise il 2026-09-30**: la cronaca si aggiorna da sola, le alleanze sono un dato, la prosa la scrive l'agente con le skill, menu numerato, le immagini si elencano… | [CICLO-SESSIONE](plans/PIANO-CICLO-DI-SESSIONE-E-MENU.md) §5 | agente: la Fase 0 |
| **RIPRESA-PR 4g e 4h**; PR aperte #99 e #106 | RIPRESA-PR | `python3 scripts/contenuti_nei_rami.py --fetch` |
| **🧲 e 🤖**, e la nota locale di una mappa che non arriva nella legenda | [RENDER-MAPPE-FEDELTA](plans/PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md) §1 · §9.3 | prima si legge che cosa vuol dire il simbolo in ogni mappa che lo usa |
| **A3 di MASTER-DEF**: il canone di ARC-08 contro lo stato del tavolo, dopo F4 | MASTER-DEF A3 | agente, poi conferma del DM |
| **Le decisioni prese che non sono su `main`, e i piani mai finiti** *(richiesta del DM, 2026-10-10)*: D17, D38, la *Torre* e il lotto D13 sono chiusi solo nella #216, D12 di RICERCA-MESTIERE solo nella #230, e le due PR… | [RECUPERO-DECISIONI](plans/PIANO-RECUPERO-DECISIONI-E-REVISIONI-INCOMPIUTE-2026-10.md) | DM: D1-D6; agente: L2 e L3 non aspettano nessuno |

## 🟡 Fatto a metà: 5

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **Gli oggetti di scena dai modelli 3D CC0** *(RESA-ASSET R4-ter, D17-D22, PR nuova come da D18)*: `build_oggetti_cc0.py` e la scena Blender con un lock solo per il set; il renderer usa la tessera dove c'è e il glifo dov… | [RESA-ASSET](plans/PIANO-RESA-E-ASSET-DELLE-MAPPE.md) R4-ter ·… | codice fatto; DM: il giro di prova sui modelli veri |
| **La resa misurata** *(RESA-ASSET R8, D23-D30, ADR-0086; PR #230)*: `misura_resa.py` con il cancello in CI (244 misure di simboli, 20 di terreni), la pagina di scelta del DM (D28: riquadri con il nome, più fonti, «nessu… | [RESA-ASSET](plans/PIANO-RESA-E-ASSET-DELLE-MAPPE.md) R8 ·… | DM: la scelta di texture e tessere nella pagina nuova, la prima immagine di ComfyUI, le celle `[PROPOSTA]` delle tre mappe |
| **I sette ritratti e le otto tavole sono nel repo** (#172, Canva AI). Restano: gli originali a piena risoluzione al posto delle copie da chat a 533 × 800, e Skullcrusher nel cortile, dove il cane di Hella è sbagliato; i… | `Immagini/PROMPT-RITRATTI-E-TAVOLE-ARC07.md` §4 | DM: esportare da Canva gli originali, stesso nome di file |
| **PI-3, il resto**: la prova del blocco dei segreti (DM), la revisione con l'IA. Le PR di Dependabot su `origin` (#207-#212, dal 2026-10-02) si fondono una alla volta il 2026-10-07, e con le tre azioni alla v7 si chiude… | PRATICHE PI-3 · §15.3 | DM: la prova del segreto |
| **PI-1 · 4i-3**: la prova della prima PR indietro rispetto a `main` | RIPRESA-PR §4.11.6 | la prima PR che resta indietro |

## Fatto di recente: le ultime 12 righe del CHANGELOG

Fonte: [`plans/CHANGELOG.md`](plans/CHANGELOG.md), una riga per lotto chiuso.

| Data | Piano | Lotto | Esito |
|---|---|---|---|
| 2026-10-12 | LETTORE-E-PLAYTESTER | Risposta al rilievo del passo 7, chiesta dal DM: che cosa muove Skullcrusher, i… | 🟡 canone nuovo marcato `[INFERRED]`, aperto come D63 |
| 2026-10-12 | LETTORE-E-PLAYTESTER · REVISIONE-ARC07 | F3-quinquies: il giro 3 completo su `DEF-4` (lettore, playtester, developer, DM… | 🟡 nessun 🔴 dopo il lettore; corretti i rilievi che il testo risolve; D49-D62 aperte al DM; serve il giro 4 di conferma dopo le decisioni |
| 2026-10-12 | REVISIONE-ARC07 · CICLO-SESSIONE | le tredici righe… | ✅ (PR #238, unita il 2026-10-12) |
| 2026-10-12 | LETTORE-E-PLAYTESTER · REVISIONE-ARC07 | giro 3 parziale su `DEF-4` (developer, DM a freddo, playtester) sulle parti del… | 🟡 parziale: tre letture sulle parti nuove; mancano il lettore e il resto del master (chiuso dal giro 3 completo, `plans/esperimenti/def4-giro3/`) |
| 2026-10-12 | REVISIONE-ARC07 · module-standard | le tattiche degli scontri che `DEF-4` rende possibili e non spiegava, e la doma… | ✅ `DEF-4`: la pattuglia dei tre fallimenti, la squadra dei lupi, lo sciamano che vede l'invisibile, le quattro guardie della tenda, Zog'tar sulla breccia all'a… |
| 2026-10-12 | CICLO-SESSIONE · REVISIONE-ARC07 | il corredo della serata dopo il 2026-09-25: `DEF-4` dalla Scena 5 all'esito del… | ✅ `homebrew/sessione-notte-e-alba/`: regia con colonna «tre ore» e «intera», quattro echi nuovi, le dieci boccette nel volume dei giocatori,… |
| 2026-10-11 | REVISIONE-ARC07 | il Torque di Thorek I passa dal consiglio alla Scena 12: il re lo dà di persona… | ✅ `DEF-4`: Momento 5 della Scena 12 con box e battuta del re, Scena 4 e §8 B allineati, ripiego se la scena salta. Rigenerati i due booklet `.hb.md` che citano… |
| 2026-10-11 | AUTOMAZIONE-STATO-SESSIONI · CICLO-SESS… | ADR-0090: la partita del primo tavolo riparte su `campaign-group-rumblingstone`… | 🟡 ADR proposta, da accettare dal DM. Provato in una copia del repo: ramo nuovo, log della serata del 2026-09-25, `state.yaml` a mano, `validate_state` e… |
| 2026-10-11 | REVISIONE-ARC07 · STATO-E-ORDINE | canone delle dieci pozioni identificate a ≈372 DR e contratto del Seme-Mercato… | ✅ `DEF-4`: le dieci pozioni di Kettra, con la brodaglia degli sciamani e la cura con la cera nera. `DEF-1` §6-bis: il contratto del Seme in otto clausole e la… |
| 2026-10-10 | AMBIENTE-RIPRODUCIBILE · PRATICHE (PI-3… | A2 in parte · Python 3.13 in CI, nel registro e nelle guide | 🟡 La #228 di Dependabot (gruppo `pip-settimanale`) alza i pavimenti a `numpy>=2.5.3` e `scipy>=1.18.1`, che chiedono Python >= 3.12: su 3.11 pip non trova vers… |
| 2026-10-10 | RECUPERO · REGISTRO-NORME | L7: le tre pratiche di Infra-Iam-PKI e AiAgentInfrastructure (D7, il DM: *«adot… | ✅ `plans/adr-prenotati.json` (lo `0088` alla #99) e `validate_docs`: `--prossimo-adr` salta i prenotati, `--sorgenti` rosso su un prenotato usato da altri o ar… |
| 2026-10-10 | RECUPERO · STATO-E-ORDINE · INDEX · AGE… | il riallineamento dopo il merge di #229, #230 e #232 (richiesta del DM: ricontr… | 🟡 La #216 portata sul `main` nuovo: sette conflitti risolti tenendo le righe di `main` e aggiungendo le sue, `docs/tools/` rigenerato, §4 e `MEMORIA.md` rigene… |

## Le misure che si portano dietro

- **Decisioni**: 32 aperte, 212 chiuse (`decisioni_dm.py`).
- **Prosa**: 11 revisioni applicate, segnalazioni -28, MQM +2.52 punti (`ciclo_prosa.py registro`).

## Dove vive ogni cosa

| Cosa | Casa unica |
|---|---|
| Lo stato del mondo di gioco | [`campaign/state.md`](campaign/state.md), e il canone si scrive sul ramo del gruppo (ADR-0007) |
| Cosa si fa e in che ordine | [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md) |
| Le decisioni del DM | le tabelle `decisioni-dm` dentro ogni piano (ADR-0047) |
| Cosa è successo | [`plans/CHANGELOG.md`](plans/CHANGELOG.md) |
| Che piani esistono | [`plans/INDEX.md`](plans/INDEX.md) |
| Perché si è deciso così | [`plans/adr/`](plans/adr/) |
| Le norme e chi le misura | [`skills/REGISTRO-NORME-EDITORIALI.md`](skills/REGISTRO-NORME-EDITORIALI.md) |
| Le regole per gli agenti | [`AGENTS.md`](AGENTS.md) |
| Questa pagina | `scripts/memoria.py`, mai a mano |
