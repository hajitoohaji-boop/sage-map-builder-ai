from sage_map_builder.formats.worldbuilder_source import verified_source_facts


def test_worldbuilder_source_facts():
    facts = verified_source_facts()
    assert facts["data_chunk"]["header_bytes"] == 4
    assert facts["data_chunk"]["version_type"] == "uint16"
    assert facts["worldbuilder_save"]["waypoint_chunk_label"] == "WaypointsList"
    assert facts["worldbuilder_save"]["waypoint_chunk_version"] == 1
    assert facts["worldbuilder_save"]["waypoint_link_record_ints"] == 2
