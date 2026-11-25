# ADR-0150 — Il prompt d'immagine si scrive per il modello che lo esegue

**Stato**: proposta (2026-11-25), in attesa che Jfs guardi il confronto del 25/11
**Data**: 2026-11-25
**Decisione-fonte**: il DM (Jfs), 2026-11-25, nel thread «Scrivere lo script FLUX per il 4050», dopo il primo collaudo su Kaggle: «per vanna il flux seme 1 meglio ma le mani non sono rovinate come dovrebbero, probabilmente il prompt deve essere più accurato […] usare i migliori prompt possibili […] mi piacerebbe che diventasse uno standard del repo se ha senso», e «fissare le regole dello standard in modo da avere lo stesso standard di prompt che è regolato e verificato e misurato da regole utilizzate come best practices dalla community».
**Rapporti**: completa [ADR-0015](ADR-0015-standard-prompt-immagine.md) (la scheda-prompt) per i modelli che non riscrivono il prompt; rispetta [ADR-0005](ADR-0005-confini-ip-uso-non-commerciale.md) e [ADR-0019](ADR-0019-licenza-dei-pesi-non-del-software.md); segue la regola di partenza di [ADR-0114](ADR-0114-ogni-prompt-ha-una-scheda-e-le-sue-prove.md) (prima lo standard di fatto). Misura: `scripts/misura_prompt_immagine.py`; esecuzione: `scripts/comfyui_batch.py` (blocchi `didascalia`).

## Contesto

Le diciotto immagini del Drappo le ha fatte il DM con Gemini il 2026-08-15,
dai prompt di `PROMPT-RITRATTI-E-TAVOLE.md`: liste di etichette separate da
virgole, scritte per SDXL, da 65 a 100 parole una volta composte col look
comune e l'ancora storica. Il repo non ha altri prompt per quelle immagini:
il thread «Contenuti su Gemini e AI Studio» e l'inventario di
`plans/INVENTARIO-GEMINI-AISTUDIO-2026-10.md` non ne riportano, e le tavole
del Palio di Channathgate le ha caricate il DM senza prompt nel repo
(`P2D-Palio-Allegati/immagini/README.txt`).

Il 21/11 il collaudo D2 ha passato gli stessi prompt a FLUX.2 [klein] 4B su
Kaggle. Il DM ha giudicato: Vanna alla pari con Gemini ma con le mani pulite,
la Ruota e il Drappo meglio Gemini. Il Drappo era frainteso (uno stendardo
bianco sopra una corsa e un blocco di volti incollato), come già nella prova
su CPU del 16/11 (MS-0182).

La guida ufficiale di Black Forest Labs spiega la differenza. Gemini, come
FLUX 3 Image, riscrive il prompt corto in una didascalia lunga prima di
disegnare. FLUX.2 [klein] no: «what you write is exactly what the model
receives». La stessa lista di etichette arriva a Gemini come una scena
descritta e a klein come una lista.

## Le regole e da dove vengono

Lette il 2026-11-25 su docs.bfl.ml: «Building a good prompt», «Technical
parameters», «Prompt reference» (sezione FLUX.2 [klein]).

| Regola | Che cosa chiede | Fonte | Come si misura |
|---|---|---|---|
| P1 | prosa, non etichette: frasi intere che descrivono la scena | BFL, klein: «write in prose, not keyword lists» | almeno 3 frasi; al massimo metà dei frammenti fra virgole sotto le quattro parole |
| P2 | la prima frase dice che immagine è e con che mezzo | BFL, «Structure helps», punto 1 | parola di tipo nella prima frase |
| P3 | la luce con la sua sorgente e la sua direzione | BFL, klein: «describe the light source, direction, and softness» | una sorgente e una direzione |
| P4 | la chiusa `Style: … Mood: …` | BFL, klein | espressione finale |
| P5 | niente negazioni: si descrive cosa c'è al posto di ciò che non si vuole | BFL, «Working without negative prompts» | `no`, `without`, `not`… |
| P6 | niente etichette di qualità | BFL: «omit quality tags such as masterpiece» | elenco chiuso |
| P7 | niente nomi di autori, niente «in the style of» | ADR-0005 | espressione |
| P8 | la didascalia fa il lavoro della riscrittura: abbastanza lunga da descrivere la scena, entro il limite del codificatore | soglie nostre: la guida mostra didascalie fra 30 e 190 parole; il codificatore di FLUX.2 legge 512 token | da 60 a 350 parole |
| P9 | la «cosa che non deve mancare» della scheda diventa una frase in primo piano, con i dettagli visibili | ADR-0015 e skill `rumblingstone-art-direction` §3; BFL: «describe visible details» | giudizio: la scheda e la didascalia si leggono accanto |

