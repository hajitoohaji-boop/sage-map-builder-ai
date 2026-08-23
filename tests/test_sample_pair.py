import pytest

from sage_map_builder.formats.sample_pair import GOLDEN_SAMPLE_PAIR, SamplePair


def test_golden_pair_contains_the_two_real_samples():
    assert GOLDEN_SAMPLE_PAIR.left == "MY MAP.map"
    assert GOLDEN_SAMPLE_PAIR.right == "CONTRA Custom Campaign The Battle for Lake Town.map"


def test_pair_rejects_same_sample():
    with pytest.raises(ValueError):
        SamplePair("same.map", "same.map")
