from sage_map_builder.map.reader import MapReader
from sage_map_builder.model.from_reader import document_from_reader


def test_reader_result_becomes_document_without_semantic_guesses():
    data = b"EAR\0" + b"x" * 12 + b"CkMp" + b"data"
    result = MapReader().read_bytes(data, "sample.map")
    doc = document_from_reader(result)
    assert doc.file_name == "sample.map"
    assert doc.raw_size == len(data)
    assert doc.dimensions.width is None
    assert len(doc.regions) == len(result.regions)
    assert len(doc.opaque_sections) == len(result.regions)
