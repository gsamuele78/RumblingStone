# La prova della revisione misurata · ARC-08, da approvare

Il 2026-10-03 il DM ha chiesto di completare la revisione automatica della
prosa, misurando di quanto migliora. Questi quattro documenti sono la prova del
ciclo intero sui file vivi dell'ARC-08: `lotto` ha scritto i pacchetti in
`../lotto-ARC08-2026-10-03/`, un agente ha riscritto i soli passaggi segnalati
dopo aver letto i `references/` di `rumblingstone-narrative-style`, `misura`
ha controllato ogni giro, `revisione` ha scritto i documenti. **Niente è stato
applicato**: si approvano modifica per modifica (D15), come il lotto D13.

## Come si approva

Si spunta `[x]` nella colonna «ok», poi, su un ramo che non sia `main`:

```
python3 scripts/ciclo_prosa.py applica plans/scrittura/revisioni-pilota-ARC08/REVISIONE-….md --data AAAA-MM-GG
```

`applica` scrive la revisione in `plans/scrittura/miglioramenti.json`, e
`ciclo_prosa.py registro` mostra il totale.

## I numeri

| File | Modifiche | Auto | Segnalazioni | MQM |
|---|---:|---:|---|---|
| `Cerimonia-delle-100-Asce.md` | 5 | 4 | 4 → 1 | 99,03 → 99,52 |
| `ARC08-15-HANDOUTS-GIOCATORE.md` | 2 | 1 | 2 → 1 | 98,26 → 98,84 |
| `ARC08-11-PONTE-ARRIVO.md` | 3 | 2 | 2 → 1 | 99,32 → 99,32 |
| `hammerfist_encounters-…-final.md` | 3 | 1 | 3 → 2 | 99,79 → 99,86 |

Il box del ponte non guadagna punti MQM perché il tic che toglie, i tic minori
in gruppo, non è una norma pesata: la soglia di due viene da Humanizer e non è
tarata su questo repo (`REGISTRO-NORME-EDITORIALI.md`). Le segnalazioni scendono
lo stesso.

## Le modifiche da approvare insieme

Il diff spezza una riscrittura in pezzi, e un pezzo può risultare «non
motivato» anche se fa parte della stessa correzione:

- **PONTE, #1 con #2 e #3**: è un solo box riscritto. Da sola la #1 unisce due
  frasi e non toglie niente.
- **HANDOUTS, #1 con #2**: la parentesi si apre nella #1 e si chiude nella #2.
- **encounters, #1, #2 e #3**: «realizzando» diventa «capisce», e il resto
  della frase si accorda.

## Le segnalazioni che restano, e perché

Restano solo segnalazioni «box con più nomi propri». Una revisione di stile non
le può chiudere, perché la garanzia sui fatti vieta di togliere un nome:

| File | Nomi | Perché resta |
|---|---|---|
| PONTE | Corona, Cuore della Montagna, Forgia, Moradin | il nome nuovo è uno solo, il Cuore della Montagna; gli altri il tavolo li conosce da due archi. Il metro conta i nomi distinti, non i nuovi (limite 3 di `misura_craft._registro_dei_nomi`) |
| Cerimonia | Eterni, Hammerfist, Thorek | come sopra: «Custodi Eterni» è il titolo che il re consegna, ed è il punto del box |
| HANDOUTS | Drellin's Ferry | un nome solo, contato due volte: non sta nei dati come nome composto |
| encounters | Mano Rossa, Borin e Dara | «Mano Rossa» non sta nei dati come nome composto; Borin e Dara sono due PNG incisi su due asce, e l'elenco dei nomi è il contenuto del box |

La prova ha trovato un difetto del metro e lo ha corretto: «Fauci di Palude»
valeva due nomi, e in `hammerfist_encounters` chiedeva di toglierne uno in tre
box. Dal 2026-10-03 un nome composto che sta nel Bestiario o in `state.md`
conta uno (`misura_craft._nomi_composti`).
