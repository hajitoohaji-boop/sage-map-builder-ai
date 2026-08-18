"""Explicit chunk identity supplied by verified evidence."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class ChunkIdentity:
    label: str
    version: int

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("chunk label must not be empty")
        if not 0 <= self.version <= 0xFFFF:
            raise ValueError("chunk version must fit uint16")
