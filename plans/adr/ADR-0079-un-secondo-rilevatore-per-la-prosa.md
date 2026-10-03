# ADR-0079 — Un secondo rilevatore per la prosa: Vale, LanguageTool, proselint

- **Stato**: **proposta** (in attesa della risposta del DM; niente di quanto
  segue è in vigore)
- **Data**: 2026-10-03
- **Decisori**: DM (Gianfranco Samuele), agente
- **Decisione-fonte**: il DM, il 2026-10-03, dopo la PR #213: se la licenza MIT
  non è un problema, qual è il vero motivo per non usare Vale, proselint e
  LanguageTool come secondo rilevatore; rivalutarli, mostrare cosa apportano,
  e chiedere se importarli, anche con un'eccezione ad ADR-0077 e al principio
  «stdlib-only» e «una norma, un rilevatore», se il miglioramento è evidente e
  misurabile.
- **Rapporti**: ritorna su [ADR-0077](ADR-0077-revisione-a-due-giri.md) §«Alternative scartate» e su
  [ADR-0078](ADR-0078-il-foglio-di-stile-si-esegue.md) §«Installare Vale»; applica
  [ADR-0060](ADR-0060-la-forma-rende-misurabile-cio-che-la-parola-non-distingue.md)
  («una norma, un rilevatore») e la sesta regola d'oro; misura: [RICERCA-SECONDO-RILEVATORE](../RICERCA-SECONDO-RILEVATORE-VALE-LT-PROSELINT-2026-10.md)

## Contesto

ADR-0077 aveva scartato Vale e proselint in una riga e lasciato LanguageTool
come servizio facoltativo fuori dalla CI. ADR-0078 aveva ripetuto il rifiuto di
Vale. **Nessuna delle due volte c'era una misura**: lo strumento non era
installato. Il motivo vero della scelta era un giudizio di costo e beneficio,
non un dato, e il DM ha fatto bene a chiederlo.

La ricerca allegata ha installato i tre strumenti nel sandbox (LanguageTool 6.8
da Maven Central come server locale; Vale compilato dal sorgente; proselint 0.16
da PyPI), li ha fatti girare su 521 file di gioco e 414 documenti, e ha letto a
mano 100 rilievi di validazione e 98 di calibrazione, con le soglie scritte
prima.

## Misura (sintesi; il dettaglio e l'elenco dei 100 rilievi sono nella ricerca)

| | LanguageTool | Vale | proselint |
|---|---|---|---|
| Configurazione predefinita | 94.755 rilievi, il 99,4% da scartare | n/a | 3.167, quasi tutti sbagliati |
| Dopo la calibrazione | 189 rilievi, **precisione 86%** su 100 letti | calchi: **11/11 identici** ai nostri; foglio: 5 veri su 10 | **0/20** su righe italiane |
| Veri nuovi rispetto ai rilevatori del repo | sì: 93% dei veri | **5**, ma sono difetti del foglio di stile | 0 |
| Veri nuovi rispetto a **una regex** nel repo | **3** (soglia 10) | 0 come motore | 0 |
| Tempo | 171-189 s, JVM, 252 MB | 3 s, 65 MB | 14 s |
| Determinismo | sì (due giri identici) | sì | sì |

Tre fatti pesano più degli altri:

1. **Il guadagno di LanguageTool è un solo errore ripetuto**: l'apostrofo al posto
   dell'accento (*e'* per *è*). 72 dei 100 letti sono questo, e 45 sono i
   contesti distinti. Una regex in `validate_lingua` trova le stesse 121 righe
   di LanguageTool, più 58 che LanguageTool non vede, e nessun falso *Da'*.
2. **Le regole grammaticali italiane di LanguageTool sono poche**: su venti
   frasi con un errore noto non rileva concordanze, congiuntivi, articoli.
   L'ortografia, che è la parte forte, sul nostro testo è rumore: gergo di
   gioco, inglese degli statblock, nomi.
3. **Vale come motore non aggiunge niente alle nostre regole**, ma usato come
   *secondo parere* sul foglio di stile ha trovato cinque grafie sbagliate
   (*Hellas*, *Cannathgate*) che due scorciatoie di `validate_prosa` mascheravano:
   `/` accanto alla forma e la freccia `→` in riga.

Le soglie scritte prima: S1 (precisione ≥ 70%) passa per LanguageTool ridotto;
S2 (≥ 30% nuovi e ≥ 50) passa alla lettera; S3 e S4 passano. **La lettura onesta
è che S2, scritta così, si supera per una ragione che G6 vieta di accettare**, e
ho aggiunto S5 dopo aver visto i dati: il contributo marginale contro la miglior
alternativa interna. S5 non passa. Lo dichiaro come criterio aggiunto a
posteriori: il DM può non riconoscerlo, e allora LanguageTool passa tutte e
quattro le soglie originali.

## Decisione proposta

**Raccomandazione (prima opzione): non importare nessuno dei tre come
rilevatore di default; prendere dalla misura tre correzioni interne.**

1. `validate_lingua.py`: una regola nuova, **avviso** e non errore, per
   l'apostrofo al posto dell'accento (*e', gia', piu', puo', perche', cio'…*),
   con la lista di parole accentabili. 179 righe oggi. Una norma, un
   rilevatore: è dove la norma già vive.
