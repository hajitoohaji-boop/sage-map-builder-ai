"""Strict, bounds-checked binary reader used by future SAGE parsers.

This module deliberately knows nothing about the .map format. Keeping byte-level
I/O separate from format parsing makes the parser easier to test and prevents
format assumptions from leaking into the low-level reader.
"""

from __future__ import annotations

import io
import struct


class BinaryReaderError(ValueError):
    """Raised when a binary read cannot be completed safely."""


class BinaryReader:
    """Small bounds-checked reader over immutable bytes."""

    def __init__(self, data: bytes) -> None:
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes")
        self._stream = io.BytesIO(data)
        self._size = len(data)

    @property
    def position(self) -> int:
        return self._stream.tell()

    @property
    def size(self) -> int:
        return self._size

    @property
    def remaining(self) -> int:
        return self._size - self.position

    def seek(self, position: int) -> None:
        if not 0 <= position <= self._size:
            raise BinaryReaderError(f"seek outside buffer: {position}")
        self._stream.seek(position)

    def read_bytes(self, count: int) -> bytes:
        if not isinstance(count, int) or count < 0:
            raise BinaryReaderError("byte count must be a non-negative integer")
        if count > self.remaining:
            raise BinaryReaderError(
                f"unexpected end of data: requested {count} bytes, "
                f"only {self.remaining} remain"
            )
        return self._stream.read(count)

    def read_struct(self, fmt: str) -> tuple[object, ...]:
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, self.read_bytes(size))

    def read_u8(self) -> int:
        return int(self.read_struct("<B")[0])

    def read_u16(self) -> int:
        return int(self.read_struct("<H")[0])

    def read_u32(self) -> int:
        return int(self.read_struct("<I")[0])

    def read_i32(self) -> int:
        return int(self.read_struct("<i")[0])

    def read_f32(self) -> float:
        return float(self.read_struct("<f")[0])
