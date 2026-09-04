# PIANO — Audit di provenienza e vendibilità del repo

> **Stato**: 🔵 **proposta, non autorizzata** · **Aperto**: 2026-09-04
> **Richiesta-fonte (DM, 2026-09-04)**: *«c'è un obiettivo commerciale, vorrei
> venderlo se possibile: tutto l'AP completo, gli standalone, e in parte
> dividendo il tool per DM, il server MCP e il generatore. Per il momento 3.5 e
> PF1e, ma pensare al supporto per la 5e e forse PF2e. In pratica avere una
> piccola revenue da questo progetto.»*
> **Precedenti da leggere prima**: [ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md)
> (confini IP e uso non commerciale) · [ADR-0029](adr/ADR-0029-licenza-doppia-testo-e-script.md)
> (licenza doppia) · `LICENSES.md` · `OGL.txt` · `docs/guides/GUIDA-CONDIVISIONE-IP.md`
> · il piano del [Drappo di Tarsilia](PIANO-DRAPPO-DI-TARSILIA-STANDALONE-PF1E.md),
> che è il prototipo funzionante della strada giusta

> ⚠️ Questo è un piano di ingegneria e di documentazione, non un parere legale.
> Stessa riserva che ADR-0005 mette su sé stesso: una vendita reale richiede
> comunque un avvocato IP, e questo piano serve a **arrivarci con le carte in
> ordine**, non a sostituirlo.

---

## §0 · Il verdetto che va detto per primo

**L'AP completo adattato da Red Hand of Doom non è vendibile, e nessun lavoro
sulle illustrazioni lo rende vendibile.**

RHoD (James Jacobs e Richard Baker, Wizards of the Coast, 2006) non è mai stato
Open Game Content. WotC ha rilasciato come OGC il *System Reference Document*,
non i propri moduli d'avventura. Trama, struttura degli incontri, PNG, toponimi,
testo descrittivo: contenuto chiuso. Un adattamento è **opera derivata**, e
l'espansione non cambia la provenienza — si può espandere per mille pagine e
resta derivata da un'opera chiusa.

Tre precisazioni, perché è qui che si sbaglia:

1. **L'OGL non è l'ostacolo.** L'OGL 1.0a *permette esplicitamente* l'uso
   commerciale: si vendono prodotti OGC da venticinque anni. L'ostacolo è che
   RHoD non è mai stato sotto OGL.
2. **Rigenerare le tavole risolve una frazione del problema.** Le illustrazioni
   sono il 5%; la trama è il 95%. Un modulo con arte nuova che racconta la stessa
   storia con gli stessi PNG negli stessi luoghi resta derivato.
3. **ADR-0005 lo diceva già**, ma lo diceva sull'*uso commerciale del repo*
   («blocco assorbente per tutto il repo», «nessuna licenza dell'autore può
   sanare»). Qui va detto sul **prodotto**, che è la forma in cui la domanda
   arriva davvero.

La conseguenza pratica: la campagna RumblingStone come tale resta quello che è
sempre stata, materiale privato per il proprio tavolo. È già la posture di
ADR-0005 e non cambia.

**Quello che si vende è un'altra cosa, e vale più di quanto sembri.**

---

## §1 · Cosa è vendibile davvero

Quattro linee di prodotto, in ordine di distanza dal blocco WotC.

| # | Linea | Cosa contiene | Stato oggi |
|---|---|---|---|
| **1** | **Gli strumenti** | `dm.py`, il generatore di creature, il renderer di mappe, la pipeline Typst, il server MCP | esistono e funzionano; MIT |
| **2** | **Gli standalone** | il Drappo di Tarsilia, e i suoi successori | uno esiste, tre lotti su cinque chiusi |
| **3** | **I sistemi originali** come supplementi | il Palio (Sorte, Partiti, Morale/Onore, Stacco, Corsa), il framework d'indagine (Acume/Perizia/Metodo, ADR-0022), il March Clock, le sei porte | sparsi dentro la campagna, mai estratti |
| **4** | **Un AP nuovo** | trama propria, costruita sull'infrastruttura editoriale già in piedi | non esiste |

