"""
Front chest hit '114' — one-color cream version (matches back badge style).
Small, ~3.5" wide on tee at 300dpi -> ~1050px wide. We render at 1800px wide
for headroom.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/home/user/workspace/one_fourteen_merch_opus"
CREAM = (242, 232, 210, 255)

F_SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
F_SANS_CONDENSED = "/usr/share/fonts/truetype/noto/NotoSansDisplay-ExtraCondensedBlack.ttf"

W, H = 2400, 1700
img = Image.new("RGBA", (W, H), (0,0,0,0))
draw = ImageDraw.Draw(img)

# Big 114 at top
nf = ImageFont.truetype(F_SERIF_BLACK, 1100)
bbox = draw.textbbox((0,0), "114", font=nf)
nw = bbox[2]-bbox[0]; nh = bbox[3]-bbox[1]
num_top = 60
nx = (W - nw)/2 - bbox[0]
ny = num_top - bbox[1]
draw.text((nx, ny), "114", fill=CREAM, font=nf)
num_bottom = num_top + nh

# Strap line below, well-separated
sf = ImageFont.truetype(F_SANS_CONDENSED, 130)
sub = "ONE FOURTEEN  ·  WHISKEY ROW"
sb = draw.textbbox((0,0), sub, font=sf)
sw = sb[2]-sb[0]; sh = sb[3]-sb[1]
sx = (W - sw)/2 - sb[0]
sy_top = num_bottom + 180
sy = sy_top - sb[1]
draw.text((sx, sy), sub, fill=CREAM, font=sf)

# Hairline rules left/right of subline (matching its vertical center)
rule_cy = sy_top + sh/2
rule_h = 8
gap = 90
draw.rectangle([sx - 360 - gap, rule_cy-rule_h/2, sx-gap, rule_cy+rule_h/2], fill=CREAM)
draw.rectangle([sx+sw+gap, rule_cy-rule_h/2, sx+sw+gap+360, rule_cy+rule_h/2], fill=CREAM)

# Crop transparent margins
bb = img.getbbox()
out = img.crop(bb)
pad = 60
final = Image.new("RGBA", (out.width+pad*2, out.height+pad*2), (0,0,0,0))
final.paste(out, (pad,pad), out)

# Resize to 1800 wide print
target_w = 1800
ratio = target_w / final.width
final = final.resize((target_w, int(final.height*ratio)), Image.LANCZOS)
final.save(os.path.join(OUT, "one_fourteen_front_chest_cream.png"), "PNG", optimize=True)
print("saved", final.size)
