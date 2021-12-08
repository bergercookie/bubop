class CustomException(BaseException):
    pass


class NoSuchFileOrDirectoryError(CustomException):
    """Exception raised when file/directory is not found."""

    def __init__(self, name):
        self._name = name
        self._msg = f"No such file or directory -> {name}"

    def __str__(self):
        return self._msg


class OperatingSystemNotSupportedError(CustomException):
    """Exception raised when an operation is not supported for the OS at hand."""

    def __init__(self, os_name: str):
        self._os_name: str = os_name
        self._msg = f"Operation is not supported for this OS -> {self._os_name}"

    def __str__(self):
        return self._msg
