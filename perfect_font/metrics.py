"""The parametric metrics model.

Every dimension in the font derives from this single dataclass. The user's hard
constraints are encoded as *derived properties* so they cannot drift:

    x_height == cap_height / 2      ("a is half as tall as A")
    ascender == cap_height         ("b is the same height as A")

Overshoot is the *optical-correction seam*: strict geometric purity is the default
(``overshoot_enabled=False`` => every round/pointed extremum sits exactly on its metric
line). Flip ``overshoot_enabled=True`` later and the *same glyph recipes* start
overshooting -- no glyph is ever redrawn.
"""

from __future__ import annotations

from dataclasses import dataclass

# Control-point distance for approximating a quarter circle with one cubic Bezier.
# k = 4/3 * (sqrt(2) - 1). Centralised here so every "true circle" is identical.
KAPPA = 0.5522847498307936


@dataclass(frozen=True)
class Metrics:
    # --- primary free parameters ---
    upm: int = 1000          # units per em (CFF/OTF standard grid)
    cap_height: int = 700    # height of A..Z and of ascenders
    stroke: int = 88         # monoline weight, uniform everywhere
    descender: int = -300    # below baseline (negative): g j p q y, comma

    # --- optical-correction seam (strict by default) ---
    overshoot: int = 12          # applied to round/pointed extrema WHEN enabled
    overshoot_enabled: bool = False

    # --- proportional spacing sidebearings ---
    side_flat: int = 80      # straight-sided glyphs (H, n, l)
    side_round: int = 64     # round-sided glyphs (o, c, O) tuck in slightly
    side_narrow: int = 48    # i, j, punctuation

    # --- monospace cell ---
    mono_advance: int = 600

    def __post_init__(self) -> None:
        if self.upm <= 0:
            raise ValueError(f"upm must be positive, got {self.upm}")
        if self.cap_height <= 0 or self.cap_height % 2 != 0:
            raise ValueError(f"cap_height must be a positive even integer, got {self.cap_height}")
        if self.stroke <= 0 or self.stroke % 2 != 0:
            raise ValueError(f"stroke must be a positive even integer, got {self.stroke}")
        if self.stroke >= self.x_height:
            raise ValueError(
                f"stroke ({self.stroke}) must be smaller than x_height ({self.x_height})"
            )

    # ---- derived invariants (cannot drift) ----
    @property
    def x_height(self) -> int:
        """Exactly half the cap height: 'a is half as tall as A'."""
        return self.cap_height // 2

    @property
    def ascender(self) -> int:
        """Ascenders reach cap height: 'b is the same height as A'."""
        return self.cap_height

    @property
    def baseline(self) -> int:
        return 0

    @property
    def half_stroke(self) -> int:
        return self.stroke // 2

    @property
    def figure_height(self) -> int:
        """Lining figures: digits are cap height."""
        return self.cap_height

    # ---- overshoot resolution (the seam) ----
    def _over(self) -> int:
        return self.overshoot if self.overshoot_enabled else 0

    def round_top(self, top: float) -> float:
        return top + self._over()

    def round_bottom(self, bot: float) -> float:
        return bot - self._over()

    def pointed_top(self, top: float) -> float:
        return top + self._over()

    def pointed_bottom(self, bot: float) -> float:
        return bot - self._over()
