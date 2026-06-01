# Perfect Font — a parametric, mathematically-exact geometric typeface

A geometric font generated entirely from math. Every glyph is built from exact
primitives — true circles, constant-width strokes, exact arcs — driven by a single
parametric metrics model. Strict geometric purity is the base; optical correction is a
seam you can flip on later without redrawing a single glyph.

Two families build from the **same** glyph skeletons:
- **Cirtemoeg Sans** — proportional monoline geometric sans
- **Cirtemoeg Mono** — fixed-width, from the identical outlines

## The geometric contract

| Rule | Encoded as |
|------|-----------|
| `a` is exactly half as tall as `A` | `x_height == cap_height / 2` (derived property) |
| `b` is the same height as `A` | `ascender == cap_height` |
| `o` is perfectly round | true-circle annulus, `kappa = 0.5522847498307936` |
| uniform stroke | one `stroke` parameter, perpendicular width on every slant |
| strict purity | `overshoot = 0` by default; round/pointed glyphs sit exactly on metric lines |

Change one number in `metrics.py` (cap height, stroke weight, x-height ratio, overshoot)
and the entire font re-derives. Nothing is hard-coded per glyph.

## Install

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
```

Dependencies are pure-Python / prebuilt wheels (`fontmake`, `ufoLib2`, `fonttools`,
`skia-pathops`, `Pillow`) — no C toolchain, safe on spaced Windows paths.

## Build

```powershell
# both families + proof sheets into dist/
python -m perfect_font.cli --all --proof

# single variants / overrides
python -m perfect_font.cli --mono
python -m perfect_font.cli --optical --overshoot 12      # flip the optical seam on
python -m perfect_font.cli --cap 700 --stroke 96 --proof
```

Outputs: `dist/Cirtemoeg-Sans.otf`, `.ttf`, `Cirtemoeg-Mono.otf`, `.ttf`, and
`*-proof.png` specimen sheets with baseline / x-height / cap / descender guide lines.

## Architecture

```
metrics.py     parametric model (x=cap/2, asc=cap, overshoot seam)
geometry.py    pure math — kappa circle, arc-to-bezier, constant-width stroke, stadium
pens.py        primitive vocabulary (circle, ring, arc, disc, stroke, stadium)
glyphs/
  base.py      GlyphDef (declarative recipe = pure fn of Metrics)
  parts.py     shared sub-shapes (stem, bar, half-rings, arcs, bowl band)
  strokes.py   chevron — constant-width diagonal join (A V W M K X y ...)
  uppercase.py / lowercase.py / digits.py / punctuation.py
  __init__.py  registry + name↔unicode map + completeness guard
spacing.py     proportional sidebearings | monospace centred advance
ufo_builder.py declarative recipes -> ufoLib2.Font (normalised, spaced)
compile.py     ufo2ft -> .otf/.ttf with skia-pathops overlap removal
proof.py       Pillow specimen renderer
config.py/cli.py   build axes: spacing (sans|mono) x optics (strict|optical)
```

A glyph recipe speaks only in metric anchors and primitives, so one definition feeds
all four variants (sans/mono × strict/optical). Overlapping parts (b's stem+bowl, A's
apex join) are merged at compile time by pathops — recipes stay simple.

## Test

```powershell
python -m perfect_font.cli            # quick build
pytest                                 # geometric invariants (fast)
pytest -m compile                      # + full compile smoke (slow)
pytest --cov=perfect_font              # coverage
```

Tests assert outline math, not rasters: `o` bbox is a perfect square on its metric
lines, `x_height == cap/2`, ascenders reach cap, descenders reach the descender, stems
equal the stroke weight, designated glyphs are mirror-symmetric, monospace advances are
all equal, and the full set compiles to valid `.otf`/`.ttf` with complete cmap coverage.

## Design choices

- **Single-story `a` and `g`** (Futura-style) — the honest geometric forms.
- **x-height = cap/2 (350/700).** Deliberately literal to "a is half as tall as A";
  this is lower than typical text faces, so it reads distinctive/long-legged. It is a
  one-parameter change (`cap_height // 2`) if you ever want it taller.

## Status / refinement backlog

Core forms (straight + round + diagonal) are geometrically exact. A few curved glyphs
are first-pass and benefit from aesthetic tuning of their arc angles: `g j f t y`, the
digits `2 3 5 6 9`, the `G` spur and `Q` tail, and `?`. Because every glyph is a short
declarative recipe, tuning these is a localised, low-risk edit.

## Later (not built yet)
- Pixel/bitmap variant rendered from the same skeletons.
- Optical-correction tuning pass (the seam exists; values need eyeballing).
