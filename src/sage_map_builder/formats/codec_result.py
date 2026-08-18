"""Structured result types for verified and opaque chunk decoding."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class DecodedChunk:
    label: str
    version: int
    value: object


@dataclass(frozen=True)
class OpaqueChunk:
    """A chunk whose payload semantics are intentionally not known yet."""
    label: str
    version: int
    payload: bytes


@dataclass(frozen=True)
class ChunkDecodeError:
    label: str
    version: int
    message: str
