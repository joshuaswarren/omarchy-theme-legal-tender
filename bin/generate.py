#!/usr/bin/env python3
"""Generate the Oligarchy banknote wallpaper.

Draws an engraved million-dollar "Omacom Foundation Note" as the printing
plate: cream and money-green intaglio lines on ink black. Supersampled 2x,
then downscaled for clean 1px engraving lines at 4K.
"""

import math
from PIL import Image, ImageDraw, ImageFont

# Final canvas and supersample factor.
W, H = 3840, 2160
SS = 2
CW, CH = W * SS, H * SS

# Palette (the plate, not the note).
BG = "#0e1411"
GREEN = "#6f9663"
GREEN_DIM = "#3a523f"
CREAM = "#ddd8c4"
GOLD = "#c9a554"
RED = "#a84a42"

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

MICROPRINT = "ELITE CAPITAL \u00b7 PUBLIC CODE \u00b7 ZERO DOLLARS \u00b7 SEVERAL BILLIONAIRES \u00b7 "

img = Image.new("RGB", (CW, CH), BG)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size * SS)


def rosette(cx, cy, r_outer, r_inner, color, petals=24, turns=360, width=1):
    """Hypotrochoid guilloche rosette between two radii."""
    cx, cy = cx * SS, cy * SS
    r_o, r_i = r_outer * SS, r_inner * SS
    mid = (r_o + r_i) / 2
    amp = (r_o - r_i) / 2
    pts = []
    for t in range(turns * 4 + 1):
        a = math.radians(t / 4)
        r = mid + amp * math.sin(petals * a)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.line(pts, fill=color, width=width * SS)


def lattice_band(y0, y1, color, waves=9, strands=14, width=1):
    """Interleaved sine strands across the full width (lathe-work band)."""
    y0, y1 = y0 * SS, y1 * SS
    mid = (y0 + y1) / 2
    amp = (y1 - y0) / 2
    for s in range(strands):
        phase = math.pi * s / strands
        pts = []
        for x in range(0, CW + 1, 6):
            y = mid + amp * math.sin(2 * math.pi * waves * x / CW + phase) * math.cos(
                math.pi * s / strands
            )
            pts.append((x, y))
        d.line(pts, fill=color, width=width * SS)


def arc_text(cx, cy, radius, text, fnt, color, start_deg, end_deg, flip=False):
    """Place characters along an arc, each rotated to the tangent."""
    n = len(text)
    for i, ch in enumerate(text):
        frac = i / max(n - 1, 1)
        ang = math.radians(start_deg + (end_deg - start_deg) * frac)
        x = cx + radius * math.cos(ang)
        y = cy + radius * math.sin(ang)
        rot = math.degrees(ang) + (-90 if flip else 90)
        glyph = Image.new("RGBA", (fnt.size * 2, fnt.size * 2), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glyph)
        gd.text((fnt.size, fnt.size), ch, font=fnt, fill=color, anchor="mm")
        glyph = glyph.rotate(-rot, resample=Image.BICUBIC, center=(fnt.size, fnt.size))
        img.paste(glyph, (int(x * SS - fnt.size), int(y * SS - fnt.size)), glyph)


def star(cx, cy, r, color):
    cx, cy, r = cx * SS, cy * SS, r * SS
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.4
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def text_at(x, y, s, fnt, color, anchor="mm", tracking=0):
    if tracking == 0:
        d.text((x * SS, y * SS), s, font=fnt, fill=color, anchor=anchor)
        return
    total = sum(d.textlength(c, font=fnt) for c in s) + tracking * SS * (len(s) - 1)
    cx = x * SS - total / 2
    for c in s:
        w = d.textlength(c, font=fnt)
        d.text((cx, y * SS), c, font=fnt, fill=color, anchor="lm")
        cx += w + tracking * SS


# ── Border: double rule with a microprint line between ──────────────────────
for m, wd in ((70, 4), (86, 1), (118, 2)):
    d.rectangle([m * SS, m * SS, CW - m * SS, CH - m * SS], outline=GREEN, width=wd * SS)

mp_font = font(SERIF, 11)
mp = (MICROPRINT * 40)
mp_len = int(d.textlength(mp, font=mp_font))
for y in (96, H - 106):
    x = 130 * SS
    while x < CW - 130 * SS:
        d.text((x, y * SS), MICROPRINT, font=mp_font, fill=GREEN_DIM)
        x += int(d.textlength(MICROPRINT, font=mp_font))

# ── Background lathe band behind the medallion ──────────────────────────────
lattice_band(970, 1090, GREEN_DIM, waves=30, strands=18)

# ── Corner denomination rosettes ────────────────────────────────────────────
for cx, cy in ((330, 320), (W - 330, 320), (330, H - 320), (W - 330, H - 320)):
    rosette(cx, cy, 170, 138, GREEN, petals=14)
    rosette(cx, cy, 118, 100, GREEN_DIM, petals=28)
    text_at(cx, cy, "1M", font(SERIF, 96), CREAM)

