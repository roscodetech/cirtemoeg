"""Candidate redesigns of the digit 4: solid top (diagonal overlaps the stem) and a
flush, spike-free lower-left (crossbar left edge under the diagonal foot)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

from perfect_font.compile import compile_font
from perfect_font.glyphs.base import ROUND, GlyphDef
from perfect_font.glyphs.parts import hbar, joint, vstem
from perfect_font.metrics import Metrics
from perfect_font.pens import draw_polygon
from perfect_font.ufo_builder import build_ufo

OUT = Path("dist/lab")
SIZE = 520


def make_four(foot_rx_f: float, bar_y_f: float = 0.30, w_f: float = 0.62):
    def four(pen, m: Metrics) -> None:
        cap, hs, s = m.cap_height, m.half_stroke, m.stroke
        w = cap * w_f
        xv = w - cap * 0.20            # stem centre
        bar_y = cap * bar_y_f
        bar_top = bar_y + hs
        TRx = xv + hs                  # diagonal top-right == stem top-right -> solid peak
        foot_rx = cap * foot_rx_f
        dx, dy = foot_rx - TRx, bar_top - cap
        L = math.hypot(dx, dy)
        hw = s * L / abs(dy)           # horizontal width so perpendicular thickness == stroke
        TR = (TRx, cap)
        BR = (foot_rx, bar_top)
        BL = (foot_rx - hw, bar_top)
        TL = (TRx - hw, cap)
        draw_polygon(pen, [TR, BR, BL, TL])
        vstem(pen, m, xv, 0, cap)
        hbar(pen, m, BL[0], w, bar_y)  # crossbar left edge flush under the diagonal foot
    return four


def render(ttf: Path, m: Metrics, label: str) -> Image.Image:
    scale = SIZE / m.upm
    cap = m.cap_height * scale
    font = ImageFont.truetype(str(ttf), SIZE)
    pad = 80
    w = int(m.upm * scale) + pad * 2
    h = int(m.cap_height * scale) + pad * 2 + 30
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    baseline = pad + cap
    for y, c in [(baseline, "#cc3333"), (baseline - cap, "#33aa55")]:
        d.line([(0, y), (w, y)], fill=c, width=2)
    d.text((pad, baseline), "4", font=font, fill="black", anchor="ls")
    d.text((6, h - 26), label, fill="black")
    return img


def main() -> None:
    m = Metrics()
    OUT.mkdir(parents=True, exist_ok=True)
    imgs = []
    for f in (0.16, 0.18, 0.20):
        gd = GlyphDef("four", 0x34, make_four(f), ROUND)
        font = build_ufo([gd], m, mono=False, family_name="Lab")
        paths = compile_font(font, OUT, stem="LabFour", formats=("ttf",))
        ttf = next(p for p in paths if p.suffix == ".ttf")
        imgs.append(render(ttf, m, f"foot_rx={f}"))
    gap = 16
    H = max(i.height for i in imgs)
    W = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
    mon = Image.new("RGB", (W, H), "white")
    x = 0
    for im in imgs:
        mon.paste(im, (x, 0))
        x += im.width + gap
    mon.save(OUT / "four_variants.png")
    print("wrote four_variants.png")


if __name__ == "__main__":
    main()
