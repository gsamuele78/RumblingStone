# ARC-07 · Lotto mappe D28 — Hammerfist nel 372 e nel 1372

> **Cos'è.** Le mappe che il lotto D28 di
> [LETTORE-E-PLAYTESTER](../../plans/PIANO-LETTORE-E-PLAYTESTER.md) chiedeva e
> che mancavano: la sezione a livelli di Hammerfist e le griglie da 1,5 m di
> fucina, gallerie, bottega dell'alchimista, cappella e armeria, nello stato del
> 372 (`ARC07-DEF-4`, Scena 5) e in quello del 1372 (l'assedio di ARC-08, la
> ritirata verso il Cuore della Montagna e la riconquista).
> Le correzioni di M7-A, M7-B e M7-C stanno nell'atlante
> `ARC07-MAPPE-DEFINITIVO.md` e nel loro contratto JSON.
>
> **Come è stato fatto.** Col set di simboli nuovo (D8 di
> [COLLAUDO-MAPPE](../../plans/PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md)), le
> griglie generate da uno script e non scritte a mano, e il collaudo:
> `python3 scripts/collaudo_mappe.py` su questo file dà **zero errori**.
>
> **Cosa è canone e cosa è proposta.** Quello che il testo giocato dice è
> canone e le mappe lo rispettano: la cappella **non ha un altare** ma una
> vecchia incudine portata dalla prima forgia; la bottega di Kettra sta **in
> fondo al corridoio della fucina**, con la porta bassa foderata di piombo; i
> quartieri ospiti sono gli alloggi dei minatori, scavati, con sei brande e un
> focolare; la cappella è **due porte più in là** dei quartieri; le gallerie
> sono **sotto la fucina**, strette, puntellate, una lampada ogni dieci passi;
> la fucina ha **tre bocche di pietra**. Il resto è marcato:
> `[PROPOSTA — needs DM confirmation]`.

| Mappa | Cosa | Stato |
|---|---|---|
| Sezione 372 | i livelli dalle mura alle gallerie | schema, non griglia |
| 1 · Livello 0, 372 | l'ala nella roccia: fucina, bottega, quartieri, dispensa, cappella, armeria | griglia 24 × 16 |
| 2 · Livello −1, 372 | le gallerie di Zeth | griglia 26 × 14 |
| Sezione 1372 | i livelli durante l'assedio, e la via di fuga di ARC-08 | schema, non griglia |
| 3 · Livello 0, 1372 | la stessa ala, il terzo giorno | griglia 24 × 16 |
| 4 · Livello −1, 1372 | le gallerie con le rune del Ghostlord | griglia 26 × 14 |

---

# IL 372

## La sezione a livelli

<!-- render: none -->
```
SEZIONE A LIVELLI — HAMMERFIST ≈372 DR (da sud a nord · quote indicative)
════════════════════════════════════════════════════════════════════════
 +18 m   camminamenti delle mura esterne, balestre pesanti (Scena 11)
 +4,5 m  camminamenti del cortile interno: gru, arcieri · 🗼 torre nord, campane
   0 m   spianata ─ porta principale ─ cortile esterno ─ CORTILE INTERNO (M7-B)
                                                        │ 🗿 statua del re antenato
         LIVELLO 0 · l'ala nella roccia, a nord del cortile (mappa 1)
           fucina (arco sul cortile) ─ corridoio ─ bottega di Kettra
           armeria · quartieri ospiti · dispensa · cappella ─ verso la sala del trono
  −6 m   LIVELLO −1 · le gallerie di Zeth (mappa 2): si scende da H15 della fucina
           strette, puntellate, una lampada ogni dieci passi
 −15 m   [PROPOSTA D28-c] la fucina grande: si scende da Y12 delle gallerie
 −30 m?  il cuore della montagna: nel 372 nessuno lo nomina
════════════════════════════════════════════════════════════════════════
 più si scende, più le sale sono ampie
```

- L'altezza delle mura esterne (18 m) è quella della Scena 11; i camminamenti
  del cortile interno a +4,5 m sono quelli di M7-B. Sono due muri diversi, e
  il modulo li dà entrambi.
