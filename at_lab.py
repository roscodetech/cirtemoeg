"""@ iteration lab: outer shell open at the lower-right with a clean tail, wrapping a
legible small lowercase 'a' (bowl with a real counter + right stem)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

from perfect_font.compile import compile_font
from perfect_font.glyphs.base import ROUND, GlyphDef
from perfect_font.glyphs.parts import arc_pt, carc, joint, ring, vstem
from perfect_font.metrics import Metrics
from perfect_font.pens import draw_disc, draw_stroke
from perfect_font.ufo_builder import build_ufo

OUT = Path("dist/lab")
SIZE = 900


def at_current(pen, m: Metrics) -> None:
    from perfect_font.glyphs.parts import diag
    cap = m.cap_height
    cx = cy = cap * 0.5
    R = cap * 0.45
    carc(pen, m, cx, cy, R, -25, 250)
    t0 = arc_pt(cx, cy, R, -25)
    diag(pen, m, t0, (cx + R * 1.05, cy - R * 0.1))
    rb = cap * 0.17
    bx = cx - cap * 0.02
    ring(pen, m, bx, cy, rb)
    vstem(pen, m, bx + rb - m.half_stroke, cy - rb, cy + rb)


def make_at(p):
    def at(pen, m: Metrics) -> None:
        cap, hs = m.cap_height, m.half_stroke
        cx = cy = cap * 0.5
        R = p["R"] * cap                       # outer shell centreline radius
        a0, a1 = p["a0"], p["a1"]              # shell open at the lower-right (gap a1..a0+360)
        carc(pen, m, cx, cy, R, a0, a1)
        # tail: a short flick OUT from the shell's lower-right end (slightly clockwise of a0
        # and further out), ending in a ball terminal -- kept clear of the inner 'a'.
        start = arc_pt(cx, cy, R, a0)
        ta = math.radians(a0 - p["tdrop"])
        tip = (cx + R * p["text"] * math.cos(ta), cy + R * p["text"] * math.sin(ta))
        draw_stroke(pen, start, tip, m.stroke)
        joint(pen, m, *start)
        draw_disc(pen, tip[0], tip[1], hs)
        # inner lowercase 'a': bowl ring (outer radius rb) + right stem, centred
        rb = p["rb"] * cap
        bx = cx + p["bxoff"] * cap
        ring(pen, m, bx, cy, rb)
        vstem(pen, m, bx + rb - hs, cy - rb, cy + rb)
    return at


CANDIDATES = {
    "current": at_current,
    "a": make_at(dict(R=0.43, a0=-42, a1=250, rb=0.20, bxoff=-0.03, tdrop=6, text=1.32)),
    "b": make_at(dict(R=0.44, a0=-38, a1=248, rb=0.21, bxoff=-0.04, tdrop=10, text=1.30)),
    "c": make_at(dict(R=0.43, a0=-48, a1=252, rb=0.19, bxoff=-0.03, tdrop=2, text=1.36)),
}


def render(ttf: Path, m: Metrics, label: str) -> Image.Image:
    scale = SIZE / m.upm
    cap = m.cap_height * scale
    font = ImageFont.truetype(str(ttf), SIZE)
    pad = 70
    w = int(m.upm * scale) + pad * 2
    h = int(m.cap_height * scale) + pad * 2 + 30
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    baseline = pad + cap
    for y, c in [(baseline, "#cc3333"), (baseline - cap, "#33aa55"),
                 (baseline - m.x_height * scale, "#3399cc")]:
        d.line([(0, y), (w, y)], fill=c, width=2)
    d.text((pad, baseline), "@", font=font, fill="black", anchor="ls")
    d.text((6, h - 26), label, fill="black")
    return img


def main() -> None:
    m = Metrics()
    OUT.mkdir(parents=True, exist_ok=True)
    sel = sys.argv[1:] if len(sys.argv) > 1 else list(CANDIDATES)
    imgs = []
    for name in sel:
        gd = GlyphDef("at", 0x40, CANDIDATES[name], ROUND)
        font = build_ufo([gd], m, mono=False, family_name="Lab")
        paths = compile_font(font, OUT, stem="LabAt", formats=("ttf",))
        ttf = next(p for p in paths if p.suffix == ".ttf")
        imgs.append(render(ttf, m, name))
    gap = 16
    H = max(i.height for i in imgs)
    W = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
    mon = Image.new("RGB", (W, H), "white")
    x = 0
    for im in imgs:
        mon.paste(im, (x, 0))
        x += im.width + gap
    mon.save(OUT / "at_variants.png")
    print("wrote at_variants.png")


if __name__ == "__main__":
    main()
