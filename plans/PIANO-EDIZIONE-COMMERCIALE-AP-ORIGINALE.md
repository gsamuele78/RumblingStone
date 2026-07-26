# PIANO — EDIZIONE COMMERCIALE: DA CAMPAGNA PRIVATA A ADVENTURE PATH ORIGINALE

> **Cos'è**: il percorso per trasformare gli archi 04-08 (**252.111 parole**) in
> un Adventure Path **originale, autonomo e vendibile**, senza toccare la
> campagna giocata al tavolo.
>
> **Decisione**: [ADR-0018](adr/ADR-0018-edizione-commerciale-ap-originale.md) —
> AP originale autonomo, **mai** un'espansione di *Red Hand of Doom*.
> **Misura di partenza**: [`docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md`](../docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md).
>
> **Terzo prodotto**: affianca il toolkit
> ([`PIANO-PRODOTTO-TOOLKIT-VENDIBILE`](PIANO-PRODOTTO-TOOLKIT-VENDIBILE.md)) e i
> map pack. Ne **riusa l'infrastruttura**: il contratto dei finding (P2.0) porta
> il check `ip/forbidden-term`; i map pack (P4.1) forniscono le mappe.
>
> **Stato**: 🔵 pianificato · **Data**: 2026-07-26 · **%**: 0%
> ⚠️ **Gate assorbente**: nulla si pubblica senza la verifica di un avvocato IP.

---

## 1. Perché è possibile, in un grafico

Densità di occorrenze *Red Hand of Doom* ogni 1.000 parole:

```
arco 04 ·············································· 0,0      2.830 parole
arco 06 ·············································· 0,0     16.271
arco 07 ·█··········································· 0,3    151.588   ← dentro
arco 08 ·███········································· 1,1     81.422   ← dentro
arco 09 ·███████████████████························· 5,3    195.739   ← FUORI v1
arco 00 ·████████████████████████████████████████████ 20,2     7.750   ← si rigenera
```

**252.111 parole a densità ≈ 0,5**: è verniciatura di nomi, non impianto. E le
due spine narrative sono diverse — RHoD va da Guado di Drellin all'assedio di
Brindol; questa va dalla miniera alla Corona di Adamantio, ai piani elementali, a
Hammerfist, con antagonisti originali e riscalatura all'8° livello.

## 2. Perimetro (da ADR-0018 §4)

| | Materiale | Parole |
|---|---|---:|
| ✅ **Dentro** | archi 04, 06, 07, 08 | 252.111 |
| ❌ **Fuori dalla v1** | arco 09 — rientra solo dopo riscrittura sostanziale, valutata a sé | 195.739 |
| 🔧 **Si rigenera** | arco 00 — impalcatura, tabelle armate | 7.750 |
| 🔒 **Privato per sempre** | `campaign/`, `state.md`, log di sessione, booklet, dossier DM | — |

**Non-obiettivi**: ❌ non si tocca la campagna al tavolo (continua con Moradin,
i Realms e la Mano Rossa) · ❌ non si pubblica su DMs Guild (sarebbe solo 5e e un
prodotto diverso) · ❌ non si vende l'arco 09 nella v1 · ❌ non si scrive
contenuto nuovo: si **trasforma** quello che c'è.

---

## 3. I lotti

### Fase E0 — Decisione e fondamenta

#### ⬜ E0.1 — Il ramo commerciale è **derivato**, mai copiato ⭐

Due varianti dello stesso contenuto divergono, se tenute a mano. La commerciale
si **genera** dalla privata con una trasformazione dichiarata, versionata e
rieseguibile: `scripts/build_commercial_edition.py` applica una **mappa di
sostituzione** (`edition/substitutions.yaml`) al sorgente privato.

- una voce = termine privato → termine pubblico + **nota di trasformazione**;
- le sostituzioni che richiedono riscrittura narrativa (non meccaniche) sono
  marcate `manual: true` e **falliscono** se il testo non è ancora stato riscritto:
  la mappa non finge di poter automatizzare Moradin;
