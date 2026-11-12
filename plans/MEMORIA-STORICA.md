# 🗄️ MEMORIA STORICA — quello che la memoria corta non tiene più

> **Cos'è** ([ADR-0127](adr/ADR-0127-la-memoria-corta-archivia-nel-repo-prima-di-togliere.md)).
> La memoria del progetto, quella che ogni sessione d'agente legge all'avvio,
> ha un limite di dimensione: tiene solo regole, stato aperto, ambiente e
> puntatori. Quando una sua riga esce (PR unita, canone ormai nel repo,
> questione chiusa), i fatti che non stanno altrove finiscono **qui**, una
> voce per riga. Questo file non ha limite, non si riassume e non si
> riscrive: si aggiunge in coda. Serve a chi lavora su una regressione o
> rivede una soluzione già adottata e ha bisogno di sapere *che cosa si
> sapeva allora*.
>
> **Non è il canone e non è il changelog.** Il canone sta nei file della
> campagna e nei piani; i lotti chiusi stanno in [`CHANGELOG.md`](CHANGELOG.md),
> che porta qui; le decisioni in [`adr/`](adr/); la memoria del lavoro
> generata in [`MEMORIA.md`](../MEMORIA.md). Una voce dice cosa la memoria
> riportava a quella data e dove il fatto si ritrova nel repo; dove non si
> ritrova, lo dice nel campo **Solo qui**.

## Come si legge

```bash
python3 scripts/memoria_storica.py --pr 242        # la storia di una PR
python3 scripts/memoria_storica.py --adr 93        # di un ADR
python3 scripts/memoria_storica.py --tema prosa    # di un tema (campo Temi)
python3 scripts/memoria_storica.py Skullcrusher Virata   # parole, tutte
python3 scripts/memoria_storica.py --da 2026-10-19 --a 2026-10-20 --elenco
python3 scripts/memoria_storica.py --json --pr 380 # per un agente
```

Lo stesso strumento è esposto dal server MCP del repo (`memoria_storica`,
sola lettura). I filtri si sommano; maiuscole e accenti non contano.

## Come si scrive una voce

Due regole (ADR-0127):

- **Addendum del changelog, obbligatorio in CI**: una PR che aggiunge righe a
  [`CHANGELOG.md`](CHANGELOG.md) aggiunge anche almeno una voce qui, con le
  decisioni, le misure, le questioni aperte e i rimandi che la riga non
  tiene. `check_plans_discipline.py` boccia la PR se manca.
- **Prima di togliere una riga dalla memoria del progetto** (fuori dal repo,
  la CI non la vede) si controlla che i suoi fatti siano qui; se mancano, si
  copia la riga com'era in una voce nuova, nello stesso giro di lavoro.

Si aggiunge in coda col numero dopo l'ultimo e si fa girare
`python3 scripts/memoria_storica.py --check` (la CI fa lo stesso).

```markdown
### MS-NNNN · AAAA-MM-GG · Titolo breve, cercabile

- **Data:** AAAA-MM-GG            (la data del fatto principale; uguale al titolo)
- **PR:** #380 #379               (oppure —)
- **ADR:** ADR-0126               (oppure —)
- **Temi:** regole motore         (parole singole, minuscole, separate da spazi)
- **Origine:** memoria del progetto, riga tolta il AAAA-MM-GG
- **Testo:** la riga della memoria, intera
- **Trovato nel repo:** `#380` → `plans/CHANGELOG.md` · …   (facoltativo)
- **Fuori dal repo:** percorsi della cartella condivisa         (facoltativo)
- **Note di memoria:** `nome-nota`                              (facoltativo)
- **Solo qui:** i fatti che non si ritrovano altrove             (facoltativo)
```

Niente dati personali (nomi dei giocatori, macchine del DM, nomi utente):
quelli restano nelle note di memoria (scelta del DM del 2026-11-12).

## Da dove vengono le voci MS-0001…MS-0067

Il 2026-11-12 la memoria del progetto è stata ridotta da circa 25 KB a 8 KB
togliendo la cronologia delle PR unite. Le sue 67 righe sono state
confrontate con il repo e con le note di memoria e archiviate qui, una per
voce, col testo intero; «Jfs» è scritto «il DM» come nel resto del repo, e
tre righe hanno dati personali tolti: il DM ha scelto il 2026-11-12 di lasciarli fuori dal repo (MS-0005,
MS-0006, MS-0009).

Misura del recupero: dei **165 riferimenti** distinti delle 67 righe (PR,
SHA, ADR, percorsi della cartella condivisa) **127** si trovavano già nel
repo, **24** solo nelle note di memoria (fuori dal repo), **14** da nessuna
parte; dei 150 fatti di contenuto controllati con una ricerca testuale, **24**
non si trovavano nel repo. Ora sono tutti qui. La ricerca è testuale: un
riferimento «trovato nel repo» vuol dire che la stringa c'è in quel file, non
che il file racconti tutto il fatto; un fatto «solo qui» può esistere nel
repo scritto con altre parole.

## Voci

### MS-0001 · 2026-10-11 · Python 3.13 ovunque e i PR di Dependabot

- **Data:** 2026-10-11
- **PR:** #228 #231 #236
- **ADR:** —
- **Temi:** piattaforma dipendenze
- **Origine:** memoria del progetto, riga 1 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Python: 3.13 ovunque (D7 di AMBIENTE-RIPRODUCIBILE, vale anche per Dependabot). #231 (CI a 3.13) e #236 (i 6 aggiornamenti di Dependabot della #228, portati a mano perché Dependabot non riusciva a rigenerarla) fuse su main il 2026-10-11. La #228 è stata chiusa come superata il 2026-10-23. I commenti `@dependabot` postati da Claude arrivano con l'@ neutralizzata, quindi un recreate lo deve scrivere il DM.
- **Trovato nel repo:** `#228` → `plans/CHANGELOG.md` · `#231` → `plans/CHANGELOG.md` · `#236` → `plans/CHANGELOG.md`

### MS-0002 · 2026-10-24 · Chiusura della PR #99 e schede dei PG

- **Data:** 2026-10-24
- **PR:** #99 #289 #291
- **ADR:** ADR-0007
- **Temi:** pr schede-pg
- **Origine:** memoria del progetto, riga 2 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #99 chiusa il 2026-10-24 (scelta A del DM): echi §1-bis, nota Golarion e inventory_inferred.py riportati con la #289 (d8b2985); 4g rifatto come 4g-1/4g-2, 4h scartato (ADR-0007). 4g-2 prima parte #291 unita il 2026-10-26 (b92f1f1).
- **Trovato nel repo:** `#99` → `plans/CHANGELOG.md` · `#289` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `#291` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `ADR-0007` → `plans/adr/ADR-0007-scritture-canone-triplo-vincolo.md` · `b92f1f1` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv` · `d8b2985` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `pr99-e-schede-pg`

### MS-0003 · 2026-10-10 · Piano recupero incompiuti: #232 e #233

- **Data:** 2026-10-10
- **PR:** #72 #99 #216 #232 #233
- **ADR:** —
- **Temi:** piani adr memoria
- **Origine:** memoria del progetto, riga 3 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Piano recupero incompiuti: #232 e #233 fuse il 2026-10-10. #233 ha portato la #216 (chiusa come portata, ADR memoria = 0087), le voci #72 nel registro rami, e D7: numeri ADR prenotati in plans/adr-prenotati.json (0088 alla #99), modello ADR con alternative e «Da rivedere se», .github/pull_request_template.md. Aperte al DM: D3-D6 di RECUPERO.
- **Trovato nel repo:** `#72` → `plans/CHANGELOG.md` · `#99` → `plans/CHANGELOG.md` · `#216` → `plans/CHANGELOG.md` · `#232` → `plans/CHANGELOG.md` · `#233` → `plans/STATO-E-ORDINE-DEI-PIANI.md`

### MS-0004 · 2026-10-12 · Routine settimanale del lunedì

- **Data:** 2026-10-12
- **PR:** —
- **ADR:** —
- **Temi:** routine audit
- **Origine:** memoria del progetto, riga 4 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Routine settimanale lunedì 06:47 UTC: PR, piani aperti (plans/INDEX.md, REGISTRO-LOTTI.md), changelog. Dal 2026-10-12 pubblica anche la coda dei piani per urgenza e avvia un thread «Chiusura piano …» alla volta.
- **Solo qui:** Routine settimanale lunedì 06:47 UTC

### MS-0005 · 2026-10-11 · Push dal computer del DM

- **Data:** 2026-10-11
- **PR:** —
- **ADR:** —
- **Temi:** ambiente git
- **Origine:** memoria del progetto, riga 5 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Push locale dal computer del DM: usare `gh auth setup-git`; il gestore delle credenziali del desktop proponeva un vecchio utente. *[Sistema operativo, desktop e nome del gestore esclusi: dati personali, fuori dal repo per scelta del DM del 2026-11-12.]*

### MS-0006 · 2026-10-11 · LLM locale per la prosa bocciato (ADR-0089)

