"""Lossless envelope for an externally identified DataChunk.

The envelope deliberately keeps the binary header separate from payload.
Semantic labels are evidence supplied by the caller; this module never infers
identity from bytes.
"""
from __future__ import annotations
from dataclasses import dataclass
import struct

HEADER_SIZE = 4

@dataclass(frozen=True)
class ChunkEnvelope:
    version: int
    payload: bytes

    def encode(self) -> bytes:
        if not 0 <= self.version <= 0xFFFF:
            raise ValueError("version outside uint16 range")
        if len(self.payload) > 0xFFFF:
            raise ValueError("payload exceeds uint16 size")
        return struct.pack("<HH", self.version, len(self.payload)) + self.payload

    @classmethod
    def decode(cls, data: bytes, *, limit: int | None = None) -> "ChunkEnvelope":
        if len(data) < HEADER_SIZE:
            raise ValueError("truncated DataChunk header")
        version, size = struct.unpack_from("<HH", data, 0)
        end = HEADER_SIZE + size
        if limit is not None and end > limit:
            raise ValueError("DataChunk exceeds supplied limit")
        if end > len(data):
            raise ValueError("truncated DataChunk payload")
        return cls(version, bytes(data[HEADER_SIZE:end]))
