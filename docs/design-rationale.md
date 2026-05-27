# One Fourteen / Whiskey Row — Hero Tee Design Rationale

## Concept

A single hero tee, not a SKU sprawl. Built around two ideas the bar already
owns: the **neon "114"** that lives in the room, and the bourbon-room
**vault / lock** vocabulary suggested by the keyhole reference. The previous
attempt failed because it took those vocabulary cues literally — wood-grain
swirls, broken arc text, fake registration marks, "BACK DESIGN" labels and
all the AI sludge — instead of distilling them into intentional vector art.

This version is built **in code, not generated**: every shape is placed,
every glyph is anchored, every curve is a calculated arc. Nothing
hallucinates.

## Tee spec

- **Garment:** Comfort Colors 1717 in **Pepper** (warm near-black)
- **Front:** small chest hit, ~3.5" wide, centered, ~3" below collar
- **Back:** vault badge, ~11–12" wide, centered upper-back placement
- **Print method:** DTG. The cream-only variant converts cleanly to 1-color
  plastisol screens if you ever do a screen run.
- **Ink:**
  - **Cream** (PMS 7527-ish / "Bone") — main ink for both front and back
  - **Neon red** (~PMS 485 / 1788 mix) — only on the neon front variant

## Front — Chest Hit (two variants)

### Variant A: One-color cream
A clean serif **"114"** with an understated **ONE FOURTEEN · WHISKEY ROW**
strap line below, flanked by hairline rules. Reads at 6 feet. Cheap to
print, easy to reorder, and pairs perfectly with the back when the customer
turns around.

File: `one_fourteen_front_chest_cream.png` (1800px wide, transparent PNG)

### Variant B: Neon
The same numerals reinterpreted as a flat neon-tube: **cream-yellow inner
core, warm red tube outline, soft red halo**. This is a *merch* neon — flat
enough to print on DTG without the halo becoming a muddy blob the way a
photographic neon would. The strap line stays cream so it doesn't compete.

File: `one_fourteen_front_neon.png` (1800px wide, transparent PNG)

Pick one for the hero. **Recommendation: lead with Variant B (neon).** It
directly references the room's neon sign and gives the tee a piece of
nightlife identity that "just a 114" can't.

## Back — Vault Badge

A circular emblem built on the bar's vault / whiskey-room conceit, but
rebuilt as **intentional, restrained vector art**:

- **Double ring** — one heavy outer line, one hairline parallel inner
  line. That's the entire frame. No woodgrain, no rope, no rivets.
- **Top arch:** `ONE FOURTEEN` in heavy display serif, true arc-aligned.
- **Bottom arch:** `WHISKEY ROW`, same family, properly oriented so it
  reads left-to-right across the bottom (the previous attempt had this
  backwards).
- **Side ornaments:** two small diamond markers at 9 and 3 o'clock,
  acting as visual stops between the top and bottom wordmarks.
- **Star** above the numeral — small, classic Kentucky-y, not corny.
- **Central "114"** in the same heavy display serif, sized large enough
  to dominate. This is the badge's anchor.
- **Tagline strip:** `BOURBON · COCKTAILS · LATE NIGHTS` in condensed
  black sans, sandwiched between two hairline rules. Categorical, not
  cute.

What it deliberately omits:
- No woodgrain or wood-stave fill (the old badge's main failure)
- No keyholes baked into the artwork (they were illegible at any printable size)
- No "EST. 20XX" date (no canon supplied; making one up is amateur)
- No fake registration marks, no "back design - apparel asset" tags
- No bourbon-barrel clip art, no horseshoe, no Derby allusions —
  this is a downtown nightlife bar, not a tourist gift shop

File: `one_fourteen_back_badge_cream.png` (4500×4500 transparent PNG)
Alt: `one_fourteen_back_badge_black.png` (same art in black ink for light tees)
Source: `one_fourteen_back_badge.svg` (editable vector source)

## Typography

- **Display serif (numerals + arched wordmarks):** Noto Serif Display
  Black. A heavy, modern Didone-influenced display face — sharp contrast,
  refined serifs, holds its weight at large sizes without feeling
  decorative. For production substitute Bodoni 72, Playfair Display Black,
  or Domaine Display.
- **Condensed sans (tagline + strap line):** Noto Sans Display Extra
  Condensed Black. Dense, modern, doesn't compete with the serif. For
  production substitute Acumin Pro Condensed Black, Barlow Condensed Black,
  or DIN Condensed Bold.
- **Numerals: tabular** — the "114" numerals are oldstyle/lining mixed
  per the chosen font's natural design. They scan as a unit, not three
  separate digits.

## Deliverables (all in `/home/user/workspace/one_fourteen_merch_opus/`)

| File | Purpose | Format |
|---|---|---|
| `one_fourteen_front_chest_cream.png` | Front chest hit, 1-color cream | Transparent PNG, 1800px wide |
| `one_fourteen_front_neon.png` | Front chest hit, neon look | Transparent PNG, 1800px wide |
| `one_fourteen_back_badge_cream.png` | Back vault badge, cream ink | Transparent PNG, 4500×4500 |
| `one_fourteen_back_badge_black.png` | Back vault badge, black ink | Transparent PNG, 4500×4500 |
| `one_fourteen_back_badge.svg` | Editable vector source for back badge | SVG |
| `one_fourteen_mockup_contact_sheet.jpg` | 3-panel preview on dark | JPG, 2800×1800 |
| `one_fourteen_tee_back_mockup.jpg` | Back placement preview | JPG, 1800×2200 |
| `one_fourteen_tee_front_mockup.jpg` | Front placement preview | JPG, 1800×2200 |
| `build_back_badge.py` | Reproducible build script for badge | Python |
| `build_front_chest.py` | Build script for cream front | Python |
| `build_front_neon.py` | Build script for neon front | Python |
| `build_mockup.py` | Build script for mockup sheet | Python |

## What I did not do

- I did **not** touch Printify or publish anything.
- I did **not** invent an `EST.` year, founding date, address, phone number,
  or any unverifiable bar copy.
- I did **not** include a bourbon barrel, horseshoe, Derby silhouette,
  Louisville skyline, or any other generic tourist-bourbon clip art.
- I did **not** generate the back badge with an image model — it is built
  in code so every element is intentional and the SVG can be edited
  directly.

## Recommended next steps for the operator

1. Open the SVG in Illustrator or Inkscape if you want to tweak text
   (e.g., swap "BOURBON · COCKTAILS · LATE NIGHTS" for a different
   tagline). The arcs and rings will hold automatically.
2. Print a single physical proof of the back badge on a Pepper Comfort
   Colors blank before committing to a run. Cream ink on Pepper is the
   make-or-break call here — verify the cream looks bone, not yellow,
   under the bar's actual light.
3. For the front, pick **one** variant and commit. Running both
   simultaneously fragments the brand.
