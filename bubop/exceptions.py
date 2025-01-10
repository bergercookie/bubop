"""Custom Exceptions."""

from typing import Any


class NoSuchFileOrDirectoryError(BaseException):
    """Exception raised when file/directory is not found.

    Usage::

        >>> raise NoSuchFileOrDirectoryError("foo")
        Traceback (most recent call last):
        bubop.exceptions.NoSuchFileOrDirectoryError: No such file or directory -> foo

    """

    def __init__(self, name):
        super().__init__(f"No such file or directory -> {name}")


class OperatingSystemNotSupportedError(BaseException):
    """
    Exception raised when an operation is not supported for the OS at hand.

    Usage::

        >>> raise OperatingSystemNotSupportedError("Windows")
        Traceback (most recent call last):
        bubop.exceptions.OperatingSystemNotSupportedError: Operation is not supported for this OS -> Windows
    """

    def __init__(self, os_name: str):
        super().__init__(f"Operation is not supported for this OS -> {os_name}")


class CliIncompatibleOptionsError(BaseException):
    """
    Exception raised when incompatible options are given in the CLI of a program.

    Usage::

        >>> raise CliIncompatibleOptionsError("foo", "bar")
        Traceback (most recent call last):
        bubop.exceptions.CliIncompatibleOptionsError: Provided option groups foo and bar are incompatible with each other
    """

    def __init__(self, opt1: Any, opt2: Any):
        super().__init__(
            f"Provided option groups {opt1} and {opt2} are incompatible with each other"
        )


class NOptionsRequired(BaseException):
    """
    Exception raised when at least N of the given options were required
    """

    def __init__(
        self, prefix: str, num_required: int, *args, num_given: int | None = None, **kargs
    ):
        args_str1 = " | ".join(kargs.values())
        args_str2 = " | ".join(args)
        args_str = f"{args_str1} {args_str2}"
        s = f"{prefix} {num_required} of the following arguments are required:\n\t{args_str}"
        if num_given is not None:
            s += f"\n\nOnly {num_given} were given."
        super().__init__(s)


class AtLeastNOptionsRequired(NOptionsRequired):
    """AtLeastNOptionsRequired exception.

    Usage::

        >>> raise AtLeastNOptionsRequired(num_required=2, foo="bar", baz="bing")
        Traceback (most recent call last):
        bubop.exceptions.AtLeastNOptionsRequired: At least 2 of the following arguments are required:

    """

    def __init__(self, *args, **kargs):
        super().__init__(prefix="At least", *args, **kargs)


class ExactlyNOptionsRequired(NOptionsRequired):
    """ExactlyNOptionsRequired exception.

    Usage::

        >>> raise ExactlyNOptionsRequired(num_required=2, foo="bar", baz="bing")
        Traceback (most recent call last):
        bubop.exceptions.ExactlyNOptionsRequired: Exactly 2 of the following arguments are required:
        ...
    """

    def __init__(self, *args, **kargs):
        super().__init__(prefix="Exactly", *args, **kargs)


class Exactly1OptionRequired(ExactlyNOptionsRequired):
    """Exactly1OptionRequired exception.

    Usage::

        >>> raise Exactly1OptionRequired(num_given=0, foo="bar", baz="bing")
        Traceback (most recent call last):
        bubop.exceptions.Exactly1OptionRequired: Exactly 1 of the following arguments are required:
        ...
    """

    def __init__(self, *args, **kargs):
        super().__init__(num_required=1, *args, **kargs)


class NotEnoughArgumentsError(BaseException):
    """
    Exception raised when incompatible options are given in the CLI of a program.

    Usage::

        >>> raise NotEnoughArgumentsError()
        Traceback (most recent call last):
        bubop.exceptions.NotEnoughArgumentsError: ...
    """

    def __init__(self):
        super().__init__("Not enough arguments provided")


class TooShallowStackError(BaseException):
    """
    Exception raised when the stack trace does not have as many frames as expected.
    """

    def __init__(self):
        super().__init__("Stack has less frames than expected")


class ApplicationNotInstalled(BaseException):
    """
    Exception raised when a required application is not installed on the system.
    """

    def __init__(self, appname: str):
        super().__init__(f"Application {appname} is not installed")


class AuthenticationError(BaseException):
    """
    Exception raised when authentication with a certain application/service failed
    """

    def __init__(self, appname: str):
        super().__init__(f"Authentication with {appname} failed.")
