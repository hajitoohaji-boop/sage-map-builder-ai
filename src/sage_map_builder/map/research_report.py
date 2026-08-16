"""Unified evidence report for two binary map samples."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .header_word_compare import compare_header_words
from .header_evidence import extract_header_evidence
from .sections import common_byte_runs


@dataclass(frozen=True)
class ResearchReport:
    left: dict[str, Any]
    right: dict[str, Any]
    header: dict[str, Any]
    common_sections: list[dict[str, int]]


def build_research_report(left: bytes, right: bytes, left_name: str, right_name: str) -> ResearchReport:
    left_header = extract_header_evidence(left)
    right_header = extract_header_evidence(right)
    sections = [asdict(span) for span in common_byte_runs(left, right, min_length=8)]
    return ResearchReport(
        left={"file": left_name, "size": len(left), "sha256": hashlib.sha256(left).hexdigest()},
        right={"file": right_name, "size": len(right), "sha256": hashlib.sha256(right).hexdigest()},
        header={
            "same_magic": left_header.magic == right_header.magic,
            "left_magic_hex": left_header.magic.hex(" "),
            "right_magic_hex": right_header.magic.hex(" "),
            "left_ckmp_offsets": list(left_header.ckmP_offsets),
            "right_ckmp_offsets": list(right_header.ckmP_offsets),
            "word_comparison": compare_header_words(left, right),
        },
        common_sections=sections,
    )


def write_research_report(report: ResearchReport, output: str | Path) -> None:
    Path(output).write_text(json.dumps(asdict(report), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
