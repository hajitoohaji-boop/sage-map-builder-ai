"""Lossless codec for source-identified chunks whose payload is not decoded yet."""
from __future__ import annotations

from .codec_result import OpaqueChunk


class OpaqueCodec:
    def __init__(self, label: str, version: int) -> None:
        if not label:
            raise ValueError("chunk label must not be empty")
        if version < 0 or version > 0xFFFF:
            raise ValueError("chunk version must fit uint16")
        self.label = label
        self.version = version

    def decode(self, payload: bytes) -> OpaqueChunk:
        return OpaqueChunk(self.label, self.version, bytes(payload))

    def encode(self, value: OpaqueChunk) -> bytes:
        if value.label != self.label or value.version != self.version:
            raise ValueError("opaque chunk identity does not match codec")
        return bytes(value.payload)
