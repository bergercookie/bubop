"""Custom Exceptions."""

from typing import Any


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
