# One Fourteen Merch

Production artwork repo for One Fourteen / Whiskey Row, Louisville KY.

> **Recommended next direction:** the *Music Sounds Better With You* /
> divey music tee in [`designs/`](designs/). See
> [`docs/next-direction.md`](docs/next-direction.md) and
> [`BRAND.md`](BRAND.md). The earlier neon / vault-badge tee under
> [`artwork/`](artwork/) is preserved for history but is no longer the
> lead concept.

## New lead — *Music Sounds Better With You* divey tee

- **Garment:** Bella+Canvas 3001 unisex tee (also fits Comfort Colors 1717), solid black
- **Front:** small typewriter left-chest lockup — [`designs/one-fourteen-tee/front-chest-divey.png`](designs/one-fourteen-tee/front-chest-divey.png)
- **Back:** large divey hero, "MUSIC / SOUNDS BETTER / WITH YOU" with attribution + address — [`designs/one-fourteen-tee/back-divey.png`](designs/one-fourteen-tee/back-divey.png)
- **Companion tank drop:** five vibe variations of the same headline in [`designs/music-sounds-better-with-you/`](designs/music-sounds-better-with-you/) — `01-divey` is the lead vibe; the other four (editorial / disco / tour / punk) are alternates kept for reference and future drops.
- **Print method:** DTG on garment-dyed black cotton, sample required before listing.
- **Positioning:** downtown Louisville nightlife, divey/editorial — not tourist bourbon merch.

Brand spec is in [`BRAND.md`](BRAND.md). Printify operations (canvas
sizes, blanks, providers, DTG pitfalls) are in [`PRINTIFY.md`](PRINTIFY.md).

### Regenerating the new artwork

```bash
pip install -r requirements.txt
cd scripts
python build_one_fourteen_tee.py        # front + back divey tee
python build_music_sounds_better.py     # all 5 tank vibes
```

Output drops into `designs/`. Fonts ship in [`fonts/`](fonts/) — all SIL
OFL or Apache 2.0 licensed for commercial use; license notes are in
[`fonts/README.md`](fonts/README.md).

## Legacy — neon chest + cream vault badge tee

The original hero tee from the first drop:

| Product | Artwork | Notes |
|---|---|---|
| Comfort Colors 1717 tee | `artwork/front/one_fourteen_front_neon.png` + `artwork/back/one_fourteen_back_badge_cream.png` | Original lead product |
| Comfort Colors 1717 tee, one-color version | `artwork/front/one_fourteen_front_chest_cream.png` + `artwork/back/one_fourteen_back_badge_cream.png` | Lower-cost fallback |
| Light garment alternate | `artwork/back/one_fourteen_back_badge_black.png` | Only for cream/white garments |

Build scripts: `scripts/build_front_neon.py`, `scripts/build_front_chest.py`,
`scripts/build_back_badge.py`, `scripts/build_mockup.py`. Design
rationale and production notes are in [`docs/`](docs/).

These assets and the Printify draft they back are **kept for history**.
Do not delete them, but treat the divey tee above as the current
direction unless explicitly reverting.

## File map

```text
designs/                              New direction — Music Sounds Better With You
  one-fourteen-tee/                     front-chest-divey.png + back-divey.png  ← lead
  music-sounds-better-with-you/         five tank vibes (01-divey is the lead)
fonts/                                Licensed font files used by build scripts
artwork/                              Legacy neon / vault badge tee artwork
  front/  back/  source/
previews/                             Legacy mockup proof sheets
docs/                                 Design rationale + production + Printify notes
scripts/                              All build + automation scripts (legacy + new)
printify/                             Printify draft product metadata (legacy)
BRAND.md                              Brand spec (Void System — colors, fonts, voice)
PRINTIFY.md                           Printify canvas specs, blanks, providers, DTG notes
```

## Printify workflow — read before running

The repo has a manual GitHub Actions workflow that pushes artwork into
an existing Printify tee draft. **It currently still points at the old
neon / vault badge files.** Before running it against the new direction,
update the workflow defaults and the script defaults to the divey
artwork. Details and the exact change list are in
[`docs/printify-automation.md`](docs/printify-automation.md). The
automation never publishes — publish is always a manual action inside
Printify after a human reviews the mockup.

## Do not use

- Old placeholder typography drafts
- V2/V3 automated badge experiments
- Checkerboard / reference-image exports
- Any image with fake production labels, warped arc text, or registration marks
