# Arco Post-Hammerfist — quattro creature della Mano Rossa per la fase finale

> **Versione**: v1 (2026-10-18). **Chi la usa**: il DM, in ARC-09.
> **Perché esiste**: la web enhancement di *Red Hand of Doom* (Wizards, 2006)
> mette in campo nove creature che il nostro Bestiario non ha. Quattro servono
> davvero agli archi: gli **abishai** che `…P3-BATTAGLIA-FINALE-STATBLOCCHI-EPICI.md`
> §3 nomina senza statblocco, e tre unità che mancavano alle tabelle di viaggio
> della fase avanzata (`Arco-Post-Hammerfist-INCONTRI-VIAGGIO-CANNATH-VALE.md` §5.1).
> Il confronto completo con la web enhancement è nel resoconto di progetto del
> 2026-10-18 (archivi Wizards).
>
> **Come sono fatte.** Sono creature **del repo**: nome, numeri e capacità sono
> ricostruiti da zero con le regole dell'SRD 3.5, e della fonte resta solo
> l'idea (ruolo, colore, posto nell'orda). La web enhancement dichiara di non
> contenere Open Game Content: nessuno statblock è trascritto, la si cita con
> la pagina, come `[Private — Red Hand of Doom WE, p. X]`.
>
> **La versione scelta è sempre la più forte** che resta la creatura (ADR-0091
> §4-bis): ogni scheda dice cosa la stampa dava, dove la nostra va oltre, e la
> riga PF1e. Il benchmark è la tabella 1-1 di PF1e
> (`skills/pathfinder-1e-srd/references/monster-advancement.md`).
>
> **Dove finiranno.** Le schede seguono la forma di ADR-0091 per poter passare
> in `Bestiario/mostri/` così come sono. Per ora stanno qui, perché il Bestiario
> è in revisione in un altro lavoro.

| § | Creatura | GS | Ispirata a | Dove si usa |
|---|---|---|---|---|
| 1 | Abishai azzurro della Mano | 11 | blue abishai, GS 7 (WE pp. 29, 33) | guardia del Fane e scorta di Azarr Kul (P3 §3) |
| 2 | Spezzamente del Kulkor Zhul | 12 | Kulkor Zhul mindbender, GS 8 (WE p. 26) | ritualisti del Fane, Thornwaste |
| 3 | Lucertola del tuono | 10 | bluespawn thunderlizard, GS 6 (WE p. 25) | Strada del Deserto, Day 31-42 |
| 4 | Furia della Mano | 10 | blood ghost berserker, GS 4 (WE pp. 7, 12, 25) | fanteria d'urto, Strada del Deserto e Fane |

---

## 1. Abishai azzurro della Mano (GS 11)

# Abishai azzurro della Mano — il cane da guardia di Tiamat (esterno, baatezu) [INFERRED — needs DM confirmation]
**Faction**: red-hand | **Role**: elite-skirmisher | **Environment**: Fane di Tiamat, Nove Inferi | **CR**: 11 | **Source**: ricostruito su SRD 3.5 (tipo esterno, capacità dei diavoli); idea da `[Private — Red Hand of Doom WE, pp. 29, 33]` | **Status**: proposta 2026-10-18

```statblocco
gs: 11
tipo: Medium outsider (baatezu, evil, extraplanar, lawful), 14 DV, LE
ca: 25
ca-dettaglio: (+4 Des, +11 naturale)
pf: 147
ts: Temp +15, Rifl +13, Vol +12
attributi: For 20 Des 18 Cos 22 Int 14 Sag 16 Car 18
velocita: 9 m, volare 18 m (media)
iniziativa: +8
attacchi:
  - Mischia coda +20 (1d8+5 + 2d6 elettricità)
  - Mischia 2 artigli +17 (1d6+2)
  - Mischia morso +17 (1d6+2)
voci:
  - Talenti: Iniziativa Migliorata, Multiattacco, Attacco in Volo, Arma Focalizzata (coda), Riflessi in Combattimento
fonte: ricostruzione del repo su SRD 3.5, 2026-10-18
```

