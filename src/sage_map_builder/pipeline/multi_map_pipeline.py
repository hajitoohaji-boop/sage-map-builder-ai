"""Deterministic two-map pipeline: per-map reports plus raw comparison."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..map.research_report import build_research_report
from .map_pipeline import analyze_map


def analyze_two_maps(left_path: str | Path, right_path: str | Path) -> dict[str, Any]:
    left = Path(left_path).read_bytes()
    right = Path(right_path).read_bytes()
    left_report = analyze_map(left_path)
    right_report = analyze_map(right_path)
    research = build_research_report(left, right, Path(left_path).name, Path(right_path).name)
    return {
        "schema_version": 1,
        "left_section_report": left_report,
        "right_section_report": right_report,
        "research_report": research.__dict__,
    }
