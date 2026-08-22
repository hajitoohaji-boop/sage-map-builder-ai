import pytest

from sage_map_builder.formats.payload_bounds import require_consumed, require_range


def test_require_range_returns_exact_slice():
    assert require_range(b"abcdef", 2, 3) == b"cde"


def test_require_range_rejects_overflow():
    with pytest.raises(ValueError):
        require_range(b"abc", 2, 2)


def test_require_consumed_rejects_trailing_bytes():
    with pytest.raises(ValueError):
        require_consumed(b"abc", 2)