**Iniziativa** +8 · **Sensi** scurovisione 18 m, vedere nell'oscurità; Ascoltare +20, Osservare +20
**Difesa** CA 25, contatto 14, colto alla sprovvista 21 · pf 147 (14d8+84); rigenerazione 7 · TS Temp +15, Rifl +13, Vol +12 · RD 10/bene; RI 22; immune a fuoco e veleno; resistenza ad acido 10 e freddo 10
**Attacco** Vel 9 m, volare 18 m (media) · Mischia coda +20 (1d8+5 più 2d6 elettricità), 2 artigli +17 (1d6+2), morso +17 (1d6+2) · capacità magiche (LI 14): a volontà *charme su persone* (CD 15), *immagine maggiore* (CD 17), *suggestione* (CD 17), *teletrasporto superiore* (solo sé più 25 kg); 3/giorno *fulmine* (CD 17); 1/giorno *catena di fulmini* (CD 20) · evocare baatezu
**Statistiche** For 20 Des 18 Cos 22 Int 14 Sag 16 Car 18 · BAB +14; Lotta +19 · Talenti Iniziativa Migliorata, Multiattacco, Attacco in Volo, Arma Focalizzata (coda), Riflessi in Combattimento · Abilità Ascoltare +20, Concentrazione +23, Intimidire +21, Muoversi Silenziosamente +21, Osservare +20, Raggirare +21 · Linguaggi Comune, Draconico, Infernale; telepatia 30 m · Qualità speciali tratti dei baatezu, vedere nell'oscurità
**Capacità speciali**
- *Rigenerazione 7 (Str)*: l'acqua santa e le armi di allineamento buono infliggono danni letali.
- *Coda del fulmine (Sop)*: ogni colpo di coda scarica 2d6 danni da elettricità.
- *Evocare baatezu (Mag)*: 1/giorno, 2d10 lemuri (100%) oppure un altro abishai azzurro (35%). Vale un incantesimo di 4° livello.
- *Vedere nell'oscurità (Sop)*: vede perfettamente in ogni oscurità, anche magica.
- *Telepatia (Sop)*: 30 m, con qualunque creatura che abbia un linguaggio.

**Tattiche** *Prima del combattimento*: resta sospeso sopra il cerchio dei ritualisti, invisibile ai PG fino al primo segnale; lancia *immagine maggiore* per mostrare un secondo Azarr Kul dove non c'è. · *Durante il combattimento*: apre con *catena di fulmini* sul gruppo più compatto, poi colpisce in volo con Attacco in Volo e torna in quota, puntando l'incantatore che sta interrompendo il rituale. Al primo round in cui un PG lo tiene in mischia evoca rinforzi. · *Morale*: sotto i 40 pf usa *teletrasporto superiore* verso Azarr Kul e torna a combattere accanto a lui; non fugge mai dal Fane finché il suo signore è vivo.

**Hook**: un servo che si crede padrone; parla solo per telepatia e sempre al PG più giovane. *«Lui ti ha già venduto. Io ti offro un prezzo migliore.»*

**Versioni**
- *Stampa 3.5* (`[Private — Red Hand of Doom WE, pp. 29, 33]`): GS 7, 52 pf, 7 DV, RD 10/magia, RI 14. È scritto per PG di 9°-11°.
- *Questa* (più forte): 14 DV, RD 10/bene invece che magia, RI 22, coda elettrica, *catena di fulmini*. ⚠ **Non SRD**: il concetto di abishai non è nell'SRD; ogni capacità usata qui invece lo è (tipo esterno, rigenerazione, RD, evocare baatezu, capacità magiche dei diavoli).
- *PF1e*: nel PRD non ho trovato un abishai; con il template semplice *Advanced* la scheda sale a GS 12 (+2 a tutti i tiri e alle CD, CA +4, pf +28).

Benchmark: PF T1-1 riga 11: CA 25 pari (25) / pf 147 sopra (145) / attacco +20 sopra (+19) / CD 20 pari (20) / TS buono +15 sopra (+14).
Combinazioni ed EL: 2 abishai = EL 13; 4 abishai (la guardia del Fane secondo `…RETHMAR-STRUTTURA.md`) = EL 15; con Azarr Kul (GS 17) restano un rinforzo, non un incontro a parte.
Notes: sostituisce, accanto alle erinni, gli «abishai di scorta (GS 9-11)» che P3 nomina senza scheda.
Boost log: 2026-10-18 — ricostruzione da zero su SRD 3.5 (esterno 14 DV) — GS 7 della stampa → 11 — guardia del Fane per PG di 13° (richiesta del DM: versione più forte).

