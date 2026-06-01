"""BuildConfig metric resolution + CLI entry point."""

from __future__ import annotations

import pytest
from fontTools.ttLib import TTFont

from perfect_font.cli import main
from perfect_font.config import BuildConfig


def test_config_defaults_to_strict_sans():
    cfg = BuildConfig()
    m = cfg.metrics()
    assert not m.overshoot_enabled
    assert cfg.stem == "Cirtemoeg-Sans"


def test_config_optical_and_mono_naming():
    cfg = BuildConfig(mono=True, optical=True)
    assert cfg.metrics().overshoot_enabled
    assert cfg.stem == "Cirtemoeg-Mono-Optical"


def test_config_metric_overrides():
    cfg = BuildConfig(cap_height=800, stroke=100, overshoot=20, optical=True)
    m = cfg.metrics()
    assert m.cap_height == 800
    assert m.stroke == 100
    assert m.x_height == 400
    assert m.round_top(400) == 420


@pytest.mark.compile
def test_cli_builds_mono_font(tmp_path):
    rc = main(["--mono", "--out", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / "Cirtemoeg-Mono.otf").exists()
    ttf = tmp_path / "Cirtemoeg-Mono.ttf"
    assert ttf.exists()
    assert TTFont(ttf)["post"].isFixedPitch != 0
