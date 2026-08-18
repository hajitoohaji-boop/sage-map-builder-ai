"""Structural validation for the verified WaypointsList v1 payload."""
from __future__ import annotations
import struct
from .waypoints_chunk import WAYPOINTS_VERSION

HEADER_SIZE = 4
LINK_SIZE = 8


def validate_waypoints_payload(payload: bytes) -> tuple[int, ...]:
    if len(payload) < HEADER_SIZE:
        raise ValueError("truncated WaypointsList payload")
    count = struct.unpack_from("<i", payload, 0)[0]
    if count < 0:
        raise ValueError("negative waypoint link count")
    expected = HEADER_SIZE + count * LINK_SIZE
    if len(payload) != expected:
        raise ValueError("WaypointsList payload length does not match link count")
    return tuple(range(count))
