from sage_map_builder.formats.source_chunk_catalog import (
    find_source_chunk_version,
    nested_source_chunks,
    top_level_source_chunks,
)


def test_exact_label_and_version_match_only():
    assert find_source_chunk_version("WaypointsList", 1) is not None
    assert find_source_chunk_version("WaypointsList", 2) is None
    assert find_source_chunk_version("Unknown", 1) is None


def test_top_level_and_nested_catalogue_are_separated():
    top = top_level_source_chunks()
    nested = nested_source_chunks()
    assert all(not spec.nested for spec in top)
    assert all(spec.nested for spec in nested)
    assert any(spec.label == "Object" and spec.parent == "ObjectsList" for spec in nested)
