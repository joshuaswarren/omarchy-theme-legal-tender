#!/usr/bin/env python3
"""Render preview.png (1800x1012) and preview-unlock.png (1280x720).

Offline desktop mock of the Legal Tender theme: the hero foundation-note
wallpaper behind a top bar and three app panels - a code editor with the
actual engraving source, a btop system monitor, and a file manager. The
lock-screen preview carries the gold-seal plate with the unlock glyph.
"""

import math
import random
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageFont

from engrave import (
    BG, BLUE, CREAM, CREAM_BRIGHT, GOLD, GREEN, GREEN_BRIGHT, GREEN_DIM,
    MONO, SERIF, SERIF_REG,
)

MONO_B = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

PANEL_BG = (27, 38, 31, 244)
PANEL_BORDER = "#55655a"
TITLE_FG = GREEN_BRIGHT

PW, PH = 1800, 1012


def F(path, size):
    return ImageFont.truetype(path, size)


def cover(path, w, h):
    """Scale-to-cover and center-crop an image to w x h."""
    im = Image.open(path).convert("RGB")
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    x0 = (im.width - w) // 2
    y0 = (im.height - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h))


def rounded_panel(canvas, x0, y0, w, h, r=12):
    """Paste a translucent rounded panel; return a Draw bound to it."""
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=PANEL_BG,
                         outline=PANEL_BORDER, width=2)
    canvas.alpha_composite(overlay, (x0, y0))
    return ImageDraw.Draw(canvas)


def tw(d, s, fnt):
    return d.textlength(s, font=fnt)


def code_lines():
    """A real excerpt of the engraving lathe, condensed to fit the panel."""
    return [
        ("class", " ", "Plate", ":", "  ", "# one plate, no globals", ""),
        ("    ", "", '"""Every helper draws on this plate: the lathe itself."""', "", ""),
        ("", "", "", ""),
        ("    ", "def", " ", "rosette", "(self, cx, cy, r_out, r_in, color, petals=", "24", "):", ""),
        ("        ", "", '"""Hypotrochoid guilloche ring drawn between two radii."""', "", ""),
        ("        cx, cy ", "=", " self.s(cx), self.s(cy)", "   ", "# supersample 2x", ""),
        ("        mid ", "=", " (r_out ", "+", " r_in) ", "/", " ", "2", " ", "*", " self.ss", "  ", "# ring midpoint", ""),
        ("        amp ", "=", " (r_out ", "-", " r_in) ", "/", " ", "2", " ", "*", " self.ss", "  ", "# petal depth", ""),
        ("        pts ", "=", " []", "   ", "# petal cycle", ""),
        ("        ", "for", " t ", "in", " ", "range", "(turns ", "*", " ", "4", " ", "+", " ", "1", "):", ""),
        ("            a ", "=", " math.radians(t ", "/", " ", "4", ")", "   ", "# quarter steps", ""),
        ("            r ", "=", " mid ", "+", " amp ", "*", " sin", "(petals ", "*", " a)", "  ", "# the wave", ""),
        ("            pts.append((cx ", "+", " r ", "*", " cos", "(a), cy ", "+", " r ", "*", " sin", "(a)))", ""),
        ("        self.d.line(pts, fill=", "color", ", width=", "6", ")", "   ", "# plate stroke", ""),
        ("", "", "", ""),
        ("    ", "def", " ", "o_medallion", "(self, cx, cy, scale=", "1.0", "):", "  ", "# engraved O", ""),
        ("        ", "", '"""Concentric rosettes, radial shading, one heavy ring."""', "", ""),
        ("        self.rosette(cx, cy, ", "860", " * scale, ", "740", ", ", "GREEN", ", petals=", "40", ")", ""),
        ("        self.rosette(cx, cy, ", "770", " * scale, ", "680", ", ", "GREEN_DIM", ", petals=", "44", ")", ""),
        ("        self.rosette(cx, cy, ", "640", " * scale, ", "600", ", ", "GOLD", ", petals=", "60", ")", ""),
        ("        self.radial(cx, cy, ", "380", ", ", "640", ", ", "GREEN_DIM", ", step=", "3", ")", "  ", "# shade", ""),
        ("        ", "", "# eight patrons, then two more", "", ""),
        ("        self.patron_stars(cx ", "+", " ", "620", ", cy ", "+", " ", "760", ")", "  ", "# capital", ""),
        ("        self.arc_text(cx, cy, ", "950", ", ", '"OMACOM FOUNDATION NOTE"', ",", " ", "CREAM", ")", ""),
        ("        ", "return", " self.save(", '"1-foundation-note.jpg"', ", quality=", "90", ")", "  ", "# 01", ""),
    ]


