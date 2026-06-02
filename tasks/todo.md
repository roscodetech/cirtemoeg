# Perfect Font — Task List

Parametric, mathematically-exact geometric font. Strict purity base, optical seam for later.
Plan: `~/.claude/plans/quiet-frolicking-peacock.md`.

## Phase 0 — Foundation  ✅
- [x] Scaffold + venv + toolchain (fontmake, ufoLib2, fontTools, Pillow, skia-pathops)
- [x] metrics.py (x=cap/2, asc=cap, overshoot seam) + tests
- [x] geometry.py (kappa circle, arc→bezier, constant-width stroke, stadium, winding orient) + tests
- [x] pens.py primitive vocabulary
- [x] glyphs/strokes.py chevron (constant-width diagonal join)
- [x] spacing.py proportional + monospace
- [x] ufo_builder.py + compile.py (ufo2ft → otf/ttf, pathops overlap removal)
- [x] proof.py specimen renderer

## Phase 1 — Full glyph set  ✅
- [x] ARC primitive + stadium (narrow 0)
- [x] uppercase A–Z, lowercase a–z (single-story a, g), digits 0–9, punctuation . , ? ! : ; ' " - ( ) / space
- [x] registry + unicode map + completeness guard (75 glyphs)
- [x] test_glyph_invariants (o square, asc=cap, descenders, symmetry, stroke const)
- [x] test_spacing (proportional + mono advances)

## Phase 2 — Build & verify  ✅
- [x] config.py + cli.py (sans|mono × strict|optical, --all, overrides)
- [x] test_buildset (full compile, reopen, validate upm/cmap/x=cap/2)
- [x] FIXED winding bug: white slashes through a/b/d/e/g/p/q (geometry.orient forces
      ccw solids / cw holes so pathops non-zero union never cancels overlaps)
- [x] Full proof sheets (Sans + Mono); bowls now solid
- [x] 67 tests pass (64 fast + 3 compile)

## Phase 2.5 — Join & jut cleanup  ✅
- [x] FIXED disjointed arcs: carc (centerline arc) + joint (round join disc) so r s S t f
      g j G ? 2 3 5 6 9 connect structurally (no gaps)
- [x] FIXED jutting diagonals: new `diag` primitive (horizontally flush-cut ends,
      thickness = stroke/sin θ to keep monoline). Converted all diagonals: chevron
      (A V W M v w), K M N Q R X Y Z k x y z, digits 1 2 4 7, slash. Apexes land exactly
      on metric lines. No perpendicular spikes past baseline/cap/x-height.

## Phase 2.6 — Per-glyph shape fixes (zoom review)  ✅
- [x] A crossbar no longer pokes past legs; K arms meet at one stem junction
- [x] M inner vee = sharp chevron (no blob); reaches near baseline
- [x] B rebuilt: two equal cap/4 bowls attached to stem, meet at waist
- [x] G: proper inward bar + right upstem (was a stubby nub)
- [x] J clean hook; S bottom bowl = exact 180-deg rotation of top (symmetric)
- [x] e: near-full ring, open eye above a lowered crossbar (was a closed blob)
- [x] m: two even round shoulders matching n (was tight flat-topped humps)
- [x] G spur re-anchored to arc terminal (was floating tick); J enlarged hook
      (r 0.28->0.34); K arms back to perpendicular draw_stroke (diag balloons at
      shallow angles: width=stroke/sinθ). 67 tests pass.
- NOTE: use `diag` (horizontal flush cut) only for steep diagonals that hit a metric
  line; for shallow/free-standing arms use draw_stroke to avoid weight ballooning.
- [x] e: open eye (bar at 0.80r, aperture terminal at -18deg tucks under bowl, no foot)
- [x] m: ROUND shoulders matching n. KEY RULE: a monoline arch reads round only when
  counter width == inner-arch diameter, i.e. stem centre-spacing = 2*r_a - stroke.
  Inner stems stop at the spring line cy (only the left stem rises to x-height).
- [x] e (again): arc starts where crossbar meets right wall (asin), 305-deg sweep like c
- [x] digits: 2 connected (arc->diag->base), 5 bowl joins stem, 9 closed ring + smooth
  tail to baseline (mirror of 6). 0 1 3 4 6 7 8 already good.
