"""Stable JSON-safe summary for a batch of identified chunks."""
from __future__ import annotations
from .chunk_batch import IdentifiedChunk


def summarize_chunks(chunks: tuple[IdentifiedChunk, ...]) -> list[dict[str, object]]:
    return [
        {
            "label": c.label,
            "version": c.version,
            "payload_size": len(c.payload),
        }
        for c in chunks
    ]
