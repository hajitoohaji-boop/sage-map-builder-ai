"""Bridge observed chunk labels to source evidence without binary guessing."""
from __future__ import annotations
from dataclasses import dataclass
from sage_map_builder.formats.source_chunk_match import SourceChunkMatch, match_source_chunk

@dataclass(frozen=True)
class ObservedChunkEvidence:
    offset: int
    end: int
    label: str
    version: int
    source: SourceChunkMatch | None


def classify_observation(offset: int, end: int, label: str, version: int) -> ObservedChunkEvidence:
    if offset < 0 or end < offset:
        raise ValueError("invalid observed chunk bounds")
    return ObservedChunkEvidence(offset, end, label, version, match_source_chunk(label, version))
