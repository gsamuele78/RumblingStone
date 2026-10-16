# Ozyrrandion, Drago Verde (Juvenile) [TRANSCRIBED — PCGen, L1 2026-07-08]
**Faction**: dragon | **Role**: flier-boss | **Environment**: swamp | **CR**: 8 | **Source**: PCGen export `Bestiario/pregen-pcgen/png_La_mano_rossa_del_destino/Ozzyrandion green 8 liv.htm` (+ variante `green dragon.htm`; .pcg `Ozyrrandion drago Verde cr8.pcg`) | **Status**: transcribed-pcgen


```statblocco
gs: 8
tipo: Large dragon (air), 14 HD, LE
ca: 26
ca-dettaglio: contatto 9, colto alla sprovvista 26 (-1 taglia, +13 naturale, +1 Armatura Naturale Migliorata, +3 bracciali)
pf: 147
pf-dado: 14d12+56
ts: Temp +13, Rifl +9, Vol +11
attributi: For 23 Des 10 Cos 19 Int 14 Sag 15 Car 16
velocita: 12 m, Volare 45 m (scarsa), nuotare 12 m
iniziativa: +0
sensi: percezione cieca 18 m, scurovisione 36 m, sensi acuti
attacchi:
  - Mischia morso +19 (2d6+6); 2 artigli +19 (1d8+3); 2 ali +19 (1d6+3); coda +19 (1d8+9)
voci:
  - Soffio: cono di 12 m di gas corrosivo, 8d6 acido, Rifl CD 21 dimezza, 1d4 round
  - Talenti: Attacco in Volata, Fluttuare, Multiattacco, Multiattacco Migliorato, Armatura Naturale Migliorata
```

> [INFERRED — needs DM confirmation] `attributi` copiati dalla riga delle caratteristiche di questa stessa scheda da `scripts/genera_attributi.py`.

