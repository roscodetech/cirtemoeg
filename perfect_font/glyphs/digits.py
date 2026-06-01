"""Digits 0-9 (lining figures: full cap height)."""

from __future__ import annotations

from perfect_font.glyphs.base import ROUND, GlyphDef
from perfect_font.glyphs.parts import arc, arc_pt, carc, diag, hbar, joint, ring, vstem
from perfect_font.metrics import Metrics
from perfect_font.pens import draw_polygon, draw_stadium_ring, draw_stroke


def zero(pen, m: Metrics) -> None:
    cap = m.cap_height
    r = cap * 0.30
    straight = (cap - 2 * r) / 2
    draw_stadium_ring(pen, r, cap / 2, r, straight, m.stroke)


def one(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    xc = cap * 0.32
    vstem(pen, m, xc, 0, cap)                                   # main stem, flat top at cap
    # flag: a parallelogram. Upper edge from the stem-top-left out to the tip; lower edge
    # parallel one stroke below. Stays at/under the cap line -> no spike.
    tipx = xc - cap * 0.22
    s = m.stroke
    draw_polygon(pen, [
        (xc, cap),              # A: stem top-left, on the cap line
        (tipx, cap - s * 0.5),  # B: flag tip (upper)
        (tipx, cap - s * 1.5),  # C: flag tip (lower)
        (xc, cap - s),          # D: back on the stem face
    ])
    hbar(pen, m, xc - cap * 0.20, xc + cap * 0.20, hs)          # base serif foot


def two(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    r = cap * 0.27                                      # arc CENTRELINE radius
    w = cap * 0.58
    s = m.stroke
    cyy = cap - r - hs                                  # arc OUTER top == cap exactly
    cx = w - r - hs
    a_end = -42                                         # arc terminal angle (the shoulder)
    # The arc ends in a flat RADIAL cut (outer edge -> inner edge). Make the diagonal's TOP
    # edge BE that same radial cut, so arc and diagonal share one edge -> the shoulder is a
    # single CRISP corner with no faceting. The diagonal then runs parallel down to the base.
    outer = arc_pt(cx, cyy, r + hs, a_end)             # arc terminal: outer edge point
    inner = arc_pt(cx, cyy, r - hs, a_end)             # arc terminal: inner edge point
    off = (outer[0] - inner[0], outer[1] - inner[1])   # radial-cut vector (outer - inner)
    # The diagonal sweeps all the way down to the BOTTOM-LEFT corner: its outer (left) edge
    # lands on the baseline (y=0) at the left, where the base bar starts and runs right.
    foot_outer = (0.0, 0.0)                            # bottom-left corner, on the baseline
    foot_inner = (foot_outer[0] - off[0], foot_outer[1] - off[1])
    draw_polygon(pen, [outer, foot_outer, foot_inner, inner])
    carc(pen, m, cx, cyy, r, 195, a_end)               # arc; shares the radial edge -> clean
    hbar(pen, m, 0, w, hs)                             # base bar LAST, runs right from the foot


def three(pen, m: Metrics) -> None:
    cap = m.cap_height
    r = cap / 4  # both bowls share a radius and meet at the waist
    cx = r
    carc(pen, m, cx, cap - r, r, 150, -90, cap1=True)  # upper bowl -> waist
    carc(pen, m, cx, r, r, 90, -150)                   # waist -> lower bowl


def four(pen, m: Metrics) -> None:
    import math
    cap, hs = m.cap_height, m.half_stroke
    s = m.stroke
    w = cap * 0.62
    xv = w - cap * 0.20            # vertical-stem centre
    bar_y = cap * 0.30            # crossbar centre
    bar_top = bar_y + hs
    stem_l = xv - hs
    # Diagonal as ONE polygon with horizontal top/bottom edges. Its RIGHT edge runs from
    # the stem's top-left corner (stem_l, cap) down to a foot on the crossbar; the top
    # edge shares the stem's left edge (flush, no step), the bottom edge lies on the
    # crossbar top (flush, no step). Horizontal width keeps perpendicular thickness == s.
    foot_x = cap * 0.16
    dx, dy = foot_x - stem_l, bar_top - cap
    L = math.hypot(dx, dy)
    hw = s * L / abs(dy)          # horizontal width so perpendicular thickness == stroke
    draw_polygon(pen, [
        (stem_l, cap),            # right edge, top (on the stem's left edge)
        (foot_x, bar_top),        # right edge, bottom (on the crossbar top)
        (foot_x - hw, bar_top),   # left edge, bottom
        (stem_l - hw, cap),       # left edge, top
    ])
    vstem(pen, m, xv, 0, cap)                          # full vertical stem (orthogonal)
    hbar(pen, m, 0, w, bar_y)                          # full crossbar (orthogonal)


def five(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.56
    r = cap * 0.30
    cx = r
    stem_foot = cap * 0.52
    vstem(pen, m, hs, stem_foot, cap)        # upper-left stem (flat top at cap)
    hbar(pen, m, hs, w, cap - hs)            # top bar (sits at cap-hs, no spike)
    joint(pen, m, hs, cap - hs)
    # lower bowl: an arc bulging right. Start at the stem foot (overlap) and sweep down
    # round the bottom and up to the lower-left aperture.
    carc(pen, m, cx, r, r, 135, -150, cap0=True, cap1=True)
    joint(pen, m, hs, stem_foot)


def six(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    rb = cap * 0.32                 # bowl radius
    cx = rb
    bowl_cy = rb
    ring(pen, m, cx, bowl_cy, rb)   # bowl at the bottom
    # spine = the bowl's left wall continued straight up, then a top hook curving right.
    x_left = hs                     # left wall centreline
    hook_r = rb * 0.92              # top hook radius
    hook_cy = cap - hook_r
    vstem(pen, m, x_left, bowl_cy, hook_cy)             # near-vertical left stem
    carc(pen, m, x_left + hook_r, hook_cy, hook_r, 180, 20, cap0=True, cap1=True)  # top hook
    joint(pen, m, x_left, bowl_cy)


def seven(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.58
    hbar(pen, m, 0, w, cap - hs)
    diag(pen, m, (w, cap - hs), (cap * 0.14, 0.0))
    joint(pen, m, w, cap - hs)


def eight(pen, m: Metrics) -> None:
    cap = m.cap_height
    r_top, r_bot = cap * 0.235, cap * 0.30
    cx = r_bot
    # place centres so the rings OVERLAP at the waist (centre gap < r_top + r_bot - stroke),
    # otherwise tangent circles leave a hairline gap and read as disconnected.
    waist = cap * 0.52
    ring(pen, m, cx, waist + r_top - m.stroke * 0.4, r_top)   # upper ring, dropped down
    ring(pen, m, cx, waist - r_bot + m.stroke * 0.4, r_bot)   # lower ring, raised up


def nine(pen, m: Metrics) -> None:
    # 180-deg mirror of six: bowl at the top, right wall continued down, hook curving left.
    cap, hs = m.cap_height, m.half_stroke
    rb = cap * 0.32
    cx = rb
    bowl_cy = cap - rb
    ring(pen, m, cx, bowl_cy, rb)         # bowl at the top
    x_right = 2 * rb - hs                  # right wall centreline
    hook_r = rb * 0.92
    hook_cy = hook_r
    vstem(pen, m, x_right, hook_cy, bowl_cy)            # near-vertical right stem
    carc(pen, m, x_right - hook_r, hook_cy, hook_r, 0, -160, cap0=True, cap1=True)  # foot hook
    joint(pen, m, x_right, bowl_cy)


DIGITS: list[GlyphDef] = [
    GlyphDef("zero", 0x30, zero, ROUND),
    GlyphDef("one", 0x31, one, ROUND),
    GlyphDef("two", 0x32, two, ROUND),
    GlyphDef("three", 0x33, three, ROUND),
    GlyphDef("four", 0x34, four, ROUND),
    GlyphDef("five", 0x35, five, ROUND),
    GlyphDef("six", 0x36, six, ROUND),
    GlyphDef("seven", 0x37, seven, ROUND),
    GlyphDef("eight", 0x38, eight, ROUND),
    GlyphDef("nine", 0x39, nine, ROUND),
]
