import pytest
from sage_map_builder.analysis.section_fingerprint import fingerprint


def test_fingerprint_is_stable():
    result = fingerprint(b"abcdef", 1, 5)
    assert result["start"] == 1
    assert result["end"] == 5
    assert result["length"] == 4
    assert result["prefix_hex"] == "62 63 64 65"
    assert result["suffix_hex"] == "62 63 64 65"


def test_fingerprint_rejects_invalid_bounds():
    with pytest.raises(ValueError):
        fingerprint(b"abc", -1, 2)
    with pytest.raises(ValueError):
        fingerprint(b"abc", 2, 1)
