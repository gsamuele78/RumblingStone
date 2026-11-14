# Guida: provare la trascrizione locale di una serata

> Forma: **guida pratica** ([Diátaxis](../../plans/adr/ADR-0123-la-documentazione-segue-diataxis.md)).

> **A chi serve.** Al DM che vuole provare, su **una** serata, se la
> trascrizione automatica gli fa risparmiare tempo nello scrivere il log.
> È una prova misurata, non un'adozione
> ([ADR-0135](../../plans/adr/ADR-0135-la-trascrizione-della-serata-e-una-bozza-locale.md)).
> La proposta e l'obiezione che la cambia sono in
> [`RICERCA-TOOL-ESTERNI-DM-2026-08.md`](../../plans/RICERCA-TOOL-ESTERNI-DM-2026-08.md) §3 e §3.1.
> Tutto gira sul PC del DM: l'audio non esce mai dalla macchina.

---

## §0 · Le cinque regole, prima di tutto

1. **Il consenso si chiede prima di registrare**, a ogni giocatore, a voce, a
   inizio serata. Chi dice no vince: non si registra. Lo script non parte senza
   `--consenso`, che è la tua dichiarazione di averlo chiesto.
2. **La bozza non è mai canone.** Porta un segno in testa; con quel segno
   `state_apply` la rifiuta e `session_recap` la salta. Il log lo scrivi e lo
   firmi tu, come sempre, con `python3 scripts/dm.py session end`.
3. **La trascrizione serve a te, non al tavolo.** Non si consegna ai giocatori e
   non sostituisce i loro appunti: chi prende appunti continua a prenderli.
4. **«Cosa hanno capito male» si scrive a mano.** La bozza ha il campo vuoto: la
   macchina non sa cosa era vero.
5. **Audio, trascrizione e nomi dei giocatori non entrano mai nel repo.** Lo
   script si rifiuta di scrivere dentro la copia del repo, e la bozza nomina
   solo i PG. Nel repo entrano soltanto i **numeri** della misura (§4).

---

## §1 · Registrare (Bazzite / KDE)

**Il microfono conta più del modello.** Un solo microfono omnidirezionale al
centro del tavolo, a circa un metro da tutti: un microfono USB da conferenza o
da tavolo va bene. Il microfono del portatile, vicino alla ventola, è la scelta
peggiore. Il telefono, appoggiato al centro, è un buon secondo registratore di
riserva.

Bazzite usa PipeWire, e `pw-record` c'è già.

```bash
wpctl status                       # sotto «Sources» trova il numero del microfono, es. 57
mkdir -p ~/RumblingStone-serate/2026-11-20
pw-record --target 57 --rate 48000 --channels 1 \
    ~/RumblingStone-serate/2026-11-20/serata.flac
# Ctrl-C a fine serata
```

Un FLAC mono a 48 kHz occupa circa 150-200 MB l'ora. Se preferisci una
finestra, Audacity (Flatpak, «Discover») registra lo stesso file.

**Prima della serata, una prova di un minuto**: registra te stesso che parli
dalla sedia più lontana dal microfono e trascrivila (§3). Se non si capisce lì,
non si capirà nemmeno dopo quattro ore.

---

## §2 · Installare whisper.cpp con la RTX 4050

whisper.cpp ha licenza MIT, non ha dipendenze e gira tutto in locale. Su
Bazzite il sistema è immutabile: lo si compila in una distrobox, che con
`--nvidia` vede la scheda.

```bash
distrobox create --nvidia --name whisper \
    --image registry.fedoraproject.org/fedora-toolbox:43
distrobox enter whisper
sudo dnf install -y git cmake gcc-c++ ffmpeg-free \
    vulkan-headers vulkan-loader-devel glslc
cd ~ && git clone https://github.com/ggml-org/whisper.cpp && cd whisper.cpp
cmake -B build -DGGML_VULKAN=1 && cmake --build build -j --config Release
sh models/download-ggml-model.sh large-v3-turbo-q8_0     # ~870 MB, il consigliato
sh models/download-vad-model.sh silero-v6.2.0            # salta i silenzi
./build/bin/whisper-cli --help | head -3                  # deve rispondere
```