- **[PROPOSTA — needs DM confirmation]** la fucina grande sotto le gallerie
  (D28-c: *«la fucina grande sta sotto, e la si vede scendendo da Zeth»*). La
  proposta non è stata decisa; finché non lo è, la scala Y12 delle gallerie
  porta a una sala che non ha una mappa.

## MAPPA 1 — LIVELLO 0: L'ALA NELLA ROCCIA (372)

**Dimensioni**: 36 m × 24 m (24 colonne × 16 righe, scala 1,5 m/quadretto)
**Quando si usa**: `ARC07-DEF-4` Scena 5, la notte nella fortezza. La riga 16
è il muro nord del cortile interno (M7-B, riga 04): l'arco della fucina sta
sulle colonne C-E, la porta dell'ala sulla colonna K.

```
════════════════════════════════════════════════════════════════════════
 L'ALA NELLA ROCCIA, 372 — 36 m × 24 m (24 col × 16 righe · 1,5 m)
 Hammerfist ≈372 DR · notte (Scena 5)
════════════════════════════════════════════════════════════════════════
COL →  A B C D E F G H I J K L M N O P Q R S T U V W X
01    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
02    🏰⬜🪓🪓🪓🪓🗄🏰⬜🛏🛏🛏🛏🛏🛏🏰🏰🏰🏰⬜⬜⬜⬜🏰   armeria [PROPOSTA] · quartieri, sei brande · cappella
03    🏰⬜⬜⬜⬜⬜⬜🏰⬜⬜⬜⬜⬜⬜⬜🏰⬜📦🏰⬜⬜⚒⬜🏰
04    🏰⬜⬜⬜⬜⬜⬜🏰⬜⬜⬜⬜⬜⬜⬜🏰⬜⬜🏰⬜⬜⬜🔵🏰
05    🏰⬜📦⬜⬜⬜📦🏰⬜⬜⬜⬜⬜⬜🔥🏰⬜🛢🏰⬜⬜⬜⬜🏰
06    🏰🏰🏰🔒🏰🏰🏰🏰🏰🏰🏰🚪🏰🏰🏰🏰🚪🏰🏰🏰🏰🚪🏰🏰   porte: armeria (chiusa), quartieri, dispensa, cappella
07    🏰⬜⬜⬜⬜⬜⬜⬜⬜⬜🔵⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🚪   → verso la sala del trono
08    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
09    🏰⬜🔥⬜🔥⬜🔥⬜🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰   le tre bocche di pietra della fucina
10    🏰⬜⬜⬜⬜⬜⬜⬜🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰⬜⬜⬜🏰
11    🏰⬜⚒⬜⚒⬜⬜⬜🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰⬜⬜🧪🏰
12    🏰⬜⬜⬜⬜⬜⬜⬜🚪⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🚪⬜🔵⬜🏰
13    🏰⬜⬜⬜⬜🔵⬜⬜🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰⬜⬜🧪🏰
14    🏰💧⬜⬜⬜⬜🪑⬜🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰⬜⬜⬜🏰
15    🏰⬜⬜⬜⬜⬜⬜🔽🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
16    🏰🏰🚪🚪🚪🏰🏰🏰🏰🏰🚪🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰   ↓ al cortile interno: righe 04 di M7-B, colonne C-E e K
════════════════════════════════════════════════════════════════════════
LEGENDA · 🏰 roccia viva e muri · ⬜ pavimento lavorato · 🚪 porta · 🔒 porta
chiusa a chiave · 🔥 fuoco della forgia o del focolare · ⚒ incudine · 💧 vasca
per temprare · 🪑 banco · 🧪 banco dell'alchimista · 📦 casse · 🛢 barile · 🛏 branda
· 🪓 rastrelliera · 🗄 armadio · 🔽 scala che scende alle gallerie · 🪵 detriti
@north N
@tipo tattica
@collega H15 ; ARC07-MAPPE-D28-HAMMERFIST.md#2 D03
@mark 1 ; W04 ; Sorella Brynja
@mark 2 ; V12 ; Kettra
@mark 3 ; F13 ; Gunnvor e il pesatore
@mark 4 ; K07 ; Durin
```

### 🌍 Ambiente

