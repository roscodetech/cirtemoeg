"""Punctuation: . , : ; ! ? - ( ) / ' " and space."""

from __future__ import annotations

from perfect_font.glyphs.base import NARROW, GlyphDef
from perfect_font.glyphs.parts import arc, carc, diag, hbar, joint, vstem
from perfect_font.metrics import Metrics
from perfect_font.pens import draw_disc, draw_stroke


def _dot(pen, m: Metrics, cx: float, cy: float) -> None:
    draw_disc(pen, cx, cy, m.half_stroke)


def _comma_tail(pen, m: Metrics, cx: float, top: float) -> None:
    hs = m.half_stroke
    _dot(pen, m, cx, top)
    draw_stroke(pen, (cx, top), (cx - hs * 0.8, top - m.stroke * 1.7), m.stroke)


def period(pen, m: Metrics) -> None:
    _dot(pen, m, m.half_stroke, m.half_stroke)


def comma(pen, m: Metrics) -> None:
    _comma_tail(pen, m, m.half_stroke, m.half_stroke)


def colon(pen, m: Metrics) -> None:
    hs = m.half_stroke
    _dot(pen, m, hs, hs)
    _dot(pen, m, hs, m.x_height - hs)


def semicolon(pen, m: Metrics) -> None:
    hs = m.half_stroke
    _dot(pen, m, hs, m.x_height - hs)
    _comma_tail(pen, m, hs, hs)


def exclam(pen, m: Metrics) -> None:
    hs = m.half_stroke
    vstem(pen, m, hs, m.stroke * 1.7, m.cap_height)
    _dot(pen, m, hs, hs)


def question(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    r = cap * 0.26
    cyy = cap - r
    cx = r
    # hook: start on the LEFT at mid-height (180 deg, horizontal -> no dangling foot),
    # sweep up over the top, down the right, and curl back in to the bottom centre.
    _p0, term = carc(pen, m, cx, cyy, r, 180, -110, cap1=True)
    # short stem drops from the curl's inner end straight down toward the dot.
    stem_x = term[0]
    vstem(pen, m, stem_x, cap * 0.30, term[1])
    joint(pen, m, stem_x, term[1])
    _dot(pen, m, stem_x, hs)


def hyphen(pen, m: Metrics) -> None:
    hbar(pen, m, 0, m.x_height * 0.55, m.x_height / 2)


def parenleft(pen, m: Metrics) -> None:
    cap = m.cap_height
    r = cap * 0.95            # large radius -> shallow, gentle curve
    cyy = cap * 0.42
    arc(pen, m, r, cyy, r, 155, 205)   # narrow sweep -> near-vertical, blunt ends


def parenright(pen, m: Metrics) -> None:
    cap = m.cap_height
    r = cap * 0.95
    cyy = cap * 0.42
    arc(pen, m, -r, cyy, r, -25, 25)


def slash(pen, m: Metrics) -> None:
    cap = m.cap_height
    diag(pen, m, (0.0, m.descender * 0.4), (cap * 0.5, cap))


def quotesingle(pen, m: Metrics) -> None:
    _comma_tail(pen, m, m.half_stroke, m.cap_height)


def quotedbl(pen, m: Metrics) -> None:
    s = m.stroke
    _comma_tail(pen, m, m.half_stroke, m.cap_height)
    _comma_tail(pen, m, m.half_stroke + s * 1.4, m.cap_height)


PUNCTUATION: list[GlyphDef] = [
    GlyphDef("space", 0x20, lambda *_: None, NARROW, is_blank=True),
    GlyphDef("period", 0x2E, period, NARROW),
    GlyphDef("comma", 0x2C, comma, NARROW),
    GlyphDef("colon", 0x3A, colon, NARROW),
    GlyphDef("semicolon", 0x3B, semicolon, NARROW),
    GlyphDef("exclam", 0x21, exclam, NARROW),
    GlyphDef("question", 0x3F, question, NARROW),
    GlyphDef("hyphen", 0x2D, hyphen, NARROW),
    GlyphDef("parenleft", 0x28, parenleft, NARROW),
    GlyphDef("parenright", 0x29, parenright, NARROW),
    GlyphDef("slash", 0x2F, slash, NARROW),
    GlyphDef("quotesingle", 0x27, quotesingle, NARROW),
    GlyphDef("quotedbl", 0x22, quotedbl, NARROW),
]
