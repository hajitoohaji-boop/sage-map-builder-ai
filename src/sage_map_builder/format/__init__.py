"""Map-format domain primitives."""

from .map_header import MapHeaderObservation, inspect_prefix
from .marker_index import MarkerIndex, MarkerLocation, build_marker_index
from .section import ByteRange, SectionObservation

__all__ = [
    "ByteRange",
    "MapHeaderObservation",
    "MarkerIndex",
    "MarkerLocation",
    "SectionObservation",
    "build_marker_index",
    "inspect_prefix",
]
