from sage_map_builder.formats.codec_round_trip import check


class IdentityCodec:
    def decode(self, payload: bytes):
        return payload

    def encode(self, value):
        return value


def test_codec_round_trip_preserves_bytes():
    result = check(IdentityCodec(), b"waypoint-payload")
    assert result.identical
    assert result.original_sha256 == result.encoded_sha256
    assert result.original_size == result.encoded_size
