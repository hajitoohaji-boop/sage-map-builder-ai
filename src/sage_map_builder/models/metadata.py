"""Metadata model for a SAGE map document."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MapMetadata(BaseModel):
    """Validated metadata shared by map readers and writers."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    title: str = Field(min_length=1)
    width: int = Field(ge=64, le=512)
    height: int = Field(ge=64, le=512)

    @field_validator("width", "height")
    @classmethod
    def dimensions_must_be_multiples_of_64(cls, value: int) -> int:
        if value % 64 != 0:
            raise ValueError("map dimensions must be multiples of 64")
        return value
