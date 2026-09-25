# Artefatti dei PG — audit dei poteri, versione per versione (2026-09-25)

> **Cosa c'è qui.** Per ognuno dei cinque artefatti: quali file esistono, quale
> è la versione definitiva, e una tabella potere per potere con cosa dice ogni
> fonte. Le discordanze hanno la fonte che vince e il perché; quelle che le
> fonti non risolvono sono domande al DM (§7), con una proposta, e **non sono
> scritte come canone** finché il DM non risponde.
>
> **Stato descritto**: il tavolo **prima** della serata del 2026-09-25
> (resurrezione di Hella, viaggio a −1.000 fino al primo ariete). I Doni e il
> Rituale 4 compaiono come caselle da segnare. L'esito della serata lo scrive
> il DM sul ramo del gruppo con `dm.py session end` (ADR-0007).
>
> **Richiesta del DM** (2026-09-25): *«la scheda di Thorik non è aggiornata
> correttamente… controlla bene i poteri di tutti gli artefatti e lo storico
> per eventuali modifiche»*, poi: *«ci sono dei poteri passivi… vedi le schede»*
> e *«fai lo stesso per tutti gli artefatti»*. Fiducia dichiarata dal DM sulle
> fonti: Bracieri alta, Anello bassa, Corona bassissima.

## §0 · Le fonti lette, e con che peso

La gerarchia usata per decidere chi vince, dalla più forte:

1. **Una decisione del DM datata** (`state-changelog.md`, un blocco
   `[CANONE — DM …]` in un master, `STATO-E-ORDINE` §12, la matrice).
2. **La regola del 2026-09-20**: *decide la scheda che il giocatore ha letto*
   (matrice §1, riga del Rituale 4).
3. **Il modulo giocato** (`PortaleForgia-P1`, `P2`, `P3`, `ARC07-DEF-1`), quando
   descrive un effetto che al tavolo è stato dato.
4. Il master dell'artefatto.
5. Le schede e gli export precedenti.

Lette per intero o nelle sezioni degli artefatti: i 14 file di testo, 4 HTML e
2 PDF della cartella della Corona; `LaCorona_di_Adamantio-DM.md` (capitoli
1-3 e scheda finale); `PortaleForgia-P1-REVISED-Corretta.md` §5-7;
`PortaleForgia-P2-REVISED-Corretta-PARTE2.md` §9, §13-15;
`PortaleForgia-P3-PianoFuoco-PARTE2.md` §10; `ARC07-DEF-1` §7b e §9;
`ARC07-DEF-2` §4 (A7); `ARC07-DEF-3` §2-bis, §5, §8-ter; `ARC07-DEF-4`
Scene 1, 12, 13; la regia della serata; `campaign/state.md` §1, §6, §7.E;
`state-changelog.md` 2026-07-02, 07-04, 07-31, 08-01, 09-12; i commit
`e0aa826`, `23d4530`, `c5411ca`, `f93facc`, `53f0aa0`, `f7e75d8`, `b6eef4a`;
`_ARCHIVIO/doni-v1-2026-09-12/`; per l'Anello le due generazioni in
`PG/Artefatti/` e la cartella `Old/`; per Aegis Fang il `.docx` originale.

⚠️ **Non letti**: i PDF binari dell'Anello in `Old/` e in `Cerebromorphosis/`
(sono export delle versioni `.md` lette), e i log delle sessioni vere, che nel
repo non ci sono: `campaign/sessions/` ha una sessione di maggio e i log
retroattivi `[INFERRED]`. Dove il tavolo ha deciso a voce e nessuno l'ha
scritto, questo audit non lo può sapere.

---

## §1 · CORONA DI ADAMANTIO (Thorik)

### Le versioni

