# ADR-0115 — typst si installa da PyPI, la CLI di mise.lock resta il ripiego

**Stato**: accettata (2026-11-08)
**Data**: 2026-11-08
**Decisione-fonte**: il DM (Jfs), 2026-11-08, thread «Installare typst e pdfcpu in automatico». Dopo i 504 di GitHub Releases: *«perché usi mise invece di pip? […] è una best practice?»*. Poi, sulla card, «Prova pip in testing, poi decidi». Infine, letta la misura: *«applicalo se funziona come standard»*.
**Rapporti**: modifica il punto 3 di [ADR-0113](ADR-0113-gli-strumenti-binari-si-installano-da-un-lockfile.md) solo per typst (pdfcpu resta a mise). È la quarta eccezione di [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md), della famiglia di Pillow: opzionale, con ripiego dichiarato. Tiene la versione fissata di [ADR-0020](ADR-0020-edizione-da-stampa-su-un-secondo-binario.md) §3 e i pacchetti vendorizzati di [ADR-0026](ADR-0026-vendoring-pacchetti-typst.md). Segue la regola del DM «si parte dallo standard di fatto, decide la misura».

## Contesto

Il giorno in cui è arrivato ADR-0113, GitHub Releases ha risposto 504 per ore a typst, a pdfcpu e allo stesso mise. githubstatus diceva «operational». La cache di ADR-0113 assorbe il guasto dal primo giro buono, ma il primo giro buono non arrivava, e i job bloccanti dipendevano comunque da GitHub per typst.

Su PyPI c'è `typst` ([messense/typst-py](https://github.com/messense/typst-py), Apache-2.0). È il compilatore ufficiale di typst dentro un modulo Python, con wheel `abi3` per Linux, macOS e Windows. PyPI serve i file da una CDN diversa da quella di GitHub Releases. Per un progetto Python, `requirements.txt` con Dependabot è lo standard di fatto, ed è quello che il repo usa già per pyyaml, Pillow e tiktoken.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Pacchetto PyPI `typst` fissato in `requirements.txt`, tutti i chiamanti attraverso `typst_motore.py`, la CLI di `mise.lock` come ripiego** (scelta) | niente GitHub Releases nei job bloccanti; Dependabot già attivo; la wheel entra da sola nel bundle `--con-ruote`; misurato identico alla CLI | binding di un manutentore singolo, non dell'organizzazione typst; la versione del pacchetto (0.15.2) non coincide con quella del compilatore (0.15.1) |
| Restare alla sola CLI di `mise.lock` (ADR-0113) con la cache | nessun cambio; la CLI è l'artefatto ufficiale | i job bloccanti dipendono da GitHub Releases finché la cache non è piena, e la cache si svuota quando cambia `mise.lock` |
| Mirror della CLI (`ghcr.io/typst/typst`) | ufficiale | misurato il 2026-11-08: binario con un altro sha256 (908d5a47… contro 29273eaa…), quindi non è lo stesso artefatto |
| Una shim `typst` fatta in casa sopra il modulo | i chiamanti restano uguali | è una CLI nostra da mantenere, che imita quella vera: il «reinventare» che il DM esclude |

## Decisione

1. **`requirements.txt`** dice `typst==0.15.2`: una versione fissata, non un pavimento (ADR-0020 §3). Dependabot la alza con una PR, e la PR passa dal job `typst-pip`.
2. **`scripts/typst_motore.py`** è l'unico punto che compila (`compila`) e interroga (`valuta`) un `.typ`:
   - usa il modulo se c'è, altrimenti la CLI trovata da `binari.trova(binari.TYPST)`;
   - `RUMBLINGSTONE_TYPST=cli` chiede la CLI, `=pypi` vieta il ripiego;
   - porta il ripiego senza tag PDF per il bug di typst 0.15.1 e passa `SOURCE_DATE_EPOCH` come data del PDF, come fa la CLI;
   - lo usano `export_booklet_typst`, `misura_stampa`, `varianti_stampa`, `validate_booklets` e `validate_corredo`.
3. **CI.**
   - I job bloccanti non scaricano più typst: arriva con `pip install -r requirements-dev.txt`.
   - `strumenti.py installa|verifica pdfcpu` installa e controlla solo pdfcpu.
   - Il job `typst-pip` (non bloccante) compila ogni booklet con la CLI e con il modulo, ed è rosso se cambiano pagine, testo o pixel.
   - Il job `strumenti` di ADR-0113 continua a confrontare mise e `strumenti.py` sulla CLI.
4. **`mise.toml` e `mise.lock` tengono la CLI di typst** come ripiego e come riferimento del confronto. Il bundle porta sia l'archivio della CLI sia la wheel.

## Misura

`plans/esperimenti/typst-pip-2026-11-08/MISURE.md`:
- 19 booklet, 856 pagine;
- testo per pagina e pixel per pagina (72 dpi; 150 dpi su tre booklet) identici;
- la query dei riquadri di `misura_stampa` identica;
- byte identici in 1 caso su 19, negli altri cambia solo la compressione Flate delle immagini;
- il modulo è circa il 30% più veloce, perché non avvia un processo.

Dopo il cambio, in locale senza la CLI passano tutti i cancelli di stampa della CI: `validate_booklets --stampa`, `validate_corredo --stampa --rigoroso`, `misura_stampa --tutti --check` e `--per-scheda`.

## Conseguenze

- I 504 di GitHub Releases non fermano più i job bloccanti per typst. pdfcpu ci passa ancora (è nella cache, e non è su PyPI).
- Un aggiornamento di typst ora lo propone Dependabot, non Renovate. Renovate continua ad aggiornare la CLI in `mise.lock`, e le due versioni possono divergere per qualche giorno: lo dice il job `typst-pip`.
- La versione del pacchetto non è quella del compilatore. Il `Creator` del PDF dice quella del compilatore, e la dice anche `python3 scripts/typst_motore.py`.
- **Quello che non è misurato:** macOS e Windows (esistono le wheel, non sono provate); la wheel dentro il bundle installata davvero senza rete.

**Da rivedere se**: il job `typst-pip` trova un booklet diverso; typst-py smette di seguire i rilasci di typst per più di un mese (si torna alla CLI, che è ancora in `mise.lock`); oppure il progetto typst pubblica un pacchetto PyPI suo.
