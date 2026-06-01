"""Pure geometric math: no font/pen dependencies, trivially unit-testable.

A *contour* here is a small list of segment tuples:
    ("move", (x, y))
    ("line", (x, y))
    ("curve", (c1x, c1y), (c2x, c2y), (x, y))
The contour is always implicitly closed. ``pens.py`` replays these into a fontTools pen.
"""

from __future__ import annotations

import math

from perfect_font.metrics import KAPPA

Point = tuple[float, float]
Segment = tuple
Contour = list[Segment]


def circle_contour(cx: float, cy: float, r: float, ccw: bool = True) -> Contour:
    """A true circle as four cubic quarter-arcs (canonical kappa construction)."""
    c = r * KAPPA
    e, n, w, s = (cx + r, cy), (cx, cy + r), (cx - r, cy), (cx, cy - r)
    if ccw:
        return [
            ("move", e),
            ("curve", (cx + r, cy + c), (cx + c, cy + r), n),
            ("curve", (cx - c, cy + r), (cx - r, cy + c), w),
            ("curve", (cx - r, cy - c), (cx - c, cy - r), s),
            ("curve", (cx + c, cy - r), (cx + r, cy - c), e),
        ]
    return [
        ("move", e),
        ("curve", (cx + r, cy - c), (cx + c, cy - r), s),
        ("curve", (cx - c, cy - r), (cx - r, cy - c), w),
        ("curve", (cx - r, cy + c), (cx - c, cy + r), n),
        ("curve", (cx + c, cy + r), (cx + r, cy + c), e),
    ]


def _arc_curves(cx: float, cy: float, r: float, a0: float, a1: float) -> tuple[Point, list[Segment]]:
    """Cubic-Bezier approximation of the arc from angle a0 to a1 (radians).

    Splits into sub-arcs <= 90 deg; per-segment handle length = 4/3*tan(dt/4)*r.
    Returns (start_point, [curve segments]).
    """
    sweep = a1 - a0
    n = max(1, math.ceil(abs(sweep) / (math.pi / 2)))
    dt = sweep / n
    k = 4.0 / 3.0 * math.tan(dt / 4.0)
    start = (cx + r * math.cos(a0), cy + r * math.sin(a0))
    segs: list[Segment] = []
    for i in range(n):
        b0 = a0 + dt * i
        b1 = a0 + dt * (i + 1)
        p0 = (cx + r * math.cos(b0), cy + r * math.sin(b0))
        p3 = (cx + r * math.cos(b1), cy + r * math.sin(b1))
        c1 = (p0[0] - k * r * math.sin(b0), p0[1] + k * r * math.cos(b0))
        c2 = (p3[0] + k * r * math.sin(b1), p3[1] - k * r * math.cos(b1))
        segs.append(("curve", c1, c2, p3))
    return start, segs


def ring_arc_contour(
    cx: float, cy: float, outer_r: float, thickness: float, start_deg: float, end_deg: float
) -> Contour:
    """An open monoline arc (partial annulus) with flat radial terminals."""
    a0, a1 = math.radians(start_deg), math.radians(end_deg)
    inner_r = outer_r - thickness
    o_start, o_curves = _arc_curves(cx, cy, outer_r, a0, a1)
    i_start, i_curves = _arc_curves(cx, cy, inner_r, a1, a0)
    return orient([("move", o_start), *o_curves, ("line", i_start), *i_curves], ccw=True)


def stadium_contour(cx: float, cy: float, r: float, straight_half: float, ccw: bool = True) -> Contour:
    """A vertical stadium (rectangle with semicircular top/bottom caps). Used for 0."""
    h = straight_half
    _ts, top = _arc_curves(cx, cy + h, r, 0.0, math.pi)
    _bs, bot = _arc_curves(cx, cy - h, r, math.pi, 2 * math.pi)
    contour: Contour = [
        ("move", (cx + r, cy - h)),
        ("line", (cx + r, cy + h)),
        *top,
        ("line", (cx - r, cy - h)),
        *bot,
    ]
    return orient(contour, ccw=ccw)


def _all_points(contour: Contour) -> list[Point]:
    pts: list[Point] = []
    for seg in contour:
        if seg[0] in ("move", "line"):
            pts.append(seg[1])
        else:
            pts.extend([seg[1], seg[2], seg[3]])
    return pts


def _signed_area(contour: Contour) -> float:
    pts = _all_points(contour)
    a = 0.0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        a += x1 * y2 - x2 * y1
    return a / 2.0


