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
    p.microprint(58)
    p.microprint(H - 64)
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
        (210, 210),
        (W - 210, 210),
        (210, H - 210),
        (W - 210, H - 210),
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
    p.lattice_band(Y(60), Y(240), GREEN_DIM, waves=26, strands=14, width=2)
    p.lattice_band(H - Y(240), H - Y(60), GREEN_DIM, waves=26, strands=14, width=2)
    cx, cy = W / 2, H / 2 + Y(120)
    p.d.ellipse([p.s(cx - SZ(560)), p.s(cy - SZ(560)), p.s(cx + SZ(560)), p.s(cy + SZ(560))],
                fill=CREAM)
    p.rosette(cx, cy, SZ(1620), SZ(1460), GREEN, petals=48, width=5)
    p.rosette(cx, cy, SZ(1500), SZ(1300), GREEN_DIM, petals=56, width=3)
    p.rosette(cx, cy, SZ(1240), SZ(1160), GOLD, petals=72, width=3)
    p.radial(cx, cy, SZ(760), SZ(1240), GREEN, step=3, width=2)

    r = SZ(640)
    p.d.ellipse([p.s(cx - r), p.s(cy - r), p.s(cx + r), p.s(cy + r)],
                outline=CREAM, width=int(120 * p.ss))
    p.d.ellipse([p.s(cx - r - SZ(56)), p.s(cy - r - SZ(56)), p.s(cx + r + SZ(56)), p.s(cy + r + SZ(56))],
                outline=GREEN, width=int(6 * p.ss))
    p.d.ellipse([p.s(cx - r + SZ(56)), p.s(cy - r + SZ(56)), p.s(cx + r - SZ(56)), p.s(cy + r - SZ(56))],
                outline=GREEN, width=int(6 * p.ss))
    p.arc_text(cx, cy, SZ(1250), "OMACOM FOUNDATION", p.font(SERIF, SZ(132)), CREAM, 200, 340)
    p.arc_text(cx, cy, SZ(1046), "IN PATRONS WE TRUST", p.font(SERIF, SZ(96)), GOLD, 150, 30,
               flip=True)

    for x, y in ((X(160), Y(160)), (W - X(160), Y(160)),
                 (X(160), H - Y(160)), (W - X(160), H - Y(160))):
        p.crosshair(x, y, SZ(46), CREAM, width=3)
    plate = p.font(MONO, SZ(40))
    p.text_at(X(230), Y(120), "PLATE 02", plate, GREEN_BRIGHT, anchor="la")
    p.text_at(X(230), H - Y(168), "SERIES 2026", plate, GREEN_BRIGHT, anchor="la")
    p.text_at(W - X(430), H - Y(168), "OG 0.001%", p.font(MONO_BOLD, SZ(40)), RED, anchor="la")


