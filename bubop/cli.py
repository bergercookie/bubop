"""CLI-related utilities."""
from typing import Any

from bubop.exceptions import CliIncompatibleOptionsError, Exactly1OptionRequired
from bubop.inspect import inspect_var_name
from bubop.misc import xor


def check_required_mutually_exclusive(
    arg1: Any, arg2: Any, arg1_name: str, arg2_name: str
) -> None:
    """
    Check if the given mutually exclusive args indeed hold the said required rule (required +
    mutual exclusivity)

    Raise exception if they don't uphold the rule.
    """

    if not arg1 and not arg2:
        raise Exactly1OptionRequired(num_given=0, opt1=arg1_name, opt2=arg2_name)

    if not xor(arg1, arg2):
        raise CliIncompatibleOptionsError(opt1=arg1_name, opt2=arg2_name)


def check_optional_mutually_exclusive(arg1: Any, arg2: Any) -> None:
    """
    Check if the given mutually exclusive args indeed hold the said required rule (optional +
    mutual exclusivity)

    Raise a CliIncompatibleOptionsError if they don't uphold the rule.

    >>> kalimera = 1
    >>> kalinuxta = 2
    >>> check_optional_mutually_exclusive(kalimera, kalinuxta)
    Traceback (most recent call last):
    bubop.exceptions.CliIncompatibleOptionsError: ... kalimera ... kalinuxta ...
    >>> kalimera = None
    >>> check_optional_mutually_exclusive(kalimera, kalinuxta) == None
    True
    >>> kalinuxta = None
    >>> check_optional_mutually_exclusive(kalimera, kalinuxta) == None
    True
    """
    if arg1 and arg2:
        raise CliIncompatibleOptionsError(
            opt1=inspect_var_name(arg1, level=2), opt2=inspect_var_name(arg2, level=2)
        )
