from sage_map_builder.formats.chunk_batch import IdentifiedChunk
from sage_map_builder.formats.chunk_batch_report import summarize_chunks


def test_summarize_chunks_is_json_safe():
    result = summarize_chunks((IdentifiedChunk("WaypointsList", 1, b"abc"),))
    assert result == [{"label": "WaypointsList", "version": 1, "payload_size": 3}]
