#!/usr/bin/env python3
"""Compose a 3x2 collage of the 9 denomination variants into backgrounds.jpg.

Matches the layout dhh uses in omarchy-diablo-dreams-theme: thin dark gutter,
no captions, full-bleed cells, 3 columns x 2 rows, 1800x1200 total.

Crop window: the medallion + serial sits in the upper-middle of each wallpaper;
we crop a 16:9 region centered on the medallion so the collage shows the
focal art, not vast black sky and signature margin.
"""

import glob
from PIL import Image

COLS = 3
ROWS = 2
CELL_W = 600
CELL_H = 600
GUTTER = 2
OUT_W = COLS * CELL_W + (COLS - 1) * GUTTER
OUT_H = ROWS * CELL_H + (ROWS - 1) * GUTTER

# Source wallpaper is 3840x2160. Medallion sits roughly at (1920, 1010).
# Crop a 16:9 window centered there -> 1920x1080 from a 3840x2160 source.
SRC_CROP_W = 3840
SRC_CROP_H = 2160
SRC_CROP_X = 0
SRC_CROP_Y = 0


def main():
    files = sorted(glob.glob("backgrounds/[1-9]-*.jpg"))
    assert len(files) == 9, f"expected 9 variant jpgs, got {len(files)}: {files}"
    bg = (10, 10, 10)
    canvas = Image.new("RGB", (OUT_W, OUT_H), bg)
    for idx, path in enumerate(files):
        col, row = divmod(idx, COLS)
        im = Image.open(path).convert("RGB").crop(
            (SRC_CROP_X, SRC_CROP_Y, SRC_CROP_X + SRC_CROP_W, SRC_CROP_Y + SRC_CROP_H)
        )
        resized = im.resize((CELL_W, CELL_H), Image.LANCZOS)
        x0 = col * (CELL_W + GUTTER)
        y0 = row * (CELL_H + GUTTER)
        canvas.paste(resized, (x0, y0))
    canvas.save("backgrounds.jpg", "JPEG", quality=88, optimize=True)
    print(f"saved backgrounds.jpg ({OUT_W}x{OUT_H})")


if __name__ == "__main__":
    main()