| File | Cos'è | Verdetto |
|---|---|---|
| `LaCorona_di_Adamantio-DM.md` | master DM, conversione da PDF | fonte di regole e rituali; **superato** in quattro punti da decisioni successive (§1.3) |
| `000_Guida_Dm_ogetto_prove_rituali_sfide.md` | stessa materia, in markdown pulito | annesso; stesse divergenze del master |
| `00_scheda_Giocatore.md` | la **prima scheda giocatore**: poteri attivi, poteri da risvegliare, i quattro rituali, sinergia con Aegis, giuramento | superata, ma è **la più completa di struttura**: è quella che il DM ricorda |
| `00_Scheda_Giocatore_Aggiornata_Fase2.md`, `01_…Sintesi_Pratica_Fase2.md` | schede dopo il Topazio | superate; portano la **Percezione del Tempo**, che poi sparisce |
| `00_SCHEDA-GIOCATORE-STATO-ATTUALE.md` | scheda viva in markdown, con note DM | la più aggiornata sui costi; conteneva ancora il «−2 COS» dei Doni v1 (corretto qui) |
| `01_Corona_1_Gemma.html` | pagina a una gemma | superata |
| `02_Corona_2_Gemme.html` / `_DM.html` | pagina a due gemme | **incompleta** (§1.2); la `_DM` parlava ancora dei Doni v1 |
| `03_Corona_3_Gemme.html` | pagina a tre gemme | **superata e da non stampare**: Rubino settimanale, Topazio che implode, Aura all'arrivo. Banner messo |
| gli altri `.md`/`.txt` | generazioni precedenti, inglese, scene | snapshot, già marcati nella matrice |

**Nessuna versione era definitiva.** Le nuove `02_Corona_2_Gemme.html` e
`02_Corona_2_Gemme_DM.html` (riscritte il 2026-09-25) lo sono per lo stato a
due gemme, con i poteri in attesa di conferma marcati come tali.

### 1.2 · Potere per potere

Legenda: ✅ c'è ed è coerente · ❌ manca · ⚠️ c'è ma diverso · — non pertinente.
Colonne: **M** master DM · **P** moduli giocati (P1-P3, DEF-1) · **S1** prima
scheda giocatore · **02** pagina a 2 gemme prima di questo audit · **Sk**
`campaign-artifacts.md` · **St** `state.md` §6.

