"""Evidence-only candidate section extraction.

A candidate is a binary interval supported by observed marker boundaries. It is
not assigned a semantic SAGE meaning.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib


@dataclass(frozen=True)
class CandidateSection:
    start: int
    end: int
    length: int
    sha256: str
    start_marker: str | None
    end_marker: str | None
    confidence: str


def build_candidates(data: bytes, markers: dict[str, list[int]]) -> list[CandidateSection]:
    points: list[tuple[int, str]] = []
    for marker, offsets in markers.items():
        for offset in offsets:
            points.append((offset, marker))
    points.sort()
    candidates: list[CandidateSection] = []
    for index, (start, start_marker) in enumerate(points):
        end, end_marker = (points[index + 1] if index + 1 < len(points) else (len(data), None))
        if end <= start:
            continue
        payload = data[start:end]
        candidates.append(CandidateSection(start, end, len(payload), hashlib.sha256(payload).hexdigest(), start_marker, end_marker, "observed_boundary"))
    return candidates


def candidates_as_dict(data: bytes, markers: dict[str, list[int]]) -> list[dict]:
    return [asdict(item) for item in build_candidates(data, markers)]
