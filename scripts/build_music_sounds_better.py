"""
Build all 5 vibe variations of "MUSIC SOUNDS BETTER WITH YOU" tank.

Run from the scripts/ directory:
    python build_music_sounds_better.py

Outputs to ../designs/music-sounds-better-with-you/
"""

import os
from PIL import Image, ImageDraw, ImageFont

from lib import (
    new_canvas, render_text, fit_font_size, paste_centered,
    apply_wear, add_xerox_noise, save_design, font_path,
    CANVAS_W, CANVAS_H, CLEAN_CREAM, AGED_CREAM, BRASS, DEEP_RED,
)


# Output directory relative to scripts/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "designs", "music-sounds-better-with-you"))


# ---------------------------------------------------------------------------
# VIBE 1: DIVEY — slab serif + typewriter, aged cream, subtle wear
# ---------------------------------------------------------------------------
def build_divey():
    c = new_canvas()

    hero_size = fit_font_size("SOUNDS BETTER", "AlfaSlabOne-Regular.ttf", 2810, 340)
    font_hero = ImageFont.truetype(font_path("AlfaSlabOne-Regular.ttf"), hero_size)
    font_sub = ImageFont.truetype(font_path("SpecialElite-Regular.ttf"), 125)
    font_addr = ImageFont.truetype(font_path("SpecialElite-Regular.ttf"), 88)

    lines = [
        apply_wear(render_text("MUSIC", font_hero, AGED_CREAM), seed=11),
        apply_wear(render_text("SOUNDS BETTER", font_hero, AGED_CREAM), seed=22),
        apply_wear(render_text("WITH YOU", font_hero, AGED_CREAM), seed=33),
    ]
    y = 540
    for line in lines:
        y = paste_centered(c, line, y) + 35
    y += 35

    stars = apply_wear(render_text("*   *   *", font_sub, AGED_CREAM), seed=44)
    y = paste_centered(c, stars, y) + 35

    sub = apply_wear(render_text("ONE FOURTEEN  \u00b7  WHISKEY ROW", font_sub, AGED_CREAM), seed=55)
    y = paste_centered(c, sub, y) + 22

    addr = apply_wear(render_text("114 W MAIN ST  \u00b7  LOUISVILLE  KY", font_addr, AGED_CREAM), seed=66)
    paste_centered(c, addr, y)

    return save_design(c, os.path.join(OUT_DIR, "01-divey.png"))


# ---------------------------------------------------------------------------
# VIBE 2: EDITORIAL — Void System pure
# ---------------------------------------------------------------------------
def build_editorial():
    c = new_canvas()
    d = ImageDraw.Draw(c)

    hero_size = fit_font_size("SOUNDS BETTER", "BebasNeue-Regular.ttf", 2810, 500)
    font_hero = ImageFont.truetype(font_path("BebasNeue-Regular.ttf"), hero_size)
    font_sub = ImageFont.truetype(font_path("BarlowCondensed-Medium.ttf"), 110)
    font_addr = ImageFont.truetype(font_path("BarlowCondensed-Medium.ttf"), 90)

    y = 560
    for txt in ["MUSIC", "SOUNDS BETTER", "WITH YOU"]:
        line = render_text(txt, font_hero, CLEAN_CREAM)
        y = paste_centered(c, line, y) + 60
    y += 30

    cx = CANVAS_W // 2
    d.rectangle([cx - 600, y, cx + 600, y + 4], fill=CLEAN_CREAM)
    y += 50

    sub = render_text("ONE FOURTEEN  \u00b7  WHISKEY ROW", font_sub, BRASS)
    y = paste_centered(c, sub, y) + 18

    addr = render_text("114 W MAIN ST  \u00b7  LOUISVILLE  KY", font_addr, CLEAN_CREAM)
    paste_centered(c, addr, y)

    return save_design(c, os.path.join(OUT_DIR, "02-editorial.png"))


# ---------------------------------------------------------------------------
# VIBE 3: DISCO — Allura script, deep red, late-night romance
# ---------------------------------------------------------------------------
def build_disco():
    c = new_canvas()
    d = ImageDraw.Draw(c)

    script_size = fit_font_size("Music sounds better", "Allura-Regular.ttf", 2900, 600, min_size=200)
    font_script = ImageFont.truetype(font_path("Allura-Regular.ttf"), script_size)

    script_size_2 = fit_font_size("with you", "Allura-Regular.ttf", 2900, script_size, min_size=200)
    font_script_2 = ImageFont.truetype(font_path("Allura-Regular.ttf"), script_size_2)

    font_sub = ImageFont.truetype(font_path("BebasNeue-Regular.ttf"), 180)
    font_addr = ImageFont.truetype(font_path("BarlowCondensed-Medium.ttf"), 90)

    y = 700
    line1 = render_text("Music sounds better", font_script, DEEP_RED)
    y = paste_centered(c, line1, y) + 30

    line2 = render_text("with you", font_script_2, DEEP_RED)
    y = paste_centered(c, line2, y) + 80

    cx = CANVAS_W // 2
    d.rectangle([cx - 500, y, cx + 500, y + 3], fill=DEEP_RED)
    y += 50

    sub = render_text("ONE  FOURTEEN", font_sub, CLEAN_CREAM)
    y = paste_centered(c, sub, y) + 25

    addr = render_text("114 W MAIN ST  \u00b7  LOUISVILLE  KY", font_addr, CLEAN_CREAM)
    paste_centered(c, addr, y)

    return save_design(c, os.path.join(OUT_DIR, "03-disco.png"))


