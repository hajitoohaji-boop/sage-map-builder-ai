"""Transactional editing session for MapDocument with byte patches."""
from __future__ import annotations
from dataclasses import dataclass
from .map_document import MapDocument
from ..map.preservation_writer import BinaryPatch, apply_patches


@dataclass
class EditSession:
    document: MapDocument
    original: bytes
    _patches: list[BinaryPatch]

    @classmethod
    def start(cls, document: MapDocument, original: bytes) -> "EditSession":
        if len(original) != document.raw_size:
            raise ValueError("original bytes do not match document raw_size")
        return cls(document, original, [])

    def patch(self, offset: int, data: bytes) -> None:
        candidate = tuple(self._patches + [BinaryPatch(offset, data)])
        apply_patches(self.original, candidate)
        self._patches.append(BinaryPatch(offset, bytes(data)))

    def preview_bytes(self) -> bytes:
        return apply_patches(self.original, tuple(self._patches))

    def commit_bytes(self) -> bytes:
        return self.preview_bytes()

    def rollback(self) -> None:
        self._patches.clear()
