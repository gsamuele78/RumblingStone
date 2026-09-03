# PIANO — La qualità del codice, misurata prima e dopo

> **Stato**: 🟡 **in corso** — **lotto B chiuso** (2026-09-03), il resto proposto
> **Aperto**: 2026-09-03
> **Nasce da**: domanda del DM — *«per ogni script si dovrebbe guardare: c'è una
> libreria o un tool open source che risolve il problema? posso usare oggetti già
> sviluppati negli altri script? sto ricreando la ruota? ci sono test che
> validano il mio codice? … se si ristruttura, i miglioramenti si devono poter
> misurare, suppongo con un ADR e un piano ben congegnato — se ne vale la pena.»*
> **Risposta breve**: sì, ne vale la pena per **tre cose su cinque**. Le altre due
> sarebbero cerimonia. Questo piano dice quali, con i numeri di partenza.

---

## §1 · La misura di partenza (presa il 2026-09-03, non stimata)

| Cosa | Numero | Come si rimisura |
|---|---:|---|
| Script in `scripts/` | 46 | `ls scripts/*.py \| wc -l` |
| Righe totali | 17.771 | `wc -l scripts/*.py` |
| Moduli condivisi in `dmcore/` | 8 | `ls scripts/dmcore/*.py` |
| Script che usano `dmcore` | **10 su 46** | `grep -l "from dmcore" scripts/*.py \| wc -l` |
| Script senza un test che li nomini | **18 su 46** | vedi §5 |
| Corpi di funzione **identici** in file diversi | **1** | AST, vedi §5 |
| Implementazioni di `slug`/`slugify` | **7** | `grep -c "def slug"` |
| Record del catalogo con id divergente | **9** | vedi §2 |
| Dipendenze esterne dichiarate | **0** | non esiste `requirements.txt` |
| Script con uno **schema d'uso** documentato | 46 (nel manifest) | `tools_manifest.py --check` |

**La lettura onesta di questi numeri.** Un solo corpo di funzione duplicato su
17.771 righe è un risultato **buono**: il repo non è un ammasso di copie. Ma
`dmcore` è usato da **dieci script su quarantasei**, e le sette `slug` mostrano
dove la ruota è stata rifatta davvero.

---

## §2 · Il difetto che questa misura ha trovato

Sette funzioni che fanno la stessa cosa, e **una si comporta diversamente**:

```python
# sei script su sette
s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# build_monster_catalog.py — SENZA la normalizzazione
re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:80]
```

Senza `NFKD`, una lettera accentata non viene traslitterata: **viene buttata via**.

| Nome nel Bestiario | id nel catalogo | id ovunque altrove |
|---|---|---|
| `Lómyn RedTongue, bardo mezzelfo` | `l-myn-redtongue-…` | `lomyn-redtongue-…` |
| `Razorfiend «Blackspawn Alfa» — spawn draconico d'élite` | `…-d-lite` | `…-d-elite` |
| `Ghaurush … «il preventivo è scaduto»` | `…-preventivo-scaduto` | `…-preventivo-e-scaduto` |

**Nove record veri.** Non è teoria: è il catalogo su cui `suggest_encounter`
lavora, e sono id che nessun altro strumento della catena ricalcolerebbe uguali.

---

## §3 · Le domande del DM, una per una

### «C'è una libreria open source che risolve il problema meglio?»

**Quasi sempre sì, e quasi sempre non va usata** — ed è una decisione, non pigrizia.

Il repo è **stdlib-only** per un motivo che vale più delle librerie: gli
strumenti girano sul portatile del DM, prima di una sessione, senza rete e senza
`pip install`. Una dipendenza in più è un modo in più di non poter stampare il
booklet la sera del gioco. Le librerie che *sarebbero* migliori, e perché non ci
sono:

| Dove servirebbe | Libreria | Perché no |
|---|---|---|
| lettura HTML (`import_html_module`) | `beautifulsoup4`, `lxml` | `html.parser` basta; la conversione è stata fatta una volta |
| YAML (`monster_catalog`) | `PyYAML` | il sottoinsieme usato sta in 60 righe e non cambia |
| slug | `python-slugify` | **qui la libreria vincerebbe** — vedi §4, lotto A |
| PDF (`export_booklet_pdf`) | `reportlab` | Typst fa già tutto e non è Python |
| test | `pytest` | la CI usa `unittest`: **una dipendenza in meno nel percorso critico** |

