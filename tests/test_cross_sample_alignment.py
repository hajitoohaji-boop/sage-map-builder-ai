from sage_map_builder.analysis.cross_sample_alignment import align_markers
from sage_map_builder.analysis.source_chunk_markers import SourceChunkMarker


def test_alignment_uses_occurrence_order_not_absolute_offset():
    left = (
        SourceChunkMarker("WorldInfo", 1, 100, 9),
        SourceChunkMarker("Object", 3, 200, 6),
        SourceChunkMarker("Object", 3, 300, 6),
    )
    right = (
        SourceChunkMarker("WorldInfo", 1, 500, 9),
        SourceChunkMarker("Object", 3, 650, 6),
        SourceChunkMarker("Object", 3, 900, 6),
    )
    result = align_markers(left, right)
    assert [(x.label, x.left_offset, x.right_offset) for x in result] == [
        ("Object", 200, 650),
        ("Object", 300, 900),
        ("WorldInfo", 100, 500),
    ]
