"""Minimal, source-derived DataChunk reader/writer primitives.

The implementation intentionally models only the header mechanics that are
confirmed by the EA World Builder source. Chunk payload semantics remain
opaque until independently verified.
"""
from __future__ import annotations
from dataclasses import dataclass
import struct

HEADER_SIZE = 8

@dataclass(frozen=True)
class DataChunkHeader:
    chunk_id: int
    version: int
    data_size: int

    def pack(self) -> bytes:
        return struct.pack("<IHH", self.chunk_id, self.version, self.data_size)

    @classmethod
    def unpack(cls, data: bytes, offset: int = 0) -> "DataChunkHeader":
        if offset < 0 or offset + HEADER_SIZE > len(data):
            raise ValueError("insufficient bytes for DataChunk header")
        chunk_id, version, data_size = struct.unpack_from("<IHH", data, offset)
        return cls(chunk_id, version, data_size)


def read_chunk(data: bytes, offset: int = 0) -> tuple[DataChunkHeader, bytes, int]:
    header = DataChunkHeader.unpack(data, offset)
    payload_start = offset + HEADER_SIZE
    payload_end = payload_start + header.data_size
    if payload_end > len(data):
        raise ValueError("DataChunk payload exceeds input")
    return header, data[payload_start:payload_end], payload_end
