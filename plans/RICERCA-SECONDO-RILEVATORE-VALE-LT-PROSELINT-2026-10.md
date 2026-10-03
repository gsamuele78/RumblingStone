# Ricerca: un secondo rilevatore per la prosa (Vale, LanguageTool, proselint)

> **Metodo.** Il DM ha chiesto perché ADR-0077 e ADR-0078 avessero scartato
> Vale, LanguageTool e proselint, se la licenza non è il problema, e di
> rivalutarli con una misura. Qui sono installati davvero, fatti girare sul
> contenuto di gioco (521 file, archivi e snapshot esclusi con
> `validate_prosa.file_di_gioco()`) e sui documenti (414 file), letti a mano su
> campioni, confrontati con ciò che il repo già segnala. Nessun file di
> contenuto è stato toccato.
>
> **Stato**: misura chiusa, decisione **proposta** in
> [ADR-0079](adr/ADR-0079-un-secondo-rilevatore-per-la-prosa.md), in attesa del DM.

## 0. Cosa mancava, e cosa si è assunto

Mancava un'etichetta di riferimento (gold) per la lingua italiana del repo: non
esiste. La precisione è quindi **il giudizio di un lettore solo**, che ha letto
ogni rilievo con la riga attorno. Non c'è un secondo lettore e non c'è un κ. Un
rilievo conta come vero quando un correttore di bozze lo cambierebbe nel testo
nostro; un errore in un testo inglese copiato da altri non conta.

Assunzioni: la CI di GitHub ha rete (qui la rete è un proxy con una lista di
host); il Java del sandbox (17) è quello della CI; i tempi del sandbox (4 core)
sono quelli di un runner.

## 1. Perché erano stati scartati, motivo per motivo

ADR-0077 scartò Vale e proselint in una riga («le regole sono in inglese») e
mise LanguageTool come servizio facoltativo fuori dalla CI, perché
`api.languagetool.org` era bloccato. **Nessuna delle tre cose era misurata.** Era
un giudizio di costo e beneficio, scritto prima di installare. Adesso i motivi,
uno per uno:

| Motivo del passato | Regge? | Prova |
|---|---|---|
| Licenza | Non era un motivo | LanguageTool LGPL-2.1 (servizio, nessun file nel repo), Vale MIT, proselint BSD. Compatibili con la politica del repo (§6) |
| Le regole sono in inglese | **Regge per proselint, non per Vale** | proselint applicato a righe italiane: 754 rilievi non tipografici su 909, **tutti** una lista di parole inglesi letta su testo italiano (§4). Vale ha il motore agnostico: le regole sono le nostre |
| Binario Go in CI | Non regge | `go install github.com/vale-cli/vale/v3/cmd/vale@latest` compila in pochi minuti, 65 MB. Il percorso `errata-ai/vale` è stato rinominato: la riga vecchia non funziona più. Le release su GitHub danno 403 dal proxy di questo sandbox, non da una runner |
| JVM e rete per LanguageTool | **Non regge** | Il server si ricostruisce da Maven Central (raggiungibile): `languagetool-server` + `language-it` 6.8, 172 jar, 252 MB, gira in locale su `127.0.0.1:8081` senza rete dopo il download |
| Solo stdlib | Regge come preferenza, non come divieto | ADR-0077 stesso ammette LanguageTool «come servizio» |
| Duplicazione con i rilevatori del repo | **Regge, ed è il motivo vero** | §3 e §5 |
| Rumore | **Regge, ed è enorme** | §3: 94.755 rilievi, il 99,4% da scartare |
| Tempo in CI | Non regge | LanguageTool 171-189 s su 521 file; Vale 3 s; proselint 14 s |

## 2. Soglie fissate prima di misurare

Scritte in un file prima di far girare niente, e qui riportate:

| Soglia | Valore |
|---|---|
| S1 precisione | almeno 70% su un campione di validazione di almeno 100 rilievi estratti a caso (seme 3510), **dopo** aver scelto le regole da spegnere su un campione di calibrazione separato (seme 11) |
| S2 contributo nuovo | fra i rilievi veri, almeno il 30% non già segnalato da `validate_prosa`, `validate_lingua` o `misura_craft` sulla stessa riga, e almeno 50 veri nuovi nel repo |
| S3 costo | intero contenuto di gioco in 10 minuti al massimo; installazione riproducibile da fonti raggiungibili, senza disattivare TLS |
| S4 determinismo | due esecuzioni sullo stesso input, stesso output |

