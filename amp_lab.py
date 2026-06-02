"""Ampersand iteration lab: render the current & next to refined candidates so we can
converge on a cleaner, more congruent (balanced/regular) self-crossing form.

The roughness in the current & is that the crossing diagonals use horizontal end-cuts
(diag) whose width exceeds the stroke on a steep slope, so their tops/feet poke past the
closing arcs as little fangs. The refinements:
  * close each loop with an arc that sweeps a bit PAST 180 deg so its ends curl inward and
    cover the diagonal terminals (no fangs);
  * balance the two loops (small-but-round top, larger bottom) and centre the crossing;
  * give the tail a consistent ball terminal.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

from perfect_font.compile import compile_font
from perfect_font.glyphs.base import ROUND, GlyphDef
from perfect_font.glyphs.parts import carc, diag, joint
from perfect_font.metrics import Metrics
from perfect_font.pens import draw_disc, draw_stroke
from perfect_font.ufo_builder import build_ufo

OUT = Path("dist/lab")
SIZE = 760


def amp_current(pen, m: Metrics) -> None:
    cap = m.cap_height
    ul = (0.24 * cap, 0.70 * cap)
    ur = (0.50 * cap, 0.70 * cap)
    ll = (0.15 * cap, 0.16 * cap)
    lr = (0.55 * cap, 0.16 * cap)
    tip = (0.74 * cap, 0.40 * cap)
    diag(pen, m, ul, lr)
    diag(pen, m, ur, ll)
    carc(pen, m, (ul[0] + ur[0]) / 2, ul[1], (ur[0] - ul[0]) / 2, 0, 180)
    joint(pen, m, *ul)
    joint(pen, m, *ur)
    carc(pen, m, (ll[0] + lr[0]) / 2, ll[1], (lr[0] - ll[0]) / 2, 180, 360)
    joint(pen, m, *ll)
    joint(pen, m, *lr)
    diag(pen, m, lr, tip)
    joint(pen, m, *lr)
    draw_disc(pen, tip[0], tip[1], m.half_stroke)


def make_amp(p):
    """Parametric refined ampersand. p is a dict of cap-fractions."""
    def amp(pen, m: Metrics) -> None:
        cap = m.cap_height
        # loop centres + radii (centreline)
        rt = p["rt"] * cap                       # top loop radius
        rb = p["rb"] * cap                       # bottom bowl radius
        cxt = p["cxt"] * cap                      # top loop centre x
        cxb = p["cxb"] * cap                      # bottom bowl centre x
        cyt = p["top"] * cap - rt                 # top loop centre y (top edge at p[top])
        cyb = p["bot"] * cap + rb                 # bottom bowl centre y (bottom edge at p[bot])
        over = p["over"]                          # extra arc sweep beyond 180 (deg), covers fangs
        # upper-loop arc ends (springs) + lower-bowl arc ends
        ul = (cxt - rt, cyt)
        ur = (cxt + rt, cyt)
        ll = (cxb - rb, cyb)
        lr = (cxb + rb, cyb)
        # the X: each diagonal joins an upper spring to the OPPOSITE lower spring.
        # draw_stroke gives exactly stroke-wide perpendicular caps (no over-wide horizontal
        # cut), so the hs joint discs fully weld each terminal -> no fangs.
        draw_stroke(pen, ul, lr, m.stroke)        # '\'
        draw_stroke(pen, ur, ll, m.stroke)        # '/'
        # close the loops with clean semicircles springing exactly off the diagonal ends
        carc(pen, m, cxt, cyt, rt, 0, 180)
        carc(pen, m, cxb, cyb, rb, 180, 360)
        for pt in (ul, ur, ll, lr):
            joint(pen, m, *pt)
        # tail off the lower-right spring, flicking out to a ball terminal
        tip = (p["tipx"] * cap, p["tipy"] * cap)
        draw_stroke(pen, lr, tip, m.stroke)
        joint(pen, m, *lr)
        draw_disc(pen, tip[0], tip[1], m.half_stroke)
    return amp


CANDIDATES = {
    "current": amp_current,
    "balanced": make_amp(dict(rt=0.15, rb=0.23, cxt=0.37, cxb=0.37, top=0.82, bot=0.02,
                              over=18, tipx=0.74, tipy=0.40)),
    "rounder": make_amp(dict(rt=0.17, rb=0.25, cxt=0.34, cxb=0.38, top=0.86, bot=0.0,
                             over=25, tipx=0.76, tipy=0.34)),
    "tighter": make_amp(dict(rt=0.14, rb=0.22, cxt=0.36, cxb=0.36, top=0.80, bot=0.04,
                             over=12, tipx=0.72, tipy=0.42)),
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
    d.text((pad, baseline), "&", font=font, fill="black", anchor="ls")
    d.text((6, h - 26), label, fill="black")
    return img


def main() -> None:
    m = Metrics()
    OUT.mkdir(parents=True, exist_ok=True)
    import sys
    sel = sys.argv[1:] if len(sys.argv) > 1 else list(CANDIDATES)
    imgs = []
    for name in sel:
        fn = CANDIDATES[name]
        gd = GlyphDef("ampersand", 0x26, fn, ROUND)
        font = build_ufo([gd], m, mono=False, family_name="Lab")
        paths = compile_font(font, OUT, stem="LabAmp", formats=("ttf",))
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
    mon.save(OUT / "amp_variants.png")
    print("wrote amp_variants.png")


if __name__ == "__main__":
    main()
