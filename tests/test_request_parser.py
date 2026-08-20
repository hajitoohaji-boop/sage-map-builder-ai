from sage_map_builder.ai.request import MapRequest
from sage_map_builder.ai.request_parser import detect_language, request_to_intent


def test_detects_arabic_and_english():
    assert detect_language("اصنع خريطة صحراوية") == "ar"
    assert detect_language("Create a desert map") == "en"


def test_extracts_explicit_dimensions_only():
    intent = request_to_intent(MapRequest("اصنع خريطة 512x256 للصحراء"))
    assert (intent.width, intent.height) == (512, 256)
    assert intent.description.startswith("اصنع")


def test_defaults_when_dimensions_are_not_explicit():
    intent = request_to_intent(MapRequest("Create a desert map"))
    assert (intent.width, intent.height) == (256, 256)