---

## 2. Spezzamente del Kulkor Zhul (GS 12)

# Spezzamente del Kulkor Zhul — la voce che fa voltare le spade (hobgoblin, mago ammaliatore 12) [INFERRED — needs DM confirmation]
**Faction**: red-hand | **Role**: controller | **Environment**: Fane di Tiamat, colonne dell'orda | **CR**: 12 | **Source**: classe e regole SRD 3.5; idea da `[Private — Red Hand of Doom WE, p. 26]` | **Status**: proposta 2026-10-18

```statblocco
gs: 12
tipo: Medium humanoid (goblinoid), hobgoblin mago 12, LE
ca: 19
ca-dettaglio: (+4 bracciali, +2 Des, +2 deflessione, +1 naturale)
pf: 66
ts: Temp +10, Rifl +9, Vol +14
attributi: For 8 Des 15 Cos 16 Int 22 Sag 12 Car 10
velocita: 9 m
iniziativa: +6
attacchi:
  - Mischia bastone ferrato +5 (1d6-1)
voci:
  - Talenti: Iniziativa Migliorata, Incantesimi Focalizzati (ammaliamento), Incantesimi Focalizzati Superiore (ammaliamento), Incantesimi Inarrestabili, Volontà di Ferro, Scrivere Pergamene, Incantesimi Rapidi, Incantesimi Estesi
fonte: ricostruzione del repo su SRD 3.5, 2026-10-18
```

**Iniziativa** +6 · **Sensi** scurovisione 18 m; Ascoltare +3, Osservare +3
**Difesa** CA 19, contatto 14, colto alla sprovvista 17; con *scudo* 23 · pf 66 (12d4+36) · TS Temp +10, Rifl +9, Vol +14 · con *pelle di pietra* RD 10/adamantio (fino a 120 danni)
**Attacco** Vel 9 m · Mischia bastone ferrato +5 (1d6−1) · incantesimi da mago (LI 12; +14 per superare la RI; scuole proibite evocazione e necromanzia). Ammaliamento con CD 18 + livello: 6° *suggestione di massa* (CD 24); 5° *dominare persone* (CD 23), *debilitazione mentale* (CD 23); 4° *confusione* (CD 22), *charme sui mostri* (CD 22); 3° *blocca persone* (CD 21); 2° *risata incontenibile* (CD 20, anche rapida in uno slot di 6°); 1° *charme su persone* (CD 19). Le altre scuole hanno CD 16 + livello: 4° *invisibilità superiore*, *pelle di pietra*; 3° *dissolvi magie*, *lentezza* (CD 19), *velocità*; 2° *immagine speculare*; 1° *scudo*
**Statistiche** For 8 Des 15 Cos 16 Int 22 Sag 12 Car 10 · BAB +6/+1; Lotta +5 · Talenti Iniziativa Migliorata, Incantesimi Focalizzati (ammaliamento), Incantesimi Focalizzati Superiore (ammaliamento), Incantesimi Inarrestabili, Volontà di Ferro; bonus da mago Scrivere Pergamene, Incantesimi Rapidi, Incantesimi Estesi · Abilità Concentrazione +18, Conoscenze (arcane) +21, Muoversi Silenziosamente +6, Sapienza Magica +23 · Linguaggi Comune, Draconico, Goblin, Infernale, Orchesco · Qualità speciali famiglio (corvo) · Equipaggiamento bracciali dell'armatura +4, anello di protezione +2, amuleto dell'armatura naturale +1, mantello della resistenza +3, fascia dell'intelletto +4, pergamena di *teletrasporto*, bastone ferrato
**Capacità speciali**
- *Mago specialista (ammaliamento)*: un incantesimo in più per livello, solo di ammaliamento. Le CD di ammaliamento contano Incantesimi Focalizzati e la versione Superiore (+2).

**Tattiche** *Prima del combattimento*: *pelle di pietra* e *invisibilità superiore* appena sente l'allarme; si mette dietro la prima fila con un'uscita alle spalle. · *Durante il combattimento*: *dominare persone* sul combattente più forte del gruppo, poi *confusione* su chi resta vicino. *Risata incontenibile* rapida sull'incantatore che prova a dissolvere. Non entra mai in mischia. · *Morale*: senza *pelle di pietra* e sotto i 30 pf legge la pergamena di *teletrasporto* e torna al Fane. Al Fane non ha più dove andare, e resta.

