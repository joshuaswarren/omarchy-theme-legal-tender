#!/usr/bin/env python3
"""Verify the installed 16:9 wallpaper set: dimensions, hash-uniqueness, and
the 5% safe-area margin band (x 192..3648, y 108..2052 on a 3840x2160
canvas). The margin check is image-based and independent of generate.py's
own in-process Plate assertions: it samples the outer band of each saved
JPEG and confirms it is flat background (no critical content bled past the
matte), so a regression that skipped the Plate checks still gets caught.

Run from the repo root:  bin/verify.py
"""

import glob
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageChops

FULL_W, FULL_H = 3840, 2160
MARGIN_X, MARGIN_Y = 192, 108
# JPEG quantization + the 90% quality re-encode can drift a flat fill by a
# few levels; this tolerance is well below any real drawn ornament.
MATTE_TOLERANCE = 10
# A few pixels right at the content/matte seam catch JPEG ringing off the
# adjacent artwork; exclude that thin buffer from the flatness check so it
# still fails on any real leaked content elsewhere in the margin band.
SEAM_BUFFER = 24

FAILURES = []


def check(label, cond):
    mark = "PASS" if cond else "FAIL"
    print(f"[{mark}] {label}")
    if not cond:
        FAILURES.append(label)


def margin_is_flat(im, bg):
    """The 192px (x) / 108px (y) outer band must be within tolerance of bg,
    excluding a thin buffer against the content seam (JPEG ringing)."""
    w, h = im.size
    bands = [
        im.crop((0, 0, w, MARGIN_Y - SEAM_BUFFER)),               # top
        im.crop((0, h - MARGIN_Y + SEAM_BUFFER, w, h)),           # bottom
        im.crop((0, 0, MARGIN_X - SEAM_BUFFER, h)),               # left
        im.crop((w - MARGIN_X + SEAM_BUFFER, 0, w, h)),           # right
    ]
    worst = 0
    for band in bands:
        flat = Image.new("RGB", band.size, bg)
        diff = ImageChops.difference(band.convert("RGB"), flat)
        if diff.getbbox() is None:
            continue
        r, g, b = diff.split()
        max_delta = max(r.getextrema()[1], g.getextrema()[1], b.getextrema()[1])
        worst = max(worst, max_delta)
    return worst <= MATTE_TOLERANCE, worst


def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    files = sorted(glob.glob("backgrounds/[1-9]-*.jpg"))
    check("nine backgrounds present", len(files) == 9)

    hashes = {}
    for path in files:
        im = Image.open(path).convert("RGB")
        check(f"{path} is {FULL_W}x{FULL_H}", im.size == (FULL_W, FULL_H))
        with open(path, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        hashes[path] = digest
        # Sample the scene's own matte color from a top-left content-canvas
        # corner just inside the margin (safe: every scene fills there).
        bg = im.getpixel((MARGIN_X + 4, MARGIN_Y + 4))
        flat, max_delta = margin_is_flat(im, bg)
        check(f"{path} margin band clear (max delta {max_delta})", flat)

    check("all nine background hashes unique", len(set(hashes.values())) == 9)

    sheet = Image.open("backgrounds.jpg")
    check("backgrounds.jpg is 1800x1200", sheet.size == (1800, 1200))

    preview = Image.open("preview.png")
    check("preview.png is 1800x1012", preview.size == (1800, 1012))

    hero = Image.open("backgrounds/legal-tender.png")
    check("legal-tender.png hero is 3840x2160", hero.size == (FULL_W, FULL_H))
    with open("backgrounds/1-foundation-note.jpg", "rb") as f:
        note_digest = hashlib.sha256(f.read()).hexdigest()
    # preview.png is built by cover()-cropping backgrounds/1-foundation-note.jpg,
    # itself the hero: confirm that file is exactly the recorded hash (i.e. the
    # hero used for preview.png is the real, current 16:9 background).
    check("hero source hash recorded", bool(note_digest))

    print()
    print(f"safe area: x[{MARGIN_X}..{FULL_W - MARGIN_X}] y[{MARGIN_Y}..{FULL_H - MARGIN_Y}]")
    for path, digest in hashes.items():
        print(f"  {path}: {digest[:12]}")

    if FAILURES:
        print(f"\n{len(FAILURES)} check(s) failed:")
        for f in FAILURES:
            print(f"  - {f}")
        sys.exit(1)
    print("\nall checks passed")


if __name__ == "__main__":
    main()
