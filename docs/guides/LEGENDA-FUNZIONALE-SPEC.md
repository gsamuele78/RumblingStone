# Legenda funzionale — specifica completa (core neutro + profili 3.5 / PF1e / 5e)

> **Cos'è**: la specifica normativa della legenda dei simboli come **dato**
> interrogabile, e la sua traduzione nei tre sistemi di regole che il prodotto
> deve supportare (D&D 3.5, Pathfinder 1e, D&D 5e).
> **Perché**: oggi la funzione di gioco di un simbolo vive in prosa dentro
> un'etichetta e in `set` cablati in due script, **già divergenti**
> (`docs/audit/AUDIT-LEVEL-DESIGN-E-INQUADRATURA.md` §2.1).
> **Decisioni**: [ADR-0014](../../plans/adr/ADR-0014-legenda-funzionale-fonte-unica.md)
> (fonte unica) · [ADR-0016](../../plans/adr/ADR-0016-profili-regole-multisistema.md)
> (profili multi-sistema e confini di licenza).
> **Attuazione**: lotti A1 e P3 di
> [`PIANO-PRODOTTO-TOOLKIT-VENDIBILE`](../../plans/PIANO-PRODOTTO-TOOLKIT-VENDIBILE.md).
> **Data**: 2026-07-26 · **Stato**: specifica proposta, gate DM.

---

## 1. Il principio: la geometria è neutra, i numeri no

Un simbolo porta **due informazioni indipendenti**, e la confusione fra le due
è la causa di tutti i difetti misurati:

| | Cos'è | Dove vive | Cambia con il sistema? |
|---|---|---|---|
| **Render** | come si disegna (pattern, colore, prop) | `legend.yaml` → `render` | **no** |
| **Funzione** | cosa fa nello spazio (blocca? copre? a che quota?) | `legend.yaml` → `function` | **no** |
| **Numeri di gioco** | +4 CA · 20% · ×2 movimento · CD 15 | `rules/<sistema>.yaml` | **sì** |

**La regola**: `legend.yaml` non contiene **nessun numero di gioco**. Una roccia
«dà copertura parziale» — che poi valga +4 CA in 3.5, +4 CA in PF1e o +2 CA in 5e
è affare del profilo. È ciò che permette di supportare tre sistemi senza tre
legende, e ciò che tiene i vincoli OGL confinati a un file solo (§5).

---

## 2. Lo schema neutro di `function`

```yaml
function:
  blocks_movement: bool          # si può attraversare la cella?
  blocks_sight: bool             # interrompe la linea di vista?
  blocks_line_of_effect: bool    # interrompe la linea d'effetto (magia)
  cover: none | half | three_quarters | total
  obscurement: none | light | heavy
  move_cost: 1 | 2 | 4           # moltiplicatore sul costo del quadretto
  elevation_m: number            # quota della cella (0 = piano di riferimento)
  climb: none | easy | moderate | hard | sheer
  hazard: null | {kind: fire|cold|acid|electric|fall|drown|magic,
                  severity: minor|major|lethal}
  light: null | {radius_m: number, color: "rrggbb"}
  destructible: bool
  nameable: bool                 # può fare da landmark citabile al tavolo (M8)
  provides_concealment_to_prone: bool   # erba alta, macerie basse
```

**Note di progetto, ciascuna con un motivo:**

- **`cover` ha quattro valori, non tre.** La bozza iniziale di ADR-0014 usava
  `none|half|full`: non basta. 3.5 e PF1e distinguono copertura (+4) da copertura
  **migliorata** (+8); 5e distingue metà (+2) da tre quarti (+5). Servono
  `half` e `three_quarters` separati, oltre a `total`.
- **`blocks_sight` e `blocks_line_of_effect` sono campi distinti.** Una grata,
  una feritoia o una siepe fitta bloccano la vista ma non la linea d'effetto (o
  viceversa). Fonderli renderebbe impossibile modellare metà del vocabolario di
  un dungeon.