**Hook**: un accademico della guerra che parla ai PG con cortesia, come a una lezione. *«Non vi chiedo di arrendervi. Vi chiedo di guardare chi avete accanto.»*

**Versioni**
- *Stampa 3.5* (`[Private — Red Hand of Doom WE, p. 26]`): GS 8, in coppia nella quarta ondata.
- *Questa* (più forte): mago 12 specialista, CD di ammaliamento fino a 24 con i due talenti di focalizzazione. ⚠ **Oltre la ricchezza SRD**: l'equipaggiamento vale circa 51.000 mo, contro le 27.000 di un PNG di 12° livello. È voluto: è un ufficiale del Fane.
- *PF1e*: il mago ha d6 per DV (pf 78 con le stesse caratteristiche), e il PRD dà all'ammaliatore *Sorriso affascinante* e *Aura di disperazione*. Con la regola PF1e la scheda è un po' più forte; restiamo sul 3.5 perché la campagna gira lì, e la riga serve a chi la porta in PF1e.

Benchmark: PF T1-1 riga 12: CA 19-23 sotto (27) / pf 66 sotto (160) / CD 24 sopra (21) / TS buono +14 pari (+15). È un incantatore: le difese sono gli incantesimi, come per l'arcidruido del Circolo (`Bestiario/png/arci-druido-circolo-cr17.md`).
Combinazioni ed EL: con 2 Furie della Mano (§4) = EL 14; con 2 abishai (§1) = EL 14,5.
Notes: alternativa alla voce 65-80 del Thornwaste, Day 31-42 (`…INCONTRI-VIAGGIO-CANNATH-VALE.md` §5.1). È la sola creatura dell'orda che toglie un PG al gruppo invece di ferirlo: usarne al massimo una per incontro.
Boost log: 2026-10-18 — classe da PNG costruita su SRD 3.5 (mago 12) — GS 8 della stampa → 12 — incantatore di controllo per PG di 13° (richiesta del DM: versione più forte).

---

## 3. Lucertola del tuono (GS 10)

# Lucertola del tuono — progenie azzurra di Tiamat (drago) [INFERRED — needs DM confirmation]
**Faction**: red-hand | **Role**: brute | **Environment**: deserto, margine dello Shaar | **CR**: 10 | **Source**: ricostruito su SRD 3.5 (tipo drago); idea da `[Private — Red Hand of Doom WE, p. 25]` | **Status**: proposta 2026-10-18

```statblocco
gs: 10
tipo: Large dragon (earth), 12 DV, LE
ca: 24
ca-dettaglio: (-1 taglia, +15 naturale)
pf: 138
ts: Temp +13, Rifl +8, Vol +9
attributi: For 26 Des 10 Cos 21 Int 6 Sag 12 Car 8
velocita: 12 m, scavare 6 m
iniziativa: +4
attacchi:
  - Mischia morso +20 (2d6+8 + 1d6 elettricità)
  - Mischia 2 artigli +17 (1d8+4)
voci:
  - Talenti: Attacco Poderoso, Multiattacco, Arma Focalizzata (morso), Iniziativa Migliorata, Incalzare
fonte: ricostruzione del repo su SRD 3.5, 2026-10-18
```

**Iniziativa** +4 · **Sensi** scurovisione 18 m, visione crepuscolare, percezione cieca 9 m; Ascoltare +9, Osservare +9
**Difesa** CA 24, contatto 9, colto alla sprovvista 24 · pf 138 (12d12+60) · TS Temp +13, Rifl +8, Vol +9 · immune a elettricità, paralisi e sonno
**Attacco** Vel 12 m, scavare 6 m · Mischia morso +20 (2d6+8 più 1d6 elettricità), 2 artigli +17 (1d8+4) · Spazio 3 m; Portata 1,5 m · soffio, ruggito del tuono
**Statistiche** For 26 Des 10 Cos 21 Int 6 Sag 12 Car 8 · BAB +12; Lotta +24 · Talenti Attacco Poderoso, Multiattacco, Arma Focalizzata (morso), Iniziativa Migliorata, Incalzare · Abilità Ascoltare +9, Osservare +9, Saltare +16 · Linguaggi Draconico (capisce, parla poco)
**Capacità speciali**
- *Soffio (Sop)*: linea di 18 m, 8d8 elettricità, Riflessi CD 21 dimezza, una volta ogni 1d4 round. La CD è basata sulla Costituzione.
- *Ruggito del tuono (Sop)*: 1/giorno, azione standard, esplosione di 6 m centrata su di sé: 4d6 danni sonori; Tempra CD 21 o assordati e frastornati per 1 round. Capacità originale del repo.
- *Scavare*: si muove sotto la sabbia e sbuca in mezzo a una colonna in marcia.

