# ADR-0107 — Chi si incontra sta nel capitolo dove lo si incontra

**Stato**: proposta
**Data**: 2026-11-03
**Decisione-fonte**: il DM (Jfs), dopo la serata del 2026-11-02 con il booklet di *Notte e Alba*:
*«per ogni capitolo accanto alla scheda una descrizione, una sua immagine e chi è e cosa vuole credo sia il minimo standard sindacale da adottare, e poi lo leggi da DM»*; e il 2026-11-03: *«voglio che aggiungi anche l'appendice con le schede perché erano fatte bene»*.
**Rapporti**: emenda il punto 7 di [ADR-0105](ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md) (il riquadro intero solo in appendice); usa la scheda d'entrata di [ADR-0073](ADR-0073-chi-e-dove-sta-scritto-nella-scena.md), il dossier di [ADR-0091](ADR-0091-la-scheda-del-png-ha-una-forma.md) e le piante di stampa di [ADR-0106](ADR-0106-ogni-mappa-si-stampa-in-pianta.md). Ricerca e misure in [RICERCA-USABILITA-AL-TAVOLO-2026-11](../RICERCA-USABILITA-AL-TAVOLO-2026-11.md).

## Contesto

La serata del 2026-11-02 cominciava dal capitolo VII, il barile sulla tenda
di Zog'tar. Il capitolo cita Zog'tar 60 volte e non dice com'è, chi è o cosa
vuole; la sua scheda d'entrata col ritratto sta nel capitolo IV, i suoi numeri
in appendice, le mappe M7-C e M7-H nell'Appendice D del capitolo IV. I
validatori erano verdi. Il DM ha dovuto cercare.

La misura sui dieci booklet del DM (`misura_standard_tavolo.py`, 2026-11-03):
su 145 coppie capitolo × persona, 6 hanno numeri, aspetto, ritratto, chi è,
cosa vuole e tattica insieme; i numeri stampati nel capitolo sono 0 su 145
(tutti in appendice, per ADR-0105 §7); la riga «chi è» c'è nel 6%; la mappa sta
nel capitolo dello scontro in 7 casi su 41.

La ricerca dice la stessa cosa da fuori: Paizo mette la scheda intera di un PNG
unico dove si combatte la prima volta, col ritratto accanto; l'Alexandrian
chiede una scheda della persona a voci (aspetto, come si interpreta, cosa sa,
statistiche) proprio perché il dettaglio sepolto in un paragrafo si perde al
tavolo; Questing Beast chiede che tutto quello che serve per un argomento stia
su una doppia pagina.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Nel capitolo i sei elementi della persona e la mappa dello scontro; l'appendice con tutti i riquadri resta** (scelta, come ha chiesto il DM) | al tavolo non si gira pagina; il capitolo si può stampare da solo; l'appendice resta l'indice di tutte le creature, «fatta bene» | più pagine; lo stesso riquadro stampato due volte |
| Solo l'appendice, come oggi (ADR-0105 §7, modello WotC) | pagine corte, un riquadro solo | è quello che al tavolo non ha funzionato |
| Scheda intera alla prima comparsa nel volume, poi «vedi p. N» (modello Paizo) | meno ripetizioni | i nostri capitoli si riusano in più volumi (il DEF-4 è in tre booklet) e la serata parte dal capitolo che serve, non dal primo: «la prima comparsa» cambia da un volume all'altro e il rimando torna a far girare pagina |
| Un capitolo «cast» con tutte le persone (la lista avversari dell'Alexandrian, la cassetta del Drappo) | una pagina da tenere aperta | è un'altra appendice: il problema era cercare fuori dal capitolo |

Il rischio della copia doppia è che le due copie divergano. Non succede se il
riquadro del capitolo e quello dell'appendice escono dallo stesso recinto
` ```statblocco ` del master: il generatore li stampa, nessuno li riscrive.

## Decisione

1. **In ogni capitolo dove una persona si incontra** (un PNG o un cattivo con
   un nome: ci parla, ci combatte, ci si nasconde), accanto alla sua scheda
   stanno:
   - **Chi è**: una riga, il suo ruolo in questa storia;
   - **Aspetto**: una o due frasi, da leggere quando la vedono;
   - **Vuole**: cosa vuole, e cosa teme;
   - **Ritratto**: la sua immagine, con la regola di quando mostrarla;
   - **Numeri**: il riquadro intero di ADR-0105;
   - **Tattica**: quella di questo incontro.

   La scheda d'entrata di ADR-0073 prende la riga **Chi è** come prima voce;
   le altre (Suona, Sa, Eco) restano.
2. **L'appendice resta**: tutti i riquadri, in ordine di nome, come la fa oggi
   `appendice-creature`. Il manifest dice `"schede": "entrambi"`; `"appendice"`
   e `"qui"` restano per i volumi che li vogliono.
3. **La mappa dello scontro sta nel capitolo dello scontro**, in pianta di
   stampa (ADR-0106), con la legenda. Se la stessa mappa serve in due
   capitoli, si stampa in tutti e due.
4. **Le creature senza nome** (guardie, wyvern, mostri) hanno nel capitolo i
   numeri e la tattica; chi è e cosa vuole non servono.
5. **Un capitolo preso da un altro master** porta con sé le persone che ci si
   incontrano: il generatore le prende dal master o dal dossier (ADR-0091) e
   le mette nel capitolo, così il capitolo del barile ha Zog'tar anche se la
   sua scheda d'entrata è scritta nella Scena 7.
6. **La misura** è `scripts/misura_standard_tavolo.py`. Oggi è un indicatore;
   quando il primo booklet è convertito diventa un cricchetto in CI, con tetti
   per booklet che scendono soltanto, come `misura_statblocchi_booklet`.
7. **Prima di consegnare un booklet si legge da DM**, con il PDF e
   nell'ordine della serata: per ogni scontro mappa, scheda, ritratto e tattica
   devono stare entro una voltata di pagina. Il messaggio di consegna dice che
   cosa si è letto.

## Conseguenze

- I booklet si allungano: un riquadro e un ritratto in più per ogni persona e
  capitolo, e le mappe ripetute. I tetti di `misura_stampa` possono salire;
  se succede lo si dice, e lo decide il DM.
- Va scritto il pezzo del generatore (ancora `#persona(Nome)`, campo
  `"mappe"` nel capitolo del manifest, modo `"entrambi"`), e va aggiunta la
  riga «Chi è» alle schede d'entrata esistenti: ARC-07 prima, poi Palio,
  Giardino, Drappo e Abbazia, dove oggi le persone sono descritte in prosa.
- Le skill `rumblingstone-module-standard` (scheda d'entrata con «Chi è», il
  controllo capitolo per capitolo) e `rumblingstone-playtest` (la lettura da
  DM con il PDF) vanno aggiornate.
- La misura conta le voci con l'etichetta, non la loro qualità: la lettura da
  DM resta il giudizio.

## Da rivedere se

- al tavolo il DM trova che le pagine in più rallentano più di quanto aiuti
  avere tutto nel capitolo;
- la misura conta troppe persone citate e non incontrate, e serve marcare nel
  master dove una persona si incontra davvero (il *Chi* del contratto «In
  scena» di ADR-0073 lo fa già, dove c'è);
- un booklet per i giocatori ha bisogno dei ritratti senza i numeri.