# ─────────────────────────────────────────────────────────────────────────
# 03 · Guilloche Field — full-frame lathe work, red treasury roundel
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_guilloche_field(p):
    bands = [
        (Y(90), Y(380), GREEN, 14, 16, 3),
        (Y(430), Y(660), GREEN_DIM, 18, 14, 2),
        (Y(700), Y(1010), GREEN_BRIGHT, 10, 18, 3),
        (Y(1050), Y(1260), GOLD, 22, 12, 2),
        (Y(1300), Y(1610), GREEN, 12, 18, 3),
        (Y(1650), Y(1860), GREEN_DIM, 18, 14, 2),
        (Y(1900), Y(2210), GREEN_BRIGHT, 14, 16, 3),
        (Y(2250), Y(2470), GOLD, 20, 12, 2),
    ]
    cream_bands = ((Y(430), Y(660)), (Y(1650), Y(1860)))
    for y0, y1 in cream_bands:
        p.d.rectangle([0, p.s(y0), p.s(W), p.s(y1)], fill=CREAM)
    bands[1] = (cream_bands[0][0], cream_bands[0][1], GREEN_INK, 18, 14, 3)
    bands[5] = (cream_bands[1][0], cream_bands[1][1], GREEN_INK, 18, 14, 3)
    for y0, y1, col, waves, strands, wd in bands:
        p.lattice_band(y0, y1, col, waves=waves, strands=strands, width=wd)

    cx, cy = W / 2, H / 2
    p.d.ellipse([p.s(cx - SZ(330)), p.s(cy - SZ(330)), p.s(cx + SZ(330)), p.s(cy + SZ(330))],
                outline=RED, width=int(10 * p.ss))
    p.d.ellipse([p.s(cx - SZ(300)), p.s(cy - SZ(300)), p.s(cx + SZ(300)), p.s(cy + SZ(300))],
                outline=RED, width=int(3 * p.ss))
    p.arc_text(cx, cy, SZ(358), "TREASURY OF THE OLIGARCHY", p.font(SERIF, SZ(52)), RED, 195, 345)
    p.arc_text(cx, cy, SZ(362), "SECURITY FIELD", p.font(SERIF, SZ(40)), RED, 15, 165, flip=True)
    p.text_at(cx, cy, "OG", p.font(SERIF, SZ(190)), CREAM_BRIGHT)

    p.text_at(X(200), Y(120), "03", p.font(MONO_BOLD, SZ(56)), CREAM_BRIGHT, anchor="la")
    p.text_at(W / 2, Y(2330), "GUILLOCHE SECURITY FIELD \u00b7 DO NOT PHOTOCOPY",
              p.font(SERIF, SZ(36)), CREAM, tracking=X(10))


# ─────────────────────────────────────────────────────────────────────────
# 04 · Seal of Stars — the great seal, sunburst behind
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_seal_of_stars(p):
    cx, cy = W / 2, H / 2
    p.rays(cx, cy, SZ(1000), SZ(1780), GREEN_DIM, count=72, width=5)
    p.rays(cx, cy, SZ(760), SZ(1100), GREEN, count=36, width=4)

    p.d.ellipse([p.s(cx - SZ(800)), p.s(cy - SZ(800)), p.s(cx + SZ(800)), p.s(cy + SZ(800))],
                fill=GOLD)
    p.d.ellipse([p.s(cx - SZ(690)), p.s(cy - SZ(690)), p.s(cx + SZ(690)), p.s(cy + SZ(690))],
                fill="#0d1812")
    p.d.ellipse([p.s(cx - SZ(800)), p.s(cy - SZ(800)), p.s(cx + SZ(800)), p.s(cy + SZ(800))],
                outline=GOLD, width=int(18 * p.ss))
    p.d.ellipse([p.s(cx - SZ(770)), p.s(cy - SZ(770)), p.s(cx + SZ(770)), p.s(cy + SZ(770))],
                outline=GOLD, width=int(3 * p.ss))
    p.d.ellipse([p.s(cx - SZ(690)), p.s(cy - SZ(690)), p.s(cx + SZ(690)), p.s(cy + SZ(690))],
                outline=GREEN, width=int(4 * p.ss))
    p.arc_text(cx, cy, SZ(800), "OMACOM FOUNDATION", p.font(SERIF, SZ(96)), GOLD, 198, 342)
    p.arc_text(cx, cy, SZ(806), "SERIES 2026", p.font(SERIF, SZ(64)), CREAM, 155, 25, flip=True)

    for i in range(8):
        a = math.radians(-90 + i * 45)
        p.star(cx + SZ(620) * math.cos(a), cy + SZ(620) * math.sin(a), SZ(64), CREAM)
    p.star(cx + SZ(500), cy + SZ(500), SZ(30), GOLD)
    p.star(cx - SZ(500), cy - SZ(500), SZ(30), GOLD)

    r = SZ(330)
    p.d.ellipse([p.s(cx - r), p.s(cy - r), p.s(cx + r), p.s(cy + r)], fill=CREAM)
    p.d.ellipse([p.s(cx - r), p.s(cy - r), p.s(cx + r), p.s(cy + r)],
                outline=GREEN_INK, width=int(58 * p.ss))
    p.star(cx, cy, SZ(190), GOLD)
    p.dot_ring(cx, cy, SZ(655), GREEN, count=8, dr=6)

    p.serials("OG 0.001% \u2605", size=SZ(40), spots=[(X(260), Y(220)), (W - X(700), H - Y(280))])


