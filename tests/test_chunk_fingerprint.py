import struct

from sage_map_builder.formats.chunk_fingerprint import fingerprint
from sage_map_builder.formats.chunk_stream import scan


def test_fingerprint_is_stable_for_same_payload():
    data = struct.pack("<HH", 4, 3) + b"abc"
    span = scan(data)[0]
    first = fingerprint(data, span)
    second = fingerprint(data, span)
    assert first == second
    assert len(first.sha256) == 64
