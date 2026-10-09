# ADR-0085 — La resa delle mappe è uguale su ogni macchina

- **Stato**: **accettata**; R1-R3 attuati il 2026-10-08, R4 deciso e in attesa del pacchetto dei dungeon, R5 e R6 rimandati (il DM, il 2026-10-08, sera: D1-D8 di [PIANO-RESA-E-ASSET-DELLE-MAPPE](../PIANO-RESA-E-ASSET-DELLE-MAPPE.md))
- **Data**: 2026-10-08
- **Decisori**: DM (Gianfranco Samuele), agente
- **Rapporti**: emenda la regola 5 di `rumblingstone-mapmaking` («nessun file di terzi»); segue [ADR-0005](ADR-0005-confini-ip-uso-non-commerciale.md) per le licenze e [ADR-0020](ADR-0020-edizione-da-stampa-su-un-secondo-binario.md) per i font nel repo; legge la legenda di [ADR-0048](ADR-0048-legenda-funzionale-fonte-unica.md); le dipendenze di sviluppo sono quelle di [ADR-0084](ADR-0084-il-collaudo-delle-mappe-e-uno-strumento-di-sviluppo.md)

## Contesto

Il DM ha chiesto *«asset e mappe per ogni categoria necessaria, uniformando
tutte le mappe, gli asset e la resa grafica»*. La misura del 2026-10-08
([RISULTATI](../esperimenti/dipendenze-e-asset-2026-10/RISULTATI.md) §5) ha
trovato tre punti in cui la stessa mappa cambiava faccia da una macchina
all'altra, o non aveva quella dei volumi:

- **177 celle in 7 SVG** disegnate con l'emoji del font di sistema: i simboli
  che una mappa dichiara nella sua riga `LEGENDA` e che la legenda universale
  non conosce;
- **il testo** chiedeva Georgia, che su Linux e in CI diventa DejaVu Serif,
  mentre i volumi usano EB Garamond e Cinzel, già nel repo con licenza OFL;
- **nessuna categoria**: 0 mappe su 44 dichiaravano il loro tipo.

Gli 84 simboli universali invece erano già tutti disegnati in casa.

La ricognizione degli asset della community (stessa cartella, §6) ha letto
la licenza di ogni progetto alla fonte. Una sola libreria di asset zenitali
dipinti è usabile (2-Minute Tabletop, CC BY-NC 4.0). Due fonti vettoriali
sono permissive: Noto Emoji, Apache-2.0; game-icons.net, CC BY 3.0, già nel
repo per gli stemmi del Palio. I generatori di Watabou e di Azgaar producono
dati, non arte.

## Decisione

1. **I font dei volumi viaggiano dentro ogni mappa.** `build_font_mappe.py`
   ricava da `scripts/fonts/` due sottoinsiemi woff2 a peso fisso (EB Garamond
   regolare 18 KB, Cinzel grassetto 14 KB), e il renderer li incorpora in
   base64. Testo in EB Garamond, ogni elemento in grassetto in Cinzel. Il
   titolo si stringe se non entra nel foglio, e sotto gli 11 px si comprime
   con `textLength`; le larghezze dei caratteri vengono dal font stesso
   (`copertura.json`), quindi il renderer resta in libreria standard.

2. **Ogni simbolo locale ha un ripiego uguale ovunque.** Le emoji che una
   mappa dichiara e la legenda universale non conosce si disegnano con l'SVG
   di Noto Emoji (Apache-2.0, commit fissato), incorporato come `<symbol>`
   una volta per mappa. `build_emoji_noto.py --check` boccia un'emoji locale
   senza il suo file. Le emoji ripetute come testo nelle righe di legenda
   restano al font di sistema: incorporarle tutte costerebbe 3,7 MB.

3. **Un concetto diventa universale solo se vuole dire la stessa cosa in ogni
   mappa che lo usa.** `🔺` (stalagmite) e `🔷` (cristallo gigante) entrano,
   disegnati in casa. `💠` resta locale: nel corpus vuol dire due cose
   diverse. `☁` e `🔲` hanno già il loro universale (`🌫`, `🟪`) e il cambio
   sulle mappe giocate è una decisione del DM, mappa per mappa (V3).

4. **La regola 5 di `rumblingstone-mapmaking` diventa una regola di licenza.**
   Un file di terzi entra in una mappa solo se:
   - la sua licenza permette la ridistribuzione e non la impone al resto:
     CC0, CC BY, Apache-2.0, OFL, MIT; CC BY-NC è ammessa perché ADR-0005
     esclude già l'uso commerciale;
   - nella sua cartella ci sono la licenza e un `CREDITS.md` con autore e
     modifiche, come per gli stemmi del Palio.

   CC BY-SA e GPL restano fuori: passerebbero agli SVG e ai PDF di mappe
   derivate da *Red Hand of Doom*, che non si possono rilicenziare.

5. **Ogni mappa dichiara la sua categoria** (`@tipo`, D18 di COLLAUDO-MAPPE),
   da un elenco solo in `dmcore/legenda.py`. È la chiave con cui i lotti
   R4-R6 sceglieranno corredo e generatore.

6. **Il tema dipinto, i generatori di città ed edifici, le regionali** entrano
   come lotti di [PIANO-RESA-E-ASSET-DELLE-MAPPE](../PIANO-RESA-E-ASSET-DELLE-MAPPE.md)
   (R4-R6), ciascuno con le sue decisioni aperte. La pergamena resta la vista
   del DM e il master resta la griglia.

## Alternative scartate

