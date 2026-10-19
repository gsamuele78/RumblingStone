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

## Aspetta il DM: 29 decisioni aperte

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
| `MASTER-DEF` | D4 | A3 | Il flashback con i pregen di ARC-08: **salta** (S1a parte dal consiglio di guerra di DEF-5, e i bonus D9 prendono i valori di default), **dopo** (giocato come ricordo) o **prima** (com'è oggi)? Consigliata: salta |
| `MASTER-DEF` | D5 | A3 | Le undici risposte consigliate di A3 (Q2-Q12 nel file): il bane di A7 non si somma al +2 del carry-over; il tetto di 3 ferite resta; il log della sessione 4 si corregge secondo DEF-4; Dana viva; gli echi di DEF-4 entran… |
| `MASTER-DEF` | D6 | A3 | Le domande del censimento delle versioni (D1-D4, D6-D15 nel file, le consigliate fra parentesi): soffio di 2B su Riflessi; PF di Fauci dal massimo della sua scheda meno il carry-over; bonus della carica ricalcolato; can… |
| `MASTER-DEF` | D9 | giro | Fauci di Palude: la versione F (si schianta ai round 18-20 e duella coi PG, Thorik in punta), quella di A e B (fugge al round 5 e lo combattono i PNG) o un ibrido (fugge sotto i 50 pf, salvo che i PG lo inseguano in vol… |
| `MASTER-DEF` | D10 | giro | Le schede che mancano (bugbear, guardie orog di Grimjaw, gufi giganti): aggiungerle a `Bestiario/mostri/` dall'SRD, o sostituirle con schede che esistono? Consigliata: aggiungerle dall'SRD (giro del 2026-10-19,… |
| `MASTER-DEF` | D11 | giro | Quando arriva Grimjaw nel 3B: al round 12 con un corno al round 11, ai round 9-10 insieme ai PG, o ai round 14-15? Consigliata: round 12 col corno all'11 (giro del 2026-10-19, `esperimenti/giro-arc08-2026-10-19/FIX.md`) |
| `MASTER-DEF` | D12 | giro | Re Thorek morente: Guarigione CD 25 a ogni round finché nessuno lo cura per magia, e tre fallimenti lo uccidono, oppure la morte per scelta del DM? E Dana, 20 pf e un muro o metà delle risorse? Consigliata: il tiro (gir… |
| `MASTER-DEF` | D13 | giro | Dalla caverna ai bastioni: mezza giornata senza riposo lungo (il default scritto), oppure un riposo di 8 ore e gli scontri della Sessione 4 alzati? Si aggiunge l'elenco delle unità nemiche ancora in campo, che il Regist… |
| `MASTER-DEF` | D14 | giro | La tempesta della 4A: Orion lancia *controllare il tempo* prima della battaglia, con una deroga dichiarata per gli arcieri alleati; solo vento violento; o la tempesta piena dell'SRD, senza attacchi a distanza? Consiglia… |
| `MASTER-DEF` | D15 | giro | Il cavaliere di Fauci: tre cose che sa e un blocco «Se lo divinano», scritti dopo D9, oppure muore o tace? Consigliata: scriverli (giro del 2026-10-19, `esperimenti/giro-arc08-2026-10-19/FIX.md`) |
| `MASTER-DEF` | D16 | giro | Lythiel cavalca coi gufi e riconosce Hella in Sessione 4, come dice lo stato del gruppo, oppure il riconoscimento slitta alla Cerimonia? Consigliata: lo stato del gruppo (giro del 2026-10-19,… |
| `MASTER-DEF` | D17 | giro | I 210 caduti: 118 + 92, coi 9 di Drellin's Ferry nominati nel Giuramento ma non contati, e i superstiti dal Registro PFU; oppure il numero sale a 219? Consigliata: 210 (giro del 2026-10-19,… |
| `MASTER-DEF` | D18 | giro | La serata: il 3B e la Sessione 4 insieme e la Cerimonia la serata dopo (il default scritto), oppure solo il 3B? Consigliata: il default (giro del 2026-10-19, `esperimenti/giro-arc08-2026-10-19/FIX.md`) |
| `MASTER-DEF` | D19 | giro | EL e PE del 3B e della 4A: l'Appendice C (2.600 e 4.600 PE al gruppo) togliendo l'EL 17 dichiarato, o l'EL 17 con lo scontro reso davvero tale? Poi le righe di scala. Consigliata: l'Appendice C (giro del 2026-10-19,… |
| `MASTER-DEF` | D20 | giro | Il box dell'Atto 2 della Cerimonia: due figure venute da fuori e non insieme, come dicono le note per il DM dello stesso file, oppure le tre figure coordinate del box originale? Consigliata: due (giro del 2026-10-19,… |
| `RECUPERO` | D3 | L5 | **`RIPRESA-PR#D2` e la #106**: il collaudo SDXL accanto a Gemini tiene aperta la #106 da otto settimane, e il suo codice è già su `main` in forma nuova. La #230 installa ComfyUI e scarica SDXL sulla tua Debian 13. *Prop… |
| `RECUPERO` | D4 | L5 | **`RIPRESA-PR#D11` (ADR-0049, l'AP originale)**: resta aperta dal 2026-09-11, legata a un avvocato IP e a VENDIBILITA, che non è autorizzato. *Proposta*: passa a voce di `adozioni-in-attesa.json` con la condizione «VEND… |
| `RECUPERO` | D5 | L4 | **I ⬜ opzionali dei piani chiusi o fermi**, per gruppo. *Proposta*: (a) chiusi come «non si fa»: AUDIT-SCRIPTS (shellcheck lo fa AMBIENTE A6), IMPORT-ULTRACLEAR (migrazione delle ~30 mappe, ora COLLAUDO-MAPPE), RENDER-F… |
| `RECUPERO` | D6 | L3 | **RICONCILIAZIONE-PR-APERTE si chiude come superato?** R3, R6, R7, R8 sono decisi o fatti altrove (§2.3). *Proposta*: sì, ✅ con il rimando a dove sta ognuno |
| `RIPRESA-PR` | D2 | F3 · 3d | **Riformulata il 2026-09-11: la domanda di prima partiva da un fatto falso.** Diceva *«i diciotto raster si generano sulla tua macchina — quando?»*, ma **esistono tutti e diciotto** (più le due extra), generati dal DM *… |
| `RIPRESA-PR` | D11 | F4 · 4b | **L'ADR ex-0018 della #72: recuperato il 2026-09-11 come [ADR-0049](plans/adr/ADR-0049-edizione-commerciale-ap-originale.md), e resta 🔵 *proposta* — non accettata.** Dice che, *se e quando* si pubblica, si pubblica un *… |

### Revisioni della prosa da approvare: 0

Fonte: i documenti `REVISIONE-*.md` sotto `plans/scrittura/` che `ciclo_prosa.py applica` può ancora applicare. Ogni cartella ha un `LEGGIMI.md` con i passaggi interi.

Nessuna.

## ▶ In corso: da qui si riparte: 7

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **Le PR aperte al 2026-10-10, dopo il merge di #229, #230 e #232, e cosa resta a ciascuna** *(rimisurate con `git merge-tree` su `e63fddd5`)*: **#216** la revisione della prosa (D13, D17, D38, la *Torre*, `MEMORIA.md`):… | [PIANO-RECUPERO](plans/PIANO-RECUPERO-DECISIONI-E-REVISIONI-INCOMPIUTE-2026-10.md) §2.6 · RIPRESA-PR | DM: il merge della PR del riallineamento e della #231, poi D3-D7 di RECUPERO |
| **Il giro 4 di conferma su DEF-4**; poi DEF-5. Le decisioni D35-D37 e D49-D63 sono applicate *(2026-10-12, PR #239)*; restano al DM D64-D68, i dettagli lasciati `[INFERRED]` | [LETTORE-E-PLAYTESTER](plans/PIANO-LETTORE-E-PLAYTESTER.md) F3-quinquies | DM, poi agente |
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
| 2026-10-19 | MASTER-DEF | giro su ARC-08 dal 3B alla Cerimonia con lo standard di ADR-0094 (richiesta del… | 🟡 74 🔴/🟠: 37 corretti, 35 al DM, 1 respinto, 1 residuo; verifica 0 aperti; D9-D20 al DM; `esperimenti/giro-arc08-2026-10-19/` |
| 2026-10-18 | MASTER-DEF | A4, D7 e D8 decise dal DM (prima le sette pratiche; SRD locale e lettori uno al… | 🟢 A4 fatto; ARC-08 a zero conti sbagliati, nove trovati sulla versione di prima della #241 |
| 2026-10-18 | MASTER-DEF | A4, lo standard del giro: audit dei giri su ARC-07 contro le norme del repo (ri… | 🟡 [ADR-0094](plans/adr/ADR-0094-il-giro-ha-correzione-verifica-e-seconda-passata.md) proposta, 58 pratiche e nove lacune in… |
| 2026-10-18 | TRASVERSALE | Creature della Mano Rossa nel Bestiario come canone | ✅ abishai azzurro, Spezzamente, lucertola del tuono e Furia della Mano spostati in `Bestiario/mostri/` come ACCEPTED (richiesta del DM); il file di ARC-09 dive… |
| 2026-10-18 | MASTER-DEF | rifacimento di stile e struttura dei cinque master di ARC-07 e secondo giro di… | 🟡 [`esperimenti/giro2-arc07-2026-10-18/`](plans/esperimenti/giro2-arc07-2026-10-18/README.md): 🔴+🟠 da 120 a 104, i 🔴 da 2 a 6 ma sono tre difetti di regola che… |
| 2026-10-18 | TRASVERSALE | Creature della Mano Rossa ispirate alla WE di RHoD (ARC-09) | 🟡 proposta: abishai azzurro, Spezzamente, lucertola del tuono, Furia della Mano in `Arco-Post-Hammerfist-CREATURE-MANO-ROSSA-STATBLOCCHI.md`, versione più fort… |
| 2026-10-18 | AVVENTURE-COMMUNITY | Lotto 1 (alto livello e statblocchi) | ✅ ricerca sulle avventure della community (quattro filoni, note in `plans/esperimenti/avventure-community/`); §9-§16 del developer; D9, D10, D15, D16 in… |
| 2026-10-18 | MASTER-DEF | nuovo giro sui cinque master di ARC-07: developer, playtester e DM a freddo su… | 🟡 [`esperimenti/giro-arc07-2026-10-18/`](plans/esperimenti/giro-arc07-2026-10-18/README.md): 15 letture, 120 🔴+🟠 sui master di partenza, nessuno resta aperto s… |
| 2026-10-18 | REVISIONE-LIBRERIA-MOSTRI-PNG-VILLAIN | le `[PROPOSTA]` di gioco diventano canone: tenda di Zog'tar (M7C), metà sud del… | ✅ zero `[PROPOSTA]` aperte nel contenuto |
| 2026-10-16 | MASTER-DEF | le versioni di ARC-08 censite sezione per sezione e mappa per mappa; i sei file… | 🟡 D6 aperta al DM |
| 2026-10-16 | REVISIONE-LIBRERIA-MOSTRI-PNG-VILLAIN | le schede nominate prendono la versione più forte fra Bestiario e moduli d'arco… | 🟢 ADR-0091 §4-bis. Una sessantina di schede rifatte: tredici file rinominati perché il GS è cambiato (per esempio Azarr Kul 15 → 17, Karruk 10 → 13, i due coma… |
| 2026-10-15 | MASTER-DEF | A3, il canone di ARC-08 contro il tavolo: lettura in sola lettura dei file vivi… | 🟡 43 punti; D4 e D5 aperte al DM |

## Le misure che si portano dietro

- **Decisioni**: 29 aperte, 264 chiuse (`decisioni_dm.py`).
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
