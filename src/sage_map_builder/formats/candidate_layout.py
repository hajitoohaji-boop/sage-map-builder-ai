"""Conservative candidate byte-layout descriptions.

A layout is only descriptive until independently promoted; this module never
assigns semantic meaning to raw fields by itself.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FieldSpan:
    name: str
    offset: int
    size: int


@dataclass(frozen=True)
class CandidateLayout:
    label: str
    version: int
    fields: tuple[FieldSpan, ...]
    confidence: int = 0

    @property
    def covered_bytes(self) -> int:
        return sum(field.size for field in self.fields)

    @property
    def contiguous(self) -> bool:
        cursor = 0
        for field in self.fields:
            if field.offset != cursor:
                return False
            cursor += field.size
        return True


def layout(label: str, version: int, *fields: FieldSpan) -> CandidateLayout:
    if not label or version < 0:
        raise ValueError("invalid candidate layout identity")
    if any(field.offset < 0 or field.size <= 0 for field in fields):
        raise ValueError("field spans must have non-negative offsets and positive sizes")
    return CandidateLayout(label, version, tuple(fields))
