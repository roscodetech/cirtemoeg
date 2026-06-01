"""Render a specimen PNG from a compiled font, with metric guide lines."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from perfect_font.metrics import Metrics

ROWS = [
    "ABCDEFGHIJKLM",
    "NOPQRSTUVWXYZ",
    "abcdefghijklm",
    "nopqrstuvwxyz",
    "0123456789",
    ".,?!:;'\"-()/ Hoxbqg",
]


def render_proof(
    font_path: Path,
    out_png: Path,
    metrics: Metrics,
    *,
    size: int = 150,
    guides: bool = True,
    rows: list[str] | None = None,
) -> Path:
    if rows is None:
        rows = ROWS
    scale = size / metrics.upm
    cap = metrics.cap_height * scale
    xh = metrics.x_height * scale
    desc = -metrics.descender * scale
    font = ImageFont.truetype(str(font_path), size)

    margin = 60
    line_h = int((metrics.cap_height - metrics.descender) * scale + 60)
    width = 1500
    height = margin * 2 + line_h * len(rows)
    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)

    for i, row in enumerate(rows):
        baseline = margin + line_h * i + cap
        if guides:
            for y, color in [
                (baseline, "#cc3333"),
                (baseline - xh, "#3399cc"),
                (baseline - cap, "#33aa55"),
                (baseline + desc, "#bbbbbb"),
            ]:
                d.line([(margin, y), (width - margin, y)], fill=color, width=1)
        d.text((margin, baseline), row, font=font, fill="black", anchor="ls")

    out_png.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_png)
    return out_png
