"""Human-readable, deterministic report for codec readiness."""
from __future__ import annotations

from .codec_matrix import build_codec_matrix


def render_codec_report(verified_labels: tuple[str, ...] = ()) -> str:
    rows = ["MAP codec readiness", "===================="]
    for item in build_codec_matrix(verified_labels):
        nesting = "nested" if item.nested else "top-level"
        rows.append(f"{item.label} v{item.version} [{nesting}] : {item.status}")
    return "\n".join(rows) + "\n"
