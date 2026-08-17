"""Unified, evidence-only JSON reporting for SAGE map binary samples."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .pipeline import MapProbeResult, probe_bytes
from .sections import common_byte_runs, marker_ranges
from .section_confidence import score_candidate


@dataclass(frozen=True)
class SectionReport:
    file: str
    size: int
    sha256: str
    magic_hex: str
    markers: dict[str, tuple[int, ...]]
    common_sections: tuple[dict[str, int | str], ...]
    section_confidence: tuple[dict[str, object], ...]
    head_hex: str


def build_report(data: bytes, file_name: str = "<memory>", *, comparison: bytes | None = None) -> SectionReport:
    probe: MapProbeResult = probe_bytes(data, file_name)
    common = ()
    confidence = ()
    if comparison is not None:
        spans = common_byte_runs(data, comparison)
        common = tuple(asdict(span) for span in spans)
        confidence = tuple(
            asdict(score_candidate(span.start, span.end, shared_offset=True))
            for span in spans
        )
    markers = {"CkMp": marker_ranges(data, b"CkMp")}
    return SectionReport(
        file=file_name,
        size=len(data),
        sha256=hashlib.sha256(data).hexdigest(),
        magic_hex=probe.evidence.magic.hex(" "),
        markers=markers,
        common_sections=common,
        section_confidence=confidence,
        head_hex=probe.head.hex(" "),
    )


def write_report(report: SectionReport, output: str | Path) -> None:
    Path(output).write_text(
        json.dumps(asdict(report), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_pair_reports(left_path: str | Path, right_path: str | Path, output_dir: str | Path) -> tuple[Path, Path]:
    left = Path(left_path)
    right = Path(right_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    left_data = left.read_bytes()
    right_data = right.read_bytes()
    left_report = out / f"{left.stem}.section-report.json"
    right_report = out / f"{right.stem}.section-report.json"
    write_report(build_report(left_data, str(left), comparison=right_data), left_report)
    write_report(build_report(right_data, str(right), comparison=left_data), right_report)
    return left_report, right_report
