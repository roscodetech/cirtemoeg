"""Command-line entry point: build the geometric font(s)."""

from __future__ import annotations

import argparse
from pathlib import Path

from perfect_font.compile import compile_font
from perfect_font.config import BuildConfig
from perfect_font.glyphs import ALL_GLYPHS
from perfect_font.proof import render_proof
from perfect_font.ufo_builder import build_ufo


def _build_one(cfg: BuildConfig, out_dir: Path, proof: bool) -> None:
    metrics = cfg.metrics()
    font = build_ufo(ALL_GLYPHS, metrics, mono=cfg.mono, family_name=cfg.family_name)
    paths = compile_font(font, out_dir, stem=cfg.stem, formats=cfg.formats)
    print(f"  {cfg.stem}: " + ", ".join(p.name for p in paths))
    if proof:
        ttf = next((p for p in paths if p.suffix == ".ttf"), paths[0])
        png = render_proof(ttf, out_dir / f"{cfg.stem}-proof.png", metrics)
        print(f"    proof -> {png.name}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build the parametric geometric font.")
    p.add_argument("--all", action="store_true", help="build all variants (sans+mono)")
    p.add_argument("--mono", action="store_true", help="monospace spacing")
    p.add_argument("--optical", action="store_true", help="enable optical overshoot")
    p.add_argument("--cap", type=int, default=None, help="cap height override")
    p.add_argument("--stroke", type=int, default=None, help="stroke weight override")
    p.add_argument("--overshoot", type=int, default=None, help="overshoot units (with --optical)")
    p.add_argument("--proof", action="store_true", help="also render a proof PNG")
    p.add_argument("--out", type=Path, default=Path("dist"), help="output directory")
    args = p.parse_args(argv)

    base = dict(
        optical=args.optical,
        cap_height=args.cap,
        stroke=args.stroke,
        overshoot=args.overshoot,
    )
    if args.all:
        configs = [BuildConfig(mono=False, **base), BuildConfig(mono=True, **base)]
    else:
        configs = [BuildConfig(mono=args.mono, **base)]

    args.out.mkdir(parents=True, exist_ok=True)
    print(f"Building into {args.out}/")
    for cfg in configs:
        _build_one(cfg, args.out, args.proof)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
