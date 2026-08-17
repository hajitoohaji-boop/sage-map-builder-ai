"""Sequential parsing of the currently verified opaque DataChunk primitive.

This module does not claim to decode the complete World Builder file format.
It only walks concatenated chunks using the existing DataChunkHeader codec and
preserves every payload byte exactly.
"""
from __future__ import annotations
from dataclasses import dataclass

from .data_chunk import DataChunkHeader, read_chunk


@dataclass(frozen=True)
class OpaqueChunk:
    header: DataChunkHeader
    payload: bytes
    offset: int
    end: int


def read_chunk_sequence(data: bytes, *, require_exact_end: bool = True) -> tuple[OpaqueChunk, ...]:
    """Parse a contiguous sequence of verified primitive chunks.

    Unknown payloads remain opaque. Parsing stops only at the exact end of the
    input; malformed/truncated chunks raise ValueError rather than being
    silently discarded.
    """
    chunks: list[OpaqueChunk] = []
    offset = 0
    while offset < len(data):
        header, payload, end = read_chunk(data, offset)
        chunks.append(OpaqueChunk(header, payload, offset, end))
        offset = end
    if require_exact_end and offset != len(data):
        raise ValueError("chunk sequence does not consume input exactly")
    return tuple(chunks)


def write_chunk_sequence(chunks: list[OpaqueChunk] | tuple[OpaqueChunk, ...]) -> bytes:
    """Re-encode opaque chunks without changing their payload bytes."""
    out = bytearray()
    for chunk in chunks:
        payload = bytes(chunk.payload)
        if len(payload) > 0xFFFF:
            raise ValueError("DataChunk payload exceeds uint16 size")
        header = DataChunkHeader(chunk.header.chunk_id, chunk.header.version, len(payload))
        out.extend(header.pack())
        out.extend(payload)
    return bytes(out)
