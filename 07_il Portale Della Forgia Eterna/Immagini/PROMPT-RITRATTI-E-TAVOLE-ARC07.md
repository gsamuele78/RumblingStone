# Immagini della serata e del −1000 — prompt eseguibili

**Cos'è.** I ritratti e le tavole che mancano alla serata della resurrezione e al
volume del viaggio a mille anni fa, scritti **nello stesso formato e nello stesso
stile del Drappo di Tarsilia**
(`STANDALONE-Il-Drappo-di-Tarsilia/ALLEGATI/immagini/PROMPT-RITRATTI-E-TAVOLE.md`),
su richiesta del DM del 2026-09-24: le immagini devono sembrare della stessa mano.

Si generano con la stessa pipeline:

```
python3 scripts/comfyui_batch.py --prompts "07_il Portale Della Forgia Eterna/Immagini/PROMPT-RITRATTI-E-TAVOLE-ARC07.md" --lista
python3 scripts/comfyui_batch.py --prompts "07_il Portale Della Forgia Eterna/Immagini/PROMPT-RITRATTI-E-TAVOLE-ARC07.md" --serie tutto
```

I PNG escono accanto a questo file. Le schede-scena con il contesto narrativo
(fonte, destinatario, spoiler) restano in `PROMPT-IMMAGINI-07ILP.md`: **il testo
da dare al modello sta qui**, e c'è una copia sola.

> ⚖️ **Regola IP del repo**: si descrivono le convenzioni del look, mai il nome
> di un illustratore vivente, mai «in the style of». L'ancora è una scuola
> pittorica in pubblico dominio.

---

## §1 · Il look comune

**Identico al Drappo, tranne la tavolozza.** Le prime cinque righe (tecnica,
inquadratura, luce, materiali) sono le stesse parola per parola. L'ultima riga
del Drappo diceva *«muted river-town palette (wet ochre, iron grey, dyed
indigo), late-summer light»*: è la tavolozza di una città di fiume, e qui siamo
in una fortezza nanica e nella sua forgia. Cambia solo quella.

<!-- blocco id=look-comune -->
```
painterly digital illustration, crisp ink line underneath, visible brushwork,
three-quarter view, waist-up character sheet portrait, single hero focal point,
simple dark vignette background, warm-cool contrast, dramatic rim lighting,
weathered leather and cloth, muted mountain-hold palette (slate grey, forge
gold, moss green), torch and forge light
```

**L'ancora storica**, identica al Drappo:

<!-- blocco id=ancora-storica -->
```
northern renaissance oil glazing, flemish panel painting light,
egg-tempera restraint in the flesh tones
```

**Negativi**, identici al Drappo:

<!-- blocco id=negativi -->
```
modern clothing, plastic sheen, glamour, neon, text, watermark, logo,
oversaturated
```

**Formati**: ritratti **832 × 1216** (verticali, come le schede del Drappo),
tavole **1536 × 864**. I tratti del volto che i master non dicono sono
`[PROPOSTA]` e stanno nelle schede-personaggio di `PROMPT-IMMAGINI-07ILP.md`: si
cambiano lì e qui prima di generare, non dopo.

---

## §2 · I sette ritratti del cast di mille anni fa

I file vanno poi copiati in `Immagini/ritratti/` col nome dell'`id` senza il
prefisso `ritratto-` (es. `ritratto-balvar-fuocospento.png` →
`ritratti/balvar-fuocospento.jpg`), e nella scheda del cast la riga «Ritratto
da generare» diventa l'immagine.

**Balvar Fuocospento — il runaio esiliato** *(si genera per primo: è il volto che conta di più)*
<!-- img id=ritratto-balvar-fuocospento size=832x1216 stile=ritratto serie=base -->
```
[look comune] + old shield dwarf seated on a workshop stool at the back of a
war tent of black hide, white beard dusted grey with slate powder, calm
unhurried eyes, leather workshop apron, a slab of slate on his knees and an
iron stylus in his right hand, engraving slowly, he has just looked up
```
*La cosa che non deve mancare*: la punta di ferro sull'ardesia. Non smette di incidere.

