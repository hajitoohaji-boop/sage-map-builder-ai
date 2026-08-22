"""Typed container for binary payloads whose semantic layout is not verified."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class OpaquePayload:
    label: str
    version: int
    payload: bytes

    def clone(self) -> "OpaquePayload":
        return OpaquePayload(self.label, self.version, bytes(self.payload))

    def encode(self) -> bytes:
        return bytes(self.payload)
