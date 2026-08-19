from sage_map_builder.formats.source_chunk_match import match_source_chunk
from sage_map_builder.map.source_evidence import classify_observation
from sage_map_builder.map.evidence_graph import build_evidence_graph


def test_graph_separates_verified_and_unresolved():
    known = classify_observation(10, 20, "WaypointsList", 1)
    unknown = classify_observation(20, 30, "Unknown", 1)
    graph = build_evidence_graph((known, unknown))
    assert len(graph.verified()) == 1
    assert len(graph.unresolved()) == 1