Al primo avvio `whisper-cli` scrive quale dispositivo usa: deve comparire la
RTX 4050 (Vulkan). Se compare solo la CPU, il passaggio della scheda nella
distrobox non è andato, e lo script funziona lo stesso ma molto più piano.

**Perché Vulkan e non CUDA.** Vulkan usa il driver che Bazzite ha già; CUDA
chiede il toolkit NVIDIA nella distrobox. Se la trascrizione di un'ora supera
i 10 minuti, vale la pena provare CUDA (`-DGGML_CUDA=1` in un'immagine
`nvidia/cuda:*-devel`): è di solito più veloce, ma non l'ho misurato.

**Quale modello, in 6 GB.** Ci stanno tutti, anche `large-v3` intero (circa
4 GB in memoria). Il consigliato è `large-v3-turbo-q8_0`: stesso codificatore
di `large-v3`, decodificatore molto più piccolo, quindi molto più veloce, con
una perdita piccola sull'italiano (che per whisper è una lingua con molti dati).
Se nella misura del §4 i nomi o le frasi escono male, la prova da fare è
`large-v3-q5_0` sugli stessi spezzoni: è più lento, non è detto che sia meglio.

---

## §3 · Trascrivere e leggere la bozza

Dalla copia del repo (anche fuori dalla distrobox, se `whisper-cli` è nel PATH;
altrimenti con `--whisper`):

```bash
python3 scripts/transcribe_session.py trascrivi \
    ~/RumblingStone-serate/2026-11-20/serata.flac --consenso \
    --out ~/RumblingStone-serate/2026-11-20 --data 2026-11-20 \
    --whisper ~/whisper.cpp/build/bin/whisper-cli \
    --modello ~/whisper.cpp/models/ggml-large-v3-turbo-q8_0.bin \
    --vad-modello ~/whisper.cpp/models/ggml-silero-v6.2.0.bin
```

Nella cartella trovi:

| File | Cos'è |
|---|---|
| `trascrizione.txt` / `.srt` / `.json` | Il testo con i tempi. Non dice **chi** parla: whisper.cpp non distingue le voci in italiano |
| `bozza-session.md` | Il log nel formato del template, con le sezioni pubbliche **vuote**. Sotto `## DM notes`: il campo «Cosa hanno capito male», i momenti candidati (bottino, PX, clock e giorni, decisioni e fine serata) col minuto, e l'indice dei nomi della campagna |
| `misura.json` | Modello, minuti di audio, minuti di trascrizione |

Come si usa: apri la bozza accanto al lettore audio, salta ai minuti che ti
servono, e scrivi il log con `dm.py session end` come hai sempre fatto. Le
sezioni pubbliche le scrivi tu: la macchina non riassume, e nessuna riga
automatica arriva nel recap dei giocatori.

**Cosa aspettarsi, onestamente.** I nomi inventati della campagna sono la
parte che whisper sbaglia di più (§5). Ai numeri e all'italiano di tutti i
giorni va molto meglio. Sopra la musica di sottofondo o a lunghi silenzi whisper
può inventare frasi: il modello VAD serve a questo, ma rileggi i passaggi
importanti ascoltandoli.

---

## §4 · La misura: cosa resta buono e quanto tempo risparmi

Tre numeri, tutti da prendere sulla stessa serata.

