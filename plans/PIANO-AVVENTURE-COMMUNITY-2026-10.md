# PIANO — Cosa portiamo dalle avventure della community

**Aperto**: 2026-10-18, su richiesta del DM · **Fonte**: [RICERCA-AVVENTURE-COMMUNITY-2026-10](RICERCA-AVVENTURE-COMMUNITY-2026-10.md) · **Decisione**: [ADR-0092](adr/ADR-0092-le-domande-dell-alto-livello.md) · D1-D3 decise dal DM il 2026-10-18, nessuna aperta

Il DM ha chiesto di confrontare i master DEF, il developer e il playtester con
le migliori avventure della community 3.5 e PF1e, in Italia e fuori, e di
portare ciò che migliora. La ricerca ha proposto tre lotti. Questo piano li
tiene, e il primo è chiuso dalla PR che lo apre.

Regola d'apertura (ADR-0044): nessun piano esistente copre la stessa cosa.
`PIANO-MASTER-DEF-ARC08-ARC09-STANDALONE` scrive i master; questo cambia le
domande che quei master devono superare, e i suoi lotti si applicano lì.

## 1 · I lotti

### Lotto 1 · Alto livello e statblocchi ✅ (2026-10-18)

- [x] FASE 1 in sola lettura: `fase1.py` sui bersagli, registro delle norme (nessuna delle quattro era misurata)
- [x] §9-§16 in `skills/rumblingstone-module-standard/references/sviluppo-degli-incontri.md`, e il rimando nel `SKILL.md`
- [x] D9, D10, D15, D16 in `scripts/domande_developer.py`, con dodici test nuovi
- [x] profili `apl` e residui con la ragione in `plans/domande-developer.json`
- [x] la riga «Statistiche base» e i due stati di *Prima del combattimento* (ADR-0092 §3)
- [x] le righe nel registro delle norme
- [ ] **applicazione**: i master di ARC-08 nascono sotto le regole nuove (S1 di MASTER-DEF); gli 11 statblocchi con una preparazione (§3) prendono la riga quando un lotto li tocca

### Lotto 2 · Il sito come sistema e gli indici ⬜

Il roster dei nemici del sito (normale e in allerta) come componente di
ADR-0074, il foglio dello scontro con il testo breve degli incantesimi, la
tabella degli incontri e l'elenco degli statblocchi generati da `componenti.py`,
l'intestazione di zona. La ricerca, §3.1 P2 e P5 e §3.2. Si applica alle ondate
di ARC-08.

### Lotto 3 · Mappe, playtest, indagine, stile ⬜

Il resto della §3.2 della ricerca. Si apre dopo aver visto se i lotti 1 e 2
trovano difetti veri.

## 2 · La calibrazione del lotto 1

Le quattro regole nuove eseguite sui nove moduli sotto cancello, prima di
attivarle. Ogni rilievo è stato letto a mano.

| Regola | Rilievi | Veri | Falsi | Note |
|---|---|---|---|---|
| D10 la riga di scala | 9 | 6 | 3 | veri: DEF-1 Scena 3, DEF-4 Scene 6, 8 e 10, DEF-5 Scena 3, la rissa del Drappo. Falsi: DEF-4 Scena 7 (lo scontro si gioca nella 8) e i due atti dell'Abbazia, che scala in un indice maestro |
| D9 il segreto e la divinazione | 1 | ½ | ½ | DEF-4: la targa della Scena 3 è un indizio da leggere, non un segreto; la natura di Balvar nella Scena 7 si divina, e il master non dice cosa succede |
| D15 l'orda di GS basso | 1 | 0 | 1 | DEF-4 Scena 6: gli otto hobgoblin non vanno battuti, conta l'allarme |
| D16 il PG fuori gioco | 0 | — | — | **non calibrata**: i quattro effetti trovati avevano tutti una via d'uscita, o erano stordito e frastornato, che non contano |

Il primo tentativo di D9 contava «segreto» e «indizio» scena per scena, e dava
2 veri su 7: la regola è passata a livello di modulo, con la risposta in forma
fissa (il blocco «Se lo divinano»). Precisione d'insieme delle regole nuove:
**6½ su 11**, vicina al 5 su 9 delle regole di settembre. Sono indicatori.

## 3 · La riga «Statistiche base», contata

37 statblocchi del Bestiario hanno *Prima del combattimento*. **11** dichiarano
incantesimi, pozioni o oggetti di preparazione senza la riga; due scrivono già
nel testo quali numeri la includono (Draxoksus «i numeri del blocco»,
Ozyrrandion «CA 35»). Uno è dubbio: l'*unto* di Lirien va sul pavimento, non su
di lei.

Gli undici: Lirien, Tempestas, l'arcidruido del circolo, Avarthel, Morlin
Coalhewer, Azarr Kul, Arbitrax, Draxoksus, l'emissario della Mano Rossa, Koth,
Ozyrrandion. Il conto si rifà con il comando della §5.

## Decisioni del DM

<!-- decisioni-dm: AVVENTURE-COMMUNITY -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | 1 | ✅ **Decisa il 2026-10-18** (il DM: *«sì sono d'accordo»*): la riga «Statistiche base» entra negli undici statblocchi della §3 quando un master li usa, a cominciare da quelli di ARC-08. Niente lotto a sé |
| ~~D2~~ | 1 | ✅ **Decisa il 2026-10-18**: nei cinque master di ARC-07 già giocati le righe di scala **non** si aggiungono; si aggiungono solo se il master serve a un gruppo nuovo (`dm.py gruppo nuovo`) |
| ~~D3~~ | 2 | ✅ **Decisa il 2026-10-18**: il lotto 2 si apre **insieme** a S1 di MASTER-DEF (ARC-08), perché il roster serve alle ondate |

<!-- eco: AVVENTURE-COMMUNITY 2026-10-18 -->
- **Decise**: D1 la riga «Statistiche base» quando un master usa lo statblocco · D2 niente righe di scala nei master di ARC-07 già giocati, salvo per un gruppo nuovo · D3 il lotto 2 insieme a S1 di MASTER-DEF
- **Aperte**: nessuna
- **Cambiate**: nessuna, tutte e tre come proposte
- **Dedotto da me**: che il «sì sono d'accordo» valga per tutte e tre le proposte del piano, anche se il messaggio a cui rispondeva nominava per esteso solo la D1
- **Confermato dal DM il 2026-10-18**: *«sì grazie procedi con tutte e tre»*, la deduzione era giusta

## 4 · Come si riparte in una chat nuova

Leggere la ricerca §3 e §5, poi questo piano §2. Le note delle quattro ricerche,
con le fonti, sono in `plans/esperimenti/avventure-community/`.

## 5 · Come si riproduce

```
python3 scripts/domande_developer.py            # il rapporto, con i rilievi D9, D10, D15, D16
python3 scripts/domande_developer.py --check    # il cancello
python3 -m pytest -q scripts/tests/test_domande_developer.py
```

Il conto della §3 è un grep su `Bestiario/` (la preparazione dentro *Prima del
combattimento*, l'assenza di `Statistiche base`); diventa un controllo con il
primo lotto che porta la riga (ADR-0092, Conseguenze).
