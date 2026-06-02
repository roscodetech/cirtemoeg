"""Lowercase a-z. Single-story geometric a and g (Futura-style) for purity."""

from __future__ import annotations

import math

from perfect_font.glyphs.base import FLAT, NARROW, ROUND, GlyphDef
from perfect_font.glyphs.parts import (
    arc,
    arc_pt,
    band_radius,
    carc,
    diag,
    half_bottom,
    half_top,
    hbar,
    joint,
    ring,
    stem_with_tail,
    vstem,
)

# Descender-tail curl radius (x-height fraction). Shared by g and j so their
# underhangs are identical -- see ``stem_with_tail``.
TAIL_RADIUS = 0.42
from perfect_font.glyphs.strokes import draw_chevron
from perfect_font.metrics import Metrics
from perfect_font.pens import draw_disc, draw_stroke


def _bowl(pen, m: Metrics):
    r, cy = band_radius(m, m.x_height, 0)
    ring(pen, m, r, cy, r)
    return r, cy


def a(pen, m: Metrics) -> None:
    r, cy = _bowl(pen, m)
    vstem(pen, m, 2 * r - m.half_stroke, 0, m.x_height)


def b(pen, m: Metrics) -> None:
    vstem(pen, m, m.half_stroke, 0, m.ascender)
    _bowl(pen, m)


def c(pen, m: Metrics) -> None:
    r = m.x_height / 2
    arc(pen, m, r, r, r, 55, 305)


def d(pen, m: Metrics) -> None:
    r, cy = _bowl(pen, m)
    vstem(pen, m, 2 * r - m.half_stroke, 0, m.ascender)


def e(pen, m: Metrics) -> None:
    r = m.x_height / 2
    cx = cy = r
    # bowl arc: start at the crossbar's right end, sweep CCW up/left/down to a clean
    # lower-right terminal -> leaves an open aperture like c.
    bar_y = r * 0.92               # crossbar sits a little above centre
    # angle on the ring centerline where the bar meets the right wall
    sin_t = (bar_y - cy) / r
    a_start = math.degrees(math.asin(max(-1.0, min(1.0, sin_t))))  # right side at bar height
    arc(pen, m, cx, cy, r, a_start, a_start + 305)  # ~305 deg sweep, open lower-right
    # crossbar from the left wall to the bar/arc junction on the right
    hbar(pen, m, m.half_stroke, cx + r, bar_y)


def f(pen, m: Metrics) -> None:
    x, hs = m.x_height, m.half_stroke
    r = x * 0.42
    xc = r + hs
    vstem(pen, m, xc, 0, m.cap_height - r)
    # top hook springs from the stem (180 deg), arches over the apex and comes down
    # to terminate up-and-right at 35 deg -- a full hook (matches r's shoulder), not
    # a quarter cut off at the top.
    carc(pen, m, xc + r, m.cap_height - r, r, 180, 35, cap0=True)
    hbar(pen, m, 0, xc + r, x - hs)


def g(pen, m: Metrics) -> None:
    r, cy = _bowl(pen, m)
    xc = 2 * r - m.half_stroke
    stem_with_tail(pen, m, xc, m.x_height * TAIL_RADIUS, m.x_height)  # tail identical to j


def _arch_glyph(pen, m: Metrics, left_full_to: float) -> float:
    x, hs = m.x_height, m.half_stroke
    w = x * 0.88
    r_a = w / 2
    cy = x - r_a
    vstem(pen, m, hs, 0, left_full_to)
    half_top(pen, m, w / 2, cy, r_a)
    vstem(pen, m, w - hs, 0, cy)
    return w


def h(pen, m: Metrics) -> None:
    _arch_glyph(pen, m, m.ascender)


def i(pen, m: Metrics) -> None:
    hs = m.half_stroke
    vstem(pen, m, hs, 0, m.x_height)
    draw_disc(pen, hs, m.x_height + m.stroke * 0.55 + hs, hs)


def j(pen, m: Metrics) -> None:
    hs = m.half_stroke
    tr = m.x_height * TAIL_RADIUS
    xc = 2 * tr - hs
    stem_with_tail(pen, m, xc, tr, m.x_height)  # tail identical to g
    draw_disc(pen, xc, m.x_height + m.stroke * 0.55 + hs, hs)


def k(pen, m: Metrics) -> None:
    x, s = m.x_height, m.stroke
    w = x * 0.72
    vstem(pen, m, m.half_stroke, 0, m.ascender)
    diag(pen, m, (s, x * 0.42), (w, x))
    diag(pen, m, (s, x * 0.42), (w, 0))
    joint(pen, m, s, x * 0.42)


def m(pen, mm: Metrics) -> None:
    x, hs = mm.x_height, mm.half_stroke
    # each shoulder is the SAME arch as n (r_a = 0.44x) so both read identically round.
    s = mm.stroke
    r_a = x * 0.44
    cy = x - r_a
    # stem centre spacing so counter width == inner-arch diameter (round, gap-free top),
    # exactly as in n: centre_dist - stroke == 2*(r_a - stroke).
    span = 2 * r_a - s
    s0 = hs                    # left stem
    s1 = s0 + span             # middle stem
    s2 = s1 + span             # right stem
    vstem(pen, mm, s0, 0, x)               # only the left stem rises to x-height
    half_top(pen, mm, (s0 + s1) / 2, cy, r_a)   # left shoulder centred on the counter
    vstem(pen, mm, s1, 0, cy)              # inner stems stop at the arch spring
    half_top(pen, mm, (s1 + s2) / 2, cy, r_a)   # right shoulder
    vstem(pen, mm, s2, 0, cy)


def n(pen, m: Metrics) -> None:
    _arch_glyph(pen, m, m.x_height)


