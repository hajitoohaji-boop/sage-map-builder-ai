"""Stable fingerprints for regression samples.

A fingerprint identifies the exact input bytes used by a regression test. It is
not a semantic interpretation of the map format.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class SampleFingerprint:
    size: int
    sha256: str


def fingerprint(data: bytes) -> SampleFingerprint:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    return SampleFingerprint(
        size=len(data),
        sha256=hashlib.sha256(data).hexdigest(),
    )
