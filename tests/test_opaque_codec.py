import pytest
from sage_map_builder.formats.codec_result import OpaqueChunk
from sage_map_builder.formats.opaque_codec import OpaqueCodec


def test_opaque_codec_is_lossless():
    codec = OpaqueCodec("ObjectsList", 3)
    payload = b"\x00\x01unknown-payload\xff"
    value = codec.decode(payload)
    assert value == OpaqueChunk("ObjectsList", 3, payload)
    assert codec.encode(value) == payload


def test_opaque_codec_rejects_wrong_identity():
    codec = OpaqueCodec("ObjectsList", 3)
    with pytest.raises(ValueError):
        codec.encode(OpaqueChunk("Object", 3, b"x"))
