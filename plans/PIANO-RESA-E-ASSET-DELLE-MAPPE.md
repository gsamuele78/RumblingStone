# PIANO — La resa e gli asset delle mappe, uguali su ogni macchina e per ogni categoria

> **Stato**: 🟡 in corso (2026-10-08), D1-D5 decise dal DM lo stesso giorno, D6-D8 aperte · **Classe**: C per R1-R3, G poi C per R4-R6
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

### R5 · Città, villaggi ed edifici da Watabou

`[engine: Sonnet · effort: medio · qualità: un'esportazione vera per tipo, importata, collaudata a zero errori, con il seme scritto]` · **C**

- `import_watabou.py` sa leggere i dungeon. Mancano le città (Medieval
  Fantasy City Generator), i villaggi e gli edifici (Dwellings), le cui mappe
  il generatore permette di usare *«as you like»*, anche commercialmente.
- Serve qualche esportazione JSON vera di ciascuno (D7): senza, l'importatore
  si scriverebbe su un formato indovinato.
- Le mappe importate escono con `@tipo tattica abitato` o `interni`.

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
| D6 | R4 | **Quali pacchetti di 2-Minute Tabletop, e dove stanno?** Proposta: si comincia con un pacchetto solo, quello dei dungeon; i PNG restano sulla macchina del DM (cartella ignorata da git) e il repo tiene solo la tabella `simbolo → file` e i crediti, perché un pacchetto pesa decine di MB |
| D7 | R5 | **Le esportazioni di Watabou da cui partire.** Servono una città, un villaggio e un edificio esportati in JSON dal DM, con il loro seme: l'importatore si scrive su file veri |
| D8 | R6 | **Quale regione inventata con Azgaar?** Proposta: nessuna finché un arco non ne chiede una; il lotto resta pronto |

<!-- eco: RESA-ASSET 2026-10-08 -->
- **Decise**: D1 i font dei volumi incorporati · D2 universali in casa e ripiego Noto · D3 il tema dipinto con 2-Minute Tabletop · D4 l'importatore Watabou · D5 Azgaar per le regionali
- **Aperte**: D6 quali pacchetti e dove stanno, D7 le esportazioni di Watabou, D8 quale regione
- **Cambiate**: D3, dove avevo sconsigliato il tema dipinto, e scipy (D17 di COLLAUDO-MAPPE), dove avevo proposto di non ammettere nessuna libreria
- **Dedotto da me**: che i nuovi universali siano solo i concetti che hanno lo stesso significato in ogni mappa (`🔺`, `🔷`), e che `💠` resti locale; che il ripiego Noto valga per le celle e non per le emoji ripetute nelle righe di legenda, che costerebbero 3,7 MB; che il corsivo dei font si lasci fuori per il peso; che il tema dipinto sia una seconda resa per i giocatori e non sostituisca la pergamena del DM

---

## Checklist di avanzamento

```
Fase A — Audit
☑ R0  librerie rimisurate, resa non uniforme misurata, asset e licenze (2026-10-08)

Fase S — Sviluppo
☑ R1  i font dei volumi dentro le mappe (2026-10-08: 47 SVG, +2,08 MB)
☑ R2  🔺 e 🔷 universali, glifi in casa (2026-10-08)
☑ R3  il ripiego Noto, 12 emoji locali (2026-10-08: 177 celle → 0)
□ R4  il tema dipinto (D6)
□ R5  città, villaggi, edifici da Watabou (D7)
□ R6  le regionali con Azgaar (D8)
□ R7  i residui: in V3 di COLLAUDO-MAPPE

Fase V — Validazione: la tabella di §4
```

> **Regola d'oro dei piani**: chi chiude un lotto aggiorna, nello stesso
> commit, questa checklist, la riga in `plans/INDEX.md` e una riga in
> `plans/CHANGELOG.md`.
