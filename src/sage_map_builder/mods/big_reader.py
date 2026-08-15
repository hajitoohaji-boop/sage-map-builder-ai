"""Minimal safe reader for the EA BIG archive container.

This first version indexes entries only after validating archive bounds. It does
not attempt decompression or game-specific interpretation yet.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass


class BigFormatError(ValueError):
    pass


@dataclass(frozen=True)
class BigEntry:
    name: str
    offset: int
    size: int


@dataclass(frozen=True)
class BigArchive:
    entries: tuple[BigEntry, ...]


def read_big(data: bytes) -> BigArchive:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if len(data) < 8 or data[:4] != b"BIGF":
        raise BigFormatError("unsupported BIG archive signature")

    count, _archive_size = struct.unpack_from(">II", data, 4)
    cursor = 12
    entries: list[BigEntry] = []
    for _ in range(count):
        if cursor + 8 > len(data):
            raise BigFormatError("truncated BIG directory")
        offset, size = struct.unpack_from(">II", data, cursor)
        cursor += 8
        end = data.find(b"\x00", cursor)
        if end < 0:
            raise BigFormatError("unterminated BIG filename")
        name = data[cursor:end].decode("latin-1")
        cursor = end + 1
        if offset > len(data) or size > len(data) - offset:
            raise BigFormatError(f"BIG entry outside archive: {name}")
        entries.append(BigEntry(name, offset, size))
    return BigArchive(tuple(entries))
