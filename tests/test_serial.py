from pathlib import Path

import pytest

from bubop import serial


@pytest.mark.parametrize("fs", [[None, [serial]]], indirect=True)
def test_pickle_unpickle(fs):
    item = {1: 2, 2: 3, 3: 4}
    path = Path("file")
    serial.pickle_dump(item=item, path=path)
    assert serial.pickle_load(path=path) == item