- output in un albero separato, mai committato accanto al canone privato.

**Accettazione**: rieseguendo il build si ottiene un output **byte-identico**;
zero file del ramo privato modificati; ogni voce `manual: true` non ancora
risolta è un errore, non un warning.
**Engine**: Sonnet · **Impegno**: medio · **Stima**: 8-10 h.

#### ⬜ E0.2 — Il check `ip/forbidden-term`, dentro il contratto unico

Riusa il contratto dei finding del piano toolkit (P2.0): lista dei termini
vietati come **dato versionato**, non regex sepolta nel codice. Severità `error`
sul ramo commerciale, `info` sul privato — **la severità dipende dal profilo di
release, non dal check**.

Copre i ~3.800 nomi RHoD e i ~4.600 di ambientazione WotC censiti nell'audit.

**Accettazione**: `dm.py verify --edition commercial` è verde solo a zero
occorrenze; introdurre di proposito «Brindol» nel ramo commerciale lo fa fallire.
**Engine**: Sonnet · **Impegno**: basso · **Stima**: 4-5 h · **Dip.**: P2.0 del
piano toolkit.

---

### Fase E1 — Sostituzione dell'ambientazione (il lavoro grosso)

#### ⬜ E1.1 — Il pantheon: Moradin e i suoi ⭐ *il lotto più grande*

**1.502 occorrenze**, e non è un find-and-replace. L'SRD esclude i nomi delle
divinità; Moradin è la spina teologica di una campagna nanica — Cuore di Moradin,
Corona di Adamantio, Forgia Eterna, *Canto della Pietra e del Fuoco*.

Serve una **divinità artigiana originale** con: nome, epiteti, dominio, mito di
fondazione, liturgia, rapporto con la forgia e la pietra. Poi la riscrittura dei
passaggi in cui la teologia *agisce* (visioni, benedizioni, il canto, i nomi degli
artefatti), non solo di quelli in cui è nominata.

**Accettazione**: la divinità regge una lettura a freddo di un playtester che non
conosce D&D; nessun epiteto è un sinonimo trasparente di Moradin; i nomi degli
artefatti sono coerenti col nuovo mito; zero occorrenze residue.
**Engine**: Opus (è scrittura di canone) · **Impegno**: alto · **Stima**: 30-40 h.

#### ⬜ E1.2 — Geografia e fazioni dei Realms

Faerûn 979 · Thay 338 · Waterdeep 284 · Channathgate 282 · Cormyr 252 · Harpers
245 · Zhentarim 218 · Dalelands 188 · Myth Drannor 90 · Sembia 73.

Le fazioni vanno **rifondate**, non rinominate: un'organizzazione di spie
originale con motivazioni proprie, non «gli Arpisti con un altro nome».

**Accettazione**: la mappa regionale sta in piedi senza riferimenti esterni; ogni
fazione ha una scheda con obiettivo, metodo e limite; nessun toponimo è
anagramma o calco del corrispondente Realms.
**Engine**: Opus · **Impegno**: alto · **Stima**: 25-35 h.

#### ⬜ E1.3 — La fazione antagonista

Red Hand 659 + Mano Rossa 225. È il lotto più **facile** dei tre, contrariamente
all'intuizione: l'orda è già usata come cornice, non come impianto, negli archi
04-08. Serve un'identità visiva e simbolica nuova (insegna, gerarchia, rito), non
una nuova trama.

⚠️ **«Artiglio Cremisi» è un sinonimo trasparente**: non conta come sostituzione
(ADR-0018 §3).

**Accettazione**: l'insegna e la gerarchia non ricalcano i Wyrmlord; il ruolo
narrativo regge senza il culto draconico dell'AP.
**Engine**: Opus · **Impegno**: medio · **Stima**: 12-16 h.

---

### Fase E2 — De-derivazione strutturale

