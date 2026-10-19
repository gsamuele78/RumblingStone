# Skullcrusher il Nero — drago nero ancestrale [POINTER — statblocco nell'arco] [RIMANDO]
**Key stats**: → `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` Appendice A.1 e `07_il Portale Della Forgia Eterna/ERRATA-ARC07-35-Verification.md` §2.3 (i numeri stanno li'; duplicarli qui creerebbe una seconda copia che diverge alla prima errata — ADR-0021).

**Faction**: orda-antica-372dr | **Role**: flier | **Environment**: aerial | **CR**: 12
> 🕰️ **Fazione d'epoca.** L'assedio di Hammerfist è del **~372 DR**, mille anni
> prima della Mano Rossa: tenerli insieme farebbe proporre a `suggest_encounter`
> un incontro che mescola due ere e non può esistere. `orda-antica-372dr`
> esisteva già per Balvar Fuocospento, il consigliere della stessa orda.
**Source**: `07_il Portale Della Forgia Eterna/ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md` Appendice A.1 e `07_il Portale Della Forgia Eterna/ERRATA-ARC07-35-Verification.md` §2.3 (statblocco nel master DEFINITIVO, Appendice A.1 — GS 14 Avanzato, vale 15: CA 33, 37 con *armatura magica* già addosso al duello, 297 pf, soffio acido 14d4 Riflessi CD 28; il duello della battaglia antica di ~372 DR, Scena 11. I numeri di ERRATA §2.3, GS 12, sono superati dal master)
**Status**: POINTER — NON duplicare lo statblock qui. Usare sempre il file d'arco.

## Summary

**Il capostipite della stirpe di Fauci di Palude**, mille anni prima della campagna. Come cade lo decide il duello: i PG lo affrontano nel viaggio a ~372 DR, e la Corona mostra le due immagini sovrapposte — questo drago adesso, e Fauci di Palude sopra una Hammerfist che brucia.


Questa voce esiste perché `build_monster_catalog.py` e `suggest_encounter.py` scansionano `Bestiario/` per popolare il pool degli incontri: senza, una creatura con statistiche scritte non è raggiungibile da nessuno strumento. Ogni modifica va fatta nel file d'arco.

Boost log: 2026-10-07 — template Avanzato PF1e, versione completa (+4 a tutte le caratteristiche, +2 di armatura naturale; SRD drago nero adulto maturo sotto) — CR 14 → 14 (vale 15, il GS non sale per scelta del DM, Q37) — più forte senza salire di EL. Numeri nel file d'arco, Appendice A.1.

## Notes

🔎 **Questa voce ha sbagliato fonte due volte, e la seconda l'ha trovata la misura.** La prima stesura puntava a `_ARCHIVIO/PortaleForgia-P6-INTEGRAZIONE-Completa.md`, che il drago lo **nomina** soltanto — l'ha trovato il cancello di D18, che vedeva due voci «Skullcrusher il Nero». La correzione la spostò su `_ARCHIVIO/PortaleForgia-P5-FASTPLAY.md`, e **anche quella era sbagliata**: quel file non porta **nessuna** marca di statblocco. I numeri sono sempre stati nel master vivo, `ARC07-DEF-4` §4. `ERRATA-ARC07-35-Verification.md` §2.3 li dichiara per esteso e resta la fonte dell'errata sul GS.

✅ **GS 12 — deciso dal DM il 2026-09-17.** La riga di `PortaleForgia-P6-INTEGRAZIONE-Completa.md` diceva `CR 11` e quella di `Mappe/ARC07-MAPPE-DEFINITIVO.md` r.558 diceva **GS 12**: vale il secondo, e il file d'archivio porta adesso l'errata accanto alla riga.

🔴 **Terzo «Skullcrusher» del repo**, e i tre non vanno confusi: *Grom Skullcrusher* (Barbaro 14, Torneo di Dauth), *Ogre Skullcrusher* (GS 5), e questo drago. E' la forma d'errore che `test_grom_non_e_l_ogre_skullcrusher` già presidia.

🔎 **Ripuntato al master vivo il 2026-09-18.** Questa voce citava `_ARCHIVIO/`, e la misura ha mostrato che non serviva: **lo statblocco è nel master DEFINITIVO**, con gli stessi numeri. `ARC07-MATRICE-VERSIONI.md` dichiara quelle righe **MASTER** al passato — «era la versione viva *prima* del consolidamento» — e leggerle al presente faceva puntare il Bestiario a una generazione superata invece che al file che si apre al tavolo.

✅ **GS 14 — allineato al master il 2026-10-19 (giro 4).** Il GS 12 del 2026-09-17 è stato superato dal template Avanzato di Q37 (2026-10-07): il master DEF-4, Appendice A.1, dà **GS 14, CA 33/37, 297 pf, soffio 14d4 CD 28**. Il nome del file resta `-cr12.md` **di proposito** (indicazione del coordinatore del giro 4), e per questo resta 12 anche il campo `CR` dell'intestazione: `validate_bestiario.py` boccia un campo diverso dal numero nel nome del file. **Il GS vero è 14**, ed è quello della riga `Source`. Per portare anche il catalogo a 14 serve rinominare il file in `-cr14.md`, seguire i rimandi e rigenerare `scripts/monster_catalog.yaml`: è un lotto a parte. ERRATA §2.3 porta ancora il GS 12 e va aggiornata a parte. La frase «cadde sotto Aegis Fang impugnata da Thorgrim» è stata tolta dal Summary: è il duello dei PG a deciderlo, e chi infligge il colpo finale è una domanda aperta al DM (`plans/esperimenti/giro4-arc07-2026-10-19/DECISIONI-DM.md`).

⚠️ **L'ERRATA resta fra le fonti dichiarate, e non è pignoleria.** Togliendola dalla riga `Source` per un momento, il catalogo è tornato a **due** record «Skullcrusher il Nero»: la deduplica funziona proprio così, una fonte dichiarata da un POINTER non viene indicizzata per conto suo. Chi dichiara meno fonti non semplifica: **crea doppioni**.
