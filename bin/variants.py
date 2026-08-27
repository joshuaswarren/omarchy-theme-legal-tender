#!/usr/bin/env python3
"""Render the 9 denomination variants of the Omacom Foundation Note.

Reuses the engraving helpers from generate.py but produces 1.jpg .. 9.jpg in
backgrounds/ at different denominations ($100 .. $10,000,000,000). The collage
composed by make_collage.py reads them in numeric order.
"""

import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
import generate
from generate import W, H, SS, BG, GREEN, GREEN_DIM, CREAM, GOLD, RED, SERIF, SERIF_IT, MONO


DENOMS = [
    ("100",    "$100",            "ONE HUNDRED DOLLARS"),
    ("1k",     "$1,000",          "ONE THOUSAND DOLLARS"),
    ("10k",    "$10,000",         "TEN THOUSAND DOLLARS"),
    ("100k",   "$100,000",        "ONE HUNDRED THOUSAND DOLLARS"),
    ("1m",     "$1,000,000",      "ONE MILLION DOLLARS"),
    ("10m",    "$10,000,000",     "TEN MILLION DOLLARS"),
    ("100m",   "$100,000,000",    "ONE HUNDRED MILLION DOLLARS"),
    ("1b",     "$1,000,000,000",  "ONE BILLION DOLLARS"),
    ("10b",    "$10,000,000,000", "TEN BILLION DOLLARS"),
]

MICROPRINT = "ELITE CAPITAL \u00b7 PUBLIC CODE \u00b7 ZERO DOLLARS \u00b7 SEVERAL BILLIONAIRES \u00b7 "


def render_one(img, d, denom_short, amount_label, headline):
    def font(path, size):
        return ImageFont.truetype(path, size * SS)

    # Outer borders + microprint.
    for m, wd in ((70, 4), (86, 1), (118, 2)):
        d.rectangle([m * SS, m * SS, W * SS - m * SS, H * SS - m * SS], outline=GREEN, width=wd * SS)
    mp_font = font(SERIF, 11)
    for y in (96, H - 106):
        x = 130 * SS
        while x < W * SS - 130 * SS:
            d.text((x, y * SS), MICROPRINT, font=mp_font, fill=GREEN_DIM)
            x += int(d.textlength(MICROPRINT, font=mp_font))

    generate.lattice_band(970, 1090, GREEN_DIM, waves=30, strands=18)

    for cx, cy in ((330, 320), (W - 330, 320), (330, H - 320), (W - 330, H - 320)):
        generate.rosette(cx, cy, 170, 138, GREEN, petals=14)
        generate.rosette(cx, cy, 118, 100, GREEN_DIM, petals=28)
        generate.text_at(cx, cy, amount_label, font(SERIF, 86), CREAM)

    CX, CY = W // 2, 1010
    generate.rosette(CX, CY, 540, 484, GREEN, petals=40)
    generate.rosette(CX, CY, 506, 446, GREEN_DIM, petals=44)
    generate.rosette(CX, CY, 428, 398, GOLD, petals=60)
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
    d.ellipse([(CX - 210) * SS, (CY - 210) * SS, (CX + 210) * SS, (CY + 210) * SS], outline=CREAM, width=52 * SS)
    d.ellipse([(CX - 228) * SS, (CY - 228) * SS, (CX + 228) * SS, (CY + 228) * SS], outline=GREEN, width=3 * SS)
    d.ellipse([(CX - 192) * SS, (CY - 192) * SS, (CX + 192) * SS, (CY + 192) * SS], outline=GREEN, width=3 * SS)

    generate.arc_text(CX, CY, 610, "OMACOM FOUNDATION NOTE", font(SERIF, 64), CREAM, 200, 340)
    generate.arc_text(CX, CY, 616, "IN PATRONS WE TRUST", font(SERIF, 46), GOLD, 150, 30, flip=True)

    generate.text_at(W // 2, 1755, headline, font(SERIF, 78), GOLD, tracking=22)
    generate.text_at(W // 2, 208, "THE OLIGARCHY \u00b7 FREE SOFTWARE \u00b7 EXPENSIVE PATRONS", font(SERIF, 40), GREEN, tracking=10)

    sx = W // 2 - 5 * 62
    for i in range(8):
        generate.star(sx + i * 62, 1878, 20, GOLD)
    for i in range(2):
        generate.star(sx + 8 * 62 + 20 + i * 46, 1882, 12, GOLD)

    ser = font(MONO, 44)
    d.text((430 * SS, 470 * SS), f"OG 0.001% {denom_short.upper()}", font=ser, fill=RED)
    d.text(((W - 850) * SS, 1620 * SS), f"OG 0.001% {denom_short.upper()}", font=ser, fill=RED)

    sig = font(SERIF_IT, 52)
    cap = font(SERIF, 26)
    d.text((560 * SS, 1930 * SS), "D. H. Hansson", font=sig, fill=CREAM, anchor="mm")
    d.line([360 * SS, 1965 * SS, 760 * SS, 1965 * SS], fill=GREEN, width=2 * SS)
    generate.text_at(560, 1995, "BENEVOLENT DICTATOR FOR LIFE", cap, GREEN, tracking=4)
    d.text(((W - 560) * SS, 1930 * SS), "you@omarchy", font=sig, fill=CREAM, anchor="mm")
    d.line([(W - 760) * SS, 1965 * SS, (W - 360) * SS, 1965 * SS], fill=GREEN, width=2 * SS)
    generate.text_at(W - 560, 1995, "PATRON OF THE ARTS", cap, GREEN, tracking=4)
    generate.text_at(W // 2, 1995, f"SERIES 2026 \u00b7 {denom_short.upper()}", cap, GREEN, tracking=6)


if __name__ == "__main__":
    os.makedirs("backgrounds", exist_ok=True)
    for i, (short, label, headline) in enumerate(DENOMS, start=1):
        canvas = Image.new("RGB", (W * SS, H * SS), BG)
        draw = ImageDraw.Draw(canvas)
        render_one(canvas, draw, short, label, headline)
        out = canvas.resize((W, H), Image.LANCZOS)
        path = f"backgrounds/{i}-foundation-note-{short}.jpg"
        out.convert("RGB").save(path, "JPEG", quality=88, optimize=True)
        print(f"saved {path}")
