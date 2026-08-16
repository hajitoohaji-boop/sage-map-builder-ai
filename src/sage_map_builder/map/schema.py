"""Evidence-first schema for the SAGE map binary format.

This module deliberately models only facts that have been observed. Unknown
bytes remain opaque instead of being assigned speculative meanings.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BinarySpan:
    offset: int
    size: int

    @property
    def end(self) -> int:
        return self.offset + self.size


@dataclass(frozen=True)
class MapEvidence:
    file_size: int
    magic: bytes
    ckmP_offsets: tuple[int, ...]
    spans: tuple[BinarySpan, ...] = ()

    def validate(self) -> None:
        if self.file_size < 0:
            raise ValueError("file_size cannot be negative")
        for span in self.spans:
            if span.offset < 0 or span.size < 0 or span.end > self.file_size:
                raise ValueError("binary span is outside file bounds")


@dataclass(frozen=True)
class OpaqueSection:
    span: BinarySpan
    data: bytes

    def validate(self, file_size: int) -> None:
        if self.span.end > file_size:
            raise ValueError("section exceeds file size")
        if len(self.data) != self.span.size:
            raise ValueError("section size does not match data length")
