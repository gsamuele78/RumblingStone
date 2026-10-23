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
- `docs/ARCHITETTURA.md` §10: la catena della prosa, tre casi d'uso in sequenza e le dipendenze fra gli script (PR #264).
- Contratto `scripts/schemas/fronti_orologi.schema.json` (fronti alla Dungeon World, orologi alla Blades) e file `plans/coerenza-residui.json`, letto da `coerenza_campagna.py fatti --check` nella CI (PR #264).
- Skill `rumblingstone-narrative-style`: tre cautele di riscrittura in `read-aloud-adulti.md` §2-ter, dal voto cieco del DM; `rumblingstone-module-standard` chiede la coerenza fra scene e, facoltativa, la sintassi (PR #264).

- `scripts/riscontro_srd.py` (canale testing, ADR-0103): riscontra le regole
  dei master sull'SRD 3.5 e sul PRD di Pathfinder 1e (OGL 1.0a), scaricati a
  commit fissato con lo sha256 in `~/.cache/rumblingstone/srd/`, fuori dal
  repo. `regola NOME` cerca una regola; `riscontra FILE.yaml` dice concorda,
  discorda o non trovata, con la citazione. Esce 3 se le fonti mancano e la
  rete non risponde. Job CI `riscontro-srd`, non bloccante.
### Modificato
- `migliora_prosa migliora` tiene l'originale quando anche la migliore candidata ha meno di 0,5 contro di lui: dal voto del 2026-10-23 il modello di preferenza supera la soglia scritta prima di addestrarlo (PR #264).
- `voto_scrittura` resta, perché il banco del modello locale (ADR-0089) lo usa per votare le sue corse: il rilevatore del «sembra» ora vive in `validate_prosa` e il banco lo riusa (PR #264).

### Rimosso
- `campioni_kappa`; da `misura_craft.py` le opzioni `--discriminante` e otto congegni (PR #264).

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
