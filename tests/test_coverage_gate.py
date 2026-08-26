import pytest

from sage_map_builder.formats.coverage_gate import completion_gaps, require_complete


def test_completion_gate_is_fail_closed_until_all_components_are_verified():
    gaps = completion_gaps()
    assert "height_map" in gaps
    assert "objects" in gaps
    assert "writer" in gaps
    with pytest.raises(RuntimeError):
        require_complete()
