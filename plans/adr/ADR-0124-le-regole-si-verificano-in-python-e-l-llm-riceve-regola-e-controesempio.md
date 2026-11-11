# ADR-0124 — Le regole si verificano in Python, e l'LLM riceve la regola violata e il controesempio via MCP

**Stato**: proposta (2026-11-11)
**Data**: 2026-11-11
**Decisione-fonte**: il DM (Jfs), 2026-11-11: valutare lo stack «grafo di eventi + regole in Prolog + regola che fallisce o controesempio restituiti all'LLM perché si corregga», chiamato via server MCP, e misurare se l'adozione nel repo è possibile.
**Rapporti**: applica [ADR-0067](ADR-0067-il-confine-dichiarato-fra-codice-e-llm.md) (l'LLM è client, i verificatori sono deterministici) e [ADR-0030](ADR-0030-server-mcp-sui-tool.md) (server MCP); segue la regola dello standard di fatto del 2026-11-08. Misure in [plans/esperimenti/prolog-verificatore-2026-11-11/ESITO.md](../esperimenti/prolog-verificatore-2026-11-11/ESITO.md).

## Contesto

La proposta separa chi genera (l'LLM) da chi verifica (un motore logico), e
rimanda all'LLM la regola esatta che fallisce. La separazione c'è già:
ADR-0067 tiene l'LLM fuori dagli script, e `mcp_server.py` espone 137 tool. La
domanda vera era se un motore logico (Prolog, lo standard di fatto della
programmazione logica; clingo come alternativa ASP impacchettabile) verifica
meglio del Python che c'è.

Banco: i prerequisiti dei talenti sulle 74 schede del Bestiario che li
elencano, gli stessi fatti dati a tre motori, più 141 difetti iniettati.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Python, regole come dati TOML, uscita strutturata via MCP** (scelta) | trova 141/141 difetti iniettati e le stesse 30 violazioni vere; 0,8 ms; nessuna dipendenza nuova; un solo linguaggio per le regole | le regole ricorsive o temporali vanno scritte a mano |
| SWI-Prolog (BSD-2) | regole dichiarative e leggibili; ricorsione e ricerca del controesempio gratis | stessi 141/141 e 30, **0 difetti in più** dalla chiusura transitiva; binario di sistema che non entra nel bundle offline; ponte janus solo da 9.1 (Ubuntu 24.04 ha 9.0.4); 70× più lento per il processo |
| clingo (ASP, MIT) | ruota PyPI per Python 3.13, si porta nel pacchetto; 14 righe di regole | stessi risultati; seconda lingua nel repo, con 3 falsi positivi introdotti al primo giro dalla traduzione dei fatti (costanti contro stringhe) |

## Decisione

1. **Nessun motore logico nel repo per ora.** La misura boccia lo standard
   (Prolog) e l'alternativa (clingo) non perché sbaglino, ma perché non trovano
   niente in più e costano un secondo linguaggio e, per Prolog, un binario
   fuori dal pacchetto.
2. **Si adotta il pattern, non il motore**: ogni verificatore di regole che
   l'LLM chiama via MCP restituisce per ogni violazione `regola`, `atteso`,
   `ha` e `file:riga`, in JSON, oltre al testo per il DM.
3. Il primo verificatore così è quello dei **prerequisiti dei talenti sulle
   schede esistenti**, che oggi nessun cancello controlla (30 violazioni in 19
   schede, campione: 6 su 8 difetti veri). Entra come tool del manifest in
   sola lettura, in canale testing (ADR-0099), dopo le scelte del DM sulle
   schede segnalate.
4. Prima di quel tool si correggono D1 (classi in italiano in `[capacita]` di
   `sistemi/dnd35/dati/talenti.toml` contro l'inglese dei prerequisiti) e D2
   (`character` mai scritto per Leadership), con test sulle chiavi.

## Conseguenze

- L'LLM riceve la regola esatta e il controesempio senza imparare un motore
  nuovo, e il server MCP che c'è basta.
- Il pacchetto resta senza binari di sistema nuovi.
- Si rinuncia alla ricorsione e alla ricerca dichiarativa: una regola come «chi
  sa cosa, attraverso chi, entro quale giorno» va scritta in Python.
- Il giro di autocorrezione (messaggio libero contro uscita strutturata) **non è
  misurato**: resta da fare col protocollo di ESITO §5.

**Da rivedere se**: arriva un dominio con regole davvero ricorsive o temporali
su fatti già strutturati (per esempio §4 «chi sa cosa» di `state.yaml` con una
colonna Tempo), oppure le regole Python di un dominio superano le 300 righe e un
banco di mutanti mostra che la versione dichiarativa trova difetti che il
Python perde.
