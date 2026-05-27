"""
Front chest hit '114' — neon-style flat 2-color version (DTG-print friendly).

Cream-yellow fill with thick warm red outline = neon-tube illusion.
Plus a soft outer red glow halo.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, numpy as np

OUT = "/home/user/workspace/one_fourteen_merch_opus"
TRANSP = (0,0,0,0)
NEON_RED  = (235, 38, 28, 255)
NEON_CORE = (255, 234, 175, 255)   # warm cream-yellow
CREAM     = (242, 232, 210, 255)

F_SCRIPT = "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf"
F_SANS   = "/usr/share/fonts/truetype/noto/NotoSansDisplay-ExtraCondensedBlack.ttf"

W, H = 2600, 1900
img = Image.new("RGBA", (W, H), TRANSP)

# ----- Numerals -----
font_main = ImageFont.truetype(F_SCRIPT, 950)
text = "114"
# Letter spacing
spacing = 100
widths = [font_main.getbbox(ch)[2]-font_main.getbbox(ch)[0] for ch in text]
total = sum(widths) + spacing*(len(text)-1)

# Determine y baseline using a tall reference character
ref_bbox = font_main.getbbox("114")
th = ref_bbox[3]-ref_bbox[1]
ty = 200 - ref_bbox[1]  # top margin 200

# Draw character-by-character with stroke for tube look
tube_img = Image.new("RGBA", (W,H), TRANSP)
tdraw = ImageDraw.Draw(tube_img)
cur_x = (W - total)/2
positions = []
for ch, w in zip(text, widths):
    b = font_main.getbbox(ch)
    px = cur_x - b[0]
    positions.append((px, ty, ch))
    tdraw.text((px, ty), ch, fill=NEON_CORE, font=font_main,
               stroke_width=22, stroke_fill=NEON_RED)
    cur_x += w + spacing

# Soft red glow halo: render same text in pure red, blur heavily
glow = Image.new("RGBA", (W,H), TRANSP)
gd = ImageDraw.Draw(glow)
for px, py, ch in positions:
    gd.text((px, py), ch, fill=(255,40,20,220), font=font_main, stroke_width=22, stroke_fill=(255,40,20,220))
glow = glow.filter(ImageFilter.GaussianBlur(radius=55))
arr = np.array(glow)
arr[...,3] = (arr[...,3].astype(np.uint16) * 2.0).clip(0,255).astype(np.uint8)
glow = Image.fromarray(arr)
# second tighter glow for hot core radiation
glow2 = Image.new("RGBA", (W,H), TRANSP)
g2d = ImageDraw.Draw(glow2)
for px, py, ch in positions:
    g2d.text((px, py), ch, fill=(255,200,120,255), font=font_main, stroke_width=22, stroke_fill=(255,200,120,255))
glow2 = glow2.filter(ImageFilter.GaussianBlur(radius=18))
arr2 = np.array(glow2)
arr2[...,3] = (arr2[...,3].astype(np.uint16) * 0.6).clip(0,255).astype(np.uint8)
glow2 = Image.fromarray(arr2)

# Composite
img.alpha_composite(glow)
img.alpha_composite(glow2)
img.alpha_composite(tube_img)

# ----- Subline strap -----
sub_top = ty + th + 260
sf = ImageFont.truetype(F_SANS, 110)
sub = "ONE FOURTEEN  ·  WHISKEY ROW"
fdraw = ImageDraw.Draw(img)
sb = sf.getbbox(sub)
sw = sb[2]-sb[0]; sh = sb[3]-sb[1]
sx = (W-sw)/2 - sb[0]
sy = sub_top - sb[1]
fdraw.text((sx, sy), sub, fill=CREAM, font=sf)
rule_cy = sub_top + sh/2
rule_w = 320; rule_h = 6; gap = 90
fdraw.rectangle([sx-gap-rule_w, rule_cy-rule_h/2, sx-gap, rule_cy+rule_h/2], fill=CREAM)
fdraw.rectangle([sx+sw+gap, rule_cy-rule_h/2, sx+sw+gap+rule_w, rule_cy+rule_h/2], fill=CREAM)

# Crop & save
bb = img.getbbox()
out = img.crop(bb)
pad = 100
canvas = Image.new("RGBA", (out.width+pad*2, out.height+pad*2), TRANSP)
canvas.paste(out, (pad,pad), out)
target_w = 1800
ratio = target_w/canvas.width
canvas = canvas.resize((target_w, int(canvas.height*ratio)), Image.LANCZOS)
canvas.save(os.path.join(OUT, "one_fourteen_front_neon.png"), "PNG", optimize=True)
print("saved", canvas.size)
