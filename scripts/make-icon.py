"""Draw the site icon: "ET" in Source Serif 4 SemiBold with an attention arc from E to T.

The letters are converted to SVG paths, so the icon never depends on a font being installed.
Writes public/favicon.svg, then renders public/apple-touch-icon.png (180 px) and public/favicon.ico
(16, 32, 48 px) from it with headless Chrome. Needs fontTools, brotli (to read the woff2 the site
already ships, so run `astro dev` or `astro build` once first) and Pillow:

    python scripts/make-icon.py
"""

import subprocess
import tempfile
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = Path(__file__).resolve().parent.parent
FONT = next((ROOT / ".astro" / "fonts").glob("font-serif-600-normal-latin-*.woff2"))

PAPER = "#0c0c0c"  # the home page's dark paper
INK = "#ece9e2"  # its text colour
SCALE = 0.06  # font units to icon units (100 x 100 box): cap height 664 -> 39.8
KERN = -30  # font units between E and T
BASELINE = 80


def main():
    font = TTFont(FONT)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    e, t = glyphs[cmap[ord("E")]], glyphs[cmap[ord("T")]]

    # Centre the ink (E's left edge 36 to T's right edge 628, both in font units) in the box.
    t_offset = e.width + KERN
    left, right = 36, t_offset + 628
    x0 = 50 - (left + right) / 2 * SCALE

    def path(glyph, dx):
        pen = SVGPathPen(glyphs, lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        glyph.draw(TransformPen(pen, (SCALE, 0, 0, -SCALE, x0 + dx * SCALE, BASELINE)))
        return pen.getCommands()

    # The arc joins the middle of each letter, a little above the cap height, like the hover arcs on the home page.
    cap_top = BASELINE - 664 * SCALE
    ex, tx = x0 + (36 + 596) / 2 * SCALE, x0 + (t_offset + (22 + 628) / 2) * SCALE
    # A low, wide curve with a dot on each end reads as an edge between two tokens; a tall one reads as a handle.
    y = cap_top - 7
    arc = f"M{ex:.1f} {y:.1f}C{ex + 10:.1f} {y - 15:.1f} {tx - 10:.1f} {y - 15:.1f} {tx:.1f} {y:.1f}"
    dots = "".join(f'<circle fill="{INK}" cx="{x:.1f}" cy="{y:.1f}" r="4"/>' for x in (ex, tx))

    mark = (
        f'<path fill="{INK}" d="{path(e, 0)} {path(t, t_offset)}"/>'
        f'<path fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round" d="{arc}"/>{dots}'
    )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        f'<rect width="100" height="100" rx="22" fill="{PAPER}"/>{mark}</svg>\n'
    )
    public = ROOT / "public"
    (public / "favicon.svg").write_text(svg)

    def png(size):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "icon.html"
            page.write_text(f'<body style="margin:0"><img src="{(public / "favicon.svg").as_uri()}" width="{size}" height="{size}">')
            shot = Path(tmp) / "icon.png"
            subprocess.run(
                [CHROME, "--headless", "--hide-scrollbars", "--force-device-scale-factor=1",
                 "--default-background-color=00000000", f"--window-size={size},{size}",
                 f"--screenshot={shot}", page.as_uri()],
                check=True, capture_output=True,
            )
            return Image.open(shot).convert("RGBA").copy()

    # Apple fills the corners itself, so the touch icon is a full square of paper.
    touch = Image.new("RGBA", (180, 180), PAPER)
    touch.alpha_composite(png(180))
    touch.convert("RGB").save(public / "apple-touch-icon.png")
    big = png(256)
    big.save(public / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("wrote public/favicon.svg, public/apple-touch-icon.png, public/favicon.ico")


if __name__ == "__main__":
    main()
