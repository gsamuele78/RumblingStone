<!-- GENERATO da scripts/inventory_inferred.py — non modificare a mano. -->

# Inventario `[INFERRED]` — il debito di canone, smaltibile a lotti

> Generato. Per rigenerarlo: `python3 scripts/inventory_inferred.py`.
> Il gate è `--check`, e sorveglia **solo la colonna «aperti»**.

## Quanti sono, e quali contano

| Classe | Quanti | Che cosa sono |
|---|---:|---|
| **aperti** | **215** | Documenti vivi: canone, moduli d'arco, bestiario, schede. **È il debito vero**, ed è l'unico numero sorvegliato |
| storici | 126 | `plans/**` e i changelog: *raccontano* un debito, non lo aprono. Contarli renderebbe il totale incapace di scendere |
| meta | 15 | `docs/audit/**`: citano il marcatore **per misurarlo** |

## Prima i record tipizzati — questi hanno già la domanda

Sono le voci `inferred:` di `campaign/state.yaml`: le uniche che portano una **domanda formulata**, rispondibile senza rileggere i file. È la forma verso cui gli altri dovrebbero migrare — un marcatore nudo dice *che* non sai, non *cosa* chiedere.

| ID | Dove | Domanda | A chi | Aperto dal |
|---|---|---|---|---|
| **INF-002** | `archi[08].march_clock` | Il Giorno di Marcia è 19 come dichiara §2.1 («Terrelton just fell as Hammerfist ended»), o ~15 come implica l'orologio Hammerfist a 3g 16h? Sposta i numeri di §2.4 e la finestra quest di ARC-09. | DM | 2026-08-05 |
| **INF-003** | `conoscenze` | La colonna `tempo` di §4 è stata assegnata meccanicamente su 31 righe (parole-chiave: post-siege, Torneo, Cerimonia, Giorni 2x/3x…). Va riletta in una passata sola: quali righe sono davvero conoscenza già acquisita al tavolo? | DM | 2026-08-05 |
| **INF-004** | `conoscenze` | Tre righe canonizzate il 2026-08-05 (Ghaurush, Zin'thara, Ushgar) dicono che quei villain sanno dei «Custodi Eterni», ma il titolo si conferisce nell'Arco 08 che non è ancora giocato. Vanno riformulate come «i quattro nani con gli artefatti», oppure il titolo circola già per altra via? | DM | 2026-08-05 |
| **INF-005** | `villain` | I clock di §3 sono marcati `giocato` (già in moto) tranne Xal'thor e Sethrax, legati al Torneo. Conferma: i clock di Ghaurush 0/6, Zin'thara 2/8 e Ushgar 0/4 stanno già avanzando adesso, o partono con l'Arco 09? | DM | 2026-08-05 |

## Il debito aperto, per area

Ordinato per numero: si smaltisce dall'alto, un'area per tornata.

### Bestiario (PNG, mostri, villain) — 44

- `Bestiario/png/Witchwood_Tiri_Kitor/Witchwood_e_Tiri_Kitor.md` — **12** (righe 9, 18, 21, 35, 52, 55, 68, 69, 72, 77, 86, 89) — needs DM confirmation
- `Bestiario/png/Secondo_Anello_Rethmar/Secondo_Anello_Rethmar.md` — **9** (righe 9, 23, 26, 41, 44, 59, 62, 77, 80) — needs DM confirmation
- `Bestiario/README.md` — **2** (righe 23, 38) — needs DM confirmation
- `Bestiario/mostri/hobgoblin-regular-warrior4-cr3.md` — **2** (righe 1, 4) — needs DM confirmation
- `Bestiario/mostri/orco-regular-warrior4-cr3.md` — **2** (righe 1, 4) — needs DM confirmation
- `Bestiario/png/bothor-malvur-cr6.md` — **2** (righe 1, 4) — needs DM confirmation
- `Bestiario/png/lomyn-redtongue-bardo4-cr3.md` — **2** (righe 1, 4) — needs DM confirmation
- `Bestiario/villain/Urialle/Urialle.md` — **2** (righe 25, 33) — verify col DM
- `Bestiario/villain/balvar-fuocospento-cr13.md` — **2** (righe 1, 5) — creato 2026-07-31 su richiesta DM; dominio Runa = FRCS
- `Bestiario/mostri/bruto-deforme-sottosuolo-cr11.md` — **1** (righe 14) — unica capacità non attestata di questa scheda
- `Bestiario/mostri/hell-hound-mezzoimmondo-cr4.md` — **1** (righe 6) — derivati dal template, .pcg senza export
- `Bestiario/mostri/myconid-guard-cr4.md` — **1** (righe 6) — needs DM confirmation
- `Bestiario/mostri/myconid-sovereign-cr7.md` — **1** (righe 6) — needs DM confirmation
- `Bestiario/mostri/myconid-worker-cr2.md` — **1** (righe 6)
- `Bestiario/png/dauth-commander-mercenari-nani-cr11.md` — **1** (righe 5)
- `Bestiario/villain/Belkram/Belkram.md` — **1** (righe 34)
- `Bestiario/villain/koth-signore-dei-dragoni-cr6.md` — **1** (righe 6) — solo .pcg
- `Bestiario/villain/ozyrrandion-drago-verde-cr8.md` — **1** (righe 7) — needs DM confirmation

### Personaggi e artefatti — 42

- `PG/Artefatti/Artefatti-Pg/Hella/01_Collana_dei_Semi_Eterni.md` — **9** (righe 50, 79, 86, 103, 137, 145, 145, 148, 160) — hook, needs DM confirmation; leva narrativa per il DM, non meccanica; needs DM confirmation
- `PG/schede/artemis.md` — **7** (righe 15, 16, 17, 18, 19, 20, 38) — needs DM confirmation
- `PG/schede/hella.md` — **6** (righe 15, 16, 17, 18, 19, 20)
- `PG/schede/tordek.md` — **6** (righe 15, 16, 17, 18, 19, 20)
- `PG/schede/thorik.md` — **4** (righe 15, 17, 18, 19)
- `PG/Artefatti/ARTEFATTI-MATRICE-VERSIONI.md` — **2** (righe 34, 53) — verificare che il giocatore lo stia usando
- `PG/Artefatti/Artefatti-Pg/Hella/00_Collana-SCHEDA-GIOCATORE-STATO-ATTUALE.hb.md` — **2** (righe 28, 35) — conferma DM; ritmo di ricarica da confermare
- `PG/Artefatti/Artefatti-Pg/Hella/00_Collana-SCHEDA-GIOCATORE-STATO-ATTUALE.md` — **2** (righe 34, 41) — conferma DM; ritmo di ricarica da confermare
- `PG/schede/artemis.yaml` — **2** (righe 22, 36) — needs DM confirmation
- `PG/schede/thorik.yaml` — **1** (righe 11)
- `PG/schede/tordek.yaml` — **1** (righe 2)

### Archi — 09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist — 40

- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/SUPPLEMENTO-P1C-MAPPE-CAMPI-DROW-COMPLETO.md` — **7** (righe 182, 192, 193, 217, 327, 332, 351) — needs DM confirmation
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-HOOKS-Artemis-TorreInvisibile.md` — **5** (righe 11, 184, 190, 216, 293) — da scrivere in Lotto B; sub-quest da scrivere in Lotto B
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2B-Torneo-DAUTH-SUBQUEST-Hella.md` — **5** (righe 4, 43, 73, 141, 150) — Shambling Mound (SRD, plant) con innesto fungino; luogotenente drow di Sonjak; sub-quest da scrivere in Lotto B
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2B-Torneo-DAUTH-SUBQUEST-Artemis.md` — **4** (righe 4, 74, 200, 202) — PNG nuovo di servizio, Umano Esperto 6 / Ladro 3, confermabile dal DM; sub-quest da scrivere in Lotto B
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-TESORO-WBL-AUDIT.md` — **4** (righe 7, 93, 106, 134) — plot item, valore a discrezione
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-HOOKS-Ghostlord-Refugees.md` — **2** (righe 161, 230) — da scrivere in Lotto B; sub-quest da scrivere in Lotto B
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-HOOKS-Hella-SacredForest.md` — **2** (righe 154, 226) — da scrivere in Lotto B; sub-quest da scrivere in Lotto B
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ARMATE-SYNC.md` — **2** (righe 59, 60) — needs DM: encounter di liberazione da scrivere se DM vuole aprire il branch; statblocchi confermati, numeri di dispiegamento da tarare DM-side
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-EVENT-DECK.md` — **2** (righe 57, 147) — needs DM confirmation
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-HANDOUTS.md` — **1** (righe 207)
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2B-Torneo-DAUTH-CONSEGUENZE-ECHI-LUNGO-PERIODO.md` — **1** (righe 63) — Lotto B
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DAY3-CITY-SIEGE.md` — **1** (righe 228)
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P2B-Torneo-DAUTH-DM-MASTER-REFERENCE.md` — **1** (righe 152)
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-ESITI-CONSEGUENZE.md` — **1** (righe 307) — needs DM confirmation
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/Arco-Post-Hammerfist-P3-BATTAGLIA-FINALE-FASE4-CIRCOLO-MYTHAL-STATUE-MAPPA.md` — **1** (righe 113) — soglia esatta al DM
- `09_Continuazione Arco Narrativo dopo Battaglia di Hammerfist/ERRATA-PARTE2-3-35-Verification.md` — **1** (righe 8)

### Canone e stato di campagna — 22

- `campaign/sessions/RETROATTIVI-ARC07-INFERRED.md` — **13** (righe 3, 8, 14, 17, 32, 35, 44, 61, 68, 79, 90, 109…) — needs DM confirmation
- `campaign/templates/mappa-tattica-template.md` — **4** (righe 22, 113, 123, 124) — needs DM confirmation
- `campaign/DM-QUICKSTART-ARC09.md` — **1** (righe 8)
- `campaign/DM-QUICKSTART-NUOVI-DM.md` — **1** (righe 150)
- `campaign/state.md` — **1** (righe 167) — needs DM confirmation
- `campaign/templates/artefatto-vivo-template.md` — **1** (righe 40)
- `campaign/templates/png-dossier-template.md` — **1** (righe 16) — needs DM confirmation

### Archi — 08_La Battaglia Di Hammerfist — 20

- `08_La Battaglia Di Hammerfist/ARC08-10-ESITI-E-CONTINGENZE.md` — **6** (righe 79, 88, 128, 237, 257, 293) — needs DM confirmation
- `08_La Battaglia Di Hammerfist/ARC08-12-CRONOLOGIA-MARCH-CLOCK.md` — **3** (righe 32, 33, 61) — needs DM: pin d'inizio della ricognizione
- `08_La Battaglia Di Hammerfist/ARC08-13-TESORO-WBL-AUDIT.md` — **3** (righe 9, 65, 69) — DMG standard, il DM sceglie con il giocatore
- `08_La Battaglia Di Hammerfist/ERRATA-ARC08-35-Verification.md` — **3** (righe 8, 20, 83)
- `08_La Battaglia Di Hammerfist/ARC08-01-GUIDA-DM.md` — **1** (righe 3194) — stessa riserva
- `08_La Battaglia Di Hammerfist/ARC08-11-PONTE-ARRIVO.md` — **1** (righe 144)
- `08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L1-REVISED-Ultra-Clear.md` — **1** (righe 297)
- `08_La Battaglia Di Hammerfist/Mappe/Hammerfist-L2-REVISED-Ultra-Clear.md` — **1** (righe 323) — needs DM confirmation: dettagli evacuazione fuori da questo file
- `08_La Battaglia Di Hammerfist/hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md` — **1** (righe 1391) — stessa riserva

### Archi — 07_il Portale Della Forgia Eterna — 16

- `07_il Portale Della Forgia Eterna/ARC07-TESORO-WBL-AUDIT.md` — **4** (righe 9, 44, 46, 60) — needs DM confirmation
- `07_il Portale Della Forgia Eterna/ERRATA-ARC07-35-Verification.md` — **3** (righe 10, 30, 114) — needs DM confirmation
- `07_il Portale Della Forgia Eterna/ARC07-ATLANTE-ASSET.md` — **2** (righe 15, 32)
- `07_il Portale Della Forgia Eterna/ARC07-DEF-1-PIANO-TERRA-TERROS.md` — **2** (righe 1417, 1517) — durata 1 round/livello; ruling
- `07_il Portale Della Forgia Eterna/Mappe/Portale-Forgia-L1-REVISED-UltraClear.md` — **2** (righe 257, 407) — needs DM confirmation; soglie/percentuali esatte a discrezione del DM
- `07_il Portale Della Forgia Eterna/homebrew/sessione-terros/ARC07-SESSIONE-TERROS-BOOKLET.hb.md` — **2** (righe 1802, 1902) — durata 1 round/livello; ruling
- `07_il Portale Della Forgia Eterna/Mappe/Portale-Forgia-L2-REVISED-UltraClear.md` — **1** (righe 231)

### Radice del repo — 16

- `CENSIMENTO-MOSTRI-PNG-VILLAIN.md` — **8** (righe 23, 50, 140, 146, 161, 161, 201, 202)
- `PIANO-REVISIONE-LIBRERIA-MOSTRI-PNG-VILLAIN.md` — **7** (righe 31, 33, 123, 125, 166, 196, 204) — needs DM confirmation
- `AGENTS.md` — **1** (righe 92) — needs DM confirmation

### Documentazione — 6

- `docs/guides/GUIDA-BESTIARIO.md` — **4** (righe 82, 89, 98, 204) — needs DM confirmation; …
- `docs/INDEX.md` — **1** (righe 48)
- `docs/tools/README.md` — **1** (righe 77)

### Archi — 00_Red Hand Of Doom — 3

- `00_Red Hand Of Doom/Armate-COMPOSIZIONE-DETTAGLIATA.md` — **2** (righe 4, 6)
- `00_Red Hand Of Doom/Armate-CALCOLI-ESERCITI-DINAMICI.md` — **1** (righe 4)

### Skill degli agenti — 3

- `skills/pathfinder-1e-srd/SKILL.md` — **1** (righe 47) — needs DM confirmation
- `skills/rumblingstone-campaign/references/campaign-coherence.md` — **1** (righe 28) — needs DM confirmation
- `skills/rumblingstone-narrative-style/references/editorial-standards.md` — **1** (righe 65) — needs DM confirmation

### Strumenti — 2

- `scripts/README-automation.md` — **2** (righe 7, 109)

### Archi — 06_Stanza-corona-di-adamantio — 1

- `06_Stanza-corona-di-adamantio/StanzaCoronaDiAdamantio/00-La Corona di Adamantio-ogetto&Prove/_SNAPSHOT-STORICO.md` — **1** (righe 14) — needs DM confirmation

---

**Nudi contro parlanti.** Un `[INFERRED]` senza nota dice *che* qualcosa non è attestato, non *che cosa chiedere al DM*: è contabilizzabile ma non smaltibile. Quando ne tocchi uno, aggiungigli la domanda — o, se riguarda il canone di campagna, promuovilo a record `inferred:` in `campaign/state.yaml`.