#### ⬜ E2.1 — Passata di somiglianza sostanziale, arco per arco

Non i nomi: la **struttura**. Per ciascuno degli archi 04-08, confronto
dichiarato contro l'AP originale su sequenza degli eventi, ruoli dei
personaggi, funzione dei luoghi. Dove un beat è riconoscibilmente quello di RHoD,
si cambia **il beat**, non l'etichetta.

Dalla misura, l'esito atteso è che gli archi 04-07 passino quasi intatti e che
l'attenzione si concentri su 08 (densità 1,1).

**Accettazione**: una tabella di confronto committata, arco per arco, con esito
e motivazione; ogni beat marcato «derivato» ha una riscrittura o una
giustificazione scritta.
**Engine**: Opus · **Impegno**: alto · **Stima**: 20-25 h.
**Gate**: è questa tabella che va **davanti all'avvocato**, non i file.

#### ⬜ E2.2 — Rigenerazione dell'arco 00

Tabelle armate, composizione, flusso di campagna: impalcatura riscritta
originale sui nuovi nomi. Volume trascurabile (7.750 parole), densità altissima
(20,2) — si rifà, non si bonifica.

**Engine**: Sonnet · **Impegno**: basso · **Stima**: 5-7 h.

---

### Fase E3 — Meccaniche, licenze, edizione

#### ⬜ E3.1 — Profilo di sistema e conformità OGL

3.5 e/o PF1e sotto **OGL 1.0a**: testo della licenza, catena Section 15,
dichiarazione di Product Identity e Open Game Content. Per PF1e, la
**Compatibility License** di Paizo (oggi senza registrazione). Marchi «D&D» e
logo d20 **fuori** da titolo e marketing.

Riusa il lavoro già fatto per il toolkit: i profili di regole di
[ADR-0016](adr/ADR-0016-profili-regole-multisistema.md) valgono anche qui.

**Accettazione**: un gate CI verifica la presenza dei file di licenza dovuti;
nessun marchio nel titolo; la dichiarazione di Product Identity copre le
creazioni originali (divinità, fazioni, toponimi, artefatti).
**Engine**: Opus · **Impegno**: medio · **Stima**: 8-10 h. **Gate**: avvocato IP.

#### ⬜ E3.2 — Mappe e illustrazioni

Le mappe arrivano dai **map pack neutri** (lotto P4.1 del piano toolkit): stesso
strumento, stessa qualità, provenienza pulita. Le immagini generate vanno
etichettate `Contains AI-Generated Content` dove pertinente, e i prompt bonificati
dai riferimenti a IP protette (lotto D4 del piano level design).

**Accettazione**: ogni mappa del prodotto passa il linter o ha deroga scritta;
nessun asset di terzi; provenienza documentata per ogni immagine.
**Engine**: Sonnet · **Impegno**: alto · **Stima**: dipende dal numero di mappe.

#### ⬜ E3.3 — Produzione editoriale e pubblicazione

Impaginazione (la via Homebrewery/booklet di ADR-0013 esiste già), indice,
introduzione per il DM, guida alla conversione, playtest esterno.
Canale: DriveThruRPG / Itch, OGL 3.5 e/o PF1e.

**Accettazione**: un DM esterno che non conosce la campagna sa condurre l'arco 06
leggendo solo il prodotto.
**Engine**: Opus (introduzione e guida) + Sonnet (impaginazione) ·
**Impegno**: alto · **Stima**: 25-35 h.

---

## 4. Sequenza e stime

| # | Fase | Ore | Alla fine hai |
|---|---|---:|---|
| 1 | E0.1 + E0.2 | 12-15 | la trasformazione è **rieseguibile e verificata**, non fatta a mano |
| 2 | E1.3 | 12-16 | la fazione antagonista è tua — il lotto più facile, per prendere ritmo |
| 3 | **E1.1** ⭐ | 30-40 | il pantheon: **il lotto che decide se il progetto è fattibile** |
| 4 | E1.2 | 25-35 | geografia e fazioni originali |
| 5 | **E2.1** | 20-25 | la tabella di somiglianza sostanziale — **ciò che va all'avvocato** |
| 6 | E2.2 + E3.1 | 13-17 | impalcatura rigenerata, conformità OGL |
| 7 | E3.2 + E3.3 | 25-35+ | mappe, impaginazione, playtest, pubblicazione |

