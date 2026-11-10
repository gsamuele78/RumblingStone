# Regole complete: inventario di ciò che i plugin hanno e di ciò che la misura non guardava

Richiesta del DM del 2026-11-10: verificare che le regole PF1e siano complete e, dove
non lo sono, completarle come per il 3.5; lo stesso per d20 SRD e 3.5. Si parte da
main f65d78e e dalla misura di ADR-0121.

**Perché un inventario.** «217/217» del PF1e e «605/606» del 3.5 dicono che le righe
*misurate* sono giuste. Non dicono che le regole ci sono tutte. Qui si elencano tutte
le parti di regola che un plugin (`sistemi/*/sistema.toml`) dichiara o che uno strumento
usa, e per ognuna se è misurata contro la fonte.

Fonti: SRD 3.5 `olimot/srd-v3.5-md@c7f30a0c`, PRD `PSRD-Data@76ea4784` (cache di
`riscontro_srd.py`). Misura nuova: `misura_regole_complete.py` (stessa forma di
`misura_plugin_regole.py`). Prima e dopo: `MISURA-PRIMA.md`, `MISURA-DOPO.md`.

## 1. Che cosa c'è e chi lo misura

| Parte di regola | 3.5 | PF1e | d20 | Misura prima di oggi | Misura da oggi |
|---|---|---|---|---|---|
| Tipi di creatura, taglie | ✓ | ✓ | — | ADR-0121 | invariata |
| Classi base, PNG, prestigio (DV, BAB, TS, gradi) | ✓ | ✓ (55) | — | ADR-0121 | invariata |
| Griglie, incantesimi conosciuti | ✓ | ✓ | — | ADR-0121 | invariata |
| Armature e scudi | ✓ | ✓ | — | ADR-0121 | invariata |
| Abilità (nomi) | ✓ | ✓ | — | ADR-0121 | invariata |
| Liste d'incantesimi classe × funzione (3.5) | ✓ | riusate | — | ADR-0121 contro SRD | **ora anche contro il PRD**, perché il plugin pf1e le riusa |
| Incantesimi «solo PF1e» (APG) | — | ✓ | — | nessuna | **nuova** |
| Liste di classe PF1e dal PRD | — | ✓ | — | ADR-0121 (uso) | invariata |
| Soglie PE | ✓ | ✓ (3 tracce) | — | solo 3.5 | **PF1e nuova** |
| PE per GS, difficoltà d'incontro | metodo | ✓ | — | nessuna | **PF1e nuova** |
| Tesoro per incontro | ✓ (`loot_tables.yaml`) | ✓ (3 velocità) | — | nessuna | **nuova, tutti e due** |
| Statistiche dei mostri per GS (Bestiary 1–1) | — | ✓ | — | nessuna | **nuova** |
| Formule (modificatore, TS, CD) | — | — | ✓ | nessuna | **modificatore nuova**; TS già dentro le classi |
| Talenti dei PNG generati | 1 «talento firma» | 1 «talento firma» | — | nessuna | **nuova (uso)** |
| Nomi italiani di condizioni, talenti, incantesimi | lessico | lessico | — | ADR-0110 (termini) | **nuova: copertura contro la fonte** |
| Conformità delle schede | ✓ | ✓ (ADR-0119) | — | cancello | invariata |

## 2. Che cosa ha trovato la misura nuova

| Sistema | Tabella | Esito | Che cosa vuol dire |
|---|---|---|---|
| 3.5 | tesoro per livello d'incontro | 19/20 | EL 19 era 60.000 mo, l'SRD dice 61.000. **Corretto in questo lotto.** |
| 3.5 | talenti dei PNG generati | 0/5 | Un guerriero 7 ne ha 1, la regola gliene dà 7; un mago 7 1 su 3. Lotto 3. |
| PF1e | talenti dei PNG generati | 0/5 | Un fighter 7 1 su 8, gli altri 1 su 4. Lotto 3. |
| PF1e | liste 3.5 riusate dal pf1e | 445 giuste, 0 sbagliate, 181 non verificabili | I 181 sono gli stessi nomi italiani fuori dal lessico già visti nel 3.5. Lotto 2. |
| PF1e | «solo PF1e» | 54/55, 1 non verificabile | *Tamburi tonanti* (Thunderous Drums) non è nel PRD in cache: non si può dire se è giusto. |
| PF1e | PE, PE per GS, tesoro, statistiche per GS, modificatore | tutte giuste | 215 righe nuove misurate, nessun errore. |
| tutti | nomi italiani | 100% | Condizioni, talenti e incantesimi del Core hanno tutti un nome nel lessico. |

## 3. Il «talento firma» viola i prerequisiti

Il guerriero 7 generato ha «Sbilanciare Migliorato» con Int 8. Il talento chiede Int 13
e Maestria in Combattimento (PRD, Improved Trip; SRD uguale). Il generatore sceglie il
talento dal ruolo e non controlla i prerequisiti. Va nel lotto 3 insieme al numero.

## 4. Residui già noti

| Residuo | Stato | Lotto |
|---|---|---|
| 181-185 nomi d'incantesimo 3.5 fuori dal lessico | aperto | 2 |
| «scaglie» letta come armatura | **chiuso in questo lotto**: la chiave è «corazza a scaglie» (nome del lessico), test di regressione con un drago | 1 |
| costrutti minuti e piccolissimi senza pf bonus | nessuna scheda pubblicata li dà: resta dichiarato, non si inventa | — |
| sciamano senza incantesimi di livello 0 | da riscontrare nel PRD (ACG) | 4 |
| prerequisiti delle classi di prestigio | non controllati | 4 |

## 5. Che cosa resta fuori, e perché

- **Testo delle regole** (benefici dei talenti, effetti delle condizioni, descrizioni degli
  incantesimi). Nessuno strumento lo legge; le skill rimandano alla fonte. Il lessico ha
  i nomi ufficiali, ed è quello che serve a `controlla_termini` (ADR-0110).
- **Oggetti magici e prezzi.** `magic_items_srd.yaml` ha 64 oggetti scelti a mano,
  non il catalogo. Da misurare se il DM vuole il generatore di tesori completo.
- **Equipaggiamento dei PNG 3.5.** Il generatore usa la colonna «heroic NPC» del PF1e anche
  in 3.5 (lo dice nel conto): la tabella 3.5 (DMG 4-23) non è nell'SRD.
- **Archetipi PF1e** (395 nel lessico): non servono al generatore di oggi.

## 6. Lotti

1. **Misura estesa e correzioni piccole** (questa PR): `misura_regole_complete.py`, EL 19,
   «corazza a scaglie».
2. **Nomi d'incantesimo 3.5**: allineare i 181 nomi di `incantesimi.toml` al lessico
   ufficiale (ADR-0110), misura: non verificabili da 181 a 0.
3. **Talenti dei PNG**: numero per livello, classe e razza (regola del manuale), scelti
   tra quelli di cui il PNG ha i prerequisiti (PRD e SRD); misura: 0/10 → 10/10.
4. **Prestigio e sciamano**: prerequisiti delle classi di prestigio nel generatore
   PF1e; livello 0 dello sciamano se il PRD lo ha.
