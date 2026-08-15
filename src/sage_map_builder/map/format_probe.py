"""Evidence-preserving probes for candidate SAGE map binaries.

This module deliberately does not label unknown bytes as fields. It records
only facts that can be established safely: signature, size, and aligned
32-bit values in a bounded prefix.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass


@dataclass(frozen=True)
class PrefixValue:
    offset: int
    value: int


@dataclass(frozen=True)
class MapFormatProbe:
    size: int
    signature: bytes
    little_endian_u32: tuple[PrefixValue, ...]
    big_endian_u32: tuple[PrefixValue, ...]


def probe(data: bytes, *, prefix_size: int = 256) -> MapFormatProbe:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if prefix_size < 4:
        raise ValueError("prefix_size must be at least 4")

    limit = min(len(data), prefix_size)
    little: list[PrefixValue] = []
    big: list[PrefixValue] = []
    for offset in range(0, limit - 3, 4):
        raw = data[offset : offset + 4]
        little.append(PrefixValue(offset, struct.unpack("<I", raw)[0]))
        big.append(PrefixValue(offset, struct.unpack(">I", raw)[0]))
    return MapFormatProbe(len(data), data[:4], tuple(little), tuple(big))
