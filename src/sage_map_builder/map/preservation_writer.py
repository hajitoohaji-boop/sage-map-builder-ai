"""Lossless baseline writer: copy original bytes unless an explicit patch is supplied."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class BinaryPatch:
    offset: int
    data: bytes


def apply_patches(original: bytes, patches: tuple[BinaryPatch, ...]) -> bytes:
    out = bytearray(original)
    occupied: list[tuple[int, int]] = []
    for patch in sorted(patches, key=lambda p: p.offset):
        if patch.offset < 0 or patch.offset + len(patch.data) > len(out):
            raise ValueError("patch is outside the original byte range")
        span = (patch.offset, patch.offset + len(patch.data))
        if any(span[0] < end and start < span[1] for start, end in occupied):
            raise ValueError("overlapping patches are not allowed")
        out[span[0]:span[1]] = patch.data
        occupied.append(span)
    return bytes(out)


def write_preserved(original: bytes, output: str | Path, patches: tuple[BinaryPatch, ...] = ()) -> None:
    Path(output).write_bytes(apply_patches(original, patches))
