"""End-to-end deterministic pipeline for one binary map."""

from __future__ import annotations

from pathlib import Path

from ..map.reader import MapReader
from ..report.section_report import build_section_report


def analyze_map(path: str | Path) -> dict:
    """Read a map and return its deterministic section report."""
    result = MapReader().read_file(path)
    return build_section_report(result)


def analyze_bytes(data: bytes, file_name: str = "<memory>") -> dict:
    result = MapReader().read_bytes(data, file_name)
    return build_section_report(result)
