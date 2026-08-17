"""Explicit, bounded binary patches.

Patches are intentionally low-level. They never infer a field layout.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class BytePatch:
    offset: int
    original: bytes
    replacement: bytes

    def validate(self, data: bytes) -> None:
        if self.offset < 0 or self.offset + len(self.original) > len(data):
            raise ValueError("patch is outside source data")
        if data[self.offset:self.offset + len(self.original)] != self.original:
            raise ValueError("source bytes do not match patch precondition")

    def apply(self, data: bytes) -> bytes:
        self.validate(data)
        return data[:self.offset] + self.replacement + data[self.offset + len(self.original):]


def apply_patches(data: bytes, patches: list[BytePatch]) -> bytes:
    ordered = sorted(patches, key=lambda p: p.offset)
    previous_end = -1
    for patch in ordered:
        if patch.offset < previous_end:
            raise ValueError("overlapping patches are not allowed")
        patch.validate(data)
        previous_end = patch.offset + len(patch.original)
    result = data
    delta = 0
    for patch in ordered:
        offset = patch.offset + delta
        result = result[:offset] + patch.replacement + result[offset + len(patch.original):]
        delta += len(patch.replacement) - len(patch.original)
    return result
