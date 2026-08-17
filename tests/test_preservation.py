from pathlib import Path
from sage_map_builder.map.preservation import preserve_bytes, preserve_file


def test_preserve_bytes_is_exact():
    source = bytes(range(256))
    output = preserve_bytes(source)
    assert output == source
    assert output is not source


def test_preserve_file_is_byte_identical(tmp_path: Path):
    source = tmp_path / "source.map"
    output = tmp_path / "output.map"
    data = bytes(range(256)) * 3
    source.write_bytes(data)
    result = preserve_file(source, output)
    assert result.identical
    assert output.read_bytes() == data
