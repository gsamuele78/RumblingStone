# Converting Between D&D 3.5 and Pathfinder 1e

Source: Paizo's official *Pathfinder RPG Conversion Guide* (free PDF,
paizo.com) summarizes 3.5→PF1e; this file covers both directions for the
needs of a 3.5 campaign that borrows PF1e material.

**Rule of thumb: don't convert — import.** The systems share the d20 OGL
skeleton; printed numbers work as-is at the table 90% of the time. Convert
only the subsystems listed below, and only when they actually come up.

---

## PF1e monster → 3.5 table (checklist)

1. **hp, AC, attacks, damage, saves, DCs, SR, DR, speeds**: keep as printed.
2. **CMB/CMD**: replace with 3.5 grapple = BAB + Str mod + special size mod
   (Large +4, Huge +8, Gargantuan +12, Colossal +16). For trip/bull rush use
   the 3.5 opposed-check rules with the creature's Str/Dex.
3. **Perception** → Spot AND Listen at the same bonus (also Search at
   Int-based approximation). **Stealth** → Hide AND Move Silently.
   **Acrobatics** → Balance/Jump/Tumble.
4. **PF-only feats**: map to nearest 3.5 feat or drop; common maps:
   - Improved Natural Armor / Toughness (PF) → Toughness ×n or Improved
     Toughness `[Non-SRD: Complete Warrior]`
   - Combat Reflexes, Power Attack, Cleave, Vital Strike: Power Attack and
     Cleave exist in 3.5 (use 3.5 wording); Vital Strike has no 3.5 twin —
     drop it or treat as a flavor rider on a single attack.
5. **Channel energy** → 3.5 turn/rebuke undead at cleric level, or keep as a
   house-ruled 30-ft burst (declare which in the encounter file).
6. **Polymorph-line spells** → use the 3.5 spell text.
7. **CR**: keep the printed PF1e CR. PF1e monsters of the same CR are
   slightly tougher than 3.5 ones on average; that is acceptable drift for a
   party that outguns printed 3.5 content (this one does — 4 PCs at level 13
   with artifacts).
8. Add a `Conversion notes:` line to the stat block listing what changed.

## 3.5 monster → PF1e (rarely needed here)

1. Keep everything printed.
2. CMB = BAB + Str + PF size mod; CMD = 10 + BAB + Str + Dex + PF size mod.
3. Merge Spot/Listen → Perception (take the better), Hide/MS → Stealth.
4. Consider +2 hp/HD or the Advanced template — 3.5 monsters run soft by
   PF1e benchmarks.

## XP, wealth, and progression — never mix

- Award XP from the **3.5 DMG table only** (`dnd-35-srd`), regardless of the
  monster's origin. A CR 13 kill is a CR 13 kill.
- Audit treasure against **3.5 WBL** (campaign standard; see arc treasure
  audits under `campaign/`).
- PF1e fast/medium/slow XP tracks, PF WBL, and PF item pricing are OFF —
  they exist in this repo only for reading PF1e sources correctly.

## Spell compatibility

~95% of spell names and effects match. Known traps:

| Spell | Difference |
|---|---|
| *Polymorph* family | Completely rewritten in PF1e — always use 3.5 text |
| *Grease, Glitterdust, Black Tentacles* | PF1e nerfed via CMB/save tweaks — use 3.5 text |
| *Save-or-die* (finger of death, etc.) | PF1e converts to damage — use 3.5 text |
| *Cure X Wounds* | identical — either |
| Core blasting/buffs (fireball, haste, stoneskin…) | identical enough — either |

When a villain is built with PF1e class features but casts spells, cast from
the 3.5 spell text with the PF1e DCs. That combination is stable and fast.

---

## PF1e spells for `--piu-cattivi` — what actually gets you more, and what doesn't

Requested by the DM: *when generating the harsher variant at the same CR, use
PF1e spells where they are stronger.* The mechanism exists
(`genera_creatura.py --piu-cattivi`, or `--incantesimi pf1e`), but the premise
does not survive contact with the table above, and the option is scoped to match
reality rather than the wish.

**On the shared core spells PF1e is not stronger — it is equal or weaker.** The
compatibility table in this same file says so: *grease*, *glitterdust* and
*black tentacles* were nerfed through CMB and save changes; the save-or-die line
(*finger of death* and relatives) was converted into damage; the polymorph line
was rewritten and this repo's standing rule is to cast it from the 3.5 text.
Swapping *fireball* for "PF1e *fireball*" buys nothing: it is the same spell.

