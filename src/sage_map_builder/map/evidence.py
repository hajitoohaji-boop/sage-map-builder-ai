"""Evidence primitives used before assigning semantic meaning to map bytes."""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256

@dataclass(frozen=True)
class ByteEvidence:
    label: str
    offset: int
    length: int
    sha256: str
    preview_hex: str


def make_evidence(data: bytes, label: str, offset: int = 0, length: int | None = None) -> ByteEvidence:
    if offset < 0 or offset > len(data):
        raise ValueError("offset outside data")
    if length is None:
        length = len(data) - offset
    if length < 0 or offset + length > len(data):
        raise ValueError("length outside data")
    chunk = data[offset:offset + length]
    return ByteEvidence(label, offset, length, sha256(chunk).hexdigest(), chunk[:32].hex(" "))
