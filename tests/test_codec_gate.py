import pytest

from sage_map_builder.formats.codec_gate import require_ready
from sage_map_builder.formats.codec_status import CodecReadiness, CodecStatus


def test_ready_codec_passes():
    require_ready(CodecReadiness("WaypointsList", 1, CodecStatus.VERIFIED, True, True, True))


def test_incomplete_codec_is_blocked():
    with pytest.raises(ValueError):
        require_ready(CodecReadiness("ObjectsList", 3, CodecStatus.EVIDENCE, True, True, False))
