"""Helpers for inspecting candidate binary fields without assigning semantics."""

from __future__ import annotations

import struct
from dataclasses import dataclass


@dataclass(frozen=True)
class FieldSample:
    offset: int
    u32: int | None
    i32: int | None
    f32: float | None


def sample_u32_i32_f32(data: bytes, offsets: range) -> tuple[FieldSample, ...]:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    result: list[FieldSample] = []
    for offset in offsets:
        if offset < 0:
            raise ValueError("offset must be non-negative")
        if offset + 4 > len(data):
            result.append(FieldSample(offset, None, None, None))
            continue
        raw = data[offset : offset + 4]
        result.append(
            FieldSample(
                offset=offset,
                u32=struct.unpack("<I", raw)[0],
                i32=struct.unpack("<i", raw)[0],
                f32=struct.unpack("<f", raw)[0],
            )
        )
    return tuple(result)
