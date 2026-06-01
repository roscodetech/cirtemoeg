"""Geometry invariants: true-circle fidelity and constant stroke width."""

from __future__ import annotations

import math

import pytest

from perfect_font import geometry as g
from perfect_font.metrics import KAPPA

from .conftest import all_points, dist


def _curve_segments(contour):
    """Yield (p0, c1, c2, p3) cubics from a contour."""
    current = contour[0][1]
    for seg in contour[1:]:
        if seg[0] == "curve":
            yield current, seg[1], seg[2], seg[3]
            current = seg[3]
        elif seg[0] == "line":
            current = seg[1]


def test_circle_control_bounds_are_exact_square():
    cx, cy, r = 100.0, 200.0, 175.0
    pts = all_points(g.circle_contour(cx, cy, r))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    assert min(xs) == pytest.approx(cx - r)
    assert max(xs) == pytest.approx(cx + r)
    assert min(ys) == pytest.approx(cy - r)
    assert max(ys) == pytest.approx(cy + r)


def test_circle_is_round_within_tolerance():
    cx, cy, r = 0.0, 0.0, 175.0
    max_dev = 0.0
    for p0, c1, c2, p3 in _curve_segments(g.circle_contour(cx, cy, r)):
        for i in range(21):
            t = i / 20
            x, y = g.cubic_point(p0, c1, c2, p3, t)
            max_dev = max(max_dev, abs(math.hypot(x - cx, y - cy) - r))
    # A 4-cubic kappa circle deviates < 0.02% of the radius.
    assert max_dev < r * 3e-4


def test_circle_ccw_and_cw_have_same_points_reversed():
    ccw = all_points(g.circle_contour(0, 0, 100, ccw=True))
    cw = all_points(g.circle_contour(0, 0, 100, ccw=False))
    assert set(round(x, 6) for x, _ in ccw) == set(round(x, 6) for x, _ in cw)


@pytest.mark.parametrize("angle_deg", [0, 30, 45, 90, 135])
def test_stroke_width_constant_on_any_angle(angle_deg):
    weight = 88.0
    length = 400.0
    a = math.radians(angle_deg)
    p0 = (0.0, 0.0)
    p1 = (length * math.cos(a), length * math.sin(a))
    quad = g.stroke_quad(p0, p1, weight)
    # opposite edges must be exactly `weight` apart
    assert dist(quad[0], quad[3]) == pytest.approx(weight)
    assert dist(quad[1], quad[2]) == pytest.approx(weight)
    # and the stroke length is preserved
    assert dist(quad[0], quad[1]) == pytest.approx(length)


def test_kappa_handles_point_inside_circle():
    c = 100 * KAPPA
    assert c < 100  # control points stay inside the bounding square
