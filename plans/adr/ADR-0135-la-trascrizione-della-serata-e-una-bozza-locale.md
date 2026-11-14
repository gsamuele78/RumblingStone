# ADR-0135 — La trascrizione della serata è una bozza locale, e si prova su una serata

**Stato**: proposta (2026-11-14) — prova in canale testing, da misurare su una serata
**Data**: 2026-11-14
**Decisione-fonte**: il DM (Jfs), 2026-11-13, sulla card del coordinatore: «Prova su una serata» della trascrizione locale con whisper.cpp. Prova misurata, non adozione.
**Rapporti**: attua la proposta di [`RICERCA-TOOL-ESTERNI-DM-2026-08.md`](../RICERCA-TOOL-ESTERNI-DM-2026-08.md) §3, con i limiti del §3.1. Lascia intatto [ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md) (la bozza non scrive canone). Prima dipendenza da un binario esterno per i log di sessione: la regola di degradazione è quella che il §3 chiedeva. Canale testing di [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md).

## Contesto

Il log di sessione lo scrive il DM a mano, a fine serata, quando è stanco: è il
punto in cui la catena verso `state_apply` e `session_recap` si rompe più
spesso. I servizi che trascrivono le sessioni caricano la voce dei giocatori su
server di terzi. whisper.cpp (MIT, C/C++, nessuna dipendenza) trascrive in
locale; il PC del DM ha una RTX 4050 da 6 GB, in cui stanno tutti i modelli
whisper.

L'obiezione del §3.1 è fondata: una trascrizione fedele cancella gli errori di
memoria dei giocatori, che sono materiale narrativo. Quindi la trascrizione serve
al DM e non al tavolo, e il campo «cosa hanno capito male» si scrive a mano.

## Decisione

1. `scripts/transcribe_session.py` (stdlib; pyyaml solo per i nomi, ADR-0037)
   trascrive un audio con `whisper-cli`, in italiano, e scrive **fuori dal repo**
   la trascrizione con i tempi e una bozza del log nel formato del template.
   Si rifiuta di scrivere dentro il repo, e di partire senza `--consenso`.
2. La bozza lascia **vuote** le sezioni pubbliche. Mette solo sotto
   `## DM notes` (che il recap taglia sempre) il campo «Cosa hanno capito male»
   vuoto, i momenti candidati con il minuto e l'indice dei nomi della campagna.
   Nessuna riga automatica può arrivare ai giocatori.
3. La bozza porta in testa `dmcore.bozza_trascrizione.MARCATORE`: con quel segno
   `state_apply` la rifiuta e `session_recap` la salta. Il log canonico resta
   quello che il DM firma con il wizard.
4. Degradazione: senza `whisper-cli`, ffmpeg o il modello, lo script dice come
   installarli ed esce con codice 3, senza file a metà. La CI non ha whisper e
   non lo installa: i test girano su una trascrizione JSON finta.
5. Modello consigliato `large-v3-turbo-q8_0`, sempre con `-mc 0` (niente testo
   precedente come contesto): su FLEURS le parole sbagliate scendono dal 16,6%
   al 5,8%, perché col contesto whisper salta le frasi che somigliano a una già
   detta. I nomi nel prompt sono **spenti** di serie: funzionano solo col
   contesto acceso, e nella prova sostituivano un nome con un altro.

## Misura

Banco non personale (`plans/esperimenti/trascrizione-2026-11-14/MISURE.md`),
CPU a 4 thread del container, `large-v3-turbo-q5_0`. FLEURS italiano (10,8
minuti, lettori umani): 5,8% di parole sbagliate con `-mc 0`, 16,6% senza. Copione
finto con i nomi della campagna, voce sintetica CC0: 12,5-13,3% di parole
sbagliate, 6 nomi giusti su 20, numeri tutti giusti. Velocità sulla CPU circa
una volta il tempo reale; sulla RTX 4050 da misurare. La
misura che decide è quella della serata (guida §4): M1 parole e nomi buoni dopo
la correzione del DM su tre spezzoni da cinque minuti; M2 quota dei momenti
candidati usati; M3 minuti per scrivere il log con la bozza contro senza.

Proposta di soglia, che decide il DM sulla misura: si adotta se M3 risparmia
almeno un terzo del tempo **e** M2 è almeno metà. Altrimenti si archivia, e
resta solo la guida.

## Conseguenze

- Il primo binario esterno nella catena dei log: opzionale, locale, e lo script
  funziona (esce pulito) anche senza.
- La trascrizione non distingue chi parla: whisper.cpp non separa le voci in
  italiano. Per la riservatezza è un bene; per il DM vuol dire ascoltare.
- I nomi inventati sono la parte peggiore della trascrizione. Il prompt coi nomi
  li aiuta in parte e ne sbaglia altri: la prova A/B è nella guida.
- Nel repo entrano solo i numeri della misura: niente audio, niente trascrizioni,
  niente nomi dei giocatori.
