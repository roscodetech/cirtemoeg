"""Spacing engine: proportional sidebearings and monospace advances."""

from __future__ import annotations

import pytest

from perfect_font.glyphs import ALL_GLYPHS
from perfect_font.metrics import Metrics
from perfect_font.ufo_builder import build_ufo


@pytest.fixture
def m() -> Metrics:
    return Metrics()


def test_monospace_all_advances_equal(m):
    font = build_ufo(ALL_GLYPHS, m, mono=True)
    widths = {g.name: font[g.name].width for g in ALL_GLYPHS}
    assert set(widths.values()) == {m.mono_advance}


def test_proportional_round_glyph_sidebearings(m):
    font = build_ufo(ALL_GLYPHS, m, mono=False)
    o = font["o"]
    b = o.getBounds(font)
    left = b.xMin
    right = o.width - b.xMax
    assert abs(left - m.side_round) < 1.0
    assert abs(right - m.side_round) < 1.0


def test_proportional_round_glyph_is_centred(m):
    font = build_ufo(ALL_GLYPHS, m, mono=False)
    o = font["o"]
    b = o.getBounds(font)
    left = b.xMin
    right = o.width - b.xMax
    assert abs(left - right) < 1.5


def test_space_has_advance_but_no_contours(m):
    font = build_ufo(ALL_GLYPHS, m, mono=False)
    space = font["space"]
    assert space.width > 0
    assert len(space) == 0
