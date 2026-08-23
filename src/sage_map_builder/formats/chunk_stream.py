"""Sequential DataChunk stream scanner.

The scanner is deliberately label-agnostic: DataChunk's binary header contains
only version and payload size, so symbolic labels must come from an external
source/table-of-contents layer. This keeps scanning separate from semantics.
"""
from __future__ import annotations

from dataclasses import dataclass

from .data_chunk import DataChunkHeader, HEADER_SIZE


@dataclass(frozen=True)
class ChunkSpan:
    offset: int
    header: DataChunkHeader
    payload_start: int
    payload_end: int

    @property
    def total_size(self) -> int:
        return HEADER_SIZE + self.header.data_size


def scan(data: bytes, start: int = 0, end: int | None = None) -> tuple[ChunkSpan, ...]:
    if start < 0:
        raise ValueError("start cannot be negative")
    if end is None:
        end = len(data)
    if end < start or end > len(data):
        raise ValueError("invalid scan bounds")

    cursor = start
    result: list[ChunkSpan] = []
    while cursor < end:
        if cursor + HEADER_SIZE > end:
            raise ValueError("truncated DataChunk header at end of stream")
        header = DataChunkHeader.unpack(data, cursor)
        payload_start = cursor + HEADER_SIZE
        payload_end = payload_start + header.data_size
        if payload_end > end:
            raise ValueError("DataChunk payload exceeds stream bounds")
        result.append(ChunkSpan(cursor, header, payload_start, payload_end))
        cursor = payload_end
    return tuple(result)
