"""The real correctness gate: assert geometric invariants on the raw recipes."""

from __future__ import annotations

import pytest
from fontTools.pens.boundsPen import ControlBoundsPen
from fontTools.pens.recordingPen import RecordingPen

from perfect_font.glyphs import ALL_GLYPHS, REGISTRY, unicodes
from perfect_font.metrics import Metrics

TOL = 1.0


@pytest.fixture
def m() -> Metrics:
    return Metrics()


def _bounds(name: str, m: Metrics):
    rec = RecordingPen()
    REGISTRY[name].recipe(rec, m)
    bp = ControlBoundsPen(None)
    rec.replay(bp)
    return bp.bounds


def _points(name: str, m: Metrics) -> list[tuple[float, float]]:
    rec = RecordingPen()
    REGISTRY[name].recipe(rec, m)
    pts: list[tuple[float, float]] = []
    for _op, args in rec.value:
        for a in args:
            if isinstance(a, tuple) and len(a) == 2:
                pts.append(a)
    return pts


def test_charset_is_complete():
    required = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    required |= set(".,?!:;'\"-()/ ")
    required |= set("&@#$%+=*")
    have = {chr(cp) for cp in unicodes()}
    assert required - have == set()


def test_no_blank_glyph_except_space():
    m = Metrics()
    for g in ALL_GLYPHS:
        if g.is_blank:
            continue
        rec = RecordingPen()
        g.recipe(rec, m)
        assert rec.value, f"{g.name} produced no contours"


@pytest.mark.parametrize("name", ["o", "O", "zero"])
def test_round_glyph_sits_on_metric_lines(name, m):
    _xmin, ymin, _xmax, ymax = _bounds(name, m)
    assert abs(ymin - 0) < TOL, f"{name} bottom off baseline"
    top = m.cap_height if name in ("O", "zero") else m.x_height
    assert abs(ymax - top) < TOL, f"{name} top off its line"


def test_o_outer_box_is_square(m):
    xmin, ymin, xmax, ymax = _bounds("o", m)
    assert abs((xmax - xmin) - (ymax - ymin)) < TOL


@pytest.mark.parametrize("name", ["b", "d", "h", "k", "l", "O", "H", "I", "A"])
def test_ascenders_and_caps_reach_cap_height(name, m):
    _, _, _, ymax = _bounds(name, m)
    assert abs(ymax - m.cap_height) < 2.0, f"{name} top={ymax} != cap {m.cap_height}"


@pytest.mark.parametrize("name", ["p", "q", "g", "j", "y"])
def test_descenders_reach_descender(name, m):
    # Must reach the descender line; diagonal terminals (y) may overshoot slightly.
    _, ymin, _, _ = _bounds(name, m)
    assert m.descender - 40 <= ymin <= m.descender + 2.0, (
        f"{name} bottom={ymin} not at descender {m.descender}"
    )


def test_stem_width_equals_stroke(m):
    xmin, _, xmax, _ = _bounds("l", m)
    assert abs((xmax - xmin) - m.stroke) < TOL


@pytest.mark.parametrize(
    "name", ["o", "O", "A", "H", "T", "V", "X", "x", "v", "M", "W", "I", "eight"]
)
def test_vertical_axis_symmetry(name, m):
    pts = _points(name, m)
    xmin = min(p[0] for p in pts)
    xmax = max(p[0] for p in pts)
    cx = (xmin + xmax) / 2
    rounded = {(round(x, 1), round(y, 1)) for x, y in pts}
    for x, y in pts:
        mx = round(2 * cx - x, 1)
        assert any(
            abs(mx - rx) < 1.5 and abs(round(y, 1) - ry) < 1.5 for rx, ry in rounded
        ), f"{name} not symmetric at ({x:.1f},{y:.1f})"
