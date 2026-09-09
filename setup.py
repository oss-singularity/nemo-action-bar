#!/usr/bin/env python3
"""Build metadata for the Nemo Action Bar Debian package."""

from pathlib import Path

from setuptools import setup


ROOT = Path(__file__).resolve().parent

setup(
    name="nemo-action-bar",
    version="2.0.0",
    description="A configurable GTK action bar for the Nemo file manager",
    long_description=(ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Claudiu Schuster",
    author_email="info@claudiuschuster.de",
    url="https://github.com/oss-singularity/nemo-action-bar",
    license="GPL-2.0-or-later",
    packages=[],
    data_files=[
        ("/usr/share/nemo-python/extensions", ["nemo_action_bar.py"]),
        ("/usr/share/nemo-action-bar", ["buttons.json"]),
        (
            "/usr/share/nemo-action-bar/icons",
            ["icons/nemo-action-bar-duplicate-symbolic.svg"],
        ),
    ],
)
