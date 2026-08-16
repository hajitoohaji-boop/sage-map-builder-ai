"""Deterministic comparison report for two SAGE map section reports."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ComparisonReport:
    left_file: str
    right_file: str
    same_size: bool
    same_magic: bool
    left_size: int
    right_size: int
    left_sha256: str
    right_sha256: str
    common_markers: dict[str, list[int]]
    left_only_markers: dict[str, list[int]]
    right_only_markers: dict[str, list[int]]
    common_sections: list[dict[str, Any]]


def _marker_dict(report: dict[str, Any]) -> dict[str, set[int]]:
    return {name: set(values) for name, values in report.get("markers", {}).items()}


def compare_reports(left: dict[str, Any], right: dict[str, Any]) -> ComparisonReport:
    lm, rm = _marker_dict(left), _marker_dict(right)
    names = sorted(set(lm) | set(rm))
    common = {name: sorted(lm.get(name, set()) & rm.get(name, set())) for name in names}
    left_only = {name: sorted(lm.get(name, set()) - rm.get(name, set())) for name in names}
    right_only = {name: sorted(rm.get(name, set()) - lm.get(name, set())) for name in names}
    left_sections = {(int(s.get("start", -1)), int(s.get("end", -1))) for s in left.get("common_sections", [])}
    right_sections = {(int(s.get("start", -1)), int(s.get("end", -1))) for s in right.get("common_sections", [])}
    keys = sorted(left_sections | right_sections)
    sections = [{"start": a, "end": b, "present_in_left": (a, b) in left_sections, "present_in_right": (a, b) in right_sections} for a, b in keys]
    return ComparisonReport(left["file"], right["file"], left["size"] == right["size"], left["magic_hex"] == right["magic_hex"], left["size"], right["size"], left["sha256"], right["sha256"], common, left_only, right_only, sections)


def compare_report_files(left_path: str | Path, right_path: str | Path, output: str | Path) -> None:
    left = json.loads(Path(left_path).read_text(encoding="utf-8"))
    right = json.loads(Path(right_path).read_text(encoding="utf-8"))
    Path(output).write_text(json.dumps(asdict(compare_reports(left, right)), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
