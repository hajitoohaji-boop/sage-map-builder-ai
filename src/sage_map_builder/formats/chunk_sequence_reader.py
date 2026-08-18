"""Read a bounded sequence of source-derived DataChunks losslessly."""
from __future__ import annotations
from dataclasses import dataclass
from .data_chunk import DataChunkHeader, HEADER_SIZE

@dataclass(frozen=True)
class RawChunk:
    offset: int
    header: DataChunkHeader
    payload: bytes
    end: int


def read_sequence(data: bytes, start: int = 0, end: int | None = None) -> tuple[RawChunk, ...]:
    limit = len(data) if end is None else end
    if start < 0 or limit < start or limit > len(data):
        raise ValueError("invalid sequence bounds")
    result: list[RawChunk] = []
    cursor = start
    while cursor < limit:
        if limit - cursor < HEADER_SIZE:
            raise ValueError("truncated DataChunk sequence header")
        header = DataChunkHeader.unpack(data, cursor)
        payload_start = cursor + HEADER_SIZE
        payload_end = payload_start + header.data_size
        if payload_end > limit:
            raise ValueError("DataChunk exceeds sequence bounds")
        result.append(RawChunk(cursor, header, bytes(data[payload_start:payload_end]), payload_end))
        cursor = payload_end
    return tuple(result)
