# Next direction — *Music Sounds Better With You* divey tee

This document captures the new lead concept for One Fourteen merch and
how it sits alongside the original neon / vault-badge tee.

## TL;DR

The new lead product is a single hero tee built around the headline
**MUSIC SOUNDS BETTER WITH YOU**, rendered in the divey / vintage vibe
defined in [`../BRAND.md`](../BRAND.md).

- Front lockup: [`../designs/one-fourteen-tee/front-chest-divey.png`](../designs/one-fourteen-tee/front-chest-divey.png)
- Back hero:    [`../designs/one-fourteen-tee/back-divey.png`](../designs/one-fourteen-tee/back-divey.png)

A companion tank drop reuses the same headline in five vibes
(`01-divey`, `02-editorial`, `03-disco`, `04-tour-tee`, `05-punk-zine`)
under [`../designs/music-sounds-better-with-you/`](../designs/music-sounds-better-with-you/).
The divey vibe is the lead; the others are kept on file as alternates.

## Why this is the new lead

The original drop (neon `114` chest hit + cream vault badge back) is
**not** being retired — it's preserved under [`../artwork/`](../artwork/)
and its Printify draft is untouched. But the divey music-tee concept
better matches the One Fourteen voice described in
[`../BRAND.md`](../BRAND.md): dark, direct, late-night, editorial,
intentionally divey rather than neon-modern. It also opens a clearer
follow-on (the five-vibe tank drop) and a clearer fit with the
Bella+Canvas / Comfort Colors black blanks used for DTG.

## What ships with this direction

| Path | What it is |
|---|---|
| [`../designs/one-fourteen-tee/front-chest-divey.png`](../designs/one-fourteen-tee/front-chest-divey.png) | Print-ready front PNG, 4500×5400 @ 300 DPI, pre-positioned for left-chest placement on a Bella 3001 / Comfort Colors 1717 front print zone. |
| [`../designs/one-fourteen-tee/back-divey.png`](../designs/one-fourteen-tee/back-divey.png) | Print-ready back PNG, 4500×5400 @ 300 DPI, large divey hero centered ~3" below the collar. |
| [`../designs/music-sounds-better-with-you/01-divey.png`](../designs/music-sounds-better-with-you/01-divey.png) | Lead tank vibe (Bella+Canvas 8800), 3210×3927. |
| [`../designs/music-sounds-better-with-you/02-editorial.png`](../designs/music-sounds-better-with-you/02-editorial.png) | Alternate tank vibe — Void System pure. |
| [`../designs/music-sounds-better-with-you/03-disco.png`](../designs/music-sounds-better-with-you/03-disco.png) | Alternate tank vibe — Allura script, deep red. |
| [`../designs/music-sounds-better-with-you/04-tour-tee.png`](../designs/music-sounds-better-with-you/04-tour-tee.png) | Alternate tank vibe — Anton tour-tee layout. |
| [`../designs/music-sounds-better-with-you/05-punk-zine.png`](../designs/music-sounds-better-with-you/05-punk-zine.png) | Alternate tank vibe — punk-zine ransom-note + Xerox noise. |
| [`../scripts/build_one_fourteen_tee.py`](../scripts/build_one_fourteen_tee.py) | Regenerates the tee front + back. |
| [`../scripts/build_music_sounds_better.py`](../scripts/build_music_sounds_better.py) | Regenerates all five tank vibes. |
| [`../scripts/lib.py`](../scripts/lib.py) | Shared rendering helpers used by both build scripts. |
| [`../fonts/`](../fonts/) | All fonts used by the new scripts. SIL OFL / Apache 2.0; full license table in [`../fonts/README.md`](../fonts/README.md). |
| [`../BRAND.md`](../BRAND.md) | Void System spec — colors, typography, voice, when to break the system. |
| [`../PRINTIFY.md`](../PRINTIFY.md) | Canvas sizes per blank, recommended providers, DTG pitfalls, sample-order log. |

## How this relates to the legacy hero tee

The original neon / vault-badge tee lives under [`../artwork/`](../artwork/)
and is unchanged. Its build scripts (`build_front_neon.py`,
`build_front_chest.py`, `build_back_badge.py`, `build_mockup.py`),
Printify draft metadata in [`../printify/`](../printify/), and the
mockup previews in [`../previews/`](../previews/) are all preserved.

If you ever want to revert to that direction, nothing has been deleted
or rewritten — just point Printify back at those PNGs.

## Printify — do this before pushing the new art

The manual GitHub Actions workflow in
[`../.github/workflows/update-printify-tee.yml`](../.github/workflows/update-printify-tee.yml)
and the script in
[`../scripts/update_printify_tee.py`](../scripts/update_printify_tee.py)
still default to the legacy neon/vault PNGs and the legacy product
title. Before running the workflow against this new direction, override
the inputs (or update the defaults) so it points at:

- `front_image`: `designs/one-fourteen-tee/front-chest-divey.png`
- `back_image`:  `designs/one-fourteen-tee/back-divey.png`
- `title`:       something like `One Fourteen Music Sounds Better With You Tee`
- `description`: rewrite to match the divey concept (see [`../PRINTIFY.md`](../PRINTIFY.md))

A `dry_run: true` rehearsal is strongly recommended before the first
real write. See [`./printify-automation.md`](./printify-automation.md)
for the full safety model — none of that changes.

## Sample-order discipline

DTG on black cotton renders cream lighter than the digital file. Order
one sample of the divey tee (front + back) before listing. The full
DTG pitfalls list is in [`../PRINTIFY.md`](../PRINTIFY.md); the
sample-order log lives in the same file.
