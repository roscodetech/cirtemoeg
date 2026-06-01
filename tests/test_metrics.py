"""Metrics invariants: the user's hard rules and the overshoot seam."""

from __future__ import annotations

import pytest

from perfect_font.metrics import KAPPA, Metrics


def test_x_height_is_exactly_half_cap():
    m = Metrics(cap_height=700)
    assert m.x_height == 350
    assert m.x_height * 2 == m.cap_height


def test_ascender_equals_cap_height():
    m = Metrics()
    assert m.ascender == m.cap_height


def test_kappa_value():
    assert KAPPA == pytest.approx(4 / 3 * (2**0.5 - 1), abs=1e-15)


def test_overshoot_strict_by_default():
    m = Metrics(overshoot=20)  # value present but disabled
    assert m.round_top(350) == 350
    assert m.round_bottom(0) == 0
    assert m.pointed_top(700) == 700
    assert m.pointed_bottom(0) == 0


def test_overshoot_seam_applies_when_enabled():
    m = Metrics(overshoot=12, overshoot_enabled=True)
    assert m.round_top(350) == 362
    assert m.round_bottom(0) == -12
    assert m.pointed_top(700) == 712


@pytest.mark.parametrize(
    "kwargs",
    [
        {"cap_height": 701},   # odd -> x-height not integral
        {"cap_height": 0},
        {"stroke": 87},        # odd
        {"stroke": 0},
        {"upm": 0},
        {"stroke": 400},       # >= x_height (350)
    ],
)
def test_invalid_parameters_fail_fast(kwargs):
    with pytest.raises(ValueError):
        Metrics(**kwargs)
