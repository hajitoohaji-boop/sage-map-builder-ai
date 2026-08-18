"""Batch decoding for externally identified chunks.

Semantic identity is supplied by the caller/evidence layer; this module never
infers labels from payload bytes. Verified codecs decode, while unsupported
chunks can remain lossless opaque values.
"""
from __future__ import annotations
from dataclasses import dataclass
from .chunk_dispatch import decode_chunk, encode_chunk
from .chunk_registry import ChunkCodecRegistry
from .codec_result import DecodedChunk, OpaqueChunk

@dataclass(frozen=True)
class IdentifiedChunk:
    label: str
    version: int
    payload: bytes


def decode_chunks(
    registry: ChunkCodecRegistry,
    chunks: tuple[IdentifiedChunk, ...],
    *,
    allow_opaque: bool = True,
) -> tuple[DecodedChunk | OpaqueChunk, ...]:
    return tuple(
        decode_chunk(registry, c.label, c.version, c.payload, allow_opaque=allow_opaque)
        for c in chunks
    )


def encode_chunks(
    registry: ChunkCodecRegistry,
    chunks: tuple[DecodedChunk | OpaqueChunk, ...],
) -> tuple[bytes, ...]:
    return tuple(encode_chunk(registry, c) for c in chunks)
