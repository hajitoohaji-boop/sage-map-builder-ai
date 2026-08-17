"""Compare candidate binary sections without assigning semantics."""
from __future__ import annotations
from dataclasses import asdict
from .candidate_sections import build_candidates


def compare_candidate_sections(left: bytes, left_markers: dict[str, list[int]], right: bytes, right_markers: dict[str, list[int]]) -> list[dict]:
    a = build_candidates(left, left_markers)
    b = build_candidates(right, right_markers)
    rows: list[dict] = []
    for index, (sa, sb) in enumerate(zip(a, b)):
        rows.append({
            "index": index,
            "left": asdict(sa),
            "right": asdict(sb),
            "same_length": sa.length == sb.length,
            "same_hash": sa.sha256 == sb.sha256,
            "same_boundary_markers": (sa.start_marker, sa.end_marker) == (sb.start_marker, sb.end_marker),
            "semantic_interpretation": None,
        })
    return rows
