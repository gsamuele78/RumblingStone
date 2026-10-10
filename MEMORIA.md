# 🧠 MEMORIA — il lavoro su RumblingStone in un posto solo

> **Generata da `scripts/memoria.py`: non si scrive a mano** ([ADR-0086](plans/adr/ADR-0086-la-memoria-del-lavoro-e-generata.md)). Ogni riga viene da una fonte che ha la sua casa, e il link porta lì: si corregge la fonte, poi `python3 scripts/memoria.py`. La CI boccia questo file se resta indietro.

## Come si riparte, in una sessione nuova

```bash
git fetch --prune origin
python3 scripts/memoria.py --check      # questa pagina è allineata?
python3 scripts/decisioni_dm.py --check # le decisioni aperte
python3 scripts/fase1.py <file>         # sempre, prima di toccare
```

Poi si legge questa pagina dall'alto: prima cosa aspetta il DM, poi da dove riparte l'agente. Le regole di lavoro stanno in [`AGENTS.md`](AGENTS.md).

## Aspetta il DM: 14 decisioni aperte

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
| `RIPRESA-PR` | D2 | F3 · 3d | **Riformulata il 2026-09-11: la domanda di prima partiva da un fatto falso.** Diceva *«i diciotto raster si generano sulla tua macchina — quando?»*, ma **esistono tutti e diciotto** (più le due extra), generati dal DM *… |
| `RIPRESA-PR` | D11 | F4 · 4b | **L'ADR ex-0018 della #72: recuperato il 2026-09-11 come [ADR-0049](plans/adr/ADR-0049-edizione-commerciale-ap-originale.md), e resta 🔵 *proposta* — non accettata.** Dice che, *se e quando* si pubblica, si pubblica un *… |
| `RICERCA-MESTIERE` | D12 | §6-bis | 🐛 **`Portale-Forgia-L2` mappa 2 ha una riga `17` duplicata** — una alla riga 290 del sorgente, una alla 297. Quale delle due debba portare un altro numero (19? 24?) lo sa solo chi ha disegnato l'arena circolare: **indov… |

### Revisioni della prosa da approvare: 4

Fonte: i documenti `REVISIONE-*.md` sotto `plans/scrittura/` che `ciclo_prosa.py applica` può ancora applicare. Ogni cartella ha un `LEGGIMI.md` con i passaggi interi.

| Documento | Originale | Modifiche | Spuntate |
|---|---|---:|---:|
| [`REVISIONE-ARC08-11-PONTE-ARRIVO-r1.md`](plans/scrittura/revisioni-pilota-ARC08/REVISIONE-ARC08-11-PONTE-ARRIVO-r1.md) | `08_La Battaglia Di Hammerfist/ARC08-11-PONTE-ARRIVO.md` | 3 | 0 |
| [`REVISIONE-ARC08-15-HANDOUTS-GIOCATORE-r1.md`](plans/scrittura/revisioni-pilota-ARC08/REVISIONE-ARC08-15-HANDOUTS-GIOCATORE-r1.md) | `08_La Battaglia Di Hammerfist/ARC08-15-HANDOUTS-GIOCATORE.md` | 2 | 0 |
| [`REVISIONE-Cerimonia-delle-100-Asce-r1.md`](plans/scrittura/revisioni-pilota-ARC08/REVISIONE-Cerimonia-delle-100-Asce-r1.md) | `08_La Battaglia Di Hammerfist/Cerimonia-delle-100-Asce.md` | 5 | 0 |
| [`REVISIONE-hammerfist_encounters-r1.md`](plans/scrittura/revisioni-pilota-ARC08/REVISIONE-hammerfist_encounters-r1.md) | `08_La Battaglia Di Hammerfist/hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md` | 3 | 0 |

