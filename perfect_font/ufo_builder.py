"""Assemble a ufoLib2.Font from glyph definitions + metrics + spacing mode."""

from __future__ import annotations

import ufoLib2
from fontTools.misc.transform import Offset
from fontTools.pens.boundsPen import ControlBoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen

from perfect_font import spacing
from perfect_font.glyphs.base import GlyphDef
from perfect_font.metrics import Metrics


def _draw_into(font_glyph, gdef: GlyphDef, metrics: Metrics, *, mono: bool) -> int:
    """Draw a glyph, place it, return its advance width."""
    if gdef.is_blank:
        # Blank glyphs (space) get a fixed advance and no contours.
        return metrics.mono_advance if mono else metrics.cap_height // 2

    recording = RecordingPen()
    gdef.recipe(recording, metrics)

    bounds_pen = ControlBoundsPen(None)
    recording.replay(bounds_pen)
    if bounds_pen.bounds is None:  # pragma: no cover - defensive
        raise ValueError(f"glyph {gdef.name!r} produced no contours")

    advance, dx = spacing.place(metrics, gdef.spacing, bounds_pen.bounds, mono=mono)
    recording.replay(TransformPen(font_glyph.getPen(), Offset(dx, 0)))
    return advance


def build_ufo(
    glyphdefs: list[GlyphDef],
    metrics: Metrics,
    *,
    mono: bool,
    family_name: str = "Cirtemoeg",
) -> ufoLib2.Font:
    style = "Mono" if mono else "Sans"
    font = ufoLib2.Font()
    info = font.info
    info.unitsPerEm = metrics.upm
    info.familyName = f"{family_name} {style}"
    info.styleName = "Regular"
    info.ascender = metrics.ascender
    info.descender = metrics.descender
    info.capHeight = metrics.cap_height
    info.xHeight = metrics.x_height
    info.openTypeOS2TypoAscender = metrics.cap_height
    info.openTypeOS2TypoDescender = metrics.descender
    info.openTypeOS2TypoLineGap = 0
    info.openTypeHheaAscender = metrics.cap_height
    info.openTypeHheaDescender = metrics.descender
    if mono:
        info.postscriptIsFixedPitch = True

    for gdef in glyphdefs:
        glyph = font.newGlyph(gdef.name)
        glyph.width = _draw_into(glyph, gdef, metrics, mono=mono)
        if gdef.unicode is not None:
            glyph.unicodes = [gdef.unicode]

    return font
