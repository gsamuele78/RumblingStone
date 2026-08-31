// tema-rumblingstone.typ — il tema di stampa del repo (ADR-0020).
//
// Lo usa scripts/export_booklet_typst.py: NON si modifica il .typ generato,
// si modifica questo. Il contenuto arriva dai master markdown (ADR-0003).
// Impaginazione da manuale: due colonne, carta avorio, capolettera, fregi,
// box read-aloud, tabelle a righe alternate, indice cliccabile.
//
// I font sono in `scripts/fonts/` — EB Garamond, Cinzel e Inconsolata, tutti
// OFL, tutti embeddati. Nessun font di sistema: è il motivo per cui esiste
// questa catena (ADR-0020 §Attuazione).

#let avorio    = rgb("#f6efe0")
#let inchiostro = rgb("#241d16")
#let seppia    = rgb("#6b4f2a")
#let rosso     = rgb("#7d2b1f")
#let boxLeggi  = rgb("#ece0c6")
#let boxLato   = rgb("#efe6d2")

#let SERIF = "EB Garamond"
#let TITOLI = "Cinzel"
#let MONO = "Inconsolata"

// Apertura di capitolo: il medaglione + il titolo, su tutta la larghezza delle
// due colonne. È il segno che dice al lettore dov'è prima che legga il titolo.
#let capitolo-aperto(titolo, fregio) = {
  // L'heading (voce d'indice + segnalibro PDF) va emesso PRIMA del float:
  // altrimenti la testatina della pagina d'apertura mostra ancora il capitolo
  // precedente, perché la query si risolve prima che il float atterri.
  hide(heading(level: 1, titolo))
  place(top, float: true, scope: "parent", clearance: 14pt)[
    #block(width: 100%, above: 0pt)[
      #line(length: 100%, stroke: 0.6pt + seppia)
      #v(7pt)
      #grid(columns: (1.5cm, 1fr), column-gutter: 10pt, align: horizon,
        if fregio != none { image(fregio, width: 1.5cm) } else { [] },
        text(font: TITOLI, size: 17pt, weight: 600, fill: rosso)[#titolo])
      #v(5pt)
      #line(length: 100%, stroke: 0.6pt + seppia)
    ]
  ]
}

// Typst non ha un «content → string» nativo: serve per leggere il «§N» dai titoli.
#let to-string(c) = {
  if type(c) == str { c }
  else if c.has("text") { c.text }
  else if c.has("children") { c.children.map(to-string).join("") }
  else if c.has("body") { to-string(c.body) }
  else if c == [ ] { " " }
  else { "" }
}

// Una figura: se è più larga che alta scavalca le due colonne (le tavole
// d'ambiente), se è verticale sta in colonna (i ritratti). La didascalia è
// l'alt del markdown.
#let figura(percorso, alt, larga: false) = {
  let corpo = block(breakable: false, width: 100%)[
    #image(percorso, width: 100%)
    #v(2pt)
    #text(size: 8pt, style: "italic", fill: seppia)[#alt]
  ]
  if larga { place(top, float: true, scope: "parent", clearance: 12pt, corpo) }
  else { corpo }
}

#let fregio() = align(center)[
  #v(0.3em)
  #text(fill: seppia, size: 11pt)[❦]
  #v(0.3em)
]

// Segno di fine voce: il rombo che i manuali mettono in coda a una sezione per
// dire «questa voce finisce qui» senza spendere una riga bianca.
#let fine = box(baseline: 0%)[#h(0.35em)#text(fill: seppia, size: 8pt)[⬦]]

