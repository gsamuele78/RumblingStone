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
| [PIANO-LEVEL-DESIGN-E-INQUADRATURA](PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md) | **Contenuto** (rev. 3: infrastruttura delegata al piano prodotto): scheda-mappa e riprogettazione delle mappe misurate fuori soglia · scheda-inquadratura e campo `## Inquadratura` · **ordine percettivo nel read-aloud** · Modalità 4 blockout 3D→depth · igiene IP dei prompt versionati. *(Legenda, substrato e linter sono passati al [PIANO-PRODOTTO](PIANO-PRODOTTO-TOOLKIT-VENDIBILE.md).)* | 🔵 **pianificato** (2026-07-26) | 0% | **rev. 3**: rami 0/A/B **delegati** a PIANO-PRODOTTO (fasi P0/P1/P2 — erano 12 lotti con due proprietari). Restano: C1-C3 (mappe) · D1-D4 (inquadratura/prosa) | C2 dipende da P2.1 del piano prodotto · C2/D2: prova al tavolo · C3: a mappa singola, decisione DM · D3: GPU + Blender sulla macchina DM |
| [PIANO-PRODOTTO-TOOLKIT-VENDIBILE](PIANO-PRODOTTO-TOOLKIT-VENDIBILE.md) | **Prodotto**: da repo di campagna a toolkit vendibile — separazione dei due prodotti e rilicenziamento ([ADR-0017](adr/ADR-0017-separazione-prodotto-e-rilicenziamento-toolkit.md)), legenda funzionale neutra a 62 simboli ([ADR-0014](adr/ADR-0014-legenda-funzionale-fonte-unica.md) + [spec](../docs/guides/LEGENDA-FUNZIONALE-SPEC.md)), **profili di regole 3.5 / PF1e / 5e** ([ADR-0016](adr/ADR-0016-profili-regole-multisistema.md)), confezionamento wheel + eseguibile autonomo ([ADR-0015](adr/ADR-0015-dipendenze-a-livelli-e-pacchettizzazione.md)), linter, map pack neutri, guida al metodo | 🟢 **DEFINITIVO — pronto all'esecuzione** (2026-07-26) | 0% | **P0.0** rete di sicurezza · P0.1-P0.4 (substrato) · **P0.5** fetta verticale (gate go/no-go) · P1.1-P1.3 (legenda + 3 sistemi) · **P2.0-P2.6 (verifica: contratto unico dei finding + matrice «ogni fallimento ha un check»)** · P3.1-P3.4 (wheel/exe/licenze) · P4.1-P4.2 (contenuto) · P5.1 (gate) — primo rilascio possibile dopo il passo 4 di 8 | ⚠️ **avvocato IP prima di qualunque vendita** (rilicenziamento, OGL 1.0a, CC BY 4.0, marchi) · PF1e `move_cost: 4` da confermare sul PRD · corpus di calibrazione con licenza documentata (mai RHoD, ADR-0005) |
| [PIANO-EDIZIONE-COMMERCIALE-AP-ORIGINALE](PIANO-EDIZIONE-COMMERCIALE-AP-ORIGINALE.md) | **Contenuto come prodotto**: gli archi 04-08 (**252.111 parole**) diventano un Adventure Path **originale autonomo** — mai un'espansione di RHoD ([ADR-0018](adr/ADR-0018-edizione-commerciale-ap-originale.md)). Sostituzione di pantheon/geografia/fazioni, passata di somiglianza sostanziale, OGL 1.0a + Compatibility License PF1e | 🔵 **pianificato** (2026-07-26) | 0% | E0.1-E0.2 (build derivato + check `ip/forbidden-term`) · E1.1-E1.3 (ambientazione; **E1.1 pantheon = 1.502 occorrenze di Moradin, decide la fattibilità**) · E2.1-E2.2 (de-derivazione strutturale) · E3.1-E3.3 (licenze, mappe, pubblicazione) — ~140-185 h | ⚠️ **avvocato IP: gate assorbente**, nulla si pubblica senza · decisione DM sul perimetro (arco 09 **fuori dalla v1**: 195.739 parole) · E0.2 dipende da P2.0 del piano toolkit |
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

