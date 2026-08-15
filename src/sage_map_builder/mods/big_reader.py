"""Safe reader and bounded extraction for EA BIG archives."""

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
    _data: bytes = b""

    def find(self, name: str) -> BigEntry | None:
        wanted = name.replace("\\", "/").casefold()
        return next((e for e in self.entries if e.name.replace("\\", "/").casefold() == wanted), None)

    def read_entry(self, entry: BigEntry) -> bytes:
        if entry not in self.entries:
            raise KeyError(entry.name)
        return self._data[entry.offset : entry.offset + entry.size]

    def read(self, name: str) -> bytes | None:
        entry = self.find(name)
        return self.read_entry(entry) if entry else None


def read_big(data: bytes) -> BigArchive:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if len(data) < 12 or data[:4] != b"BIGF":
        raise BigFormatError("unsupported BIG archive signature")

    count, archive_size = struct.unpack_from(">II", data, 4)
    if archive_size > len(data):
        raise BigFormatError("declared archive size exceeds input")

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
    return BigArchive(tuple(entries), data)
