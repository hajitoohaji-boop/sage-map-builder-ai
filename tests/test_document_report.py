from types import SimpleNamespace
from sage_map_builder.map.document import MapDocument, MapObject, Waypoint
from sage_map_builder.map.document_report import document_summary


def test_document_summary_is_json_safe():
    asset = SimpleNamespace(name="TestTank")
    document = MapDocument(
        title="Test",
        width=64,
        height=64,
        objects=[MapObject(asset=asset, owner="Player", x=10, y=20)],
        waypoints=[Waypoint(name="SPAWN", x=5, y=6)],
    )
    result = document_summary(document)
    assert result["dimensions"] == {"width": 64, "height": 64}
    assert result["objects"][0]["asset"] == "TestTank"
    assert result["waypoints"][0]["name"] == "SPAWN"