def draw_editor(canvas):
    x0, y0, w, h = 46, 96, 1030, 806
    d = rounded_panel(canvas, x0, y0, w, h)
    # Title bar.
    d.line([x0, y0 + 40, x0 + w, y0 + 40], fill=GREEN_DIM, width=2)
    d.text((x0 + 22, y0 + 20), "engrave.py", font=F(MONO_B, 15), fill=CREAM, anchor="lm")
    d.text((x0 + w - 22, y0 + 20), "python · utf-8 · 3840x2560", font=F(MONO, 13),
           fill=GREEN_DIM, anchor="rm")
    # Gutter.
    gx = x0 + 76
    d.line([gx, y0 + 40, gx, y0 + h], fill=(26, 38, 31), width=2)
    # Code.
    cx = gx + 18
    line_h = 32
    y = y0 + 62
    num_f, code_f = F(MONO, 16), F(MONO, 21)
    for i, parts in enumerate(code_lines()[:22], 27):
        if i == 38:
            d.rectangle([x0 + 8, y - 4, x0 + w - 8, y + 23], fill="#243029")
        d.text((gx - 14, y + 8), str(i), font=num_f, fill="#6d7f6e", anchor="rm")
        x = cx
        for j, seg in enumerate(parts):
            if not seg:
                continue
            if j == 0 and seg in ("class", "def", "for", "in", "self"):
                col = GOLD
            elif seg.lstrip() in ("def", "for", "in", "return", "class", "self", "import", "range"):
                col = GOLD
            elif seg.startswith('"') or seg.startswith('"""'):
                col = "#a8c98a"
            elif seg.isdigit():
                col = "#cc5a55"
            elif seg.startswith("#"):
                col = "#a3b394"
            elif seg in ("GREEN", "GOLD", "CREAM", "GREEN_DIM", "SERIF"):
                col = "#6fa08d"
            elif seg in ("=", "+", "-", "/", "*"):
                col = "#c9c4ae"
            else:
                col = "#d6d1bd"
            d.text((x, y + 8), seg, font=code_f, fill=col)
            x += tw(d, seg, code_f)
        y += line_h
    # Status bar.
    d.line([x0, y0 + h - 34, x0 + w, y0 + h - 34], fill=GREEN_DIM, width=2)
    # Minimap column: tiny bright blocks mirroring the code lines.
    mx0 = x0 + w - 84
    d.line([mx0 - 10, y0 + 52, mx0 - 10, y0 + h - 40], fill="#243029", width=2)
    random.seed(7)
    for i in range(46):
        my = y0 + 56 + i * 15
        mw = random.randint(30, 64)
        mcol = random.choice(("#d6d1bd", "#c9a554", "#a8c98a", "#8a9587"))
        d.rectangle([mx0, my, mx0 + mw, my + 5], fill=mcol)
        if random.random() < 0.3:
            d.rectangle([mx0 + random.randint(8, 40), my + 8, mx0 + random.randint(44, 62), my + 11],
                        fill="#8a9587")
    d.rectangle([mx0 - 6, y0 + 130, mx0 + 70, y0 + 236], fill=(231, 226, 205, 40),
                outline="#55655a", width=1)
    # Status bar.
    d.line([x0, y0 + h - 34, x0 + w, y0 + h - 34], fill=GREEN_DIM, width=2)
    badge_f = F(MONO_B, 14)
    btxt = "-- NORMAL --"
    bw = tw(d, btxt, badge_f)
    d.rectangle([x0 + 16, y0 + h - 30, x0 + 20 + bw, y0 + h - 4], fill="#e6e1cd")
    d.text((x0 + 18, y0 + h - 17), btxt, font=badge_f, fill="#0e1411", anchor="lm")
    d.text((x0 + 40 + bw, y0 + h - 17), "engrave.py \u00b7 utf-8 \u00b7 python \u00b7 62%", font=F(MONO, 14),
           fill="#c9c4ae", anchor="lm")
    d.text((x0 + w - 22, y0 + h - 17), "41:9", font=F(MONO, 14), fill="#a3b394", anchor="rm")


