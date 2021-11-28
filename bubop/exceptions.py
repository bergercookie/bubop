class CustomException(BaseException):
    pass


class NoSuchFileOrDirectoryError(CustomException):
    """Exception raised when file/directory is not found."""

    def __init__(self, name):
        self.name = name
        self.msg = f"No such file or directory -> {name}"

    def __str__(self):
        return self.msg
