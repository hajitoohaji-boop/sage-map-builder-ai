import pytest
from sage_map_builder.map.patches import BytePatch, apply_patches


def test_patch_requires_original_bytes():
    with pytest.raises(ValueError):
        BytePatch(1, b"x", b"Y").apply(b"abc")


def test_patch_applies_exactly():
    assert BytePatch(1, b"b", b"XYZ").apply(b"abc") == b"aXYZc"


def test_overlapping_patches_are_rejected():
    with pytest.raises(ValueError):
        apply_patches(b"abcdef", [BytePatch(1, b"bc", b"BC"), BytePatch(2, b"cd", b"CD")])


def test_multiple_non_overlapping_patches():
    data = b"abcdef"
    result = apply_patches(data, [BytePatch(0, b"a", b"A"), BytePatch(4, b"e", b"E")])
    assert result == b"AbcdEf"
