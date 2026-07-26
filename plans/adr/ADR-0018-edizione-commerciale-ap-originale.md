# ADR-0018 — L'edizione commerciale è un Adventure Path **originale autonomo**, mai un'espansione di *Red Hand of Doom*

**Stato**: proposta — **gate: decisione DM + verifica di un avvocato IP**
**Rev. 2** (2026-07-26, stessa giornata): ⚠️ **perimetro corretto** — la misura iniziale cercava solo RHoD e i toponimi FR ed era incompleta. `campaign-history.md` dichiara **altre quattro fonti WotC** (*Expedition to Undermountain* con numeri di pagina, *Underdark*, *Out of the Abyss*, lore FR/Salvatore). Vedi audit §6-bis
**Data**: 2026-07-26
**Decisione-fonte**: domanda DM del 2026-07-26 sulla vendibilità come espansione 3.5 / Paizo. Misura in [`docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md`](../../docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md). **Estende** [ADR-0005](ADR-0005-confini-ip-uso-non-commerciale.md) senza sostituirlo, come [ADR-0017](ADR-0017-separazione-prodotto-e-rilicenziamento-toolkit.md) ha fatto per il toolkit.

## Contesto

ADR-0005 stabiliva che il repo non è commercializzabile e che il blocco
WotC/Forgotten Realms è **assorbente per tutto il repo**. ADR-0017 ha già
mostrato che quella conclusione valeva per il *contenuto*, non per il toolkit.
Resta la domanda vera: **il contenuto può diventare un prodotto?**

La misura dice qualcosa che nessuno aveva quantificato prima: **la derivazione da
RHoD non è distribuita, è concentrata.**

| Arco | Parole | Densità RHoD (per 1.000 parole) |
|---|---:|---:|
| 04 · 06 | 19.101 | **0,0** |
| 07 | 151.588 | **0,3** |
| 08 | 81.422 | **1,1** |
| 09 | 195.739 | **5,3** |
| 00 (impalcatura) | 7.750 | 20,2 |

**252.111 parole stanno a densità ≈ 0,5**: naming, non struttura. E le due spine
narrative sono diverse — RHoD va da Guado di Drellin all'assedio di Brindol;
RumblingStone va dalla miniera alla Corona di Adamantio, ai piani elementali, a
Hammerfist, con antagonisti originali (Il Collezionista, Sonjak, Therysol) e una
riscalatura all'8° livello.

L'arco 09 è l'eccezione, e lo è **per scelta**: il piano
`PIANO-REINTEGRAZIONE-PNG-AP-RHOD` (chiuso il 2026-07-20) reintegrò
deliberatamente PNG e luoghi dell'AP originale.

## Decisione

**Se e quando si pubblica, si pubblica un Adventure Path originale autonomo. Mai
un'espansione, un supplemento o un «sequel» di *Red Hand of Doom*.**

### 1. La via esclusa, e perché non ha varianti prudenti

Un'espansione *per* RHoD deve nominarlo: titolo, trama, cast, luoghi. Nessuna
licenza lo copre — l'OGL riguarda le meccaniche dichiarate Open Game Content e
RHoD non lo è; la Community Use Policy di Paizo è **non commerciale** e riguarda
IP Paizo; DMs Guild non licenzia RHoD ed è solo 5e. **La richiesta stessa è il
problema**: non esiste un modo più cauto di formularla.

### 2. La via scelta

AP originale autonomo, meccaniche sotto **OGL 1.0a** (3.5 e/o PF1e), più — per
PF1e — la **Compatibility License** di Paizo, che oggi non richiede
registrazione. Ambientazione, pantheon, geografia e fazioni **originali**.

Marchi: «Dungeons & Dragons», «D&D» e il logo d20 **non sono usabili** (la d20
System Trademark License non è più disponibile). Si comunica per compatibilità,
con la formula ammessa dalla licenza scelta.

### 3. Rinominare non basta — e il criterio è dichiarato

Il metro non è «ho cambiato i nomi» ma la **somiglianza sostanziale
dell'espressione protetta**: sequenza degli eventi, personaggi distintivi,
ambientazioni specifiche. Per questo la bonifica **non è un find-and-replace**, e
per questo l'arco 09 va trattato diversamente dagli altri (§4).

Regola operativa: ogni sostituzione deve produrre un elemento che **starebbe in
piedi da solo**, non un sinonimo trasparente. «Mano Rossa» → «Artiglio Cremisi»
è un sinonimo trasparente e non serve a niente.

### 4. Perimetro della v1