**Zog'tar Deatheye — il generale**
<!-- img id=ritratto-zogtar-deatheye size=832x1216 stile=ritratto serie=base -->
```
[look comune] + huge half-ogre warlord, short tusks, old scars, a smooth
polished black obsidian stone set into his right eye socket, blackened full
plate with rust-red cloth, two-handed greataxe resting on his shoulder,
counting on his fingers, dwarven bones hanging from the tent behind him
```
*La cosa che non deve mancare*: la pietra nera al posto dell'occhio destro.

**Re Thorek I — il re di una fortezza giovane**
<!-- img id=ritratto-re-thorek-i size=832x1216 stile=ritratto serie=base -->
```
[look comune] + ancient dwarf king, very long white beard in three braids,
heavy grey eyes, mithral armour, dark blue cloak, plain iron crown with no
gems, a great axe of pale blue-white steel with frost patterns along the
blade in his right hand, a war map on a stone table, freshly cut white walls
```
*La cosa che non deve mancare*: Frostcleaver in pugno, anche al tavolo.

**Thorgrim Barbadiferro — l'antenato**
<!-- img id=ritratto-thorgrim-barbadiferro size=832x1216 stile=ritratto serie=base -->
```
[look comune] + old dwarf warrior seated on a stone bench, iron-grey beard,
eyes wet without him noticing, large hands resting on his knees with the
callus of an axe grip visible on the right palm, a single-bladed dwarven war
axe with a haft worn smooth leaning beside him, looking up at a relic
```
*La cosa che non deve mancare*: il callo sul palmo. È lo stesso di Thorik.

**Durin Rocciadura — la pattuglia**
<!-- img id=ritratto-durin-rocciadura size=832x1216 stile=ritratto serie=base -->
```
[look comune] + dwarf veteran guard at night in a pine forest, short brown
beard tied in one knot, a nose broken once, eyes that keep moving, dented
full plate, round shield painted dark blue on his back, a double-headed axe
held too tightly in both hands, torches of six other dwarves blurred behind
```
*La cosa che non deve mancare*: le mani strette sull'ascia. Ha paura.

**Mastro Costruttore Zeth — il seme del Ghostlord**
<!-- img id=ritratto-zeth-mastro-costruttore size=832x1216 stile=ritratto serie=base -->
```
[look comune] + thin half-elf master builder in a narrow torchlit mining
tunnel, high cheekbones, feverish bright eyes, a few days of stubble, rock
dust up to the elbows on an ochre work tunic, drawing runes on the wall with
chalk, one rune half erased by his thumb, a stone lion faintly carved behind
```
*La cosa che non deve mancare*: la speranza sul viso. È quella che mette a disagio.

**Vatore — il ladro che diventerà Sal**
<!-- img id=ritratto-vatore size=832x1216 stile=ritratto serie=base -->
```
[look comune] + lean man in his forties between two dark tents of a vast night
camp, grey silk clothes of a close dark-elven cut, hood half raised, no
ornaments, cold calculating eyes, clutching a cloth bundle to his chest,
reverent terror badly hidden, looking at something that should not exist
```
*La cosa che non deve mancare*: il fagotto stretto al petto.

---

## §3 · Le sei tavole

Le tavole prendono **solo l'ancora storica** (il look comune dice «waist-up
portrait» e rovinerebbe una veduta), come nel Drappo.

