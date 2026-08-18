"""Stable JSON-safe summaries for chunk batches and decode results."""
from __future__ import annotations
from .chunk_batch import IdentifiedChunk
from .codec_result import DecodedChunk, OpaqueChunk


def summarize_chunks(chunks: tuple[IdentifiedChunk, ...]) -> list[dict[str, object]]:
    return [{"label": c.label, "version": c.version, "payload_size": len(c.payload)} for c in chunks]


def summarize_decoded(chunks: tuple[DecodedChunk | OpaqueChunk, ...]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for chunk in chunks:
        if isinstance(chunk, DecodedChunk):
            result.append({"label": chunk.label, "version": chunk.version, "kind": "decoded"})
        else:
            result.append({"label": chunk.label, "version": chunk.version, "kind": "opaque", "payload_size": len(chunk.payload)})
    return result