def draw_btop(canvas):
    x0, y0, w, h = 1112, 96, 642, 428
    d = rounded_panel(canvas, x0, y0, w, h)
    d.text((x0 + 22, y0 + 24), "btop", font=F(SERIF, 19), fill=TITLE_FG, anchor="lm")
    d.text((x0 + w - 22, y0 + 24), "omarchy · 22:41:07", font=F(MONO, 13),
           fill=GREEN_DIM, anchor="rm")
    d.line([x0 + 18, y0 + 44, x0 + w - 18, y0 + 44], fill=GREEN_DIM, width=1)

    # CPU box: 8 core graphs.
    bx, by, bw, bh = x0 + 18, y0 + 56, w - 36, 150
    d.rectangle([bx, by, bx + bw, by + bh], outline=GREEN_DIM, width=1)
    d.text((bx + 10, by + 12), "CPU", font=F(MONO_B, 13), fill=GREEN, anchor="lm")
    d.text((bx + bw - 10, by + 12), "EPYC 7443P 24C/48T · 2.99GHz", font=F(MONO, 12),
           fill=GREEN_DIM, anchor="rm")
    core_h = [34, 51, 22, 68, 29, 44, 95, 38, 26, 60, 31, 19]
    cw = (bw - 24) // len(core_h) - 4
    for i, v in enumerate(core_h):
        cxx = bx + 14 + i * (cw + 4)
        ch_h = int((bh - 44) * v / 100)
        top = by + bh - 10 - ch_h
        col = "#a8c98a" if v < 55 else (GOLD if v < 80 else "#b0413e")
        d.rectangle([cxx, top, cxx + cw, by + bh - 10], fill=col)
        d.text((cxx + cw / 2, top - 9), str(v), font=F(MONO, 10), fill=GREEN_DIM, anchor="mm")

    # MEM box.
    my = by + bh + 14
    mh = 92
    d.rectangle([bx, my, bx + bw, my + mh], outline=GREEN_DIM, width=1)
    d.text((bx + 10, my + 13), "MEM", font=F(MONO_B, 13), fill=GREEN, anchor="lm")
    d.text((bx + bw - 10, my + 13), "15.6GiB / 62.7GiB", font=F(MONO, 12), fill=CREAM, anchor="rm")
    bar_x0, bar_x1, bar_y, bar_h = bx + 12, bx + bw - 12, my + 28, 16
    used_w = int((bar_x1 - bar_x0) * 0.25)
    d.rectangle([bar_x0, bar_y, bar_x1, bar_y + bar_h], fill="#243029")
    d.rectangle([bar_x0, bar_y, bar_x0 + used_w, bar_y + bar_h], fill=GREEN_BRIGHT)
    d.text((bar_x0, bar_y + 34), "used 15.6G", font=F(MONO, 11), fill=GREEN_BRIGHT, anchor="lm")
    d.text((bar_x1, bar_y + 34), "free 47.1G", font=F(MONO, 11), fill=GREEN_DIM, anchor="rm")

    # NET box.
    ny = my + mh + 14
    nh = 74
    d.rectangle([bx, ny, bx + bw, ny + nh], outline=GREEN_DIM, width=1)
    d.text((bx + 10, ny + 13), "NET", font=F(MONO_B, 13), fill=GREEN, anchor="lm")
    d.text((bx + bw - 10, ny + 13), "dn 42.1MiB/s  up 8.4MiB/s", font=F(MONO, 12),
           fill=CREAM, anchor="rm")
    gx0, gx1 = bx + 12, bx + bw - 12
    gy0, gy1 = ny + 22, ny + nh - 8
    d.line([gx0, (gy0 + gy1) / 2, gx1, (gy0 + gy1) / 2], fill="#243029", width=1)
    for vals, col in (([3, 5, 9, 14, 10, 16, 22, 18, 26, 20, 28, 24], GREEN_BRIGHT),
                      ([1, 2, 2, 4, 3, 5, 4, 6, 5, 7, 6, 8], GOLD)):
        pts = []
        for i, v in enumerate(vals):
            px = gx0 + (gx1 - gx0) * i / (len(vals) - 1)
            py = gy1 - (gy1 - gy0) * v / 30
            pts.append((px, py))
        d.line(pts, fill=col, width=2)


