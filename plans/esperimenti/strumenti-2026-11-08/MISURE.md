# Misure prima/dopo — strumenti binari da un lockfile (ADR-0113)

Data: 2026-11-08, container Linux x86_64, Python 3.13.

| Misura | Prima (curl di ci.yml) | Dopo (`strumenti.py installa`) | Esito |
|---|---|---|---|
| versione di typst | 0.15.1 (`TYPST_VERSION`, due copie) | 0.15.1 (`mise.toml`, una copia) | uguale |
| sha256 dell'archivio | non controllato | `a6d077d0…3118c`, verificato contro `mise.lock` | più severo |
| sha256 del binario `typst` | `29273eaa04f6d00edd0c2bec578f565fc9c65be856bfbffc894567c68ed0b237` | `29273eaa04f6d00edd0c2bec578f565fc9c65be856bfbffc894567c68ed0b237` | identico |
| `misura_stampa.py --tutti --json` (19 booklet: pagine, righe, misure di stampa) | `misura_stampa-prima.json` | [`misura_stampa-dopo.json`](misura_stampa-dopo.json) | **byte identici** (`cmp`) |
| tempo di `misura_stampa --tutti` | 127,4 s | 126,1 s | uguale (rumore) |
| pdfcpu in CI | assente | 0.11.0, sha256 `e14d9e8b…0bbac`, `verifica` risponde v0.11.0 | nuovo |
| bundle (4 piattaforme, senza wheel), due build con lo stesso `SOURCE_DATE_EPOCH` | — | stessi 4 sha256 | riproducibile |
| installazione dal bundle senza rete | — | `cmp` col binario installato dalla rete: identico | ok |

Il file «prima» non si versiona: è identico al «dopo» byte per byte.

Come rifarle:

```bash
# prima: il typst estratto dal tarball come faceva il curl di ci.yml
PATH=<cartella del typst estratto>:$PATH python3 scripts/misura_stampa.py --tutti --json > prima.json
# dopo
python3 scripts/strumenti.py installa
PATH=$PWD/.strumenti/bin:$PATH python3 scripts/misura_stampa.py --tutti --json > dopo.json
cmp prima.json dopo.json
```

Il tempo della CI si legge sui run della PR #338, job `validate` e `stampa-misurata`.
