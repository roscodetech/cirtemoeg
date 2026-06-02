"""Quantitative symmetry audit of the compiled font.

For each glyph we rasterise the outline, crop to its ink, and measure the residual
(fraction of mismatched pixels) under three transforms:

  LR  : left-right mirror      (vertical axis of symmetry)
  TB  : top-bottom mirror      (horizontal axis of symmetry)
  ROT : 180-degree rotation    (point symmetry -- S, Z, N, s, z, n-ish)

A glyph is only *expected* to be symmetric under some of these; the EXPECT map below
encodes the design intent. Residual is reported for the expected axes; anything above
~3% on an expected axis is a real asymmetry worth fixing.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFont

from perfect_font.metrics import Metrics

TTF = Path("dist/Cirtemoeg-Sans.ttf")
SIZE = 400

# expected symmetry axes per glyph (others left blank -> reported as FYI only)
EXPECT = {
    "A": "LR", "H": "LR+TB", "I": "LR+TB", "M": "LR", "O": "LR+TB", "T": "LR",
    "U": "LR", "V": "LR", "W": "LR", "X": "LR+TB", "Y": "LR", "N": "ROT",
    "S": "ROT", "Z": "ROT", "B": "TB", "C": "TB", "D": "TB", "E": "TB",
    "K": "TB", "o": "LR+TB", "x": "LR+TB", "v": "LR", "w": "LR", "s": "ROT",
    "z": "ROT", "l": "LR", "i": "LR", "0": "LR+TB", "8": "LR", "1": "",
    "c": "TB", "e": "", "u": "LR", "n": "", "H": "LR+TB", "+": "LR+TB",
    "*": "LR+TB", "=": "LR+TB", "-": "LR+TB", ".": "LR+TB", "#": "LR+TB",
    "t": "", "f": "", "r": "", "k": "", "y": "",  # 8 small top bowl; y has a descender
}


def glyph_bitmap(font: ImageFont.FreeTypeFont, ch: str) -> np.ndarray | None:
    big = SIZE * 3
    img = Image.new("L", (big, big), 0)
    from PIL import ImageDraw

    d = ImageDraw.Draw(img)
    d.text((big // 2, big // 2), ch, font=font, fill=255, anchor="mm")
    arr = np.asarray(img)
    ys, xs = np.where(arr > 64)
    if len(xs) == 0:
        return None
    crop = arr[ys.min(): ys.max() + 1, xs.min(): xs.max() + 1]
    return (crop > 64).astype(np.uint8)


def residual(a: np.ndarray, b: np.ndarray) -> float:
    h = max(a.shape[0], b.shape[0])
    w = max(a.shape[1], b.shape[1])

    def pad(x):
        out = np.zeros((h, w), np.uint8)
        oy = (h - x.shape[0]) // 2
        ox = (w - x.shape[1]) // 2
        out[oy:oy + x.shape[0], ox:ox + x.shape[1]] = x
        return out

    A, B = pad(a), pad(b)
    union = (A | B).sum()
    if union == 0:
        return 0.0
    return float((A ^ B).sum()) / float(union)


def main() -> None:
    m = Metrics()
    font = ImageFont.truetype(str(TTF), SIZE)
    chars = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "abcdefghijklmnopqrstuvwxyz"
             "0123456789"
             ".,?!:;'\"-()/+=*#$%&@")
    print(f"{'ch':>3} {'LR':>6} {'TB':>6} {'ROT':>6}  expect")
    print("-" * 40)
    flagged = []
    for ch in chars:
        bm = glyph_bitmap(font, ch)
        if bm is None:
            continue
        lr = residual(bm, bm[:, ::-1])
        tb = residual(bm, bm[::-1, :])
        rot = residual(bm, bm[::-1, ::-1])
        exp = EXPECT.get(ch, "")
        mark = ""
        for axis, val in (("LR", lr), ("TB", tb), ("ROT", rot)):
            if axis in exp and val > 0.03:
                mark += f" !{axis}={val:.3f}"
                flagged.append((ch, axis, val))
        print(f"{ch!r:>3} {lr:6.3f} {tb:6.3f} {rot:6.3f}  {exp:7}{mark}")
    print("-" * 40)
    if flagged:
        print("FLAGGED (expected-symmetric axis residual > 3%):")
        for ch, axis, val in sorted(flagged, key=lambda t: -t[2]):
            print(f"  {ch!r} {axis} = {val:.3f}")
    else:
        print("No expected-symmetry violations above 3%.")


if __name__ == "__main__":
    main()
