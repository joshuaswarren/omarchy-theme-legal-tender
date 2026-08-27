#!/usr/bin/env python3
"""Engraving primitives for the Omacom Foundation Note wallpapers.

Every drawing method lives on a Plate instance and draws on that Plate's
own canvas. No module-global image state: a scene receives a Plate and
everything it draws lands on that Plate. Coordinates are in final-output
space; the Plate supersamples internally and downsamples on save.
"""

import math
from PIL import Image, ImageDraw, ImageFont

# Palette of the theme (mirrors colors.toml).
BG = "#0e1411"
BG_DEEP = "#0a0f0d"
GREEN = "#6f9663"
GREEN_BRIGHT = "#85a760"
GREEN_DIM = "#3a523f"
GREEN_INK = "#2e4a38"
CREAM = "#ddd8c4"
CREAM_BRIGHT = "#f2eddb"
GOLD = "#c9a554"
RED = "#b0413e"
BLUE = "#5b7fa6"

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_BOLD = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"

MICROPRINT = "ELITE CAPITAL \u00b7 PUBLIC CODE \u00b7 ZERO DOLLARS \u00b7 SEVERAL BILLIONAIRES \u00b7 "

# Final wallpaper canvas and its 5% safe area. Scenes compose onto a
# smaller content canvas that a caller mats onto this full canvas at an
# inset equal to the margins below, so anything drawn inside the content
# canvas structurally lands inside the safe area. The runtime checks below
# are a second, independent numeric guarantee for text and other critical
# bounds, keyed to these same numbers.
FULL_W, FULL_H = 3840, 2160
SAFE_X0, SAFE_X1 = 192, FULL_W - 192
SAFE_Y0, SAFE_Y1 = 108, FULL_H - 108


