"""Evidence-driven dispatch between verified and opaque chunk codecs.

The caller must provide an externally established chunk label/version. This
module never derives semantic identity from payload bytes.
"""
from __future__ import annotations

from .chunk_registry import ChunkCodecRegistry
from .codec_result import DecodedChunk, OpaqueChunk
from .opaque_codec import OpaqueCodec


def decode_chunk(
    registry: ChunkCodecRegistry,
    label: str,
    version: int,
    payload: bytes,
    *,
    allow_opaque: bool = True,
) -> DecodedChunk | OpaqueChunk:
    codec = registry.get(label, version)
    if codec is not None:
        return DecodedChunk(label, version, codec.decoder(bytes(payload)))
    if not allow_opaque:
        raise KeyError(f"no verified codec: {label} v{version}")
    return OpaqueCodec(label, version).decode(payload)


def encode_chunk(registry: ChunkCodecRegistry, value: DecodedChunk | OpaqueChunk) -> bytes:
    codec = registry.get(value.label, value.version)
    if isinstance(value, OpaqueChunk):
        return OpaqueCodec(value.label, value.version).encode(value)
    if codec is None:
        raise KeyError(f"no verified codec: {value.label} v{value.version}")
    return codec.encoder(value.value)
