"""
114 Whiskey Row Merch — shared rendering helpers.

All build scripts in this repo import from this module.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np


# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

# Printify print-area spec for Bella+Canvas 8800 women's racerback tank
CANVAS_W = 3210
CANVAS_H = 3927
DPI = 300

# Void System palette
CLEAN_CREAM = (232, 224, 208, 255)   # #E8E0D0 — editorial primary
AGED_CREAM  = (224, 213, 188, 255)   # #E0D5BC — vintage/divey
BRASS       = (181, 149, 58, 255)    # #B5953A — accent
DEEP_RED    = (185, 28, 28, 255)     # #B91C1C — bold accent
WHITE       = (245, 240, 230, 255)   # off-white
VOID_BLACK  = (10, 10, 10, 255)      # #0A0A0A — backgrounds only, not for print

# Resolve fonts directory relative to this file
_LIB_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.abspath(os.path.join(_LIB_DIR, "..", "fonts"))


def font_path(name):
    """Get the full path to a font file in /fonts."""
    return os.path.join(FONTS_DIR, name)


# ---------------------------------------------------------------------------
# RENDERING
# ---------------------------------------------------------------------------

def new_canvas(width=CANVAS_W, height=CANVAS_H):
    """Create a blank transparent canvas.

    Defaults to the tank print area (3210 x 3927). Override for other blanks:
        new_canvas(4500, 5400)   # Bella 3001 / Comfort Colors 1717 unisex tee
    """
    return Image.new("RGBA", (width, height), (0, 0, 0, 0))


def render_text(text, font, fill):
    """Render text to a tightly-cropped RGBA image based on actual pixel bounds.

    Uses oversized scratch canvas + getbbox() to avoid PIL's typographic
    bbox lying about glyph extents (which causes line-overlap bugs).
    """
    tmp = Image.new("RGBA", (10000, 1600), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text((50, 150), text, font=font, fill=fill)
    bbox = tmp.getbbox()
    return tmp.crop(bbox) if bbox else tmp


def fit_font_size(text, font_file, target_w, start_size=600, min_size=80, step=10):
    """Find the largest font size where `text` fits within `target_w` pixels.

    Use this to size hero lines so they don't overflow the canvas width.
    Returns an int (point size).
    """
    path = font_path(font_file) if not os.path.isabs(font_file) else font_file
    for size in range(start_size, min_size - 1, -step):
        f = ImageFont.truetype(path, size)
        tmp = Image.new("RGBA", (10000, 1600), (0, 0, 0, 0))
        d = ImageDraw.Draw(tmp)
        d.text((50, 50), text, font=f, fill=(255, 255, 255, 255))
        bb = tmp.getbbox()
        if bb and (bb[2] - bb[0]) <= target_w:
            return size
    return min_size


def paste_centered(canvas, img, y):
    """Paste an image horizontally centered on the canvas at vertical position y.

    Returns the y-coordinate of the bottom of the pasted image.
    Centering uses the canvas's actual width, so works for any blank.
    """
    x = (canvas.width - img.width) // 2
    canvas.paste(img, (x, y), img)
    return y + img.height


# ---------------------------------------------------------------------------
# EFFECTS
# ---------------------------------------------------------------------------

def apply_wear(img, intensity=0.04, n_cracks=3, seed=None):
    """Subtle worn-print effect: fine speckle + hairline horizontal cracks.

    Use for divey / vintage designs. Type stays fully readable.
    Increase `intensity` and `n_cracks` for heavier wear.
    """
    if seed is not None:
        np.random.seed(seed)

    arr = np.array(img).copy()
    alpha = arr[:, :, 3].astype(np.float32) / 255.0
    h, w = alpha.shape

    # Fine speckle — knock out ~intensity proportion of pixels with partial wear
    speckle = np.random.random((h, w))
    speckle_mask = (speckle < intensity).astype(np.float32) * np.random.uniform(0.4, 0.85, (h, w))

    # Horizontal cracks with slight wobble (mimics aged screen print)
    crack_arr = np.zeros_like(alpha)
    for _ in range(n_cracks):
        y_pos = np.random.randint(int(h * 0.2), int(h * 0.8))
        x_start = np.random.randint(0, w // 4)
        x_end = np.random.randint(3 * w // 4, w)
        thickness = np.random.randint(1, 3)
        opacity = np.random.uniform(0.3, 0.5)
        for x in range(x_start, x_end):
            wob = int(np.sin(x * 0.005) * 2)
            yy = y_pos + wob
            for ty in range(max(0, yy - thickness), min(h, yy + thickness)):
                crack_arr[ty, x] = max(crack_arr[ty, x], opacity)

    wear = np.maximum(speckle_mask, crack_arr)
    new_alpha = alpha * (1.0 - wear)
    arr[:, :, 3] = (new_alpha * 255).astype(np.uint8)
    return Image.fromarray(arr)


def add_xerox_noise(img, intensity=0.012, fill=CLEAN_CREAM, seed=None):
    """Photocopied / Xerox effect: scattered specks in transparent areas
    + light wear on the existing type.

    Use for punk zine / DIY designs.
    """
    if seed is not None:
        np.random.seed(seed)

    arr = np.array(img).copy()
    h, w = arr.shape[:2]

    # Scattered specks in transparent areas (photocopier dust)
    noise = np.random.random((h, w))
    speck_mask = noise < intensity
    transparent = arr[:, :, 3] == 0
    add_specks = speck_mask & transparent
    arr[add_specks] = [fill[0], fill[1], fill[2], np.random.randint(30, 90)]

    # Subtle wear on existing type
    alpha = arr[:, :, 3].astype(np.float32) / 255.0
    text_wear = (np.random.random((h, w)) < 0.03).astype(np.float32) * 0.6
    new_alpha = alpha * (1.0 - text_wear)
    arr[:, :, 3] = (new_alpha * 255).astype(np.uint8)
    return Image.fromarray(arr)


# ---------------------------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------------------------

def save_design(canvas, output_path):
    """Save a finished design as a print-ready PNG at 300 DPI."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    canvas.save(output_path, "PNG", dpi=(DPI, DPI))
    return output_path
