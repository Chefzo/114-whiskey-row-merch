# One Fourteen Merch

Production artwork repo for the first One Fourteen / Whiskey Row merch drop.

## Hero concept

The current lead product is a single hero tee:

- **Garment:** Comfort Colors 1717, Pepper or Black
- **Front:** small neon-inspired `114` chest hit
- **Back:** cream one-color vault badge
- **Print method:** DTG first, screen-printable later
- **Positioning:** downtown Louisville nightlife, not tourist bourbon merch

## Recommended product setup

| Product | Artwork | Notes |
|---|---|---|
| Comfort Colors 1717 tee | `artwork/front/one_fourteen_front_neon.png` + `artwork/back/one_fourteen_back_badge_cream.png` | Lead product |
| Comfort Colors 1717 tee, one-color version | `artwork/front/one_fourteen_front_chest_cream.png` + `artwork/back/one_fourteen_back_badge_cream.png` | Lower-cost fallback |
| Light garment alternate | `artwork/back/one_fourteen_back_badge_black.png` | Use only if producing cream/white garments |

## File map

```text
artwork/
  front/      Front chest artwork PNGs
  back/       Back badge artwork PNGs
  source/     Editable SVG source
previews/     Proof sheets and placement mockups
docs/         Design rationale and production notes
scripts/      Reproducible artwork build scripts
printify/     Printify draft product metadata
```

## Do not use

- Old placeholder typography drafts
- V2/V3 automated badge experiments
- Checkerboard/reference-image exports
- Any image with fake production labels, warped arc text, or registration marks

## Current recommendation

Use the neon chest hit with the cream vault badge back. Publish only after checking Printify mockups at actual garment scale.