def o(pen, m: Metrics) -> None:
    _bowl(pen, m)


def p(pen, m: Metrics) -> None:
    vstem(pen, m, m.half_stroke, m.descender, m.x_height)
    _bowl(pen, m)


def q(pen, m: Metrics) -> None:
    r, cy = _bowl(pen, m)
    vstem(pen, m, 2 * r - m.half_stroke, m.descender, m.x_height)


def r(pen, m: Metrics) -> None:
    x, hs = m.x_height, m.half_stroke
    r_a = x * 0.44                       # same shoulder radius as n: rounds identically
    cy = x - r_a
    cx = hs + r_a                        # centre offset so the arc springs off the stem
    vstem(pen, m, hs, 0, x)
    # shoulder springs from the stem (180 deg), arches over the apex, and the arm
    # terminates up-and-right at 25 deg -- a rounded shoulder that never tilts down.
    carc(pen, m, cx, cy, r_a, 180, 25, cap0=True)


def s(pen, m: Metrics) -> None:
    x = m.x_height
    r = x / 4  # so the two bowls meet exactly at the waist (x = 4r)
    cx = r
    # bottom bowl is the exact 180deg rotation of the top about the waist (cx, x/2):
    # equal bowls, and the lower-left terminal mirrors the upper-right one.
    carc(pen, m, cx, x - r, r, 25, 270, cap1=True)  # top bowl: terminal(25) -> waist(270)
    carc(pen, m, cx, r, r, 90, -155)                # bottom bowl: waist(90) -> terminal(-155)


def t(pen, m: Metrics) -> None:
    x, hs = m.x_height, m.half_stroke
    r_a = x * 0.34
    xc = x * 0.34
    vstem(pen, m, xc, r_a, x * 1.42)
    hbar(pen, m, 0, xc + r_a, x - hs)
    # foot springs from the stem base (180 deg), curls under and up to terminate
    # up-and-right at 340 deg -- a full J-foot, not a quarter cut off at the baseline.
    carc(pen, m, xc + r_a, r_a, r_a, 180, 340, cap0=True)


def u(pen, m: Metrics) -> None:
    x, hs = m.x_height, m.half_stroke
    w = x * 0.88
    r_a = w / 2
    cy = r_a
    # both stems spring from the arch (cy -> x) so u is left-right symmetric, exactly
    # like U -- no lone right foot dropping to the baseline.
    vstem(pen, m, hs, cy, x)
    half_bottom(pen, m, w / 2, cy, r_a)
    vstem(pen, m, w - hs, cy, x)


def v(pen, m: Metrics) -> None:
    x = m.x_height
    w = x * 0.78
    draw_chevron(pen, m, (0.0, x), (w, x), (w / 2, m.pointed_bottom(0)))


def w(pen, m: Metrics) -> None:
    x = m.x_height
    u = x * 0.52
    bot = m.pointed_bottom(0)
    draw_chevron(pen, m, (0.0, x), (2 * u, x), (u, bot))
    draw_chevron(pen, m, (u, x), (3 * u, x), (2 * u, bot))


def x(pen, m: Metrics) -> None:
    xh = m.x_height
    w = xh * 0.74
    diag(pen, m, (0.0, 0.0), (w, xh))
    diag(pen, m, (0.0, xh), (w, 0.0))


def y(pen, m: Metrics) -> None:
    xh = m.x_height
    w = xh * 0.78
    # right diagonal runs full x-height straight down through baseline into the descender
    diag(pen, m, (w, xh), (w / 2 + (w / 2) * (m.descender / xh), m.descender))
    # left diagonal meets it at the baseline vee
    diag(pen, m, (0.0, xh), (w / 2, 0.0))
    joint(pen, m, w / 2, 0.0)


def z(pen, m: Metrics) -> None:
    xh, hs = m.x_height, m.half_stroke
    w = xh * 0.74
    hbar(pen, m, 0, w, xh - hs)
    diag(pen, m, (w, xh), (0.0, 0.0))
    hbar(pen, m, 0, w, hs)


def _l(pen, m: Metrics) -> None:
    vstem(pen, m, m.half_stroke, 0, m.ascender)


LOWERCASE: list[GlyphDef] = [
    GlyphDef("a", 0x61, a, ROUND),
    GlyphDef("b", 0x62, b, ROUND),
    GlyphDef("c", 0x63, c, ROUND),
    GlyphDef("d", 0x64, d, ROUND),
    GlyphDef("e", 0x65, e, ROUND),
    GlyphDef("f", 0x66, f, NARROW),
    GlyphDef("g", 0x67, g, ROUND),
    GlyphDef("h", 0x68, h, FLAT),
    GlyphDef("i", 0x69, i, NARROW),
    GlyphDef("j", 0x6A, j, NARROW),
    GlyphDef("k", 0x6B, k, FLAT),
    GlyphDef("l", 0x6C, _l, NARROW),
    GlyphDef("m", 0x6D, m, FLAT),
    GlyphDef("n", 0x6E, n, FLAT),
    GlyphDef("o", 0x6F, o, ROUND),
    GlyphDef("p", 0x70, p, ROUND),
    GlyphDef("q", 0x71, q, ROUND),
    GlyphDef("r", 0x72, r, NARROW),
    GlyphDef("s", 0x73, s, ROUND),
    GlyphDef("t", 0x74, t, NARROW),
    GlyphDef("u", 0x75, u, FLAT),
    GlyphDef("v", 0x76, v, FLAT),
    GlyphDef("w", 0x77, w, FLAT),
    GlyphDef("x", 0x78, x, FLAT),
    GlyphDef("y", 0x79, y, FLAT),
    GlyphDef("z", 0x7A, z, FLAT),
]
