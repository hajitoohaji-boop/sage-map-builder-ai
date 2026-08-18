"""Deterministic report for the audited source chunk catalogue."""
from __future__ import annotations
from .source_chunk_catalog import nested_source_chunks, top_level_source_chunks


def build_source_chunk_report() -> dict[str, object]:
    return {
        "top_level": [
            {"label": s.label, "version": s.version, "order": s.container_order}
            for s in top_level_source_chunks()
        ],
        "nested": [
            {"label": s.label, "version": s.version, "order": s.container_order, "parent": s.parent}
            for s in nested_source_chunks()
        ],
    }
