from sage_map_builder.formats.evidence_matrix import EvidenceCell
from sage_map_builder.formats.evidence_report import render_matrix
from sage_map_builder.formats.chunk_identity_table import identity


def test_report_contains_all_cell_fields():
    cell = EvidenceCell(identity('HeightMapData', 4), 1, 1, 2, 2)
    report = render_matrix((cell,))
    assert 'HeightMapData v4' in report
    assert '1 | 1 | True | 4' in report