# ─────────────────────────────────────────────────────────────────────────
# 05 · Corner Denomination — four giant engraved 100s
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_corner_denomination(p):
    for cx, cy in ((X(430), Y(430)), (W - X(430), Y(430)),
                   (X(430), H - Y(430)), (W - X(430), H - Y(430))):
        p.d.ellipse([p.s(cx - SZ(470)), p.s(cy - SZ(470)), p.s(cx + SZ(470)), p.s(cy + SZ(470))],
                    fill=CREAM)
        p.rosette(cx, cy, SZ(440), SZ(400), GREEN_INK, petals=28, width=4)
        p.rosette(cx, cy, SZ(360), SZ(335), GREEN, petals=36, width=3)
        p.text_at(cx, cy + SZ(10), "100", p.font(SERIF, SZ(420)), GREEN_INK)

    p.border(((SZ(660), 1), (SZ(672), 1)), GREEN_DIM)

    cx, cy = W / 2, H / 2 - Y(60)
    p.rosette(cx, cy, SZ(400), SZ(350), GREEN, petals=32, width=3)
    p.rosette(cx, cy, SZ(330), SZ(300), GOLD, petals=48, width=2)
    r = SZ(200)
    p.d.ellipse([p.s(cx - r), p.s(cy - r), p.s(cx + r), p.s(cy + r)],
                outline=CREAM, width=int(30 * p.ss))
    p.text_at(cx, cy, "OG", p.font(SERIF, SZ(150)), GOLD)
    p.arc_text(cx, cy, SZ(440), "ONE HUNDRED DOLLARS", p.font(SERIF, SZ(56)), CREAM, 195, 345)

    p.lattice_band(Y(1660), Y(1770), GREEN_DIM, waves=30, strands=16, width=2)
    p.text_at(W / 2, Y(1900), "ONE HUNDRED DOLLARS", p.font(SERIF, SZ(88)), GOLD, tracking=X(24))
    p.patron_stars(W / 2, Y(2030))
    p.serials("OG 0.001% 100", size=SZ(48),
              spots=[(W / 2 - X(600), Y(1150)), (W / 2 + X(300), Y(1150))])


