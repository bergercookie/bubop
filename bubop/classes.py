"""Class and metaclass-related utilities."""

from typing import Any


def all_subclasses(cls: type[Any]) -> set[type[Any]]:
    """Recursively get all the (reachable) subclasses of the given class.

    Usage::

        >>> class Foo: pass
        >>> class Bar(Foo): pass
        >>> class Baz(Foo): pass
        >>> class Bing(Bar): pass
        >>> sorted([c.__name__ for c in all_subclasses(Foo)])
        ['Bar', 'Baz', 'Bing']



    """

    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)]
    )