> [INFERRED — needs DM confirmation] **Versione scelta**: l'export A (`Ozzyrandion green 8 liv.htm`), che è quello col suo nome e torna con la serie SRD del drago verde giovane (For 19, Cos 17 + amuleto della salute +2, CA 26 coi bracciali). L'export B ha For 23 e Car 18 senza un oggetto o una regola che li spieghi. **Conti rifatti sul SRD, senza far scendere i numeri dell'export A**:
> - **pf 147**: la media di 14d12+56 (l'export ne dava 139, sotto la media).
> - **Danni**: in un drago SRD il morso prende la For intera, artigli e ali metà, la coda una volta e mezza. Con For 19 il morso faceva 2d6+4, non +6. Una *cintura della forza del gigante* +4 `[INFERRED]` (For 23) riporta il morso a +6 e alza tutti i tiri per colpire. Artigli e ali restano a metà For (+3) e la coda a +9: sotto il +6 e il +10 dell'export, che non tornano con nessuna For.
> - **Multiattacco Migliorato** `[Private source — Draconomicon]` toglie il malus agli attacchi secondari: tutti a +19.
> - **CD degli incantesimi**: 13 + livello con un *mantello del carisma* +2 `[INFERRED]` (Car 16), come l'export la dava; con Car 14 sarebbe 12 + livello.

> ⚠ Colore ed età: `campaign/state.md` e i riassunti dell'arco 09 lo chiamano «Blue adult» alla Torre Invisibile. Nessun file del repo ha i numeri di un drago blu adulto con questo nome: le due build esistenti sono verdi e giovani, e in RHoD è verde. Qui resta verde; la scelta fra i due la fa il DM. Se diventa adulto, è un altro statblocco.

Large dragon (air), 14 HD, LE. Drago verde SRD; incantesimi da stregone di 1° livello.

**Iniziativa** +0 · **Sensi** percezione cieca 18 m, scurovisione 36 m, sensi acuti; Ascoltare +19, Osservare +19

**Difesa** **CA 26**, contatto 9, colto alla sprovvista 26 · **pf 147** (14 DV) · TS Temp +13, Rifl +9, Vol +11 · immune ad acido, sonno e paralisi

**Attacco** Vel 12 m, Volare 45 m (scarsa), nuotare 12 m · Spazio 3 m, portata 1,5 m (3 m col morso) · **Mischia** morso +19 (2d6+6), 2 artigli +19 (1d8+3), 2 ali +19 (1d6+3), coda +19 (1d8+9) · **Soffio** (Sop) cono di 12 m di gas corrosivo, 8d6 acido, Rifl CD 21 dimezza, ogni 1d4 round · **Incantesimi da stregone** (LI 1°; CD 13 + livello; 5/4 al giorno): 1° — *charme su persone, armatura magica*; 0 — *spruzzo acido, individuazione del magico, individuazione del veleno, distruggere non morti*

**Statistiche** For 23, Des 10, Cos 19, Int 14, Sag 15, Car 16 · BAB +14; Lotta +24 · **Talenti** Attacco in Volata, Fluttuare, Multiattacco, Multiattacco Migliorato `[Private source — Draconomicon]`, Armatura Naturale Migliorata · **Equipaggiamento** amuleto della salute +2, bracciali dell'armatura +3, cintura della forza del gigante +4 `[INFERRED]`, mantello del carisma +2 `[INFERRED]`, pozione di *cura ferite gravi* · **Linguaggi** draconico

**Capacità speciali**
- **Respirare sott'acqua** (Str): respira e combatte sott'acqua senza penalità, e può usare il soffio anche lì.
- **Fluttuare**: se resta sospeso vicino al suolo alza una nube di polvere o d'acqua che dà occultamento a chi è sotto.

**Tattiche**
- *Prima del combattimento*: sorvola il ponte o la Torre in alto, fuori tiro, e studia i PG. Si lancia *armatura magica* (CA 30) quando li vede arrivare.
- *Durante il combattimento*:
  - **Round 1**: picchiata e soffio sul gruppo raccolto, poi risale con Attacco in Volata.
  - **Round 2-3**: Attacco in Volata sui PG isolati (morso, poi via), mai fermo vicino ai guerrieri. Soffio ogni volta che si ricarica.
  - **Round 4 e seguenti**: se i PG non volano, si mette a fluttuare sopra di loro per l'attacco completo nella nube di polvere che si alza; se volano, li porta sopra la gola o l'acqua.
  - Contro un incantatore che lo minaccia: *charme su persone* sul suo guerriero.
- *Morale*: sotto 60 pf chiude le ali e si lascia cadere nella gola o nell'acqua, dove respira e loro no, e beve la pozione. È il più giovane dei draghi della Mano Rossa e ci tiene alla pelle: non muore per Koth.
> [INFERRED — needs DM confirmation] Tattiche scritte da un agente sui poteri della scheda e sui consigli per Ozyrrandion della guida per il DM in `campaign/lore`.

**Benchmark** PF T1-1 riga 8 (CA 21, pf 100, att. +15, danno medio 35, CD 18): CA 26 ✓ · pf 147 ✓ · att. +19 ✓ · danno completo ≈ 45 ✓ · CD 21 ✓. I numeri valgono un GS 10-11: il GS 8 è quello del drago giovane SRD senza oggetti.

**Variante export B** (`green dragon.htm`): hp 147, AC 23, Init +1, morso +18 (3d6+6), For 23 senza fonte — seconda generazione della stessa build; superata dalla A con la cintura.

Notes: il drago verde del Ponte della Gola del Teschio (RHoD). ⚠️ CR: l'export PCGen calcola 6, ma il filename DM e il MM (juvenile green) dicono **CR 8** — qui vale 8 `[INFERRED — needs DM confirmation]`.

Boost log: correzione sul SRD con due oggetti — GS 8 → 8 — pf alla media, danni dei draghi SRD con la cintura +4 che riporta il morso al +6 dell'export, CD 13 + livello col mantello del carisma.

<!-- storico -->
era: pf 139, dall'export A.
era: Forza 19 e Carisma 14 (le altre caratteristiche uguali), trascritti dall'export A da `scripts/genera_attributi.py`.
era: morso +17 (2d6+6); 2 artigli +15 (1d8+6); 2 ali +15 (1d6+6); coda +15 (1d8+10); Lotta +22, dall'export A.
era: CD degli incantesimi 13 + livello con Car 14, dall'export A.
<!-- /storico -->