# ─────────────────────────────────────────────────────────────────────────
# 06 · Signature Plate — the signing ceremony, facsimile at press scale
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_signature_plate(p):
    ink, ink_dim, proof_gold = GREEN_INK, "#57705f", "#8a6d2a"
    p.hatch(X(120), Y(120), W - X(120), H - Y(120), 45, 16, "#b9b29a", width=3)
    p.microprint(Y(88), ink_dim, size=16)
    p.microprint(H - Y(98), ink_dim, size=16)
    for cx, cy in ((X(300), Y(300)), (W - X(300), Y(300)),
                   (X(300), H - Y(300)), (W - X(300), H - Y(300))):
        p.rosette(cx, cy, SZ(190), SZ(158), ink, petals=16, width=5)
        p.rosette(cx, cy, SZ(132), SZ(112), ink_dim, petals=30, width=3)
    p.lattice_band(Y(1540), Y(1640), ink_dim, waves=26, strands=14, width=3)
    p.border(((SZ(56), 5), (SZ(72), 2)), ink)

    p.d.rounded_rectangle([p.s(X(620)), p.s(Y(80)), p.s(W - X(620)), p.s(Y(260))],
                          radius=SZ(36), fill=ink)
    p.text_at(W / 2, Y(170), "SIGNING CEREMONY \u00b7 OMACOM FOUNDATION",
              p.font(SERIF, SZ(44)), CREAM, tracking=X(12))
    p.text_at(W / 2, Y(980), "D. H. Hansson", p.font(SERIF_IT, SZ(420)), ink)
    p.d.line([p.s(X(320)), p.s(Y(1290)), p.s(W - X(320)), p.s(Y(1290))], fill=proof_gold,
             width=int(8 * p.ss))
    p.d.line([p.s(X(320)), p.s(Y(1312)), p.s(W - X(320)), p.s(Y(1312))], fill=proof_gold,
             width=int(3 * p.ss))
    p.text_at(W / 2, Y(1420), "BENEVOLENT DICTATOR FOR LIFE", p.font(SERIF, SZ(64)), proof_gold,
              tracking=X(22))

    seal_cx, seal_cy = W - X(640), Y(760)
    p.d.ellipse([p.s(seal_cx - SZ(280)), p.s(seal_cy - SZ(280)),
                 p.s(seal_cx + SZ(280)), p.s(seal_cy + SZ(280))], fill=ink)
    p.rosette(seal_cx, seal_cy, SZ(226), SZ(196), RED, petals=22, width=5)
    p.arc_text(seal_cx, seal_cy, SZ(252), "NOTARY OF PATRONS", p.font(SERIF, SZ(32)), RED, 195, 345)
    p.star(seal_cx, seal_cy, SZ(78), RED)

    p.d.rounded_rectangle([p.s(X(760)), p.s(Y(1810)), p.s(W / 2 - X(240)), p.s(Y(2080))],
                          radius=SZ(40), fill=ink)
    p.text_at(W / 2 - X(750), Y(1930), "you@omarchy", p.font(SERIF_IT, SZ(140)), CREAM)
    p.text_at(W / 2 - X(750), Y(2038), "PATRON OF THE ARTS", p.font(SERIF, SZ(36)), "#8f9a85",
              tracking=X(8))
    p.d.rounded_rectangle([p.s(W / 2 + X(180)), p.s(Y(1790)), p.s(W - X(560)), p.s(Y(2090))],
                          radius=SZ(40), fill=ink)
    p.text_at(W / 2 + X(750), Y(1930), "0.001%", p.font(MONO_BOLD, SZ(120)), RED)
    p.text_at(W / 2 + X(750), Y(2048), "THE REMAINDER", p.font(SERIF, SZ(36)), "#8f9a85",
              tracking=X(8))


# ─────────────────────────────────────────────────────────────────────────
# 07 · Serial Strip — the numbering plate, diagonal cream band
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_serial_strip(p):
    p.rosette(X(330), Y(330), SZ(260), SZ(225), GREEN, petals=20, width=3)
    p.rosette(W - X(330), H - Y(330), SZ(260), SZ(225), GREEN, petals=20, width=3)

    # Diagonal cream band through the frame center.
    ang = -14.0
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    cxx, cyy = W / 2, H / 2
    half_w = SZ(330)
    far = W
    band = [
        (cxx + dx * far + nx * half_w, cyy + dy * far + ny * half_w),
        (cxx + dx * far - nx * half_w, cyy + dy * far - ny * half_w),
        (cxx - dx * far - nx * half_w, cyy - dy * far - ny * half_w),
        (cxx - dx * far + nx * half_w, cyy - dy * far + ny * half_w),
    ]
    p.d.polygon([(p.s(x), p.s(y)) for x, y in band], fill=CREAM)
    for off, wd in ((half_w + SZ(18), 8), (half_w + SZ(40), 3)):
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
    p.text_along(cxx, cyy - Y(90), ang, "OG 0.001% 10B", p.font(MONO_BOLD, SZ(170)), RED)
    p.text_along(cxx, cyy + Y(130), ang, "OG 0.001% 10B", p.font(MONO_BOLD, SZ(90)), GREEN_INK)
    micro = "OG 0.001% \u00b7 ELITE CAPITAL \u00b7 PUBLIC CODE \u00b7 " * 4
    p.text_along(cxx, cyy - Y(250), ang, micro, p.font(MONO, SZ(34)), GREEN_INK)
    p.text_along(cxx, cyy + Y(255), ang, micro, p.font(MONO, SZ(34)), GREEN_INK)

    p.text_at(X(200), Y(190), "SERIAL CONTROL STRIP", p.font(SERIF, SZ(44)), CREAM, anchor="lm",
              tracking=X(10))
    p.text_at(W - X(200), H - Y(190), "EVERY PATRON NUMBERED \u00b7 NONE FORGOTTEN",
              p.font(SERIF, SZ(36)), GREEN, anchor="rm", tracking=X(8))
    for x, y in ((X(200), H - Y(190)), (W - X(200), Y(190))):
        p.crosshair(x, y, SZ(40), GREEN_DIM, width=3)


