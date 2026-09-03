# Le licenze di questo repo

> Non è una licenza sola, ed è deliberato. Questo repo è **per tre quarti prosa**
> e per un quarto strumenti: applicare a entrambi la stessa licenza avrebbe
> significato sbagliarne una. Decisione:
> [ADR-0029](plans/adr/ADR-0029-licenza-doppia-testo-e-script.md), che sostituisce
> il `LICENSE` GPL-3.0 unico e richiama esplicitamente il perimetro di
> [ADR-0005](plans/adr/ADR-0005-confini-ip-uso-non-commerciale.md).

## Il taglio, in due righe

| Cosa | Licenza | File |
|---|---|---|
| **Il testo** — avventure, moduli, canone, guide, piani, ADR, skill, tavole e immagini prodotte qui | **CC BY-NC-SA 4.0** | [`LICENSE`](LICENSE) |
| **Gli strumenti** — tutto ciò che sta in `scripts/` (Python, Typst, CI) | **MIT** | [`scripts/LICENSE`](scripts/LICENSE) |

In caso di dubbio su un file: **se lo legge un essere umano al tavolo è testo; se
lo esegue una macchina è strumento.**

## Perché due

- **Il testo** è un'opera dell'ingegno, e CC BY-NC-SA è scritta per quelle: dà
  attribuzione, impone la stessa licenza a chi lo rielabora, e **vieta l'uso
  commerciale** — che è esattamente la postura che ADR-0005 dichiara da sempre e
  che la GPL, scritta per il software, non sapeva dire.
- **Gli strumenti** sono utili fuori di qui — un validatore di prosa italiana, un
  esportatore Typst con colophon, un convertitore HTML→markdown — e MIT è la
  licenza che non contamina chi li riusa. Un DM che vuole il nostro
  `validate_prosa.py` per la sua campagna non deve ereditare la licenza della
  nostra campagna.

## ⚠️ Cosa queste due licenze NON coprono

Sono tre cose, e ignorarle è il modo di trasformare una licenza in un problema.

### 1. Il contenuto SRD 3.5 resta sotto OGL 1.0a

Statblocchi, incantesimi, classi, oggetti magici e regole derivati dal **System
Reference Document 3.5** sono **Open Game Content** e restano governati dalla
**Open Game License 1.0a**, non da CC BY-NC-SA. Le due cose convivono nello
stesso repo perché riguardano **porzioni diverse** del materiale: la prosa
originale è nostra e va sotto CC; ciò che deriva dall'SRD resta OGC.

> **Chi ridistribuisce materiale di questo repo che contenga OGC** deve
> accompagnarlo con la Sezione 15 dell'OGL (la catena delle dichiarazioni di
> copyright). Non è un adempimento nostro finché il repo resta a uso privato: lo
> diventa nel momento in cui qualcosa esce, ed è **parte del cancello d'uscita**
> di [`docs/guides/GUIDA-CONDIVISIONE-IP.md`](docs/guides/GUIDA-CONDIVISIONE-IP.md) §7.

### 2. I marchi altrui non si licenziano perché si nominano

*Dungeons & Dragons*, *Forgotten Realms*, i nomi di divinità e luoghi dei Reami e
ogni altro marchio di Wizards of the Coast **restano dei rispettivi titolari**.
Metterli sotto CC BY-NC-SA non li rende nostri da dare. ADR-0005 è la regola che
governa il loro uso, e questa licenza non la allarga di un millimetro.

### 3. I componenti di terzi tengono la loro licenza

Sono vendorizzati, con il loro file `LICENSE` **integro** — è la condizione per
cui possiamo tenerli:

| Componente | Licenza | Dove | ADR |
|---|---|---|---|
| `droplet` 0.3.1 — capolettera annegato | MIT © Eric Biedert | `scripts/typst/packages/preview/droplet/` | [ADR-0026](plans/adr/ADR-0026-vendoring-pacchetti-typst.md) |
| `in-dexter` 0.7.2 — indice analitico | Apache-2.0 © JKRB e contributori | `scripts/typst/packages/preview/in-dexter/` | [ADR-0026](plans/adr/ADR-0026-vendoring-pacchetti-typst.md) |
| `systematic-debugging` — metodo delle 4 fasi | MIT © 2025 Jesse Vincent | `skills/rumblingstone-debugging/` | [ADR-0010](plans/adr/ADR-0010-vendoring-skill-terzi.md) |

**MIT su `scripts/` non si applica a `scripts/typst/packages/`**: quella cartella
è codice di terzi, e le sue licenze sono quelle della tabella.

Dipendenze **non** vendorizzate, cioè eseguibili che ognuno installa da sé e che
non stanno nel repo: `typst` (Apache-2.0, [ADR-0020](plans/adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md))
e `pdfcpu` (Apache-2.0, [ADR-0027](plans/adr/ADR-0027-imposizione-con-pdfcpu.md)).
L'elenco vivo sta in [`scripts/binari.py`](scripts/binari.py).

## Se vuoi usare qualcosa

- **Giocare questo materiale al tuo tavolo** → sì, liberamente. È il caso per cui
  esiste.
- **Rielaborarlo e ripubblicarlo gratis, citando la fonte** → sì, con la stessa
  licenza (è cosa vuol dire *ShareAlike*), e con la Sezione 15 dell'OGL se porti
  con te dell'OGC.
- **Riusare uno script** → sì, MIT, fai pure. Ci fa piacere.
- **Venderlo, in qualunque forma** → **no.** CC BY-NC-SA lo vieta, e prima ancora
  lo vieta ADR-0005 finché non è stata eseguita la bonifica §7. Se stai pensando
  di farlo, la conversazione comincia da lì e non da questa pagina.

*Questa pagina descrive delle scelte, non è un parere legale. Il testo che vale è
quello dei file `LICENSE`.*
