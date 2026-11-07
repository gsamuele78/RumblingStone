# Changelog di RumblingStone

Qui stanno i rilasci del progetto: cosa è cambiato per chi usa i suoi
strumenti, le skill e i contratti dei file. Il diario dei piani resta in
[plans/CHANGELOG.md](plans/CHANGELOG.md).

Il formato è [Keep a Changelog](https://keepachangelog.com/it-IT/1.1.0/). I
numeri seguono il [versionamento semantico](https://semver.org/lang/it/), con
la superficie pubblica descritta in
[docs/RILASCIO.md](docs/RILASCIO.md): la CLI `dm.py`, i contratti dei file
(JSON delle mappe, `campaign/group.yaml`, le regioni `auto` di `state.md`), i
nomi e il formato dei pacchetti delle skill, la versione di Python.

Rilasciare è unire una PR che sposta «Non rilasciato» sotto un titolo
`## [X.Y.Z] - AAAA-MM-GG` e alza `__version__` in `scripts/dmcore/__init__.py`.
Il tag e il rilascio li crea il workflow Release (ADR-0100).

## [Non rilasciato]

### Aggiunto
- I sistemi di gioco come plugin di dati (ADR-0111, proposta): `sistemi.toml` in radice dice quali sistemi sono attivi, quali di rinforzo e quale usa ogni cartella; i plugin stanno in `sistemi/<id>/sistema.toml` con le capacità dichiarate; `scripts/sistemi.py` stampa i sistemi supportati e la matrice strumenti × sistemi, `--di FILE` il sistema di un file, `--check` è il cancello (in CI). Le voci di `scripts/tools.manifest.json` possono dichiarare `sistema.capacita`. Nessuno strumento esistente cambia comportamento.
- Pathfinder 1e supportato in cinque capacità prima dichiarate «non supportato» (ADR-0111): `--sistema pf1e` in `update_xp.py` (tre tracce PE, `--traccia`), `suggest_encounter.py` (GS dell'incontro dalla somma dei PE), `suggest_loot.py` (valore per incontro per APL, `--velocita`), `genera_creatura.py` (dado, BAB, TS, BMC/DMC e gradi PF1e); `coerenza_campagna.py` riconosce le classi PF1e nei moduli PF1e. I numeri stanno in `sistemi/pf1e/dati/`, estratti dal PRD con la fonte; le scelte di campagna in `[opzioni.pf1e]` di `sistemi.toml`. Senza `--sistema` l'uscita 3.5 non cambia.
- Un solo rilevamento del sistema di gioco (ADR-0111, L2): il catalogo dei mostri, il censimento del Bestiario e le domande del developer prendono il sistema di un modulo da `sistemi.toml`. Il Giardino PF1e esce dal catalogo dei mostri 3.5 (387 → 386 voci). `sistemi.py --check` boccia un modulo la cui riga «**Sistema:**» dice un sistema diverso da `sistemi.toml`; i plugin dichiarano con `riconosci` come si scrive il loro nome. Un profilo di `plans/domande-developer.json` non può più dichiarare «sistema». `lessico_regole.e_pf1()` segue `sistemi.toml`: tutti i 22 file del Drappo sono controllati con le tabelle PF1e, prima 3.
- Termini e lessico dai plugin (ADR-0111, L3): la lista dei termini 5e vietati è una sola, `sistemi/d20/dati/termini-vietati.toml`, letta da `validate_modules.py` e `validate_standalone.py` (prima due copie diverse: ora tutti e due bocciano «azione bonus», «bonus action», «lair action», «con vantaggio»). Le abilità vengono da `lessico.abilita` del sistema del file: `validate_prosa.py --caratteristiche` controlla le abilità PF1e nei moduli PF1e. Classi e razze 3.5 di `coerenza_campagna.py` in `sistemi/dnd35/dati/entita.toml`. `validate_standalone.py` non importa più `RIPOSO_5E` da `validate_modules.py`.
- `scripts/controlla_marche.py` (ADR-0109): sulle righe cambiate di una PR avvisa per una marca INFERRED senza domanda e base e per un INFERRED tolto senza CANONE, GENERATO o storico. In CI non blocca (canale testing).
- Termini ufficiali (ADR-0110): `scripts/lessico_regole.py` con le tabelle `lessico_it_35.tsv` (italiano → SRD 3.5) e `lessico_it_pf1.tsv` (italiano PF1e → PRD), ogni riga con la fonte; `controlla` sui talenti (cricchetto in CI) e `controlla --campi` su incantesimi, abilità e oggetti magici delle schede (conto nel riepilogo della CI, non blocca).
- Marcature dei fatti (ADR-0109): grammatica unica in `docs/guides/GUIDA-MARCATURE.md` (`[INFERRED — domanda; base: …]`, `[CANONE — DM data, codice]`, `[GENERATO]`, fonti). Dieci skill di contenuto hanno la sezione «Vincoli sui fatti», uguale alla guida (`test_vincoli_delle_skill.py`); AGENTS.md e le skill non riscrivono più la regola.
- Skill `dnd-35-srd`: `references/resources.md` dice dove trovare il testo
  degli incantesimi fuori rete, nelle esportazioni PCGen di
  `Bestiario/pregen-pcgen/`, e cosa portano (un riassunto, non il testo SRD).
- `scripts/misura_fedelta_nli.py`: il riscritto contraddice l'originale? Coppie di righe del diff giudicate da un modello NLI multilingue (solo in locale, `transformers`). Con `--ripara`, e da sé dentro `ciclo_prosa revisione` e `misura`, le righe che contraddicono tornano all'originale. Sulle 26 coppie del DM F1 0,83 contro 0,62 dei soli numeri (RICERCA-GUARDRAIL §9).
- `misura_box_telecomando.py --check` (cancello in CI) e `misura_ripetizioni_frasi.py --check` (cancello locale, `plans/scrittura/ripetizioni-accettate.json`).
- `scripts/misura_ripetizioni_frasi.py`: le immagini ripetute fra i box, frase per frase, con embedding (solo in locale, `sentence-transformers`). `scripts/misura_box_telecomando.py`: i box che dicono al gruppo cosa capisce o sa. Indicatori, nati dalle prove scartate rifatte con una configurazione rigorosa (RICERCA-GUARDRAIL §8).
- `conformita_statblocchi.py --master` legge anche gli statblocchi recintati di ADR-0091 nei master: pf, CA, riga Difesa contro recinto, CD di soffio, schiacciare e presenza, *corrompere l'acqua*, voci ereditate con «come A.n», scurovisione dei tipi SRD (ADR-0108). Cricchetto in `test_conformita_statblocchi`.
- `scripts/misura_distanza_pagine.py`: le pagine fra dove una persona agisce e la pagina con la sua CA e i suoi pf, lette dal PDF stampato con PyMuPDF (ADR-0108).
- `misura_standard_tavolo.py` conta le note di lavoro che vanno in stampa («[INFERRED…]», «va riscontrato», TODO), con cricchetto per volume.
- Ogni `skills/*/SKILL.md` ha la sezione «Cancelli deterministici»; `test_cancelli_delle_skill.py` la impone (ADR-0108).
- `scripts/dmcore/chi_si_incontra.py` e la chiave `"chi_si_incontra": true` del manifest (ADR-0107): prima di stampare porta nel capitolo il riquadro accanto alla scheda d'entrata, le persone nominate in «In scena … Chi:» e le mappe stampate lontano; `misura_standard_tavolo.py --prova` misura il risultato.
- `scripts/misura_standard_tavolo.py` (ADR-0107): per ogni booklet del
  DM e ogni capitolo, le persone con un nome che ci compaiono e se nello stesso
  capitolo ci sono numeri, aspetto, ritratto, chi è, cosa vuole e tattica; per
  ogni capitolo con uno scontro, se c'è la mappa. Indicatore, non cancello.
- Il riquadro unico delle creature in stampa (ADR-0105): `#statblocco` nel
  tema Typst ha le fasce Difesa, Attacco, Statistiche, Capacità speciali e
  Tattiche, riempite dalle righe di ADR-0091 o dai campi del blocco; la stessa
  forma esce nell'HTML dei booklet e in Homebrewery (`{{monster,frame}}`). Il
  campo `gs` accetta un testo («PG di 13°») o «—».
- Le schede intere delle creature in appendice (ADR-0105 punto 7): nel punto
  dell'incontro una riga con nome, GS, CA, pf, la pagina della scheda e la
  tattica di quell'incontro; in fondo al volume `appendice-creature` con un
  riquadro per creatura, mai spezzato a pagina girata, con «continua» e
  «(segue)» quando è più alto di una colonna. Lo stesso in HTML e Homebrewery.
  Chiave di manifest `"schede": "qui"` per tenere i riquadri dove sono.
- `scripts/varianti_stampa.py`: compila un booklet in più varianti del tema
  (interlinea, box da leggere senza riquadro), le misura, scarta quelle che
  peggiorano una misura con tetto e prepara il fascicolo per la scelta alla
  cieca, con la chiave a parte.
- `componenti.py`: l'ancora `#scheda` include il blocco ```statblocco con la
  sua parte leggibile e il nome dal titolo della scheda.
- `scripts/misura_statblocchi_booklet.py`: conta per booklet le schede di
  creatura e la forma in cui escono (`--stampa` conta i riquadri nel sorgente
  Typst); `--check` in CI contro i tetti di `docs/audit/statblocchi-booklet.json`.
- `scripts/misura_stampa.py`: compila ogni booklet e ne misura il PDF come un
  controllo di prestampa (font non incorporati, testo sotto 7 pt, testo oltre
  la gabbia, immagini sotto 300 dpi, riquadri di creatura spezzati fra due
  pagine). Un job della CI controlla i tetti di `docs/audit/stampa-booklet.json`.
  Il riquadro `#statblocco` del tema lascia due segnaposti invisibili
  (`<sb-inizio>`, `<sb-fine>`) per questa misura.
- `scripts/inventory_inferred.py`, canale testing (ADR-0088, ADR-0099): conta i
  marcatori INFERRED aperti separandoli da quelli dei piani e dei changelog; in CI
  `--check` non bloccante contro `docs/audit/inferred-baseline.json` (260).
  Ripreso dalla PR #99, chiusa il 2026-10-24.
- La regola del cambio d'autore delle echi nella skill di stile
  (`consequence-echoes.md` §1-bis), ripresa dalla PR #99.
- `dm.py maps pianta`: il tema «pianta» delle mappe tattiche, nello stile delle
  piante delle città, in `rendered-pianta/` (ADR-0102). ARC-07 l'ha adottato.
- `dm.py maps citta [rethmar|dauth|channathgate] [--check]` e
  `scripts/genera_pianta_citta.py`: le piante delle città si rifanno dai loro
  programmi in `scripts/piante/`. Con una scheda `*.watabou.json` il comando
  resta quello di prima.
- shapely 2.2.0 in `requirements-dev.txt`, canale testing.
- Le schede dei PG come dato: `PG/schede/<pg>.yaml` (schema
  `scripts/schemas/pg_scheda.schema.json`) con le caratteristiche e i
  modificatori permanenti, ognuno con la sua fonte, e la vista `<pg>.md`
  generata. `validate_pg.py` e `render_pg.py --check` sono cancelli della CI.
  Classe, PF e stato restano in `campaign/state.yaml` (ADR-0088).
- `dm.py gruppo nuovo` rifà `PG/schede/` vuote per i PG del nuovo gruppo.
- `dm.py prosa <azione>`: la catena della prosa da un solo ingresso, nell'ordine d'uso (misura, ciclo, mqm, sintassi, coerenza, domande, migliora, cieco, banco, voto), ADR-0101 (PR #264).
- `binari.py` conosce spaCy (facoltativa) e le catene «prosa misurata», «coerenza fra scene e archi», «sintassi della prosa» e «secondo lettore LanguageTool»; `requirements-completo.txt` installa spaCy col modello italiano (PR #264).
- Documentazione allineata ad ADR-0102, ADR-0105…ADR-0108: `docs/ARCHITETTURA.md` §11 (pianta di stampa, schemi, generatori delle città), §12 (chiavi `schede` e `chi_si_incontra`, misure di stampa), §13 (cancelli delle skill), §16, §18 (ramo «stampa» del flusso della qualità e i cancelli della prosa della #308 e della #309, §10.1) e §19; README; GUIDA-BOOKLET-E-PDF §1.3, §3 e §9.
- `docs/ARCHITETTURA.md` §10: la catena della prosa, tre casi d'uso in sequenza e le dipendenze fra gli script (PR #264).
- Contratto `scripts/schemas/fronti_orologi.schema.json` (fronti alla Dungeon World, orologi alla Blades) e file `plans/coerenza-residui.json`, letto da `coerenza_campagna.py fatti --check` nella CI (PR #264).
- Skill `rumblingstone-narrative-style`: tre cautele di riscrittura in `read-aloud-adulti.md` §2-ter, dal voto cieco del DM; `rumblingstone-module-standard` chiede la coerenza fra scene e, facoltativa, la sintassi (PR #264).

- `scripts/riscontro_srd.py` (canale testing, ADR-0103): riscontra le regole
  dei master sull'SRD 3.5 e sul PRD di Pathfinder 1e (OGL 1.0a), scaricati a
  commit fissato con lo sha256 in `~/.cache/rumblingstone/srd/`, fuori dal
  repo. `regola NOME` cerca una regola; `riscontra FILE.yaml` dice concorda,
  discorda o non trovata, con la citazione. Esce 3 se le fonti mancano e la
  rete non risponde. Job CI `riscontro-srd`, non bloccante.
- Booklet ARC-07 *Notte e Alba*: nuovo capitolo VII «Il barile sulla tenda di Zog'tar» (quote, calcoli ed esiti del bombardamento, PR #292 e #296); la mappa M7-H del campo del capo entra nell'Appendice D di DEF-4, quindi anche nei volumi Resurrezione e Mille anni. Le tre tabelle più lunghe del capitolo stanno su pagina a una colonna. M7-H e M7-C entrano nello stile pianta (quello di Dauth) in modo stampa, ognuna su due pagine (mappa, poi luoghi e legenda): i tetti di stampa dei tre volumi non salgono.
- `render_map_svg.py --stampa` (in `rendered-stampa-<tema>/`, GUIDA-MAPPE §5.5), per ogni tema: per una mappa grande nel booklet A4, scritte in punti mai sotto i 7,4 pt, luoghi e legenda in un secondo SVG, nessun filtro rasterizzato. `validate_maps` controlla questi SVG contro il master.
- La pianta in stampa è lo standard di ogni mappa (ADR-0106): accanto a ogni `rendered/` c'è `rendered-stampa-pianta/` (`render_map_svg.py --tutti-i-master --tema pianta --stampa`), `validate_maps` segnala quelle mancanti e `validate_booklets` ferma una mappa a pergamena o senza legenda in un booklet. M7-B, PF-2 e M7-D/E/F passano alla pianta nei volumi di ARC-07: righe sotto 7 pt a 0. Il tema pianta disegna le mappe alte e le foreste, scrive in stampa le voci di legenda intere, usa la legenda del master per i simboli locali e produce lo stesso SVG in ogni processo.
- `validate_booklets` controlla anche che il `.hb.md` committato di un booklet sia quello che il manifest produce oggi (`build_booklet_html.testo_hb`): i `.hb.md` di Notte e Alba, Resurrezione e Mille anni erano rimasti alla versione prima del capitolo del barile e delle mappe nuove.
- Nei booklet di ARC-07 le griglie ASCII delle mappe tattiche (T-2, T-3, T-6, S-2, M7-B, e CM-1 e CM-2 in DEF-5) lasciano il posto alla pianta in stampa con la legenda; la griglia resta nel master come apparato. `validate_booklets` ferma una griglia disegnabile stampata in un booklet. Le sei schematiche passano anche loro: T-5, R-1 e S-1 ridisegnate in scala in `ARC07-MAPPE-SCHEMATICHE-IN-SCALA.md` (S-1 sulla pianta di PF-2 con gli affreschi di DEF-2), T-1, T-4 e M7-A come schemi senza griglia generati da `scripts/render_schemi.py` (`--check` in CI). In CM-1 e CM-2 (e nella MAPPA 5 di ARC-08) i 90 nani non stanno più ad anello ma schierati verso la porta, centro pesante e due ali piegate (scelta del DM, 2026-10-30); i numeri dello scontro non cambiano. Lo standard vale per tutto il repo: `validate_booklets` ferma ogni disegno a riquadri stampato in un booklet, e le due linee del tempo che restavano (Palio, Drappo) sono diventate tabelle.
### Modificato
- ADR-0107 **accettata** (2026-11-03): `"schede": "entrambe"` e `"chi_si_incontra": true` sono lo standard nei 6 booklet dove migliorano (Notte e Alba, Serata Resurrezione, Mille Anni, Ritorno alla Forgia, Drappo, Abbazia rotta). Numeri nel capitolo 8 → 25, mappe vicine allo scontro 5 → 9 su 42, distanza scena-numeri di Zog'tar 23,5 → 4,5 pagine. Terros resta fuori: si allunga.
- Il tema Typst piazza in alto la tabella «Chi si incontra in questo capitolo» e misura il riquadro dove cade davvero, così una scheda non si spezza fra due colonne e il titolo non resta solo in fondo.
- ADR-0108 **accettata**: i cancelli deterministici sono lo standard di ogni skill.
- `converters/pdf-to-md-engine`: minimi di `transformers` (5.22.1) e `spacy` (3.8.18)
  alzati da Dependabot (gruppo convertitori-settimanale, PR #304), allineati a EarlRagnar78.
- `scripts/booklet-container`: immagine base `debian:13-slim` aggiornata al digest
  nuovo da Dependabot (gruppo docker-settimanale, PR #303).
- `converters/pdf-to-md-engine`: minimo di `nltk` alzato a 3.10.4 da Dependabot
  (gruppo convertitori-settimanale, PR #294).
- `scripts/booklet-container`: immagine base `debian:13-slim` aggiornata al digest
  nuovo da Dependabot (gruppo docker-settimanale, PR #293).
- `converters/`: minimi delle dipendenze alzati da Dependabot (gruppo
  convertitori-settimanale, PR #274), fra cui transformers 5.20.2, Pillow 13.0.0,
  lxml 6.1.3, language-tool-python 3.4.0, spacy 3.8.16, scikit-learn 1.9.1.
- La norma `italiano-nativo` §1 e §8 vieta il possessivo solo sulle parti del corpo e sulle cose addosso; gli altri sono liberi (decisione del DM, 2026-10-23).
- `coerenza_campagna fronti`: un orologio che dichiara `unita` (giorni, ore) tiene la sua durata invece di 4, 6 o 8 tacche. La CI controlla i file `ARCnn-FRONTI.yaml` degli archi, canone da ARC-08 in poi.
- `migliora_prosa migliora` tiene l'originale quando anche la migliore candidata ha meno di 0,5 contro di lui: dal voto del 2026-10-23 il modello di preferenza supera la soglia scritta prima di addestrarlo (PR #264).
- `voto_scrittura` resta, perché il banco del modello locale (ADR-0089) lo usa per votare le sue corse: il rilevatore del «sembra» ora vive in `validate_prosa` e il banco lo riusa (PR #264).

### Corretto
- Master ARC-07: Treant di Adamantio 95 pf (10d8+50, prima 90), scurovisione 18 m a Durin e alle wyvern. `conformita_statblocchi --master` accetta il primo dado al massimo per i PNG con livelli di classe (Balvar 101 pf). Cricchetto dei conti a 0.
- Appendice delle creature in stampa: i nomi nei titoli dei riquadri non vanno più a capo col trattino («Skullcru-sher»); una scheda che non entra nella colonna di sinistra continua nella colonna accanto della stessa pagina invece di lasciarne bianca la metà; il «continua» in fondo all'ultimo pezzo di una scheda lunga non compare più («continua a pagina 60» sotto Terros, che finiva a p. 59). `misura_stampa` conta ora i rimandi di pagina sbagliati (tetto 0) e fallisce se l'impaginazione non converge.
- `export_map_png.py`: con Chromium la legenda delle mappe più alte usciva tagliata, perché il headless nuovo toglie alla finestra la fascia della cornice. Ora la finestra si apre più alta e il PNG torna all'altezza dell'SVG, con la sola libreria standard.

### Rimosso
- `campioni_kappa`; da `misura_craft.py` le opzioni `--discriminante` e otto congegni (PR #264).

### Cambiato
- `inventory_inferred.py` conta come meta skill, modelli, README, fixture e lo schema da copiare, e dà la forma di ogni marca: il debito aperto passa da 25 a 0. Le forme vecchie fuori da `plans/` sono migrate (`[ACCEPTED — DM-canon …]` → `[CANONE — DM …]`, 138 righe); `validate_bestiario.py` accetta `[CANONE` nel titolo.

## [1.0.0] - 2026-10-23

Il primo rilascio con un numero. Raccoglie il lavoro fatto dal 2026-09-30 a
oggi e fissa la piattaforma da cui partono i rilasci successivi.

### Cosa promette la 1.0.0, e cosa no
Stabile vuol dire che da qui in avanti un cambiamento incompatibile della
superficie pubblica alza il primo numero. Su cosa si regge la promessa, al
2026-10-23:
- gli ultimi 30 run della CI su `main` sono verdi (dal 2026-10-15), con
  oltre 2.000 prove automatiche e i cancelli bloccanti di `ci.yml`;
- la CLI `dm.py` e i contratti dei file hanno uno schema e sono stati usati a
  serate vere del primo tavolo;
- l'archivio delle skill si costruisce in modo riproducibile: tre costruzioni
  dello stesso commit danno gli stessi byte.

Cosa la 1.0.0 **non** promette:
- gli strumenti nel canale testing (ruff, uv, pytest-xdist, il job dei
  convertitori) possono cambiare o sparire senza un numero nuovo: non fanno
  parte della superficie pubblica;
- il workflow Release stesso è in testing fino al suo primo giro completo,
  che è questo rilascio;
- il contenuto di gioco (archi, Bestiario, prosa) cambia a ogni giro di
  letture e non è coperto dal versionamento: la versione dice com'erano gli
  strumenti e le skill, non quale canone è definitivo;
- alcune decisioni sono ancora «proposta» (per esempio ADR-0095, il giro delle letture) e
  il lotto P6 della piattaforma (un solo controllo della Python) non è fatto.

### Piattaforma
- **Una Python sola, 3.13**, quella di Debian 13, ovunque: CI, Dockerfile,
  `binari.py`, `converters/`. Si sale con Debian 14 (ADR-0099).
- **Tre canali come Debian** per ogni componente di terzi: unstable, testing
  (CI non bloccante), stable (bloccante). Si sale solo con una misura prima e
  dopo e con l'ok del DM (ADR-0099).
- In testing: ruff con le sole regole che cercano bug, uv per installare,
  pytest-xdist per i test in parallelo, il job dei convertitori.
- La suite di test gira una volta sola nel job principale: da 914 a 458
  secondi. La parità fra unittest e pytest resta controllata da un test.
- **Il rilascio è una PR** (ADR-0100): questo file, il workflow Release, tag e
  note automatici, i pacchetti delle skill con le impronte SHA-256.
- `dm.py --version` dice la versione.

### Corretto
- Tre bug in `converters/`: un `NameError` all'import di
  `fallback_manager`, uno a fine installazione, uno nascosto da un `except`.
  `pdfplumber` mancava da `requirements.txt`.
- 13 `Path` usati senza import in `scripts/dmcore/testo.py`.
- 120 `DeprecationWarning` di Python 3.13 nella suite, da un `re.split` con
  `maxsplit` posizionale.
- L'indice dei pacchetti delle skill (`index.json`) cambiava a ogni
  costruzione: l'ora di oggi e i domini in ordine casuale. Con
  `SOURCE_DATE_EPOCH` e i domini ordinati, due costruzioni dello stesso
  commit danno gli stessi byte.

### Contenuto del progetto a questa versione
- Archi 00-09 della campagna (Red Hand of Doom nella Valle di Cannath), i
  master ARC-07 al ciclo del master, il modulo autonomo del Drappo di Tarsilia
  e quello dell'Abbazia.
- 18 skill, impacchettate per agente da `build-skills.sh`.
- 97 ADR, i piani in `plans/` con il loro indice, oltre 2.000 prove automatiche.
