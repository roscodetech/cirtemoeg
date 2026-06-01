"""Uppercase A-Z, from circles, arcs and constant-width strokes (baseline 0 to cap)."""

from __future__ import annotations

from perfect_font import geometry as g
from perfect_font.glyphs.base import FLAT, ROUND, GlyphDef
from perfect_font.glyphs.parts import (
    arc,
    arc_pt,
    band_radius,
    carc,
    diag,
    half_bottom,
    half_right,
    hbar,
    joint,
    ring,
    vstem,
)
from perfect_font.glyphs.strokes import draw_chevron
from perfect_font.metrics import Metrics
from perfect_font.pens import draw_stroke


def _C_arc(pen, m: Metrics, r: float) -> None:
    arc(pen, m, r, r, r, 55, 305)


def A(pen, m: Metrics) -> None:
    cap = m.cap_height
    w = cap * 0.74
    apex = (w / 2, m.pointed_top(cap))
    draw_chevron(pen, m, (0.0, 0.0), (w, 0.0), apex)
    # crossbar spans only the inner gap between the legs; ends tucked inside the leg
    # outer edges so no bar corner pokes past the diagonal silhouette.
    bar_y = cap * 0.30
    lx_in = g.x_on_line((0.0, 0.0), apex, bar_y + m.half_stroke)
    rx_in = g.x_on_line((w, 0.0), apex, bar_y + m.half_stroke)
    hbar(pen, m, lx_in, rx_in, bar_y)


def B(pen, m: Metrics) -> None:
    cap, s, hs = m.cap_height, m.stroke, m.half_stroke
    r = cap / 4  # two equal bowls, each a semicircle of height cap/2, meeting at mid
    vstem(pen, m, hs, 0, cap)
    half_right(pen, m, s, cap - r, r)  # top bowl, flat side on stem right edge
    half_right(pen, m, s, r, r)        # bottom bowl
    hbar(pen, m, hs, s + hs, cap / 2)  # tie bowls to stem at the waist


def C(pen, m: Metrics) -> None:
    _C_arc(pen, m, m.cap_height / 2)


def D(pen, m: Metrics) -> None:
    cap, s = m.cap_height, m.stroke
    vstem(pen, m, m.half_stroke, 0, cap)
    half_right(pen, m, s, cap / 2, cap / 2)