**Tattiche** *Prima del combattimento*: aspetta sotto la sabbia lungo la pista; i PG la notano con Osservare CD 25 (la sabbia vibra). · *Durante il combattimento*: sbuca in mezzo al gruppo e usa subito il ruggito, poi il soffio in linea su chi è rimasto allineato. In mischia carica l'incantatore. · *Morale*: sotto i 30 pf si rintana sotto la sabbia e scappa; se c'è un'altra lucertola viva, resta.

**Hook**: una bestia da traino diventata arma; porta ancora il collare di bronzo dei carrettieri della Mano. *Il ruggito si sente prima che la sabbia si apra.*

**Versioni**
- *Stampa 3.5* (`[Private — Red Hand of Doom WE, p. 25]`): GS 6, 69 pf, 6 DV, cinque esemplari nella terza ondata.
- *Questa* (più forte): 12 DV, soffio 8d8 CD 21, ruggito del tuono. ⚠ **Non SRD**: la progenie di Tiamat non è nell'SRD; il tipo drago, l'avanzamento e il soffio seguono le sue regole.
- *PF1e*: con *Advanced* GS 11 (morso +22, CD 23, CA 28, pf 162).

Benchmark: PF T1-1 riga 10: CA 24 pari (24) / pf 138 sopra (130) / attacco +20 sopra (+18) / CD 21 sopra (19) / TS buono +13 pari (+13). Picchia come un GS 11.
Combinazioni ed EL: 2 = EL 12; 3 = EL 13 (il tetto della tabella di viaggio in fase avanzata).
Notes: alternativa alla voce 73-86 della Strada del Deserto, Day 31-42 (`…INCONTRI-VIAGGIO-CANNATH-VALE.md` §5.1).
Boost log: 2026-10-18 — ricostruzione da zero su SRD 3.5 (drago Grande, 12 DV) — GS 6 della stampa → 10 — unità della fase avanzata per PG di 13° (richiesta del DM: versione più forte).

---

## 4. Furia della Mano (GS 10)

# Furia della Mano — chi grida il nome dei suoi morti (hobgoblin, barbaro 10) [INFERRED — needs DM confirmation]
**Faction**: red-hand | **Role**: brute | **Environment**: qualunque, in squadre di 3-4 | **CR**: 10 | **Source**: classe e regole SRD 3.5; idea da `[Private — Red Hand of Doom WE, pp. 7, 12, 25]` | **Status**: proposta 2026-10-18

```statblocco
gs: 10
tipo: Medium humanoid (goblinoid), hobgoblin barbaro 10, CE
ca: 20
ca-dettaglio: (+6 corazza di piastre +1, +2 Des, +1 deflessione, +1 naturale)
pf: 105
ts: Temp +13, Rifl +7, Vol +6
attributi: For 21 Des 15 Cos 18 Int 10 Sag 12 Car 8
velocita: 12 m
iniziativa: +6
attacchi:
  - Mischia ascia bipenne +1 +17/+12 (1d12+8/x3)
voci:
  - Talenti: Attacco Poderoso, Incalzare, Arma Focalizzata (ascia bipenne), Iniziativa Migliorata
fonte: ricostruzione del repo su SRD 3.5, 2026-10-18
```

