from sage_map_builder.formats.codec_result import DecodedChunk, OpaqueChunk
from sage_map_builder.formats.chunk_batch_report import summarize_decoded


def test_summarize_decoded_and_opaque():
    values = (
        DecodedChunk("WaypointsList", 1, object()),
        OpaqueChunk("WorldInfo", 1, b"abc"),
    )
    assert summarize_decoded(values) == [
        {"label": "WaypointsList", "version": 1, "kind": "decoded"},
        {"label": "WorldInfo", "version": 1, "kind": "opaque", "payload_size": 3},
    ]