⚠️ **Questa decisione non è scritta da nessuna parte.** È l'omissione vera:
`stdlib_only: true` sta in ogni voce del manifest come *constatazione*, mai come
*regola con un perché*. → **ADR proposto**, §4 lotto 0.

### «Posso usare oggetti già sviluppati negli altri script?»

Sì, e `dmcore` esiste apposta: `statblock` (il contratto del blocco),
`tabelle` (SRD e PF1e), `config`, `gitio`, `regions`, `schede`, `visibility`.
Ma lo usano **10 script su 46**. Le sette `slug` sono la prova che il riflesso
«guardo se c'è già» non è automatico.

### «Sto ricreando la ruota?»

Misurato: **una volta sola in modo grave** (le slug), **una volta in modo lieve**
(`col_label`, quattro istruzioni). Il resto del repo non duplica.

### «Ci sono test che validano il mio codice?»

370 test, e **18 script su 46 non ne hanno nessuno**. Non tutti servono allo
stesso modo: `compress_skills` e `measure_tokens` sono utilità di misura, e un
test lì è cerimonia. Ma `build_monster_catalog`, `validate_bestiario`,
`validate_maps` e `validate_modules` **sono cancelli della CI** e non hanno un
test che dimostri che bocciano davvero un file rotto — cioè: **non sappiamo se
quei gate funzionano**, sappiamo solo che passano.

Questo è il buco più serio del repo, e non è un problema di stile: è che un gate
che non boccia mai è indistinguibile da un gate rotto.

### «TDD e OOP migliorerebbero?»

**TDD: sì, e c'è la prova in questa PR.** Il generatore è stato scritto con il
collaudo come criterio d'accettazione, e il collaudo ha respinto la prima
versione (GS 7 con 38 pf). Poi i test hanno trovato altri tre difetti veri: il
chierico con la caratteristica sbagliata, i punteggi fuori banda, i due druidi
con incantesimi che non possono lanciare. **Nessuno dei quattro sarebbe emerso
rileggendo il codice** — sembravano tutti conti giusti.

**OOP: no, non come programma generale.** Questi script sono *filtri*: leggono
file, scrivono file, escono con un codice. Le funzioni sono la forma giusta, e
incapsularle in classi aggiungerebbe cerimonia senza togliere un difetto. Dove
l'oggetto **serve davvero** ce l'ha già: `Statblocco` è una dataclass,
`Binario` una NamedTuple, `Ruolo` una dataclass congelata. Il criterio è
semplice: **un oggetto dove c'è uno stato con degli invarianti**, una funzione
dove c'è una trasformazione.

### «Uno schema d'uso renderebbe più facile il debug?»

**Esiste già, e nessuno se ne accorge**: `scripts/tools.manifest.json` dichiara
per ogni tool argomenti, ingressi, uscite, codici d'uscita, determinismo, effetti
collaterali. È la fonte di `docs/tools/`, del server MCP e del gate di copertura.
Quello che manca non è lo schema — è il **caso d'uso**: *«questo tool serve a
questa domanda, e la risposta giusta è questa»*. È da lì che nascono i test dei
18 scoperti.

---

## §4 · I lotti, con la misura di accettazione

### ⬜ Lotto 0 — L'ADR che manca: perché stdlib-only
La decisione più importante del repo non è scritta. **Accettazione**: un ADR che
dica il perché (il portatile del DM, la sera della sessione, senza rete), le
eccezioni ammesse (`pdfcpu` e `typst` sono binari, non librerie — ADR-0027) e il
**criterio per rivederla**.

### ⬜ Lotto A — Una `slug` sola, e i nove id che si raddrizzano
`dmcore/testo.py` con **una** implementazione, parametrica su troncamento e
ripiego. Le sette copie la chiamano. **Accettazione**: `grep -c "def slug"` = 1;
i nove record divergenti tornano coerenti; un test con `Città`, `Lómyn`,
`d'élite` e `12–13` (trattino lungo).
⚠️ Rigenera il catalogo → alcuni id cambiano: **va fatto in un commit suo**,
perché i riferimenti esistenti vanno visti.

### ✅ Lotto B — I quattro cancelli che nessuno ha mai visto bocciare
Un test per `validate_bestiario`, `validate_maps`, `validate_modules`,
`build_monster_catalog` che gli dia in pasto un file **deliberatamente rotto** e
verifichi che escano **non-zero**. **Accettazione**: 4 gate su 4 con un test
negativo. È il lotto che vale di più, perché oggi non sappiamo se funzionano.

