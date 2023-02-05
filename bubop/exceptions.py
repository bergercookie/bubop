"""Custom Exceptions."""

from typing import Any, Optional


class NoSuchFileOrDirectoryError(BaseException):
    """Exception raised when file/directory is not found."""

    def __init__(self, name):
        super().__init__(f"No such file or directory -> {name}")


class OperatingSystemNotSupportedError(BaseException):
    """
    Exception raised when an operation is not supported for the OS at hand.
    """

    def __init__(self, os_name: str):
        super().__init__(f"Operation is not supported for this OS -> {os_name}")


class CliIncompatibleOptionsError(BaseException):
    """
    Exception raised when incompatible options are given in the CLI of a program.
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
        self, prefix: str, num_required: int, *args, num_given: Optional[int] = None, **kargs
    ):
        args_str1 = " | ".join(kargs.values())
        args_str2 = " | ".join(args)
        args_str = f"{args_str1} {args_str2}"
        s = f"{prefix} {num_required} of the following arguments are required:\n\t{args_str}"
        if num_given is not None:
            s += f"\n\nOnly {num_given} were given."
        super().__init__(s)


class AtLeastNOptionsRequired(NOptionsRequired):
    """AtLeastNOptionsRequired exception."""

    def __init__(self, *args, **kargs):
        super().__init__(prefix="At least", *args, **kargs)


class ExactlyNOptionsRequired(NOptionsRequired):
    """ExactlyNOptionsRequired exception."""

    def __init__(self, *args, **kargs):
        super().__init__(prefix="Exactly", *args, **kargs)


class Exactly1OptionRequired(ExactlyNOptionsRequired):
    """Exactly1OptionRequired exception."""

    def __init__(self, *args, **kargs):
        super().__init__(num_required=1, *args, **kargs)


class NotEnoughArgumentsError(BaseException):
    """
    Exception raised when incompatible options are given in the CLI of a program.

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