La riga 4 è quella che vale di più, ed è la meno ovvia. Il repo ha costruito, per
servire RHoD, un apparato che RHoD non richiedeva: lo standard di modulo
definitivo, il motore di stile narrativo, la pipeline delle mappe a qualità AP, la
catena editoriale Typst con colophon e imposizione, il collaudo. Quell'apparato
non è derivato da niente. **RHoD è stato il campo di addestramento**, e ciò che si
è imparato è trasferibile a una storia propria.

⚠️ La riga 1 ha un problema suo, e va deciso presto. Gli strumenti sono **MIT**:
chiunque li può prendere e ridistribuire, anche a pagamento. Vendere software MIT
si può, ma il modello non è «vendo le copie» — è servizio ospitato, supporto,
distribuzione comoda, o doppia licenza. Il DM ne detiene il copyright e **può**
cambiare licenza per le versioni future; le versioni già pubblicate restano MIT
per sempre. Se la vendita degli strumenti è seria, la scelta va fatta prima che
il codice giri.

---

## §2 · I quattro regimi, e quale conviene

Questa è la parte che il supporto a 5e e PF2e rende decisiva, perché **i sistemi
non hanno tutti lo stesso regime, e il più permissivo non è quello che il repo
usa oggi.**

| Sistema | Regime | Commerciale | Cosa comporta nel prodotto |
|---|---|---|---|
| **D&D 5e** — SRD 5.1 e 5.2 | **CC BY 4.0** | ✅ | una riga di attribuzione. **Nessuna catena di copyright, nessun testo di licenza da allegare** |
| **D&D 3.5** — SRD | OGL 1.0a | ✅ | testo integrale della licenza + Sezione 15 in ogni copia |
| **PF1e** — PRD | OGL 1.0a | ✅ | idem, con le voci Paizo |
| **PF2e Remaster** | **ORC** | ✅ | licenza diversa e irrevocabile; il pre-remaster resta OGL |
| **RHoD, Forgotten Realms non-SRD** | chiuso | ❌ | nessuna via |

Due conseguenze strategiche che cambierebbero l'ordine dei lavori.

**Il 5e è la porta più larga, e nel repo non c'è ancora niente di 5e.** WotC ha
messo l'SRD 5.1 sotto CC BY 4.0 nel 2023, e ha dichiarato che tutte le versioni
future dell'SRD escono solo sotto Creative Commons — l'SRD 5.2 è già così. CC BY
4.0 è il regime più semplice che esista in questo settore: attribuzione, e basta.
Nessuna Sezione 15 da tenere allineata, nessun obbligo di allegare il testo della
licenza, nessuna «contaminazione» del contenuto proprio. Sommato al fatto che il
5e è il mercato più grande, è la direzione con il rapporto sforzo/ritorno
migliore — ed è anche quella su cui il repo ha meno lavoro fatto.

**Non si mescolano i regimi dentro un prodotto.** Un volume che prende meccanica
dall'SRD 3.5 (OGL) e dall'SRD 5.1 (CC BY) deve rispettare tutt'e due, e non può
ri-licenziare l'OGC come CC BY. La regola operativa è: **un prodotto, un
regime**. Il supporto multi-sistema si fa con edizioni separate, non con un
volume che le contiene entrambe.

---

## §3 · Le tavole, che è la domanda che il DM ha posto

**Le illustrazioni originali di RHoD non si vendono, in nessuna forma.** Vale
anche per le mappe: `fr-cannath-vale.md` credita esplicitamente la mappa della
Elsir Vale a **Mike Schley**, che è un illustratore vivente e il titolare del suo
lavoro. Al tavolo privato vanno bene; in un prodotto in vendita, no.

Rigenerare è la strada giusta. Ma «mantenere lo stesso stile» va inteso bene, e
la distinzione è netta:

- **il linguaggio visivo** — palette, tratto, resa del terreno, tipografia della
  legenda — non è protetto, e imitarlo è lecito e sensato;
