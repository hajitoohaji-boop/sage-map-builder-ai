from sage_map_builder.formats.evidence_consistency import same_identity, same_span_shape
from sage_map_builder.formats.evidence_pairing import Observation, PairedObservation


def test_identity_and_span_checks():
    item = PairedObservation(
        Observation("a.map", "HeightMapData", 4, 10, 30),
        Observation("b.map", "HeightMapData", 4, 100, 120),
    )
    assert same_identity(item)
    assert same_span_shape(item)
