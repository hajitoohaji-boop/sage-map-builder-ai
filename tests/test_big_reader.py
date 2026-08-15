import struct

import pytest

from sage_map_builder.mods.big_reader import BigFormatError, read_big


def make_big() -> bytes:
    name = b"Data\\INI\\test.ini\x00"
    payload = b"Object Test\n"
    directory_size = 12 + 8 + len(name)
    offset = directory_size
    return b"BIGF" + struct.pack(">II", 1, offset + len(payload)) + struct.pack(">II", offset, len(payload)) + name + payload


def test_big_entry_can_be_read() -> None:
    archive = read_big(make_big())
    assert archive.read("data/ini/test.ini") == b"Object Test\n"


def test_big_rejects_bad_archive_size() -> None:
    data = b"BIGF" + struct.pack(">II", 0, 999)
    with pytest.raises(BigFormatError):
        read_big(data)
