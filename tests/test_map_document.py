from sage_map_builder.model.map_document import MapDocument, MapDimensions, MapRegion


def test_map_document_keeps_unknown_data_opaque():
    doc = MapDocument(
        "sample.map",
        100,
        MapDimensions(),
        [MapRegion(0, 100, "unknown")],
        opaque_sections=[MapRegion(0, 100, "unknown")],
    )
    data = doc.to_dict()
    assert data["dimensions"] == {"width": None, "height": None}
    assert data["opaque_sections"][0]["source"] == "unknown"
