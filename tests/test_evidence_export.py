from sage_map_builder.formats.chunk_identity_table import identity
from sage_map_builder.formats.evidence_export import to_records
from sage_map_builder.formats.evidence_matrix import EvidenceCell


def test_export_contains_machine_readable_identity_and_score():
    cell = EvidenceCell(identity("HeightMapData", 4), 2, 1, 2, 1)
    record = to_records((cell,))[0]
    assert record["label"] == "HeightMapData"
    assert record["version"] == 4
    assert record["score"] == 3
    assert record["comparable"] is True
