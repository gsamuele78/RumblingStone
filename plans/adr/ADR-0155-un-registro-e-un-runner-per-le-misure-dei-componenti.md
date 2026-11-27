# ADR-0155 — Un registro e un runner per le misure dei componenti

**Stato**: proposta (2026-11-27)
**Data**: 2026-11-27
**Decisione-fonte**: il DM (Jfs), 2026-11-27, su card nel thread «Misurare e migliorare agenti, skill e automatismi» (scelta E1, la consigliata: «un registro e un runner soli per misurare tutti i componenti»). Il canale lo fissa questo ADR con le regole di [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md).
**Rapporti**: è il contenitore delle misure di [ADR-0154](ADR-0154-l-instradamento-degli-agenti-si-misura-su-messaggi-veri.md) e di [ADR-0058](ADR-0058-orchestrazione-a-strati-delle-skill.md); segue la forma dei cricchetti di [ADR-0148](ADR-0148-i-fatti-si-verificano-con-script-e-gli-agenti-con-prove-fisse.md). Il censimento dei componenti da misurare è in `/mnt/project-files/agenti-eval-2026-11-27/CANALE-MIGLIORAMENTO.md` (lotti E0-E11).

## Contesto

Ogni componente che decide qualcosa (l'hook degli agenti, i trigger delle
skill, i rilevatori della prosa, il server MCP) aveva o avrebbe avuto il suo
passo CI, il suo tetto e il suo modo di dire che è sceso. Il censimento del
27/11 conta dodici lotti da misurare: con un passo e un cricchetto a testa,
la CI cresce di dodici forme diverse dello stesso controllo, e un tetto
abbassato a mano in uno di quei file non lo vede nessuno.

Le comunità che misurano modelli hanno già risolto la cosa con un registro
dichiarativo e un runner solo: lm-eval-harness ha un file per task con
comando, metriche e aggregazione, OpenAI evals un registro YAML per eval.

## Decisione

1. **Il registro.** `plans/eval/componenti.json`: una voce per componente con
   `id`, `componente`, `set`, `comando` (argv senza shell, con i segnaposto
   `{python}` e `{set}`), `metriche` (percorso nel JSON d'uscita e verso,
   «alto» o «basso»), `tetto`, `canale` di ADR-0099 e `adr`.
2. **Il tetto ha una fonte sola.** Se il set lo scrive già, la voce lo punta
   con `{"dal_set": "percorso"}` e il runner lo legge da lì. Così
   `raccogli_casi_agenti.py applica`, che rimette il tetto nel set, non deve
   sapere che il registro esiste. Un tetto in chiaro si scrive solo quando il
   set non lo porta.
3. **Il runner.** `scripts/eval_componenti.py` esegue le voci, confronta con
   `fractions.Fraction` (un float è una voce malformata) ed esce 0 al tetto o
   sopra, 1 sotto il tetto, 2 se un comando fallisce o una voce è malformata.
   `--json`, `--solo ID`, `--check-registro`.
4. **Il cricchetto contro il tetto abbassato a mano.** Con `--rispetto-a REF`
   (in CI il ramo di base) ogni tetto si confronta con quello su REF: se è
   peggiorato esce 1, salvo che la nota del tetto nel set porti una rimessa di
   `applica` nuova rispetto a REF, perché allora è cambiato il set e non il
   componente.
5. **Un componente nuovo entra con la sua voce**, non con un passo CI suo.
6. **Canale testing** dal merge, non bloccante; stable non prima di 14 giorni
   e 10 run su main. Il passo bloccante di `instradamento_skill.py --check`
   resta finché il runner non è stable, perché un runner in testing non può
   bloccare un componente stable. Il passo testing di
   `instradamento_agenti.py --check` lo sostituisce il runner.

## Le conseguenze

- Le prime due voci danno gli stessi numeri dei passi che c'erano: agenti
  sul test 4/17 esatti, 4/17 indulgenti, macro-F1 58/315; skill 17 omissioni,
  1 violazione, 0 conflitti fra le L1. Il runner gira in 1,5 s.
- I lotti che seguono (E2-E11) aggiungono una voce e il loro set, non un
  passo CI.
- **Quello che si paga.** Ogni comando deve stampare JSON con le metriche a
  un percorso fisso: un componente che oggi stampa solo testo va adattato
  prima di entrare. Il controllo contro REF chiede la storia completa
  (`fetch-depth: 0`); in un clone shallow il runner lo dice e quel controllo
  passa. Finché il runner è testing, il passo bloccante delle skill misura due
  volte la stessa cosa.
