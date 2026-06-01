"""Build configuration: the two independent axes (spacing mode, optics) + overrides."""

from __future__ import annotations

from dataclasses import dataclass

from perfect_font.metrics import Metrics


@dataclass(frozen=True)
class BuildConfig:
    mono: bool = False
    optical: bool = False
    formats: tuple[str, ...] = ("otf", "ttf")
    family_name: str = "Cirtemoeg"
    cap_height: int | None = None
    stroke: int | None = None
    overshoot: int | None = None

    def metrics(self) -> Metrics:
        kwargs: dict[str, object] = {"overshoot_enabled": self.optical}
        if self.cap_height is not None:
            kwargs["cap_height"] = self.cap_height
        if self.stroke is not None:
            kwargs["stroke"] = self.stroke
        if self.overshoot is not None:
            kwargs["overshoot"] = self.overshoot
        return Metrics(**kwargs)

    @property
    def stem(self) -> str:
        style = "Mono" if self.mono else "Sans"
        optic = "-Optical" if self.optical else ""
        return f"{self.family_name}-{style}{optic}"
