from sage_map_builder.formats.chunk_validation import validate_chunk
from sage_map_builder.formats.data_chunk import DataChunkHeader


def test_source_backed_chunk_with_matching_size_is_valid():
    result = validate_chunk("WaypointsList", DataChunkHeader(1, 3), b"abc")
    assert result.structurally_valid


def test_wrong_payload_size_is_invalid():
    result = validate_chunk("WaypointsList", DataChunkHeader(1, 4), b"abc")
    assert not result.structurally_valid


def test_unknown_label_is_not_source_backed():
    result = validate_chunk("Unknown", DataChunkHeader(1, 3), b"abc")
    assert not result.structurally_valid