| Alternativa | Perché no |
|---|---|
| Lasciare i font al sistema | la stessa mappa aveva due facce, e nessuna era quella dei volumi |
| Incorporare i tre font variabili interi | 96 KB a mappa, 128 KB in base64; i pesi fissi senza corsivo ne pesano 32 |
| Noto anche per le emoji delle righe di legenda | 3,7 MB in più su 5,8 |
| game-icons.net per i simboli locali | vista frontale o di profilo, non zenitale; e credito per autore in ogni mappa. Resta disponibile per le legende, sotto la regola del punto 4 |
| OpenMoji | CC BY-SA 4.0 |
| Forgotten Adventures | la licenza vieta la ridistribuzione |
| Rendere universale anche `💠` | nelle due mappe vuol dire «base corrosa del pilastro» e «Cristallo Vivente» |

## Le conseguenze

**Cosa si ottiene.** Le 47 mappe hanno la faccia dei volumi su ogni macchina,
in CI e nel PDF. Le celle a emoji di sistema passano da 177 a 0, e nessun
titolo esce più dal foglio. Un simbolo nuovo ha una strada scritta: in casa se
il significato è uno, Noto se è locale, un asset di terzi solo con la licenza
giusta.

**Quello che si paga.**

- **+2,08 MB** sui 47 SVG (da 3,77 a 5,85), circa 43 KB a mappa per i font.
- Tutti i 47 SVG rigenerati in un commit, compresi quelli delle mappe giocate
  e dell'archivio: master intatti, resa diversa. Sulla mappa 1 dell'atlante
  ARC-07 la riga di legenda di `🔷` passa da «Cristallo Gigante (copertura
  totale, indistruttibile)» alla voce universale «Cristallo gigante
  (copertura totale)»; «indistruttibile» resta nel master.
- `🔷` blocca la vista, quindi l'export UVTT lo fa diventare un muro: nella
  foresta di cristalli (DEF-1 e atlante, mappa 1) i 25 cristalli fermano la
  vista anche in Foundry, come dice la legenda locale («copertura totale»).
- Cinzel è in maiuscoletto: i titoli delle mappe cambiano forma, come i
  capitoli dei volumi.
- Due script nuovi da tenere: `build_font_mappe.py` (con fonttools, solo per
  rigenerare) e `build_emoji_noto.py` (rete solo per scaricare).

**Il difetto trovato per strada.** Il glifo del cristallo gigante è stato
scritto con la chiave `pr_crystal`, che esisteva già (il glifo di `🔮`): un
dizionario Python con due chiavi uguali tiene l'ultima senza dire niente, e il
cristallo magico di tutte le mappe aveva cambiato faccia. L'ha visto solo il
PNG. Adesso `test_resa_mappe.py` boccia una chiave ripetuta nei dizionari del
renderer.

---

## Emendamento del 2026-10-09: le mappe più ricche passano dalle texture CC0

**Stato**: accettato dal DM il 2026-10-09 (D13-D15 di
[PIANO-RESA-E-ASSET](../PIANO-RESA-E-ASSET-DELLE-MAPPE.md)).

**Contesto.** Il tema dipinto con 2-Minute Tabletop (R4) non si può
pubblicare: i contenuti base sono CC BY-NC 4.0, i premium non hanno licenza
fuori dal tavolo, anche se pagati (pagina «General Licensing and Attribution»,
letta il 2026-10-09). Il DM ha chiesto una strada senza questo problema, con i
progetti gratuiti meglio valutati dalla community.

**Le licenze lette alla fonte, lo stesso giorno.**

| Fonte | Licenza | Esito |
|---|---|---|
| Poly Haven (texture) | CC0 1.0: uso commerciale, ridistribuzione, nessun credito obbligatorio | **entra**: 11 texture, con l'MD5 che l'API dichiara |
| ambientCG | CC0 1.0 | ammessa, non usata: Poly Haven basta e ha un'API con le impronte |
| Dungeon Crawl Stone Soup (OpenGameArt) | «use freely, no attribution», taggata CC0 | non usata: pixel art 32×32 in tre quarti, stile diverso |
| 2-Minute Tabletop | CC BY-NC (base), nessuna (premium) | resta un extra opzionale per il tavolo del DM |

**Decisione.**

1. **Il tema texture** è la seconda resa di ogni mappa: i terreni si riempiono
   con le texture CC0, velate del colore della pergamena (0,30, tarata dal DM con D16), e
   contorni, ombre e glifi restano gli stessi. Il muro sceglie roccia o
   muratura dall'ambiente di `@tipo`. Bosco fitto, acqua, lava, fogna, vuoto,
   zona letale e pilastri restano vettoriali.
2. **Gli SVG del tema stanno nel repo**, in `rendered-texture/` accanto a
   `rendered/` (D14, contro la proposta di tenerli in locale), e
   `validate_maps` li rigenera per confronto come la pergamena, una volta che
   le texture sono committate.
3. **Le texture si scaricano una volta** (`build_texture_cc0.py`, Pillow) e si
   committano in `scripts/texture-cc0/` con l'indice; il renderer resta in
   libreria standard e legge solo i webp.
4. **Gli oggetti di scena restano i glifi in casa**; un lotto futuro li genera
   con l'IA locale e pesi a licenza permissiva (D15, ADR-0019).

**Quello che si paga.** Misurato il 2026-10-09 dopo il download del DM: le 11
tessere pesano 90 KB, e i 53 SVG del tema **7,6 MB**, contro i 6,2 MB della
pergamena: il peso delle mappe nel repo più che raddoppia. La stima fatta prima,
+2,3 MB, contava solo le texture incorporate e non il resto di ogni SVG: era
sbagliata per difetto. La rete dell'ambiente dell'agente non raggiunge Poly
Haven: le texture le ha scaricate il DM.
