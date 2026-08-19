"""Deterministic evidence graph for observed map chunks."""
from __future__ import annotations
from dataclasses import dataclass
from .source_evidence import ObservedChunkEvidence

@dataclass(frozen=True)
class EvidenceNode:
    evidence: ObservedChunkEvidence
    verified: bool

@dataclass(frozen=True)
class EvidenceGraph:
    nodes: tuple[EvidenceNode, ...]

    def verified(self) -> tuple[EvidenceNode, ...]:
        return tuple(n for n in self.nodes if n.verified)

    def unresolved(self) -> tuple[EvidenceNode, ...]:
        return tuple(n for n in self.nodes if not n.verified)


def build_evidence_graph(observations: tuple[ObservedChunkEvidence, ...]) -> EvidenceGraph:
    return EvidenceGraph(tuple(EvidenceNode(item, item.source is not None) for item in observations))