class Plate:
    """A supersampled engraving canvas bound to one image."""

    def __init__(self, w, h, bg=BG, ss=2, origin=(0, 0), safe_check=True):
        self.w, self.h, self.ss = w, h, ss
        self.origin = origin
        self.safe_check = safe_check
        self.img = Image.new("RGB", (w * ss, h * ss), bg)
        self.d = ImageDraw.Draw(self.img)

    # ── plumbing ────────────────────────────────────────────────────────
    def s(self, v):
        return v * self.ss

    def font(self, path, size):
        return ImageFont.truetype(path, max(1, int(size * self.ss)))

    def save(self, path, quality=None):
        out = self.img.resize((self.w, self.h), Image.LANCZOS)
        if quality is None:
            out.save(path)
        else:
            out.save(path, "JPEG", quality=quality, optimize=True)
        return path

    def check_safe(self, x0, y0, x1, y1, label):
        """Assert a critical element's bbox (content-canvas coords) lands
        inside the 5% safe area once this plate is matted at self.origin."""
        if not self.safe_check:
            return
        ox, oy = self.origin
        ax0, ax1 = ox + min(x0, x1), ox + max(x0, x1)
        ay0, ay1 = oy + min(y0, y1), oy + max(y0, y1)
        assert SAFE_X0 - 0.5 <= ax0 and ax1 <= SAFE_X1 + 0.5 and \
            SAFE_Y0 - 0.5 <= ay0 and ay1 <= SAFE_Y1 + 0.5, (
            f"{label} at ({ax0:.0f},{ay0:.0f})-({ax1:.0f},{ay1:.0f}) breaches "
            f"safe area x[{SAFE_X0}..{SAFE_X1}] y[{SAFE_Y0}..{SAFE_Y1}]"
        )

    def _check_bbox(self, bbox, label):
        x0, y0, x1, y1 = (v / self.ss for v in bbox)
        self.check_safe(x0, y0, x1, y1, label)

    # ── ornaments ───────────────────────────────────────────────────────
    def rosette(self, cx, cy, r_outer, r_inner, color, petals=24, turns=360, width=1):
        """Hypotrochoid guilloche ring between two radii."""
        cx, cy = cx * self.ss, cy * self.ss
        mid = (r_outer + r_inner) / 2 * self.ss
        amp = (r_outer - r_inner) / 2 * self.ss
        pts = []
        for t in range(turns * 4 + 1):
            a = math.radians(t / 4)
            r = mid + amp * math.sin(petals * a)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        self.d.line(pts, fill=color, width=max(1, int(width * self.ss)))

    def lattice_band(self, y0, y1, color, waves=9, strands=14, width=1):
        """Interleaved sine strands across the full width (lathe work)."""
        cw = self.w * self.ss
        y0, y1 = y0 * self.ss, y1 * self.ss
        mid, amp = (y0 + y1) / 2, (y1 - y0) / 2
        for i in range(strands):
            phase = math.pi * i / strands
            pts = []
            for x in range(0, cw + 1, 6 * self.ss):
                y = mid + amp * math.sin(2 * math.pi * waves * x / cw + phase) * math.cos(
                    math.pi * i / strands
                )
                pts.append((x, y))
            self.d.line(pts, fill=color, width=max(1, int(width * self.ss)))

    def radial(self, cx, cy, r1, r2, color, step=3, width=1):
        """Engraved radial shading strokes between two radii."""
        for t in range(0, 360, step):
            a = math.radians(t)
            self.d.line(
                [
                    (self.s(cx) + self.s(r1) * math.cos(a), self.s(cy) + self.s(r1) * math.sin(a)),
                    (self.s(cx) + self.s(r2) * math.cos(a), self.s(cy) + self.s(r2) * math.sin(a)),
                ],
                fill=color,
                width=max(1, int(width * self.ss)),
            )

    def rays(self, cx, cy, r_short, r_long, color, count=72, width=4):
        """Sunburst of alternating long and short rays."""
        for i in range(count):
            a = math.radians(i * 360 / count)
            r = r_long if i % 2 == 0 else r_short
            self.d.line(
                [
                    (self.s(cx) + self.s(r_long * 0.18) * math.cos(a),
                     self.s(cy) + self.s(r_long * 0.18) * math.sin(a)),
                    (self.s(cx) + self.s(r) * math.cos(a), self.s(cy) + self.s(r) * math.sin(a)),
                ],
                fill=color,
                width=max(1, int(width * self.ss)),
            )

    def star(self, cx, cy, r, color, inner=0.4):
        pts = []
        for i in range(10):
            ang = math.radians(-90 + i * 36)
            rr = r if i % 2 == 0 else r * inner
            pts.append(
                (self.s(cx) + self.s(rr) * math.cos(ang), self.s(cy) + self.s(rr) * math.sin(ang))
            )
        self.d.polygon(pts, fill=color)

    def dot_ring(self, cx, cy, r, color, count=36, dr=4):
        for i in range(count):
            a = math.radians(i * 360 / count)
            x = self.s(cx) + self.s(r) * math.cos(a)
            y = self.s(cy) + self.s(r) * math.sin(a)
            rr = self.s(dr)
            self.d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=color)

    def crosshair(self, cx, cy, r, color, width=2, circle=True):
        x, y, rr = self.s(cx), self.s(cy), self.s(r)
        self.d.line([x - rr, y, x + rr, y], fill=color, width=int(width * self.ss))
        self.d.line([x, y - rr, x, y + rr], fill=color, width=int(width * self.ss))
        if circle:
            self.d.ellipse([x - rr * 0.45, y - rr * 0.45, x + rr * 0.45, y + rr * 0.45],
                           outline=color, width=int(width * self.ss))

    def hatch(self, x0, y0, x1, y1, angle_deg, gap, color, width=1):
        """Parallel-line engraving hatch clipped to a rectangle."""
        a = math.radians(angle_deg)
        dx, dy = math.cos(a), math.sin(a)
        nx, ny = -dy, dx
        corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        proj = [cx * nx + cy * ny for cx, cy in corners]
        lo, hi = int(min(proj)) - gap, int(max(proj)) + gap
        span = math.hypot(x1 - x0, y1 - y0)
        for p in range(lo, hi + 1, gap):
            mx, my = (x0 + x1) / 2 + nx * p, (y0 + y1) / 2 + ny * p
            self.d.line(
                [
                    (self.s(mx - dx * span), self.s(my - dy * span)),
                    (self.s(mx + dx * span), self.s(my + dy * span)),
                ],
                fill=color,
                width=max(1, int(width * self.ss)),
            )

    # ── type ────────────────────────────────────────────────────────────
    def text_at(self, x, y, s, fnt, color, anchor="mm", tracking=0):
        if tracking == 0:
            self.d.text((self.s(x), self.s(y)), s, font=fnt, fill=color, anchor=anchor)
            bbox = self.d.textbbox((self.s(x), self.s(y)), s, font=fnt, anchor=anchor)
            self._check_bbox(bbox, f"text {s[:24]!r}")
            return
        total = sum(self.d.textlength(c, font=fnt) for c in s) + self.s(tracking) * (len(s) - 1)
        if anchor[0] == "m":
            cx = self.s(x) - total / 2
        elif anchor[0] == "r":
            cx = self.s(x) - total
        else:
            cx = self.s(x)
        x0 = cx
        for c in s:
            w = self.d.textlength(c, font=fnt)
            self.d.text((cx, self.s(y)), c, font=fnt, fill=color, anchor="lm")
            cx += w + self.s(tracking)
        asc, desc = fnt.getmetrics()
        self._check_bbox((x0, self.s(y) - asc, cx - self.s(tracking), self.s(y) + desc),
                          f"text {s[:24]!r}")

    def arc_text(self, cx, cy, radius, text, fnt, color, start_deg, end_deg, flip=False):
        """Characters along an arc, each rotated to the tangent."""
        n = len(text)
        xs, ys = [], []
        for i, ch in enumerate(text):
            frac = i / max(n - 1, 1)
            ang = math.radians(start_deg + (end_deg - start_deg) * frac)
            x = self.s(cx) + self.s(radius) * math.cos(ang)
            y = self.s(cy) + self.s(radius) * math.sin(ang)
            xs.append(x)
            ys.append(y)
            rot = math.degrees(ang) + (-90 if flip else 90)
            glyph = Image.new("RGBA", (fnt.size * 2 + 8, fnt.size * 2 + 8), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glyph)
            half = glyph.width // 2
            gd.text((half, half), ch, font=fnt, fill=color, anchor="mm")
            glyph = glyph.rotate(-rot, resample=Image.BICUBIC, center=(half, half))
            self.img.paste(glyph, (int(x - half), int(y - half)), glyph)
        pad = self.s(fnt.size) / 2 + 4
        self._check_bbox((min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad),
                          f"arc text {text[:24]!r}")

    def text_along(self, x0, y0, angle_deg, s, fnt, color, anchor_mid=True):
        """Whole string rotated to an arbitrary angle, anchored at (x0, y0)."""
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        bbox = ld.textbbox((0, 0), s, font=fnt)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pad = fnt.size
        strip = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
        sd = ImageDraw.Draw(strip)
        sd.text((pad - bbox[0], pad - bbox[1]), s, font=fnt, fill=color)
        strip = strip.rotate(angle_deg, resample=Image.BICUBIC, expand=True)
        if anchor_mid:
            px = int(self.s(x0) - strip.width / 2)
            py = int(self.s(y0) - strip.height / 2)
        else:
            px, py = int(self.s(x0)), int(self.s(y0))
        self.img.paste(strip, (px, py), strip)
        self._check_bbox((px, py, px + strip.width, py + strip.height),
                          f"text-along {s[:24]!r}")

    # ── note furniture ──────────────────────────────────────────────────
    def border(self, rules, color=GREEN):
        """rules: iterable of (margin, width)."""
        for m, wd in rules:
            self.d.rectangle(
                [self.s(m), self.s(m), self.s(self.w - m), self.s(self.h - m)],
                outline=color,
                width=int(wd * self.ss),
            )
            self.check_safe(m, m, self.w - m, self.h - m, "border rule")

    def microprint(self, y, color=GREEN, size=11, text=None, x0=130, x1=None,
                   clip=False):
        """A line of tiny repeated text between the border rules. Decorative."""
        text = text or MICROPRINT
        fnt = self.font(SERIF_REG, size)
        x1 = x1 if x1 is not None else self.w - 130
        unit = self.d.textlength(text, font=fnt)
        start = int(self.s(x0))
        end = int(self.s(x1))
        if clip:
            # Tile on a bounded strip so the final repetition is clipped
            # cleanly at x1 instead of spilling through the right border.
            height = max(1, int(fnt.size * 1.6))
            strip = Image.new("RGBA", (max(1, end - start), height), (0, 0, 0, 0))
            sd = ImageDraw.Draw(strip)
            x = 0
            while x < strip.width:
                sd.text((x, 0), text, font=fnt, fill=color)
                x += unit
            self.img.paste(strip, (start, int(self.s(y))), strip)
        else:
            x = start
            while x < end:
                self.d.text((x, self.s(y)), text, font=fnt, fill=color)
                x += unit
        self.check_safe(x0, y - size, x1, y + size, "microprint")

    def patron_stars(self, cx, cy, color=GOLD):
        """Eight founding patrons, then two smaller ones, added later."""
        sx = cx - 5 * 62
        for i in range(8):
            self.star(sx + i * 62, cy, 20, color)
        for i in range(2):
            self.star(sx + 8 * 62 + 20 + i * 46, cy + 4, 12, color)

    def serials(self, s, color=RED, size=44, spots=None):
        fnt = self.font(MONO_BOLD, size)
        spots = spots or [(self.w * 0.112, self.h * 0.184), (self.w * 0.753, self.h * 0.633)]
        for x, y in spots:
            self.d.text((self.s(x), self.s(y)), s, font=fnt, fill=color)
            self._check_bbox(self.d.textbbox((self.s(x), self.s(y)), s, font=fnt),
                              f"serial {s!r}")

    def o_medallion(self, cx, cy, scale=1.0, ring=CREAM, green=GREEN, dim=GREEN_DIM,
                    gold=GOLD, caption_top="OMACOM FOUNDATION NOTE",
                    caption_bottom="IN PATRONS WE TRUST"):
        """The engraved O: concentric rosettes, radial shading, heavy ring."""
        self.rosette(cx, cy, 860 * scale, 740 * scale, green, petals=40, width=3)
        self.rosette(cx, cy, 770 * scale, 680 * scale, dim, petals=44, width=2)
        self.rosette(cx, cy, 640 * scale, 600 * scale, gold, petals=60, width=2)
        self.radial(cx, cy, 380 * scale, 640 * scale, dim, step=3, width=1)
        r = 320 * scale
        self.d.ellipse([self.s(cx - r), self.s(cy - r), self.s(cx + r), self.s(cy + r)],
                       outline=ring, width=int(46 * scale * self.ss))
        self.d.ellipse(
            [self.s(cx - r - 26 * scale), self.s(cy - r - 26 * scale),
             self.s(cx + r + 26 * scale), self.s(cy + r + 26 * scale)],
            outline=green, width=max(1, int(3 * scale * self.ss)))
        self.d.ellipse(
            [self.s(cx - r + 26 * scale), self.s(cy - r + 26 * scale),
             self.s(cx + r - 26 * scale), self.s(cy + r - 26 * scale)],
            outline=green, width=max(1, int(3 * scale * self.ss)))
        if caption_top:
            self.arc_text(cx, cy, 950 * scale, caption_top,
                          self.font(SERIF, 88 * scale), ring, 200, 340)
        if caption_bottom:
            self.arc_text(cx, cy, 880 * scale, caption_bottom,
                          self.font(SERIF, 64 * scale), gold, 150, 30, flip=True)