## ▶ In corso: da qui si riparte: 6

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **Il giro 3 delle letture su DEF-4**, con le mappe nuove, **un subagente alla volta**; poi DEF-5 | [LETTORE-E-PLAYTESTER](plans/PIANO-LETTORE-E-PLAYTESTER.md) F3-quinquies | agente, sessione nuova |
| **Le `[PROPOSTA]` e gli `[INFERRED]` degli altri archi**, un lotto alla volta: 568 in tutto il repo, circa 400 nel contenuto | §12.1 | agente: il prossimo lotto è ARC-08 (32), poi ARC-09 (53), `campaign/` (50), `PG/` (22), il Bestiario (212) per ultimo perché è il più grande |
| **Le regole di 3.5 fuori rete**: gli incantesimi nelle esportazioni PCGen di `Bestiario/pregen-pcgen/` | §8.3 | agente: una riga in `dnd-35-srd/references/resources.md` e la sua voce nel registro delle norme |
| **DEF-1, 2, 3 nella forma del ciclo** *(30 settembre, sera)*: passi 1-4 fatti (scene, contratto, schede, apparati), box letti al tavolo invariati. Letture cieche: DEF-1 lettore 🔴 2, DEF-2 🔴 2 + 2, DEF-3 🔴 1 + 2, DEF-1 p… | LETTORE F4 · `esperimenti/f4-def1-def3/` | DM: D35 (il rito che va male), D36 (sei rilievi di regole), D37 (la Sentinella); D34 e D9 sono decise. Poi agente: applica e rilegge |
| **ARC-07 al ciclo completo** *(30 settembre)*: DEF-5 ai passi 1-6 (tre scene col contratto, schede di Re Thorek e Madre Dana, box al metro, letture a freddo prima e dopo). Restano il passo 7 di DEF-5 (il quiz, D10) e DE… | [LETTORE](plans/PIANO-LETTORE-E-PLAYTESTER.md) F4 | agente: DEF-1 (Varis), poi DEF-2 e DEF-3, `fase1.py` prima di ognuno; una scena già letta al tavolo si converte nella forma, non si riscrive |
| **Il giro delle quattro letture** *(30 settembre, notte)*: lettore, playtester, developer e il DM a freddo (rubrica nuova) su DEF-4 e DEF-5; la procedura è il passo 6 del ciclo in `module-standard`. Giro 1: DEF-5 🔴 2 →… | LETTORE F4 · `esperimenti/giro-def4-def5/` | DM: D38, D39, D40; agente: lotto mappe D28, poi il giro 2 |

