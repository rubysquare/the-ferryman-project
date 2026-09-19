#!/usr/bin/env python3
"""
The Ferryman Project — Setup script for backwards-compatible builds.
Primary configuration is maintained in pyproject.toml (PEP 517/518/621).
"""

from setuptools import setup, find_packages

setup(
    name="ferryman",
    version="0.2.0",
    description="An open-source, anti-engagement lifeline for grounded consciousness.",
    packages=find_packages(include=["ferryman*"], exclude=["tests*", "connectors*"]),
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ferryman = ferryman.cli:main",
        ],
    },
)
