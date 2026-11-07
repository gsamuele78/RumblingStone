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

## Aspetta il DM: 18 decisioni aperte

Fonte: le tabelle `decisioni-dm` dei piani, aggregate in [STATO-E-ORDINE §4](plans/STATO-E-ORDINE-DEI-PIANI.md). Si risponde col numero e il piano: *«CODA-SECONDO-LETTORE D2 sì»*.

| Piano | # | Ambito | Domanda |
|---|---|---|---|
| `INVENTARIO-GEMINI-AISTUDIO` | D1 | `battle_stats_maps.md`: Spaventadraghi,… | Si riprende come proposta in ARC-08 (MASTER-DEF), con le regole confrontate con l'SRD; quello che diverge da ADR-0091 resta fuori. |
| `INVENTARIO-GEMINI-AISTUDIO` | D2 | I tre mini-boss di «Branch of Sistema C… | Restano fuori finché il DM non dice se Tiamat è mai stato canone; i mini-boss possono entrare nel Bestiario come proposta. |
| `INVENTARIO-GEMINI-AISTUDIO` | D3 | Il «Manuale da campo del DM» e il «Gior… | Si confrontano con `ARC08-01` quando si scrive il master definitivo di ARC-08. |
| `INVENTARIO-GEMINI-AISTUDIO` | D4 | Statblocchi alternativi di «Organizing… | Restano fuori: le schede canone sono quelle di ADR-0091. |
| `INVENTARIO-GEMINI-AISTUDIO` | D5 | «Red Hand of Doom 3.5 Conversion» | Si legge come fonte di idee per ARC-09, senza importare nulla. |
| `INVENTARIO-GEMINI-AISTUDIO` | D6 | Le chat non scaricate (§5), le sette no… | Secondo giro solo se il DM esporta le chat dell'app Gemini o mette i file grandi in `/mnt/project-files/`. |
| `BOX-LUOGO` | D2 | B0 | **Le dimensioni nella prima frase del box** («camera quadrata di quaranta piedi»), come nel modello del 2026-10-01, o il paragone di ADR-0014 con le misure nei Dati per il DM? Proposta: resta ADR-0014. Dal modello ester… |
| `BOX-LUOGO` | D3 | B2 | **Ogni box dichiara il suo tipo?** Per esempio `**Read-aloud (luogo · Salvatore lead).**`, con i tipi luogo, ingresso, round, rivelazione, chiusura. Sblocca la norma «niente creature nel box di luogo» e le soglie per ti… |
| `BOX-LUOGO` | D4 | — | **I box già giocati fuori dalle nuove misure**: nei DEF di ARC-07, 27 box oltre i 500 caratteri e 61 oltre le quattro frasi. Proposta: non si toccano, come per D9 di PIANO-LETTORE: si spezzano solo se lo chiedi, e senza… |
| `BOX-LUOGO` | D5 | B5 | **L'Abbazia con le stanze *keyed*** (è la F5 di PIANO-LETTORE, «decidere col DM se ogni stanza vuole un box»). Proposta: sì, un box di luogo breve per stanza nell'ordine di *Dungeon*, quando F5 tocca l'Abbazia; è il ban… |
| `BOX-LUOGO` | D6 | B1 | **Il template d'area va in `campaign/templates/`**, accanto a quelli di sessione e di mappa, in due versioni (3.5 e PF1e)? Proposta: sì, tutte e due, con la creatura sempre come rimando al Bestiario e mai trascritta |
| `CODA-SECONDO-LETTORE` | D2 | 3 | **Il campo *Etichetta regia* troncato in `PROMPT-IMMAGINI-07ILP.md`**: si cerca chi compila il file e si corregge lì, o si correggono a mano le 32 righe? *Proposta*: prima si cerca il generatore (`extract_scene_prompts`… |
| `CODA-SECONDO-LETTORE` | D3 | 4 | **La *d* eufonica** (*legato a Aegis Fang*, *a area*): la vuoi come norma? *Proposta*: sì, *ad* solo davanti alla stessa vocale, scritta in `editorial-standards.md` e misurata; se no, resta com'è |
| `MASTER-DEF` | D6 | A3 | Le domande del censimento delle versioni (D1-D4, D6-D15 nel file, le consigliate fra parentesi): soffio di 2B su Riflessi; PF di Fauci dal massimo della sua scheda meno il carry-over; bonus della carica ricalcolato; can… |
| `RECUPERO` | D5 | L4 | **I ⬜ opzionali dei piani chiusi o fermi**, per gruppo. *Proposta*: (a) chiusi come «non si fa»: AUDIT-SCRIPTS (shellcheck lo fa AMBIENTE A6), IMPORT-ULTRACLEAR (migrazione delle ~30 mappe, ora COLLAUDO-MAPPE), RENDER-F… |
| `RECUPERO` | D6 | L3 | **RICONCILIAZIONE-PR-APERTE si chiude come superato?** R3, R6, R7, R8 sono decisi o fatti altrove (§2.3). *Proposta*: sì, ✅ con il rimando a dove sta ognuno |
| `RIPRESA-PR` | D2 | F3 · 3d | **Riformulata il 2026-09-11: la domanda di prima partiva da un fatto falso.** Diceva *«i diciotto raster si generano sulla tua macchina — quando?»*, ma **esistono tutti e diciotto** (più le due extra), generati dal DM *… |
| `RIPRESA-PR` | D11 | F4 · 4b | **L'ADR ex-0018 della #72: recuperato il 2026-09-11 come [ADR-0049](plans/adr/ADR-0049-edizione-commerciale-ap-originale.md), e resta 🔵 *proposta* — non accettata.** Dice che, *se e quando* si pubblica, si pubblica un *… |

### Revisioni della prosa da approvare: 0

Fonte: i documenti `REVISIONE-*.md` sotto `plans/scrittura/` che `ciclo_prosa.py applica` può ancora applicare. Ogni cartella ha un `LEGGIMI.md` con i passaggi interi.

Nessuna.

## ▶ In corso: da qui si riparte: 5

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P01 · MASTER-DEF: A3 chiuso, D4 e D5 decise** (#259, ARC-08: il collo e l'ala nella presa di Thorik, ADR-0096) | [MASTER-DEF](plans/PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md) A3 | merge della #259 quando il thread dà il via; poi S1-S4 |
| **P02 · AVVENTURE-COMMUNITY 7c**: D4-D6 decise dal DM il 2026-10-23 e applicate (ARC-08 allineato al Bestiario nella #286, possessivo vietato solo sul corpo, fronti e orologi canone da ARC-08). Resta il primo… | [AVVENTURE-COMMUNITY](plans/PIANO-AVVENTURE-COMMUNITY-2026-10.md) §Decisioni | il thread di ARC-08, col prossimo master |
| **P03 · ARC-07 riscritto con le norme nuove**, misurato contro le versioni di prima (tag `prima-rifacimento-arc07`), e l'handout del contratto del Seme da portare in `ARC07-HANDOUTS` | ADR-0093 · `/mnt/project-files/contratto-seme/` | il thread |
| **P04 · LLM locale, la prova del 12B sull'ASUS e del 26B sulla Dell** (gemma4 e4b bocciato, #234 su `main`) | [ADR-0089](plans/adr/ADR-0089-un-llm-locale-per-la-prosa-si-misura-prima.md) · `plans/scrittura/` | una PR nuova dal thread |
| **P16 · Le marcature rimaste nel contenuto**: rimisurate il 2026-11-04 con `inventory_inferred.py` corretto (righe di regola in «meta», note che vanno a capo contate): **240 aperte su `main`**, non 44 (il `grep` vedeva… | … | le card di ARC-08, poi un lotto per arco: ARC-07, ARC-09, il resto |

## 🙋 Aspetta il DM: 11

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P05 · Lo schedario dei PG, la seconda parte della 4g-2**: la #99 è chiusa (2026-10-24, ADR-0088 accettata, scelta A); 4g-1 su `main` con la #278; i tre pezzi rimasti ripresi con la #289; la prima parte della 4g-2 su… | [RIPRESA-PR](plans/PIANO-RIPRESA-PR-ABBANDONATE.md) F4 §4.13 «4g-2, prima parte» | i nove valori dal DM |
| **P06 · Accettare le ADR ancora «proposta»**: ADR-0090 (la partita sul ramo di gruppo nuovo, dal 2026-10-11), ADR-0094 (il giro si misura contro la versione di prima), ADR-0095 (correzione, verifica e seconda passata).… | `plans/adr/` | un sì o un no per ADR; l'agente cambia lo stato e la riga di CHANGELOG |
| **P07 · Le decisioni numerate dei piani**: BOX-DI-LUOGO D2-D6, CODA-SECONDO-LETTORE D2 e D3, MASTER-DEF D6 (il censimento delle versioni), RECUPERO D5 e D6, RIPRESA-PR D2 (Gemini o SDXL per il Drappo, con la #106) e D11… | §4, generata da `decisioni_dm.py` | rispondere col piano e il numero: *«BOX D2 sì»* |
| **P08 · Le patch di `state.md` sul ramo di gruppo**, scritte e mai applicate (verificato su `ce34599`): il Bane di Aegis Fang contro Fauci (affresco A7); la Cintura della Devastazione a 4 cariche al giorno (lo stato dic… | `/mnt/project-files/ramo-di-gruppo-2026-11-05/` (serie unica 0001-0004, provata su `ce34599` il 2026-11-05: ingloba le… | `git am --3way` sul ramo `campaign-group-rumblingstone`, passi in `docs/guides/GUIDA-PATCH-RAMO-DI-GRUPPO.md` |
| **P09 · Le domande di canone lasciate aperte dai thread di ARC-07 e ARC-08**: i pf di Terros (345 o 348 con Robustezza); *Virata* da riscontrare su d20srd; la portata del sussurro della Catena… | `plans/esperimenti/giro4-arc07-2026-10-19/DECISIONI-DM.md` · `DEF-4` · `ARC08` | una risposta per domanda; l'agente le porta nei master in una PR |
| **P10 · Mappe, le scelte del DM**: texture e tessere nella pagina di scelta (R8, livello B), la prima immagine di ComfyUI (R4-quinquies), il giro di prova sui modelli 3D CC0 e lo zip Standard di Quaternius (R4-ter), il… | [RESA-ASSET](plans/PIANO-RESA-E-ASSET-DELLE-MAPPE.md) §8 · [COLLAUDO-MAPPE](plans/PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) | DM; poi l'agente mette le tessere nel tema e rimisura |
| **P11 · I collaudi che solo il DM può fare**: l'import `.uvtt` in Foundry (INTEGRAZIONE, ~92%), il gate κ ≥ 0,6 (MISURA-EDITORIALE, ~90%), la prova del blocco dei segreti (PRATICHE PI-3), il collaudo del Drappo L9 al ta… | i piani | DM |
| **P12 · Immagini da Canva**: gli originali a piena risoluzione dei sette ritratti al posto delle copie da 533 × 800, e Skullcrusher nel cortile col cane di Hella sbagliato | `07_…/Immagini/PROMPT-RITRATTI-E-TAVOLE-ARC07.md` §4 | esportare da Canva con lo stesso nome di file |
| **P13 · La bozza del Caos Ultimo** (TRASVERSALE D13): approvarla o correggerla | `PG/Artefatti/…/04_Anello_S3_Caos_Ultimo_DM.html` | DM |
| **P14 · Le promozioni a stable** (ADR-0099): ruff e uv proponibili dal 2026-11-06, pytest-xdist dopo 14 giorni dal 2026-10-23 | [PIATTAFORMA](plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md) | la card nel thread padre |
| **P29 · Le chat di Claude.ai, la parte che solo il DM può fare**: archiviare a mano le 24 chat del triage (nessuno strumento qui le raggiunge, né i loro allegati) e ripetere la ricerca dentro gli altri progetti di Claud… | triage chat 2026-10-23, «Note oneste» | archiviare; dire se esistono altri progetti RumblingStone |

## ⬜ Da fare, nell'ordine dei piani: 9

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P19 · Il rilevatore dei box e le battute etichettate** (`> **2 di 3 — …**`): da riverificare se `misura_craft.box_read_aloud` le apre; se no, allargare l'apertura e rimisurare i residui | `scripts/misura_craft.py` | prima la prova su `DEF-4` (Balvar) |
| **P20 · Residui di stampa**: «Naviga i capitoli qui sopra» ancora stampato nel Palio (`PALIO-BOOKLET-INTRO.md`); l'ultima riga dell'indice dell'Abbazia sola a pagina 35; i residui d'apparato del Palio e del Drappo (… | §11.3 · CICLO-SESSIONE 2g | una PR di classe M |
| **P21 · RECUPERO L2 e L4**: R-3 e il suo test; i piani fermi, quando il DM risponde a D5 | [RECUPERO](plans/PIANO-RECUPERO-DECISIONI-E-REVISIONI-INCOMPIUTE-2026-10.md) | L2 subito, L4 dopo D5 |
| **P22 · L'ambiente riproducibile dentro la piattaforma**: A1-A3 di AMBIENTE (checksum nel registro, tre piattaforme, lock) vanno rimisurati contro ADR-0099, che ha già portato Python 3.13, i canali e i test una volta so… | [AMBIENTE](plans/PIANO-AMBIENTE-RIPRODUCIBILE.md) · [PIATTAFORMA](plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md) | dire cosa di AMBIENTE è superato, poi A1 |
| **P23 · PRATICHE**: PI-6, PI-2, PI-5, PI-4 (dopo CICLO D6); PI-1 4i-3 aspetta la prima PR che resta indietro rispetto a `main` | [PRATICHE](plans/PIANO-PRATICHE-DI-INGEGNERIA.md) §5 e §8 | una PR ciascuno, in quest'ordine |
| **P24 · CICLO-DI-SESSIONE, la Fase 0** (D1-D6 decise il 2026-09-30) | [CICLO-SESSIONE](plans/PIANO-CICLO-DI-SESSIONE-E-MENU.md) §5 | la Fase 0 |
| **P25 · Il Drappo L9, la lettura a freddo**: lettore e playtester che non vedono il piano sul §2-bis, e un dry-run cronometrato | [DRAPPO](plans/PIANO-DRAPPO-DI-TARSILIA-STANDALONE-PF1E.md) Lotto 9 | due agenti a freddo, poi P11 |
| **P27 · I nomi dell'Elsir Vale rimasti nel testo di gioco**: il triage delle chat dice «sostituiti da Cannath», ma «Elsir» compare ancora in ~30 file di contenuto. Molte righe sono note d'adattamento e vanno tenute (REA… | triage chat 2026-10-23, chat 15 | censire le righe, separare note d'adattamento e finzione, correggere solo la finzione |
| **P30 · Gli altri archi senza testo, e cosa si è perso nell'import**: 06, 07, 10 senza perdite. D7-D12 decise dal DM il 2026-10-23 e la cronaca corretta (P30-b: partenza all'8° livello, appunti d'apertura giocati, chier… | [ARCHI-SENZA-TESTO](plans/RICERCA-ARCHI-SENZA-TESTO-2026-10.md) §5 | P30-a, le schede che mancano nel Bestiario |

## 🟡 Fatto a metà: 0

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

Nessuna.

## Fatto di recente: le ultime 12 righe del CHANGELOG

Fonte: [`plans/CHANGELOG.md`](plans/CHANGELOG.md), una riga per lotto chiuso.

| Data | Piano | Lotto | Esito |
|---|---|---|---|
| 2026-11-07 | SISTEMI-DI-GIOCO-PLUGIN | L1: fondazione dei plugin dei sistemi di gioco | ✅ 0 problemi; 24 righe di matrice; dnd35 2/10/0, pf1e 1/6/5 (dati/codice/non supportato); impronte 12/12 dopo la correzione dell'orologio di `update_xp` |
| 2026-11-07 | SISTEMI-DI-GIOCO-PLUGIN | L0: censimento degli strumenti, banco d'invarianza, ADR-0111 proposta | ✅ 31 script su 202 dipendono dal sistema; M1 3, M2 2, M3 76, M4 24; 12 impronte riproducibili; D1-D5 al DM |
| 2026-11-07 | STATO-E-ORDINE · P16 | Lotto 5: Bestiario, ARC-08, Tarsilia, Corona e menzioni storiche | ✅ card del DM: lama mortale al bugbear, orog e gufo di Lythiel nella versione forte, piazza di Tarsilia a 1,5 m, troll dell'ariete a 10 DV, riserva +3, nessuno… |
| 2026-11-05 | STATO-E-ORDINE · P16 | Lotto 4: le caratteristiche dei PG dalla scheda di carta del DM | ✅ foto del DM del 2026-11-05 riscontrata con le abilità senza gradi: Artemis 10/18/14/10/10/18; Thorik con il rito dello Smeraldo che la carta non aveva (DES 1… |
| 2026-11-05 | STATO-E-ORDINE · P16 | Lotto 3: le marcature aperte di ARC-09 | ✅ tre card del DM: la leva non sale sulle mura (Rethmar e Dauth), guarnigione fissa di Dauth 200 nani, Witchwood a 300 m. ARC-09 da 3 a 0 aperte, repo 58 |
| 2026-11-05 | STATO-E-ORDINE · P16 | Lotto 2-bis: i PX del gruppo e il 14° livello, dal registro del DM | ✅ registro completato dall'arco 06 al 25/09 con le scelte del DM, riga per riga; Thorik, Tordek e Artemis al 14° fermi a 104.999 (un livello alla volta), Hella… |
| 2026-11-04 | STATO-E-ORDINE · P16 | Quota sul mare di Hammerfist abbassata: piana a 520 m (scelta del DM, in linea… | ✅ cancello 600, cortile 620, cittadella 640; gradoni invariati |
| 2026-11-04 | STATO-E-ORDINE · P16 | Lotto 1, ARC-08: conto vero e marcature chiuse da conti e decisioni | ✅ le aperte erano 240, non 44: il contatore ora mette in «meta» le 21 righe che descrivono la convenzione e vede le 17 note che vanno a capo (3 test). ARC-08 d… |
| 2026-11-03 | RICERCA-USABILITA-AL-TAVOLO, RICERCA-GU… | documentazione dopo la #306 | ✅ ARCHITETTURA §11-§13, §16, §18, §19, README, GUIDA-BOOKLET-E-PDF e CHANGELOG allineati ad ADR-0102, ADR-0105…ADR-0108 e ai cancelli della #308 e della #309;… |
| 2026-11-03 | RICERCA-GUARDRAIL-E-TECNICHE | §9 fedeltà del riscritto (NLI) e correzioni | ✅ 30 coppie al DM alla cieca: NLI F1 0,83 contro 0,62 dei numeri; `misura_fedelta_nli.py` corregge da sé dentro `ciclo_prosa`; corretti i 2 box telecomando (4… |
| 2026-11-03 | RICERCA-GUARDRAIL-E-TECNICHE | §8 prove scartate rifatte con configurazione rigorosa | ✅ adottati come indicatori: ripetizioni frase per frase (6 vere invece di 1) e box telecomando al plurale (2 su 4 invece di 2 su 15); NLI sulla stessa entità (… |
| 2026-11-03 | RICERCA-GUARDRAIL-E-TECNICHE | conti dei master all'SRD (scelta del DM) | ✅ Treant di Adamantio 95 pf (10d8+50), scurovisione 18 m a Durin e alle wyvern; Balvar 101 resta, perché i PNG con classi hanno il primo dado al massimo (DMG 3… |

## Le misure che si portano dietro

- **Decisioni**: 18 aperte, 306 chiuse (`decisioni_dm.py`).
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
