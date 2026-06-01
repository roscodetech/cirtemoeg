"""Compile a ufoLib2.Font to .otf and/or .ttf via ufo2ft (fontmake's own engine).

We call ufo2ft's compileOTF/compileTTF directly rather than fontmake's
run_from_ufos, because the latter mutates the shared in-memory Font across calls
(it rescaled unitsPerEm when invoked twice for two formats). Overlap removal is
delegated to skia-pathops, so recipes may overlap freely and be merged at compile.
"""

from __future__ import annotations

from pathlib import Path

import ufoLib2
from ufo2ft import compileOTF, compileTTF


def compile_font(
    font: ufoLib2.Font,
    out_dir: Path,
    *,
    stem: str,
    formats: tuple[str, ...] = ("otf", "ttf"),
) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for fmt in formats:
        if fmt == "otf":
            tt = compileOTF(font, removeOverlaps=True, overlapsBackend="pathops")
        elif fmt == "ttf":
            tt = compileTTF(font, removeOverlaps=True, overlapsBackend="pathops")
        else:  # pragma: no cover - defensive
            raise ValueError(f"unsupported format {fmt!r}")
        target = out_dir / f"{stem}.{fmt}"
        tt.save(target)
        written.append(target)
    return written