| Elemento | Dove | Effetto |
|---|---|---|
| Luce | fucina (righe 09-15) | le tre forge accese: luce piena in tutta la sala |
| Luce | corridoi, quartieri | lampade e il focolare (N05): luce fioca fuori dai cerchi |
| Rumore | fucina | l'unico posto della fortezza dove nessuno parla sottovoce: Ascoltare a −10 dentro la sala, come per un ambiente rumoroso dell'SRD `[INFERRED — needs DM confirmation]` |
| Porte | D06 armeria | **chiusa a chiave**: Aprire Serrature o Forza con la tabella delle porte di ferro dell'SRD |
| Porte | U12 bottega | bassa e foderata di piombo |
| Soffitto | quartieri | una crepa chiusa col piombo, del primo crollo: nessuno dorme sotto (Scena 5) |
| Scala | H15 | scende alle gallerie (mappa 2, D03) |

### ⚔️ Tattiche

La notte del 372 non ha scontri qui: è il giro della fortezza della Scena 5,
dove ogni cosa costa una tacca dell'orologio. La mappa serve a sapere **chi
sta dove** e **quanto è lontano**, contato sul grafo dal collaudo: dalla
porta dell'ala (K16) alla porta della bottega di Kettra ci sono 13 quadretti,
alla porta della cappella 21, alla scala delle gallerie 10 passando per la
fucina; dall'arco della fucina (D16) alla scala, 5.

- **Brynja** (W04) conta fiale accanto all'incudine; venti chierici dormono
  seduti con la schiena ai muri della cappella.
- **Kettra** (V12) riempie le fiasche al banco; la cassa di sabbia (V14) è
  per quando qualcosa va storto.
- **Gunnvor** (F13) al banco della fucina, il pesatore accanto; la fila dei
  ragazzi davanti alle tre forge.
- **Durin** (K07) accompagna i PG.

### 🔄 Evoluzione

- All'alba la fucina resta accesa: è quella che nel duello (M7-B) si vede
  dall'arco C04-E04, e dove si può spingere il drago (Scena 11).
- **[PROPOSTA — needs DM confirmation]** l'armeria. Il modulo non la descrive
  nel 372: la Scena 5 manda a comprare alla fucina, e l'«armeria nanica» è il
  banco del 1372. Qui c'è perché il lotto D28 la chiede; se il DM preferisce
  che nel 372 non ci sia, la stanza diventa un magazzino e la porta D06
  resta chiusa.

## MAPPA 2 — LIVELLO −1: LE GALLERIE DI ZETH (372)

**Dimensioni**: 39 m × 21 m (26 colonne × 14 righe, scala 1,5 m/quadretto)
**Quando si usa**: `ARC07-DEF-4` Scena 5, *«cercarlo costa una tacca»*.

```
════════════════════════════════════════════════════════════════════════
 LE GALLERIE DI ZETH, 372 — 39 m × 21 m (26 col × 14 righe · 1,5 m)
 Hammerfist ≈372 DR · sotto la fucina
════════════════════════════════════════════════════════════════════════
COL →  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
01    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
02    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
03    🏰🏰🟤🔼🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰   🔼 su, alla fucina (H15 dell'ala)
04    🏰🏰🟤🟤🟤🟤🟤🕯🟤🟤🟤🟤🕯🟤🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
05    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🟤🟤🟣🟤🟤🏰   🟣 Zeth, col gesso e il martelletto
06    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
07    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🟤🟤🟤🕯🟤🟤🟤🟤🟤🟤🏰
08    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
09    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
10    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
11    🏰🏰🏰🏰🟤🟤🟤🟤🕯🟤🟤🟤🟤🟤🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
12    🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🟤🟤🟤🔽🏰   🔽 giù: la fucina grande [PROPOSTA D28-c]
13    🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰   cunicolo cieco
14    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
════════════════════════════════════════════════════════════════════════
LEGENDA · 🏰 roccia · 🟤 galleria scavata (larga un quadretto, puntellata) ·
🕯 lampada a olio · 🔼 scala che sale · 🔽 scala che scende · 🟣 Zeth · ✨ runa
attiva · 🗿 leone di pietra · 🪵 detriti
@north N
@tipo tattica
@collega D03 ; ARC07-MAPPE-D28-HAMMERFIST.md#1 H15
@deroga posa/fra-livelli ; la scala Y12 scende alla fucina grande, che e' una proposta (D28-c) non ancora disegnata
@mark 1 ; W05 ; Mastro Costruttore Zeth
```