### PIANO-LEVEL-DESIGN-E-INQUADRATURA
- ⬜ _(D2 ⭐ — ordine percettivo nel read-aloud in `narrative-style`: ~4 h, zero dipendenze, è l'item a ritorno più alto del piano)_
- ⬜ _(A1 — `scripts/legend.yaml` fonte unica: chiude **oggi** la divergenza SVG↔UVTT su `⛰ 🏛 🗼 🗿`; coincide col lotto E1 del PIANO-EDITOR — un lavoro, tre piani. **Gated**: le 4 classificazioni sono decisioni di regole 3.5, non di codice)_
- ⬜ _(C1 — `campaign/templates/scheda-mappa-template.md`: indipendente, candidabile per primo insieme a D2)_
- ⬜ _(**Ramo 0, rev. 2** — substrato: `pyproject.toml` + fine degli 11 `sys.path.insert`, dipendenze a livelli (ADR-0015), ruff/pytest, confine dominio/presentazione. È ciò che rende il toolkit **estraibile e riusabile**; serve anche al PIANO-EDITOR, che oggi non avrebbe nulla da importare)_
- ⬜ _(**rev. 3 consolidamento**: l'infrastruttura è del PIANO-PRODOTTO. Qui la sequenza è D2 → C1 → *(attesa P2.1)* → C2 → D1+D4 → D3 → C3)_
- ⬜ _(decisione DM: corpus di calibrazione delle soglie — B5 resta «euristiche dichiarate» finché non arriva)_

### PIANO-PRODOTTO-TOOLKIT-VENDIBILE
- ✅ _(decisioni DM 2026-07-26: rilicenziare il toolkit · supportare **3.5 + Pathfinder 1e + D&D 5e** · distribuire come **wheel + eseguibile autonomo** · vendere toolkit + map pack neutri + il metodo)_
- ⬜ _(P0.1-P0.3 substrato: pyproject, fine degli 11 `sys.path.insert`, livelli di dipendenza, ruff/pytest — sblocca tutto il resto)_
- ⬜ _(P1.1 `legend.yaml` 62 simboli + le 4 correzioni `⛰ 🏛 🗼 🗿`: recupera **3.689 celle di muro** nell'export UVTT di 6 mappe, a SVG invariati)_
- ⬜ _(P1.2 i tre profili di regole — **verificare `move_cost: 4` per PF1e sul PRD** prima del rilascio di quel profilo)_
- ⬜ _(**P2.0 ⭐ contratto unico dei finding + `dm.py verify`**: precede il linter, così non nasce come settimo silo — oggi i 6 validator hanno 6 forme JSON diverse. P2.5 chiude la matrice di copertura con un meta-check che la verifica da sola; P2.6 copre l'unico ramo oggi senza alcun tool, `framing/*` e `prose/*`)_
- ⬜ _(P3.3/P3.4 — **gated su verifica di un avvocato IP**: rilicenziamento, conformità OGL 1.0a per 3.5/PF1e, attribuzione CC BY 4.0 per 5e, marchi fuori dal marketing)_
- ⬜ _(decisione rimandata di proposito: repo unico con package interno **o** due repo — si decide quando il toolkit ha una superficie pubblica stabile, cioè dopo P0.4)_

### PIANO-EDIZIONE-COMMERCIALE-AP-ORIGINALE
- ✅ _(misura 2026-07-26 in `docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md`: la derivazione da RHoD **non è distribuita, è concentrata** — archi 04-08 a densità ≈ **0,5** occorrenze/1.000 parole (verniciatura di nomi), arco 09 a **5,3** (derivazione vera, per scelta del piano REINTEGRAZIONE-PNG-AP-RHOD))_
- ⬜ _(**risposta alla domanda DM**: come «espansione per RHoD» **nessuna via** — l'OGL copre le meccaniche OGC e RHoD non lo è, la CUP Paizo è non commerciale, DMs Guild non licenzia RHoD ed è solo 5e. Come **AP originale autonomo**: sì, ed è già quasi lì)_
- ⬜ _(E1.1 — **il pantheon decide**: 1.502 occorrenze di Moradin, che non è SRD ed è la spina teologica della campagna nanica. Criterio di accettazione **esterno** (lettura a freddo di un playtester), non autovalutazione)_
- ⬜ _(E2.1 — la tabella di somiglianza sostanziale per arco è **ciò che va davanti all'avvocato**, non i file: si produce a ~100 h, non a 180)_
- ⬜ _(decisione DM rimandata: se e quando l'arco 09 rientra, dopo riscrittura sostanziale valutata a sé)_

### VERIFICA LEGALE-IP (P2D "Palio")
- ⬜ _(bonifica §7 — rinomina contrade, cambio livree, riscrittura motti da zero, rimozione "Piazza il Campo", riambientazione fuori Forgotten Realms: **gated** su una decisione DM di puntare a un'edizione commerciale, non ancora presa — vedi ADR-0005)_
- ⬜ _(debito documentale a bassa priorità: correggere la nota IP interna che dichiara i motti "originali" — sono parafrasi §3.3; documentare provenienza/licenza delle 2 tavole PNG del DM)_

### PIANO-REINTEGRAZIONE-PNG-AP-RHOD
- ✅ _(R2 — secondo anello di Rethmar preparato 2026-07-20: `Bestiario/png/Secondo_Anello_Rethmar/`)_
- ✅ _(R3 — Witchwood/Tiri Kitor preparato 2026-07-20: `Bestiario/png/Witchwood_Tiri_Kitor/`; Killiar cross-linkato allo statblock d'arco)_
- ✅ _(R4 — deciso dal DM 2026-07-20: Hravek Kharn fuso in Karruk; Ulwai non reintegrata 1:1; blackspawn rilivellati → tier élite CR 13 «Razorfiend Blackspawn Alfa»)_
- ✅ _(R6 — canonizzazione DM di R1+R5 avvenuta il 2026-07-20: flag sciolti, righe applicate a state.md §1/§3/§7/§8)_
- ✅ _(R7 — Mira Serani «l'Aranea»: reintegrata + twist figlia-di-Lorana; statblock **canon CR 8** calibrato PG 8-9 (ramo APL-13 CR 11/13-14 nel dossier); collisione risolta: «Mira del Traghetto» → «Nania Seriv del Traghetto»)_
