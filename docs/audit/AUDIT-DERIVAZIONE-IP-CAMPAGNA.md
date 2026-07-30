# AUDIT — Quanto di RumblingStone è derivato da *Red Hand of Doom*?

> **Domanda del DM (2026-07-26)**: *«tutta l'avventura è stata scalata all'8° livello,
> sono state introdotte molte parti non esistenti, PNG e villain non presenti
> nell'avventura principale, tutta la parte di Hammerfist, la discesa nell'Underdark…
> non saprei se è possibile venderlo come espansione per D&D 3.5 o su Paizo, se si
> cambiano l'ambientazione, i PNG e i luoghi.»*
>
> **Metodo**: misura, non impressione. Conteggio dei nomi propri di terzi su tutto
> il corpus, normalizzato sul volume di ogni arco.
>
> ⚠️ **LEGGERE §6-bis PRIMA DI §1-§5.** La prima stesura cercava solo *Red Hand
> of Doom* e i toponimi Forgotten Realms. Il repo dichiara **altre quattro fonti
> WotC**, con numeri di pagina: le conclusioni di §1-§5 sono corrette per la
> fonte che misurano e **insufficienti** per decidere il perimetro commerciale.
> **Data**: 2026-07-26 · **Corpus**: `main` @ branch di analisi.
>
> ⚠️ **Questa non è consulenza legale.** È un'analisi documentale di conformità,
> come già il rapporto P2D del 2026-07-18. Una pubblicazione commerciale reale
> richiede un avvocato IP.

---

## 0. La risposta in tre righe

1. **Come «espansione per Red Hand of Doom»: no, per nessuna via.** Non esiste
   licenza che lo consenta (§4.1).
2. **Come Adventure Path originale autonomo: sì.** Base pulita da *tutte* le
   fonti: **archi 07+08 ≈ 233.000 parole** (§6-bis).
3. **Il problema più grosso non è la Mano Rossa: è Moradin** — 1.502 occorrenze,
   e non è SRD (§3.2).
4. ⚠️ **§1-§5 misurano solo RHoD e i toponimi FR: sono incompleti.** Ci sono
   **altre quattro fonti WotC dichiarate dal repo stesso** — leggere §6-bis
   **prima** di prendere decisioni su questi numeri.

---

## 1. Volume del corpus

| Arco | Parole | Densità RHoD (occorrenze / 1.000 parole) |
|---|---:|---:|
| 00 — impalcatura di campagna (tabelle armate, flusso) | 7.750 | **20,2** |
| 04 — Tomba di Belkram | 2.830 | **0,0** |
| 06 — Stanza della Corona di Adamantio | 16.271 | **0,0** |
| 07 — Portale della Forgia Eterna | 151.588 | **0,3** |
| 08 — Battaglia di Hammerfist | 81.422 | **1,1** |
| 09 — Continuazione post-Hammerfist | 195.739 | **5,3** |
| **Totale** | **~455.600** | |

*(Gli archi 01, 02, 03, 05 hanno cartelle senza `.md`: il contenuto vive altrove.)*

Per scala: 455.000 parole sono **tre o quattro manuali d'avventura**. Non è un
progetto da valutare come «un modulo».

---

## 2. La derivazione non è distribuita: è concentrata

**Questo è il risultato che cambia la risposta.**

```
arco 04 ·············································· 0,0
arco 06 ·············································· 0,0
arco 07 ·█··········································· 0,3   151.588 parole
arco 08 ·███········································· 1,1    81.422 parole
arco 09 ·███████████████████························· 5,3   195.739 parole
arco 00 ·████████████████████████████████████████████ 20,2    7.750 parole
```

- **252.111 parole** (archi 04-08) stanno a densità **≈ 0,5**: è *naming*, non
  struttura. Un nome si sostituisce; una struttura no.
- **195.739 parole** (arco 09) stanno a **5,3** — dieci volte tanto. E non per
  caso: il piano `PIANO-REINTEGRAZIONE-PNG-AP-RHOD` (chiuso il 2026-07-20)
  **reintegrò deliberatamente** PNG e luoghi dell'AP originale — Guado di
  Drellin, secondo anello di Rethmar, Witchwood/Tiri Kitor, i Wyrmlord. Quel
  lavoro portò la campagna *verso* l'AP, non lontano.
