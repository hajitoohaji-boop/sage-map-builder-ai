"""Stable fingerprints for observed binary sections."""
from __future__ import annotations
from hashlib import sha256


def fingerprint(data: bytes, start: int, end: int) -> dict:
    if start < 0 or end < start or end > len(data):
        raise ValueError("invalid section bounds")
    payload = data[start:end]
    return {
        "start": start,
        "end": end,
        "length": len(payload),
        "sha256": sha256(payload).hexdigest(),
        "prefix_hex": payload[:16].hex(" "),
        "suffix_hex": payload[-16:].hex(" ") if payload else "",
    }