// Read-aloud: il testo che si legge ad alta voce al tavolo.
#let leggi(body) = block(
  width: 100%, fill: boxLeggi, inset: (x: 9pt, y: 8pt), radius: 2pt,
  stroke: (left: 2pt + seppia),
  breakable: true,
)[#text(style: "italic", size: 9.4pt, fill: inchiostro)[#body]]

// Nota di regia per il DM.
#let nota(body) = block(
  width: 100%, inset: (x: 8pt, y: 6pt),
  stroke: (left: 1.5pt + rgb("#b9a789")),
  breakable: true,
)[#text(size: 9pt, fill: rgb("#4a3f33"))[#body]]

// Riquadro laterale: la regola opzionale, la nota d'ambientazione, la variante.
// È il terzo caso che mancava — `leggi` è per i giocatori, `nota` è per la
// regia, questo è per il regolamento che si può anche non usare.
#let riquadro(titolo: "", body) = block(
  width: 100%, fill: boxLato, inset: (x: 9pt, y: 8pt), radius: 2pt,
  stroke: 0.6pt + seppia.lighten(30%),
  breakable: true,
)[
  #if titolo != "" [
    #text(font: TITOLI, size: 9.5pt, weight: 600, fill: rosso, tracking: 0.4pt)[#upper(titolo)]
    #v(3pt)
    #line(length: 100%, stroke: 0.4pt + seppia.lighten(40%))
    #v(3pt)
  ]
  #text(size: 9pt)[#body]
]

// Capolettera «versale»: la maiuscola d'apertura, grande, sulla riga del testo.
//
// ⚠️ È un versale, non un capolettera annegato: il testo NON scorre attorno
// alla lettera. Farlo annegato richiede di misurare il paragrafo e spezzarlo
// riga per riga — è quello che fa il pacchetto `droplet`, che però va preso
// dalla rete a ogni compilazione (o vendorizzato con la sua licenza). Il
// versale dà lo stesso segno d'apertura, costa zero dipendenze, e non può
// rompersi su un paragrafo corto. Se un giorno si vuole l'annegato, si apre
// un ADR sul vendoring dei pacchetti Typst: la decisione è quella, non il CSS.
#let capolettera(lettera, corpo) = {
  set par(first-line-indent: 0pt)
  par[#box(baseline: 25%)[
      #text(font: TITOLI, size: 2.6em, weight: 600, fill: rosso)[#lettera]
    ]#h(0.05em)#corpo]
}

// Una figura. In due colonne un'immagine più larga della colonna va in float a
// piena larghezza, esattamente come le tabelle larghe: dentro la colonna
// verrebbe scalata fino a non vedersi più.
#let figura(percorso, didascalia: none, larga: false, alt: none) = {
  let corpo = figure(
    image(percorso, width: 100%, alt: alt),
    caption: if didascalia == none { none } else {
      text(size: 8.4pt, style: "italic", fill: seppia)[#didascalia]
    },
    supplement: none,
    numbering: none,
  )
  if larga { place(top, float: true, scope: "parent", clearance: 12pt, block(width: 100%, corpo)) }
  else { block(width: 100%, above: 0.8em, below: 0.8em, corpo) }
}

// Una tabella da 4+ colonne in una colonna da 8 cm diventa illeggibile: si
// spezzano perfino le parole del titolo. Sopra quella soglia scavalca le due
// colonne, che è quello che fa un manuale stampato.
#let tabella(n, ..celle) = {
  let corpo = block(breakable: true)[
  #table(
    columns: n,
    stroke: none,
    inset: (x: 6pt, y: 4.5pt),
    fill: (_, row) => if row == 0 { seppia.lighten(60%) }
                      else if calc.odd(row) { boxLato } else { none },
    ..celle
  )
]
  if n >= 4 { place(top, float: true, scope: "parent", clearance: 10pt, corpo) }
  else { corpo }
}