- **arco 00** è impalcatura (tabelle di composizione degli eserciti, flusso di
  campagna): densità altissima ma volume trascurabile.

---

## 3. Cosa pesa davvero

### 3.1 Nomi propri di *Red Hand of Doom* — ~3.800 occorrenze

| Categoria | Termini e conteggi |
|---|---|
| **Personaggi** (~1.650) | Ghostlord 551 · Azarr Kul 340 · Wyrmlord 302 · Saarvith 221 · Koth 92 · Sertieren 54 · Ulwai 39 · Kharn 31 · Blackspawn 16 · Jorr 13 · Trellara 5 |
| **Luoghi** (~1.270) | Rhest 338 · Drellin 206 · Vraath 176 · Skull Gorge 159 · Elsir 134 · Brindol 109 · Tiri Kitor 103 · Witchwood 48 |
| **Fazione** (~880) | Red Hand 659 · Mano Rossa 225 |

### 3.2 Ambientazione WotC / Forgotten Realms — ~4.600 occorrenze

| Termine | Conteggio | |
|---|---:|---|
| **Moradin** | **1.502** | ⚠️ **il caso peggiore** |
| Faerûn / Faerun | 979 | |
| Thay | 338 | |
| Waterdeep | 284 | |
| Channathgate / Channath | 282 | |
| Cormyr | 252 | |
| Harper | 245 | |
| Zhentarim | 218 | |
| Dalelands | 188 | |
| Forgotten Realms | 157 | |
| Myth Drannor | 90 | · Sembia 73 |

**Perché Moradin è il problema serio, e non la Mano Rossa.** L'SRD 3.5 esclude
deliberatamente i nomi delle divinità: Moradin è Product Identity, non Open Game
Content. E questa è una campagna **nanica costruita su Moradin** — il Cuore di
Moradin, la Corona di Adamantio, la Forgia Eterna, il *Canto della Pietra e del
Fuoco*. Sostituirlo non è un find-and-replace: tocca la spina teologica della
storia, i nomi degli artefatti e il senso di metà delle scene.

Rinominare «Mano Rossa» costa un pomeriggio. Sostituire Moradin costa una
revisione narrativa.

---

## 4. Le tre vie, valutate

### 4.1 «Espansione per Red Hand of Doom» — ❌ **nessuna via**

Un'espansione *per* RHoD deve nominarlo: titolo, trama, cast, luoghi. È l'uso
derivativo che nessuna licenza copre:

- l'**OGL 1.0a** copre le *meccaniche* dichiarate Open Game Content. RHoD non è
  OGC: è un'avventura pubblicata, protetta come espressione;
- la **Community Use Policy di Paizo** è **esplicitamente non commerciale**, e
  comunque riguarda IP Paizo, non WotC;
- **DMs Guild** consente materiale in ambientazioni WotC, ma RHoD non è fra i
  contenuti licenziabili, ed è **solo 5e** (§4.3).

Non c'è un modo «più prudente» di farlo: la richiesta stessa è il problema.

### 4.2 Adventure Path **originale autonomo**, OGL 3.5 o PF1e — ✅ **la via**

Ambientazione tua, divinità tue, fazione tua. Le meccaniche 3.5 o PF1e restano
utilizzabili commercialmente sotto **OGL 1.0a** (testo della licenza + catena
Section 15). Per Pathfinder 1e esiste in più la **Compatibility License** di
Paizo, che concede di dire «compatible with Pathfinder» e di usare il logo di
compatibilità; nella versione attuale **non richiede più registrazione**, e i
prodotti PF1e continuano a viaggiare su OGL.

Vincolo di marchio, valido per entrambe: **«Dungeons & Dragons», «D&D» e il logo
d20 non sono usabili** — la d20 System Trademark License non è più disponibile.
Si comunica per compatibilità, con la formula ammessa dalla licenza scelta.

### 4.3 DMs Guild — ⚠️ risolve il problema sbagliato

È l'**unica** via legittima per tenere i Forgotten Realms in un prodotto
venduto. Ma: **solo 5e** (non 3.5, non PF1e), quota di ricavo alla piattaforma,
e si concede a WotC e agli altri autori una licenza sul proprio contenuto. E
**non** sblocca RHoD.

