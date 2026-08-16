"""Deterministic discovery-to-report pipeline for map datasets."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .sample_discovery import discover_maps
from .map_pipeline import analyze_map


def analyze_directory(root: str | Path) -> dict[str, Any]:
    """Discover valid Generals maps and analyze every valid sample."""
    samples = discover_maps(root)
    reports = []
    skipped = []
    for sample in samples:
        if not sample.valid_magic:
            skipped.append({"path": sample.path, "reason": "invalid_magic", "magic_hex": sample.magic_hex})
            continue
        reports.append(analyze_map(sample.path))
    return {
        "schema_version": 1,
        "root": str(Path(root)),
        "sample_count": len(reports),
        "reports": reports,
        "skipped": skipped,
    }
