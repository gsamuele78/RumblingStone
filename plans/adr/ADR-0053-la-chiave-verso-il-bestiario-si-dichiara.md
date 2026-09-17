# ADR-0053 — La chiave verso il Bestiario si dichiara, non si deduce

- **Stato**: accettata (2026-09-17), **attuata**
- **Decide**: come si passa dallo stato vivo di un PNG alla sua scheda
- **Chiude**: **D17** (i due villain senza scheda: si scrivono, si contano o
  escono da §3?)
- **Segue**: ADR-0052, che aveva dichiarato questo limite e rimandato qui

---

## Contesto

ADR-0052 ha chiuso la domanda di cosa è dato e cosa è prosa, e ha lasciato
scritto il proprio limite: *«un LLM che parte dallo stato vivo e vuole la scheda
di un PNG non ha una chiave»*. La misura di allora diceva 11 villain su 13 e 23
righe di §4 su 31 agganciabili per somiglianza di stringa.

**Rimisurando prima di costruire, quel numero si è rivelato ottimista in un modo
che conta più del numero.** Il primo confronto era severo — pretendeva tutte le
parole del nome della cartella — e produceva solo silenzi. Allentandolo, le
righe agganciate salgono; ma le nuove risposte sono **sbagliate**:

| Riga in `state.yaml` | Cosa aggancia un confronto permissivo | |
|---|---|---|
| `Zalkatar (Illithid Warlock)` | `Xal_thor` **oppure** `Zarim` | due illithid diversi |
| `Wyrmlord Saarvith + Regiarix` | `Wyrmlord_Karruk` | un altro wyrmlord |
| `Zalkatar (via Sethrax)` | `Sethrax_il_Velato` | ma chi *sa* è Zalkatar: il tramite non è il soggetto |
| `Druid Circle of the Sacred Forest` | `druid-bear-ally-cr12.md` | l'orso alleato di un druido |

🔴 **È la scoperta che decide l'architettura.** Un matcher più generoso non
riduce l'ignoranza: la **traveste**. Trasforma «non lo so» in un errore sicuro
di sé, e il quarto caso mostra perché è la forma peggiore — «Sethrax» è un PNG
che esiste davvero, quindi il collegamento sbagliato supera qualunque controllo
di esistenza. È esattamente il modo in cui sbaglia un LLM.

Una seconda cosa emersa misurando: il `Bestiario/` **non ha un file per
persona**. La scheda canonica sta in `X/X/X.md` o `X/X.md`, il `*-crN.md` in
cima è spesso un puntatore, e alcune persone (Brenna Sorvane, Sertieren, Norro
Wiston) vivono come **sezione dentro un file di gruppo**. Nessuna regola di
derivazione dal nome può sapere questo.

## Decisione

**Una sezione `png` in `campaign/state.yaml`: l'anagrafica, con la chiave
dichiarata.** Ventotto voci, una per soggetto nominato in §3 o §4:

```yaml
- id: sonjak                      # chiave stabile
  nome: Sonjak (Matrona Sajak)    # nome canonico
  tipo: persona                   # persona | gruppo | divinita
  scheda: Bestiario/villain/Sonjak/Sonjak.md
```

E `png_id` sulle righe di §3 (13) e §4 (31), che vi puntano.

Tre regole la tengono vera, e sono tutte provate a mordere:

- **R10** — ogni `png_id` risolve a una voce, gli `id` sono unici, e un
  `scheda: null` porta sempre il proprio `perche_senza_scheda`. Un id rotto
  sarebbe invisibile: il nome per esteso resta leggibile nella riga, quindi il
  documento *sembra* sano e solo la macchina inciampa.
- **R11** — ogni `scheda` dichiarata punta a un file che **esiste**. È ciò che
  rende la chiave una chiave: senza, sarebbe una stringa plausibile, cioè la
  stessa cosa di prima scritta meglio. Le schede si spostano e si rinominano;
  questa regola se ne accorge il giorno stesso, non sei settimane dopo al tavolo.
- **R12** — le voci senza scheda si **contano** a ogni esecuzione, come R7 (il
  tempo non dichiarato) e R8 (gli stati ignoti). Forma di ADR-0041.