Quindi risolve l'ambientazione e non l'avventura — cioè il problema minore.

---

## 5. L'avvertenza che conta più di tutte

> **Rinominare è necessario e NON è sufficiente.**

Il criterio non è «ho cambiato i nomi», ma la **somiglianza sostanziale
dell'espressione protetta**: sequenza degli eventi, personaggi distintivi,
ambientazioni specifiche. Limare i numeri di serie non trasforma un'opera
derivata in un'opera originale.

**La buona notizia è che la misura dice che la tua struttura già non è quella di
RHoD.**

| | *Red Hand of Doom* | RumblingStone |
|---|---|---|
| Spina | Guado di Drellin → Vraath Keep → Skull Gorge → Witchwood/Rhest → **assedio di Brindol** → Fane di Tiamat | miniera → scala d'ossa → cittadella → **tomba di Belkram** → stanza runica → **Corona di Adamantio** → **portale della Forgia / piani elementali** → **Hammerfist** |
| Livelli | 5-10 | riscalata a **8+** |
| Antagonisti | Wyrmlord, Azarr Kul, culto di Tiamat | Il Collezionista, Sonjak, Therysol — **originali** |
| Motore | orologio militare: ritardare un'orda | artefatti e discesa: forgia, corona, piani |

Sono due avventure diverse. Le densità di §2 lo confermano: 0,3 e 1,1 occorrenze
ogni mille parole sono **una verniciatura di nomi**, non un impianto.

**L'eccezione è l'arco 09**, ed è un'eccezione per scelta deliberata (§2).

---

## 6-bis. ⚠️ CORREZIONE (2026-07-26, stessa giornata) — c'è una **seconda** fonte WotC

**La misura di §1-§5 cercava solo *Red Hand of Doom* e i toponimi dei Forgotten
Realms. Era incompleta.** Interrogando `campaign/lore/campaign-history.md` — cioè
la documentazione del repo stesso — emergono **altre quattro fonti di terzi
dichiarate, con tanto di numero di pagina**:

| Fonte | Dove è dichiarata | Riferimento |
|---|---|---|
| ***Expedition to Undermountain*** (WotC 2007) | Tana dei Minotauri · archi 02 · 03 · 04 | p.165 · p.123 · p.122 e p.140 · p.117 |
| ***Underdark*** sourcebook (WotC 2003) | Tana dei Minotauri · arco 01 | p.95 (Maur) · p.93 (Cristal Warriors) |
| ***Out of the Abyss*** (D&D 5e) | **Neverlight Grove** = la torre fungina, convertita in 3.5 | — |
| Lore FR / Salvatore | *Aegis Fang* — «originally Wulfgar's warhammer» | `campaign-artifacts.md` |
| ***Drow of the Underdark*** (WotC 2007) | **Gardens of Resplendent Hues** — il Giardino dove Hella ottiene il viaggio nel micelio | p.189 *(dichiarato dal DM il 2026-07-26; **0 occorrenze** nel repo)* |

**«Belkram» compare 232 volte in 49 file.** *Belkram's Fall* è una località di
Undermountain: **l'arco 04 è intitolato a un luogo altrui.**

### Densità di *Undermountain* per arco

| Arco | Parole | occorrenze | densità |
|---|---:|---:|---:|
| 06 — Stanza della Corona di Adamantio | 16.271 | 144 | **8,8** ⚠️ la più alta del repo |
| 00 — impalcatura | 7.750 | 10 | 1,2 |
| Bestiario | 14.398 | 15 | 1,0 |
| `campaign/` | 84.808 | 60 | 0,7 |
| 07 — Portale della Forgia | 151.588 | 36 | **0,2** |
| 04 · 08 · 09 | — | 0-5 | **0,0** |

### Cosa cambia nella conclusione

**Quello che avevo scritto**: «archi 04-08 = 252.111 parole, base vendibile».
**Corretto**: gli archi 02, 03, 04 sono **adattamenti dichiarati** di un altro
manuale WotC, e l'arco 06 ha la densità Undermountain più alta del repo. La
densità RHoD 0,0 di quegli archi era vera **e irrilevante**: misuravo la fonte
sbagliata.