### ⬜ Lotto C — Il caso d'uso, dove i test nascono
Per i 18 script senza test, una riga di caso d'uso nel manifest (`use_case`:
*«a quale domanda risponde»*) e, dove il tool decide qualcosa, un test che lo
verifichi. **Accettazione**: 46/46 con caso d'uso; i tool che *decidono* (non
quelli che *misurano*) con almeno un test.

### ⬜ Lotto D — L'ambiente riproducibile
Il DM chiede *«quali sono i requisiti software e hardware?»*, e oggi la risposta
è sparsa fra `GUIDA-SETUP-MACCHINA`, `dm.py doctor` e `binari.py`.
**Accettazione**: un file solo che dichiari Python minimo, binari opzionali con
la loro degradazione, e cosa serve *davvero* per ogni catena; `doctor` lo legge
invece di avere la propria lista.

---

## §5 · Come si rimisura (i comandi, non le impressioni)

```bash
grep -l "from dmcore" scripts/*.py | wc -l          # oggi 10 / 46
grep -c "def slug" scripts/*.py | grep -v ':0' | wc -l   # oggi 7
python3 - <<'EOF'                                    # corpi identici: oggi 1
import ast, hashlib, pathlib, collections
c = collections.defaultdict(list)
for f in pathlib.Path("scripts").glob("*.py"):
    for n in ast.walk(ast.parse(f.read_text())):
        if isinstance(n, ast.FunctionDef) and len(n.body) > 2:
            c[hashlib.md5(ast.dump(ast.Module(body=n.body, type_ignores=[])).encode()).hexdigest()].append(f.name)
print(sum(1 for v in c.values() if len(set(v)) > 1))
EOF
```

---

## §6 · Ne vale la pena? La risposta onesta

**Sì per il lotto B, e non è vicino.** Quattro cancelli della CI senza un test
che li veda bocciare sono quattro cose di cui crediamo di fidarci. Costo: mezza
giornata.

**Sì per il lotto A**, perché c'è un difetto vero e misurabile con nove record
già sbagliati. Costo: due ore più il commit di rigenerazione.

**Sì per il lotto 0**, perché una decisione non scritta viene rimessa in
discussione ogni volta che qualcuno chiede *«perché non usiamo una libreria?»* —
com'è appena successo. Costo: un'ora.

**Forse per C e D**, e solo per i tool che *decidono*.

**No a una riscrittura OOP**, e no all'adozione di `pytest` come dipendenza: la
prima aggiungerebbe cerimonia a codice che è già nella forma giusta, la seconda
metterebbe una dipendenza nel percorso critico della CI per comodità di scrittura.
Il vantaggio vero — TDD — non richiede nessuna delle due, e in questa PR è già
stato applicato: **quattro difetti trovati dai test che una rilettura non
avrebbe trovato**.


---

## §7 · Da dove si comincia, in una chat nuova

```bash
# la misura di partenza, rifatta adesso: se i numeri di §1 non tornano,
# qualcuno ha già lavorato e questo piano va riletto prima di eseguirlo
grep -l "from dmcore" scripts/*.py | wc -l        # atteso 10
grep -c "def slug" scripts/*.py | grep -v ':0'    # atteso 7 file
python3 -m pytest scripts/tests/test_gate_bocciano.py -q   # atteso 22 verdi

# la prova che il difetto del lotto A è reale, su dati veri
python3 -c "
import re, unicodedata
c = lambda s: re.sub(r'[^a-z0-9]+','-', s.lower()).strip('-')
a = lambda s: re.sub(r'[^a-z0-9]+','-', unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()).strip('-')
print(c('Lómyn RedTongue'), '≠', a('Lómyn RedTongue'))"
```

**L'ordine consigliato**: **0** (l'ADR, un'ora, sblocca la discussione sulle
librerie) → **A** (la `slug`, due ore più un commit di rigenerazione a parte) →
**C** e **D** se il DM li vuole.

⚠️ **Il lotto A cambia degli id nel catalogo.** Va in un commit suo, e i
riferimenti esistenti vanno guardati prima di rigenerare: `grep -rn "l-myn\|d-lite"`.

**Il metodo che ha funzionato nel lotto B, e che vale per gli altri**: scritto il
test, **mutare il codice che dovrebbe coprire** e verificare che il test cada.
Nel lotto B ha trovato un difetto nel test stesso, che rileggendolo non si vedeva.