| Potere | M | P | S1 | 02 | Sk | St | Vince, e perché |
|---|---|---|---|---|---|---|---|
| Prerequisiti (nano o mezzonano, BAB +5, fede in Moradin **o** legame con Aegis Fang) | ⚠️ la scheda finale del master chiede anche «un incantesimo divino» | — | ✅ | ❌ | ✅ | — | la formula di S1, ripetuta in `000_…ogetto`, nella pagina a 1 gemma e nella skill. Il banner di T6b dice già che sul prereq vince il master, ma il master si contraddice fra cap. 1 e scheda finale: Thorik è guerriero, e l'incantesimo divino lo escluderebbe dal proprio artefatto |
| Corona di Protezione +2 (deflessione) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | tutti. Il Dono può portarla a +1 (§1.4) |
| Consapevolezza della Pietra | ⚠️ senza Linguaggi | ✅ | ⚠️ senza Trappole | ✅ | ✅ | ✅ | entrambe le liste, DM 2026-07-04 |
| Intuito di Moradin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| Volontà Adamantina | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | immunità **e** +4 (master cap. 3) |
| Manto di Pietra e Spirito | ✅ Rit. 3 | — | ⚠️ Rit. 4 | ✅ | ✅ | ✅ | **Rituale 3**, correzione DM 2026-09-20 |
| RD del Manto | «5/epic and evil» | — | — | «5/epico» `[da confermare]` | — | «5/epico» | **domanda D7** |
| +4 CAR, −2 DES, non rimovibile volontariamente | — | ✅ P1 §5 | — | ❌ | — | ✅ | P1, **DM 2026-09-04**. Mancavano dalla pagina |
| −2 DES / +2 COS del pegno del Rituale 3 | — | ✅ DEF-1 §9 | — | solo nel registro | — | ✅ | DEF-1 §9, rettifica DM 2026-07-31/08-06 |
| **Immunità alla paura** | — | ✅ P1 §5 | ⚠️ solo come sinergia con Aegis | ❌ | ❌ | ❌ | **domanda D3** |
| **Scurovisione 36 m** | — | ✅ P1 §5, ripresa in P2 §10 | — | ❌ | ❌ | ❌ | **domanda D3** |
| **Aura di Comando** 1/giorno (*Comando* CD 15, LI 13) | — | ✅ P1 §5 | — | ❌ | ❌ | ❌ | **domanda D3** |
| **Guida di Moradin** 1/giorno (la direzione verso le gemme) | — | ✅ P1 §5 | — | ❌ | ❌ | ❌ | **domanda D3** |
| Topazio: viaggio 1/mese, 1 ora, 1d10 anni, pegno per i non fedeli | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | DM 2026-07-04 per l'ora |
| **Topazio: Percezione del Tempo** (sa quanto manca a Hammerfist) | — | ✅ P3 §10 | — | ❌ | ❌ | ❌ | **domanda D4**; era sulla scheda Fase 2 che il giocatore ha letto |
| **Topazio: Visione Temporale** (echi del passato dei luoghi) | — | ✅ P3 §10 | — | ❌ | ❌ | ❌ | **domanda D4** |
| **Topazio: Rallentare il Tempo** 1/giorno (*accelerazione* 3 round, solo Thorik) | — | ✅ P3 §10 | — | ❌ | ❌ | ❌ | **domanda D4** |
| Smeraldo: tre effetti 1/settimana, 1.000 mo | ✅ | ✅ DEF-1 | ✅ | ✅ | ✅ | ✅ | — |
| Smeraldo: **Chiave del Tempo** (stabilizza il viaggio) | — | ✅ DEF-1 §9 | — | ❌ | — | — | DEF-1, canone giocato. Aggiunto alla pagina come tratto, non come potere attivabile |
| Rubino | ⚠️ 1/settimana, sbloccato al Rit. 3 | ✅ monouso | ⚠️ 1/settimana | «vuota» | ⚠️ «si accende all'alba» | ✅ speso | **monouso, entra al Rituale 4 e si spende nel ritorno**: D16, `DEF-4` Scene 12-13 (DM 2026-09-19). Il Rubino settimanale del master è superato |
| Rituale 4 → Corona +3 | ✅ | ✅ DEF-4 | — | solo DM | ✅ | ✅ | tutti. Con il Dono: **domanda D5** |
| Rituale 4 → Senzienza | ⚠️ «dopo il Rituale 1, con Aegis» | ✅ DEF-4 | ⚠️ «quando impugni entrambi» | solo DM | — | ✅ | **Rituale 4**: `DEF-4` Scena 12 (DM 2026-09-19), `state.md`, e la scheda Fase 2 che dice *«la piena senzienza al completamento»*. Vedi D2 |
| Rituale 4 → Aura della Forgia Eterna | ⚠️ evento unico all'arrivo | ✅ DEF-4 Momento 4 | — | ❌ | ⚠️ evento unico | ✅ matrice | **dopo il duello, fino all'alba la prima volta, poi 1/settimana**: DM 2026-09-20 |
| Rituale 4 → «la Gemma del Tempo si disintegra» | ✅ | ❌ | — | — | — | — | **superato**: il Topazio resta, si spende il Rubino (D16). Il master descriveva un Rituale 4 di una scena sola |
| Rituale 4 → costi | 1d10 anni + pegno alleati | «senza ulteriori costi» (DEF-4 Scena 12) | — | — | — | — | il rito non costa niente; il **viaggio** col Topazio sì: **domanda D6** |
| Costi dei rituali («Rituale della Donazione») | R1 2.500 mo · R2 12.500 mo · R3 40.500 mo + pegno | R2 pagato (Fase 2); R3 solo pegno (DEF-1) | — | ❌ | — | — | riportati nel registro della pagina. R1: al tavolo non registrato |
| Giuramento del Portatore | ✅ | — | ✅ | ❌ | — | — | reintegrato |

### 1.3 · La sinergia con Aegis Fang: due strati, che il master confonde

`LaCorona_di_Adamantio-DM.md` cap. 3 mette **in un blocco solo** due cose che i
moduli giocati tengono separate:

