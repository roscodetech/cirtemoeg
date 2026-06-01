"""Glyph registry: the single source of which glyphs exist and their codepoints."""

from __future__ import annotations

from perfect_font.glyphs.base import GlyphDef
from perfect_font.glyphs.digits import DIGITS
from perfect_font.glyphs.lowercase import LOWERCASE
from perfect_font.glyphs.punctuation import PUNCTUATION
from perfect_font.glyphs.uppercase import UPPERCASE

ALL_GLYPHS: list[GlyphDef] = [*UPPERCASE, *LOWERCASE, *DIGITS, *PUNCTUATION]

REGISTRY: dict[str, GlyphDef] = {g.name: g for g in ALL_GLYPHS}

if len(REGISTRY) != len(ALL_GLYPHS):  # pragma: no cover - guards duplicate names
    seen: set[str] = set()
    dupes = {g.name for g in ALL_GLYPHS if g.name in seen or seen.add(g.name)}
    raise ValueError(f"duplicate glyph names: {sorted(dupes)}")


def unicodes() -> dict[int, str]:
    return {g.unicode: g.name for g in ALL_GLYPHS if g.unicode is not None}
