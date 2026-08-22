import pytest

from sage_map_builder.formats.source_sample_gate import SampleGate, SampleRangeClaim


def test_source_backed_claim_requires_real_range():
    gate = SampleGate().add(SampleRangeClaim("MY MAP.map", "WaypointsList", 1, 100, 120))
    assert gate.for_sample("MY MAP.map")[0].start == 100


def test_unknown_chunk_is_rejected():
    with pytest.raises(ValueError):
        SampleRangeClaim("MY MAP.map", "UnknownChunk", 1, 0, 4)


def test_invalid_range_is_rejected():
    with pytest.raises(ValueError):
        SampleRangeClaim("MY MAP.map", "WaypointsList", 1, 20, 10)