def E(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.60
    vstem(pen, m, hs, 0, cap)
    hbar(pen, m, 0, w, cap - hs)
    hbar(pen, m, 0, w * 0.92, cap / 2)
    hbar(pen, m, 0, w, hs)


def F(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.58
    vstem(pen, m, hs, 0, cap)
    hbar(pen, m, 0, w, cap - hs)
    hbar(pen, m, 0, w * 0.92, cap / 2)


def G(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    r = cap / 2
    a_term = 318  # lower-right terminal angle for the C opening
    arc(pen, m, r, r, r, 55, a_term)          # the C
    tx, ty = arc_pt(r, r, r - hs, a_term)     # arc stroke centerline terminal
    bar_y = cap * 0.44
    vstem(pen, m, tx, ty, bar_y)              # vertical rising from the arc terminal
    hbar(pen, m, cap * 0.46, tx, bar_y)       # bar reaching inward to centre
    joint(pen, m, tx, ty)
    joint(pen, m, tx, bar_y)


def H(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.66
    vstem(pen, m, hs, 0, cap)
    vstem(pen, m, w - hs, 0, cap)
    hbar(pen, m, hs, w - hs, cap / 2)


def I(pen, m: Metrics) -> None:
    vstem(pen, m, m.half_stroke, 0, m.cap_height)


def J(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    r = cap * 0.34            # bigger hook so J fills the cap like other letters
    xc = cap * 0.46           # stem x: hook centre sits left of it
    vstem(pen, m, xc, r, cap)
    # bottom hook curving left: centerline arc from the stem foot down and round to the left
    carc(pen, m, xc - r, r, r, 0, -180, cap0=True)


def K(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.62
    vstem(pen, m, hs, 0, cap)
    # arms meet at one junction on the stem; perpendicular strokes keep constant weight
    # (free-standing tips, so no flush-cut needed and no shallow-angle ballooning)
    junc = (hs, cap * 0.48)
    draw_stroke(pen, junc, (w, cap), m.stroke)
    draw_stroke(pen, junc, (w, 0), m.stroke)
    joint(pen, m, *junc)
    joint(pen, m, *junc)


def L(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    vstem(pen, m, hs, 0, cap)
    hbar(pen, m, 0, cap * 0.56, hs)


def M(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.86
    vstem(pen, m, hs, 0, cap)
    vstem(pen, m, w - hs, 0, cap)
    # inner vee as a sharp chevron from the two stem tops down to a baseline-near vertex
    draw_chevron(pen, m, (hs, cap), (w - hs, cap), (w / 2, cap * 0.18))


def N(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.68
    vstem(pen, m, hs, 0, cap)
    vstem(pen, m, w - hs, 0, cap)
    diag(pen, m, (hs, cap), (w - hs, 0))


def O(pen, m: Metrics) -> None:
    r, cy = band_radius(m, m.cap_height, 0)
    ring(pen, m, r, cy, r)


def P(pen, m: Metrics) -> None:
    cap, s = m.cap_height, m.stroke
    r = cap * 0.28
    vstem(pen, m, m.half_stroke, 0, cap)
    half_right(pen, m, s, cap - r, r)


def Q(pen, m: Metrics) -> None:
    cap = m.cap_height
    r = cap / 2
    ring(pen, m, r, r, r)
    diag(pen, m, (cap * 0.58, cap * 0.30), (cap * 0.96, -cap * 0.02))


def R(pen, m: Metrics) -> None:
    cap, s = m.cap_height, m.stroke
    r = cap * 0.28
    w = s + r
    vstem(pen, m, m.half_stroke, 0, cap)
    half_right(pen, m, s, cap - r, r)
    diag(pen, m, (s, cap - 2 * r), (w + r * 0.2, 0))
    joint(pen, m, s, cap - 2 * r)


def S(pen, m: Metrics) -> None:
    cap = m.cap_height
    r = cap / 4  # two bowls meet exactly at the waist (cap = 4r)
    cx = r
    # bottom bowl is the top bowl rotated 180 deg about the centre -> exact point symmetry
    carc(pen, m, cx, cap - r, r, 28, 270, cap1=True)   # top bowl -> waist
    carc(pen, m, cx, r, r, 28 + 180, 270 + 180, cap1=True)  # waist -> bottom bowl


def T(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.62
    hbar(pen, m, 0, w, cap - hs)
    vstem(pen, m, w / 2, 0, cap - hs)


def U(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.66
    r = w / 2
    vstem(pen, m, hs, r, cap)
    vstem(pen, m, w - hs, r, cap)
    half_bottom(pen, m, w / 2, r, r)


def V(pen, m: Metrics) -> None:
    cap = m.cap_height
    w = cap * 0.72
    draw_chevron(pen, m, (0.0, cap), (w, cap), (w / 2, m.pointed_bottom(0)))


def W(pen, m: Metrics) -> None:
    cap = m.cap_height
    u = cap * 0.5
    bot = m.pointed_bottom(0)
    draw_chevron(pen, m, (0.0, cap), (2 * u, cap), (u, bot))
    draw_chevron(pen, m, (u, cap), (3 * u, cap), (2 * u, bot))


def X(pen, m: Metrics) -> None:
    cap = m.cap_height
    w = cap * 0.66
    diag(pen, m, (0.0, 0.0), (w, cap))
    diag(pen, m, (0.0, cap), (w, 0.0))


def Y(pen, m: Metrics) -> None:
    cap = m.cap_height
    w = cap * 0.66
    mid = cap * 0.5
    diag(pen, m, (0.0, cap), (w / 2, mid))
    diag(pen, m, (w, cap), (w / 2, mid))
    vstem(pen, m, w / 2, 0, mid)
    joint(pen, m, w / 2, mid)


def Z(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    w = cap * 0.62
    hbar(pen, m, 0, w, cap - hs)
    diag(pen, m, (w, cap), (0.0, 0.0))
    hbar(pen, m, 0, w, hs)


UPPERCASE: list[GlyphDef] = [
    GlyphDef("A", 0x41, A, FLAT),
    GlyphDef("B", 0x42, B, FLAT),
    GlyphDef("C", 0x43, C, ROUND),
    GlyphDef("D", 0x44, D, FLAT),
    GlyphDef("E", 0x45, E, FLAT),
    GlyphDef("F", 0x46, F, FLAT),
    GlyphDef("G", 0x47, G, ROUND),
    GlyphDef("H", 0x48, H, FLAT),
    GlyphDef("I", 0x49, I, FLAT),
    GlyphDef("J", 0x4A, J, FLAT),
    GlyphDef("K", 0x4B, K, FLAT),
    GlyphDef("L", 0x4C, L, FLAT),
    GlyphDef("M", 0x4D, M, FLAT),
    GlyphDef("N", 0x4E, N, FLAT),
    GlyphDef("O", 0x4F, O, ROUND),
    GlyphDef("P", 0x50, P, FLAT),
    GlyphDef("Q", 0x51, Q, ROUND),
    GlyphDef("R", 0x52, R, FLAT),
    GlyphDef("S", 0x53, S, ROUND),
    GlyphDef("T", 0x54, T, FLAT),
    GlyphDef("U", 0x55, U, FLAT),
    GlyphDef("V", 0x56, V, FLAT),
    GlyphDef("W", 0x57, W, FLAT),
    GlyphDef("X", 0x58, X, FLAT),
    GlyphDef("Y", 0x59, Y, FLAT),
    GlyphDef("Z", 0x5A, Z, FLAT),
]
