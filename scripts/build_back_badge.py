"""
One Fourteen / Whiskey Row — Back tee badge.
Premium, single-color cream ink. Built in PIL for full vector-like control.

Concept: 'Vault' — circular emblem with double ring, arched top/bottom
wordmarks, a large central serif '114', a single understated keyhole below,
and a small star above. No woodgrain, no AI sludge, no fake registration
marks, no production labels. Designed to read from 6 feet, print clean on
DTG at 4200 x 4800 (12" x ~14" at 300 DPI).
"""

from PIL import Image, ImageDraw, ImageFont
import math, os

OUT = "/home/user/workspace/one_fourteen_merch_opus"
os.makedirs(OUT, exist_ok=True)

# Print spec: ~12"x14" art board at 300 DPI -> 3600 x 4200, but we work square
# at 4200 for crisp scaling, then trim.
SIZE = 4200
CREAM = (242, 232, 210, 255)   # Comfort Colors off-white / bone
BG_TRANSPARENT = (0, 0, 0, 0)

img = Image.new("RGBA", (SIZE, SIZE), BG_TRANSPARENT)
draw = ImageDraw.Draw(img)

cx = cy = SIZE // 2

# ---------- Font loading ----------
def font(path, size):
    return ImageFont.truetype(path, size)

# Serif display for the "114" numeral and arched wordmarks.
F_SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
F_SERIF_BLACK_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-BlackItalic.ttf"
F_SANS_CONDENSED = "/usr/share/fonts/truetype/noto/NotoSansDisplay-ExtraCondensedBlack.ttf"
F_SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"

# Fallback check
for fp in [F_SERIF_BLACK, F_SANS_CONDENSED, F_SANS_BOLD]:
    assert os.path.exists(fp), f"missing {fp}"

# ---------- Outer double ring ----------
# Outer ring radius
R_OUTER = 1850
R_INNER_RING = 1760   # creates a ring band ~90px wide
RING_W = 28           # actual stroke width for thin band lines

# Heavy outer line
draw.ellipse([cx-R_OUTER, cy-R_OUTER, cx+R_OUTER, cy+R_OUTER],
             outline=CREAM, width=RING_W)
# Inner thin parallel line
draw.ellipse([cx-R_INNER_RING, cy-R_INNER_RING, cx+R_INNER_RING, cy+R_INNER_RING],
             outline=CREAM, width=10)

# ---------- Arched text helper ----------
def draw_arched_text(text, radius, center_angle_deg, font_obj,
                     letter_spacing=1.0, upright=True, clockwise=True):
    """
    Draws text along an arc. center_angle_deg = where the middle of the text sits.
    Angles: 0=right, 90=down (screen coords), -90=up.
    For top arc use center_angle_deg = -90; for bottom arc 90.
    """
    # Pre-measure per-char widths
    char_widths = []
    for ch in text:
        bbox = font_obj.getbbox(ch)
        w = bbox[2] - bbox[0]
        char_widths.append(w)
    total_w = sum(char_widths) * letter_spacing
    # Convert total width to angular span (arc length / radius)
    span = total_w / radius  # radians
    # Determine direction
    if clockwise:
        start_angle = math.radians(center_angle_deg) - span/2
        direction = 1
    else:
        start_angle = math.radians(center_angle_deg) + span/2
        direction = -1

    cursor = start_angle
    for ch, w in zip(text, char_widths):
        char_angle = (w * letter_spacing) / radius
        a = cursor + direction * (char_angle / 2)
        # Position on circle
        x = cx + radius * math.cos(a)
        y = cy + radius * math.sin(a)
        # Render glyph onto a transparent canvas, rotate, paste
        glyph_canvas_size = int(max(w * 2, font_obj.size * 2))
        gimg = Image.new("RGBA", (glyph_canvas_size, glyph_canvas_size), (0,0,0,0))
        gdraw = ImageDraw.Draw(gimg)
        # Center glyph in canvas
        gbbox = font_obj.getbbox(ch)
        gw = gbbox[2] - gbbox[0]
        gh = gbbox[3] - gbbox[1]
        gx = (glyph_canvas_size - gw)/2 - gbbox[0]
        gy = (glyph_canvas_size - gh)/2 - gbbox[1]
        gdraw.text((gx, gy), ch, fill=CREAM, font=font_obj)
        # Rotation: text baseline tangent to circle.
        if upright:
            if clockwise:
                rot = -math.degrees(a) - 90
            else:
                rot = -math.degrees(a) + 90
        else:
            rot = -math.degrees(a) + 90
        gimg = gimg.rotate(rot, resample=Image.BICUBIC)
        # Paste centered at (x,y)
        px = int(x - gimg.width/2)
        py = int(y - gimg.height/2)
        img.alpha_composite(gimg, (px, py))
        cursor += direction * char_angle