### 🌍 Ambiente

| Elemento | Dove | Effetto |
|---|---|---|
| Larghezza | tutte le gallerie | un quadretto: una creatura Grande ci passa solo strizzandosi (SRD: costo doppio, −4 a colpire e alla CA) |
| Luce | 🕯 ogni cinque quadretti circa | ogni lampada fa il suo cerchio di luce, *«e poi niente»*: fra un cerchio e l'altro è buio |
| Pareti | ovunque | segni a gesso, metà cancellati col pollice: le rune di Zeth, **colore** nel 372 (D30) |
| Camera di lavoro | U03-Y12 | la sala più ampia: più si scende, più le sale si allargano |
| Anello | E04-O04-O11-E11 | le gallerie chiudono un giro: si può arrivare da Zeth per due strade |

### ⚔️ Tattiche

Nessuno scontro nel 372. La domanda di questa mappa è **dove trovare Zeth**:
si sente il martelletto *«da un punto più in fondo»*, quindi chi segue il
suono va verso est, nella camera di lavoro.

### 🔄 Evoluzione

Le rune che Zeth traccia stanotte saranno, nel 1372, le difese del Ghostlord
(D30): la mappa 4 è questa stessa galleria mille anni dopo.

---

# IL 1372

## La sezione a livelli

<!-- render: none -->
```
SEZIONE A LIVELLI — HAMMERFIST 1372 DR, terzo giorno dell'assedio
════════════════════════════════════════════════════════════════════════
 +20 m   torri est e ovest · +15 m bastioni · +12 m mura principali
         (MAPPA 2C dell'atlante di ARC-08)
  +3 m   CORTILE INTERNO, rialzato · 🗿 statua del Re Antenato
           └─ passaggio segreto sotto la statua (MAPPA 3X): la fuga
   0 m   cortile esterno · fossato −3 m · ponte levatoio
         LIVELLO 0 · l'ala nella roccia (mappa 3): fucina, sala dei
           feriti, cappella della forgia, armeria
  −6 m   LIVELLO −1 · le gallerie di Zeth (mappa 4): rune del Ghostlord,
           leoni di pietra
   ...   la fuga: tunnel ─ ponte sospeso (3Y) ─ incrocio silenzioso (3Z)
   ...   IL CUORE DELLA MONTAGNA (CM-1, MAPPA 5): 100 m × 80 m, volta a 40 m
════════════════════════════════════════════════════════════════════════
 la quota del Cuore della Montagna non è scritta nel modulo
```

- Le quote delle mura, dei bastioni e delle torri sono quelle dell'atlante di
  ARC-08 (MAPPA 2C), e la via di fuga quella delle mappe 3X, 3Y e 3Z.
- **La statua del re antenato** sta a nord del cortile interno in tutte e due
  le epoche (M7-B nel 372, MAPPA 3X nel 1372). Nel 1372 nasconde il passaggio
  di fuga. **[PROPOSTA — needs DM confirmation]** che sia la stessa statua, la
  sola che la Zona 1 del 372 descrive («una statua di re, non venti»).
- Il cortile del 1372 ha già la sua mappa (H3-1 in
  `08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L3-REVISED-Ultra-Clear.md`):
  qui non se ne disegna un'altra.

## MAPPA 3 — LIVELLO 0: L'ALA NELLA ROCCIA (1372)

**Dimensioni**: 36 m × 24 m (24 colonne × 16 righe, scala 1,5 m/quadretto)
**Quando si usa**: ARC-08, il terzo giorno, quando l'orda entra nel cortile
interno e la ritirata passa per la statua; e dopo, nella riconquista.

