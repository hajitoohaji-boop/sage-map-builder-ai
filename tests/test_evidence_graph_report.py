from sage_map_builder.map.source_evidence import classify_observation
from sage_map_builder.map.evidence_graph import build_evidence_graph
from sage_map_builder.map.evidence_graph_report import summarize_graph


def test_summary_counts_evidence_states():
    graph = build_evidence_graph((
        classify_observation(0, 10, "WaypointsList", 1),
        classify_observation(10, 20, "Unknown", 1),
    ))
    assert summarize_graph(graph) == {"total": 2, "verified": 1, "unresolved": 1}
