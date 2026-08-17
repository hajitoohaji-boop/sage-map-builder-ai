import pytest
from sage_map_builder.map.section_validation import SectionRange, validate_non_overlapping


def test_sections_are_sorted_and_validated():
    result = validate_non_overlapping([SectionRange(10, 20), SectionRange(0, 5)], 30)
    assert result == [SectionRange(0, 5), SectionRange(10, 20)]


def test_overlapping_sections_rejected():
    with pytest.raises(ValueError, match="overlap"):
        validate_non_overlapping([SectionRange(0, 10), SectionRange(9, 20)], 30)