| Strato | Cosa dà | Fonte | Stato |
|---|---|---|---|
| **Risonanza** (da quando Thorik ha preso la Corona) | +2 sacro a tutti i TS · +1d6 sacro contro caotici o malvagi · *Richiamo Ancestrale* 1/giorno · *Eco degli Eroi* 1/combattimento · *Bane* +3d6 ×4 contro i draghi | P1 §6, P2 §9, `Sinergie_Artefatti_QuickReference.html`, HANDOUT 4 di `P2` | ❌ **assente** da `SINERGIE-ARTEFATTI-MASTER.md` dal 2026-07-03, e **nessuna decisione registra il taglio**. **Domanda D1** |
| **Completamento** (Rituale 4) | Corona senziente · Aegis +4 Sacra Ritornante, Ego 20 · telepatia coi nani 90 m · nani vicini immuni alla paura · *Guarigione* 1/giorno | master cap. 3, `05_Aegis_Fang_Final_Awakening.html`, `DEF-4` Scena 12 | ✅ canone al Rituale 4. **Domanda D2** solo per chiudere la lettura del master |

⚠️ Il *Bane* del primo strato (+3d6 ×4 contro **tutti** i draghi) contraddice
`ARC07-DEF-2` A7, dove +3d6 ×4 è il premio **contro Fauci di Palude** e
*«invece di +2d6 vs draghi»*. Dentro D1.

### 1.4 · Il Dono e il Rituale 4

- **Doni v1 superati** (2026-09-12): *Il Sangue della Stirpe* (−2 COS), *La
  Memoria della Battaglia*, *Il Filo dell'Ascia*. Restavano nella pagina DM a
  due gemme e in una nota della scheda markdown; tolti.
- **Doni v4-bis** (canone): Thorik dona il +2 di deflessione, scende a **+1**,
  e Hella riceve lo Scudo del Custode. Nella pagina è una casella.
- ⚠️ **Il Rituale 4 non si gioca stasera.** La regia della serata (decisione
  S1) chiude al **primo ariete** (`DEF-4` Scena 10). Il Rituale è la Scena 12:
  **la sessione dopo**. Stasera si gioca solo il Dono.
- ⚠️ **Cosa non dire al giocatore** (`DEF-3` §2-bis e §8-ter): che l'incasso
  vuoto si riempie a −1.000, e che il Rubino si spende. La pagina del giocatore
  dice cosa sblocca il Rituale 4, non dove né cosa costa alla pietra.

---

## §2 · AEGIS FANG (Thorik)

| File | Verdetto |
|---|---|
| `Aegis Fang.docx` / `.pdf` | fonte originale dello Stadio 0; **coincide** col master |
| `00_Aegis_Fang-MASTER-DM.md` | ⭐ master, corretto. Un `[INFERRED]` si risolve dalla sua fonte (sotto) |
| `00_Aegis_Fang-SCHEDA-GIOCATORE-STATO-ATTUALE.md` | corretto (Doni v4-bis) |
| `00_Aegis_Fang_Stadio0.html` / `_DM.html` | **definitive dopo questo audit**; prima portavano ancora il *Filo dell'Ascia* (Doni v1) e non avevano sinergie né la reazione dell'ascia al Dono |
| `05_Aegis_Fang_Final_Awakening.html` | lo Stadio 1, fonte |

