"""Evidence-only probe for the observed ``CkMp`` marker.

The real sample maps begin with an ``EAR\\0`` prefix and contain ``CkMp`` near
 the header. This module records the bytes immediately following the marker as
an observed little-endian u32 value. It deliberately does NOT call that value a
chunk size, TOC count, offset, or version until the source/binary investigation
proves its meaning.
"""
from __future__ import annotations

from dataclasses import dataclass
import struct

CKMP_MARKER = b"CkMp"


@dataclass(frozen=True)
class CkMpEvidence:
    marker_offset: int
    following_u32: int | None
    following_bytes: bytes

    @property
    def has_u32(self) -> bool:
        return len(self.following_bytes) >= 4


def find_ckmp_evidence(data: bytes) -> tuple[CkMpEvidence, ...]:
    """Return every CkMp occurrence without assigning semantic meaning."""
    result: list[CkMpEvidence] = []
    cursor = 0
    while True:
        offset = data.find(CKMP_MARKER, cursor)
        if offset < 0:
            break
        following = data[offset + 4 : offset + 8]
        value = struct.unpack("<I", following)[0] if len(following) == 4 else None
        result.append(CkMpEvidence(offset, value, following))
        cursor = offset + 1
    return tuple(result)


def first_ckmp_evidence(data: bytes) -> CkMpEvidence | None:
    """Return the first observed CkMp marker, if any."""
    items = find_ckmp_evidence(data)
    return items[0] if items else None
