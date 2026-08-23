"""Stable export helpers for cross-sample evidence matrices."""
from __future__ import annotations

from .evidence_matrix import EvidenceCell


def to_records(cells: tuple[EvidenceCell, ...]) -> tuple[dict[str, object], ...]:
    return tuple({
        "label": cell.identity.label,
        "version": cell.identity.version,
        "nested": cell.identity.nested,
        "left_count": cell.left_count,
        "right_count": cell.right_count,
        "comparable": cell.comparable,
        "score": cell.score,
    } for cell in cells)
