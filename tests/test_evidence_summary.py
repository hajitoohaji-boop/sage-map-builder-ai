from sage_map_builder.map.evidence_summary import summarize_evidence
from sage_map_builder.map.source_evidence_batch import EvidenceBatch


def test_evidence_summary_counts_items():
    class Item:
        def __init__(self, source_spec):
            self.source_spec = source_spec
    batch = EvidenceBatch((Item(object()), Item(None)))
    assert summarize_evidence(batch) == {"total": 2, "verified": 1, "unresolved": 1}
