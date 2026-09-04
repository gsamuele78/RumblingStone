# PIANO — La strada per vendere: sequenza operativa

> **Stato**: 🔵 **proposta, non autorizzata** · **Aperto**: 2026-09-04
> **Richiesta-fonte (DM, 2026-09-04)**: *«crea il piano completo»* — il documento
> che tiene insieme la discussione del 3-4 settembre 2026 e dice **in che ordine**
> si fanno le cose.
> **Non duplica**: l'analisi sta nei due piani che lo precedono, e questo li
> sequenzia.
>
> | Piano | Risponde a |
> |---|---|
> | [AUDIT-PROVENIENZA-E-VENDIBILITA](PIANO-AUDIT-PROVENIENZA-E-VENDIBILITA.md) | **cosa** si può vendere, sul piano dei diritti; e i tre metri di qualità (§7) |
> | [PROPOSTA-COMMERCIALE-E-SFIDE](PIANO-PROPOSTA-COMMERCIALE-E-SFIDE.md) | **quanto vale**, cosa lo blocca, il MIT, e la divergenza da RHoD (§7) |
> | **questo** | **in che ordine**, con i criteri d'accettazione |

> ⚠️ Ingegneria e prodotto, **non parere legale**. Per una vendita reale i test di
> auto-controllo qui dentro non sostituiscono un avvocato IP.

---

## §0 · Dove siamo, in una pagina

**L'obiettivo**: una piccola revenue dal progetto. Sistemi: 3.5 e PF1e per ora
(decisione DM). Il cancello di qualità viene prima di quello di mercato
(decisione DM).

**Le quattro cose accertate in questa discussione**, che decidono tutto il resto:

1. **L'adattamento di RHoD non è vendibile.** RHoD non è mai stato Open Game
   Content, e un adattamento è opera derivata. L'OGL **non** è l'ostacolo:
   permette il commerciale. Le tavole sono il 5% del problema, la trama il 95%.
2. **Ma la divergenza raccontata dal DM è profonda**, e sposta la prognosi: gli
   assedi vengono da Tolkien prima che da RHoD, e interi archi sono inventati.
   Resta da **verificare**, e la verifica è il lotto P2.
3. **La dipendenza vera non è RHoD: è il bestiario non-SRD.** Illithid in 86
   file, githyanki in 58, Circolo degli Otto in 31 — concentrati proprio
   nell'arco inventato da zero. È più pesante del previsto e **più economico da
   chiudere**, perché un mostro si sostituisce e una trama si riscrive.
4. **Il software venduto com'è vale essenzialmente zero**, perché nessuno compra
   una CLI. La strada corta alla revenue passa dal **contenuto**.

**Il vincolo che nessuna di queste risolve**: non c'è un pubblico. È l'unica
sfida che non si chiude con un commit, ed è la principale.

---

## §1 · Il percorso critico

Tre catene, che **non** hanno la stessa urgenza e possono correre in parallelo.

```
  QUALITÀ      Q1 stampa ──► Q2 Drappo a beta ──► Q3 audit contenuto
                  │                 │
                  └────────┬────────┘
                           ▼
  PRODOTTO                S1 il Drappo esce ──► S2 mappe scorporate ──► S3 UI?
                           ▲
  PROVENIENZA  P1 bestiario ┘      P2 struttura ──► P3 gate eseguibile
```

**Q1 blocca tutto quello che si consegna.** Finché le immagini non entrano nel
volume da stampa, nessun PDF è vendibile: al posto dell'illustrazione stampa il
suo nome.

**P1 e Q2 possono partire subito e insieme.** Non dipendono l'uno dall'altro.

**P2 (la verifica su RHoD) blocca solo l'AP**, non il Drappo — che non ha mai
avuto niente di RHoD dentro.

---

## §2 · I lotti, in ordine

### Catena QUALITÀ