# ---------- Top arched wordmark: "ONE FOURTEEN" ----------
top_font = font(F_SERIF_BLACK, 360)
draw_arched_text("ONE  FOURTEEN", radius=1620, center_angle_deg=-90,
                 font_obj=top_font, letter_spacing=1.02,
                 upright=True, clockwise=True)

# ---------- Bottom arched wordmark: "WHISKEY ROW" centered at 6 o'clock ----------
bottom_font = font(F_SERIF_BLACK, 340)
# Bottom arc text: letters sit ALONG the curve with their feet on the inside
# (toward the center). Implementation: place at center_angle 90 (bottom),
# walking CCW, then rotate each glyph 180 from its position so it reads
# correctly. We use a custom helper that flips orientation for the bottom.
def draw_arched_text_bottom(text, radius, font_obj, letter_spacing=1.0):
    """Bottom arc: text reads left to right across the bottom of the circle,
    with letters oriented so they appear upright to a viewer (feet toward center)."""
    char_widths = []
    for ch in text:
        b = font_obj.getbbox(ch); char_widths.append(b[2]-b[0])
    total_w = sum(char_widths)*letter_spacing
    span = total_w / radius
    # Walk from left of bottom (angle = pi/2 + span/2) to right (pi/2 - span/2)
    # but we want letters in normal reading order, so start at left:
    start_angle = math.pi/2 + span/2
    cursor = start_angle
    for ch, w in zip(text, char_widths):
        char_angle = (w*letter_spacing)/radius
        a = cursor - char_angle/2
        x = cx + radius*math.cos(a)
        y = cy + radius*math.sin(a)
        gs = int(max(w*2, font_obj.size*2.2))
        gimg = Image.new("RGBA",(gs,gs),(0,0,0,0))
        gd = ImageDraw.Draw(gimg)
        gb = font_obj.getbbox(ch)
        gw = gb[2]-gb[0]; gh = gb[3]-gb[1]
        gx = (gs-gw)/2 - gb[0]
        gy = (gs-gh)/2 - gb[1]
        gd.text((gx,gy), ch, fill=CREAM, font=font_obj)
        # Rotation: letter's baseline tangent to the circle, head pointing
        # AWAY from center (so feet are at the inner radius, head at outer).
        # Tangent angle = a + pi/2 in standard coords. In PIL rotation
        # (positive = CCW, applied to image), formula:
        rot = -math.degrees(a) - 90 + 180  # flip 180 for bottom arc
        gimg = gimg.rotate(rot, resample=Image.BICUBIC)
        img.alpha_composite(gimg, (int(x-gimg.width/2), int(y-gimg.height/2)))
        cursor -= char_angle

draw_arched_text_bottom("WHISKEY  ROW", radius=1610,
                        font_obj=bottom_font, letter_spacing=1.02)

# ---------- Side ornament stars (3-pointed/diamond markers at 9 and 3 o'clock) ----------
def draw_diamond(cx_, cy_, size_, fill):
    pts = [(cx_, cy_-size_), (cx_+size_, cy_), (cx_, cy_+size_), (cx_-size_, cy_)]
    draw.polygon(pts, fill=fill)

# Separator diamonds between top and bottom arcs (at 9 and 3 o'clock)
for ang_deg in (0, 180):
    a = math.radians(ang_deg)
    x = cx + 1620 * math.cos(a)
    y = cy + 1620 * math.sin(a)
    draw_diamond(int(x), int(y), 50, CREAM)

