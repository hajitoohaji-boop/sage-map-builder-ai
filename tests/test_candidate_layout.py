import pytest

from sage_map_builder.formats.candidate_layout import FieldSpan, layout


def test_contiguous_candidate_layout():
    item = layout("HeightMapData", 4, FieldSpan("a", 0, 2), FieldSpan("b", 2, 4))
    assert item.contiguous
    assert item.covered_bytes == 6


def test_non_contiguous_layout_is_not_claimed_complete():
    item = layout("HeightMapData", 4, FieldSpan("a", 0, 2), FieldSpan("b", 4, 2))
    assert not item.contiguous


def test_invalid_field_span_is_rejected():
    with pytest.raises(ValueError):
        layout("HeightMapData", 4, FieldSpan("bad", 0, 0))