// Blocco statistiche: il riquadro del mostro/PNG, coi numeri dove il DM li
// cerca invece che dentro un paragrafo (ADR-0021). I campi arrivano già
// strutturati da `dmcore.statblock`: qui c'è solo la forma.
#let statblocco(
  nome: "", tipo: "", gs: "", iniziativa: "", sensi: "",
  ca: "", pf: "", ts: "", velocita: "",
  attributi: (), attacchi: (), voci: (), tattica: "", fonte: "",
  larga: false,
) = {
  let corpo = block(
    width: 100%, fill: boxLato, inset: (x: 9pt, y: 8pt), radius: 2pt,
    stroke: (top: 1.4pt + rosso, bottom: 1.4pt + rosso),
    breakable: true,
  )[
    #grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
      text(font: TITOLI, size: 12pt, weight: 600, fill: rosso)[#nome],
      if gs != "" { text(font: TITOLI, size: 9pt, fill: seppia)[GS #gs] } else { [] })
    #if tipo != "" [ #v(1pt) #text(size: 8.6pt, style: "italic", fill: seppia)[#tipo] ]
    #v(3pt)
    #line(length: 100%, stroke: 0.5pt + seppia)
    #v(3pt)
    #set text(size: 8.8pt)
    #let riga(e, v) = if v != "" [ *#e* #v \ ]
    #riga("Iniziativa", iniziativa)
    #riga("Sensi", sensi)
    #riga("CA", ca)
    #riga("pf", pf)
    #riga("TS", ts)
    #riga("Velocità", velocita)
    #if attributi.len() > 0 [
      #v(2pt)
      #grid(columns: (1fr,) * attributi.len(), column-gutter: 4pt,
        ..attributi.map(((k, v)) => align(center)[
          #text(font: TITOLI, size: 7pt, fill: seppia)[#upper(k)] \
          #text(size: 9pt, weight: 600)[#v]
        ]))
      #v(2pt)
    ]
    #for a in attacchi [ *#a.at(0)* #a.at(1) \ ]
    #for v in voci [ *#v.at(0)* #v.at(1) \ ]
    #if tattica != "" [
      #v(2pt)
      #line(length: 100%, stroke: 0.4pt + seppia.lighten(40%))
      #v(2pt)
      #text(size: 8.4pt, style: "italic")[*Tattica.* #tattica]
    ]
    #if fonte != "" [ #v(2pt) #text(size: 7.4pt, fill: seppia)[#fonte] ]
  ]
  if larga { place(top, float: true, scope: "parent", clearance: 10pt, corpo) } else { corpo }
}

