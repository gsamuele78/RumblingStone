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

## Aspetta il DM: 26 decisioni aperte

Fonte: le tabelle `decisioni-dm` dei piani, aggregate in [STATO-E-ORDINE §4](plans/STATO-E-ORDINE-DEI-PIANI.md). Si risponde col numero e il piano: *«CODA-SECONDO-LETTORE D2 sì»*.

| Piano | # | Ambito | Domanda |
|---|---|---|---|
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
| `RECUPERO` | D5 | L4 | **I ⬜ opzionali dei piani chiusi o fermi**, per gruppo. *Proposta*: (a) chiusi come «non si fa»: AUDIT-SCRIPTS (shellcheck lo fa AMBIENTE A6), IMPORT-ULTRACLEAR (migrazione delle ~30 mappe, ora COLLAUDO-MAPPE), RENDER-F… |
| `RECUPERO` | D6 | L3 | **RICONCILIAZIONE-PR-APERTE si chiude come superato?** R3, R6, R7, R8 sono decisi o fatti altrove (§2.3). *Proposta*: sì, ✅ con il rimando a dove sta ognuno |
| `RIPRESA-PR` | D2 | F3 · 3d | **Riformulata il 2026-09-11: la domanda di prima partiva da un fatto falso.** Diceva *«i diciotto raster si generano sulla tua macchina — quando?»*, ma **esistono tutti e diciotto** (più le due extra), generati dal DM *… |
| `RIPRESA-PR` | D11 | F4 · 4b | **L'ADR ex-0018 della #72: recuperato il 2026-09-11 come [ADR-0049](plans/adr/ADR-0049-edizione-commerciale-ap-originale.md), e resta 🔵 *proposta* — non accettata.** Dice che, *se e quando* si pubblica, si pubblica un *… |
| `ARCHI-SENZA-TESTO` | D1 | 05 | **I funghi della Stanza Runica.** I PDF: la druida segue la spirale di zurkhwood, trova la Runa di Ysgard e i funghi crescono e la coprono. Il canone: il gruppo brucia i funghi della stanza e Hella perde il micelio. *Pr… |
| `ARCHI-SENZA-TESTO` | D2 | 05 | **Chi è lo spirito nel sarcofago.** I PDF: «Thorek Forgiamartello, l'antico portatore della Corona». Il canone: Thorek è il re di Hammerfist, Thorek I suo antenato di mille anni fa, e una statua del Cuore è Thorek I. *P… |
| `ARCHI-SENZA-TESTO` | D3 | 05 | **La gemma della prova.** I PDF: la Gemma del Legame Spirituale, chiave per la Corona. Il canone: tre gemme, tutte nella Corona e spente nell'arco 06; la Prova della Sala Profonda attiva il topazio. *Proposta*: la gemma… |
| `ARCHI-SENZA-TESTO` | D4 | 05 | **Le ricompense della Stanza Runica.** I PDF: Benedizione di Thorek (+2 permanente ai TS contro la paura) e +1 slot del livello più alto; 4.800 PE totali più bonus. Il registro XP: 5.800 PX per PG; nessuna scheda di PG… |
| `ARCHI-SENZA-TESTO` | D5 | 05 | **I nomi tolkieniani delle rune** (Moria, Erebor, Durin, Khazad-dûm e altri sei). Il canone non li usa. *Proposta*: restano nella trascrizione come documento d'archivio; un master li sostituisce con nomi nanici di Faerû… |
| `ARCHI-SENZA-TESTO` | D6 | 05 | **I numeri in contrasto fra i tre PDF**: il soffitto (per fasce dal round 6, o 30 cm ogni 5 round dal 10), Conoscenze (natura) CD 25 o 28, il dominio dei non morti a 1d4 o 1d6 Saggezza, le catene dal round 4 o dal 7. *P… |
| `ARCHI-SENZA-TESTO` | D7 | 00 | **Il livello di partenza.** `campagna_flusso.txt` e il registro XP (28.000 PX): 8° livello. La cronaca: «Phase A … (Levels 4–6)». *Proposta*: correggere la cronaca a «8° livello», se il DM conferma che il gruppo non ha… |
| `ARCHI-SENZA-TESTO` | D8 | 00 | **Gli appunti d'apertura mai portati**: Lando Norris e l'offerta da 3.500 a 4.500 mo, Khalzon Burn con la maschera dei draghi, il negromante di Castel Wrath con gli scheletri dei giganti e la tribù della Luna della Mort… |
| `ARCHI-SENZA-TESTO` | D9 | 02 | **Il nemico della Scala d'Ossa**: «necromante di Abbathor» (cronaca) o chierico di Abbathor (file, registro XP, Bestiario)? E GS 11 (Bestiario) o 12 (registro)? *Proposta*: chierico, come dicono tre fonti su quattro; il… |
| `ARCHI-SENZA-TESTO` | D10 | 02-03 | **Il duergar mago fuggito.** I file lo fanno scappare dalla Scala d'Ossa e tornare davanti al tempio con i drow del casato. La cronaca non ha il filo. *Proposta*: entra nella cronaca se il DM conferma che è andata così |
| `ARCHI-SENZA-TESTO` | D11 | 03 | **Il retriever e lo scontro davanti al tempio.** Il retriever: comandato dallo stregone drow (cronaca) o mandato dai chierici di Abbathor a riprendere Aegis Fang (nome del file sorgente)? E lo scontro EL 14 (capitano de… |
| `ARCHI-SENZA-TESTO` | D12 | 00-03 | **Le trascrizioni di testi altrui nel repo**: il capitolo di *Expedition to Undermountain* (01, con il link ad archive.org), il Grell Patriarca di *Lords of Madness* (01), le pagine dei drow e dei warlock (03), le pagin… |

### Revisioni della prosa da approvare: 0

Fonte: i documenti `REVISIONE-*.md` sotto `plans/scrittura/` che `ciclo_prosa.py applica` può ancora applicare. Ogni cartella ha un `LEGGIMI.md` con i passaggi interi.

Nessuna.

## ▶ In corso: da qui si riparte: 4

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P01 · MASTER-DEF: A3 chiuso, D4 e D5 decise** (#259, ARC-08: il collo e l'ala nella presa di Thorik, ADR-0096) | [MASTER-DEF](plans/PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md) A3 | merge della #259 quando il thread dà il via; poi S1-S4 |
| **P03 · ARC-07 riscritto con le norme nuove**, misurato contro le versioni di prima (tag `prima-rifacimento-arc07`), e l'handout del contratto del Seme da portare in `ARC07-HANDOUTS` | ADR-0093 · `/mnt/project-files/contratto-seme/` | il thread |
| **P04 · LLM locale, la prova del 12B sull'ASUS e del 26B sulla Dell** (gemma4 e4b bocciato, #234 su `main`) | [ADR-0089](plans/adr/ADR-0089-un-llm-locale-per-la-prosa-si-misura-prima.md) · `plans/scrittura/` | una PR nuova dal thread |
| **P05 · La #99 e lo schedario dei PG**: chiusura proposta (ADR-0007 del thread); 4g da rifare come 4g-1 e 4g-2 da `main`, 4h scartato | [RIPRESA-PR](plans/PIANO-RIPRESA-PR-ABBANDONATE.md) F4 · `/mnt/project-files/pr99/` | il sì del DM per chiudere la #99, poi 4g-1 |

## 🙋 Aspetta il DM: 10

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P02 · AVVENTURE-COMMUNITY 7c, fronti e orologi**, e i residui del lotto 7: i 4 di `plans/coerenza-residui.json` e i possessivi contro italiano-nativo §1 | [AVVENTURE-COMMUNITY](plans/PIANO-AVVENTURE-COMMUNITY-2026-10.md) | una risposta del DM; poi il thread «Avventure della community a confronto» |
| **P06 · Accettare le ADR ancora «proposta»**: ADR-0090 (la partita sul ramo di gruppo nuovo, dal 2026-10-11), ADR-0094 (il giro si misura contro la versione di prima), ADR-0095 (correzione, verifica e seconda passata).… | `plans/adr/` | un sì o un no per ADR; l'agente cambia lo stato e la riga di CHANGELOG |
| **P07 · Le decisioni numerate dei piani**: BOX-DI-LUOGO D2-D6, CODA-SECONDO-LETTORE D2 e D3, MASTER-DEF D6 (il censimento delle versioni), RECUPERO D5 e D6, RIPRESA-PR D2 (Gemini o SDXL per il Drappo, con la #106) e D11… | §4, generata da `decisioni_dm.py` | rispondere col piano e il numero: *«BOX D2 sì»* |
| **P08 · Le patch di `state.md` sul ramo di gruppo**, scritte e mai applicate (verificato su `ce34599`): il Bane di Aegis Fang contro Fauci (affresco A7); la Cintura della Devastazione a 4 cariche al giorno (lo stato dic… | `/mnt/project-files/sessione-2026-10-15/` · `/mnt/project-files/giro-arc07-2026-10-18/PATCH-STATE-MD.md` | `git am` o a mano sul ramo `campaign-group-rumblingstone` |
| **P09 · Le domande di canone lasciate aperte dai thread di ARC-07 e ARC-08**: i pf di Terros (345 o 348 con Robustezza); *Virata* da riscontrare su d20srd; la portata del sussurro della Catena… | `plans/esperimenti/giro4-arc07-2026-10-19/DECISIONI-DM.md` · `DEF-4` · `ARC08` | una risposta per domanda; l'agente le porta nei master in una PR |
| **P10 · Mappe, le scelte del DM**: texture e tessere nella pagina di scelta (R8, livello B), la prima immagine di ComfyUI (R4-quinquies), il giro di prova sui modelli 3D CC0 e lo zip Standard di Quaternius (R4-ter), il… | [RESA-ASSET](plans/PIANO-RESA-E-ASSET-DELLE-MAPPE.md) §8 · [COLLAUDO-MAPPE](plans/PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) | DM; poi l'agente mette le tessere nel tema e rimisura |
| **P11 · I collaudi che solo il DM può fare**: l'import `.uvtt` in Foundry (INTEGRAZIONE, ~92%), il gate κ ≥ 0,6 (MISURA-EDITORIALE, ~90%), la prova del blocco dei segreti (PRATICHE PI-3), il collaudo del Drappo L9 al ta… | i piani | DM |
| **P12 · Immagini da Canva**: gli originali a piena risoluzione dei sette ritratti al posto delle copie da 533 × 800, e Skullcrusher nel cortile col cane di Hella sbagliato | `07_…/Immagini/PROMPT-RITRATTI-E-TAVOLE-ARC07.md` §4 | esportare da Canva con lo stesso nome di file |
| **P13 · La bozza del Caos Ultimo** (TRASVERSALE D13): approvarla o correggerla | `PG/Artefatti/…/04_Anello_S3_Caos_Ultimo_DM.html` | DM |
| **P14 · Le promozioni a stable** (ADR-0099): ruff e uv proponibili dal 2026-11-06, pytest-xdist dopo 14 giorni dal 2026-10-23 | [PIATTAFORMA](plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md) | la card nel thread padre |

## ⬜ Da fare, nell'ordine dei piani: 12

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P16 · Le marcature rimaste nel contenuto**: 44 `[INFERRED]` e `[PROPOSTA]` (erano 568 il 2026-09-25; il Bestiario è a 0): ARC-08 3, ARC-09 9, `campaign/` 26 (20 nel `state-changelog`), PG 2, ARC-07 1 fuori archivio | `grep -rc "\[INFERRED\]\\|\[PROPOSTA\]"` | un lotto per arco: prima ARC-08, poi ARC-09 |
| **P17 · Skullcrusher Vecchio nei file di ARC-08**: l'ERRATA §2.3 e `ARC08-11-PONTE-ARRIVO` vanno allineati al duello deciso (il Vecchio con 2 wyvern, EL 17) | memoria del 2026-10-19 · `08_…/ERRATA-*.md` | da riverificare prima di toccare |
| **P18 · Le regole di 3.5 fuori rete**: gli incantesimi nelle esportazioni PCGen di `Bestiario/pregen-pcgen/` non hanno ancora la loro riga in `dnd-35-srd/references/resources.md` | §8.3 | una riga e la voce nel registro delle norme |
| **P19 · Il rilevatore dei box e le battute etichettate** (`> **2 di 3 — …**`): da riverificare se `misura_craft.box_read_aloud` le apre; se no, allargare l'apertura e rimisurare i residui | `scripts/misura_craft.py` | prima la prova su `DEF-4` (Balvar) |
| **P20 · Residui di stampa**: «Naviga i capitoli qui sopra» ancora stampato nel Palio (`PALIO-BOOKLET-INTRO.md`); l'ultima riga dell'indice dell'Abbazia sola a pagina 35; i residui d'apparato del Palio e del Drappo (… | §11.3 · CICLO-SESSIONE 2g | una PR di classe M |
| **P21 · RECUPERO L2 e L4**: R-3 e il suo test; i piani fermi, quando il DM risponde a D5 | [RECUPERO](plans/PIANO-RECUPERO-DECISIONI-E-REVISIONI-INCOMPIUTE-2026-10.md) | L2 subito, L4 dopo D5 |
| **P22 · L'ambiente riproducibile dentro la piattaforma**: A1-A3 di AMBIENTE (checksum nel registro, tre piattaforme, lock) vanno rimisurati contro ADR-0099, che ha già portato Python 3.13, i canali e i test una volta so… | [AMBIENTE](plans/PIANO-AMBIENTE-RIPRODUCIBILE.md) · [PIATTAFORMA](plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md) | dire cosa di AMBIENTE è superato, poi A1 |
| **P23 · PRATICHE**: PI-6, PI-2, PI-5, PI-4 (dopo CICLO D6); PI-1 4i-3 aspetta la prima PR che resta indietro rispetto a `main` | [PRATICHE](plans/PIANO-PRATICHE-DI-INGEGNERIA.md) §5 e §8 | una PR ciascuno, in quest'ordine |
| **P24 · CICLO-DI-SESSIONE, la Fase 0** (D1-D6 decise il 2026-09-30) | [CICLO-SESSIONE](plans/PIANO-CICLO-DI-SESSIONE-E-MENU.md) §5 | la Fase 0 |
| **P25 · Il Drappo L9, la lettura a freddo**: lettore e playtester che non vedono il piano sul §2-bis, e un dry-run cronometrato | [DRAPPO](plans/PIANO-DRAPPO-DI-TARSILIA-STANDALONE-PF1E.md) Lotto 9 | due agenti a freddo, poi P11 |
| **P26 · L'eccezione di ruff per `misura_craft.py`**, da togliere dopo la #264 | `ruff.toml` | dopo il merge della #264 |
| **P30 · Gli altri archi senza testo, e cosa si è perso nell'import**: 06, 07, 10 senza perdite; mai arrivati nei markdown l'Orrore Palustre d'Ombra e Zanna (03), lo scontro davanti al tempio e il warlock (03), gli appun… | [ARCHI-SENZA-TESTO](plans/RICERCA-ARCHI-SENZA-TESTO-2026-10.md) §5 | P30-a, le schede che mancano nel Bestiario; poi P30-b dopo D7-D11 |

## 🟡 Fatto a metà: 1

Fonte: [STATO-E-ORDINE §0](plans/STATO-E-ORDINE-DEI-PIANI.md), la lista viva.

| Cosa | Dove sta il dettaglio | Da dove si parte |
|---|---|---|
| **P28 · L'arco 05 (la Stanza Runica) viveva solo in PDF**: trascritto in `05_aa-stanza-runica/ARC05-STANZA-RUNICA-TRASCRIZIONE.md` coi numeri dei tre PDF; il canone resta `campaign/lore/campaign-chronicle.md`. Sei diver… | [ARCHI-SENZA-TESTO](plans/RICERCA-ARCHI-SENZA-TESTO-2026-10.md) §3.6 e D1-D6 | una risposta per voce; l'agente la porta nella trascrizione e nella cronaca |

## Fatto di recente: le ultime 12 righe del CHANGELOG

Fonte: [`plans/CHANGELOG.md`](plans/CHANGELOG.md), una riga per lotto chiuso.

| Data | Piano | Lotto | Esito |
|---|---|---|---|
| 2026-10-23 | RICERCA-ARCHI-SENZA-TESTO | censimento e trascrizione dell'arco 05 (DM: *«controllare se ci sono pdf o altr… | 🟡 Censiti i file non markdown degli archi 00-10 e degli standalone e confrontati coi markdown (numeri e nomi propri della fonte assenti nel markdown, poi a man… |
| 2026-10-23 | STATO-E-ORDINE · INDEX · RECUPERO · RIP… | P15 dell'indice: la coerenza dell'archivio dei piani | ✅ Otto intestazioni di piano riallineate allo stato di `INDEX.md`: le sei dell'indice (AMBIENTE, PRATICHE, TRAVASO, AUTOMAZIONE, AGENT-SKILLS, DRAPPO) e due tr… |
| 2026-10-23 | MAPPE-QUALITA (esperimento) · ADR-0102 | strumenti delle mappe nel repo: tema «pianta» e generatori delle città (DM: «co… | ✅ Il tema pianta disegna le griglie emoji nello stile delle piante delle città (roccia tratteggiata entro 0,24 quadretti, lastricato, «Luoghi» e legenda sotto)… |
| 2026-10-23 | MAPPE-QUALITA (esperimento) | piante v3 di Rethmar, Dauth e Channathgate canone (DM: rilievo, quote, taglie e… | ✅ |
| 2026-10-23 | AVVENTURE-COMMUNITY | lotto 7g, voto del DM sulla prima prova della pipeline | 🟡 Pipeline 4, originale 1, pari 1: miglioramento non dimostrato (soglia 5 su 6). Il modello di preferenza passa la soglia di `SOGLIA.txt` (0,661 su 59 coppie,… |
| 2026-10-23 | AVVENTURE-COMMUNITY | lotto 7i: la catena della prosa ha un ingresso solo (richiesta del DM: integrar… | 🟡 `dm.py prosa` mette in fila i dieci script; spaCy e LanguageTool nel registro, così `doctor` li vede; quattro diagrammi nuovi (catena, tre sequenze, dipenden… |
| 2026-10-23 | AVVENTURE-COMMUNITY | lotto 7e, correzione dopo il merge con main: `voto_scrittura` resta | ✅ La #234 (ADR-0089) ha portato su main `banco_prosa_locale`, che fa votare le corse del modello locale a `voto_scrittura`: toglierlo spezzava quel flusso. Il… |
| 2026-10-23 | STATO-E-ORDINE-DEI-PIANI | §0 · l'indice dei punti in sospeso | ✅ Richiesta del DM: *«un index da aggiornare con le decisioni prese, quelle abbandonate e quelle sorpassate da PR o altre soluzioni»*, da usare per aprire thre… |
| 2026-10-23 | PIATTAFORMA-DI-SVILUPPO | D7 · primo rilascio | ✅ Risposta del DM: *«1.0.0, solo le skill»*. Al merge della #275 esce v1.0.0 con l'archivio dei pacchetti delle skill, SHA256SUMS e attestazione; i PDF dei boo… |
| 2026-10-23 | PIATTAFORMA-DI-SVILUPPO | P10 · il rilascio è una PR | 🟡 Il DM: *«diventa std per tutto il resto… |
| 2026-10-23 | PIATTAFORMA-DI-SVILUPPO | P9 · `converters/` nella piattaforma (D6) | ✅ Risposta del DM: *«D6 b»*, e *«misura se ci sono miglioramenti anche nella qualità del progetto»*. Corretti i 3 bug di `converters/` (un modulo che non si im… |
| 2026-10-23 | PIATTAFORMA-DI-SVILUPPO | D1-D5 e metà di P4 | 🟡 Risposta del DM: *«D1-d5 ok»*. Il passo `unittest discover` esce dalla CI (222 s su 914), la parità dei due corridori resta in `test_i_test_girano_in_ci.py`.… |

## Le misure che si portano dietro

- **Decisioni**: 26 aperte, 286 chiuse (`decisioni_dm.py`).
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