## Decisione

- La scheda di ADR-0015 resta il sorgente. Per un modello che non riscrive il
  prompt (oggi FLUX.2 [klein]) l'immagine porta anche un blocco
  `<!-- didascalia id=… modello=flux2-klein -->` con la didascalia in inglese
  che segue P1-P9. Con `--modello flux2-klein-4b`, `comfyui_batch.py` la usa
  al posto del prompt composto e lascia vuoto il negativo, che a cfg 1 klein
  non legge. Con gli altri modelli non cambia niente.
- `python3 scripts/misura_prompt_immagine.py FILE [--check]` misura P1-P8.
  P9 resta giudizio.
- Primo lotto: le tre tavole del collaudo D2 (§9 di
  `10-stand-alone/Il-Drappo-di-Tarsilia/ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md`).

## La misura

Sulle tre tavole del collaudo, prompt composti del 21/11 contro didascalie
del 25/11: 0/3 contro 3/3 senza errori di `misura_prompt_immagine.py`. Che le
immagini vengano meglio non lo dice lo script: lo dice il DM guardando il
confronto del 25/11 (stessi semi 0 e 1 del 21/11, più il seme 2, su Kaggle).

## Chi scrive le didascalie: la prova fra due modelli

Il DM ha chiesto il 25/11 una prova «completa, indipendente e misurabile» fra
i due modelli che possono scrivere le didascalie in questo thread. Com'è
fatta:

- un solo incarico scritto, uguale per tutti e due: le schede delle tre
  tavole, le regole P1-P9, i giudizi del DM sulla prova del 21/11;
- due scritture separate, una per modello, che non vedono il lavoro
  dell'altra, le didascalie di §9 né il resto del repo;
- le due consegne girano su FLUX.2 [klein] con gli stessi semi 0, 1 e 2;
- le immagini arrivano al DM con le sigle A e B, assegnate a sorte, e la
  chiave si apre dopo la sua scelta (la regola del cieco di ADR-0093).

Misura automatica: le sei didascalie passano `misura_prompt_immagine.py`
(6/6). Quale serie dà immagini migliori lo dice la scelta del DM, e si scrive
qui quando c'è. Il limite: tre tavole e tre semi sono un campione piccolo, e
una preferenza di misura non dimostra una differenza fra i modelli.

## Le conseguenze

- Un prompt per klein costa di più da scrivere: 180-200 parole invece di 70,
  e una scheda in più da tenere allineata con quella breve.
- Le soglie di P8 sono nostre e vanno riviste se un modello con un
  codificatore diverso entra nel repo.
- Il misuratore vede la forma, non la resa: una didascalia che passa può
  ancora dare un'immagine da buttare (gate di rifiuto della skill
  `rumblingstone-art-direction` §6).
- Non è un cancello della CI finché il DM non ha visto il confronto: l'ADR
  passa ad «accettata» solo se le immagini nuove battono quelle del 21/11.
- FLUX 3 Image Klein (5,6 miliardi di parametri, uscito il 15/10/2026) ha la
  riscrittura del prompt dentro, come Gemini. Gira sotto la FLUX Kommunity
  License (uso commerciale sotto i 5 milioni di dollari di fatturato), che il
  DM ha considerato usabile il 29/10 nel thread «Immagini dei personaggi in
  posa con l'AI», ma che `comfyui_batch.py` non ha fra i pesi ammessi. I pesi
  sono gratuiti e si scaricano solo dopo aver accettato i termini su Hugging
  Face. Le versioni a 8 bit pesano 5,8 GB (modello), 4,9 GB (codificatore) e
  6,7 GB (riscrittore), e Black Forest Labs le dà per schede da 8 GB: nella
  4050 da 6 GB non entra, in una T4 di Kaggle da 16 GB sulla carta sì. Il DM
  l'ha messo a condizione il 25/11: si prova solo se resta gratuito e gira
  sulla Kaggle gratuita. Non è ancora stato provato: serve un token Hugging
  Face nell'ambiente, che mette il DM.
