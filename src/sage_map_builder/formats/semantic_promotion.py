"""Controlled promotion of a codec from evidence to verified."""
from __future__ import annotations

from dataclasses import replace

from .codec_status import CodecReadiness, CodecStatus


def promote(readiness: CodecReadiness) -> CodecReadiness:
    if not readiness.source_backed:
        raise ValueError("cannot promote without source evidence")
    if not readiness.sample_backed:
        raise ValueError("cannot promote without golden-sample evidence")
    if not readiness.round_trip_tested:
        raise ValueError("cannot promote without round-trip verification")
    return replace(readiness, status=CodecStatus.VERIFIED)
