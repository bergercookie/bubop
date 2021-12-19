"""Serialization utilities."""

import pickle
from pathlib import Path
from typing import Any, Union


def pickle_dump(item: Any, path: Union[Path, str], *, protocol=0, **kargs):
    """Helper method to serialize your dictionary to the given path.

    By default use protocol 0.
    """
    with Path(path).open("wb") as f:
        pickle.dump(item, f, **kargs, protocol=protocol)


def pickle_load(path: Union[Path, str]) -> Any:
    """Pickle-load using the given path."""
    with Path(path).open("rb") as f:
        return pickle.load(f)
