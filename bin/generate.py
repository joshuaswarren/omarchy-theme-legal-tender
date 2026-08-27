#!/usr/bin/env python3
"""Render the nine Legal Tender backgrounds natively at 3840x2160 (16:9).

Nine distinct engravings of the Omacom Foundation Note, one per plate:
full note, medallion macro, guilloche field, seal of stars, corner
denomination, signature plate, serial strip, inverse cream note, and a
minimal gold seal. Also writes the canonical hero and the unlock glyph.

Every scene composes onto a 3456x1944 content canvas (also 16:9) that is
then matted onto the full 3840x2160 wallpaper at a 192/108px inset. That
inset is exactly the engraving's 5% safe area (x 192..3648, y 108..2052),
so anything a scene draws inside the content canvas structurally lands
inside the safe area — Plate's runtime checks (engrave.py) give a second,
independent numeric guarantee for text, serials, arcs, and borders.

The scenes were originally tuned for a 3840x2560 (3:2) canvas. X()/Y()/SZ()
below port each absolute coordinate from that old canvas onto the new one
by a fixed per-axis scale, preserving the approved composition's relative
layout and non-collisions rather than stretching or center-cropping pixels.

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

# Content canvas: 16:9, inset within the final wallpaper by the safe margin.
W, H = 3456, 1944
# Final wallpaper canvas and the inset that centers the content canvas in it.
FULL_W, FULL_H = 3840, 2160
MARGIN_X, MARGIN_Y = (FULL_W - W) // 2, (FULL_H - H) // 2  # 192, 108

# The scenes below were designed for this now-retired 3:2 canvas.
OLD_W, OLD_H = 3840, 2560
XS, YS = W / OLD_W, H / OLD_H  # 0.9, 0.759375


def X(v):
    """Port an absolute X position/offset from the old 3:2 canvas."""
    return v * XS


def Y(v):
    """Port an absolute Y position/offset from the old 3:2 canvas."""
    return v * YS


SZ = Y  # sizes (radii, font points, tracking, tick lengths) use the Y scale

SCENES = []  # (slug, builder) filled by the decorators below


def scene(fn):
    SCENES.append((fn.__name__.replace("scene_", "").replace("_", "-"), fn))
    return fn


# ─────────────────────────────────────────────────────────────────────────
# 01 · Foundation Note — the complete bill, edge to edge
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_foundation_note(p):
    # A classic note hierarchy: header, seal, value, patrons, signatures.
    # Nothing crosses the medallion or denomination plaque.
    p.border(((42, 4), (56, 1), (82, 2)))
    p.microprint(58, x0=110, x1=W - 110, clip=True)
    p.microprint(H - 64, x0=110, x1=W - 110, clip=True)
    p.text_at(
        W / 2,
        112,
        "THE OLIGARCHY · FREE SOFTWARE · EXPENSIVE PATRONS",
        p.font(SERIF, 34),
        GREEN_BRIGHT,
        tracking=8,
    )

    # Four small value seals stay in the corners and out of the copy.
    for cx, cy in (
        (250, 250),
        (W - 250, 250),
        (250, H - 250),
        (W - 250, H - 250),
    ):
        p.d.ellipse(
            [p.s(cx - 132), p.s(cy - 132), p.s(cx + 132), p.s(cy + 132)],
            fill=CREAM,
        )
        p.rosette(cx, cy, 122, 102, GREEN_INK, petals=14, width=4)
        p.rosette(cx, cy, 86, 72, GREEN, petals=28, width=3)
        p.text_at(cx, cy, "1M", p.font(SERIF, 82), GREEN_INK)

    # The seal owns the center. No horizontal band cuts through it.
    cx, cy = W / 2, 760
    p.d.ellipse(
        [p.s(cx - 220), p.s(cy - 220), p.s(cx + 220), p.s(cy + 220)],
        fill=CREAM,
    )
    p.o_medallion(cx, cy, scale=0.56)

    # Serials sit in open fields, away from the seal and signatures.
    p.serials(
        "OG 0.001% 1M",
        size=34,
        spots=[(420, 410), (W - 760, 1200)],
    )

    # A single value plaque below the complete seal.
    p.d.rounded_rectangle(
        [p.s(590), p.s(1360), p.s(W - 590), p.s(1535)],
        radius=34,
        fill=CREAM,
    )
    p.text_at(
        W / 2,
        1448,
        "ONE MILLION DOLLARS",
        p.font(SERIF, 86),
        GREEN_INK,
        tracking=18,
    )
    p.patron_stars(W / 2, 1605, GOLD)

    sig, cap = p.font(SERIF_IT, 42), p.font(SERIF, 21)
    p.text_at(620, 1740, "D. H. Hansson", sig, CREAM)
    p.d.line([p.s(430), p.s(1772), p.s(810), p.s(1772)], fill=GREEN, width=4)
    p.text_at(620, 1802, "BENEVOLENT DICTATOR FOR LIFE", cap, GREEN_BRIGHT, tracking=3)
    p.text_at(W - 620, 1740, "you@omarchy", sig, CREAM)
    p.d.line([p.s(W - 810), p.s(1772), p.s(W - 430), p.s(1772)], fill=GREEN, width=4)
    p.text_at(W - 620, 1802, "PATRON OF THE ARTS", cap, GREEN_BRIGHT, tracking=3)
    p.text_at(W / 2, 1778, "SERIES 2026", cap, GREEN, tracking=5)


# ─────────────────────────────────────────────────────────────────────────
# 02 · Medallion Macro — the O at press scale, cropped by the frame
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_medallion_macro(p):
    p.border(((52, 2), (70, 1)), GREEN_DIM)
    p.text_at(W / 2, 160, "FOUNDATION SEAL", p.font(SERIF, 72), CREAM, tracking=18)

    cx, cy = W / 2, 960
    p.rosette(cx, cy, 720, 660, GREEN, petals=40, width=5)
    p.rosette(cx, cy, 620, 570, GOLD, petals=56, width=3)
    p.radial(cx, cy, 390, 610, GREEN_DIM, step=4, width=2)
    p.d.ellipse([p.s(cx - 390), p.s(cy - 390), p.s(cx + 390), p.s(cy + 390)],
                fill=CREAM)
    p.d.ellipse([p.s(cx - 300), p.s(cy - 300), p.s(cx + 300), p.s(cy + 300)],
                fill=BG_DEEP)
    p.d.ellipse([p.s(cx - 355), p.s(cy - 355), p.s(cx + 355), p.s(cy + 355)],
                outline=GREEN, width=8)
    p.d.ellipse([p.s(cx - 300), p.s(cy - 300), p.s(cx + 300), p.s(cy + 300)],
                outline=CREAM, width=10)

    p.text_at(W / 2, H - 180, "IN PATRONS WE TRUST", p.font(SERIF, 56), GOLD,
              tracking=14)
    p.text_at(230, 160, "PLATE 02", p.font(MONO_BOLD, 34), GREEN_BRIGHT, anchor="la")
    p.text_at(W - 230, H - 180, "OG 0.001%", p.font(MONO_BOLD, 34), RED, anchor="ra")
    for x, y in ((150, 150), (W - 150, 150), (150, H - 150), (W - 150, H - 150)):
        p.crosshair(x, y, 34, CREAM, width=3)


# ─────────────────────────────────────────────────────────────────────────
# 03 · Guilloche Field — full-frame lathe work, red treasury roundel
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_guilloche_field(p):
    p.text_at(300, 220, "SECURITY THREAD", p.font(SERIF, 76), CREAM, anchor="lm",
              tracking=12)
    p.text_at(300, 300, "PUBLIC CODE · PLATE 03", p.font(MONO_BOLD, 32), GREEN_BRIGHT,
              anchor="lm")

    for y0, y1 in ((430, 580), (820, 970), (1210, 1360)):
        p.d.rounded_rectangle([p.s(260), p.s(y0), p.s(W - 260), p.s(y1)],
                              radius=28, fill=CREAM)
        p.lattice_band(y0 + 18, y1 - 18, GREEN_INK, waves=12, strands=5, width=4)

    seal_x, seal_y = W - 690, 1650
    p.d.ellipse([p.s(seal_x - 260), p.s(seal_y - 260),
                 p.s(seal_x + 260), p.s(seal_y + 260)],
                fill=BG_DEEP, outline=RED, width=14)
    p.d.ellipse([p.s(seal_x - 210), p.s(seal_y - 210),
                 p.s(seal_x + 210), p.s(seal_y + 210)],
                outline=RED, width=5)
    p.text_at(seal_x, seal_y, "OG", p.font(SERIF, 150), CREAM)
    p.text_at(380, 1570, "THREE THREADS", p.font(SERIF, 86), GOLD, anchor="lm")
    p.text_at(380, 1675, "ONE PUBLIC LEDGER", p.font(SERIF, 48), GREEN_BRIGHT,
              anchor="lm", tracking=8)
    p.text_at(380, 1775, "DO NOT PHOTOCOPY", p.font(MONO_BOLD, 30), RED, anchor="lm")


# ─────────────────────────────────────────────────────────────────────────
# 04 · Seal of Stars — the great seal, sunburst behind
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_seal_of_stars(p):
    cx, cy = 1180, 990
    p.rays(cx, cy, 620, 860, GREEN_DIM, count=48, width=5)
    p.d.ellipse([p.s(cx - 610), p.s(cy - 610), p.s(cx + 610), p.s(cy + 610)],
                fill=GOLD)
    p.d.ellipse([p.s(cx - 520), p.s(cy - 520), p.s(cx + 520), p.s(cy + 520)],
                fill=BG_DEEP)
    for i in range(8):
        a = math.radians(-90 + i * 45)
        p.star(cx + 395 * math.cos(a), cy + 395 * math.sin(a), 58, CREAM)
    p.d.ellipse([p.s(cx - 235), p.s(cy - 235), p.s(cx + 235), p.s(cy + 235)],
                fill=CREAM)
    p.d.ellipse([p.s(cx - 235), p.s(cy - 235), p.s(cx + 235), p.s(cy + 235)],
                outline=GREEN_INK, width=48)
    p.star(cx, cy, 135, GOLD)

    tx = 2180
    p.text_at(tx, 610, "THE GREAT", p.font(SERIF, 86), CREAM, anchor="lm", tracking=10)
    p.text_at(tx, 735, "SEAL", p.font(SERIF, 150), GOLD, anchor="lm", tracking=12)
    p.d.line([p.s(tx), p.s(820), p.s(W - 260), p.s(820)], fill=GREEN, width=6)
    p.text_at(tx, 930, "EIGHT FOUNDING PATRONS", p.font(SERIF, 44), GREEN_BRIGHT,
              anchor="lm", tracking=7)
    p.text_at(tx, 1010, "PLUS TWO MORE", p.font(SERIF, 44), GREEN_BRIGHT,
              anchor="lm", tracking=7)
    p.text_at(tx, 1170, "OMACOM FOUNDATION", p.font(SERIF, 56), CREAM, anchor="lm",
              tracking=8)
    p.text_at(tx, 1260, "SERIES 2026", p.font(MONO_BOLD, 34), RED, anchor="lm")
    p.serials("OG 0.001% ★", size=30, spots=[(260, 220), (W - 720, H - 240)])


# ─────────────────────────────────────────────────────────────────────────
# 05 · Corner Denomination — four giant engraved 100s
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_corner_denomination(p):
    p.border(((52, 3), (70, 1)), GREEN_DIM)
    p.text_at(240, 190, "VALUE PLATE 05", p.font(MONO_BOLD, 34), GREEN_BRIGHT,
              anchor="la")

    p.d.rounded_rectangle([p.s(280), p.s(360), p.s(1660), p.s(1570)],
                          radius=70, fill=CREAM)
    p.text_at(970, 910, "100", p.font(SERIF, 520), GREEN_INK)
    p.text_at(970, 1370, "ONE HUNDRED", p.font(SERIF, 58), GREEN, tracking=12)

    cx, cy = 2580, 850
    p.d.ellipse([p.s(cx - 390), p.s(cy - 390), p.s(cx + 390), p.s(cy + 390)],
                fill=CREAM)
    p.rosette(cx, cy, 350, 310, GREEN_INK, petals=28, width=5)
    p.rosette(cx, cy, 270, 240, GOLD, petals=40, width=3)
    p.d.ellipse([p.s(cx - 150), p.s(cy - 150), p.s(cx + 150), p.s(cy + 150)],
                fill=BG_DEEP)
    p.text_at(cx, cy, "OG", p.font(SERIF, 105), GOLD)

    p.text_at(2580, 1350, "ONE HUNDRED DOLLARS", p.font(SERIF, 66), GOLD,
              tracking=12)
    p.patron_stars(2580, 1480, CREAM)
    p.text_at(2580, 1630, "PUBLIC CODE · PRIVATE WEALTH", p.font(SERIF, 34),
              GREEN_BRIGHT, tracking=7)
    p.serials("OG 0.001% 100", size=34, spots=[(2050, 350), (W - 720, H - 260)])


# ─────────────────────────────────────────────────────────────────────────
# 06 · Signature Plate — the signing ceremony, facsimile at press scale
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_signature_plate(p):
    ink, ink_dim, proof_gold = GREEN_INK, "#57705f", "#8a6d2a"
    p.border(((52, 5), (70, 2)), ink)
    p.microprint(58, ink_dim, size=13, x0=110, x1=W - 110, clip=True)
    p.microprint(H - 64, ink_dim, size=13, x0=110, x1=W - 110, clip=True)
    p.text_at(W / 2, 150, "THE SIGNING DESK", p.font(SERIF, 64), ink, tracking=14)
    p.text_at(W / 2, 226, "OMACOM FOUNDATION · SERIES 2026",
              p.font(MONO_BOLD, 30), ink_dim, tracking=6)

    # The signing book: one blank signature line, waiting.
    p.d.rounded_rectangle([p.s(640), p.s(430), p.s(W - 640), p.s(1560)],
                          radius=30, fill=CREAM, outline=ink, width=8)
    p.text_at(1180, 620, "SIGN HERE", p.font(SERIF, 46), ink_dim, tracking=9)
    p.d.line([p.s(980), p.s(1180), p.s(2900), p.s(1180)], fill=ink, width=10)
    p.text_at(980, 1218, "BENEVOLENT DICTATOR FOR LIFE",
              p.font(SERIF, 26), ink_dim, anchor="la", tracking=5)
    p.text_at(2900, 1218, "0.001%", p.font(MONO_BOLD, 26), RED, anchor="ra")

    # Notary seal, pressed at an angle over the book's corner.
    seal = Image.new("RGBA", (520 * p.ss, 520 * p.ss), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seal)
    sd.ellipse([20, 20, 500 * p.ss - 20, 500 * p.ss - 20], fill=ink)
    sd.ellipse([int(48 * p.ss), int(48 * p.ss), int(472 * p.ss), int(472 * p.ss)],
               outline=RED, width=int(12 * p.ss))
    sd.ellipse([int(76 * p.ss), int(76 * p.ss), int(444 * p.ss), int(444 * p.ss)],
               outline=RED, width=int(4 * p.ss))
    sd.regular_polygon((260 * p.ss, 260 * p.ss, 95 * p.ss), 5,
                       rotation=180, fill=RED)
    seal = seal.rotate(-14, resample=Image.BICUBIC, expand=True)
    p.img.paste(seal, (int(p.s(2540)), int(p.s(1080))), seal)

    # Fountain pen silhouette crossing the page's top-right corner.
    pen = Image.new("RGBA", (1250 * p.ss, 420 * p.ss), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pen)
    pd.regular_polygon((170 * p.ss, 210 * p.ss, 54 * p.ss), 3,
                       rotation=90, fill=GOLD)
    pd.polygon(
        [(200 * p.ss, 150 * p.ss), (1060 * p.ss, 210 * p.ss),
         (1060 * p.ss, 270 * p.ss), (200 * p.ss, 270 * p.ss)],
        fill=ink,
    )
    pd.rectangle([1060 * p.ss, 218 * p.ss, 1180 * p.ss, 262 * p.ss], fill=GOLD)
    pen = pen.rotate(24, resample=Image.BICUBIC, expand=True)
    p.img.paste(pen, (int(p.s(2180)), int(p.s(250))), pen)

    p.text_at(W / 2, H - 220, "LEFT BLANK FOR THE NEXT PATRON",
              p.font(SERIF, 44), ink, tracking=11)
    p.text_at(W / 2, H - 145, "NOTARY OF PATRONS · INK DRIES FAST",
              p.font(MONO_BOLD, 26), RED, tracking=5)


# ─────────────────────────────────────────────────────────────────────────
# 07 · Serial Strip — the numbering plate, diagonal cream band
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_serial_strip(p):
    p.border(((52, 3), (70, 1)), GREEN_DIM)
    p.text_at(W / 2, 250, "SERIAL NUMBER PLATE", p.font(SERIF, 82), CREAM,
              tracking=16)

    p.d.rounded_rectangle([p.s(320), p.s(620), p.s(W - 320), p.s(1270)],
                          radius=54, fill=CREAM)
    seal_x, seal_y = 820, 945
    p.d.ellipse([p.s(seal_x - 230), p.s(seal_y - 230),
                 p.s(seal_x + 230), p.s(seal_y + 230)],
                fill=BG_DEEP, outline=GREEN, width=14)
    p.rosette(seal_x, seal_y, 190, 165, GOLD, petals=24, width=4)
    p.text_at(seal_x, seal_y, "OG", p.font(SERIF, 94), GOLD)

    p.text_at(2050, 855, "OG 0.001% 10B", p.font(MONO_BOLD, 132), RED)
    p.text_at(2050, 1035, "REGISTERED TO THE PEOPLE", p.font(SERIF, 48), GREEN_INK,
              tracking=10)
    p.text_at(2050, 1135, "ZERO PRICE · PUBLIC CODE", p.font(MONO_BOLD, 32),
              GREEN, tracking=5)

    p.text_at(W / 2, 1510, "EVERY PATRON NUMBERED", p.font(SERIF, 60), GOLD,
              tracking=14)
    p.text_at(W / 2, 1610, "NONE FORGOTTEN", p.font(SERIF, 36), GREEN_BRIGHT,
              tracking=10)
    p.patron_stars(W / 2, 1740, GOLD)
    p.text_at(W / 2, 1840, "SERIES 2026", p.font(MONO_BOLD, 28), RED, tracking=5)


# ─────────────────────────────────────────────────────────────────────────
# 08 · Inverse Cream Note — the paper proof, ink on cream
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_inverse_cream(p):
    ink, ink_dim = GREEN_INK, "#57705f"
    p.border(((52, 6), (70, 2), (88, 2)), ink)
    p.microprint(58, ink_dim, size=13, x0=110, x1=W - 110, clip=True)
    p.microprint(H - 64, ink_dim, size=13, x0=110, x1=W - 110, clip=True)
    p.text_at(240, 180, "PROOF PLATE 08", p.font(MONO_BOLD, 34), ink_dim, anchor="la")

    p.text_at(260, 720, "ZERO", p.font(SERIF, 430), ink, anchor="lm")
    p.text_at(260, 1110, "DOLLARS", p.font(SERIF, 300), ink, anchor="lm")
    p.text_at(290, 1320, "THE PRICE IS ZERO", p.font(SERIF, 52), GOLD, anchor="lm",
              tracking=10)
    p.text_at(290, 1420, "THE CODE IS PUBLIC", p.font(SERIF, 42), ink_dim,
              anchor="lm", tracking=8)

    cx, cy = 2740, 820
    p.d.ellipse([p.s(cx - 380), p.s(cy - 380), p.s(cx + 380), p.s(cy + 380)],
                fill=ink)
    p.d.ellipse([p.s(cx - 300), p.s(cy - 300), p.s(cx + 300), p.s(cy + 300)],
                fill=CREAM)
    p.d.ellipse([p.s(cx - 225), p.s(cy - 225), p.s(cx + 225), p.s(cy + 225)],
                outline=ink, width=28)
    p.star(cx, cy, 130, GOLD)
    p.text_at(cx, 1320, "SEVERAL BILLIONAIRES", p.font(SERIF, 44), ink,
              tracking=8)
    p.patron_stars(cx, 1430, ink)

    p.d.line([p.s(300), p.s(1660), p.s(W - 300), p.s(1660)], fill=ink_dim, width=5)
    p.text_at(820, 1770, "D. H. Hansson", p.font(SERIF_IT, 48), ink)
    p.text_at(W - 820, 1770, "you@omarchy", p.font(SERIF_IT, 48), ink)
    p.text_at(W / 2, 1770, "0.001%", p.font(MONO_BOLD, 48), RED)
    p.text_at(W / 2, 1870, "SERIES 2026 · CREAM PROOF", p.font(SERIF, 25), ink_dim,
              tracking=6)


# ─────────────────────────────────────────────────────────────────────────
# 09 · Gold Seal Minimal — plate 09, the vault: near-black, one seal
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_gold_seal_minimal(p):
    cx, cy = W / 2, H / 2
    p.rays(cx, cy, SZ(340), SZ(700), "#a5853e", count=72, width=12)
    p.d.ellipse([p.s(cx - SZ(660)), p.s(cy - SZ(660)), p.s(cx + SZ(660)), p.s(cy + SZ(660))],
                fill=GOLD)
    p.d.ellipse([p.s(cx - SZ(560)), p.s(cy - SZ(560)), p.s(cx + SZ(560)), p.s(cy + SZ(560))],
                fill=BG_DEEP)
    p.d.ellipse([p.s(cx - SZ(660)), p.s(cy - SZ(660)), p.s(cx + SZ(660)), p.s(cy + SZ(660))],
                outline=GOLD, width=int(26 * p.ss))
    p.d.ellipse([p.s(cx - SZ(620)), p.s(cy - SZ(620)), p.s(cx + SZ(620)), p.s(cy + SZ(620))],
                outline=GOLD, width=int(5 * p.ss))
    p.arc_text(cx, cy, SZ(748), "OMACOM", p.font(SERIF, SZ(128)), GOLD, 205, 335)
    p.arc_text(cx, cy, SZ(756), "2026", p.font(SERIF, SZ(90)), CREAM, 145, 35, flip=True)
    p.dot_ring(cx, cy, SZ(540), GOLD, count=28, dr=8)
    p.dot_ring(cx, cy, SZ(400), "#6d5a2e", count=16, dr=6)
    p.d.ellipse([p.s(cx - SZ(250)), p.s(cy - SZ(250)), p.s(cx + SZ(250)), p.s(cy + SZ(250))],
                fill=CREAM)
    p.star(cx, cy, SZ(260), GOLD)
    p.text_at(X(200), Y(120), "09", p.font(MONO_BOLD, SZ(56)), GREEN_DIM, anchor="la")

    m = SZ(140)
    arm = SZ(90)
    for x0, y0, hx, vy in ((m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)):
        p.d.line([p.s(x0), p.s(y0), p.s(x0 + arm * hx), p.s(y0)], fill=CREAM, width=int(5 * p.ss))
        p.d.line([p.s(x0), p.s(y0), p.s(x0), p.s(y0 + arm * vy)], fill=CREAM, width=int(5 * p.ss))
    p.text_at(W / 2, H - Y(170), "IN PATRONS WE TRUST \u00b7 IN PATRONS WE TRUST",
              p.font(SERIF_REG, SZ(30)), "#8a7136", tracking=X(30))


# ─────────────────────────────────────────────────────────────────────────
def build_unlock(size=512):
    """Lock-screen glyph: engraved 1M rosette on transparency."""
    p = Plate(size, size, BG_DEEP, ss=2, safe_check=False)
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
        bg = getattr(fn, "bg", BG)
        p = Plate(W, H, bg, origin=(MARGIN_X, MARGIN_Y))
        fn(p)
        content = p.img.resize((p.w, p.h), Image.LANCZOS)
        canvas = Image.new("RGB", (FULL_W, FULL_H), bg)
        canvas.paste(content, (MARGIN_X, MARGIN_Y))
        path = f"backgrounds/{i}-{slug}.jpg"
        canvas.save(path, "JPEG", quality=90, optimize=True)
        print(f"saved {path} ({FULL_W}x{FULL_H})")
        if fn is hero_fn:
            canvas.save("backgrounds/legal-tender.png")
            print("saved backgrounds/legal-tender.png")
    build_unlock().save("unlock.png")
    print("saved unlock.png")


if __name__ == "__main__":
    main()
