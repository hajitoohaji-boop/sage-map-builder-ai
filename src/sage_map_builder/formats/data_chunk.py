"""Source-derived DataChunk header primitives.

EA's released DataChunk.h defines the chunk header as two shorts:
version and data size. The symbolic chunk ID is supplied by the table of
contents and is not encoded in this four-byte header.
"""
from __future__ import annotations
from dataclasses import dataclass
import struct

HEADER_SIZE = 4

@dataclass(frozen=True)
class DataChunkHeader:
    version: int
    data_size: int

    def pack(self) -> bytes:
        if not 0 <= self.version <= 0xFFFF:
            raise ValueError("DataChunk version exceeds uint16")
        if not 0 <= self.data_size <= 0xFFFF:
            raise ValueError("DataChunk size exceeds uint16")
        return struct.pack("<HH", self.version, self.data_size)

    @classmethod
    def unpack(cls, data: bytes, offset: int = 0) -> "DataChunkHeader":
        if offset < 0 or offset + HEADER_SIZE > len(data):
            raise ValueError("insufficient bytes for DataChunk header")
        version, data_size = struct.unpack_from("<HH", data, offset)
        return cls(version, data_size)


def read_chunk(data: bytes, offset: int = 0) -> tuple[DataChunkHeader, bytes, int]:
    header = DataChunkHeader.unpack(data, offset)
    payload_start = offset + HEADER_SIZE
    payload_end = payload_start + header.data_size
    if payload_end > len(data):
        raise ValueError("DataChunk payload exceeds input")
    return header, data[payload_start:payload_end], payload_end
