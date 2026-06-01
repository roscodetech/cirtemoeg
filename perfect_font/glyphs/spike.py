"""A small representative subset used to de-risk the pipeline before the full set:
round (o/O/8), flat (H/l/i), the diagonal join (A/V/W/x), and a bowl+stem (b).
"""

from __future__ import annotations

from perfect_font import geometry as g
from perfect_font.glyphs.base import FLAT, NARROW, ROUND, GlyphDef
from perfect_font.glyphs.strokes import draw_chevron
from perfect_font.metrics import Metrics
from perfect_font.pens import draw_disc, draw_ring, draw_stroke


def _ring_band(m: Metrics, top_line: float, bot_line: float):
    top = m.round_top(top_line)
    bot = m.round_bottom(bot_line)
    r = (top - bot) / 2
    cy = (top + bot) / 2
    return r, cy


def draw_H(pen, m: Metrics) -> None:
    w = round(m.cap_height * 0.66)
    hs = m.half_stroke
    draw_stroke(pen, (hs, 0), (hs, m.cap_height), m.stroke)
    draw_stroke(pen, (w - hs, 0), (w - hs, m.cap_height), m.stroke)
    draw_stroke(pen, (hs, m.cap_height / 2), (w - hs, m.cap_height / 2), m.stroke)


def draw_l(pen, m: Metrics) -> None:
    hs = m.half_stroke
    draw_stroke(pen, (hs, 0), (hs, m.ascender), m.stroke)


def draw_i(pen, m: Metrics) -> None:
    hs = m.half_stroke
    draw_stroke(pen, (hs, 0), (hs, m.x_height), m.stroke)
    cy = m.x_height + m.stroke * 0.55 + hs
    draw_disc(pen, hs, cy, hs)


def draw_o(pen, m: Metrics) -> None:
    r, cy = _ring_band(m, m.x_height, 0)
    draw_ring(pen, r, cy, r, m.stroke)


def draw_O(pen, m: Metrics) -> None:
    r, cy = _ring_band(m, m.cap_height, 0)
    draw_ring(pen, r, cy, r, m.stroke)


def draw_b(pen, m: Metrics) -> None:
    hs = m.half_stroke
    draw_stroke(pen, (hs, 0), (hs, m.ascender), m.stroke)
    r, cy = _ring_band(m, m.x_height, 0)
    draw_ring(pen, r, cy, r, m.stroke)


def draw_A(pen, m: Metrics) -> None:
    w = m.cap_height * 0.74
    apex = (w / 2, m.pointed_top(m.cap_height))
    draw_chevron(pen, m, (0.0, 0.0), (w, 0.0), apex)
    bar_y = m.cap_height * 0.32
    lx = g.x_on_line((0.0, 0.0), apex, bar_y)
    rx = g.x_on_line((w, 0.0), apex, bar_y)
    draw_stroke(pen, (lx, bar_y), (rx, bar_y), m.stroke)


def draw_V(pen, m: Metrics) -> None:
    w = m.cap_height * 0.72
    draw_chevron(pen, m, (0.0, m.cap_height), (w, m.cap_height), (w / 2, m.pointed_bottom(0)))


def draw_W(pen, m: Metrics) -> None:
    u = m.cap_height * 0.5
    cap = m.cap_height
    bot = m.pointed_bottom(0)
    draw_chevron(pen, m, (0.0, cap), (2 * u, cap), (u, bot))
    draw_chevron(pen, m, (u, cap), (3 * u, cap), (2 * u, bot))


def draw_x(pen, m: Metrics) -> None:
    w = m.x_height * 0.82
    draw_stroke(pen, (0.0, 0.0), (w, m.x_height), m.stroke)
    draw_stroke(pen, (0.0, m.x_height), (w, 0.0), m.stroke)


def draw_eight(pen, m: Metrics) -> None:
    h = m.figure_height
    r_top, r_bot = h * 0.21, h * 0.27
    cx = r_bot
    top = m.round_top(h)
    bot = m.round_bottom(0)
    draw_ring(pen, cx, top - r_top, r_top, m.stroke)
    draw_ring(pen, cx, bot + r_bot, r_bot, m.stroke)


def draw_period(pen, m: Metrics) -> None:
    draw_disc(pen, m.half_stroke, m.half_stroke, m.half_stroke)


SPIKE: list[GlyphDef] = [
    GlyphDef("space", 0x20, lambda *_: None, is_blank=True),
    GlyphDef("H", 0x48, draw_H, FLAT),
    GlyphDef("l", 0x6C, draw_l, NARROW),
    GlyphDef("i", 0x69, draw_i, NARROW),
    GlyphDef("o", 0x6F, draw_o, ROUND),
    GlyphDef("O", 0x4F, draw_O, ROUND),
    GlyphDef("b", 0x62, draw_b, ROUND),
    GlyphDef("A", 0x41, draw_A, FLAT),
    GlyphDef("V", 0x56, draw_V, FLAT),
    GlyphDef("W", 0x57, draw_W, FLAT),
    GlyphDef("x", 0x78, draw_x, FLAT),
    GlyphDef("eight", 0x38, draw_eight, ROUND),
    GlyphDef("period", 0x2E, draw_period, NARROW),
]
