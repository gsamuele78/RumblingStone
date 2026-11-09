# Python 3.14 in prova: la prima misura (2026-11-09)

> P8 di [PIANO-PIATTAFORMA-DI-SVILUPPO](../../PIANO-PIATTAFORMA-DI-SVILUPPO.md),
> anticipata dal DM il 2026-11-09 con la card «Accendilo ora». Il salto vero
> resta legato a Debian 14 (ADR-0099 §6). Criterio: un mese di verde su `main`
> del job «Python 3.14 in prova — non bloccante» prima del salto.

## In locale, prima del job

Python 3.14.6 (`uv python install 3.14`), ambiente pulito,
`uv pip install -r requirements-dev.txt`:

- **Librerie**: si installano tutte da ruota, niente da compilare. Elenco con
  le versioni in [pacchetti-314.txt](pacchetti-314.txt) (68 pacchetti). Le
  dipendenze native pesanti (pymupdf, tcod, onnxruntime, scipy, scikit-image,
  shapely, typst, tiktoken) si importano.
- **Test**: giro parallelo 2.431 passate e 14 saltate, giro in serie
  (`scrive_nel_repo`) 131 passate e 2 saltate. Su 3.13, stesso commit:
  2.431 e 14 nel giro parallelo, come 3.14. Nessun fallimento, nessun avviso
  nel riepilogo di pytest.
- **Saltate**, le stesse su tutte e due le versioni: spaCy assente (12),
  CLI typst assente (1), PRD PF1e non in cache (1), `bpy` assente (1), più i
  2 del giro in serie.
- **Blender**: `bpy` vuole 3.13 esatto e sta solo in
  `requirements-completo.txt` con il marcatore `python_version == "3.13"`; il
  job installa `requirements-dev.txt`, quindi `test_blender_vero` salta come
  nel job principale. Non serve un'esclusione esplicita.

Cosa questa misura non dice: i passi di «validate» diversi da pytest (gate,
booklet, mappe) non girano su 3.14; il job prova solo la suite. Se il mese di
verde regge, il passo successivo è far girare su 3.14 anche `gate_locale.py`.

## Primo run in CI

Da compilare con il run della PR: tempo del job, prove passate e saltate,
eventuali differenze da 3.13.
