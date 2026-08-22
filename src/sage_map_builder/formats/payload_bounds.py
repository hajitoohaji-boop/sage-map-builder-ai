"""Bounds helpers used by binary MAP codecs."""
from __future__ import annotations


def require_range(payload: bytes, start: int, size: int) -> bytes:
    if start < 0 or size < 0 or start + size > len(payload):
        raise ValueError("payload range is outside chunk bounds")
    return payload[start:start + size]


def require_consumed(payload: bytes, cursor: int) -> None:
    if cursor != len(payload):
        raise ValueError(
            f"codec did not consume complete payload: cursor={cursor} size={len(payload)}"
        )
