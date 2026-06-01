"""Shared fixtures and geometric assertion helpers."""

from __future__ import annotations

import math

import pytest
from fontTools.pens.boundsPen import ControlBoundsPen
from fontTools.pens.recordingPen import RecordingPen

from perfect_font.metrics import Metrics

TOL = 0.5  # font units; sub-unit tolerance for "exact" geometric claims


@pytest.fixture
def m() -> Metrics:
    return Metrics()


def record(draw, *args, **kwargs) -> RecordingPen:
    """Run a draw(pen, ...) callable into a RecordingPen and return it."""
    pen = RecordingPen()
    draw(pen, *args, **kwargs)
    return pen


def control_bounds(recording: RecordingPen) -> tuple[float, float, float, float]:
    """(xmin, ymin, xmax, ymax) over on- and off-curve points."""
    bp = ControlBoundsPen(None)
    recording.replay(bp)
    return bp.bounds


def all_points(contour) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for seg in contour:
        pts.extend(seg[1:])
    return pts


def dist(a, b) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])
