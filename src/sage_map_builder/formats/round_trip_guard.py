"""Guards for lossless MAP round-trip operations.

The guard does not decode unknown chunks. It verifies that a reconstructed byte
stream is identical to its source before an edit is considered safe.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib


@dataclass(frozen=True)
class RoundTripResult:
    identical: bool
    source_size: int
    rebuilt_size: int
    source_sha256: str
    rebuilt_sha256: str


def verify_round_trip(source: bytes, rebuilt: bytes) -> RoundTripResult:
    source_hash = hashlib.sha256(source).hexdigest()
    rebuilt_hash = hashlib.sha256(rebuilt).hexdigest()
    return RoundTripResult(
        identical=source == rebuilt,
        source_size=len(source),
        rebuilt_size=len(rebuilt),
        source_sha256=source_hash,
        rebuilt_sha256=rebuilt_hash,
    )


def require_lossless_round_trip(source: bytes, rebuilt: bytes) -> RoundTripResult:
    result = verify_round_trip(source, rebuilt)
    if not result.identical:
        raise ValueError(
            "lossless MAP round-trip failed: "
            f"source={result.source_sha256} rebuilt={result.rebuilt_sha256}"
        )
    return result
