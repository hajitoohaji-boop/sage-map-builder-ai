from sage_map_builder.formats.coverage_snapshot import current_snapshot


def test_snapshot_reflects_verified_components_only():
    snapshot = current_snapshot(7)
    assert "data_chunk" in snapshot.verified_components
    assert snapshot.total_catalogued_components == 7
    assert snapshot.verified_count >= 1