**Il portale del Tempo** *(scheda 22; sostituisce `PortaleDellaForgiaEterna.webp`, che è un'immagine di testo)*
<!-- img id=tavola-portale-del-tempo size=1536x864 stile=tavola serie=base -->
```
epic fantasy matte-painting, a fresco as tall as three men in a frame of gold
and adamantine on the wall of a dark octagonal hall, its liquid-glass surface
showing two scenes at once like a double exposure: a young white-walled
dwarven fortress with a young black dragon diving on it, and the same
fortress centuries older and soot-black under a much larger black dragon, a
vertical oval of gold light pulsing where they overlap, a dwarf seen from
behind wearing a crown with two lit gems and one empty socket, no text
```

**La Custode delle Radici** *(scheda 28 · solo DM fino allo Step 5)*
<!-- img id=tavola-custode-delle-radici size=832x1216 stile=tavola serie=base -->
```
a tall figure shaped like a woman but made of braided dark roots and
lichen-grey rock, two old knots of wood for eyes, standing perfectly still at
the empty southern edge of a glowing ritual circle in a basalt and gold hall,
the gold light thinning around her feet, three small kneeling figures out of
focus, solemn and neutral, a patient official waiting for a signature, no text
```

**Il Cuore di Moradin, il reliquiario che si apre** *(scheda 27 · `serie=extra`: l'immagine esistente `ilCuoreDiMoradin` lo mostra già appoggiato sull'Altare; questa è la versione fedele al testo di `DEF-3` §3)*
<!-- img id=tavola-cuore-di-moradin size=1536x864 stile=tavola serie=extra -->
```
a seamless altar of mithral at the centre of a dark octagonal hall opening
like a metal flower, its petals folding back to reveal a small inner chamber,
and suspended in golden light inside it a crystal of blood-red ruby the size
of a fist carved in the exact shape of a dwarven heart, four chambers and
its vessels visible through the transparent stone, a dwarf's gauntleted hands
resting on the altar's rim, warmth rising from it, no text
```

**Il risveglio di Hella** *(scheda 29 · ai giocatori solo dopo il rito)*
<!-- img id=tavola-risveglio-di-hella size=1536x864 stile=tavola serie=base -->
```
a dwarf woman lying on a mithral altar at the instant she breathes in again
after death, chest lifting, eyes just opened and amber-gold, light wavy
blonde hair with small green leaves and a thin vein of bark, pointed ears
like young leaves, a fist-sized ruby shaped like a heart fading on her
breastbone, thin golden roots running from her hands into the altar, three
armoured figures kneeling at the edge of a ritual circle, a large dog of dark
stone and mithral with topaz eyes waiting at the altar's edge, warm gold
light from below, no text
```

**Durik e Hella** *(scheda 31 · dopo il risveglio)*
<!-- img id=tavola-durik-e-hella size=832x1216 stile=tavola serie=base -->
```
a large sighthound made of dark porous stone braided with ribbons of mithral
along the tendons, topaz eyes half closed, resting his heavy head on the
chest of a dwarf woman just returned from death, sitting up on an altar, one
trembling hand between his ears, her light blonde hair with small leaves,
pointed ears like young leaves, no collar, no mechanical joints, tender and
quiet, warm light from below left, no text
```

**La fortezza giovane** *(scheda 33 · all'arrivo a −1000)*
<!-- img id=tavola-hammerfist-giovane size=1536x864 stile=tavola serie=base -->
```
epic fantasy matte-painting, a young dwarven fortress carved into a
mountainside at dusk seen from its own gate, walls of freshly cut white
limestone with sharp unweathered edges, a single king's statue in the
courtyard, stonemasons' scaffolding against one tower, a freshly engraved
bronze plaque on the gate with bronze shavings beneath it, far off the smoke
of a thousand campfires on the plain, low warm sunset, no text
```

**Skullcrusher nel cortile** *(scheda 41 · solo DM fino al duello)*
<!-- img id=tavola-skullcrusher-nel-cortile size=1536x864 stile=tavola serie=base -->
```
a huge lean black dragon landing in the stone courtyard of a young dwarven
fortress at dawn, long neck, narrow horned skull, wings half open from the
dive, matte black scales with an oily green sheen, acid dripping from closed
jaws and smoking on the flagstones, hundreds of dwarves on the walls looking
up, four small figures seen from behind facing him: a dwarf with a crown and a
great axe, a bare-handed dwarf monk with glowing braziers on his wrists, a
caster wreathed in light and shadow, a blonde dwarf woman with a stone hound,
cold grey dawn light, low camera, no text
```
