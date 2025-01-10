"""Class and metaclass-related utilities."""
from typing import Any


def all_subclasses(cls: type[Any]) -> set[type[Any]]:
    """Recursively get all the (reachable) subclasses of the given class."""

    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]
    )