```
════════════════════════════════════════════════════════════════════════
 L'ALA NELLA ROCCIA, 1372 — 36 m × 24 m (24 col × 16 righe · 1,5 m)
 Hammerfist 1372 DR · terzo giorno dell'assedio
════════════════════════════════════════════════════════════════════════
COL →  A B C D E F G H I J K L M N O P Q R S T U V W X
01    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
02    🏰⬜🪓🪓🪓🪓🗄🏰⬜🛏🛏🛏🛏🛏🛏🏰🏰🏰🏰⬜⬜⬜⬜🏰   armeria · sala dei feriti · cappella della forgia
03    🏰⬜⬜⬜⬜⬜⬜🏰⬜⬜⬜⬜⬜🔵⬜🏰⬜📦🏰⬜🔵⚒⬜🏰
04    🏰⬜⬜⬜⬜⬜⬜🏰⬜⬜⬜⬜⬜⬜⬜🏰⬜⬜🏰⬜⬜⬜🔵🏰
05    🏰⬜📦⬜⬜⬜📦🏰⬜⬜⬜⬜⬜⬜🔥🏰⬜🛢🏰⬜⬜⬜⬜🏰
06    🏰🏰🏰🔒🏰🏰🏰🏰🏰🏰🏰🚪🏰🏰🏰🏰🚪🏰🏰🏰🏰🚪🏰🏰   porte: armeria (chiusa), quartieri, dispensa, cappella
07    🏰⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🪵🪵⬜⬜⬜⬜🚪   → verso la sala del trono
08    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
09    🏰⬜🔥⬜🔥⬜🔥⬜🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰   le tre bocche di pietra della fucina
10    🏰⬜⬜⬜⬜⬜⬜⬜🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰⬜⬜⬜🏰
11    🏰⬜⚒⬜🪵⬜⬜⬜🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰⬜⬜🧪🏰
12    🏰⬜⬜⬜⬜⬜⬜⬜🚪🔵⬜⬜⬜⬜⬜⬜⬜⬜⬜🚪⬜⬜⬜🏰
13    🏰⬜⬜⬜🔴⬜⬜⬜🏰🏰🔵🏰🏰🏰🏰🏰🏰🏰🏰🏰⬜⬜🧪🏰
14    🏰💧⬜🔴⬜🔴🪑⬜🏰🏰🔵🏰🏰🏰🏰🏰🏰🏰🏰🏰⬜⬜⬜🏰   barricata sull'arco: l'orda è entrata
15    🏰⬜📦📦⬜⬜⬜🔽🏰🏰⬜🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
16    🏰🏰🚪🚪🚪🏰🏰🏰🏰🏰🚪🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰   ↓ al cortile interno: righe 04 di M7-B, colonne C-E e K
════════════════════════════════════════════════════════════════════════
LEGENDA · 🏰 roccia viva e muri · ⬜ pavimento lavorato · 🚪 porta · 🔒 porta
chiusa a chiave · 🔥 fuoco della forgia o del focolare · ⚒ incudine · 💧 vasca
per temprare · 🪑 banco · 🧪 banco dell'alchimista · 📦 casse · 🛢 barile · 🛏 branda
· 🪓 rastrelliera · 🗄 armadio · 🔽 scala che scende alle gallerie · 🪵 detriti
@north N
@tipo tattica
@collega H15 ; ARC07-MAPPE-D28-HAMMERFIST.md#4 D03
```

### 🌍 Ambiente

| Elemento | Dove | Effetto |
|---|---|---|
| Fucina | righe 09-15 | *«La fucina è la stessa. Le tre bocche di pietra»* (`ARC08-17`): due nani anziani battono su **un'incudine sola** (C11); dove c'era la seconda ci sono i detriti (E11) |
| Barricata | C15-D15 | casse contro l'arco: copertura totale finché stanno in piedi; si sfondano |
| Detriti | R07-S07 | il corridoio nord è ingombro: terreno difficile (×2) |
| Sala dei feriti | quartieri (J02-O05) | i chierici di Dana, *«dietro la seconda porta»* (`ARC08-17`): è la seconda porta del corridoio nord, quella dei vecchi quartieri |
| Cappella della forgia | T02-W05 | Dana e Thorin (`ARC08-17`) |

### ⚔️ Tattiche — la ritirata

- **Disposizione**: tre orchi (D14, E13, F14) sono entrati dall'arco della
  fucina; tre difensori tengono il corridoio della porta (J12, K12, K14). Nella
  sala dei feriti e nella cappella ci sono i chierici.
- **La strozzatura** è il corridoio K: largo un quadretto, ci si combatte uno
  contro uno, e chi lo tiene copre la ritirata dei feriti verso il cortile e
  la statua.
- **La porta K16** porta al cortile interno: è da lì che i feriti escono
  verso il passaggio segreto (MAPPA 3X).

