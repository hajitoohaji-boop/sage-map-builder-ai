from pathlib import Path

import pytest

from sage_map_builder.map.preservation_writer import write_preserved


SAMPLES = (
    "MY MAP.map",
    "CONTRA Custom Campaign The Battle for Lake Town.map",
)


@pytest.mark.parametrize("name", SAMPLES)
def test_real_sample_untouched_preservation(name: str, tmp_path: Path):
    source = Path(name)
    if not source.exists():
        pytest.skip(f"reference sample is not present: {name}")

    original = source.read_bytes()
    output = tmp_path / name
    write_preserved(original, output)

    assert output.read_bytes() == original