**Iniziativa** +6 · **Sensi** scurovisione 18 m; Ascoltare +14, Osservare +1
**Difesa** CA 20, contatto 13, colto alla sprovvista 20 (schivare prodigioso); in ira CA 18 · pf 105 (10d12+40); in ira 125 · TS Temp +13, Rifl +7, Vol +6; in ira Temp +15, Vol +8 · RD 2/—; schivare prodigioso migliorato; percepire trappole +3
**Attacco** Vel 12 m · Mischia ascia bipenne +1 +17/+12 (1d12+8/×3); in ira +19/+14 (1d12+11/×3) · ira 3/giorno
**Statistiche** For 21 Des 15 Cos 18 Int 10 Sag 12 Car 8 · BAB +10/+5; Lotta +15 (in ira +17) · Talenti Attacco Poderoso, Incalzare, Arma Focalizzata (ascia bipenne), Iniziativa Migliorata · Abilità Ascoltare +14, Intimidire +12, Saltare +18, Scalare +15 · Linguaggi Comune, Goblin · Equipaggiamento corazza di piastre +1, ascia bipenne +1, cintura della forza del gigante +4, amuleto della salute +2, mantello della resistenza +2, anello di protezione +1, amuleto dell'armatura naturale +1
**Capacità speciali**
- *Ira (Str)*: 3/giorno, For e Cos +4, Volontà +2, CA −2, per 9 round.
- *Schivare prodigioso migliorato (Str)*: non può essere colto alla sprovvista né attaccato ai fianchi da chi ha meno di 14 livelli da ladro.
- *Grido dei morti (Str)*: quando entra in ira grida il nome di un compagno caduto; le altre Furie entro 9 m che lo sentono ottengono +1 morale ai tiri per colpire per quel round. Capacità originale del repo, nessun effetto magico.

**Tattiche** *Prima del combattimento*: avanza in squadra di quattro, in fila, dietro a uno scudo di fanteria regolare. · *Durante il combattimento*: entra in ira al primo round e carica; Attacco Poderoso a −5 su chi ha la CA più bassa. Incalzare sui feriti. · *Morale*: non si ritira mai in ira. Finita l'ira, sotto i 25 pf si arrende se nessun ufficiale lo vede.

**Hook**: ogni Furia porta al collo un nastro rosso per ogni compagno morto e li conta prima della battaglia. *«Questo era Gresh. Questo era Ulk. Tu sarai il nastro di qualcun altro.»*

**Versioni**
- *Stampa 3.5* (`[Private — Red Hand of Doom WE, pp. 7, 12, 25]`): GS 4, a gruppi fino a ventiquattro.
- *Questa* (più forte): barbaro 10 con equipaggiamento d'élite. ⚠ **Oltre la ricchezza SRD**: circa 31.700 mo contro le 16.000 di un PNG di 10° livello.
- *PF1e*: l'ira PF1e dà gli stessi +4/+4 e aggiunge i *poteri d'ira*; con *Sangue di bestia* o *Forza sovrumana* la Furia picchia più forte. Con il solo *Advanced* sale a GS 11.

Benchmark: PF T1-1 riga 10: CA 20 sotto (24) / pf 125 in ira poco sotto (130) / attacco +19 in ira sopra (+18) / danno con Attacco Poderoso ~45 pari (45) / TS buono +15 sopra (+13). Cannone di vetro voluto, come gli ogre frantumapietra.
Combinazioni ed EL: 3 = EL 13; 4 = EL 14. Come unità di massa (24 Furie) vanno nel sistema AU/DU/PFU di `08_La Battaglia Di Hammerfist/mass_combat_guide_Dm.md`, non in un incontro.
Notes: alternativa alla voce 28-42 della Strada del Deserto, Day 31-42 (`…INCONTRI-VIAGGIO-CANNATH-VALE.md` §5.1), e squadra per la breccia del Fane.
Boost log: 2026-10-18 — classe da PNG costruita su SRD 3.5 (barbaro 10) — GS 4 della stampa → 10 — fanteria d'urto per PG di 13° (richiesta del DM: versione più forte).

---

## 5. Cosa non è entrato, e perché

| Creatura della WE | Perché resta fuori per ora |
|---|---|
| Doom Fist Monk | il monaco 3.5 regge male oltre il 10° livello; la Furia (§4) copre già lo stesso posto con meno conti |
| Lesser Bonedrinker | il Thornwaste ha già deathlock, naga d'ossa e leoni scheletrici; un quarto non-morto non aggiunge un ruolo |
| Wyrmlord Ulwai Stormcaller | coperta da `Bestiario/villain/emissario-red-hand-cr12.md` (lo dice `…P3-Ghostlord-LICH-ALLEANZA-STATBLOCCHI.md` §3) |
| Varanthian, Skather | PNG unici del libro con un loro posto nella trama di Brindol; la campagna non passa da lì |