#### ⬜ Q1 — Le cinque riparazioni della catena di stampa
I difetti D1–D5 sono già specificati in
[RICERCA-AUDIT-COMPONENTI-E-LIVELLO-EDITORIALE-2026-08](RICERCA-AUDIT-COMPONENTI-E-LIVELLO-EDITORIALE-2026-08.md)
§2.1, che dichiara: *«nessuna decisione da prendere, sono bug»*. I due che
contano sono **D1** (le immagini non entrano nel volume da stampa: `![alt](path)`
cade nella regola dei link e diventa `!Stemma Oca`) e **D4** (nessun gate CI
sulla stampa: `typst` non è installato in CI).
**Accettazione**: un booklet con immagini compila e **le mostra**; `typst` gira
in CI e il tema, il convertitore e i quattro booklet hanno una prova che
compilano. Un test negativo: un manifest con una chiave ignota **avvisa** invece
di tacere (D3).

#### ⬜ Q2 — Il Drappo a beta
Una serata con un gruppo vero, tempi annotati, correzioni applicate ai file. Il
modulo è ad **alfa** e lo dichiara da sé: *«questo non sostituisce il tavolo
vero»*.
**Accettazione**: `PLAYTEST-BETA.md` con i tempi reali delle tre serate, i punti
morti, e le correzioni applicate — non solo elencate.
⚠️ **È l'unica voce di tutto questo piano che non si esegue al computer.**

#### ⬜ Q3 — L'audit del contenuto contro il proprio metro
Passare i master definitivi esistenti contro la checklist di
`rumblingstone-module-standard` (benchmark dichiarato: RHoD + AP Paizo) e
**contare quanti la passano**. Esiste un esemplare di riferimento
(`ARC07-DEF-1`); quanti altri siano al livello non è mai stato misurato.
**Accettazione**: una tabella modulo × voce di checklist, con il conto dei
passati e la stima di lavoro per i restanti. È un audit, non una riscrittura.

### Catena PROVENIENZA

#### ⬜ P1 — Bonifica del bestiario non-SRD
Sostituire le entità di Product Identity con creature originali che occupino lo
stesso ruolo tattico. Le **statistiche** restano derivabili dal SRD: è
l'identità a essere protetta, non i numeri.

| Da sostituire | File | Priorità |
|---|---:|---|
| illithid / mind flayer | 108 | alta (arco 09) |
| githyanki / githzerai | 61 | alta (arco 09) |
| Circolo degli Otto / Circle of Eight | 31 | alta |
| beholder | 10 | media |
| maur · yuan-ti · umber hulk | 10 | bassa |

**Accettazione**: zero occorrenze delle entità in elenco fuori da note storiche
esplicite; ogni sostituzione ha una scheda nel Bestiario con `fonte:` che dichiara
il ruolo tattico ereditato; un validatore che **fallisce** se una rientra.
⚠️ **E la regola da adottare il giorno zero**, prima ancora del lotto: *quello
che si popola d'ora in poi si popola dal SRD*. Ogni illithid aggiunto oggi è un
file in più da bonificare domani.

#### ⬜ P2 — La verifica della struttura contro RHoD
Il lotto che stabilisce se il racconto del DM (§7 di PROPOSTA-COMMERCIALE) regge:
beat, sequenza, toponimi, PNG. Metodo: la **camera bianca** — una pagina con la
sola premessa in forma di idea, e il confronto di ciò che il repo contiene contro
quella; più il **test del lettore**, cioè darlo a chi ha condotto RHoD e sentire
se dice «stesso genere» o «coi nomi cambiati».
**Accettazione**: per ogni arco, un verdetto motivato — indipendente / da
rimaneggiare / derivato. E ⚠️ **solo se P2 stabilisce che è falsa**, si corregge
la riga *«heavily based on Red Hand of Doom»* del README, che oggi è
l'ammissione di derivazione più dannosa del repo e forse è pure inesatta.
**Mai riscriverla prima della verifica.**

#### ⬜ P3 — Il gate d'uscita eseguibile
Campo `provenienza:` machine-readable, `validate_provenienza.py`, e il test nei
**due sensi**: ogni artefatto OGC ha la sua voce in `OGL.txt`, e ogni voce in
`OGL.txt` è usata da almeno un artefatto.
**Accettazione**: `dm.py doctor --ip` in CI; il Drappo passa il gate **a secco**,
senza deroghe; un file dell'arco 00 lo **fallisce** con la ragione scritta. Un
gate che passa solo aggiungendo eccezioni non è un gate.

### Catena PRODOTTO

