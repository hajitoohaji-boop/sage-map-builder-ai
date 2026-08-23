"""Consistency checks for paired binary evidence observations."""
from __future__ import annotations

from .evidence_pairing import PairedObservation


def same_span_shape(observation: PairedObservation) -> bool:
    left_size = observation.left.end - observation.left.start
    right_size = observation.right.end - observation.right.start
    return left_size == right_size


def same_identity(observation: PairedObservation) -> bool:
    return (
        observation.left.label == observation.right.label
        and observation.left.version == observation.right.version
    )
