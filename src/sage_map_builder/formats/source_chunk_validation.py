"""Validation helpers for source-backed chunk specifications.

This module compares an observed label/version pair with the explicit EA
World Builder source catalogue. It deliberately does not infer unknown chunks.
"""
from __future__ import annotations
from dataclasses import dataclass
from .worldbuilder_source import SourceChunkSpec, find_source_chunk

@dataclass(frozen=True)
class SourceChunkMatch:
    label: str
    observed_version: int
    spec: SourceChunkSpec
    verified: bool


def match_source_chunk(label: str, observed_version: int) -> SourceChunkMatch | None:
    spec = find_source_chunk(label)
    if spec is None:
        return None
    return SourceChunkMatch(label, observed_version, spec, spec.version == observed_version)


def require_source_chunk(label: str, observed_version: int) -> SourceChunkMatch:
    match = match_source_chunk(label, observed_version)
    if match is None:
        raise ValueError(f"chunk is not explicitly supported by the source catalogue: {label}")
    if not match.verified:
        raise ValueError(
            f"chunk version mismatch for {label}: observed {observed_version}, source {match.spec.version}"
        )
    return match
