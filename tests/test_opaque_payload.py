from sage_map_builder.formats.opaque_payload import OpaquePayload


def test_opaque_payload_is_byte_preserving():
    payload = OpaquePayload("HeightMapData", 4, b"\x00\x01\xfe\xff")
    copy = payload.clone()
    assert copy.encode() == payload.payload
    assert copy == payload
