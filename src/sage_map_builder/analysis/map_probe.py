"""Conservative binary probe for real SAGE map samples.

The probe reports observations only. It does not claim that an observed byte
sequence is a complete SAGE structure until the format has been verified.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MapProbeResult:
    file_size: int
    prefix_hex: str
    ascii_tokens: tuple[str, ...]


def probe_map(data: bytes, *, max_prefix: int = 64) -> MapProbeResult:
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if max_prefix < 0:
        raise ValueError("max_prefix must be non-negative")

    tokens: list[str] = []
    current = bytearray()
    for byte in data:
        if 32 <= byte <= 126:
            current.append(byte)
        elif current:
            if len(current) >= 3:
                tokens.append(current.decode("ascii"))
            current.clear()
    if len(current) >= 3:
        tokens.append(current.decode("ascii"))

    return MapProbeResult(
        file_size=len(data),
        prefix_hex=data[:max_prefix].hex(" "),
        ascii_tokens=tuple(tokens),
    )
