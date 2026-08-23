import pytest

from sage_map_builder.formats.codec_status import CodecReadiness, CodecStatus
from sage_map_builder.formats.semantic_promotion import promote


def test_complete_codec_is_promoted():
    readiness = CodecReadiness("WaypointsList", 1, CodecStatus.EVIDENCE, True, True, True)
    result = promote(readiness)
    assert result.status is CodecStatus.VERIFIED
    assert result.ready


@pytest.mark.parametrize("field", ["source_backed", "sample_backed", "round_trip_tested"])
def test_incomplete_codec_cannot_be_promoted(field):
    values = {"source_backed": True, "sample_backed": True, "round_trip_tested": True}
    values[field] = False
    readiness = CodecReadiness("HeightMapData", 4, CodecStatus.EVIDENCE, **values)
    with pytest.raises(ValueError):
        promote(readiness)
