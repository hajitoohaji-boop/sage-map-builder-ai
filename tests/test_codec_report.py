from sage_map_builder.formats.codec_report import render_codec_report


def test_codec_report_is_deterministic():
    report = render_codec_report(("WaypointsList",))
    assert "WaypointsList v1" in report
    assert "verified" in report
    assert report.endswith("\n")
