#!/usr/bin/env python3
"""Render a deterministic Nemo Action Bar social-preview variant."""

from __future__ import annotations

import argparse
import html
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

WIDTH = 1280
HEIGHT = 640


def parse_args(variants: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=variants, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def rsvg_convert() -> str:
    executable = shutil.which("rsvg-convert")
    if not executable:
        raise SystemExit("librsvg2-bin is required (rsvg-convert).")
    return executable


def main() -> int:
    source_dir = Path(__file__).resolve().parent
    repo_dir = source_dir.parents[1]
    variants = json.loads((source_dir / "variants.json").read_text(encoding="utf-8"))
    args = parse_args(sorted(variants))
    variant = variants[args.variant]

    background = source_dir / "background.png"
    icon = repo_dir / "icons/nemo-action-bar-duplicate-symbolic.svg"
    if not background.is_file() or not icon.is_file():
        raise SystemExit("Social-preview background or Nemo Action Bar icon is missing.")

    replacements = {
        "{{TAGLINE}}": html.escape(str(variant["tagline"])),
        "{{DETAIL}}": html.escape(str(variant["detail"])),
    }
    overlay_text = (source_dir / "overlay.svg").read_text(encoding="utf-8")
    for marker, value in replacements.items():
        overlay_text = overlay_text.replace(marker, value)

    svg_renderer = rsvg_convert()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="nemo-action-bar-social-preview-") as temporary:
        work_dir = Path(temporary)
        overlay_svg = work_dir / "overlay.svg"
        shutil.copy2(background, work_dir / "background.png")
        shutil.copy2(icon, work_dir / "icon.svg")
        overlay_svg.write_text(overlay_text, encoding="utf-8")

        subprocess.run(
            [
                svg_renderer,
                "--width",
                str(WIDTH),
                "--height",
                str(HEIGHT),
                "--output",
                str(output),
                str(overlay_svg),
            ],
            check=True,
        )

    print(f"Rendered {args.variant}: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