Tutte e quattro devono valere. **S5 è stata aggiunta dopo aver visto i dati**,
e va letta come tale: *il contributo marginale rispetto alla miglior alternativa
interna* (una regex nel rilevatore che già c'è) deve essere di almeno 10 veri
nuovi. La aggiungo perché S2, scritta come sopra, si supera per una ragione che
la regola sesta del repo (G6) vieta di accettare: un rilevatore interno non ce
l'ha *oggi*, ma costerebbe dieci righe.

## 3. LanguageTool 6.8, italiano

Server locale, testo piano ricavato dal markdown con **una riga per riga
sorgente** (tabelle, codice e front matter svuotati, link e grassetti tolti)
perché i numeri di riga restino veri.

**Configurazione predefinita: inutilizzabile.**

| | Rilievi |
|---|---:|
| Totale su 521 file | 94.755 |
| `MORFOLOGIK_RULE_IT_IT` (ortografia) | 91.862 (97%) |
| di cui su righe inglesi (statblock, testi copiati) | 46.536 |
| di cui su nomi del registro `misura_craft._registro_dei_nomi()` | 13.249 |
| di cui su parole minuscole italiane (il resto, dopo i filtri) | 9.721 |
| `WHITESPACE_RULE` e `UPPERCASE_SENTENCE_START` | 2.338 (artefatti delle tabelle e dei frammenti) |
| regole grammaticali e di stile, tutte | 555 |

L'ortografia minuscola è il caso che sembrava promettente: i filtri tolgono
inglese e nomi, e restano 9.721 rilievi su 2.337 parole distinte. In un
campione di 15 non c'è un vero: *statblocco*, *spawn*, *humanoid*, *nanica*,
*companion*. È gergo di gioco, e il dizionario non lo conosce. Un dizionario
personale con i 322 nomi non lo risolve, perché il gergo è migliaia di parole.

**Calibrazione** (98 rilievi, seme 11, 5 per regola): tenute tre regole
(`GR_04_002`, `ARTICOLATA_SOSTANTIVO`, `COMMA_PARENTHESIS_WHITESPACE`), spente
le altre. Il motivo, regola per regola: `ER_01_00x` propone *ha
sorpresa* per *a sorpresa*; `ST_03_001` segnala la *d* eufonica in *e
equipaggiamento* ma il messaggio stesso dice «è ammesso»; `ST_01_005` propone
*bilancio* per *budget*; `GR_10_003` chiede il congiuntivo dove c'è già
(*prima che… fosse*); `UNPAIRED_BRACKETS` conta male le parentesi che
attraversano una cella. `ITALIAN_WORD_REPEAT_RULE` ha scattato solo su `X X`,
la maschera con cui il mio preparatore sostituisce il codice in linea: un
artefatto mio.

**Validazione** (100 rilievi della configurazione ridotta, seme 3510, letti a
mano, elenco completo in appendice):

| Regola | Letti | Veri | Falsi | Cosa sono |
|---|---:|---:|---:|---|
| `GR_04_002` (apostrofo al posto dell'accento) | 76 | 72 | 4 | *e'* per *è*, *gia'*, *piu'*. I 4 falsi: *Da'* (imperativo di *dare*, corretto) e un apostrofo di chiusura di citazione |
| `COMMA_PARENTHESIS_WHITESPACE` | 14 | 11 | 3 | *Environment: urban,plane* nelle schede; `Etichetta regia: .` con il campo vuoto. I falsi sono in un testo inglese copiato |
| `ARTICOLATA_SOSTANTIVO` | 10 | 3 | 7 | Veri: *del Mano Rossa* (la Mano è femminile), *dalla Conoscenze*. Falsi: *session log*, *del label* (prestiti), *alle Civetta* (una contrada) |
| **Totale** | **100** | **86** | **14** | |

**S1: precisione 86%. Passa.** Ma i veri non sono 86 cose diverse:

- 72 dei 100 sono lo stesso errore, *e'* per *è*, e dentro il blocco
  «non e' raggiungibile da nessuno strumento» copiato in decine di schede del
  Bestiario. I contesti distinti fra i veri sono **45**, non 86.
- Nel repo intero la configurazione ridotta dà 189 rilievi su 102 file e 117
  frasi distinte.

**S2: contributo nuovo.** Dei 86 veri, **6** cadono su una riga che i rilevatori
del repo già segnalano: 93% nuovi, e oltre 50 in assoluto. **Passa, alla
lettera.** Il motivo è che `validate_lingua` conosce `perchè` e `E'` a inizio
frase e non conosce `e'` in mezzo alla frase.

**Il controllo che la regola sesta impone (S5).** Una regex sola, con le parole
accentabili che il repo usa (*e, gia, piu, puo, cosi, perche, pero, citta,
poiche, cioe, verra, sara…* seguite da apostrofo):

| | Righe |
|---|---:|
| la regex | 179 |
| `GR_04_002` di LanguageTool | 128 |
| in comune | 121 |
| solo regex (per esempio *mai piu'*, *cio'*, *perche'*) | 58 |
| solo LanguageTool | 7, tutti falsi (*Da'*, citazioni) |

La regex **trova tutto ciò che LanguageTool trova di vero e 58 righe in più**.
Il contributo marginale di LanguageTool su questa regola è zero. Resta
`ARTICOLATA_SOSTANTIVO`: 3 veri su 10, cioè *del Mano Rossa* (due righe in un
file) e *dalla Conoscenze*. **S5 non passa** (3 contro 10).

**Capacità grammaticale, a parte.** Venti frasi scritte da me con un errore
noto ciascuno (concordanza, congiuntivo, periodo ipotetico, articolo, ausiliare,
apostrofo, *qual'è*, parola ripetuta): LanguageTool italiano ne rileva 5 su 15
di quelle con errore vero, e sono le cinque di ortografia o ripetizione. Zero su
concordanza verbo-soggetto, aggettivo, congiuntivo, periodo ipotetico, articolo,
ausiliare. Su «Le case è rosse» tace. Le regole grammaticali italiane di
LanguageTool sono poche: nei 94.755 rilievi del repo scattano una ventina di regole in
tutto. È un limite del progetto, non della nostra configurazione.

**Sui documenti** (`plans/`, `docs/`, `skills/`, 414 file): 61.762 rilievi
totali, 54 con la configurazione ridotta. Letti 20: 5 veri (`GR_04_002`),
`ARTICOLATA_SOSTANTIVO` scatta quasi sempre su *sorgente* (maschile, e corretto: 25 rilievi) e
`COMMA_PARENTHESIS_WHITESPACE` su frammenti di codice in prosa. Qui la
precisione è bassa.

**Determinismo (S4).** Due esecuzioni complete, stessi 94.755 rilievi con la
stessa riga, regola e frammento. Passa.

**Costo (S3).** 171-189 s su 521 file con 3 thread; 119 s sui 414 documenti; 252
MB di jar; avvio del server 20 s. Passa.

**Un difetto trovato nel repo.** `ciclo_prosa.languagetool()` contava gli
offset di LanguageTool come punti di codice. LanguageTool li dà in unità UTF-16:
un'emoji ne vale due. Nei file con emoji (molti dei nostri) la riga
scivolava in avanti, e la prima passata ha dato parole troncate (*oradin* per
*Moradin*) finché non l'ho visto. Corretto in questa PR, con un test che fallisce
sul codice vecchio.

## 4. proselint 0.16 (BSD)

Solo inglese, e si vede. Sul contenuto di gioco: 3.167 rilievi in 14 s.

| Controllo | Rilievi | Cosa fa su testo italiano |
|---|---:|---|
| `typography.symbols.curly_quotes` | 1.280 | chiede «“”» al posto di `"`: il repo prescrive «», quindi **consiglia il contrario della norma** |
| `typography.symbols.ellipsis` | 821 | chiede `…`: il repo ha già `validate_lingua` |
| `misc.preferred_forms` | 326 | su *ne* («'né' is the preferred form») |
| `spelling.misc` | 271 | su *momento* («'memento' is the preferred spelling») |
| `industrial_language.chatspeak` | 79 | su *B4* (una coordinata di mappa) |
| `weasel_words.very`, `archaism`… | 155 | su righe **inglesi** copiate da guide altrui |

Righe italiane non tipografiche: 754 su 909. Di 20 letti a caso: **0 veri**; le
tre regole che producono 672 dei 754 sono liste di parole inglesi applicate a
italiano e non possono avere un vero. Il campione è di 40 (20 italiane, 20
inglesi), non di 100, e dichiaro la scelta: il difetto è strutturale, e leggere
altri 60 rilievi di *ne* → *né* non avrebbe aggiunto informazione. Sulle righe
inglesi i consigli sono di stile su testo che non è nostro. **proselint non
serve.**

## 5. Vale 3.x (MIT) con uno stile nostro

Lo stile è **generato** dalle tabelle del repo, non scritto a mano: una
`substitution` dalla tabella §8 del glossario, quattro `existence` dalle regex
di `CALCHI_SEMPRE`. È il test giusto, perché dice cosa aggiunge il motore e non
cosa aggiungono regole che avrei scritto io.

| Prova | Esito |
|---|---|
| Tokenizzazione di italiano e markdown (*città, perché, È*, tabelle, codice) | corretta; salta i blocchi di codice da solo |
| Le quattro regole dei calchi contro `validate_prosa` | **identiche: 11 righe su 11**, 0 in più, 0 in meno |
| Il foglio di stile contro `validate_prosa --foglio` | Vale 10 righe, il repo 0 |
| Tempo | 3 s, 4 processi |
| Fallimenti | **1 file di gioco** manda Vale in errore (`E201`): un `---` iniziale seguito da markdown è letto come front matter YAML. In un'esecuzione unica l'errore abortisce tutto |

Le 10 righe di Vale sul foglio, lette una per una:

| Riga | Cosa è |
|---|---|
| 4 nel glossario (§8) | la tabella che definisce le forme: attese, il repo salta `GLOSSARIO` |
| 1 nel titolo di `Arco-Post-Hammerfist-P1A…Hellas-COMPLETA.md` | un nome di file, che il repo non cambia |
| 5 in prosa | **errori veri che il repo non vede**: *«rituale di Hellas/arcidruidi»* (FASE0…:120), *«Hellas/druidi‑orsi»* (RETHMAR…:22), *«area Witchwood/Hellas»* (avarthel:25), *«**Hellas:** Round 40 … → COMPLETE!»* (P1C:859), *Cannathgate* (ARMATE-SYNC:200) |

I cinque veri sono mascherati da due scorciatoie di `validate_prosa`
(`_rx_forma` rifiuta una forma accanto a `/`; `_spiega_il_cambio` salta ogni
riga con una freccia `→`), scritte da me nella PR #213 per non segnalare i
percorsi e le righe che spiegano un cambio. **Il secondo rilevatore ha trovato
un difetto del primo.** Si ripara nel primo, in due righe: non serve Vale per
farlo. Non l'ho riparato qui, perché cambia cosa il gate segnala e i cinque
file andrebbero corretti nello stesso lotto.

Cosa **non** aggiunge Vale: i suoi tipi di regola (`existence`, `substitution`,
`consistency`, `repetition`, `occurrence`) sono quelli che il repo ha già come
liste di coppie `(regex, perché)`. Le regole che usano il testo analizzato
(`sequence`, `capitalization` su titoli) sono per l'inglese. L'ortografia di
Vale richiede un dizionario Hunspell italiano e ha lo stesso problema del gergo.
**Scrivere le norme in YAML di Vale vuol dire tenere due tabelle per la stessa
norma**, e la regola «una norma, un rilevatore» (ADR-0060) vieta proprio questo.

## 6. Licenze (parere nel mestiere dell'editore)

L'adozione di uno strumento è lo stesso mestiere dell'uscita (skill
`rumblingstone-edizione`, §1): il gate chiede il regime di ciò che entra.

| Strumento | Licenza | Come entrerebbe | Compatibilità con il repo |
|---|---|---|---|
| LanguageTool | LGPL-2.1 | servizio su `127.0.0.1`, nessun suo file nel repo, nessun suo codice linkato | compatibile; la LGPL obbliga chi *distribuisce* LanguageTool, e qui lo scarica la CI |
| Vale | MIT | binario compilato in CI, regole nostre | compatibile; le regole sono del repo, nessun pacchetto di stili di terzi (Microsoft, Google, write-good) |
| proselint | BSD (2014-2015, Suchow, Pacer, Ross) | non entra | irrilevante |

Nessun contenuto di gioco esce dal repo verso un servizio esterno: il server è
locale. Questo vincolo è la condizione, e l'ADR lo scrive.

## 7. Sintesi delle misure

| | LanguageTool (ridotto) | Vale (stile generato) | proselint |
|---|---|---|---|
| Rilievi sul contenuto | 189 (di 94.755) | 21 | 3.167 |
| Precisione, campione letto | **86%** su 100 | 11/11 identici ai nostri; 5 veri su 10 sul foglio | **0/20** italiano |
| Veri che il repo non vede | molti, ma una regex li trova | **5** (maschere del foglio) | 0 |
| Veri che solo lui trova | 3 (genere di *Mano Rossa*, *Conoscenze*) | 0 | 0 |
| Tempo | 171-189 s | 3 s | 14 s |
| Dimensione | 252 MB, JVM | 65 MB | 1 pacchetto |
| S1 | passa | non applicabile | non passa |
| S2 (alla lettera) | passa | non passa | non passa |
| S5 (contro la regex) | **non passa** | non passa | non passa |
| S3, S4 | passano | passano | passano |

**Conclusione onesta**: il miglioramento che LanguageTool sembra dare è
misurabile e **si ottiene con una regex**. Quello che resta non regge il costo
di una JVM e 252 MB in CI. Vale non apporta niente di nuovo come motore, ma
ha rivelato cinque errori veri e un difetto del foglio di stile. proselint non
serve.

## 8. Cosa non so

- La precisione è di un lettore solo. Su 100 rilievi, 86 ± 7 punti (intervallo
  di Wilson al 95%): sopra il 70% con margine, ma i 45 contesti distinti
  scendono il margine.
- Non ho una misura del **richiamo** sugli errori che il repo non sa descrivere:
  non c'è un corpus con gli errori marcati. La prova a 20 frasi è un indizio,
  non una misura.
- Non ho provato LanguageTool con l'estensione n-gram o con il modello neurale
  (richiedono gigabyte di dati) né con l'edizione a pagamento.
- Non ho provato Vale con dizionari Hunspell o con `Vale.Spelling`.
- I tempi di CI sono quelli del sandbox, non di un runner.

## Appendice A. Il campione di validazione (100 rilievi, seme 3510)

Etichette date a mano. «Vero» = un correttore lo cambierebbe nel testo nostro.

| # | Regola | File:riga | Frammento | Etichetta |
|---|---|---|---|---|
| 0 | ARTICOLATA_SOSTANTIVO | STANDALONE-Il-Drappo-di-Tarsilia/01-GIORNO-1-LA-SORTE.md:318 | «del Torre» | FP |
| 1 | GR_04_002 | Bestiario/png/thorgrim-barbadiferro.md:45 | «e'» | TP |
| 2 | GR_04_002 | Bestiario/mostri/underdark-dovil-runecaster-cr7.md:3 | «e'» | TP |
| 3 | GR_04_002 | Bestiario/villain/ostro-il-muto-cr5.md:12 | «e'» | TP |
| 4 | GR_04_002 | Bestiario/mostri/guardiano-di-luce-cr10.md:12 | «e'» | TP |
| 5 | GR_04_002 | 07_il Portale Della Forgia Eterna/ARC07-DEF-2-RITORNO-E-AFFRESCHI.md:192 | «Da'» | FP |
| 6 | GR_04_002 | Bestiario/mostri/sentinella-drow-ranger-cr8.md:12 | «e'» | TP |
| 7 | GR_04_002 | Bestiario/villain/zog-tar-deatheye-cr15.md:23 | «e'» | TP |
| 8 | COMMA_PARENTHESIS_WHITESPACE | Bestiario/villain/Il_Collezionista_Rakshasa/il-collezionista-rakshasa-cr18.md:5 | «,plane» | TP |
| 9 | GR_04_002 | Bestiario/mostri/marea-annis-cr6.md:12 | «e'» | TP |
| 10 | GR_04_002 | Bestiario/villain/terros-l-antico-cr15.md:10 | «e'» | TP |
| 11 | GR_04_002 | Bestiario/png/durin-rocciadura-cr6.md:50 | «e'» | TP |
| 12 | GR_04_002 | Bestiario/mostri/spettri-di-conoscenza-cr7.md:12 | «e'» | TP |
| 13 | GR_04_002 | 07_il Portale Della Forgia Eterna/ARC07-MATRICE-VERSIONI.md:35 | «e'» | TP |
| 14 | ARTICOLATA_SOSTANTIVO | 09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/RUMBLINGSTONE — ESPANSIONE NARRATIVA POST-HAMMERFIST.md:506 | «del Mano» | TP |
| 15 | GR_04_002 | Bestiario/png/re-thorek-i-cr16.md:24 | «e'» | TP |
| 16 | GR_04_002 | Bestiario/mostri/half-illithid-yochlol-cr11.md:12 | «e'» | TP |
| 17 | GR_04_002 | Bestiario/mostri/underdark-cleric-ainin-cr5.md:5 | «e'» | TP |
| 18 | GR_04_002 | Bestiario/villain/skullcrusher-il-nero-cr12.md:5 | «e'» | TP |
| 19 | GR_04_002 | Bestiario/png/durin-rocciadura-cr6.md:32 | «e'» | TP |
| 20 | GR_04_002 | Bestiario/mostri/carcassa-vivente-cr9.md:12 | «e'» | TP |
| 21 | GR_04_002 | Bestiario/png/durin-rocciadura-cr6.md:52 | «e'» | TP |
| 22 | GR_04_002 | Bestiario/png/durin-rocciadura-cr6.md:55 | «e'» | TP |
| 23 | GR_04_002 | Bestiario/mostri/drow-fungal-minion-cr6.md:12 | «e'» | TP |
| 24 | ARTICOLATA_SOSTANTIVO | Bestiario/villain/Sethrax_il_Velato/Sethrax.md:40 | «al lavanda» | FP |
| 25 | ARTICOLATA_SOSTANTIVO | campaign/DM-CAMPAIGN-PLAYBOOK.md:301 | «nel session» | FP |
| 26 | GR_04_002 | Bestiario/mostri/grinza-megera-acquatica-cr4.md:12 | «e'» | TP |
| 27 | COMMA_PARENTHESIS_WHITESPACE | 07_il Portale Della Forgia Eterna/Immagini/PROMPT-IMMAGINI-07ILP.md:212 | «.» | TP |
| 28 | GR_04_002 | 07_il Portale Della Forgia Eterna/ARC07-MATRICE-VERSIONI.md:36 | «e'» | TP |
| 29 | GR_04_002 | Bestiario/png/lady-koryn-cr12.md:12 | «e'» | TP |
| 30 | ARTICOLATA_SOSTANTIVO | campaign/DM-CAMPAIGN-PLAYBOOK.md:299 | «dai uno» | FP |
| 31 | GR_04_002 | Bestiario/villain/terros-l-antico-cr15.md:28 | «E'» | TP |
| 32 | COMMA_PARENTHESIS_WHITESPACE | Bestiario/mostri/ghost-lion-spettrale-cr8.md:3 | «,ruins» | TP |
| 33 | GR_04_002 | Bestiario/png/rurik-gorunn-cr10.md:21 | «e'» | TP |
| 34 | GR_04_002 | Bestiario/villain/zog-tar-deatheye-cr15.md:5 | «e'» | TP |
| 35 | GR_04_002 | Bestiario/mostri/costrutto-di-guardia-cr5.md:12 | «e'» | TP |
| 36 | GR_04_002 | Bestiario/png/kira-rogue12-cr12.md:12 | «e'» | TP |
| 37 | GR_04_002 | Bestiario/mostri/xorn-anziano-fauci-di-diamante-cr11.md:19 | «e'» | TP |
| 38 | COMMA_PARENTHESIS_WHITESPACE | Bestiario/villain/emissario-red-hand-cr12.md:3 | «,ruins» | TP |
| 39 | GR_04_002 | Bestiario/villain/skullcrusher-il-nero-cr12.md:25 | «E'» | TP |
| 40 | GR_04_002 | Bestiario/villain/saarvith-regiarix-cr13.md:12 | «e'» | TP |
| 41 | GR_04_002 | Bestiario/png/thorgrim-barbadiferro.md:54 | «e'» | TP |
| 42 | COMMA_PARENTHESIS_WHITESPACE | campaign/lore/dm-guide-to-be-adapted-tips&tricks.md:1159 | «,you» | FP |
| 43 | GR_04_002 | Bestiario/mostri/dire-worg-fiendish-corrotto-cr10.md:16 | «e'» | TP |
| 44 | ARTICOLATA_SOSTANTIVO | STANDALONE-Il-Drappo-di-Tarsilia/02-GIORNO-2-I-PARTITI-E-LA-CENA.md:190 | «dal Torre» | FP |
| 45 | GR_04_002 | Bestiario/villain/ostro-il-muto-cr5.md:10 | «e'» | TP |
| 46 | GR_04_002 | Bestiario/villain/terros-l-antico-cr15.md:21 | «e'» | TP |
| 47 | GR_04_002 | Bestiario/mostri/grinza-megera-acquatica-cr4.md:16 | «e'» | TP |
| 48 | GR_04_002 | Bestiario/villain/sedda-corvara-cr6.md:12 | «e'» | TP |
| 49 | GR_04_002 | Bestiario/mostri/xorn-anziano-fauci-di-diamante-cr11.md:10 | «e'» | TP |
| 50 | GR_04_002 | Bestiario/png/durin-rocciadura-cr6.md:45 | «e'» | TP |
| 51 | GR_04_002 | 09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ESITI-CONSEGUENZE.md:377 | «città'» | FP |
| 52 | GR_04_002 | Bestiario/mostri/cervello-fungino-errante-cr12.md:12 | «e'» | TP |
| 53 | COMMA_PARENTHESIS_WHITESPACE | 07_il Portale Della Forgia Eterna/Immagini/PROMPT-IMMAGINI-07ILP.md:831 | «.» | TP |
| 54 | COMMA_PARENTHESIS_WHITESPACE | 07_il Portale Della Forgia Eterna/ARC07-DEF-5-RITORNO-HAMMERFIST.md:23 | «(» | FP |
| 55 | GR_04_002 | Bestiario/mostri/drow-scout-ranger5-cr5.md:12 | «e'» | TP |
| 56 | COMMA_PARENTHESIS_WHITESPACE | 07_il Portale Della Forgia Eterna/Immagini/PROMPT-IMMAGINI-07ILP.md:192 | «.» | TP |
| 57 | GR_04_002 | Bestiario/png/zhen-windwhisper-cr11.md:12 | «e'» | TP |
| 58 | GR_04_002 | Bestiario/png/thorgrim-barbadiferro.md:53 | «e'» | TP |
| 59 | COMMA_PARENTHESIS_WHITESPACE | Bestiario/mostri/githyanki-knight-elite-cr10.md:3 | «,plains» | TP |
| 60 | COMMA_PARENTHESIS_WHITESPACE | Bestiario/mostri/ondata-giganti-fanteria-cr15.md:7 | «,urban» | TP |
| 61 | GR_04_002 | Bestiario/villain/terros-l-antico-cr15.md:26 | «e'» | TP |
| 62 | GR_04_002 | campaign/state-changelog.md:8 | «e'» | TP |
| 63 | GR_04_002 | Bestiario/png/durin-rocciadura-cr6.md:35 | «e'» | TP |
| 64 | GR_04_002 | Bestiario/mostri/underdark-cleric-ainin-cr5.md:3 | «e'» | TP |
| 65 | GR_04_002 | Bestiario/png/madre-ilaria-sonda-cr7.md:12 | «e'» | TP |
| 66 | GR_04_002 | Bestiario/png/grom-skullcrusher-cr14.md:12 | «e'» | TP |
| 67 | COMMA_PARENTHESIS_WHITESPACE | 07_il Portale Della Forgia Eterna/Immagini/PROMPT-IMMAGINI-07ILP.md:871 | «.» | TP |
| 68 | GR_04_002 | Bestiario/villain/skullcrusher-il-nero-cr12.md:29 | «e'» | TP |
| 69 | GR_04_002 | 07_il Portale Della Forgia Eterna/ARC07-DEF-3-RESURREZIONE-HELLA.md:941 | «Da'» | FP |
| 70 | GR_04_002 | Bestiario/mostri/underdark-dovil-runecaster-cr7.md:26 | «e'» | TP |
| 71 | GR_04_002 | Bestiario/villain/skullcrusher-il-nero-cr12.md:27 | «e'» | TP |
| 72 | GR_04_002 | Bestiario/mostri/swarm-pseudodraconici-gith-cr8.md:12 | «e'» | TP |
| 73 | GR_04_002 | Bestiario/mostri/drow-pyromancer-completo-cr9.md:12 | «e'» | TP |
| 74 | ARTICOLATA_SOSTANTIVO | 09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/RUMBLINGSTONE — ESPANSIONE NARRATIVA POST-HAMMERFIST.md:439 | «del Mano» | TP |
| 75 | GR_04_002 | Bestiario/villain/terros-l-antico-cr15.md:34 | «e'» | TP |
| 76 | GR_04_002 | 07_il Portale Della Forgia Eterna/ARC07-DEF-3-RESURREZIONE-HELLA.md:760 | «Da'» | FP |
| 77 | GR_04_002 | Bestiario/mostri/drow-psionica-mezzo-illithid-cr8.md:12 | «e'» | TP |
| 78 | GR_04_002 | Bestiario/villain/terros-l-antico-cr15.md:17 | «e'» | TP |
| 79 | GR_04_002 | Bestiario/mostri/underdark-dovil-runecaster-cr7.md:3 | «e'» | TP |
| 80 | GR_04_002 | Bestiario/villain/terros-l-antico-cr15.md:13 | «e'» | TP |
| 81 | GR_04_002 | Bestiario/mostri/underdark-dovil-runecaster-cr7.md:5 | «e'» | TP |
| 82 | GR_04_002 | Bestiario/png/durin-rocciadura-cr6.md:44 | «e'» | TP |
| 83 | ARTICOLATA_SOSTANTIVO | 09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/RUMBLINGSTONE — ESPANSIONE NARRATIVA POST-HAMMERFIST.md:373 | «del Mano» | TP |
| 84 | GR_04_002 | Bestiario/mostri/underdark-cleric-ainin-cr5.md:3 | «e'» | TP |
| 85 | GR_04_002 | Bestiario/villain/zog-tar-deatheye-cr15.md:14 | «E'» | TP |
| 86 | GR_04_002 | Bestiario/png/re-thorek-i-cr16.md:20 | «e'» | TP |
| 87 | GR_04_002 | Bestiario/png/durin-rocciadura-cr6.md:35 | «e'» | TP |
| 88 | GR_04_002 | Bestiario/mostri/xorn-anziano-fauci-di-diamante-cr11.md:17 | «e'» | TP |
| 89 | GR_04_002 | Bestiario/png/bothor-malvur-cr6.md:3 | «e'» | TP |
| 90 | GR_04_002 | Bestiario/villain/ghebro-malaluna-cr8.md:12 | «e'» | TP |
| 91 | GR_04_002 | Bestiario/png/re-thorek-i-cr16.md:16 | «e'» | TP |
| 92 | COMMA_PARENTHESIS_WHITESPACE | campaign/lore/dm-guide-to-be-adapted-tips&tricks.md:1269 | «)» | FP |
| 93 | GR_04_002 | Bestiario/png/tetsu-serpente-di-vento-cr12.md:12 | «e'» | TP |
| 94 | GR_04_002 | Bestiario/png/tiberio-sarda-cr6.md:12 | «e'» | TP |
| 95 | COMMA_PARENTHESIS_WHITESPACE | Bestiario/villain/Zarim/zarim-illithid-luogotenente-cr12.md:3 | «,dungeon» | TP |
| 96 | ARTICOLATA_SOSTANTIVO | 09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2D-PALIO-VERIFICA-LEGALE-IP.md:143 | «del label» | FP |
| 97 | COMMA_PARENTHESIS_WHITESPACE | 07_il Portale Della Forgia Eterna/Immagini/PROMPT-IMMAGINI-07ILP.md:453 | «.» | TP |
| 98 | ARTICOLATA_SOSTANTIVO | STANDALONE-Il-Drappo-di-Tarsilia/03-GIORNO-3-LO-STACCO-E-LA-CORSA.md:387 | «alle Civetta» | FP |
| 99 | GR_04_002 | Bestiario/mostri/avatar-minore-madre-funghi-cr13.md:12 | «e'» | TP |
