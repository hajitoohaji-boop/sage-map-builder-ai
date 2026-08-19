from sage_map_builder.formats.source_chunk_match import match_source_chunk


def test_exact_source_match():
    match = match_source_chunk("WaypointsList", 1)
    assert match is not None
    assert match.source_verified is True
    assert match.nested is False


def test_nested_source_match():
    match = match_source_chunk("Object", 3)
    assert match is not None
    assert match.nested is True
    assert match.parent == "ObjectsList"


def test_unknown_version_is_not_matched():
    assert match_source_chunk("WaypointsList", 99) is None
