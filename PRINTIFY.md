# Printify Operations

Everything needed to take a design from `/designs` to a listable product.

## Print area specs

| Product | Canvas (px) | Inches | DPI |
|---|---|---|---|
| **Bella+Canvas 8800** (women's racerback tank) | 3210 × 3927 | 10.7" × 13.1" | 300 |
| Bella+Canvas 3001 (unisex tee) | 4500 × 5400 | 15" × 18" | 300 |
| Comfort Colors 1717 (heavyweight tee) | 4500 × 5400 | 15" × 18" | 300 |
| Independent SS4500 (hoodie) | 4500 × 5400 | 15" × 18" | 300 |
| Richardson 112 (cap embroidery) | 1500 × 1000 | 5" × 3.3" | 300 |

Always confirm in Printify's product editor — specs change.

## Blank recommendations

### Tank — Bella+Canvas 8800
- Variant: **Solid Black** only (not Black Heather, not Charcoal)
- Provider: Monster Digital or The Dream Junction (consistency on dark fabric)

### Tee — Comfort Colors 1717
- Variant: **Black** (pigment-dyed, slightly worn texture out of the bag — pairs well with divey designs)
- Provider: Underground Threads or MyLocker
- Note: Comfort Colors blanks have variation by design — embrace it for vintage drops

### Hoodie — Independent SS4500
- Variant: **Black**
- Provider: Drive Fashion or MyLocker
- Embroidery only — no DTG. Simplify the design to a left-chest mark + back hit.

### Cap — Richardson 112
- Variant: **Black / Black**
- Provider: MyLocker
- Embroidery only — `114` mark or short lockup, no detail under 0.25" stroke

## Upload checklist

- [ ] Design canvas matches the blank's print area spec exactly
- [ ] Design is pre-positioned for chest-high placement (upper ~15% of canvas)
- [ ] Confirmed `Solid Black` (or correct dark variant) selected
- [ ] DPI indicator shows green
- [ ] Provider confirmed (don't accept Printify's default — pick from this doc)

## Pricing tiers

| Product | Cost (approx) | Retail | Margin |
|---|---|---|---|
| Tank | $13–15 | **$34** | $19–21 |
| Tee | $13–16 | **$38** | $22–25 |
| Hoodie (embroidered) | $32–38 | **$78** | $40–46 |
| Cap (embroidered) | $11 | **$34** | $23 |

Round numbers, no 9s. `$34`, not `$33.99`.

## Sample order log

Order one sample of every new SKU before listing. Photograph in the bar for content.

| Date | Drop | SKU | Sample ordered? | Notes |
|---|---|---|---|---|
| | Music Sounds Better With You — tank | Bella 8800 / black | ☐ | Cream DTG on black — verify before bulk |

## Common DTG pitfalls

- **Cream prints lighter on cotton than on screen.** Files in this repo use `#E8E0D0` (Void) or `#E0D5BC` (aged) — both will look ~10% more muted on the actual shirt.
- **Brass `#B5953A` can read greenish on certain blanks.** Sample order is non-negotiable for any brass-accented design.
- **Deep red `#B91C1C`** holds well on cotton. Most reliable color in the system.
- **Avoid type under 14pt** for DTG — gets fuzzy. Embroidery worse — stay above 0.25" stroke.

## File naming convention

```
designs/<drop-slug>/<NN>-<vibe-slug>.png
```

Example: `designs/music-sounds-better-with-you/03-disco.png`

The 2-digit prefix locks ordering. Drop slug is kebab-case lowercase.