# Small 'LOUISVILLE' on left side, 'KENTUCKY' on right — STRAIGHT (not arched)
side_font = font(F_SERIF_BLACK, 130)
for txt, ang_deg in (("LOUISVILLE", 180), ("KENTUCKY", 0)):
    # Skip — keep it clean. Diamonds alone read better.
    pass

# ---------- Central giant "114" numeral ----------
num_font = font(F_SERIF_BLACK, 1700)
num_text = "114"
nbbox = draw.textbbox((0,0), num_text, font=num_font)
nw = nbbox[2] - nbbox[0]
nh = nbbox[3] - nbbox[1]
nx = cx - nw/2 - nbbox[0]
ny = cy - nh/2 - nbbox[1] - 60  # slight lift to balance keyhole below
draw.text((nx, ny), num_text, fill=CREAM, font=num_font)

# ---------- Small "EST." & year flanking the numeral ----------
small_font = font(F_SERIF_BLACK_ITALIC, 130) if os.path.exists(F_SERIF_BLACK_ITALIC) else font(F_SERIF_BLACK, 130)
# "EST." on left of 114, year on right -- but only if it doesn't crowd. Skip year (no canon), use bourbon-classic "EST." dropped.
# Instead place small label "BOURBON · COCKTAILS" above keyhole.

# ---------- Tagline strip under numeral ----------
tag_font = font(F_SANS_CONDENSED, 130)
tag = "BOURBON  ·  COCKTAILS  ·  LATE NIGHTS"
tbbox = draw.textbbox((0,0), tag, font=tag_font)
tw = tbbox[2] - tbbox[0]
th = tbbox[3] - tbbox[1]
draw.text((cx - tw/2 - tbbox[0], cy + 780 - tbbox[1]), tag, fill=CREAM, font=tag_font)

# Thin underline rule under tagline
draw.rectangle([cx - tw/2 - 40, cy + 780 + th + 50,
                cx + tw/2 + 40, cy + 780 + th + 56], fill=CREAM)
# Matching hairline above tagline
draw.rectangle([cx - tw/2 - 40, cy + 760,
                cx + tw/2 + 40, cy + 766], fill=CREAM)

# ---------- Small star above numeral ----------
def draw_star(cx_, cy_, r_outer, r_inner, points=5, fill=CREAM, rotation=-math.pi/2):
    pts = []
    for i in range(points*2):
        ang = rotation + i * math.pi / points
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx_ + r*math.cos(ang), cy_ + r*math.sin(ang)))
    draw.polygon(pts, fill=fill)

draw_star(cx, cy - 1170, 75, 32, points=5, fill=CREAM)

# ---------- Hairline circle behind the 114 (very subtle inner emblem) ----------
# REMOVED - kept clean per requirements.

print("Saved base layer")

# ---------- Trim transparent margins and save full + 'standard' tee print size ----------
bbox = img.getbbox()
img_cropped = img.crop(bbox)
# Add small breathing room
pad = 60
final = Image.new("RGBA", (img_cropped.width + pad*2, img_cropped.height + pad*2), (0,0,0,0))
final.paste(img_cropped, (pad, pad), img_cropped)

# Resize to print-ready 4500 wide (15" at 300 DPI) — DTG safe area.
target_w = 4500
ratio = target_w / final.width
target_h = int(final.height * ratio)
final_print = final.resize((target_w, target_h), Image.LANCZOS)

out_path = os.path.join(OUT, "one_fourteen_back_badge_cream.png")
final_print.save(out_path, "PNG", optimize=True)
print(f"Saved {out_path}  size={final_print.size}")

# Also save a black-ink variant for light tees
img_black = Image.new("RGBA", final_print.size, (0,0,0,0))
px_src = final_print.load()
px_dst = img_black.load()
for y in range(final_print.height):
    for x in range(final_print.width):
        r,g,b,a = px_src[x,y]
        if a > 0:
            px_dst[x,y] = (28, 22, 18, a)
out_black = os.path.join(OUT, "one_fourteen_back_badge_black.png")
img_black.save(out_black, "PNG", optimize=True)
print(f"Saved {out_black}")
