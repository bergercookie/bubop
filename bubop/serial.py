"""Serialization utilities."""

import pickle
from pathlib import Path
from typing import Any, Union


def pickle_dump(item: Any, path: Union[Path, str], *, protocol=0, **kargs):
    """Helper method to serialize your dictionary to the given path

    By default use protocol 4 which is the default for Python 3.8 - added in Python 3.4.
    """
    with Path(path).open("wb") as f:
        pickle.dump(item, f, **kargs, protocol=protocol)


def pickle_load(path: Union[Path, str]) -> Any:
    """Pickle-load using the given path."""
    return pickle.load(Path(path).open("rb"))
