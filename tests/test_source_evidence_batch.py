import pytest
from sage_map_builder.map.source_evidence_batch import EvidenceBatch


def test_empty_batch_is_fully_verified():
    batch = EvidenceBatch(())
    assert batch.verified == ()
    assert batch.unresolved == ()
    assert batch.require_all_verified() == ()


def test_unresolved_batch_is_not_verified():
    # SourceEvidence construction is intentionally exercised through its own tests;
    # this test only verifies batch behavior for objects exposing source_spec.
    class Item:
        def __init__(self, source_spec):
            self.source_spec = source_spec
    batch = EvidenceBatch((Item(None),))
    assert len(batch.unresolved) == 1
    with pytest.raises(ValueError):
        batch.require_all_verified()
