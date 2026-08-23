import pytest

from sage_map_builder.formats.promotion_evidence import PromotionEvidence


def test_complete_evidence_is_sufficient():
    evidence = PromotionEvidence("worldbuilder_source.py", ("MY MAP.map", "CONTRA Custom Campaign The Battle for Lake Town.map"), ((10, 20),), True)
    assert evidence.sufficient
    evidence.require()


def test_incomplete_evidence_is_rejected():
    evidence = PromotionEvidence("worldbuilder_source.py", ("MY MAP.map",), (), True)
    assert not evidence.sufficient
    with pytest.raises(ValueError):
        evidence.require()