- **La copertura morbida (creature) NON è qui.** In tutti e tre i sistemi deriva
  dalle creature interposte, non dal terreno: è una proprietà del *momento*, non
  della cella. La calcola il motore, non la legenda.
- **`obscurement` invece di `concealment`.** 3.5 e PF1e usano una percentuale di
  fallimento; 5e non ha percentuali e usa livelli di oscuramento con
  svantaggio/accecato. Un nome neutro con tre livelli (`none|light|heavy`) mappa
  su entrambi i modelli; un nome preso da un sistema no.
- **`elevation_m` è geometria, non bonus.** La quota è un fatto della mappa; che
  dia +1 all'attacco (3.5/PF1e) o niente (5e RAW) lo dice il profilo.
- **`nameable` non è un dettaglio estetico**: è la metrica M8 e il criterio di
  Lynch. Distingue «mi sposto dietro il carro bruciato» da «vado in K12».

---

## 3. I tre profili di regole

Un profilo traduce i valori neutri in meccanica. Sono file separati e
sostituibili; il motore non ne conosce nessuno per nome.

### 3.1 Copertura

| Neutro | D&D 3.5 | Pathfinder 1e | D&D 5e |
|---|---|---|---|
| `none` | — | — | — |
| `half` | **+4 CA, +2 Riflessi** | **+4 CA, +2 Riflessi** | **+2 CA e ai TS Destrezza** |
| `three_quarters` | copertura migliorata: **+8 CA, +4 Riflessi** | **+8 CA, +4 Riflessi** | **+5 CA e ai TS Destrezza** |
| `total` | non bersagliabile direttamente | non bersagliabile direttamente | non bersagliabile direttamente |

### 3.2 Oscuramento / occultamento

| Neutro | D&D 3.5 | Pathfinder 1e | D&D 5e |
|---|---|---|---|
| `none` | — | — | — |
| `light` | occultamento: **20% di fallimento** | occultamento: **20%** | *lightly obscured*: **svantaggio** alle prove di percezione basate sulla vista |
| `heavy` | occultamento totale: **50%**, bersaglio non individuabile, niente AdO | idem | *heavily obscured*: chi vi si trova è di fatto **accecato** |

### 3.3 Costo di movimento

| Neutro | D&D 3.5 | Pathfinder 1e | D&D 5e |
|---|---|---|---|
| `1` | normale | normale | normale |
| `2` | terreno difficile (2 quadretti per 1 di movimento) | terreno difficile ×2 | terreno difficile ×2 |
| `4` | sottobosco denso: **×4** | ×4 ⚠️ *(da verificare sul PRD prima del rilascio)* | **la categoria non esiste** → il profilo la riduce a **×2** |

Il caso `4` è il più istruttivo: 5e **non ha** il moltiplicatore ×4. Il profilo
lo **satura** a ×2 e lo dichiara nel report, invece di fingere una regola che nel
sistema di destinazione non c'è. Questo è il comportamento richiesto a ogni
profilo davanti a un valore che il suo sistema non sa esprimere: **saturare e
dichiarare, mai inventare**.

### 3.4 Quota

| Neutro | D&D 3.5 | Pathfinder 1e | D&D 5e |
|---|---|---|---|
| dislivello ≥ 1 banda a favore | **+1 all'attacco in mischia** (posizione elevata) | **+1 all'attacco in mischia** | **nessun bonus RAW** — il profilo lo dichiara come opzionale del DM |

### 3.5 Scala del quadretto

Tutti e tre i sistemi usano il quadretto da 5 piedi. La convenzione metrica del
repo — **1,5 m/quadretto** — vale identica per tutti e tre. Le diagonali
differiscono (1-2-1 in 3.5/PF1e; 5 ft fisse in 5e base, 1-2-1 come variante) e
sono una proprietà del **profilo**, non della mappa.

---