| Arco | Parole | Esito **corretto** |
|---|---:|---|
| **07** — Portale della Forgia, piani elementali | **151.588** | ✅ RHoD 0,3 · UM 0,2 — **il corpo pulito più grande del repo** |
| **08** — Hammerfist | **81.422** | ✅ RHoD 1,1 · UM 0,0 — pulito |
| 06 — Corona di Adamantio | 16.271 | ⚠️ UM **8,8** — riscrittura o fuori |
| 04 — Tomba di Belkram | 2.830 | ⚠️ adattamento dichiarato **e intitolato** a un luogo WotC |
| 02 · 03 | (non scritti) | ⚠️ adattamenti dichiarati (p.123 · p.122/140) |
| 01 · 05 | (non scritti) | ⚠️ arco 01 cita *Underdark* p.93 |
| 09 | 195.739 | ❌ RHoD 5,3 |

**Base vendibile corretta: archi 07 + 08 ≈ 233.000 parole** — sempre due
manuali abbondanti, ma non 252.000 e non quelli che avevo indicato.

### Il rovescio della medaglia, ed è una buona notizia

**Gli archi 01-05 non sono scritti** (zero markdown: solo `.txt`, `.pdf`,
`.webp`, appunti). Quindi:

> **Il punto in cui è più economico diventare originali è esattamente quello che
> non esiste ancora.** Scrivere quegli archi *dalle fonti* aggiungerebbe
> derivazione dove oggi non ce n'è nel testo; scriverli **originali costa la
> stessa fatica** e produce materiale nato pulito.

Non è una scelta fra «bonificare» e «lasciar stare»: è una scelta su **come
scrivere qualcosa che va scritto comunque**.

---

## 6-ter. Cosa resta genuinamente originale

Al netto di tutte e cinque le fonti:

- **Il Collezionista** — rakshasa con un basilisco vincolato, pietrifica le
  vittime e ne vende le statue. Fugge dalla Tana dei Minotauri e diventa il
  villain ricorrente;
- **Sonjak**, matrona drow *architetto* — modifica lo **spazio** oltre che la
  struttura;
- **Therysol**, e la catena di artefatti (Corona di Adamantio, Bracieri Gemelli,
  Collana dei Semi Eterni, Anello dell'Illuminazione Caotica);
- l'**arco 07** per intero: portale, Forgia Eterna, piani elementali;
- **Hammerfist**;
- gli archi personali dei quattro PG — inclusa la rinuncia di Artemis alla
  classe di prestigio, e la morte di Hella.

È l'ossatura di un Adventure Path. Il problema non è la mancanza di materiale
originale: è che il materiale originale non è ancora stato **scritto** per le
parti 01-05, e che le parti scritte poggiano su ambientazione altrui.

---

## 6. Conclusione operativa

| Materiale | Parole | Esito |
|---|---:|---|
| ~~Archi 04-08~~ **Archi 07-08** | ~~252.111~~ **233.010** | ✅ **base vendibile** dopo sostituzione dell'ambientazione — vedi la **correzione di §6-bis** |
| Archi 01-05 (non scritti) + 06 | ~19.000 + da scrivere | 🟡 **da scrivere originali**: è il punto più economico in cui diventare puliti |
| Arco 09 | 195.739 | ⚠️ **triage**: riscrittura sostanziale, oppure **fuori dalla v1** |
| Arco 00 | 7.750 | 🔧 impalcatura: si rigenera |
| Campagna giocata (`campaign/`, `state.md`, log) | — | ❌ **resta privata**: è il diario del tavolo, non un prodotto |

**Il prodotto realistico non è «un'espansione di RHoD». È un Adventure Path
originale di ~250.000 parole**, con un impianto che non deve niente all'AP
originale se non l'ispirazione iniziale — che non è protetta.

Piano di attuazione: [`plans/PIANO-EDIZIONE-COMMERCIALE-AP-ORIGINALE.md`](../../plans/PIANO-EDIZIONE-COMMERCIALE-AP-ORIGINALE.md).
Decisione: [ADR-0018](../../plans/adr/ADR-0018-edizione-commerciale-ap-originale.md).

**Fonti consultate** per §4.2:
[Paizo Compatibility License](https://paizo.com/licenses/compatibility) ·
[Paizo Licenses](https://paizo.com/licenses) ·
[Compatibility License FAQ](https://paizo.com/licenses/compatibility/faq)
