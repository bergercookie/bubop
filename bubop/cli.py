"""CLI-related utilities."""
from typing import Any

from bubop.exceptions import CliIncompatibleOptionsError
from bubop.inspect import inspect_var_name
from bubop.misc import xor


def check_required_mutually_exclusive(arg1: Any, arg2: Any) -> None:
    """
    Check if the given mutually exclusive args indeed hold the said required rule (required +
    mutual exclusivity)

    Raise a CliIncompatibleOptionsError if they don't uphold the rule.
    """
    if not xor(arg1, arg2):
        raise CliIncompatibleOptionsError(
            opt1=inspect_var_name(arg1, level=2), opt2=inspect_var_name(arg2, level=2)
        )


def check_optional_mutually_exclusive(arg1: Any, arg2: Any) -> None:
    """
    Check if the given mutually exclusive args indeed hold the said required rule (optional +
    mutual exclusivity)

    Raise a CliIncompatibleOptionsError if they don't uphold the rule.
    """
    if arg1 and arg2:
        raise CliIncompatibleOptionsError(
            opt1=inspect_var_name(arg1, level=2), opt2=inspect_var_name(arg2, level=2)
        )