- **la composizione specifica** — questa mappa, questa inquadratura, questo
  personaggio in questa posa — lo è. Una ricostruzione riconoscibile di una
  tavola precisa è derivata anche se ridisegnata da zero.

Il repo ha già lo strumento giusto e non lo sa: la skill
`rumblingstone-art-direction` ha la **bibbia visiva** e il **gate di rifiuto**.
Quella è esattamente la disciplina per definire uno stile *proprio* e coerente
invece di inseguirne uno altrui. Il lavoro non è «rifare le tavole»: è **decidere
come si vede RumblingStone**, e poi produrre su quella decisione.

⚠️ **Il problema vero dell'arte generata da IA in un prodotto venduto non è
usarla: è proteggerla.** Le opere puramente generate da IA hanno tutela
incerta — negli Stati Uniti il Copyright Office richiede autorialità umana. Per
un prodotto in vendita significa che le immagini si possono usare, ma non si può
impedire a nessuno di riusarle. Se il prodotto vende **sulle immagini**, è un
problema serio; se vende **sul contenuto**, è un costo accettabile — e per un
modulo d'avventura è il secondo caso.

Sui generatori, due cose e non di più, perché la scelta va rifatta al momento
dell'uso:

- **le licenze commerciali variano per strumento e spesso stanno dietro
  abbonamento** (Inkarnate, DungeonFog e simili aprono il commerciale solo sui
  piani a pagamento). Vanno lette per strumento, al momento in cui si compra;
- **il repo ha già il percorso a licenza più chiara e costo marginale zero**:
  ComfyUI locale, che `GUIDA-IMMAGINI` §setup documenta e che la skill mapmaking
  usa per la passata «hero map» partendo da una mappa **già renderizzata dal
  renderer del repo**. ⚠️ La guida già segnala il punto vero: ComfyUI è GPL-3 e
  non limita ciò che produce, **ma i pesi del modello hanno licenza propria**. È
  lì che va guardato, non nel software.

Che il punto di partenza sia una mappa generata dal repo, e non un'immagine
altrui, è ciò che rende questa strada difendibile: la composizione è già nostra.

---

## §4 · I lotti

### ⬜ Lotto A — L'audit di provenienza, su tutto il repo

Il DM ha chiesto l'audit completo, e per l'obiettivo commerciale ha ragione:
una mappa parziale non permette di dire «questo si vende» di niente.

Per ogni artefatto, una domanda sola e ben posta: **«se questo file fosse
l'unica cosa dentro il prodotto, sotto quale regime esce?»** Quattro secchi:

| Secchio | Regime | Può essere venduto |
|---|---|---|
| **OGC-3.5** | OGL 1.0a | sì, con Sezione 15 |
| **OGC-PF1e** | OGL 1.0a | sì, con Sezione 15 |
| **WotC chiuso** (trama RHoD, FR non-SRD, tavole altrui) | nessuno | **no** |
| **Originale** | CC BY-NC-SA oggi, rinegoziabile dall'autore | sì, ed è **staccabile** |

Buona parte è già leggibile a macchina e non va fatta a mano: le righe `fonte:`
dei 157 statblocchi, `tools.manifest.json`, il contratto JSON delle mappe, i
frontmatter delle skill. I casi duri sono tre, e vanno affrontati sapendo che
sono duri: la **prosa** che porta struttura RHoD senza citarla; i **398 file
immagine**; le **mappe che rappresentano luoghi RHoD** anche quando il disegno è
nostro.

⚠️ **Prerequisito bloccante, già noto**: ADR-0005 segna come debito aperto la
provenienza delle tavole raster «fornite dal DM». Finché non è documentata,
quella fetta dell'audit non si chiude. Va affrontata per prima, non per ultima,
o il lotto si ferma a tre quarti.

**Accettazione**: una tabella per artefatto con secchio e verdetto di
vendibilità; l'elenco esplicito dei casi **irrisolti** (che è un'uscita, non un
fallimento); e per ciascuna delle quattro linee di prodotto di §1, la lista dei
file che ci entrerebbero.

