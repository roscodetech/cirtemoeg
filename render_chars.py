"""Render arbitrary strings from the compiled font as big guided rows / pairs."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from perfect_font.metrics import Metrics

TTF = Path("dist/Cirtemoeg-Sans.ttf")


def row(text: str, size: int, name: str) -> Path:
    m = Metrics()
    scale = size / m.upm
    cap = m.cap_height * scale
    xh = m.x_height * scale
    desc = -m.descender * scale
    font = ImageFont.truetype(str(TTF), size)
    pad = 50
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    tw = int(d0.textlength(text, font=font))
    w = tw + pad * 2
    h = int((m.cap_height - m.descender) * scale) + pad * 2
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    baseline = pad + cap
    for y, color in [(baseline, "#e0a0a0"), (baseline - xh, "#a0c8e0"),
                     (baseline - cap, "#a0d8b0"), (baseline + desc, "#e0c89a")]:
        d.line([(0, y), (w, y)], fill=color, width=1)
    d.text((pad, baseline), text, font=font, fill="black", anchor="ls")
    out = Path("dist/lab") / f"row_{name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def main() -> None:
    if len(sys.argv) > 2:
        print(row(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 3 else 200, sys.argv[2]))
        return
    row("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 150, "upper")
    row("abcdefghijklmnopqrstuvwxyz", 150, "lower")
    row("0123456789", 170, "digits")
    row(".,?!:;'\"-()/+=*#$%&@", 170, "symbols")
    row("uU nN Kk", 320, "uUnNKk")
    row("Ss Zz 8 oO", 300, "SsZz8")
    print("wrote row_*.png")


if __name__ == "__main__":
    main()
