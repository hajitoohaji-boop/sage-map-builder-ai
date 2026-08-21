import pytest

from sage_map_builder.formats.round_trip_guard import require_lossless_round_trip, verify_round_trip


def test_identical_round_trip_is_accepted():
    result = verify_round_trip(b"EAR\x00payload", b"EAR\x00payload")
    assert result.identical
    assert result.source_size == result.rebuilt_size
    assert result.source_sha256 == result.rebuilt_sha256


def test_changed_round_trip_is_rejected():
    with pytest.raises(ValueError):
        require_lossless_round_trip(b"original", b"changed")
