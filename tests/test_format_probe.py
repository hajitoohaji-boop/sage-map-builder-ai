import struct

import pytest

from sage_map_builder.map.format_probe import probe


def test_probe_records_only_observable_prefix_values() -> None:
    data = b"CkMp" + struct.pack("<I", 512) + b"\x00" * 8
    result = probe(data, prefix_size=16)
    assert result.size == len(data)
    assert result.signature == b"CkMp"
    assert result.little_endian_u32[0].offset == 0
    assert result.little_endian_u32[0].value == 0x706D6B43
    assert result.little_endian_u32[1].value == 512


def test_probe_rejects_too_small_prefix() -> None:
    with pytest.raises(ValueError):
        probe(b"abc", prefix_size=3)