Three things do make a PF1e-flavoured caster harder at the same CR, and only the
first is about spells at all:

1. **Spells that exist only in PF1e**, with no 3.5 twin — the list below.
2. **The Advanced template's +4 to mental scores**, which raises every save DC
   by 2. `--piu-cattivi` already applies this; it is the largest single effect.
3. **PF1e summon lists**, which offer better creatures per spell level.

### PF1e-only spells with no 3.5 equivalent

Names are given as the PRD prints them, with a working Italian gloss, because a
DM who wants one of these has to read the PF1e text — there is no 3.5 paragraph
to fall back on. Source: PF1e PRD, Core Rulebook and Advanced Player's Guide
(OGL), class and level checked against [d20pfsrd](https://www.d20pfsrd.com/magic/all-spells/).

The check was worth doing: **it caught two spells on the wrong list**, which is
the same defect class the 3.5 lists exist to prevent.

- *ill omen* was on the sorcerer/wizard list at 1st. It is a **witch**, psychic
  and mesmerist spell — not arcane-prepared at all. Removed.
- *stone call* was at 3rd for sorcerer/wizard. It is **sorcerer/wizard 2**
  (druid 2, ranger 2). Moved.

| Level | PRD name | Gloss | Lists (checked) | Why it is worth importing |
|---|---|---|---|---|
| 1 | *saving finale* | finale salvifico | bard 1 | immediate-action reroll of a failed save for an ally |
| 2 | *create pit* | fossa | sorc/wiz 2 | the pit line has no 3.5 twin; removes a PC from the fight on a failed Reflex |
| 2 | *stone call* | pioggia di pietre | druid 2, ranger 2, sorc/wiz 2 | 2d6 bludgeoning over the area plus difficult terrain, no save |
| 2 | *gallant inspiration* | ispirazione galante | bard 2 | immediate-action +2d4 to a failed attack or check |
| 3 | *spiked pit* | fossa irta | sorc/wiz 3 | the pit, with spikes on the bottom and the walls |
| 3 | *aqueous orb* | sfera d'acqua | druid 3, sorc/wiz 3, magus 3 | rolling engulf; control plus forced movement |
| 3 | *instant enemy* | nemico istantaneo | ranger 3 ⚠️ **level not confirmed** | makes any target the ranger's favoured enemy for the fight |
| 4 | *ball lightning* | fulmini globulari | druid 4, sorc/wiz 4, shaman 4 | two moving damage globes from one slot |
| 4 | *acid pit* | fossa acida | sorc/wiz 4 | the pit, plus 2d6 acid per round in the pool at the bottom |
| 4 | *blessing of fervor* | benedizione del fervore | cleric/oracle 4 | the strongest single party buff PF1e added; a real threat multiplier on a villain's side |
| 5 | *hungry pit* | fossa vorace | sorc/wiz 5 | the pit that squeezes and crushes what falls in |
| 6 | *sirocco* | scirocco | druid 6, sorc/wiz 6, magus 6 | 4d6+1/level fire, prone, and fatigued in one burst |
| 8 | *stormbolts* | saette | cleric 8, druid 8, sorc/wiz 8, witch 8 | 1d8/level electricity (max 20d8) to every target in range |
| 9 | *clashing rocks* | rocce cozzanti | druid 9, sorc/wiz 9 | the highest single-target damage PF1e added |

⚠️ One row is still unchecked — *instant enemy*'s printed level. The generator
keeps it and says so; a block that contains it is a proposal to verify.

⚠️ **Why the check was done by search and not from the PRD itself.** This
environment's network policy does not allow `pathfinder.d20srd.org` or
`legacy.aonprd.com`, so the rows could not be read from the source document.
Allowing those two domains in the environment's network settings would let a
later pass import the PF1e class spell lists properly — the way
`dnd-35-srd/references/spells.md` holds the 3.5 ones — and turn this table from
a hand-checked shortlist into a real anchor.

### What the generator refuses to do

It will not "upgrade" a spell that this file already flags as *nerfed in PF1e*
(*grease*, *glitterdust*, *black tentacles*, the save-or-die line, the polymorph
line). Presenting a weaker spell as the harsher variant would be the worst kind
of wrong: invisible at generation time, and discovered at the table.
