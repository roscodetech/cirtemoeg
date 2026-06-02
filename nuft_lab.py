"""Compare: (1) current n vs a symmetric-arch n (mirror of u, no left notch);
(2) f/t crossbars at matched widths."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

from perfect_font.compile import compile_font
from perfect_font.glyphs.base import FLAT, NARROW, GlyphDef
from perfect_font.glyphs.parts import carc, half_bottom, half_top, hbar, vstem
from perfect_font.glyphs.lowercase import n as n_cur, u as u_cur, f as f_cur, t as t_cur
from perfect_font.metrics import Metrics
from perfect_font.ufo_builder import build_ufo
from perfect_font.compile import compile_font as _cf

OUT = Path("dist/lab")
SIZE = 520


def n_sym(pen, m: Metrics) -> None:
    """Symmetric-arch n: both stems spring from the arch (0..cy) -> clean dome, no notch."""
    x, hs = m.x_height, m.half_stroke
    w = x * 0.88
    r_a = w / 2
    cy = x - r_a
    vstem(pen, m, hs, 0, cy)
    half_top(pen, m, w / 2, cy, r_a)
    vstem(pen, m, w - hs, 0, cy)


def make_f(half):
    def f(pen, m: Metrics) -> None:
        x, hs = m.x_height, m.half_stroke
        r = x * 0.42
        xc = r + hs
        vstem(pen, m, xc, 0, m.cap_height - r)
        carc(pen, m, xc + r, m.cap_height - r, r, 180, 90, cap0=True)
        hbar(pen, m, xc - half, xc + half, x - hs)
    return f


def make_t(half):
    def t(pen, m: Metrics) -> None:
        x, hs = m.x_height, m.half_stroke
        r_a = x * 0.34
        xc = x * 0.34
        vstem(pen, m, xc, r_a, x * 1.42)
        hbar(pen, m, xc - half, xc + half, x - hs)
        carc(pen, m, xc + r_a, r_a, r_a, 180, 270, cap0=True)
    return t


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
    for y, c in [(baseline, "#cc3333"), (baseline - cap, "#33aa55"),
                 (baseline - m.x_height * scale, "#3399cc")]:
        d.line([(0, y), (w, y)], fill=c, width=2)
    d.text((pad, baseline), ch, font=font, fill="black", anchor="ls")
    d.text((6, h - 26), label, fill="black")
    return img


def one(fn, ch, uni, spacing, label, m):
    gd = GlyphDef(ch, uni, fn, spacing)
    font = build_ufo([gd], m, mono=False, family_name="Lab")
    paths = _cf(font, OUT, stem="LabNUFT", formats=("ttf",))
    ttf = next(p for p in paths if p.suffix == ".ttf")
    return render(ttf, ch, m, label)


def montage(imgs, name):
    gap = 16
    H = max(i.height for i in imgs)
    W = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
    mon = Image.new("RGB", (W, H), "white")
    x = 0
    for im in imgs:
        mon.paste(im, (x, 0))
        x += im.width + gap
    mon.save(OUT / name)


def main():
    m = Metrics()
    OUT.mkdir(parents=True, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "n"
    if mode == "n":
        imgs = [one(n_cur, "n", 0x6E, FLAT, "n current", m),
                one(n_sym, "n", 0x6E, FLAT, "n symmetric", m),
                one(u_cur, "u", 0x75, FLAT, "u (ref)", m)]
        montage(imgs, "n_compare.png")
        print("wrote n_compare.png")
    else:
        # f/t crossbar halves to test matched widths
        imgs = [one(f_cur, "f", 0x66, NARROW, "f current(169)", m),
                one(make_f(119), "f", 0x66, NARROW, "f half=119", m),
                one(t_cur, "t", 0x74, NARROW, "t current(119)", m),
                one(make_t(119), "t", 0x74, NARROW, "t half=119", m)]
        montage(imgs, "ft_compare.png")
        print("wrote ft_compare.png")


if __name__ == "__main__":
    main()
