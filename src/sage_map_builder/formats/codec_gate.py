"""Single gate used before promoting an experimental codec."""
from __future__ import annotations

from .codec_status import CodecReadiness


def require_ready(readiness: CodecReadiness) -> None:
    if not readiness.ready:
        raise ValueError(
            f"codec is not ready: {readiness.label} v{readiness.version}; "
            f"status={readiness.status.value}, source={readiness.source_backed}, "
            f"sample={readiness.sample_backed}, round_trip={readiness.round_trip_tested}"
        )
