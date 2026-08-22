"""Small explicit little-endian binary primitives used by verified codecs."""
from __future__ import annotations
import struct


def read_i32(data: bytes, offset: int = 0) -> tuple[int, int]:
    if offset < 0 or offset + 4 > len(data):
        raise ValueError("truncated i32")
    return struct.unpack_from("<i", data, offset)[0], offset + 4


def read_u16(data: bytes, offset: int = 0) -> tuple[int, int]:
    if offset < 0 or offset + 2 > len(data):
        raise ValueError("truncated u16")
    return struct.unpack_from("<H", data, offset)[0], offset + 2


def read_i16(data: bytes, offset: int = 0) -> tuple[int, int]:
    if offset < 0 or offset + 2 > len(data):
        raise ValueError("truncated i16")
    return struct.unpack_from("<h", data, offset)[0], offset + 2


def write_i32(value: int) -> bytes:
    return struct.pack("<i", value)


def write_u16(value: int) -> bytes:
    return struct.pack("<H", value)


def write_i16(value: int) -> bytes:
    return struct.pack("<h", value)