2. `validate_prosa.py`: le due scorciatoie del foglio di stile. Una forma
   esclusa accanto a `/` in prosa è un rilievo (il confine di parola vale per i
   percorsi, non per *Hellas/druidi*); una riga con `→` non è «spiegata» se la
   forma esclusa sta fuori dalle virgolette della spiegazione. Poi correggere i
   cinque casi nei quattro file, in un lotto di contenuto separato.
3. `ciclo_prosa.languagetool()`: la correzione degli offset UTF-16, **già in
   questa PR** con un test che fallisce sul vecchio codice. Il servizio
   facoltativo resta come in ADR-0077 (`--languagetool URL`, fuori dalla CI),
   ora con la riga giusta.

Cosa **non** cambia: ADR-0077 resta in vigore. L'eccezione che il DM ha
previsto non serve.

### Le opzioni, per la risposta del DM

| | Cosa | Costo | Cosa si ottiene |
|---|---|---|---|
| **A (raccomandata)** | le tre correzioni interne sopra; niente di nuovo in CI | poche righe, con test | tutto il vero che LanguageTool e Vale hanno trovato, più 58 righe |
| B | A, più LanguageTool come **passo facoltativo** del ciclo (`ciclo_prosa.py segnala --languagetool`) con la lista di sole tre regole tenute; documentato, non in CI | uno script di avvio del server, 252 MB in locale | 3 veri in più su 10 di `ARTICOLATA_SOSTANTIVO`, e in futuro la grammatica di cui il progetto si accorgerà |
| C | B, più LanguageTool come **passo di CI** (Java 17, cache Maven di 252 MB, ~3 minuti, non bloccante, peso `minore` in `specifiche-qualita.yaml`) | JVM e Maven nella CI, manutenzione del server, rumore da governare | il controllo a ogni PR |
| D | Vale come secondo motore del foglio di stile | un binario Go, **due tabelle per una norma** | niente che A non dia |

Con **B o C** servono, prima di scrivere il codice: la lista delle regole tenute
in una sola tabella (non una seconda tabella di norme: LanguageTool è un
*rilevatore* e la norma resta in `editorial-standards.md`); una riga nel
`REGISTRO-NORME-EDITORIALI.md` che dica *chi la misura* (ADR-0056); un test con
il server finto, come quelli di `TestLanguageTool`; la voce nel manifest dei
tool; e il comando di avvio con il percorso Maven riproducibile. Il peso nel
punteggio MQM sarebbe `minore` (1), mai `critico`: un falso positivo non può
bocciare un documento.

## Alternative scartate

- **Importare LanguageTool con tutte le regole**: 94.755 rilievi. Inutilizzabile.
- **Dizionario personale per l'ortografia**: il gergo (statblocco, humanoid,
  upscale, nanica) è di migliaia di parole e cresce a ogni sessione.
- **Vale con regole scritte in YAML**: le regole diventerebbero due tabelle,
  quella di `validate_prosa` e quella di Vale, e andrebbero tenute in sincronia
  a mano. È proprio ciò che ADR-0060 e ADR-0078 hanno vietato.
- **proselint**: lista di parole inglesi letta su testo italiano; consiglia
  `“”` dove il repo prescrive «».
- **Aggiungere un criterio di accettazione per non decidere**: S5 è dichiarata a
  posteriori e il DM può scartarla; non è nascosta.

## Conseguenze

**Quello che si paga con A.** Un avviso nuovo in `validate_lingua` (179 righe in
contenuto che oggi non lo vede: il conteggio degli avvisi sale), e un lotto di
correzione quando il DM lo approva. Il foglio di stile, riparato, segnala
cinque righe che oggi tace. Nessuna dipendenza nuova.

**Quello che si paga con B o C.** Java 17 e 252 MB di jar; un server da avviare;
un rilevatore che dipende dalla rete al primo download e dal dizionario di una
versione (6.8): un aggiornamento di LanguageTool cambia i rilievi e rompe il
confronto prima/dopo. Il rumore resta alto se si apre una regola non tarata.
La LGPL-2.1 non pesa finché LanguageTool si usa come servizio e non si copia
nel repo; la CI lo scarica, non lo distribuisce. Il contenuto di gioco non
esce dal repo: il server è su `127.0.0.1`. **`api.languagetool.org` non va mai
usato**: manderebbe il testo della campagna a un servizio esterno.

**Cosa non so.** La precisione è di un lettore solo (86% con intervallo di
Wilson 78-91). Non ho una misura del richiamo. I tempi sono del sandbox. Non ho
provato i modelli n-gram, Vale con Hunspell, né l'edizione a pagamento.

## Da rivisitare

Se in un anno LanguageTool avrà regole italiane di grammatica che scattano su
errori veri della prosa nostra (concordanza, congiuntivo), la prova a venti
frasi e la validazione si rifanno con la stessa procedura: le soglie S1-S4 sono
scritte nella ricerca.

## Se il DM risponde sì a B, C o D

Si introduce l'eccezione a questo ADR (che passa da *proposta* ad *accettata*,
con la riga della scelta), si scrivono le soglie e i pesi **prima**, si
implementa con test e si rimisura il miglioramento sul repo. Niente di questo è
stato fatto.