def orient(contour: Contour, ccw: bool = True) -> Contour:
    """Force a contour's winding: ccw=True for solid fills, False for holes.

    Consistent winding is required so skia-pathops' non-zero union never cancels
    overlapping solids (which showed up as white slashes through a/b/d/e/g)."""
    is_ccw = _signed_area(contour) > 0
    return contour if is_ccw == ccw else _reverse(contour)


def _reverse(contour: Contour) -> Contour:
    """Reverse a contour's direction (for inner holes)."""
    pts = [contour[0][1]]
    rebuilt: list[tuple] = []
    for seg in contour[1:]:
        if seg[0] == "line":
            rebuilt.append(("line", seg[1], None, None))
            pts.append(seg[1])
        else:
            rebuilt.append(("curve", seg[1], seg[2], seg[3]))
            pts.append(seg[3])
    out: Contour = [("move", pts[-1])]
    for i in range(len(rebuilt) - 1, -1, -1):
        if rebuilt[i][0] == "line":
            out.append(("line", pts[i]))
        else:
            out.append(("curve", rebuilt[i][2], rebuilt[i][1], pts[i]))
    return out


def polygon_contour(points: list[Point]) -> Contour:
    """A closed straight-edged contour through ``points``."""
    if len(points) < 3:
        raise ValueError("polygon_contour needs at least 3 points")
    segs: Contour = [("move", points[0])]
    segs.extend(("line", p) for p in points[1:])
    return orient(segs, ccw=True)


def stroke_quad(p0: Point, p1: Point, weight: float) -> list[Point]:
    """The 4 corners of a constant perpendicular-width stroke from p0 to p1."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    if length == 0:
        raise ValueError("stroke_quad: zero-length stroke")
    nx, ny = -dy / length, dx / length
    hw = weight / 2.0
    return [
        (x0 + nx * hw, y0 + ny * hw),
        (x1 + nx * hw, y1 + ny * hw),
        (x1 - nx * hw, y1 - ny * hw),
        (x0 - nx * hw, y0 - ny * hw),
    ]


def diag_quad_h(p0: Point, p1: Point, weight: float) -> list[Point]:
    """A diagonal stroke of constant *horizontal* width ``weight`` with ends cut flat
    along horizontal lines through p0 and p1.

    Unlike ``stroke_quad`` (perpendicular caps, which spike past baseline/cap lines),
    this keeps the top and bottom edges horizontal, so diagonal terminals sit flush on
    their metric line with no overhang. Requires p0 and p1 at different heights.
    """
    (x0, y0), (x1, y1) = p0, p1
    if y0 == y1:
        raise ValueError("diag_quad_h: endpoints must differ in y (use stroke_quad)")
    hw = weight / 2.0
    return [
        (x0 - hw, y0),
        (x0 + hw, y0),
        (x1 + hw, y1),
        (x1 - hw, y1),
    ]


def offset_segment(p0: Point, p1: Point, dist: float, toward_x: float) -> tuple[Point, Point]:
    """Offset segment (p0,p1) perpendicular by ``dist`` toward the side of ``toward_x``."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    midx = (x0 + x1) / 2
    if (toward_x - midx) * nx < 0:
        nx, ny = -nx, -ny
    return (x0 + nx * dist, y0 + ny * dist), (x1 + nx * dist, y1 + ny * dist)


def line_intersection(a1: Point, a2: Point, b1: Point, b2: Point) -> Point:
    """Intersection of infinite lines (a1,a2) and (b1,b2). Raises if parallel."""
    x1, y1 = a1
    x2, y2 = a2
    x3, y3 = b1
    x4, y4 = b2
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-9:
        raise ValueError("line_intersection: parallel lines")
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
    return (px, py)


def x_on_line(p0: Point, p1: Point, y: float) -> float:
    """X coordinate where the infinite line through p0,p1 reaches height ``y``."""
    (x0, y0), (x1, y1) = p0, p1
    if y1 == y0:
        raise ValueError("x_on_line: horizontal line")
    return x0 + (x1 - x0) * (y - y0) / (y1 - y0)


def cubic_point(p0: Point, p1: Point, p2: Point, p3: Point, t: float) -> Point:
    """Evaluate a cubic Bezier at parameter t in [0, 1] (for fidelity tests)."""
    mt = 1 - t
    a, b, c, d = mt**3, 3 * mt**2 * t, 3 * mt * t**2, t**3
    return (
        a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
        a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1],
    )
