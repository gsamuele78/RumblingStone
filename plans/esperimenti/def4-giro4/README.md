# Giro 4 su `ARC07-DEF-4`: la conferma dopo le decisioni del 12 ottobre

Il master letto è quello con D49-D63 applicate (commit `18268dc` del ramo
`claude/project-thread-e860p0`). Le letture sono **un subagente alla volta**:
prima il lettore, poi il playtester, poi il DM a freddo rifatto. Si corregge
fra una lettura e l'altra.

| Lettura | 🔴 | 🟠 | 🟡 | Rapporto |
|---|---:|---:|---:|---|
| lettore (intero, a blocchi, con diario) | 0 | 5 | 16 | `def4-giro4-LETTORE.md`, `def4-giro4-LETTORE-diario.md` |
| playtester (due percorsi, i Treant in tutte e quattro le destinazioni) | 0 | 6 | 17 | `def4-giro4-PLAYTESTER.md` |
| DM a freddo (`lettura_a_scene.py`) | | | | da fare |

Il lettore non è passato da `lettura_a_scene.py` (il percorso del file gliel'ha
dato chi orchestra) e non entra in `letture-a-freddo.json`.

## Il triage del lettore

| # | Rilievo | Esito |
|---|---|---|
| 1 🟠 | la pozione d'invisibilità comprata copre «il primo blocco» o «mezzo blocco» | corretto: mezzo blocco, e quel blocco si tira a Nascondersi |
| 2 🟠 | «ucciso e basta» contro le guardie che scappano gridando | corretto: due domande in ordine, allarme e poi spettacolo; un allarme senza spettacolo costa il successo e basta |
| 3 🟠 | l'indizio del capitano sta nella Scena 5 | spostato in Scena 4, «Il fianco est»; la Scena 5 rimanda |
| 4 🟠 | il §0 della serata non dice che i Treant e il dado dei caduti sono in Scena 5 | aggiunte due righe al §0 |
| 5 🟠 | Zog'tar catturato: il dopo | scritto `[INFERRED]` (la cella, la giustizia del re) e una riga in §7; **D69** al DM |
| 6 | metà di 5 *volare* | 2, per difetto, `[INFERRED]` → D71 |
| 7 | la variante dice *volare* comprato | corretto: la dotazione del re o il volo proprio |
| 8 | le pozioni del re e i 10.000 mo del forziere | un dono a parte, `[INFERRED]` → D71 |
| 9 | «(Scena 5)» per Balvar non sorvegliato | corretto in Scena 6 |
| 10 | Balvar entra nella fortezza in tre modi | allineati: postierla con garanzia e catene anche a piedi; da solo all'alba entra dalla postierla aperta, `[INFERRED]` → D71 |
| 11 | Balvar senza Nascondersi e Muoversi Silenziosamente | −1, dalla CA (armatura completa di mithral), `[INFERRED]` → D71 |
| 12 | quando si sveglia Zog'tar | regola SRD scritta; −8 se imbavagliato, `[INFERRED]` → D69 |
| 13 | il drago senza ordine fra i bersagli | ordine scritto, `[INFERRED]` → D71 |
| 14 | TS di A.1-bis | rifatti: Rifl +18, Vol +20; nono talento e soglia di fuga (~112 pf) scritti → D71 |
| 15 | le wyvern senza numeri | riga SRD nella tabella |
| 16 | il dado dei caduti con due regole | una regola sola: un tiro per tipo di cura, le bacchette un tiro; all'alba se la Scena 10 salta |
| 17 | PX di Zog'tar umiliato o catturato | sconfitto vale come ucciso (DMG); il rimando della Scena 10 riscritto |
| 18 | dodici ore o otto | le prime quattro fra arrivo, porta e consiglio, `[INFERRED]` → D71 |
| 19 | cinque pozioni di *neutralizza veleno* (4°) | **D70** al DM: è nel conto del tavolo del 25 settembre |
| 20 | «sosta» ambiguo | riscritto: un minuto al buio |
| 21 | quanto costa a Balvar finire la lastra | un'azione di round pieno, l'ultima, `[INFERRED]` → D71 |

Tolte anche le sigle di decisione rimaste nel testo stampato (`(D18`, `(D40,
D58)`, `(Scena 5, D62)`), che la CI non boccia ma ADR-0070 non vuole.

## Il triage del playtester

Il playtester ha letto `cbc083c`; D64-D68 (`4981480`) sono arrivate mentre
leggeva, e ne chiudono in parte due rilievi.

| # | Rilievo | Esito |
|---|---|---|
| 1 🟠 | le cariche della Collana | chiuso da D65 (le tre cariche sono una riserva sola, l'eccezione dell'alba è nella scheda) |
| 2 🟠 | *trasporto vegetale* salta la Scena 6 | niente alberi vivi entro 500 m dalla tenda → D74 c |
| 3 🟠 | *silenzio* su Grask e la bolla alla tenda | allarme senza corno → D74 d |
| 4 🟠 | la ronda dopo la pattuglia senza tattica | grida, campo pre-allertato → D74 e |
| 5 🟠 | il Treant senza TS e FOR | FOR 28 e TS dai numeri dei suoi schianti → D74 a |
| 6 🟠 | il bottino della tenda non lo compra nessuno | si vende nel 1372; l'armatura di Zog'tar al re → D74 o |
| 7 | «Due tengono la tenda» senza il costo del mese | scritto nella colonna del costo |
| 8 | la tacca di un Treant alla tenda | 0 → D74 b |
| 9 | un Treant nella tenda è spettacolare? | sì → D74 b |
| 10 | Durik dopo l'ora | resta con Hella → D74 g |
| 11 | il fiuto dei lupi in tacche | una tacca → D74 f |
| 12 | un blocco fallito consuma l'invisibilità | non corretto: le tacche non sono minuti (#23) |
| 13 | l'atterraggio senza prova | prova solo con Grask sveglio → D74 h |
| 14 | chi torna in volo al corno | dentro prima del drago → D74 i |
| 15 | Balvar conta per la metà? | sì → D74 k |
| 16 | il peso di Zog'tar e la forma selvatica | 300 kg, una bestia Grande lo porta → D74 j |
| 17 | gli slot di Hella all'alba | restano spesi, come l'SRD |
| 18 | la breccia con l'attacco a CD 18 | attacco contro CA 28 → D74 l |
| 19 | le wyvern senza tattica | scritta → D74 m |
| 20 | gli aiutanti alla corda | al massimo tre → D74 n |
| 21 | il rimando dell'orologio alla Scena 8 | riga in Scena 8 verso §8 B |
| 22 | la penalità al ritorno | chiusa da D64 e D72 |
| 23 | le tacche e le ore | detto che una tacca non è un'ora → D74 p |
