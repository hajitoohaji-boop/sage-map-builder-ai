"""Registry of verified binary chunk codecs.

Only codecs backed by explicit source facts are registered here. Unknown
chunks remain opaque and are never guessed into a codec.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

from .source_chunk_validation import require_source_chunk

@dataclass(frozen=True)
class ChunkCodec:
    label: str
    version: int
    decoder: Callable[[bytes], object]
    encoder: Callable[[object], bytes]

class ChunkCodecRegistry:
    def __init__(self) -> None:
        self._items: dict[tuple[str, int], ChunkCodec] = {}

    def register(self, codec: ChunkCodec) -> None:
        require_source_chunk(codec.label, codec.version)
        key = (codec.label, codec.version)
        if key in self._items:
            raise ValueError(f"codec already registered: {codec.label} v{codec.version}")
        self._items[key] = codec

    def get(self, label: str, version: int) -> ChunkCodec | None:
        return self._items.get((label, version))

    def require(self, label: str, version: int) -> ChunkCodec:
        codec = self.get(label, version)
        if codec is None:
            raise KeyError(f"no verified codec: {label} v{version}")
        return codec

    def labels(self) -> tuple[str, ...]:
        return tuple(sorted(label for label, _ in self._items))