| Materiale | Decisione |
|---|---|
| **Archi 07 + 08** (233.010 parole) | **dentro** — è la base del prodotto. Sono gli unici due corpi grandi puliti da *entrambe* le fonti: arco 07 (RHoD 0,3 · Undermountain 0,2), arco 08 (1,1 · 0,0) |
| **Archi 01-05** (non scritti) | **dentro, ma da SCRIVERE originali.** Non esiste testo da bonificare: esiste testo da scrivere, e scriverlo originale costa quanto scriverlo derivato. È l'unico punto del repo in cui diventare originali è **gratis** — vedi `SOGGETTO-DISCESA-UNDERDARK-ARCHI-01-05.md` |
| Arco 06 — Corona di Adamantio (16.271) | ⚠️ **riscrittura**: densità *Undermountain* **8,8**, la più alta del repo |
| ~~Archi 04-08 come blocco~~ | ~~dentro~~ — **superato dalla rev. 2**: l'arco 04 è un adattamento dichiarato (p.117) ed è **intitolato a una località WotC** (*Belkram's Fall*, 232 occorrenze in 49 file) |
| Arco 09 (195.739 parole) | **fuori dalla v1.** Rientra solo dopo riscrittura sostanziale, valutata a sé |
| Arco 00 (impalcatura, tabelle armate) | si **rigenera** originale |
| `campaign/`, `state.md`, i log di sessione, i booklet | **restano privati per sempre**: sono il diario del tavolo, non un prodotto |

### 5. Moradin è un lotto narrativo, non una sostituzione

1.502 occorrenze, e l'SRD 3.5 esclude deliberatamente i nomi delle divinità:
Moradin è Product Identity. Ma è anche la spina teologica di una campagna nanica
— Cuore di Moradin, Corona di Adamantio, Forgia Eterna, *Canto della Pietra e del
Fuoco*. **Va trattato come riscrittura narrativa**, non come find-and-replace: è
il singolo lotto di contenuto più grande dell'intera bonifica, più grande del
nome-fazione.

### 6. La bonifica si verifica in continuo, non una volta

Il contratto unico dei finding del `PIANO-PRODOTTO-TOOLKIT-VENDIBILE` (lotto
P2.0) fornisce il meccanismo: un check `ip/forbidden-term` con la lista dei
termini vietati come **dato versionato**, severità `error` sul ramo commerciale
e `info` sul ramo privato. Una bonifica fatta a mano si erode alla prima
sessione; una verificata in CI no.

## Conseguenze

**Cosa diventa più facile**

- esiste un prodotto di contenuto reale — **233.000 parole già scritte e pulite**
  (archi 07+08) più gli archi 01-05 da scrivere: due manuali abbondanti subito,
  invece di un «forse un giorno»;
- il perimetro è **dichiarato**: si sa cosa è dentro (07+08, e 01-05 da scrivere
  originali), cosa è fuori (09, arco 06 da riscrivere, campagna giocata) e
  perché, invece di rimandare la domanda a ogni file nuovo;
- si smette di aggiungere debito: ogni contenuto nuovo può nascere già pulito, a
  costo zero, invece di essere bonificato dopo;
- il ramo privato resta **intatto**: la campagna al tavolo continua con Moradin,
  i Forgotten Realms e la Mano Rossa. Non si tocca il gioco.

**Cosa diventa più difficile / a cosa si rinuncia**

- **si rinuncia all'arco 09 nella v1** — 195.739 parole, il volume maggiore. È il
  costo della scelta, e va detto senza addolcirlo;
- la sostituzione del pantheon è una riscrittura narrativa, non un'operazione
  meccanica: settimane, non giorni;
- due varianti dello stesso contenuto (privata e commerciale) vanno tenute
  allineate, o divergono. Mitigazione: la commerciale **deriva** dalla privata
  con una trasformazione dichiarata e verificata, mai una copia a mano;
- **questa non è consulenza legale.** Prima di pubblicare serve un avvocato IP:
  la somiglianza sostanziale non è autocertificabile, e questo ADR non pretende
  di esserlo.

**Cosa va rivisitato e quando**

- **la lezione della rev. 2 vale come metodo**: prima di dichiarare pulito un
  arco, si cercano **tutte** le fonti dichiarate in `campaign-history.md`, non
  solo quella che si ha in mente. La misura parziale è più pericolosa
  dell'assenza di misura, perché dà fiducia;
- se un avvocato IP giudicasse insufficiente la trasformazione degli archi 07-08,
  il perimetro si restringe — e la decisione va presa **prima** della produzione
  editoriale, non dopo;
- se si scegliesse la via DMs Guild (solo 5e) per tenere i Forgotten Realms,
  questo ADR va riscritto: sarebbe un prodotto diverso, con un altro pubblico;
- l'arco 09 si rivaluta a sé, dopo la v1.