# ── Central medallion ────────────────────────────────────────────────────────
CX, CY = W // 2, 1010
rosette(CX, CY, 540, 484, GREEN, petals=40)
rosette(CX, CY, 506, 446, GREEN_DIM, petals=44)
rosette(CX, CY, 428, 398, GOLD, petals=60)
# Radial engraving shading inside the ring.
for t in range(0, 360, 3):
    a = math.radians(t)
    r1, r2 = 236 * SS, 390 * SS
    d.line(
        [
            (CX * SS + r1 * math.cos(a), CY * SS + r1 * math.sin(a)),
            (CX * SS + r2 * math.cos(a), CY * SS + r2 * math.sin(a)),
        ],
        fill=GREEN_DIM,
        width=SS,
    )
# The O: a heavy engraved ring.
d.ellipse(
    [(CX - 210) * SS, (CY - 210) * SS, (CX + 210) * SS, (CY + 210) * SS],
    outline=CREAM,
    width=52 * SS,
)
d.ellipse(
    [(CX - 228) * SS, (CY - 228) * SS, (CX + 228) * SS, (CY + 228) * SS],
    outline=GREEN,
    width=3 * SS,
)
d.ellipse(
    [(CX - 192) * SS, (CY - 192) * SS, (CX + 192) * SS, (CY + 192) * SS],
    outline=GREEN,
    width=3 * SS,
)

# Arc captions around the medallion.
arc_text(CX, CY, 610, "OMACOM FOUNDATION NOTE", font(SERIF, 64), CREAM, 200, 340)
arc_text(CX, CY, 616, "IN PATRONS WE TRUST", font(SERIF, 46), GOLD, 150, 30, flip=True)

# ── Headline and denomination ───────────────────────────────────────────────
text_at(W // 2, 1755, "ONE MILLION DOLLARS", font(SERIF, 92), GOLD, tracking=26)
text_at(W // 2, 208, "THE OLIGARCHY \u00b7 FREE SOFTWARE \u00b7 EXPENSIVE PATRONS", font(SERIF, 40), GREEN, tracking=10)

# ── Stars: eight founding patrons, then two more ────────────────────────────
sx = W // 2 - 5 * 62
for i in range(8):
    star(sx + i * 62, 1878, 20, GOLD)
for i in range(2):
    star(sx + 8 * 62 + 20 + i * 46, 1882, 12, GOLD)

# ── Serial numbers ──────────────────────────────────────────────────────────
ser = font(MONO, 44)
d.text((430 * SS, 470 * SS), "OG 0.001% A", font=ser, fill=RED)
d.text(((W - 850) * SS, 1620 * SS), "OG 0.001% A", font=ser, fill=RED)

# ── Signatures and series ───────────────────────────────────────────────────
sig = font(SERIF_IT, 52)
cap = font(SERIF, 26)
d.text((560 * SS, 1930 * SS), "D. H. Hansson", font=sig, fill=CREAM, anchor="mm")
d.line([360 * SS, 1965 * SS, 760 * SS, 1965 * SS], fill=GREEN, width=2 * SS)
text_at(560, 1995, "BENEVOLENT DICTATOR FOR LIFE", cap, GREEN, tracking=4)
d.text(((W - 560) * SS, 1930 * SS), "you@omarchy", font=sig, fill=CREAM, anchor="mm")
d.line([(W - 760) * SS, 1965 * SS, (W - 360) * SS, 1965 * SS], fill=GREEN, width=2 * SS)
text_at(W - 560, 1995, "PATRON OF THE ARTS", cap, GREEN, tracking=4)
text_at(W // 2, 1995, "SERIES 2026", cap, GREEN, tracking=6)

out = img.resize((W, H), Image.LANCZOS)
out.save("backgrounds/legal-tender.png")
print("saved backgrounds/legal-tender.png")

# ── Lock-screen glyph: a small engraved 1M rosette on transparency ──────────
U = 512
ug = Image.new("RGBA", (U * SS, U * SS), (0, 0, 0, 0))
ud = ImageDraw.Draw(ug)
ucx = U * SS / 2
mid, amp = 0.42 * U * SS, 0.06 * U * SS
pts = []
for t in range(360 * 4 + 1):
    a = math.radians(t / 4)
    r = mid + amp * math.sin(14 * a)
    pts.append((ucx + r * math.cos(a), ucx + r * math.sin(a)))
ud.line(pts, fill=CREAM, width=2 * SS)
ud.ellipse(
    [ucx - 0.30 * U * SS, ucx - 0.30 * U * SS, ucx + 0.30 * U * SS, ucx + 0.30 * U * SS],
    outline=CREAM,
    width=2 * SS,
)
ud.text((ucx, ucx), "1M", font=font(SERIF, 150), fill=CREAM, anchor="mm")
ug.resize((U, U), Image.LANCZOS).save("unlock.png")
print("saved unlock.png")
