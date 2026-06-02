"""Render candidate glyph recipes side by side to choose geometry before editing
the real modules. Pure preview: defines candidate functions locally."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

from perfect_font.compile import compile_font
from perfect_font.glyphs.base import GlyphDef, NARROW, ROUND
from perfect_font.glyphs.parts import carc, vstem
from perfect_font.glyphs.lowercase import _bowl, n
from perfect_font.metrics import Metrics
from perfect_font.pens import draw_disc
from perfect_font.ufo_builder import build_ufo

OUT = Path("dist/lab")
SIZE = 520


# ---- candidate r recipes (arm-end angle varies) ----
def make_r(arm_end: float, r_factor: float = 0.44):
    def r(pen, m: Metrics) -> None:
        x, hs = m.x_height, m.half_stroke
        r_a = x * r_factor
        cy = x - r_a
        cx = hs + r_a
        vstem(pen, m, hs, 0, x)
        carc(pen, m, cx, cy, r_a, 180, arm_end, cap0=True)
    return r


# ---- candidate s (mirror bottom = 180deg rotation of top) ----
def s_fixed(pen, m: Metrics) -> None:
    x = m.x_height
    r = x / 4
    cx = r
    carc(pen, m, cx, x - r, r, 25, 270, cap1=True)
    carc(pen, m, cx, r, r, 90, -155)


# ---- candidate g/j with shared tail ----
TAIL_R = 0.42


def g_fixed(pen, m: Metrics) -> None:
    r, cy = _bowl(pen, m)
    xc = 2 * r - m.half_stroke
    tr = m.x_height * TAIL_R
    ctr_y = m.descender + tr + m.half_stroke
    vstem(pen, m, xc, ctr_y, m.x_height)
    carc(pen, m, xc - tr, ctr_y, tr, 0, -180, cap0=True)


def j_fixed(pen, m: Metrics) -> None:
    hs = m.half_stroke
    tr = m.x_height * TAIL_R
    xc = 2 * tr - hs
    ctr_y = m.descender + tr + hs
    vstem(pen, m, xc, ctr_y, m.x_height)
    carc(pen, m, xc - tr, ctr_y, tr, 0, -180, cap0=True)
    draw_disc(pen, xc, m.x_height + m.stroke * 0.55 + hs, hs)


def render(ttf: Path, ch: str, m: Metrics, label: str) -> Image.Image:
    scale = SIZE / m.upm
    cap = m.cap_height * scale
    xh = m.x_height * scale
    desc = -m.descender * scale
    font = ImageFont.truetype(str(ttf), SIZE)
    pad = 90
    w = int(m.upm * scale) + pad * 2
    h = int((m.cap_height - m.descender) * scale) + pad * 2 + 30
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    baseline = pad + cap
    for y, color in [(baseline, "#cc3333"), (baseline - xh, "#3399cc"),
                     (baseline - cap, "#33aa55"), (baseline + desc, "#cc9933")]:
        d.line([(0, y), (w, y)], fill=color, width=2)
    d.text((pad, baseline), ch, font=font, fill="black", anchor="ls")
    d.text((6, h - 26), label, fill="black")
    return img


def montage(imgs, path):
    gap = 16
    H = max(i.height for i in imgs)
    W = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
    m = Image.new("RGB", (W, H), "white")
    x = 0
    for im in imgs:
        m.paste(im, (x, 0))
        x += im.width + gap
    m.save(path)


def build_and_render(defs, m):
    font = build_ufo(defs, m, mono=False, family_name="Lab")
    paths = compile_font(font, OUT, stem="LabV", formats=("ttf",))
    return next(p for p in paths if p.suffix == ".ttf")


def main() -> None:
    m = Metrics()
    OUT.mkdir(parents=True, exist_ok=True)

    # r variants: arm-end angle sweep
    imgs = []
    for end in (40, 25, 12, 0, -12):
        gd = GlyphDef("r", 0x72, make_r(end), NARROW)
        nd = GlyphDef("n", 0x6E, n, NARROW)
        ttf = build_and_render([gd, nd], m)
        imgs.append(render(ttf, "r", m, f"arm_end={end}"))
    # append n reference
    ttf = build_and_render([GlyphDef("n", 0x6E, n, NARROW)], m)
    imgs.append(render(ttf, "n", m, "n (ref)"))
    montage(imgs, OUT / "r_variants.png")

    # s fixed vs nothing
    ttf = build_and_render([GlyphDef("s", 0x73, s_fixed, ROUND)], m)
    montage([render(ttf, "s", m, "s fixed")], OUT / "s_fixed.png")

    # g/j shared tail
    gd = GlyphDef("g", 0x67, g_fixed, ROUND)
    jd = GlyphDef("j", 0x6A, j_fixed, NARROW)
    ttf = build_and_render([gd, jd], m)
    montage([render(ttf, "g", m, "g fixed"), render(ttf, "j", m, "j fixed")],
            OUT / "gj_fixed.png")
    print("wrote r_variants.png, s_fixed.png, gj_fixed.png")


if __name__ == "__main__":
    main()
