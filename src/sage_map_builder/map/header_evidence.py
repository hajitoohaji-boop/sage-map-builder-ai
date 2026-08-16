"""Conservative extraction of only header facts that can be observed safely."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HeaderEvidence:
    magic: bytes
    ckmP_offsets: tuple[int, ...]
    file_size: int

    def validate(self) -> None:
        if self.file_size < 4:
            raise ValueError("file is too small to contain a four-byte magic")
        if not isinstance(self.magic, bytes) or len(self.magic) != 4:
            raise ValueError("magic must contain exactly four bytes")
        if any(offset < 0 or offset >= self.file_size for offset in self.ckmP_offsets):
            raise ValueError("marker offset is outside the file")


def extract_header_evidence(data: bytes) -> HeaderEvidence:
    if len(data) < 4:
        raise ValueError("map file is too small")
    offsets: list[int] = []
    cursor = 0
    while True:
        index = data.find(b"CkMp", cursor)
        if index < 0:
            break
        offsets.append(index)
        cursor = index + 1
    result = HeaderEvidence(data[:4], tuple(offsets), len(data))
    result.validate()
    return result
