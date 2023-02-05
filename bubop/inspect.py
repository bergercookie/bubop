"""Runtime-related utilities - making use of the inspect module."""
import inspect
from typing import Any, Optional

from bubop.exceptions import TooShallowStackError


def inspect_var_name(var: Any, level=2) -> Optional[str]:
    """Retrieve the name of the variable `var` passed from the caller to this function.

    Use the `level` argument to refer to the argument name of the caller's caller (level=2) or
    the caller's caller's caller, (level=3) etc. instead.

    Quite experimental function in nature, may not work as expected.

    Usage::

    >>> var1 = "kalimera"
    >>> inspect_var_name(var1, level=1)
    'var1'
    >>> fn = lambda x: (inspect_var_name(x, level=1), inspect_var_name(x))
    >>> fn(var1)
    ('x', 'var1')
    >>> inspect_var_name(var1, level=1000) == None
    Traceback (most recent call last):
    bubop.exceptions.TooShallowStackError: Stack has less ...
    >>> inspect_var_name(1, level=1) == None
    True
    """
    currframe = inspect.currentframe()

    # walk up the stack, find the right frame
    while level > 0:
        if currframe is None:
            raise TooShallowStackError()

        currframe = currframe.f_back
        level -= 1

    if currframe is None:
        raise TooShallowStackError()

    callers_local_vars = currframe.f_locals.items()

    li = [var_name for var_name, var_val in callers_local_vars if var_val is var]
    if li:
        return li[-1]

    return None
