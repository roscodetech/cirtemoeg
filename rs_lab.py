"""Fix s and r so their ink fits exactly in the x-height band [0, x] like o/c/e
(no half-stroke overshoot). Render candidates next to o for height comparison."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

from perfect_font.compile import compile_font
from perfect_font.glyphs.base import NARROW, ROUND, GlyphDef
from perfect_font.glyphs.parts import carc, vstem
from perfect_font.glyphs.lowercase import o as o_cur
from perfect_font.metrics import Metrics
from perfect_font.ufo_builder import build_ufo

OUT = Path("dist/lab")
SIZE = 520


def s_fixed(pen, m: Metrics) -> None:
    x, hs = m.x_height, m.half_stroke
    r = (x - m.stroke) / 4              # centreline radius so OUTER edges sit on [0, x]
    cx = r + hs
    top_cy = x - hs - r                 # outer top on the x-height line
    bot_cy = hs + r                     # outer bottom on the baseline
    carc(pen, m, cx, top_cy, r, 25, 270, cap1=True)
    carc(pen, m, cx, bot_cy, r, 90, -155)


def make_r(r_out_f, arm):
    def r(pen, m: Metrics) -> None:
        x, hs = m.x_height, m.half_stroke
        r_out = x * r_out_f
        r_ctr = r_out - hs
        cy = x - r_out                  # apex OUTER edge on the x-height line (no overshoot)
        cx = hs + r_ctr
        vstem(pen, m, hs, 0, cy)
        carc(pen, m, cx, cy, r_ctr, 180, arm, cap0=True)
    return r


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
    for y, c in [(baseline, "#cc3333"), (baseline - m.x_height * scale, "#3399cc"),
                 (baseline - cap, "#33aa55")]:
        d.line([(0, y), (w, y)], fill=c, width=2)
    d.text((pad, baseline), ch, font=font, fill="black", anchor="ls")
    d.text((6, h - 26), label, fill="black")
    return img


def one(fn, ch, uni, sp, label, m):
    gd = GlyphDef(ch, uni, fn, sp)
    font = build_ufo([gd], m, mono=False, family_name="Lab")
    paths = compile_font(font, OUT, stem="LabRS", formats=("ttf",))
    ttf = next(p for p in paths if p.suffix == ".ttf")
    return render(ttf, ch, m, label)


def montage(imgs, name):
    gap = 16
    H = max(i.height for i in imgs); W = sum(i.width for i in imgs) + gap*(len(imgs)-1)
    mon = Image.new("RGB", (W, H), "white"); x = 0
    for im in imgs:
        mon.paste(im, (x, 0)); x += im.width + gap
    mon.save(OUT / name)


def main():
    m = Metrics(); OUT.mkdir(parents=True, exist_ok=True)
    imgs = [one(o_cur, "o", 0x6F, ROUND, "o (ref 350)", m),
            one(s_fixed, "s", 0x73, ROUND, "s fixed", m),
            one(make_r(0.44, 25), "r", 0x72, NARROW, "r 0.44", m),
            one(make_r(0.40, 30), "r", 0x72, NARROW, "r 0.40", m),
            one(make_r(0.36, 35), "r", 0x72, NARROW, "r 0.36", m)]
    montage(imgs, "rs_fixed.png")
    print("wrote rs_fixed.png")


if __name__ == "__main__":
    main()
