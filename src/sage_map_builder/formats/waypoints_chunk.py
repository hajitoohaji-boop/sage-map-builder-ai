"""Verified WaypointsList payload codec derived from World Builder serialization.

The EA World Builder source explicitly writes a version-1 WaypointsList as:
number of links, followed by two integer waypoint IDs per link.
"""
from __future__ import annotations
from dataclasses import dataclass
import struct

WAYPOINTS_VERSION = 1

@dataclass(frozen=True)
class WaypointLink:
    waypoint1: int
    waypoint2: int


def encode_waypoint_links(links: list[WaypointLink]) -> bytes:
    out = bytearray(struct.pack("<i", len(links)))
    for link in links:
        out.extend(struct.pack("<ii", link.waypoint1, link.waypoint2))
    return bytes(out)


def decode_waypoint_links(payload: bytes) -> list[WaypointLink]:
    if len(payload) < 4:
        raise ValueError("truncated WaypointsList payload")
    count = struct.unpack_from("<i", payload, 0)[0]
    if count < 0:
        raise ValueError("negative waypoint link count")
    expected = 4 + count * 8
    if len(payload) != expected:
        raise ValueError("WaypointsList payload length does not match link count")
    return [WaypointLink(*struct.unpack_from("<ii", payload, 4 + i * 8)) for i in range(count)]
