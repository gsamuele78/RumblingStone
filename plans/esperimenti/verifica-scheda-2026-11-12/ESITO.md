# Verifica di una scheda via MCP e divario delle regole: misura del 2026-11-12

Richieste del DM (2026-11-12): verificare via server MCP non solo i talenti ma
anche BAB, gradi delle abilità e «tutto quello che la scheda scrive», con le
regole del plugin del sistema e nell'ordine **SRD d20 → D&D 3.5 → PF1e**;
misurare che cosa manca ai plugin rispetto a SRD, srd.dndtools.org, PCGen e
chiudere il divario dove la misura dice che serve. Decisione in
[ADR-0124](../../adr/ADR-0124-le-regole-si-verificano-in-python-e-l-llm-riceve-regola-e-controesempio.md) §6-§7.

## 1. Che cosa c'è adesso

`scripts/verifica_scheda.py`, nel manifest e quindi nel server MCP, sola
lettura. Una chiamata, un'uscita: per ogni difetto `verifica` (talenti o
numeri), `regola`, `atteso`, `ha`, `fonte`, `file:riga`. Non ha regole sue:
chiama `verifica_talenti` e `conformita_statblocchi.giudica`.

Bestiario: 126 schede lette, **23 violazioni in 12 schede** (tutte di
talenti), 65 voci non verificabili.

## 2. Quanto vede: numeri sbagliati messi apposta

`muta_numeri.py` cambia un numero per volta nelle schede `*-cr*.md` pulite e
chiede allo strumento se lo vede.

| Errore messo | Visto |
|---|---|
| BAB +1 | 66 / 91 |
| lotta +3 | 74 / 101 |
| tiro salvezza −2 (Temp, Rifl, Vol) | 89 / 121, 88 / 121, 79 / 120 |
| tiro salvezza +5 | 91 / 121, 91 / 121, 87 / 120 |
| tiro salvezza +2 | 1 / 121, 0 / 121, 0 / 120 |
| **Totale** | **666 / 1.278 (52%)** |

Perché ne perde metà, contato sui mutanti persi:

- **Tiri salvezza +2: non li vede per regola.** `conformita_statblocchi`
  accetta fino a +4 sopra il minimo, perché un mantello della resistenza o un
  talento non stanno nella riga dei TS. È una scelta, non un difetto, ma vuol
  dire che un TS gonfiato di 2 passa.
- **La regola non parte** su circa un quarto delle schede: la composizione dei
  dadi vita non è nota (9 dei 25 BAB persi, 19 dei 32 Tempra persi) oppure la
  scheda ha una **classe che il plugin non conosce** (5 e 5).
- **Parte ma tollera lo scarto** (10 BAB, 26 lotte): il confronto accetta
  ±1 o varianti dichiarate.
- **Schede a dossier** (`Bestiario/png/*/*.md`): la lettura dei numeri non è
  collaudata su quel formato («BAB/Lotta: +8 / +10» letto come lotta 8), quindi
  i loro numeri vanno fra i non verificabili.
- **Gradi delle abilità: nessun controllo.** Il plugin 3.5 ha i nomi delle
  abilità ma non la caratteristica chiave né i punti per livello di classe e di
  tipo; il PF1e ha i punti per livello delle classi.

## 3. Divario dei plugin, sezione per sezione

| Sezione | Plugin `dnd35` oggi | SRD 3.5 in cache | srd.dndtools.org | Dati PCGen (WotC 3.5) | Plugin `pf1e` |
|---|---|---|---|---|---|
| Talenti | 363 SRD + 2.193 dei manuali (da oggi) | 363 | 38 pagine, 1.553 in tabella | 2.037 | 1.227 |
| Classi base | 11 + 5 da PNG | 11 + psioniche | 65 pagine | 74 file `class` (base e prestigio) | 55 |
| Classi di prestigio | 14 (SRD) | 14 + epiche e psioniche | **268 pagine** | compresi sopra | nelle 55 |
| Abilità | solo nomi | pagine complete | 4 pagine | 28 file | nomi |
| Punti abilità per livello | **assenti** | nelle pagine di classe e di tipo | nelle pagine di classe | campi `STARTSKILLPTS` | presenti |
| Incantesimi (liste per classe) | 6 classi, liste corte del generatore | tutti | 27 pagine | 72 file | liste complete |
| Razze | 20 | Core + mostri | 2 pagine indice | 57 file | 37 + 100 voci |
| Tipi di creatura | 15 | sì | sì | — | 13 |
| Equipaggiamento | 30 armature, 11 scudi | sì | 5 pagine | 98 file | 12 + 6 |
| Poteri psionici, invocazioni, magie alternative | assenti | psionici sì | 18 + 8 + 8 pagine | parziale | — |
| Mostri | Bestiario del repo | sì | 5 pagine indice | — | — |
| Varianti (Unearthed Arcana) | assenti | no | 37 pagine | parziale | — |

Il sito ha 616 pagine nella mappa; 404 sono classi (base e di prestigio) e
manuali.

## 4. Ordine in cui chiudere (dal più utile alla verifica)

1. **Punti e gradi delle abilità** (3.5 e PF1e): è il controllo che manca del
   tutto. Servono caratteristica chiave, punti per livello di classe e di
   tipo; l'SRD in cache li ha, quindi resta dentro l'OGL.
2. **Classi di prestigio e classi base fuori SRD** (BAB, TS, dado vita, punti
   abilità, avanzamento da incantatore): toglie «la regola non parte» e i
   «non verificabili per classe ignota». Fonti: srd.dndtools.org e PCGen,
   con lo stesso confronto fra le due fatto per i talenti.
3. **Composizione dei dadi vita non nota**: è lettura delle schede, non
   regola; va vista scheda per scheda.
4. **Liste di incantesimi complete per classe** (oggi il generatore ne ha
   poche): serve a controllare che un incantesimo scritto sia della lista e
   del livello giusti.
5. Razze dei manuali, equipaggiamento, psionici: dopo, e solo se una misura
   come quella del §2 mostra errori che oggi passano.

## 5. Limiti

- srd.dndtools.org riporta manuali non OGL e il repo PCGen non dichiara una
  licenza: nel repo entrano solo fatti di regola (nomi, soglie, progressioni),
  mai testo. Se il DM non vuole tenerli, i file `*_manuali.toml` si tolgono
  senza toccare il codice.
- Sui talenti le due fonti divergono in 353 casi su 1.156: una violazione che
  viene da un manuale va riletta sul libro prima di correggere la scheda.
- Il giro di autocorrezione su un modello vero resta non misurato (ESITO del
  2026-11-11, §5).

## Riprodurre

```bash
python3 scripts/verifica_scheda.py Bestiario
python3 plans/esperimenti/verifica-scheda-2026-11-12/muta_numeri.py
```
