from sage_map_builder.analysis.source_chunk_markers import find_source_chunk_markers


def test_source_chunk_markers_are_literal_evidence_only():
    data = b"xxHeightMapData\x00yyWaypointsList\x00zz"
    markers = find_source_chunk_markers(data)
    assert [(m.label, m.version, m.offset) for m in markers] == [
        ("HeightMapData", 4, 2),
        ("WaypointsList", 1, 18),
    ]


def test_unknown_labels_are_not_invented():
    assert find_source_chunk_markers(b"ScriptsList ObjectsList")[-1].label == "ObjectsList"