## 4. La tabella completa dei 62 simboli

Valori **neutri**. `mov` = `blocks_movement`, `vista` = `blocks_sight`,
`cop` = `cover`, `osc` = `obscurement`, `cost` = `move_cost`,
`nom` = `nameable`.

### 4.1 Terreni (modo `fill`)

| Sim | Significato | mov | vista | cop | osc | cost | nom | Note |
|---|---|---|---|---|---|---|---|---|
| 🟩 | Pianura / area aperta | no | no | none | none | 1 | no | il default |
| 🟫 | Terra battuta / sentiero | no | no | none | none | 1 | no | |
| 🟨 | Sabbia / area segnalata | no | no | none | none | 1 | no | |
| ⬜ | Pavimento lavorato | no | no | none | none | 1 | no | |
| 🌿 | Vegetazione bassa | no | no | none | **light** | **2** | no | sottobosco leggero |
| 🌲 | Foresta densa | no | **sì** ¹ | **half** | **heavy** | **4** | no | ¹ blocca la vista **oltre** la cella, non dentro |
| 🟦 | Acqua profonda | no | no | none | none | — | no | `swim: true`; il costo lo dà il profilo (prova di Nuotare) |
| 🌊 | Acqua / corrente | no | no | none | none | **2** | no | acqua bassa |
| 🟧 | Lava raffreddata / pericolo | no | no | none | none | **2** | no | `hazard: {fire, minor}` |
| 🟥 | Zona letale | no | no | none | none | 1 | no | `hazard: {magic, lethal}` |
| ⛰ | **Montagne / creste rocciose** | **sì** | **sì** | **total** | none | — | sì | ⚠️ **correzione**: vedi §6 |
| 🏰 | Muro / roccia solida | **sì** | **sì** | **total** | none | — | no | |
| 🟪 | Pilastro / mithral | **sì** | **sì** | **total** | none | — | sì | |
| ⬛ | Struttura (tenda, edificio, dais) | **sì** | **sì** | **total** | none | — | sì | |

### 4.2 Ostacoli, coperture e pericoli (modo `icon`)

| Sim | Significato | mov | vista | cop | osc | cost | nom | Note |
|---|---|---|---|---|---|---|---|---|
| 🪨 | Rocce / macerie | no | no | **half** | none | **2** | **sì** | `destructible`, `prone_concealment` |
| 🧱 | Muretto / copertura bassa | no | no | **half** | none | 1 | **sì** | scavalcabile: `climb: easy` |
| 📦 | Casse / rifornimenti | **sì** | **sì** | **total** | none | — | **sì** | `destructible` |
| 🛢 | Barile | **sì** | no | **half** | none | — | **sì** | `destructible` |
| 🪑 | Tavolo e sedie | no | no | **half** | none | **2** | **sì** | ribaltabile |
| 🌾 | Erba alta / cespugli | no | no | none | **light** | **2** | **sì** | `prone_concealment` |
| 🌳 | Treant / creatura vegetale | **sì** | **sì** | **total** | none | — | **sì** | è una **creatura**: vedi §7 |
| 🗿 | **Statua** | **sì** | **sì** | **total** | none | — | **sì** | ⚠️ §6 · `destructible` |
| 🗼 | **Torre / struttura alta** | **sì** | **sì** | **total** | none | — | **sì** | ⚠️ §6 |
| 🏛 | **Edificio / tempio** | **sì** | **sì** | **total** | none | — | **sì** | ⚠️ §6 |
| ⛺ | Tenda | **sì** | **sì** | **total** | none | — | **sì** | `destructible` |
| 🕸 | Ragnatele | no | no | none | **light** | **4** | no | `hazard: {magic, minor}` — intrappola |
| ❄ | Ghiaccio | no | no | none | none | **2** | no | scivoloso: prova del profilo |
| 🍄 | Funghi giganti | no | no | **half** | **light** | **2** | **sì** | |
| 🦴 | Ossa / resti | no | no | none | none | **2** | **sì** | |
| 🔥 | Fuoco | no | no | none | **light** | 1 | no | `hazard: {fire, major}` (fumo → osc.) |
| 💥 | Fiamme / esplosione | no | no | none | **light** | 1 | no | `hazard: {fire, major}` |
| 🌋 | Bocca vulcanica / fumarola | no | no | none | **heavy** | **2** | **sì** | `hazard: {fire, lethal}` |
| ⚡ | Energia / pericolo magico | no | no | none | none | 1 | no | `hazard: {electric, major}` |
| 💀 | Fossa / trappola | no | no | none | none | 1 | no | `hazard: {fall, major}` |
| 🕳 | Voragine / buco | **sì** ² | no | none | none | — | **sì** | ² `hazard: {fall, lethal}`; volando si attraversa |

