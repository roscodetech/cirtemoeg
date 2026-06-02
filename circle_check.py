"""Overlay round glyphs to prove every bowl is the same circle.
Renders each glyph from the compiled font onto a shared baseline/left origin and
tints them, so coincident bowls land exactly on top of each other."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from perfect_font.metrics import Metrics

m = Metrics()
S = 700
scale = S / m.upm
font = ImageFont.truetype("dist/Cirtemoeg-Sans.ttf", S)
PAD = 80
BASE = (PAD, PAD + int(m.cap_height * scale))
W = PAD * 2 + int(m.x_height * scale) + 40
H = PAD * 2 + int(m.cap_height * scale)


def mask(ch: str) -> np.ndarray:
    img = Image.new("L", (W, H), 0)
    ImageDraw.Draw(img).text(BASE, ch, font=font, fill=255, anchor="ls")
    return np.asarray(img) > 64


def tint(msk, color):
    layer = np.zeros((H, W, 4), np.uint8)
    layer[msk] = (*color, 130)
    return Image.fromarray(layer, "RGBA")


def guides(img):
    d = ImageDraw.Draw(img)
    for fy, c in [(0, "#cc3333"), (m.x_height, "#3399cc"), (m.cap_height, "#33aa55")]:
        y = BASE[1] - fy * scale
        d.line([(0, y), (W, y)], fill=c, width=1)
    return img


def overlay(pairs, name):
    base = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    for ch, col in pairs:
        base.alpha_composite(tint(mask(ch), col))
    guides(base)
    out = Path("dist/lab") / name
    base.convert("RGB").save(out)


def main():
    Path("dist/lab").mkdir(parents=True, exist_ok=True)
    overlay([("o", (0, 0, 0)), ("c", (220, 30, 30))], "circle_o_vs_c.png")
    overlay([("a", (0, 0, 0)), ("d", (220, 30, 30))], "circle_a_vs_d.png")
    overlay([("o", (30, 30, 30)), ("a", (220, 30, 30)), ("b", (30, 150, 30)),
             ("d", (30, 30, 220)), ("p", (200, 140, 0)), ("q", (180, 0, 180))],
            "circle_all_bowls.png")
    print("wrote circle_o_vs_c.png, circle_a_vs_d.png, circle_all_bowls.png")


if __name__ == "__main__":
    main()