## 🙋 Aspetta il DM: 10

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **Al DM: il lotto D13 e la D17 di AGENT-SKILLS** *(dalla #206)*: undici documenti di revisione, 23 modifiche applicabili con `ciclo_prosa.py applica --auto` e quattro da guardare; la D17 decide se i box con «sembra» seg… | `plans/scrittura/revisioni-D13/LEGGIMI.md` · §14.4-bis | DM: approvare il lotto, rispondere alla D17; agente: `applica` e rimisura |
| **Al DM: quattro incoerenze di canone** trovate dalle corse di L11 e L12 *(dalla #206)*: il carry-over su Fauci nell'handout di DEF-5 §9, le pozioni antiche fra DEF-4 §6 e DEF-5 §0-bis, il «−2 COS» di Thorik in… | `plans/scrittura/RISULTATI.md` «Cosa hanno trovato le corse» | DM: quale versione vince, una riga per incoerenza |
| **Al DM: le D1-D6 di BOX-DI-LUOGO** *(dalla #206)*: il tetto del box di luogo, le dimensioni nella prima frase, il tipo del box, i box già giocati, l'Abbazia *keyed*, il template d'area | [BOX-DI-LUOGO](plans/PIANO-BOX-DI-LUOGO-E-AREA-CHIAVE.md) | DM; poi la chat editoriale di quel piano, da B1 |
| **Al DM: le quattro revisioni della prova sull'ARC-08** (13 modifiche, segnalazioni da 11 a 5, MQM su in tre file su quattro) | `plans/scrittura/revisioni-pilota-ARC08/LEGGIMI.md` | DM: spuntare e `applica`; poi l'agente fa il lotto di `ARC08-01-GUIDA-DM` (55 segnalazioni) |
| **Al DM: la bozza del Caos Ultimo** (D13) e due righe per `state.md` sul ramo del gruppo: RD del Manto 5/epico e male, *Fortezza Mentale* di Artemis | `04_Anello_S3_Caos_Ultimo_DM.html` · audit §7-bis | DM: approvare o correggere la bozza; `dm.py session end` per `state.md` |
| **Al DM: chiudere la serata del 2026-09-25.** In `campaign/sessions/` non c'è ancora il log: cosa è successo al tavolo lo sa solo il DM | regia della serata §6 (il registro) · `rumblingstone-automation` | `python3 scripts/dm.py session end` sul ramo `campaign-group-rumblingstone-dm-gianfranco`, mai su `main` (ADR-0007) |
| **Al DM: le marcature `[INFERRED]` di DEF-4 e DEF-5**: erano 44 in DEF-4 il 30 settembre, il 2026-10-07 sono 51 in DEF-4 e 12 in DEF-5 (`grep -c INFERRED`), fra cui il livello e il prezzo delle rune di Zeth, il +15 di K… | `ARC07-DEF-4` (cercare `INFERRED`) | DM: confermare in blocco o correggere; l'agente toglie la marcatura |
| **D27** *(30 settembre, sera)*: il messaggio del DM del 2026-09-27 si interrompe a «considera che i…». La D26 è fatta: il registro delle letture a freddo è `registro_letture.py`, in CI, lotto L4 di AGENT-SKILLS (#193) | §4 | DM: D27 |
| **Al DM: D35, D36, D37** *(30 settembre, sera)*: il rito di DEF-3 quando va male; sei rilievi di regole; la Sentinella di DEF-1. Ognuna con la proposta | §4 | DM: rispondere col numero |
| **Al DM: `state.md` e il Rubino**: §6 lo dà «speso»; ora si usa una volta sola, resta nell'incasso, e dopo l'uso la Corona è intera, +3 e Senzienza (D6). E il log delle serate del 25-27 settembre | `campaign/state.md` §6 · `campaign/sessions/` | `dm.py session end` sul ramo del gruppo, mai su `main` (ADR-0007) |

## ⬜ Da fare, nell'ordine dei piani: 12

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **Drappo L9, il collaudo**: lettore e playtester a freddo sul §2-bis (passo 6 di ADR-0075, rubrica di LETTORE F5), dry-run cronometrato (sta in cinque minuti per taglio?), poi il tavolo. Il booklet `DRAPPO-BOOKLET-DM` è… | DRAPPO Lotto 9 | agente: due agenti che non vedono il piano; poi il DM al tavolo |
| **L'ambiente riproducibile: la macchina come la CI** *(ordine del DM, 2026-10-08; D1-D11 decise)*. La CI è lo standard e la macchina combacia: versione e checksum di ogni binario nel registro, Python 3.13 ovunque, lock… | [AMBIENTE-RIPRODUCIBILE](plans/PIANO-AMBIENTE-RIPRODUCIBILE.md) ·… | agente, dopo D28: A1, un ramo e una PR per lotto. |
| **I residui d'apparato del Palio (26) e del Drappo (43)**: patch a `state.md`, procedura degli stemmi, mappa dei file dell'hub. Cosa è apparato in un modulo autonomo | CICLO-SESSIONE 2g · `scripts/apparato-residui.json` | agente con il DM: una domanda per gruppo, poi i marcatori, poi si abbassa il tetto |
| **Il rilevatore dei box non apre le battute etichettate** (`> **2 di 3 — …** *…`, la forma di Balvar in `DEF-4`): `--box`, `--p1` e `validate_corredo` misurano la prima battuta e non le altre | `misura_craft.box_read_aloud` | agente: allargare l'apertura del box e rimisurare; il denominatore di `--p1` sale, i 22 residui vanno riverificati uno per uno |
| **Le 120 legature della Corona** (`aﬀresco`) | §10.1 | agente: prima si conta in tutto il repo, poi si decide se è un lotto o uno per file; qualità: nessuna legatura, nessun'altra riga cambiata |
| **Due residui editoriali minori**: l'ultima riga dell'indice delle 48 aree dell'Abbazia cade sola a pagina 35; il Palio stampa «Naviga i capitoli qui sopra», che è una frase della catena HTML | §11.3 | agente: il primo si prova con una soglia di righe per pagina, il secondo va tolto dall'introduzione del manifest solo nella stampa |
| **PI-6**, **PI-2**, **PI-5**, **PI-4** (dopo CICLO D6) | PRATICHE §5 e §8 | in quest'ordine, una PR ciascuno |
| **Ciclo di sessione e menu**: Fase 0, poi F1-F4. **D1-D6 decise il 2026-09-30**: la cronaca si aggiorna da sola, le alleanze sono un dato, la prosa la scrive l'agente con le skill, menu numerato, le immagini si elencano… | [CICLO-SESSIONE](plans/PIANO-CICLO-DI-SESSIONE-E-MENU.md) §5 | agente: la Fase 0 |
| **RIPRESA-PR 4g e 4h**; PR aperte #99 e #106 | RIPRESA-PR | `python3 scripts/contenuti_nei_rami.py --fetch` |
| **🧲 e 🤖**, e la nota locale di una mappa che non arriva nella legenda | [RENDER-MAPPE-FEDELTA](plans/PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md) §1 · §9.3 | prima si legge che cosa vuol dire il simbolo in ogni mappa che lo usa |
| **A3 di MASTER-DEF**: il canone di ARC-08 contro lo stato del tavolo, dopo F4 | MASTER-DEF A3 | agente, poi conferma del DM |
| **Il lotto mappe D28**: sezione a livelli di Hammerfist nel 372 (più si scende, più le sale sono ampie, come Erebor) e griglie da 1,5 m di fucina, gallerie, alchimista, cappella e armeria, coerenti con le Scene 4-5 già… | LETTORE F3-bis | agente con `rumblingstone-mapmaking`; prima `fase1.py` sulle mappe M7 di ARC-07 |

## 🟡 Fatto a metà: 3

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **I sette ritratti e le otto tavole sono nel repo** (#172, Canva AI). Restano: gli originali a piena risoluzione al posto delle copie da chat a 533 × 800, e Skullcrusher nel cortile, dove il cane di Hella è sbagliato; i… | `Immagini/PROMPT-RITRATTI-E-TAVOLE-ARC07.md` §4 | DM: esportare da Canva gli originali, stesso nome di file |
| **PI-3, il resto**: la prova del blocco dei segreti (DM), la revisione con l'IA. Le PR di Dependabot su `origin` (#207-#212, dal 2026-10-02) si fondono una alla volta il 2026-10-07, e con le tre azioni alla v7 si chiude… | PRATICHE PI-3 · §15.3 | DM: la prova del segreto |
| **PI-1 · 4i-3**: la prova della prima PR indietro rispetto a `main` | RIPRESA-PR §4.11.6 | la prima PR che resta indietro |

## Fatto di recente: le ultime 12 righe del CHANGELOG

Fonte: [`plans/CHANGELOG.md`](plans/CHANGELOG.md), una riga per lotto chiuso.

| Data | Piano | Lotto | Esito |
|---|---|---|---|
| 2026-10-10 | STATO-E-ORDINE | la memoria in un posto solo (ADR-0086) | ✅ Richiesta del DM: tutta la memoria in un posto, senza perdere parti o decisioni; il DM sceglie «nel repo, generata». `MEMORIA.md` in radice, generato da… |
| 2026-10-09 | RESA-E-ASSET-DELLE-MAPPE | D17-D18 · R4-ter pianificato | ⬜ Il DM chiede se servono oggetti di scena da fonti CC0. Misura: 46 simboli-oggetto usati su 61, i mobili rari; Poly Haven (521 modelli CC0), Quaternius (CC0,… |
| 2026-10-09 | RESA-E-ASSET-DELLE-MAPPE | D16 · R4-bis chiuso: texture vere e velatura | ✅ Il DM scarica le 11 texture CC0 (MD5 verificato) e committa i 53 SVG del tema. Il primo push aveva solo l'indice: il `.gitignore` escludeva tutti i `*.webp`,… |
| 2026-10-09 | RESA-E-ASSET-DELLE-MAPPE | D13-D15 · R4-bis il tema texture CC0 | ✅ Il DM chiede una strada senza problemi di licenza: lette alla fonte Poly Haven e ambientCG (CC0 1.0), Dungeon Crawl (libera, pixel art), 2-Minute Tabletop (C… |
| 2026-10-09 | RESA-E-ASSET-DELLE-MAPPE | D9-D12 · R4 installatore · R5 l'assedio di Dauth | ✅ Il DM decide dopo aver chiesto a cosa servono R4, R5 e R6: R4 una prova su una mappa, R5 da Dauth, R6 in attesa, al tavolo Foundry. Letta la licenza di 2-Min… |
| 2026-10-08 | COLLAUDO-E-GENERAZIONE-MAPPE · RESA-E-A… | D12 · le mappe della #225 al set nuovo; D6-D8, D10, D19 | ✅ Il DM chiude le sei decisioni aperte. D12 eseguita: nei sei contratti JSON di M7-D, M7-E, M7-F le cinque `🪜` diventano `🔼`/`🔽` con la gemella (campo… |
| 2026-10-08 | COLLAUDO-E-GENERAZIONE-MAPPE | V2 · la categoria · scipy | ✅ D17: scipy per M1 e M2 nel collaudo (20 ms contro 105, risultato identico), obbligatoria come tcod; emendamento di ADR-0084. D18: `@tipo <tipo> <ambiente>` s… |
| 2026-10-08 | RESA-E-ASSET-DELLE-MAPPE | R0-R3 · piano aperto, resa uniforme | ✅ Aperto il piano, con ADR-0085, dopo la richiesta del DM di rimisurare le librerie scartate e cercare asset e generatori per ogni categoria. R0: le cinque lib… |
| 2026-10-08 | COLLAUDO-E-GENERAZIONE-MAPPE | V2-quater · le dipendenze misurate | ✅ Sei candidati misurati sul corpus (`plans/esperimenti/orientamento-e-dipendenze-2026-10/`). Solo `tcod` vince: M4 da tutte le 43.423 celle in 0,6 s contro 69… |
| 2026-10-08 | COLLAUDO-E-GENERAZIONE-MAPPE | V2-quater · l'asse delle chiusure | ✅ Audit in sola lettura: delle 125 chiusure del corpus 36 stanno in muri nord-sud e il renderer le disegnava di traverso; `export_uvtt` girava 13 portali su 96… |
| 2026-10-08 | COLLAUDO-E-GENERAZIONE-MAPPE · STATO-E-… | l'ordine nuovo del DM, prima degli altri | ⬜ Riga ▶ nuova in STATO-E-ORDINE e V2-quater nel piano: porte, grate e celle orientate nel verso giusto, controllate dal collaudo e disegnate dal renderer; gli… |
| 2026-10-08 | COLLAUDO-E-GENERAZIONE-MAPPE | il test che perdeva la corsa con git | ✅ `test_gruppo_nuovo` falliva due run su cinque all'uscita del `TemporaryDirectory` (`Directory not empty: 'objects'`). Causa: da git 2.54 la manutenzione dopo… |

## Le misure che si portano dietro

- **Decisioni**: 14 aperte, 196 chiuse (`decisioni_dm.py`).
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