### ⬜ Lotto B — Rendere la provenienza un dato, non un'opinione

Un campo `provenienza:` machine-readable dove manca, un
`validate_provenienza.py` nello stile dei validatori che il repo ha già, e
`OGL.txt` che cresce **additivamente**: una voce di Sezione 15 per ogni fonte
effettivamente trovata dal lotto A.

⚠️ **Additivo, mai «importa tutto e poi lima».** Importare le 93 voci del PRD e
poi togliere ha due difetti: nella finestra fra import e limatura il repo
*dichiara* usi che non ha (e una catena falsa è peggio di una corta, perché
rivendica libri mai aperti); e limare è sottrattivo, cioè si toglie una voce
perché non si è *trovato* un uso — un argomento dall'assenza, che fallisce in
silenzio proprio su ciò che non si è pensato di cercare. È lo stesso modo in cui
*hungry pit* era sparito dall'ancora PF1e mentre il test passava.

**Accettazione**: ogni artefatto ha una provenienza dichiarata o compare
nell'elenco degli irrisolti; nessuna voce di `OGL.txt` è priva di un artefatto
che la giustifichi.

### ⬜ Lotto C — Il gate che si passa, invece di citarlo

Il test nei **due sensi**, che è ciò che rende la limatura inutile per
costruzione: ogni artefatto OGC ha la sua voce in `OGL.txt`, **e** ogni voce in
`OGL.txt` è usata da almeno un artefatto. La catena non può andare né lunga né
corta.

Poi il cancello di `GUIDA-CONDIVISIONE-IP` §7 diventa eseguibile — `dm.py doctor
--ip` o simile — e un **test negativo**: un artefatto con provenienza WotC chiusa
deve **fallire** il controllo «può uscire».

⚠️ **L'ambito di collaudo che il DM ha chiesto più severo.** Il test che conta
non è unitario: si prende una **linea di prodotto candidata** (il Drappo è già
pronta a farlo), la si passa dal gate **senza eccezioni manuali**, e si guarda se
esce. Un gate che passa solo aggiungendo deroghe non è un gate.

**Accettazione**: il Drappo passa il gate a secco; un file dell'arco 00 lo
fallisce con la ragione scritta; `doctor --ip` sta in CI.

---

## §5 · Quando arriva l'ADR

**Dopo il lotto A, non prima**, e la ragione è di sostanza. Il contenuto
decisionale dell'ADR è *la tassonomia dei secchi e la regola per assegnarli*, e
non la si scrive credibilmente prima che l'audit mostri come sono distribuiti i
casi reali. Scriverla prima significa decidere su una distribuzione che non si è
vista — e i quattro secchi di §4 sono un'ipotesi, non un risultato.

Probabilmente saranno due ADR e non uno: la tassonomia della provenienza, e la
scelta di regime per linea di prodotto (che è dove entra la decisione 5e).

---

## §6 · Cosa resta da decidere, e va deciso dal DM

1. **La licenza degli strumenti.** MIT permette a chiunque di rivendere. Se la
   linea 1 è seria, la scelta (doppia licenza? servizio ospitato? MIT e si vende
   il servizio?) va fatta **prima** che il codice circoli.
2. **L'ordine fra 5e e l'audit.** Se il 5e è la porta più larga e nel repo non
   c'è, forse il primo prodotto vendibile non è un pezzo dell'esistente: è un
   supplemento nuovo, in 5e, sotto CC BY 4.0, costruito su un sistema originale
   della riga 3. Costerebbe meno dell'audit completo e produrrebbe ricavo prima.
   L'audit resta necessario, ma forse non è il **primo** lavoro.
3. **La provenienza delle tavole raster** (ADR-0005). Blocca il lotto A.
4. **Che cosa si vende, per davvero.** «Un po' di revenue» da un modulo
   d'avventura indipendente è un ordine di grandezza diverso da «revenue» da uno
   strumento in abbonamento. Le due cose vogliono lavori diversi, e sapere quale
   si insegue cambia l'ordine dei lotti.
