from sage_map_builder.map.reader import MapReader
from sage_map_builder.model.from_reader import document_from_reader
from sage_map_builder.model.serialization import document_from_dict, document_to_json


def test_document_round_trip_is_deterministic():
    data = b"EAR\0" + b"x" * 12 + b"CkMp" + b"data"
    doc = document_from_reader(MapReader().read_bytes(data, "sample.map"))
    encoded = document_to_json(doc)
    restored = document_from_dict(__import__("json").loads(encoded))
    assert restored.to_dict() == doc.to_dict()
    assert document_to_json(restored) == encoded
