"""Compare only header evidence; no semantic field guessing."""

from __future__ import annotations

from dataclasses import dataclass

from .header_evidence import HeaderEvidence, extract_header_evidence


@dataclass(frozen=True)
class HeaderComparison:
    same_magic: bool
    same_ckmp_offsets: bool
    left_magic: bytes
    right_magic: bytes
    left_ckmp_offsets: tuple[int, ...]
    right_ckmp_offsets: tuple[int, ...]
    size_difference: int


def compare_headers(left: bytes, right: bytes) -> HeaderComparison:
    a: HeaderEvidence = extract_header_evidence(left)
    b: HeaderEvidence = extract_header_evidence(right)
    return HeaderComparison(
        same_magic=a.magic == b.magic,
        same_ckmp_offsets=a.ckmP_offsets == b.ckmP_offsets,
        left_magic=a.magic,
        right_magic=b.magic,
        left_ckmp_offsets=a.ckmP_offsets,
        right_ckmp_offsets=b.ckmP_offsets,
        size_difference=b.file_size - a.file_size,
    )