- **Data:** 2026-10-11
- **PR:** #234
- **ADR:** ADR-0089
- **Temi:** prosa llm
- **Origine:** memoria del progetto, riga 6 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** LLM locale per la prosa (ADR-0089, PR #234): gemma4 e4b bocciato il 2026-10-11 (voto 40/42%, cieco 0/10 vs B-con). Prossima prova possibile: gemma4:12b-it-qat sul portatile del DM, poi 26B su un'altra macchina del DM *[modelli delle macchine esclusi: dati personali, fuori dal repo per scelta del DM del 2026-11-12]*. Avvio: start.sh poi prova.sh; dopo un riavvio il box impiega minuti.
- **Trovato nel repo:** `#234` → `plans/CHANGELOG.md` · `ADR-0089` → `plans/adr/ADR-0089-un-llm-locale-per-la-prosa-si-misura-prima.md`

### MS-0007 · 2026-10-12 · Ramo della partita del primo tavolo

- **Data:** 2026-10-12
- **PR:** #235 #237 #240
- **ADR:** ADR-0090
- **Temi:** campagna ramo-di-gruppo
- **Origine:** memoria del progetto, riga 7 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Partita del primo tavolo: ramo `campaign-group-rumblingstone` (ADR-0090, PR #237 unita il 2026-10-12), il vecchio `-dm-gianfranco` non riceve più main. Patch della serata 2026-09-25 in /mnt/project-files/sessione-2026-09-25/. PR #235 pozioni unita il 2026-10-11. PR #240 (rune di Balvar nel Bestiario allineate al master) unita su main il 2026-10-14.
- **Trovato nel repo:** `#235` → `plans/CHANGELOG.md` · `#240` → `plans/CHANGELOG.md` · `ADR-0090` → `plans/adr/ADR-0090-la-partita-riparte-su-un-ramo-di-gruppo-nuovo.md`
- **Fuori dal repo:** `/mnt/project-files/sessione-2026-09-25/` (cartella condivisa del progetto)
- **Note di memoria:** `ramo-di-gruppo-campagna`
- **Solo qui:** `#237`

### MS-0008 · 2026-10-12 · Tattiche DEF-4 canone e Seme di Varis

- **Data:** 2026-10-12
- **PR:** #238
- **ADR:** —
- **Temi:** canone arc07 booklet
- **Origine:** memoria del progetto, riga 8 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #238 unita il 2026-10-12: tattiche DEF-4 [INFERRED] diventate canone; Seme di Varis (da DEF-1 §6-bis) è capitolo II del booklet DM (77 pp). Canone: Seme nello zaino di Tordek, lo identifica Artemis con la pergamena del re (UOM CD 21, 1 tacca) perché Brynja e Kettra non sanno usarla; le pozioni le identificano Brynja e Kettra. Aperta: quale versione delle pozioni del re in Scena 4 per gruppi futuri.
- **Trovato nel repo:** `#238` → `plans/CHANGELOG.md`

### MS-0009 · 2026-11-05 · Tavolo e registro PX

- **Data:** 2026-11-05
- **PR:** #312
- **ADR:** —
- **Temi:** campagna tavolo px
- **Origine:** memoria del progetto, riga 9 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Tavolo: chi gioca quale PG è nella nota di memoria `registro-px-gruppo` *[nomi dei giocatori esclusi: dati personali, fuori dal repo per scelta del DM del 2026-11-12]*. PX e livelli: vedi Registro PX (PR #312).
- **Trovato nel repo:** `#312` → `plans/esperimenti/p16-inferred-2026-11-04/ARC09-DECISIONI.md`

### MS-0010 · 2026-10-18 · Schede PNG e villain (ADR-0091)

- **Data:** 2026-10-18
- **PR:** #241
- **ADR:** ADR-0091
- **Temi:** schede-png canone
- **Origine:** memoria del progetto, riga 10 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Schede PNG/villain: ADR-0091 (PR #241 unita su main il 2026-10-18): statblocco Difesa/Attacco/Statistiche/Capacità speciali/Tattiche, dossier a sezioni fisse, numeri solo nello statblocco. Tutte convertite; i 5 dossier di gruppo restano come sono. Tempestas = Bardo 12 / Stormsinger 2, 70 anni; Ozyrrandion drago verde adulto GS 14, ora nel sanctum di Zalkatar (scontro unico EL 16, volta ≥15 m). Cantitrici chieriche 8/barde 4 GS 12, Dana Chierica 12/Cantante Divina 3. Con #241 tutti gli INFERRED di contenuto sono chiusi (numeri da script ora [GENERATO]). Canone da applicare dal DM sul ramo di gruppo: Belkram morendo redento dice «sono in pace» e riconosce Thorik degno degli avi e portatore della Corona.
- **Trovato nel repo:** `#241` → `plans/CHANGELOG.md` · `ADR-0091` → `plans/adr/ADR-0091-la-scheda-del-png-ha-una-forma.md`

### MS-0011 · 2026-10-18 · Versione più potente e terrificante

- **Data:** 2026-10-18
- **PR:** —
- **ADR:** —
- **Temi:** regole preferenze
- **Origine:** memoria del progetto, riga 11 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Preferenzal DM (2026-10-18): versione più potente e terrificante, nell'ordine D&D 3.5, PF1e, SRD, con fonte e divergenza dall'SRD. Dal 9/11: solo se il numero si ricostruisce da una scheda legale.
- **Note di memoria:** `feedback-numeri-piu-forti-calcolati`

### MS-0012 · 2026-10-15 · Lettore e playtester completo, Bane di Thorik

- **Data:** 2026-10-15
- **PR:** #239
- **ADR:** —
- **Temi:** arc07 canone piani
- **Origine:** memoria del progetto, riga 12 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #239 unita il 2026-10-15: PIANO-LETTORE-E-PLAYTESTER completo (ARC-07 DEF-1…DEF-5 al ciclo del master; DEF-5 senza INFERRED, D90-D92). Canone: Thorik ha il Bane contro Fauci di Aegis Fang dall'affresco A7 (serata 2026-09-25); patch di state.md §6 per il ramo di gruppo in /mnt/project-files/sessione-2026-10-15/, la applical DM. Prossimo: A3 di PIANO-MASTER-DEF (canone ARC-08 contro il tavolo), poi S1.
- **Trovato nel repo:** `#239` → `plans/CHANGELOG.md`
- **Fuori dal repo:** `/mnt/project-files/sessione-2026-10-15/` (cartella condivisa del progetto)
- **Solo qui:** patch state.md §6 in /mnt/project-files/sessione-2026-10-15/

### MS-0013 · 2026-10-18 · Domande developer dell'alto livello (ADR-0092)

- **Data:** 2026-10-18
- **PR:** #244
- **ADR:** ADR-0092
- **Temi:** misura qualita
- **Origine:** memoria del progetto, riga 13 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #244 unita il 2026-10-18: domande developer dell'alto livello (ADR-0092), D1-D3 decise, default in CI (da ARC-08 in poi; i master ARC-07 restano invariati per D2). Misura: 13 → 24 rilievi sui 9 moduli, 6½ degli 11 nuovi sono difetti veri.
- **Trovato nel repo:** `#244` → `plans/PIANO-AVVENTURE-COMMUNITY-2026-10.md` · `ADR-0092` → `plans/adr/ADR-0092-le-domande-dell-alto-livello.md`
- **Note di memoria:** `ricerca-avventure-community`

### MS-0014 · 2026-10-18 · Quattro creature dalla WE RHoD

- **Data:** 2026-10-18
- **PR:** #247 #248
- **ADR:** —
- **Temi:** bestiario canone arc09
- **Origine:** memoria del progetto, riga 14 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #247 e #248 unite il 2026-10-18: 4 creature ispirate alla WE RHoD (abishai azzurro GS 11, Spezzamente GS 12, Lucertola del tuono GS 10, Furia della Mano GS 10) canone in Bestiario/mostri/ senza INFERRED, usate in ARC-09 (tabella viaggio Day 31-42 e battaglia finale). D2 archivi chiusa per queste creature.
- **Trovato nel repo:** `#247` → `plans/CHANGELOG.md` · `#248` → `plans/STATO-E-ORDINE-DEI-PIANI.md`

### MS-0015 · 2026-10-18 · Giro developer/playtester/DM su ARC-07

- **Data:** 2026-10-18
- **PR:** #245
- **ADR:** —
- **Temi:** arc07 giro srd
- **Origine:** memoria del progetto, riga 15 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #245 unita il 2026-10-18: giro developer/playtester/DM su ARC-07 DEF-1…5 (plans/esperimenti/giro-arc07-2026-10-18/), 29 decisioni DM applicate (scelta «Tutte»), righe di scala + «Se lo divinano», 9 discrepanze SRD corrette (VERIFICA-SRD.md). Fauci GS 12 (file -cr12), voce Treant di Adamantio. Aperti: patch state.md Cintura in /mnt/project-files/giro-arc07-2026-10-18/PATCH-STATE-MD.md (la applical DM); pf di Terros 345 vs 348 con Robustezza.
- **Trovato nel repo:** `#245` → `plans/CHANGELOG.md`
- **Fuori dal repo:** `/mnt/project-files/giro-arc07-2026-10-18/PATCH-STATE-MD.md` (cartella condivisa del progetto)
- **Note di memoria:** `srd-in-rete`

### MS-0016 · 2026-10-23 · Corpus della prosa italiana

- **Data:** 2026-10-23
- **PR:** #279
- **ADR:** —
- **Temi:** prosa corpus
- **Origine:** memoria del progetto, riga 16 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Corpus prosa: PDF, box e script in /mnt/project-files/corpus-prosa/ (mai nel repo); config per PDF = carattere del read-aloud. 2026-10-23 (PR #279, nota §7): +Dragons' Lair (download senza login, 21 avventure) e Chimera «Dove le profezie sbagliano» → 2.335 box IT, 34 titoli. Fasce --stile confermate (16 titoli: -mente med 6,1‰, gerundio 1,7‰). Need Games/Isola Illyon/Liber Liber fuori rete; archive.org raggiungibile ma non usato (copie non verificabili).
- **Fuori dal repo:** `/mnt/project-files/corpus-prosa/` (cartella condivisa del progetto)
- **Solo qui:** `#279` · 2026-10-23 PR #279 +Dragons' Lair 21 avventure e Chimera → 2.335 box IT, 34 titoli

### MS-0017 · 2026-10-19 · Rifacimento ARC-07 e cieco 8 a 8

- **Data:** 2026-10-19
- **PR:** #246 #249 #251
- **ADR:** —
- **Temi:** prosa cieco arc07
- **Origine:** memoria del progetto, riga 17 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #249 unita su main il 2026-10-18 (rifacimento 5 DEF ARC-07 + giro2). Cieco del DM: 8 a 8 su 16, miglioramento non dimostrato. PR #251 unita il 2026-10-19 (prima della #246, fuori ordine): le 8 vecchie vincitrici rimesse intatte, lezione applicata agli altri box (dettagli sensoriali, nomi noti, monologhi interi; box impoveriti da 26 a 2 falsi positivi con ciclo_prosa.box_impoveriti della #246). Nomi noti rimessi = lettura della norma §2-ter, non voto (cieco diviso: coppie 5 vs 6, 10). Le 55 decisioni G2 applicate come «Tutte». Una PR in conflitto con main non fa partire la CI: guardare mergeable_state.
- **Trovato nel repo:** `#246` → `plans/CHANGELOG.md` · `#249` → `plans/CHANGELOG.md` · `#251` → `plans/PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md`

### MS-0018 · 2026-10-19 · Riscrittura ARC-07 misurata contro le versioni di prima

- **Data:** 2026-10-19
- **PR:** #246 #249 #251
- **ADR:** —
- **Temi:** prosa arc07 regole
- **Origine:** memoria del progetto, riga 18 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** 2026-10-19 Il DM: rendere standard (#246 su main) e poi ricominciare la riscrittura di ARC-07 con tutte le norme nuove, misurando contro le versioni precedenti (tag prima-rifacimento-arc07, #249=2ee82472, #251=e0ce0e6). Ogni box nuovo entra solo se verdetto_misurato/box_impoveriti non lo peggiora; cieco nuovo su campione nuovo.
- **Trovato nel repo:** `#246` → `plans/CHANGELOG.md` · `#249` → `plans/CHANGELOG.md` · `#251` → `plans/PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md` · `2ee82472` → `plans/esperimenti/a3-arc08/AUDIT-GIRI-STANDARD-2026-10-18.md` · `e0ce0e6` → `plans/esperimenti/giro3-arc07-2026-10-19/cancello.py`

### MS-0019 · 2026-10-19 · La prosa migliora solo se il DM la sceglie alla cieca (ADR-0093)

- **Data:** 2026-10-19
- **PR:** #246 #251
- **ADR:** ADR-0093
- **Temi:** prosa cieco adr
- **Origine:** memoria del progetto, riga 19 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #246 unita il 2026-10-19 (ADR-0093, ancora «proposta»): la prosa migliora solo se il DM la sceglie alla cieca (14/20 riproporzionato). Decide prima la misura (§2-ter read-aloud-adulti: meno dettagli sensoriali o monologo spezzato = perde), al cieco solo le indecise + 4 controlli. ciclo_prosa.box_impoveriti è standard. Primo cieco ARC-07 8 a 8; dopo #251 resta 1 box su 26 (DEF-4 Scena 4, Thorgrim).
- **Trovato nel repo:** `#246` → `plans/CHANGELOG.md` · `#251` → `plans/PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE.md` · `ADR-0093` → `plans/adr/ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md`

### MS-0020 · 2026-10-19 · Giro 3 ARC-07 e box congelati

- **Data:** 2026-10-19
- **PR:** #252
- **ADR:** —
- **Temi:** prosa cieco arc07
- **Origine:** memoria del progetto, riga 20 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #252 (giro 3 ARC-07) unita il 2026-10-19 (8a6b1e1). Cieco del DM: nuova 5, vecchia 4 (soglia 7/9): non dimostrato; le 4 vecchie vincitrici rimesse e i 9 box votati in giro3/misure/CONGELATI.json (25 congelati totali). -mente ancora 0,6‰ vs 3,8-13,4‰ umano.
- **Trovato nel repo:** `#252` → `plans/esperimenti/giro4-arc07-2026-10-19/cancello.py` · `8a6b1e1` → `plans/CHANGELOG.md`

### MS-0021 · 2026-10-19 · Giro 4: DEF-4/DEF-5 per la serata

- **Data:** 2026-10-19
- **PR:** #254
- **ADR:** —
- **Temi:** arc07 serata giro
- **Origine:** memoria del progetto, riga 21 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #254 (giro 4, 2026-10-19): DEF-4/DEF-5 per la serata sullo stato del ramo di gruppo; 6 letture a freddo, correzioni, regia con risorse del gruppo e tacche in volo; numeri senza fonte INFERRED con domande in plans/esperimenti/giro4-arc07-2026-10-19/DECISIONI-DM.md (+ DEF-5/). PDF serata in /mnt/project-files/sessione-notte-e-alba/. Skullcrusher resta file -cr12 col GS 14 nella Source; ERRATA §2.3 e ARC08-11-PONTE-ARRIVO da aggiornare.
- **Trovato nel repo:** `#254` → `plans/CHANGELOG.md`
- **Fuori dal repo:** `/mnt/project-files/sessione-notte-e-alba/` (cartella condivisa del progetto)

### MS-0022 · 2026-10-19 · Giro finale DEF-4/DEF-5 e simulazione del duello

- **Data:** 2026-10-19
- **PR:** #256
- **ADR:** —
- **Temi:** arc07 skullcrusher serata
- **Origine:** memoria del progetto, riga 22 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #256 unita il 2026-10-19 (22162fc): giro finale su DEF-4/DEF-5 e booklet della serata (42/48 rilievi corretti, domande 28-33 in giro4/DECISIONI-DM.md). Il DM: Skullcrusher Adulto GS 14 + 2 wyvern (non il Vecchio). Simulazione duello in giro4/finale/SIMULAZIONE-DUELLO.md (~8 round, prima versione senza Risonanza/Ali e Passo d'Ombra; rifatta con tutti gli artefatti). validate_booklets --stampa boccia rimandi «(Dnn)» nel testo stampato.
- **Solo qui:** `#256` · `22162fc` · PR #256 unita 2026-10-19 (22162fc) 42/48 rilievi

### MS-0023 · 2026-10-19 · Duello con Skullcrusher il Vecchio e Zog'tar

- **Data:** 2026-10-19
- **PR:** #242 #257
- **ADR:** —
- **Temi:** arc07 skullcrusher canone
- **Origine:** memoria del progetto, riga 23 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #257 unita il 2026-10-19 (45d1fcf): scelte del DM dopo simulazioni con tutti gli artefatti. Duello ARC-07 = Skullcrusher Vecchio + 2 wyvern EL 17 (D60 esteso al 13°), Virata al posto di Ghermire («la passata e il nome»: colpisce solo chi ha un nome, D71); la presa in bocca con caduta è di Fauci contro Thorik in ARC-08 (thread PR #242). Zog'tar: guardie che aiutano la CA, sacerdote nella tenda, >20 cariche di bacchetta = una tacca. Aperti: nome falso/silenzio, Virata da riscontrare su d20srd.
- **Trovato nel repo:** `#242` → `plans/CHANGELOG.md`
- **Solo qui:** `#257` · `45d1fcf` · PR #257 unita 2026-10-19 (45d1fcf) Skullcrusher Vecchio + 2 wyvern EL 17

### MS-0024 · 2026-10-19 · Skullcrusher sente i nomi attraverso la Catena

- **Data:** 2026-10-19
- **PR:** #258
- **ADR:** —
- **Temi:** arc07 skullcrusher canone
- **Origine:** memoria del progetto, riga 24 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #258 unita il 2026-10-19 (7f508b9): Skullcrusher non chiede i nomi, li sente attraverso la Catena (runa gemella del corno di Grask fuori dalla tenda); chi non ha sentito lo chiama per epiteto; regia allineata al Vecchio EL 17. Aperto [INFERRED]: portata del sussurro. PDF finali in /mnt/project-files/sessione-notte-e-alba/.
- **Trovato nel repo:** `#258` → `plans/STATO-E-ORDINE-DEI-PIANI.md`
- **Fuori dal repo:** `/mnt/project-files/sessione-notte-e-alba/` (cartella condivisa del progetto)
- **Solo qui:** `7f508b9`

### MS-0025 · 2026-10-20 · Fauci in ARC-08: presa in bocca

- **Data:** 2026-10-20
- **PR:** #242
- **ADR:** ADR-0095
- **Temi:** arc08 fauci canone
- **Origine:** memoria del progetto, riga 25 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #242 unita il 2026-10-20 (thread «Chiusura piano LETTORE-PLAYTESTER · F4»; standard del giro = ADR-0095, perché 0094 era già usato). Fauci in ARC-08: presa in bocca (presa migliorata, CA normale, niente AdO), solleva Thorik senza sforzo, Scalare CD 25 sul collo; cicatrice ancestrale da Aegis Fang, Fauci riconosce l'ascia e chiama Thorik «Portatore» (i nomi sono di Skullcrusher). Regola della casa PF1e Called Shots solo per questo scontro: occhio −10, ala −2. Aperti: D4-D6 (flashback pregen, risposte A3, censimento versioni), cosa succede sul collo, discesa da ala colpita (proposti 22,5 m).
- **Trovato nel repo:** `#242` → `plans/CHANGELOG.md` · `ADR-0095` → `plans/adr/ADR-0095-il-giro-ha-correzione-verifica-e-seconda-passata.md`

### MS-0026 · 2026-10-28 · Mappe a scala reale e barile sulla tenda

- **Data:** 2026-10-28
- **PR:** #261 #262 #292 #296
- **ADR:** —
- **Temi:** mappe arc07
- **Origine:** memoria del progetto, riga 26 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Mappe a scala reale (2026-10-21): PR #261 tenda di Zog'tar e campo, PR #262 altre 13 mappe ARC-07/09; simbolo 🎪 per i teli. PR #292 unita il 2026-10-28 (0a67e19): barile sulla tenda di Zog'tar, M7-C e M7-H; B16-B21 decise; B22-B25 decise dal DM il 2026-10-29 e unite con la PR #296 (21d4a8a), nessun INFERRED nel documento.
- **Trovato nel repo:** `#261` → `plans/esperimenti/barile-zogtar-2026-10-24/genera_mappe.py` · `#292` → `CHANGELOG.md` · `#296` → `CHANGELOG.md` · `0a67e19` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv` · `21d4a8a` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `mappe-scala-reale`
- **Solo qui:** `#262`

### MS-0027 · 2026-10-21 · Skill scrittura-italiana come eccezione (ADR-0097)

- **Data:** 2026-10-21
- **PR:** #260
- **ADR:** ADR-0097
- **Temi:** prosa adr contratto-seme
- **Origine:** memoria del progetto, riga 27 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #260 unita il 2026-10-21 (e639efa, ADR-0097 accettata): skill esterna scrittura-italiana (CC BY-SA, commit e397599, mai nel repo) usata solo come eccezione via references/scrittura-italiana-eccezione.md (documenti-regole in gioco, testi non capiti, Gulpease <60); colonna `Gulp.` in misura_craft --stile. Cieco DEF-4/DEF-5: nuova 10, vecchia 3 (soglia esatta); perse le 2 del «grigio» di Zog'tar. Handout DM/giocatore del contratto del Seme in /mnt/project-files/contratto-seme/; dissolvi superiore = regola 3.5 (CD 20, l'anticipo speso resta), scritto nella clausola 8; handout da portare in ARC07-HANDOUTS.
- **Trovato nel repo:** `#260` → `plans/CHANGELOG.md` · `ADR-0097` → `plans/adr/ADR-0097-scrittura-italiana-entra-come-eccezione.md` · `e397599` → `plans/adr/ADR-0097-scrittura-italiana-entra-come-eccezione.md`
- **Fuori dal repo:** `/mnt/project-files/contratto-seme/` (cartella condivisa del progetto)
- **Solo qui:** `e639efa`

### MS-0028 · 2026-10-22 · Ricerca sulla qualità misurabile

- **Data:** 2026-10-22
- **PR:** #264
- **ADR:** —
- **Temi:** prosa misura qualita
- **Origine:** memoria del progetto, riga 28 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #264 (2026-10-22, lotto 7 di AVVENTURE-COMMUNITY): ricerca sulla qualità misurabile (plans/RICERCA-QUALITA-MISURABILE-2026-10.md). 17 misure di prosa provate sui 38 voti ciechi del DM: nessuna lo prevede (vincono le versioni con più possessivi, p 0,057), quindi niente cancelli di prosa nuovi. 7a: `cieco_versioni` accetta etichette del perché (`7 B goffo spiega`, dieci da LAMP/TTCW). 7b: D18-D21 in domande_developer (domanda della scena, scelta con conseguenza, presagio del boss, rete indizi marcata `<!-- conclusione C1 -->`/`<!-- indizio C1 -->`), cancello solo sui master nuovi, 30 residui. 7c fronti/orologi in attesa del DM.
- **Trovato nel repo:** `#264` → `plans/STATO-E-ORDINE-DEI-PIANI.md`

### MS-0029 · 2026-10-23 · Rete del container: Hugging Face

- **Data:** 2026-10-23
- **PR:** —
- **ADR:** —
- **Temi:** ambiente rete
- **Origine:** memoria del progetto, riga 29 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Hugging Face dal container: funziona dal 2026-10-22, ma con HF_HUB_DISABLE_XET=1. Dal 2026-10-23 l'ambiente apre anche xethub, pytorch, SRD 3.5/PF1e, LanguageTool, Debian, typst.Ricerca web: se Firecrawl manca, WebSearch/WebFetch/curl via proxy.
- **Note di memoria:** `hugging-face-rete` · `ricerca-web-senza-firecrawl`

### MS-0030 · 2026-10-23 · Stanza contro spaCy

- **Data:** 2026-10-23
- **PR:** #264 #270
- **ADR:** —
- **Temi:** prosa sintassi misura
- **Origine:** memoria del progetto, riga 30 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #270 unita il 2026-10-23 nel ramo della #264, su main con la #264 (bfe0e39): Stanza contro spaCy (anche spaCy lg, peggio del md; tratti esterni Stanza + perplessità Qwen2.5-0.5B in sintassi/stanza/tratti-esterni.json). Stanza non vince (precisione dei calchi 87% contro 90%, calibrazione più debole, 50-100 volte più lento), quindi misura_sintassi resta con spaCy. Su 54 coppie votate nessuna misura sintattica passa Bonferroni. Segnalato: in riscrittura/ESITO-VOTO.md B08 la vince N, non V.
- **Trovato nel repo:** `#264` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `#270` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `bfe0e39` → `plans/STATO-E-ORDINE-DEI-PIANI.md`

### MS-0031 · 2026-10-22 · Watabou dal container

- **Data:** 2026-10-22
- **PR:** —
- **ADR:** —
- **Temi:** mappe citta
- **Origine:** memoria del progetto, riga 31 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Watabou pilotabile dal container dal 2026-10-22: piante Rethmar/Dauth/Channathgate in /mnt/project-files/mappe-valle-2026-10-22/watabou/.
- **Fuori dal repo:** `/mnt/project-files/mappe-valle-2026-10-22/watabou/` (cartella condivisa del progetto)
- **Note di memoria:** `watabou-generatore`

### MS-0032 · 2026-10-22 · Città della valle e taglie

- **Data:** 2026-10-22
- **PR:** #269 #271 #272
- **ADR:** —
- **Temi:** mappe citta canone
- **Origine:** memoria del progetto, riga 32 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Città della valle (PR #269, #271, #272 su main il 2026-10-22): entrano solo le piante del generatore nostro, non Watabou. Taglie scelte dal DM per reggere l'orda di ~10.000: Rethmar capitale ~18.000 ab., 110 ha, mura 4,3 km senza fossato; Dauth ~7.000, 42 ha, murata sullo sperone; Channathgate città aperta ~25.000, 250 ha, la più popolosa. Aperta: guarnigione nanica di Dauth.
- **Trovato nel repo:** `#269` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `#271` → `plans/STATO-E-ORDINE-DEI-PIANI.md` · `#272` → `plans/STATO-E-ORDINE-DEI-PIANI.md`

### MS-0033 · 2026-11-09 · Piattaforma a tre canali

- **Data:** 2026-11-09
- **PR:** #273 #353 #359
- **ADR:** ADR-0099
- **Temi:** piattaforma ci
- **Origine:** memoria del progetto, riga 33 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Piattaforma (ADR-0099, PR #273): tre canali Debian, Python 3.13. PR #353 unita il 2026-11-08 (125e535): ruff, uv, converters/ stable; xdist in testing fino al 22/11; ruleset da aggiornare dal DM. Job Python 3.14 non bloccante dal 2026-11-09 (#359).
- **Trovato nel repo:** `#273` → `plans/CHANGELOG.md` · `#353` → `plans/esperimenti/promozioni-2026-11-08/MISURE.md` · `#359` → `plans/esperimenti/python-314-2026-11-09/MISURE.md` · `ADR-0099` → `plans/adr/ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md`
- **Note di memoria:** `piattaforma-promozioni-stable` · `piattaforma-di-sviluppo`
- **Solo qui:** `125e535`

### MS-0034 · 2026-10-23 · Rilascio v1.0.0

- **Data:** 2026-10-23
- **PR:** #275
- **ADR:** —
- **Temi:** rilasci documentazione
- **Origine:** memoria del progetto, riga 34 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Rilasci: PR #275 unita il 2026-10-23, v1.0.0 pubblicata (skill riproducibili, SHA256SUMS, Sigstore). Rilasciare = PR con `## [X.Y.Z]` in CHANGELOG.md e `__version__`; ogni cambio di superficie pubblica va in «Non rilasciato». Architettura in docs/ARCHITETTURA.md (20 diagrammi Mermaid, poi 26).
- **Trovato nel repo:** `#275` → `plans/CHANGELOG.md`

### MS-0035 · 2026-10-23 · Merge passato al thread padre

- **Data:** 2026-10-23
- **PR:** —
- **ADR:** —
- **Temi:** regole pr
- **Origine:** memoria del progetto, riga 35 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regolal DM 2026-10-23: a CI verde il thread figlio avvisa i thread interessati e passa il merge al thread padre, che tiene la lista delle PR aperte.
- **Note di memoria:** `chiusura-pr-dai-thread-figli`

### MS-0036 · 2026-10-23 · Pipeline prova-1, modello di preferenza e lotto 7

- **Data:** 2026-10-23
- **PR:** #285 #286
- **ADR:** ADR-0102
- **Temi:** prosa misura canone
- **Origine:** memoria del progetto, riga 36 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** 2026-10-23 voto DM pipeline prova-1: pipeline 4/orig 1/pari 1 (non dimostrato); modello di preferenza passa SOGLIA (0,661 su 59, 5/5 in prospettiva) → `migliora` tiene l'originale se la migliore < 0,5. Aperta per il DM: i voti ciechi premiano i possessivi, contro italiano-nativo §1. ADR-0102 va al thread schede PNG. Poi PR #285 unita il 2026-10-23 (f2da2512): lotto 7 chiuso, D4 schede ARC-08 al Bestiario (nella #286), D5 possessivo vietato solo su corpo/cose addosso, D6 fronti e orologi canone da ARC-08 (`ARCnn-FRONTI.yaml` in CI, orologio a tempo con `unita`).
- **Trovato nel repo:** `#286` → `plans/CHANGELOG.md` · `ADR-0102` → `plans/adr/ADR-0102-lo-stile-delle-piante-e-i-generatori-delle-citta-nel-repo.md`
- **Solo qui:** `#285` · `f2da2512` · PR #285 unita 2026-10-23 (f2da2512) lotto 7 chiuso

### MS-0037 · 2026-10-23 · P15 chiuso: CHANGELOG a 5 colonne

- **Data:** 2026-10-23
- **PR:** #283
- **ADR:** —
- **Temi:** piani ci
- **Origine:** memoria del progetto, riga 37 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #283 unita il 2026-10-23: P15 chiuso (intestazioni piani = INDEX, CHANGELOG a 5 colonne con controllo in check_plans_discipline.py, RECUPERO D3/D4 spostate in RIPRESA-PR D2/D11; §4 a 14 aperte).
- **Trovato nel repo:** `#283` → `plans/CHANGELOG.md`

### MS-0038 · 2026-10-23 · Inventario Gemini/AI Studio

- **Data:** 2026-10-23
- **PR:** #284
- **ADR:** —
- **Temi:** inventario
- **Origine:** memoria del progetto, riga 38 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Inventario Gemini/AI Studio contro il repo: PR #284 unita il 2026-10-23, D1-D6 al DM.
- **Note di memoria:** `inventario-gemini-aistudio`
- **Solo qui:** `#284` · Inventario Gemini PR #284

### MS-0039 · 2026-10-24 · Archi senza testo: censimento e decisioni

- **Data:** 2026-10-24
- **PR:** #287 #290
- **ADR:** —
- **Temi:** archi censimento
- **Origine:** memoria del progetto, riga 39 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** PR #287 unita il 2026-10-23 (censimento file non markdown archi 00-10, arco 05 trascritto). D1-D12 decise dal DM il 2026-10-24, PR #290 unita (b1500ca1): cronaca corretta, P28 chiuso, testi altrui in */_testi-altrui/, P30 aperto su P30-a.
- **Trovato nel repo:** `#287` → `plans/STATO-E-ORDINE-DEI-PIANI.md`
- **Note di memoria:** `archi-senza-testo`
- **Solo qui:** `#290` · `b1500ca1` · D1-D12 decise 2026-10-24, PR #290 (b1500ca1) P28 chiuso, _testi-altrui, P30-a

### MS-0040 · 2026-10-29 · Personaggi in posa con l'AI (ADR-0104)

- **Data:** 2026-10-29
- **PR:** —
- **ADR:** ADR-0015 ADR-0104
- **Temi:** immagini adr
- **Origine:** memoria del progetto, riga 40 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Personaggi in posa con l'AI (2026-10-29): esiste già catena testo-solo (ADR-0015/0019, GUIDA-IMMAGINI, comfyui_batch), manca posa/identità da immagine; ADR-0104 proposta, D1-D4 al DM.
- **Trovato nel repo:** `ADR-0015` → `plans/adr/ADR-0015-standard-prompt-immagine.md` · `ADR-0104` → `plans/PIANO-STANDARD-STAMPA.md`
- **Note di memoria:** `immagini-personaggi-in-posa`

### MS-0041 · 2026-10-31 · Standard di stampa (ADR-0105, ADR-0106)

- **Data:** 2026-10-31
- **PR:** #295 #298
- **ADR:** ADR-0105 ADR-0106
- **Temi:** stampa booklet mappe
- **Origine:** memoria del progetto, riga 41 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Standard di stampa: PR #295 unita il 2026-10-29 (fe93e5b; ADR-0105 con D5 = appendice delle creature + tattica nell'incontro). PR #298 unita il 2026-10-31 (ae8d1884): ADR-0106, ogni mappa in pianta da stampa, nessun disegno a caratteri stampato nei booklet (validate_booklets), schemi da render_schemi.py. Piano STANDARD-STAMPA ancora in corso.
- **Trovato nel repo:** `#295` → `plans/CHANGELOG.md` · `#298` → `plans/CHANGELOG.md` · `ADR-0105` → `plans/adr/ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md` · `ADR-0106` → `plans/adr/ADR-0106-ogni-mappa-si-stampa-in-pianta.md` · `fe93e5b` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `riquadro-creature-booklet`
- **Solo qui:** `ae8d1884`

### MS-0042 · 2026-10-30 · Cuore della Montagna: schieramento dei nani

- **Data:** 2026-10-30
- **PR:** —
- **ADR:** —
- **Temi:** mappe arc08 canone
- **Origine:** memoria del progetto, riga 42 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Cuore della Montagna (2026-10-30): 90 nani schierati verso la porta (centro pesante, ali piegate), numeri invariati; allineata anche ARC-08 MAPPA 5.
- **Note di memoria:** `cuore-montagna-nani`

### MS-0043 · 2026-10-31 · Regola: vince la decisione senza regressione

- **Data:** 2026-10-31
- **PR:** —
- **ADR:** —
- **Temi:** regole decisioni
- **Origine:** memoria del progetto, riga 43 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regolal DM 2026-10-31: tra decisioni che si superano vince quella senza regressione misurabile, i dubbi vanno a card con la consigliata. Voci ⬜ dell'indice §0 lavorate un thread alla volta.
- **Note di memoria:** `decisioni-superate-regressione`

### MS-0044 · 2026-11-02 · Stand alone Il Giardino di Sale e Calce

- **Data:** 2026-11-02
- **PR:** #301
- **ADR:** —
- **Temi:** stand-alone
- **Origine:** memoria del progetto, riga 44 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Stand alone «Il Giardino di Sale e Calce» dalla chat Gemini: PR #301 unita il 2026-11-02 (2cf8a0d): modulo 3.5 a Rethmar e PF1e a Qasr al-Milah; resta un tavolo vero.
- **Trovato nel repo:** `#301` → `plans/CHANGELOG.md` · `2cf8a0d` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `standalone-giardino-sale-calce`

### MS-0045 · 2026-11-01 · Drappo e Palio misurati

- **Data:** 2026-11-01
- **PR:** #302
- **ADR:** —
- **Temi:** stand-alone misura
- **Origine:** memoria del progetto, riga 45 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Drappo/Palio misurati (2026-11-01): il Drappo deriva dal Palio, 0 frasi in comune, 62% dell'impianto condiviso; PR #302 unita (229adc6) con lo spostamento del Drappo in 10-stand-alone/Il-Drappo-di-Tarsilia e i rimandi nei due sensi.
- **Trovato nel repo:** `#302` → `plans/CHANGELOG.md` · `229adc6` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `drappo-palio-genealogia`

### MS-0046 · 2026-11-03 · Fork e upstream EarlRagnar78

- **Data:** 2026-11-03
- **PR:** #33
- **ADR:** —
- **Temi:** fork git
- **Origine:** memoria del progetto, riga 46 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Fork: gsamuele78/RumblingStone è fork di EarlRagnar78/RumblingStone. Il DM (2026-11-02): PR dal fork verso EarlRagnar78, in conflitto vince il fork; merge su EarlRagnar78 solo col sì del DM e a fork stabile. Il 2026-11-03 la PR #33 su EarlRagnar78 (59ff922) ha riallineato i due main, alberi identici.
- **Trovato nel repo:** `#33` → `plans/adr/ADR-0075-il-ciclo-del-master-vale-per-ogni-piano.md`
- **Note di memoria:** `fork-e-upstream`
- **Solo qui:** `59ff922` · 59ff922

### MS-0047 · 2026-11-03 · Serata del 2026-11-02 e booklet v5

- **Data:** 2026-11-03
- **PR:** #305
- **ADR:** —
- **Temi:** serata booklet arc07
- **Origine:** memoria del progetto, riga 47 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Serata 2026-11-02 (il DM): si riparte dal volo sul campo, pozioni di Kettra fatte, si rigioca lo sgancio del barile. PR #305: barile cucito in DEF-4 Scene 6/9/10/11 + Echo Ledger, riga in DEF-5, regia «dal barile al drago», colophon v2. PDF in /mnt/project-files/sessione-2026-11-02/. Ramo di gruppo fermo alla sessione 4 (25/09): patch Bane (10-15), Cintura (10-18) e canone Belkram mai applicate. In locale typst 0.15.1 va scaricato nello scratchpad (install in /usr/local/bin negato). Poi (2026-11-03) booklet v5 con cap. II «Chi c'è stanotte» (chi è/vuole/aspetto/ritratto/scheda + mappe M7-C/M7-H), barile cap. III, manifest `"schede": "entrambe"` (scheda nel capitolo E appendice, il DM lo vuole); CI verde su 651cf82.
- **Trovato nel repo:** `#305` → `plans/CHANGELOG.md`
- **Fuori dal repo:** `/mnt/project-files/sessione-2026-11-02/` (cartella condivisa del progetto)
- **Solo qui:** `651cf82` · PDF /mnt/project-files/sessione-2026-11-02/ · 651cf82

### MS-0048 · 2026-11-02 · Booklet pronto solo dopo lettura da DM

- **Data:** 2026-11-02
- **PR:** —
- **ADR:** —
- **Temi:** regole booklet
- **Origine:** memoria del progetto, riga 48 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Feedback del DM 2026-11-02: booklet pronto solo dopo lettura da DM scena per scena.
- **Note di memoria:** `booklet-letto-da-dm`

### MS-0049 · 2026-11-03 · Usabilità al tavolo (ADR-0107, ADR-0108)

- **Data:** 2026-11-03
- **PR:** #305 #306
- **ADR:** ADR-0107 ADR-0108
- **Temi:** booklet adr usabilita
- **Origine:** memoria del progetto, riga 49 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Usabilità al tavolo: PR #306 unita il 2026-11-03 (47489fb) con dentro la #305. ADR-0107 e ADR-0108 accettate: chi_si_incontra+entrambe in 6 booklet (Terros escluso), cancelli in ogni skill, NLI provata e non adottata. Card al DM: 4 conti dei master all'SRD.
- **Trovato nel repo:** `#305` → `plans/CHANGELOG.md` · `#306` → `plans/CHANGELOG.md` · `ADR-0107` → `plans/adr/ADR-0107-chi-si-incontra-sta-nel-capitolo.md` · `ADR-0108` → `plans/adr/ADR-0108-i-cancelli-deterministici-stanno-in-ogni-skill.md` · `47489fb` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `usabilita-al-tavolo`

### MS-0050 · 2026-11-03 · Documentazione dopo la #306

- **Data:** 2026-11-03
- **PR:** #306 #307 #308 #309
- **ADR:** —
- **Temi:** documentazione
- **Origine:** memoria del progetto, riga 50 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Documentazione dopo la #306: PR #307 unita il 2026-11-03 (90db0f7), allineata a #308 e #309 (ARCHITETTURA 26 diagrammi, §10.1/§11-§13/§16/§18/§19; README 107 ADR; GUIDA-BOOKLET-E-PDF). Ogni PR che aggiunge una riga a plans/CHANGELOG.md rigenera MEMORIA.md.
- **Trovato nel repo:** `#306` → `plans/CHANGELOG.md` · `#307` → `plans/CHANGELOG.md` · `#308` → `plans/CHANGELOG.md` · `#309` → `plans/CHANGELOG.md` · `90db0f7` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`

### MS-0051 · 2026-11-03 · Tecnica scartata: rifarla con configurazione rigorosa

- **Data:** 2026-11-03
- **PR:** #308 #309
- **ADR:** —
- **Temi:** regole misura
- **Origine:** memoria del progetto, riga 51 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Feedback del DM 2026-11-03: una tecnica scartata va rifatta con configurazione rigorosa e rimisurata; ciò che un controllo trova si corregge e il controllo diventa cancello (PR #308, PR #309 unita 008c07c, NLI fedeltà in ciclo_prosa).
- **Trovato nel repo:** `#308` → `plans/CHANGELOG.md` · `#309` → `plans/CHANGELOG.md` · `008c07c` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `feedback-configurazione-rigorosa`

### MS-0052 · 2026-11-07 · P16 marcature INFERRED da 240 a 25

- **Data:** 2026-11-07
- **PR:** #310 #311 #313
- **ADR:** —
- **Temi:** inferred marcature
- **Origine:** memoria del progetto, riga 52 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** P16 marcature INFERRED: 240 → 25 aperte (#310, #311 unite; #313 con i lotti 3-5 unita il 2026-11-07). Le 25 restanti sono righe di regole. Termine ufficiale «Sbilanciare», mai «sgambetto».
- **Trovato nel repo:** `#310` → `Bestiario/pregen-pcgen/Myconid Sovereign - Monster Stat Block - Kassoon.com_files/js.js` · `#311` → `plans/esperimenti/p16-inferred-2026-11-04/ARC07-DECISIONI.md` · `#313` → `plans/CHANGELOG.md`
- **Note di memoria:** `p16-marcature-inferred`

### MS-0053 · 2026-11-04 · Card chiuse solo se risolte

- **Data:** 2026-11-04
- **PR:** —
- **ADR:** —
- **Temi:** regole card
- **Origine:** memoria del progetto, riga 53 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regolal DM 2026-11-04: card chiuse solo se già fatte/risolte/superate (con prova).
- **Note di memoria:** `card-solo-se-risolte`

### MS-0054 · 2026-11-05 · Registro PX completato al 25/09

- **Data:** 2026-11-05
- **PR:** #312
- **ADR:** —
- **Temi:** campagna px
- **Origine:** memoria del progetto, riga 54 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Registro PX = CalcoloPuntiEperienza-current.ods (+ campaign/REGISTRO-PX.md), completato fino al 25/09 con le card del DM del 2026-11-05 (PR #312): Th/To/Ar al 14° fermi a 104.999, Hella 86.354 passa nella notte di DEF-4. Storia giocata archi 00-06 in plans/esperimenti/p16-inferred-2026-11-04/STORIA-ARCHI-00-06.md.
- **Trovato nel repo:** `#312` → `plans/esperimenti/p16-inferred-2026-11-04/ARC09-DECISIONI.md`
- **Note di memoria:** `registro-px-gruppo`
- **Solo qui:** STORIA-ARCHI-00-06.md

### MS-0055 · 2026-11-05 · Indice §0 al 4-5 novembre

- **Data:** 2026-11-05
- **PR:** #300 #310 #311 #312
- **ADR:** ADR-0114
- **Temi:** piani inferred
- **Origine:** memoria del progetto, riga 55 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Indice §0 (2026-11-04/05): #300 unita (8d4bb89, P17/P18/P26); P16 con #310 (ARC-08 109→11), #311 (mare a 520 m, ARC-07 70→1), #312 (fcf6642): 61 aperte sul repo. RECUPERO D5 rifatta col criterio del DM: 2 card aperte. Card «guida agenti» ritirata l'8/11: superata da ADR-0114 (esempi in evals/, testo letto = dato).
- **Trovato nel repo:** `#310` → `Bestiario/pregen-pcgen/Myconid Sovereign - Monster Stat Block - Kassoon.com_files/js.js` · `#311` → `plans/esperimenti/p16-inferred-2026-11-04/ARC07-DECISIONI.md` · `#312` → `plans/esperimenti/p16-inferred-2026-11-04/ARC09-DECISIONI.md` · `ADR-0114` → `plans/adr/ADR-0114-ogni-prompt-ha-una-scheda-e-le-sue-prove.md` · `8d4bb89` → `plans/esperimenti/p16-inferred-2026-11-04/ARC08-DECISIONI.md` · `fcf6642` → `plans/esperimenti/p16-inferred-2026-11-04/ARC09-DECISIONI.md`
- **Solo qui:** `#300` · #300 unita (8d4bb89, P17/P18/P26) · Card guida agenti ritirata l'8/11 superata da ADR-0114

### MS-0056 · 2026-11-07 · Standard marcature INFERRED (ADR-0109)

- **Data:** 2026-11-07
- **PR:** #314
- **ADR:** ADR-0109
- **Temi:** inferred adr
- **Origine:** memoria del progetto, riga 56 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Standard marcature INFERRED (2026-11-07, PR #314): ADR-0109, A/B 11 meglio/4 peggio, P16 a 0, migrazione ACCEPTED→CANONE e controlla_marche.py fatti; resta card statblock potenziati.
- **Trovato nel repo:** `#314` → `plans/PIANO-SISTEMI-DI-GIOCO-PLUGIN.md` · `ADR-0109` → `plans/adr/ADR-0109-una-marcatura-sola-e-il-dm-decide-il-canone.md`
- **Note di memoria:** `standard-marcature-inferred`

### MS-0057 · 2026-11-09 · Regolamenti plugin e motore (ADR-0111, ADR-0112)

- **Data:** 2026-11-09
- **PR:** #355 #361
- **ADR:** ADR-0111 ADR-0112
- **Temi:** motore plugin
- **Origine:** memoria del progetto, riga 57 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regolamenti plugin ADR-0111 e motore ADR-0112: tutto su main (L0-L8, F0-F6, #355, #361 19c8670); piano chiuso il 9/11.
- **Trovato nel repo:** `#361` → `plans/esperimenti/plugin-regole-2026-11-09/RAPPORTO.md` · `ADR-0111` → `plans/adr/ADR-0111-il-sistema-di-gioco-e-un-plugin-di-dati.md` · `ADR-0112` → `plans/adr/ADR-0112-il-motore-e-agnostico-e-le-regole-d20-sono-dati-e-formule.md`
- **Note di memoria:** `regolamenti-plugin-cronologia` · `sistemi-di-gioco-plugin`
- **Solo qui:** `#355` · `19c8670`

### MS-0058 · 2026-11-08 · Regola: si parte dallo standard di fatto

- **Data:** 2026-11-08
- **PR:** —
- **ADR:** —
- **Temi:** regole dipendenze
- **Origine:** memoria del progetto, riga 58 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regolal DM 2026-11-08 (codice, mappe, storia, editoria, booklet): si parte dallo standard de facto, il fatto in casa entra solo se la misura boccia lo standard (motivo nell'ADR); librerie dentro il pacchetto (modello iemod-fetch). Librerie oltre la stdlib solo se standard di fatto e la misura dice che migliorano (D1 del motore: simpleeval e fastjsonschema dentro; pydantic fuori perché non prende un difetto in più).
- **Note di memoria:** `feedback-standard-di-fatto`

### MS-0059 · 2026-11-07 · Termini ufficiali, razze PF1e e oggetti unici

- **Data:** 2026-11-07
- **PR:** #314 #315 #316 #317 #318 #319
- **ADR:** ADR-0110
- **Temi:** regole lessico canone
- **Origine:** memoria del progetto, riga 59 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** 2026-11-07: #315, #314, #316 (ADR-0110) e #318 (eae2126: fase 5 ARC-07/08, 37 razze PF1e tipo «razza» per il plugin #317) unite. A/B rifatta C10/C11/C16: 2 inventati non marcati contro 15/12. Oggetti unici in campaign/OGGETTI-DELLA-CAMPAGNA.md (esito `campagna` del controllo). Schede dei 152 termini sconosciuti con scelta del DM: artifact K9QvJMTuxvwK7mBPxF2fuD (db: termini, scelte); PR #319 le applica. Criterio Il DM: termine sconosciuto → SRD → 3.5 → PF1e.
- **Trovato nel repo:** `#314` → `plans/PIANO-SISTEMI-DI-GIOCO-PLUGIN.md` · `#315` → `skills/forgotten-realms-lore/references/fr-feats.md` · `#316` → `plans/PIANO-SISTEMI-DI-GIOCO-PLUGIN.md` · `#318` → `plans/PIANO-SISTEMI-DI-GIOCO-PLUGIN.md` · `#319` → `plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md` · `ADR-0110` → `plans/adr/ADR-0110-i-termini-ufficiali-hanno-una-tabella-e-un-cancello.md` · `eae2126` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `fonti-nomi-italiani-regole`
- **Solo qui:** `#317` · 152 termini sconosciuti artifact K9QvJMTuxvwK7mBPxF2fuD; PR #319

### MS-0060 · 2026-11-07 · Indici dei talenti 3.5/PF1e

- **Data:** 2026-11-07
- **PR:** #319 #328
- **ADR:** —
- **Temi:** regole talenti
- **Origine:** memoria del progetto, riga 60 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Talenti 3.5/PF1e (#319-#328, 2026-11-07): indici tsv, sconosciuti 0, cricchetto CI a 0.
- **Trovato nel repo:** `#319` → `plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md`
- **Note di memoria:** `talenti-indici-2026-11-07`
- **Solo qui:** `#328` · Talenti #319-#328 indici tsv sconosciuti 0 cricchetto

### MS-0061 · 2026-11-08 · Prompt a schede (ADR-0114)

- **Data:** 2026-11-08
- **PR:** #339 #343
- **ADR:** ADR-0114
- **Temi:** prompt skill
- **Origine:** memoria del progetto, riga 61 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Standard dei prompt a schede: PR #339 unita il 2026-11-08 (d0cc674, ADR-0114): GUIDA-SCHEDE-PROMPT, 54 prove in skills/*/evals/, prove_skill.py. Lotto 2: PR #343 unita (A/B 32→30 inventati; ADR-0114 accettata). Resta: avvisi check_schede bloccanti dopo 2 settimane.
- **Trovato nel repo:** `ADR-0114` → `plans/adr/ADR-0114-ogni-prompt-ha-una-scheda-e-le-sue-prove.md` · `d0cc674` → `plans/esperimenti/promozioni-2026-11-08/lista.tsv`
- **Note di memoria:** `standard-prompt-a-schede`
- **Solo qui:** `#339` · `#343` · PR #339 (d0cc674 ADR-0114) 54 prove skills/*/evals, prove_skill.py; lotto 2 PR #343 A/B 32→30 · #343

### MS-0062 · 2026-11-08 · Strumenti binari da PyPI (ADR-0116)

- **Data:** 2026-11-08
- **PR:** #338 #341 #342
- **ADR:** ADR-0113 ADR-0116
- **Temi:** piattaforma strumenti
- **Origine:** memoria del progetto, riga 62 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Strumenti binari: ADR-0113 (mise, #338/#341) superata da ADR-0116 (PR #342, 29056bf): typst e pdfimpose da PyPI, mise/Renovate/strumenti.py tolti, bundle_offline.py nel rilascio. Check richiesti su main = Validate + Build skill packages.
- **Trovato nel repo:** `#338` → `plans/adr/ADR-0113-gli-strumenti-binari-si-installano-da-un-lockfile.md` · `#341` → `plans/CHANGELOG.md` · `#342` → `plans/CHANGELOG.md` · `ADR-0113` → `plans/adr/ADR-0113-gli-strumenti-binari-si-installano-da-un-lockfile.md` · `ADR-0116` → `plans/adr/ADR-0116-typst-si-installa-da-pypi.md` · `29056bf` → `plans/esperimenti/promozioni-2026-11-08/MISURE.md`
- **Note di memoria:** `strumenti-binari-lockfile`

### MS-0063 · 2026-11-08 · Roadmap unica del motore

- **Data:** 2026-11-08
- **PR:** —
- **ADR:** —
- **Temi:** roadmap
- **Origine:** memoria del progetto, riga 63 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Roadmap unica: /mnt/project-files/roadmap-motore-2026-11-08/DECISIONI-E-ROADMAP.md.
- **Fuori dal repo:** `/mnt/project-files/roadmap-motore-2026-11-08/DECISIONI-E-ROADMAP.md` (cartella condivisa del progetto)
- **Solo qui:** Roadmap unica DECISIONI-E-ROADMAP.md

### MS-0064 · 2026-11-10 · Merge del 10 novembre e blocco 1

- **Data:** 2026-11-10
- **PR:** #363 #364 #365 #366 #367 #368
- **ADR:** ADR-0118 ADR-0120 ADR-0122
- **Temi:** pr motore
- **Origine:** memoria del progetto, riga 64 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** 2026-11-10 su main: #364 (ADR-0118), #363, #365, #367, #366, #368 (f65d78e, ADR-0120 «d» eufonica in testing fino al 24/11). Blocco 1 chiuso; prossimo 1-bis standard del volume (ADR-0122).
- **Trovato nel repo:** `#363` → `plans/CHANGELOG.md` · `#364` → `plans/CHANGELOG.md` · `#365` → `plans/CHANGELOG.md` · `ADR-0118` → `plans/adr/ADR-0118-un-numero-entra-solo-se-la-regola-lo-calcola.md` · `ADR-0120` → `plans/adr/ADR-0120-la-d-eufonica-si-misura-con-una-regex-tarata-su-languagetool.md` · `f65d78e` → `plans/adr/ADR-0121-un-plugin-di-regole-si-misura-contro-la-fonte.md`
- **Note di memoria:** `thread-padre-pr` · `blocco1-scelte-8-11`
- **Solo qui:** `#366` · `#367` · `#368` · `ADR-0122` · 2026-11-10 #364 #363 #365 #367 #366 #368 (f65d78e ADR-0120) · #367 · Blocco 1 chiuso; prossimo 1-bis standard del volume ADR-0122

### MS-0065 · 2026-11-10 · Milestone v1.1.0-v1.5.0

- **Data:** 2026-11-10
- **PR:** —
- **ADR:** —
- **Temi:** roadmap milestone
- **Origine:** memoria del progetto, riga 65 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Milestone GitHub v1.1.0…v1.5.0 fissate il 2026-11-10.
- **Note di memoria:** `milestone-roadmap`
- **Solo qui:** Milestone GitHub v1.1.0…v1.5.0 fissate 2026-11-10

### MS-0066 · 2026-11-10 · Regole PF1e del cancello e regole complete

- **Data:** 2026-11-10
- **PR:** #363 #369 #372 #375
- **ADR:** ADR-0119 ADR-0121
- **Temi:** regole motore plugin
- **Origine:** memoria del progetto, riga 66 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Regole PF1e del cancello (ADR-0119, #363): 14 conti in prova, promozione proposta 23/11. Audit plugin regole (ADR-0121): 3.5 605/606, PF1e 217/217; completamento = v1.2.0. Regole complete 3.5/PF1e: lotti 1-5 su main (#369, #372-#375, ultimo 0f70d7c), tre limiti ADR-0121 chiusi.
- **Trovato nel repo:** `#363` → `plans/CHANGELOG.md` · `#372` → `Bestiario/pregen-pcgen/Myconid Sovereign - Monster Stat Block - Kassoon.com_files/js.js` · `ADR-0119` → `plans/adr/ADR-0119-le-regole-pf1e-del-cancello-vengono-dal-prd.md` · `ADR-0121` → `plans/adr/ADR-0121-un-plugin-di-regole-si-misura-contro-la-fonte.md`
- **Solo qui:** `#369` · `#375` · `0f70d7c` · Regole complete lotti 1-5 (#369 #372-#375, 0f70d7c)

### MS-0067 · 2026-11-12 · Verifica schede via MCP, coerenza, regole senza omissioni

- **Data:** 2026-11-12
- **PR:** #378 #379 #380
- **ADR:** ADR-0124 ADR-0125 ADR-0126
- **Temi:** regole motore coerenza
- **Origine:** memoria del progetto, riga 67 di 67 (versione prima della riduzione del 2026-11-12)
- **Testo:** Verifica schede via MCP (ADR-0124, PR #378 unita il 2026-11-12, 43656328): violazioni 34 → 7, le 7 al DM. Coerenza della storia (ADR-0125, PR #379): +4 difetti su 35, parafrasi 1/18. Regole senza omissioni (ADR-0126, 12 lotti): lotto 1 = PR #380.
- **Trovato nel repo:** `#378` → `plans/CHANGELOG.md` · `#379` → `plans/esperimenti/regole-senza-omissioni-2026-11-12/INVENTARIO-E-PIANO.md` · `#380` → `plans/esperimenti/regole-senza-omissioni-2026-11-12/INVENTARIO-E-PIANO.md` · `ADR-0124` → `plans/adr/ADR-0124-le-regole-si-verificano-in-python-e-l-llm-riceve-regola-e-controesempio.md` · `ADR-0125` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md` · `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`

### MS-0068 · 2026-11-12 · La memoria storica nel repo e l'addendum del changelog

- **Data:** 2026-11-12
- **PR:** —
- **ADR:** ADR-0127
- **Temi:** memoria regole ci
- **Origine:** addendum della riga del 2026-11-12 «la memoria storica nel repo (ADR-0127)» in `plans/CHANGELOG.md`
- **Testo:** Richiesta del DM: verificare che la riduzione della memoria del progetto (da circa 25 KB a 8 KB, 2026-11-12) non avesse perso niente, salvare il resto nel repo collegato al changelog, farne un meccanismo che eviti la saturazione e si possa leggere quando serve, e obbligare tutte le sessioni «tipo changelog, tipo addendum». Fatto: MS-0001…MS-0067 con le 67 righe della memoria lunga; `scripts/memoria_storica.py` (lettore e `--check`, nel server MCP); addendum in `check_plans_discipline.py` (riga del changelog senza voce nuova = PR bocciata); regola in AGENTS.md, nel modello delle PR, nella skill rumblingstone-plans e nell'intestazione della memoria del progetto. Misura: riferimenti delle 67 righe nel repo da 127/165 a 165/165; fatti di contenuto non trovati da 24 a 0. Delle 67 righe 53 nascevano da una PR (l'addendum le avrebbe prese), 14 no (regole, ambiente, routine, roadmap, scelte in chat): per queste resta solo la regola. Deciso dal DM (card del 2026-11-12): i dati personali tolti da MS-0005, MS-0006, MS-0009 restano fuori dal repo, nelle note di memoria. Notato durante la verifica: ADR-0104 (personaggi in posa) è citato come «proposta» ma il file non esiste in `plans/adr/`; ADR-0123 è usato sia dal ramo della #371 sia dai commit locali della #370.
- **Trovato nel repo:** `ADR-0127` → `plans/adr/ADR-0127-la-memoria-corta-archivia-nel-repo-prima-di-togliere.md`

### MS-0069 · 2026-11-12 · ADR-0126 lotto 1: cumulo dei bonus, niente tolleranza

- **Data:** 2026-11-12
- **PR:** #380
- **ADR:** ADR-0126 ADR-0124
- **Temi:** regole motore
- **Origine:** voce scritta dopo il merge, per la riga del 2026-11-12 «ADR-0126 … lotto 1» in `plans/CHANGELOG.md` (la PR è entrata prima dell'addendum)
- **Testo:** PR #380 unita il 2026-11-12 (merge b23fd0d0). Programma «regole senza omissioni» in 12 lotti, chiesto dal DM; lotto 1 = cumulo dei bonus per tipo (`bonus.cumulo`, `dmcore.bonus`), tiri salvezza e attacco senza tolleranza in `verifica_scheda` (`--tolleranza` per tornare indietro). Misura: errori messi apposta visti 55% → 79% (701 → 1.007 su 1.279), TS +2 visti 1/362 → 286/362; 22 numeri senza sorgente chiusi (16 in 14 schede con la sorgente scelta dal DM: mantello della resistenza o bonus razziale). Prossimo: lotto 1-bis (CA 3.5, oggetti col prezzo). Il DM ha scelto anche: variante della campagna per elemento intero, motore dichiarabile e vincolabile, forme ibride solo nella variante e registrate.
- **Trovato nel repo:** `#380` → `plans/CHANGELOG.md` (riga senza numero di PR) · `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** lo SHA del merge b23fd0d0 e il numero #380 accanto alla riga del changelog

### MS-0070 · 2026-11-12 · Coerenza della storia contro state.yaml

- **Data:** 2026-11-12
- **PR:** #379
- **ADR:** ADR-0125
- **Temi:** coerenza storia regole
- **Origine:** voce scritta dopo il merge, per le due righe ADR-0125 del 2026-11-12 in `plans/CHANGELOG.md` (la PR è entrata prima dell'addendum)
- **Testo:** PR #379 unita il 2026-11-12 (merge c2cc7756), dopo la #380. Verificatore deterministico della storia con àncora su `state.yaml`; scelta del DM «solo le regole precise, in testing»: `coerenza_campagna.py fatti --state` con S1 arrivo dell'orda, S5 portatore, S6 modifiche permanenti, S7 echi armati senza scena; «chi sa cosa» fra i non verificabili; S2-S4 restano in laboratorio. Misura: +4 incoerenze su 35 del corpus storico, mutanti S1/S5/S6 9/9, parafrasi 0/9 (1/18 nel prototipo), 0 violazioni su main. Il server MCP ora passa le opzioni di un sottocomando. Segue la PR del grafo degli eventi (Prolog/clingo equivalenti a Python; RAG col modello locale 3B: 0 rilievi veri su 23); prova sulla GPU locale ancora da fare. Aperti al DM: i 5 file di ARC-09 tarati per l'11°-12°.
- **Trovato nel repo:** `#379` → `plans/CHANGELOG.md` · `ADR-0125` → `plans/adr/` (file ADR-0125)
- **Solo qui:** lo SHA del merge c2cc7756; il seguito sul grafo degli eventi e l'esito del RAG col modello locale

### MS-0071 · 2026-11-12 · ADR-0126 lotto 1-bis: classe armatura del 3.5

- **Data:** 2026-11-12
- **PR:** #382
- **ADR:** ADR-0126
- **Temi:** regole motore schede
- **Origine:** voce scritta dopo il merge, per la riga del 2026-11-12 «ADR-0126, lotto 1-bis» in `plans/CHANGELOG.md` (la PR è entrata prima dell'addendum)
- **Testo:** PR #382 unita il 2026-11-12 (merge 66ce69b6, base c2cc7756). `dmcore.classe_armatura` ricostruisce la CA del 3.5 dalle voci (armature e scudi dalla tabella, bonus per tipo, contatto, sprovvista); sensi della razza e CD delle capacità dentro `verifica_scheda`; banco `muta_ca.py`; 18 schede corrette per la CA e 10 per la scurovisione (27 file del Bestiario toccati, impronta delle creature rigenerata); `_dv` somma i dadi vita di più classi. Misura: errori di CA messi apposta visti 0/379 → 377/379; scarti veri nel Bestiario 31 → 0. Limiti: 28 schede su 145 senza voci di CA restano non verificabili; scurovisione vista solo per le razze in tabella (10/25); gli oggetti col prezzo, annunciati per il 1-bis, passano al lotto 8.
- **Trovato nel repo:** `ADR-0126` → `plans/adr/ADR-0126-una-scheda-si-verifica-senza-omissioni-e-col-motore-dichiarato.md`
- **Solo qui:** il numero #382 e lo SHA del merge 66ce69b6 accanto alla riga del changelog; lo spostamento degli oggetti col prezzo dal lotto 1-bis al lotto 8 rispetto a quanto annunciato in memoria

### MS-0072 · 2026-11-12 · Grafo degli eventi, Prolog e RAG per «chi sa cosa»

- **Data:** 2026-11-12
- **PR:** #383
- **ADR:** ADR-0125
- **Temi:** coerenza storia regole
- **Origine:** voce scritta con la PR, per la riga del 2026-11-12 «Punti chiave, grafo degli eventi, Prolog e RAG» in `plans/CHANGELOG.md`
- **Testo:** Domanda del DM del 12/11: punti chiave nel tempo, grafo degli eventi, Prolog e RAG, tutto insieme e misurato. Laboratorio `plans/esperimenti/grafo-eventi-2026-11-12/`. Misura: i giorni si ricavano da state.yaml solo per 6 righe su 31 di §4; Python, SWI-Prolog e clingo danno violazioni identiche (29/29 sui mutanti, 6/6 su main), quindi il motore logico non entra; la regola ricorsiva trova 3 catene rotte in §4; il RAG (BM25 + e5-small + Qwen2.5-3B su CPU) recupera 8 parafrasi su 11 ma su main dà 0 rilievi veri su 23, quindi non entra; regole + RAG: parafrasi 0/11 → 5/11 con 42 rilievi in più. Correzione in corsa: la Cerimonia delle 100 Asce è al Day 21, non al 19; numeri invariati. Due correzioni alla #379 dalla revisione automatica arrivata dopo il merge: S1 dichiarata non verificabile se manca `giorno_arrivo`, `STATE` letto alla chiamata; gli altri 8 rilievi restano come limiti dichiarati nella PR. Decisione del DM (card): i giorni di §4 li propone il thread e li conferma lui riga per riga; T1 e T2 entrano in `coerenza_campagna --state` solo dopo. Aperti al DM: le 31 righe di `PROPOSTA-GIORNI-CHI-SA-COSA.md` e D1-D4 (D1: la lettera di Brenna usa «Custodi Eterni» ed è datata al Day 21 e al Giorno 22 nello stesso file); `ARC07-DEF-1-PIANO-TERRA-TERROS.md:69`; la prova del lettore con 7B e 12B via Ollama sulla RTX 4050 (6 GB di VRAM: il 12B non ci sta tutto).
- **Trovato nel repo:** `ADR-0125` → `plans/adr/` (file ADR-0125) · il laboratorio → `plans/esperimenti/grafo-eventi-2026-11-12/ESITO.md`
- **Solo qui:** il criterio per riprovare il lettore (90% di SÌ giusti, 5% col PNG sbagliato, 70% di precisione su main) accanto alla decisione di non adottarlo; l'errore di lettura dello stato della PR (controlli verdi ma PR in conflitto dopo #382 e #381)
