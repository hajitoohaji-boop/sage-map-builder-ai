import pytest

from sage_map_builder.format import ByteRange, SectionObservation


def test_byte_range_size() -> None:
    region = ByteRange(10, 25)
    assert region.size == 15


def test_byte_range_rejects_invalid_order() -> None:
    with pytest.raises(ValueError):
        ByteRange(25, 10)


def test_unverified_observation_is_explicit() -> None:
    observation = SectionObservation(
        name="GlobalLighting",
        location=ByteRange(40, 56),
        evidence="ASCII marker observed in two supplied samples",
    )
    assert observation.verified is False
