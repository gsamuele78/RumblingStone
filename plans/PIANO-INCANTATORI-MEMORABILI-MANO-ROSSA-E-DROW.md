# PIANO — Incantatori memorabili: Mano Rossa e drow di Sonjak

> **Origine**: richiesta DM (2026-08-02). *«Aggiungere fra le file della Mano
> Rossa qualche incantatore forte oltre agli sciamani e ai war adept: un
> generale ogre magi con livelli da elementalista capace di tenere testa al
> gruppo con i loro artefatti, o una combinazione di incantatore e forza bruta
> che sopravviva più di qualche round. Comprimari più brutali, tipo la versione
> sotterranea degli ogre. E per i drow qualche incantatore subdolo in più
> comandato dalla matrona Sonjak.»*
>
> **Stato**: 🟢 eseguito (lotto unico, 2026-08-02) — **tutto il materiale è
> `[INFERRED — needs DM confirmation]`**: sono proposte, non canone. Nessuna
> riga di `campaign/state.md` è stata toccata.

---

## §0 Risposta breve alla domanda del DM

**Sì, si può fare, e l'ogre magi è la scelta giusta** — per una ragione
meccanica precisa, non solo di colore: il suo kit nativo (volo a volontà,
forma gassosa, invisibilità, rigenerazione) è **l'unico modo pulito, dentro
l'SRD, di far sopravvivere un incantatore a Thorik e Tordek per più di due
round**. Non serve inventargli poteri.

**No, però, non basta alzare il GS.** Contro 4 PG di livello 13 con artefatti,
un mostro solo di GS 17 muore comunque nel round 2 se lo si può raggiungere.
La sopravvivenza di un boss incantatore, a questo tavolo, si compra con
**negazione del contatto**, non con punti ferita. Tutto il piano sta in questa
frase.

---

## §1 Cosa minaccia davvero *Il Rumbling Stone* (analisi onesta)

Fonti: `campaign/state.md` §1/§6, `skills/rumblingstone-campaign/references/campaign-party.md`.

| PG | Difese oggi (stato reale al tavolo) | Superficie d'attacco che resta |
|---|---|---|
| **Thorik** | **Mind Blank permanente** + Volontà Adamantina (Rituale 3 della Corona): niente charme, compulsioni, letture del pensiero, divinazioni. RD 5/epico, CA altissima, +2 deflessione | Danno diretto, **illusioni quasi-reali**, effetti d'area senza TS, terreno, RD che la sua ascia non buca |
| **Tordek** | TS da monaco, RD 5/adamantio, Resistenza al fuoco 10, **Ancoraggio della Montagna 2/g** (immune al movimento forzato), lotta i casters | **−2 DES permanente** (Peso del Mondo, 2026-07-31): CA senz'armatura, Riflessi e iniziativa peggiorati. Ancoraggio è **2 volte al giorno**, non sempre |
| **Hella** | Cura, RD 3/—, Res. Freddo 10, rigenerazione su terra, Rinascita Spontanea 1/g | **Vulnerabilità al fuoco ×1,5** (Ibrido Treant). È la falla più grossa e più bella del gruppo |
| **Artemis** | Volo a volontà, Passo d'Ombra, Res. Fuoco 10, Anello | d6 di DV, TS su Tempra il più debole, **tocchi a distanza** (nessun TS), *polvere scintillante* che gli cancella l'invisibilità, dissolvi sull'Anello |
| **Gruppo** | Trinità Divina 1/g (5 round: +4 TS sacri, immunità paura/charme), niente ladro | Nessuna individuazione trappole affidabile; poca AoE; **la Trinità dura 5 round** — se lo scontro ne dura 8, gli ultimi 3 sono nudi |

### Le tre conclusioni che contano

1. **Gli incantatori mentali sono morti come categoria.** Dopo il Rituale 3
   della Corona, ogni villain costruito su *dominare*, *charme*, *suggestione*
   ha metà arsenale spento contro il tank. Chi resta utile: **illusioni
   quasi-reali**, **danni senza tiro salvezza**, **tocchi a distanza**,
   **controllo del terreno**.
2. **Il fuoco è l'asse morale del gruppo.** L'unico modo di spegnere una
   rigenerazione è il fuoco, e il fuoco è il veleno di Hella. Ogni scontro
   costruito su una creatura rigenerante è automaticamente un **Triangolo di
   Rischio**: Tordek e Artemis devono bruciare, Hella deve stare dove non si
   brucia, e la cura arriva da lei.
3. **L'adamantio è il tema nascosto della campagna.** Corona di Adamantio,
   Pelle di Adamantio, Treant Adamantini, Bracieri di adamantio — e **Aegis
   Fang, che adamantina non è**. Un boss con *pelle di pietra* (RD
   10/adamantio) trasforma questa coincidenza in un puzzle: per due round il
   nano che risolve tutto non buca, e a bucare è chi di solito flanchea.

