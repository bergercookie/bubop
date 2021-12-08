"""Miscellaneous utilities - not tied to a more specific module right now."""
from typing import Any


def get_object_unique_name(obj: Any) -> str:
    """Return a unique string associated with the given object.

    That string is constructed as follows: <object class name>_<object_hex_id>
    """

    return f"{type(obj).__name__}_{hex(id(obj))}"


def xor(*args) -> bool:
    """True if exactly one of the arguments of the iterable is True.

    >>> xor(0,1,0,)
    True
    >>> xor(1,2,3,)
    False
    >>> xor(False, False, False)
    False
    >>> xor("kalimera", "kalinuxta")
    False
    >>> xor("", "a", "")
    True
    >>> xor("", "", "")
    False
    """
    return sum([bool(i) for i in args]) == 1