#### ⬜ S1 — Il Drappo esce
Il primo prodotto candidato: è l'unico artefatto insieme **vendibile** e già
passato per una passata di collaudo, ed è nato fuori da Faerûn e da RHoD apposta.
**Dipende da**: Q1 (senza, il PDF non mostra gli stemmi), Q2, P3.
**Accettazione**: un PDF con colophon, licenza e Sezione 15 corretti, che passa
il gate d'uscita, messo in vendita.

#### ⬜ S2 — La pipeline mappe scorporata
Progetto separato, MIT, con la sua documentazione. Sette strumenti sono **già
generici** (`render_map_svg`, `export_uvtt`, `import_ultraclear`, `validate_maps`,
`suggest_map`, `import_watabou`, `compile_map_json`) ed è **l'unico asset del
repo indipendente dal sistema**: un export UVTT con muri, porte e luci serve a
chi gioca 5e, PF2e o Traveller.
**Accettazione**: repo separato che gira senza il canone; un README che si legge
da fuori; e — il criterio vero — **serve da vetrina**, cioè comincia ad attaccare
la sfida del pubblico prima ancora di essere un prodotto.

#### ⬜ S3 — Decidere se la UI si fa
**Solo con i numeri di S1 e S2 sotto gli occhi.** Se S1 non vende e S2 non porta
utenti, una UI non cambia il risultato: lo rende più caro. La forma, se si fa, è
**open core** — core MIT, e sopra UI, servizio e contenuti.

---

## §3 · Le regole da adottare subito, prima di qualunque lotto

1. **Si popola dal SRD.** Nessuna entità non-SRD nel materiale nuovo.
2. **Un prodotto, un regime.** Non si mescolano OGL e CC BY in un volume, e non
   si ri-licenzia l'OGC come CC BY. Il multi-sistema si fa a edizioni separate.
3. **Additivo, mai «importa tutto e poi lima».** Vale per `OGL.txt` e per ogni
   dichiarazione di provenienza: si aggiunge la voce quando si trova l'uso.
   Limare è un argomento dall'assenza, e fallisce in silenzio.
4. **Non si riscrive la storia del repo per convenienza.** Le dichiarazioni si
   correggono quando una verifica le smentisce, mai prima.

---

## §4 · Le decisioni che restano al DM

| # | Decisione | Perché ora |
|---|---|---|
| 1 | **Licenza del core** — raccomandazione: **lasciarlo MIT** | cambiarla protegge poco (il passato resta MIT) e costa l'adozione, che è ciò che manca |
| 2 | **Il marchio** «RumblingStone» | non è registrato, difende dove il MIT non arriva, e ha tempi lunghi |
| 3 | **Accettare il tetto legacy**, o rivedere 3.5/PF1e **per i soli prodotti** | il mercato che paga è su 5e (CC BY 4.0) e PF2e (ORC); la campagna può restare com'è |
| 4 | **Chi fa il playtest beta** (Q2) | è l'unica cosa che non si fa al computer, ed è sul percorso critico di S1 |
| 5 | **La provenienza delle tavole raster** «fornite dal DM» | ADR-0005 la segna come debito; blocca la parte immagini di P3 |

---

## §5 · Da dove ricominciare, in una chat nuova

```bash
# lo stato reale, non quello che dicono i file
python3 -m pytest scripts/tests/ -q
python3 scripts/dm.py doctor --ci
python3 scripts/extract_statblocks.py --check

# il difetto che blocca ogni consegna (D1): riprodurlo prima di ripararlo
grep -rn 'cover_image' scripts/export_booklet_typst.py   # → nulla: e' D3
```

**Leggere prima**: §0 di questo piano, poi §0 e §7 di
[AUDIT-PROVENIENZA-E-VENDIBILITA](PIANO-AUDIT-PROVENIENZA-E-VENDIBILITA.md), poi
§7 di [PROPOSTA-COMMERCIALE-E-SFIDE](PIANO-PROPOSTA-COMMERCIALE-E-SFIDE.md).

**Il primo lotto da aprire**: **Q1**, perché è fatto di bug già specificati e
sblocca tutto ciò che si consegna. **In parallelo P1**, perché è meccanico,
elencabile e finito, e ogni giorno che passa senza la regola di §3.1 lo allunga.
