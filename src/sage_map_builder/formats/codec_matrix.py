"""Central readiness matrix for source-backed MAP chunks.

This is deliberately descriptive: a chunk is not considered decoded merely
because World Builder names it. Only an independently verified codec is ready.
"""
from __future__ import annotations
from dataclasses import dataclass

from .source_chunk_catalog import top_level_source_chunks, nested_source_chunks


@dataclass(frozen=True)
class CodecStatus:
    label: str
    version: int
    nested: bool
    status: str


def build_codec_matrix(verified_labels: tuple[str, ...] = ()) -> tuple[CodecStatus, ...]:
    verified = set(verified_labels)
    specs = (*top_level_source_chunks(), *nested_source_chunks())
    return tuple(
        CodecStatus(
            label=spec.label,
            version=spec.version,
            nested=spec.nested,
            status="verified" if spec.label in verified else "opaque",
        )
        for spec in specs
    )