- [x] ? proper hook (opens lower-left, over top, stem to dot); ( ) gentle blunt-ended
  curves (large radius cap*0.95, narrow sweep) not pointed bows.
- NOTE: glyph set is a-z A-Z 0-9 . , ? ! : ; ' " - ( ) / space. & @ # $ % + = * are
  NOT included -> they render as .notdef box. Add on request.
- [x] digits 6/8/9 DISCONNECTED -> fixed. KEY RULE: tangent circles do NOT merge under
  boolean union (single touch point = zero-width join). Pieces must genuinely OVERLAP.
  8: drop/raise the two rings so they intersect at the waist.
- [x] 6/9 "drunk"/lopsided (giant-radius single arc swung wild) -> REBUILT as
  bowl + near-vertical stem rising from it + small top hook (hook_r = 0.92*rb). Bowl
  dominates, stem keeps it upright, modest hook curves over without swinging out.
  9 = exact 180-deg mirror.
- [x] 1/2/4/5 connection+spike cleanup: 1 flag = full-weight parallelogram (was thin
  sliver) flush at cap; 2 diagonal joints to arc terminal + base; 4 diagonal starts
  below stem top, tucks into crossbar (no stray joint left of bar); 5 bar clamped to
  cap-hs, bowl overlaps stem foot. All connected, no spikes.