### 🔄 Evoluzione — la riconquista

Quando i Rumbling Stones tornano (DEF-5, poi ARC-08), si entra da K16 e
dall'arco della fucina, al contrario: la fucina è il primo posto da
riprendere, perché è da lì che escono le armi. **[PROPOSTA — needs DM
confirmation]** le posizioni dell'orda nella riconquista: il modulo non le
scrive, e questa mappa non le inventa.

## MAPPA 4 — LIVELLO −1: LE GALLERIE DI ZETH (1372)

**Dimensioni**: 39 m × 21 m (26 colonne × 14 righe, scala 1,5 m/quadretto)
**Quando si usa**: ARC-08, se i PG scendono dalla fucina; e ARC-09, dove il
dilemma di Hella su Zeth il Murato comincia a farsi sentire.

```
════════════════════════════════════════════════════════════════════════
 LE GALLERIE DI ZETH, 1372 — 39 m × 21 m (26 col × 14 righe · 1,5 m)
 Hammerfist 1372 DR · le difese del Ghostlord
════════════════════════════════════════════════════════════════════════
COL →  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
01    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
02    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰   ✨ le rune del Ghostlord · 🗿 i leoni di pietra di Zeth
03    🏰🏰🟤🔼🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🗿🟤🗿🟤🏰   🔼 su, alla fucina (H15 dell'ala)
04    🏰🏰🟤🟤🟤🟤🟤🕯🟤✨🟤🟤🕯🟤🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
05    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
06    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
07    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🟤🟤🟤🕯✨🟤🟤✨🟤🟤🏰
08    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
09    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
10    🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
11    🏰🏰🏰🏰🟤🟤🪵🟤🕯🟤🟤✨🟤🟤🟤🏰🏰🏰🏰🏰🟤🟤🟤🟤🟤🏰
12    🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🟤🟤🟤🔽🏰   🔽 giù: la fucina grande [PROPOSTA D28-c]
13    🏰🏰🏰🏰🏰🏰🏰🏰🏰🟤🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰   cunicolo cieco
14    🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰🏰
════════════════════════════════════════════════════════════════════════
LEGENDA · 🏰 roccia · 🟤 galleria scavata (larga un quadretto, puntellata) ·
🕯 lampada a olio · 🔼 scala che sale · 🔽 scala che scende · 🟣 Zeth · ✨ runa
attiva · 🗿 leone di pietra · 🪵 detriti
@north N
@tipo tattica
@collega D03 ; ARC07-MAPPE-D28-HAMMERFIST.md#3 H15
@deroga posa/fra-livelli ; la scala Y12 scende alla fucina grande, che e' una proposta (D28-c) non ancora disegnata
```

### 🌍 Ambiente

| Elemento | Dove | Effetto |
|---|---|---|
| Rune | ✨ J04, L11, T07, W07 | **le difese del Ghostlord** (D30): sono attive. Che cosa fanno lo decide il DM, dalle tre famiglie che Zeth sapeva incidere (protezione, annullamento come nella miniera di Belkram, spegnere un incantesimo solo) `[PROPOSTA — needs DM confirmation]` |
| Leoni di pietra | 🗿 V03, X03 | *«I miei leoni di pietra proteggeranno queste gallerie per sempre»* (Scena 5): eccoli, all'ingresso della camera |
| Detriti | G11 | terreno difficile (×2) |

### ⚔️ Tattiche

Le gallerie non sono la via di fuga di ARC-08, che passa sotto la statua del
cortile (MAPPA 3X). **[PROPOSTA — needs DM confirmation]** se le due si
incrociino: il modulo non lo dice, e farle incrociare cambierebbe l'incontro
dell'incrocio silenzioso (3Z).

### 🔄 Evoluzione

La camera di lavoro è dove Zeth stava nel 372. Nel 1372 è vuota: il Ghostlord
vive nel Thornwaste (ARC-09).

---

## Il collaudo

```bash
python3 scripts/collaudo_mappe.py "07_il Portale Della Forgia Eterna/Mappe/ARC07-MAPPE-D28-HAMMERFIST.md"
```

Zero errori. L'unico rilievo è la scala Y12 delle gallerie, che porta alla
fucina grande non ancora decisa: ha la sua deroga scritta nella griglia.
