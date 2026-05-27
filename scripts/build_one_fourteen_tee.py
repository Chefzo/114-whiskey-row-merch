"""
One Fourteen Tee — Music Sounds Better With You drop.

Generates:
    - front-chest-divey.png  (small left-chest lockup, upper-right position)
    - back-divey.png         (large back hero print, upper-center position)

Both files are 4500 x 5400 px (Bella+Canvas 3001 unisex tee print area).
Designed to be uploaded directly to Printify front/back zones.

Run from scripts/:
    python build_one_fourteen_tee.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

from lib import (
    new_canvas, render_text, fit_font_size, paste_centered,
    apply_wear, save_design, font_path,
    AGED_CREAM,
)

# Bella 3001 / Comfort Colors 1717 unisex tee print area
TEE_W, TEE_H = 4500, 5400

# Output
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "designs", "one-fourteen-tee"))


# ---------------------------------------------------------------------------
# FRONT CHEST — small divey lockup, upper-right (= wearer's left chest)
# ---------------------------------------------------------------------------
def build_front_chest_divey():
    """Small typewriter lockup positioned at left-chest (~3.5 inches wide)."""
    canvas = new_canvas(TEE_W, TEE_H)

    # Build the lockup on a tight temp canvas first
    name_font = ImageFont.truetype(font_path("SpecialElite-Regular.ttf"), 120)
    addr_font = ImageFont.truetype(font_path("SpecialElite-Regular.ttf"), 55)

    # Render each piece with subtle wear
    name_img = apply_wear(
        render_text("ONE  FOURTEEN", name_font, AGED_CREAM),
        seed=101
    )
    addr_img = apply_wear(
        render_text("WHISKEY ROW  \u00b7  LOUISVILLE  KY", addr_font, AGED_CREAM),
        seed=102
    )

    # Match the divider width to the address line (looks like a typewriter rule)
    divider_w = addr_img.width
    divider_h = 3

    # Compose lockup on tight canvas
    lockup_w = max(name_img.width, addr_img.width) + 60
    lockup_h = name_img.height + 30 + divider_h + 35 + addr_img.height + 40
    lockup = Image.new("RGBA", (lockup_w, lockup_h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lockup)

    # Center each line within the lockup
    cy = 0
    name_x = (lockup_w - name_img.width) // 2
    lockup.paste(name_img, (name_x, cy), name_img)
    cy += name_img.height + 30

    # Divider rule
    div_x = (lockup_w - divider_w) // 2
    ld.rectangle([div_x, cy, div_x + divider_w, cy + divider_h], fill=AGED_CREAM)
    cy += divider_h + 35

    # Address
    addr_x = (lockup_w - addr_img.width) // 2
    lockup.paste(addr_img, (addr_x, cy), addr_img)

    # Trim lockup to actual content
    bbox = lockup.getbbox()
    lockup = lockup.crop(bbox)

    # Position the lockup at upper-right (wearer's left chest)
    # Target: ~3.5" wide, ~3" down from top of print zone, ~4" right of center
    # In 300 DPI pixels: ~1050 wide, ~900 down, ~1200 right of center
    pos_x = TEE_W // 2 + 350   # offset right of center
    pos_y = 850                 # down from top of print zone
    canvas.paste(lockup, (pos_x, pos_y), lockup)

    return save_design(canvas, os.path.join(OUT_DIR, "front-chest-divey.png"))


# ---------------------------------------------------------------------------
# BACK — divey hero, scaled UP for tee back, positioned 3-4" below collar
# ---------------------------------------------------------------------------
def build_back_divey():
    """Big back hero print — 11-12 inches wide, sits in upper portion of canvas."""
    canvas = new_canvas(TEE_W, TEE_H)

    # Hero sized for a tee back — target ~12" wide (3600 px) for SOUNDS BETTER
    hero_size = fit_font_size("SOUNDS BETTER", "AlfaSlabOne-Regular.ttf", 3600, 550)
    font_hero = ImageFont.truetype(font_path("AlfaSlabOne-Regular.ttf"), hero_size)
    font_sub = ImageFont.truetype(font_path("SpecialElite-Regular.ttf"), 155)
    font_addr = ImageFont.truetype(font_path("SpecialElite-Regular.ttf"), 110)

    # Hero lines with independent wear patterns
    lines = [
        apply_wear(render_text("MUSIC", font_hero, AGED_CREAM), seed=11),
        apply_wear(render_text("SOUNDS BETTER", font_hero, AGED_CREAM), seed=22),
        apply_wear(render_text("WITH YOU", font_hero, AGED_CREAM), seed=33),
    ]

    # Position: top of design at ~3 inches below top of canvas
    # (= ~3 inches below collar seam on the actual shirt — standard back-print placement)
    y = 900
    for line in lines:
        y = paste_centered(canvas, line, y) + 60
    y += 60

    # Stars divider
    stars = apply_wear(render_text("*   *   *", font_sub, AGED_CREAM), seed=44)
    y = paste_centered(canvas, stars, y) + 45

    # Attribution
    sub = apply_wear(
        render_text("ONE FOURTEEN  \u00b7  WHISKEY ROW", font_sub, AGED_CREAM),
        seed=55
    )
    y = paste_centered(canvas, sub, y) + 28

    # Address
    addr = apply_wear(
        render_text("114 W MAIN ST  \u00b7  LOUISVILLE  KY", font_addr, AGED_CREAM),
        seed=66
    )
    paste_centered(canvas, addr, y)

    return save_design(canvas, os.path.join(OUT_DIR, "back-divey.png"))


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Output directory: {OUT_DIR}\n")

    front = build_front_chest_divey()
    print(f"  built front-chest-divey  ->  {os.path.relpath(front, SCRIPT_DIR)}")

    back = build_back_divey()
    print(f"  built back-divey         ->  {os.path.relpath(back, SCRIPT_DIR)}")

    print(f"\nOne Fourteen tee — front + back ready for upload.")
