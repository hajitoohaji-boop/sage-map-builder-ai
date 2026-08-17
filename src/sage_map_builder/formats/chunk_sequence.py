"""Sequential parsing of verified four-byte DataChunk headers.

Chunk labels/IDs are deliberately not inferred here; EA stores the symbolic
mapping in the table of contents. This module only preserves the header and
opaque payload bytes of a contiguous chunk-data stream.
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
    out = bytearray()
    for chunk in chunks:
        payload = bytes(chunk.payload)
        if len(payload) > 0xFFFF:
            raise ValueError("DataChunk payload exceeds uint16 size")
        out.extend(DataChunkHeader(chunk.header.version, len(payload)).pack())
        out.extend(payload)
    return bytes(out)