// `apparato: false` toglie frontespizio e indice. Serve a un fascicolo di
// schede: sei fogli da stampare e dare in mano, dove una copertina e un indice
// sarebbero due pagine da saltare ogni volta che si va alla fotocopiatrice.
//
// `carta: "bianca"` toglie il fondo avorio. Sessanta pagine di fondo pieno su
// una stampante di casa sono una cartuccia: il volume «da leggere» e il volume
// «da stampare stasera» non sono lo stesso file.
#let libro(titolo: "", sottotitolo: "", brand: "", banner: "", meta: "", capitolo: "",
           apparato: true, carta: "avorio", copertina: none, intro: none,
           corpo) = {
  let fondo = if carta == "bianca" { white } else { avorio }
  set document(title: titolo)
  set page(
    paper: "a4",
    // Margini SPECULARI: rilegato o pinzato, il margine interno finisce nella
    // piega. `inside`/`outside` è ciò che distingue un libro da una risma.
    margin: (inside: 2.0cm, outside: 1.5cm, top: 2.1cm, bottom: 2.0cm),
    binding: left,
    fill: fondo,
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: 8pt, fill: seppia, style: "italic")
        // La testatina destra segue il CAPITOLO corrente: è ciò che rende
        // sfogliabile un volume di sessanta pagine.
        let qui = query(selector(heading.where(level: 1)).before(here()))
        grid(columns: (1fr, 1fr),
          align(left)[#titolo],
          align(right)[#if qui.len() > 0 { qui.last().body } else { capitolo }],
        )
        v(-6pt)
        line(length: 100%, stroke: 0.4pt + seppia.lighten(40%))
      }
    },
    footer: context {
      set text(size: 9pt, fill: seppia)
      align(center)[#text(size: 7pt)[⬦]~#counter(page).display()~#text(size: 7pt)[⬦]]
    },
  )
  set text(font: SERIF, size: 10.2pt, fill: inchiostro, lang: "it")
  set par(justify: true, leading: 0.62em, first-line-indent: 1.1em)

  // Il § nei TITOLI diventa un numero dentro un medaglione — la stessa cornice
  // circolare dei fregi di capitolo, così il libro ha un segno solo invece di
  // due. Nei RIMANDI dentro il testo il § resta piatto: serve a ritrovare la
  // sezione («vedi §4»), e sostituirlo lì romperebbe i riferimenti.
  let medaglione(n) = box(baseline: 16%)[
    #circle(radius: 0.52em, stroke: 0.7pt + seppia, fill: none)[
      #align(center + horizon)[
        #text(font: TITOLI, size: 0.66em, fill: seppia, weight: 600)[#n]
      ]
    ]
  ]
  // Un titolo in fondo alla colonna, col suo testo nella colonna dopo, è il
  // difetto che si nota per primo sfogliando: `sticky` lo tiene attaccato.
  show heading: set block(above: 1.1em, below: 0.65em, sticky: true)
  show heading: it => {
    set text(font: TITOLI, fill: if it.level == 1 { rosso } else { seppia })
    if it.level == 1 { text(size: 15pt, weight: 600)[#it.body] }
    else {
      // «§3 · Titolo» → medaglione(3) + Titolo. Se il titolo non comincia con
      // un §, resta esattamente com'è.
      let grezzo = to-string(it.body)
      let m = grezzo.match(regex("^§\s*([0-9]+(?:[-–][a-z]+)?)\s*(?:·|-|—)?\s*(.*)$"))
      let dim = if it.level == 2 { 11.5pt } else { 10pt }
      if m != none {
        text(size: dim, weight: 600)[#medaglione(m.captures.at(0))~#m.captures.at(1)]
      } else {
        text(size: dim, weight: 600)[#it.body]
      }
    }
  }
  show strong: set text(fill: rgb("#4a2c12"), weight: 600)
  show raw: set text(font: MONO, size: 9pt)

  if not apparato {
    corpo
    return
  }

  // Frontespizio
  align(center)[
    #v(if copertina == none { 3.2cm } else { 1.4cm })
    #text(font: TITOLI, size: 11pt, fill: seppia, tracking: 3pt)[#brand]
    #v(0.6cm)
    #line(length: 45%, stroke: 0.6pt + seppia)
    #v(0.5cm)
    #text(font: TITOLI, size: 27pt, weight: 600, fill: rosso)[#titolo]
    #v(0.25cm)
    #text(size: 11.5pt, style: "italic", fill: seppia)[#sottotitolo]
    #v(0.5cm)
    #line(length: 45%, stroke: 0.6pt + seppia)
    #if copertina != none [
      #v(0.7cm)
      #block(clip: true, radius: 2pt, stroke: 0.7pt + seppia,
        image(copertina, width: 11cm, alt: titolo))
    ]
    #v(0.8cm)
    #text(font: TITOLI, size: 8.5pt, fill: seppia, tracking: 1.5pt)[#banner]
    #if meta != "" [
      #v(0.35cm)
      #text(size: 8.5pt, style: "italic", fill: seppia)[#meta]
    ]
    #v(1.2cm)
    #text(fill: seppia, size: 15pt)[❦]
  ]
  pagebreak()

  // La pagina d'introduzione del manifest (`intro_md`): la catena HTML la
  // stampa da sempre, questa la ignorava in silenzio.
  if intro != none {
    intro
    pagebreak()
  }

  // Indice cliccabile (e segnalibri PDF dagli heading)
  align(center)[#text(font: TITOLI, size: 13pt, fill: rosso)[Indice]]
  v(0.4cm)
  outline(title: none, depth: 3, indent: 1em)
  pagebreak()

  set page(columns: 2)
  corpo
}
