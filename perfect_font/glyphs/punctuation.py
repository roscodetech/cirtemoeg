"""Punctuation: . , : ; ! ? - ( ) / ' " and symbols & @ # $ % + = * and space."""

from __future__ import annotations

from perfect_font.glyphs.base import FLAT, NARROW, ROUND, GlyphDef
from perfect_font.glyphs.parts import arc, arc_pt, carc, diag, hbar, joint, ring, vstem
from perfect_font.metrics import Metrics
from perfect_font.pens import draw_disc, draw_ring, draw_stroke


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


def plus(pen, m: Metrics) -> None:
    cap = m.cap_height
    midy = cap * 0.46
    half = cap * 0.26
    hbar(pen, m, 0, 2 * half, midy)                      # horizontal
    vstem(pen, m, half, midy - half, midy + half)        # vertical


def equal(pen, m: Metrics) -> None:
    cap = m.cap_height
    w = cap * 0.52
    hbar(pen, m, 0, w, cap * 0.56)
    hbar(pen, m, 0, w, cap * 0.36)


def asterisk(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    cy = cap * 0.72
    r = cap * 0.20
    import math
    for k in range(3):                                   # three crossing strokes -> 6 arms
        a = math.radians(60 * k + 90)
        dx, dy = r * math.cos(a), r * math.sin(a)
        draw_stroke(pen, (hs - dx, cy - dy), (hs + dx, cy + dy), m.stroke)


def numbersign(pen, m: Metrics) -> None:
    cap = m.cap_height
    w = cap * 0.62
    # two verticals (slightly sheared look via vertical bars) + two horizontals
    vstem(pen, m, w * 0.34, 0, cap)
    vstem(pen, m, w * 0.66, 0, cap)
    hbar(pen, m, 0, w, cap * 0.64)
    hbar(pen, m, 0, w, cap * 0.36)


def percent(pen, m: Metrics) -> None:
    cap = m.cap_height
    r = cap * 0.16
    draw_ring(pen, r, cap - r, r, m.stroke)              # upper-left ring
    draw_ring(pen, cap * 0.62 - r + r, r, r, m.stroke)   # lower-right ring
    diag(pen, m, (cap * 0.62, cap), (0.0, 0.0))          # slash through


def dollar(pen, m: Metrics) -> None:
    cap, hs = m.cap_height, m.half_stroke
    r = cap / 4
    cx = r
    # the S body
    carc(pen, m, cx, cap - r, r, 28, 270, cap1=True)
    carc(pen, m, cx, r, r, 28 + 180, 270 + 180, cap1=True)
    vstem(pen, m, cx, -cap * 0.12, cap * 1.12)           # vertical bar through


def ampersand(pen, m: Metrics) -> None:
    # Crossing 'et' form: an upper loop welded onto an open lower bowl, with a LEG
    # descending from the loop to a baseline foot and a TAIL rising from the bowl's
    # upper lip — the leg and tail cross on the right to form the ampersand knot.
    # Both free ends carry a ball terminal (echoing the serif teardrop terminals).
    cap = m.cap_height
    rt = cap * 0.185                                      # upper loop
    rb = cap * 0.24                                       # lower bowl
    cxt, cyt = cap * 0.295, cap * 0.62                    # loop lowered to overlap bowl
    cxb, cyb = cap * 0.285, rb
    ring(pen, m, cxt, cyt, rt)
    carc(pen, m, cxb, cyb, rb, 60, 300, cap0=True, cap1=True)  # bowl, mouth on the right
    joint(pen, m, cxb, cyb + rb)                         # weld loop to bowl top
    # leg: loop's lower-right down to a baseline foot (crossing pulled toward centre)
    leg0 = arc_pt(cxt, cyt, rt, -58)
    leg1 = (cap * 0.52, cap * 0.05)
    diag(pen, m, leg0, leg1)
    joint(pen, m, *leg0)
    draw_disc(pen, leg1[0], leg1[1], m.half_stroke)      # foot ball terminal
    # tail: bowl's upper lip rising steeply to the right (crosses the leg)
    up = arc_pt(cxb, cyb, rb, 60)
    tip = (cap * 0.64, cap * 0.66)
    diag(pen, m, up, tip)
    joint(pen, m, *up)
    draw_disc(pen, tip[0], tip[1], m.half_stroke)        # tail ball terminal


def at(pen, m: Metrics) -> None:
    # Outer ring open at the lower-right with a tail curling out, wrapping a small
    # lowercase 'a' (bowl ring + right stem) with a clearly open counter.
    cap = m.cap_height
    cx = cy = cap * 0.5
    R = cap * 0.45                                        # outer ring centreline radius
    carc(pen, m, cx, cy, R, -25, 250)                    # outer ring, open lower-right
    t0 = arc_pt(cx, cy, R, -25)
    diag(pen, m, t0, (cx + R * 1.05, cy - R * 0.1))      # tail flicking out
    rb = cap * 0.17                                       # inner 'a' bowl
    bx = cx - cap * 0.02
    ring(pen, m, bx, cy, rb)
    vstem(pen, m, bx + rb - m.half_stroke, cy - rb, cy + rb)  # 'a' stem


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
    GlyphDef("plus", 0x2B, plus, FLAT),
    GlyphDef("equal", 0x3D, equal, FLAT),
    GlyphDef("asterisk", 0x2A, asterisk, NARROW),
    GlyphDef("numbersign", 0x23, numbersign, FLAT),
    GlyphDef("percent", 0x25, percent, ROUND),
    GlyphDef("dollar", 0x24, dollar, ROUND),
    GlyphDef("ampersand", 0x26, ampersand, ROUND),
    GlyphDef("at", 0x40, at, ROUND),
]
