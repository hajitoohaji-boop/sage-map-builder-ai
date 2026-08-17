"""Unified evidence pipeline for real .map samples.

This layer composes existing deterministic scanners. It does not infer
semantic field meanings.
"""
from __future__ import annotations
from pathlib import Path
import json

from ..report.sample_report import build_sample_report
from ..report.compare_report import build_compare_report


def analyze_samples(paths: list[str | Path]) -> dict:
    resolved = [Path(p) for p in paths]
    samples = [build_sample_report(p) for p in resolved]
    result = {"schema_version": 1, "samples": samples, "comparison": None}
    if len(resolved) == 2:
        result["comparison"] = build_compare_report(resolved[0], resolved[1])
    return result


def write_evidence_pipeline(paths: list[str | Path], output: str | Path) -> dict:
    result = analyze_samples(paths)
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result
