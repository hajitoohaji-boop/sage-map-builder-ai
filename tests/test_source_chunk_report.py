from sage_map_builder.formats.source_chunk_report import build_source_chunk_report


def test_source_chunk_report_is_deterministic():
    report = build_source_chunk_report()
    assert [x["label"] for x in report["top_level"]] == [
        "HeightMapData", "BlendTileData", "WorldInfo", "ObjectsList", "GlobalLighting", "WaypointsList"
    ]
    assert report["nested"] == [
        {"label": "Object", "version": 3, "order": 5, "parent": "ObjectsList"}
    ]
