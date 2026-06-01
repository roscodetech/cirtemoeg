"""Reusable geometric sub-shapes shared across many glyphs.

Connectivity rule: wherever a centerline arc meets a stem/bar, drop a ``joint`` disc
(radius = half-stroke) at the shared centerline point. The disc guarantees a solid,
gap-free join under pathops' union regardless of the meeting angle. Arc endpoints are
computed with ``arc_pt`` so they land exactly on the stem they should connect to.
"""

from __future__ import annotations

import math

from perfect_font.metrics import Metrics
from perfect_font.pens import draw_diag, draw_disc, draw_ring, draw_ring_arc, draw_stroke


def diag(pen, m: Metrics, p0, p1) -> None:
    """A diagonal of constant *visual* (perpendicular) weight, ends cut flush on the
    horizontal lines through p0/p1 so terminals never spike past a metric line.

    Horizontal thickness = stroke / sin(theta) so the perpendicular thickness stays == stroke.
    """
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    sin_t = abs(dy) / length  # angle from horizontal
    h_weight = m.stroke / sin_t
    draw_diag(pen, p0, p1, h_weight)


def vstem(pen, m: Metrics, x_center: float, y0: float, y1: float) -> None:
    draw_stroke(pen, (x_center, y0), (x_center, y1), m.stroke)


def hbar(pen, m: Metrics, x0: float, x1: float, y: float) -> None:
    draw_stroke(pen, (x0, y), (x1, y), m.stroke)


def ring(pen, m: Metrics, cx: float, cy: float, r: float) -> None:
    draw_ring(pen, cx, cy, r, m.stroke)


def joint(pen, m: Metrics, x: float, y: float) -> None:
    """A round join filler: a disc of radius half-stroke at a centerline meeting point."""
    draw_disc(pen, x, y, m.half_stroke)


def arc_pt(cx: float, cy: float, r: float, a_deg: float) -> tuple[float, float]:
    """Point on a circle of radius ``r`` at angle ``a_deg`` (degrees)."""
    a = math.radians(a_deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def carc(
    pen,
    m: Metrics,
    cx: float,
    cy: float,
    radius: float,
    a0: float,
    a1: float,
    *,
    cap0: bool = False,
    cap1: bool = False,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Stroke a *centerline* arc of given radius and the metric stroke width.

    ``radius`` is the centerline radius (not the outer edge). Optionally drop join
    discs at the start (cap0) / end (cap1). Returns the two centerline endpoints so
    callers can chain connecting strokes exactly.
    """
    outer = radius + m.half_stroke
    draw_ring_arc(pen, cx, cy, outer, m.stroke, a0, a1)
    p0 = arc_pt(cx, cy, radius, a0)
    p1 = arc_pt(cx, cy, radius, a1)
    if cap0:
        joint(pen, m, *p0)
    if cap1:
        joint(pen, m, *p1)
    return p0, p1


def half_right(pen, m: Metrics, cx: float, cy: float, r: float) -> None:
    """Right-bulging semicircle (vertical flat side at x=cx): bowls of B, D, P, R."""
    draw_ring_arc(pen, cx, cy, r, m.stroke, 90, -90)


def half_bottom(pen, m: Metrics, cx: float, cy: float, r: float) -> None:
    """Bottom-bulging semicircle: foot arch of u, U."""
    draw_ring_arc(pen, cx, cy, r, m.stroke, 180, 360)


def half_top(pen, m: Metrics, cx: float, cy: float, r: float) -> None:
    """Top-bulging semicircle: shoulder arch of n, h, m."""
    draw_ring_arc(pen, cx, cy, r, m.stroke, 0, 180)


def arc(pen, m: Metrics, cx: float, cy: float, r: float, a0: float, a1: float) -> None:
    draw_ring_arc(pen, cx, cy, r, m.stroke, a0, a1)


def band_radius(m: Metrics, top: float, bottom: float) -> tuple[float, float]:
    """Outer radius and centre-y for a circle filling the band [bottom, top]."""
    t = m.round_top(top)
    b = m.round_bottom(bottom)
    return (t - b) / 2, (t + b) / 2
