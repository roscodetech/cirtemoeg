"""The declarative glyph data model.

A glyph recipe is a *pure function of Metrics* that draws into a pen using glyph-local
coordinates. It bakes in no sidebearing (the spacing engine normalises placement) and
resolves strict-vs-optical entirely through Metrics, so one recipe serves all four
build variants (proportional/mono x strict/optical).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from perfect_font.metrics import Metrics

# A recipe receives (pen, metrics) and draws one glyph.
Recipe = Callable[[object, Metrics], None]

# Spacing classes drive proportional sidebearing selection.
FLAT = "flat"
ROUND = "round"
NARROW = "narrow"


@dataclass(frozen=True)
class GlyphDef:
    name: str
    unicode: int | None
    recipe: Recipe
    spacing: str = FLAT
    is_blank: bool = False  # space: no contours, fixed advance