---

## §2 Perché "più GS" non risolve (i numeri)

Formula EL 3.5 (DMG cap. 3, implementata in `scripts/suggest_encounter.py`):
`EL ≈ 2·log2( Σ 2^(GS/2) )`. Tetto della skill di boosting: **EL ≤ APL+4 = 17**.

- Un mostro solo contro 4 PG perde **3:1 sull'economia delle azioni**,
  qualunque sia il GS.
- Un incantatore PNG 3.5 di GS 16 sta **molto sotto** i benchmark PF T1-1 per
  il suo GS (CA 21 contro 31, ~107 pf contro 200, CD 20 contro 24). È un
  difetto strutturale del sistema, non della build: gli slot di uno Stregone 8
  sono quelli e basta (**un solo incantesimo di 4° conosciuto**).
- Quindi: si compensa con **equipaggiamento da tabella PNG** (bastone del
  fuoco, pergamene di *assorbimento vitale*), **due round di preparazione**
  (un caster che si è pre-buffato vale +1/+2 GS effettivi) e **comprimari che
  assorbono azioni**.

### Le quattro leve che funzionano a questo tavolo

| Leva | Come si realizza | Effetto sul tavolo |
|---|---|---|
| **Negazione del contatto** | volo, *velo di dislocamento*, forma gassosa contro la lotta, gittata | il boss agisce 5-6 volte invece di 2 |
| **Danno senza tiro salvezza** | *muro di fuoco*, *assorbimento vitale* (tocco a distanza, 1d4 livelli negativi), *dardo incantato* | aggira i TS altissimi del gruppo |
| **Terreno che divide** | muro di fuoco, *nebbia solida*, chokepoint | separa Hella dai curati: il vero costo |
| **Uscita di scena** | forma gassosa, *porta dimensionale*, *teletrasporto* | il villain torna, e la seconda volta ha imparato |

---

## §3 Il roster proposto (6 schede nuove)

Tutte nel formato standard `Bestiario/`, tutte SRD, tutte flaggate INFERRED.

### Mano Rossa

| Scheda | Cosa fa | GS | File |
|---|---|---|---|
| **Ghaurush «Cenerevento»** — ogre magi / Stregone 8 | Generale elementalista. Vola, taglia il campo col muro di fuoco, *pelle di pietra* (RD 10/adamantio), rigenerazione 5, esce dalla lotta in forma gassosa. **Tratta prima di combattere** | **16** (variante *Advanced* 17) | `Bestiario/villain/Ghaurush_Cenerevento/` (dossier + statblock) |
| **Ogre Frantumapietra** (Barbaro 6) | Comprimario brutale delle gallerie profonde. **Colpo Tremendo**: spedisce un PG Medio a 3 m e prono. Contro-mossa del party: Ancoraggio della Montagna | **9** | `Bestiario/mostri/ogre-frantumapietra-barbaro6-cr9.md` |
| **Ogre Micelio** (Sporeborn, Barbaro 4) | La versione sotterranea e sbagliata: innesto fungino di Sonjak. Ferocia fino a −10 pf, sbuffo di spore (nausea, **non mentale**), berserk 1/10 round, **vulnerabile al fuoco** | **8** | `Bestiario/mostri/ogre-micelio-sporeborn-cr8.md` |

**Perché l'ogre magi e non un mago hobgoblin**: la Mano Rossa ha già i War
Adept KulkorZhul, i chierici Mano del Fato e i warpriest di Tiamat
(`Bestiario/mostri/`). Manca un comandante che sia **incantatore e mole
insieme** e che non creda alla causa. Ghaurush è un appaltatore con quattro
secoli e un registro contabile: dà alla Mano Rossa una faccia che non urla.

### Drow di Sonjak

| Scheda | Cosa fa | GS | File |
|---|---|---|---|
| **Zin'thara Vel'Ryn «la Voce di Ragnatela»** — Illusionista 9 / Danzatrice delle Ombre 2 | L'incantatrice che **resta pericolosa dopo il Mind Blank di Thorik**: ombre quasi-reali che fanno danno anche a chi è blindato contro il mentale. Nascondersi in piena vista, 44 pf, non si fa mai toccare. Ha in mano le prove dei traffici di Sonjak col Collezionista → **ramo giocabile** | **12** | `Bestiario/villain/Zin_thara_Vel_Ryn/` (dossier + statblock) |
| **Drow Trickster Arcano** (Ladro 3 / Mago 5 / Trickster 2) | **Prestidigitazione a distanza**: ruba a 9 metri. Non gli artefatti legati — ma pozioni, bacchette, e **quello che sta negli zaini** | **11** | `Bestiario/mostri/drow-trickster-arcano-cr11.md` |
| **Drow Assassina di Lolth** (Ladro 4 / Assassino 5) | Attacco Mortale CD 19 dopo 3 round di studio, +5d6 furtivo, invisibilità. Progettata per uccidere **PNG alleati**, non PG | **10** | `Bestiario/mostri/drow-assassina-lolth-cr10.md` |

