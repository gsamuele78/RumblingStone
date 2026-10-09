# PIANO — La resa e gli asset delle mappe, uguali su ogni macchina e per ogni categoria

> **Stato**: 🟡 in corso (2026-10-08), D1-D8 decise dal DM il 2026-10-08, D9-D16 il 2026-10-09: le texture CC0 strada principale (R4-bis fatto, velatura 0,30), R4 una prova su una mappa (installatore fatto, aspetta il pacchetto), R5 parte da Dauth (sei mappe dell'assedio fatte), R6 in attesa · **Classe**: C per R1-R3, G poi C per R4-R6
> **Nasce da**: la richiesta del DM della sera del 2026-10-08, dopo la #227:
> *«verifica se ci sono progetti best community valuated che possono essere
> importati andando in deroga alla std lib e che migliorano o aiutano a creare
> asset e mappe per ogni categoria necessaria, in modo da avere gli asset per
> ogni necessità e le mappe migliori possibili, categorizzando bene,
> uniformando tutte le mappe, gli asset e la resa grafica delle mappe»*.
> **Decisione**: [ADR-0085](adr/ADR-0085-la-resa-delle-mappe-e-uguale-su-ogni-macchina.md) (accettata). Le dipendenze: [ADR-0084](adr/ADR-0084-il-collaudo-delle-mappe-e-uno-strumento-di-sviluppo.md) e il suo emendamento.
> **Misura riproducibile**: [`esperimenti/dipendenze-e-asset-2026-10/`](esperimenti/dipendenze-e-asset-2026-10/RISULTATI.md).

---

## §1 · Cosa ho guardato prima, e cosa questo piano NON rifà

Regola di apertura (ADR-0044): letti `plans/INDEX.md` e i piani e le ricerche
che parlano di mappe; `fase1.py` sui file toccati, nessun archivio fra i
bersagli (gli SVG di `_ARCHIVIO` si rigenerano come derivati, sul precedente
di ADR-0070).

| Documento | Cosa copre | Rapporto con questo piano |
|---|---|---|
| [RICERCA-GENERATORI-MAPPE](RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md) | il censimento di luglio: Watabou, Azgaar, mipui, 2-Minute Tabletop | la sua **Fase 3** (Azgaar per le regionali, la città di Watabou) è documentata e mai eseguita: la eseguono R5 e R6. Aveva scartato 2-Minute Tabletop; il DM lo riapre (R4) |
| [RICERCA-TOOL-ESTERNI-DM](RICERCA-TOOL-ESTERNI-DM-2026-08.md) | le tre soglie per far entrare un tool | ogni lotto qui le passa per scritto |
| [COLLAUDO-MAPPE](PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md) | il collaudo come grafo, il generatore di bozze | **non rifà niente** di quello: la categoria `@tipo` (D18) e scipy (D17) sono suoi |
| [EDITOR-VISUALE-MAPPE](PIANO-EDITOR-VISUALE-MAPPE-TATTICHE.md) | un editor a griglia | non si tocca |
| [LEVEL-DESIGN](PIANO-LEVEL-DESIGN-E-INQUADRATURA-SCENICA.md) | il disegno delle mappe e l'inquadratura | non si tocca: qui si parla di resa, non di disegno |
| `rumblingstone-art-direction` | le immagini, la hero map | il tema dipinto (R4) è per le mappe a griglia, non per la hero map |

## §2 · La misura, in breve

Tutto in [RISULTATI](esperimenti/dipendenze-e-asset-2026-10/RISULTATI.md);
qui i numeri che hanno deciso i lotti.

| Difetto | Prima | Dopo R1-R3 |
|---|---:|---:|
| celle disegnate con l'emoji del font di sistema | 177 in 7 SVG | **0** |
| font del testo | Georgia → DejaVu Serif in CI | EB Garamond e Cinzel incorporati |
| titoli fuori dal foglio | sì, sulle mappe strette | **0** (1 compresso con `textLength`) |
| mappe con la categoria dichiarata | 0 su 44 | **44 su 44** (D18) |
| peso dei 47 SVG | 3,77 MB | 5,85 MB |

## §3 · I lotti

### R0 · Audit ✅

Le cinque librerie scartate in V2-quater, rimisurate sul loro compito vero;
dove la resa non è uniforme; gli asset e i generatori della community con la
licenza letta alla fonte.

### R1 · I font dei volumi dentro le mappe ✅

`[engine: Opus, sessione principale · effort: alto · qualità: 0 testi al font di sistema nei 47 SVG; titoli dentro il foglio; validate_maps verde]` · **C**

`scripts/build_font_mappe.py` (fonttools, solo sviluppo) → `scripts/fonts/mappe/`;
il renderer incorpora i due woff2 e stringe i titoli con le larghezze di
`copertura.json`.

### R2 · Due universali nuovi ✅

`[engine: Opus · effort: medio · qualità: glifo diverso dai vicini (🔮, 🪨), verificato sul PNG]` · **C**

`🔺` stalagmite e `🔷` cristallo gigante in `legend.yaml`, glifi in casa.

### R3 · Il ripiego Noto per le emoji locali ✅

`[engine: Opus · effort: medio · qualità: build_emoji_noto --check verde; nessun id ripetuto in un SVG]` · **C**

`scripts/build_emoji_noto.py` → `scripts/emoji-noto/` (Apache-2.0, `CREDITS.md`).

### R4 · Il tema dipinto per le mappe dei giocatori

`[engine: Opus per le scelte, Sonnet per il codice · effort: alto · qualità: una mappa nel tema dipinto che il DM approva accanto alla pergamena; i crediti CC BY-NC nel colophon e nella mappa]` · **G → C**

- Una seconda resa dello stesso master con gli asset zenitali di
  2-Minute Tabletop (CC BY-NC 4.0), per la vista dei giocatori e i VTT. La
  pergamena resta la vista del DM; il master resta la griglia.
- Prima del codice: quali pacchetti, e se gli asset entrano nel repo o restano
  sulla macchina del DM (D6). Un pacchetto pesa decine di MB di PNG.
- Ogni asset per simbolo della legenda: una tabella `simbolo → file`, con la
  stessa regola di posa e lo stesso asse delle chiusure (ADR-0083).
- **Fatto il 2026-10-09** (D9): `scripts/asset_2mtt.py` e `dm.py asset
  installa|stato|controlla`. Il DM scarica lo zip, perché il sito manda i link
  per email anche a 0 $; l'installatore estrae in `asset-esterni/`, ignorata da
  git, e registra la categoria. La licenza (letta il 2026-10-09) divide i
  pacchetti in `base`, a offerta libera e CC BY-NC, e `premium`, senza
  licenza: `controlla` boccia la tabella che usa un premium. Guida:
  `docs/guides/GUIDA-MAPPE.md` §5.2. Resta la tabella sui nomi veri dei file,
  e la mappa di prova.

### R4-bis · Il tema texture CC0 (la strada principale)

`[engine: Opus · effort: medio · qualità: 11 texture CC0 con MD5 verificato; il tema texture di ogni mappa in rendered-texture/, allineato in validate_maps; colori leggibili come in pergamena]` · **C**

- Decise D13-D15 il 2026-10-09: texture CC0 di Poly Haven nei terreni,
  committate accanto alla pergamena, glifi in casa per gli oggetti.
- **Fatto il 2026-10-09**: `build_texture_cc0.py` (scarica, verifica l'MD5
  contro l'API, riduce a tessere webp da 256 px), il tema `texture` in
  `render_map_svg.py` (`--tema`, `--tutti-i-master`), `validate_maps` che
  pretende il gemello texture quando le texture ci sono, `dm.py asset texture`
  e `dm.py maps texture`, `doctor`, guida §5.1, test con texture finte.
- **Fatto il 2026-10-09, dal DM**: le 11 texture scaricate e verificate
  (90 KB di tessere) e i 53 SVG del tema, committati; la velatura tarata a 0,30
  (D16) guardando M7-D e il canyon di Hammerfist L1. Peso misurato: 7,6 MB
  per i 53 SVG del tema, contro i 6,2 MB della pergamena.
- **Dopo** (D15): gli oggetti di scena generati con l'IA locale.

### R4-ter · Gli oggetti di scena del tema texture (in una PR nuova, D18)

`[engine: Opus · effort: medio · qualità: ogni tessera da un modello CC0 con la sua impronta; stessa luce e scala; il DM approva una mappa]` · **C**

- Misurato il 2026-10-09: 46 simboli-oggetto usati su 61; i più presenti
  sono fuoco, rocce, fiamme e porte; i mobili sono rari (🪑 15 celle, 🛏 29).
- Poly Haven, 521 modelli CC0: rocce, alberi, statue, barili, casse,
  forziere, tavoli, panche, letto, librerie, vasi, candelabri. Mancano
  incudine, fontana, trono, altare, tenda, ossa, funghi: li copre Quaternius
  (Fantasy Props MegaKit, CC0, 60-70% gratuito; da verificare la licenza della
  parte a pagamento prima di usarlo).
- Script che scarica i modelli (il DM, come per le texture), Blender che li
  rende dall'alto con luce e scala fisse, tessere webp committate; il tema
  texture le usa al posto dei glifi. Restano glifi: fuoco ed effetti, porte,
  finestre e sbarre (ruotano con l'asse del muro).

### R5 · Città, villaggi ed edifici da Watabou

`[engine: Sonnet · effort: medio · qualità: un'esportazione vera per tipo, importata, collaudata a zero errori, con il seme scritto]` · **C**

- `import_watabou.py` sa leggere i dungeon. Mancano le città (Medieval
  Fantasy City Generator), i villaggi e gli edifici (Dwellings), le cui mappe
  il generatore permette di usare *«as you like»*, anche commercialmente.
- Serve qualche esportazione JSON vera di ciascuno (D7): senza, l'importatore
  si scriverebbe su un formato indovinato.
- Le mappe importate escono con `@tipo tattica abitato` o `interni`.
- **Fatto il 2026-10-09** (D10): le cinque carte dell'assedio di Dauth
  (`DAY3-CITY-SIEGE`) in sei griglie da contratto JSON, in
  `09_…/Mappe/dauth-assedio/` (il chiostro e il suo cunicolo sono due mappe
  collegate da `@collega`), collaudate a zero errori e zero avvisi. La pianta
  della città: la scheda `dauth-pianta.watabou.json` con seme e parametri, e
  `dm.py maps citta`, che ne ricava l'URL (`watabou_citta.py`). La rete di
  questo ambiente non raggiunge Watabou: l'esportazione la fa il DM.

### R6 · Le regionali con Azgaar

`[engine: Sonnet · effort: medio · qualità: un file .map committato come master, l'SVG esportato accanto, il seme scritto]` · **C**

- Azgaar Fantasy Map Generator (MIT) per una **regione inventata**: la
  geografia di Faerûn è canone e non si genera (`forgotten-realms-lore`).
- Quale regione è la D8.

### R7 · I residui, dichiarati

- Le emoji ripetute come testo nelle righe di legenda restano al font di
  sistema: incorporarle costerebbe 3,7 MB (ADR-0085).
- `☁` (71 celle) e `🔲` (15) hanno già un universale (`🌫`, `🟪`); `💠` resta
  locale. Cambiarle su mappe giocate è V3 di COLLAUDO-MAPPE, col DM.

## §4 · La validazione

| Lotto | Cosa lo dice chiuso |
|---|---|
| R1 | `build_font_mappe.py --check` e `validate_maps` verdi; nessun `<text>` delle mappe resta al font di sistema, salvo le emoji delle righe di legenda (R7) |
| R2 | `test_resa_mappe.py`: glifi diversi da `🔮` e `🪨`, nessuna chiave doppia nei dizionari del renderer |
| R3 | `build_emoji_noto.py --check` verde in `test_resa_mappe.py`; licenza e crediti nella cartella |
| R4 | il DM approva una mappa nel tema dipinto; il colophon porta il credito |
| R4-bis | `build_texture_cc0.py --check` e `validate_maps` verdi con le texture vere; il DM approva una mappa nel tema texture accanto alla pergamena |
| R5 | un'esportazione per tipo importata e collaudata a zero errori |
| R6 | il master `.map` committato e l'SVG rigenerabile |

---

## §7 · Le decisioni del DM

<!-- decisioni-dm: RESA-ASSET -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | R1 | ✅ **Decisa il 2026-10-08, sera, il DM: come proposto.** Era: **Il testo delle mappe come lo uniformo ai volumi?** Proposta: font OFL incorporati in sottoinsieme (+52 KB stimati a SVG; misurati 43) |
| ~~D2~~ | R2, R3 | ✅ **Decisa il 2026-10-08, sera, il DM: come proposto, tutte e due.** Era: **Le 177 celle a emoji di sistema?** Proposta: nuovi universali in casa dove il significato è uno, e il ripiego Noto per il resto. game-icons.net per le legende non scelto |
| ~~D3~~ | R4 | ✅ **Decisa il 2026-10-08, sera, il DM: sì.** Era: **Un tema «dipinto» con 2-Minute Tabletop?** Proposta mia: non raccomandata (lavoro grosso, deroga alla regola 5); il DM l'ha scelta |
| ~~D4~~ | R5 | ✅ **Decisa il 2026-10-08, sera, il DM: sì.** Era: **Un importatore Watabou per città, villaggi, edifici?** |
| ~~D5~~ | R6 | ✅ **Decisa il 2026-10-08, sera, il DM: sì.** Era: **Azgaar FMG per le regionali?** Solo per regioni inventate |
| ~~D6~~ | R4 | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: come proposto.** Era: **Quali pacchetti di 2-Minute Tabletop, e dove stanno?** Proposta: si comincia con un pacchetto solo, quello dei dungeon; i PNG restano sulla macchina del DM (cartella ignorata da git) e il repo tiene solo la tabella `simbolo → file` e i crediti, perché un pacchetto pesa decine di MB |
| ~~D7~~ | R5 | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: R5 si rimanda** finché non ci sono le esportazioni vere. Era: **Le esportazioni di Watabou da cui partire.** Servono una città, un villaggio e un edificio esportati in JSON dal DM, con il loro seme: l'importatore si scrive su file veri |
| ~~D8~~ | R6 | ✅ **Decisa il 2026-10-08, sera (terzo messaggio), il DM: nessuna per ora**, come proposto. Era: **Quale regione inventata con Azgaar?** Proposta: nessuna finché un arco non ne chiede una; il lotto resta pronto |
| ~~D9~~ | R4 | ✅ **Decisa il 2026-10-09, il DM: una prova su una mappa.** Era: **R4 come procede?** Il DM aveva chiesto a cosa serve e se valeva un download automatico; la misura: il pacchetto gratuito dei dungeon ha 131 tessere e copre circa 10-15 degli 86 simboli, i link arrivano per email dopo una cassa a 0 $, la rete dell'ambiente non raggiunge Dropbox. Proposta: un installatore (`dm.py asset installa <zip>`) con guida e controllo in `doctor`, poi una sola mappa di interni nel tema dipinto, da confrontare con la pergamena |
| ~~D10~~ | R5 | ✅ **Decisa il 2026-10-09, il DM: si parte da Dauth.** Era: **R5 come procede?** Proposta: la guida per esportare da Watabou la pianta di Dauth assediata, da usare come immagine; le cinque mappe tattiche dell'assedio (carte A-E di `DAY3-CITY-SIEGE`) col contratto JSON; l'importatore di città ed edifici solo se le esportazioni vere lo meritano. Sostituisce il «rimandato» di D7 |
| ~~D11~~ | R6 | ✅ **Decisa il 2026-10-09, il DM: resta in attesa**, come proposto. La Cannath Vale è la Elsir Vale di *Red Hand of Doom* rinominata: è canone e non si genera. Nessun codice finché un arco non porta i PG in una regione inventata |
| ~~D12~~ | R4 | ✅ **Risposta del DM il 2026-10-09: al tavolo usa Foundry.** Era: **Usi un VTT?** Decide il valore di R4: la resa dipinta va nell'export UVTT come immagine di sfondo |
| ~~D13~~ | R4-bis | ✅ **Decisa il 2026-10-09, il DM: sì, CC0 principale**, come proposto. Era: **Le texture CC0 (Poly Haven, ambientCG) diventano la strada principale per mappe più ricche, e 2-Minute Tabletop un extra opzionale solo per il tavolo?** Il DM aveva chiesto una strada senza problemi di licenza; le licenze lette alla fonte: Poly Haven e ambientCG CC0 1.0 |
| ~~D14~~ | R4-bis | ✅ **Decisa il 2026-10-09, il DM: committate accanto alla pergamena**, non come proposto. Era: **Le mappe con texture dove finiscono?** Proposta: solo in locale. Scelto: un secondo SVG per ogni mappa in `rendered-texture/`, controllato da `validate_maps`; stima +2,3 MB sui 50 SVG |
| ~~D15~~ | R4-bis | ✅ **Decisa il 2026-10-09, il DM: glifi ora, IA locale dopo.** Era: **Gli oggetti di scena da dove vengono?** I glifi in casa restano sopra le texture; un lotto futuro genera oggetti zenitali con ComfyUI e pesi a licenza permissiva (ADR-0019), col gate di rifiuto di `rumblingstone-art-direction` |
| ~~D16~~ | R4-bis | ✅ **Decisa il 2026-10-09, il DM: velatura 0,30**, come proposto, dopo il confronto 0,45 / 0,30 / 0,20 sulle texture vere (M7-D per gli interni, Hammerfist L1 per l'esterno). Era: **Quale velatura per il tema texture?** A 0,45 erba e sentiero sembravano tinte piatte; a 0,20 muri e pavimenti degli interni si avvicinavano di tono |
| ~~D17~~ | R4-ter | ✅ **Decisa il 2026-10-09, il DM: modelli 3D di Poly Haven e Quaternius**, non come proposto (solo Poly Haven). Era: **Gli oggetti di scena nel tema texture da dove vengono?** Modelli 3D CC0 renderizzati dall'alto con Blender in tessere webp, solo per il tema texture; Quaternius (Fantasy Props MegaKit, CC0, solo la parte gratuita) per ciò che Poly Haven non ha. Sostituisce l'IA locale di D15 |
| ~~D18~~ | R4-ter | ✅ **Decisa il 2026-10-09, il DM: in una PR nuova, dopo il merge della #227**, non come proposto (nella #227) |

<!-- eco: RESA-ASSET 2026-10-08 -->
- **Decise**: D1 i font dei volumi incorporati · D2 universali in casa e ripiego Noto · D3 il tema dipinto con 2-Minute Tabletop · D4 l'importatore Watabou · D5 Azgaar per le regionali
- **Aperte**: D6 quali pacchetti e dove stanno, D7 le esportazioni di Watabou, D8 quale regione
- **Cambiate**: D3, dove avevo sconsigliato il tema dipinto, e scipy (D17 di COLLAUDO-MAPPE), dove avevo proposto di non ammettere nessuna libreria
- **Dedotto da me**: che i nuovi universali siano solo i concetti che hanno lo stesso significato in ogni mappa (`🔺`, `🔷`), e che `💠` resti locale; che il ripiego Noto valga per le celle e non per le emoji ripetute nelle righe di legenda, che costerebbero 3,7 MB; che il corsivo dei font si lasci fuori per il peso; che il tema dipinto sia una seconda resa per i giocatori e non sostituisca la pergamena del DM
- **Decise** (terzo messaggio): D6 un pacchetto solo, quello dei dungeon, con i PNG fuori dal repo · D7 R5 rimandato finché non ci sono esportazioni vere · D8 nessuna regione per ora
- **Aperte** (terzo messaggio): nessuna
- **Dedotto da me** (terzo messaggio): che R4 non parta finché il DM non ha scaricato il pacchetto: la tabella `simbolo → file` si scrive sui nomi veri dei file, non su nomi indovinati

<!-- eco: RESA-ASSET 2026-10-09 -->
- **Decise**: D9 R4 come prova su una mappa, con l'installatore · D10 R5 a partire da Dauth · D11 R6 in attesa · D12 il DM usa Foundry
- **Aperte**: nessuna
- **Cambiate**: D7, da «R5 rimandato» a «R5 parte da Dauth»
- **Dedotto da me**: che l'installatore non scarichi niente da solo, perché i link del pacchetto arrivano per email dopo la cassa e la licenza chiede di mandare chi vuole i file al sito; che le cinque mappe dell'assedio stiano in `Mappe/` dell'arco 09 e le prenda il futuro `ARC09-DEF-05` di MASTER-DEF, senza scrivere il master qui; che la pianta della città resti un'immagine esportata da Watabou e non diventi una griglia
- **Decise** (secondo messaggio): D13 le texture CC0 strada principale, 2-Minute Tabletop extra opzionale · D14 il tema texture committato accanto alla pergamena · D15 glifi ora, oggetti generati con l'IA locale in un lotto futuro
- **Aperte** (secondo messaggio): nessuna
- **Cambiate** (secondo messaggio): D14, dove avevo proposto il tema texture solo in locale; e R4, che da strada principale diventa un extra per il tavolo
- **Dedotto da me** (secondo messaggio): che le texture vengano da Poly Haven sola, perché ha un'API con l'MD5 di ogni file (ambientCG resta ammessa, non usata); che il bosco fitto, l'acqua, la lava e i pilastri restino vettoriali; che il muro scelga roccia o muratura dall'ambiente di `@tipo`; che il tema texture diventi obbligatorio per `validate_maps` solo dopo il commit delle texture
- **Decise** (terzo messaggio): D16 la velatura 0,30, scelta guardando le texture vere
- **Aperte** (terzo messaggio): nessuna
- **Dedotto da me** (terzo messaggio): che il peso vada riscritto con la misura vera: i 53 SVG del tema texture pesano 7,6 MB, contro i 6,2 MB della pergamena; la stima di +2,3 MB contava solo le texture e non il resto di ogni SVG
- **Decise** (quarto messaggio): D17 gli oggetti di scena del tema texture dai modelli 3D CC0 di Poly Haven e Quaternius · D18 il lotto in una PR nuova dopo la #227
- **Aperte** (quarto messaggio): nessuna
- **Cambiate** (quarto messaggio): D15, l'IA locale per gli oggetti, sostituita da D17; D17 aggiunge Quaternius alla proposta; D18 sposta il lotto fuori dalla #227
- **Dedotto da me** (quarto messaggio): che Quaternius si usi solo per i simboli che Poly Haven non copre, e solo nella parte gratuita, dopo aver letto se la licenza CC0 vale anche per la parte a pagamento; che fuoco, effetti, porte, finestre e sbarre restino glifi

---

## Checklist di avanzamento

```
Fase A — Audit
☑ R0  librerie rimisurate, resa non uniforme misurata, asset e licenze (2026-10-08)

Fase S — Sviluppo
☑ R1  i font dei volumi dentro le mappe (2026-10-08: 47 SVG, +2,08 MB)
☑ R2  🔺 e 🔷 universali, glifi in casa (2026-10-08)
☑ R3  il ripiego Noto, 12 emoji locali (2026-10-08: 177 celle → 0)
□ R4  il tema dipinto: una prova su una mappa (D9); ☑ installatore, `dm.py asset`, doctor e guida (2026-10-09) · □ la tabella simbolo → file e la mappa di prova, quando il DM ha scaricato il pacchetto base
□ R4-bis il tema texture CC0 (D13-D16): ☑ script, tema, gate e guida · ☑ le 11 texture scaricate dal DM e i 53 gemelli committati (7,6 MB) · ☑ la velatura tarata a 0,30 (D16) (2026-10-09) · ~~gli oggetti con l'IA locale (D15)~~, sostituita da R4-ter (D17)
□ R4-ter gli oggetti di scena dai modelli 3D CC0 (D17), in una PR nuova dopo la #227 (D18)
□ R5  Watabou, a partire da Dauth (D10): ☑ le mappe dell'assedio, cinque carte in sei griglie collaudate a zero (2026-10-09) · ☑ la scheda e `dm.py maps citta` per la pianta · □ la pianta esportata dal DM · □ l'importatore, solo con esportazioni vere
□ R6  le regionali con Azgaar: in attesa (D8, D11), nessun codice
□ R7  i residui: in V3 di COLLAUDO-MAPPE

Fase V — Validazione: la tabella di §4
```

> **Regola d'oro dei piani**: chi chiude un lotto aggiorna, nello stesso
> commit, questa checklist, la riga in `plans/INDEX.md` e una riga in
> `plans/CHANGELOG.md`.
