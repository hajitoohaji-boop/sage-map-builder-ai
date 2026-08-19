"""Stable summary of map evidence verification."""
from __future__ import annotations
from .evidence_graph import EvidenceGraph


def summarize_graph(graph: EvidenceGraph) -> dict[str, int]:
    return {
        "total": len(graph.nodes),
        "verified": len(graph.verified()),
        "unresolved": len(graph.unresolved()),
    }
