"""Explicit contract for lossless chunk round-trips."""
from __future__ import annotations


def require_roundtrip(original: bytes, encoded: bytes) -> None:
    if original != encoded:
        raise ValueError(
            f"lossless round-trip failed: original={len(original)} bytes, "
            f"encoded={len(encoded)} bytes"
        )