### D17 — i quattro buchi, e cosa se ne fa

Il DM aveva tre strade: scrivere le schede mancanti, contarle, o togliere le
righe da §3. **Contarle**, e per un motivo preciso: scrivere due statblock è
canone, e un lotto di infrastruttura non scrive canone; togliere da §3 due
villain con clock in corsa (Zalkatar a 6/8, Saarvith a 3/8) sarebbe **perdere
stato vivo** per far tornare un conto.

| | Perché non ha scheda |
|---|---|
| `zalkatar` | compare solo citato in `Tempestas.md`, `Xal_thor.md`, `Sethrax.md` |
| `saarvith-regiarix` | citati solo nei documenti di Rethmar |
| `cerchio-sacro` | esistono i singoli druidi, non il Cerchio come gruppo |
| `lathander-mask` | due divinità, non una creatura: una scheda del Bestiario non sarebbe la cosa giusta |

I primi due sono lavoro di contenuto che aspetta il DM. Gli altri due sono
**buchi corretti**: nessuna scheda è la risposta giusta, e dirlo vale più che
inventare un rimando.

## Alternative scartate

| | Perché no |
|---|---|
| **Derivare la scheda dal nome a ogni lettura** | È la cosa che questo ADR esiste per non fare. Quattro errori su quattro casi difficili, e il peggiore punta a un PNG reale |
| **`scheda` direttamente sulle righe di §3 e §4** | Tre persone compaiono in due righe di §4 (Sonjak, Varis, Conte Valerius) e quattro anche in §3: il puntatore finirebbe in due o tre posti, che divergono alla prima rinomina |
| **Un `id` derivato dal nome con uno slugger** | «Zin'thara Vel'Ryn «la Voce di Ragnatela»» e «Wyrmlord Saarvith + Regiarix» non hanno uno slug ovvio, e cambiare il nome visualizzato cambierebbe la chiave. L'`id` è stabile *perché* è scritto a mano |
| **Portare `stato` nell'anagrafica adesso** | Sarebbe il refactor giusto (vedi sotto), ma metterebbe `stato` in due posti durante la migrazione — il difetto dei due master. Si fa quando l'anagrafica ha dimostrato di reggere |

## Conseguenze

**Quel che si guadagna.** Da `state.yaml` alla scheda in un passo, verificato:
un algoritmo segue `png_id` → `png[].scheda` e apre un file che c'è. E l'errore
di attribuzione più insidioso — la conoscenza di Zalkatar messa in conto a
Sethrax — è **scritto**, quindi non si ripete.

**Quel che si perde.** Ventotto voci da tenere vere, e un `png_id` in più su 44
righe. Il costo si paga a ogni PNG nuovo: prima si dichiara, poi si nomina.

⚠️ **L'anagrafica è strato macchina e non si vede in `state.md`.** È ADR-0052
applicato a se stesso: un `png_id` non spiega niente a chi legge, quindi non ha
motivo di comparire nella vista. `render_state --check` resta byte-identico
dopo tutto il lotto, ed è la prova che il DM non paga niente per questa chiave.

🔵 **Il passo successivo, già visibile.** Con l'anagrafica in piedi, `stato` e
`reversibile` possono **salire** dalle righe di §3 all'anagrafica — e allora
anche i PNG di §4 ne avranno uno, che è la cosa che D16 aveva chiesto e che si
era dovuta rimandare perché tre righe di §4 non sono persone. Il `tipo`
(`persona` · `gruppo` · `divinita`) esiste già per quel giorno: dice a chi uno
stato vivo si applica e a chi no.

## Riferimenti

- `plans/PIANO-RIPRESA-PR-ABBANDONATE.md` §4.8.10 — il lotto, misure e validazione
- [ADR-0052](ADR-0052-cosa-e-dato-e-cosa-e-prosa.md) — il criterio, e il limite che questo chiude
- [ADR-0050](ADR-0050-stato-di-campagna-dati-e-prosa.md) — un master, mai due
- `scripts/validate_state.py` (R10, R11, R12) · `scripts/tests/test_anagrafica_png.py`
