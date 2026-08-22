from sage_map_builder.formats.codec_status import CodecReadiness, CodecStatus


def test_verified_codec_requires_all_gates():
    item = CodecReadiness("WaypointsList", 1, CodecStatus.VERIFIED, True, True, True)
    assert item.ready


def test_evidence_codec_is_not_ready():
    item = CodecReadiness("HeightMapData", 4, CodecStatus.EVIDENCE, True, True, False)
    assert not item.ready
