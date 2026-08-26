import pytest

from sage_map_builder.formats.roundtrip_contract import require_roundtrip


def test_identical_bytes_pass():
    require_roundtrip(b"abc", b"abc")


def test_changed_bytes_fail():
    with pytest.raises(ValueError):
        require_roundtrip(b"abc", b"abd")
