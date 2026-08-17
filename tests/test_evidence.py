import pytest
from sage_map_builder.map.evidence import make_evidence


def test_evidence_is_reproducible():
    ev = make_evidence(b"abcdef", "sample", 1, 3)
    assert ev.offset == 1
    assert ev.length == 3
    assert ev.preview_hex == "62 63 64"
    assert len(ev.sha256) == 64


def test_invalid_evidence_range_is_rejected():
    with pytest.raises(ValueError):
        make_evidence(b"abc", "bad", 2, 2)
