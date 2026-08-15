import pytest
from pydantic import ValidationError

from sage_map_builder.models import MapMetadata


def test_valid_metadata() -> None:
    metadata = MapMetadata(title="Test Map", width=512, height=256)
    assert metadata.title == "Test Map"
    assert metadata.width == 512
    assert metadata.height == 256


@pytest.mark.parametrize("width", [63, 65, 127, 513])
def test_invalid_width(width: int) -> None:
    with pytest.raises(ValidationError):
        MapMetadata(title="Test Map", width=width, height=256)


def test_unknown_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        MapMetadata(title="Test Map", width=256, height=256, unknown="bad")