- NOTE: the proof's green cap guide line renders a hair BELOW true cap, so flush-at-cap
  strokes LOOK like they spike above it. Verify ymax==cap numerically before chasing
  a phantom spike (1's ymax was exactly 700==cap; the "spike" was guide-line offset).
- [x] 2/4 "jutty": cause was `joint` discs poking past the stroke silhouette + diagonal
  ends landing below/left of the covering stroke. FIX: draw the covering stroke (base
  bar / crossbar / stem) so it OVERLAPS the junction, drop the joint disc, and land the
  diagonal foot ON the bar (not below it). Verify bounds have no negative x.
- [x] ? hook rebuilt: start horizontal on the LEFT (180 deg, no dangling foot), sweep
  over top + down right, curl to -110, short stem from the curl end down to the dot.
- [x] 2 "chip" + 4 "jagged edges": diagonal meeting a curve/stroke leaves a concave
  notch (chip) or a misaligned step (jag) when edges don't align. FIX: start the
  diagonal from a point computed ON the other piece's geometry (arc_pt on the arc circle
  for 2; the stem's exact top corner for 4), end the arc exactly at that join, and add a
  small rounding joint at a curve->diagonal shoulder. Draw order: bar/stem that should
  cover the junction goes last.
- [x] 2/4 "nub sticking out": ROOT CAUSE = `diag` (horizontal flush cut) has width
  stroke/sin(theta); on a STEEP diagonal that cut spreads sideways and pokes ~4u past
  the stroke it joins -> visible nub.
- [x] 2/4 "jaggered" (FINAL FIX): overlapping two separate rectangles at an angle makes
  a stepped/faceted junction. The robust fix is to build the diagonal limb as ONE filled
  draw_polygon whose edges land FLUSH on the strokes it joins (stem left edge + crossbar
  top for 4; arc shoulder + base bar for 2), and draw the orthogonal covering strokes
  (stem/crossbar/base bar) so the diagonal's buried corners are absorbed.
- THE STANDARD (user-corrected): the bar is NOT "connected / no poke" -- it is SMOOTHNESS.
  Compare 2 vs 5: a curve must flow, and where it meets a straight it makes exactly ONE
  CRISP corner, never a faceted/kinked multi-step mess. To get one crisp shoulder where an
  ARC meets a DIAGONAL: make the diagonal's top edge BE the arc's flat radial terminal cut
  (share the SAME edge: outer = arc_pt(r+hs, a_end), inner = arc_pt(r-hs, a_end); the
  diagonal is the parallelogram hanging off that radial cut, both long edges parallel,
  offset by (outer-inner)). Shared edge => single corner, zero facets. Feet land at y=s
  (base-bar top) so nothing dips below baseline. ALWAYS judge at 900px against the 5.

## Phase 3 — later
- [ ] Aesthetic polish: single-story g/a feel, ? hook, digit 2 gentleness
- [ ] Pixel/bitmap variant from the same skeletons (user: "geometric first, pixel after")
- [ ] Optical correction tuning (flip overshoot_enabled, eyeball overshoot values)

## Review
Built a parametric geometric-font generator from scratch. Architecture is the win: one
`Metrics` model drives everything, glyphs are declarative pure functions, four variants
(sans/mono × strict/optical) fall out of config permutations with zero per-glyph
duplication. Geometric invariants enforced by unit tests on outline math (not rasters):
perfect-square o, x=cap/2, ascenders/descenders on their lines, constant stroke, mirror
symmetry. Pipeline proven end-to-end: declarative recipe → ufoLib2 UFO → ufo2ft/
skia-pathops → installable .otf/.ttf, with Pillow proof sheets.

Key fixes: ufo2ft (not fontmake.run_from_ufos, which rescaled UPM across double calls);
skia-pathops as overlap backend; contour winding orientation (the slash artifact).

Honest gap: straight/round/diagonal glyphs are geometrically exact and look clean; several
arc-based glyphs (G/Q/S/?, parens, digits 2/3/5/6/9) are first-pass and want arc-angle
tuning — cheap localised edits given the declarative recipes.

CAUTION (this session): tool channel intermittently returned phantom "success" results;
verify writes with ls/grep and outputs with a real file read before trusting.

## Full-sweep findings (2026-06-01, name = Cirtemoeg, repo pushed dev+prod)
Rendered all 75 glyphs at 170px (sweepU/sweepL) + zooms. Status of junctions vs the
"smoothness like 5" standard:
- [x] r shoulder: jutting flat terminal -> ended arc at +20deg (clean up-right arm). DONE.
- [ ] B: waist join slightly pinched/uneven (zoom at 600px, even the two bowls).
- [ ] G: spur/bar junction -- verify at 600px for facet.
- [ ] f: top hook terminal blunt (acceptable but could ease); crossbar junction ok.
- [ ] g / j tails: terminals blunt (acceptable, low priority).
- Uppercase A C D E F H I J K L M N O P Q R S T U V W X Y Z: clean at 170px.
- Lowercase a b c d e h i k l m n o p q s t u v w x y z: clean at 170px.
- Digits 0-9: clean (2/4/6/8/9 all rebuilt this session).
- Punct . , ? ! : ; - ( ) / : clean.
NEXT: zoom B and G at 600px, apply shared-edge / clean-terminal fixes if faceted.
Repo: github.com/roscodetech/cirtemoeg (dev + prod). Family "Cirtemoeg Sans/Mono".

## Correctness + symmetry sweep (2026-06-01, session 2)
Fixed the three reported defects, then ran a quantitative symmetry audit over all 80 glyphs.
- [x] s: bottom bowl now the EXACT 180deg rotation of the top about the waist (was a 295deg
  sweep vs the top's 245deg). Lower-left terminal mirrors upper-right. Locked by
  test_point_symmetry.
- [x] r: shoulder rebuilt on n's geometry (radius 0.44x, centre offset hs+r_a) so it arcs
  180deg->25deg off the stem — rounds exactly like n, arm points up-right, no droop.
- [x] g / j: shared `stem_with_tail` helper (radius 0.42x, half-circle to descender) so the
  underhangs are IDENTICAL in width and length. Locked by test_g_and_j_underhangs_identical.
- [x] u: right stem dropped to baseline (asymmetric vs the symmetric U). Now both stems
  spring cy->x; u is left-right symmetric like U. Locked by test_vertical_axis_symmetry.
- Audit (symmetry_audit.py) clean: only K TB=0.107 (deliberate 0.48cap junction) and a
  raster-noise floor of <=0.042 on diagonal/thin glyphs (N s S T *) remain — all expected.
- Dev tools added: glyph_lab.py (big guided single-glyph render), variant_lab.py
  (candidate compare), render_chars.py (guided rows), symmetry_audit.py (LR/TB/ROT residuals).
- 72 tests pass (8 new invariants). Font rebuilt: dist/Cirtemoeg-Sans.{otf,ttf} + proof.
