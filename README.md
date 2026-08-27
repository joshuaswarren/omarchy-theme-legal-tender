# Legal Tender

An Omarchy theme. Elite capital. Public code.

![Legal Tender preview](preview.png)

![Legal Tender backgrounds](backgrounds.jpg)

The wallpaper is the printing plate of an Omacom Foundation Note: guilloche
rosettes, a lathe-work band, eight security stars for the eight founding
patrons (plus two smaller ones, added later), and genuine anti-counterfeit
microprinting. Zoom in on the border. The terminal palette is intaglio ink:
money green, gold leaf, cream paper, and serial-number red on black-green plate.

Nine denominations ship with the theme - $100, $1,000, $10,000, $100,000,
$1,000,000, $10,000,000, $100,000,000, $1,000,000,000, and $10,000,000,000.
Each carries its own serial (`OG 0.001% 100`, `OG 0.001% 1M`, etc).

Zero dollars. Several billionaires.

## Install

```
omarchy-theme-install https://github.com/joshuaswarren/omarchy-theme-legal-tender
```

## Anatomy

- `preview.png` - hero wallpaper
- `backgrounds.jpg` - all 9 denominations at a glance
- `backgrounds/[1-9]-foundation-note-*.jpg` - individual denominations
- `backgrounds/legal-tender.png` - the canonical $1M note at 3840x2160
- `bin/generate.py` - the engraving lathe; regenerates wallpaper and unlock glyph
- `bin/variants.py` - renders the 9 denomination variants
- `bin/make_collage.py` - composes the 3x2 collage into `backgrounds.jpg`
- `colors.toml` - terminal and shell palette
- `btop.theme`, `neovim.lua` (inline mini.base16), `vscode.json`, `icons.theme`
- `unlock.png` - a small 1M rosette for the lock screen

## Palette

| Role | Hex |
| --- | --- |
| Background (plate) | `#0e1411` |
| Foreground (cream) | `#d6d1bd` |
| Accent (gold leaf) | `#c9a554` |
| Money green | `#85a760` |
| Serial red | `#b0413e` |
| Treasury blue | `#5b7fa6` |

This note is legal tender for all debts, technical and otherwise.