# ---------------------------------------------------------------------------
# VIBE 4: TOUR TEE — Anton bold + residency dates
# ---------------------------------------------------------------------------
def build_tour():
    c = new_canvas()
    d = ImageDraw.Draw(c)

    font_top = ImageFont.truetype(font_path("Anton-Regular.ttf"), 240)
    font_list = ImageFont.truetype(font_path("BebasNeue-Regular.ttf"), 130)
    font_small = ImageFont.truetype(font_path("BarlowCondensed-Medium.ttf"), 95)

    y = 460
    bar = render_text("ONE FOURTEEN", font_top, CLEAN_CREAM)
    y = paste_centered(c, bar, y) + 25

    tour_label = render_text("- 2026 RESIDENCY -", font_small, BRASS)
    y = paste_centered(c, tour_label, y) + 90

    hero_size = fit_font_size("SOUNDS BETTER", "Anton-Regular.ttf", 2810, 450)
    font_hero = ImageFont.truetype(font_path("Anton-Regular.ttf"), hero_size)
    for txt in ["MUSIC", "SOUNDS BETTER", "WITH YOU"]:
        line = render_text(txt, font_hero, CLEAN_CREAM)
        y = paste_centered(c, line, y) + 130
    y += 30

    cx = CANVAS_W // 2
    d.rectangle([cx - 1100, y, cx + 1100, y + 3], fill=CLEAN_CREAM)
    y += 35

    dates = [
        ("01.14.2026", "LOUISVILLE  KY  -  OPENING"),
        ("ONGOING", "WHISKEY ROW RESIDENCY"),
        ("FRI / SAT", "DJ NIGHTS  -  10 PM TIL LATE"),
        ("EVERY NIGHT", "WHISKEY  -  COCKTAILS  -  MUSIC"),
    ]
    for date, label in dates:
        date_img = render_text(date, font_list, BRASS)
        label_img = render_text(label, font_list, CLEAN_CREAM)
        date_x = cx - 1050
        label_x = cx - 350
        c.paste(date_img, (date_x, y), date_img)
        c.paste(label_img, (label_x, y), label_img)
        y += max(date_img.height, label_img.height) + 25

    y += 25
    d.rectangle([cx - 1100, y, cx + 1100, y + 3], fill=CLEAN_CREAM)
    y += 30

    addr = render_text("114 W MAIN ST  \u00b7  LOUISVILLE  KY", font_small, CLEAN_CREAM)
    paste_centered(c, addr, y)

    return save_design(c, os.path.join(OUT_DIR, "04-tour-tee.png"))


# ---------------------------------------------------------------------------
# VIBE 5: PUNK ZINE — mixed fonts, ransom-note tilts, Xerox noise
# ---------------------------------------------------------------------------
def build_punk():
    import numpy as np
    c = new_canvas()

    # Each word gets a different font for ransom-note feel
    word_specs = [
        ("MUSIC",   "BlackOpsOne-Regular.ttf",     450, -3),
        ("SOUNDS",  "SpecialElite-Regular.ttf",    420,  5),
        ("BETTER",  "PermanentMarker-Regular.ttf", 480, -4),
        ("WITH",    "AlfaSlabOne-Regular.ttf",     430,  6),
        ("YOU",     "Anton-Regular.ttf",           520, -2),
    ]

    def fit_word(text, font_file, max_size, target_w=2400):
        for s in range(max_size, 100, -20):
            f = ImageFont.truetype(font_path(font_file), s)
            tmp = Image.new("RGBA", (8000, 1200), (0, 0, 0, 0))
            d = ImageDraw.Draw(tmp)
            d.text((50, 50), text, font=f, fill=(255, 255, 255, 255))
            bb = tmp.getbbox()
            if bb and (bb[2] - bb[0]) <= target_w:
                return f
        return ImageFont.truetype(font_path(font_file), 100)

    y = 550
    np.random.seed(7)

    for word, fname, size, rotation in word_specs:
        font = fit_word(word, fname, size)
        img = render_text(word, font, CLEAN_CREAM)
        img = img.rotate(rotation, resample=Image.BICUBIC, expand=True)
        offset = np.random.randint(-80, 80)
        x = (CANVAS_W - img.width) // 2 + offset
        c.paste(img, (x, y), img)
        y += img.height + 25

    y += 60

    font_sub = ImageFont.truetype(font_path("SpecialElite-Regular.ttf"), 110)
    sub = render_text("ONE FOURTEEN //  WHISKEY ROW  //  LOUISVILLE", font_sub, CLEAN_CREAM)
    y = paste_centered(c, sub, y) + 12

    addr = render_text("114  W  MAIN  ST", font_sub, CLEAN_CREAM)
    paste_centered(c, addr, y)

    c = add_xerox_noise(c, intensity=0.012, seed=99)
    return save_design(c, os.path.join(OUT_DIR, "05-punk-zine.png"))


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    builders = [
        ("01 divey",     build_divey),
        ("02 editorial", build_editorial),
        ("03 disco",     build_disco),
        ("04 tour tee",  build_tour),
        ("05 punk zine", build_punk),
    ]

    print(f"Output directory: {OUT_DIR}\n")
    for name, fn in builders:
        path = fn()
        print(f"  built {name}  ->  {os.path.relpath(path, SCRIPT_DIR)}")

    print(f"\nAll 5 vibes generated.")
