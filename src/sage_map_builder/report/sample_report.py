"""Unified deterministic report for one real binary map sample."""
from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import hashlib
import json

from sage_map_builder.map.marker_scan import scan
from sage_map_builder.map.evidence import make_evidence
from sage_map_builder.map.section_evidence import section_evidence


def build_sample_report(path: Path) -> dict:
    data = path.read_bytes()
    marker_report = scan(data)
    sections = [asdict(s) for s in section_evidence(data)]
    return {
        "schema_version": 1,
        "sample": {"file": path.name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()},
        "header_evidence": asdict(make_evidence(data, "first_64_bytes", 0, min(64, len(data)))),
        "markers": marker_report["markers"],
        "sections": sections,
        "semantic_interpretation": None,
        "interpretation_rule": "No semantic label is assigned unless independently verified.",
    }


def write_sample_report(path: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_sample_report(path), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
