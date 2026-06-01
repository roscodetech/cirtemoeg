"""The primitive drawing vocabulary: feed geometry into a fontTools-style pen.

A "pen" is any object with moveTo/lineTo/curveTo/closePath.
"""

from __future__ import annotations

from perfect_font import geometry as g
from perfect_font.geometry import Contour, Point


def play(pen, contour: Contour) -> None:
    for seg in contour:
        kind = seg[0]
        if kind == "move":
            pen.moveTo(seg[1])
        elif kind == "line":
            pen.lineTo(seg[1])
        elif kind == "curve":
            pen.curveTo(seg[1], seg[2], seg[3])
        else:  # pragma: no cover - defensive
            raise ValueError(f"unknown segment {kind!r}")
    pen.closePath()


def draw_circle(pen, cx: float, cy: float, r: float, ccw: bool = True) -> None:
    play(pen, g.circle_contour(cx, cy, r, ccw=ccw))


def draw_disc(pen, cx: float, cy: float, r: float) -> None:
    """A solid filled circle (dots, period)."""
    draw_circle(pen, cx, cy, r, ccw=True)


def draw_ring(pen, cx: float, cy: float, outer_r: float, thickness: float) -> None:
    """A monoline circular annulus: outer filled, inner counter (hole)."""
    draw_circle(pen, cx, cy, outer_r, ccw=True)
    draw_circle(pen, cx, cy, outer_r - thickness, ccw=False)


def draw_ring_arc(
    pen, cx: float, cy: float, outer_r: float, thickness: float, start_deg: float, end_deg: float
) -> None:
    """An open monoline arc (partial annulus): c, e, shoulders, tails."""
    play(pen, g.ring_arc_contour(cx, cy, outer_r, thickness, start_deg, end_deg))


def draw_stadium_ring(
    pen, cx: float, cy: float, r: float, straight_half: float, thickness: float
) -> None:
    """A monoline stadium (narrow round 0): outer stadium + inner counter (hole)."""
    play(pen, g.stadium_contour(cx, cy, r, straight_half, ccw=True))
    play(pen, g.stadium_contour(cx, cy, r - thickness, straight_half, ccw=False))


def draw_stroke(pen, p0: Point, p1: Point, weight: float) -> None:
    """A straight stroke of constant perpendicular width (vertical, horizontal, diagonal)."""
    play(pen, g.polygon_contour(g.stroke_quad(p0, p1, weight)))


def draw_diag(pen, p0: Point, p1: Point, weight: float) -> None:
    """A diagonal stroke with horizontally flush ends (no perpendicular spike).

    ``weight`` is the horizontal thickness. p0/p1 must differ in y.
    """
    play(pen, g.polygon_contour(g.diag_quad_h(p0, p1, weight)))


def draw_polygon(pen, points: list[Point]) -> None:
    play(pen, g.polygon_contour(points))
