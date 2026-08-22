import pytest

from sage_map_builder.formats.binary_primitives import (
    read_i16, read_i32, read_u16, write_i16, write_i32, write_u16,
)


def test_signed_and_unsigned_round_trip():
    assert read_i32(write_i32(-123))[0] == -123
    assert read_i16(write_i16(-321))[0] == -321
    assert read_u16(write_u16(65530))[0] == 65530


def test_truncated_values_are_rejected():
    with pytest.raises(ValueError):
        read_i32(b"\x00\x00\x00")
    with pytest.raises(ValueError):
        read_u16(b"\x00")
