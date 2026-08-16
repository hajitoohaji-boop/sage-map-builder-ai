import pytest
from sage_map_builder.map.preservation_writer import BinaryPatch, apply_patches


def test_no_patches_are_lossless():
    original = b"abcdef"
    assert apply_patches(original, ()) == original


def test_patch_changes_only_requested_bytes():
    assert apply_patches(b"abcdef", (BinaryPatch(2, b"XY"),)) == b"abXYef"


def test_out_of_range_patch_is_rejected():
    with pytest.raises(ValueError):
        apply_patches(b"abc", (BinaryPatch(2, b"XYZ"),))


def test_overlapping_patches_are_rejected():
    with pytest.raises(ValueError):
        apply_patches(b"abcdef", (BinaryPatch(1, b"XX"), BinaryPatch(2, b"YY")))