| Potere | Fonti | Vince |
|---|---|---|
| Allineamento | `.docx`, master, pagine: **Legale Neutrale**; skill: *Lawful Good* | **LN**, la fonte originale. Skill corretta |
| Poteri inferiori (*cura ferite moderate* 3/g, *resistere all'energia* 1/g) | `.docx`, master, pagina; skill: assenti | aggiunti alla skill |
| *Filo dell'Ascia* | pagine HTML | **superato** (2026-09-12) |
| Reazione al Dono di Thorik | `DEF-3` §5, master, scheda md; HTML: assente | aggiunta |
| Bane contro Fauci (A7) | `DEF-2` §4; si gioca **stasera**, Atto I | casella nella pagina DM, non nella pagina giocatore (è una scoperta) |
| Stadio 1: aura dei comandanti | master: `[INFERRED — effetto non quantificato]` | **risolto dalla fonte**: `05_…Final_Awakening.html` dice *telepatia coi nani entro 90 m* e *nani vicini immuni alla paura* (aura di 18 m nel calcolo del valore) |
| Stadio 1: quando | `.docx`/master: apoteosi all'Assedio + Corona senziente; `state.md`: vittoria dell'Assedio; `DEF-4` Scena 12: una scena | coincidono: tutto al Rituale 4 |

---

## §3 · ANELLO DELL'ILLUMINAZIONE CAOTICA (Artemis)

| File | Verdetto |
|---|---|
| `PG/Artefatti/Ring of Chaotic Illumination.md` | generazione 1, inglese, pre-riforgiatura; ha dettagli dei poteri di crisi che poi cadono |
| `PG/Artefatti/Ring_of_chaotic_illumination-master.md` | generazione 2, «documento riservato DM»: intelligenza (Int 14, Sag 12, Car 16, Ego 12, CB), prova di legame CD 17, lo Scettro di Ylluminuk |
| `Old/` | export delle due generazioni, deprecati |
| `00_Ring_of_Chaotic_Illumination_Revised.md` | ⭐ master (A10), inglese, *Reforged* |
| `00_Ring-SCHEDA-GIOCATORE-STATO-ATTUALE.md` | scheda viva, con il Dono |
| `00_Ring_Riforgiato.html` / `_DM.html` | **definitive dopo questo audit**; prima mancava il Dono |
| `Artemis/Cerebromorphosis/` | sottosistema di crisi, non poteri dell'anello |
| `PrestigeClass/lord_sun_shadow/` | percorso rifiutato: nessun potere in gioco |

| Potere | Revised | Pagine HTML | Generazione 1 / 2 | Moduli giocati | Vince |
|---|---|---|---|---|---|
| Sempre attivi (vista, conoscenze, diplomazia, doppia fiamma) | ✅ | ✅ | vista ✅ | — | Revised |
| Sei poteri attivabili | ✅ | ✅ | tre soli | — | Revised |
| Parole di comando (*Noctis Revelum/Velum* per la vista) | ❌ | ❌ | ✅ | — | colore; aggiunte alla pagina DM come nota |
| Aspetto per chi non è il prescelto | acquamarina blu | — | anello di **resistenza +3** | — | Revised; la versione 1 resta nota DM |
| *Dawn's Defiance* | *Spezzare Incantamento*, immunità 24 h | lato DM | + luce 3 m, **1/settimana** | — | **domanda D9** |
| *Solar Purge* | 1d6/DV alle aberrazioni, anello spento 24 h | lato DM | + cura metà dei danni, toglie un livello negativo | — | **domanda D9** |
| Intelligenza dell'anello (Ego 12) | ❌ «opera con lui» | ❌ | ✅ gen. 2 | — | Revised: **nessun Ego**. La generazione 2 aveva anche il cambio d'allineamento dello Scettro, un filo mai giocato |
| *Dualità Armoniosa* (+1 carica con la Corona entro 9 m) | ❌ | ❌ | — | ✅ P1 §7, P2 §9 | **domanda D9**: il Riforgiato non ha cariche, quindi va tradotta o tolta |
| *Parlare coi Morti* sul corpo di Hella 1/giorno | ❌ | ❌ | — | ✅ P1 §7, «fino alla resurrezione» | temporaneo: **scade stasera**. Nota DM |
| Il Dono (1d6 di *Eldritch Blast*) e le reazioni | scheda md ✅ | ❌ | — | `DEF-3` §5 | aggiunto |
| Sinergie S1-S3 | ✅ | ✅ | — | P2 §9 (+4 all'Alba Oscura) | S1-S3 come nel master delle sinergie (T4, ripetuto dal Revised) |

---

## §4 · BRACIERI GEMELLI DI MORADIN + CINTURA DELLA DEVASTAZIONE (Tordek)

| File | Verdetto |
|---|---|
| `05_Bracieri_Gemelli_Scheda_PG_Completa.md` / `.html` | ⭐ **definitive** (pagina giocatore), con due correzioni sotto |
| `01_Bracieri_Gemelli_di_Moradin.md` | master di struttura e parte DM (il Dono sta qui) |
| `02_`, `03_` | scene dei due risvegli, giocate |
| `04_…Fuoco` | superata dallo stadio Terra |
| `05_…Final.html`, `05_…copy 2.html` | copie deprecate |
| `00_Cintura_della_Devastazione.md` | master della Cintura |

| Voce | Fonti | Vince |
|---|---|---|
| Nomi dei poteri del Fuoco | `01_`: *Pugno di Moradin*, *Salto Infuocato*; `04_`/`05_`: *Pugni di Magma*, *Salto Fiammeggiante*, *Passo di Brace*; skill: i nomi di `01_` | **`05_`**, la scheda che il giocatore ha in mano (regola 2026-09-20). Skill allineata |
| Benedizione della Forgia | DM 2026-07-04: **permanente**; `05_.md`: permanente; `05_.html` e Cintura: «fino al completamento dell'avventura» | **permanente**. HTML e Cintura corretti |
| *Diventare una Collina* | `05_`, `state.md`, changelog 2026-08-01 | ✅ coerenti; mancava dalla skill |
| Stadio Terra | skill: «in completamento»; tutto il resto: giocato | giocato. Skill corretta |
| Il Dono (Ancoraggio della Montagna) | `01_` e `DEF-3` §5 ✅; `05_.html`: solo nella riga delle sinergie | aggiunto come casella |

**Pagina DM**: non esiste in HTML, e non serve una pagina nuova: la parte DM
dei Bracieri è `01_Bracieri_Gemelli_di_Moradin.md`, che ha già il Dono, le
reazioni e la coscienza. Fiducia del DM alta, e l'audit la conferma.

---

## §5 · COLLANA DEI SEMI ETERNI (Hella)

Pagine fatte il 2026-09-25 (PR #177) su decisioni del DM dello stesso giorno:
`01_Collana_Radicata{,_DM}.html`, `02_Durik_Guardiano_di_Pietra{,_DM}.html`.
Confrontate con `DEF-3` §5 e §7, con la skill e con `SINERGIE` §1: coerenti, i
Doni sono già caselle. **Definitive, nessuna modifica.**

---

## §6 · I file toccati da questo audit

| File | Cosa |
|---|---|
| `02_Corona_2_Gemme.html`, `02_Corona_2_Gemme_DM.html` | riscritte complete |
| `03_Corona_3_Gemme.html` | banner «superata, non stampare» |
| `00_SCHEDA-GIOCATORE-STATO-ATTUALE.md` (Corona) | nota 3-ter dei Doni v1 corretta; rimando alle pagine |
| `LaCorona_di_Adamantio-DM.md` | banner con i quattro punti superati |
| `00_Aegis_Fang_Stadio0{,_DM}.html` | Dono v4-bis, sinergie, Stadio 1 e A7 lato DM |
| `00_Aegis_Fang-MASTER-DM.md` | `[INFERRED]` dello Stadio 1 risolto dalla fonte |
| `00_Ring_Riforgiato{,_DM}.html` | Dono, note di crisi e dei moduli giocati lato DM |
| `05_Bracieri_…Completa.html`, `00_Cintura_della_Devastazione.md` | Benedizione permanente; Dono nella pagina |
| `ARTEFATTI-MATRICE-VERSIONI.md` | una riga «versione definitiva» per artefatto |
| `skills/rumblingstone-campaign/references/campaign-artifacts.md` | Aegis LN e poteri inferiori; Corona gemme, Aura, prereq; Bracieri coi nomi della scheda |

---

## §7 · Domande al DM

Una per voce, con la proposta. Nelle pagine, ogni voce aperta porta la
marcatura `[da confermare col DM — D<n>]` e **non è scritta come canone**.
Le stesse domande sono in `plans/PIANO-REVISIONE-TRASVERSALE-COERENZA-E-QUALITA.md`
§3, lotto T10, dove il gate `decisioni_dm` le conta.

| # | Domanda | Proposta |
|---|---|---|
| D1 | **La Risonanza fra Corona e Aegis Fang** (P1 §6, P2 §9, la quick reference data al tavolo): +2 sacro a tutti i TS, +1d6 sacro contro caotici o malvagi, *Richiamo Ancestrale* 1/giorno, *Eco degli Eroi* 1/combattimento. Il master delle sinergie l'ha tolta il 2026-07-03 senza dirlo. È attiva? | **Sì**, dal P1: è nel modulo giocato e nell'handout. Entra in `SINERGIE` come **S0**. Il *Bane* +3d6 ×4 invece resta **solo contro Fauci**, come dice A7: contro gli altri draghi vale il +2d6 della *Dragondoom* |
| D2 | **Il blocco «Sinergia con Aegis Fang» del master** (senzienza, +4 sacra, telepatia, *Guarigione*) si sblocca «dopo il Rituale 1»? | **No, al Rituale 4**, com'è in `DEF-4` Scena 12, in `state.md` e nella scheda Fase 2 (*«al completamento»*). Il master mescola i due strati di §1.3 |
| D3 | **I bonus di quando l'ha indossata** (P1 §5): immunità alla paura, scurovisione 36 m, *Aura di Comando* 1/giorno (*Comando* CD 15, LI 13), *Guida di Moradin* 1/giorno. Il 2026-09-04 ha confermato solo +4 CAR e non-rimovibilità dallo stesso blocco | **Sì a tutti e quattro**: stanno nello stesso elenco di cui metà è già canone, e nessuna fonte li revoca |
| D4 | **I poteri del Topazio** (P3 §10): *Percezione del Tempo* (sa quanto manca a Hammerfist), *Visione Temporale* (echi del passato dei luoghi), *Rallentare il Tempo* 1/giorno (accelerato 3 round, solo lui). E il «+1 a tutti i poteri della Corona»? | **Sì ai tre**: la *Percezione* era sulla scheda Fase 2 che il giocatore ha letto. **No al +1 generico**: non dice a cosa si somma, e nessuna scheda l'ha mai applicato. ⚠️ *Rallentare il Tempo* e l'Eco del Custode sono entrambi *accelerazione*: non si sommano |
| D5 | **La deflessione dopo il Rituale 4, se Thorik ha donato**: +2 (il rito aggiunge uno) o +3 (il rito la porta a +3 comunque)? | **+2**. `DEF-3` §5: *«La Corona protegge di 1 in meno, per sempre»* |
| D6 | **Il Topazio al viaggio a −1.000**: si tira l'invecchiamento di 1d10 anni? E Artemis, che non è né nano né fedele di Moradin, paga il pegno o tira Tempra CD 25? `DEF-4` non ne parla, e la Scena 12 dice «senza ulteriori costi» per il **rito** | **Sì a entrambi, al portale**: sono il prezzo del Topazio, stampato sulla scheda da luglio; D-B esclude i costi del rito, non quelli del viaggio. La *Guarigione del passaggio* non li toglie, come non toglie il −4 DES |
| D7 | **La RD del Manto**: 5/epico o 5/epico **e** male? | **5/epico**: è quel che la scheda del giocatore dice dal 2026-07-31 |
| D8 | **La Senzienza della Corona**: il master le dà Int 16, Sag 17, Car 18, **Ego 20**, gli stessi numeri dello Stadio 1 di Aegis Fang. Li ha entrambi? | **Sì, e la Corona non tira mai l'Ego contro Thorik**: `DEF-4` la vuole voce calda o fredda, con un *Want* suo (la montagna), non un padrone. Se il DM preferisce, niente punteggi |
| D9 | **L'Anello**: (a) i poteri di crisi tornano ai dettagli della prima versione (*Dawn's Defiance* 1/settimana con luce 3 m; *Solar Purge* che cura metà dei danni e toglie un livello negativo)? (b) la *Dualità Armoniosa* dei moduli (+1 carica con la Corona vicina) come si traduce, visto che il Riforgiato non ha cariche? | (a) **No**: vince il Revised, eletto dopo e con la fiducia bassa del DM sulle versioni vecchie. (b) **Tolta**: era scritta per l'anello a cariche della P1, e nessuna scheda del Riforgiato l'ha mai portata |
