# 📚 ARCHIVIO PIANI — INDICE

> **Cos'è**: la vista d'insieme di tutti i piani di lavoro della campagna
> (revisioni, infrastruttura), con stato, % di completamento, lotti
> rimanenti e gate. Creato dal Lotto **K-A** del piano DM-TOOLKIT (K-D3).
>
> **Regola di manutenzione** (regola d'oro 4 dei piani): *chi chiude un
> lotto aggiorna — nello stesso commit — (1) la checklist del piano,
> (2) la riga qui sotto, (3) una riga in `plans/CHANGELOG.md`.*
>
> Le decisioni architetturali (il "perché" delle scelte di struttura)
> vivono in `plans/adr/`.

## Stato dei piani

| Piano | Ambito | Stato | % | Lotti/task rimanenti | Gate |
|---|---|---|---|---|---|
| [PIANO-REVISIONE-ARC07](PIANO-REVISIONE-ARC07-COERENZA-E-QUALITA.md) | Arco 07 — Portale della Forgia Eterna | 🟡 quasi completo | ~95% | B1 parziale: date/XP/loot **reali** dei log ricostruiti | sessioni giocate al tavolo |
| [PIANO-REVISIONE-ARC08](PIANO-REVISIONE-ARC08-COERENZA-E-QUALITA.md) | Arco 08 — Battaglia di Hammerfist | ✅ completo | 100% | — | — (l'arco resta ⬜ da giocare: il *piano* è chiuso, il *gioco* no) |
| [PIANO-REVISIONE-ARC09](PIANO-REVISIONE-ARC09-COERENZA-E-QUALITA.md) | Arco 09 — post-Hammerfist | ✅ completo | 100% | — | — (idem) |
| [PIANO-REVISIONE-TRASVERSALE](PIANO-REVISIONE-TRASVERSALE-COERENZA-E-QUALITA.md) | Rituale P3B · Mappe · Artefatti (tutta la campagna) | 🟡 gated dal tavolo | ~95% | T8 (sinergie Collana) · chiusura T9 (esito P3B in state.md §8) · SVG dei 16 narrativi (opzionale/estetico) | T8: quest ARC-09 giocata · T9: P3B giocato |
| [PIANO-DM-TOOLKIT](PIANO-DM-TOOLKIT-HYPE-E-ARCHIVIO-PIANI.md) | Infrastruttura: CLI dm.py · hype Homebrewery · questo archivio · **standard booklet [ADR-0013](adr/ADR-0013-standard-generazione-booklet-sessioni.md)** (K-B9…K-B11: builder pergamena, teaser spoiler-free, doppia via HTML/`.hb.md`) | ✅ completo | 100% | — | — (code da tavolo: verifica visiva dei brew al collaudo del container; piloti lettera/avviso-torneo quando il DM fornisce testo canone) |
| [RICERCA-GENERATORI-MAPPE](RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md) | Infrastruttura: pipeline mappe qualità AP — renderer "pergamena", import Watabou, export PNG, skill `rumblingstone-mapmaking` | 🟡 completo + follow-up in review | ~100% | Ultra-Clear P4 Piano Terra (PR #42 **aperta**, non mergiata) | — (hero map ComfyUI: opzionale, macchina DM con GPU; giudizio a occhio caso per caso) |
| [INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITÀ](PIANO-INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITA.md) | Infrastruttura: 3 modalità mappa, contratto JSON+validatore (Mod. 3), export UVTT/dd2vtt (Foundry/Roll20), infra container ComfyUI su Bazzite, **overlay professionale mappe** (bussola/movimenti/callout/zone, ADR-0006), direzione artistica IP-safe | 🟡 M1-M5 implementati, collaudo al tavolo | ~92% | collaudo DM: import `.uvtt` in Foundry, setup container ComfyUI su GPU; opz.: convertire Campo Drow 2/3 in JSON | collaudo al tavolo/macchina DM |
| [PIANO-RENDER-MAPPE-FEDELTÀ-DETTAGLI](PIANO-RENDER-MAPPE-FEDELTA-DETTAGLI.md) | Infrastruttura: renderer mappe a **fedeltà piena** (ASCII ultra-clear → SVG senza perdere posizioni/annotazioni/token) | 🟢 **eseguito** (2026-07-23): F1-F6 nucleo completo, 6 SVG ARC-07 resi, 17 legacy byte-identici | ~95% | opzionale: callout grafici ancorati (F3 pieno), `--strict` come default | — |
| [PIANO-IMPORT-ULTRACLEAR](PIANO-IMPORT-ULTRACLEAR-ASCII-TO-JSON.md) | Infrastruttura: `import_ultraclear.py` — ASCII ultra-clear → **bozza JSON contratto + report conflitti** (migrazione semi-automatica delle mappe esistenti) | 🟢 **eseguito** (2026-07-24): F1-F7 completi — registro R1-R10, report `editor-ready` (`map_conflicts.schema.json`), golden case Hammerfist verde, 17 test + CI | ~100% | opzionale: migrare al contratto le altre ~30 mappe ultra-clear (al tavolo/DM); il `--json-report` sarà consumato dall'editor visuale (Piano 2) | — |
| [PIANO-EDITOR-VISUALE-MAPPE](PIANO-EDITOR-VISUALE-MAPPE-TATTICHE.md) | Infrastruttura: **editor visuale a griglia** (progetto separato) che round-trippa col contratto JSON — alternativa domain-fit a FreeCAD | 🔵 **pianificato** (2026-07-23) | 0% | E0 ADR + scaffold, E1 legenda condivisa `legend.json`, E2-E10 (canvas/strumenti/import/export/e2e/packaging/test/doc) | E0: ADR «editor come progetto separato» |
| [PIANO-AUTOMAZIONE-STATO-SESSIONI](PIANO-AUTOMAZIONE-STATO-SESSIONI-BRANCH-GRUPPO.md) | Infrastruttura: `dm.py session` — wizard fine-sessione, apply engine `state.md` (regioni marcate), visibilità per-PG, brief prossima sessione, branch-per-gruppo con guardia su `main` | 🟢 implementato (A-F ✅, LLM E-bis escluso per decisione DM; [ADR-0007](adr/ADR-0007-scritture-canone-triplo-vincolo.md); wizard, per-PG, hook ❓, 31 test in CI; Quick Guide nuovi DM) | ~98% | — | collaudo al tavolo del flusso `session end` alla prima sessione reale |
| [PIANO-AUDIT-SCRIPTS](PIANO-AUDIT-SCRIPTS-QUALITA-E-CONTRATTI.md) | Infrastruttura: audit qualità script + **contratto machine-readable** (manifest/registry/MCP), normalizzazione CLI, `docs/INDEX` categorizzato, de-collisione `Script/`→`converters/` ([ADR-0011](adr/ADR-0011-de-collisione-scripts-converters.md)), **standard ingegneria verificabile in CI** ([ADR-0012](adr/ADR-0012-standard-ingegneria-tool-verificabile.md)) | 🟢 **eseguito** (2026-07-24): F0-F7, 70/70 test verdi, `tools_manifest --check` pulito | ~100% | opz.: shellcheck bloccante · convertitori allo standard pieno · fallback pyyaml in compress_skills | — |
| [PIANO-REINTEGRAZIONE-PNG-AP-RHOD](PIANO-REINTEGRAZIONE-PNG-AP-RHOD.md) | Contenuto: reintegrazione PNG dell'AP originale (Guado di Drellin, Rethmar 2° anello, Witchwood/Tiri Kitor, Wyrmlord) + proposta PNG caotico Lirien | ✅ **completo** (2026-07-20): R1-R7 tutti chiusi | 100% | — | — (canonizzazione dei lotti di preparazione R2/R3 a valle, in gioco) |
| [PIANO-INCANTATORI-MEMORABILI](PIANO-INCANTATORI-MEMORABILI-MANO-ROSSA-E-DROW.md) | Contenuto: incantatori nuovi per Mano Rossa (generale ogre magi elementalista + comprimari ogre sotterranei) e drow di Sonjak (illusionista-ombra, trickster arcano, assassina) + **ala orchesca in equivalenti SRD** (chierico di Gruumsh, bruto deforme del Sottosuolo, Ushgar «Occhio Reso» con ramo politico sulla faglia Gruumsh/Tiamat) — 9 schede + 3 dossier, tarati sulle difese reali del party (Mind Blank di Thorik, vulnerabilità al fuoco di Hella) + **indice d'uso di una web enhancement di fonte privata** (roster valutato contro il benchmark, ricette di adattamento, errata; solo puntatori, nessuno statblock trascritto) | ✅ **completo** (L6 approvato dal DM 2026-08-05): materiale a `[ACCEPTED — DM-canon]`, righe applicate in `state.md` §3/§4/§5/§7.E/§8 | 100% | — (resta l'assegnazione dei token, cosmetica) | — |
| [PIANO-SFIDE-COMBINATE](PIANO-SFIDE-COMBINATE-INCANTATORI-E-FORZA-BRUTA.md) | Contenuto: **sei pacchetti di scontro** che combinano gli incantatori SRD del repo, i comprimari di forza bruta e quattro statblock di fonte privata (solo puntatori a pagina) — EL calcolati, apertura round per round, che PG mette sotto pressione, uscita; + **Ghaurush GS 18** con *muro di forza*, dichiarato sopra il tetto e segnalato come «fuggi o muori». Principio guida: contro questo gruppo l'architettura dello scontro conta più del grado del mostro — **sette** sfide dopo l'aggiunta di «Il Sangue Sbagliato» (ondata di tanarukk con resistenza al fuoco e RI, specchio della sfida A: toglie la soluzione agli incantatori e la restituisce alla mischia) | ✅ **completo** (S4 deciso dal DM 2026-08-05): sfide approvate; **sfida E** solo come variante *Advanced* GS 17 dentro il tetto; **faglia della sfida G aperta** | 100% | — (S7, CdP Signore della Guerra Orchesco, **non presa**: Ushgar resta Barbaro 13) | — |
| [PIANO-INNESTI-SFIDE](PIANO-INNESTI-SFIDE-NEI-BEAT-DI-CAMPAGNA.md) | Contenuto: **dove vanno le sfide dentro il canone giocato** — sei innesti (Hammerfist ≈372 DR, Battaglia di Hammerfist, Notte dei Drow, viaggio Giorni 33-38, Torneo di Dauth, Torre Invisibile), ciascuno con slot canonico verificato, EL, e un aggancio che muove qualcosa di tracciato (clock §3, numeri §2.4, echi §7.E). Include le **esclusioni motivate**: niente tanarukk né Ghaurush a 372 DR (verifica di epoca), e il vincolo di collisione col Giorno 3 del Torneo | ✅ **completo** (N4 deciso dal DM 2026-08-05): **tutti e sei** gli innesti approvati; attori in `state.md` §3/§4/§5, eco **E-08a** in §7.E | 100% | — | — |
| [PIANO-REVISIONE-GLOBALE-2026-08](PIANO-REVISIONE-GLOBALE-2026-08.md) | Trasversale: audit su tre assi — **PRD/editoriale/pubblicazione**, **coerenza di flusso-storia-narrazione** (`[INFERRED]` inclusi), **ingegneria/ADR/testing/CI-CD** — con focus tavolo adulti | 🟡 **in esecuzione**: G0 (audit), **G1** (due tempi), **G2** (deriva doc↔realtà) **G2-bis** (`state.yaml` + ADR-0017) **G2-ter** (pipeline sessione→stato) e **G2-quater** (prodotto vs partita) chiusi il 2026-08-05; **G3** (link e path) chiuso del tutto il 2026-08-09 | ~65% (11 di 17 lotti) | G3-G4 subito (nessuna decisione DM) · G5-G6 su decisione DM · G7-G9 infrastruttura · G10-G11 gated | G5/G6: decisioni DM (**percorso critico**, ferme da luglio) · G10: prima sessione reale · G11: intervista di ricostruzione |
| VERIFICA LEGALE-IP (P2D "Palio") — [ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md) · [rapporto](../09_Continuazione%20Arco%20Narrativo%20dopo%20Battaglia%20di%20Hammerfist/Arco-Post-Hammerfist-P2D-PALIO-VERIFICA-LEGALE-IP.md) | Conformità IP: Regolamento/Consorzio Palio di Siena + blocco WotC/Forgotten Realms | ✅ verifica completata (PR #47) | 100% | bonifica §7 (rinomina contrade/livree/motti, "Piazza il Campo", riambientazione fuori FR) — **solo se** si punta a edizione commerciale | decisione DM su uso commerciale (non presa) |

## Prossimi passaggi (volutamente in bianco — si riempiono al tavolo / su decisione DM)

### PIANO-REVISIONE-ARC07
- ⬜ _(da definire al tavolo: date/XP/loot reali per chiudere B1)_

### PIANO-REVISIONE-ARC08
- ⬜ _(nessuno pianificato — eventuali emergenze dal gioco dell'arco)_

### PIANO-REVISIONE-ARC09
- ⬜ _(nessuno pianificato — eventuali emergenze dal gioco dell'arco)_

### PIANO-REVISIONE-TRASVERSALE
- ⬜ _(T8: quando la quest ARC-09 di Hella è giocata)_
- ⬜ _(chiusura T9: quando il P3B è giocato — esito reale in state.md §8)_

### PIANO-DM-TOOLKIT
- 🟡 _(K-B3.9 — tavole di Channathgate ricollocate in `immagini/` + ridimensionate con Pillow: **PR #46 aperta**, non mergiata; le tavole PNG del DM sono già su main via `ed56aa6`)_
- ⬜ _(riapertura estetica K-B0 solo se il DM indicherà template specifici del pack)_
- ⬜ _(collaudo al tavolo: container + brew I-V; piloti lettera/avviso-torneo quando arriva testo canone)_

### RICERCA-GENERATORI-MAPPE
- 🟡 _(P4 Piano Terra → griglie Ultra-Clear, dall'agguato Xorn al boss Terros: **PR #42 aperta**, non mergiata — quando merge, tracciare qui e in CHANGELOG)_
- ⬜ _(opzionale/estetico: portare a griglia Ultra-Clear le altre mappe KO del censimento — Torre P2A, Torneo P2B, Battaglia Finale P3 — ora che il renderer c'è)_
- ⬜ _(mappa regionale Cannath Vale/Dalelands con Azgaar FMG — `.map` master + export in rendered/)_
- ⬜ _(hero map ComfyUI sulle 2-3 mappe chiave — solo su macchina DM, vedi skill mapmaking)_

### INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITÀ
- ⬜ _(collaudo DM: generare una mappa Mod. 3 reale da JSON per un incontro ARC-08/09 e renderla)_
- ⬜ _(collaudo DM: importare un `.uvtt` in Foundry e verificare muri/luci)_
- ⬜ _(collaudo DM: setup container ComfyUI su Bazzite con GPU + hero map su una mappa chiave)_

### PIANO-AUTOMAZIONE-STATO-SESSIONI
- ⬜ _(collaudo al tavolo: primo `dm.py session end` — wizard incluso — su una sessione reale del gruppo, sul branch `campaign-group-rumblingstone-dm-gianfranco`)_
- ⬜ _(opzionale, decisione DM futura: lotto E-bis LLM per evoluzioni narrative — oggi escluso)_

### PIANO-IMPORT-ULTRACLEAR
- ✅ _(F1-F7 eseguiti 2026-07-24: `scripts/import_ultraclear.py` + `scripts/schemas/map_conflicts.schema.json` + 17 test + smoke CI + doc skill — branch `claude/piani-completare-5b85qg`)_
- ⬜ _(opzionale: migrare al contratto JSON le altre ~30 mappe ultra-clear del censimento — un file alla volta, risolvendo i conflitti segnalati; da fare al tavolo/su decisione DM)_
- ⬜ _(gancio Piano 2: l'editor visuale consuma `--json-report` per evidenziare le celle in conflitto e applicare le `actions`)_

### PIANO-EDITOR-VISUALE-MAPPE
- ⬜ _(E0: ADR «editor come sotto-progetto separato» — decisione stack/offline/confini, prerequisito a tutto il front-end)_
- ⬜ _(E1: `export_legend_json.py` → `legend.json` + gate CI di sync — prerequisito tecnico con valore autonomo, candidabile per primo)_
- ⬜ _(E2-E10: canvas griglia, strumenti, import Watabou/bozza-ultraclear, export contratto, round-trip e2e, packaging offline, test Playwright, doc)_

### PIANO-INCANTATORI-MEMORABILI
- ✅ _(L6 chiuso 2026-08-05: **approvato tutto**. 13 file a `[ACCEPTED — DM-canon]`; tre clock villain in `state.md` §3, conoscenze in §4, ramo terra in §5, eco E-08a in §7.E, changelog §8)_
- ✅ _(ramo di Ushgar: **aperto**, con l'ordine deciso dal DM — prima l'uscita laterale di **Hella** (il Cerchio non si oppone all'insediamento), la firma di Thorik solo come secondo passo. La penale «perdita status Custode Eterno» scatta **solo** se si arriva alla firma del nano)_
- ⬜ _(unica coda cosmetica: assegnare i token in `Bestiario/tokens/`)_
- ✅ _(ex-opzionale: l'ogre deforme del Sottosuolo da fonte privata è stato risolto in L7 come **equivalente SRD** — `bruto-deforme-sottosuolo-cr11.md`. Nessuna citazione di fonte privata necessaria)_

### PIANO-SFIDE-COMBINATE
- ✅ _(S4 chiuso 2026-08-05: **sfide approvate**. La scelta operativa passa dagli innesti I1-I6)_
- ✅ _(S5 chiuso 2026-08-05: scheda tanarukk fornita dal DM → sfida **G** «Il Sangue Sbagliato». Con correzione dichiarata: avevo dedotto GS 6, il tanarukk base è **GS 6 solo con Barbaro 4** — da solo è **GS 2**)_
- ✅ _(S6 chiuso 2026-08-05: scheda orchi montani fornita dal DM. Esito onesto: **nessun nemico nuovo** — i tratti sono identici all'orco SRD, quindi le schede orchesche del repo *sono già* orchi montani. Il valore sta altrove, in §2-ter dell'indice)_
- ✅ _(deciso 2026-08-05: **la faglia si apre**. Ushgar **non** ha «Adattamento alla Luce» e il Controllo delle Fiamme **fa scattare** la cecità alla luce — i tanarukk possono accecare i propri comandanti)_
- 🚫 _(S7 **non presa** 2026-08-05: Ushgar resta Barbaro 13. La CdP resta disponibile se un giorno servisse)_
- ✅ _(deciso 2026-08-05 sulla sfida **E**: **non come primo incontro**. Si usa la variante *Advanced* **GS 17** (EL 17, dentro il tetto); la GS 18 col *muro di forza* resta per il ritorno, e solo se il primo Ghaurush è scappato)_

### PIANO-INNESTI-SFIDE
- ✅ _(N4 chiuso 2026-08-05: approvati **tutti e sei** gli innesti I1-I6)_
- ⚠️ _(vincolo da rispettare: l'innesto **I5** va al **Giorno 1 o 2** del Torneo di Dauth, mai al Giorno 3 — quel giorno è già occupato dall'assalto di Xal'thor e dallo smascheramento di Sethrax, e tre trame nella stessa scena si annullano)_

### PIANO-REVISIONE-GLOBALE-2026-08
- ✅ _(G0 — audit read-only eseguito 2026-08-05: 3 documenti in `docs/audit/`, 9 misure riproducibili, 17 finding con severità. Nessuna modifica a canone, codice o CI)_
- ✅ _(G1 — chiuso 2026-08-05: nuova §-1 con la legenda dei due tempi e il confine dichiarato · §1 Party a due colonne come §6 (**Hella morta**, i quattro nella Sala della Forgia Eterna) · banner dei due tempi su §2/§4/§5, con la conseguenza a verbale che nessun PNG può ancora riconoscere i PG come Custodi Eterni · `campaign-history.md` non è più «single source of truth» e la riga di Hella è marcata 📋. **Nessun contenuto cancellato, solo etichettato**)_
- ⚠️ _(**delle due domande al DM aperte da G1**, la prima è **chiusa il 2026-08-09**: il **−2 COS di Thorik** **oggi non esiste** — è il prezzo del Dono «Il Sangue della Stirpe» al rito di Hella, non ancora giocato, e quando arriverà si sommerà al **+2 COS** del rito dello Smeraldo (netto zero). Resta aperta la seconda: il **Giorno di Marcia** è **19** come dice §2.1 o **~15** come implica l'orologio Hammerfist a 3g 16h? Non risolta d'ufficio: alimenta i numeri di §2.4 e la finestra quest di Arco 09. Il **−2 DES** che il DM ricordava è stato **trovato ed è vero**: non è anteriore alla Corona, è **della** Corona — `PortaleForgia-P1` lo elenca fra le Limitazioni all'atto di indossarla, col ricalcolo **DES 10 → 8**, e nessuna scheda successiva lo riportava più. Reintegrato; il conto totale è **10 → 8 → 6**. Resta **INF-007**: valgono ancora anche il **+4 CAR** e la **non-rimovibilità** della Corona, che stanno nello stesso blocco?)_
- ✅ _(G2 — chiuso 2026-08-05: `AGENTS.md` e `README.md` allineati al filesystem reale (via le 3 cartelle mai esistite, il formato-scheda PNG morto, la regola 5 che puntava a un file inesistente) + nuovo gate **bloccante** `scripts/validate_docs.py`, costruito per non dare falsi positivi (abbreviazioni ADR, modelli di nome, direttive di esclusione). 41 tool a manifest, 80 test)_
- ✅ _(G2-bis — chiuso 2026-08-05, su domanda del DM sul formato: **[ADR-0017](adr/ADR-0017-stato-dati-e-prosa.md)** — i fatti di §0/§1/§6 in `campaign/state.yaml` validato da schema, la prosa in markdown, le tabelle **generate** da `render_state.py`, lo storico in `state-changelog.md`. `state.md` da **1677 a 546 righe**. Il vincolo: `oggi` e `tempo` obbligatori → **un fatto senza tempo dichiarato non è esprimibile**. `[INFERRED]` diventa record tipizzato: le due domande di G1 sono INF-001 e INF-002)_
- ✅ _(G2-ter — chiuso 2026-08-05: **una sola via di scrittura** sessione→stato. §3, §4 e i numeri di §2.4 migrati a dati (`state.yaml` da 3 a **7 sezioni**); **front-matter dei delta** emesso dal wizard, così `state_apply` legge dati invece di dedurli con regex — prima i clock villain passavano da una lista di nomi cablata nel sorgente, e Ghaurush non sarebbe stato visto. Retrocompatibile. Tre domande nuove: INF-003/004/005, fra cui i villain che «sanno dei Custodi Eterni» prima che il titolo esista)_
- ✅ _(G2-quater — chiuso 2026-08-05: **prodotto vs partita**. Il reset per gruppo nuovo perdeva — un DM nuovo ereditava `state.yaml`, `state-changelog.md`, `campaign-history.md` e i recap del gruppo precedente, e trovava la CI rossa perché il template non aveva i marcatori. `campaign-history.md` spaccato in **premessa** (prodotto, resta) e **cronaca** (partita, si azzera); tre template nuovi; `test_new_group.py` verifica che ogni file di stato sia coperto)_
- ✅ _(**decisione presa 2026-08-05**: **[ADR-0018](adr/ADR-0018-directory-per-gruppo.md)** — il multi-gruppo diventa `groups/<slug>/`, il gruppo esistente è `rumblingstone`, `campaign/` resta solo prodotto. Risoluzione `--group` > env > file locale gitignored > gruppo unico nel registro committato; slug validato invece che quotato; un solo resolver `dmcore/groups.py`; la guardia si sposta dal branch alla directory e blocca il **canone**, non i commit al prodotto. Esecuzione: **lotto G12, PR dedicata dopo G3/G4**)_
- ✅ _(**memoria degli agenti, decisa 2026-08-05**: **nessun memory store** — sarebbe non versionato e divergente, cioè C2 in forma invisibile. Al suo posto **G13**, `dm.py brief --for-agent`: context pack generato dai dati, e soprattutto un **indice con puntatori**, non un riassunto)_
- ✅ _(G3 — **chiuso del tutto il 2026-08-09**: gate `validate_links.py` bloccante su tutti i `.md`; 18 link rotti e 25 path assoluti trovati, di cui **due classi intere di falsi positivi** (deploy dei converters = path di *server*; documenti d'audit che citano il difetto). Riparati i 2 `cd /home/jfs/` del PLAYBOOK, i 2 link `file:///` della scheda Bracieri, l'immagine dell'Anello (`.webp` → `.png`) e un bug mio di G2-quater. **I «13 asset mancanti» del Palio non mancavano**: esistono in `09_…/P2D-Palio-Allegati/`, era il generatore `.hb.md` a non rebasare i percorsi. La toppa di G3 — `validate-links: ignore` incollato **dentro l'artefatto generato**, contro ADR-0003 — è sparita alla prima rigenerazione. Corretto nel generatore, **decisione A1 caduta**)_ <!-- validate-links: ignore -->
- ⬜ _(G4 — 17 link rotti + 4 path `/home/jfs/…` committati · inventario e ratchet dei 379 `[INFERRED]`)_ <!-- validate-links: ignore -->
- ⬜ _(G5-G6 — **servono due decisioni DM**: destinatari/ambizione editoriale (PRD) e confini di contenuto + strumento di stop al tavolo)_
- ✅ _(**G4 · G14 · G15 — TAPPA 1 chiusa il 2026-08-10.** **G4**: la scoperta che decide il design è che **121 marcatori su 353 stanno in `plans/` e nei changelog** — *raccontano* un debito invece di aprirlo, e contarli dava un numero incapace di scendere. Tre classi, solo gli **aperti (215)** sorvegliati; inventario generato + ratchet in CI. **G14**: 4 schede PG come dati + scheda generata che mostra la **catena** (`DES 10 → 8 → 6`), e `validate_pg.py` con quattro controlli — il quarto (**partita doppia** con le fonti primarie) l'ha imposto un test che falliva, perché Thorik ha **due** −2 DES e il confronto per tipo lasciava il gate decorativo. INF-007 chiusa in blocco: la Corona **non è rimovibile**, vincolo attivo con tutte le conseguenze. **G15**: Echo Ledger a dati con **autore e stato obbligatori**, §7.E generata, e la regola col test da fare prima di armare un'eco — *regge se le cambio l'autore?* Se sì è scritta male: **un'eco buona è intrasferibile**. 158 test, 47 tool a manifest, 3 gate nuovi in CI)_
- 📐 _(**motore ed effort per lotto** + sequenza in cinque tappe: [PIANO §Come si esegue](PIANO-REVISIONE-GLOBALE-2026-08.md#come-si-esegue--motore-effort-sequenza). Regola usata: **chi verifica il lavoro?** — se lo verifica un gate basta Sonnet 5, se lo verifica solo un lettore umano (prosa, canone, echi, PRD) serve Opus 5)_
- ⬜ _(G7-G9 — validatore prosa + bonifica 30 file · igiene Python e CI hardening · **pipeline CD: oggi la CI valida e nulla pubblica**, nessun tag, nessuna release)_
- ⬜ _(G10 — attivare la pipeline ADR-0007: `doctor` segnala `group.yaml` assente e marker `auto:` assenti. Costruita, 31 test, mai accesa)_
- ⬜ _(G11 — ricostruzione della storia giocata archi 00-06: 1 solo log reale in `campaign/sessions/` contro 7 archi completati; archi 01/02/03/05 senza alcun `.md`. **Gated sull'intervista al DM**)_

### VERIFICA LEGALE-IP (P2D "Palio")
- ⬜ _(bonifica §7 — rinomina contrade, cambio livree, riscrittura motti da zero, rimozione "Piazza il Campo", riambientazione fuori Forgotten Realms: **gated** su una decisione DM di puntare a un'edizione commerciale, non ancora presa — vedi ADR-0005)_
- ⬜ _(debito documentale a bassa priorità: correggere la nota IP interna che dichiara i motti "originali" — sono parafrasi §3.3; documentare provenienza/licenza delle 2 tavole PNG del DM)_

### PIANO-REINTEGRAZIONE-PNG-AP-RHOD
- ✅ _(R2 — secondo anello di Rethmar preparato 2026-07-20: `Bestiario/png/Secondo_Anello_Rethmar/`)_
- ✅ _(R3 — Witchwood/Tiri Kitor preparato 2026-07-20: `Bestiario/png/Witchwood_Tiri_Kitor/`; Killiar cross-linkato allo statblock d'arco)_
- ✅ _(R4 — deciso dal DM 2026-07-20: Hravek Kharn fuso in Karruk; Ulwai non reintegrata 1:1; blackspawn rilivellati → tier élite CR 13 «Razorfiend Blackspawn Alfa»)_
- ✅ _(R6 — canonizzazione DM di R1+R5 avvenuta il 2026-07-20: flag sciolti, righe applicate a state.md §1/§3/§7/§8)_
- ✅ _(R7 — Mira Serani «l'Aranea»: reintegrata + twist figlia-di-Lorana; statblock **canon CR 8** calibrato PG 8-9 (ramo APL-13 CR 11/13-14 nel dossier); collisione risolta: «Mira del Traghetto» → «Nania Seriv del Traghetto»)_
