"""Evidence scoring for binary section candidates.

Scores are descriptive only. They never assign semantic section names.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class SectionConfidence:
    start: int
    end: int
    score: float
    evidence: tuple[str, ...]


def score_candidate(start: int, end: int, *, shared_offset: bool = False, marker_nearby: bool = False, source_supported: bool = False) -> SectionConfidence:
    if start < 0 or end <= start:
        raise ValueError("invalid section range")
    score = 0.0
    evidence: list[str] = []
    if shared_offset:
        score += 0.35
        evidence.append("same range/offset observed across samples")
    if marker_nearby:
        score += 0.20
        evidence.append("known marker occurs at/near boundary")
    if source_supported:
        score += 0.45
        evidence.append("supported by World Builder source evidence")
    return SectionConfidence(start, end, min(score, 1.0), tuple(evidence))