### Combinazioni e EL (già calcolati)

| Incontro | EL | Riga della tabella di taratura |
|---|---|---|
| Ghaurush + 2 Frantumapietra | **16,5** | APL+3/+4 — boss d'arco, può costare un PG |
| Ghaurush *Advanced* da solo | **17** | tetto assoluto (APL+4): solo con via di fuga segnalata |
| Zin'thara + Assassina + Trickster | **14,3** | APL+1/+2 — set-piece della Notte dei Drow |
| Trickster + Assassina | **12,5** | facile in combattimento, **duro nelle conseguenze** |
| 2 Frantumapietra | **11** | scontro standard |
| 3 Ogre Micelio | **11,2** | ondata, con rischio fuoco amico |

---

## §4 Come si incastrano nella campagna

- **Ghaurush** → incontro di viaggio ARC-09 Giorni 33-38, oppure Rethmar Fase
  1. **Non** all'Arco 08: l'avanguardia ha già Grimjaw e Gorthak.
- **Frantumapietra / Micelio** → scorta di Ghaurush; gli Ogre Micelio cadono
  col **Sabotaggio Campi Drow** se i PG lo fanno (`state.md` §0, ARC-09 P3).
- **Zin'thara + le sue due mani** → campi drow, **Notte dei Drow** (Rethmar
  Fase 0), infiltrazione fra i profughi (`state.md` §2.5).
- **Eco già armato che si può far esplodere** (`state.md` §7.E): il Trickster
  Arcano che sfila il **Seme-Mercato di Varis** dallo zaino di Tordek (E-07b).
  Oppure Ghaurush che lo **chiede in pegno** nella trattativa. In entrambi i
  casi il ramo cambia: da usare solo con l'ok esplicito del DM.
- **Ramo nuovo aperto**: Ghaurush e Zin'thara, indipendentemente, hanno **prove
  che Sonjak tratta col Collezionista alle spalle della Mano Rossa**. È il
  primo cuneo giocabile fra le due fazioni nemiche, e i PG possono arrivarci
  da due strade diverse.

---

## §5 Cosa NON ho fatto (decisioni che spettano al DM)

1. **Non ho toccato `campaign/state.md`.** Nessun clock, nessuna riga di
   conoscenza PNG, nessun villain aggiunto: sono proposte. Le righe da
   aggiungere in caso di approvazione sono scritte in fondo a ciascun dossier.
2. **Non ho usato materiale non-SRD.** Il fomoriano (il "vero" ogre deforme
   del Sottosuolo) sarebbe la scelta di colore più ovvia, ma sta su fonti
   private: se il DM lo vuole, si aggiunge come scheda a parte citando
   `[Private source]`, senza riprodurre testo.
3. **Non ho potenziato PNG esistenti.** Sonjak resta a GS 13 e Zin'thara le
   sta sotto di proposito.
4. **Non ho inventato poteri.** L'unica capacità non attestata è lo **Sbuffo
   di Spore** dell'Ogre Micelio, derivato dalla riga canonica «Sporeborn» di
   `Armate-CALCOLI-ESERCITI-DINAMICI.md` e flaggata.
5. **Aperto**: se il DM vuole Ghaurush come **incantatore puro e più letale**
   invece che caster-bruto, la strada è Ogre magi + Stregone 10 (GS 18), fuori
   dal tetto EL — accettabile solo come «fuggi o muori» segnalato.

---

## Checklist lotti

- [x] **L1** — Analisi difese/superfici del party e leve di design (§1-§2)
- [x] **L2** — Ghaurush: statblock GS 16 + variante *Advanced* GS 17 + dossier
- [x] **L3** — Comprimari ogre sotterranei: Frantumapietra GS 9, Micelio GS 8
- [x] **L4** — Drow subdoli: Zin'thara GS 12 (statblock + dossier), Trickster
      Arcano GS 11, Assassina di Lolth GS 10
- [x] **L5** — Catalogo rigenerato (`build_monster_catalog.py`) e
      `validate_bestiario.py` verde
- [ ] **L6** — *(gated su DM)* approvazione: flag INFERRED → ACCEPTED, righe
      in `state.md` §3/§4, assegnazione token
