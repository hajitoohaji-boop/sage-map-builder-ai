import pytest

from sage_map_builder.formats.sample_comparison import compare
from sage_map_builder.formats.chunk_fingerprint import ChunkFingerprint


def test_comparison_reports_size_and_payload_identity():
    left = ChunkFingerprint(10, 4, 3, "a" * 64)
    right = ChunkFingerprint(20, 4, 3, "a" * 64)
    result = compare(left, right)
    assert result.same_payload
    assert result.same_size


def test_comparison_rejects_different_versions():
    left = ChunkFingerprint(10, 4, 3, "a" * 64)
    right = ChunkFingerprint(20, 7, 3, "a" * 64)
    with pytest.raises(ValueError):
        compare(left, right)
