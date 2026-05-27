"""
Contact sheet / mockup preview on a black-pepper tee tone background.
Three panels:
  - Front (cream variant)
  - Front (neon variant)
  - Back badge
With labels and approximate scale indicators.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/home/user/workspace/one_fourteen_merch_opus"

# Comfort Colors 'pepper' = warm near-black
BG = (32, 28, 25)
TEE_TONE = (38, 33, 30)   # slightly lighter tee panel
INK = (242, 232, 210)
MUTED = (140, 130, 115)

# Sheet 2400x1500
W, H = 2800, 1800
sheet = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(sheet)

# Fonts
F_TITLE = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", 56)
F_LABEL = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", 28)
F_BODY  = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", 24)
F_SERIF_BLACK = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf", 40)

# Header
d.text((80, 60), "ONE FOURTEEN  /  WHISKEY ROW", fill=INK, font=F_SERIF_BLACK)
d.text((80, 120), "MERCH ARTWORK — HERO TEE — PROOF", fill=MUTED, font=F_LABEL)
d.text((W-560, 75), "Comfort Colors  ·  Pepper / Black", fill=MUTED, font=F_LABEL)
d.text((W-560, 110), "DTG print  ·  one-color cream + accent red", fill=MUTED, font=F_LABEL)

# Hairline
d.rectangle([80, 175, W-80, 178], fill=(80,70,62))

# ----- Tee panel coordinates -----
panel_top = 230
panel_h = 1480
# Three panels side by side
pad = 50
pw = (W - 80*2 - pad*2) // 3
ph = panel_h

panels = [
    ("FRONT — CHEST HIT (CREAM)", "one_fourteen_front_chest_cream.png", "Centered chest, ~3.5\" wide"),
    ("FRONT — CHEST HIT (NEON)",  "one_fourteen_front_neon.png",        "Centered chest, ~3.5\" wide"),
    ("BACK — VAULT BADGE",        "one_fourteen_back_badge_cream.png",  "Centered upper back, ~12\" wide"),
]

x = 80
for label, fname, sub in panels:
    # Panel background (tee tone)
    d.rectangle([x, panel_top, x+pw, panel_top+ph], fill=TEE_TONE)
    # Subtle frame
    d.rectangle([x, panel_top, x+pw, panel_top+ph], outline=(60,53,48), width=2)

    # Label band at top of panel
    band_h = 80
    d.rectangle([x, panel_top, x+pw, panel_top+band_h], fill=(50,44,40))
    d.text((x+24, panel_top+22), label, fill=INK, font=F_LABEL)

    # Load art
    art_path = os.path.join(OUT, fname)
    art = Image.open(art_path).convert("RGBA")
    # Fit inside panel below the band, with margin
    avail_w = pw - 80
    avail_h = ph - band_h - 160
    ar = art.width / art.height
    if ar >= avail_w/avail_h:
        new_w = avail_w
        new_h = int(new_w / ar)
    else:
        new_h = avail_h
        new_w = int(new_h * ar)
    art_small = art.resize((new_w, new_h), Image.LANCZOS)
    ax = x + (pw - new_w)//2
    ay = panel_top + band_h + 60 + (avail_h - new_h)//2
    sheet.paste(art_small, (ax, ay), art_small)

    # Sub caption at bottom
    sb = F_BODY.getbbox(sub)
    sw = sb[2]-sb[0]
    d.text((x + (pw-sw)//2, panel_top + ph - 60), sub, fill=MUTED, font=F_BODY)
    x += pw + pad

# Footer
d.rectangle([80, H-90, W-80, H-87], fill=(80,70,62))
d.text((80, H-70), "Cream ink: PMS 7527-ish (Bone)  ·  Neon red ink: ~PMS 1788 / 485 mix  ·  Designed for DTG; convert to plastisol screens if needed.",
       fill=MUTED, font=F_BODY)

sheet.save(os.path.join(OUT, "one_fourteen_mockup_contact_sheet.jpg"), "JPEG", quality=92)
print("saved sheet")

# Also export a single "tee back" mockup approximation
tee = Image.new("RGB", (1800, 2200), BG)
td = ImageDraw.Draw(tee)
# Tee silhouette (very simplified rect with curved shoulders)
tee_body = (38, 33, 30)
# Crewneck rounded rect
from PIL import ImageDraw
shoulder = 200
neck = 250
body_top = 240
body_bottom = 2100
left = 280; right = 1520
# Tee body
td.rounded_rectangle([left, body_top+80, right, body_bottom], radius=40, fill=tee_body)
# Sleeves
td.polygon([(left, body_top+80), (left-150, body_top+260), (left-90, body_top+560), (left+60, body_top+340), (left, body_top+200)], fill=tee_body)
td.polygon([(right, body_top+80), (right+150, body_top+260), (right+90, body_top+560), (right-60, body_top+340), (right, body_top+200)], fill=tee_body)
# Neckline
td.ellipse([900-neck//2, body_top+30, 900+neck//2, body_top+170], fill=BG)
# Place back badge centered on upper back area
back = Image.open(os.path.join(OUT, "one_fourteen_back_badge_cream.png")).convert("RGBA")
target_w = 1000
ratio = target_w/back.width
back_small = back.resize((target_w, int(back.height*ratio)), Image.LANCZOS)
bx = 900 - back_small.width//2
by = body_top + 320
tee.paste(back_small, (bx, by), back_small)
# Add a label
td.text((100, 100), "TEE BACK — APPROX. PLACEMENT", fill=MUTED, font=F_LABEL)
tee.save(os.path.join(OUT, "one_fourteen_tee_back_mockup.jpg"), "JPEG", quality=92)
print("saved tee back mockup")

# Tee front mockup with neon
tee2 = Image.new("RGB", (1800, 2200), BG)
td2 = ImageDraw.Draw(tee2)
td2.rounded_rectangle([left, body_top+80, right, body_bottom], radius=40, fill=tee_body)
td2.polygon([(left, body_top+80), (left-150, body_top+260), (left-90, body_top+560), (left+60, body_top+340), (left, body_top+200)], fill=tee_body)
td2.polygon([(right, body_top+80), (right+150, body_top+260), (right+90, body_top+560), (right-60, body_top+340), (right, body_top+200)], fill=tee_body)
td2.ellipse([900-neck//2, body_top+30, 900+neck//2, body_top+170], fill=BG)
front = Image.open(os.path.join(OUT, "one_fourteen_front_neon.png")).convert("RGBA")
target_w = 520
ratio = target_w/front.width
front_small = front.resize((target_w, int(front.height*ratio)), Image.LANCZOS)
fx = 900 - front_small.width//2
fy = body_top + 380
tee2.paste(front_small, (fx, fy), front_small)
td2.text((100, 100), "TEE FRONT — CHEST HIT (NEON)", fill=MUTED, font=F_LABEL)
tee2.save(os.path.join(OUT, "one_fourteen_tee_front_mockup.jpg"), "JPEG", quality=92)
print("saved tee front mockup")
