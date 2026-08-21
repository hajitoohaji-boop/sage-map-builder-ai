from sage_map_builder.formats.evidence_manifest import EvidenceClaim, EvidenceManifest


def test_manifest_filters_by_chunk_identity():
    manifest = EvidenceManifest().add(
        EvidenceClaim("WaypointsList", 1, "WorldBuilder", "sample-a")
    ).add(
        EvidenceClaim("ObjectsList", 3, "WorldBuilder", "sample-a")
    )
    claims = manifest.for_chunk("WaypointsList", 1)
    assert len(claims) == 1
    assert claims[0].sample_reference == "sample-a"
