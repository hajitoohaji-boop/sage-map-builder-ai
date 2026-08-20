from sage_map_builder.map.forensics import (
    ForensicMapSummary,
    MapObjectRecord,
    PlayerRecord,
    TeamRecord,
)


def test_forensic_records_match_observed_map_dump_fields():
    obj = MapObjectRecord(
        unique_id="Boss_ChinaTankDragon 79",
        original_owner="team0006",
        veterancy=3,
    )
    team = TeamRecord(name="team0006", owner="PlyrAmerica")
    player = PlayerRecord(
        name="PlyrAmericaBossGeneral",
        human=True,
        display_name="PlyrAmericaBossGeneral",
        faction="FactionAmericaBossGeneral",
    )
    summary = ForensicMapSummary(
        weather=0,
        objects=(obj,),
        teams=(team,),
        players=(player,),
        script_blocks=("ATTACK",),
    )
    assert summary.object_count == 1
    assert summary.team_count == 1
    assert summary.player_count == 1
    assert summary.script_count == 1
    assert summary.objects[0].veterancy == 3
    assert summary.players[0].faction == "FactionAmericaBossGeneral"
