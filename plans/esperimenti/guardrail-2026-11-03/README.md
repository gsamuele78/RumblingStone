# Guardrail e tecniche avanzate: le prove (2026-11-03)

Le prove di [RICERCA-GUARDRAIL-E-TECNICHE](../../RICERCA-GUARDRAIL-E-TECNICHE-2026-11.md).

| file | cosa contiene | come si rifà |
|---|---|---|
| `conti-recinti.json` | i 6 conti dei boss recintati che non tornano | `python3 scripts/conformita_statblocchi.py --master --json` |
| `note-di-lavoro.json` | le 60 note di lavoro che vanno in stampa, per volume | `python3 scripts/misura_standard_tavolo.py --json` |
| `distanza-pagine.json` | le pagine fra scena e numeri, prima e dopo la prova ADR-0107 | `python3 scripts/misura_distanza_pagine.py --json PRIMA.pdf DOPO.pdf` (PDF in /mnt/project-files/usabilita-al-tavolo/) |
| `box-telecomando.tsv` | i 15 colpi del rilevatore dei box che decidono per i PG, fuori dalle battute | regex in RICERCA §3; giudizio a mano: 2 veri |
| `varianti-dei-nomi.txt` | le 64 varianti rare dei nomi del glossario: 1 vera | lo script è nella RICERCA §6 |
| `numeri-incrociati.txt`, `prova_numeri_incrociati.py` | CA e pf citati nel testo contro il recinto: 0 veri su 6 | `python3 plans/esperimenti/guardrail-2026-11-03/prova_numeri_incrociati.py` |
| `ripetizioni.json`, `prova_ripetizioni_embedding.py` | le 20 coppie di box più simili per embedding e per 4-grammi | richiede `sentence-transformers` e torch per CPU, fuori dalla dotazione; `HF_HUB_DISABLE_XET=1` |

## Richiamo contro la lettura del DM e del playtester

Dei difetti di contenuto che i due lettori hanno trovato nella prova ADR-0107,
quelli numerici con una regola SRD erano 2, e i controlli nuovi li trovano
tutti e 2:

| trovato dai lettori | trovato dai controlli |
|---|---|
| *corrompere l'acqua* del Vecchio CD 25, dovrebbe essere 26 | ✓ conti dei recinti, «come A.1» |
| Zog'tar senza scurovisione | ✓ conti dei recinti, sensi |
| «[INFERRED…]» e «va riscontrato su d20srd.org» stampati | ✓ note di lavoro (60 in tutto) |
| Concentrazione CD 21 del Vecchio | ✗ non ritrovata nei master: da chiarire con il lettore |
| frequenza di Presenza Minacciosa mancante | ✗ non è un conto |
| M7-C non torna col testo, quota di 45 m contro un soffio di 30 m | ✗ giudizio di lettura |

I controlli trovano in più 4 difetti che nessun lettore aveva visto: pf del
Treant di Adamantio (90, 10d8+50 ne fa 95), pf di Balvar (101, 13d8+39 ne fa
97), scurovisione di Durin (nano) e delle wyvern (SRD: 18 m).
