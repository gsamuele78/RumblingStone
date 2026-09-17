# Skullcrusher il Nero — drago nero ancestrale [POINTER — statblocco nell'arco] [RIMANDO]
**Key stats**: → `07_il Portale Della Forgia Eterna/_ARCHIVIO/PortaleForgia-P6-INTEGRAZIONE-Completa.md` (i numeri stanno li'; duplicarli qui creerebbe una seconda copia che diverge alla prima errata — ADR-0021).

**Faction**: red-hand | **Role**: flier | **Environment**: aerial | **CR**: 12
**Source**: `07_il Portale Della Forgia Eterna/_ARCHIVIO/PortaleForgia-P6-INTEGRAZIONE-Completa.md` (statblocco d'arco, drago nero adulto; battaglia antica di ~372 DR (ARC-07 P6))
**Status**: POINTER — NON duplicare lo statblock qui. Usare sempre il file d'arco.

## Summary

**Il capostipite della stirpe di Fauci di Palude**, mille anni prima della campagna. Cadde sotto Aegis Fang impugnata da **Thorgrim Barbadiferro**; i PG lo affrontano nel viaggio a ~372 DR, e la Corona mostra le due immagini sovrapposte — questo drago adesso, e Fauci di Palude sopra una Hammerfist che brucia.

⚠️ **La fonte sta dentro `_ARCHIVIO/`, e non e' una copia.** `ARC07-MATRICE-VERSIONI.md` la dichiara **MASTER** (D8: il power-up e' voluto). Gli archivi restano fuori dall'**indicizzazione** — una copia farebbe un record doppio, ed e' la regola che `test_archivi_non_indicizzati.py` prova a rovescio — ma un master dichiarato deve restare **raggiungibile**: e' quello che fa questo POINTER, senza indicizzare l'archivio.

Questa voce esiste perche' `build_monster_catalog.py` e `suggest_encounter.py` scansionano `Bestiario/` per popolare il pool degli incontri: senza, una creatura con statistiche scritte non e' raggiungibile da nessuno strumento. Ogni modifica va fatta nel file d'arco.

## Notes

⚠️ **Due numeri dichiarati e non riconciliati**: `07_il Portale Della Forgia Eterna/_ARCHIVIO/PortaleForgia-P6-INTEGRAZIONE-Completa.md` r.25 dice *«Adult Black Dragon CR 11»*, `07_il Portale Della Forgia Eterna/Mappe/ARC07-MAPPE-DEFINITIVO.md` r.558 dice **GS 12** per la mappa tattica BOSS 24x18. Questa voce registra il GS della mappa; la riconciliazione e' del DM.

🔴 **Terzo «Skullcrusher» del repo**, e i tre non vanno confusi: *Grom Skullcrusher* (Barbaro 14, Torneo di Dauth), *Ogre Skullcrusher* (GS 5), e questo drago. E' la forma d'errore che `test_grom_non_e_l_ogre_skullcrusher` gia' presidia.