# ─────────────────────────────────────────────────────────────────────────
# 08 · Inverse Cream Note — the paper proof, ink on cream
# ─────────────────────────────────────────────────────────────────────────
@scene
def scene_inverse_cream(p):
    ink, ink_dim = GREEN_INK, "#57705f"
    p.border(((SZ(56), 7), (SZ(72), 2), (SZ(102), 4)), ink)
    p.microprint(Y(86), ink_dim, size=15)
    p.microprint(H - Y(96), ink_dim, size=15)
    p.text_at(W / 2, Y(168), "THE OLIGARCHY \u00b7 PUBLIC CODE \u00b7 EXPENSIVE PATRONS",
              p.font(SERIF, SZ(42)), ink_dim, tracking=X(10))
    p.lattice_band(Y(960), Y(1090), ink_dim, waves=30, strands=18, width=4)

    for cx, cy in ((X(300), Y(300)), (W - X(300), Y(300)),
                   (X(300), H - Y(300)), (W - X(300), H - Y(300))):
        p.d.ellipse([p.s(cx - SZ(205)), p.s(cy - SZ(205)), p.s(cx + SZ(205)), p.s(cy + SZ(205))],
                    fill=ink)
        p.rosette(cx, cy, SZ(186), SZ(156), CREAM, petals=14, width=4)
        p.rosette(cx, cy, SZ(130), SZ(110), "#8f9a85", petals=28, width=3)
        p.text_at(cx, cy, "0", p.font(SERIF, SZ(150)), CREAM)

    p.o_medallion(W / 2, Y(1150), scale=YS, ring=ink, green=ink, dim=ink_dim, gold="#a8842e",
                  caption_top="OMACOM FOUNDATION NOTE", caption_bottom="ZERO DOLLARS")
    p.d.rounded_rectangle([p.s(X(560)), p.s(Y(1660)), p.s(W - X(560)), p.s(Y(1958))],
                          radius=SZ(48), fill=ink)
    p.text_at(W / 2, Y(1772), "ZERO DOLLARS", p.font(SERIF, SZ(112)), CREAM, tracking=X(28))
    p.text_at(W / 2, Y(1888), "SEVERAL BILLIONAIRES", p.font(SERIF_IT, SZ(52)), GOLD, tracking=X(12))
    p.patron_stars(W / 2, Y(1990), ink)
    p.serials("OG 0.001% $0", RED, spots=[(X(430), Y(470)), (W - X(950), Y(1560))])

    sig, cap = p.font(SERIF_IT, SZ(52)), p.font(SERIF, SZ(26))
    p.text_at(X(560), Y(2140), "D. H. Hansson", sig, ink)
    p.text_at(X(560), Y(2210), "BENEVOLENT DICTATOR FOR LIFE", cap, ink_dim, tracking=X(4))
    p.text_at(W - X(560), Y(2140), "you@omarchy", sig, ink)
    p.text_at(W - X(560), Y(2210), "PATRON OF THE ARTS", cap, ink_dim, tracking=X(4))
    p.text_at(W / 2, Y(2210), "SERIES 2026 \u00b7 PROOF", cap, ink_dim, tracking=X(6))


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
