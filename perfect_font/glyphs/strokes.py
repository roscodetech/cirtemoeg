"""Shared multi-stroke constructions used across several glyphs.

The chevron is the constant-width diagonal join (A, V, W, M, v, w): two slanted legs
meeting at a sharp apex. Each leg has constant perpendicular width and its foot is cut
FLAT on the horizontal baseline/cap line (no spike past the metric line). Legs are built
from horizontally-offset edges so both the outer apex tip and the inner notch are exact
intersections.
"""

from __future__ import annotations

import math

from perfect_font import geometry as g
from perfect_font.geometry import Point
from perfect_font.metrics import Metrics


def _h_half(p0: Point, p1: Point, weight: float) -> float:
    """Horizontal half-width giving perpendicular width ``weight`` for leg p0->p1."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    length = math.hypot(dx, dy)
    sin_t = abs(dy) / length
    return (weight / sin_t) / 2.0


def _shift(p0: Point, p1: Point, dx: float) -> tuple[Point, Point]:
    return ((p0[0] + dx, p0[1]), (p1[0] + dx, p1[1]))


def draw_chevron(pen, metrics: Metrics, foot_l: Point, foot_r: Point, apex: Point) -> Point:
    """Two legs from ``foot_l`` and ``foot_r`` (same y) meeting sharply at ``apex``.

    Returns the inner-apex point for use as a crossbar anchor (e.g. A's bar).
    """
    from perfect_font.pens import draw_polygon

    s = metrics.stroke
    base_y = foot_l[1]
    # full horizontal stroke width for each leg (perpendicular width stays == stroke)
    wl = 2 * _h_half(foot_l, apex, s)
    wr = 2 * _h_half(foot_r, apex, s)

    # Outer edges pass through the nominal apex and the outer foot corners, so the apex
    # tip lands EXACTLY on the apex (no miter overshoot past the metric line). Inner edges
    # are the outer edges shifted horizontally inward by the full leg width.
    l_in0, l_in1 = _shift(foot_l, apex, +wl)   # left leg inner edge (shifted right)
    r_in0, r_in1 = _shift(foot_r, apex, -wr)   # right leg inner edge (shifted left)
    inner_apex = g.line_intersection(l_in0, l_in1, r_in0, r_in1)

    draw_polygon(pen, [foot_l, apex, inner_apex, (foot_l[0] + wl, base_y)])
    draw_polygon(pen, [foot_r, apex, inner_apex, (foot_r[0] - wr, base_y)])
    return inner_apex
