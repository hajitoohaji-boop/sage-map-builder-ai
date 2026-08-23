"""Explicit pair of golden MAP samples used for comparative evidence."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SamplePair:
    left: str
    right: str

    def __post_init__(self) -> None:
        if not self.left or not self.right:
            raise ValueError("both sample references are required")
        if self.left == self.right:
            raise ValueError("comparative sample pair must contain two distinct samples")


GOLDEN_SAMPLE_PAIR = SamplePair("MY MAP.map", "CONTRA Custom Campaign The Battle for Lake Town.map")
