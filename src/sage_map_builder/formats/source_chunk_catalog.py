"""Safe query helpers over the audited World Builder chunk catalogue."""
from __future__ import annotations
from .worldbuilder_source import SourceChunkSpec, source_chunk_specs


def find_source_chunk_version(label: str, version: int) -> SourceChunkSpec | None:
    """Return a spec only when both label and version exactly match source facts."""
    for spec in source_chunk_specs():
        if spec.label == label and spec.version == version:
            return spec
    return None


def top_level_source_chunks() -> tuple[SourceChunkSpec, ...]:
    """Return only explicitly catalogued top-level chunks."""
    return tuple(spec for spec in source_chunk_specs() if not spec.nested)


def nested_source_chunks() -> tuple[SourceChunkSpec, ...]:
    """Return only explicitly catalogued nested chunks."""
    return tuple(spec for spec in source_chunk_specs() if spec.nested)
