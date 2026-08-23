import pytest

from sage_map_builder.formats.stable_range import StableRange


def test_range_size_and_overlap():
    a = StableRange(10, 20)
    b = StableRange(15, 25)
    assert a.size == 10
    assert a.overlaps(b)


def test_adjacent_ranges_do_not_overlap():
    assert not StableRange(0, 10).overlaps(StableRange(10, 20))


def test_invalid_range_is_rejected():
    with pytest.raises(ValueError):
        StableRange(20, 10)
