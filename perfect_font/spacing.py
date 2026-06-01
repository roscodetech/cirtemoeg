"""Placement engine: turn a glyph's ink bounds into (advance, x_shift).

Recipes draw in arbitrary glyph-local coordinates; this normalises every glyph into
its advance box. Two modes share one return shape so the builder is mode-agnostic:

  * proportional -> sidebearing per spacing class, ink left edge moved to the sidebearing
  * monospace    -> fixed advance, ink centred in the cell
"""

from __future__ import annotations

from perfect_font.glyphs.base import FLAT, NARROW, ROUND
from perfect_font.metrics import Metrics

Bounds = tuple[float, float, float, float]


def _sidebearing(metrics: Metrics, spacing_class: str) -> int:
    return {
        FLAT: metrics.side_flat,
        ROUND: metrics.side_round,
        NARROW: metrics.side_narrow,
    }[spacing_class]


def place_proportional(metrics: Metrics, spacing_class: str, bounds: Bounds) -> tuple[int, float]:
    xmin, _, xmax, _ = bounds
    side = _sidebearing(metrics, spacing_class)
    ink_width = xmax - xmin
    dx = side - xmin
    advance = round(side + ink_width + side)
    return advance, dx


def place_monospace(metrics: Metrics, spacing_class: str, bounds: Bounds) -> tuple[int, float]:
    xmin, _, xmax, _ = bounds
    ink_width = xmax - xmin
    advance = metrics.mono_advance
    dx = (advance - ink_width) / 2 - xmin
    return advance, dx


def place(metrics: Metrics, spacing_class: str, bounds: Bounds, *, mono: bool) -> tuple[int, float]:
    if mono:
        return place_monospace(metrics, spacing_class, bounds)
    return place_proportional(metrics, spacing_class, bounds)
