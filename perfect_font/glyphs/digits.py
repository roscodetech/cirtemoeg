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
    cap, hs, s = m.cap_height, m.half_stroke, m.stroke
    xc = cap * 0.34
    vstem(pen, m, xc, 0, cap)                                   # main stem, flat top at cap
    # flag: a parallelogram attached along the stem's LEFT EDGE (so the stem's flat top
    # stays clean -- no top-left corner poking above the flag) and slanting down to the tip.
    tipx = xc - hs - cap * 0.20
    draw_polygon(pen, [
        (xc - hs, cap),          # stem top-left corner (flag springs from here)
        (tipx, cap - s * 0.7),   # flag tip (upper)
        (tipx, cap - s * 1.7),   # flag tip (lower)
        (xc - hs, cap - s),      # back on the stem's left face
    ])
    hbar(pen, m, xc - cap * 0.20, xc + cap * 0.20, hs)          # base serif foot


def two(pen, m: Metrics) -> None:
    cap, hs, s = m.cap_height, m.half_stroke, m.stroke
    r = cap * 0.27                                      # arc CENTRELINE radius
    w = cap * 0.58
    cyy = cap - r - hs                                  # arc OUTER top == cap exactly
    cx = w - r - hs
    a_end = -42                                         # arc terminal angle (the shoulder)
    # Diagonal spine: a constant-width stroke from the arc terminal down into the base bar
    # (foot buried near the left so the base bar's own square corner is the clean bottom-left).
    term = arc_pt(cx, cyy, r, a_end)                   # arc CENTRELINE terminal
    foot = (hs + cap * 0.04, hs)                       # foot sits inside the base bar
    draw_stroke(pen, term, foot, s)
    joint(pen, m, *foot)
    carc(pen, m, cx, cyy, r, 195, a_end, cap1=True)    # arc; welded to the spine at the terminal
    joint(pen, m, *term)
    hbar(pen, m, 0, w, hs)                             # base bar -> clean square bottom-left


def three(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    r = (cap - m.stroke) / 4  # centreline radius so OUTER edges sit on [0, cap] (no overshoot)
    cx = r + hs
    top_cy = cap - hs - r
    bot_cy = hs + r
    carc(pen, m, cx, top_cy, r, 150, -90, cap1=True)  # upper bowl -> waist
    carc(pen, m, cx, bot_cy, r, 90, -150)             # waist -> lower bowl


def four(pen, m: Metrics) -> None:
    import math
    cap, hs = m.cap_height, m.half_stroke
    s = m.stroke
    w = cap * 0.62
    xv = w - cap * 0.20            # vertical-stem centre
    bar_y = cap * 0.30            # crossbar centre
    bar_top = bar_y + hs
    # Diagonal as ONE polygon with horizontal top/bottom edges. Its top-right corner sits on
    # the stem's top-RIGHT corner, so the diagonal OVERLAPS the whole stem top -> a solid,
    # gap-free peak (no white slit running up to the cap line). The foot lands on the crossbar
    # top, and the crossbar starts flush under the diagonal's outer foot -> a clean, spike-free
    # lower-left corner. Horizontal width keeps perpendicular thickness == stroke.
    TRx = xv + hs                 # diagonal top-right == stem top-right
    foot_rx = cap * 0.18          # diagonal foot (inner/right edge) on the crossbar
    dx, dy = foot_rx - TRx, bar_top - cap
    L = math.hypot(dx, dy)
    hw = s * L / abs(dy)
    bl_x = foot_rx - hw           # diagonal outer foot == crossbar left edge
    draw_polygon(pen, [
        (TRx, cap),               # right edge, top (on the stem's right edge)
        (foot_rx, bar_top),       # right edge, bottom (on the crossbar top)
        (bl_x, bar_top),          # left edge, bottom
        (TRx - hw, cap),          # left edge, top
    ])
    vstem(pen, m, xv, 0, cap)                          # full vertical stem (orthogonal)
    hbar(pen, m, bl_x, w, bar_y)                       # crossbar, flush under the diagonal foot


def five(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.56
    r = cap * 0.30
    cx = r
    stem_foot = cap * 0.52
    bowl_cy = r + hs                         # bowl OUTER bottom on the baseline (no overshoot)
    vstem(pen, m, hs, stem_foot, cap)        # upper-left stem (flat top at cap)
    hbar(pen, m, hs, w, cap - hs)            # top bar (sits at cap-hs, no spike)
    joint(pen, m, hs, cap - hs)
    # lower bowl: an arc bulging right. Start at the stem foot (overlap) and sweep down
    # round the bottom and up to the lower-left aperture.
    carc(pen, m, cx, bowl_cy, r, 135, -150, cap0=True, cap1=True)
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
    hook_cy = cap - hook_r - hs     # hook OUTER apex on the cap line (no overshoot)
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
    # rings sit on the metric lines (top edge at cap, bottom edge at baseline) and overlap
    # at the waist (top ring bottom = cap-2*r_top, below bottom ring top = 2*r_bot).
    ring(pen, m, cx, cap - r_top, r_top)   # upper ring: top edge on the cap line
    ring(pen, m, cx, r_bot, r_bot)         # lower ring: bottom edge on the baseline


def nine(pen, m: Metrics) -> None:
    # 180-deg mirror of six: bowl at the top, right wall continued down, hook curving left.
    cap, hs = m.cap_height, m.half_stroke
    rb = cap * 0.32
    cx = rb
    bowl_cy = cap - rb
    ring(pen, m, cx, bowl_cy, rb)         # bowl at the top
    x_right = 2 * rb - hs                  # right wall centreline
    hook_r = rb * 0.92
    hook_cy = hook_r + hs                  # hook OUTER bottom on the baseline (no overshoot)
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
