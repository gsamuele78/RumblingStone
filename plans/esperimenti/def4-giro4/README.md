# Giro 4 su `ARC07-DEF-4`: la conferma dopo le decisioni del 12 ottobre

Il master letto è quello con D49-D63 applicate (commit `18268dc` del ramo
`claude/project-thread-e860p0`). Le letture sono **un subagente alla volta**:
prima il lettore, poi il playtester, poi il DM a freddo rifatto. Si corregge
fra una lettura e l'altra.

| Lettura | 🔴 | 🟠 | 🟡 | Rapporto |
|---|---:|---:|---:|---|
| lettore (intero, a blocchi, con diario) | 0 | 5 | 16 | `def4-giro4-LETTORE.md`, `def4-giro4-LETTORE-diario.md` |
| playtester | | | | da fare |
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
