"""Batch source-evidence classification without semantic guessing."""
from __future__ import annotations
from dataclasses import dataclass
from sage_map_builder.map.source_evidence import SourceEvidence

@dataclass(frozen=True)
class EvidenceBatch:
    items: tuple[SourceEvidence, ...]

    @property
    def verified(self) -> tuple[SourceEvidence, ...]:
        return tuple(item for item in self.items if item.source_spec is not None)

    @property
    def unresolved(self) -> tuple[SourceEvidence, ...]:
        return tuple(item for item in self.items if item.source_spec is None)

    def require_all_verified(self) -> tuple[SourceEvidence, ...]:
        if self.unresolved:
            raise ValueError("batch contains unresolved source evidence")
        return self.items
