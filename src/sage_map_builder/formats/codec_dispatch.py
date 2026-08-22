"""Safe dispatch from chunk identity to an explicitly verified codec."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .chunk_identity_table import identity


class ChunkCodec(Protocol):
    def decode(self, payload: bytes) -> Any: ...
    def encode(self, value: Any) -> bytes: ...


@dataclass(frozen=True)
class CodecDispatch:
    codec: ChunkCodec
    label: str
    version: int


def dispatch(codec: ChunkCodec, label: str, version: int) -> CodecDispatch:
    spec = identity(label, version)
    if spec is None:
        raise ValueError(f"unknown MAP chunk identity: {label} v{version}")
    if spec.semantic_status != "verified":
        raise ValueError(f"codec is not verified: {label} v{version}")
    return CodecDispatch(codec=codec, label=label, version=version)
