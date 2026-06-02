"""Visual lab: compile an arbitrary set of glyph recipes and render each one BIG
with metric guide lines, so geometry/symmetry fixes can be eyeballed precisely.

    python glyph_lab.py sgrj          # render current s,g,r,j (one PNG each + montage)

The recipes come straight from the live modules, so what you see is exactly what
the compiled font produces (real skia-pathops union, real flattening).
"""

from __future__ import annotations

import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

from perfect_font.compile import compile_font
from perfect_font.glyphs import REGISTRY
from perfect_font.metrics import Metrics
from perfect_font.ufo_builder import build_ufo

OUT = Path("dist/lab")
SIZE = 600  # px per em -> huge glyphs


def render_one(ttf: Path, ch: str, m: Metrics) -> Image.Image:
    scale = SIZE / m.upm
    cap = m.cap_height * scale
    xh = m.x_height * scale
    desc = -m.descender * scale
    font = ImageFont.truetype(str(ttf), SIZE)

    pad = 120
    w = int(m.upm * scale) + pad * 2
    h = int((m.cap_height - m.descender) * scale) + pad * 2
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    baseline = pad + cap
    guides = [
        (baseline, "#cc3333", "base"),
        (baseline - xh, "#3399cc", "x"),
        (baseline - cap, "#33aa55", "cap"),
        (baseline + desc, "#cc9933", "desc"),
    ]
    for y, color, _ in guides:
        d.line([(0, y), (w, y)], fill=color, width=2)
    # vertical centre guide of the advance cell
    d.text((pad, baseline), ch, font=font, fill="black", anchor="ls")
    return img


def main() -> None:
    chars = sys.argv[1] if len(sys.argv) > 1 else "sgrj"
    m = Metrics()
    subset = [REGISTRY[c] for c in chars if c in REGISTRY]
    font = build_ufo(subset, m, mono=False, family_name="Lab")
    OUT.mkdir(parents=True, exist_ok=True)
    paths = compile_font(font, OUT, stem="Lab", formats=("ttf",))
    ttf = next(p for p in paths if p.suffix == ".ttf")

    imgs = [render_one(ttf, c, m) for c in chars if c in REGISTRY]
    for c, im in zip([c for c in chars if c in REGISTRY], imgs):
        im.save(OUT / f"glyph_{c}.png")
    # montage
    gap = 20
    H = max(i.height for i in imgs)
    W = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
    montage = Image.new("RGB", (W, H), "white")
    x = 0
    for im in imgs:
        montage.paste(im, (x, 0))
        x += im.width + gap
    montage.save(OUT / f"montage_{chars}.png")
    print(f"wrote {OUT}/montage_{chars}.png and per-glyph PNGs")


if __name__ == "__main__":
    main()
