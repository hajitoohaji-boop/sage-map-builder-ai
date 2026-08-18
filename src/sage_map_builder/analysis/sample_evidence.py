"""Unified, non-semantic evidence collection for one real map byte stream."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from .ckmp_evidence import CkMpEvidence, find_ckmp_evidence
from .source_chunk_markers import SourceChunkMarker, find_source_chunk_markers


@dataclass(frozen=True)
class SampleEvidence:
    file_name: str
    size: int
    sha256: str
    prefix_hex: str
    ckmp: tuple[CkMpEvidence, ...]
    source_chunk_markers: tuple[SourceChunkMarker, ...]


def collect_sample_evidence(data: bytes, file_name: str = "<memory>") -> SampleEvidence:
    """Collect deterministic observations without decoding semantic fields."""
    return SampleEvidence(
        file_name=file_name,
        size=len(data),
        sha256=sha256(data).hexdigest(),
        prefix_hex=data[:16].hex(" "),
        ckmp=find_ckmp_evidence(data),
        source_chunk_markers=find_source_chunk_markers(data),
    )


def sample_evidence_dict(data: bytes, file_name: str = "<memory>") -> dict:
    """Return JSON-friendly evidence for research reports."""
    report = collect_sample_evidence(data, file_name)
    return {
        "file": report.file_name,
        "size": report.size,
        "sha256": report.sha256,
        "prefix_hex": report.prefix_hex,
        "ckmp": [
            {
                "marker_offset": item.marker_offset,
                "following_u32": item.following_u32,
                "following_hex": item.following_bytes.hex(" "),
            }
            for item in report.ckmp
        ],
        "source_chunk_markers": [
            {
                "label": item.label,
                "version": item.version,
                "offset": item.offset,
                "length": item.length,
            }
            for item in report.source_chunk_markers
        ],
    }
