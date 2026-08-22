"""Codec-level round-trip verification."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Protocol


class Codec(Protocol):
    def decode(self, payload: bytes) -> Any: ...
    def encode(self, value: Any) -> bytes: ...


@dataclass(frozen=True)
class CodecRoundTrip:
    identical: bool
    original_sha256: str
    encoded_sha256: str
    original_size: int
    encoded_size: int


def check(codec: Codec, payload: bytes) -> CodecRoundTrip:
    value = codec.decode(payload)
    encoded = codec.encode(value)
    return CodecRoundTrip(
        identical=payload == encoded,
        original_sha256=hashlib.sha256(payload).hexdigest(),
        encoded_sha256=hashlib.sha256(encoded).hexdigest(),
        original_size=len(payload),
        encoded_size=len(encoded),
    )