**Totale**: ~140-185 h, più le mappe.

**Ordine ragionato**: E1.1 (il pantheon) sta al terzo posto e non al primo di
proposito — E0 dà la rete e E1.3 dà un lotto piccolo su cui tarare il metodo di
sostituzione prima di affrontare 1.502 occorrenze. Ma **è il lotto che decide**:
se il pantheon originale non regge alla lettura, il progetto non è fattibile, e
va scoperto prima di spendere le 100 ore successive.

---

## 5. Rischi

| Rischio | Mitigazione |
|---|---|
| **Rinominare senza trasformare** — il rischio principale | E2.1 misura la struttura, non i nomi; i sinonimi trasparenti sono esplicitamente esclusi (ADR-0018 §3) |
| Il ramo commerciale diverge da quello privato | E0.1: il commerciale è **generato**, mai copiato; rieseguibile e byte-identico |
| La bonifica si erode al primo contenuto nuovo | E0.2: `ip/forbidden-term` in CI con severità per edizione |
| Moradin non è sostituibile senza perdere l'anima della campagna | è **il** rischio di contenuto. Per questo E1.1 ha un criterio di accettazione esterno (lettura a freddo di un playtester) invece di un'autovalutazione |
| L'avvocato giudica insufficiente la trasformazione di 07-08 | E2.1 produce la tabella **prima** della produzione editoriale: si scopre a 100 ore, non a 180 |
| Si finisce per rifare la campagna da zero | il perimetro di ADR-0018 §4 è vincolante: arco 09 fuori, campagna giocata privata |
| Il prodotto non trova compratori | ~250.000 parole di AP per 3.5/PF1e è materiale raro: il mercato è piccolo ma poco servito. Resta un rischio commerciale, non tecnico |

---

## 6. Cosa questo piano NON fa

- **Non rende vendibile *Red Hand of Doom*.** Nulla lo rende: l'unica via è non
  citarlo (ADR-0018 §1).
- **Non tocca la campagna al tavolo.** Il ramo privato continua con Moradin, i
  Realms e la Mano Rossa. Il gioco non cambia.
- **Non vende l'arco 09** — 195.739 parole fuori dalla v1, ed è il costo dichiarato.
- **Non sostituisce un avvocato IP.** La somiglianza sostanziale non è
  autocertificabile: questo piano prepara il materiale della valutazione, non la
  valutazione.

---

## Checklist

```
E0 fondamenta
□ E0.1 ⭐ build_commercial_edition.py + substitutions.yaml (derivato, non copiato)
□ E0.2 check ip/forbidden-term nel contratto unico (severità per edizione)

E1 ambientazione
□ E1.3 fazione antagonista (659+225 occorrenze) — il più facile, per tarare
□ E1.1 ⭐ pantheon: divinità artigiana originale (1.502) — DECIDE la fattibilità
□ E1.2 geografia e fazioni dei Realms (~2.900)

E2 de-derivazione
□ E2.1 passata di somiglianza sostanziale per arco → tabella per l'avvocato
□ E2.2 rigenerazione arco 00

E3 edizione
□ E3.1 OGL 1.0a + Compatibility License PF1e + Product Identity  [gate: avvocato]
□ E3.2 mappe dai map pack + provenienza immagini
□ E3.3 impaginazione, guida DM, playtest esterno, pubblicazione
```

> **Regola d'oro dei piani**: chi chiude un lotto aggiorna — nello stesso commit —
> questa checklist, la riga in `plans/INDEX.md` e una riga in `plans/CHANGELOG.md`.
