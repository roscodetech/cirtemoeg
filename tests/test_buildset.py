"""Compile smoke test: the full font compiles to valid .otf/.ttf (slow)."""

from __future__ import annotations

import pytest
from fontTools.ttLib import TTFont

from perfect_font.compile import compile_font
from perfect_font.glyphs import ALL_GLYPHS
from perfect_font.metrics import Metrics
from perfect_font.ufo_builder import build_ufo


@pytest.mark.compile
@pytest.mark.parametrize("mono", [False, True])
def test_full_font_compiles_and_is_valid(tmp_path, mono):
    m = Metrics()
    font = build_ufo(ALL_GLYPHS, m, mono=mono)
    paths = compile_font(font, tmp_path, stem="probe")
    assert {p.suffix for p in paths} == {".otf", ".ttf"}

    for p in paths:
        tt = TTFont(p)
        assert tt["head"].unitsPerEm == 1000
        cmap = tt.getBestCmap()
        for ch in "AaZz0o .?":
            assert ord(ch) in cmap, f"{ch!r} missing from cmap in {p.name}"
        assert tt["OS/2"].sxHeight * 2 == pytest.approx(tt["OS/2"].sCapHeight, abs=2)