def draw_files(canvas):
    x0, y0, w, h = 1112, 548, 642, 354
    d = rounded_panel(canvas, x0, y0, w, h)
    d.text((x0 + 22, y0 + 22), "files", font=F(SERIF, 17), fill=TITLE_FG, anchor="lm")
    d.text((x0 + w - 22, y0 + 22), "~/src/omarchy-theme-legal-tender", font=F(MONO, 12),
           fill=GREEN_DIM, anchor="rm")
    d.line([x0 + 18, y0 + 40, x0 + w - 18, y0 + 40], fill=GREEN_DIM, width=1)

    tree = [(".", 0, True), ("bin", 0, True), ("engrave.py", 1, False),
            ("generate.py", 1, False), ("make_collage.py", 1, False),
            ("make_preview.py", 1, False), ("backgrounds", 0, True),
            ("legal-tender.png", 1, False), ("preview.png", 1, False)]
    fx, fy = x0 + 22, y0 + 58
    row_h = 27
    name_f = F(MONO, 13)
    sel_y = None
    for i, (name, depth, is_dir) in enumerate(tree):
        col = GOLD if is_dir else CREAM
        prefix = "  " * depth
        icon = "> " if is_dir else "  "
        if name == "engrave.py":
            sel_y = fy + i * row_h
            d.rectangle([fx - 6, sel_y - 14, x0 + 330, sel_y + 14], fill=GOLD)
            col = "#0e1411"
        d.text((fx, sel_y if name == "engrave.py" else fy + i * row_h),
               prefix + icon + name, font=name_f, fill=col, anchor="lm")

    # Right column: detail list with sizes.
    rx = x0 + 340
    rows = [("backgrounds/", "dir"), ("engrave.py", "12.2K"), ("generate.py", "16.9K"),
            ("make_collage.py", "1.0K"), ("make_preview.py", "8.8K"), ("colors.toml", "461"),
            ("btop.theme", "1.4K"), ("unlock.png", "512px"), ("preview.png", "1800px")]
    for i, (name, size) in enumerate(rows):
        yy = fy + i * row_h
        d.text((rx, yy), name, font=name_f, fill=GREEN_BRIGHT if i else GOLD, anchor="lm")
        d.text((x0 + w - 22, yy), size, font=name_f, fill=GREEN_DIM, anchor="rm")

    d.line([x0 + 18, y0 + h - 32, x0 + w - 18, y0 + h - 32], fill=GREEN_DIM, width=1)
    d.text((x0 + 22, y0 + h - 16), "9 wallpapers · 3840x2560", font=F(MONO, 12),
           fill=GREEN_DIM, anchor="lm")
    d.text((x0 + w - 22, y0 + h - 16), "legal tender", font=F(SERIF_IT, 13), fill=GOLD, anchor="rm")


def draw_topbar(canvas):
    d = ImageDraw.Draw(canvas)
    bar = Image.new("RGBA", (PW, 36), (14, 20, 17, 242))
    canvas.alpha_composite(bar)
    d = ImageDraw.Draw(canvas)
    d.line([0, 35, PW, 35], fill=GREEN_DIM, width=2)
    d.text((24, 18), "\u25c8 OMACOM", font=F(SERIF, 15), fill=GOLD, anchor="lm")
    d.text((120, 18), "FOUNDATION DESKTOP", font=F(SERIF, 12), fill=GREEN, anchor="lm",
           spacing=0)
    d.text((PW - 24, 18), "OG 0.001%  \u00b7  22:41  \u00b7  2026", font=F(MONO, 13),
           fill=CREAM, anchor="rm")


def make_preview():
    canvas = cover("backgrounds/1-foundation-note.jpg", PW, PH).convert("RGBA")
    draw_topbar(canvas)
    draw_editor(canvas)
    draw_btop(canvas)
    draw_files(canvas)
    canvas.convert("RGB").save("preview.png")
    print("saved preview.png (1800x1012)")


def make_unlock_preview():
    canvas = cover("backgrounds/3-guilloche-field.jpg", PW, PH).convert("RGBA")
    veil = Image.new("RGBA", (PW, PH), (8, 12, 10, 96))
    canvas.alpha_composite(veil)
    d = ImageDraw.Draw(canvas)
    glyph = Image.open("unlock.png").convert("RGBA").resize((240, 240), Image.LANCZOS)
    canvas.alpha_composite(glyph, (PW // 2 - 120, 200))
    d.text((PW / 2, 130), "THURSDAY \u00b7 AUGUST 27", font=F(SERIF, 26), fill=GREEN_BRIGHT,
           anchor="mm")
    d.text((PW / 2, 600), "22:41", font=F(SERIF, 150), fill=CREAM, anchor="mm")
    pw_f = F(MONO, 20)
    pill_w = 460
    d.rounded_rectangle([PW / 2 - pill_w / 2, 716, PW / 2 + pill_w / 2, 768], radius=26,
                        outline="#55655a", width=3)
    dots = "\u25cf " * 6
    d.text((PW / 2 - pill_w / 2 + 30, 742), dots, font=pw_f, fill=CREAM, anchor="lm")
    caret_x = PW / 2 - pill_w / 2 + 30 + tw(d, dots, pw_f) + 12
    d.rectangle([caret_x, 726, caret_x + 4, 758], fill=CREAM)
    d.text((PW / 2, 830), "IN PATRONS WE TRUST", font=F(SERIF, 20), fill=GOLD, anchor="mm")
    d.text((60, 952), "OG 0.001%", font=F(MONO, 16), fill=GREEN_DIM, anchor="lm")
    d.text((PW - 60, 952), "SERIES 2026", font=F(MONO, 16), fill=GREEN_DIM, anchor="rm")
    canvas.convert("RGB").save("preview-unlock.png")
    print("saved preview-unlock.png (1800x1012)")


if __name__ == "__main__":
    make_preview()
    make_unlock_preview()
