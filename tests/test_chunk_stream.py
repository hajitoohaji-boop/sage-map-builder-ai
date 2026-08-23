import struct
import pytest

from sage_map_builder.formats.chunk_stream import scan


def test_scan_reads_multiple_data_chunks():
    data = struct.pack("<HH", 4, 2) + b"ab" + struct.pack("<HH", 1, 3) + b"xyz"
    spans = scan(data)
    assert [(s.header.version, s.header.data_size) for s in spans] == [(4, 2), (1, 3)]
    assert spans[0].payload_start == 4
    assert spans[1].offset == 6


def test_scan_rejects_truncated_header():
    with pytest.raises(ValueError):
        scan(b"\x01\x00")


def test_scan_rejects_payload_outside_bounds():
    data = struct.pack("<HH", 4, 5) + b"abc"
    with pytest.raises(ValueError):
        scan(data)
