"""Deterministic summary of source evidence; no semantic inference."""
from __future__ import annotations
from sage_map_builder.map.source_evidence_batch import EvidenceBatch


def summarize_evidence(batch: EvidenceBatch) -> dict[str, int]:
    return {
        "total": len(batch.items),
        "verified": len(batch.verified),
        "unresolved": len(batch.unresolved),
    }
