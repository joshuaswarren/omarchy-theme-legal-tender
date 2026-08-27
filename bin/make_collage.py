#!/usr/bin/env python3
"""Compose the nine backgrounds into backgrounds.jpg.

True 3x3 contact sheet: 1800x1200 total, nine 600x400 cells, edge to
edge with no gutters or labels. Sources are 3840x2560 (3:2), so each
cell is a straight LANCZOS resize of a whole background.
"""

import glob
from PIL import Image

CELL_W, CELL_H = 600, 400
COLS, ROWS = 3, 3
OUT_W, OUT_H = COLS * CELL_W, ROWS * CELL_H  # 1800x1200


def main():
    files = sorted(glob.glob("backgrounds/[1-9]-*.jpg"))
    assert len(files) == 9, f"expected 9 backgrounds, got {len(files)}: {files}"
    canvas = Image.new("RGB", (OUT_W, OUT_H), "#000000")
    for idx, path in enumerate(files):
        row, col = divmod(idx, COLS)
        im = Image.open(path).convert("RGB").resize((CELL_W, CELL_H), Image.LANCZOS)
        canvas.paste(im, (col * CELL_W, row * CELL_H))
    canvas.save("backgrounds.jpg", "JPEG", quality=88, optimize=True)
    print(f"saved backgrounds.jpg ({OUT_W}x{OUT_H})")


if __name__ == "__main__":
    main()