### 4.3 Passaggi, quota e luce

| Sim | Significato | mov | vista | cop | cost | nom | Note |
|---|---|---|---|---|---|---|---|
| 🚪 | Porta / ingresso | **sì** ³ | **sì** ³ | total ³ | 1 | **sì** | ³ **stato dinamico**: chiusa = muro, aperta = passaggio. `door: {state: closed\|open\|locked\|secret}` |
| 🌉 | Ponte / passerella | no | no | none | 1 | **sì** | `elevation_m` dalla zona |
| 🪜 | Scale / rampa | no | no | none | **2** | **sì** | collega due bande di quota |
| ⬇ | Discesa / pendenza | no | no | none | **2** | no | `climb: easy` |
| 🏮 | Braciere / fonte di luce | **sì** | no | **half** | — | **sì** | `light: {radius_m: 6, color: ffd9a0}` |
| 🕯 | Candele / rituale | no | no | none | 1 | **sì** | `light: {radius_m: 1.5}` |
| ✨ | Effetto magico attivo | no | no | none | 1 | **sì** | `light: {radius_m: 3}` |
| 🔮 | Cristalli / altare magico | **sì** | no | **half** | — | **sì** | `light: {radius_m: 3}` |
| 🌀 | Portale / vortice | no | no | none | 1 | **sì** | trasporto: logica del modulo |

### 4.4 Arredo e segnaposto (nessun effetto meccanico salvo indicato)

| Sim | Significato | mov | vista | cop | nom |
|---|---|---|---|---|---|
| 🏺 | Contenitore / bottino | no | no | none | **sì** |
| 💎 | Tesoro / oggetto magico | no | no | none | **sì** |
| 👑 | Trono / Corona | **sì** | no | **half** | **sì** |
| 🪓 | Rastrelliera / armi | **sì** | no | **half** | **sì** |
| 🛏 | Giaciglio | no | no | none | **sì** |
| ⚰ | Sarcofago / bara | **sì** | no | **half** | **sì** |
| 🐴 | Cavalcature | no | no | none ⁴ | **sì** |
| 🖼 | Affresco / quadro | no | no | none | **sì** |
| 🔔 | Allarme / trappola sonora | no | no | none | **sì** |
| ⭐ · 🎯 · ⚔ | Obiettivo primario · Obiettivo tattico · Zona di scontro | no | no | none | **sì** |

⁴ le cavalcature sono creature: la copertura morbida la calcola il motore (§7).

### 4.5 Unità (modo `unit`) — **non sono terreno**

`🔵 🔴 ⚫ 🟡 🟢 🟣` marcano **posizioni di creature**, non proprietà della cella.
Non hanno `function`: hanno `unit: {side, role}`. La copertura morbida che
generano è calcolata a runtime. Confonderle con il terreno è l'errore che rende
`M9` incalcolabile su metà del corpus (audit §3.1).

---

## 5. Confini di licenza — cosa può essere venduto

*(Non è un parere legale. Prima di vendere serve una verifica di un avvocato IP.)*

