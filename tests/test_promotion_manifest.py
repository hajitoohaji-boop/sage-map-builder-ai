from sage_map_builder.formats.promotion_evidence import PromotionEvidence
from sage_map_builder.formats.promotion_manifest import PromotionManifest


def test_manifest_becomes_promotable_only_when_complete():
    evidence = PromotionEvidence("source", ("a.map", "b.map"), ((10, 20),), True)
    manifest = PromotionManifest("HeightMapData", 4, evidence)
    assert manifest.score.points == 4
    assert manifest.promotable
