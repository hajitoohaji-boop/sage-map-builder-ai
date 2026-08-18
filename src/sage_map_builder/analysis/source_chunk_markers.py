"""Find literal source-backed WorldBuilder chunk labels in map bytes.

This is evidence collection only. A label occurrence is reported as a binary
observation; it is never promoted to a decoded chunk or TOC entry here.
"""
from __future__ import annotations
from dataclasses import dataclass

from sage_map_builder.formats.worldbuilder_source import SourceChunkSpec, source_chunk_specs


@dataclass(frozen=True)
class SourceChunkMarker:
    label: str
    version: int
    offset: int
    length: int


def find_source_chunk_markers(
    data: bytes,
    specs: tuple[SourceChunkSpec, ...] | None = None,
) -> tuple[SourceChunkMarker, ...]:
    """Return exact ASCII label occurrences, preserving every occurrence."""
    selected = specs if specs is not None else source_chunk_specs()
    found: list[SourceChunkMarker] = []
    for spec in selected:
        needle = spec.label.encode("ascii")
        start = 0
        while True:
            offset = data.find(needle, start)
            if offset < 0:
                break
            found.append(SourceChunkMarker(spec.label, spec.version, offset, len(needle)))
            start = offset + 1
    return tuple(sorted(found, key=lambda item: (item.offset, item.label)))