**M1 · Quanta trascrizione resta buona.** Scegli tre spezzoni di cinque minuti
(l'inizio, un combattimento, un momento di decisione). Tagliali:

```bash
cd ~/RumblingStone-serate/2026-11-20
ffmpeg -ss 00:12:00 -t 300 -i serata.flac s1.flac     # e così s2, s3
```

Trascrivili, poi copia ogni `trascrizione.txt` in `s1-corretta.txt` e
correggila ascoltando: solo le parole sbagliate, non lo stile. Poi:

```bash
python3 scripts/transcribe_session.py misura s1/trascrizione.txt s1-corretta.txt
```

Esce `parole_buone` (la parte che non hai dovuto toccare) e, per i nomi della
campagna, quanti erano giusti e quanti whisper ne ha messi dove non c'erano.

**Prova A/B sui nomi.** Rifai gli stessi tre spezzoni con `--nomi-nel-prompt`
(lo script passa a whisper i nomi di `state.yaml`) e confronta. Attenzione: il
prompt funziona solo col contesto del testo precedente acceso, e quel contesto
fa saltare a whisper le frasi che somigliano a una già detta. Nella prova del §5
il prompt correggeva alcuni nomi ma ne **sostituiva** altri (Tordek diventava
Thorik): per questo di serie è spento, e il contesto pure (`-mc 0`).

**M2 · Quanta bozza ti è servita.** Mentre scrivi il log, spunta `[x]` i
momenti candidati che hai usato. Poi:

```bash
python3 scripts/transcribe_session.py misura-bozza bozza-session.md
```

**M3 · Il tempo.** Cronometra quanto ci metti a scrivere il log **con** la
bozza, ascolto compreso. Il confronto è con quanto ci metti di solito senza:
se non l'hai mai cronometrato è una stima, e va detto come tale.

Mandami i tre numeri (o scrivili in
`plans/esperimenti/trascrizione-2026-11-14/MISURE.md`): solo numeri, mai
frasi della trascrizione né nomi dei giocatori. La soglia per parlare di
adozione la decidi tu sulla misura; la proposta è nell'ADR-0135.

---

## §5 · La prova già fatta (non personale)

Nel container del repo, senza GPU, su audio che non è di nessun tavolo:

- **italiano vero**: 40 frasi del set FLEURS (CC BY 4.0), 10,8 minuti, lettori
  umani;
- **nomi della campagna**: un copione finto di 16 battute letto da una voce
  sintetica (Piper, voce `it_IT-paola-medium`, CC0), pulito e con rumore e eco.

I numeri e il banco per rifarli sono in
[`plans/esperimenti/trascrizione-2026-11-14/`](../../plans/esperimenti/trascrizione-2026-11-14/MISURE.md).
In breve:

- sull'italiano letto, con le opzioni di serie, whisper sbaglia il **5,8%**
  delle parole; con il contesto del testo precedente acceso (il default di
  whisper) il **16,6%**, perché salta interi pezzi che somigliano a frasi già
  dette. Per questo lo script passa sempre `-mc 0`;
- sui nomi inventati ne sbaglia **più della metà** (6 giusti su 20), ma la voce
  sintetica pronuncia male proprio quelli, quindi quel numero va preso con le
  pinze;
- numeri di tiri, danni, monete, PX e giorni escono giusti in tutte le prove;
- sulla CPU del container va a circa una volta il tempo reale: sulla scheda va
  misurato.

La misura vera è la tua serata.

---

## §6 · Se qualcosa non va

| Sintomo | Cosa fare |
|---|---|
| `Manca whisper-cli` ed esce con codice 3 | Non è un errore: ripeti il §2 o passa `--whisper` col percorso |
| `Serve --consenso` | Hai chiesto a tutti? Allora aggiungi `--consenso` |
| `non entrano mai nel repo` | `--out` punta dentro la copia del repo: usa `~/RumblingStone-serate/…` |
| Frasi ripetute o inventate nei silenzi | Aggiungi `--vad-modello` |
| Pezzi interi che mancano | Hai usato `--nomi-nel-prompt`? Riaccende il contesto: toglilo |
| `state_apply` dice «ancora una bozza» | Il log non è ancora tuo: riscrivilo con il wizard e togli le due righe di testa |
