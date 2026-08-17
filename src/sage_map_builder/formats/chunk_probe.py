"""Evidence-only probing of DataChunk headers inside known byte regions."""
from __future__ import annotations
from dataclasses import dataclass

from .data_chunk import DataChunkHeader, HEADER_SIZE


@dataclass(frozen=True)
class ChunkProbe:
    offset: int
    end: int
    version: int
    data_size: int
    payload_end: int
    valid: bool


def probe_region(data: bytes, start: int, end: int) -> ChunkProbe:
    if start < 0 or end <= start or end > len(data):
        raise ValueError("invalid probe region")
    if end - start < HEADER_SIZE:
        return ChunkProbe(start, end, 0, 0, start, False)
    header = DataChunkHeader.unpack(data, start)
    payload_end = start + HEADER_SIZE + header.data_size
    return ChunkProbe(start, end, header.version, header.data_size, payload_end, payload_end <= end)


def probe_regions(data: bytes, regions: list[tuple[int, int]]) -> tuple[ChunkProbe, ...]:
    return tuple(probe_region(data, start, end) for start, end in regions)
