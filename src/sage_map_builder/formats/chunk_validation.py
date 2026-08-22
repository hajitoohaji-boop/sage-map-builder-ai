"""Generic structural validation for a source-backed DataChunk."""
from __future__ import annotations

from dataclasses import dataclass

from .data_chunk import DataChunkHeader
from .source_chunk_catalog import find_source_chunk_version


@dataclass(frozen=True)
class ChunkValidation:
    label: str
    version: int
    data_size: int
    payload_size: int
    source_backed: bool
    size_matches_header: bool

    @property
    def structurally_valid(self) -> bool:
        return self.source_backed and self.size_matches_header


def validate_chunk(label: str, header: DataChunkHeader, payload: bytes) -> ChunkValidation:
    spec = find_source_chunk_version(label, header.version)
    return ChunkValidation(
        label=label,
        version=header.version,
        data_size=header.data_size,
        payload_size=len(payload),
        source_backed=spec is not None,
        size_matches_header=header.data_size == len(payload),
    )