| Componente | Contenuto | Regime | Vendibile |
|---|---|---|---|
| Motore + `legend.yaml` | geometria e affordance, **zero numeri di gioco** | opera propria | **sì**, licenza a scelta dell'autore |
| `rules/dnd35.yaml` | meccaniche dall'SRD 3.5 | **OGL 1.0a** — richiede testo della licenza + catena Section 15 | sì, con OGL |
| `rules/pf1e.yaml` | meccaniche dal PRD Paizo | **OGL 1.0a** — Section 15 deve includere le note Paizo | sì, con OGL |
| `rules/dnd5e.yaml` | meccaniche dall'SRD 5.1 | **CC BY 4.0** (rilascio WotC 2023) — richiede solo attribuzione | sì, con attribuzione |
| Campagna RumblingStone | RHoD, Forgotten Realms | **bloccata** (ADR-0005) | **no** |

**Marchi**: «Dungeons & Dragons», «D&D», «Pathfinder» e i loghi **non** sono
usabili nel nome del prodotto né nel marketing. Il prodotto si descrive per
compatibilità, con la formula ammessa da ciascuna licenza — e la formula esatta
va verificata testo alla mano prima del rilascio, per ciascuno dei tre.

**Il vantaggio architetturale**: separando i numeri in tre file, l'OGL tocca
**due file**, non il prodotto. Un acquirente che usa solo il profilo 5e non
riceve nemmeno contenuto OGL.

---

## 6. Le quattro correzioni che chiudono la divergenza SVG↔UVTT

Oggi il renderer e l'esportatore UVTT non concordano su cosa sia un muro
(audit §2.1). Risolto sopra, con la regola 3.5 come arbitro: **una cella occupata
da roccia, edificio, torre o statua è impenetrabile e opaca**, quindi copertura
totale.

| Simbolo | Renderer oggi | UVTT oggi | Spec | Effetto del fix |
|---|---|---|---|---|
| `⛰` | solido (ombra, contorno) | **non è muro** | `total` | **3.689 celle in 6 mappe** acquistano muri nell'export: il *Dirupo Mortale* smette di essere trasparente in Foundry |
| `🗿` | icon | è muro | `total` | nessun cambio funzionale — ora **dichiarato** |
| `🗼` | icon | è muro | `total` | idem |
| `🏛` | icon | è muro | `total` | idem |

**Nessun SVG cambia.** Modo di rendering e funzione sono campi ortogonali: una
statua continua a disegnarsi come prop illustrato e *contemporaneamente* a
dichiararsi opaca. La byte-identità dei 17 SVG legacy regge; l'unico artefatto
che cambia è l'export UVTT delle 6 mappe con `⛰` — **ed è esattamente il bug**.

---

## 7. Limiti dichiarati della specifica

- **La copertura morbida non è modellabile staticamente**: dipende da chi sta
  dove in quel momento. La legenda dichiara il terreno; le creature le mette il
  motore.
- **`🌲` è un'approssimazione onesta.** Una cella di foresta densa non blocca la
  vista *dentro* di sé ma la blocca *attraverso*. La specifica la marca
  `blocks_sight: true` perché è il comportamento corretto sulle distanze che
  contano in una battlemap; per il combattimento corpo a corpo dentro il bosco,
  il DM deroga.
- **`🚪` ha uno stato**, non un valore: una porta chiusa è un muro, aperta è un
  passaggio. Il campo `door.state` è l'unico caso in cui `function` dipende da
  una variabile della mappa e non solo dal simbolo.
- **Le severità dei pericoli (`minor|major|lethal`) sono etichette, non danni.**
  Il profilo le traduce (1d6 / 2d6 / 4d6, CD del TS): sono numeri di gioco, e i
  numeri di gioco non stanno qui.
- **PF1e `move_cost: 4`** è l'unico valore di questa specifica che non è stato
  verificato sul testo: va confermato sul PRD prima del rilascio del profilo.
