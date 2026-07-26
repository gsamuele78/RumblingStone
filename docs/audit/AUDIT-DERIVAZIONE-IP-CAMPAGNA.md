# AUDIT — Quanto di RumblingStone è derivato da *Red Hand of Doom*?

> **Domanda del DM (2026-07-26)**: *«tutta l'avventura è stata scalata all'8° livello,
> sono state introdotte molte parti non esistenti, PNG e villain non presenti
> nell'avventura principale, tutta la parte di Hammerfist, la discesa nell'Underdark…
> non saprei se è possibile venderlo come espansione per D&D 3.5 o su Paizo, se si
> cambiano l'ambientazione, i PNG e i luoghi.»*
>
> **Metodo**: misura, non impressione. Conteggio dei nomi propri di terzi su tutto
> il corpus, normalizzato sul volume di ogni arco.
> **Data**: 2026-07-26 · **Corpus**: `main` @ branch di analisi.
>
> ⚠️ **Questa non è consulenza legale.** È un'analisi documentale di conformità,
> come già il rapporto P2D del 2026-07-18. Una pubblicazione commerciale reale
> richiede un avvocato IP.

---

## 0. La risposta in tre righe

1. **Come «espansione per Red Hand of Doom»: no, per nessuna via.** Non esiste
   licenza che lo consenta (§4.1).
2. **Come Adventure Path originale autonomo: sì — e sei molto più vicino di
   quanto pensi.** ~252.000 parole hanno già densità RHoD ≈ **0,5 occorrenze
   ogni 1.000 parole** (§2).
3. **Il problema più grosso non è la Mano Rossa: è Moradin** — 1.502 occorrenze,
   e non è SRD (§3.2).

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

## 6. Conclusione operativa

| Materiale | Parole | Esito |
|---|---:|---|
| Archi 04-08 | **252.111** | ✅ **base vendibile** dopo sostituzione dello strato di ambientazione e del nome-fazione |
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
