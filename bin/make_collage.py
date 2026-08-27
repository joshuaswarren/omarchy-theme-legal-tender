#!/usr/bin/env python3
"""Compose the nine backgrounds into backgrounds.jpg.

1800x1200 contact sheet: nine 600x400 cells. Sources are native 3840x2160
(16:9); each cell letterboxes the ENTIRE background into a 600x338 area
(scale-to-fit, no crop) with a 31px theme-colored matte top and bottom.
"""

import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image

from engrave import BG

CELL_W, CELL_H = 600, 400
COLS, ROWS = 3, 3
OUT_W, OUT_H = COLS * CELL_W, ROWS * CELL_H  # 1800x1200
LETTERBOX_H = 338
MATTE = (CELL_H - LETTERBOX_H) // 2  # 31


def main():
    files = sorted(glob.glob("backgrounds/[1-9]-*.jpg"))
    assert len(files) == 9, f"expected 9 backgrounds, got {len(files)}: {files}"
    canvas = Image.new("RGB", (OUT_W, OUT_H), "#000000")
    for idx, path in enumerate(files):
        im = Image.open(path).convert("RGB")
        assert im.size == (3840, 2160), f"{path} is {im.size}, expected 3840x2160"
        row, col = divmod(idx, COLS)
        frame = im.resize((CELL_W, LETTERBOX_H), Image.LANCZOS)
        cell = Image.new("RGB", (CELL_W, CELL_H), BG)
        cell.paste(frame, (0, MATTE))
        canvas.paste(cell, (col * CELL_W, row * CELL_H))
    canvas.save("backgrounds.jpg", "JPEG", quality=88, optimize=True)
    print(f"saved backgrounds.jpg ({OUT_W}x{OUT_H})")


if __name__ == "__main__":
    main()
