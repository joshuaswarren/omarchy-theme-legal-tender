#!/usr/bin/env python3
"""Render the nine Legal Tender backgrounds at 3840x2560 (3:2).

Nine distinct engravings of the Omacom Foundation Note, one per plate:
full note, medallion macro, guilloche field, seal of stars, corner
denomination, signature plate, serial strip, inverse cream note, and a
minimal gold seal. Also writes the canonical hero and the unlock glyph.

Run from the repo root:  bin/generate.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw

from engrave import (
    BG, BG_DEEP, BLUE, CREAM, CREAM_BRIGHT, GOLD, GREEN, GREEN_BRIGHT, GREEN_DIM,
    GREEN_INK, MONO, MONO_BOLD, Plate, RED, SERIF, SERIF_IT, SERIF_REG,
)

W, H = 3840, 2560

SCENES = []  # (slug, builder) filled by the decorators below


def scene(fn):
    SCENES.append((fn.__name__.replace("scene_", "").replace("_", "-"), fn))
    return fn


# ─────────────────────────────────────────────────────────────────────────
# 01 · Foundation Note — the complete bill, edge to edge
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_foundation_note(p):
    p.border(((56, 4), (72, 1), (102, 2)))
    p.microprint(86)
    p.microprint(H - 96)
    p.text_at(W / 2, 168, "THE OLIGARCHY \u00b7 FREE SOFTWARE \u00b7 EXPENSIVE PATRONS",
              p.font(SERIF, 42), GREEN, tracking=10)

    p.lattice_band(1000, 1130, GREEN_DIM, waves=30, strands=18, width=2)

    for cx, cy in ((300, 300), (W - 300, 300), (300, H - 300), (W - 300, H - 300)):
        p.d.ellipse([p.s(cx - 205), p.s(cy - 205), p.s(cx + 205), p.s(cy + 205)], fill=CREAM)
        p.rosette(cx, cy, 190, 158, GREEN_INK, petals=14, width=4)
        p.rosette(cx, cy, 132, 112, GREEN, petals=28, width=3)
        p.text_at(cx, cy, "1M", p.font(SERIF, 130), GREEN_INK)

    p.d.ellipse([p.s(W / 2 - 290), p.s(1150 - 290), p.s(W / 2 + 290), p.s(1150 + 290)],
                fill=CREAM)
    p.o_medallion(W / 2, 1150)
    p.d.rounded_rectangle([p.s(340), p.s(1720), p.s(W - 340), p.s(1975)], radius=44, fill=CREAM)
    p.text_at(W / 2, 1848, "ONE MILLION DOLLARS", p.font(SERIF, 130), GREEN_INK, tracking=24)
    p.patron_stars(W / 2, 1910, GREEN_INK)
    p.serials("OG 0.001% 1M")

    sig, cap = p.font(SERIF_IT, 52), p.font(SERIF, 26)
    p.text_at(560, 2050, "D. H. Hansson", sig, CREAM)
    p.d.line([p.s(360), p.s(2085), p.s(760), p.s(2085)], fill=GREEN, width=int(2 * p.ss))
    p.text_at(560, 2115, "BENEVOLENT DICTATOR FOR LIFE", cap, GREEN, tracking=4)
    p.text_at(W - 560, 2050, "you@omarchy", sig, CREAM)
    p.d.line([p.s(W - 760), p.s(2085), p.s(W - 360), p.s(2085)], fill=GREEN, width=int(2 * p.ss))
    p.text_at(W - 560, 2115, "PATRON OF THE ARTS", cap, GREEN, tracking=4)
    p.text_at(W / 2, 2115, "SERIES 2026", cap, GREEN, tracking=6)
    p.text_at(W / 2, 2340, "THIS NOTE IS LEGAL TENDER FOR ALL DEBTS, TECHNICAL AND OTHERWISE",
              p.font(SERIF_REG, 30), GREEN_DIM, tracking=6)


# ─────────────────────────────────────────────────────────────────────────
# 02 · Medallion Macro — the O at press scale, cropped by the frame
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_medallion_macro(p):
    p.lattice_band(60, 240, GREEN_DIM, waves=26, strands=14, width=2)
    p.lattice_band(H - 240, H - 60, GREEN_DIM, waves=26, strands=14, width=2)
    p.d.ellipse([p.s(W / 2 - 560), p.s(H / 2 + 120 - 560), p.s(W / 2 + 560), p.s(H / 2 + 120 + 560)],
                fill=CREAM)
    p.rosette(W / 2, H / 2 + 120, 1620, 1460, GREEN, petals=48, width=5)
    p.rosette(W / 2, H / 2 + 120, 1500, 1300, GREEN_DIM, petals=56, width=3)
    p.rosette(W / 2, H / 2 + 120, 1240, 1160, GOLD, petals=72, width=3)
    p.radial(W / 2, H / 2 + 120, 760, 1240, GREEN, step=3, width=2)

    cx, cy, r = W / 2, H / 2 + 120, 640
    p.d.ellipse([p.s(cx - r), p.s(cy - r), p.s(cx + r), p.s(cy + r)],
                outline=CREAM, width=int(120 * p.ss))
    p.d.ellipse([p.s(cx - r - 56), p.s(cy - r - 56), p.s(cx + r + 56), p.s(cy + r + 56)],
                outline=GREEN, width=int(6 * p.ss))
    p.d.ellipse([p.s(cx - r + 56), p.s(cy - r + 56), p.s(cx + r - 56), p.s(cy + r - 56)],
                outline=GREEN, width=int(6 * p.ss))
    p.arc_text(cx, cy, 1250, "OMACOM FOUNDATION", p.font(SERIF, 132), CREAM, 200, 340)
    p.arc_text(cx, cy, 1046, "IN PATRONS WE TRUST", p.font(SERIF, 96), GOLD, 150, 30, flip=True)

    for x, y in ((160, 160), (W - 160, 160), (160, H - 160), (W - 160, H - 160)):
        p.crosshair(x, y, 46, CREAM, width=3)
    plate = p.font(MONO, 40)
    p.d.text((p.s(230), p.s(120)), "PLATE 02", font=plate, fill=GREEN_DIM)
    p.d.text((p.s(230), p.s(H - 168)), "SERIES 2026", font=plate, fill=GREEN_DIM)
    p.d.text((p.s(W - 430), p.s(H - 168)), "OG 0.001%", font=p.font(MONO_BOLD, 40), fill=RED)


# ─────────────────────────────────────────────────────────────────────────
# 03 · Guilloche Field — full-frame lathe work, red treasury roundel
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_guilloche_field(p):
    bands = [
        (90, 380, GREEN, 14, 16, 3),
        (430, 660, GREEN_DIM, 18, 14, 2),
        (700, 1010, GREEN_BRIGHT, 10, 18, 3),
        (1050, 1260, GOLD, 22, 12, 2),
        (1300, 1610, GREEN, 12, 18, 3),
        (1650, 1860, GREEN_DIM, 18, 14, 2),
        (1900, 2210, GREEN_BRIGHT, 14, 16, 3),
        (2250, 2470, GOLD, 20, 12, 2),
    ]
    for y0, y1 in ((430, 660), (1650, 1860)):
        p.d.rectangle([0, p.s(y0), p.s(W), p.s(y1)], fill=CREAM)
    bands[1] = (430, 660, GREEN_INK, 18, 14, 3)
    bands[5] = (1650, 1860, GREEN_INK, 18, 14, 3)
    for y0, y1, col, waves, strands, wd in bands:
        p.lattice_band(y0, y1, col, waves=waves, strands=strands, width=wd)

    cx, cy = W / 2, H / 2
    p.d.ellipse([p.s(cx - 330), p.s(cy - 330), p.s(cx + 330), p.s(cy + 330)],
                outline=RED, width=int(10 * p.ss))
    p.d.ellipse([p.s(cx - 300), p.s(cy - 300), p.s(cx + 300), p.s(cy + 300)],
                outline=RED, width=int(3 * p.ss))
    p.arc_text(cx, cy, 358, "TREASURY OF THE OLIGARCHY", p.font(SERIF, 52), RED, 195, 345)
    p.arc_text(cx, cy, 362, "SECURITY FIELD", p.font(SERIF, 40), RED, 15, 165, flip=True)
    p.text_at(cx, cy, "OG", p.font(SERIF, 190), CREAM_BRIGHT)

    p.d.text((p.s(200), p.s(120)), "03", font=p.font(MONO_BOLD, 56), fill=GREEN_DIM)
    p.text_at(W / 2, 2330, "GUILLOCHE SECURITY FIELD \u00b7 DO NOT PHOTOCOPY",
              p.font(SERIF, 36), CREAM, tracking=10)


# ─────────────────────────────────────────────────────────────────────────
# 04 · Seal of Stars — the great seal, sunburst behind
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_seal_of_stars(p):
    p.rays(W / 2, H / 2, 1000, 1780, GREEN_DIM, count=72, width=5)
    p.rays(W / 2, H / 2, 760, 1100, GREEN, count=36, width=4)

    cx, cy = W / 2, H / 2
    p.d.ellipse([p.s(cx - 800), p.s(cy - 800), p.s(cx + 800), p.s(cy + 800)], fill=GOLD)
    p.d.ellipse([p.s(cx - 690), p.s(cy - 690), p.s(cx + 690), p.s(cy + 690)],
                fill="#0d1812")
    p.d.ellipse([p.s(cx - 800), p.s(cy - 800), p.s(cx + 800), p.s(cy + 800)],
                outline=GOLD, width=int(18 * p.ss))
    p.d.ellipse([p.s(cx - 770), p.s(cy - 770), p.s(cx + 770), p.s(cy + 770)],
                outline=GOLD, width=int(3 * p.ss))
    p.d.ellipse([p.s(cx - 690), p.s(cy - 690), p.s(cx + 690), p.s(cy + 690)],
                outline=GREEN, width=int(4 * p.ss))
    p.arc_text(cx, cy, 800, "OMACOM FOUNDATION", p.font(SERIF, 96), GOLD, 198, 342)
    p.arc_text(cx, cy, 806, "SERIES 2026", p.font(SERIF, 64), CREAM, 155, 25, flip=True)

    for i in range(8):
        a = math.radians(-90 + i * 45)
        p.star(cx + 620 * math.cos(a), cy + 620 * math.sin(a), 64, CREAM)
    p.star(cx + 500, cy + 500, 30, GOLD)
    p.star(cx - 500, cy - 500, 30, GOLD)

    r = 330
    p.d.ellipse([p.s(cx - r), p.s(cy - r), p.s(cx + r), p.s(cy + r)], fill=CREAM)
    p.d.ellipse([p.s(cx - r), p.s(cy - r), p.s(cx + r), p.s(cy + r)],
                outline=GREEN_INK, width=int(58 * p.ss))
    p.star(cx, cy, 190, GOLD)
    p.dot_ring(cx, cy, 655, GREEN, count=8, dr=6)

    p.serials("OG 0.001% \u2605", size=40, spots=[(260, 220), (W - 700, H - 280)])


# ─────────────────────────────────────────────────────────────────────────
# 05 · Corner Denomination — four giant engraved 100s
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_corner_denomination(p):
    for cx, cy in ((430, 430), (W - 430, 430), (430, H - 430), (W - 430, H - 430)):
        p.d.ellipse([p.s(cx - 470), p.s(cy - 470), p.s(cx + 470), p.s(cy + 470)], fill=CREAM)
        p.rosette(cx, cy, 440, 400, GREEN_INK, petals=28, width=4)
        p.rosette(cx, cy, 360, 335, GREEN, petals=36, width=3)
        p.text_at(cx, cy + 10, "100", p.font(SERIF, 420), GREEN_INK)

    p.border(((660, 1), (672, 1)), GREEN_DIM)

    cx, cy = W / 2, H / 2 - 60
    p.rosette(cx, cy, 400, 350, GREEN, petals=32, width=3)
    p.rosette(cx, cy, 330, 300, GOLD, petals=48, width=2)
    r = 200
    p.d.ellipse([p.s(cx - r), p.s(cy - r), p.s(cx + r), p.s(cy + r)],
                outline=CREAM, width=int(30 * p.ss))
    p.text_at(cx, cy, "OG", p.font(SERIF, 150), GOLD)
    p.arc_text(cx, cy, 440, "ONE HUNDRED DOLLARS", p.font(SERIF, 56), CREAM, 195, 345)

    p.lattice_band(1660, 1770, GREEN_DIM, waves=30, strands=16, width=2)
    p.text_at(W / 2, 1900, "ONE HUNDRED DOLLARS", p.font(SERIF, 88), GOLD, tracking=24)
    p.patron_stars(W / 2, 2030)
    p.serials("OG 0.001% 100", size=48, spots=[(W / 2 - 600, 1150), (W / 2 + 300, 1150)])


# ─────────────────────────────────────────────────────────────────────────
# 06 · Signature Plate — the signing ceremony, facsimile at press scale
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_signature_plate(p):
    ink, ink_dim, proof_gold = GREEN_INK, "#57705f", "#8a6d2a"
    p.hatch(120, 120, W - 120, H - 120, 45, 16, "#b9b29a", width=3)
    p.microprint(88, ink_dim, size=16)
    p.microprint(H - 98, ink_dim, size=16)
    for cx, cy in ((300, 300), (W - 300, 300), (300, H - 300), (W - 300, H - 300)):
        p.rosette(cx, cy, 190, 158, ink, petals=16, width=5)
        p.rosette(cx, cy, 132, 112, ink_dim, petals=30, width=3)
    p.lattice_band(1540, 1640, ink_dim, waves=26, strands=14, width=3)
    p.border(((56, 5), (72, 2)), ink)

    p.d.rounded_rectangle([p.s(620), p.s(80), p.s(W - 620), p.s(260)], radius=36, fill=ink)
    p.text_at(W / 2, 170, "SIGNING CEREMONY \u00b7 OMACOM FOUNDATION",
              p.font(SERIF, 44), CREAM, tracking=12)
    p.text_at(W / 2, 980, "D. H. Hansson", p.font(SERIF_IT, 420), ink)
    p.d.line([p.s(320), p.s(1290), p.s(W - 320), p.s(1290)], fill=proof_gold, width=int(8 * p.ss))
    p.d.line([p.s(320), p.s(1312), p.s(W - 320), p.s(1312)], fill=proof_gold, width=int(3 * p.ss))
    p.text_at(W / 2, 1420, "BENEVOLENT DICTATOR FOR LIFE", p.font(SERIF, 64), proof_gold, tracking=22)

    p.d.ellipse([p.s(W - 640 - 280), p.s(760 - 280), p.s(W - 640 + 280), p.s(760 + 280)], fill=ink)
    p.rosette(W - 640, 760, 226, 196, RED, petals=22, width=5)
    p.arc_text(W - 640, 760, 252, "NOTARY OF PATRONS", p.font(SERIF, 32), RED, 195, 345)
    p.star(W - 640, 760, 78, RED)

    p.d.rounded_rectangle([p.s(760), p.s(1810), p.s(W / 2 - 240), p.s(2080)], radius=40, fill=ink)
    p.text_at(W / 2 - 750, 1930, "you@omarchy", p.font(SERIF_IT, 140), CREAM)
    p.text_at(W / 2 - 750, 2038, "PATRON OF THE ARTS", p.font(SERIF, 36), "#8f9a85", tracking=8)
    p.d.rounded_rectangle([p.s(W / 2 + 180), p.s(1790), p.s(W - 560), p.s(2090)], radius=40, fill=ink)
    p.text_at(W / 2 + 750, 1930, "0.001%", p.font(MONO_BOLD, 120), RED)
    p.text_at(W / 2 + 750, 2048, "THE REMAINDER", p.font(SERIF, 36), "#8f9a85", tracking=8)


# ─────────────────────────────────────────────────────────────────────────
# 07 · Serial Strip — the numbering plate, diagonal cream band
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_serial_strip(p):
    p.rosette(330, 330, 260, 225, GREEN, petals=20, width=3)
    p.rosette(W - 330, H - 330, 260, 225, GREEN, petals=20, width=3)

    # Diagonal cream band through the frame center.
    ang = -14.0
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    cxx, cyy = W / 2, H / 2
    half_w = 330
    far = W
    band = [
        (cxx + dx * far + nx * half_w, cyy + dy * far + ny * half_w),
        (cxx + dx * far - nx * half_w, cyy + dy * far - ny * half_w),
        (cxx - dx * far - nx * half_w, cyy - dy * far - ny * half_w),
        (cxx - dx * far + nx * half_w, cyy - dy * far + ny * half_w),
    ]
    p.d.polygon([(p.s(x), p.s(y)) for x, y in band], fill=CREAM)
    for off, wd in ((half_w + 18, 8), (half_w + 40, 3)):
        edge = [
            (cxx + dx * far + nx * off, cyy + dy * far + ny * off),
            (cxx - dx * far + nx * off, cyy - dy * far + ny * off),
        ]
        p.d.line([(p.s(x), p.s(y)) for x, y in edge], fill=GREEN, width=int(wd * p.ss))
        edge = [
            (cxx + dx * far - nx * off, cyy + dy * far - ny * off),
            (cxx - dx * far - nx * off, cyy - dy * far - ny * off),
        ]
        p.d.line([(p.s(x), p.s(y)) for x, y in edge], fill=GREEN, width=int(wd * p.ss))

    # Serial number printed along the band, in serial red.
    p.text_along(cxx, cyy - 90, ang, "OG 0.001% 10B", p.font(MONO_BOLD, 170), RED)
    p.text_along(cxx, cyy + 130, ang, "OG 0.001% 10B", p.font(MONO_BOLD, 90), GREEN_INK)
    micro = "OG 0.001% \u00b7 ELITE CAPITAL \u00b7 PUBLIC CODE \u00b7 " * 4
    p.text_along(cxx, cyy - 250, ang, micro, p.font(MONO, 34), GREEN_INK)
    p.text_along(cxx, cyy + 255, ang, micro, p.font(MONO, 34), GREEN_INK)

    p.text_at(200, 190, "SERIAL CONTROL STRIP", p.font(SERIF, 44), CREAM, anchor="lm", tracking=10)
    p.text_at(W - 200, H - 190, "EVERY PATRON NUMBERED \u00b7 NONE FORGOTTEN",
              p.font(SERIF, 36), GREEN, anchor="rm", tracking=8)
    for x, y in ((200, H - 190), (W - 200, 190)):
        p.crosshair(x, y, 40, GREEN_DIM, width=3)


# ─────────────────────────────────────────────────────────────────────────
# 08 · Inverse Cream Note — the paper proof, ink on cream
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_inverse_cream(p):
    ink, ink_dim = GREEN_INK, "#57705f"
    p.border(((56, 7), (72, 2), (102, 4)), ink)
    p.microprint(86, ink_dim, size=15)
    p.microprint(H - 96, ink_dim, size=15)
    p.text_at(W / 2, 168, "THE OLIGARCHY \u00b7 PUBLIC CODE \u00b7 EXPENSIVE PATRONS",
              p.font(SERIF, 42), ink_dim, tracking=10)
    p.lattice_band(960, 1090, ink_dim, waves=30, strands=18, width=4)

    for cx, cy in ((300, 300), (W - 300, 300), (300, H - 300), (W - 300, H - 300)):
        p.d.ellipse([p.s(cx - 205), p.s(cy - 205), p.s(cx + 205), p.s(cy + 205)], fill=ink)
        p.rosette(cx, cy, 186, 156, CREAM, petals=14, width=4)
        p.rosette(cx, cy, 130, 110, "#8f9a85", petals=28, width=3)
        p.text_at(cx, cy, "0", p.font(SERIF, 150), CREAM)

    p.o_medallion(W / 2, 1150, ring=ink, green=ink, dim=ink_dim, gold="#a8842e",
                  caption_top="OMACOM FOUNDATION NOTE", caption_bottom="ZERO DOLLARS")
    p.d.rounded_rectangle([p.s(560), p.s(1660), p.s(W - 560), p.s(1958)], radius=48, fill=ink)
    p.text_at(W / 2, 1772, "ZERO DOLLARS", p.font(SERIF, 112), CREAM, tracking=28)
    p.text_at(W / 2, 1888, "SEVERAL BILLIONAIRES", p.font(SERIF_IT, 52), GOLD, tracking=12)
    p.patron_stars(W / 2, 1990, ink)
    p.serials("OG 0.001% $0", RED, spots=[(430, 470), (W - 950, 1560)])

    sig, cap = p.font(SERIF_IT, 52), p.font(SERIF, 26)
    p.text_at(560, 2140, "D. H. Hansson", sig, ink)
    p.text_at(560, 2210, "BENEVOLENT DICTATOR FOR LIFE", cap, ink_dim, tracking=4)
    p.text_at(W - 560, 2140, "you@omarchy", sig, ink)
    p.text_at(W - 560, 2210, "PATRON OF THE ARTS", cap, ink_dim, tracking=4)
    p.text_at(W / 2, 2210, "SERIES 2026 \u00b7 PROOF", cap, ink_dim, tracking=6)


# ─────────────────────────────────────────────────────────────────────────
# 09 · Gold Seal Minimal — plate 09, the vault: near-black, one seal
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_gold_seal_minimal(p):
    cx, cy = W / 2, H / 2
    p.rays(cx, cy, 340, 700, "#a5853e", count=72, width=12)
    p.d.ellipse([p.s(cx - 660), p.s(cy - 660), p.s(cx + 660), p.s(cy + 660)], fill=GOLD)
    p.d.ellipse([p.s(cx - 560), p.s(cy - 560), p.s(cx + 560), p.s(cy + 560)], fill=BG_DEEP)
    p.d.ellipse([p.s(cx - 660), p.s(cy - 660), p.s(cx + 660), p.s(cy + 660)],
                outline=GOLD, width=int(26 * p.ss))
    p.d.ellipse([p.s(cx - 620), p.s(cy - 620), p.s(cx + 620), p.s(cy + 620)],
                outline=GOLD, width=int(5 * p.ss))
    p.arc_text(cx, cy, 748, "OMACOM", p.font(SERIF, 128), GOLD, 205, 335)
    p.arc_text(cx, cy, 756, "2026", p.font(SERIF, 90), CREAM, 145, 35, flip=True)
    p.dot_ring(cx, cy, 540, GOLD, count=28, dr=8)
    p.dot_ring(cx, cy, 400, "#6d5a2e", count=16, dr=6)
    p.d.ellipse([p.s(cx - 250), p.s(cy - 250), p.s(cx + 250), p.s(cy + 250)], fill=CREAM)
    p.star(cx, cy, 260, GOLD)
    p.d.text((p.s(200), p.s(120)), "09", font=p.font(MONO_BOLD, 56), fill=GREEN_DIM)

    m = 140
    arm = 90
    for x0, y0, hx, vy in ((m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)):
        p.d.line([p.s(x0), p.s(y0), p.s(x0 + arm * hx), p.s(y0)], fill=CREAM, width=int(5 * p.ss))
        p.d.line([p.s(x0), p.s(y0), p.s(x0), p.s(y0 + arm * vy)], fill=CREAM, width=int(5 * p.ss))
    p.text_at(W / 2, H - 170, "IN PATRONS WE TRUST \u00b7 IN PATRONS WE TRUST",
              p.font(SERIF_REG, 30), "#8a7136", tracking=30)


# ─────────────────────────────────────────────────────────────────────────
def build_unlock(size=512):
    """Lock-screen glyph: engraved 1M rosette on transparency."""
    p = Plate(size, size, BG_DEEP, ss=2)
    p.img = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
    p.d = ImageDraw.Draw(p.img)
    cx = size / 2
    p.rosette(cx, cx, 215, 185, CREAM, petals=14, width=3)
    p.rosette(cx, cx, 150, 128, GREEN, petals=28, width=2)
    r = 92
    p.d.ellipse([p.s(cx - r), p.s(cx - r), p.s(cx + r), p.s(cx + r)],
                outline=CREAM, width=int(10 * p.ss))
    p.text_at(cx, cx, "1M", p.font(SERIF, 74), CREAM)
    return p.img.resize((size, size), Image.LANCZOS)


# Plate tones: a luminance ladder so the contact sheet reads dark / mid / bright.
scene_medallion_macro.bg = "#182720"
scene_guilloche_field.bg = "#1d2a22"
scene_seal_of_stars.bg = "#122015"
scene_corner_denomination.bg = "#2c3a2a"
scene_signature_plate.bg = "#e2dcc6"
scene_inverse_cream.bg = CREAM


def main():
    os.makedirs("backgrounds", exist_ok=True)
    hero_fn = SCENES[0][1]
    for i, (slug, fn) in enumerate(SCENES, 1):
        p = Plate(W, H, getattr(fn, "bg", BG))
        fn(p)
        path = f"backgrounds/{i}-{slug}.jpg"
        p.save(path, quality=90)
        print(f"saved {path}")
        if fn is hero_fn:
            p.img.resize((W, H), Image.LANCZOS).save("backgrounds/legal-tender.png")
            print("saved backgrounds/legal-tender.png")
    build_unlock().save("unlock.png")
    print("saved unlock.png")


if __name__ == "__main__":
    main()
