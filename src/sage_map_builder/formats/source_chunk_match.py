"""Evidence-only matching between observed labels and source-backed chunks."""
from __future__ import annotations
from dataclasses import dataclass
from .source_chunk_catalog import find_source_chunk_version

@dataclass(frozen=True)
class SourceChunkMatch:
    label: str
    version: int
    source_verified: bool
    nested: bool = False
    parent: str | None = None


def match_source_chunk(label: str, version: int) -> SourceChunkMatch | None:
    spec = find_source_chunk_version(label, version)
    if spec is None:
        return None
    return SourceChunkMatch(label, version, True, spec.nested, spec.parent)
