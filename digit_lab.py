"""Redesign digits 1 (clean flag, no top poke) and 2 (clean bottom-left)."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

from perfect_font.compile import compile_font
from perfect_font.glyphs.base import ROUND, GlyphDef
from perfect_font.glyphs.parts import arc_pt, carc, hbar, joint, vstem
from perfect_font.metrics import Metrics
from perfect_font.pens import draw_polygon, draw_stroke
from perfect_font.ufo_builder import build_ufo

OUT = Path("dist/lab")
SIZE = 560


def one_a(pen, m: Metrics) -> None:
    # flag attaches along the stem's LEFT edge (top-left corner) -> no poke
    cap, hs, s = m.cap_height, m.half_stroke, m.stroke
    xc = cap * 0.34
    vstem(pen, m, xc, 0, cap)
    tipx = xc - hs - cap * 0.20
    draw_polygon(pen, [
        (xc - hs, cap),          # stem top-left corner
        (tipx, cap - s * 0.7),   # tip upper
        (tipx, cap - s * 1.7),   # tip lower
        (xc - hs, cap - s),      # stem left face
    ])
    hbar(pen, m, xc - cap * 0.20, xc + cap * 0.20, hs)


def one_b(pen, m: Metrics) -> None:
    # flag as a proper constant-width diagonal beak, tip on the cap line, overlapping the stem
    cap, hs, s = m.cap_height, m.half_stroke, m.stroke
    xc = cap * 0.34
    vstem(pen, m, xc, 0, cap)
    tip = (xc - cap * 0.22, cap - hs)        # upper-left beak tip
    draw_stroke(pen, tip, (xc, cap - s * 1.6), s)  # diagonal into the stem
    joint(pen, m, xc, cap - s * 1.6)
    hbar(pen, m, xc - cap * 0.20, xc + cap * 0.20, hs)


def two_a(pen, m: Metrics) -> None:
    # diagonal as a constant-width stroke resting in the base bar; base bar's left = bottom-left
    cap, hs, s = m.cap_height, m.half_stroke, m.stroke
    r = cap * 0.27
    w = cap * 0.58
    cyy = cap - r - hs
    cx = w - r - hs
    a_end = -42
    term = arc_pt(cx, cyy, r, a_end)          # arc centreline terminal
    foot = (hs + cap * 0.04, hs)              # foot sits in the base bar, near the left
    draw_stroke(pen, term, foot, s)
    joint(pen, m, *foot)
    carc(pen, m, cx, cyy, r, 195, a_end, cap1=True)
    joint(pen, m, *term)
    hbar(pen, m, 0, w, hs)


def two_b(pen, m: Metrics) -> None:
    # diagonal polygon with a horizontal foot flush on the base-bar top (y = stroke)
    cap, hs, s = m.cap_height, m.half_stroke, m.stroke
    r = cap * 0.27
    w = cap * 0.58
    cyy = cap - r - hs
    cx = w - r - hs
    a_end = -42
    outer = arc_pt(cx, cyy, r + hs, a_end)
    inner = arc_pt(cx, cyy, r - hs, a_end)
    # left edge from outer down to (0, s); right edge from inner down to (foot_w, s)
    foot_left = (0.0, s)
    foot_right = (inner[0] - outer[0] + foot_left[0] + s * 1.2, s)
    draw_polygon(pen, [outer, inner, foot_right, foot_left])
    carc(pen, m, cx, cyy, r, 195, a_end, cap1=True)
    hbar(pen, m, 0, w, hs)


def render(ttf, ch, m, label):
    scale = SIZE / m.upm
    cap = m.cap_height * scale
    font = ImageFont.truetype(str(ttf), SIZE)
    pad = 70
    w = int(m.upm * scale) + pad * 2
    h = int(m.cap_height * scale) + pad * 2 + 30
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    baseline = pad + cap
    for y, c in [(baseline, "#cc3333"), (baseline - cap, "#33aa55")]:
        d.line([(0, y), (w, y)], fill=c, width=2)
    d.text((pad, baseline), ch, font=font, fill="black", anchor="ls")
    d.text((6, h - 26), label, fill="black")
    return img


def one(fn, ch, uni, label, m):
    gd = GlyphDef("d", uni, fn, ROUND)
    font = build_ufo([gd], m, mono=False, family_name="Lab")
    paths = compile_font(font, OUT, stem="LabDig", formats=("ttf",))
    ttf = next(p for p in paths if p.suffix == ".ttf")
    return render(ttf, ch, m, label)


def montage(imgs, name):
    gap = 16
    H = max(i.height for i in imgs); W = sum(i.width for i in imgs)+gap*(len(imgs)-1)
    mon = Image.new("RGB", (W, H), "white"); x = 0
    for im in imgs:
        mon.paste(im, (x, 0)); x += im.width + gap
    mon.save(OUT / name)


def main():
    m = Metrics(); OUT.mkdir(parents=True, exist_ok=True)
    imgs = [one(one_a, "1", 0x31, "1a edge", m),
            one(one_b, "1", 0x31, "1b beak", m),
            one(two_a, "2", 0x32, "2a stroke", m),
            one(two_b, "2", 0x32, "2b poly", m)]
    montage(imgs, "digit_variants.png")
    print("wrote digit_variants.png")


if __name__ == "__main__":
    main()
