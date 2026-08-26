from sage_map_builder.formats.candidate_layout import FieldSpan, layout
from sage_map_builder.formats.layout_candidate_set import LayoutCandidateSet


def test_ranked_candidates_are_deterministic():
    low = layout("HeightMapData", 4, FieldSpan("a", 0, 2))
    high = layout("HeightMapData", 4, FieldSpan("a", 0, 4), FieldSpan("b", 4, 2))
    high = type(high)(high.label, high.version, high.fields, 10)
    low = type(low)(low.label, low.version, low.fields, 1)
    result = LayoutCandidateSet("HeightMapData", 4, (low, high)).ranked()
    assert result[0] == high


def test_complete_filters_to_exact_contiguous_coverage():
    exact = layout("HeightMapData", 4, FieldSpan("a", 0, 2), FieldSpan("b", 2, 2))
    partial = layout("HeightMapData", 4, FieldSpan("a", 0, 2))
    candidates = LayoutCandidateSet("HeightMapData", 4, (partial, exact))
    assert candidates.complete(4) == (exact,)
